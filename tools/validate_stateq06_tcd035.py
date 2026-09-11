#!/usr/bin/env python3
import csv
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "8bd1d0a5e20e5fa1d15508e0fdf7c69a5150a84f"
GHG01 = "dac7b7b5c591b781b82ec968896edb5957664c88"
BUILDQ03 = "5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47"
STATEQ01 = "4adae99576eb56978da71f7c8a250e4445fd3bc4"
B3Q04 = "dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
CONTRACT = ROOT / "integration/animo-state/TCD035_GHG_PHASE_RESTART_RECONSTRUCTION_CONTRACT.json"
STATUS = ROOT / "integration/animo-state/ANIMO-STATEQ06_STATUS.json"

ALLOWED = {
    ".github/workflows/animo-stateq06-tcd035-phase-restart.yml",
    "docs/stateq06/TCD035_GHG_PHASE_RESTART_RECONSTRUCTION.md",
    "integration/animo-state/TCD035_GHG_PHASE_RESTART_RECONSTRUCTION_CONTRACT.json",
    "integration/animo-state/ANIMO-STATEQ06_STATUS.json",
    "integration/animo-state/ANIMO-STATEQ06_AUTHORING_FREEZE.json",
    "integration/animo-state/ANIMO-STATEQ06_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/stateq06/tcd035_phase_reconstruction_oracle.py",
    "tests/stateq06/test_tcd035_phase_reconstruction.py",
    "tools/validate_stateq06_tcd035.py",
}


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(commit, path):
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)
    except subprocess.CalledProcessError as exc:
        raise AssertionError(f"cannot load pinned artifact {commit}:{path}") from exc


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return {line.strip() for line in out.splitlines() if line.strip()}


def validate_scope():
    changed = changed_files()
    extra = sorted(changed - ALLOWED)
    require(not extra, f"scope violation: {extra}")
    for p in [
        "docs/stateq06/TCD035_GHG_PHASE_RESTART_RECONSTRUCTION.md",
        "integration/animo-state/TCD035_GHG_PHASE_RESTART_RECONSTRUCTION_CONTRACT.json",
        "tools/stateq06/tcd035_phase_reconstruction_oracle.py",
        "tests/stateq06/test_tcd035_phase_reconstruction.py",
        "tools/validate_stateq06_tcd035.py",
    ]:
        require(p in changed, f"required artifact missing: {p}")
    return changed


def validate_upstream():
    ghg = json.loads(git_text(GHG01, "integration/animo-ghg/GHG_RESTART_STATE_CONTINUITY_AUDIT.json"))
    require(ghg["status"] == "SOURCE_CONFIRMED_GHG_RESTART_PHASE_STATE_DISCONTINUITIES_REFERENCE_UNEXERCISED", "GHG01 restart authority mismatch")
    require(ghg["serialized_ghg_state"]["owner_representation"] == "TOTAL_GAS_WATER_SYSTEM_CONCENTRATION", "GHG owner representation mismatch")
    soil = ghg["restart_soil_phase_partition"]
    require(soil["checkpoint_temperature_used"] is False, "legacy restart unexpectedly uses checkpoint temperature")
    require(soil["reconstruction_temperature"] == "Terf", "legacy reconstruction temperature mismatch")
    require(soil["behavioural_restart_equivalence_established"] is False, "GHG01 must not already establish restart equivalence")
    require(ghg["arch02_reconciliation"]["serialize_both_Cs_and_Co_required"] is False, "Cs/Co ownership mismatch")
    require("GHG_PHASE_VIEW_RECONSTRUCTION_USES_ACCEPTED_CHECKPOINT_THERMODYNAMIC_AND_HYDROLOGY_STATE" in ghg["arch02_reconciliation"]["strengthened_invariants"], "checkpoint coordinate invariant missing")
    require(ghg["ponding_layer0"]["classification"].startswith("SOURCE_CONFIRMED_PONDING_GHG_LAYER0"), "TCD036 boundary missing")

    build = json.loads(git_text(BUILDQ03, "integration/animo-build/ANIMO-BUILDQ03_STATUS.json"))
    phase = build["qualified_runtime_families"]["GHGasses"]
    require(phase["owner"] == "GHG_TIMESTEP_PHASE_CONTEXT", "BUILDQ03 phase context mismatch")
    require(phase["persistent_model_state"] is False, "within-timestep context must not be promoted to checkpoint state")
    require(build["b3_scientific_admitted"] is False, "BUILDQ03 is not B3 admission")

    matrix = git_text(STATEQ01, "integration/animo-state/PERSISTENT_STATE_MATRIX.csv")
    rows = list(csv.DictReader(io.StringIO(matrix)))
    hyd6 = next((r for r in rows if r.get("state_id") == "HYD-006"), None)
    require(hyd6 is not None, "STATEQ01 HYD-006 missing")
    require(hyd6["class"] == "EXTERNAL_OWNER_REFERENCE", "temperature ownership mismatch")
    require("future" in hyd6["checkpoint_requirement"].lower(), "temperature checkpoint condition not preserved")

    queue = json.loads(git_text(B3Q04, "integration/animo-reg/RG05_B3_QUEUE.json"))
    entry = next(e for e in queue["entries"] if e["tcd"] == "TCD-035")
    require(entry["queue_state"] == "WAITING_ON_STATE", "expected pre-STATEQ06 TCD035 queue state")
    require("checkpoint phase owner not admitted" in entry["blockers"], "expected TCD035 owner blocker missing")


def validate_contract(c):
    require(c["work_unit"] == "ANIMO-STATEQ06" and c["target"] == "TCD-035", "contract identity")
    require(c["base_authority"] == f"ANIMO-B3D37@{BASE}", "base authority mismatch")
    s = c["supported_scope"]
    require(s["layers"] == "1..Nl" and s["layer0_included"] is False, "soil/layer0 scope widened")
    require(s["species"] == ["CH4", "N2O"], "species scope mismatch")
    owner = c["owner_model"]
    require(owner["co_independent_checkpoint_owner"] is False, "Co must remain derived")
    require("T_checkpoint" in owner["restart_reconstruction"], "checkpoint temperature missing from reconstruction")
    legacy = c["revision53_restart_defect"]
    require(legacy["reconstruction_temperature"] == "Terf" and legacy["accepted_checkpoint_temperature_used"] is False, "legacy defect mismatch")
    require(len(legacy["exact_continuity_conditions"]) == 3, "continuity controls incomplete")
    cl = c["classification_resolution"]
    require(cl["prior_queue_class"] == "C provisional", "prior class mismatch")
    require(cl["missing_physical_state_required"] is False and cl["new_phase_or_storage_required"] is False, "new state must not be invented")
    require(cl["deterministic_reconstruction_from_accepted_coordinates_qualified"] is True, "bounded reconstruction not qualified")
    require(cl["candidate_b3_class_for_later_readiness"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "candidate class mismatch")
    require(cl["review_risk_floor"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "risk floor reduced")
    require(c["evidence_strength"]["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty erased")
    require(c["evidence_strength"]["oracle"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2", "oracle promoted beyond B1")
    require(c["b3_admission_performed"] is False, "STATEQ06 cannot admit B3")


def validate_status(s):
    require(s["work_unit"] == "ANIMO-STATEQ06" and s["target"] == "TCD-035", "status identity")
    require(s["risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "risk tier mismatch")
    require(s["b3_admitted"] is False and s["production_authorized"] is False, "qualification boundary violated")
    require(s["layer0_tcd036_resolved"] is False, "TCD036 scope contamination")
    require(s["canonical_state_admitted"] is False, "canonical STATE must remain closed")
    require(s["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty mismatch")
    require(s["phase"] in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, "unexpected phase")
    if s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        require(s["qualified"] is True, "final status not qualified")
        r = s["review"]
        require(r["completed"] is True and r["same_agent"] is True and r["genuinely_independent"] is False, "review governance mismatch")
        require(r["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance mismatch")


def main():
    changed = validate_scope()
    validate_upstream()
    validate_contract(load(CONTRACT))
    validate_status(load(STATUS))
    print("PASS ANIMO-STATEQ06 TCD035 bounded GHG phase restart reconstruction qualification")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
