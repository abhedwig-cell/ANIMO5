from __future__ import annotations

from pathlib import Path
import importlib.util
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "stateq01"
    / "management_cursor_exact_time_harness.py"
)
SPEC = importlib.util.spec_from_file_location("management_cursor_exact_time_harness", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

ExactTime = MODULE.ExactTime
Event = MODULE.ManagementEvent
Schedule = MODULE.ManagementSchedule
CursorError = MODULE.CursorContractError
advance = MODULE.advance_interval
checkpoint = MODULE.checkpoint_payload
initial = MODULE.initial_cursor
restore = MODULE.restore_checkpoint


def schedule_for_split() -> object:
    split = ExactTime(730120)
    return Schedule.build(
        "management-schedule:test:v1",
        [
            Event("ADD-001", split),
            Event("ADD-002", ExactTime(730120, 1, 2)),
        ],
    )


class ExactManagementCursorQualificationTests(unittest.TestCase):
    def test_rc_r2_split_at_management_t1_has_no_replay_or_skip(self) -> None:
        schedule = schedule_for_split()
        t0 = ExactTime(730119)
        split = ExactTime(730120)
        t2 = ExactTime(730121)

        uninterrupted_state = initial(schedule, t0)
        uninterrupted_first = advance(schedule, uninterrupted_state, split)
        uninterrupted_second = advance(
            schedule, uninterrupted_first.accepted_state, t2
        )
        uninterrupted_trace = (
            uninterrupted_first.delivered_event_ids
            + uninterrupted_second.delivered_event_ids
        )

        split_state = initial(schedule, t0)
        pre_split = advance(schedule, split_state, split)
        payload = checkpoint(schedule, pre_split.accepted_state)
        self.assertEqual(payload["next_event_id"], "ADD-002")
        restored = restore(schedule, payload)
        post_split = advance(schedule, restored, t2)
        split_trace = pre_split.delivered_event_ids + post_split.delivered_event_ids

        self.assertEqual(uninterrupted_trace, ("ADD-001", "ADD-002"))
        self.assertEqual(split_trace, uninterrupted_trace)
        self.assertNotIn("ADD-001", post_split.delivered_event_ids)

    def test_event_exactly_at_split_belongs_to_ending_interval(self) -> None:
        schedule = Schedule.build(
            "schedule:boundary",
            [Event("AT-SPLIT", ExactTime(100))],
        )
        result = advance(schedule, initial(schedule, ExactTime(99)), ExactTime(100))
        self.assertEqual(result.delivered_event_ids, ("AT-SPLIT",))

    def test_event_just_before_split_is_selected_exactly(self) -> None:
        schedule = Schedule.build(
            "schedule:before",
            [Event("BEFORE", ExactTime(99, 86399, 86400))],
        )
        result = advance(schedule, initial(schedule, ExactTime(99)), ExactTime(100))
        self.assertEqual(result.delivered_event_ids, ("BEFORE",))

    def test_event_just_after_split_is_not_selected_in_ending_interval(self) -> None:
        schedule = Schedule.build(
            "schedule:after",
            [Event("AFTER", ExactTime(100, 1, 86400))],
        )
        first = advance(schedule, initial(schedule, ExactTime(99)), ExactTime(100))
        self.assertEqual(first.delivered_event_ids, ())
        second = advance(schedule, first.accepted_state, ExactTime(101))
        self.assertEqual(second.delivered_event_ids, ("AFTER",))

    def test_checkpoint_does_not_duplicate_next_event_time_owner(self) -> None:
        schedule = schedule_for_split()
        first = advance(schedule, initial(schedule, ExactTime(730119)), ExactTime(730120))
        payload = checkpoint(schedule, first.accepted_state)
        self.assertEqual(payload["next_event_id"], "ADD-002")
        self.assertNotIn("next_event_time", payload)
        self.assertNotIn("next_event_boundary", payload)

    def test_time_only_restore_is_rejected(self) -> None:
        schedule = schedule_for_split()
        payload = {
            "schedule_identity": schedule.schedule_identity,
            "accepted_time": ExactTime(730120).to_payload(),
        }
        with self.assertRaises(CursorError):
            restore(schedule, payload)

    def test_schedule_identity_mismatch_is_rejected(self) -> None:
        schedule = schedule_for_split()
        payload = {
            "schedule_identity": "other-schedule",
            "accepted_time": ExactTime(730120).to_payload(),
            "next_event_id": "ADD-002",
        }
        with self.assertRaises(CursorError):
            restore(schedule, payload)

    def test_unknown_explicit_cursor_is_rejected(self) -> None:
        schedule = schedule_for_split()
        payload = {
            "schedule_identity": schedule.schedule_identity,
            "accepted_time": ExactTime(730120).to_payload(),
            "next_event_id": "ADD-999",
        }
        with self.assertRaises(CursorError):
            restore(schedule, payload)

    def test_noncanonical_rational_fraction_is_rejected(self) -> None:
        with self.assertRaises(CursorError):
            ExactTime(100, 2, 4)

    def test_float_coordinate_is_not_accepted_as_canonical_identity(self) -> None:
        with self.assertRaises(CursorError):
            ExactTime(100.0)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
