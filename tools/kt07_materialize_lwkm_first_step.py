#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
EXPECTED_GROUP_SHA256 = "2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7"
EXPECTED_TYPED_STEP_DIGEST = "eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c"


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

    index = 0
    count = 8 + static["nudr"]
    start = static["dynamic_start"] + index * count
    group = records[start:start + count]
    if len(group) != count:
        raise SystemExit("incomplete first dynamic record group")

    provenance = legacy_step_provenance(records, index, static)
    if provenance.source_record_sha256 != EXPECTED_GROUP_SHA256:
        raise SystemExit(
            f"unexpected dynamic-group SHA-256: {provenance.source_record_sha256}"
        )

    step = parse_dynamic_step(records, index, static)
    step_digest = typed_step_digest(step)
    if step_digest != EXPECTED_TYPED_STEP_DIGEST:
        raise SystemExit(f"unexpected typed-step digest: {step_digest}")

    payload = {
        "workunit": "ANIMO-KT07",
        "evidence_class": "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2",
        "source_case": "LWKM_gras_1040.2021.2045",
        "source_member": "input/SWATRE.UNF",
        "source_sha256": source_sha,
        "source_model_version": "V7.3.3.3",
        "legacy_layout_id": LEGACY_LAYOUT_ID,
        "hlpimp": static["hlpimp"],
        "dynamic_step_index_zero_based": index,
        "dynamic_group_sha256": provenance.source_record_sha256,
        "dynamic_group_record_lengths": [len(record) for record in group],
        "static": {
            "layer_count": static["nl"],
            "horizon_count": static["nh"],
            "drainage_count": static["nudr"],
            "has_soil_temperature": bool(static["ioptte"]),
        },
        "diagnostic_normalization": {
            "authority": (
                "prototype/kt03/hydrology_step.py::"
                "legacy_dble_trunc_diagnostic"
            ),
            "classification": "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2",
        },
        "diagnostic_normalized_step": step.__dict__,
        "typed_step_digest_sha256": step_digest,
        "nonclaims": [
            "B2 historical compiler equivalence",
            "revision-53 Hydro_detailed execution equivalence",
            "ANIMO scientific admissibility",
            "KT02 runtime integration",
            "Hlpimp=1 semantics",
            "production coupling",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
