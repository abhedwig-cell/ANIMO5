#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D01_STATUS.json"
DISP = ROOT / "integration/animo-b3/TCD017_B3_DISPOSITION_GOV03.json"
DOC = ROOT / "docs/b3/TCD017_GOV03_FORMAL_DISPOSITION.md"

GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3A02 = "1a714eb144e43420ef5b176727e496ff9c46bc6d"
FROZEN_REVIEW = "3ff8f4bda77c631b82110b83317c6a9b42b867ad"
SOURCE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    s = load(STATUS)
    d = load(DISP)
    doc = DOC.read_text(encoding="utf-8")

    assert s["work_unit"] == "ANIMO-B3D01"
    assert s["branch"] == "work/animo-b3d01-tcd017-gov03-disposition"
    assert s["base"]["head"] == GOV03
    assert s["target_tcd"] == "TCD-017"
    assert s["readiness_authority"].endswith(B3A02)
    assert s["b3_framework"].endswith(B3Q01)
    assert s["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"

    route = s["route_reconciliation"]
    assert route["historical_B2_available"] is False
    assert route["GOV03_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
    assert route["G6U"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS"
    assert route["b2_route_gate"] == "PASS"
    assert route["historical_behaviour_status"] == "UNKNOWN"

    gates = s["scientific_gates"]
    assert gates["b0_identity"] == "PASS"
    assert gates["b1_evidence"] == "PASS"
    assert gates["b2_route"] == "PASS"
    assert gates["theory"] == "PASS"
    assert gates["causal"] == "PASS"
    assert gates["conservation"] == "PASS"
    assert gates["expected_difference"] == "PASS"
    assert gates["non_interference"] == "PASS"
    assert gates["coverage"] == "PASS"
    assert gates["class_specific"] == "PASS"
    assert gates["residual_uncertainty"] == "PASS"
    assert gates["independent_review"] == "FAIL_PENDING_NOT_COMPLETED"
    assert gates["composition_if_applicable"] == "PASS_NOT_APPLICABLE"

    r = s["independent_review"]
    assert r["issue"] == 25
    assert r["clean_branch"] == "review/animo-b3a02r-tcd017-second-line"
    assert r["frozen_review_object_head"] == FROZEN_REVIEW
    assert r["same_authoring_context_may_count"] is False
    assert r["review_complete"] is False
    assert r["gate"] == "BLOCKING"

    a = s["admission"]
    assert all(v is False for v in a.values())

    assert d["record_id"] == "B3D01-TCD017-GOV03-DISPOSITION"
    assert d["tcd_ids"] == ["TCD-017"]
    assert d["atomicity"] == "ATOMIC"
    assert d["qualification_class"] == "A"
    assert d["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
    assert d["disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert d["identities"]["b0"]["source_sha256"] == SOURCE
    assert d["identities"]["b0"]["testbank_sha256"] == TESTBANK
    assert d["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT"
    assert GOV03 in d["identities"]["b2"]["acquisition_effort_ref"]
    assert d["evidence"]["independent_review"]["status"] == "INCOMPLETE"
    assert d["evidence"]["independent_review"]["result"] == "NOT_REVIEWED"
    assert d["gates"]["b2_route"]["status"] == "PASS"
    assert d["gates"]["independent_review"]["status"] == "FAIL"
    assert d["composition"] == {"is_composition": False, "component_record_ids": []}
    assert d["admission_decision"]["admitted"] is False
    assert d["admission_decision"]["decision"] == "UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03"

    assert "independent_review = FAIL_PENDING_NOT_COMPLETED" in doc
    assert "UNRESOLVED_NOT_ADMITTED" in doc
    assert "G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" in doc
    assert "does not modify production source" in doc

    expected = {
        "integration/animo-b3/TCD017_B3_DISPOSITION_GOV03.json",
        "integration/animo-b3/ANIMO-B3D01_STATUS.json",
        "docs/b3/TCD017_GOV03_FORMAL_DISPOSITION.md",
        "tools/validate_b3d01_tcd017_disposition.py",
        ".github/workflows/animo-b3d01-tcd017-disposition.yml",
    }
    assert set(s["deliverables"]) == expected
    for rel in expected:
        assert (ROOT / rel).exists(), rel

    if s["work_status"]["qualified"]:
        assert s["state"] == "QUALIFIED_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION"
        assert s["work_status"]["tested"] is True
        assert s["work_status"]["work_unit_complete"] is True
        assert s["validation"]["validator_result"] == "PASS"
        assert s["validation"]["github_actions_conclusion"] == "success"
    else:
        assert s["state"] == "QUALIFIED_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION"
        assert s["work_status"]["tested"] is False
        assert s["work_status"]["work_unit_complete"] is False

    print("ANIMO-B3D01 validator: PASS")
    print("GOV03 historical-uncertainty route: PASS")
    print("TCD-017 Class-A readiness gates except independent review: PASS")
    print("independent second-line review: PENDING/BLOCKING")
    print("B3 admission: NO")


if __name__ == "__main__":
    main()
