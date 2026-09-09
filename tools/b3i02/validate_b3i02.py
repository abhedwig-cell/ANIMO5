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

FINAL_STATUS = "QUALIFIED_INCREMENTAL_CANONICAL_DISCREPANCY_INTAKE_NO_ADMISSIONS"
INTERIM_STATUS = "IN_PROGRESS_MASSQ02_SUPPLEMENT_PERSISTED_PENDING_VALIDATION"
RG03_HEAD = "b67a6cac325fe3f838aedc9df106e120fd5a3d0f"
MASSQ02_HEAD = "56a11b524d03c33ee4ab9b1cd13b2cd523d543fc"
STATEQ02_HEAD = "0875f7f5c0976f8b0b3ae70d00fd2f48b31697d5"
TCD042_ATOMICITY = "ONE_ZERO_TOP_THROUGHFLOW_EXTERNAL_N_INPUT_STATE_TRANSFER_SEAM_MULTI_SPECIES_SCOPE"


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
    require(status["status"] in {INTERIM_STATUS, FINAL_STATUS}, "unexpected workunit status")
    require(status["scope"]["incremental_only"] is True, "incremental-only guard missing")
    require(status["scope"]["admission_allowed"] is False, "admission must remain forbidden")
    require(status["scope"]["source_localization_not_sufficient_without_atomic_identity"] is True, "causality/atomicity guard missing")
    require(status["scientific_admission_performed"] is False, "scientific admission recorded")
    require(status["corrected_legacy_admission_performed"] is False, "corrected-legacy admission recorded")
    require(status["production_migration_admitted"] is False, "production migration recorded")
    require(status["production_code_modified"] is False, "production code modification recorded")

    canonical = status["canonical_results"]
    require(canonical["new_tcd_reservations"] == ["TCD-042"], "status must reserve exactly TCD-042")
    require(canonical["new_child_atoms"] == [], "status contains unexpected child atoms")
    require(canonical["canonical_register_append_required"] is True, "TCD-042 append must remain required")
    require(canonical["canonical_register_append_performed"] is False, "TCD-042 must not already be appended in reservation checkpoint")
    require(canonical["canonical_register_tail_remains"] == "TCD-041", "canonical tail must remain TCD-041 before append")

    completed = {item["work_unit"]: item for item in status["post_b3i01_completed_incremental_evidence"]}
    require(set(completed) == {"ANIMO-STATEQ01", "ANIMO-RG03", "ANIMO-MASSQ02"}, "completed incremental evidence set mismatch")

    rg03 = completed["ANIMO-RG03"]
    require(rg03["head"] == RG03_HEAD, "RG03 closeout head mismatch")
    require(rg03["disposition"] == "GOVERNANCE_RECONCILIATION_NO_NEW_DISCREPANCY", "RG03 was promoted into a discrepancy")
    require(rg03["qualified"] is True and rg03["tested"] is True, "RG03 closeout is not recorded as tested and qualified")
    require(rg03["scientific_admission_performed"] is False, "RG03 scientific admission leaked into B3I02")
    require(rg03["evidence_strength_increased"] is False, "RG03 integration incorrectly increases evidence strength")
    require(rg03["canonical_tcd_register_tail"] == "TCD-041", "RG03 canonical register tail differs from B3I01 authority")
    require(rg03["new_tcd_count"] == 0, "RG03 generated a new TCD in B3I02")

    massq02 = completed["ANIMO-MASSQ02"]
    require(massq02["head"] == MASSQ02_HEAD, "MASSQ02 closeout head mismatch")
    require(massq02["qualified"] is True and massq02["tested"] is True, "MASSQ02 is not recorded as completed qualification evidence")
    require(massq02["mass_admitted"] is False, "MASSQ02 mass admission leaked into B3I02")
    require(massq02["new_causal_findings"] == 15, "MASSQ02 causal finding count mismatch")
    require(massq02["b3i02_new_tcd_reservations"] == ["TCD-042"], "MASSQ02 intake reservation mismatch")
    require(massq02["b3i02_insufficient_identity_count"] == 14, "MASSQ02 insufficient-identity count mismatch")
    require(massq02["scientific_admission_performed"] is False, "MASSQ02 scientific admission recorded")

    excluded = {item["work_unit"]: item for item in status["explicitly_excluded_in_progress_workunits"]}
    require(set(excluded) == {"ANIMO-STATEQ02"}, "in-progress exclusion set must contain only STATEQ02")
    require(excluded["ANIMO-STATEQ02"]["head"] == STATEQ02_HEAD, "STATEQ02 checkpoint head mismatch")

    require(reservations["work_unit"] == "ANIMO-B3I02", "wrong reservation work_unit")
    require(reservations["incremental_refresh"]["head"] == MASSQ02_HEAD, "reservation file MASSQ02 head mismatch")
    require(reservations["collision_scan"]["reservation_created_for_tcd_042"] is True, "TCD-042 must be reserved")
    require(reservations["collision_scan"]["tcd_042_present_in_authoritative_register"] is False, "collision scan says TCD-042 already exists")
    require(reservations["collision_scan"]["tcd_042_found_in_live_b3i_branch_or_commit_collision_scan"] is False, "parallel TCD-042 collision recorded")
    require(len(reservations["reservations"]) == 1, "expected exactly one new reservation")
    tcd42_res = reservations["reservations"][0]
    require(tcd42_res["tcd_id"] == "TCD-042", "wrong reserved TCD ID")
    require(tcd42_res["source_finding"] == "MASSQ02-R016", "TCD-042 source finding mismatch")
    require(tcd42_res["crosswalk_key"] == "MASSQ01-LCL-N006", "TCD-042 crosswalk key mismatch")
    require(tcd42_res["atomicity"] == TCD042_ATOMICITY, "TCD-042 atomicity mismatch")
    require(tcd42_res["species_scope"] == ["NH4-N", "NO3-N"], "TCD-042 species scope mismatch")
    require(tcd42_res["species_specific_tcds_created"] is False, "TCD-042 incorrectly split by species")
    require(tcd42_res["canonical_register_appended"] is False, "reservation claims canonical append")
    require(tcd42_res["admitted"] is False, "reservation claims admission")
    require(reservations["massq02_policy"]["new_tcd_reservations"] == 1, "reservation file new-TCD count mismatch")
    require(reservations["massq02_policy"]["insufficient_identity_or_mechanism_count"] == 14, "reservation file insufficient count mismatch")
    require(reservations["massq02_policy"]["new_child_atoms"] == 0, "reservation file child-atom count mismatch")
    require(reservations["massq02_policy"]["acceptance_epsilon_introduced"] is False, "acceptance epsilon introduced")
    require(reservations["canonical_register_append_required"] is True, "reservation file must require canonical append")
    require(reservations["canonical_register_append_performed"] is False, "reservation file claims canonical append")
    require(reservations["admission_performed"] is False, "reservation file records admission")
    require(reservations["production_change_performed"] is False, "reservation file records production change")

    require(len(crosswalk) == 21, f"expected 21 crosswalk findings, found {len(crosswalk)}")
    keys = [row["finding_key"] for row in crosswalk]
    require(len(keys) == len(set(keys)), "duplicate finding_key in crosswalk")
    require(all(row["admission"] == "NONE" for row in crosswalk), "crosswalk contains an admission")

    mass_rows = [row for row in crosswalk if row["finding_key"].startswith("MASSQ01-LCL-")]
    require(len(mass_rows) == 15, f"expected 15 MASSQ01-origin mass findings, found {len(mass_rows)}")
    require(all(row["source_workunit"] == "ANIMO-MASSQ02" for row in mass_rows), "MASSQ02 closeout not bound to all mass rows")
    reserved_mass = [row for row in mass_rows if row["intake_disposition"] == "NEW_TCD_RESERVED_PENDING_CANONICAL_REGISTER_APPEND"]
    insufficient_mass = [row for row in mass_rows if row["intake_disposition"] == "INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION"]
    require(len(reserved_mass) == 1, f"expected one reserved MASSQ02 finding, found {len(reserved_mass)}")
    require(len(insufficient_mass) == 14, f"expected fourteen insufficient-identity MASSQ02 findings, found {len(insufficient_mass)}")
    require(all(row["intake_disposition"] != "LOCAL_OBSERVER_FINDING_PENDING_CAUSALITY" for row in mass_rows), "stale MASSQ01 pending-causality disposition remains")

    by_key = {row["finding_key"]: row for row in crosswalk}
    tcd42_row = by_key["MASSQ01-LCL-N006"]
    require(tcd42_row["canonical_tcd"] == "TCD-042", "Ruurlo N finding must reserve TCD-042")
    require(tcd42_row["atomicity_or_scope"] == TCD042_ATOMICITY, "Ruurlo TCD-042 atomicity mismatch")
    require(tcd42_row["related_tcd"] == "", "TCD-042 row should not alias an existing TCD")

    layer0 = by_key["RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING"]
    require(layer0["canonical_tcd"] == "TCD-040", "layer-0 restart finding must reuse TCD-040")
    require(layer0["atomicity_or_scope"] == "ONE_CAUSAL_INITIALIZATION_TRANSACTION_MULTI_COORDINATE_SCOPE", "layer-0 atomicity changed")
    flair = by_key["BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED"]
    require(flair["canonical_tcd"] == "TCD-041", "Flair(Nl+1) finding must reuse TCD-041")
    require(flair["atomicity_or_scope"] == "ONE_LOWER_EXTERNAL_AIR_INTERFACE_INITIALIZATION_OMISSION", "Flair atomicity changed")

    state_rows = [row for row in crosswalk if row["finding_key"].startswith("STATEQ01-LCL-EXTCROP-")]
    require(len(state_rows) == 2, f"expected 2 post-cutoff STATEQ01 observations, found {len(state_rows)}")
    require(all(row["intake_disposition"] == "INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION" for row in state_rows), "STATEQ01 behavioural symptom was canonicalized without causality")

    register_ids = [row["ID"] for row in register]
    require(len(register_ids) == len(set(register_ids)), "duplicate canonical TCD ID")
    require("TCD-040" in register_ids, "authoritative register lacks TCD-040")
    require("TCD-041" in register_ids, "authoritative register lacks TCD-041")
    require("TCD-042" not in register_ids, "reservation checkpoint must not append TCD-042 yet")
    numeric_ids = [int(value.split("-")[1]) for value in register_ids if value.startswith("TCD-") and value.split("-")[1].isdigit()]
    require(max(numeric_ids) == 41, f"canonical register tail is not TCD-041: max={max(numeric_ids)}")

    require(FINAL_STATUS in doc, "narrative does not preserve final no-admission status")
    require("`reservations = [TCD-042]`" in doc, "narrative does not state TCD-042 reservation")
    require("NEW_TCD_RESERVED_PENDING_CANONICAL_REGISTER_APPEND" in doc, "narrative does not state TCD-042 pending-append disposition")
    require(MASSQ02_HEAD in doc, "narrative does not bind MASSQ02 closeout head")
    require("Fourteen rows are retained as" in doc, "narrative does not preserve fourteen fail-closed residual dispositions")
    require("GOVERNANCE_RECONCILIATION_NO_NEW_DISCREPANCY" in doc, "narrative does not record RG03 no-discrepancy disposition")
    require(RG03_HEAD in doc, "narrative does not bind RG03 closeout head")

    print("ANIMO-B3I02 validation: PASS")
    print(f"status={status['status']}")
    print(f"crosswalk_findings={len(crosswalk)}")
    print("massq02_new_causal_findings=15")
    print("massq02_reserved_tcd=1:TCD-042")
    print("massq02_pending_atomic_identity=14")
    print("state_pending_causal_isolation=2")
    print("new_child_atoms=0")
    print("canonical_register_tail=TCD-041")
    print("canonical_append_pending=TCD-042")


if __name__ == "__main__":
    main()
