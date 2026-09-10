#!/usr/bin/env python3
"""Bounded B1 synthetic activation probe for TCD-041.

This does not emulate the full GHG subsystem and is not historical B2 evidence.
It exercises only the source-qualified lower-air boundary seam and direct
bottom-layer algebra already isolated by ANIMO-BUILDQ04.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Result:
    active: bool
    q_bottom: float | None
    flaiio_bottom: float | None
    flaiou_bottom: float | None
    delta_tofl_boundary: float | None
    delta_y3_boundary: float | None
    lower_neighbour_coupling: float | None


def seam_result(
    ioptghg: int,
    q_bottom: float,
    *,
    upper_face_outflow_component: float = 0.0,
    avca: float = 0.03,
    rebuav: float = 0.8,
    he: float = 0.1,
    st: float = 1.0,
) -> Result:
    """Evaluate only the direct lower-boundary contribution.

    Source guard: active when IoptGHG >= 1.
    Sign convention: q_bottom is Flair(Nl+1), downward positive, unit m/d.
    Bottom lower-neighbour transport coupling is zero by the qualified source
    contract in GHGtranssub.
    """
    if ioptghg < 1:
        return Result(False, None, None, None, None, None, None)

    flaiio = -min(0.0, q_bottom)
    flaiou = max(0.0, q_bottom) + upper_face_outflow_component
    delta_tofl = -avca * max(0.0, q_bottom) * st
    delta_y3 = rebuav * max(0.0, q_bottom) / he
    lower_neighbour_coupling = 0.0
    return Result(
        True,
        q_bottom,
        flaiio,
        flaiou,
        delta_tofl,
        delta_y3,
        lower_neighbour_coupling,
    )


def self_test() -> dict[str, object]:
    # Inactive control: the GHG seam is not evaluated.
    inactive = seam_result(0, 0.001)
    assert inactive == Result(False, None, None, None, None, None, None)

    # Active controls cover both source-reachable GHG option values.
    closed_1 = seam_result(1, 0.0)
    closed_2 = seam_result(2, 0.0)
    for closed in (closed_1, closed_2):
        assert closed.active
        assert closed.flaiio_bottom == 0.0
        assert closed.flaiou_bottom == 0.0
        assert closed.delta_tofl_boundary == 0.0
        assert closed.delta_y3_boundary == 0.0
        assert closed.lower_neighbour_coupling == 0.0

    # Positive contaminated lower flux reproduces BUILDQ04 direct identities.
    positive = seam_result(1, 0.001, avca=0.03, rebuav=0.8, he=0.1, st=1.0)
    assert positive.flaiio_bottom == 0.0
    assert positive.flaiou_bottom == 0.001
    assert positive.delta_tofl_boundary == -0.00003
    assert positive.delta_y3_boundary == 0.008
    assert positive.lower_neighbour_coupling == 0.0

    # Small positive sensitivity remains proportional and sign-consistent.
    positive_small = seam_result(2, 0.000001, avca=0.03, rebuav=0.8, he=0.1, st=1.0)
    assert positive_small.flaiou_bottom == 0.000001
    assert positive_small.delta_tofl_boundary == -0.03 * 0.000001
    assert positive_small.delta_y3_boundary == 0.8 * 0.000001 / 0.1

    # Negative residual is classified as lower inflow but has no modeled lower
    # neighbour concentration coupling. This is a source-contract hazard, not
    # a qualified nonzero deep-gas boundary model.
    negative = seam_result(1, -0.001)
    assert negative.flaiio_bottom == 0.001
    assert negative.flaiou_bottom == 0.0
    assert negative.delta_tofl_boundary == 0.0
    assert negative.delta_y3_boundary == 0.0
    assert negative.lower_neighbour_coupling == 0.0

    return {
        "classification": "B1_SYNTHETIC_SOURCE_SEAM_ACTIVATION_NOT_B2",
        "source_guard": "IoptGHG >= 1",
        "inactive_control": asdict(inactive),
        "closed_boundary_ioptghg_1": asdict(closed_1),
        "closed_boundary_ioptghg_2": asdict(closed_2),
        "positive_boundary_sensitivity": asdict(positive),
        "small_positive_boundary_sensitivity": asdict(positive_small),
        "negative_boundary_sensitivity": asdict(negative),
        "result": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("only --self-test is supported")
    print(json.dumps(self_test(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
