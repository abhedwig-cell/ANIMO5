"""Qualification-only RC-R4 site-resolved phosphorus checkpoint harness.

No ANIMO physics is implemented here. The harness tests the candidate state
ownership contract for an explicitly initialized P-active profile: aqueous P,
fast-site P, slow-site P and precipitated P are persistent owners, while summed
totals are derived views and are not independent checkpoint owners.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


INPO1_ID = "INPO1_EXPLICIT_P_STATE"


class PStateContractError(ValueError):
    """Raised when the RC-R4 candidate checkpoint contract is violated."""


def _count(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise PStateContractError(f"{label}: positive integer required")
    return value


def _fraction(value: object, label: str) -> Fraction:
    if isinstance(value, bool):
        raise PStateContractError(f"{label}: bool is not a P state value")
    if isinstance(value, Fraction):
        result = value
    elif isinstance(value, int):
        result = Fraction(value, 1)
    else:
        raise PStateContractError(f"{label}: exact synthetic value must be int or Fraction")
    if result < 0:
        raise PStateContractError(f"{label}: negative P state is outside this sentinel")
    return result


def _vector(values: Sequence[object], count: int, label: str) -> tuple[Fraction, ...]:
    if len(values) != count:
        raise PStateContractError(f"{label}: expected {count} entries, got {len(values)}")
    return tuple(_fraction(value, f"{label}[{idx}]") for idx, value in enumerate(values))


def _matrix(
    values: Sequence[Sequence[object]], rows: int, cols: int, label: str
) -> tuple[tuple[Fraction, ...], ...]:
    if len(values) != rows:
        raise PStateContractError(f"{label}: expected {rows} layers, got {len(values)}")
    return tuple(
        _vector(row, cols, f"{label}[layer={layer}]")
        for layer, row in enumerate(values)
    )


@dataclass(frozen=True)
class PStateLayout:
    soil_layer_count: int
    fast_site_count: int
    slow_site_count: int
    initialization_mode: str = INPO1_ID

    @classmethod
    def build(
        cls,
        *,
        soil_layer_count: object,
        fast_site_count: object,
        slow_site_count: object,
        initialization_mode: object = INPO1_ID,
    ) -> "PStateLayout":
        if initialization_mode != INPO1_ID:
            raise PStateContractError("RC-R4 sentinel is restricted to explicit INPO1 fixture")
        return cls(
            soil_layer_count=_count(soil_layer_count, "soil_layer_count"),
            fast_site_count=_count(fast_site_count, "fast_site_count"),
            slow_site_count=_count(slow_site_count, "slow_site_count"),
        )


@dataclass(frozen=True)
class PState:
    layout: PStateLayout
    aqueous_po4: tuple[Fraction, ...]
    fast_sorbed: tuple[tuple[Fraction, ...], ...]
    slow_sorbed: tuple[tuple[Fraction, ...], ...]
    precipitated: tuple[Fraction, ...]

    @classmethod
    def build(
        cls,
        *,
        layout: PStateLayout,
        aqueous_po4: Sequence[object],
        fast_sorbed: Sequence[Sequence[object]],
        slow_sorbed: Sequence[Sequence[object]],
        precipitated: Sequence[object],
    ) -> "PState":
        if not isinstance(layout, PStateLayout):
            raise PStateContractError("layout: PStateLayout required")
        return cls(
            layout=layout,
            aqueous_po4=_vector(
                aqueous_po4, layout.soil_layer_count, "aqueous_po4"
            ),
            fast_sorbed=_matrix(
                fast_sorbed,
                layout.soil_layer_count,
                layout.fast_site_count,
                "fast_sorbed",
            ),
            slow_sorbed=_matrix(
                slow_sorbed,
                layout.soil_layer_count,
                layout.slow_site_count,
                "slow_sorbed",
            ),
            precipitated=_vector(
                precipitated, layout.soil_layer_count, "precipitated"
            ),
        )


def _encode_fraction(value: Fraction) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
    }


def _decode_fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, Mapping) or set(value) != {"numerator", "denominator"}:
        raise PStateContractError(f"{label}: rational mapping required")
    try:
        numerator = int(str(value["numerator"]))
        denominator = int(str(value["denominator"]))
    except ValueError as exc:
        raise PStateContractError(f"{label}: invalid integer text") from exc
    if denominator <= 0:
        raise PStateContractError(f"{label}: denominator must be positive")
    result = Fraction(numerator, denominator)
    if result < 0:
        raise PStateContractError(f"{label}: negative P state")
    return result


def checkpoint_payload(state: PState) -> dict[str, object]:
    if not isinstance(state, PState):
        raise PStateContractError("state: PState required")
    return {
        "layout": {
            "soil_layer_count": state.layout.soil_layer_count,
            "fast_site_count": state.layout.fast_site_count,
            "slow_site_count": state.layout.slow_site_count,
            "initialization_mode": state.layout.initialization_mode,
        },
        "aqueous_po4": [_encode_fraction(value) for value in state.aqueous_po4],
        "fast_sorbed": [
            [_encode_fraction(value) for value in layer]
            for layer in state.fast_sorbed
        ],
        "slow_sorbed": [
            [_encode_fraction(value) for value in layer]
            for layer in state.slow_sorbed
        ],
        "precipitated": [_encode_fraction(value) for value in state.precipitated],
    }


def restore_checkpoint(
    payload: Mapping[str, object], *, expected_layout: PStateLayout
) -> PState:
    if not isinstance(payload, Mapping):
        raise PStateContractError("checkpoint payload: mapping required")
    raw_layout = payload.get("layout")
    if not isinstance(raw_layout, Mapping):
        raise PStateContractError("checkpoint layout header missing")
    checkpoint_layout = PStateLayout.build(
        soil_layer_count=raw_layout.get("soil_layer_count"),
        fast_site_count=raw_layout.get("fast_site_count"),
        slow_site_count=raw_layout.get("slow_site_count"),
        initialization_mode=raw_layout.get("initialization_mode"),
    )
    if checkpoint_layout != expected_layout:
        raise PStateContractError("checkpoint P layout mismatch before state decode")

    required = {"layout", "aqueous_po4", "fast_sorbed", "slow_sorbed", "precipitated"}
    missing = required.difference(payload)
    if missing:
        raise PStateContractError("checkpoint missing field(s): " + ",".join(sorted(missing)))

    aqueous_raw = payload["aqueous_po4"]
    fast_raw = payload["fast_sorbed"]
    slow_raw = payload["slow_sorbed"]
    precip_raw = payload["precipitated"]
    if not all(isinstance(value, Sequence) for value in (aqueous_raw, fast_raw, slow_raw, precip_raw)):
        raise PStateContractError("checkpoint state arrays must be sequences")

    aqueous = [_decode_fraction(value, "aqueous_po4") for value in aqueous_raw]
    fast = [
        [_decode_fraction(value, "fast_sorbed") for value in layer]
        for layer in fast_raw
    ]
    slow = [
        [_decode_fraction(value, "slow_sorbed") for value in layer]
        for layer in slow_raw
    ]
    precipitated = [_decode_fraction(value, "precipitated") for value in precip_raw]
    return PState.build(
        layout=expected_layout,
        aqueous_po4=aqueous,
        fast_sorbed=fast,
        slow_sorbed=slow,
        precipitated=precipitated,
    )


def derived_total_by_layer(state: PState) -> tuple[Fraction, ...]:
    """Derived view only; deliberately absent from checkpoint payload."""

    return tuple(
        state.aqueous_po4[layer]
        + sum(state.fast_sorbed[layer], Fraction(0, 1))
        + sum(state.slow_sorbed[layer], Fraction(0, 1))
        + state.precipitated[layer]
        for layer in range(state.layout.soil_layer_count)
    )
