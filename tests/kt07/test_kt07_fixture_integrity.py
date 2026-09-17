from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prototype.kt03.hydrology_step import HydrologyStep, typed_step_digest

FIXTURE = ROOT / "reference/kt07/LWKM_FIRST_EXPLICIT_HYDROLOGY_STEP.json"
data = json.loads(FIXTURE.read_text())

assert data["evidence_class"] == "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2"
assert data["source_sha256"] == (
    "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c"
)
assert data["dynamic_group_sha256"] == (
    "2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7"
)
assert data["hlpimp"] == 11
assert data["dynamic_group_record_lengths"] == [
    76, 120, 120, 120, 124, 120, 120, 120, 120, 120, 16, 4, 120
]

step_payload = data["diagnostic_normalized_step"]
step = HydrologyStep(**step_payload)
step.validate()
assert typed_step_digest(step) == data["typed_step_digest_sha256"]

assert step.layer_count == data["static"]["layer_count"] == 30
assert step.drainage_count == data["static"]["drainage_count"] == 5
assert data["static"]["horizon_count"] == 30
assert step.has_interception_storage_end
assert step.interception_storage_end == 0.0
assert step.has_soil_temperature
assert len(step.soil_temperature) == step.layer_count
assert len(step.flab) == step.layer_count + 1
assert len(step.fldr) == step.drainage_count
assert all(len(row) == step.layer_count for row in step.fldr)

assert "B2 historical compiler equivalence" in data["nonclaims"]
assert data["diagnostic_normalization"]["classification"] == (
    "B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2"
)

print("KT07 real-packet fixture integrity: PASS")
