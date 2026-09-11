#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "c2b29f05b7726f3c57a39481b92f211e78dbee59"
STATEQ05 = ROOT / "integration/animo-state/ANIMO-STATEQ05_STATUS.json"
STATEQ05_CONTRACT = ROOT / "integration/animo-state/TCD039_POTENTIAL_UPTAKE_CONTINUATION_CONTRACT.json"
STATEQ01_MATRIX = ROOT / "integration/animo-state/PERSISTENT_STATE_MATRIX.csv"
QUEUE = ROOT / "integration/animo-reg/RG05_B3_QUEUE.json"
CONTRACT = ROOT / "integration/animo-b3/B3B11_TCD039_READINESS_CONTRACT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B11_STATUS.json"

ALLOWED = {
    ".github/workflows/animo-b3b11-tcd039-readiness.yml",
    "docs/b3b11/TCD039_POTENTIAL_UPTAKE_RESTART_READINESS.md",
    "integration/animo-b3/B3B11_TCD039_READINESS_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3B11_STATUS.json",
    "integration/animo-b3/ANIMO-B3B11_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3B11_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3b11_tcd039.py",
}


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return {line.strip() for line in out.splitlines() if line.strip()}


def validate_scope():
    changed = changed_files()
    require(not sorted(changed - ALLOWED), f"scope violation: {sorted(changed - ALLOWED)}")
    require("integration/animo-b3/B3B11_TCD039_READINESS_CONTRACT.json" in changed, "readiness contract missing")
    require("tools/validate_b3b11_tcd039.py" in changed, "validator missing")
    return changed


def validate_upstream():
    state = load(STATEQ05)
    require(state["work_unit"] == "ANIMO-STATEQ05" and state["tcd"] == "TCD-039", "wrong STATEQ05 target")
    require(state["state"] == "QUALIFIED_TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_CONTINUATION_OWNERSHIP_READY_FOR_SEPARATE_B3_READINESS", "STATEQ05 not final qualified authority")
    require(state["work_status"]["qualified"] is True and state["work_status"]["work_unit_complete"] is True, "STATEQ05 not qualified/complete")
    require(state["scientific_admission_performed"] is False, "STATEQ05 must not already admit TCD039")
    require(state["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "STATEQ05 GOV05 assurance mismatch")
    require(state["review"]["genuinely_independent"] is False, "STATEQ05 independence overclaim")

    sc = load(STATEQ05_CONTRACT)
    require(sc["qualified_claim"].startswith("FOR_FROZEN_REVISION53_INTERNAL_CROP_MODE"), "STATEQ05 claim scope widened")
    owners = sc["logical_continuation_owners"]
    require(len(owners) == 2, "expected two logical continuation owners")
    require(owners[0]["accepted_owner"] == "Rsamplni_pot" and owners[0]["working_alias"] == "Amplni_pot", "N owner pair mismatch")
    require(owners[1]["accepted_owner"] == "Rsamplpo_pot" and owners[1]["working_alias"] == "Amplpo_pot", "P owner pair mismatch")
    require(owners[1]["feature_guard"] == "Ipo == 1", "P feature guard missing")

    matrix = STATEQ01_MATRIX.read_text(encoding="utf-8")
    require("CROP-005,cumulative potential crop nitrogen uptake continuation,NUMERICAL_CONTINUATION" in matrix, "STATEQ01 CROP-005 missing")
    require("CROP-006,cumulative potential crop phosphorus uptake continuation,NUMERICAL_CONTINUATION" in matrix, "STATEQ01 CROP-006 missing")
    require("CROP-007,remaining crop demand deficit stage and rotation continuation,UNRESOLVED_SCIENTIFIC_STATE" in matrix, "STATEQ01 CROP-007 boundary missing")

    queue = load(QUEUE)
    entries = {e["tcd"]: e for e in queue["entries"]}
    require("TCD-039" in entries, "TCD039 absent from canonical queue source")
    q = entries["TCD-039"]
    require(q["process"] == "crop potential uptake restart continuation state", "TCD039 process mismatch")
    require(q["b3_class"] == "C provisional", "expected provisional queue class")
    require(q["queue_state"] == "WAITING_ON_STATE", "expected pre-STATEQ05 queue state")
    require("owner versus deterministic reconstruction unresolved for internal-crop profile" in q["blockers"], "expected TCD039 blocker missing")


def validate_contract(c):
    require(c["work_unit"] == "ANIMO-B3B11" and c["target"] == "TCD-039", "contract identity")
    require(c["base_authority"] == f"ANIMO-STATEQ05@{BASE}", "base authority mismatch")
    cl = c["classification"]
    require(cl["prior_queue_class"] == "C provisional", "prior class mismatch")
    require(cl["resolved_b3_qualification_class"] == "B_LOCAL_RESTART_CHECKPOINT_OMISSION_EXISTING_CONTINUATION_OWNER", "resolved class mismatch")
    require(cl["class_c_definition_triggered"] is False, "Class C must not remain triggered after owner resolution")
    require(cl["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "Tier C risk must be preserved")
    require(cl["strictest_risk_rule_applied"] is True and cl["scientific_gate_reduced_by_reclassification"] is False, "risk reduction forbidden")
    a = c["admission_candidate"]
    require(a["identity"] == "TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_OWNER_RESTORE_N_AND_CONDITIONAL_P", "candidate identity mismatch")
    require(a["scope"] == "FROZEN_REV53_INTERNAL_CROP_Ioptplant_1", "candidate scope mismatch")
    require(a["p_guard"] == "Ipo == 1", "P guard mismatch")
    require(a["zero_reset_at_arbitrary_restart"] == "FORBIDDEN", "zero reset must be forbidden")
    require(a["checkpoint_representation_implementation_defined_here"] is False, "readiness must not define production format")
    forms = {x["id"] for x in c["causal_evidence_forms"]}
    require(forms == {"FORM1_FROZEN_SOURCE_LIFECYCLE", "FORM2_PRIOR_STATE_AUTHORITY", "FORM3_EXECUTABLE_NEGATIVE_CONTROL"}, "causal evidence forms incomplete")
    require(c["historical_disposition"]["behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty erased")
    require(c["historical_disposition"]["b2_created"] is False, "synthetic promoted to B2")
    r = c["readiness"]
    require(r["owner_vs_reconstruction_blocker_resolved_for_bounded_profile"] is True, "state blocker not resolved")
    require(r["atomic_candidate_defined"] is True and r["ready_for_separate_tier_c_admission_decision"] is True, "readiness incomplete")
    require(r["b3_admitted"] is False, "B3B11 cannot admit")


def validate_status(s):
    require(s["work_unit"] == "ANIMO-B3B11" and s["target"] == "TCD-039", "status identity")
    require(s["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk tier")
    require(s["b3_admitted"] is False and s["production_authorized"] is False, "readiness boundary")
    require(s["canonical_state_admitted"] is False, "canonical STATE must remain closed")
    require(s["canonical_register_modified"] is False and s["central_queue_modified"] is False, "canonical governance mutation forbidden")
    require(s["tcd038_reopened"] is False and s["crop007_closed"] is False, "scope contamination")
    phase = s["phase"]
    require(phase in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, f"unexpected phase {phase}")
    if phase == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        require(s["readiness_qualified"] is True, "final readiness not qualified")
        review = s["review"]
        require(review["completed"] is True, "final status lacks review")
        require(review["same_agent"] is True and review["genuinely_independent"] is False, "review independence overclaim")
        require(review["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance mismatch")


def main():
    changed = validate_scope()
    validate_upstream()
    validate_contract(load(CONTRACT))
    validate_status(load(STATUS))
    print("PASS ANIMO-B3B11 TCD-039 bounded Class-B readiness with Tier-C risk")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
