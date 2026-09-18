#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import zlib

SCALARS = [
    "producer_endpoint_day", "producer_step_days", "prr", "prsn", "prirr",
    "evicpr", "evicirr", "evsn", "evso", "evpn", "evsoma", "evtrma",
    "runon", "runoff", "groundwater_level", "ponding_end", "snow_storage_end",
    "water_balance_aeration", "interception_storage_end",
]


def real_literal(value: float) -> str:
    if value == 0.0:
        return "0.0_real64"
    return f"{float(value):.17g}_real64"


def load_bundle(path: Path) -> dict:
    encoded = path.read_text().strip()
    return json.loads(zlib.decompress(base64.b64decode(encoded)))


def emit_step(lines: list[str], step: dict) -> None:
    nl = int(step["layer_count"])
    nudr = int(step["drainage_count"])
    lines.extend([
        f"      step%schema_id = '{step['schema_id']}'",
        f"      step%unit_contract_id = '{step['unit_contract_id']}'",
        f"      step%layer_count = {nl}",
        f"      step%drainage_count = {nudr}",
    ])
    for name in SCALARS:
        lines.append(f"      step%{name} = {real_literal(step[name])}")
    lines.extend([
        "      step%has_interception_storage_end = .true.",
        "      step%has_soil_temperature = .true.",
        f"      allocate(step%sc({nl}))",
        f"      allocate(step%mofrt({nl}))",
        f"      allocate(step%flev({nl}))",
        f"      allocate(step%flab({nl + 1}))",
        f"      allocate(step%fldr({nudr}, {nl}))",
        f"      allocate(step%soil_temperature({nl}))",
    ])
    for name in ("sc", "mofrt", "flev", "flab", "soil_temperature"):
        for i, value in enumerate(step[name], start=1):
            lines.append(f"      step%{name}({i}) = {real_literal(value)}")
    for i, row in enumerate(step["fldr"], start=1):
        for j, value in enumerate(row, start=1):
            lines.append(f"      step%fldr({i}, {j}) = {real_literal(value)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    bundle = load_bundle(args.fixture)
    anchors = bundle["anchors"]
    count = len(anchors)
    indices = ", ".join(str(a["index_zero_based"]) for a in anchors)
    endpoints = ", ".join(real_literal(a["diagnostic_normalized_step"]["producer_endpoint_day"]) for a in anchors)
    durations = ", ".join(real_literal(a["diagnostic_normalized_step"]["producer_step_days"]) for a in anchors)

    lines = [
        "module mod_kt09_real_lwkm_anchors",
        "  use, intrinsic :: iso_fortran_env, only : real64",
        "  use mod_animo_hydrology_adapter, only: hydrology_step_t",
        "  implicit none",
        "  private",
        f"  integer, parameter, public :: KT09_ANCHOR_COUNT = {count}",
        f"  integer, parameter, public :: KT09_SOURCE_INDEX({count}) = [{indices}]",
        f"  real(real64), parameter, public :: KT09_ENDPOINT({count}) = [{endpoints}]",
        f"  real(real64), parameter, public :: KT09_DURATION({count}) = [{durations}]",
        "  public :: make_kt09_anchor_step",
        "contains",
        "  subroutine make_kt09_anchor_step(which, step)",
        "    integer, intent(in) :: which",
        "    type(hydrology_step_t), intent(out) :: step",
        "    select case (which)",
    ]
    for which, anchor in enumerate(anchors, start=1):
        lines.append(f"    case ({which})")
        emit_step(lines, anchor["diagnostic_normalized_step"])
    lines.extend([
        "    case default",
        "      error stop 91",
        "    end select",
        "  end subroutine make_kt09_anchor_step",
        "end module mod_kt09_real_lwkm_anchors",
        "",
    ])
    args.output.write_text("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
