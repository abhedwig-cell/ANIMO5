#!/usr/bin/env python3
"""Bounded KT03-F01 diagnostic probe for SWAP3 interception-state semantics.

This tool evaluates the whole-profile water-balance identity encoded by
revision-53 Hydro_detailed against a supplied legacy SWATRE.UNF file. It
compares the residual with no interception-storage state to the residual with
an explicit Sict-Sic term when the Hlpimp=11 record layout actually supplies
that state.

The probe is B1 diagnostic evidence. It does not reconstruct historical
compiler behaviour and does not mutate or execute ANIMO scientific source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path

from prototype.kt03.hydrology_step import legacy_dble_trunc_diagnostic
from tools.convert_legacy_unformatted import parse_powerstation_records


def _f32(record: bytes, expected: int, label: str) -> tuple[float, ...]:
    if len(record) != expected * 4:
        raise ValueError(f"{label}: expected {expected * 4} bytes, got {len(record)}")
    values = struct.unpack("<" + "f" * expected, record)
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f"{label}: non-finite value")
    return values


def _i32(record: bytes, expected: int, label: str) -> tuple[int, ...]:
    if len(record) != expected * 4:
        raise ValueError(f"{label}: expected {expected * 4} bytes, got {len(record)}")
    return struct.unpack("<" + "i" * expected, record)


def _norm(values: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(legacy_dble_trunc_diagnostic(value) for value in values)


def _stats(values: list[float]) -> dict[str, float | int]:
    if not values:
        raise ValueError("cannot summarize empty residual series")
    absolute = sorted(abs(value) for value in values)
    p95_index = int(0.95 * (len(absolute) - 1))
    return {
        "count": len(values),
        "max_abs_m": max(absolute),
        "mean_abs_m": sum(absolute) / len(absolute),
        "p95_abs_m": absolute[p95_index],
        "signed_sum_m": sum(values),
    }


def analyze_records(records: list[bytes]) -> dict:
    if len(records) < 18:
        raise ValueError("insufficient logical records")
    headers = [record.decode("ascii", errors="strict").rstrip() for record in records[:5]]
    if not all(header.startswith("*") for header in headers):
        raise ValueError("not the bounded textual SWAP3/SWAP hydrology layout")

    (hlpimp,) = _i32(records[5], 1, "Hlpimp")
    if hlpimp not in (1, 11):
        raise ValueError(f"unsupported Hlpimp={hlpimp}; KT03-F01 is bounded to 1/11")
    layer_count, horizon_count, drainage_count = _i32(records[7], 3, "dimensions")
    if layer_count <= 0 or horizon_count <= 0 or drainage_count < 0:
        raise ValueError("invalid dimensions")

    layer_thickness = _norm(_f32(records[12], layer_count, "layer thickness"))
    moisture_previous = list(_norm(_f32(records[13], layer_count, "initial moisture")))
    surface = _norm(
        _f32(records[14], 3 if hlpimp == 11 else 2, "initial surface state")
    )
    interception_previous = surface[1] if hlpimp == 11 else None
    ponding_previous = surface[-1]
    (snow_previous,) = _norm(_f32(records[15], 1, "initial snow storage"))

    records_per_step = 8 + drainage_count
    dynamic = records[17:]
    if len(dynamic) % records_per_step:
        raise ValueError("dynamic logical-record tail is not an integral timestep sequence")

    without_interception: list[float] = []
    with_explicit_interception: list[float] = []
    explicit_interception_delta_abs: list[float] = []
    negative_runoff_steps = 0

    for step_index in range(len(dynamic) // records_per_step):
        start = step_index * records_per_step
        group = dynamic[start : start + records_per_step]
        surface_step = _norm(
            _f32(group[0], 19 if hlpimp == 11 else 18, "dynamic surface record")
        )
        if hlpimp == 11:
            (
                _endpoint,
                step_days,
                prr,
                prsn,
                prirr,
                evicpr,
                evicirr,
                evsn,
                evso,
                evpn,
                _evsoma,
                _evtrma,
                runon,
                runoff,
                _groundwater_level,
                interception_end,
                ponding_end,
                snow_end,
                _wabaer,
            ) = surface_step
        else:
            (
                _endpoint,
                step_days,
                prr,
                prsn,
                prirr,
                evicpr,
                evicirr,
                evsn,
                evso,
                evpn,
                _evsoma,
                _evtrma,
                runon,
                runoff,
                _groundwater_level,
                ponding_end,
                snow_end,
                _wabaer,
            ) = surface_step
            interception_end = None

        moisture_end = _norm(_f32(group[2], layer_count, "Mofrt"))
        flev = _norm(_f32(group[3], layer_count, "Flev"))
        flab = _norm(_f32(group[4], layer_count + 1, "Flab"))

        position = 5
        drainage_total = 0.0
        for drainage_index in range(drainage_count):
            row = _norm(
                _f32(group[position], layer_count, f"Fldr[{drainage_index + 1}]")
            )
            drainage_total += sum(row)
            position += 1

        _f32(group[position], 4, "local producer crop/weather")
        position += 1
        _f32(group[position], 1, "local average date")
        position += 1
        _f32(group[position], layer_count, "producer temperature/dummy")
        position += 1
        if position != len(group):
            raise ValueError("unexpected dynamic record count")

        if step_days <= 0.0:
            raise ValueError("non-positive producer timestep")
        run_in = -runoff if runoff < 0.0 else 0.0
        if runoff < 0.0:
            negative_runoff_steps += 1

        profile_evapotranspiration = sum(flev)
        leak = flab[-1]
        soil_storage_term = sum(
            (previous - current) * thickness
            for previous, current, thickness in zip(
                moisture_previous, moisture_end, layer_thickness
            )
        )

        residual_without = (
            step_days
            * (
                prr
                + prsn
                + prirr
                + runon
                + run_in
                - evicpr
                - evicirr
                - evsn
                - evpn
                - evso
                - profile_evapotranspiration
                - runoff
                - drainage_total
                - leak
            )
            - (ponding_end - ponding_previous)
            - (snow_end - snow_previous)
            + soil_storage_term
        )
        without_interception.append(residual_without)

        if hlpimp == 11:
            assert interception_previous is not None and interception_end is not None
            interception_delta = interception_end - interception_previous
            residual_with = residual_without - interception_delta
            with_explicit_interception.append(residual_with)
            explicit_interception_delta_abs.append(abs(interception_delta))
            interception_previous = interception_end

        moisture_previous = list(moisture_end)
        ponding_previous = ponding_end
        snow_previous = snow_end

    result = {
        "evidence_class": "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2",
        "headers": headers,
        "hlpimp": hlpimp,
        "layer_count": layer_count,
        "horizon_count": horizon_count,
        "drainage_count": drainage_count,
        "timestep_count": len(without_interception),
        "dynamic_records_per_step": records_per_step,
        "negative_runoff_steps": negative_runoff_steps,
        "whole_profile_residual_without_interception_storage": _stats(without_interception),
    }
    if hlpimp == 11:
        result["whole_profile_residual_with_explicit_interception_storage"] = _stats(
            with_explicit_interception
        )
        no_storage = result["whole_profile_residual_without_interception_storage"]
        with_storage = result["whole_profile_residual_with_explicit_interception_storage"]
        result["mean_abs_improvement_factor"] = (
            no_storage["mean_abs_m"] / with_storage["mean_abs_m"]
            if with_storage["mean_abs_m"] > 0.0
            else None
        )
        result["max_abs_interception_delta_m"] = max(explicit_interception_delta_abs)
    else:
        result["whole_profile_residual_with_explicit_interception_storage"] = (
            "NOT_AVAILABLE_IN_LAYOUT"
        )
    return result


def analyze_file(path: Path, expected_sha256: str | None = None) -> dict:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected_sha256 is not None and digest.lower() != expected_sha256.lower():
        raise ValueError(
            f"source SHA-256 mismatch: expected {expected_sha256}, got {digest}"
        )
    records, physical_blocks = parse_powerstation_records(data)
    result = analyze_records(records)
    result.update(
        {
            "source_path": str(path),
            "source_sha256": digest,
            "logical_record_count": len(records),
            "physical_block_count": physical_blocks,
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--expect-sha256")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze_file(args.source, args.expect_sha256)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
