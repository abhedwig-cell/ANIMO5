#!/usr/bin/env python3
"""Schema-driven non-production adapter fixtures for ANIMO-TIMEQ02.

The implementation instantiates candidate ARCH05 exchange and TIMEQ01
transaction contracts with synthetic external producers. It contains no ANIMO,
SWAP or WOFOST process physics and produces no historical B2 evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from copy import deepcopy
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional, Sequence, Tuple

from timeq01_runtime_fixture import ContractError, Frame as TimeFrame, PHYSICAL, RuntimeFixture


HYDRO = "EX-HYDROLOGY"
CROP = "EX-CROP-EXTERNAL"


@dataclass(frozen=True)
class FieldSchema:
    field_id: str
    domain: str
    unit: str
    shape: str
    required_when: str
    sign_or_direction: str
    qualification_status: str


@dataclass(frozen=True)
class FieldValue:
    value: Any
    unit: str
    shape: str


@dataclass(frozen=True)
class AdapterConfig:
    hydrology_mode: str = "detailed"
    snow_enabled: bool = False
    macropore_enabled: bool = False
    macropore_admitted: bool = False
    lateral_drainage_exists: bool = False
    lateral_infiltration_exists: bool = False
    runon_exists: bool = False
    irrigation_exists: bool = False
    crop_or_root_uptake_active: bool = False
    crop_mode: str = "external"
    root_distribution_required: bool = False
    n_uptake_active: bool = False
    p_uptake_active: bool = False
    combined_crop_ledger_requested: bool = False
    crop_dm_ledger_requested: bool = False
    external_crop_generates_residue: bool = False


@dataclass(frozen=True)
class AdapterBinding:
    exchange_contract_schema_id: str = "ARCH05-EXCHANGE-v1"
    transaction_schema_id: str = "TIME01-TRANSACTION-v1"
    physical_layout_id: str = "layout-A"
    geometry_id: str = "geometry-A"
    feature_set_id: str = "features-A"
    precision_policy_ref: str = "precision-candidate-A"
    configuration_identity: str = "configuration-A"
    exchange_binding_id: str = "exchange-binding-A"
    hydrology_exchange_schema_id: str = "ARCH05-HYDROLOGY-v1"
    crop_exchange_schema_id: str = "ARCH05-CROP-v1"


@dataclass(frozen=True)
class ProducerFrame:
    domain: str
    frame_id: str
    interval_id: str
    trial_id: str
    t0: Any
    t1: Any
    accepted_generation: int
    producer_model_id: str
    producer_model_version: str
    producer_accepted_snapshot_id: str
    exchange_contract_schema_id: str
    transaction_schema_id: str
    physical_layout_id: str
    geometry_id: str
    feature_set_id: str
    precision_policy_ref: str
    configuration_identity: str
    exchange_binding_id: str
    domain_schema_id: str
    fields: Mapping[str, FieldValue]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def signature(self) -> str:
        def encode_field(fv: FieldValue) -> Mapping[str, Any]:
            return {"value": fv.value, "unit": fv.unit, "shape": fv.shape}

        body = {
            "domain": self.domain,
            "frame_id": self.frame_id,
            "interval_id": self.interval_id,
            "trial_id": self.trial_id,
            "t0": self.t0,
            "t1": self.t1,
            "accepted_generation": self.accepted_generation,
            "producer_model_id": self.producer_model_id,
            "producer_model_version": self.producer_model_version,
            "producer_accepted_snapshot_id": self.producer_accepted_snapshot_id,
            "exchange_contract_schema_id": self.exchange_contract_schema_id,
            "transaction_schema_id": self.transaction_schema_id,
            "physical_layout_id": self.physical_layout_id,
            "geometry_id": self.geometry_id,
            "feature_set_id": self.feature_set_id,
            "precision_policy_ref": self.precision_policy_ref,
            "configuration_identity": self.configuration_identity,
            "exchange_binding_id": self.exchange_binding_id,
            "domain_schema_id": self.domain_schema_id,
            "fields": {k: encode_field(v) for k, v in sorted(self.fields.items())},
            "metadata": self.metadata,
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":"))

    def to_time_frame(self) -> TimeFrame:
        return TimeFrame(
            frame_id=self.frame_id,
            interval_id=self.interval_id,
            accepted_generation=self.accepted_generation,
            topology_id=self.physical_layout_id,
            config_id=self.configuration_identity,
            geometry_id=self.geometry_id,
            payload={"producer_frame_signature": self.signature(), "domain": self.domain},
        )


def load_field_schema(repository_root: Path) -> Dict[str, FieldSchema]:
    path = repository_root / "integration/animo-architecture/ARCH05_EXCHANGE_FIELDS.csv"
    result: Dict[str, FieldSchema] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result[row["field_id"]] = FieldSchema(
                field_id=row["field_id"],
                domain=row["domain"],
                unit=row["unit_semantics"],
                shape=row["shape"],
                required_when=row["required_when"],
                sign_or_direction=row["sign_or_direction"],
                qualification_status=row["qualification_status"],
            )
    if len(result) != 42:
        raise ContractError(f"expected 42 ARCH05 exchange fields, observed {len(result)}")
    return result


def condition_active(expr: str, cfg: AdapterConfig) -> bool:
    table = {
        "always_for_transport": True,
        "hydrology_mode=detailed": cfg.hydrology_mode == "detailed",
        "snow_enabled=true": cfg.snow_enabled,
        "when_lateral_drainage_exists": cfg.lateral_drainage_exists,
        "when_lateral_infiltration_exists": cfg.lateral_infiltration_exists,
        "when_runon_exists": cfg.runon_exists,
        "always_for_detailed_water_ledger": cfg.hydrology_mode == "detailed",
        "when_irrigation_exists": cfg.irrigation_exists,
        "when_crop_or_root_uptake_active": cfg.crop_or_root_uptake_active,
        "macropore_enabled=true AND macropore_admitted": cfg.macropore_enabled and cfg.macropore_admitted,
        "crop_mode=external": cfg.crop_mode == "external",
        "crop_mode=external AND root_distribution_required": cfg.crop_mode == "external" and cfg.root_distribution_required,
        "crop_mode=external AND N_uptake_active": cfg.crop_mode == "external" and cfg.n_uptake_active,
        "crop_mode=external AND P_uptake_active": cfg.crop_mode == "external" and cfg.p_uptake_active,
        "crop_mode=external AND combined_crop_ledger_requested": cfg.crop_mode == "external" and cfg.combined_crop_ledger_requested,
        "crop_mode=external AND crop_dm_ledger_requested": cfg.crop_mode == "external" and cfg.crop_dm_ledger_requested,
        "crop_mode=external AND external_crop_generates_residue": cfg.crop_mode == "external" and cfg.external_crop_generates_residue,
    }
    if expr not in table:
        raise ContractError(f"unsupported ARCH05 required_when expression: {expr}")
    return table[expr]


def active_field_ids(schema: Mapping[str, FieldSchema], domain: str, cfg: AdapterConfig) -> Tuple[str, ...]:
    return tuple(sorted(fid for fid, spec in schema.items() if spec.domain == domain and condition_active(spec.required_when, cfg)))


def _dummy_value(spec: FieldSchema) -> Any:
    if spec.field_id == "CROP-ACTIVE":
        return True
    if spec.shape == "event_list":
        quantity = "dry_matter" if "RESIDUE" in spec.field_id else "external_export"
        return [{"source": "external_crop", "target": "soil" if "RESIDUE" in spec.field_id else "external", "quantity": quantity, "amount": 1.0, "unit": "explicit"}]
    if "layer_count" in spec.shape or "interface" in spec.shape or "domain_shape" in spec.shape:
        return [1.0]
    return 1.0


def build_valid_frame(
    schema: Mapping[str, FieldSchema],
    domain: str,
    cfg: AdapterConfig,
    binding: AdapterBinding,
    *,
    frame_id: str,
    interval_id: str = "I1",
    trial_id: str = "T1",
    t0: Any = 0,
    t1: Any = 1,
    accepted_generation: int = 0,
    producer_model_id: str = "synthetic-producer",
    producer_model_version: str = "fixture-v1",
    metadata: Optional[Mapping[str, Any]] = None,
) -> ProducerFrame:
    fields: Dict[str, FieldValue] = {}
    for fid in active_field_ids(schema, domain, cfg):
        spec = schema[fid]
        fields[fid] = FieldValue(_dummy_value(spec), spec.unit, spec.shape)
    md = dict(metadata or {})
    if domain == CROP and cfg.root_distribution_required:
        md.setdefault("root_distribution_contract", "fraction_sum_explicit")
    domain_schema_id = binding.hydrology_exchange_schema_id if domain == HYDRO else binding.crop_exchange_schema_id
    return ProducerFrame(
        domain=domain,
        frame_id=frame_id,
        interval_id=interval_id,
        trial_id=trial_id,
        t0=t0,
        t1=t1,
        accepted_generation=accepted_generation,
        producer_model_id=producer_model_id,
        producer_model_version=producer_model_version,
        producer_accepted_snapshot_id=f"{producer_model_id}-accepted-{accepted_generation}",
        exchange_contract_schema_id=binding.exchange_contract_schema_id,
        transaction_schema_id=binding.transaction_schema_id,
        physical_layout_id=binding.physical_layout_id,
        geometry_id=binding.geometry_id,
        feature_set_id=binding.feature_set_id,
        precision_policy_ref=binding.precision_policy_ref,
        configuration_identity=binding.configuration_identity,
        exchange_binding_id=binding.exchange_binding_id,
        domain_schema_id=domain_schema_id,
        fields=fields,
        metadata=md,
    )


def replace_field(frame: ProducerFrame, field_id: str, *, value: Any = None, unit: Optional[str] = None, shape: Optional[str] = None) -> ProducerFrame:
    fields = dict(frame.fields)
    old = fields[field_id]
    fields[field_id] = FieldValue(old.value if value is None else value, old.unit if unit is None else unit, old.shape if shape is None else shape)
    return replace(frame, fields=fields)


class FrameAdapter:
    def __init__(self, schema: Mapping[str, FieldSchema], binding: AdapterBinding, expected_accepted_generation: int = 0) -> None:
        self.schema = dict(schema)
        self.binding = binding
        self.expected_accepted_generation = expected_accepted_generation
        self._frame_registry: Dict[str, str] = {}

    def _validate_identity(self, frame: ProducerFrame) -> None:
        expected = {
            "exchange_contract_schema_id": self.binding.exchange_contract_schema_id,
            "transaction_schema_id": self.binding.transaction_schema_id,
            "physical_layout_id": self.binding.physical_layout_id,
            "geometry_id": self.binding.geometry_id,
            "feature_set_id": self.binding.feature_set_id,
            "precision_policy_ref": self.binding.precision_policy_ref,
            "configuration_identity": self.binding.configuration_identity,
            "exchange_binding_id": self.binding.exchange_binding_id,
        }
        for name, value in expected.items():
            if getattr(frame, name) != value:
                raise ContractError(f"{name} mismatch")
        expected_domain_schema = self.binding.hydrology_exchange_schema_id if frame.domain == HYDRO else self.binding.crop_exchange_schema_id
        if frame.domain not in {HYDRO, CROP}:
            raise ContractError(f"unsupported exchange domain {frame.domain}")
        if frame.domain_schema_id != expected_domain_schema:
            raise ContractError("domain exchange schema mismatch")
        if frame.accepted_generation != self.expected_accepted_generation:
            raise ContractError("producer accepted generation mismatch")

    def _validate_bundle(self, value: Any, field_id: str) -> None:
        if not isinstance(value, list) or not value:
            raise ContractError(f"{field_id} requires nonempty explicit event list")
        required = {"source", "target", "quantity", "amount", "unit"}
        for leg in value:
            if not isinstance(leg, dict) or not required.issubset(leg):
                raise ContractError(f"{field_id} event leg incomplete")
            if leg["amount"] < 0:
                raise ContractError(f"{field_id} amount must be directed and nonnegative")

    def validate(self, frame: ProducerFrame, cfg: AdapterConfig) -> ProducerFrame:
        self._validate_identity(frame)
        if frame.domain == HYDRO:
            if cfg.hydrology_mode not in {"detailed", "aggregated"}:
                raise ContractError("unsupported hydrology mode")
            if cfg.macropore_enabled and not cfg.macropore_admitted:
                raise ContractError("macropore frame blocked without matching scientific admission")
            for key in frame.metadata:
                low = key.lower()
                if "solute" in low or "chem" in low or "concentration" in low:
                    raise ContractError("undeclared chemistry cannot enter hydrology frame")
        else:
            if cfg.crop_mode != "external":
                raise ContractError("external crop frame requires crop_mode=external")
            if cfg.root_distribution_required and frame.metadata.get("root_distribution_contract") != "fraction_sum_explicit":
                raise ContractError("root distribution contract must be explicit")

        expected = set(active_field_ids(self.schema, frame.domain, cfg))
        observed = set(frame.fields)
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        if missing:
            raise ContractError(f"missing required fields: {missing}")
        if extra:
            raise ContractError(f"inactive or undeclared fields present: {extra}")

        for fid, fv in frame.fields.items():
            spec = self.schema[fid]
            if fv.unit != spec.unit:
                raise ContractError(f"unit mismatch for {fid}")
            if fv.shape != spec.shape:
                raise ContractError(f"shape mismatch for {fid}")
            if spec.shape == "event_list":
                self._validate_bundle(fv.value, fid)

        signature = frame.signature()
        old = self._frame_registry.get(frame.frame_id)
        if old is not None and old != signature:
            raise ContractError("immutable frame_id reused with changed content")
        self._frame_registry.setdefault(frame.frame_id, signature)
        return frame

    def normalize_sign(self, frame: ProducerFrame, native_to_canonical_multiplier: Mapping[str, float], *, new_frame_id: str) -> ProducerFrame:
        if new_frame_id == frame.frame_id:
            raise ContractError("normalization must create a new immutable frame identity")
        fields = dict(frame.fields)
        for fid, multiplier in native_to_canonical_multiplier.items():
            if fid not in fields:
                raise ContractError(f"cannot normalize absent field {fid}")
            if multiplier not in {-1.0, 1.0}:
                raise ContractError("fixture accepts only explicit sign reversal or identity mapping")
            fv = fields[fid]
            value = fv.value
            if isinstance(value, list):
                value = [multiplier * x for x in value]
            else:
                value = multiplier * value
            fields[fid] = FieldValue(value, fv.unit, fv.shape)
        return replace(frame, frame_id=new_frame_id, fields=fields)

    def forbid_state_delta_transfer_inference(self) -> None:
        raise ContractError("physical residue/export transfer cannot be inferred from external crop state delta")

    def link_realized_uptake(self, runtime: RuntimeFixture, *, quantity: str, amount: float, event_id: str) -> Mapping[str, Any]:
        if runtime.phase != runtime.TRIAL_EXECUTING:
            raise ContractError("uptake result requires an active trial")
        if quantity not in {"N", "P"}:
            raise ContractError("unsupported uptake quantity")
        matches = [
            e for e in runtime.trial_events
            if e.event_id == event_id
            and e.kind == PHYSICAL
            and e.amount == amount
            and e.source == f"soil_{quantity}"
            and e.target == f"crop_{quantity}"
            and e.metadata.get("quantity") == quantity
        ]
        if len(matches) != 1:
            raise ContractError("realized uptake must link to exactly one matching typed physical transfer event")
        return {"trial_id": runtime.trial_id, "event_id": event_id, "quantity": quantity, "amount": amount}

    def checkpoint_with_external_refs(self, runtime: RuntimeFixture, frames: Sequence[ProducerFrame]) -> Mapping[str, Any]:
        checkpoint = runtime.checkpoint()
        return {
            "animo_checkpoint": checkpoint,
            "external_frame_refs": [f.frame_id for f in frames],
            "external_persistent_state": None,
        }


@dataclass(frozen=True)
class StaticIdentities:
    physical_layout_id: str
    feature_set_id: str
    configuration_identity: str
    exchange_binding_id: str
    observer_configuration_id: str


def _digest(*parts: str) -> str:
    body = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(body).hexdigest()[:20]


def derive_static_identities(*, layout_semantics: str, feature_semantics: str, parameter_set_id: str, diagnostics_mode: str, observer_settings: str = "default") -> StaticIdentities:
    physical_layout_id = "layout-" + _digest(layout_semantics, feature_semantics)
    feature_set_id = "features-" + _digest(feature_semantics)
    exchange_binding_id = "exchange-" + _digest(physical_layout_id, feature_set_id, "ARCH05-HYDROLOGY-v1", "ARCH05-CROP-v1")
    configuration_identity = "config-" + _digest(physical_layout_id, feature_set_id, parameter_set_id, exchange_binding_id)
    observer_configuration_id = "observer-" + _digest(diagnostics_mode, observer_settings)
    return StaticIdentities(physical_layout_id, feature_set_id, configuration_identity, exchange_binding_id, observer_configuration_id)


def begin_runtime_with_frames(runtime: RuntimeFixture, frames: Sequence[ProducerFrame], *, interval_id: str, trial_id: str, t0: Any, t1: Any, participants: Iterable[str]) -> None:
    if not frames:
        raise ContractError("at least one producer frame required")
    for frame in frames:
        if frame.interval_id != interval_id or frame.trial_id != trial_id or frame.t0 != t0 or frame.t1 != t1:
            raise ContractError("producer frame interval/trial endpoints do not match coupled begin")
        if frame.accepted_generation != runtime.accepted_generation:
            raise ContractError("producer frame accepted generation does not match ANIMO accepted generation")
    runtime.begin_trial(
        interval_id=interval_id,
        trial_id=trial_id,
        t0=t0,
        t1=t1,
        frames=[f.to_time_frame() for f in frames],
        topology_id=frames[0].physical_layout_id,
        config_id=frames[0].configuration_identity,
        geometry_id=frames[0].geometry_id,
        required_participants=participants,
    )
