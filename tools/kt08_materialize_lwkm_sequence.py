#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.convert_legacy_unformatted import parse_powerstation_records
from prototype.kt03.hydrology_step import (
    LEGACY_LAYOUT_ID,
    legacy_step_provenance,
    parse_dynamic_step,
    parse_swap3_static,
    typed_step_digest,
)

EXPECTED_SOURCE_SHA256 = "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c"
EXPECTED_PACKET_COUNT = 1800
EXPECTED_TYPED_SEQUENCE_SHA256 = "c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4"
EXPECTED_GROUP_SEQUENCE_SHA256 = "40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34"
EXPECTED_RECORD_SEQUENCE_SHA256 = "eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1"
EXPECTED_DURATION_HISTOGRAM = {8.0: 37, 9.0: 13, 10.0: 1400, 11.0: 350}
EXPECTED_LAST_ENDPOINT = 18263.0
EXPECTED_NONZERO_SICT_COUNT = 652
EXPECTED_MAX_SICT = 0.0002


def sequence_sha256(values: list[str]) -> str:
    return hashlib.sha256(("\n".join(values) + "\n").encode("ascii")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    raw = args.source.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"unexpected LWKM source SHA-256: {source_sha}")

    records, _ = parse_powerstation_records(raw)
    static = parse_swap3_static(records)
    required = {
        "hlpimp": 11,
        "nl": 30,
        "nh": 30,
        "nudr": 5,
        "ioptte": True,
    }
    for key, expected in required.items():
        if static[key] != expected:
            raise SystemExit(f"unexpected {key}: {static[key]!r}")

    model_header = static["headers"][3]
    if "V7.3.3.3" not in model_header:
        raise SystemExit(f"unexpected producer model header: {model_header!r}")

    records_per_step = 8 + static["nudr"]
    dynamic_count = len(records) - static["dynamic_start"]
    if dynamic_count % records_per_step != 0:
        raise SystemExit("dynamic logical-record count is not step-aligned")
    packet_count = dynamic_count // records_per_step
    if packet_count != EXPECTED_PACKET_COUNT:
        raise SystemExit(f"unexpected packet count: {packet_count}")

    typed_digests: list[str] = []
    group_digests: list[str] = []
    record_lines: list[str] = []
    durations: Counter[float] = Counter()
    anchors: list[dict] = []
    selected_anchor_indices = {0, 2, 5, 41, 449, 899, 1349, 1799}

    previous_endpoint: float | None = None
    first_origin: float | None = None
    nonzero_sict_count = 0
    minimum_sict: float | None = None
    maximum_sict: float | None = None

    for index in range(packet_count):
        step = parse_dynamic_step(records, index, static)
        step.validate()
        step.require_hydro_detailed_projection()
        provenance = legacy_step_provenance(records, index, static)

        endpoint = step.producer_endpoint_day
        duration = step.producer_step_days
        origin = endpoint - duration
        if index == 0:
            first_origin = origin
        elif origin != previous_endpoint:
            raise SystemExit(
                f"producer chain discontinuity at {index}: "
                f"origin={origin}, previous_endpoint={previous_endpoint}"
            )
        previous_endpoint = endpoint

        typed = typed_step_digest(step)
        group = provenance.source_record_sha256
        typed_digests.append(typed)
        group_digests.append(group)
        record_lines.append(
            f"{index}|{endpoint:.17g}|{duration:.17g}|{group}|{typed}"
        )
        durations[duration] += 1

        sict = step.interception_storage_end
        if sict is None:
            raise SystemExit(f"explicit interception unexpectedly absent at {index}")
        if sict != 0.0:
            nonzero_sict_count += 1
        minimum_sict = sict if minimum_sict is None else min(minimum_sict, sict)
        maximum_sict = sict if maximum_sict is None else max(maximum_sict, sict)

        if index in selected_anchor_indices:
            anchors.append({
                "index_zero_based": index,
                "endpoint_day": endpoint,
                "duration_days": duration,
                "dynamic_group_sha256": group,
                "typed_step_sha256": typed,
            })

    typed_sequence_sha = sequence_sha256(typed_digests)
    group_sequence_sha = sequence_sha256(group_digests)
    record_sequence_sha = sequence_sha256(record_lines)

    checks = {
        "typed sequence": (typed_sequence_sha, EXPECTED_TYPED_SEQUENCE_SHA256),
        "group sequence": (group_sequence_sha, EXPECTED_GROUP_SEQUENCE_SHA256),
        "record sequence": (record_sequence_sha, EXPECTED_RECORD_SEQUENCE_SHA256),
        "last endpoint": (previous_endpoint, EXPECTED_LAST_ENDPOINT),
        "duration histogram": (dict(durations), EXPECTED_DURATION_HISTOGRAM),
        "nonzero Sict count": (nonzero_sict_count, EXPECTED_NONZERO_SICT_COUNT),
        "maximum Sict": (maximum_sict, EXPECTED_MAX_SICT),
    }
    for label, (actual, expected) in checks.items():
        if actual != expected:
            raise SystemExit(f"{label} mismatch: {actual!r} != {expected!r}")

    payload = {
        "workunit": "ANIMO-KT08",
        "evidence_class": "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2",
        "source_case": "LWKM_gras_1040.2021.2045",
        "source_member": "input/SWATRE.UNF",
        "source_sha256": source_sha,
        "source_model_version": "V7.3.3.3",
        "legacy_layout_id": LEGACY_LAYOUT_ID,
        "hlpimp": static["hlpimp"],
        "static": {
            "layer_count": static["nl"],
            "horizon_count": static["nh"],
            "drainage_count": static["nudr"],
            "has_soil_temperature": bool(static["ioptte"]),
        },
        "sequence": {
            "packet_count": packet_count,
            "first_origin_day": first_origin,
            "first_endpoint_day": parse_dynamic_step(records, 0, static).producer_endpoint_day,
            "last_endpoint_day": previous_endpoint,
            "sum_producer_step_days": sum(k * v for k, v in durations.items()),
            "chain_violation_count": 0,
            "unique_endpoint_count": packet_count,
            "all_packets_explicit_interception": True,
            "all_packets_soil_temperature": True,
            "duration_histogram_days": {
                str(int(key)): value for key, value in sorted(durations.items())
            },
            "interception_storage_end_m": {
                "minimum": minimum_sict,
                "maximum": maximum_sict,
                "nonzero_packet_count": nonzero_sict_count,
            },
        },
        "aggregate_identity": {
            "typed_step_digest_sequence_sha256": typed_sequence_sha,
            "dynamic_group_digest_sequence_sha256": group_sequence_sha,
            "temporal_and_digest_record_sequence_sha256": record_sequence_sha,
        },
        "anchors": anchors,
        "diagnostic_normalization": {
            "authority": (
                "prototype/kt03/hydrology_step.py::"
                "legacy_dble_trunc_diagnostic"
            ),
            "classification": "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2",
        },
        "nonclaims": [
            "B2 historical compiler equivalence",
            "generic producer sequence semantics outside the pinned LWKM file",
            "KT02 or KT06 runtime integration",
            "multi-packet forcing-provider semantics",
            "retry or timestep-selection policy",
            "Hydro_detailed scientific execution",
            "ANIMO scientific admissibility",
            "Hlpimp=1 semantics",
            "production coupling",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
