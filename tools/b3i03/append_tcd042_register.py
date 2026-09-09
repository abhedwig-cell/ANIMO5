#!/usr/bin/env python3
import csv
import hashlib
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
STATUS = ROOT / "integration/animo-b3/B3I03_CANONICAL_REGISTER_APPEND_STATUS.json"
EXPECTED_BEFORE_BLOB = "c057fdc5a9b2199dde07a19f0d70213cfaab235b"
BASE_HEAD = "6a015587807130b4ce12c9f1518c1ddac4e5d624"
HEADER = [
    "ID", "process", "theory", "documentation", "legacy_implementation",
    "ANIMO5_implementation", "difference", "impact", "classification",
    "evidence", "decision", "status"
]
ROW = [
    "TCD-042",
    "upper-boundary precipitation/deposition solute transaction at zero top throughflow",
    "external solute input must either cross the declared system boundary into a represented owner or remain outside until the physical crossing occurs; one accepted interval cannot both book the external input and omit its represented transfer or state ownership",
    "supplied ANIMO 4.0 guide describes precipitation and deposition plus upper-boundary solute routing but exact zero-throughflow transaction ownership semantics are not yet independently qualified",
    "revision-53 UBoundconc zero-throughflow branch uses Flux=0 A1=1 A2=0 and retains previous top concentrations while Outbal_calc books Pr*Coprnhyn and Pr*Coprniyn as external N input; Ruurlo TITO1915 booked total 0.006749373218 kg/ha N matches observer residual 0.0067493732130969875 kg/ha N",
    "not started",
    "accepted-interval external input accounting and represented upper-boundary solute state or transfer semantics disagree at zero throughflow",
    "creates deterministic N nonclosure and leaves boundary-owner semantics unresolved; corrected behaviour may be accounting-only local algebra or missing-state and therefore requires atomization",
    "RESERVED_POST_MASSQ02_UPPER_BOUNDARY_TRANSACTION_OWNERSHIP_GAP_REQUIRES_ATOMIZATION",
    "MASSQ02 R016 and MASSQ02_FINAL_RESIDUAL_PROBE_EVIDENCE.json plus B3I03_MASSQ02_FINDING_CROSSWALK.csv and B3I03_TCD_RESERVATIONS.json",
    "retain frozen behaviour; atomize Class A versus Class C versus possible Class B semantics before any admission; qualify zero and nonzero throughflow with B2 or governed historical-uncertainty route",
    "OPEN",
]


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def fail(msg: str):
    raise SystemExit(f"B3I03 register append failed: {msg}")

before = REGISTER.read_bytes()
before_sha = git_blob_sha(before)
if before_sha != EXPECTED_BEFORE_BLOB:
    fail(f"unexpected register blob before append: {before_sha}")

text = before.decode("utf-8")
reader = list(csv.reader(io.StringIO(text)))
if not reader or reader[0] != HEADER:
    fail("canonical register header changed")
ids = [r[0] for r in reader[1:] if r]
expected_ids = [f"TCD-{i:03d}" for i in range(1, 42)]
if ids != expected_ids:
    fail("pre-append IDs are not exactly TCD-001 through TCD-041")
if any(r and r[0] == "TCD-042" for r in reader):
    fail("TCD-042 already present")
if len(ROW) != len(HEADER):
    fail("TCD-042 row field count mismatch")

out = io.StringIO(newline="")
writer = csv.writer(out, lineterminator="\n")
for r in reader:
    writer.writerow(r)
writer.writerow(ROW)
after_text = out.getvalue()
after = after_text.encode("utf-8")

# csv.writer may quote fields but must preserve the existing logical rows exactly.
after_rows = list(csv.reader(io.StringIO(after_text)))
if after_rows[:-1] != reader:
    fail("pre-existing logical rows changed during append")
if after_rows[-1] != ROW:
    fail("appended row readback mismatch")
if [r[0] for r in after_rows[1:]] != [f"TCD-{i:03d}" for i in range(1, 43)]:
    fail("post-append IDs are not contiguous TCD-001 through TCD-042")

REGISTER.write_bytes(after)
after_sha = git_blob_sha(after)

status = {
    "work_unit": "ANIMO-B3I03",
    "followup": "CANONICAL_REGISTER_APPEND",
    "status": "QUALIFIED_CANONICAL_REGISTER_APPEND_TCD042_NO_ADMISSIONS",
    "decision": "QUALIFIED_CANONICAL_REGISTER_APPEND_TCD042_NO_ADMISSIONS",
    "repository": "abhedwig-cell/ANIMO5",
    "branch": "work/animo-b3i03-canonical-register-append",
    "base_head": BASE_HEAD,
    "registered_ids": ["TCD-042"],
    "canonical_register": {
        "path": "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
        "blob_before": before_sha,
        "blob_after_append": after_sha,
        "tail_before": "TCD-041",
        "tail_after": "TCD-042",
        "append_only": True,
        "preexisting_logical_rows_unchanged": True,
        "contiguous_ids_tcd001_through_tcd042": True,
    },
    "reservation_authority": {
        "branch": "work/animo-b3i03-massq02-causal-intake",
        "head": BASE_HEAD,
        "artifact": "integration/animo-b3/B3I03_TCD_RESERVATIONS.json",
        "reserved_id": "TCD-042",
    },
    "validation": {
        "workflow": ".github/workflows/animo-b3i03-register-append.yml",
        "workflow_run_id": int(os.environ.get("GITHUB_RUN_ID", "0")),
        "workflow_trigger_head": os.environ.get("GITHUB_SHA", "UNKNOWN"),
        "validator_result": "PASS_GENERATION_AND_READBACK",
    },
    "invariants": {
        "register_presence_is_not_b3_admission": True,
        "new_corrections_admitted": False,
        "b3_baseline_established": False,
        "production_migration_admitted": False,
        "production_code_modified": False,
        "source_correction": False,
        "evidence_strength_increased_by_append": False,
        "tcd042_requires_atomization_before_admission": True,
    },
    "tested": True,
    "qualified": True,
    "work_unit_complete": True,
}
STATUS.parent.mkdir(parents=True, exist_ok=True)
STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
print("PASS B3I03 canonical register append")
print(f"before_blob={before_sha}")
print(f"after_blob={after_sha}")
print("tail=TCD-042")
