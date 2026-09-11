#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "26f6e61da328a5578b9c4b332de04eb99a3ac04f"
B3Q04 = "dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
CONTRACT = ROOT / "integration/animo-b3/B3B13_TCD036_READINESS_CONTRACT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B13_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3b13-tcd036-readiness.yml",
    "docs/b3b13/TCD036_GHG_PONDING_LAYER0_RESTART_READINESS.md",
    "integration/animo-b3/B3B13_TCD036_READINESS_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3B13_STATUS.json",
    "integration/animo-b3/ANIMO-B3B13_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3B13_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3b13_tcd036.py",
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

    sq = git_json(BASE, "integration/animo-state/ANIMO-STATEQ07_STATUS.json")
    req(sq["qualified"] is True and sq["b3_admitted"] is False, "STATEQ07 authority is not qualified state-only evidence")
    req(sq["decision"] == "QUALIFY_TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_RESTART_IDENTITY_FROM_SERIALIZED_TOTAL_SYSTEM_OWNER_ONLY", "STATEQ07 decision mismatch")
    req(sq["candidate_b3_class_after_state_resolution"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "STATEQ07 class mismatch")
    req(sq["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "STATEQ07 risk mismatch")
    req(sq["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "STATEQ07 historical status mismatch")
    qo = sq["qualified_owner_model"]
    req(qo["co_independent_checkpoint_owner"] is False, "STATEQ07 invented second owner")
    req(qo["restart_identity"] == "Co(0)=Cs(0) for active pre-existing ponding only", "STATEQ07 identity mismatch")
    req(qo["new_ponding_source_initialization_preserved"] is True and qo["dormant_layer0_state_when_ponding_absent"] is False, "STATEQ07 lifecycle mismatch")
    req(qo["species_kept_separate"] == ["CH4", "N2O"], "STATEQ07 species mismatch")

    q = git_json(B3Q04, "integration/animo-reg/RG05_B3_QUEUE.json")
    e = next(x for x in q["entries"] if x["tcd"] == "TCD-036")
    req(e["b3_class"] == "C provisional" and e["queue_state"] == "WAITING_ON_STATE", "prior queue classification mismatch")

    c = load(CONTRACT)
    req(c["base_authority"] == f"ANIMO-STATEQ07@{BASE}", "base authority mismatch")
    req(c["candidate_identity"] == "TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_GHG_RESTART_IDENTITY_FROM_SERIALIZED_TOTAL_SYSTEM_OWNER", "identity mismatch")
    req(c["b3_qualification_class"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "resolved class mismatch")
    req(c["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY" and c["strictest_risk_trigger_wins"] is True, "review tier reduced")
    s = c["supported_scope"]
    req(s["layer"] == 0 and s["ponding_state"] == "ACTIVE_PRE_EXISTING_PONDING", "scope mismatch")
    req(s["species"] == ["CH4", "N2O"], "species mismatch")
    req(s["reconstruction"] == "Co(0)=Cs(0)", "reconstruction mismatch")
    g = c["lifecycle_guards"]
    req(g["new_ponding_event"] == "EXCLUDED_KEEP_SOURCE_INFLOW_INITIALIZATION", "new ponding guard lost")
    req(g["ponding_absent"] == "EXCLUDED_NO_DORMANT_LAYER0_GHG_STORE", "no-ponding guard lost")
    req(g["species_cross_mapping"] == "FORBIDDEN" and g["independent_second_co_checkpoint_owner"] == "FORBIDDEN", "ownership/species guard lost")
    ev = c["evidence_strength"]
    req(ev["oracle"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2" and ev["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "evidence overclaim")
    req(c["candidate_readiness_disposition"] == "READY_TCD036_BOUNDED_PRE_EXISTING_PONDING_LAYER0_RESTART_FOR_SEPARATE_ADMISSION", "readiness disposition mismatch")
    req(c["b3_admission_performed"] is False and c["production_authorized"] is False and c["b4_opened"] is False, "premature admission/production")

    st = load(STATUS)
    req(st["resolved_b3_qualification_class"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "status class mismatch")
    req(st["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk mismatch")
    req(st["b3_admitted"] is False and st["production_authorized"] is False, "readiness workunit cannot admit")
    req(st["phase"] in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, "unexpected phase")
    if st["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        req(st["readiness_qualified"] is True and st["review"]["completed"] is True, "final readiness incomplete")
        req(st["review"]["same_agent"] is True and st["review"]["genuinely_independent"] is False and st["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review overclaim")

    print("PASS ANIMO-B3B13 TCD036 bounded admission-readiness contract")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
