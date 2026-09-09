"""Qualification-only RC-R3 exact year-boundary continuation harness.

No ANIMO physics is implemented here. The harness encodes the source-qualified
TS01 ordering around a 1 January boundary and the TIME02 candidate requirement
that the shared boundary has one exact identity rather than epsilon-separated
copies.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Callable, Generic, TypeVar


T = TypeVar("T")
CALENDAR_CONTRACT_ID = "ANIMO_PG_86400_NOLEAPSECONDS_V1"


class YearBoundaryContractError(ValueError):
    """Raised when the qualification-only year-boundary contract is violated."""


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise YearBoundaryContractError(f"{label}: integer required")
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
            raise YearBoundaryContractError("unsupported calendar_contract_id")
        if den <= 0:
            raise YearBoundaryContractError("subday_denominator must be positive")
        if num < 0 or num >= den:
            raise YearBoundaryContractError("subday fraction must satisfy 0 <= numerator < denominator")
        if gcd(num, den) != 1:
            raise YearBoundaryContractError("subday fraction must be reduced")
        object.__setattr__(self, "day_index", day)

    @property
    def rational_day(self) -> Fraction:
        return Fraction(self.day_index, 1) + Fraction(
            self.subday_numerator, self.subday_denominator
        )


@dataclass(frozen=True)
class YearBoundary:
    boundary: ExactTime
    civil_label: str

    @classmethod
    def january_first(cls, *, boundary: ExactTime, year: int) -> "YearBoundary":
        if isinstance(year, bool) or not isinstance(year, int) or year < 1:
            raise YearBoundaryContractError("year: positive integer required")
        if boundary.subday_numerator != 0:
            raise YearBoundaryContractError("year boundary must be exact midnight")
        return cls(boundary=boundary, civil_label=f"{year:04d}-01-01T00:00:00")


@dataclass(frozen=True)
class BoundaryCheckpoint(Generic[T]):
    accepted_time: ExactTime
    accepted_state: T


@dataclass(frozen=True)
class LifecycleTrace(Generic[T]):
    accepted_state: T
    events: tuple[str, ...]
    checkpoint: BoundaryCheckpoint[T] | None


def close_interval_at_year_boundary(
    *,
    t0: ExactTime,
    t1: ExactTime,
    year_boundary: YearBoundary,
    accepted_state: T,
    execute_physical_interval: Callable[[T], T],
    close_prior_year_output: Callable[[T], None],
    checkpoint_after_closeout: bool,
) -> LifecycleTrace[T]:
    """Execute physical t0->t1, then prior-year closeout at exact t1."""

    if t1.rational_day <= t0.rational_day:
        raise YearBoundaryContractError("interval requires t1 > t0")
    if t1 != year_boundary.boundary:
        raise YearBoundaryContractError("RC-R3 closing interval must end exactly at year boundary")

    events: list[str] = []
    next_state = execute_physical_interval(accepted_state)
    events.append("PHYSICAL_TO_T1")
    close_prior_year_output(next_state)
    events.append("PRIOR_YEAR_CLOSEOUT_AFTER_PHYSICAL_T1")

    checkpoint = None
    if checkpoint_after_closeout:
        checkpoint = BoundaryCheckpoint(accepted_time=t1, accepted_state=next_state)
        events.append("CHECKPOINT_ACCEPTED_BOUNDARY")
    return LifecycleTrace(
        accepted_state=next_state,
        events=tuple(events),
        checkpoint=checkpoint,
    )


def start_next_year_interval(
    *,
    t0: ExactTime,
    year_boundary: YearBoundary,
    accepted_state: T,
    initialize_new_year_inputs: Callable[[T], T],
) -> LifecycleTrace[T]:
    """Apply new-year start semantics from the same exact boundary coordinate."""

    if t0 != year_boundary.boundary:
        raise YearBoundaryContractError("next interval must start at exact year boundary")
    next_state = initialize_new_year_inputs(accepted_state)
    return LifecycleTrace(
        accepted_state=next_state,
        events=("NEXT_INTERVAL_NEW_YEAR_START_AT_SAME_EXACT_T1",),
        checkpoint=None,
    )


def restore_year_boundary_checkpoint(
    *, checkpoint: BoundaryCheckpoint[T], year_boundary: YearBoundary
) -> T:
    if checkpoint.accepted_time != year_boundary.boundary:
        raise YearBoundaryContractError("checkpoint accepted time is not the exact year boundary")
    return checkpoint.accepted_state
