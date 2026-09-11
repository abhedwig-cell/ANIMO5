#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "6d8ba72ffd33eef4a16eb4dc693b1eaada772c4a"
RG05M = "7146612d5dfa8ad87a4660f0c50c68a5db1e3a29"
CONTRACT = ROOT / "integration/animo-b3/B3D37_TCD039_ADMISSION_CONTRACT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D37_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3d37-tcd039.yml",
    "docs/b3d37/TCD039_ATOMIC_B3_ADMISSION.md",
    "integration/animo-b3/B3D37_TCD039_ADMISSION_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3D37_STATUS.json",
    "integration/animo-b3/ANIMO-B3D37_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3D37_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3d37_tcd039.py",
}

def req(cond, msg):
    if not cond:
        raise AssertionError(msg)

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_json(commit, path):
    text = subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)
    return json.loads(text)

def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return {x.strip() for x in out.splitlines() if x.strip()}

def validate_scope():
    changed = changed_files()
    req(not sorted(changed - ALLOWED), f"scope violation: {sorted(changed - ALLOWED)}")
    req("integration/animo-b3/B3D37_TCD039_ADMISSION_CONTRACT.json" in changed, "admission contract missing")
    req("tools/validate_b3d37_tcd039.py" in changed, "validator missing")
    return changed

def validate_readiness():
    s = git_json(BASE, "integration/animo-b3/ANIMO-B3B11_STATUS.json")
    req(s["work_unit"] == "ANIMO-B3B11" and s["target"] == "TCD-039", "wrong readiness authority")
    req(s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI", "B3B11 not closed")
    req(s["readiness_qualified"] is True and s["b3_admitted"] is False, "B3B11 readiness state invalid")
    req(s["resolved_b3_qualification_class"] == "B_LOCAL_RESTART_CHECKPOINT_OMISSION_EXISTING_CONTINUATION_OWNER", "B3B11 class mismatch")
    req(s["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "B3B11 risk mismatch")
    req(s["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty lost")
    req(s["review"]["completed"] is True, "B3B11 review incomplete")
    req(s["review"]["same_agent"] is True and s["review"]["genuinely_independent"] is False, "B3B11 assurance overclaim")
    c = git_json(BASE, "integration/animo-b3/B3B11_TCD039_READINESS_CONTRACT.json")
    req(c["admission_candidate"]["identity"] == "TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_OWNER_RESTORE_N_AND_CONDITIONAL_P", "candidate identity mismatch")
    req(c["admission_candidate"]["p_guard"] == "Ipo == 1", "P guard mismatch")
    req(c["admission_candidate"]["zero_reset_at_arbitrary_restart"] == "FORBIDDEN", "zero-reset rule mismatch")
    req(c["readiness"]["ready_for_separate_tier_c_admission_decision"] is True, "B3B11 not ready for admission decision")

def validate_aggregate():
    s = git_json(RG05M, "integration/animo-reg/ANIMO-RG05M_STATUS.json")
    req(s["work_unit"] == "ANIMO-RG05M", "wrong aggregate authority")
    req(s["scientific_admission_count"] == 26, "unexpected RG05M admission count")
    req(s["b3_complete"] is False and s["b4_open"] is False and s["production_open"] is False, "downstream gate unexpectedly open")

def validate_contract(c):
    req(c["work_unit"] == "ANIMO-B3D37" and c["target"] == "TCD-039", "contract identity")
    req(c["base_authority"] == f"ANIMO-B3B11@{BASE}", "base authority mismatch")
    req(c["aggregate_authority"] == f"ANIMO-RG05M@{RG05M}", "aggregate mismatch")
    req(c["b3_qualification_class"] == "B_LOCAL_RESTART_CHECKPOINT_OMISSION_EXISTING_CONTINUATION_OWNER", "class mismatch")
    req(c["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "risk tier mismatch")
    req(c["candidate_decision"] == "ADMIT_TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C", "decision mismatch")
    req(c["admitted_identity"] == "TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_OWNER_RESTORE_N_AND_CONDITIONAL_P", "admitted identity mismatch")
    req(c["supported_scope"]["guard"] == "Ioptplant == 1", "crop guard mismatch")
    req(c["supported_scope"]["phosphorus"]["guard"] == "Ipo == 1", "P guard mismatch")
    req(c["historical_disposition"]["behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty erased")
    req(c["historical_disposition"]["b1_promoted_to_b2"] is False, "B1 promoted to B2")
    req(c["admission_effect"]["tcd039_top_level_admitted"] is True, "top-level admission effect missing")
    req(c["admission_effect"]["canonical_state_admitted"] is False, "canonical STATE overclaim")
    req(c["aggregate_policy"]["post_RG05M_new_admissions_if_exact_final_green"] == 1, "aggregate cadence mismatch")
    req(c["aggregate_policy"]["aggregate_update_required_after_exact_final_green"] is False, "premature aggregate update")

def validate_status(s):
    req(s["work_unit"] == "ANIMO-B3D37" and s["target"] == "TCD-039", "status identity")
    req(s["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk tier")
    req(s["production_authorized"] is False and s["canonical_state_admitted"] is False, "scope overclaim")
    req(s["tcd038_reopened"] is False and s["crop007_resolved"] is False, "crop scope contamination")
    req(s["historical_b2_created"] is False, "historical B2 created")
    phase = s["phase"]
    req(phase in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, f"unexpected phase {phase}")
    if phase == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        req(s["admitted"] is True and s["qualified"] is True, "final admission missing")
        r = s["review"]
        req(r["completed"] is True and r["same_agent"] is True and r["genuinely_independent"] is False, "final review assurance invalid")
        req(r["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance mismatch")

def main():
    changed = validate_scope()
    validate_readiness()
    validate_aggregate()
    validate_contract(load(CONTRACT))
    validate_status(load(STATUS))
    print("PASS ANIMO-B3D37 TCD-039 bounded Tier-C atomic admission package")
    print(f"changed_files={len(changed)}")

if __name__ == "__main__":
    main()
