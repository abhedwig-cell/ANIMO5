from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "reference/kt08/LWKM_SEQUENCE_SUMMARY.json"

EXPECTED_SOURCE_SHA = "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c"
EXPECTED_TYPED_SEQUENCE = "c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4"
EXPECTED_GROUP_SEQUENCE = "40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34"
EXPECTED_RECORD_SEQUENCE = "eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1"
EXPECTED_FIRST_PACKET_TYPED = "eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c"
EXPECTED_LAST_PACKET_TYPED = "fd66644f8ff471befadc0cb4ac46e615349e379d588437e6d6df390818fb4e0e"

data = json.loads(SUMMARY.read_text())

assert data["workunit"] == "ANIMO-KT08"
assert data["evidence_class"] == "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2"
assert data["source_sha256"] == EXPECTED_SOURCE_SHA
assert data["source_model_version"] == "V7.3.3.3"
assert data["legacy_layout_id"] == "ANIMO41_SWAP3_RECORD_LAYOUT_V1"
assert data["hlpimp"] == 11

static = data["static"]
assert static == {
    "layer_count": 30,
    "horizon_count": 30,
    "drainage_count": 5,
    "has_soil_temperature": True,
}

seq = data["sequence"]
assert seq["packet_count"] == 1800
assert seq["first_origin_day"] == 0.0
assert seq["first_endpoint_day"] == 10.0
assert seq["last_endpoint_day"] == 18263.0
assert seq["sum_producer_step_days"] == 18263.0
assert seq["chain_violation_count"] == 0
assert seq["unique_endpoint_count"] == 1800
assert seq["all_packets_explicit_interception"]
assert seq["all_packets_soil_temperature"]
assert seq["duration_histogram_days"] == {
    "8": 37,
    "9": 13,
    "10": 1400,
    "11": 350,
}
assert sum(
    int(duration) * count
    for duration, count in seq["duration_histogram_days"].items()
) == 18263
assert sum(seq["duration_histogram_days"].values()) == 1800
assert seq["interception_storage_end_m"] == {
    "minimum": 0.0,
    "maximum": 0.0002,
    "nonzero_packet_count": 652,
}

identity = data["aggregate_identity"]
assert identity["typed_step_digest_sequence_sha256"] == EXPECTED_TYPED_SEQUENCE
assert identity["dynamic_group_digest_sequence_sha256"] == EXPECTED_GROUP_SEQUENCE
assert (
    identity["temporal_and_digest_record_sequence_sha256"]
    == EXPECTED_RECORD_SEQUENCE
)

anchors = data["anchors"]
assert [a["index_zero_based"] for a in anchors] == [0, 2, 5, 41, 449, 899, 1349, 1799]
assert anchors[0]["typed_step_sha256"] == EXPECTED_FIRST_PACKET_TYPED
assert anchors[-1]["typed_step_sha256"] == EXPECTED_LAST_PACKET_TYPED
assert {int(a["duration_days"]) for a in anchors[:4]} == {8, 9, 10, 11}

for anchor in anchors:
    for key in ("dynamic_group_sha256", "typed_step_sha256"):
        digest = anchor[key]
        assert len(digest) == 64
        int(digest, 16)

assert data["diagnostic_normalization"]["classification"] == (
    "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2"
)
assert "multi-packet forcing-provider semantics" in data["nonclaims"]
assert "B2 historical compiler equivalence" in data["nonclaims"]

print("KT08 LWKM full-sequence evidence summary: PASS")
