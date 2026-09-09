#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-reg/ANIMO-RG05A_STATUS.json"
INVENTORY = ROOT / "integration/animo-reg/RG05A_B3_ADMISSION_INVENTORY.json"
DELTA = ROOT / "integration/animo-reg/RG05A_B3_QUEUE_DELTA.json"
DOC = ROOT / "docs/governance/ANIMO_RG05A_FIRST_B3_ADMISSION_REGIE.md"
ADMISSION = ROOT / "integration/animo-b3/TCD017_B3_ADMISSION_CLOSEOUT.json"
RG05 = ROOT / "integration/animo-reg/ANIMO-RG05_STATUS.json"

RG05_HEAD = "f127528e148b9106149daec02d48ad972581e6df"
GOV03_HEAD = "cbd262bdabe92923113b7326f2f42822ce9a971c"
REVIEW_HEAD = "8b38b03ac489c349192ae9fa55a8fe51cea183cb"
B3D02_HEAD = "bf31ffa96b4f71541c13d1426ccf48eac9536b24"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
DECISION = "ADMIT_TCD017_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_RG05A: " + msg)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    status = load(STATUS)
    inventory = load(INVENTORY)
    delta = load(DELTA)
    admission = load(ADMISSION)
    rg05 = load(RG05)
    doc = DOC.read_text(encoding="utf-8")

    require(rg05["work_unit"] == "ANIMO-RG05", "RG05 inherited status")
    require(rg05["decision"] == "QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS", "RG05 frozen decision")
    require(rg05["admission_state"]["scientific_admission_performed"] is False, "RG05 remains pre-admission snapshot")

    require(admission["record_id"] == "B3D02-TCD017-GOV03-ADMISSION", "B3D02 record id")
    require(admission["tcd_ids"] == ["TCD-017"], "B3D02 atomic target")
    require(admission["admission_route"] == ROUTE, "B3D02 route")
    require(admission["disposition"] == DISPOSITION, "B3D02 disposition")
    require(admission["admission_decision"]["admitted"] is True, "B3D02 admitted")
    require(admission["admission_decision"]["decision"] == DECISION, "B3D02 decision")
    require(admission["evidence"]["independent_review"]["status"] == "COMPLETE", "independent review complete")
    require(admission["evidence"]["independent_review"]["result"] == "PASS", "independent review PASS")
    require(REVIEW_HEAD in admission["evidence"]["independent_review"]["reviewer_or_workunit"], "review head pinned")
    require(GOV03_HEAD in admission["identities"]["b2"]["acquisition_effort_ref"], "GOV03 route pinned")
    require(admission["evidence"]["historical_uncertainty"]["uncertainty_statement"].lower().find("unknown") >= 0, "historical uncertainty retained")

    require(status["work_unit"] == "ANIMO-RG05A", "status work unit")
    require(status["base"]["head"] == B3D02_HEAD, "B3D02 base head")
    require(status["base"]["ancestor_rg05"] == RG05_HEAD, "RG05 ancestor pinned")
    require(status["authority"]["RG05"] == RG05_HEAD, "RG05 authority")
    require(status["authority"]["GOV03"] == GOV03_HEAD, "GOV03 authority")
    require(status["authority"]["B3A02R"] == REVIEW_HEAD, "review authority")
    require(status["authority"]["B3D02"] == B3D02_HEAD, "admission authority")
    require(status["admission_state"]["scientific_admissions"] == 1, "one scientific admission")
    require(status["admission_state"]["admitted_tcds"] == ["TCD-017"], "only TCD-017 admitted")
    require(status["admission_state"]["tcd017_disposition"] == DISPOSITION, "status disposition")
    require(status["admission_state"]["tcd017_decision"] == DECISION, "status decision")
    require(status["admission_state"]["b3_whole_model_baseline_complete"] is False, "B3 incomplete")
    require(status["admission_state"]["b4_baseline_admitted"] is False, "B4 closed")
    require(status["admission_state"]["production_migration_admitted"] is False, "production closed")
    require(status["admission_state"]["production_code_modified"] is False, "production unchanged")
    require(status["admission_state"]["legacy_source_modified"] is False, "legacy source unchanged")
    require(status["admission_state"]["frozen_testcase_modified"] is False, "testbank unchanged")
    require(status["admission_state"]["canonical_tcd_register_modified"] is False, "TCD register unchanged")
    require(status["admission_state"]["evidence_strength_promoted_by_integration"] is False, "no integration evidence promotion")

    inv = inventory["admissions"]
    require(len(inv) == 1, "inventory has exactly one admission")
    item = inv[0]
    require(item["tcd"] == "TCD-017", "inventory TCD-017")
    require(B3D02_HEAD in item["admission_authority"], "inventory B3D02 head")
    require(REVIEW_HEAD in item["review_authority"], "inventory review head")
    require(item["route"] == ROUTE, "inventory route")
    require(item["disposition"] == DISPOSITION, "inventory disposition")
    require(item["decision"] == DECISION, "inventory decision")
    require(item["historical_behaviour"] == "UNKNOWN", "inventory historical status")
    require(item["historical_fidelity_claimed"] is False, "no historical fidelity")
    require(item["composition_admitted"] is False, "no composition")
    require(item["b4_admitted"] is False, "no B4 admission")
    require(item["production_migration_admitted"] is False, "no production migration")
    require(inventory["counts"]["scientific_admissions"] == 1, "inventory admission count")
    require(inventory["project_boundary"]["B3_complete"] is False, "inventory B3 incomplete")
    require(inventory["project_boundary"]["B4_open"] is False, "inventory B4 closed")
    require(inventory["project_boundary"]["production_open"] is False, "inventory production closed")

    require(delta["route_delta"]["to"]["authority"].endswith(GOV03_HEAD), "queue delta GOV03 authority")
    require(delta["route_delta"]["to"]["historical_uncertainty_route_eligible"] is True, "queue delta route eligible")
    require(len(delta["tcd_deltas"]) == 1, "one TCD queue delta")
    d = delta["tcd_deltas"][0]
    require(d["tcd"] == "TCD-017", "delta TCD-017")
    require(d["from_queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW", "delta source state")
    require(d["to_state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "delta admitted state")
    require(B3D02_HEAD in d["admission_authority"], "delta B3D02 authority")
    require(d["historical_behaviour"] == "UNKNOWN", "delta historical uncertainty")

    counts = delta["post_delta_counts"]
    queue_keys = [
        "READY_FOR_ADMISSION_READINESS", "IN_PROGRESS_ADMISSION_READINESS",
        "WAITING_ON_ROUTE_AND_REVIEW", "WAITING_ON_THEORY", "WAITING_ON_NUMERICS",
        "WAITING_ON_STATE", "WAITING_ON_RUNTIME", "WAITING_ON_CHILDREN", "NOT_READY"
    ]
    active_sum = sum(counts[k] for k in queue_keys)
    require(counts["canonical_tcd_entries"] == 25, "canonical count remains 25")
    require(counts["active_queue_entries"] == 24, "active queue becomes 24")
    require(active_sum == 24, "active queue arithmetic")
    require(counts["WAITING_ON_ROUTE_AND_REVIEW"] == 6, "route/review queue decremented once")
    require(counts["scientific_admissions"] == 1, "delta admission count")
    require(counts["active_queue_entries"] + counts["scientific_admissions"] == counts["canonical_tcd_entries"], "queue plus admissions equals canonical count")

    require("does not reopen RG05" in doc, "RG05 immutability documented")
    require("exactly one qualified atomic B3 scientific admission" in doc, "one-admission project state documented")
    require("Production" not in doc or "production" in doc.lower(), "production boundary documented")

    if status["work_status"]["qualified"]:
        require(status["state"] == "QUALIFIED_POST_RG05_FIRST_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION", "qualified state")
        require(status["decision"] == "QUALIFIED_POST_RG05_FIRST_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION", "qualified decision")
        require(status["work_status"]["tested"] is True, "qualified tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_RG05A_FIRST_B3_ADMISSION_INTEGRATION")


if __name__ == "__main__":
    main()
