"""Qualification-only RC-R7 physical-layout restore guard.

This module contains no ANIMO physics and is not a production checkpoint reader.
It tests one narrow STATEQ01 contract: logical state topology must match exactly
before any persistent state payload is consumed or constructed.

In particular, fast and slow phosphorus site counts are logical dimensions of
P-002 and P-003. A larger fixed legacy array capacity does not permit checkpoint
padding, truncation, reshaping or implicit zero filling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class LayoutMismatchError(ValueError):
    """Raised before state payload consumption when physical layouts differ."""


def _positive_count(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise LayoutMismatchError(f"{label}: integer required")
    if value <= 0:
        raise LayoutMismatchError(f"{label}: must be positive")
    return value


def _site_count(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise LayoutMismatchError(f"{label}: integer required")
    if value < 0:
        raise LayoutMismatchError(f"{label}: must be non-negative")
    return value


def _identity(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LayoutMismatchError(f"{label}: non-empty identity required")
    return value


@dataclass(frozen=True)
class PhysicalLayout:
    state_schema_id: str
    geometry_id: str
    soil_layer_count: int
    fast_p_site_count: int
    slow_p_site_count: int
    organic_fraction_count: int
    phosphorus_active: bool
    precision_policy_id: str

    @classmethod
    def build(
        cls,
        *,
        state_schema_id: object,
        geometry_id: object,
        soil_layer_count: object,
        fast_p_site_count: object,
        slow_p_site_count: object,
        organic_fraction_count: object,
        phosphorus_active: object,
        precision_policy_id: object,
    ) -> "PhysicalLayout":
        if not isinstance(phosphorus_active, bool):
            raise LayoutMismatchError("phosphorus_active: bool required")

        fast_sites = _site_count(fast_p_site_count, "fast_p_site_count")
        slow_sites = _site_count(slow_p_site_count, "slow_p_site_count")
        if not phosphorus_active and (fast_sites != 0 or slow_sites != 0):
            raise LayoutMismatchError(
                "P-inactive layout must have zero fast and slow P site counts"
            )
        if phosphorus_active and (fast_sites == 0 or slow_sites == 0):
            raise LayoutMismatchError(
                "P-active RC-R7 layout requires explicit nonzero fast and slow site counts"
            )

        return cls(
            state_schema_id=_identity(state_schema_id, "state_schema_id"),
            geometry_id=_identity(geometry_id, "geometry_id"),
            soil_layer_count=_positive_count(soil_layer_count, "soil_layer_count"),
            fast_p_site_count=fast_sites,
            slow_p_site_count=slow_sites,
            organic_fraction_count=_positive_count(
                organic_fraction_count, "organic_fraction_count"
            ),
            phosphorus_active=phosphorus_active,
            precision_policy_id=_identity(
                precision_policy_id, "precision_policy_id"
            ),
        )


@dataclass(frozen=True)
class RestoreResult(Generic[T]):
    layout: PhysicalLayout
    restored_state: T


def mismatch_fields(
    checkpoint_layout: PhysicalLayout, target_layout: PhysicalLayout
) -> tuple[str, ...]:
    """Return exact physical-layout fields that differ."""

    fields = (
        "state_schema_id",
        "geometry_id",
        "soil_layer_count",
        "fast_p_site_count",
        "slow_p_site_count",
        "organic_fraction_count",
        "phosphorus_active",
        "precision_policy_id",
    )
    return tuple(
        field
        for field in fields
        if getattr(checkpoint_layout, field) != getattr(target_layout, field)
    )


def require_exact_layout(
    checkpoint_layout: PhysicalLayout, target_layout: PhysicalLayout
) -> None:
    mismatches = mismatch_fields(checkpoint_layout, target_layout)
    if mismatches:
        raise LayoutMismatchError(
            "physical layout mismatch before state consumption: "
            + ",".join(mismatches)
        )


def guarded_restore(
    *,
    checkpoint_layout: PhysicalLayout,
    target_layout: PhysicalLayout,
    consume_and_construct_state: Callable[[], T],
) -> RestoreResult[T]:
    """Validate exact topology before reading or constructing state payload.

    The callback represents the first operation allowed to consume persistent
    state bytes. On any layout mismatch it must not be called.
    """

    require_exact_layout(checkpoint_layout, target_layout)
    restored = consume_and_construct_state()
    return RestoreResult(layout=target_layout, restored_state=restored)
