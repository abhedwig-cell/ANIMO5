from __future__ import annotations

from pathlib import Path
import importlib.util
import sys
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "stateq01"
    / "year_boundary_continuation_harness.py"
)
SPEC = importlib.util.spec_from_file_location(
    "year_boundary_continuation_harness", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

ExactTime = MODULE.ExactTime
YearBoundary = MODULE.YearBoundary
BoundaryError = MODULE.YearBoundaryContractError
close_interval = MODULE.close_interval_at_year_boundary
start_interval = MODULE.start_next_year_interval
restore = MODULE.restore_year_boundary_checkpoint


class YearBoundaryContinuationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.t0 = ExactTime(730118)
        self.split = ExactTime(730119)
        self.boundary = YearBoundary.january_first(boundary=self.split, year=2000)

    def _physical(self, state: dict[str, int]) -> dict[str, int]:
        return {"physical_generation": state["physical_generation"] + 1, "year_init": state["year_init"]}

    def _new_year(self, state: dict[str, int]) -> dict[str, int]:
        return {"physical_generation": state["physical_generation"], "year_init": state["year_init"] + 1}

    def test_rc_r3_prior_year_closeout_occurs_after_physical_t1(self) -> None:
        observed = []

        def physical(state: dict[str, int]) -> dict[str, int]:
            observed.append("physical")
            return self._physical(state)

        def closeout(state: dict[str, int]) -> None:
            observed.append("closeout")
            self.assertEqual(state["physical_generation"], 1)

        result = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state={"physical_generation": 0, "year_init": 0},
            execute_physical_interval=physical,
            close_prior_year_output=closeout,
            checkpoint_after_closeout=True,
        )
        self.assertEqual(observed, ["physical", "closeout"])
        self.assertEqual(
            result.events,
            (
                "PHYSICAL_TO_T1",
                "PRIOR_YEAR_CLOSEOUT_AFTER_PHYSICAL_T1",
                "CHECKPOINT_ACCEPTED_BOUNDARY",
            ),
        )

    def test_rc_r3_checkpoint_and_next_interval_share_one_exact_boundary(self) -> None:
        result = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state={"physical_generation": 0, "year_init": 0},
            execute_physical_interval=self._physical,
            close_prior_year_output=lambda state: None,
            checkpoint_after_closeout=True,
        )
        assert result.checkpoint is not None
        restored = restore(checkpoint=result.checkpoint, year_boundary=self.boundary)
        started = start_interval(
            t0=self.split,
            year_boundary=self.boundary,
            accepted_state=restored,
            initialize_new_year_inputs=self._new_year,
        )
        self.assertEqual(result.checkpoint.accepted_time, self.split)
        self.assertEqual(started.accepted_state, {"physical_generation": 1, "year_init": 1})

    def test_rc_r3_split_and_uninterrupted_lifecycle_have_same_physical_new_year_state(self) -> None:
        initial = {"physical_generation": 0, "year_init": 0}

        uninterrupted_close = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state=initial,
            execute_physical_interval=self._physical,
            close_prior_year_output=lambda state: None,
            checkpoint_after_closeout=False,
        )
        uninterrupted_start = start_interval(
            t0=self.split,
            year_boundary=self.boundary,
            accepted_state=uninterrupted_close.accepted_state,
            initialize_new_year_inputs=self._new_year,
        )

        split_close = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state=initial,
            execute_physical_interval=self._physical,
            close_prior_year_output=lambda state: None,
            checkpoint_after_closeout=True,
        )
        assert split_close.checkpoint is not None
        restored = restore(checkpoint=split_close.checkpoint, year_boundary=self.boundary)
        split_start = start_interval(
            t0=self.split,
            year_boundary=self.boundary,
            accepted_state=restored,
            initialize_new_year_inputs=self._new_year,
        )
        self.assertEqual(split_start.accepted_state, uninterrupted_start.accepted_state)

    def test_rc_r3_checkpoint_does_not_replay_prior_year_closeout(self) -> None:
        closeouts = []
        closed = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state={"physical_generation": 0, "year_init": 0},
            execute_physical_interval=self._physical,
            close_prior_year_output=lambda state: closeouts.append("close"),
            checkpoint_after_closeout=True,
        )
        assert closed.checkpoint is not None
        restore(checkpoint=closed.checkpoint, year_boundary=self.boundary)
        self.assertEqual(closeouts, ["close"])

    def test_rc_r3_new_year_init_occurs_only_on_next_interval_side(self) -> None:
        inits = []
        closed = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state={"physical_generation": 0, "year_init": 0},
            execute_physical_interval=self._physical,
            close_prior_year_output=lambda state: None,
            checkpoint_after_closeout=True,
        )
        self.assertEqual(inits, [])
        assert closed.checkpoint is not None
        restored = restore(checkpoint=closed.checkpoint, year_boundary=self.boundary)

        def init(state: dict[str, int]) -> dict[str, int]:
            inits.append("init")
            return self._new_year(state)

        start_interval(
            t0=self.split,
            year_boundary=self.boundary,
            accepted_state=restored,
            initialize_new_year_inputs=init,
        )
        self.assertEqual(inits, ["init"])

    def test_non_boundary_t1_is_rejected(self) -> None:
        with self.assertRaises(BoundaryError):
            close_interval(
                t0=self.t0,
                t1=ExactTime(730118, 86399, 86400),
                year_boundary=self.boundary,
                accepted_state={"physical_generation": 0, "year_init": 0},
                execute_physical_interval=self._physical,
                close_prior_year_output=lambda state: None,
                checkpoint_after_closeout=True,
            )

    def test_next_interval_with_epsilon_like_offset_is_rejected(self) -> None:
        closed = close_interval(
            t0=self.t0,
            t1=self.split,
            year_boundary=self.boundary,
            accepted_state={"physical_generation": 0, "year_init": 0},
            execute_physical_interval=self._physical,
            close_prior_year_output=lambda state: None,
            checkpoint_after_closeout=True,
        )
        assert closed.checkpoint is not None
        restored = restore(checkpoint=closed.checkpoint, year_boundary=self.boundary)
        with self.assertRaises(BoundaryError):
            start_interval(
                t0=ExactTime(730119, 1, 86400),
                year_boundary=self.boundary,
                accepted_state=restored,
                initialize_new_year_inputs=self._new_year,
            )

    def test_float_time_coordinate_is_rejected(self) -> None:
        with self.assertRaises(BoundaryError):
            ExactTime(730119, 0.5, 1)

    def test_nonreduced_time_coordinate_is_rejected(self) -> None:
        with self.assertRaises(BoundaryError):
            ExactTime(730119, 2, 4)

    def test_year_boundary_requires_midnight(self) -> None:
        with self.assertRaises(BoundaryError):
            YearBoundary.january_first(
                boundary=ExactTime(730119, 1, 86400), year=2000
            )


if __name__ == "__main__":
    unittest.main()
