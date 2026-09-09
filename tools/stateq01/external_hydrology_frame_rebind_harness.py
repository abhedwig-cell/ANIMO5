"""Qualification-only RC-R6 exact external hydrology frame rebind guard.

This module contains no hydrology or ANIMO physics. It encodes the STATEQ01,
TIME02 and candidate architecture rule that an external hydrology frame may be
bound to a restored interval only when chronology and provenance identities
match exactly before any process-state construction is allowed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Callable, Generic, TypeVar


T = TypeVar("T")
CALENDAR_CONTRACT_ID = "ANIMO_PG_86400_NOLEAPSECONDS_V1"


class FrameRebindError(ValueError):
    """Raised before process mutation when external frame binding is invalid."""


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise FrameRebindError(f"{label}: integer required")
    return value


def _identity(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FrameRebindError(f"{label}: non-empty identity required")
    return value


@dataclass(frozen=True)
class ExactTime:
    day_index: int
    subday_numerator: int = 0
    subday_denominator: int = 1
    calendar_contract_id: str = CALENDAR_CONTRACT_ID

    def __post_init__(self) -> None:
        day = _integer(self.day_index, "day_index")
        num = _integer(self.subday_numerator, "subday_numerator")
        den = _integer(self.subday_denominator, "subday_denominator")
        if self.calendar_contract_id != CALENDAR_CONTRACT_ID:
            raise FrameRebindError("unsupported calendar_contract_id")
        if den <= 0:
            raise FrameRebindError("subday_denominator must be positive")
        if num < 0 or num >= den:
            raise FrameRebindError("subday fraction must satisfy 0 <= numerator < denominator")
        if gcd(num, den) != 1:
            raise FrameRebindError("subday fraction must be reduced")
        object.__setattr__(self, "day_index", day)

    @property
    def rational_day(self) -> Fraction:
        return Fraction(self.day_index, 1) + Fraction(
            self.subday_numerator, self.subday_denominator
        )


@dataclass(frozen=True)
class IntervalIdentity:
    t0: ExactTime
    t1: ExactTime
    accepted_generation: int
    geometry_id: str
    hydrology_schema_id: str
    configuration_id: str

    @classmethod
    def build(
        cls,
        *,
        t0: ExactTime,
        t1: ExactTime,
        accepted_generation: object,
        geometry_id: object,
        hydrology_schema_id: object,
        configuration_id: object,
    ) -> "IntervalIdentity":
        generation = _integer(accepted_generation, "accepted_generation")
        if generation < 0:
            raise FrameRebindError("accepted_generation must be non-negative")
        if not isinstance(t0, ExactTime) or not isinstance(t1, ExactTime):
            raise FrameRebindError("interval times must be exact canonical candidates")
        if t1.rational_day <= t0.rational_day:
            raise FrameRebindError("interval requires exact t1 > t0")
        return cls(
            t0=t0,
            t1=t1,
            accepted_generation=generation,
            geometry_id=_identity(geometry_id, "geometry_id"),
            hydrology_schema_id=_identity(hydrology_schema_id, "hydrology_schema_id"),
            configuration_id=_identity(configuration_id, "configuration_id"),
        )


@dataclass(frozen=True)
class HydrologyFrame:
    frame_id: str
    t0: ExactTime
    t1: ExactTime
    producer_accepted_generation: int
    geometry_id: str
    hydrology_schema_id: str
    configuration_id: str
    content_fingerprint: str

    @classmethod
    def build(
        cls,
        *,
        frame_id: object,
        t0: ExactTime,
        t1: ExactTime,
        producer_accepted_generation: object,
        geometry_id: object,
        hydrology_schema_id: object,
        configuration_id: object,
        content_fingerprint: object,
    ) -> "HydrologyFrame":
        generation = _integer(
            producer_accepted_generation, "producer_accepted_generation"
        )
        if generation < 0:
            raise FrameRebindError("producer generation must be non-negative")
        if not isinstance(t0, ExactTime) or not isinstance(t1, ExactTime):
            raise FrameRebindError("frame times must be exact canonical candidates")
        return cls(
            frame_id=_identity(frame_id, "frame_id"),
            t0=t0,
            t1=t1,
            producer_accepted_generation=generation,
            geometry_id=_identity(geometry_id, "geometry_id"),
            hydrology_schema_id=_identity(hydrology_schema_id, "hydrology_schema_id"),
            configuration_id=_identity(configuration_id, "configuration_id"),
            content_fingerprint=_identity(content_fingerprint, "content_fingerprint"),
        )


@dataclass(frozen=True)
class RebindResult(Generic[T]):
    interval: IntervalIdentity
    frame: HydrologyFrame
    payload: T


def rebind_mismatches(
    interval: IntervalIdentity, frame: HydrologyFrame
) -> tuple[str, ...]:
    mismatches: list[str] = []
    if frame.t0 != interval.t0:
        mismatches.append("t0")
    if frame.t1 != interval.t1:
        mismatches.append("t1")
    if frame.producer_accepted_generation != interval.accepted_generation:
        mismatches.append("accepted_generation")
    if frame.geometry_id != interval.geometry_id:
        mismatches.append("geometry_id")
    if frame.hydrology_schema_id != interval.hydrology_schema_id:
        mismatches.append("hydrology_schema_id")
    if frame.configuration_id != interval.configuration_id:
        mismatches.append("configuration_id")
    return tuple(mismatches)


def guarded_rebind(
    *,
    interval: IntervalIdentity,
    frame: HydrologyFrame,
    consume_frame_and_construct_process_state: Callable[[], T],
) -> RebindResult[T]:
    """Fail closed on exact interval/provenance mismatch before consumption."""

    mismatches = rebind_mismatches(interval, frame)
    if mismatches:
        raise FrameRebindError(
            "external hydrology frame mismatch before process execution: "
            + ",".join(mismatches)
        )
    payload = consume_frame_and_construct_process_state()
    return RebindResult(interval=interval, frame=frame, payload=payload)
