#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-reg/ANIMO-RG05C_STATUS.json"
INVENTORY = ROOT / "integration/animo-reg/RG05C_B3_ADMISSION_INVENTORY.json"
DELTA = ROOT / "integration/animo-reg/RG05C_B3_QUEUE_DELTA.json"
DOC = ROOT / "docs/governance/ANIMO_RG05C_THIRD_B3_ADMISSION_REGIE.md"
RG05B = ROOT / "integration/animo-reg/ANIMO-RG05B_STATUS.json"
TCD017 = ROOT / "integration/animo-b3/TCD017_B3_ADMISSION_CLOSEOUT.json"
TCD018 = ROOT / "integration/animo-b3/TCD018_B3_ADMISSION_CLOSEOUT.json"
TCD024 = ROOT / "integration/animo-b3/TCD024_B3_ADMISSION_CLOSEOUT.json"
B3D06_STATUS = ROOT / "integration/animo-b3/ANIMO-B3D06_STATUS.json"

RG05B_HEAD = "c353c3179f213c1bf24c48b3c06f8065c760d3e2"
B3D02_HEAD = "bf31ffa96b4f71541c13d1426ccf48eac9536b24"
B3D04_HEAD = "a42e1158b3eda670ca08329bc55943c7c6c9d655"
B3D06_HEAD = "11286faafcc59717196ed045d96c9d215c74abeb"
REVIEW017 = "8b38b03ac489c349192ae9fa55a8fe51cea183cb"
REVIEW018 = "fc4a53c2e2e32dee27062959c7ecba7b605cf398"
REVIEW024 = "b36aedb4406c3f92d6ee7cd2fa4231ed872620ec"
REMEDIATION018 = "4c92b27ed5bbcaadb0e703e622e8c3f690458fa8"
GOV03_HEAD = "cbd262bdabe92923113b7326f2f42822ce9a971c"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
DEC017 = "ADMIT_TCD017_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
DEC018 = "ADMIT_TCD018_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
DEC024 = "ADMIT_TCD024_ATOMIC_CLASS_B_SCIENTIFIC_INDEX_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
R2_RESULT = "PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_READINESS_REVIEW"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_RG05C: " + msg)


def main():
    status = load(STATUS)
    inventory = load(INVENTORY)
    delta = load(DELTA)
    rg05b = load(RG05B)
    a17 = load(TCD017)
    a18 = load(TCD018)
    a24 = load(TCD024)
    b3d06 = load(B3D06_STATUS)
    doc = DOC.read_text(encoding="utf-8")

    require(rg05b["work_unit"] == "ANIMO-RG05B", "RG05B inherited")
    require(rg05b["decision"] == "QUALIFIED_POST_RG05A_SECOND_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION", "RG05B qualified snapshot")
    require(rg05b["admission_state"]["scientific_admissions"] == 2, "RG05B remains two-admission snapshot")
    require(rg05b["admission_state"]["admitted_tcds"] == ["TCD-017", "TCD-024"], "RG05B admitted set unchanged")
    require(rg05b["queue_state"]["active_queue_entries"] == 23, "RG05B active queue 23")
    require(rg05b["queue_state"]["WAITING_ON_ROUTE_AND_REVIEW"] == 5, "RG05B route/review count 5")

    require(b3d06["work_unit"] == "ANIMO-B3D06", "B3D06 status")
    require(b3d06["decision"] == DEC018, "B3D06 decision")
    require(b3d06["admission"]["scientific_b3_admission_qualified"] is True, "B3D06 admission qualified")
    require(b3d06["review_authority"]["head"] == REVIEW018, "B3D06 R2 review pin")
    require(b3d06["review_authority"]["result"] == R2_RESULT, "B3D06 R2 PASS")
    require(b3d06["evidence_remediation_authority"]["head"] == REMEDIATION018, "B3D06 remediation pin")
    require(b3d06["admission"]["historical_behaviour_status"] == "UNKNOWN", "B3D06 historical behaviour unknown")
    require(b3d06["admission"]["global_water_closure_claimed"] is False, "B3D06 no global closure")
    require(b3d06["admission"]["production_migration_admitted"] is False, "B3D06 no production migration")

    require(a17["record_id"] == "B3D02-TCD017-GOV03-ADMISSION", "TCD017 admission record")
    require(a17["admission_decision"]["admitted"] is True, "TCD017 admitted")
    require(a17["admission_decision"]["decision"] == DEC017, "TCD017 decision")
    require(a17["admission_route"] == ROUTE and a17["disposition"] == DISPOSITION, "TCD017 route/disposition")
    require(REVIEW017 in a17["evidence"]["independent_review"]["reviewer_or_workunit"], "TCD017 review pin")

    require(a18["record_id"] == "B3D06-TCD018-GOV03-ADMISSION", "TCD018 admission record")
    require(a18["admission_decision"]["admitted"] is True, "TCD018 admitted")
    require(a18["admission_decision"]["decision"] == DEC018, "TCD018 decision")
    require(a18["admission_route"] == ROUTE and a18["disposition"] == DISPOSITION, "TCD018 route/disposition")
    require(a18["authorities"]["B3A03R2"] == REVIEW018, "TCD018 review authority")
    require(a18["authorities"]["B3A03E"] == REMEDIATION018, "TCD018 remediation authority")
    require(a18["evidence"]["independent_review"]["result"] == R2_RESULT, "TCD018 R2 result")
    require(a18["evidence"]["independent_review"]["previous_fail_retained"] == "FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW", "TCD018 previous FAIL retained")
    require(a18["evidence"]["residual_boundary"]["MASSQ01_CranGrass_TITO724_class"] == "UNEXPLAINED_RESIDUAL_OUTSIDE_TCD018", "TCD018 unrelated residual retained")
    require(a18["evidence"]["residual_boundary"]["global_water_closure_claimed"] is False, "TCD018 no global closure")
    require(a18["admission_decision"]["production_patch_authorized"] is False, "TCD018 no production patch")

    require(a24["record_id"] == "B3D04-TCD024-GOV03-ADMISSION", "TCD024 admission record")
    require(a24["admission_decision"]["admitted"] is True, "TCD024 admitted")
    require(a24["admission_decision"]["decision"] == DEC024, "TCD024 decision")
    require(a24["admission_route"] == ROUTE and a24["disposition"] == DISPOSITION, "TCD024 route/disposition")
    require(REVIEW024 in a24["evidence"]["independent_review"]["reviewer_or_workunit"], "TCD024 review pin")
    require(a24["evidence"]["coverage"]["natural_positive_Optcxsl2_activation"] is False, "TCD024 limitation retained")
    require(a24["class_specific_evidence"]["TCD019_separation"] == "PASS", "TCD019 separation retained")

    require(status["work_unit"] == "ANIMO-RG05C", "status work unit")
    require(status["base"]["head"] == B3D06_HEAD, "status B3D06 base")
    require(status["base"]["ancestor_rg05b"] == RG05B_HEAD, "status RG05B ancestor")
    require(status["authority"]["RG05B"] == RG05B_HEAD, "status RG05B authority")
    require(status["authority"]["B3D02"] == B3D02_HEAD, "status B3D02 authority")
    require(status["authority"]["B3D04"] == B3D04_HEAD, "status B3D04 authority")
    require(status["authority"]["B3D06"] == B3D06_HEAD, "status B3D06 authority")
    require(status["authority"]["B3A03R2"] == REVIEW018, "status R2 authority")
    require(status["authority"]["B3A03E"] == REMEDIATION018, "status remediation authority")
    require(status["authority"]["GOV03"] == GOV03_HEAD, "status GOV03 authority")
    require(status["admission_state"]["scientific_admissions"] == 3, "status three admissions")
    require(status["admission_state"]["admitted_tcds"] == ["TCD-017", "TCD-018", "TCD-024"], "status admitted set")
    require(status["admission_state"]["tcd017_decision"] == DEC017, "status TCD017 decision")
    require(status["admission_state"]["tcd018_decision"] == DEC018, "status TCD018 decision")
    require(status["admission_state"]["tcd024_decision"] == DEC024, "status TCD024 decision")
    require(status["admission_state"]["b3_whole_model_baseline_complete"] is False, "B3 remains incomplete")
    require(status["admission_state"]["b4_baseline_admitted"] is False, "B4 closed")
    require(status["admission_state"]["production_migration_admitted"] is False, "production closed")
    require(status["admission_state"]["production_code_modified"] is False, "production source unchanged")
    require(status["admission_state"]["legacy_source_modified"] is False, "legacy source unchanged")
    require(status["admission_state"]["frozen_testcase_modified"] is False, "frozen testbank unchanged")
    require(status["admission_state"]["canonical_tcd_register_modified"] is False, "canonical register unchanged")
    require(status["admission_state"]["evidence_strength_promoted_by_integration"] is False, "no evidence promotion")
    require(status["admission_state"]["global_water_closure_claimed"] is False, "status no global closure")

    inv = inventory["admissions"]
    require(len(inv) == 3, "inventory exactly three admissions")
    require([x["tcd"] for x in inv] == ["TCD-017", "TCD-018", "TCD-024"], "inventory admitted order")
    i17, i18, i24 = inv
    require(B3D02_HEAD in i17["admission_authority"], "inventory TCD017 authority")
    require(B3D06_HEAD in i18["admission_authority"], "inventory TCD018 authority")
    require(REVIEW018 in i18["review_authority"], "inventory TCD018 review")
    require(REMEDIATION018 in i18["evidence_remediation_authority"], "inventory TCD018 remediation")
    require(i18["previous_independent_fail_retained"] is True, "inventory previous FAIL retained")
    require(i18["unrelated_MASSQ01_residual_retained"] is True, "inventory unrelated residual retained")
    require(i18["global_water_closure_claimed"] is False, "inventory no global closure")
    require(B3D04_HEAD in i24["admission_authority"], "inventory TCD024 authority")
    require(all(x["historical_behaviour"] == "UNKNOWN" for x in inv), "historical uncertainty retained")
    require(i24["TCD019_composed"] is False, "inventory TCD019 not composed")
    require(inventory["counts"]["scientific_admissions"] == 3, "inventory count three")
    require(inventory["counts"]["atomic_admissions"] == 3, "inventory atomic count three")
    require(inventory["counts"]["historical_uncertainty_admissions"] == 3, "inventory historical uncertainty count three")
    require(inventory["project_boundary"]["B3_complete"] is False, "inventory B3 incomplete")
    require(inventory["project_boundary"]["B4_open"] is False, "inventory B4 closed")
    require(inventory["project_boundary"]["production_open"] is False, "inventory production closed")

    require(len(delta["tcd_deltas"]) == 1, "one incremental TCD delta")
    d = delta["tcd_deltas"][0]
    require(d["tcd"] == "TCD-018", "delta TCD018")
    require(d["from_queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW", "delta source state")
    require(d["to_state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "delta admitted state")
    require(B3D06_HEAD in d["admission_authority"], "delta B3D06 authority")
    require(REVIEW018 in d["review_authority"], "delta R2 authority")
    require(REMEDIATION018 in d["evidence_remediation_authority"], "delta remediation authority")
    require(d["previous_independent_fail_retained"] is True, "delta previous fail retained")
    require(d["global_water_closure_claimed"] is False, "delta no global closure")
    require(delta["admitted_tcds"] == ["TCD-017", "TCD-018", "TCD-024"], "delta admitted set")

    counts = delta["post_delta_counts"]
    queue_keys = [
        "READY_FOR_ADMISSION_READINESS", "IN_PROGRESS_ADMISSION_READINESS",
        "WAITING_ON_ROUTE_AND_REVIEW", "WAITING_ON_THEORY", "WAITING_ON_NUMERICS",
        "WAITING_ON_STATE", "WAITING_ON_RUNTIME", "WAITING_ON_CHILDREN", "NOT_READY"
    ]
    active_sum = sum(counts[k] for k in queue_keys)
    require(counts["canonical_tcd_entries"] == 25, "canonical count 25")
    require(counts["active_queue_entries"] == 22, "active queue 22")
    require(active_sum == 22, "active queue arithmetic")
    require(counts["WAITING_ON_ROUTE_AND_REVIEW"] == 4, "route/review count 4")
    require(counts["scientific_admissions"] == 3, "queue scientific admissions 3")
    require(counts["active_queue_entries"] + counts["scientific_admissions"] == counts["canonical_tcd_entries"], "queue plus admissions equals canonical count")

    require("exactly three qualified atomic B3 scientific admissions" in doc, "three-admission state documented")
    require("preserves RG05, RG05A and RG05B as historical snapshots" in doc, "snapshot immutability documented")
    require("previous independent review FAIL remains historically valid" in doc, "review history retained")
    require("UNEXPLAINED_RESIDUAL" in doc, "unrelated residual documented")
    require("No global water-closure claim is made" in doc, "no global closure documented")
    require("B4" in doc and "production migration" in doc.lower(), "downstream boundaries documented")

    if status["work_status"]["qualified"]:
        expected = "QUALIFIED_POST_RG05B_THIRD_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION"
        require(status["state"] == expected, "qualified state")
        require(status["decision"] == expected, "qualified decision")
        require(status["work_status"]["tested"] is True, "qualified tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_RG05C_THIRD_B3_ADMISSION_INTEGRATION")


if __name__ == "__main__":
    main()
