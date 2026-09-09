from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import importlib.util
import sys
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "stateq01"
    / "upper_boundary_reservoir_wiring_harness.py"
)
SPEC = importlib.util.spec_from_file_location(
    "upper_boundary_reservoir_wiring_harness", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

State = MODULE.ReservoirState
ContractError = MODULE.UpperBoundaryContractError
checkpoint = MODULE.checkpoint_payload
interval = MODULE.exact_zero_flux_interval
amounts = MODULE.physical_amounts
restore = MODULE.restore_checkpoint


def cnp_state() -> object:
    return State.build(
        {
            "nh4": Fraction(1, 10),
            "no3": Fraction(1, 20),
            "dom": Fraction(3, 100),
            "don": Fraction(1, 100),
            "po4": Fraction(1, 200),
            "dop": Fraction(1, 500),
        },
        phosphorus_active=True,
    )


class UpperBoundaryReservoirWiringTests(unittest.TestCase):
    def test_rc_r12_nonzero_exact_zero_flux_branch_preserves_owner_and_average(self) -> None:
        start = cnp_state()
        result = interval(start, flpn=0)
        self.assertEqual(result.accepted_owner, start)
        self.assertEqual(result.interval_average, start)
        self.assertEqual(result.first_compartment_boundary, start)
        self.assertEqual(result.first_active_compartment, 1)

    def test_rc_r12_split_roundtrip_matches_uninterrupted_wiring(self) -> None:
        start = cnp_state()
        hetop = Fraction(1, 100)
        geometry = "geometry:test:v1"

        first_uninterrupted = interval(start, flpn=0)
        second_uninterrupted = interval(
            first_uninterrupted.accepted_owner, flpn=0
        )

        first_split = interval(start, flpn=0)
        payload = checkpoint(
            accepted_owner=first_split.accepted_owner,
            geometry_identity=geometry,
            hetop=hetop,
            phosphorus_active=True,
        )
        restored_start = restore(
            payload,
            expected_geometry_identity=geometry,
            expected_hetop=hetop,
            expected_phosphorus_active=True,
        )
        second_split = interval(restored_start, flpn=0)

        self.assertEqual(
            second_split.accepted_owner, second_uninterrupted.accepted_owner
        )
        self.assertEqual(
            second_split.first_compartment_boundary,
            second_uninterrupted.first_compartment_boundary,
        )

    def test_checkpoint_contains_one_owner_copy_not_start_or_average_aliases(self) -> None:
        state = cnp_state()
        payload = checkpoint(
            accepted_owner=state,
            geometry_identity="geometry:test:v1",
            hetop=Fraction(1, 100),
            phosphorus_active=True,
        )
        self.assertIn("accepted_upper_boundary", payload)
        self.assertNotIn("start_upper_boundary", payload)
        self.assertNotIn("interval_average_upper_boundary", payload)
        self.assertNotIn("avtop", payload)

    def test_nonzero_physical_amount_is_concentration_times_hetop(self) -> None:
        state = cnp_state()
        result = amounts(state, hetop=Fraction(1, 100))
        self.assertEqual(result["nh4"], Fraction(1, 1000))
        self.assertEqual(result["po4"], Fraction(1, 20000))
        self.assertTrue(all(value > 0 for value in result.values()))

    def test_geometry_identity_mismatch_rejected_before_restore(self) -> None:
        payload = checkpoint(
            accepted_owner=cnp_state(),
            geometry_identity="geometry:test:v1",
            hetop=Fraction(1, 100),
            phosphorus_active=True,
        )
        with self.assertRaises(ContractError):
            restore(
                payload,
                expected_geometry_identity="geometry:test:v2",
                expected_hetop=Fraction(1, 100),
                expected_phosphorus_active=True,
            )

    def test_hetop_mismatch_rejected_before_restore(self) -> None:
        payload = checkpoint(
            accepted_owner=cnp_state(),
            geometry_identity="geometry:test:v1",
            hetop=Fraction(1, 100),
            phosphorus_active=True,
        )
        with self.assertRaises(ContractError):
            restore(
                payload,
                expected_geometry_identity="geometry:test:v1",
                expected_hetop=Fraction(1, 50),
                expected_phosphorus_active=True,
            )

    def test_phosphorus_activation_mismatch_rejected(self) -> None:
        payload = checkpoint(
            accepted_owner=cnp_state(),
            geometry_identity="geometry:test:v1",
            hetop=Fraction(1, 100),
            phosphorus_active=True,
        )
        with self.assertRaises(ContractError):
            restore(
                payload,
                expected_geometry_identity="geometry:test:v1",
                expected_hetop=Fraction(1, 100),
                expected_phosphorus_active=False,
            )

    def test_flpn_one_is_outside_restricted_rc_r12_sentinel(self) -> None:
        with self.assertRaises(ContractError):
            interval(cnp_state(), flpn=1)

    def test_synthetic_exact_state_rejects_float_concentration(self) -> None:
        with self.assertRaises(ContractError):
            State.build(
                {"nh4": 0.1, "no3": 0, "dom": 0, "don": 0},
                phosphorus_active=False,
            )

    def test_operations_do_not_mutate_input_state_or_payload(self) -> None:
        state = cnp_state()
        payload = checkpoint(
            accepted_owner=state,
            geometry_identity="geometry:test:v1",
            hetop=Fraction(1, 100),
            phosphorus_active=True,
        )
        before = deepcopy(payload)
        interval(state, flpn=0)
        restore(
            payload,
            expected_geometry_identity="geometry:test:v1",
            expected_hetop=Fraction(1, 100),
            expected_phosphorus_active=True,
        )
        self.assertEqual(payload, before)


if __name__ == "__main__":
    unittest.main()
