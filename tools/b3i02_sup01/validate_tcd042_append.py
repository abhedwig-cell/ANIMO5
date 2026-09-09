#!/usr/bin/env python3
"""Fail-closed validator for B3I02 Supplement 01 TCD-042 canonical registration."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROW_PATH = ROOT / "integration/animo-b3/B3I02_REGISTER_APPEND_SUPPLEMENT_01_ROWS.csv"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3I02_SUPPLEMENT_01_STATUS.json"
REGISTER_PATH = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
RECON_PATH = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_B3I02_SUPPLEMENT_01_RECONCILIATION.json"

PRE_STATUS = "IN_PROGRESS_APPEND_ROW_FROZEN_COLLISION_SCAN_PASS_REGISTER_NOT_YET_MODIFIED"
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


def main() -> None:
    status = load_json(STATUS_PATH)
    rows = load_csv(ROW_PATH)
    register = load_csv(REGISTER_PATH)

    require(status["work_unit"] == "ANIMO-B3I02-SUPPLEMENT-01", "wrong work unit")
    require(status["target"] == "TCD-042", "wrong target")
    require(status["base"]["head"] == "4da9ec0af5ccb902e456c861a548afa00bd43c2a", "wrong B3I02 base head")
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

    if tcd42_count == 0:
        require(status["status"] == PRE_STATUS, "register is pre-append but status is not pre-append")
        require(status["tested"] is False and status["qualified"] is False, "pre-append state cannot claim tested/qualified")
        require(status["work_unit_complete"] is False, "pre-append state cannot be complete")
        require(status["planned_append"]["expected_tail_after"] == "TCD-042", "planned tail mismatch")
        require(status["planned_append"]["expected_compare_additions"] == 1, "planned additions mismatch")
        require(status["planned_append"]["expected_compare_deletions"] == 0, "planned deletions mismatch")
        print("ANIMO-B3I02-SUP01 validation: PASS_PRE_APPEND")
        print("canonical_register_tail=TCD-041")
        print("prepared_row=TCD-042")
        return

    require(ids[-1] == "TCD-042", "TCD-042 is present but is not the canonical tail")
    canonical = next(item for item in register if item["ID"] == "TCD-042")
    require(canonical == row, "canonical TCD-042 row differs from frozen prepared row")
    require(status["status"] == FINAL_STATUS, "appended register requires final qualified status")
    require(status["tested"] is True and status["qualified"] is True, "final state must be tested and qualified")
    require(status["work_unit_complete"] is True, "final state must be complete")
    require(RECON_PATH.exists(), "final state lacks append reconciliation artifact")
    recon = load_json(RECON_PATH)
    reg = recon["canonical_register"]
    require(reg["tail_before"] == "TCD-041" and reg["tail_after"] == "TCD-042", "reconciliation tail mismatch")
    require(reg["append_only"] is True, "reconciliation does not assert append-only")
    require(reg["existing_rows_changed"] is False, "reconciliation says existing rows changed")
    require(reg["compare_additions"] == 1 and reg["compare_deletions"] == 0, "reconciliation diff is not +1/-0")
    require(recon["registered_not_admitted"] == ["TCD-042"], "reconciliation admission boundary mismatch")
    require(recon["admission_state"]["new_corrections_admitted"] is False, "reconciliation admits correction")
    require(recon["admission_state"]["production_migration_admitted"] is False, "reconciliation admits production migration")
    require(recon["admission_state"]["evidence_strength_increased_by_register_append"] is False, "registration incorrectly increases evidence strength")

    print("ANIMO-B3I02-SUP01 validation: PASS_REGISTERED")
    print("canonical_register_tail=TCD-042")
    print("registered_not_admitted=TCD-042")


if __name__ == "__main__":
    main()
