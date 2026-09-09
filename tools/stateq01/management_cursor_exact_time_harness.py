"""Qualification-only exact-time management cursor harness for ANIMO-STATEQ01.

This module consumes the candidate TIME02 exact rational coordinate and the
STATEQ01 explicit-next-event cursor contract. It contains no ANIMO physics and
is not a production scheduler. Its narrow purpose is to make RC-R2 restart
ownership executable without floating tolerance or time-only cursor inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Mapping, Sequence


CALENDAR_CONTRACT_ID = "ANIMO_PG_86400_NOLEAPSECONDS_V1"
END_CURSOR = "__END__"


class CursorContractError(ValueError):
    """Raised when an exact-time management continuation contract is violated."""


def _require_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CursorContractError(f"{label}: expected integer")
    return value


@dataclass(frozen=True)
class ExactTime:
    day_index: int
    subday_numerator: int = 0
    subday_denominator: int = 1
    calendar_contract_id: str = CALENDAR_CONTRACT_ID

    def __post_init__(self) -> None:
        day = _require_int(self.day_index, "day_index")
        num = _require_int(self.subday_numerator, "subday_numerator")
        den = _require_int(self.subday_denominator, "subday_denominator")
        if self.calendar_contract_id != CALENDAR_CONTRACT_ID:
            raise CursorContractError("unsupported calendar_contract_id")
        if den <= 0:
            raise CursorContractError("subday_denominator: must be positive")
        if num < 0 or num >= den:
            raise CursorContractError("subday fraction must satisfy 0 <= numerator < denominator")
        if gcd(num, den) != 1:
            raise CursorContractError("subday fraction must be reduced")
        object.__setattr__(self, "day_index", day)

    @property
    def rational_day(self) -> Fraction:
        return Fraction(self.day_index, 1) + Fraction(
            self.subday_numerator, self.subday_denominator
        )

    def _assert_same_calendar(self, other: "ExactTime") -> None:
        if self.calendar_contract_id != other.calendar_contract_id:
            raise CursorContractError("cross-calendar comparison is not admitted")

    def __lt__(self, other: "ExactTime") -> bool:
        self._assert_same_calendar(other)
        return self.rational_day < other.rational_day

    def __le__(self, other: "ExactTime") -> bool:
        self._assert_same_calendar(other)
        return self.rational_day <= other.rational_day

    def __gt__(self, other: "ExactTime") -> bool:
        self._assert_same_calendar(other)
        return self.rational_day > other.rational_day

    def __ge__(self, other: "ExactTime") -> bool:
        self._assert_same_calendar(other)
        return self.rational_day >= other.rational_day

    def to_payload(self) -> dict[str, str]:
        return {
            "calendar_contract_id": self.calendar_contract_id,
            "day_index": str(self.day_index),
            "subday_numerator": str(self.subday_numerator),
            "subday_denominator": str(self.subday_denominator),
        }

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "ExactTime":
        required = {
            "calendar_contract_id",
            "day_index",
            "subday_numerator",
            "subday_denominator",
        }
        missing = required.difference(payload)
        if missing:
            raise CursorContractError(
                "accepted_time: missing field(s): " + ",".join(sorted(missing))
            )
        if payload["calendar_contract_id"] != CALENDAR_CONTRACT_ID:
            raise CursorContractError("accepted_time: incompatible calendar contract")
        try:
            day = int(str(payload["day_index"]))
            num = int(str(payload["subday_numerator"]))
            den = int(str(payload["subday_denominator"]))
        except ValueError as exc:
            raise CursorContractError("accepted_time: non-integer decimal field") from exc
        return cls(day, num, den)


@dataclass(frozen=True)
class ManagementEvent:
    event_id: str
    boundary: ExactTime

    def __post_init__(self) -> None:
        if not self.event_id or self.event_id == END_CURSOR:
            raise CursorContractError("event_id: invalid or reserved")


@dataclass(frozen=True)
class ManagementSchedule:
    schedule_identity: str
    events: tuple[ManagementEvent, ...]

    @classmethod
    def build(
        cls, schedule_identity: str, events: Sequence[ManagementEvent]
    ) -> "ManagementSchedule":
        if not schedule_identity:
            raise CursorContractError("schedule_identity: required")
        event_tuple = tuple(events)
        ids = [event.event_id for event in event_tuple]
        if len(ids) != len(set(ids)):
            raise CursorContractError("event ids must be unique")
        for previous, current in zip(event_tuple, event_tuple[1:]):
            if current.boundary < previous.boundary:
                raise CursorContractError("normalized schedule boundaries must be ordered")
        return cls(schedule_identity=schedule_identity, events=event_tuple)

    def index_of(self, event_id: str) -> int:
        for index, event in enumerate(self.events):
            if event.event_id == event_id:
                return index
        raise CursorContractError(f"next_event_id: unknown event {event_id!r}")


@dataclass(frozen=True)
class CursorState:
    accepted_time: ExactTime
    next_event_index: int


@dataclass(frozen=True)
class IntervalResult:
    accepted_state: CursorState
    delivered_event_ids: tuple[str, ...]


def initial_cursor(schedule: ManagementSchedule, accepted_time: ExactTime) -> CursorState:
    """Construct only a known initial cursor, never a restart reconstruction rule."""

    return CursorState(accepted_time=accepted_time, next_event_index=0)


def advance_interval(
    schedule: ManagementSchedule, state: CursorState, t1: ExactTime
) -> IntervalResult:
    """Apply the source management endpoint rule once for one accepted interval.

    Revision-53 calls the management addition reader at most once per main-loop
    interval. This harness therefore considers only the explicit current cursor
    event. The exact membership predicate is TIME02's source-equivalent
    ``t0 < E <= t1``. No epsilon is used.
    """

    t0 = state.accepted_time
    if not t0 < t1:
        raise CursorContractError("interval end must be strictly after accepted t0")
    if state.next_event_index < 0 or state.next_event_index > len(schedule.events):
        raise CursorContractError("next_event_index outside schedule")

    next_index = state.next_event_index
    delivered: tuple[str, ...] = ()
    if next_index < len(schedule.events):
        event = schedule.events[next_index]
        if t0 < event.boundary and event.boundary <= t1:
            delivered = (event.event_id,)
            next_index += 1

    return IntervalResult(
        accepted_state=CursorState(accepted_time=t1, next_event_index=next_index),
        delivered_event_ids=delivered,
    )


def checkpoint_payload(
    schedule: ManagementSchedule, state: CursorState
) -> dict[str, object]:
    if state.next_event_index < 0 or state.next_event_index > len(schedule.events):
        raise CursorContractError("next_event_index outside schedule")
    next_event_id = (
        END_CURSOR
        if state.next_event_index == len(schedule.events)
        else schedule.events[state.next_event_index].event_id
    )
    return {
        "schedule_identity": schedule.schedule_identity,
        "accepted_time": state.accepted_time.to_payload(),
        "next_event_id": next_event_id,
    }


def restore_checkpoint(
    schedule: ManagementSchedule, payload: Mapping[str, object]
) -> CursorState:
    """Restore from explicit schedule identity + next event identity.

    The next event boundary is deliberately absent from the checkpoint. It is
    derived from the bound immutable schedule under the exact TIME02 candidate
    coordinate. Missing cursor identity is a hard failure; accepted time alone
    is never used to search for the first future event.
    """

    required = {"schedule_identity", "accepted_time", "next_event_id"}
    missing = required.difference(payload)
    if missing:
        raise CursorContractError(
            "checkpoint: missing mandatory field(s): " + ",".join(sorted(missing))
        )
    if payload["schedule_identity"] != schedule.schedule_identity:
        raise CursorContractError("checkpoint schedule identity mismatch")
    accepted_payload = payload["accepted_time"]
    if not isinstance(accepted_payload, Mapping):
        raise CursorContractError("accepted_time: expected mapping")
    accepted_time = ExactTime.from_payload(accepted_payload)
    next_event_id = payload["next_event_id"]
    if not isinstance(next_event_id, str) or not next_event_id:
        raise CursorContractError("next_event_id: explicit string identity required")
    if next_event_id == END_CURSOR:
        next_index = len(schedule.events)
    else:
        next_index = schedule.index_of(next_event_id)
    return CursorState(accepted_time=accepted_time, next_event_index=next_index)
