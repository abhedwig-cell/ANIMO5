#!/usr/bin/env python3
"""Executable synthetic ARCH07 case subset for ANIMO-TIMEQ02."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from timeq01_runtime_fixture import ContractError, PHYSICAL, RuntimeFixture  # noqa: E402
from timeq02_adapter_fixture import (  # noqa: E402
    AdapterBinding,
    AdapterConfig,
    CROP,
    HYDRO,
    FieldValue,
    FrameAdapter,
    active_field_ids,
    begin_runtime_with_frames,
    build_valid_frame,
    derive_static_identities,
    load_field_schema,
    replace_field,
)


class TimeQ02AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_field_schema(ROOT)

    def binding(self, **kwargs):
        return replace(AdapterBinding(), **kwargs)

    def adapter(self, binding=None, generation=0):
        return FrameAdapter(self.schema, binding or AdapterBinding(), generation)

    def runtime(self, binding=None, owners=None, values=None):
        b = binding or AdapterBinding()
        return RuntimeFixture(
            values or {"soil_N": 10.0, "soil_P": 5.0},
            owners or {"ANIMO": 0, "HYDRO": 0, "CROP": 0},
            topology_id=b.physical_layout_id,
            config_id=b.configuration_identity,
            geometry_id=b.geometry_id,
        )

    def hydro(self, cfg=None, binding=None, frame_id="H-F1", interval="I1", trial="T1", generation=0, metadata=None):
        return build_valid_frame(self.schema, HYDRO, cfg or AdapterConfig(), binding or AdapterBinding(), frame_id=frame_id, interval_id=interval, trial_id=trial, accepted_generation=generation, metadata=metadata)

    def crop(self, cfg=None, binding=None, frame_id="C-F1", interval="I1", trial="T1", generation=0, metadata=None):
        return build_valid_frame(self.schema, CROP, cfg or AdapterConfig(), binding or AdapterBinding(), frame_id=frame_id, interval_id=interval, trial_id=trial, accepted_generation=generation, metadata=metadata)

    def begin_pair(self, runtime, hydro, crop, trial="T1", interval="I1"):
        begin_runtime_with_frames(runtime, [hydro, crop], interval_id=interval, trial_id=trial, t0=0, t1=1, participants=["ANIMO", "HYDRO", "CROP"])

    def test_H001_valid_detailed_frame(self):
        cfg = AdapterConfig(hydrology_mode="detailed")
        frame = self.hydro(cfg)
        self.assertIs(self.adapter().validate(frame, cfg), frame)
        self.assertIn("HYD-INTERCEPTION-BEGIN", frame.fields)
        self.assertIn("HYD-PRECIP-IN", frame.fields)

    def test_H002_valid_aggregated_frame(self):
        cfg = AdapterConfig(hydrology_mode="aggregated")
        frame = self.hydro(cfg)
        self.adapter().validate(frame, cfg)
        self.assertNotIn("HYD-INTERCEPTION-BEGIN", frame.fields)
        self.assertNotIn("HYD-PRECIP-IN", frame.fields)
        self.assertIn("HYD-MATRIX-WATER-BEGIN", frame.fields)

    def test_H003_missing_required_field(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg)
        fields = dict(frame.fields)
        fields.pop("HYD-MATRIX-WATER-BEGIN")
        with self.assertRaises(ContractError):
            self.adapter().validate(replace(frame, fields=fields), cfg)

    def test_H004_forbidden_conditional_field(self):
        cfg = AdapterConfig(hydrology_mode="aggregated")
        frame = self.hydro(cfg)
        spec = self.schema["HYD-INTERCEPTION-BEGIN"]
        fields = dict(frame.fields)
        fields[spec.field_id] = FieldValue(1.0, spec.unit, spec.shape)
        with self.assertRaises(ContractError):
            self.adapter().validate(replace(frame, fields=fields), cfg)

    def test_H005_unit_mismatch(self):
        cfg = AdapterConfig()
        frame = replace_field(self.hydro(cfg), "HYD-BOTTOM-WATER", unit="mm_per_day")
        with self.assertRaises(ContractError):
            self.adapter().validate(frame, cfg)

    def test_H006_shape_mismatch(self):
        cfg = AdapterConfig()
        frame = replace_field(self.hydro(cfg), "HYD-MATRIX-WATER-BEGIN", shape="profile_scalar")
        with self.assertRaises(ContractError):
            self.adapter().validate(frame, cfg)

    def test_H007_sign_normalization(self):
        cfg = AdapterConfig()
        adapter = self.adapter()
        frame = replace_field(self.hydro(cfg), "HYD-BOTTOM-WATER", value=2.5)
        normalized = adapter.normalize_sign(frame, {"HYD-BOTTOM-WATER": -1.0}, new_frame_id="H-F2")
        adapter.validate(normalized, cfg)
        self.assertEqual(normalized.fields["HYD-BOTTOM-WATER"].value, -2.5)
        self.assertEqual(frame.fields["HYD-BOTTOM-WATER"].value, 2.5)

    def test_H008_frame_immutability(self):
        cfg = AdapterConfig()
        adapter = self.adapter()
        frame = self.hydro(cfg)
        adapter.validate(frame, cfg)
        changed = replace_field(frame, "HYD-BOTTOM-WATER", value=9.0)
        with self.assertRaises(ContractError):
            adapter.validate(changed, cfg)

    def test_H009_accepted_generation_mismatch(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg, generation=1)
        with self.assertRaises(ContractError):
            self.adapter(generation=0).validate(frame, cfg)

    def test_H010_layout_and_geometry_mismatch(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg)
        with self.assertRaises(ContractError):
            self.adapter(self.binding(physical_layout_id="layout-B")).validate(frame, cfg)
        with self.assertRaises(ContractError):
            self.adapter(self.binding(geometry_id="geometry-B")).validate(frame, cfg)

    def test_H011_configuration_and_exchange_binding_mismatch(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg)
        with self.assertRaises(ContractError):
            self.adapter(self.binding(configuration_identity="configuration-B")).validate(frame, cfg)
        with self.assertRaises(ContractError):
            self.adapter(self.binding(exchange_binding_id="exchange-binding-B")).validate(frame, cfg)

    def test_H012_chemical_boundary_separation(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg, metadata={"solute_concentration_NH4": 3.0})
        with self.assertRaises(ContractError):
            self.adapter().validate(frame, cfg)

    def test_H013_interception_storage_ledger_observability(self):
        cfg = AdapterConfig(hydrology_mode="detailed")
        frame = self.hydro(cfg)
        frame = replace_field(frame, "HYD-INTERCEPTION-BEGIN", value=0.002)
        frame = replace_field(frame, "HYD-INTERCEPTION-END", value=0.001)
        frame = replace_field(frame, "HYD-EVAP-INTERCEPTION", value=0.0005)
        self.adapter().validate(frame, cfg)
        self.assertGreater(frame.fields["HYD-INTERCEPTION-BEGIN"].value, 0)
        self.assertGreater(frame.fields["HYD-EVAP-INTERCEPTION"].value, 0)

    def test_H014_macropore_disabled_rejects_fields(self):
        cfg = AdapterConfig(macropore_enabled=False)
        frame = self.hydro(cfg)
        spec = self.schema["HYD-MP-WATER-BEGIN"]
        fields = dict(frame.fields)
        fields[spec.field_id] = FieldValue([1.0], spec.unit, spec.shape)
        with self.assertRaises(ContractError):
            self.adapter().validate(replace(frame, fields=fields), cfg)

    def test_H015_macropore_without_admission(self):
        cfg = AdapterConfig(macropore_enabled=True, macropore_admitted=False)
        frame = self.hydro(cfg)
        with self.assertRaises(ContractError):
            self.adapter().validate(frame, cfg)

    def test_C001_valid_external_crop_frame_nonowner(self):
        cfg = AdapterConfig(crop_mode="external")
        frame = self.crop(cfg)
        self.adapter().validate(frame, cfg)
        runtime = self.runtime(values={"soil_N": 10.0})
        self.assertNotIn("CROP-ACTIVE", runtime.accepted_values)

    def test_C002_owner_mode_mismatch(self):
        frame = self.crop(AdapterConfig(crop_mode="external"))
        with self.assertRaises(ContractError):
            self.adapter().validate(frame, AdapterConfig(crop_mode="none"))

    def test_C003_demand_unit_and_shape_mismatch(self):
        cfg = AdapterConfig(n_uptake_active=True)
        frame = self.crop(cfg)
        with self.assertRaises(ContractError):
            self.adapter().validate(replace_field(frame, "CROP-N-DEMAND", unit="kg_per_day"), cfg)
        with self.assertRaises(ContractError):
            self.adapter().validate(replace_field(frame, "CROP-N-DEMAND", shape="wrong_shape"), cfg)

    def test_C004_root_distribution_contract(self):
        cfg = AdapterConfig(root_distribution_required=True)
        frame = self.crop(cfg)
        self.adapter().validate(frame, cfg)
        with self.assertRaises(ContractError):
            self.adapter().validate(replace(frame, frame_id="C-F2", metadata={}), cfg)

    def test_C005_realized_n_uptake_link(self):
        cfg = AdapterConfig(n_uptake_active=True)
        b = AdapterBinding()
        h = self.hydro(AdapterConfig(), b, trial="T1")
        c = self.crop(cfg, b, trial="T1")
        self.adapter(b).validate(h, AdapterConfig())
        self.adapter(b).validate(c, cfg)
        rt = self.runtime(b)
        self.begin_pair(rt, h, c)
        rt.emit_event(event_id="N-UP", kind=PHYSICAL, source="soil_N", target="crop_N", amount=2.0, metadata={"quantity": "N"})
        result = self.adapter(b).link_realized_uptake(rt, quantity="N", amount=2.0, event_id="N-UP")
        self.assertEqual(result["trial_id"], "T1")

    def test_C006_realized_p_uptake_link(self):
        cfg = AdapterConfig(p_uptake_active=True)
        b = AdapterBinding()
        h = self.hydro(AdapterConfig(), b, trial="T1")
        c = self.crop(cfg, b, trial="T1")
        rt = self.runtime(b)
        self.begin_pair(rt, h, c)
        rt.emit_event(event_id="P-UP", kind=PHYSICAL, source="soil_P", target="crop_P", amount=1.5, metadata={"quantity": "P"})
        result = self.adapter(b).link_realized_uptake(rt, quantity="P", amount=1.5, event_id="P-UP")
        self.assertEqual(result["amount"], 1.5)

    def test_C007_rejected_uptake_result(self):
        cfg = AdapterConfig(n_uptake_active=True)
        b = AdapterBinding()
        h = self.hydro(AdapterConfig(), b)
        c = self.crop(cfg, b)
        rt = self.runtime(b)
        self.begin_pair(rt, h, c)
        rt.emit_event(event_id="N-UP", kind=PHYSICAL, source="soil_N", target="crop_N", amount=2.0, metadata={"quantity": "N"})
        self.adapter(b).link_realized_uptake(rt, quantity="N", amount=2.0, event_id="N-UP")
        rt.reject()
        self.assertEqual(rt.committed_events, [])
        self.assertEqual(rt.owner_generations, {"ANIMO": 0, "HYDRO": 0, "CROP": 0})

    def test_C008_residue_explicit_bundle(self):
        cfg = AdapterConfig(external_crop_generates_residue=True)
        frame = self.crop(cfg)
        self.adapter().validate(frame, cfg)
        self.assertTrue(frame.fields["CROP-RESIDUE-INPUT-BUNDLE"].value)

    def test_C009_residue_delta_inference_forbidden(self):
        with self.assertRaises(ContractError):
            self.adapter().forbid_state_delta_transfer_inference()

    def test_C010_external_export_explicit_bundle(self):
        cfg = AdapterConfig(combined_crop_ledger_requested=True)
        frame = self.crop(cfg)
        self.adapter().validate(frame, cfg)
        self.assertIn("CROP-EXTERNAL-EXPORT-BUNDLE", frame.fields)

    def test_C011_state_observation_nonownership(self):
        cfg = AdapterConfig(combined_crop_ledger_requested=True, crop_dm_ledger_requested=True)
        frame = self.crop(cfg)
        self.adapter().validate(frame, cfg)
        rt = self.runtime(values={"soil_N": 10.0, "soil_P": 5.0})
        for fid in ["CROP-N-BEGIN", "CROP-P-BEGIN", "CROP-SHOOT-DM-BEGIN", "CROP-ROOT-DM-BEGIN"]:
            self.assertIn(fid, frame.fields)
            self.assertNotIn(fid, rt.accepted_values)

    def test_C012_crop_frame_immutability(self):
        cfg = AdapterConfig()
        adapter = self.adapter()
        frame = self.crop(cfg)
        adapter.validate(frame, cfg)
        changed = replace_field(frame, "CROP-ACTIVE", value=False)
        with self.assertRaises(ContractError):
            adapter.validate(changed, cfg)

    def test_T001_begin_trial_binding(self):
        b = AdapterBinding()
        h = self.hydro(binding=b)
        c = self.crop(binding=b)
        self.adapter(b).validate(h, AdapterConfig())
        self.adapter(b).validate(c, AdapterConfig())
        rt = self.runtime(b)
        self.begin_pair(rt, h, c)
        self.assertEqual(rt.bound_frame_ids, ("H-F1", "C-F1"))
        self.assertEqual(rt.interval_id, "I1")
        self.assertEqual(rt.trial_id, "T1")

    def test_T002_reject_atomicity(self):
        b = AdapterBinding()
        h, c = self.hydro(binding=b), self.crop(binding=b)
        rt = self.runtime(b)
        before_values = dict(rt.accepted_values)
        before_owners = dict(rt.owner_generations)
        self.begin_pair(rt, h, c)
        rt.mutate("soil_N", 8.0)
        rt.emit_event(event_id="E", kind=PHYSICAL, source="soil_N", target="crop_N", amount=2.0, metadata={"quantity": "N"})
        rt.reject()
        self.assertEqual(rt.accepted_values, before_values)
        self.assertEqual(rt.owner_generations, before_owners)
        self.assertEqual(rt.committed_events, [])

    def test_T003_accept_commit_barrier(self):
        b = AdapterBinding()
        h, c = self.hydro(binding=b), self.crop(binding=b)
        rt = self.runtime(b)
        self.begin_pair(rt, h, c)
        rt.mutate("soil_N", 9.0)
        rt.mark_ready()
        with self.assertRaises(ContractError):
            rt.accept({"ANIMO": 1, "HYDRO": 1})
        self.assertEqual(rt.owner_generations, {"ANIMO": 0, "HYDRO": 0, "CROP": 0})
        rt.accept({"ANIMO": 1, "HYDRO": 1, "CROP": 1})
        self.assertEqual(rt.owner_generations, {"ANIMO": 1, "HYDRO": 1, "CROP": 1})

    def test_T004_retry_identity(self):
        b = AdapterBinding()
        rt = self.runtime(b)
        h1, c1 = self.hydro(binding=b, frame_id="H1", trial="T1"), self.crop(binding=b, frame_id="C1", trial="T1")
        self.begin_pair(rt, h1, c1, trial="T1")
        rt.reject()
        h2, c2 = self.hydro(binding=b, frame_id="H2", trial="T2"), self.crop(binding=b, frame_id="C2", trial="T2")
        self.begin_pair(rt, h2, c2, trial="T2")
        self.assertEqual(rt.bound_frame_ids, ("H2", "C2"))

    def test_T005_diagnostic_nonownership(self):
        b = AdapterBinding()
        rt = self.runtime(b)
        h, c = self.hydro(binding=b), self.crop(binding=b)
        self.begin_pair(rt, h, c)
        rt.record_trace("G_REPORT_ONLY", "adapter_validation", {"ok": True})
        rt.mark_ready()
        rt.accept({"ANIMO": 1, "HYDRO": 1, "CROP": 1})
        self.assertEqual(rt.committed_events, [])

    def test_T006_checkpoint_owner_split(self):
        b = AdapterBinding()
        rt = self.runtime(b)
        h, c = self.hydro(binding=b), self.crop(binding=b)
        packet = self.adapter(b).checkpoint_with_external_refs(rt, [h, c])
        self.assertEqual(packet["external_frame_refs"], ["H-F1", "C-F1"])
        self.assertIsNone(packet["external_persistent_state"])
        self.assertIn("accepted_values", packet["animo_checkpoint"])

    def test_T007_precision_reference_mismatch(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg)
        with self.assertRaises(ContractError):
            self.adapter(self.binding(precision_policy_ref="precision-other")).validate(frame, cfg)

    def test_I001_diagnostic_identity_invariance(self):
        a = derive_static_identities(layout_semantics="layers=2", feature_semantics="hydro=detailed;crop=external", parameter_set_id="P1", diagnostics_mode="off")
        b = derive_static_identities(layout_semantics="layers=2", feature_semantics="hydro=detailed;crop=external", parameter_set_id="P1", diagnostics_mode="detailed")
        self.assertEqual(a.physical_layout_id, b.physical_layout_id)
        self.assertEqual(a.feature_set_id, b.feature_set_id)
        self.assertEqual(a.configuration_identity, b.configuration_identity)
        self.assertEqual(a.exchange_binding_id, b.exchange_binding_id)
        self.assertNotEqual(a.observer_configuration_id, b.observer_configuration_id)

    def test_I002_parameter_configuration_change(self):
        a = derive_static_identities(layout_semantics="layers=2", feature_semantics="hydro=detailed;crop=external", parameter_set_id="P1", diagnostics_mode="off")
        b = derive_static_identities(layout_semantics="layers=2", feature_semantics="hydro=detailed;crop=external", parameter_set_id="P2", diagnostics_mode="off")
        self.assertEqual(a.physical_layout_id, b.physical_layout_id)
        self.assertEqual(a.exchange_binding_id, b.exchange_binding_id)
        self.assertNotEqual(a.configuration_identity, b.configuration_identity)

    def test_I003_feature_layout_change_rejects_stale_frame(self):
        cfg = AdapterConfig()
        old_binding = AdapterBinding()
        frame = self.hydro(cfg, old_binding)
        new_binding = self.binding(physical_layout_id="layout-new", feature_set_id="features-new", exchange_binding_id="exchange-new", configuration_identity="config-new")
        with self.assertRaises(ContractError):
            self.adapter(new_binding).validate(frame, cfg)

    def test_I004_schema_version_change_rejected(self):
        cfg = AdapterConfig()
        frame = self.hydro(cfg)
        new_binding = self.binding(exchange_contract_schema_id="ARCH05-EXCHANGE-v2")
        with self.assertRaises(ContractError):
            self.adapter(new_binding).validate(frame, cfg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
