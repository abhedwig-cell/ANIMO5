#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D03_STATUS.json"
DISP = ROOT / "integration/animo-b3/TCD024_B3_DISPOSITION_GOV03.json"
DOC = ROOT / "docs/b3/TCD024_GOV03_FORMAL_DISPOSITION.md"

RG05A = "a4eb1bb1632a573c93b7d44186f7d200a862c6e7"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3B03 = "446f57f3aeff6e7db56ce473f0724bdb58cad94f"
HANDOFF = "07e440bb42d58facad6b4e5408dd57a0d8f82daf"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
DECISION = "UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03"


def req(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D03: " + msg)


def main():
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    disp = json.loads(DISP.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    req(disp["record_id"] == "B3D03-TCD024-GOV03-DISPOSITION", "record id")
    req(disp["tcd_ids"] == ["TCD-024"], "target")
    req(disp["atomicity"] == "ATOMIC", "atomicity")
    req(disp["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "class")
    req(disp["admission_route"] == ROUTE, "route")
    req(disp["disposition"] == "UNRESOLVED_NOT_ADMITTED", "fail-closed disposition")
    req(disp["scope"]["legacy_expression"] == "Yy = One + Parcxsl(3,I) * Avc", "legacy expression")
    req(disp["scope"]["candidate_atomic_correction"] == "Yy = One + Parcxsl(3,J) * Avc", "corrected index")
    req(disp["authorities"]["RG05A"] == RG05A, "RG05A authority")
    req(disp["authorities"]["GOV03"] == GOV03, "GOV03 authority")
    req(disp["authorities"]["B3B03"] == B3B03, "B3B03 authority")
    req(HANDOFF in disp["authorities"]["review_handoff"], "handoff authority")
    req(disp["historical_route"]["b2_available"] is False, "B2 unavailable")
    req(disp["historical_route"]["historical_prevalence"] == "UNKNOWN", "historical prevalence unknown")
    req(disp["historical_route"]["historical_fidelity_claimed"] is False, "no historical fidelity")
    req(disp["coverage"]["natural_positive_Optcxsl2_activation"] is False, "natural positive activation absent")
    req(disp["coverage"]["natural_negative_control"] == "PASS", "natural negative control")
    req(disp["coverage"]["synthetic_active_unequal_site_discriminator"] == "PASS", "synthetic active discriminator")
    req(disp["gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "review remains blocking")
    req(disp["independent_review"]["review_status_at_reconciliation"] == "PENDING_INDEPENDENT_REVIEW", "review pending")
    req(disp["independent_review"]["same_authoring_context_may_count"] is False, "same context cannot review")
    req(disp["admission_decision"]["admitted"] is False, "not admitted")
    req(disp["admission_decision"]["decision"] == DECISION, "decision")
    req(disp["admission_decision"]["production_patch_authorized"] is False, "no production patch")
    req(disp["admission_decision"]["production_migration_admitted"] is False, "no production migration")

    req(status["work_unit"] == "ANIMO-B3D03", "status work unit")
    req(status["base"]["head"] == RG05A, "base head")
    req(status["target_tcd"] == "TCD-024", "status target")
    req(status["readiness_authority"].endswith(B3B03), "readiness authority")
    req(status["admission_route"] == ROUTE, "status route")
    req(status["route_reconciliation"]["b2_route_gate"] == "PASS", "route gate pass")
    req(status["route_reconciliation"]["historical_prevalence"] == "UNKNOWN", "status historical unknown")
    req(status["scientific_gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "status review pending")
    req(status["independent_review"]["handoff_head"] == HANDOFF, "status handoff head")
    req(status["admission"]["admitted"] is False, "status not admitted")
    req(status["admission"]["historical_fidelity_claimed"] is False, "status no historical fidelity")
    req(status["admission"]["production_patch_authorized"] is False, "status no patch")

    req("historical prevalence" in doc.lower(), "doc historical prevalence")
    req("PENDING_INDEPENDENT_REVIEW" in doc, "doc review pending")
    req("performs no B3 admission" in doc, "doc no admission")

    if status["work_status"]["qualified"]:
        req(status["state"] == "QUALIFIED_TCD024_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION", "qualified state")
        req(status["decision"] == DECISION, "qualified decision")
        req(status["work_status"]["tested"] is True, "qualified tested")
        req(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_B3D03_TCD024_GOV03_DISPOSITION")


if __name__ == "__main__":
    main()
