#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMISSION = ROOT / "integration/animo-b3/TCD017_B3_ADMISSION_CLOSEOUT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D02_STATUS.json"
DOC = ROOT / "docs/b3/TCD017_B3_ADMISSION_CLOSEOUT.md"

EXPECTED_REVIEW_HEAD = "8b38b03ac489c349192ae9fa55a8fe51cea183cb"
EXPECTED_GOV03_HEAD = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_B3D01_HEAD = "6ada2522101587ab74974a70f980b50e64cf9b86"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
EXPECTED_ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D02: " + msg)


def main():
    admission = json.loads(ADMISSION.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(admission["record_id"] == "B3D02-TCD017-GOV03-ADMISSION", "record id")
    require(admission["tcd_ids"] == ["TCD-017"], "atomic TCD identity")
    require(admission["atomicity"] == "ATOMIC", "atomicity")
    require(admission["qualification_class"] == "A", "Class-A qualification")
    require(admission["admission_route"] == EXPECTED_ROUTE, "historical uncertainty route")
    require(admission["disposition"] == EXPECTED_DISPOSITION, "fallback scientific disposition")
    require(admission["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 unavailability state")
    require(EXPECTED_GOV03_HEAD in admission["identities"]["b2"]["acquisition_effort_ref"], "GOV03 acquisition authority")

    review = admission["evidence"]["independent_review"]
    require(review["status"] == "COMPLETE", "independent review complete")
    require(review["result"] == "PASS", "independent review PASS")
    require(review["independent_from_correction_authoring"] is True, "separate authoring-context review")
    require(EXPECTED_REVIEW_HEAD in review["reviewer_or_workunit"], "review head pinned")
    require("no organizational or human independence claimed" in review["scope"], "independence boundary retained")

    hist = admission["evidence"]["historical_uncertainty"]
    require("UNKNOWN" in hist["uncertainty_statement"].upper() or "unknown" in hist["uncertainty_statement"].lower(), "historical uncertainty explicit")
    require(EXPECTED_REVIEW_HEAD in hist["second_line_review_ref"], "second-line ref pinned")

    gates = admission["gates"]
    expected_gates = {
        "b0_identity", "b1_evidence", "b2_route", "theory", "causal",
        "conservation", "expected_difference", "non_interference", "coverage",
        "independent_review", "residual_uncertainty", "class_specific",
        "composition_if_applicable"
    }
    require(set(gates) == expected_gates, "complete gate set")
    require(all(v["status"] == "PASS" for v in gates.values()), "all admission gates PASS")
    require(gates["composition_if_applicable"]["applicability"] == "NOT_APPLICABLE", "composition not applicable")

    decision = admission["admission_decision"]
    require(decision["admitted"] is True, "admission decision true")
    require(decision["decision"] == "ADMIT_TCD017_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY", "bounded admission decision")

    expected_forbidden = {
        "physical states", "process fluxes", "Bafop", "TCD-027 and TCD-028 surfaces"
    }
    unchanged = set(admission["evidence"]["expected_difference"]["unchanged_surfaces"])
    require(expected_forbidden.issubset(unchanged), "expected-difference non-interference boundary")

    require(admission["composition"]["is_composition"] is False, "no composition")
    require(admission["composition"]["component_record_ids"] == [], "no composition components")

    require(status["base"]["head"] == EXPECTED_B3D01_HEAD, "B3D01 base pinned")
    require(status["review_authority"]["head"] == EXPECTED_REVIEW_HEAD, "B3A02R authority pinned")
    require(status["review_authority"]["result"] == "PASS_TCD017_INDEPENDENT_SECOND_LINE_READINESS_REVIEW", "review result pinned")
    require(status["admission_route"] == EXPECTED_ROUTE, "status route")
    require(status["intended_final_disposition"] == EXPECTED_DISPOSITION, "status disposition")

    hard = status["hard_boundaries"]
    require(all(v is False for v in hard.values()), "all prohibited boundary changes remain false")

    require("Historical revision-53 behaviour remains `UNKNOWN`" in doc, "documentation retains historical uncertainty")
    require("does not" in doc, "documentation contains explicit boundaries")

    if status["work_status"]["qualified"]:
        require(status["state"] == "QUALIFIED_TCD017_ATOMIC_B3_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_NO_PRODUCTION_MIGRATION", "qualified state")
        require(status["admission"]["scientific_b3_admission_intended"] is True, "qualified admission flag")
        require(status["work_status"]["tested"] is True, "qualified status tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified status complete")

    print("PASS_B3D02_TCD017_ADMISSION")


if __name__ == "__main__":
    main()
