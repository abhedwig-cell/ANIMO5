#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys
import zlib

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
EXPECTED_JSON_SHA256 = "fcb306cb4661139be0bc425db8fd4ff3d1d8d696a1a485c22dd6c67f5bb662b2"
ANCHORS = {
    0: "first_packet_and_first_duration_10",
    2: "first_duration_11",
    5: "first_duration_8",
    41: "first_duration_9",
    449: "quarter_anchor",
    899: "mid_sequence_anchor",
    1349: "three_quarter_anchor",
    1799: "last_packet",
}


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
    if "V7.3.3.3" not in static["headers"][3]:
        raise SystemExit("unexpected producer model header")

    items = []
    for index, role in ANCHORS.items():
        step = parse_dynamic_step(records, index, static)
        step.require_hydro_detailed_projection()
        provenance = legacy_step_provenance(records, index, static)
        items.append({
            "index_zero_based": index,
            "role": role,
            "dynamic_group_sha256": provenance.source_record_sha256,
            "typed_step_sha256": typed_step_digest(step),
            "diagnostic_normalized_step": step.__dict__,
        })

    payload = {
        "workunit": "ANIMO-KT09",
        "title": "LWKM Representative Real-Packet Compiled KT05 Consumption",
        "evidence_class": "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2",
        "source_sha256": source_sha,
        "source_model_version": "V7.3.3.3",
        "legacy_layout_id": LEGACY_LAYOUT_ID,
        "hlpimp": 11,
        "anchor_count": len(items),
        "anchors": items,
        "nonclaims": [
            "B2 historical compiler equivalence",
            "complete 1800-packet compiled KT05 consumption",
            "KT02 or KT06 runtime integration",
            "multi-packet forcing-provider semantics",
            "Hydro_detailed scientific execution",
            "ANIMO scientific admissibility",
            "Hlpimp=1 semantics",
            "production coupling",
        ],
    }

    raw_json = json.dumps(payload, indent=2).encode("utf-8")
    digest = hashlib.sha256(raw_json).hexdigest()
    if digest != EXPECTED_JSON_SHA256:
        raise SystemExit(f"unexpected KT09 bundle SHA-256: {digest}")
    encoded = base64.b64encode(zlib.compress(raw_json, 9)).decode("ascii")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
