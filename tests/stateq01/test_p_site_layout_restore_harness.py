from __future__ import annotations

from pathlib import Path
import importlib.util
import sys
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "stateq01"
    / "p_site_layout_restore_harness.py"
)
SPEC = importlib.util.spec_from_file_location("p_site_layout_restore_harness", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

Layout = MODULE.PhysicalLayout
LayoutError = MODULE.LayoutMismatchError
guarded_restore = MODULE.guarded_restore
mismatch_fields = MODULE.mismatch_fields


def layout(**overrides: object) -> object:
    values = {
        "state_schema_id": "animo-state:v1",
        "geometry_id": "geometry:profile:v1",
        "soil_layer_count": 5,
        "fast_p_site_count": 2,
        "slow_p_site_count": 3,
        "organic_fraction_count": 4,
        "phosphorus_active": True,
        "precision_policy_id": "precision:qualification:v1",
    }
    values.update(overrides)
    return Layout.build(**values)


class PSiteLayoutRestoreTests(unittest.TestCase):
    def assert_rejected_before_state_consumption(self, checkpoint: object, target: object) -> None:
        calls = []

        def consume() -> object:
            calls.append("consumed")
            return {"state": "should-not-be-read"}

        with self.assertRaises(LayoutError):
            guarded_restore(
                checkpoint_layout=checkpoint,
                target_layout=target,
                consume_and_construct_state=consume,
            )
        self.assertEqual(calls, [])

    def test_exact_layout_allows_state_consumption_once(self) -> None:
        current = layout()
        calls = []

        def consume() -> object:
            calls.append("consumed")
            return {"p_state": "opaque"}

        result = guarded_restore(
            checkpoint_layout=current,
            target_layout=current,
            consume_and_construct_state=consume,
        )
        self.assertEqual(calls, ["consumed"])
        self.assertEqual(result.restored_state, {"p_state": "opaque"})

    def test_fast_site_count_increase_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(fast_p_site_count=2), layout(fast_p_site_count=3)
        )

    def test_fast_site_count_decrease_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(fast_p_site_count=3), layout(fast_p_site_count=2)
        )

    def test_slow_site_count_increase_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(slow_p_site_count=3), layout(slow_p_site_count=4)
        )

    def test_slow_site_count_decrease_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(slow_p_site_count=4), layout(slow_p_site_count=3)
        )

    def test_same_array_capacity_is_not_a_compatibility_escape_hatch(self) -> None:
        checkpoint = layout(fast_p_site_count=2, slow_p_site_count=3)
        target = layout(fast_p_site_count=3, slow_p_site_count=2)
        self.assertEqual(
            mismatch_fields(checkpoint, target),
            ("fast_p_site_count", "slow_p_site_count"),
        )
        self.assert_rejected_before_state_consumption(checkpoint, target)

    def test_geometry_identity_mismatch_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(geometry_id="geometry:a"), layout(geometry_id="geometry:b")
        )

    def test_soil_layer_count_mismatch_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(soil_layer_count=5), layout(soil_layer_count=6)
        )

    def test_organic_fraction_count_mismatch_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(organic_fraction_count=4), layout(organic_fraction_count=5)
        )

    def test_precision_policy_mismatch_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(precision_policy_id="precision:a"),
            layout(precision_policy_id="precision:b"),
        )

    def test_state_schema_mismatch_rejected_before_state_consumption(self) -> None:
        self.assert_rejected_before_state_consumption(
            layout(state_schema_id="state:v1"), layout(state_schema_id="state:v2")
        )

    def test_p_activation_mismatch_rejected_at_layout_construction(self) -> None:
        with self.assertRaises(LayoutError):
            layout(phosphorus_active=False, fast_p_site_count=2, slow_p_site_count=3)

    def test_p_inactive_layout_requires_zero_site_counts(self) -> None:
        inactive = layout(
            phosphorus_active=False,
            fast_p_site_count=0,
            slow_p_site_count=0,
        )
        self.assertFalse(inactive.phosphorus_active)

    def test_p_active_layout_requires_explicit_nonzero_site_counts(self) -> None:
        with self.assertRaises(LayoutError):
            layout(fast_p_site_count=0)
        with self.assertRaises(LayoutError):
            layout(slow_p_site_count=0)

    def test_boolean_is_not_accepted_as_site_count(self) -> None:
        with self.assertRaises(LayoutError):
            layout(fast_p_site_count=True)


if __name__ == "__main__":
    unittest.main()
