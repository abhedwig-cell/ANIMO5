#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "integration/animo-science/NQ04_TCD029_POLICY.json"
STATUS = ROOT / "integration/animo-science/ANIMO-NQ04_STATUS.json"
FREEZE = ROOT / "integration/animo-science/ANIMO-NQ04_AUTHORING_FREEZE.json"
REVIEW = ROOT / "integration/animo-science/NQ04_GOV05_ADVERSARIAL_REVIEW.json"
DOC = ROOT / "docs/numerics/TCD029_IFLSOL4_COEFFICIENT_QUALIFICATION.md"
ORACLE = ROOT / "tools/nq04/tcd029_coefficient_oracle.py"
BASE = "9ca23f41dc3c28af686b1bc0bff8e7d66416d367"

ALLOWED = {
    "docs/numerics/TCD029_IFLSOL4_COEFFICIENT_QUALIFICATION.md",
    "integration/animo-science/NQ04_TCD029_POLICY.json",
    "integration/animo-science/ANIMO-NQ04_STATUS.json",
    "integration/animo-science/ANIMO-NQ04_AUTHORING_FREEZE.json",
    "integration/animo-science/NQ04_GOV05_ADVERSARIAL_REVIEW.json",
    "tools/nq04/tcd029_coefficient_oracle.py",
    "tools/nq04/validate_nq04.py",
    ".github/workflows/animo-nq04-tcd029.yml",
}

def load(path):
    return json.loads(path.read_text())

def need(condition, message):
    if not condition:
        raise AssertionError(message)

def validate_policy(p):
    need(p["work_unit"] == "ANIMO-NQ04", "wrong work unit")
    need(p["target"] == "TCD-029", "wrong target")
    need(p["qualification_class"] == "E_NUMERICAL_POLICY", "wrong class")
    need(p["risk_tier"] == "C", "numerical policy must be Tier C")
    need(p["frozen_identity"]["source_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "source identity drift")
    need(p["frozen_identity"]["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "testbank identity drift")
    need(p["evaluation_policy"]["series_region"] == "abs(x) <= 0.25", "series region drift")
    need(p["evaluation_policy"]["series_degree"] == 24, "series degree drift")
    need(p["oracle"]["deterministic_points"] == 4756, "oracle point count drift")
    need(p["oracle"]["relative_verification_bound_u"] == 128.0, "oracle bound drift")
    need(p["oracle"]["verification_bound_role"] == "EQUATION_EVALUATION_ONLY_NOT_MODEL_ACCEPTANCE_TOLERANCE", "verification bound misuse")
    need(p["evidence_semantics"]["mass_balance_improvement_is_acceptance_criterion"] is False, "mass balance cannot define numerical correctness")
    need(p["evidence_semantics"]["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty lost")
    for key, value in p["hard_boundaries"].items():
        if key.endswith("_allowed") or key.endswith("_modified") or key.endswith("_performed") or key.endswith("_qualified") or key.endswith("_changed") or key.endswith("_opened") or key.endswith("_authorized"):
            need(value is False, f"hard boundary opened: {key}")

def validate_status(s, review_exists):
    need(s["work_unit"] == "ANIMO-NQ04", "status wrong work unit")
    need(s["target"] == "TCD-029", "status wrong target")
    need(s["qualification_class"] == "E_NUMERICAL_POLICY", "status wrong class")
    need(s["review_risk_tier"] == "C_NUMERICAL_POLICY", "status wrong review tier")
    need(s["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty lost")
    need(s["admission"]["tcd029_b3_admitted"] is False, "NQ04 cannot admit TCD029")
    need(s["admission"]["production_implementation_authorized"] is False, "NQ04 cannot authorize production")
    if review_exists:
        need(s["review"]["started"] is True and s["review"]["completed"] is True, "review artifact exists but status not closed")
        need(s["review"]["genuinely_independent"] is False, "same-agent review cannot be independent")
        need(s["work_status"]["reviewed"] is True, "reviewed flag missing")
        need(s["work_status"]["qualified"] is True, "qualified flag missing")
        need(s["work_status"]["work_unit_complete"] is True, "workunit completion missing")
    else:
        need(s["review"]["completed"] is False, "status claims review without artifact")
        need(s["work_status"]["qualified"] is False, "pre-review status cannot be qualified")

def validate_freeze(f):
    need(f["work_unit"] == "ANIMO-NQ04", "freeze wrong work unit")
    need(f["base_head"] == "ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367", "freeze base drift")
    need(f["production_source_changes_allowed"] is False, "production scope opened")
    need(f["b3_admission_allowed"] is False, "admission scope opened")
    need(f["review_must_bind_exact_authoring_head"] is True, "review head binding missing")
    need(f["exact_final_head_ci_required"] is True, "exact-final CI missing")

def validate_review(r, status):
    need(r["work_unit"] == "ANIMO-NQ04", "review wrong work unit")
    need(r["risk_tier"] == "C", "review wrong tier")
    need(r["review_mode"] == "INTERNAL_ADVERSARIAL_REVIEW", "wrong review mode")
    need(r["assurance_label"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT", "wrong assurance")
    need(r["same_agent"] is True and r["independence_claimed"] is False, "independence semantics violated")
    need(len(r["reviewed_authoring_head"]) == 40, "reviewed head missing")
    need(r["review_boundary"]["complete_authoring_package_persisted"] is True, "authoring package not persisted")
    need(r["review_boundary"]["immutable_head_frozen_before_review"] is True, "head not frozen")
    need(r["review_boundary"]["authoring_head_matches_reviewed_head"] is True, "moving tree reviewed")
    need(r["review_boundary"]["moving_tree_reviewed"] is False, "moving tree reviewed")
    for value in r["evidence_reuse_checks"].values():
        need(value == "PASS", "evidence reuse failure")
    need(r["counter_hypothesis"]["tested"] is True, "counter-hypothesis not tested")
    need(r["counter_hypothesis"]["result"] == "ALTERNATIVE_REJECTED_BY_PINNED_EVIDENCE", "counter-hypothesis unresolved")
    for gate, record in r["scientific_gates"].items():
        if record["applicability"] == "APPLICABLE":
            need(record["result"] == "PASS", f"scientific gate failed: {gate}")
        else:
            need(record["result"] == "NOT_APPLICABLE", f"bad N/A gate: {gate}")
    for gate, result in r["adversarial_gates"].items():
        need(result == "PASS", f"adversarial gate failed: {gate}")
    t = r["tier_c_enhanced"]
    for key in (
        "immutable_authoring_checkpoint",
        "complete_source_state_ownership_reconstruction",
        "first_read_first_write_or_restore_direction_analysis",
        "counter_hypothesis_test",
        "active_controls",
        "negative_controls",
        "regression_guard",
    ):
        need(t[key] == "PASS", f"tier C gate failed: {key}")
    need(t["split_run_or_restart_evidence"]["applicability"] == "NOT_APPLICABLE", "restart applicability wrong")
    need(t["split_run_or_restart_evidence"]["result"] == "NOT_APPLICABLE", "restart result wrong")
    need(t["no_invented_tolerance"] is True, "invented tolerance")
    need(t["regression_surface_declared"] is True, "regression surface missing")
    need(t["exact_final_head_ci_required"] is True, "exact final CI not required")
    need(r["outcome"] == "SELF_REVIEW_PASS", "review did not pass")
    need(status["validation"]["immutable_authoring_head"] == r["reviewed_authoring_head"], "status/review head mismatch")

def scope_guard():
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"{BASE}..HEAD"],
            cwd=ROOT, text=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise AssertionError("scope guard could not compare against B3D35 base")
    changed = {line.strip() for line in out.splitlines() if line.strip()}
    unexpected = changed - ALLOWED
    need(not unexpected, f"unexpected NQ04 paths: {sorted(unexpected)}")
    need(not any(path.startswith("src/") for path in changed), "production source changed")
    return sorted(changed)

def main():
    for p in (POLICY, STATUS, FREEZE, DOC, ORACLE):
        need(p.exists(), f"missing {p.relative_to(ROOT)}")
    policy = load(POLICY)
    status = load(STATUS)
    freeze = load(FREEZE)
    validate_policy(policy)
    validate_freeze(freeze)
    validate_status(status, REVIEW.exists())

    text = DOC.read_text()
    for token in (
        "UNKNOWN_WITHOUT_B2",
        "abs(x)<=1/4",
        "128u",
        "not an acceptance criterion",
        "does not perform B3 admission",
        "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT",
    ):
        need(token in text, f"documentation missing token: {token}")

    oracle = json.loads(subprocess.check_output([sys.executable, str(ORACLE)], text=True))
    need(oracle["result"] == "PASS", "oracle failed")
    need(oracle["deterministic_points"] == 4756, "oracle count mismatch")
    need(max(oracle["max_relative_error_u"].values()) <= 128.0, "oracle bound exceeded")

    if REVIEW.exists():
        validate_review(load(REVIEW), status)

    changed = scope_guard()
    print(json.dumps({
        "work_unit": "ANIMO-NQ04",
        "target": "TCD-029",
        "review_present": REVIEW.exists(),
        "changed_paths": changed,
        "oracle_max_relative_error_u": oracle["max_relative_error_u"],
        "result": "PASS",
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
