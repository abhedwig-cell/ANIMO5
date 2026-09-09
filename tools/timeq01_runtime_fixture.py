#!/usr/bin/env python3
"""Non-production synthetic runtime fixture for ANIMO-TIMEQ01.

This module implements only the abstract transaction and scheduler semantics
qualified by TIME01/ARCHG02. It contains no ANIMO process physics and provides
no historical B2 evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
import json
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


class ContractError(RuntimeError):
    """Fail-closed contract violation."""


PHYSICAL = "PHYSICAL"
PROVISIONAL = "PROVISIONAL"
REPORT_ONLY = "REPORT_ONLY"
EVENT_KINDS = {PHYSICAL, PROVISIONAL, REPORT_ONLY}

GENERATION_LABELS = {
    "G_ACCEPTED_START",
    "G_MUTATED_EVENT",
    "G_PROVISIONAL",
    "G_ACTUAL_RESULT",
    "G_PREVIOUS_NEIGHBOR",
    "G_SAME_STEP_DERIVED",
    "G_REPORT_ONLY",
}


@dataclass(frozen=True)
class Frame:
    frame_id: str
    interval_id: str
    accepted_generation: int
    topology_id: str
    config_id: str
    geometry_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)

    def signature(self) -> str:
        body = {
            "interval_id": self.interval_id,
            "accepted_generation": self.accepted_generation,
            "topology_id": self.topology_id,
            "config_id": self.config_id,
            "geometry_id": self.geometry_id,
            "payload": self.payload,
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class Event:
    event_id: str
    kind: str
    source: str
    target: str
    amount: float
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def signature(self) -> Tuple[Any, ...]:
        return (
            self.event_id,
            self.kind,
            self.source,
            self.target,
            self.amount,
            json.dumps(self.metadata, sort_keys=True, separators=(",", ":")),
        )


@dataclass(frozen=True)
class TraceRecord:
    label: str
    subject: str
    value: Any


class RuntimeFixture:
    """Small fail-closed transaction state machine.

    Accepted values are immutable while a trial is active. Trial values,
    provisional/report records and physical events are discarded on reject.
    Only physical events are appended to the committed journal on accept.
    """

    ACCEPTED_IDLE = "ACCEPTED_IDLE"
    TRIAL_EXECUTING = "TRIAL_EXECUTING"
    TRIAL_READY = "TRIAL_READY"

    def __init__(
        self,
        accepted_values: Optional[Mapping[str, Any]] = None,
        owner_generations: Optional[Mapping[str, int]] = None,
        *,
        topology_id: str = "topology-A",
        config_id: str = "config-A",
        geometry_id: str = "geometry-A",
    ) -> None:
        self.phase = self.ACCEPTED_IDLE
        self.accepted_values: Dict[str, Any] = deepcopy(dict(accepted_values or {}))
        self.accepted_generation = 0
        self.owner_generations: Dict[str, int] = dict(owner_generations or {"ANIMO": 0})
        self.topology_id = topology_id
        self.config_id = config_id
        self.geometry_id = geometry_id

        self.committed_events: List[Event] = []
        self.used_trial_ids: set[str] = set()
        self.interval_endpoints: Dict[str, Tuple[Any, Any]] = {}
        self.frame_registry: Dict[str, str] = {}

        self.trial_id: Optional[str] = None
        self.interval_id: Optional[str] = None
        self.t0: Any = None
        self.t1: Any = None
        self.trial_values: Optional[Dict[str, Any]] = None
        self.trial_events: List[Event] = []
        self.trial_trace: List[TraceRecord] = []
        self.required_participants: Tuple[str, ...] = tuple()
        self.bound_frame_ids: Tuple[str, ...] = tuple()

    def _require_phase(self, *allowed: str) -> None:
        if self.phase not in allowed:
            raise ContractError(f"phase {self.phase} not in allowed {allowed}")

    def _reset_trial(self) -> None:
        self.phase = self.ACCEPTED_IDLE
        self.trial_id = None
        self.interval_id = None
        self.t0 = None
        self.t1 = None
        self.trial_values = None
        self.trial_events = []
        self.trial_trace = []
        self.required_participants = tuple()
        self.bound_frame_ids = tuple()

    def begin_trial(
        self,
        *,
        interval_id: str,
        trial_id: str,
        t0: Any,
        t1: Any,
        frames: Sequence[Frame] = (),
        topology_id: Optional[str] = None,
        config_id: Optional[str] = None,
        geometry_id: Optional[str] = None,
        required_participants: Optional[Iterable[str]] = None,
    ) -> None:
        self._require_phase(self.ACCEPTED_IDLE)

        if trial_id in self.used_trial_ids:
            raise ContractError("trial_id must be fresh on every attempt")

        endpoint = (t0, t1)
        if interval_id in self.interval_endpoints and self.interval_endpoints[interval_id] != endpoint:
            raise ContractError("changed interval endpoint requires a new interval_id")

        topo = topology_id or self.topology_id
        cfg = config_id or self.config_id
        geom = geometry_id or self.geometry_id
        if topo != self.topology_id or cfg != self.config_id or geom != self.geometry_id:
            raise ContractError("trial identity must bind current topology/configuration/geometry")

        pending_frame_signatures: Dict[str, str] = {}
        for frame in frames:
            if frame.interval_id != interval_id:
                raise ContractError("frame interval_id does not match trial interval")
            if frame.accepted_generation != self.accepted_generation:
                raise ContractError("stale or future accepted generation in frame")
            if frame.topology_id != topo or frame.config_id != cfg or frame.geometry_id != geom:
                raise ContractError("frame topology/configuration/geometry does not match trial")
            signature = frame.signature()
            previous = self.frame_registry.get(frame.frame_id)
            if previous is not None and previous != signature:
                raise ContractError("frame_id reused with changed content")
            if frame.frame_id in pending_frame_signatures and pending_frame_signatures[frame.frame_id] != signature:
                raise ContractError("duplicate frame_id has inconsistent content")
            pending_frame_signatures[frame.frame_id] = signature

        participants = tuple(required_participants or self.owner_generations.keys())
        if not participants:
            raise ContractError("at least one coupled participant is required")
        unknown = [p for p in participants if p not in self.owner_generations]
        if unknown:
            raise ContractError(f"unknown coupled participants: {unknown}")

        self.interval_endpoints.setdefault(interval_id, endpoint)
        self.frame_registry.update(pending_frame_signatures)
        self.used_trial_ids.add(trial_id)
        self.phase = self.TRIAL_EXECUTING
        self.trial_id = trial_id
        self.interval_id = interval_id
        self.t0 = t0
        self.t1 = t1
        self.trial_values = deepcopy(self.accepted_values)
        self.required_participants = participants
        self.bound_frame_ids = tuple(frame.frame_id for frame in frames)
        self.trial_trace = [TraceRecord("G_ACCEPTED_START", "accepted_generation", self.accepted_generation)]

    def mutate(self, key: str, value: Any, *, label: str = "G_MUTATED_EVENT") -> None:
        self._require_phase(self.TRIAL_EXECUTING)
        if label not in GENERATION_LABELS:
            raise ContractError(f"unknown generation label {label}")
        assert self.trial_values is not None
        self.trial_values[key] = deepcopy(value)
        self.trial_trace.append(TraceRecord(label, key, deepcopy(value)))

    def read_trial(self, key: str) -> Any:
        self._require_phase(self.TRIAL_EXECUTING, self.TRIAL_READY)
        assert self.trial_values is not None
        return deepcopy(self.trial_values[key])

    def read_previous_neighbor(self, key: str) -> Any:
        self._require_phase(self.TRIAL_EXECUTING, self.TRIAL_READY)
        value = deepcopy(self.accepted_values[key])
        self.trial_trace.append(TraceRecord("G_PREVIOUS_NEIGHBOR", key, value))
        return value

    def record_trace(self, label: str, subject: str, value: Any) -> None:
        self._require_phase(self.TRIAL_EXECUTING, self.TRIAL_READY)
        if label not in GENERATION_LABELS:
            raise ContractError(f"unknown generation label {label}")
        self.trial_trace.append(TraceRecord(label, subject, deepcopy(value)))

    def emit_event(
        self,
        *,
        event_id: str,
        kind: str,
        source: str,
        target: str,
        amount: float,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Event:
        self._require_phase(self.TRIAL_EXECUTING)
        if kind not in EVENT_KINDS:
            raise ContractError(f"unknown event kind {kind}")
        if any(e.event_id == event_id for e in self.trial_events):
            raise ContractError("event_id must be unique within a trial")
        if any(e.event_id == event_id for e in self.committed_events):
            raise ContractError("committed event_id cannot be reused")
        event = Event(event_id, kind, source, target, amount, dict(metadata or {}))
        self.trial_events.append(event)
        label = {
            PHYSICAL: "G_ACTUAL_RESULT",
            PROVISIONAL: "G_PROVISIONAL",
            REPORT_ONLY: "G_REPORT_ONLY",
        }[kind]
        self.trial_trace.append(TraceRecord(label, event_id, event.signature()))
        return event

    def mark_ready(self) -> None:
        self._require_phase(self.TRIAL_EXECUTING)
        self.phase = self.TRIAL_READY

    def accept(self, participant_next_generation: Mapping[str, int]) -> None:
        self._require_phase(self.TRIAL_READY)
        expected = {
            participant: self.owner_generations[participant] + 1
            for participant in self.required_participants
        }
        supplied = {participant: participant_next_generation.get(participant) for participant in self.required_participants}
        if supplied != expected:
            raise ContractError(f"coupled accept barrier incomplete or invalid: expected {expected}, got {supplied}")

        assert self.trial_values is not None
        new_values = deepcopy(self.trial_values)
        new_physical = [e for e in self.trial_events if e.kind == PHYSICAL]
        new_owner_generations = dict(self.owner_generations)
        for participant, generation in expected.items():
            new_owner_generations[participant] = generation

        # Atomic publication happens only after all validation above.
        self.accepted_values = new_values
        self.committed_events.extend(new_physical)
        self.owner_generations = new_owner_generations
        self.accepted_generation += 1
        self._reset_trial()

    def reject(self) -> None:
        self._require_phase(self.TRIAL_EXECUTING, self.TRIAL_READY)
        self._reset_trial()

    def checkpoint(self) -> Dict[str, Any]:
        self._require_phase(self.ACCEPTED_IDLE)
        return {
            "accepted_generation": self.accepted_generation,
            "accepted_values": deepcopy(self.accepted_values),
            "owner_generations": dict(self.owner_generations),
            "topology_id": self.topology_id,
            "config_id": self.config_id,
            "geometry_id": self.geometry_id,
        }

    def reconfigure(self, *, topology_id: str, config_id: str, geometry_id: Optional[str] = None) -> None:
        if self.phase != self.ACCEPTED_IDLE:
            raise ContractError("mid-trial topology/configuration change is forbidden")
        self.topology_id = topology_id
        self.config_id = config_id
        if geometry_id is not None:
            self.geometry_id = geometry_id

    @staticmethod
    def event_selected(kind: str, event_time: Any, t0: Any, t1: Any) -> bool:
        if kind == "management":
            return t0 < event_time <= t1
        if kind == "harvest":
            return t0 <= event_time < t1
        raise ContractError(f"unsupported event classifier {kind}")

    def enforce_sqnu_order(self, expected_order: Sequence[int], observed_order: Sequence[int]) -> None:
        self._require_phase(self.TRIAL_EXECUTING, self.TRIAL_READY)
        if list(observed_order) != list(expected_order):
            raise ContractError("Sqnu traversal differs from bound source-equivalence order")
        self.trial_trace.append(TraceRecord("G_SAME_STEP_DERIVED", "Sqnu", list(observed_order)))

    def enforce_p_layer_coupling(
        self,
        layers: Sequence[int],
        observed_trace: Sequence[Tuple[str, int]],
    ) -> None:
        self._require_phase(self.TRIAL_EXECUTING, self.TRIAL_READY)
        expected: List[Tuple[str, int]] = []
        for layer in layers:
            expected.extend([("transport", layer), ("phase", layer)])
        if list(observed_trace) != expected:
            raise ContractError("phosphorus transport/phase trace is not coupled per layer")
        self.trial_trace.append(TraceRecord("G_SAME_STEP_DERIVED", "P_layer_coupling", list(observed_trace)))

    def committed_event_signatures(self) -> Tuple[Tuple[Any, ...], ...]:
        return tuple(event.signature() for event in self.committed_events)
