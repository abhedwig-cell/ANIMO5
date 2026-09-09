"""Qualification-only restore identity guard for ANIMO-STATEQ01 RC-R6/RC-R7.

This module contains no ANIMO physics and is not a production restart
implementation. It makes the candidate checkpoint fail-before-mutate identity
contract executable for exact external hydrology frame binding and exact
geometry/P-site cardinality compatibility.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from math import gcd
from typing import Callable, Mapping, Sequence, TypeVar


CALENDAR_CONTRACT_ID = "ANIMO_PG_86400_NOLEAPSECONDS_V1"
T = TypeVar("T")


class RestoreIdentityError(ValueError):
    """Raised before accepted-state construction when restore identity fails."""


def _require_nonempty_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RestoreIdentityError(f"{label}: non-empty string required")
    return value


def _require_nonnegative_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RestoreIdentityError(f"{label}: non-negative integer required")
    return value


def _decimal_string(value: object, label: str) -> int:
    # TIME02 canonical JSON identity uses decimal strings. Floats and implicit
    # numeric coercion are deliberately rejected here.
    if not isinstance(value, str) or not value:
        raise RestoreIdentityError(f"{label}: canonical decimal string required")
    if value[0] == "-":
        digits = value[1:]
    else:
        digits = value
    if not digits.isdigit():
        raise RestoreIdentityError(f"{label}: canonical decimal string required")
    if len(digits) > 1 and digits[0] == "0":
        raise RestoreIdentityError(f"{label}: non-canonical leading zero")
    if value == "-0":
        raise RestoreIdentityError(f"{label}: negative zero is non-canonical")
    return int(value)


@dataclass(frozen=True)
class ExactTimeIdentity:
    calendar_contract_id: str
    day_index: int
    subday_numerator: int
    subday_denominator: int

    @classmethod
    def from_payload(cls, payload: Mapping[str, object], label: str) -> "ExactTimeIdentity":
        if not isinstance(payload, Mapping):
            raise RestoreIdentityError(f"{label}: mapping required")
        calendar = _require_nonempty_text(payload.get("calendar_contract_id"), f"{label}.calendar_contract_id")
        if calendar != CALENDAR_CONTRACT_ID:
            raise RestoreIdentityError(f"{label}: incompatible calendar contract")
        day = _decimal_string(payload.get("day_index"), f"{label}.day_index")
        num = _decimal_string(payload.get("subday_numerator"), f"{label}.subday_numerator")
        den = _decimal_string(payload.get("subday_denominator"), f"{label}.subday_denominator")
        if den <= 0:
            raise RestoreIdentityError(f"{label}: denominator must be positive")
        if num < 0 or num >= den:
            raise RestoreIdentityError(f"{label}: require 0 <= numerator < denominator")
        if gcd(num, den) != 1:
            raise RestoreIdentityError(f"{label}: rational fraction must be reduced")
        return cls(calendar, day, num, den)


def _identity(mapping: Mapping[str, object], key: str, label: str) -> str:
    return _require_nonempty_text(mapping.get(key), f"{label}.{key}")


def _validate_p_payload(
    *,
    checkpoint: Mapping[str, object],
    soil_layers: int,
    fast_sites: int,
    slow_sites: int,
    p_cycle: bool,
) -> None:
    fast_payload = checkpoint.get("p_fast_sites_by_layer", ())
    slow_payload = checkpoint.get("p_slow_sites_by_layer", ())

    if not p_cycle:
        if fast_sites != 0 or slow_sites != 0:
            raise RestoreIdentityError("P inactive but nonzero site cardinality declared")
        if fast_payload not in ((), [], None) or slow_payload not in ((), [], None):
            raise RestoreIdentityError("P inactive but site-resolved P payload present")
        return

    if not isinstance(fast_payload, Sequence) or isinstance(fast_payload, (str, bytes)):
        raise RestoreIdentityError("checkpoint.p_fast_sites_by_layer: sequence required")
    if not isinstance(slow_payload, Sequence) or isinstance(slow_payload, (str, bytes)):
        raise RestoreIdentityError("checkpoint.p_slow_sites_by_layer: sequence required")
    if len(fast_payload) != soil_layers:
        raise RestoreIdentityError("fast-site P payload soil-layer cardinality mismatch")
    if len(slow_payload) != soil_layers:
        raise RestoreIdentityError("slow-site P payload soil-layer cardinality mismatch")

    for row in fast_payload:
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)) or len(row) != fast_sites:
            raise RestoreIdentityError("fast-site P payload site cardinality mismatch")
    for row in slow_payload:
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)) or len(row) != slow_sites:
            raise RestoreIdentityError("slow-site P payload site cardinality mismatch")


def validate_restore_identity(
    *,
    checkpoint: Mapping[str, object],
    runtime_target: Mapping[str, object],
    hydrology_frame: Mapping[str, object],
    next_interval_t1: Mapping[str, object],
) -> dict[str, object]:
    """Validate RC-R6/RC-R7 identity compatibility without mutating inputs."""

    # Take snapshots only to assert non-mutation inside this qualification guard.
    before_checkpoint = deepcopy(checkpoint)
    before_target = deepcopy(runtime_target)
    before_frame = deepcopy(hydrology_frame)
    before_t1 = deepcopy(next_interval_t1)

    accepted_t0 = ExactTimeIdentity.from_payload(
        checkpoint.get("accepted_time", {}), "checkpoint.accepted_time"
    )
    interval_t1 = ExactTimeIdentity.from_payload(next_interval_t1, "next_interval_t1")
    frame_t0 = ExactTimeIdentity.from_payload(hydrology_frame.get("t0", {}), "hydrology_frame.t0")
    frame_t1 = ExactTimeIdentity.from_payload(hydrology_frame.get("t1", {}), "hydrology_frame.t1")

    if frame_t0 != accepted_t0:
        raise RestoreIdentityError("hydrology frame t0 does not equal checkpoint accepted time")
    if frame_t1 != interval_t1:
        raise RestoreIdentityError("hydrology frame t1 does not equal requested next interval t1")

    # Checkpoint identity against the target runtime topology.
    exact_header_keys = (
        "profile_id",
        "configuration_identity",
        "physical_layout_id",
        "geometry_identity",
    )
    for key in exact_header_keys:
        if _identity(checkpoint, key, "checkpoint") != _identity(runtime_target, key, "runtime_target"):
            raise RestoreIdentityError(f"{key}: checkpoint/runtime mismatch")

    checkpoint_generation = _identity(checkpoint, "accepted_generation_id", "checkpoint")
    expected_generation = _identity(runtime_target, "accepted_generation_id", "runtime_target")
    if checkpoint_generation != expected_generation:
        raise RestoreIdentityError("accepted_generation_id: checkpoint/runtime mismatch")

    cp_layers = _require_nonnegative_int(checkpoint.get("soil_layer_count"), "checkpoint.soil_layer_count")
    rt_layers = _require_nonnegative_int(runtime_target.get("soil_layer_count"), "runtime_target.soil_layer_count")
    if cp_layers <= 0 or cp_layers != rt_layers:
        raise RestoreIdentityError("soil_layer_count: checkpoint/runtime mismatch")

    cp_p_cycle = checkpoint.get("p_cycle")
    rt_p_cycle = runtime_target.get("p_cycle")
    if not isinstance(cp_p_cycle, bool) or not isinstance(rt_p_cycle, bool):
        raise RestoreIdentityError("p_cycle: boolean required")
    if cp_p_cycle != rt_p_cycle:
        raise RestoreIdentityError("p_cycle: checkpoint/runtime mismatch")

    cp_fast = _require_nonnegative_int(checkpoint.get("p_fast_site_count"), "checkpoint.p_fast_site_count")
    cp_slow = _require_nonnegative_int(checkpoint.get("p_slow_site_count"), "checkpoint.p_slow_site_count")
    rt_fast = _require_nonnegative_int(runtime_target.get("p_fast_site_count"), "runtime_target.p_fast_site_count")
    rt_slow = _require_nonnegative_int(runtime_target.get("p_slow_site_count"), "runtime_target.p_slow_site_count")
    if cp_fast != rt_fast:
        raise RestoreIdentityError("p_fast_site_count: checkpoint/runtime mismatch")
    if cp_slow != rt_slow:
        raise RestoreIdentityError("p_slow_site_count: checkpoint/runtime mismatch")

    _validate_p_payload(
        checkpoint=checkpoint,
        soil_layers=cp_layers,
        fast_sites=cp_fast,
        slow_sites=cp_slow,
        p_cycle=cp_p_cycle,
    )

    # External hydrology remains external ownership. The checkpoint does not
    # acquire the frame state; it binds exact identities for a compatible frame.
    frame_exact_matches = {
        "physical_layout_id": checkpoint["physical_layout_id"],
        "geometry_identity": checkpoint["geometry_identity"],
        "schema_identity": runtime_target.get("hydrology_schema_identity"),
        "content_identity": runtime_target.get("hydrology_content_identity"),
        "producer_accepted_generation_id": runtime_target.get("hydrology_producer_generation_id"),
    }
    for key, expected in frame_exact_matches.items():
        expected_text = _require_nonempty_text(expected, f"runtime_target.expected_{key}")
        actual_text = _identity(hydrology_frame, key, "hydrology_frame")
        if actual_text != expected_text:
            raise RestoreIdentityError(f"hydrology_frame.{key}: incompatible binding")

    _identity(hydrology_frame, "frame_id", "hydrology_frame")

    if checkpoint != before_checkpoint or runtime_target != before_target or hydrology_frame != before_frame or next_interval_t1 != before_t1:
        raise AssertionError("qualification guard mutated input")

    return {
        "status": "RESTORE_IDENTITY_COMPATIBLE",
        "accepted_t0": accepted_t0,
        "next_interval_t1": interval_t1,
        "soil_layer_count": cp_layers,
        "p_fast_site_count": cp_fast,
        "p_slow_site_count": cp_slow,
        "hydrology_frame_id": hydrology_frame["frame_id"],
    }


def guarded_restore_identity(
    *,
    checkpoint: Mapping[str, object],
    runtime_target: Mapping[str, object],
    hydrology_frame: Mapping[str, object],
    next_interval_t1: Mapping[str, object],
    construct_accepted_state: Callable[[], T],
) -> T:
    """Run all identity checks before constructing any restored accepted state."""

    validate_restore_identity(
        checkpoint=checkpoint,
        runtime_target=runtime_target,
        hydrology_frame=hydrology_frame,
        next_interval_t1=next_interval_t1,
    )
    return construct_accepted_state()
