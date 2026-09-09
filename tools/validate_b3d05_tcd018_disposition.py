#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D05_STATUS.json"
DISP = ROOT / "integration/animo-b3/TCD018_B3_DISPOSITION_GOV03.json"
DOC = ROOT / "docs/b3/TCD018_GOV03_FORMAL_DISPOSITION.md"

RG05B = "c353c3179f213c1bf24c48b3c06f8065c760d3e2"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3A03 = "8eaaca34e4f0d906c2d8245f0df232586efe8ff3"
B3A03R = "0876e6e1b6ce33ee5e7b812ab4107f54760d6b27"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
DECISION = "UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def req(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D05: " + msg)


def main():
    s = load(STATUS)
    d = load(DISP)
    doc = DOC.read_text(encoding="utf-8")

    req(s["work_unit"] == "ANIMO-B3D05", "status work unit")
    req(s["base"]["head"] == RG05B, "RG05B base")
    req(B3A03 in s["readiness_authority"], "B3A03 authority")
    req(B3A03R in s["technical_review_authority"], "B3A03R technical authority")
    req(B3Q01 in s["b3_framework"], "B3Q01 authority")
    req(s["admission_route"] == ROUTE, "route")
    req(s["route_reconciliation"]["b2_route_gate"] == "PASS", "GOV03 route pass")
    req(s["route_reconciliation"]["historical_B2_available"] is False, "no B2")
    req(s["route_reconciliation"]["historical_behaviour"] == "UNKNOWN", "historical unknown")
    req(s["scientific_gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "independent review remains blocker")
    req(s["admission"]["admitted"] is False, "not admitted")
    req(s["admission"]["production_patch_authorized"] is False, "no production patch")

    req(d["record_id"] == "B3D05-TCD018-GOV03-DISPOSITION", "record id")
    req(d["tcd_ids"] == ["TCD-018"], "atomic TCD")
    req(d["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "class A")
    req(d["admission_route"] == ROUTE, "disposition route")
    req(d["authorities"]["RG05B"] == RG05B, "RG05B pin")
    req(d["authorities"]["GOV03"] == GOV03, "GOV03 pin")
    req(d["authorities"]["B3A03"] == B3A03, "B3A03 pin")
    req(d["authorities"]["B3A03R_TECH"] == B3A03R, "technical review pin")
    req(d["historical_route"]["b2_available"] is False, "no historical B2")
    req(d["historical_route"]["historical_behaviour"] == "UNKNOWN", "historical behaviour unknown")
    req(d["readiness_reconciliation"]["isolated_eight_case_noninterference"].startswith("PASS_TECHNICAL"), "isolated noninterference")
    req(d["readiness_reconciliation"]["raw_0_0601_mm_not_used_as_tolerance"] == "PASS", "no residual tolerance")
    req(d["gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "review gate fail closed")
    req(d["independent_review"]["technical_review_independent"] is False, "technical review not independent")
    req(d["admission_decision"]["admitted"] is False, "disposition not admitted")
    req(d["admission_decision"]["decision"] == DECISION, "disposition decision")
    req(d["admission_decision"]["production_patch_authorized"] is False, "no production authorization")

    changed = d["expected_difference"]["changed_surfaces"]
    req(len(changed) == 6, "six water-only changed surfaces")
    req(set(changed) == {"bawaGP.Out","bawaRP.Out","bawaTP.Out","ani_waGP.Bal","ani_waRP.Bal","ani_waTP.Bal"}, "water whitelist exact")

    req("0.0601" in doc and "not an acceptance epsilon" in doc, "tolerance boundary documented")
    req("separate ChatGPT context" in doc, "independence boundary documented")
    req("Historical revision-53 behaviour remains `UNKNOWN`" in doc, "historical uncertainty documented")

    if s["work_status"]["qualified"]:
        req(s["state"] == "QUALIFIED_TCD018_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION", "qualified state")
        req(s["decision"] == DECISION, "qualified decision")
        req(s["work_status"]["tested"] is True, "qualified tested")
        req(s["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_B3D05_TCD018_GOV03_DISPOSITION")


if __name__ == "__main__":
    main()
