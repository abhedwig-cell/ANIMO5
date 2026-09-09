"""Qualification-only fail-closed guard for ANIMO-STATEQ01 restricted core.

This module is not production ANIMO5 code. It encodes the source-qualified
application-envelope predicates from RESTRICTED_CORE_ENVELOPE_QUALIFICATION_SPEC.md
so that fail-before-mutate sentinel tests can be executed independently of the
legacy physics.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from typing import Mapping


PROFILE_ID = "CORE_CNP_SUBSURFACE_ONLY"
_C_N_KEYS = frozenset({"nh4", "no3", "dom", "don"})
_P_KEYS = frozenset({"po4", "dop"})


class RestrictedCoreGuardError(ValueError):
    """Raised when the candidate state lies outside the restricted-core envelope."""


@dataclass(frozen=True)
class GuardResult:
    profile_id: str
    hydrology_mode: str
    phosphorus_active: bool
    accepted: bool = True


def _as_finite_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise RestrictedCoreGuardError(f"{label}: expected real numeric coordinate")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise RestrictedCoreGuardError(f"{label}: non-finite coordinate")
    return numeric


def _require_zero(value: object, label: str) -> None:
    numeric = _as_finite_number(value, label)
    if numeric != 0.0:
        raise RestrictedCoreGuardError(
            f"{label}: restricted-core envelope requires exact zero, got {numeric!r}"
        )


def _require_nonnegative(value: object, label: str) -> float:
    numeric = _as_finite_number(value, label)
    if numeric < 0.0:
        raise RestrictedCoreGuardError(f"{label}: negative physical storage")
    return numeric


def _require_keys(mapping: Mapping[str, object], required: frozenset[str], label: str) -> None:
    missing = required.difference(mapping)
    if missing:
        raise RestrictedCoreGuardError(
            f"{label}: missing required coordinate(s): {','.join(sorted(missing))}"
        )


def _validate_surface_frame(
    frame: Mapping[str, object], *, hydrology_mode: str, label: str
) -> None:
    if hydrology_mode == "aggregated":
        _require_keys(frame, frozenset({"ponding"}), label)
        ponding = _require_nonnegative(frame["ponding"], f"{label}.ponding")
        if ponding != 0.0:
            raise RestrictedCoreGuardError(
                f"{label}.ponding: restricted-core envelope requires exact zero"
            )
        return

    if hydrology_mode == "detailed":
        _require_keys(frame, frozenset({"ponding", "snow"}), label)
        ponding = _require_nonnegative(frame["ponding"], f"{label}.ponding")
        snow = _require_nonnegative(frame["snow"], f"{label}.snow")
        if ponding + snow != 0.0:
            raise RestrictedCoreGuardError(
                f"{label}.ponding+snow: restricted-core envelope requires exact zero"
            )
        return

    raise RestrictedCoreGuardError(
        f"hydrology_mode: unsupported value {hydrology_mode!r}; expected 'aggregated' or 'detailed'"
    )


def _validate_layer0_restart(
    layer0_restart: Mapping[str, object], *, phosphorus_active: bool
) -> None:
    required = _C_N_KEYS | (_P_KEYS if phosphorus_active else frozenset())
    _require_keys(layer0_restart, required, "layer0_restart")

    unknown = set(layer0_restart).difference(required)
    if unknown:
        raise RestrictedCoreGuardError(
            "layer0_restart: unrecognized coordinate(s) for declared profile: "
            + ",".join(sorted(unknown))
        )

    for key in sorted(required):
        _require_zero(layer0_restart[key], f"layer0_restart.{key}")


def validate_restricted_core_envelope(
    *,
    hydrology_mode: str,
    accepted_surface: Mapping[str, object],
    candidate_surface: Mapping[str, object],
    layer0_restart: Mapping[str, object],
    phosphorus_active: bool,
) -> GuardResult:
    """Validate the restricted-core application envelope without mutating inputs.

    The guard is intentionally stricter than the revision-53 ``Flpn`` threshold:
    physically positive surface storage is rejected even when it would remain
    below the legacy activation threshold. All in-scope layer-0 restart solute
    coordinates must be exactly zero. No clipping, projection, remapping or
    epsilon-based acceptance is performed.
    """

    if not isinstance(accepted_surface, Mapping):
        raise RestrictedCoreGuardError("accepted_surface: expected mapping")
    if not isinstance(candidate_surface, Mapping):
        raise RestrictedCoreGuardError("candidate_surface: expected mapping")
    if not isinstance(layer0_restart, Mapping):
        raise RestrictedCoreGuardError("layer0_restart: expected mapping")
    if not isinstance(phosphorus_active, bool):
        raise RestrictedCoreGuardError("phosphorus_active: expected bool")

    _validate_surface_frame(
        accepted_surface, hydrology_mode=hydrology_mode, label="accepted_surface"
    )
    _validate_surface_frame(
        candidate_surface, hydrology_mode=hydrology_mode, label="candidate_surface"
    )
    _validate_layer0_restart(layer0_restart, phosphorus_active=phosphorus_active)

    return GuardResult(
        profile_id=PROFILE_ID,
        hydrology_mode=hydrology_mode,
        phosphorus_active=phosphorus_active,
    )
