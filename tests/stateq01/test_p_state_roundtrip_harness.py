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
    / "p_state_roundtrip_harness.py"
)
SPEC = importlib.util.spec_from_file_location("p_state_roundtrip_harness", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

Layout = MODULE.PStateLayout
State = MODULE.PState
ContractError = MODULE.PStateContractError
checkpoint = MODULE.checkpoint_payload
restore = MODULE.restore_checkpoint
derived_total = MODULE.derived_total_by_layer


def layout(**overrides: object) -> object:
    values = {
        "soil_layer_count": 2,
        "fast_site_count": 2,
        "slow_site_count": 3,
    }
    values.update(overrides)
    return Layout.build(**values)


def state(current_layout: object | None = None) -> object:
    current_layout = current_layout or layout()
    return State.build(
        layout=current_layout,
        aqueous_po4=[Fraction(1, 10), Fraction(1, 20)],
        fast_sorbed=[
            [Fraction(1, 4), Fraction(1, 8)],
            [Fraction(1, 16), Fraction(1, 32)],
        ],
        slow_sorbed=[
            [Fraction(1, 5), Fraction(1, 10), Fraction(1, 20)],
            [Fraction(1, 25), Fraction(1, 50), Fraction(1, 100)],
        ],
        precipitated=[Fraction(1, 40), Fraction(1, 80)],
    )


class PStateRoundtripTests(unittest.TestCase):
    def test_rc_r4_exact_site_resolved_roundtrip(self) -> None:
        original = state()
        restored = restore(checkpoint(original), expected_layout=original.layout)
        self.assertEqual(restored, original)

    def test_rc_r4_fast_site_order_is_preserved(self) -> None:
        original = state()
        restored = restore(checkpoint(original), expected_layout=original.layout)
        self.assertEqual(restored.fast_sorbed[0][0], Fraction(1, 4))
        self.assertEqual(restored.fast_sorbed[0][1], Fraction(1, 8))

    def test_rc_r4_slow_site_order_is_preserved(self) -> None:
        original = state()
        restored = restore(checkpoint(original), expected_layout=original.layout)
        self.assertEqual(
            restored.slow_sorbed[0],
            (Fraction(1, 5), Fraction(1, 10), Fraction(1, 20)),
        )

    def test_layout_header_mismatch_rejected_before_state_decode(self) -> None:
        original = state()
        payload = checkpoint(original)
        with self.assertRaises(ContractError):
            restore(payload, expected_layout=layout(fast_site_count=3))

    def test_slow_site_cardinality_mismatch_rejected(self) -> None:
        original = state()
        with self.assertRaises(ContractError):
            restore(checkpoint(original), expected_layout=layout(slow_site_count=2))

    def test_checkpoint_has_no_derived_total_owner(self) -> None:
        payload = checkpoint(state())
        self.assertNotIn("total_mineral_p", payload)
        self.assertNotIn("summed_sorbed_p", payload)

    def test_derived_total_is_recomputed_from_site_resolved_owners(self) -> None:
        original = state()
        totals = derived_total(original)
        expected0 = (
            Fraction(1, 10)
            + Fraction(1, 4)
            + Fraction(1, 8)
            + Fraction(1, 5)
            + Fraction(1, 10)
            + Fraction(1, 20)
            + Fraction(1, 40)
        )
        self.assertEqual(totals[0], expected0)

    def test_checkpoint_and_restore_do_not_mutate_inputs(self) -> None:
        original = state()
        payload = checkpoint(original)
        before = deepcopy(payload)
        restore(payload, expected_layout=original.layout)
        self.assertEqual(payload, before)
        self.assertEqual(original, state())

    def test_mutating_payload_after_restore_does_not_change_restored_state(self) -> None:
        original = state()
        payload = checkpoint(original)
        restored = restore(payload, expected_layout=original.layout)
        payload["aqueous_po4"][0]["numerator"] = "999"
        self.assertEqual(restored.aqueous_po4[0], Fraction(1, 10))

    def test_missing_site_value_is_not_zero_filled(self) -> None:
        original = state()
        payload = checkpoint(original)
        payload["fast_sorbed"][0].pop()
        with self.assertRaises(ContractError):
            restore(payload, expected_layout=original.layout)

    def test_extra_site_value_is_not_truncated(self) -> None:
        original = state()
        payload = checkpoint(original)
        payload["slow_sorbed"][0].append({"numerator": "0", "denominator": "1"})
        with self.assertRaises(ContractError):
            restore(payload, expected_layout=original.layout)

    def test_float_state_value_is_rejected_by_exact_synthetic_fixture(self) -> None:
        current_layout = layout()
        with self.assertRaises(ContractError):
            State.build(
                layout=current_layout,
                aqueous_po4=[0.1, 0],
                fast_sorbed=[[0, 0], [0, 0]],
                slow_sorbed=[[0, 0, 0], [0, 0, 0]],
                precipitated=[0, 0],
            )

    def test_non_inpo1_fixture_is_outside_rc_r4_sentinel(self) -> None:
        with self.assertRaises(ContractError):
            Layout.build(
                soil_layer_count=2,
                fast_site_count=2,
                slow_site_count=3,
                initialization_mode="INPO2",
            )


if __name__ == "__main__":
    unittest.main()
