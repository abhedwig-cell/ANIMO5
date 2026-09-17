#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    fixture = json.loads(args.fixture.read_text())
    step = fixture["diagnostic_normalized_step"]
    nl = int(step["layer_count"])
    nudr = int(step["drainage_count"])

    lines = [
        "module mod_kt07_real_lwkm_fixture",
        "  use, intrinsic :: iso_fortran_env, only : real64",
        "  use mod_animo_hydrology_adapter, only: hydrology_step_t",
        "  implicit none",
        "  private",
        "  public :: make_kt07_lwkm_step",
        "contains",
        "  subroutine make_kt07_lwkm_step(step)",
        "    type(hydrology_step_t), intent(out) :: step",
        f"    step%schema_id = '{step['schema_id']}'",
        f"    step%unit_contract_id = '{step['unit_contract_id']}'",
        f"    step%layer_count = {nl}",
        f"    step%drainage_count = {nudr}",
    ]
    for name in SCALARS:
        lines.append(f"    step%{name} = {real_literal(step[name])}")
    lines.extend([
        "    step%has_interception_storage_end = .true.",
        "    step%has_soil_temperature = .true.",
        f"    allocate(step%sc({nl}))",
        f"    allocate(step%mofrt({nl}))",
        f"    allocate(step%flev({nl}))",
        f"    allocate(step%flab({nl + 1}))",
        f"    allocate(step%fldr({nudr}, {nl}))",
        f"    allocate(step%soil_temperature({nl}))",
    ])
    for name in ("sc", "mofrt", "flev", "flab", "soil_temperature"):
        for i, value in enumerate(step[name], start=1):
            lines.append(f"    step%{name}({i}) = {real_literal(value)}")
    for i, row in enumerate(step["fldr"], start=1):
        for j, value in enumerate(row, start=1):
            lines.append(f"    step%fldr({i}, {j}) = {real_literal(value)}")
    lines.extend([
        "  end subroutine make_kt07_lwkm_step",
        "end module mod_kt07_real_lwkm_fixture",
        "",
    ])
    args.output.write_text("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
