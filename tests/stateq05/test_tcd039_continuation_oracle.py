import unittest

from tools.stateq05.tcd039_continuation_oracle import (
    advance_from_layers,
    apply_n_shortage,
    apply_p_shortage,
    demand_deficit,
    restore_working,
    split_witness,
)


class TCD039ContinuationOracleTests(unittest.TestCase):
    def test_n_deficit_depends_on_potential_owner(self):
        self.assertEqual(demand_deficit(0.0125, 0.0078125), 0.0046875)
        self.assertNotEqual(demand_deficit(0.0, 0.0078125), 0.0046875)

    def test_p_deficit_depends_on_potential_owner(self):
        self.assertEqual(demand_deficit(0.00390625, 0.001953125), 0.001953125)

    def test_advance_starts_from_prior_owner(self):
        self.assertEqual(
            advance_from_layers(0.0078125, [0.25, 0.5], 0.00390625, 0.5),
            0.00927734375,
        )
        self.assertNotEqual(
            advance_from_layers(0.0, [0.25, 0.5], 0.00390625, 0.5),
            0.00927734375,
        )

    def test_n_shortage_changes_persistent_potential_state(self):
        n_out, p_out = apply_n_shortage(0.0078125, 0.015625, 0.00390625)
        self.assertNotEqual(n_out, 0.015625)
        self.assertNotEqual(p_out, 0.00390625)

    def test_p_shortage_changes_both_potential_states(self):
        n_out, p_out = apply_p_shortage(0.001953125, 0.0078125, 0.015625)
        self.assertNotEqual(n_out, 0.015625)
        self.assertNotEqual(p_out, 0.0078125)

    def test_exact_owner_split_is_exact(self):
        continuous, resumed = split_witness(zero_at_split=False)
        self.assertEqual(continuous, resumed)

    def test_zero_reset_split_diverges(self):
        continuous, resumed = split_witness(zero_at_split=True)
        self.assertNotEqual(continuous, resumed)

    def test_p_restore_guard(self):
        self.assertEqual(restore_working(0.01, 0.002, 1)["Amplpo_pot"], 0.002)
        self.assertIsNone(restore_working(0.01, 0.002, 0)["Amplpo_pot"])


if __name__ == "__main__":
    unittest.main()
