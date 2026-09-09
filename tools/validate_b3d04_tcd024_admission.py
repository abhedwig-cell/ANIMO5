#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMISSION = ROOT / "integration/animo-b3/TCD024_B3_ADMISSION_CLOSEOUT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D04_STATUS.json"
DOC = ROOT / "docs/b3/TCD024_B3_ADMISSION_CLOSEOUT.md"

EXPECTED_B3D03 = "a3e194573b3a7ce95d5ef15fc179ddb3a613d8a6"
EXPECTED_REVIEW = "b36aedb4406c3f92d6ee7cd2fa4231ed872620ec"
EXPECTED_GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_READINESS = "446f57f3aeff6e7db56ce473f0724bdb58cad94f"
EXPECTED_ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
EXPECTED_DECISION = "ADMIT_TCD024_ATOMIC_CLASS_B_SCIENTIFIC_INDEX_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D04: " + msg)


def main():
    admission = json.loads(ADMISSION.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(admission["record_id"] == "B3D04-TCD024-GOV03-ADMISSION", "record id")
    require(admission["tcd_ids"] == ["TCD-024"], "atomic TCD identity")
    require(admission["atomicity"] == "ATOMIC", "atomicity")
    require(admission["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "Class-B identity")
    require(admission["admission_route"] == EXPECTED_ROUTE, "route")
    require(admission["disposition"] == EXPECTED_DISPOSITION, "disposition")

    auth = admission["authorities"]
    require(auth["B3D03"] == EXPECTED_B3D03, "B3D03 authority")
    require(auth["B3B03"] == EXPECTED_READINESS, "B3B03 authority")
    require(auth["B3B03R"] == EXPECTED_REVIEW, "review authority")
    require(auth["GOV03"] == EXPECTED_GOV03, "GOV03 authority")

    scope = admission["scope"]
    require(scope["legacy_expression"] == "Yy = One + Parcxsl(3,I) * Avc", "legacy expression")
    require(scope["candidate_atomic_correction"] == "Yy = One + Parcxsl(3,J) * Avc", "candidate expression")

    require(admission["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 status")
    require(EXPECTED_GOV03 in admission["identities"]["b2"]["acquisition_effort_ref"], "GOV03 acquisition ref")

    review = admission["evidence"]["independent_review"]
    require(review["status"] == "COMPLETE", "review complete")
    require(review["result"] == "PASS", "review PASS")
    require(review["independent_from_correction_authoring"] is True, "separate authoring context")
    require(EXPECTED_REVIEW in review["reviewer_or_workunit"], "review head pinned")
    require(review["workflow_run"] == 34396595546, "review workflow run")
    require("no organizational or human independence claimed" in review["scope"], "independence boundary")

    coverage = admission["evidence"]["coverage"]
    require(coverage["natural_positive_Optcxsl2_activation"] is False, "natural positive limitation")
    require(coverage["natural_negative_control"] == "PASS", "natural negative control")
    require(coverage["synthetic_active_unequal_site_discriminator"] == "PASS", "synthetic positive discriminator")
    require(coverage["inactive_site_control"] == "PASS_EXACT", "inactive site control")

    hist = admission["evidence"]["historical_uncertainty"]
    require(hist["historical_prevalence"] == "UNKNOWN", "historical prevalence remains unknown")
    require("unknown" in hist["uncertainty_statement"].lower(), "historical uncertainty explicit")

    gates = admission["gates"]
    expected_gates = {
        "b0_identity", "b1_evidence", "b2_route", "theory_or_exact_identity",
        "causal", "conservation", "expected_difference", "non_interference",
        "coverage", "independent_review", "residual_uncertainty", "class_specific",
        "composition_if_applicable"
    }
    require(set(gates) == expected_gates, "complete gate set")
    require(all(v["status"] == "PASS" for v in gates.values()), "all gates PASS")
    require(gates["composition_if_applicable"]["applicability"] == "NOT_APPLICABLE", "composition not applicable")
    require(gates["coverage"]["applicability"] == "APPLICABLE_WITH_EXPLICIT_LIMITATION", "coverage limitation retained")

    unchanged = set(admission["evidence"]["expected_difference"]["required_unchanged"])
    required_unchanged = {
        "TCD-019 fast-sorption finite-change policy",
        "TCD-019 C_unl stopping or convergence policy",
        "all solver tolerances and clipping thresholds",
        "Optcxsl=3 Freundlich slow-sorption route",
        "hydrological forcing, hydrological states and water fluxes",
    }
    require(required_unchanged.issubset(unchanged), "non-interference whitelist")

    require(admission["composition"]["is_composition"] is False, "no composition")
    require(admission["composition"]["component_record_ids"] == [], "no composition components")

    decision = admission["admission_decision"]
    require(decision["admitted"] is True, "admission true")
    require(decision["decision"] == EXPECTED_DECISION, "bounded admission decision")
    require(decision["production_patch_authorized"] is False, "no production patch")
    require(decision["production_migration_admitted"] is False, "no production migration")

    require(status["base"]["head"] == EXPECTED_B3D03, "status B3D03 base")
    require(status["review_authority"]["head"] == EXPECTED_REVIEW, "status review head")
    require(status["review_authority"]["result"] == "PASS", "status review PASS")
    require(status["admission_route"] == EXPECTED_ROUTE, "status route")
    require(status["intended_final_disposition"] == EXPECTED_DISPOSITION, "status disposition")
    require(all(v is False for v in status["hard_boundaries"].values()), "hard boundaries false")

    require("Historical revision-53 prevalence" in doc, "doc historical uncertainty")
    require("does **not** authorize" in doc, "doc non-admission boundaries")

    if status["work_status"]["qualified"]:
        require(status["state"] == "QUALIFIED_TCD024_ATOMIC_B3_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_NO_PRODUCTION_MIGRATION", "qualified state")
        require(status["decision"] == EXPECTED_DECISION, "qualified decision")
        require(status["admission"]["scientific_b3_admission_qualified"] is True, "qualified admission flag")
        require(status["work_status"]["tested"] is True, "qualified tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_B3D04_TCD024_ADMISSION")


if __name__ == "__main__":
    main()
