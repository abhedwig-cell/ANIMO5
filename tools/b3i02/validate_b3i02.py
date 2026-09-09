#!/usr/bin/env python3
"""Fail-closed consistency checks for ANIMO-B3I02 governance artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3I02_STATUS.json"
RES_PATH = ROOT / "integration/animo-b3/B3I02_TCD_RESERVATIONS.json"
XWALK_PATH = ROOT / "integration/animo-b3/B3I02_LOCAL_FINDING_CROSSWALK.csv"
REGISTER_PATH = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
DOC_PATH = ROOT / "docs/b3/POST_B3I01_INCREMENTAL_INTAKE.md"

EXPECTED_STATUS = "QUALIFIED_INCREMENTAL_CANONICAL_DISCREPANCY_INTAKE_NO_ADMISSIONS"
RG03_HEAD = "b67a6cac325fe3f838aedc9df106e120fd5a3d0f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"B3I02 validation failed: {message}")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    status = load_json(STATUS_PATH)
    reservations = load_json(RES_PATH)
    crosswalk = load_csv(XWALK_PATH)
    register = load_csv(REGISTER_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")

    require(status["work_unit"] == "ANIMO-B3I02", "wrong status work_unit")
    require(status["status"] == EXPECTED_STATUS, "unexpected workunit status")
    require(status["scope"]["incremental_only"] is True, "incremental-only guard missing")
    require(status["scope"]["admission_allowed"] is False, "admission must remain forbidden")
    require(status["scientific_admission_performed"] is False, "scientific admission recorded")
    require(status["corrected_legacy_admission_performed"] is False, "corrected-legacy admission recorded")
    require(status["production_migration_admitted"] is False, "production migration recorded")
    require(status["production_code_modified"] is False, "production code modification recorded")
    require(status["canonical_results"]["new_tcd_reservations"] == [], "status contains new TCD reservations")
    require(status["canonical_results"]["new_child_atoms"] == [], "status contains new child atoms")
    require(status["canonical_results"]["canonical_register_append_required"] is False, "register append unexpectedly required")
    require(status["canonical_results"]["next_unallocated_candidate_observed_not_reserved"] == "TCD-042", "next unallocated candidate mismatch")

    completed = {item["work_unit"]: item for item in status["post_b3i01_completed_incremental_evidence"]}
    require(set(completed) == {"ANIMO-STATEQ01", "ANIMO-RG03"}, "completed incremental evidence set changed unexpectedly")
    rg03 = completed["ANIMO-RG03"]
    require(rg03["head"] == RG03_HEAD, "RG03 closeout head mismatch")
    require(rg03["disposition"] == "GOVERNANCE_RECONCILIATION_NO_NEW_DISCREPANCY", "RG03 was promoted into a discrepancy")
    require(rg03["qualified"] is True and rg03["tested"] is True, "RG03 closeout is not recorded as tested and qualified")
    require(rg03["scientific_admission_performed"] is False, "RG03 scientific admission leaked into B3I02")
    require(rg03["evidence_strength_increased"] is False, "RG03 integration incorrectly increases evidence strength")
    require(rg03["canonical_tcd_register_tail"] == "TCD-041", "RG03 canonical register tail differs from B3I01 authority")
    require(rg03["new_tcd_count"] == 0, "RG03 generated a new TCD in B3I02")

    excluded = {item["work_unit"] for item in status["explicitly_excluded_in_progress_workunits"]}
    require(excluded == {"ANIMO-MASSQ02", "ANIMO-STATEQ02"}, "in-progress exclusion set changed unexpectedly")
    require("ANIMO-RG03" not in excluded, "completed RG03 remains incorrectly excluded as in progress")

    require(reservations["work_unit"] == "ANIMO-B3I02", "wrong reservation work_unit")
    require(reservations["reservations"] == [], "reservation file must remain empty")
    require(reservations["collision_scan"]["reservation_created_for_tcd_042"] is False, "TCD-042 must not be reserved")
    require(reservations["canonical_register_append_required"] is False, "reservation file requests register append")
    require(reservations["admission_performed"] is False, "reservation file records admission")
    require(reservations["production_change_performed"] is False, "reservation file records production change")

    require(len(crosswalk) == 21, f"expected 21 crosswalk findings, found {len(crosswalk)}")
    keys = [row["finding_key"] for row in crosswalk]
    require(len(keys) == len(set(keys)), "duplicate finding_key in crosswalk")
    require(all(row["admission"] == "NONE" for row in crosswalk), "crosswalk contains an admission")
    require(all(row["canonical_tcd"] != "TCD-042" for row in crosswalk), "crosswalk allocates TCD-042")

    mass_rows = [row for row in crosswalk if row["finding_key"].startswith("MASSQ01-LCL-")]
    require(len(mass_rows) == 15, f"expected 15 MASSQ01 local residual findings, found {len(mass_rows)}")
    require(all(row["intake_disposition"] == "LOCAL_OBSERVER_FINDING_PENDING_CAUSALITY" for row in mass_rows), "a MASSQ01 unexplained residual was over-classified")

    state_rows = [row for row in crosswalk if row["finding_key"].startswith("STATEQ01-LCL-EXTCROP-")]
    require(len(state_rows) == 2, f"expected 2 post-cutoff STATEQ01 observations, found {len(state_rows)}")
    require(all(row["intake_disposition"] == "INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION" for row in state_rows), "STATEQ01 behavioural symptom was canonicalized without causality")

    by_key = {row["finding_key"]: row for row in crosswalk}
    layer0 = by_key["RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING"]
    require(layer0["canonical_tcd"] == "TCD-040", "layer-0 restart finding must reuse TCD-040")
    require(layer0["atomicity_or_scope"] == "ONE_CAUSAL_INITIALIZATION_TRANSACTION_MULTI_COORDINATE_SCOPE", "layer-0 atomicity changed")
    flair = by_key["BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED"]
    require(flair["canonical_tcd"] == "TCD-041", "Flair(Nl+1) finding must reuse TCD-041")
    require(flair["atomicity_or_scope"] == "ONE_LOWER_EXTERNAL_AIR_INTERFACE_INITIALIZATION_OMISSION", "Flair atomicity changed")

    register_ids = [row["ID"] for row in register]
    require(len(register_ids) == len(set(register_ids)), "duplicate canonical TCD ID")
    require("TCD-040" in register_ids, "authoritative register lacks TCD-040")
    require("TCD-041" in register_ids, "authoritative register lacks TCD-041")
    require("TCD-042" not in register_ids, "B3I02 branch unexpectedly contains TCD-042")
    numeric_ids = [int(value.split("-")[1]) for value in register_ids if value.startswith("TCD-") and value.split("-")[1].isdigit()]
    require(max(numeric_ids) == 41, f"canonical register tail is not TCD-041: max={max(numeric_ids)}")

    require(EXPECTED_STATUS in doc, "narrative does not state final status")
    require("`reservations = []`" in doc, "narrative does not state empty reservations")
    require("do not receive `TCD-042`" in doc, "narrative does not preserve fail-closed TCD-042 disposition")
    require("GOVERNANCE_RECONCILIATION_NO_NEW_DISCREPANCY" in doc, "narrative does not record RG03 no-discrepancy disposition")
    require(RG03_HEAD in doc, "narrative does not bind the consumed RG03 closeout head")

    print("ANIMO-B3I02 validation: PASS")
    print(f"crosswalk_findings={len(crosswalk)}")
    print(f"mass_pending_causality={len(mass_rows)}")
    print(f"state_pending_causal_isolation={len(state_rows)}")
    print("rg03_disposition=GOVERNANCE_RECONCILIATION_NO_NEW_DISCREPANCY")
    print("new_tcd_reservations=0")
    print("canonical_register_tail=TCD-041")


if __name__ == "__main__":
    main()
