#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-reg/ANIMO-RG05B_STATUS.json"
INVENTORY = ROOT / "integration/animo-reg/RG05B_B3_ADMISSION_INVENTORY.json"
DELTA = ROOT / "integration/animo-reg/RG05B_B3_QUEUE_DELTA.json"
DOC = ROOT / "docs/governance/ANIMO_RG05B_SECOND_B3_ADMISSION_REGIE.md"
RG05A = ROOT / "integration/animo-reg/ANIMO-RG05A_STATUS.json"
TCD017 = ROOT / "integration/animo-b3/TCD017_B3_ADMISSION_CLOSEOUT.json"
TCD024 = ROOT / "integration/animo-b3/TCD024_B3_ADMISSION_CLOSEOUT.json"
B3D04_STATUS = ROOT / "integration/animo-b3/ANIMO-B3D04_STATUS.json"

RG05A_HEAD = "a4eb1bb1632a573c93b7d44186f7d200a862c6e7"
B3D02_HEAD = "bf31ffa96b4f71541c13d1426ccf48eac9536b24"
B3D04_HEAD = "a42e1158b3eda670ca08329bc55943c7c6c9d655"
REVIEW017 = "8b38b03ac489c349192ae9fa55a8fe51cea183cb"
REVIEW024 = "b36aedb4406c3f92d6ee7cd2fa4231ed872620ec"
GOV03_HEAD = "cbd262bdabe92923113b7326f2f42822ce9a971c"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
DEC017 = "ADMIT_TCD017_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
DEC024 = "ADMIT_TCD024_ATOMIC_CLASS_B_SCIENTIFIC_INDEX_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_RG05B: " + msg)


def main():
    status = load(STATUS)
    inventory = load(INVENTORY)
    delta = load(DELTA)
    rg05a = load(RG05A)
    a17 = load(TCD017)
    a24 = load(TCD024)
    b3d04 = load(B3D04_STATUS)
    doc = DOC.read_text(encoding="utf-8")

    require(rg05a["work_unit"] == "ANIMO-RG05A", "RG05A inherited")
    require(rg05a["decision"] == "QUALIFIED_POST_RG05_FIRST_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION", "RG05A frozen qualified decision")
    require(rg05a["admission_state"]["scientific_admissions"] == 1, "RG05A remains one-admission snapshot")
    require(rg05a["admission_state"]["admitted_tcds"] == ["TCD-017"], "RG05A admitted set unchanged")

    require(b3d04["decision"] == DEC024, "B3D04 decision")
    require(b3d04["admission"]["scientific_b3_admission_qualified"] is True, "B3D04 qualified admission")
    require(b3d04["admission"]["production_migration_admitted"] is False, "B3D04 no production migration")

    require(a17["record_id"] == "B3D02-TCD017-GOV03-ADMISSION", "TCD017 admission record")
    require(a17["admission_decision"]["admitted"] is True, "TCD017 admitted")
    require(a17["admission_decision"]["decision"] == DEC017, "TCD017 decision")
    require(a17["admission_route"] == ROUTE, "TCD017 route")
    require(a17["disposition"] == DISPOSITION, "TCD017 disposition")
    require(REVIEW017 in a17["evidence"]["independent_review"]["reviewer_or_workunit"], "TCD017 review pin")

    require(a24["record_id"] == "B3D04-TCD024-GOV03-ADMISSION", "TCD024 admission record")
    require(a24["admission_decision"]["admitted"] is True, "TCD024 admitted")
    require(a24["admission_decision"]["decision"] == DEC024, "TCD024 decision")
    require(a24["admission_route"] == ROUTE, "TCD024 route")
    require(a24["disposition"] == DISPOSITION, "TCD024 disposition")
    require(a24["evidence"]["independent_review"]["result"] == "PASS", "TCD024 independent review pass")
    require(REVIEW024 in a24["evidence"]["independent_review"]["reviewer_or_workunit"], "TCD024 review pin")
    require(a24["evidence"]["coverage"]["natural_positive_Optcxsl2_activation"] is False, "TCD024 natural-positive limitation retained")
    require(a24["class_specific_evidence"]["TCD019_separation"] == "PASS", "TCD019 separation retained")
    require(GOV03_HEAD in a24["identities"]["b2"]["acquisition_effort_ref"], "TCD024 GOV03 route pin")

    require(status["work_unit"] == "ANIMO-RG05B", "status work unit")
    require(status["base"]["head"] == B3D04_HEAD, "status B3D04 base")
    require(status["base"]["ancestor_rg05a"] == RG05A_HEAD, "status RG05A ancestor")
    require(status["authority"]["RG05A"] == RG05A_HEAD, "status RG05A authority")
    require(status["authority"]["B3D02"] == B3D02_HEAD, "status B3D02 authority")
    require(status["authority"]["B3D04"] == B3D04_HEAD, "status B3D04 authority")
    require(status["authority"]["B3A02R"] == REVIEW017, "status TCD017 review authority")
    require(status["authority"]["B3B03R"] == REVIEW024, "status TCD024 review authority")
    require(status["authority"]["GOV03"] == GOV03_HEAD, "status GOV03 authority")
    require(status["admission_state"]["scientific_admissions"] == 2, "status two admissions")
    require(status["admission_state"]["admitted_tcds"] == ["TCD-017", "TCD-024"], "status admitted set")
    require(status["admission_state"]["tcd017_decision"] == DEC017, "status TCD017 decision")
    require(status["admission_state"]["tcd024_decision"] == DEC024, "status TCD024 decision")
    require(status["admission_state"]["b3_whole_model_baseline_complete"] is False, "B3 remains incomplete")
    require(status["admission_state"]["b4_baseline_admitted"] is False, "B4 closed")
    require(status["admission_state"]["production_migration_admitted"] is False, "production closed")
    require(status["admission_state"]["production_code_modified"] is False, "production source unchanged")
    require(status["admission_state"]["legacy_source_modified"] is False, "legacy source unchanged")
    require(status["admission_state"]["frozen_testcase_modified"] is False, "frozen testbank unchanged")
    require(status["admission_state"]["canonical_tcd_register_modified"] is False, "canonical register unchanged")
    require(status["admission_state"]["evidence_strength_promoted_by_integration"] is False, "no evidence promotion")

    inv = inventory["admissions"]
    require(len(inv) == 2, "inventory exactly two admissions")
    require([x["tcd"] for x in inv] == ["TCD-017", "TCD-024"], "inventory admitted order")
    i17, i24 = inv
    require(B3D02_HEAD in i17["admission_authority"], "inventory TCD017 authority")
    require(B3D04_HEAD in i24["admission_authority"], "inventory TCD024 authority")
    require(REVIEW024 in i24["review_authority"], "inventory TCD024 review")
    require(i17["historical_behaviour"] == "UNKNOWN" and i24["historical_behaviour"] == "UNKNOWN", "historical uncertainty retained")
    require(i24["TCD019_composed"] is False, "inventory TCD019 not composed")
    require(inventory["counts"]["scientific_admissions"] == 2, "inventory count two")
    require(inventory["counts"]["atomic_admissions"] == 2, "inventory atomic count two")
    require(inventory["project_boundary"]["B3_complete"] is False, "inventory B3 incomplete")
    require(inventory["project_boundary"]["B4_open"] is False, "inventory B4 closed")
    require(inventory["project_boundary"]["production_open"] is False, "inventory production closed")

    require(len(delta["tcd_deltas"]) == 1, "one incremental TCD delta")
    d = delta["tcd_deltas"][0]
    require(d["tcd"] == "TCD-024", "delta TCD024")
    require(d["from_queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW", "delta source state")
    require(d["to_state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "delta admitted state")
    require(B3D04_HEAD in d["admission_authority"], "delta B3D04 authority")
    require(REVIEW024 in d["review_authority"], "delta review authority")
    require(delta["admitted_tcds"] == ["TCD-017", "TCD-024"], "delta admitted set")

    counts = delta["post_delta_counts"]
    queue_keys = [
        "READY_FOR_ADMISSION_READINESS", "IN_PROGRESS_ADMISSION_READINESS",
        "WAITING_ON_ROUTE_AND_REVIEW", "WAITING_ON_THEORY", "WAITING_ON_NUMERICS",
        "WAITING_ON_STATE", "WAITING_ON_RUNTIME", "WAITING_ON_CHILDREN", "NOT_READY"
    ]
    active_sum = sum(counts[k] for k in queue_keys)
    require(counts["canonical_tcd_entries"] == 25, "canonical count 25")
    require(counts["active_queue_entries"] == 23, "active queue 23")
    require(active_sum == 23, "active queue arithmetic")
    require(counts["WAITING_ON_ROUTE_AND_REVIEW"] == 5, "route/review count 5")
    require(counts["scientific_admissions"] == 2, "queue scientific admissions 2")
    require(counts["active_queue_entries"] + counts["scientific_admissions"] == counts["canonical_tcd_entries"], "queue plus admissions equals canonical count")

    require("exactly two qualified atomic B3 scientific admissions" in doc, "two-admission state documented")
    require("does not reopen RG05 or RG05A" in doc, "snapshot immutability documented")
    require("TCD-019 is not composed into TCD-024" in doc, "TCD019 separation documented")
    require("B4" in doc and "production migration" in doc.lower(), "downstream boundaries documented")

    if status["work_status"]["qualified"]:
        expected = "QUALIFIED_POST_RG05A_SECOND_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION"
        require(status["state"] == expected, "qualified state")
        require(status["decision"] == expected, "qualified decision")
        require(status["work_status"]["tested"] is True, "qualified tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_RG05B_SECOND_B3_ADMISSION_INTEGRATION")


if __name__ == "__main__":
    main()
