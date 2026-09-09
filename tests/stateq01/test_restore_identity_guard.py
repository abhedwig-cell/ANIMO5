from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[2] / "tools" / "stateq01"
sys.path.insert(0, str(TOOLS))

from restore_identity_guard import (  # noqa: E402
    RestoreIdentityError,
    guarded_restore_identity,
    validate_restore_identity,
)


CAL = "ANIMO_PG_86400_NOLEAPSECONDS_V1"


def time(day: str, num: str = "0", den: str = "1") -> dict[str, str]:
    return {
        "calendar_contract_id": CAL,
        "day_index": day,
        "subday_numerator": num,
        "subday_denominator": den,
    }


def base_objects():
    checkpoint = {
        "profile_id": "CORE_CNP_SUBSURFACE_ONLY",
        "configuration_identity": "cfg-A",
        "physical_layout_id": "layout-7",
        "geometry_identity": "geom-7",
        "accepted_generation_id": "gen-42",
        "accepted_time": time("730120"),
        "soil_layer_count": 2,
        "p_cycle": True,
        "p_fast_site_count": 2,
        "p_slow_site_count": 1,
        "p_fast_sites_by_layer": [[1.0, 2.0], [3.0, 4.0]],
        "p_slow_sites_by_layer": [[5.0], [6.0]],
    }
    target = {
        "profile_id": "CORE_CNP_SUBSURFACE_ONLY",
        "configuration_identity": "cfg-A",
        "physical_layout_id": "layout-7",
        "geometry_identity": "geom-7",
        "accepted_generation_id": "gen-42",
        "soil_layer_count": 2,
        "p_cycle": True,
        "p_fast_site_count": 2,
        "p_slow_site_count": 1,
        "hydrology_schema_identity": "swap-frame-v1",
        "hydrology_content_identity": "sha256:hydro-A",
        "hydrology_producer_generation_id": "hydro-gen-99",
    }
    frame = {
        "frame_id": "frame-730120-730121",
        "t0": time("730120"),
        "t1": time("730121"),
        "physical_layout_id": "layout-7",
        "geometry_identity": "geom-7",
        "schema_identity": "swap-frame-v1",
        "content_identity": "sha256:hydro-A",
        "producer_accepted_generation_id": "hydro-gen-99",
    }
    return checkpoint, target, frame, time("730121")


class RestoreIdentityQualificationTests(unittest.TestCase):
    def assert_rejects_before_callback(self, mutator):
        checkpoint, target, frame, t1 = base_objects()
        mutator(checkpoint, target, frame, t1)
        calls = []
        with self.assertRaises(RestoreIdentityError):
            guarded_restore_identity(
                checkpoint=checkpoint,
                runtime_target=target,
                hydrology_frame=frame,
                next_interval_t1=t1,
                construct_accepted_state=lambda: calls.append("constructed"),
            )
        self.assertEqual(calls, [])

    def test_exact_compatible_restore_constructs_once(self):
        checkpoint, target, frame, t1 = base_objects()
        calls = []
        result = guarded_restore_identity(
            checkpoint=checkpoint,
            runtime_target=target,
            hydrology_frame=frame,
            next_interval_t1=t1,
            construct_accepted_state=lambda: calls.append("constructed") or "accepted",
        )
        self.assertEqual(result, "accepted")
        self.assertEqual(calls, ["constructed"])

    def test_rc_r6_frame_t0_one_second_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["t0"] = time("730119", "86399", "86400")
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_frame_t1_one_second_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["t1"] = time("730120", "86399", "86400")
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_calendar_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["t0"]["calendar_contract_id"] = "OTHER_CALENDAR"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_stale_producer_generation_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["producer_accepted_generation_id"] = "hydro-gen-98"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_schema_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["schema_identity"] = "other-schema"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_content_identity_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["content_identity"] = "sha256:changed"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_frame_geometry_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["geometry_identity"] = "geom-other"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_frame_layout_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["physical_layout_id"] = "layout-other"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_float_time_identity_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["t0"]["day_index"] = 730120.0
        self.assert_rejects_before_callback(mutate)

    def test_rc_r6_nonreduced_rational_rejected(self):
        def mutate(cp, target, frame, t1):
            frame["t0"] = time("730120", "2", "4")
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_checkpoint_geometry_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["geometry_identity"] = "geom-other"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_checkpoint_layout_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["physical_layout_id"] = "layout-other"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_configuration_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["configuration_identity"] = "cfg-other"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_profile_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["profile_id"] = "CORE_CNP"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_accepted_generation_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["accepted_generation_id"] = "gen-43"
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_soil_layer_cardinality_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["soil_layer_count"] = 3
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_fast_site_header_cardinality_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["p_fast_site_count"] = 3
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_slow_site_header_cardinality_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["p_slow_site_count"] = 2
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_fast_site_payload_cardinality_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            cp["p_fast_sites_by_layer"][1] = [3.0]
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_slow_site_payload_layer_count_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            cp["p_slow_sites_by_layer"] = [[5.0]]
        self.assert_rejects_before_callback(mutate)

    def test_rc_r7_p_activation_mismatch_rejected(self):
        def mutate(cp, target, frame, t1):
            target["p_cycle"] = False
            target["p_fast_site_count"] = 0
            target["p_slow_site_count"] = 0
        self.assert_rejects_before_callback(mutate)

    def test_p_inactive_requires_zero_site_cardinality(self):
        checkpoint, target, frame, t1 = base_objects()
        checkpoint.update({
            "p_cycle": False,
            "p_fast_site_count": 0,
            "p_slow_site_count": 0,
            "p_fast_sites_by_layer": [],
            "p_slow_sites_by_layer": [],
        })
        target.update({"p_cycle": False, "p_fast_site_count": 0, "p_slow_site_count": 0})
        result = validate_restore_identity(
            checkpoint=checkpoint,
            runtime_target=target,
            hydrology_frame=frame,
            next_interval_t1=t1,
        )
        self.assertEqual(result["status"], "RESTORE_IDENTITY_COMPATIBLE")

    def test_inputs_are_not_mutated_on_success(self):
        checkpoint, target, frame, t1 = base_objects()
        originals = tuple(deepcopy(x) for x in (checkpoint, target, frame, t1))
        validate_restore_identity(
            checkpoint=checkpoint,
            runtime_target=target,
            hydrology_frame=frame,
            next_interval_t1=t1,
        )
        self.assertEqual((checkpoint, target, frame, t1), originals)


if __name__ == "__main__":
    unittest.main()
