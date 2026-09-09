#!/usr/bin/env python3
"""Validate ANIMO-B3A01 TCD-027 Class A readiness evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "integration/animo-b3/TCD027_CLASS_A_READINESS.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3A01_STATUS.json"
CLASSIFICATION = ROOT / "integration/animo-b3/B3_EXISTING_TCD_CLASSIFICATION.csv"
PREP06 = ROOT / "integration/animo-prep/PREP06_ORGANIC_P_DETAILED_ACCUMULATOR_DEFECT.json"
FRAMEWORK_STATUS = ROOT / "integration/animo-b3/ANIMO-B3Q01_STATUS.json"

SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
DOC_SHA = "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    readiness = load_json(READINESS)
    status = load_json(STATUS)
    prep06 = load_json(PREP06)
    framework = load_json(FRAMEWORK_STATUS)

    require(readiness["work_unit"] == "ANIMO-B3A01", "wrong work unit")
    require(readiness["tcd_id"] == "TCD-027", "wrong TCD")
    require(readiness["qualification_class"] == "A", "TCD-027 readiness must be Class A")
    require(readiness["record_type"] == "B3_ADMISSION_READINESS_NOT_DISPOSITION", "readiness must not masquerade as disposition")
    require(readiness["admitted"] is False, "B3A01 must not admit TCD-027")
    require(readiness["admission_record_created"] is False, "B3A01 must not create an admission record before route availability")
    require(readiness["current_disposition"] == "UNRESOLVED_NOT_ADMITTED", "current disposition must remain unresolved")

    b0 = readiness["b0"]
    require(b0["source_sha256"] == SOURCE_SHA, "source identity mismatch")
    require(b0["testbank_sha256"] == TESTBANK_SHA, "testbank identity mismatch")
    require(b0["documentation_sha256"] == DOC_SHA, "documentation identity mismatch")
    require(b0["documentation_exact_revision53_authority"] is False, "must not overstate documentation authority")

    require(readiness["b1"]["status"] == "DIAGNOSTIC_NOT_REFERENCE", "B1 role must remain diagnostic")
    require(readiness["b1"]["historical_reference_implied"] is False, "B1 must not imply B2")
    require(readiness["b1"]["evidence_blob_sha"] == "5bc14b350b1b60f870ab568d4c8a127275ca8a84", "PREP06 evidence blob binding mismatch")

    b2 = readiness["b2"]
    require(b2["status"] == "NOT_ESTABLISHED", "B2 must remain unavailable")
    require(b2["normal_route_available"] is False, "normal route must be blocked")
    require(b2["historical_uncertainty_route_precondition_met"] is False, "fallback cannot be invoked yet")

    require(prep06["reserved_discrepancy_id"] == "TCD-027", "PREP06 evidence TCD mismatch")
    require(prep06["corrected_legacy_class"] == "A_ACCOUNTING_ONLY_DETAILED_TRANSFER_REPORTING", "PREP06 class mismatch")
    require(prep06["source"]["legacy_expression"] == readiness["source_claim"]["legacy_expression"], "legacy expression mismatch")
    require(prep06["source"]["correct_expression_probe"] == readiness["source_claim"]["candidate_probe_expression"], "probe expression mismatch")

    obs = readiness["observed_b1_difference"]
    require(obs["legacy_redis_EXP_kg_ha_p"] == prep06["natural_case"]["legacy_redis_EXP_kg_ha_p"], "legacy redis_EXP mismatch")
    require(obs["probe_redis_EXP_kg_ha_p"] == prep06["natural_case"]["probe_redis_EXP_kg_ha_p"], "probe redis_EXP mismatch")
    require(obs["changed_output_count"] == 3, "unexpected changed output count")
    require(sorted(obs["changed_outputs"]) == sorted(prep06["non_interference"]["changed_outputs"]), "changed output whitelist mismatch")

    ni = readiness["class_a_non_interference"]
    require(ni["physical_state_trajectory_unchanged"] is True, "Class A requires unchanged state")
    require(ni["process_flux_trajectory_unchanged"] is True, "Class A requires unchanged flux")
    require(ni["total_organic_p_balance_outputs_changed"] is False, "total organic-P balance must remain unchanged")
    require(ni["total_mass_balance_changed"] is False, "total mass balance must remain unchanged")
    require(ni["ordinary_state_or_process_outputs_changed"] is False, "ordinary state/process outputs must remain unchanged")
    require(ni["sufficient_for_b3_admission"] is False, "B1 non-interference must not be declared admission-sufficient")

    require(readiness["gates"]["b2_route"] == "BLOCKED", "B2 gate must fail closed")
    require(readiness["gates"]["historical_uncertainty_fallback"] == "NOT_ELIGIBLE_YET", "fallback eligibility mismatch")
    require(readiness["gates"]["independent_review"] == "PENDING", "independent review must remain pending")
    require(readiness["gates"]["b3_admission"] == "FAIL_CLOSED_NOT_ADMITTED", "B3 admission must be fail-closed")
    require(readiness["production_migration"] == "NOT_ADMITTED", "production migration must remain blocked")

    with CLASSIFICATION.open(newline="", encoding="utf-8") as handle:
        rows = {row["tcd_id"]: row for row in csv.DictReader(handle)}
    require("TCD-027" in rows, "TCD-027 missing from B3Q01 classification")
    row = rows["TCD-027"]
    require(row["provisional_class"] == "A", "B3Q01 classification disagrees with readiness")
    require(row["admitted"].lower() == "false", "B3Q01 must not have pre-admitted TCD-027")

    require(framework["decision"] == "QUALIFIED_B3_SCIENTIFIC_ADMISSION_FRAMEWORK_NO_LEGACY_CORRECTIONS_ADMITTED", "wrong framework base status")
    require(framework["corrected_legacy_admitted"] is False, "framework must admit no corrections")

    require(status["target_tcd"] == "TCD-027", "status target mismatch")
    require(status["corrected_legacy_admitted"] is False, "status must not admit correction")
    require(status["production_migration_admitted"] is False, "status must not admit production migration")

    print("ANIMO-B3A01 TCD-027 Class A readiness validation: PASS")


if __name__ == "__main__":
    main()
