#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from prototype.kt03.hydrology_step import typed_step_digest
from prototype.kt19.pinned_lwkm_file_provider import (
    PinnedLWKMFileHydrologyProvider,
)

ROOT = Path(__file__).resolve().parents[1]
KT08_SUMMARY = ROOT / "reference" / "kt11" / "LWKM_SEQUENCE_SUMMARY_KT08.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--container-sha256", default="")
    parser.add_argument("--container-label", default="")
    args = parser.parse_args()

    provider = PinnedLWKMFileHydrologyProvider.from_path(
        args.source,
        runtime_calendar_contract_id="ANIMO_KT19_EXTERNAL_REPLAY_CALENDAR",
        producer_day_offset=0,
    )
    summary = json.loads(KT08_SUMMARY.read_text())
    identity = provider.identity

    expected = summary["aggregate_identity"]
    actual = {
        "typed_step_digest_sequence_sha256":
            identity.typed_step_digest_sequence_sha256,
        "dynamic_group_digest_sequence_sha256":
            identity.dynamic_group_digest_sequence_sha256,
        "temporal_and_digest_record_sequence_sha256":
            identity.temporal_and_digest_record_sequence_sha256,
    }
    if actual != expected:
        raise SystemExit(f"aggregate identity mismatch: {actual!r} != {expected!r}")

    anchors = []
    for anchor in summary["anchors"]:
        endpoint = int(anchor["endpoint_day"])
        duration = int(anchor["duration_days"])
        selected = provider.select(
            endpoint - duration,
            endpoint,
            "ANIMO_KT19_EXTERNAL_REPLAY_CALENDAR",
        )
        digest = typed_step_digest(selected)
        if digest != anchor["typed_step_sha256"]:
            raise SystemExit(
                f"anchor {anchor['index_zero_based']} digest mismatch: "
                f"{digest} != {anchor['typed_step_sha256']}"
            )
        anchors.append({
            "index_zero_based": anchor["index_zero_based"],
            "endpoint_day": endpoint,
            "duration_days": duration,
            "typed_step_sha256": digest,
            "result": "PASS",
        })

    implementation_path = ROOT / "prototype" / "kt19" / "pinned_lwkm_file_provider.py"
    payload = {
        "work_unit": "ANIMO-KT19",
        "evidence_role": "EXTERNAL_PINNED_B0_REPLAY_OF_KT19_PROVIDER_NOT_CI_SELF_CONTAINED",
        "source_path_label": args.source.name,
        "source_sha256": identity.source_sha256,
        "source_size_bytes": args.source.stat().st_size,
        "source_container_label": args.container_label,
        "source_container_sha256": args.container_sha256,
        "implementation_sha256": hashlib.sha256(
            implementation_path.read_bytes()
        ).hexdigest(),
        "packet_count": identity.packet_count,
        "logical_record_count": identity.logical_record_count,
        "physical_block_count": identity.physical_block_count,
        "static_metadata": {
            "hlpimp": provider.static_metadata["hlpimp"],
            "layer_count": provider.static_metadata["nl"],
            "horizon_count": provider.static_metadata["nh"],
            "drainage_count": provider.static_metadata["nudr"],
            "has_soil_temperature": bool(provider.static_metadata["ioptte"]),
        },
        "aggregate_identity": actual,
        "kt08_identity_match": True,
        "anchor_selection_results": anchors,
        "runtime_selection_mode": "EXACT_INTEGER_WHOLE_DAY_WITH_EXPLICIT_CALENDAR_AND_OFFSET",
        "source_bytes_committed_to_repository": False,
        "b2_claimed": False,
        "production_claimed": False,
        "notes": [
            "The full pinned source is externally supplied and hash-verified.",
            "CI can replay the committed B1-derived first-packet byte fixture but not the full B0 source.",
            "This evidence does not establish historical compiler or executable equivalence."
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
