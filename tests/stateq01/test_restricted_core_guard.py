from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import importlib.util
import unittest


MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "stateq01" / "restricted_core_guard.py"
SPEC = importlib.util.spec_from_file_location("restricted_core_guard", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

GuardError = MODULE.RestrictedCoreGuardError
validate = MODULE.validate_restricted_core_envelope


def cn_zero() -> dict[str, float]:
    return {"nh4": 0.0, "no3": 0.0, "dom": 0.0, "don": 0.0}


def cnp_zero() -> dict[str, float]:
    return {**cn_zero(), "po4": 0.0, "dop": 0.0}


class RestrictedCoreGuardTests(unittest.TestCase):
    def test_aggregated_exact_zero_accepts(self) -> None:
        result = validate(
            hydrology_mode="aggregated",
            accepted_surface={"ponding": 0.0},
            candidate_surface={"ponding": -0.0},
            layer0_restart=cn_zero(),
            phosphorus_active=False,
        )
        self.assertTrue(result.accepted)

    def test_detailed_exact_zero_with_p_accepts(self) -> None:
        result = validate(
            hydrology_mode="detailed",
            accepted_surface={"ponding": 0.0, "snow": 0.0},
            candidate_surface={"ponding": 0.0, "snow": 0.0},
            layer0_restart=cnp_zero(),
            phosphorus_active=True,
        )
        self.assertTrue(result.accepted)

    def test_positive_accepted_ponding_rejected(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 1.0e-8},
                candidate_surface={"ponding": 0.0},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_positive_candidate_ponding_rejected(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 1.0e-8},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_positive_detailed_snow_rejected(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="detailed",
                accepted_surface={"ponding": 0.0, "snow": 0.0},
                candidate_surface={"ponding": 0.0, "snow": 1.0e-12},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_nonzero_layer0_nh4_rejected(self) -> None:
        state = cn_zero()
        state["nh4"] = 1.0e-12
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 0.0},
                layer0_restart=state,
                phosphorus_active=False,
            )

    def test_nonzero_layer0_dop_rejected_when_p_active(self) -> None:
        state = cnp_zero()
        state["dop"] = -1.0e-12
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 0.0},
                layer0_restart=state,
                phosphorus_active=True,
            )

    def test_subnormal_positive_surface_storage_is_not_epsilon_accepted(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 1.0e-300},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_nan_surface_rejected(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": float("nan")},
                candidate_surface={"ponding": 0.0},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_infinite_layer0_rejected(self) -> None:
        state = cn_zero()
        state["don"] = float("inf")
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 0.0},
                layer0_restart=state,
                phosphorus_active=False,
            )

    def test_negative_surface_storage_rejected(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": -1.0e-9},
                candidate_surface={"ponding": 0.0},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_unknown_hydrology_mode_rejected(self) -> None:
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="mystery",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 0.0},
                layer0_restart=cn_zero(),
                phosphorus_active=False,
            )

    def test_missing_required_layer0_coordinate_rejected(self) -> None:
        state = cn_zero()
        del state["don"]
        with self.assertRaises(GuardError):
            validate(
                hydrology_mode="aggregated",
                accepted_surface={"ponding": 0.0},
                candidate_surface={"ponding": 0.0},
                layer0_restart=state,
                phosphorus_active=False,
            )

    def test_guard_does_not_mutate_inputs(self) -> None:
        accepted = {"ponding": 0.0, "snow": 0.0}
        candidate = {"ponding": 0.0, "snow": 0.0}
        layer0 = cnp_zero()
        before = deepcopy((accepted, candidate, layer0))
        validate(
            hydrology_mode="detailed",
            accepted_surface=accepted,
            candidate_surface=candidate,
            layer0_restart=layer0,
            phosphorus_active=True,
        )
        self.assertEqual((accepted, candidate, layer0), before)


if __name__ == "__main__":
    unittest.main()
