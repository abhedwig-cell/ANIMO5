#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "7e4ee6ebdfe168b24414c97df39b2ca76940ea44"
B3Q04 = "dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
STATEQ06_STATUS = ROOT / "integration/animo-state/ANIMO-STATEQ06_STATUS.json"
STATEQ06_CONTRACT = ROOT / "integration/animo-state/TCD035_GHG_PHASE_RESTART_RECONSTRUCTION_CONTRACT.json"
CONTRACT = ROOT / "integration/animo-b3/B3B12_TCD035_READINESS_CONTRACT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B12_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3b12-tcd035-readiness.yml",
    "docs/b3b12/TCD035_GHG_PHASE_RESTART_READINESS.md",
    "integration/animo-b3/B3B12_TCD035_READINESS_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3B12_STATUS.json",
    "integration/animo-b3/ANIMO-B3B12_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3B12_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3b12_tcd035.py",
}


def req(cond, msg):
    if not cond:
        raise AssertionError(msg)


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def git_json(commit, path):
    text = subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)
    return json.loads(text)


def main():
    changed = {x for x in subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True).splitlines() if x}
    req(not (changed - ALLOWED), f"scope violation {sorted(changed - ALLOWED)}")
    s6 = load(STATEQ06_STATUS)
    req(s6["state"] == "QUALIFIED_TCD035_SOIL_LAYER_GHG_PHASE_RECONSTRUCTION_OWNERSHIP_READY_FOR_SEPARATE_B3_READINESS", "STATEQ06 not final qualified")
    req(s6["qualified"] is True and s6["b3_admitted"] is False, "STATEQ06 boundary mismatch")
    req(s6["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" and s6["review"]["genuinely_independent"] is False, "STATEQ06 review mismatch")
    sc = load(STATEQ06_CONTRACT)
    req(sc["owner_model"]["co_independent_checkpoint_owner"] is False, "Co owner widened")
    req(sc["supported_scope"]["layer0_included"] is False, "layer0 widened")
    req(sc["classification_resolution"]["deterministic_reconstruction_from_accepted_coordinates_qualified"] is True, "state blocker unresolved")
    q = git_json(B3Q04, "integration/animo-reg/RG05_B3_QUEUE.json")
    e = next(x for x in q["entries"] if x["tcd"] == "TCD-035")
    req(e["b3_class"] == "C provisional" and e["queue_state"] == "WAITING_ON_STATE", "prior queue state mismatch")
    c = load(CONTRACT)
    req(c["base_authority"] == f"ANIMO-STATEQ06@{BASE}", "base mismatch")
    cl = c["classification"]
    req(cl["resolved_b3_qualification_class"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "class mismatch")
    req(cl["class_c_definition_triggered"] is False and cl["scientific_gate_reduced_by_reclassification"] is False, "unsafe reclassification")
    req(cl["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "risk reduced")
    a = c["admission_candidate"]
    req(a["layer0_in_scope"] is False and a["co_independent_checkpoint_owner"] is False, "scope/owner widened")
    req(a["legacy_Terf_general_equivalence"] is False and a["source_relation_preserved"] is True, "reconstruction semantics mismatch")
    req({x["id"] for x in c["causal_evidence_forms"]} == {"FORM1_FROZEN_SOURCE_AND_GHG01_ALGEBRA", "FORM2_STATEQ06_OWNER_RECONSTRUCTION_AUTHORITY", "FORM3_EXECUTABLE_SOURCE_SHAPED_ORACLE"}, "evidence forms incomplete")
    req(c["historical_disposition"]["behavior"] == "UNKNOWN_WITHOUT_B2" and c["historical_disposition"]["b2_created"] is False, "historical overclaim")
    req(c["readiness"]["ready_for_separate_tier_c_admission_decision"] is True and c["readiness"]["b3_admitted"] is False, "readiness boundary")
    s = load(STATUS)
    req(s["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk mismatch")
    req(s["b3_admitted"] is False and s["production_authorized"] is False and s["tcd036_reopened"] is False, "status boundary")
    req(s["phase"] in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, "unexpected phase")
    if s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        req(s["readiness_qualified"] is True and s["review"]["completed"] is True, "final readiness incomplete")
        req(s["review"]["same_agent"] is True and s["review"]["genuinely_independent"] is False and s["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review overclaim")
    print("PASS ANIMO-B3B12 TCD035 bounded Class-B readiness with Tier-C risk")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
