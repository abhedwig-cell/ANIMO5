#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "b930d17d98cd6ec9f6dda1613a7f9aa68148a0d3"
STATEQ06 = "7e4ee6ebdfe168b24414c97df39b2ca76940ea44"
CONTRACT = ROOT / "integration/animo-b3/B3D38_TCD035_ADMISSION_CONTRACT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D38_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3d38-tcd035.yml",
    "docs/b3d38/TCD035_ATOMIC_B3_ADMISSION.md",
    "integration/animo-b3/B3D38_TCD035_ADMISSION_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3D38_STATUS.json",
    "integration/animo-b3/ANIMO-B3D38_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3D38_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3d38_tcd035.py",
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
    b = git_json(BASE, "integration/animo-b3/ANIMO-B3B12_STATUS.json")
    req(b["state"] == "QUALIFIED_TCD035_CLASS_B_ADMISSION_READINESS_TIER_C_DECISION_REQUIRED", "B3B12 not final readiness authority")
    req(b["readiness_qualified"] is True and b["b3_admitted"] is False, "B3B12 boundary mismatch")
    req(b["review"]["completed"] is True and b["review"]["genuinely_independent"] is False, "B3B12 GOV05 review mismatch")
    s6 = git_json(STATEQ06, "integration/animo-state/ANIMO-STATEQ06_STATUS.json")
    req(s6["qualified"] is True and s6["b3_admitted"] is False, "STATEQ06 mismatch")
    req(s6["layer0_tcd036_resolved"] is False, "TCD036 must remain open")
    c = load(CONTRACT)
    req(c["base_authority"] == f"ANIMO-B3B12@{BASE}", "base authority mismatch")
    req(c["state_authority"] == f"ANIMO-STATEQ06@{STATEQ06}", "state authority mismatch")
    req(c["b3_qualification_class"] == "B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER", "class mismatch")
    req(c["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "risk mismatch")
    scope = c["supported_scope"]
    req(scope["layers"] == "1..Nl" and scope["layer0_included"] is False, "scope widened")
    req(scope["species"] == ["CH4", "N2O"], "species mismatch")
    req(scope["source_bunsen_relation_unchanged"] is True and scope["legacy_Terf_general_equivalence_admitted"] is False, "source semantics changed")
    req(c["evidence"]["source_shaped_oracle_cases"] == 72 and c["evidence"]["oracle_strength"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2", "oracle claim mismatch")
    req(c["historical_disposition"]["behavior"] == "UNKNOWN_WITHOUT_B2" and c["historical_disposition"]["b2_created"] is False, "historical overclaim")
    ap = c["aggregate_policy"]
    req(ap["post_RG05M_exact_final_admissions_before_candidate"] == 1 and ap["post_RG05M_exact_final_admissions_if_candidate_green"] == 2, "aggregate count mismatch")
    req(ap["normal_batch_threshold"] == 3 and ap["aggregate_update_required_if_green"] is False, "premature aggregate")
    s = load(STATUS)
    req(s["review_risk_tier"] == "C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY", "status risk mismatch")
    req(s["production_authorized"] is False and s["tcd036_modified_or_admitted"] is False and s["canonical_state_admitted"] is False, "hard boundary")
    req(s["phase"] in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, "unexpected phase")
    if s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        req(s["admitted"] is True and s["qualified"] is True, "final admission missing")
        req(s["review"]["completed"] is True and s["review"]["same_agent"] is True and s["review"]["genuinely_independent"] is False, "review governance mismatch")
        req(s["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance mismatch")
    print("PASS ANIMO-B3D38 TCD035 bounded Tier-C atomic admission package")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
