"""Qualification-only RC-R12 upper-boundary reservoir wiring harness.

This is not ANIMO physics and not a production checkpoint implementation. It
encodes only the source-qualified accepted-boundary lifecycle for the exact
zero-flux, zero-load branch of revision-53 UBoundconc where, for Flpn=0,
Rs*top == Av*top == Con*top exactly.

Fractions are used so the synthetic sentinel itself introduces no floating
comparison tolerance.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping


CORE_SPECIES = ("nh4", "no3", "dom", "don")
P_SPECIES = ("po4", "dop")


class UpperBoundaryContractError(ValueError):
    """Raised when the qualification-only reservoir contract is violated."""


def _as_fraction(value: object, label: str) -> Fraction:
    if isinstance(value, bool):
        raise UpperBoundaryContractError(f"{label}: bool is not a concentration")
    if isinstance(value, Fraction):
        result = value
    elif isinstance(value, int):
        result = Fraction(value, 1)
    else:
        raise UpperBoundaryContractError(
            f"{label}: exact synthetic sentinel requires int or Fraction"
        )
    if result < 0:
        raise UpperBoundaryContractError(f"{label}: negative concentration")
    return result


def _required_species(phosphorus_active: bool) -> tuple[str, ...]:
    return CORE_SPECIES + (P_SPECIES if phosphorus_active else ())


@dataclass(frozen=True)
class ReservoirState:
    concentrations: tuple[tuple[str, Fraction], ...]

    @classmethod
    def build(
        cls, values: Mapping[str, object], *, phosphorus_active: bool
    ) -> "ReservoirState":
        required = _required_species(phosphorus_active)
        missing = set(required).difference(values)
        extra = set(values).difference(required)
        if missing:
            raise UpperBoundaryContractError(
                "reservoir: missing species: " + ",".join(sorted(missing))
            )
        if extra:
            raise UpperBoundaryContractError(
                "reservoir: unexpected species: " + ",".join(sorted(extra))
            )
        return cls(
            concentrations=tuple(
                (species, _as_fraction(values[species], f"reservoir.{species}"))
                for species in required
            )
        )

    def as_dict(self) -> dict[str, Fraction]:
        return dict(self.concentrations)


@dataclass(frozen=True)
class BoundaryIntervalResult:
    accepted_owner: ReservoirState
    interval_average: ReservoirState
    first_compartment_boundary: ReservoirState
    first_active_compartment: int


def exact_zero_flux_interval(
    start_alias: ReservoirState, *, flpn: int
) -> BoundaryIntervalResult:
    """Apply only the exact zero-flux, zero-load source branch.

    UBoundconc.for:119-124 makes A1=B1=1 and A2=B2=0 for Flux<1e-8.
    The sentinel narrows this further to the unambiguous exact Flux=0 and
    Load=0 case. It therefore tests owner/alias/average wiring, not the
    exponential nonzero-flux numerical update.
    """

    if flpn != 0:
        raise UpperBoundaryContractError(
            "RC-R12 sentinel is restricted to Flpn=0"
        )
    accepted_owner = start_alias
    interval_average = start_alias
    return BoundaryIntervalResult(
        accepted_owner=accepted_owner,
        interval_average=interval_average,
        first_compartment_boundary=interval_average,
        first_active_compartment=1,
    )


def physical_amounts(
    state: ReservoirState, *, hetop: Fraction
) -> dict[str, Fraction]:
    hetop_exact = _as_fraction(hetop, "Hetop")
    if hetop_exact <= 0:
        raise UpperBoundaryContractError("Hetop: must be positive")
    return {
        species: concentration * hetop_exact
        for species, concentration in state.concentrations
    }


def checkpoint_payload(
    *,
    accepted_owner: ReservoirState,
    geometry_identity: str,
    hetop: Fraction,
    phosphorus_active: bool,
) -> dict[str, object]:
    if not geometry_identity:
        raise UpperBoundaryContractError("geometry_identity: required")
    hetop_exact = _as_fraction(hetop, "Hetop")
    if hetop_exact <= 0:
        raise UpperBoundaryContractError("Hetop: must be positive")
    state = accepted_owner.as_dict()
    return {
        "geometry_identity": geometry_identity,
        "hetop": {
            "numerator": str(hetop_exact.numerator),
            "denominator": str(hetop_exact.denominator),
        },
        "phosphorus_active": phosphorus_active,
        "accepted_upper_boundary": {
            species: {
                "numerator": str(value.numerator),
                "denominator": str(value.denominator),
            }
            for species, value in state.items()
        },
    }


def _fraction_from_payload(value: object, label: str) -> Fraction:
    if not isinstance(value, Mapping):
        raise UpperBoundaryContractError(f"{label}: expected rational mapping")
    if set(value) != {"numerator", "denominator"}:
        raise UpperBoundaryContractError(f"{label}: invalid rational fields")
    try:
        numerator = int(str(value["numerator"]))
        denominator = int(str(value["denominator"]))
    except ValueError as exc:
        raise UpperBoundaryContractError(f"{label}: invalid integer text") from exc
    if denominator <= 0:
        raise UpperBoundaryContractError(f"{label}: denominator must be positive")
    return Fraction(numerator, denominator)


def restore_checkpoint(
    payload: Mapping[str, object],
    *,
    expected_geometry_identity: str,
    expected_hetop: Fraction,
    expected_phosphorus_active: bool,
) -> ReservoirState:
    """Restore accepted owner as the next interval's Con*top alias.

    The payload deliberately contains no Av*top field and no duplicate Con*top
    field. Geometry/P-activation mismatches fail before a start alias is built.
    """

    required = {
        "geometry_identity",
        "hetop",
        "phosphorus_active",
        "accepted_upper_boundary",
    }
    missing = required.difference(payload)
    if missing:
        raise UpperBoundaryContractError(
            "checkpoint: missing field(s): " + ",".join(sorted(missing))
        )
    if payload["geometry_identity"] != expected_geometry_identity:
        raise UpperBoundaryContractError("checkpoint geometry identity mismatch")
    if payload["phosphorus_active"] is not expected_phosphorus_active:
        raise UpperBoundaryContractError("checkpoint P activation mismatch")

    payload_hetop = _fraction_from_payload(payload["hetop"], "Hetop")
    expected_hetop_exact = _as_fraction(expected_hetop, "expected_Hetop")
    if payload_hetop != expected_hetop_exact:
        raise UpperBoundaryContractError("checkpoint Hetop mismatch")

    values = payload["accepted_upper_boundary"]
    if not isinstance(values, Mapping):
        raise UpperBoundaryContractError(
            "accepted_upper_boundary: expected mapping"
        )
    decoded = {
        species: _fraction_from_payload(raw, f"accepted_upper_boundary.{species}")
        for species, raw in values.items()
    }
    return ReservoirState.build(
        decoded, phosphorus_active=expected_phosphorus_active
    )
