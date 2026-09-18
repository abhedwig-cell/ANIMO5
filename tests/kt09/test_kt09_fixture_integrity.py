from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prototype.kt03.hydrology_step import HydrologyStep, typed_step_digest

FIXTURE = ROOT / "reference/kt09/LWKM_REPRESENTATIVE_ANCHOR_PACKETS.json.zlib.b64"
KT08 = ROOT / "reference/kt08/LWKM_SEQUENCE_SUMMARY.json"
KT07 = ROOT / "reference/kt07/LWKM_FIRST_EXPLICIT_HYDROLOGY_STEP.json"

EXPECTED_COMPRESSED_TEXT_SHA256 = "bb28e4f8ce0a23dfad497c4c52c4916fd6c30b322ad66b326db09d7d88f2ea13"
EXPECTED_JSON_SHA256 = "fcb306cb4661139be0bc425db8fd4ff3d1d8d696a1a485c22dd6c67f5bb662b2"
EXPECTED_SOURCE_SHA256 = "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c"
EXPECTED_INDICES = [0, 2, 5, 41, 449, 899, 1349, 1799]


def load_bundle() -> dict:
    encoded = FIXTURE.read_text().strip()
    assert hashlib.sha256(encoded.encode("ascii")).hexdigest() == EXPECTED_COMPRESSED_TEXT_SHA256
    raw_json = zlib.decompress(base64.b64decode(encoded))
    assert hashlib.sha256(raw_json).hexdigest() == EXPECTED_JSON_SHA256
    return json.loads(raw_json)


bundle = load_bundle()
kt08 = json.loads(KT08.read_text())
kt07 = json.loads(KT07.read_text())

assert bundle["workunit"] == "ANIMO-KT09"
assert bundle["evidence_class"] == "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2"
assert bundle["source_sha256"] == EXPECTED_SOURCE_SHA256
assert bundle["source_model_version"] == "V7.3.3.3"
assert bundle["legacy_layout_id"] == "ANIMO41_SWAP3_RECORD_LAYOUT_V1"
assert bundle["hlpimp"] == 11
assert bundle["anchor_count"] == 8

anchors = bundle["anchors"]
assert [a["index_zero_based"] for a in anchors] == EXPECTED_INDICES
kt08_by_index = {a["index_zero_based"]: a for a in kt08["anchors"]}

durations = set()
nonzero_sict = 0
for anchor in anchors:
    index = anchor["index_zero_based"]
    evidence = kt08_by_index[index]
    assert anchor["role"] == evidence["role"]
    assert anchor["dynamic_group_sha256"] == evidence["dynamic_group_sha256"]
    assert anchor["typed_step_sha256"] == evidence["typed_step_sha256"]

    step = HydrologyStep(**anchor["diagnostic_normalized_step"])
    step.validate()
    step.require_hydro_detailed_projection()
    assert typed_step_digest(step) == anchor["typed_step_sha256"]
    assert step.layer_count == 30
    assert step.drainage_count == 5
    assert step.has_interception_storage_end
    assert step.has_soil_temperature
    assert len(step.sc) == 30
    assert len(step.mofrt) == 30
    assert len(step.flev) == 30
    assert len(step.flab) == 31
    assert len(step.fldr) == 5
    assert all(len(row) == 30 for row in step.fldr)
    assert len(step.soil_temperature) == 30
    durations.add(int(step.producer_step_days))
    if step.interception_storage_end != 0.0:
        nonzero_sict += 1

assert durations == {8, 9, 10, 11}
assert nonzero_sict >= 1

first = anchors[0]["diagnostic_normalized_step"]
assert first == kt07["diagnostic_normalized_step"]
assert anchors[0]["typed_step_sha256"] == kt07["typed_step_digest_sha256"]
assert anchors[0]["dynamic_group_sha256"] == kt07["dynamic_group_sha256"]

assert "complete 1800-packet compiled KT05 consumption" in bundle["nonclaims"]
assert "KT02 or KT06 runtime integration" in bundle["nonclaims"]

print("KT09 representative real-packet fixture integrity: PASS")
