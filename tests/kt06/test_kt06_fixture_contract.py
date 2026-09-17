from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
metadata = json.loads(
    (ROOT / "reference/kt06/LWKM_FIRST_INTERVAL_METADATA.json").read_text()
)
source = (ROOT / "tests/kt06/mod_kt06_lwkm_interval_fixture.f90").read_text()


def scalar(name: str) -> float:
    match = re.search(rf"{name}\s*=\s*([0-9.+-]+)(?:_real64)?", source)
    if not match:
        raise AssertionError(f"missing fixture constant {name}")
    return float(match.group(1))


def integer(name: str) -> int:
    match = re.search(rf"{name}\s*=\s*([0-9]+)", source)
    if not match:
        raise AssertionError(f"missing fixture constant {name}")
    return int(match.group(1))


assert integer("LWKM_LAYER_COUNT") == metadata["layer_count"]
assert integer("LWKM_DRAINAGE_COUNT") == metadata["drainage_count"]
assert scalar("LWKM_ENDPOINT_DAY") == metadata["producer_endpoint_day_raw_real4"]
assert scalar("LWKM_STEP_DAYS") == metadata["producer_step_days_raw_real4"]
assert scalar("LWKM_SICT_END") == metadata["interception_storage_end_raw_real4_m"]
assert metadata["first_dynamic_group_sha256"] in source
print("KT06 derived fixture parity: PASS")
