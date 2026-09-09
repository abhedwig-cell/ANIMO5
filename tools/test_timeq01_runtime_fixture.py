#!/usr/bin/env python3
"""Synthetic contract tests for ANIMO-TIMEQ01.

These tests exercise only the abstract runtime fixture. They are not B2,
scientific, numerical, or production evidence.
"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from timeq01_runtime_fixture import (  # noqa: E402
    ContractError,
    Frame,
    PHYSICAL,
    PROVISIONAL,
    REPORT_ONLY,
    RuntimeFixture,
)


def make_frame(engine: RuntimeFixture, frame_id: str, interval_id: str, payload=None) -> Frame:
    return Frame(
        frame_id=frame_id,
        interval_id=interval_id,
        accepted_generation=engine.accepted_generation,
        topology_id=engine.topology_id,
        config_id=engine.config_id,
        geometry_id=engine.geometry_id,
        payload=payload or {"q": 1.0},
    )


def begin_basic(engine: RuntimeFixture, interval="I1", trial="T1", *, participants=None) -> None:
    engine.begin_trial(
        interval_id=interval,
        trial_id=trial,
        t0=0,
        t1=1,
        frames=[make_frame(engine, f"F-{interval}-{trial}", interval)],
        required_participants=participants,
    )


class TimeQ01FixtureTests(unittest.TestCase):
    def test_T01_begin_trial_identity_binding(self):
        engine = RuntimeFixture({"x": 10})
        frame = make_frame(engine, "F1", "I1")
        engine.begin_trial(interval_id="I1", trial_id="T1", t0=0, t1=1, frames=[frame])
        self.assertEqual(engine.phase, engine.TRIAL_EXECUTING)
        self.assertEqual(engine.trial_id, "T1")
        self.assertEqual(engine.interval_id, "I1")
        self.assertEqual(engine.bound_frame_ids, ("F1",))
        self.assertEqual(engine.trial_trace[0].label, "G_ACCEPTED_START")

    def test_T02_accepted_state_immutable_during_trial(self):
        engine = RuntimeFixture({"x": 10})
        begin_basic(engine)
        engine.mutate("x", 15)
        self.assertEqual(engine.accepted_values["x"], 10)
        self.assertEqual(engine.read_trial("x"), 15)

    def test_T03_reject_atomicity(self):
        engine = RuntimeFixture({"x": 10})
        before = engine.checkpoint()
        begin_basic(engine)
        engine.mutate("x", 99)
        engine.emit_event(event_id="E1", kind=PHYSICAL, source="soil", target="crop", amount=1.0)
        engine.emit_event(event_id="E2", kind=PROVISIONAL, source="a", target="b", amount=2.0)
        engine.emit_event(event_id="E3", kind=REPORT_ONLY, source="diag", target="diag", amount=0.0)
        engine.reject()
        self.assertEqual(engine.checkpoint(), before)
        self.assertEqual(engine.committed_events, [])

    def test_T04_retry_requires_fresh_trial_id(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine, trial="TRY1")
        engine.reject()
        with self.assertRaises(ContractError):
            begin_basic(engine, trial="TRY1")
        begin_basic(engine, trial="TRY2")
        self.assertEqual(engine.trial_id, "TRY2")

    def test_T05_changed_t1_requires_new_interval_identity(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine, interval="I1", trial="T1")
        engine.reject()
        with self.assertRaises(ContractError):
            engine.begin_trial(interval_id="I1", trial_id="T2", t0=0, t1=2)
        engine.begin_trial(interval_id="I2", trial_id="T3", t0=0, t1=2)
        self.assertEqual(engine.interval_id, "I2")

    def test_T06_frame_identity_is_immutable(self):
        engine = RuntimeFixture({"x": 1})
        frame = make_frame(engine, "F1", "I1", {"q": 1.0})
        engine.begin_trial(interval_id="I1", trial_id="T1", t0=0, t1=1, frames=[frame])
        engine.reject()
        changed = make_frame(engine, "F1", "I1", {"q": 2.0})
        with self.assertRaises(ContractError):
            engine.begin_trial(interval_id="I1", trial_id="T2", t0=0, t1=1, frames=[changed])

    def test_T07_stale_generation_frame_rejected(self):
        engine = RuntimeFixture({"x": 1})
        stale = Frame("F1", "I1", -1, engine.topology_id, engine.config_id, engine.geometry_id, {})
        with self.assertRaises(ContractError):
            engine.begin_trial(interval_id="I1", trial_id="T1", t0=0, t1=1, frames=[stale])
        self.assertEqual(engine.phase, engine.ACCEPTED_IDLE)

    def test_T08_same_step_management_visibility(self):
        engine = RuntimeFixture({"pool": 10})
        begin_basic(engine)
        engine.mutate("pool", 13, label="G_MUTATED_EVENT")
        self.assertEqual(engine.read_trial("pool"), 13)
        self.assertEqual(engine.accepted_values["pool"], 10)
        self.assertTrue(any(r.label == "G_MUTATED_EVENT" and r.subject == "pool" for r in engine.trial_trace))

    def test_T09_previous_neighbor_reads_accepted_generation(self):
        engine = RuntimeFixture({"neighbor": 4})
        begin_basic(engine)
        engine.mutate("neighbor", 9)
        self.assertEqual(engine.read_previous_neighbor("neighbor"), 4)
        self.assertTrue(any(r.label == "G_PREVIOUS_NEIGHBOR" for r in engine.trial_trace))

    def test_T10_provisional_event_not_committed(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine)
        engine.emit_event(event_id="POT", kind=PROVISIONAL, source="a", target="b", amount=1.0)
        engine.emit_event(event_id="ACT", kind=PHYSICAL, source="a", target="b", amount=1.0)
        engine.mark_ready()
        engine.accept({"ANIMO": 1})
        self.assertEqual([e.event_id for e in engine.committed_events], ["ACT"])

    def test_T11_report_only_event_not_committed(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine)
        engine.emit_event(event_id="REP", kind=REPORT_ONLY, source="diag", target="diag", amount=0.0)
        engine.emit_event(event_id="PHY", kind=PHYSICAL, source="a", target="b", amount=1.0)
        engine.mark_ready()
        engine.accept({"ANIMO": 1})
        self.assertEqual([e.event_id for e in engine.committed_events], ["PHY"])

    def test_T12_checkpoint_only_at_accepted_boundary(self):
        engine = RuntimeFixture({"x": 1})
        self.assertEqual(engine.checkpoint()["accepted_generation"], 0)
        begin_basic(engine)
        with self.assertRaises(ContractError):
            engine.checkpoint()

    def test_T13_coupled_barrier_has_no_partial_commit(self):
        engine = RuntimeFixture({"x": 1}, {"ANIMO": 0, "HYDRO": 7, "CROP": 3})
        begin_basic(engine, participants=["ANIMO", "HYDRO", "CROP"])
        engine.mutate("x", 2)
        engine.mark_ready()
        owners_before = dict(engine.owner_generations)
        accepted_before = dict(engine.accepted_values)
        with self.assertRaises(ContractError):
            engine.accept({"ANIMO": 1, "HYDRO": 8})
        self.assertEqual(engine.owner_generations, owners_before)
        self.assertEqual(engine.accepted_values, accepted_before)
        self.assertEqual(engine.phase, engine.TRIAL_READY)
        engine.accept({"ANIMO": 1, "HYDRO": 8, "CROP": 4})
        self.assertEqual(engine.owner_generations, {"ANIMO": 1, "HYDRO": 8, "CROP": 4})
        self.assertEqual(engine.accepted_values["x"], 2)

    def test_T14_reject_then_replay_matches_clean_fixture(self):
        replay = RuntimeFixture({"x": 10})
        begin_basic(replay, interval="I1", trial="reject-me")
        replay.mutate("x", 99)
        replay.emit_event(event_id="TEMP", kind=PHYSICAL, source="soil", target="crop", amount=9.0)
        replay.reject()

        begin_basic(replay, interval="I1", trial="replay")
        replay.mutate("x", 15)
        replay.emit_event(event_id="UPTAKE", kind=PHYSICAL, source="soil", target="crop", amount=2.0)
        replay.mark_ready()
        replay.accept({"ANIMO": 1})

        clean = RuntimeFixture({"x": 10})
        begin_basic(clean, interval="I1", trial="clean")
        clean.mutate("x", 15)
        clean.emit_event(event_id="UPTAKE", kind=PHYSICAL, source="soil", target="crop", amount=2.0)
        clean.mark_ready()
        clean.accept({"ANIMO": 1})

        self.assertEqual(replay.accepted_values, clean.accepted_values)
        self.assertEqual(replay.owner_generations, clean.owner_generations)
        self.assertEqual(replay.committed_event_signatures(), clean.committed_event_signatures())

    def test_T15_mid_trial_topology_change_rejected(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine)
        before = dict(engine.accepted_values)
        with self.assertRaises(ContractError):
            engine.reconfigure(topology_id="topology-B", config_id="config-B")
        self.assertEqual(engine.accepted_values, before)
        self.assertEqual(engine.topology_id, "topology-A")

    def test_T16_exact_event_endpoint_classifiers(self):
        self.assertFalse(RuntimeFixture.event_selected("management", 0, 0, 1))
        self.assertTrue(RuntimeFixture.event_selected("management", 0.5, 0, 1))
        self.assertTrue(RuntimeFixture.event_selected("management", 1, 0, 1))
        self.assertTrue(RuntimeFixture.event_selected("harvest", 0, 0, 1))
        self.assertTrue(RuntimeFixture.event_selected("harvest", 0.5, 0, 1))
        self.assertFalse(RuntimeFixture.event_selected("harvest", 1, 0, 1))

    def test_T17_crop_uptake_has_one_physical_identity(self):
        engine = RuntimeFixture({"soil_N": 10, "crop_N": 0})
        begin_basic(engine)
        engine.emit_event(event_id="CROP-UPTAKE-1", kind=PHYSICAL, source="soil_N", target="crop_N", amount=2.0)
        with self.assertRaises(ContractError):
            engine.emit_event(event_id="CROP-UPTAKE-1", kind=PHYSICAL, source="soil_N", target="crop_N", amount=2.0)
        engine.record_trace("G_REPORT_ONLY", "crop_bookkeeping", 2.0)
        engine.mark_ready()
        engine.accept({"ANIMO": 1})
        uptake = [e for e in engine.committed_events if e.event_id == "CROP-UPTAKE-1"]
        self.assertEqual(len(uptake), 1)

    def test_T18_sqnu_order_enforced_exactly(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine)
        engine.enforce_sqnu_order([2, 1, 3], [2, 1, 3])
        with self.assertRaises(ContractError):
            engine.enforce_sqnu_order([2, 1, 3], [1, 2, 3])

    def test_T19_phosphorus_transport_phase_is_per_layer_coupled(self):
        engine = RuntimeFixture({"x": 1})
        begin_basic(engine)
        engine.enforce_p_layer_coupling(
            [2, 1],
            [("transport", 2), ("phase", 2), ("transport", 1), ("phase", 1)],
        )
        with self.assertRaises(ContractError):
            engine.enforce_p_layer_coupling(
                [2, 1],
                [("transport", 2), ("transport", 1), ("phase", 2), ("phase", 1)],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
