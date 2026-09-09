from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import importlib.util
import sys
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "stateq01"
    / "checkpoint_projection_purity_harness.py"
)
SPEC = importlib.util.spec_from_file_location(
    "checkpoint_projection_purity_harness", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

Metadata = MODULE.CheckpointMetadata
ProjectionError = MODULE.CheckpointProjectionError
project = MODULE.project_checkpoint
payload = MODULE.projection_payload


def metadata() -> object:
    return Metadata.build(
        accepted_time_id="time:730120:0/1",
        accepted_generation=23,
        physical_layout_id="layout:core-cnp:v1",
        configuration_id="config:v1",
    )


def physical() -> dict[str, object]:
    return {
        "nh4": [1.0, 2.0],
        "no3": [3.0, 4.0],
        "organic": {"fresh": [5.0, 6.0]},
        "upper_boundary": {"nh4": 0.1},
    }


def continuation() -> dict[str, object]:
    return {
        "next_management_event_id": "add004",
        "solver_continuation": {"mode": "candidate-only-placeholder"},
    }


def report() -> dict[str, object]:
    return {
        "period_n_input": 17.5,
        "period_n_output": 12.0,
        "report_sequence": 9,
    }


class CheckpointProjectionPurityTests(unittest.TestCase):
    def test_rc_r8_projection_does_not_mutate_any_input(self) -> None:
        p = physical()
        c = continuation()
        r = report()
        p0, c0, r0 = deepcopy(p), deepcopy(c), deepcopy(r)

        project(
            metadata=metadata(),
            physical_state=p,
            continuation_state=c,
            report_accumulators=r,
            final_result_generation=True,
        )

        self.assertEqual(p, p0)
        self.assertEqual(c, c0)
        self.assertEqual(r, r0)

    def test_rc_r8_repeated_projection_is_idempotent(self) -> None:
        first = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report(),
                final_result_generation=True,
            )
        )
        second = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report(),
                final_result_generation=True,
            )
        )
        self.assertEqual(first, second)

    def test_rc_r8_final_result_generation_flag_does_not_change_checkpoint_view(self) -> None:
        before_final = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report(),
                final_result_generation=False,
            )
        )
        at_final = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report(),
                final_result_generation=True,
            )
        )
        self.assertEqual(before_final, at_final)

    def test_rc_r9_report_values_do_not_change_physical_checkpoint_payload(self) -> None:
        report_a = report()
        report_b = report()
        report_b["period_n_input"] = 999999.0
        report_b["report_sequence"] = 1000

        checkpoint_a = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report_a,
                final_result_generation=False,
            )
        )
        checkpoint_b = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report_b,
                final_result_generation=False,
            )
        )
        self.assertEqual(checkpoint_a, checkpoint_b)

    def test_rc_r9_report_accumulators_are_not_serialized_as_physical_or_continuation(self) -> None:
        checkpoint = payload(
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report(),
                final_result_generation=False,
            )
        )
        self.assertNotIn("report", checkpoint)
        self.assertNotIn("report_accumulators", checkpoint)
        self.assertNotIn("period_n_input", repr(checkpoint))

    def test_projection_owns_copies_not_aliases(self) -> None:
        p = physical()
        c = continuation()
        projected = project(
            metadata=metadata(),
            physical_state=p,
            continuation_state=c,
            report_accumulators=report(),
            final_result_generation=False,
        )
        p["nh4"][0] = -999.0
        c["next_management_event_id"] = "changed"
        self.assertEqual(projected.physical_state["nh4"][0], 1.0)
        self.assertEqual(
            projected.continuation_state["next_management_event_id"], "add004"
        )

    def test_payload_copy_cannot_mutate_projection(self) -> None:
        projected = project(
            metadata=metadata(),
            physical_state=physical(),
            continuation_state=continuation(),
            report_accumulators=report(),
            final_result_generation=False,
        )
        serialized = payload(projected)
        serialized["physical_state"]["nh4"][0] = -999.0
        self.assertEqual(projected.physical_state["nh4"][0], 1.0)

    def test_invalid_final_flag_is_rejected(self) -> None:
        with self.assertRaises(ProjectionError):
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=report(),
                final_result_generation=1,
            )

    def test_missing_mapping_input_is_rejected(self) -> None:
        with self.assertRaises(ProjectionError):
            project(
                metadata=metadata(),
                physical_state=physical(),
                continuation_state=continuation(),
                report_accumulators=None,
                final_result_generation=False,
            )


if __name__ == "__main__":
    unittest.main()
