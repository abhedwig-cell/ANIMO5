#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="frozen SWATRE.UNF file")
    parser.add_argument("--profile-bottom", type=float)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    raw = args.source.read_bytes()
    records, physical_blocks = parse_powerstation_records(raw)
    static = parse_swap3_static(records)

    records_per_step = 8 + static["nudr"]
    remainder = len(records) - static["dynamic_start"]
    if remainder < 0 or remainder % records_per_step != 0:
        raise HydrologyAdapterError("dynamic record tail is not an integral timestep sequence")
    timestep_count = remainder // records_per_step
    if timestep_count <= 0:
        raise HydrologyAdapterError("no dynamic timesteps found")

    sentinel_count = 0
    for index in range(timestep_count):
        start = static["dynamic_start"] + index * records_per_step
        surface = records[start]
        if len(surface) != 72:
            raise HydrologyAdapterError("unexpected CranMais surface record size")
        values = struct.unpack("<18f", surface)
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

    expected_tiwa = [float(index) for index in range(1, timestep_count + 1)]
    if [step.tiwa for step in steps] != expected_tiwa:
        raise HydrologyAdapterError("CranMais Tiwa sequence is not exact 1..N")

    dynamic_payload = b"".join(records[static["dynamic_start"] :])
    metadata = {
        "evidence_class": "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2",
        "case_id": "CranMais",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "logical_record_count": len(records),
        "physical_block_count": physical_blocks,
        "header_record_count": static["dynamic_start"],
        "dynamic_record_count": remainder,
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
        "tiwa_first": steps[0].tiwa,
        "tiwa_last": steps[-1].tiwa,
        "all_step_days_one": all(step.step_days == 1.0 for step in steps),
        "groundwater_sentinel_count": sentinel_count,
        "interception_storage_end_available_from_file": False,
        "dynamic_logical_payload_sha256": hashlib.sha256(dynamic_payload).hexdigest(),
        "first_step_source_record_sha256": steps[0].source_record_sha256,
        "last_step_source_record_sha256": steps[-1].source_record_sha256,
        "first_step_typed_sha256": typed_step_digest(steps[0]),
        "last_step_typed_sha256": typed_step_digest(steps[-1]),
        "normalization": (
            "diagnostic reimplementation of revision-53 Dble_trunc; "
            "not independently qualified historical compiler authority"
        ),
        "downstream_compatibility": "BLOCKED_UNDEFINED_SICT_FOR_HLPIMP_1",
    }

    text = json.dumps(metadata, indent=2) + "\n"
    if args.metadata:
        args.metadata.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
