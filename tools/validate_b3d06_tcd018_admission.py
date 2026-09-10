#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMISSION = ROOT / "integration/animo-b3/TCD018_B3_ADMISSION_CLOSEOUT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D06_STATUS.json"
DOC = ROOT / "docs/b3/TCD018_B3_ADMISSION_CLOSEOUT.md"

EXPECTED_B3D05 = "2f06cc86225637f8dadfdd969fe48dcf851b9ee2"
EXPECTED_REMEDIATION = "4c92b27ed5bbcaadb0e703e622e8c3f690458fa8"
EXPECTED_REVIEW = "fc4a53c2e2e32dee27062959c7ecba7b605cf398"
EXPECTED_GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
EXPECTED_DECISION = "ADMIT_TCD018_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
EXPECTED_REVIEW_RESULT = "PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_READINESS_REVIEW"
EXPECTED_REVIEW_RUN = 34443743545
EXPECTED_PREVIOUS_FAIL = "FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW"
EXPECTED_WHITELIST = {
    "ani_waGP.Bal", "ani_waRP.Bal", "ani_waTP.Bal",
    "bawaGP.Out", "bawaRP.Out", "bawaTP.Out",
}


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D06: " + msg)


def main():
    admission = json.loads(ADMISSION.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(admission["record_id"] == "B3D06-TCD018-GOV03-ADMISSION", "record id")
    require(admission["tcd_ids"] == ["TCD-018"], "atomic TCD identity")
    require(admission["atomicity"] == "ATOMIC", "atomicity")
    require(admission["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "Class-A identity")
    require(admission["admission_route"] == EXPECTED_ROUTE, "route")
    require(admission["disposition"] == EXPECTED_DISPOSITION, "disposition")

    auth = admission["authorities"]
    require(auth["B3D05"] == EXPECTED_B3D05, "B3D05 authority")
    require(auth["B3A03E"] == EXPECTED_REMEDIATION, "B3A03E authority")
    require(auth["B3A03R2"] == EXPECTED_REVIEW, "R2 review authority")
    require(auth["GOV03"] == EXPECTED_GOV03, "GOV03 authority")
    require(auth["B3Q01"] == EXPECTED_B3Q01, "B3Q01 authority")

    scope = admission["scope"]
    require("Sict-Sic" in scope["claim"], "Sic/Sict claim")
    require(scope["candidate_accounting_relation"] == "Bawa_Ddev_corrected = Bawa_Ddev_legacy - sum((Sict-Sic)*1000) over the active reporting period/control volume", "candidate accounting relation")

    require(admission["identities"]["b0"]["source_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "B0 source hash")
    require(admission["identities"]["b0"]["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "B0 testbank hash")
    require(admission["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 status")
    require(EXPECTED_GOV03 in admission["identities"]["b2"]["acquisition_effort_ref"], "GOV03 acquisition ref")

    review = admission["evidence"]["independent_review"]
    require(review["status"] == "COMPLETE", "review complete")
    require(review["result"] == EXPECTED_REVIEW_RESULT, "R2 review PASS")
    require(review["independent_from_correction_authoring"] is True, "separate authoring context")
    require(EXPECTED_REVIEW in review["reviewer_or_workunit"], "review head pinned")
    require(review["final_workflow_run"] == EXPECTED_REVIEW_RUN, "review workflow run")
    require(review["previous_fail_retained"] == EXPECTED_PREVIOUS_FAIL, "previous FAIL retained")
    require("no organizational or human independence claimed" in review["scope"], "independence boundary")

    coverage = admission["evidence"]["coverage"]
    require(coverage["natural_LWKM_activation"] is True, "natural LWKM activation")
    require(coverage["period_reconciliation_rows"] == 25, "25 period rows")
    require(coverage["detailed_hydrology_probe_records"] == 900, "900 hydrology records")
    require(coverage["isolated_cases"] == 8, "8 cases")
    require(coverage["baseline_candidate_run_records"] == 16, "16 run records")
    require(coverage["output_digest_rows"] == 376, "376 digest rows")
    require(coverage["raw_equal"] == 270, "270 raw equal")
    require(coverage["equal_after_declared_volatile_normalization_only"] == 100, "100 normalized equal")
    require(coverage["whitelisted_differences"] == 6, "6 whitelist differences")
    require(coverage["unexpected_differences"] == 0, "0 unexpected")
    require(coverage["missing_or_extra"] == 0, "0 missing extra")

    expected = admission["evidence"]["expected_difference"]
    require(set(expected["changed_surfaces"]) == EXPECTED_WHITELIST, "exact six-output whitelist")
    unchanged = set(expected["required_unchanged"])
    for item in {
        "Sic and Sict physical trajectories",
        "all hydrological states",
        "all hydrological and management/process fluxes",
        "interception physics",
        "state-promotion semantics",
        "all non-water reporting families",
    }:
        require(item in unchanged, "required unchanged: " + item)

    ni = admission["evidence"]["non_interference"]
    require(ni["candidate_assigns_Sic_or_Sict"] is False, "candidate does not write Sic/Sict")
    require(ni["candidate_modifies_hydrology_or_process_flux_assignment"] is False, "candidate does not modify hydrology/process flux assignments")
    require(ni["output_equality_used_as_sole_state_or_flux_proof"] is False, "state/flux not inferred from output equality alone")
    require(set(ni["candidate_added_writes"]) == {"Tcd018IcCu reporting accumulator", "Bawa(Ddev) reporting deviation"}, "bounded added write set")

    hist = admission["evidence"]["historical_uncertainty"]
    require(hist["historical_revision53_behaviour"] == "UNKNOWN", "historical behaviour UNKNOWN")
    require(hist["qualified_B2_exists"] is False, "no qualified B2")

    residual = admission["evidence"]["residual_boundary"]
    require(residual["LWKM_approximately_0_0601_mm"] == "CAUSAL_EVIDENCE_NOT_TOLERANCE", "0.0601 not tolerance")
    require(residual["MASSQ01_CranGrass_TITO724_mm"] == -0.0030198960466805147, "MASSQ01 residual retained")
    require(residual["MASSQ01_CranGrass_TITO724_class"] == "UNEXPLAINED_RESIDUAL_OUTSIDE_TCD018", "MASSQ01 residual class")
    require(residual["global_water_closure_claimed"] is False, "no global water closure")

    gates = admission["gates"]
    expected_gates = {
        "b0_identity", "b1_evidence", "b2_route", "theory_or_exact_identity",
        "causal", "conservation", "expected_difference", "non_interference",
        "coverage", "independent_review", "residual_uncertainty", "class_specific",
        "composition_if_applicable"
    }
    require(set(gates) == expected_gates, "complete gate set")
    require(all(v["status"] == "PASS" for v in gates.values()), "all admission gates PASS")
    require(gates["composition_if_applicable"]["applicability"] == "NOT_APPLICABLE", "composition not applicable")

    require(admission["composition"]["is_composition"] is False, "no composition")
    require(admission["composition"]["component_record_ids"] == [], "no composition components")

    decision = admission["admission_decision"]
    require(decision["admitted"] is True, "admission true")
    require(decision["decision"] == EXPECTED_DECISION, "bounded admission decision")
    require(decision["historical_fidelity_claimed"] is False, "no historical fidelity")
    require(decision["global_water_closure_claimed"] is False, "no global closure")
    require(decision["production_patch_authorized"] is False, "no production patch")
    require(decision["production_migration_admitted"] is False, "no production migration")
    require(decision["b4_admitted"] is False, "no B4")

    require(status["base"]["head"] == EXPECTED_B3D05, "status B3D05 base")
    require(status["review_authority"]["head"] == EXPECTED_REVIEW, "status review head")
    require(status["review_authority"]["result"] == EXPECTED_REVIEW_RESULT, "status review PASS")
    require(status["review_authority"]["workflow_run"] == EXPECTED_REVIEW_RUN, "status review workflow")
    require(status["evidence_remediation_authority"]["head"] == EXPECTED_REMEDIATION, "status remediation head")
    require(status["admission_route"] == EXPECTED_ROUTE, "status route")
    require(status["intended_final_disposition"] == EXPECTED_DISPOSITION, "status disposition")
    require(all(v is False for v in status["hard_boundaries"].values()), "hard boundaries false")

    require("does **not** authorize" in doc, "doc non-authorization boundary")
    require("Historical revision-53 behaviour" in doc, "doc historical uncertainty")
    require("UNEXPLAINED_RESIDUAL" in doc, "doc unrelated residual retained")

    if status["work_status"]["qualified"]:
        require(status["state"] == "QUALIFIED_TCD018_ATOMIC_B3_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_NO_PRODUCTION_MIGRATION", "qualified state")
        require(status["decision"] == EXPECTED_DECISION, "qualified decision")
        require(status["admission"]["scientific_b3_admission_qualified"] is True, "qualified admission flag")
        require(status["project_effect"]["tcd018_atomic_b3_scientific_admission"] is True, "project effect admitted")
        require(status["work_status"]["tested"] is True, "qualified tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_B3D06_TCD018_ADMISSION")


if __name__ == "__main__":
    main()
