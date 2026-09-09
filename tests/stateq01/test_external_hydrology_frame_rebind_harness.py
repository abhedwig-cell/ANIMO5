from __future__ import annotations

from pathlib import Path
import importlib.util
import sys
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "stateq01"
    / "external_hydrology_frame_rebind_harness.py"
)
SPEC = importlib.util.spec_from_file_location(
    "external_hydrology_frame_rebind_harness", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

ExactTime = MODULE.ExactTime
Interval = MODULE.IntervalIdentity
Frame = MODULE.HydrologyFrame
FrameError = MODULE.FrameRebindError
guarded_rebind = MODULE.guarded_rebind
rebind_mismatches = MODULE.rebind_mismatches


def second_before(day: int) -> object:
    return ExactTime(day - 1, 86399, 86400)


def interval(**overrides: object) -> object:
    values = {
        "t0": ExactTime(730119),
        "t1": ExactTime(730120),
        "accepted_generation": 17,
        "geometry_id": "geometry:v1",
        "hydrology_schema_id": "hydrology-schema:v1",
        "configuration_id": "config:v1",
    }
    values.update(overrides)
    return Interval.build(**values)


def frame(**overrides: object) -> object:
    values = {
        "frame_id": "hydrology-frame:17:18",
        "t0": ExactTime(730119),
        "t1": ExactTime(730120),
        "producer_accepted_generation": 17,
        "geometry_id": "geometry:v1",
        "hydrology_schema_id": "hydrology-schema:v1",
        "configuration_id": "config:v1",
        "content_fingerprint": "sha256:qualification-frame-content",
    }
    values.update(overrides)
    return Frame.build(**values)


class ExternalHydrologyFrameRebindTests(unittest.TestCase):
    def assert_rejected_before_consumption(self, candidate_interval: object, candidate_frame: object) -> None:
        calls = []

        def consume() -> object:
            calls.append("consumed")
            return {"should": "not happen"}

        with self.assertRaises(FrameError):
            guarded_rebind(
                interval=candidate_interval,
                frame=candidate_frame,
                consume_frame_and_construct_process_state=consume,
            )
        self.assertEqual(calls, [])

    def test_exact_frame_match_allows_consumption_once(self) -> None:
        calls = []

        def consume() -> object:
            calls.append("consumed")
            return {"hydrology": "opaque-frame"}

        result = guarded_rebind(
            interval=interval(),
            frame=frame(),
            consume_frame_and_construct_process_state=consume,
        )
        self.assertEqual(calls, ["consumed"])
        self.assertEqual(result.payload, {"hydrology": "opaque-frame"})

    def test_t0_mismatch_rejected_before_consumption(self) -> None:
        self.assert_rejected_before_consumption(
            interval(), frame(t0=second_before(730119))
        )

    def test_t1_one_second_mismatch_rejected_without_tolerance(self) -> None:
        self.assert_rejected_before_consumption(
            interval(), frame(t1=second_before(730120))
        )

    def test_future_t1_mismatch_rejected_before_consumption(self) -> None:
        self.assert_rejected_before_consumption(
            interval(), frame(t1=ExactTime(730121))
        )

    def test_stale_producer_generation_rejected_before_consumption(self) -> None:
        self.assert_rejected_before_consumption(
            interval(accepted_generation=17),
            frame(producer_accepted_generation=16),
        )

    def test_geometry_mismatch_rejected_before_consumption(self) -> None:
        self.assert_rejected_before_consumption(
            interval(geometry_id="geometry:v1"), frame(geometry_id="geometry:v2")
        )

    def test_schema_mismatch_rejected_before_consumption(self) -> None:
        self.assert_rejected_before_consumption(
            interval(hydrology_schema_id="hydrology-schema:v1"),
            frame(hydrology_schema_id="hydrology-schema:v2"),
        )

    def test_configuration_mismatch_rejected_before_consumption(self) -> None:
        self.assert_rejected_before_consumption(
            interval(configuration_id="config:v1"),
            frame(configuration_id="config:v2"),
        )

    def test_multiple_mismatches_are_reported_exactly(self) -> None:
        mismatches = rebind_mismatches(
            interval(),
            frame(
                t1=second_before(730120),
                producer_accepted_generation=18,
                geometry_id="geometry:v2",
            ),
        )
        self.assertEqual(
            mismatches,
            ("t1", "accepted_generation", "geometry_id"),
        )

    def test_float_time_coordinate_is_not_accepted(self) -> None:
        with self.assertRaises(FrameError):
            ExactTime(730119, 0.5, 1)

    def test_nonreduced_rational_coordinate_is_rejected(self) -> None:
        with self.assertRaises(FrameError):
            ExactTime(730119, 2, 4)

    def test_interval_requires_strictly_increasing_exact_boundary(self) -> None:
        with self.assertRaises(FrameError):
            interval(t1=ExactTime(730119))

    def test_negative_generation_is_rejected(self) -> None:
        with self.assertRaises(FrameError):
            interval(accepted_generation=-1)
        with self.assertRaises(FrameError):
            frame(producer_accepted_generation=-1)

    def test_content_fingerprint_is_mandatory_provenance(self) -> None:
        with self.assertRaises(FrameError):
            frame(content_fingerprint="")


if __name__ == "__main__":
    unittest.main()
