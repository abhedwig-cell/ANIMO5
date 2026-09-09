"""Qualification-only transaction harness for ANIMO-STATEQ01 restricted core.

The harness exists only to test fail-before-mutate ordering around the
restricted-core guard. It is not a production transaction implementation and
contains no ANIMO physics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Mapping, TypeVar

from restricted_core_guard import GuardResult, validate_restricted_core_envelope


T = TypeVar("T")


@dataclass(frozen=True)
class HarnessResult(Generic[T]):
    stage: str
    guard: GuardResult
    payload: T


def guarded_restore(
    *,
    hydrology_mode: str,
    accepted_surface: Mapping[str, object],
    candidate_surface: Mapping[str, object],
    layer0_restart: Mapping[str, object],
    phosphorus_active: bool,
    construct_accepted_state: Callable[[], T],
) -> HarnessResult[T]:
    """Validate first, then construct restored accepted state exactly once."""

    guard = validate_restricted_core_envelope(
        hydrology_mode=hydrology_mode,
        accepted_surface=accepted_surface,
        candidate_surface=candidate_surface,
        layer0_restart=layer0_restart,
        phosphorus_active=phosphorus_active,
    )
    payload = construct_accepted_state()
    return HarnessResult(stage="RESTORED_ACCEPTED", guard=guard, payload=payload)


def guarded_candidate_accept(
    *,
    hydrology_mode: str,
    accepted_surface: Mapping[str, object],
    candidate_surface: Mapping[str, object],
    layer0_state: Mapping[str, object],
    phosphorus_active: bool,
    run_chemistry_and_management: Callable[[], T],
) -> HarnessResult[T]:
    """Validate candidate hydrology before any chemistry/management mutation."""

    guard = validate_restricted_core_envelope(
        hydrology_mode=hydrology_mode,
        accepted_surface=accepted_surface,
        candidate_surface=candidate_surface,
        layer0_restart=layer0_state,
        phosphorus_active=phosphorus_active,
    )
    payload = run_chemistry_and_management()
    return HarnessResult(stage="CANDIDATE_PROCESSING_ALLOWED", guard=guard, payload=payload)
