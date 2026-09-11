#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "202a2983d1cce07682eaa95825891fc33e4f6398"
STATEQ07 = "26f6e61da328a5578b9c4b332de04eb99a3ac04f"
B3D37 = "8bd1d0a5e20e5fa1d15508e0fdf7c69a5150a84f"
B3D38 = "c6fe71cfd1822aea5d00a802862e4b3a4a991cd2"
CONTRACT = ROOT / "integration/animo-b3/B3D39_TCD036_ADMISSION_CONTRACT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D39_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3d39-tcd036.yml",
    "docs/b3d39/TCD036_ATOMIC_B3_ADMISSION.md",
    "integration/animo-b3/B3D39_TCD036_ADMISSION_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3D39_STATUS.json",
    "integration/animo-b3/ANIMO-B3D39_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3D39_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3d39_tcd036.py",
}


def req(cond, msg):
    if not cond:
        raise AssertionError(msg)


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def git_json(commit, path):
    return json.loads(subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True))


def main():
    changed = {x for x in subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True).splitlines() if x}
    req(not (changed - ALLOWED), f"scope violation {sorted(changed - ALLOWED)}")

    b = git_json(BASE, "integration/animo-b3/ANIMO-B3B13_STATUS.json")
    req(b["state"] == "QUALIFIED_TCD036_CLASS_B_LAYER0_RESTART_IDENTITY_READY_FOR_SEPARATE_GOV05_TIER_C_ADMISSION", "B3B13 not final readiness authority")
    req(b["readiness_qualified"] is True and b["b3_admitted"] is False, "B3B13 boundary mismatch")
    req(b["resolved_b3_qualification_class"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "B3B13 class mismatch")
    req(b["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "B3B13 risk mismatch")
    req(b["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "B3B13 historical mismatch")
    req(b["review"]["completed"] is True and b["review"]["same_agent"] is True and b["review"]["genuinely_independent"] is False, "B3B13 GOV05 review mismatch")

    s7 = git_json(STATEQ07, "integration/animo-state/ANIMO-STATEQ07_STATUS.json")
    req(s7["qualified"] is True and s7["b3_admitted"] is False, "STATEQ07 mismatch")
    qo = s7["qualified_owner_model"]
    req(qo["restart_identity"] == "Co(0)=Cs(0) for active pre-existing ponding only", "STATEQ07 identity mismatch")
    req(qo["co_independent_checkpoint_owner"] is False, "second checkpoint owner introduced")
    req(qo["new_ponding_source_initialization_preserved"] is True and qo["dormant_layer0_state_when_ponding_absent"] is False, "lifecycle guards mismatch")
    req(qo["species_kept_separate"] == ["CH4", "N2O"], "gas identities mismatch")

    c = load(CONTRACT)
    req(c["base_authority"] == f"ANIMO-B3B13@{BASE}", "base authority mismatch")
    req(c["state_authority"] == f"ANIMO-STATEQ07@{STATEQ07}", "state authority mismatch")
    req(c["b3_qualification_class"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "class mismatch")
    req(c["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY" and c["strictest_risk_trigger_wins"] is True, "risk mismatch")
    req(c["candidate_decision"] == "ADMIT_TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_RESTART_IDENTITY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C", "decision mismatch")
    req(c["admitted_identity_if_green"] == "TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_GHG_RESTART_IDENTITY_FROM_SERIALIZED_TOTAL_SYSTEM_OWNER", "identity mismatch")
    sc = c["supported_scope"]
    req(sc["layer"] == 0 and sc["ponding_state"] == "ACTIVE_PRE_EXISTING_PONDING", "scope widened")
    req(sc["species"] == ["CH4", "N2O"], "species mismatch")
    req(sc["reconstruction"] == "Co(0)=Cs(0)" and sc["independent_second_co_checkpoint_owner"] is False, "ownership mismatch")
    req(sc["new_ponding_source_initialization_preserved"] is True and sc["dormant_layer0_state_when_ponding_absent"] is False, "lifecycle semantics changed")
    req(sc["species_cross_mapping"] is False, "species cross-mapping allowed")
    ev = c["evidence"]
    req(ev["stateq07_exact_final"] is True and ev["b3b13_exact_final"] is True, "required exact-final evidence missing")
    req(ev["oracle_strength"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2" and ev["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "evidence overclaim")
    req(ev["whole_model_split_run"] is False, "whole-model split-run overclaim")
    ap = c["aggregate_policy"]
    req(ap["post_RG05M_exact_final_admissions_before_candidate"] == 2 and ap["post_RG05M_exact_final_admissions_if_candidate_green"] == 3, "aggregate count mismatch")
    req(ap["existing_post_RG05M_admissions"] == [f"ANIMO-B3D37@{B3D37}:TCD-039", f"ANIMO-B3D38@{B3D38}:TCD-035"], "post-RG05M authority mismatch")
    req(ap["normal_batch_threshold"] == 3 and ap["aggregate_update_required_if_green"] is True, "aggregate trigger mismatch")
    req(ap["next_aggregate_when_threshold_reached"] == "ANIMO-RG05N" and ap["fourth_scientific_admission_before_RG05N"] == "FORBIDDEN", "aggregation governance mismatch")
    hd = c["historical_disposition"]
    req(hd["behavior"] == "UNKNOWN_WITHOUT_B2" and hd["b2_created"] is False, "historical overclaim")

    s = load(STATUS)
    req(s["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk mismatch")
    req(s["production_authorized"] is False and s["tcd035_reopened"] is False and s["tcd032_034_modified_or_admitted"] is False, "hard boundary violated")
    req(s["canonical_state_admitted"] is False and s["whole_model_split_run_claimed"] is False and s["b4_opened"] is False, "scope overclaim")
    req(s["phase"] in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, "unexpected phase")
    if s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        req(s["admitted"] is True and s["qualified"] is True, "final admission missing")
        req(s["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "final state mismatch")
        req(s["review"]["completed"] is True and s["review"]["same_agent"] is True and s["review"]["genuinely_independent"] is False, "review governance mismatch")
        req(s["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance mismatch")
        req(s["aggregate_policy"]["aggregate_update_required_if_green"] is True, "RG05N trigger lost")

    print("PASS ANIMO-B3D39 TCD036 bounded Tier-C atomic admission package")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
