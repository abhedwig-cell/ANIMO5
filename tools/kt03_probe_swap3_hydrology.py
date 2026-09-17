#!/usr/bin/env python3
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import json
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype.kt03.hydrology_step import (  # noqa: E402
    HydrologyAdapterError,
    parse_dynamic_step,
    parse_swap3_static,
    typed_step_digest,
)
from tools.convert_legacy_unformatted import parse_powerstation_records  # noqa: E402


def decimal_value(value: float) -> Decimal:
    return Decimal(str(value))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--profile-bottom", type=float)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    raw = args.source.read_bytes()
    source_sha256 = hashlib.sha256(raw).hexdigest()
    if args.expected_sha256 and source_sha256 != args.expected_sha256:
        raise HydrologyAdapterError(
            f"source SHA-256 mismatch: {source_sha256} != {args.expected_sha256}"
        )

    records, physical_blocks = parse_powerstation_records(raw)
    static = parse_swap3_static(records)
    records_per_step = 8 + static["nudr"]
    dynamic_record_count = len(records) - static["dynamic_start"]
    if dynamic_record_count <= 0 or dynamic_record_count % records_per_step != 0:
        raise HydrologyAdapterError(
            "dynamic record tail is not an integral timestep sequence"
        )
    timestep_count = dynamic_record_count // records_per_step

    sentinel_count = 0
    for index in range(timestep_count):
        start = static["dynamic_start"] + index * records_per_step
        expected_surface_values = 19 if static["hlpimp"] == 11 else 18
        surface = records[start]
        if len(surface) != expected_surface_values * 4:
            raise HydrologyAdapterError(
                f"unexpected dynamic surface record size at step {index + 1}"
            )
        values = struct.unpack("<" + "f" * expected_surface_values, surface)
        if not all(math.isfinite(value) for value in values):
            raise HydrologyAdapterError(
                f"non-finite dynamic surface value at step {index + 1}"
            )
        if values[14] < -9.98:
            sentinel_count += 1

    if sentinel_count and args.profile_bottom is None:
        raise HydrologyAdapterError(
            "groundwater sentinel occurs in source; --profile-bottom is required"
        )

    steps = [
        parse_dynamic_step(
            records,
            index,
            static,
            profile_bottom=args.profile_bottom,
        )
        for index in range(timestep_count)
    ]

    chain_mismatches = []
    previous_endpoint = decimal_value(steps[0].tiwa) - decimal_value(
        steps[0].step_days
    )
    interval_origin = previous_endpoint
    for index, step in enumerate(steps):
        origin = decimal_value(step.tiwa) - decimal_value(step.step_days)
        if origin != previous_endpoint:
            chain_mismatches.append(
                {
                    "step_index": index + 1,
                    "expected_origin": str(previous_endpoint),
                    "observed_origin": str(origin),
                }
            )
        previous_endpoint = decimal_value(step.tiwa)

    downstream_compatible_count = 0
    for step in steps:
        try:
            step.hydro_detailed_boundary()
        except HydrologyAdapterError:
            pass
        else:
            downstream_compatible_count += 1

    dynamic_payload = b"".join(records[static["dynamic_start"] :])
    metadata = {
        "evidence_class": "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2",
        "case_id": args.case_id,
        "source_sha256": source_sha256,
        "logical_record_count": len(records),
        "physical_block_count": physical_blocks,
        "header_record_count": static["dynamic_start"],
        "dynamic_record_count": dynamic_record_count,
        "dynamic_records_per_step": records_per_step,
        "timestep_count": timestep_count,
        "hlpimp": static["hlpimp"],
        "layer_count": static["nl"],
        "horizon_count": static["nh"],
        "drainage_count": static["nudr"],
        "hydrology_period": {
            "start_year": static["start_year"],
            "end_year": static["end_year"],
            "start_time": static["start_time"],
            "end_time": static["end_time"],
        },
        "ioptte_from_initial_temperature_record": static["ioptte"],
        "interval_origin": float(interval_origin),
        "tiwa_first": steps[0].tiwa,
        "tiwa_last": steps[-1].tiwa,
        "step_days_values": sorted({step.step_days for step in steps}),
        "interval_chain_exact_decimal": len(chain_mismatches) == 0,
        "interval_chain_mismatches": chain_mismatches[:20],
        "groundwater_sentinel_count": sentinel_count,
        "interception_storage_available_count": sum(
            1 for step in steps if step.has_interception_storage_end
        ),
        "downstream_compatible_count": downstream_compatible_count,
        "dynamic_logical_payload_sha256": hashlib.sha256(dynamic_payload).hexdigest(),
        "first_step_source_record_sha256": steps[0].source_record_sha256,
        "last_step_source_record_sha256": steps[-1].source_record_sha256,
        "first_step_typed_sha256": typed_step_digest(steps[0]),
        "last_step_typed_sha256": typed_step_digest(steps[-1]),
        "normalization": (
            "diagnostic reimplementation of revision-53 Dble_trunc; "
            "not independently qualified historical compiler authority"
        ),
    }

    text = json.dumps(metadata, indent=2) + "\n"
    if args.metadata:
        args.metadata.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
