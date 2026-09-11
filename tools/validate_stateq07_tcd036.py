#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "c6fe71cfd1822aea5d00a802862e4b3a4a991cd2"
GHG01 = "dac7b7b5c591b781b82ec968896edb5957664c88"
B3Q04 = "dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
CONTRACT = ROOT / "integration/animo-state/TCD036_GHG_PONDING_LAYER0_RESTART_CONTRACT.json"
STATUS = ROOT / "integration/animo-state/ANIMO-STATEQ07_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-stateq07-tcd036-layer0-restart.yml",
    "docs/stateq07/TCD036_GHG_PONDING_LAYER0_RESTART.md",
    "integration/animo-state/TCD036_GHG_PONDING_LAYER0_RESTART_CONTRACT.json",
    "integration/animo-state/ANIMO-STATEQ07_STATUS.json",
    "integration/animo-state/ANIMO-STATEQ07_AUTHORING_FREEZE.json",
    "integration/animo-state/ANIMO-STATEQ07_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/stateq07/tcd036_ponding_layer0_oracle.py",
    "tests/stateq07/test_tcd036_ponding_layer0.py",
    "tools/validate_stateq07_tcd036.py",
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
    ghg = git_json(GHG01, "integration/animo-ghg/GHG_RESTART_STATE_CONTINUITY_AUDIT.json")
    p = ghg["ponding_layer0"]
    req(p["serialized_layer0_total_state"] is True and p["input_reads_layer0_total_state"] is True, "layer0 owner not serialized/read")
    req(p["inicalc_reconstructs_CoCH4_0"] is False and p["inicalc_reconstructs_CoN2O_0"] is False, "legacy gap not established")
    req(p["new_ponding_transport_overwrites_Co0"] is True and p["pre_existing_ponding_transport_overwrites_Co0"] is False, "ponding lifecycle partition mismatch")
    req("ACTIVE_PONDING_GHG_STATE_HAS_EXPLICIT_LAYER0_OWNER_OR_DETERMINISTIC_RECONSTRUCTION" in ghg["arch02_reconciliation"]["strengthened_invariants"], "ARCH02 layer0 invariant missing")
    q = git_json(B3Q04, "integration/animo-reg/RG05_B3_QUEUE.json")
    e = next(x for x in q["entries"] if x["tcd"] == "TCD-036")
    req(e["b3_class"] == "C provisional" and e["queue_state"] == "WAITING_ON_STATE", "prior queue state mismatch")
    req("layer0 GHG owner/reconstruction not admitted" in e["blockers"], "expected blocker missing")
    c = load(CONTRACT)
    req(c["base_authority"] == f"ANIMO-B3D38@{BASE}", "base authority mismatch")
    s = c["supported_scope"]
    req(s["layer"] == 0 and s["ponding_state"] == "ACTIVE_PRE_EXISTING_PONDING", "scope mismatch")
    req(s["species"] == ["CH4", "N2O"], "species mismatch")
    o = c["owner_model"]
    req(o["independent_second_checkpoint_owner_required"] is False, "second owner invented")
    req(o["restart_reconstruction"].startswith("Co(0) = Cs(0)"), "identity reconstruction mismatch")
    life = c["lifecycle_partition"]
    req("source inflow initialization" in life["new_ponding_event"], "new ponding source rule not preserved")
    req("no dormant" in life["ponding_absent"], "dormant state invented")
    cl = c["classification_resolution"]
    req(cl["missing_physical_state_required"] is False and cl["new_phase_or_storage_required"] is False, "new state invented")
    req(cl["deterministic_reconstruction_from_serialized_owner_qualified"] is True, "reconstruction not qualified")
    req(cl["candidate_b3_class_for_later_readiness"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "candidate class mismatch")
    req(cl["review_risk_floor"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY" and cl["scientific_gate_reduced"] is False, "risk/gate reduced")
    req(c["evidence_strength"]["oracle"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2" and c["evidence_strength"]["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "evidence overclaim")
    req(c["b3_admission_performed"] is False, "STATEQ07 cannot admit B3")
    st = load(STATUS)
    req(st["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk mismatch")
    req(st["b3_admitted"] is False and st["production_authorized"] is False and st["tcd035_reopened"] is False, "boundary violation")
    req(st["phase"] in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, "unexpected phase")
    if st["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        req(st["qualified"] is True and st["review"]["completed"] is True, "final qualification incomplete")
        req(st["review"]["same_agent"] is True and st["review"]["genuinely_independent"] is False and st["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review overclaim")
    print("PASS ANIMO-STATEQ07 TCD036 bounded pre-existing ponding layer0 restart qualification")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
