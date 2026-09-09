#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I04_STATUS.json"
CROSSWALK = ROOT / "integration/animo-b3/B3I04_STATEQ02_FINDING_CROSSWALK.csv"
RESERVATIONS = ROOT / "integration/animo-b3/B3I04_TCD_RESERVATIONS.json"
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
NARRATIVE = ROOT / "docs/b3/POST_STATEQ02_INCREMENTAL_STATE_INTAKE.md"
BASE = "814ea660d367494432beb63ea78298d1f6cd73d7"
PENDING_STATUS = "PERSISTED_STATEQ02_INCREMENTAL_STATE_INTAKE_VALIDATION_PENDING"
FINAL_STATUS = "QUALIFIED_POST_STATEQ02_INCREMENTAL_STATE_EVIDENCE_INTAKE_NO_NEW_TCD_NO_ADMISSIONS"


def fail(msg):
    raise SystemExit(f"B3I04 validation failed: {msg}")


status = json.loads(STATUS.read_text())
if status.get("work_unit") != "ANIMO-B3I04":
    fail("wrong work unit")
if status.get("status") not in {PENDING_STATUS, FINAL_STATUS}:
    fail("unexpected status")
if status.get("base", {}).get("head") != BASE:
    fail("wrong canonical authority base")
if status.get("base", {}).get("canonical_register_tail") != "TCD-042":
    fail("base canonical tail must be TCD-042")
if status.get("evidence", {}).get("stateq02_head") != "ada93a409aa054f9aebac32728e79f80468215a7":
    fail("wrong STATEQ02 head")
if status.get("evidence", {}).get("comparison_policy") != "EXACT_BITWISE_NO_TOLERANCE":
    fail("STATEQ02 exact comparison policy missing")
if status.get("evidence", {}).get("longest_exact_post_restore_horizon_records") != 833:
    fail("833-record exact horizon missing")
if status.get("evidence", {}).get("guard_checkpoint_created") is not False:
    fail("guard checkpoint must not be created")

intake = status.get("intake", {})
if intake.get("new_tcd_reservations") != [] or intake.get("new_tcd_reservation_count") != 0:
    fail("new TCD reservation must be empty")
if intake.get("existing_tcd_routes") != ["TCD-040"]:
    fail("only TCD-040 may be reused")
if intake.get("canonical_register_append_performed") is not False:
    fail("canonical register append must remain false")
if intake.get("canonical_register_tail_after_work") != "TCD-042":
    fail("canonical register tail after work must remain TCD-042")
if intake.get("next_observed_unallocated_candidate") != "TCD-043":
    fail("next observed unallocated candidate must be TCD-043")
if intake.get("tcd_043_reserved") is not False:
    fail("TCD-043 must not be reserved")

admission = status.get("admission_state", {})
for key in (
    "scientific_admission_performed",
    "corrected_legacy_admitted",
    "canonical_state_admitted",
    "b3_baseline_established",
    "production_migration_admitted",
    "production_code_modified",
    "whole_model_state_claim",
):
    if admission.get(key) is not False:
        fail(f"admission guard {key} must remain false")

if status.get("status") == FINAL_STATUS:
    work = status.get("work_status", {})
    if not all(work.get(k) is True for k in ("realized", "persisted", "tested", "qualified", "work_unit_complete")):
        fail("final status requires all work-status flags true")
    if status.get("validation", {}).get("validator_result") != "PASS":
        fail("final status requires validator PASS")

with CROSSWALK.open(newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) != 3:
    fail(f"expected exactly 3 crosswalk rows, got {len(rows)}")
if len({r["finding_key"] for r in rows}) != 3:
    fail("crosswalk finding keys must be unique")
if any(r["admission"] != "NONE" for r in rows):
    fail("crosswalk contains an admission")
if any(r.get("canonical_route") == "TCD-043" for r in rows):
    fail("crosswalk must not route anything to TCD-043")

by_key = {r["finding_key"]: r for r in rows}
guard = by_key.get("STATEQ02-GUARD-282-TCD040-ACTIVE-SENTINEL")
if not guard:
    fail("missing STATEQ02 guard finding")
if guard["b3i04_classification"] != "EXISTING_TCD" or guard["canonical_route"] != "TCD-040":
    fail("guard finding must reuse TCD-040")

pn = by_key.get("STATEQ01-LCL-EXTCROP-FIRST-POSTRESTART-PN-DIVERGENCE")
if not pn or pn["b3i04_classification"] != "RUNTIME_HAZARD_NO_SCIENTIFIC_TCD" or pn["canonical_route"]:
    fail("Pn divergence must be runtime hazard with no TCD")

final_div = by_key.get("STATEQ01-LCL-EXTCROP-FINAL-STATE-DIVERGENCE")
if not final_div or final_div["b3i04_classification"] != "INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION" or final_div["canonical_route"]:
    fail("final-state divergence must remain insufficient evidence with no TCD")

res = json.loads(RESERVATIONS.read_text())
if res.get("reservations") != []:
    fail("reservation artifact must be empty")
if res.get("collision_scan", {}).get("reservation_created_for_tcd_043") is not False:
    fail("reservation artifact must not reserve TCD-043")
if [x.get("tcd_id") for x in res.get("existing_routes_reused", [])] != ["TCD-040"]:
    fail("reservation artifact must reuse only TCD-040")
for key, value in res.get("guards", {}).items():
    if value is not False:
        fail(f"reservation guard {key} must remain false")

with REGISTER.open(newline="") as f:
    reg_rows = list(csv.DictReader(f))
ids = [r.get("ID", "") for r in reg_rows]
if "TCD-042" not in ids:
    fail("canonical register must contain TCD-042 authority")
if "TCD-043" in ids:
    fail("canonical register must not contain TCD-043")
nums = [int(x.split("-")[1]) for x in ids if x.startswith("TCD-") and x.split("-")[1].isdigit()]
if not nums or max(nums) != 42:
    fail("canonical register maximum TCD id must remain 42")

narrative = NARRATIVE.read_text()
for token in (
    FINAL_STATUS,
    "reservations = []",
    "TCD-043 reservation = false",
    "RUNTIME_HAZARD_NO_SCIENTIFIC_TCD",
    "INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION",
    "canonical STATE admission = PENDING",
    "whole-model STATE claim = false",
    "EXACT",
):
    if token not in narrative:
        fail(f"narrative missing required token: {token}")

allowed = {
    "docs/b3/POST_STATEQ02_INCREMENTAL_STATE_INTAKE.md",
    "integration/animo-b3/B3I04_STATEQ02_FINDING_CROSSWALK.csv",
    "integration/animo-b3/B3I04_TCD_RESERVATIONS.json",
    "integration/animo-b3/ANIMO-B3I04_STATUS.json",
    "tools/b3i04/validate_b3i04.py",
    ".github/workflows/animo-b3i04-stateq02-intake.yml",
}
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
if "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" in changed:
    fail("canonical register changed")
if any(x.startswith("src/") or x.startswith("reference/") for x in changed):
    fail("production source or frozen reference changed")

print("PASS B3I04 STATEQ02 incremental state intake validation")
print(f"status={status['status']}")
print(f"crosswalk_rows={len(rows)}")
print("new_tcd_reservations=0")
print("canonical_tail=TCD-042")
print(f"changed_files={len(changed)}")
