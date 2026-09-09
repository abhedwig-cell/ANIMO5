#!/usr/bin/env python3
"""Fail-closed validator for B3I02 Supplement 01 TCD-042 canonical registration."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROW_PATH = ROOT / "integration/animo-b3/B3I02_REGISTER_APPEND_SUPPLEMENT_01_ROWS.csv"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3I02_SUPPLEMENT_01_STATUS.json"
REGISTER_PATH = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
RECON_PATH = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_B3I02_SUPPLEMENT_01_RECONCILIATION.json"
BASE_HEAD = "4da9ec0af5ccb902e456c861a548afa00bd43c2a"
REGISTER_REL = "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"

PRE_STATUS = "IN_PROGRESS_APPEND_ROW_FROZEN_COLLISION_SCAN_PASS_REGISTER_NOT_YET_MODIFIED"
APPENDED_STATUS = "IN_PROGRESS_REGISTER_APPENDED_EXACT_BYTE_TRANSFORM_PENDING_CLOSEOUT"
FINAL_STATUS = "QUALIFIED_TCD042_CANONICAL_REGISTRATION_NO_ADMISSION"
EXPECTED_ATOMICITY = "ONE_ZERO_TOP_THROUGHFLOW_EXTERNAL_N_INPUT_STATE_TRANSFER_SEAM_MULTI_SPECIES_SCOPE"
EXPECTED_CLASS = "RESERVED_POST_B3I02_ZERO_THROUGHFLOW_EXTERNAL_N_INPUT_STATE_TRANSFER_GAP"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"B3I02-SUP01 validation failed: {message}")


def load_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def base_register_bytes() -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE_HEAD}:{REGISTER_REL}"], cwd=ROOT)


def expected_registered_bytes(base: bytes) -> bytes:
    prepared = ROW_PATH.read_bytes().splitlines()
    require(len(prepared) == 2, "prepared-row CSV must contain exactly header plus one row")
    row = prepared[1]
    delimiter = b"" if base.endswith(b"\n") else b"\n"
    return base + delimiter + row + b"\n"


def main() -> None:
    status = load_json(STATUS_PATH)
    rows = load_csv(ROW_PATH)
    register = load_csv(REGISTER_PATH)

    require(status["work_unit"] == "ANIMO-B3I02-SUPPLEMENT-01", "wrong work unit")
    require(status["target"] == "TCD-042", "wrong target")
    require(status["base"]["head"] == BASE_HEAD, "wrong B3I02 base head")
    require(status["source_finding"]["head"] == "56a11b524d03c33ee4ab9b1cd13b2cd523d543fc", "wrong MASSQ02 head")
    require(status["source_finding"]["record"] == "R016", "wrong MASSQ02 record")
    require(status["atomicity"] == EXPECTED_ATOMICITY, "atomicity drift")
    require(status["admission_boundary"]["scientific_admission"] is False, "scientific admission recorded")
    require(status["admission_boundary"]["corrected_legacy_admission"] is False, "corrected-legacy admission recorded")
    require(status["admission_boundary"]["b3_baseline_established"] is False, "B3 baseline recorded")
    require(status["admission_boundary"]["production_migration_admitted"] is False, "production migration recorded")
    require(status["admission_boundary"]["correction_semantics_selected"] is False, "correction semantics selected during registration")

    require(len(rows) == 1, f"expected one prepared row, found {len(rows)}")
    row = rows[0]
    require(row["ID"] == "TCD-042", "prepared row ID mismatch")
    require(row["classification"] == EXPECTED_CLASS, "prepared row classification mismatch")
    require(row["status"] == "OPEN", "prepared row status must be OPEN")
    require("MASSQ02 R016" in row["evidence"], "prepared row lacks MASSQ02 R016 evidence binding")
    require("without admission" in row["decision"], "prepared row does not preserve no-admission boundary")

    ids = [item["ID"] for item in register]
    require(len(ids) == len(set(ids)), "duplicate canonical TCD ID")
    require("TCD-041" in ids, "register lacks TCD-041")
    tcd42_count = ids.count("TCD-042")
    require(tcd42_count in {0, 1}, f"unexpected TCD-042 multiplicity: {tcd42_count}")

    base_bytes = base_register_bytes()
    current_bytes = REGISTER_PATH.read_bytes()
    require(not base_bytes.endswith(b"\n"), "expected base register to retain historical missing final newline")

    if tcd42_count == 0:
        require(status["status"] == PRE_STATUS, "register is pre-append but status is not pre-append")
        require(current_bytes == base_bytes, "pre-append register bytes differ from B3I02 base")
        require(status["tested"] is False and status["qualified"] is False, "pre-append state cannot claim tested/qualified")
        require(status["work_unit_complete"] is False, "pre-append state cannot be complete")
        print("ANIMO-B3I02-SUP01 validation: PASS_PRE_APPEND")
        print("canonical_register_tail=TCD-041")
        print("prepared_row=TCD-042")
        return

    require(ids[-1] == "TCD-042", "TCD-042 is present but is not the canonical tail")
    canonical = next(item for item in register if item["ID"] == "TCD-042")
    require(canonical == row, "canonical TCD-042 row differs from frozen prepared row")
    require(current_bytes == expected_registered_bytes(base_bytes), "register bytes are not exact base bytes plus delimiter plus frozen TCD-042 row")
    require(status["status"] in {APPENDED_STATUS, FINAL_STATUS}, "appended register has invalid status")

    if status["status"] == APPENDED_STATUS:
        require(status["tested"] is False and status["qualified"] is False, "interim appended state cannot claim qualification")
        require(status["work_unit_complete"] is False, "interim appended state cannot be complete")
        print("ANIMO-B3I02-SUP01 validation: PASS_APPENDED_PENDING_CLOSEOUT")
        print("byte_transform=EXACT_BASE_PLUS_NEWLINE_PLUS_TCD042_ROW")
        return

    require(status["tested"] is True and status["qualified"] is True, "final state must be tested and qualified")
    require(status["work_unit_complete"] is True, "final state must be complete")
    require(RECON_PATH.exists(), "final state lacks append reconciliation artifact")
    recon = load_json(RECON_PATH)
    reg = recon["canonical_register"]
    require(reg["tail_before"] == "TCD-041" and reg["tail_after"] == "TCD-042", "reconciliation tail mismatch")
    require(reg["append_only_semantic"] is True, "reconciliation does not assert semantic append-only")
    require(reg["existing_content_bytes_preserved_as_prefix"] is True, "reconciliation does not preserve existing register content bytes")
    require(reg["terminal_newline_normalized"] is True, "historical EOF newline normalization not recorded")
    require(reg["semantic_rows_added"] == 1, "semantic row-add count mismatch")
    require(reg["git_compare_additions"] == 2 and reg["git_compare_deletions"] == 1, "Git numstat must record the no-EOF-newline artifact")
    require(reg["exact_byte_transform_verified"] is True, "exact byte transform not recorded")
    require(recon["registered_not_admitted"] == ["TCD-042"], "reconciliation admission boundary mismatch")
    require(recon["admission_state"]["new_corrections_admitted"] is False, "reconciliation admits correction")
    require(recon["admission_state"]["production_migration_admitted"] is False, "reconciliation admits production migration")
    require(recon["admission_state"]["evidence_strength_increased_by_register_append"] is False, "registration incorrectly increases evidence strength")

    print("ANIMO-B3I02-SUP01 validation: PASS_REGISTERED")
    print("canonical_register_tail=TCD-042")
    print("semantic_rows_added=1")
    print("git_numstat=+2/-1_due_to_historical_missing_EOF_newline")
    print("registered_not_admitted=TCD-042")


if __name__ == "__main__":
    main()
