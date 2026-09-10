#!/usr/bin/env python3
"""Fail-closed validation for ANIMO-GOV04 risk-tiered review governance."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md"
MATRIX_PATH = ROOT / "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json"
STATUS_PATH = ROOT / "integration/animo-governance/ANIMO-GOV04_STATUS.json"

RG05D = "f3d6b9780631bd627f8bca0658a8e3878746e666"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"

EXPECTED_FINAL_DECISION = "QUALIFIED_RISK_TIERED_SCIENTIFIC_REVIEW_POLICY_NO_SCIENTIFIC_GATE_REDUCTION"
PASS_TOKEN = "PASS_GOV04_RISK_TIERED_REVIEW_POLICY"
SCOPE_PASS_TOKEN = "PASS_GOV04_SCOPE_GUARD"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def git_show_json(commit: str, path: str) -> dict:
    try:
        proc = subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(proc.stdout)
    except Exception as exc:
        errors.append(f"cannot inspect pinned authority {commit}:{path}: {exc}")
        return {}


def enum_at(schema: dict, *keys: str) -> list[str]:
    node = schema
    try:
        for key in keys:
            node = node[key]
        return list(node)
    except Exception:
        return []


def main() -> None:
    for path in (POLICY_PATH, MATRIX_PATH, STATUS_PATH):
        require(path.is_file() and path.stat().st_size > 0, f"missing deliverable: {path}")

    if errors:
        finish()
        return

    policy = POLICY_PATH.read_text(encoding="utf-8")
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))

    require(matrix.get("policy_id") == "ANIMO-GOV04", "wrong policy id")
    require(matrix.get("policy_name") == "RISK_TIERED_REVIEW_INTENSITY", "wrong policy name")
    require(matrix.get("policy_version") == 1, "unexpected policy version")
    require(matrix.get("authorities", {}).get("central_regie") == f"ANIMO-RG05D@{RG05D}", "wrong RG05D authority")
    require(matrix.get("authorities", {}).get("b3_framework") == f"ANIMO-B3Q01@{B3Q01}", "wrong B3Q01 authority")
    require(matrix.get("authorities", {}).get("historical_uncertainty_route") == f"ANIMO-GOV03@{GOV03}", "wrong GOV03 authority")

    semantics = matrix.get("governance_semantics", {})
    require(semantics.get("qualification_class_is_not_risk_tier") is True, "class and risk tier must remain distinct")
    require(semantics.get("strictest_applicable_risk_trigger_wins") is True, "strictest-trigger rule missing")
    require(semantics.get("scientific_gate_reduction_allowed") is False, "scientific gate reduction must be forbidden")
    require(semantics.get("historical_behaviour_without_qualified_b2") == "UNKNOWN", "historical UNKNOWN invariant missing")
    require(set(semantics.get("review_workunit_reduction_allowed_only_by", [])) == {
        "BETTER_RISK_ALLOCATION", "VERIFY_AND_REUSE", "AUTOMATION", "CLEAR_ESCALATION_RULES"
    }, "invalid review-reduction basis")

    expected_stages = {
        "EVIDENCE_QUALIFICATION",
        "TECHNICAL_REVIEW",
        "GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW",
        "ADMISSION_DECISION",
        "CENTRAL_PROJECT_REGIE_INTEGRATION",
    }
    require(set(matrix.get("review_stages", [])) == expected_stages, "review stages are incomplete")

    tiers = matrix.get("risk_tiers", {})
    require(set(tiers) == {"A", "B", "C", "D"}, "risk tiers must be exactly A, B, C and D")
    for tier_id in ("A", "B", "C", "D"):
        tier = tiers.get(tier_id, {})
        gates = tier.get("required_gates", [])
        require(isinstance(gates, list) and len(gates) >= 10, f"Tier {tier_id} has insufficient explicit required gates")
        require(len(gates) == len(set(gates)), f"Tier {tier_id} has duplicate required gates")
        require("allowed_review_reuse" in tier, f"Tier {tier_id} missing review reuse policy")
        require("remediation_review_scope" in tier, f"Tier {tier_id} missing remediation scope")
        require("admission_workunit_combination_allowed" in tier, f"Tier {tier_id} missing combination policy")

    require(tiers.get("A", {}).get("independent_second_line_required") is False, "Tier A must permit independent-review waiver")
    require(tiers.get("B", {}).get("independent_second_line_required") is True, "Tier B must require independent review")
    require(tiers.get("C", {}).get("independent_second_line_required") is True, "Tier C must require independent review")
    require(tiers.get("D", {}).get("independent_second_line_required") is True, "Tier D must require independent review")
    require(tiers.get("D", {}).get("automatic_promotion_from_atomic_admission") is False, "Tier D cannot auto-promote atomic admission")

    waiver = matrix.get("tier_a_independent_review_waiver_conditions", {})
    required_waiver = {
        "EXACT_SOURCE_SEAM",
        "UNAMBIGUOUS_PHYSICAL_AND_ACCOUNTING_OWNERSHIP",
        "ATOMICITY",
        "EXACT_CONSERVATION_OR_ACCOUNTING_IDENTITY",
        "EXPECTED_DIFFERENCE_PREDECLARED",
        "PHYSICAL_STATE_NON_INTERFERENCE",
        "PROCESS_FLUX_NON_INTERFERENCE",
        "NO_NUMERICAL_POLICY_CHANGE",
        "NO_SOLVER_OR_TOLERANCE_CHANGE",
        "NO_RESTART_INITIALIZATION_OR_STATE_SEMANTIC_CHANGE",
        "NO_COMPOSITION",
        "NO_UNRESOLVED_SCIENTIFIC_OR_SOURCE_MEANING_AMBIGUITY",
        "REPRODUCIBLE_VALIDATOR",
        "SCOPE_GUARD",
        "NATURAL_OR_QUALIFIED_SYNTHETIC_ACTIVATION",
        "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2",
        "GOV03_ROUTE_CONDITIONS_RETAINED_WHEN_APPLICABLE",
        "NO_PRODUCTION_OR_B4_OR_CANONICAL_REGISTER_CHANGE",
    }
    require(waiver.get("logic") == "ALL_MUST_PASS", "Tier A waiver must require all conditions")
    require(set(waiver.get("conditions", [])) == required_waiver, "Tier A waiver condition set is incomplete or broadened")
    require(waiver.get("on_false_or_unknown") == "WAIVER_DENIED_ESCALATE_BY_STRICTEST_TRIGGER", "Tier A must fail closed on false or unknown gate")

    c_forced = set(tiers.get("C", {}).get("forced_tier_triggers", []))
    require({
        "RESTART_OR_COLD_START_DISCRIMINATION",
        "INITIALIZATION_SEMANTICS",
        "CANONICAL_STATE_OWNERSHIP",
        "CHECKPOINT_SEMANTICS",
        "NUMERICAL_POLICY",
        "SOLVER_OR_TOLERANCE_CHANGE",
        "RUNTIME_BRANCHING_WITH_BEHAVIOURAL_EFFECT",
        "EXACT_ZERO_OR_SINGULAR_DOMAIN_SEMANTICS",
        "AMBIGUOUS_DOMAIN_CONTRACT",
    }.issubset(c_forced), "restart/state/numerical/runtime risks are not all forced to Tier C")

    d_forced = set(tiers.get("D", {}).get("forced_tier_triggers", []))
    require({
        "COMPOSITION_OF_MULTIPLE_ADMITTED_TCDS",
        "MULTI_TCD_CHANGE",
        "CROSS_MODULE_COUPLING",
        "PRODUCTION_SOURCE_MIGRATION",
        "B4_QUALIFICATION_OR_AUTHORIZATION",
        "WHOLE_MODEL_BASELINE_CLAIM",
        "PRODUCTION_BOUND_CHANGE",
    }.issubset(d_forced), "composition/production risks are not all forced to Tier D")

    defaults = matrix.get("qualification_class_defaults", {})
    require(defaults.get("A_ACCOUNTING_REPORTING_ONLY") == "A", "Class A default tier wrong")
    require(defaults.get("B_LOCAL_ALGEBRA_INDEX_SPECIES") == "B", "Class B default tier wrong")
    require(defaults.get("MISSING_PHYSICAL_STATE_OR_INCOMPLETE_STATE_MODEL") == "C", "Class C state default tier wrong")
    require(defaults.get("NUMERICAL_POLICY_CHANGE") == "C", "numerical policy default tier wrong")
    require(defaults.get("PHYSICS_MODEL_EVOLUTION") == "C", "physics evolution must not be low-risk")

    reuse = matrix.get("review_reuse", {})
    require(reuse.get("mode") == "VERIFY_AND_REUSE", "VERIFY_AND_REUSE missing")
    require(reuse.get("reperform_everything_default") is False, "REPERFORM_EVERYTHING must not be default")
    require(set(reuse.get("mandatory_downstream_checks", [])) == {
        "VERIFY_PIN", "VERIFY_SCOPE_COMPATIBILITY", "VERIFY_NO_SUPERSEDING_EVIDENCE"
    }, "review reuse verification checks incomplete")
    require(reuse.get("evidence_strength_promotion_allowed") is False, "review reuse may not promote evidence strength")

    remediation = matrix.get("remediation_policy", {})
    require(remediation.get("principle") == "REVIEW_FAIL != AUTOMATIC_FULL_REVIEW_RESET", "review reset principle missing")
    failure = remediation.get("failure_classes", {})
    require(set(failure) == {
        "SCIENTIFIC_FALSIFICATION",
        "EVIDENCE_INSUFFICIENCY",
        "PROVENANCE_INSUFFICIENCY",
        "TOOLING_VALIDATOR_FAILURE",
        "SCOPE_AMBIGUITY",
    }, "failure taxonomy incomplete")
    require(failure.get("SCIENTIFIC_FALSIFICATION", {}).get("targeted_rereview_allowed") is False, "scientific falsification cannot use targeted re-review")
    require(failure.get("SCIENTIFIC_FALSIFICATION", {}).get("full_substantive_reassessment_required") is True, "scientific falsification must require full reassessment")
    for key in ("EVIDENCE_INSUFFICIENCY", "PROVENANCE_INSUFFICIENCY", "TOOLING_VALIDATOR_FAILURE"):
        require(failure.get(key, {}).get("targeted_rereview_allowed") is True, f"{key} must allow targeted remediation review")
    require(failure.get("SCOPE_AMBIGUITY", {}).get("scope_mutation_requires_full_substantive_reassessment") is True, "scope mutation must require full reassessment")
    targeted_pre = set(remediation.get("targeted_rereview_preconditions", []))
    require({
        "FAILED_GATES_IDENTIFIED",
        "ALL_REUSED_PRIOR_PASS_GATES_IMMUTABLE",
        "VERIFY_PIN",
        "VERIFY_SCOPE_COMPATIBILITY",
        "VERIFY_NO_SUPERSEDING_EVIDENCE",
        "REGRESSION_GUARDS_INCLUDED",
    }.issubset(targeted_pre), "targeted re-review preconditions incomplete")

    independence = matrix.get("independence_policy", {})
    require(independence.get("separate_chatgpt_context_means") == "PROCESS_INDEPENDENCE_ONLY", "separate context semantics wrong")
    require(independence.get("organizational_or_human_independence_implied") is False, "separate context must not imply human independence")
    require(independence.get("same_authoring_context_may_sign_required_independent_gate") is False, "authoring context cannot self-sign independent gate")

    central = matrix.get("central_regie_integration", {})
    require(central.get("normal_batch_min") == 3 and central.get("normal_batch_max") == 5, "central integration cadence must be 3 to 5 admissions")
    require(central.get("aggregate_before_exceeding_pending_count") == 5, "central aggregation upper bound wrong")
    require(central.get("atomic_admission_authority_equals_latest_aggregate_regie_snapshot") is False, "atomic admission must remain distinct from aggregate snapshot")
    require(central.get("atomic_admission_is_authoritative_before_aggregate_integration") is True, "atomic authority must survive pending aggregation")
    require(central.get("information_loss_allowed") is False, "RG aggregation may not lose information")
    require({
        "B3_COMPLETENESS_CHANGES",
        "B4_ELIGIBILITY_CHANGES",
        "PRODUCTION_ELIGIBILITY_CHANGES",
        "CANONICAL_ROUTING_CHANGES",
    }.issubset(set(central.get("early_integration_triggers", []))), "early RG integration gate triggers incomplete")

    transition = matrix.get("live_transition_decisions", {})
    require(transition.get("TCD-015", {}).get("risk_tier") == "B", "TCD-015 transition tier wrong")
    require("a6880282e9ed743f97a3435b55e4fb54f7d55a44" in transition.get("TCD-015", {}).get("independent_review", ""), "TCD-015 independent PASS not pinned")
    require(transition.get("TCD-027", {}).get("risk_tier") == "A_CANDIDATE_CONDITIONAL", "TCD-027 must be conditional Tier A candidate")
    require(transition.get("TCD-027", {}).get("new_separate_second_line_required_if_tier_a_waiver_passes") is False, "TCD-027 Tier A waiver semantics wrong")
    require(len(transition.get("TCD-027", {}).get("unresolved_checks_to_close", [])) == 3, "TCD-027 unresolved source checks not retained")
    require(transition.get("TCD-040", {}).get("risk_tier") == "C", "TCD-040 must be risk Tier C")
    require(transition.get("TCD-040", {}).get("independent_review_still_required") is True, "TCD-040 independent review must remain required")
    require(transition.get("TCD-040", {}).get("scientific_falsification") is False, "TCD-040 review failure must not be rewritten as scientific falsification")

    hard = matrix.get("hard_invariants", {})
    for key in (
        "scientific_gates_removed",
        "b2_fabricated",
        "historical_uncertainty_promoted_to_fidelity",
        "existing_fails_rewritten",
        "existing_admissions_withdrawn",
        "b4_opened",
        "production_migration_opened",
        "canonical_tcd_register_modified",
        "production_source_modified",
        "open_scientific_blockers_administratively_removed",
        "tcd_admission_performed_by_gov04",
    ):
        require(hard.get(key) is False, f"hard invariant violated or missing: {key}")

    transitional = matrix.get("transitional_rules", {})
    require(transitional.get("retroactive_invalidation") is False, "GOV04 may not invalidate historical work")
    require(transitional.get("existing_finalized_reviews_remain_valid") is True, "existing reviews must remain valid")
    require(transitional.get("existing_admissions_remain_valid") is True, "existing admissions must remain valid")
    require(transitional.get("existing_fail_or_incomplete_records_rewritten") is False, "existing FAIL/INCOMPLETE records must remain immutable")
    require(transitional.get("historical_rg_snapshots_immutable") == ["RG05", "RG05A", "RG05B", "RG05C", "RG05D"], "historical RG snapshot immutability missing")

    compat = matrix.get("b3q01_schema_compatibility", {})
    require(compat.get("b3q01_schema_modified_by_gov04") is False, "GOV04 must not rewrite B3Q01 schema")
    encoding = compat.get("tier_a_waived_independent_review_encoding", {})
    require(encoding.get("evidence_independent_review_result") == "NOT_REVIEWED", "Tier A waiver must not claim a review occurred")
    require(encoding.get("independent_from_correction_authoring") is False, "Tier A waiver must not claim independent authoring")
    require(encoding.get("gate_status") == "PASS" and encoding.get("gate_applicability") == "NOT_APPLICABLE", "Tier A compatibility gate encoding wrong")
    require(compat.get("admitted_tier_a_not_reviewed_without_verified_waiver") == "FAIL_CLOSED", "unverified Tier A waiver must fail closed")

    b3_schema = git_show_json(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    if b3_schema:
        review_result_enum = enum_at(
            b3_schema,
            "properties", "evidence", "properties", "independent_review", "properties", "result", "enum"
        )
        gate_applicability_enum = enum_at(
            b3_schema,
            "properties", "gates", "properties", "independent_review", "properties", "applicability", "enum"
        )
        require("NOT_REVIEWED" in review_result_enum, "B3Q01 schema cannot encode NOT_REVIEWED")
        require("NOT_APPLICABLE" in gate_applicability_enum, "B3Q01 schema cannot encode NOT_APPLICABLE independent review")

    gov03_status = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    if gov03_status:
        require(gov03_status.get("qualified_closure_state") == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")
        require(gov03_status.get("route_effect", {}).get("historical_behaviour_without_B2") == "UNKNOWN", "GOV03 historical UNKNOWN changed")

    rg05d_status = git_show_json(RG05D, "integration/animo-reg/ANIMO-RG05D_STATUS.json")
    if rg05d_status:
        adm = rg05d_status.get("admission_state", {})
        require(adm.get("scientific_admissions") == 4, "RG05D scientific admission count changed")
        require(adm.get("admitted_tcds") == ["TCD-017", "TCD-018", "TCD-024", "TCD-026"], "RG05D admitted set changed")
        require(adm.get("b4_baseline_admitted") is False and adm.get("production_migration_admitted") is False, "RG05D project boundary unexpectedly open")

    require(status.get("work_unit") == "ANIMO-GOV04", "wrong status work unit")
    require(status.get("base", {}).get("head") == RG05D, "wrong GOV04 base")
    require(status.get("governance_only") is True, "GOV04 must be governance-only")
    project = status.get("project_boundaries", {})
    require(project.get("scientific_tcd_admissions_performed") == 0, "GOV04 may not perform a TCD admission")
    for key in (
        "b4_opened",
        "production_migration_opened",
        "production_code_modified",
        "canonical_tcd_register_modified",
        "frozen_source_modified",
        "frozen_testcase_modified",
    ):
        require(project.get(key) is False, f"status project boundary violated: {key}")
    history = status.get("historical_boundaries", {})
    require(history.get("historical_behaviour_without_b2") == "UNKNOWN", "status lost historical UNKNOWN")
    require(history.get("existing_reviews_rewritten") is False, "status rewrites reviews")
    require(history.get("existing_admissions_withdrawn") is False, "status withdraws admissions")
    require(history.get("historical_rg_snapshots_modified") is False, "status modifies historical RG snapshots")

    pending_state = "IN_PROGRESS_PERSISTED_RISK_TIERED_REVIEW_POLICY_VALIDATION_PENDING"
    if status.get("state") == pending_state:
        require(status.get("decision") == "PENDING_FAIL_CLOSED_VALIDATION", "pending status decision wrong")
        require(status.get("work_status", {}).get("tested") is False, "pending status cannot claim tested")
        require(status.get("work_status", {}).get("qualified") is False, "pending status cannot claim qualified")
    else:
        require(status.get("state") == EXPECTED_FINAL_DECISION, "unexpected qualified state")
        require(status.get("decision") == EXPECTED_FINAL_DECISION, "unexpected qualified decision")
        work = status.get("work_status", {})
        require(work.get("realized") and work.get("persisted") and work.get("tested") and work.get("qualified") and work.get("work_unit_complete"), "qualified work status incomplete")
        validation = status.get("validation", {})
        require(validation.get("github_actions_conclusion") == "success", "qualified status lacks successful workflow")
        require(validation.get("validator_result") == PASS_TOKEN, "qualified status has wrong validator token")
        require(validation.get("scope_guard") == SCOPE_PASS_TOKEN, "qualified status has wrong scope guard token")
        require(isinstance(validation.get("github_actions_run_id"), int), "qualified status missing run id")
        require(isinstance(validation.get("github_actions_job_id"), int), "qualified status missing job id")
        require(isinstance(validation.get("tested_head"), str) and len(validation.get("tested_head")) == 40, "qualified status missing tested head")

    for token in (
        "RISK_TIERED_REVIEW_INTENSITY",
        "VERIFY_AND_REUSE",
        "REVIEW_FAIL != AUTOMATIC_FULL_REVIEW_RESET",
        "atomic admission authority != latest aggregate regie snapshot",
        "process independence only",
        "historical behaviour remains `UNKNOWN`",
        "TCD-015",
        "TCD-027",
        "TCD-040",
    ):
        require(token.lower() in policy.lower(), f"policy document missing required concept: {token}")

    finish()


def finish() -> None:
    if errors:
        print("FAIL_GOV04_RISK_TIERED_REVIEW_POLICY")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(PASS_TOKEN)


if __name__ == "__main__":
    main()
