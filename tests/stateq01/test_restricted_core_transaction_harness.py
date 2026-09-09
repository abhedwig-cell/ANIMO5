from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest


TOOLS = Path(__file__).resolve().parents[2] / "tools" / "stateq01"
sys.path.insert(0, str(TOOLS))

from restricted_core_guard import RestrictedCoreGuardError
from restricted_core_transaction_harness import guarded_candidate_accept, guarded_restore


def cn_zero() -> dict[str, float]:
    return {"nh4": 0.0, "no3": 0.0, "dom": 0.0, "don": 0.0}


class RestrictedCoreTransactionHarnessTests(unittest.TestCase):
    def test_valid_candidate_allows_mutation_once(self) -> None:
        calls = []

        def mutate() -> str:
            calls.append("mutated")
            return "trial"

        result = guarded_candidate_accept(
            hydrology_mode="aggregated",
            accepted_surface={"ponding": 0.0},
            candidate_surface={"ponding": 0.0},
            layer0_state=cn_zero(),
            phosphorus_active=False,
            run_chemistry_and_management=mutate,
        )
        self.assertEqual(calls, ["mutated"])
        self.assertEqual(result.stage, "CANDIDATE_PROCESSING_ALLOWED")

    def test_rc_r10_positive_candidate_fails_before_mutation(self) -> None:
        calls = []

        def mutate() -> None:
            calls.append("mutated")

        with self.assertRaises(RestrictedCoreGuardError):
            guarded_candidate_accept(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 1.0e-12},
                layer0_state=cn_zero(),
                phosphorus_active=False,
                run_chemistry_and_management=mutate,
            )
        self.assertEqual(calls, [])

    def test_rc_r10_subnormal_positive_candidate_fails_before_mutation(self) -> None:
        calls = []

        def mutate() -> None:
            calls.append("mutated")

        with self.assertRaises(RestrictedCoreGuardError):
            guarded_candidate_accept(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 1.0e-300},
                layer0_state=cn_zero(),
                phosphorus_active=False,
                run_chemistry_and_management=mutate,
            )
        self.assertEqual(calls, [])

    def test_rc_r10_detailed_snow_fails_before_mutation(self) -> None:
        calls = []

        def mutate() -> None:
            calls.append("mutated")

        with self.assertRaises(RestrictedCoreGuardError):
            guarded_candidate_accept(
                hydrology_mode="detailed",
                accepted_surface={"ponding": 0.0, "snow": 0.0},
                candidate_surface={"ponding": 0.0, "snow": 1.0e-10},
                layer0_state=cn_zero(),
                phosphorus_active=False,
                run_chemistry_and_management=mutate,
            )
        self.assertEqual(calls, [])

    def test_rc_r11_nonzero_layer0_restore_fails_before_accepted_construction(self) -> None:
        calls = []
        layer0 = cn_zero()
        layer0["nh4"] = 1.0e-9

        def construct() -> str:
            calls.append("constructed")
            return "accepted"

        with self.assertRaises(RestrictedCoreGuardError):
            guarded_restore(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 0.0},
                layer0_restart=layer0,
                phosphorus_active=False,
                construct_accepted_state=construct,
            )
        self.assertEqual(calls, [])

    def test_rc_r11_valid_zero_restore_constructs_once(self) -> None:
        calls = []

        def construct() -> str:
            calls.append("constructed")
            return "accepted"

        result = guarded_restore(
            hydrology_mode="aggregated",
            accepted_surface={"ponding": 0.0},
            candidate_surface={"ponding": 0.0},
            layer0_restart=cn_zero(),
            phosphorus_active=False,
            construct_accepted_state=construct,
        )
        self.assertEqual(calls, ["constructed"])
        self.assertEqual(result.stage, "RESTORED_ACCEPTED")

    def test_rejected_candidate_does_not_mutate_input_mappings(self) -> None:
        accepted = {"ponding": 0.0}
        candidate = {"ponding": 1.0e-12}
        layer0 = cn_zero()
        before = deepcopy((accepted, candidate, layer0))

        with self.assertRaises(RestrictedCoreGuardError):
            guarded_candidate_accept(
                hydrology_mode="aggregated",
                accepted_surface=accepted,
                candidate_surface=candidate,
                layer0_state=layer0,
                phosphorus_active=False,
                run_chemistry_and_management=lambda: None,
            )
        self.assertEqual((accepted, candidate, layer0), before)


if __name__ == "__main__":
    unittest.main()
