#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I03_STATUS.json"
CROSSWALK = ROOT / "integration/animo-b3/B3I03_MASSQ02_FINDING_CROSSWALK.csv"
RESERVATIONS = ROOT / "integration/animo-b3/B3I03_TCD_RESERVATIONS.json"
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
EXPECTED_STATUS = "QUALIFIED_POST_MASSQ02_INCREMENTAL_CAUSAL_INTAKE_TCD042_RESERVED_NO_ADMISSIONS"
BASE = "c1a69c00a02aa0e32ca60580c3d0ebee96442c17"


def fail(msg):
    raise SystemExit(f"B3I03 validation failed: {msg}")


status = json.loads(STATUS.read_text())
if status.get("status") != EXPECTED_STATUS:
    fail("unexpected final status")
if status.get("work_unit") != "ANIMO-B3I03":
    fail("wrong work unit")
if status.get("work_status", {}).get("qualified") is not True:
    fail("qualified flag is not true")
if status.get("work_status", {}).get("work_unit_complete") is not True:
    fail("work unit complete flag is not true")
if status.get("admission_state", {}).get("corrected_legacy_admitted") is not False:
    fail("correction admission must remain false")
if status.get("admission_state", {}).get("production_migration_admitted") is not False:
    fail("production migration must remain false")

with CROSSWALK.open(newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) != 15:
    fail(f"expected 15 crosswalk rows, got {len(rows)}")
new_res = [r for r in rows if r["disposition"] == "NEW_FAIL_CLOSED_TCD_RESERVATION"]
if len(new_res) != 1 or new_res[0]["canonical_route"] != "TCD-042":
    fail("crosswalk must contain exactly one new reservation for TCD-042")
if any(r["admission"] != "NONE" for r in rows):
    fail("crosswalk contains an admission")

res = json.loads(RESERVATIONS.read_text())
items = res.get("reservations", [])
if len(items) != 1 or items[0].get("tcd_id") != "TCD-042":
    fail("reservation artifact must contain exactly TCD-042")
if items[0].get("admitted") is not False:
    fail("TCD-042 must not be admitted")
if items[0].get("atomicity") != "REQUIRES_ATOMIZATION_BEFORE_ADMISSION":
    fail("TCD-042 atomicity guard missing")
if res.get("allocation_summary", {}).get("canonical_register_append_performed") is not False:
    fail("canonical register append must remain false")

register_lines = [ln for ln in REGISTER.read_text().splitlines() if ln.strip()]
if not register_lines[-1].startswith("TCD-041,"):
    fail("canonical register tail is not TCD-041")
if any(ln.startswith("TCD-042,") for ln in register_lines):
    fail("TCD-042 must not already be appended by B3I03")

allowed = (
    "docs/b3/POST_MASSQ02_INCREMENTAL_CAUSAL_INTAKE.md",
    "integration/animo-b3/ANIMO-B3I03_STATUS.json",
    "integration/animo-b3/B3I03_MASSQ02_FINDING_CROSSWALK.csv",
    "integration/animo-b3/B3I03_TCD_RESERVATIONS.json",
    "tools/b3i03/validate_b3i03.py",
    ".github/workflows/animo-b3i03-massq02-intake.yml",
)
proc = subprocess.run(
    ["git", "diff", "--name-only", f"{BASE}..HEAD"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=True,
)
changed = [x for x in proc.stdout.splitlines() if x]
unexpected = [x for x in changed if x not in allowed]
if unexpected:
    fail(f"unexpected changed files: {unexpected}")

print("PASS B3I03 governance-only incremental intake validation")
print(f"crosswalk_rows={len(rows)}")
print("new_reservation=TCD-042")
print(f"changed_files={len(changed)}")
