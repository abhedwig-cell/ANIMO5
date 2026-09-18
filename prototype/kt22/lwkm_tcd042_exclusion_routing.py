from __future__ import annotations

from dataclasses import dataclass
import math

from prototype.kt21.lwkm_bounded_envelope import (
    CLASS_OUTSIDE,
    TCD042_FLUX_THRESHOLD,
    TCD042_P_MAX,
    PacketEnvelopeResult,
)

ROUTE_ORDINARY_POSITIVE_FLOW = "ORDINARY_POSITIVE_FLOW_FLUX_GE_THRESHOLD"
ROUTE_SUBTHRESHOLD_P_OUTSIDE = "SUBTHRESHOLD_POSITIVE_FLOW_P_OUTSIDE_NQ03_ENVELOPE"
ROUTE_NOT_KT21_OUTSIDE = "NOT_KT21_OUTSIDE_REMAINDER"


@dataclass(frozen=True)
class ExclusionRoute:
    label: str
    flux: float | None
    p: float | None


def route_kt21_outside(result: PacketEnvelopeResult) -> ExclusionRoute:
    """Route an already-characterized KT21 packet without widening any science.

    KT22 is diagnostic only. It does not execute UBoundconc and does not make
    an outside packet scientifically admissible.
    """
    if result.classification != CLASS_OUTSIDE:
        return ExclusionRoute(ROUTE_NOT_KT21_OUTSIDE, result.flux, result.p)

    if result.flux is None or result.p is None:
        raise ValueError("KT21 outside result missing deterministic flux/P")
    if not math.isfinite(result.flux) or not math.isfinite(result.p):
        raise ValueError("KT21 outside result has non-finite flux/P")
    if result.flux <= 0.0:
        raise ValueError("KT21 outside result has non-positive flux")

    if result.flux >= TCD042_FLUX_THRESHOLD:
        return ExclusionRoute(ROUTE_ORDINARY_POSITIVE_FLOW, result.flux, result.p)

    if result.p > TCD042_P_MAX:
        return ExclusionRoute(ROUTE_SUBTHRESHOLD_P_OUTSIDE, result.flux, result.p)

    raise ValueError("KT21 outside result does not violate the admitted parent envelope")
