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
RG05E = "eed822037ed8d906a2ab424220597cffac9cca73"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3D12 = "5e33c195174e41ea949d5a828d30bb7b9e313a5d"
B3A01E = "5232ef5fa6daafa2296401b19fd9e866a34152bd"
B3B04E1 = "b3f509806119ea2c2aaf0694c08d4a5bb13e6ca3"

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
    auth = matrix.get("authorities", {})
    require(auth.get("authoring_base_central_regie") == f"ANIMO-RG05D@{RG05D}", "wrong RG05D authoring base")
    require(auth.get("current_central_regie") == f"ANIMO-RG05E@{RG05E}", "wrong current RG05E authority")
    require(auth.get("b3_framework") == f"ANIMO-B3Q01@{B3Q01}", "wrong B3Q01 authority")
    require(auth.get("historical_uncertainty_route") == f"ANIMO-GOV03@{GOV03}", "wrong GOV03 authority")

    semantics = matrix.get("governance_semantics", {})
    require(semantics.get("qualification_class_is_not_risk_tier") is True, "class and risk tier must remain distinct")
    require(semantics.get("strictest_applicable_risk_trigger_wins") is True, "strictest-trigger rule missing")
    require(semantics.get("scientific_gate_reduction_allowed") is False, "scientific gate reduction must be forbidden")
    require(semantics.get("historical_behaviour_without_qualified_b2") == "UNKNOWN", "historical UNKNOWN invariant missing")
    require(set(semantics.get("review_workunit_reduction_allowed_only_by", [])) == {
        "BETTER_RISK_ALLOCATION", "VERIFY_AND_REUSE", "AUTOMATION", "CLEAR_ESCALATION_RULES"
    }, "invalid review-reduction basis")

    require(set(matrix.get("review_stages", [])) == {
        "EVIDENCE_QUALIFICATION",
        "TECHNICAL_REVIEW",
        "GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW",
        "ADMISSION_DECISION",
        "CENTRAL_PROJECT_REGIE_INTEGRATION",
    }, "review stages are incomplete")

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
    require(set(waiver.get("conditions", [])) == required_waiver, "Tier A waiver condition set incomplete or broadened")
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
    require(defaults.get("MISSING_PHYSICAL_STATE_OR_INCOMPLETE_STATE_MODEL") == "C", "state default tier wrong")
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
    require({
        "FAILED_GATES_IDENTIFIED",
        "ALL_REUSED_PRIOR_PASS_GATES_IMMUTABLE",
        "VERIFY_PIN",
        "VERIFY_SCOPE_COMPATIBILITY",
        "VERIFY_NO_SUPERSEDING_EVIDENCE",
        "REGRESSION_GUARDS_INCLUDED",
    }.issubset(set(remediation.get("targeted_rereview_preconditions", []))), "targeted re-review preconditions incomplete")

    independence = matrix.get("independence_policy", {})
    require(independence.get("separate_chatgpt_context_means") == "PROCESS_INDEPENDENCE_ONLY", "separate context semantics wrong")
    require(independence.get("organizational_or_human_independence_implied") is False, "separate context must not imply human independence")
    require(independence.get("same_authoring_context_may_sign_required_independent_gate") is False, "authoring context cannot self-sign independent gate")

    central = matrix.get("central_regie_integration", {})
    require(central.get("starting_aggregate_snapshot") == f"ANIMO-RG05E@{RG05E}", "wrong prospective aggregate starting snapshot")
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

    transitional = matrix.get("transitional_rules", {})
    require(transitional.get("retroactive_invalidation") is False, "GOV04 may not invalidate historical work")
    require(transitional.get("existing_finalized_reviews_remain_valid") is True, "existing reviews must remain valid")
    require(transitional.get("existing_admissions_remain_valid") is True, "existing admissions must remain valid")
    require(transitional.get("existing_fail_or_incomplete_records_rewritten") is False, "existing FAIL/INCOMPLETE records must remain immutable")
    require(transitional.get("historical_rg_snapshots_immutable") == ["RG05", "RG05A", "RG05B", "RG05C", "RG05D", "RG05E"], "finalized RG snapshot immutability missing")

    transition = matrix.get("live_transition_decisions", {})
    t15 = transition.get("TCD-015", {})
    require(t15.get("risk_tier") == "B", "TCD-015 transition tier wrong")
    require(t15.get("transition_state") == "COMPLETED_CONCURRENTLY_NO_GOV04_REOPEN", "TCD-015 concurrent completion not retained")
    require(t15.get("atomic_admission") == f"ANIMO-B3D12@{B3D12}", "TCD-015 admission authority wrong")
    require(t15.get("central_integration") == f"ANIMO-RG05E@{RG05E}", "TCD-015 RG05E integration missing")
    require(t15.get("historical_behaviour") == "UNKNOWN", "TCD-015 historical uncertainty changed")
    require(t15.get("admitted_by_gov04") is False, "GOV04 must not admit TCD-015")

    t27 = transition.get("TCD-027", {})
    require(t27.get("risk_tier") == "A_CANDIDATE_CONDITIONAL", "TCD-027 must be conditional Tier A candidate")
    require(t27.get("qualified_evidence_remediation") == f"ANIMO-B3A01E@{B3A01E}", "TCD-027 remediation packet not pinned")
    require(set(t27.get("remediated_checks", [])) == {
        "EXACT_LOCAL_DUM_CONSTRUCTION_AND_MEANING",
        "EXACT_OUTBAL_WRITE_SLOT_24_TO_27_MAPPING",
        "EXACT_ORGANIC_P_SLOT_25_26_27_SELF_ACCUMULATORS",
    }, "TCD-027 remediated source checks incomplete")
    require(t27.get("new_separate_second_line_required_if_tier_a_waiver_passes") is False, "TCD-027 Tier A waiver semantics wrong")
    require(t27.get("automatic_admission_ready") is False, "GOV04 may not auto-admit TCD-027")

    t40 = transition.get("TCD-040", {})
    require(t40.get("risk_tier") == "C", "TCD-040 must be risk Tier C")
    require(t40.get("live_evidence_remediation") == f"ANIMO-B3B04E1@{B3B04E1}", "TCD-040 remediation head not current")
    require(t40.get("live_remediation_state") == "FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN", "TCD-040 live remediation state not fail closed")
    require(t40.get("independent_review_still_required") is True, "TCD-040 independent review must remain required")
    require(t40.get("scientific_falsification") is False, "TCD-040 failure must not become scientific falsification")

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

    compat = matrix.get("b3q01_schema_compatibility", {})
    require(compat.get("b3q01_schema_modified_by_gov04") is False, "GOV04 must not rewrite B3Q01 schema")
    encoding = compat.get("tier_a_waived_independent_review_encoding", {})
    require(encoding.get("evidence_independent_review_result") == "NOT_REVIEWED", "Tier A waiver must not claim a review occurred")
    require(encoding.get("independent_from_correction_authoring") is False, "Tier A waiver must not claim independent authoring")
    require(encoding.get("gate_status") == "PASS" and encoding.get("gate_applicability") == "NOT_APPLICABLE", "Tier A compatibility gate encoding wrong")
    require(compat.get("admitted_tier_a_not_reviewed_without_verified_waiver") == "FAIL_CLOSED", "unverified Tier A waiver must fail closed")

    b3_schema = git_show_json(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    if b3_schema:
        require("NOT_REVIEWED" in enum_at(b3_schema, "properties", "evidence", "properties", "independent_review", "properties", "result", "enum"), "B3Q01 schema cannot encode NOT_REVIEWED")
        require("NOT_APPLICABLE" in enum_at(b3_schema, "properties", "gates", "properties", "independent_review", "properties", "applicability", "enum"), "B3Q01 schema cannot encode NOT_APPLICABLE")

    gov03_status = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    if gov03_status:
        require(gov03_status.get("qualified_closure_state") == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")
        require(gov03_status.get("route_effect", {}).get("historical_behaviour_without_B2") == "UNKNOWN", "GOV03 historical UNKNOWN changed")

    rg05e_status = git_show_json(RG05E, "integration/animo-reg/ANIMO-RG05E_STATUS.json")
    if rg05e_status:
        adm = rg05e_status.get("admission_state", {})
        require(adm.get("scientific_admissions") == 5, "RG05E scientific admission count wrong")
        require(adm.get("admitted_tcds") == ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015"], "RG05E admitted set wrong")
        require(adm.get("tcd015_historical_behaviour") == "UNKNOWN", "RG05E changed TCD-015 historical uncertainty")
        require(adm.get("b3_whole_model_baseline_complete") is False, "RG05E must leave B3 incomplete")
        require(adm.get("b4_baseline_admitted") is False and adm.get("production_migration_admitted") is False, "RG05E project boundary unexpectedly open")

    b3d12 = git_show_json(B3D12, "integration/animo-b3/ANIMO-B3D12_STATUS.json")
    if b3d12:
        require(b3d12.get("admission", {}).get("scientific_b3_admission_qualified") is True, "B3D12 TCD-015 admission not qualified")
        require(b3d12.get("admission", {}).get("historical_behaviour_status") == "UNKNOWN", "B3D12 historical state wrong")
        require(b3d12.get("admission", {}).get("production_migration_admitted") is False, "B3D12 opened production")

    b3a01e = git_show_json(B3A01E, "integration/animo-b3/ANIMO-B3A01E_STATUS.json")
    if b3a01e:
        require(b3a01e.get("prior_review_result_retained") == "INCOMPLETE", "B3A01E rewrote prior review result")
        require(b3a01e.get("historical_behaviour") == "UNKNOWN", "B3A01E changed historical uncertainty")
        rem = b3a01e.get("evidence_remediation", {})
        require(all(rem.get(k) == "PERSISTED_AND_STRUCTURALLY_VALIDATED" for k in (
            "R1_DUM_LOCAL_CONSTRUCTION",
            "R2_OUTBAL_WRITE_SLOT24_27_MAPPING",
            "R3_P_SLOT25_26_27_SELF_ACCUMULATORS",
        )), "B3A01E three source remediations are not all validated")
        require(b3a01e.get("boundaries", {}).get("admitted") is False, "B3A01E must not admit TCD-027")

    b3b04e1 = git_show_json(B3B04E1, "integration/animo-b3/ANIMO-B3B04E1_STATUS.json")
    if b3b04e1:
        require(b3b04e1.get("status") == "FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN", "B3B04E1 current fail-closed state changed")
        require(b3b04e1.get("decision") == "EVIDENCE_REPLAYABILITY_NOT_QUALIFIED", "B3B04E1 evidence replayability must remain unqualified")
        require(b3b04e1.get("canonical_tcd_status") == "UNRESOLVED_NOT_ADMITTED", "B3B04E1 must not admit TCD-040")

    require(status.get("work_unit") == "ANIMO-GOV04", "wrong status work unit")
    require(status.get("base", {}).get("head") == RG05D, "wrong GOV04 authoring base")
    require(status.get("governance_only") is True, "GOV04 must be governance-only")
    status_auth = status.get("authorities", {})
    require(status_auth.get("authoring_base_central_regie") == f"ANIMO-RG05D@{RG05D}", "status lost RG05D authoring base")
    require(status_auth.get("current_central_regie") == f"ANIMO-RG05E@{RG05E}", "status current central regie wrong")
    discovery = status.get("live_discovery", {})
    require(discovery.get("concurrent_rg05e_detected") is True, "status must record concurrent RG05E")
    require(discovery.get("current_central_regie_head") == RG05E, "status live central head wrong")
    require(discovery.get("current_scientific_admission_count") == 5, "status live admission count wrong")
    require(discovery.get("current_admitted_tcds") == ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015"], "status live admitted set wrong")

    project = status.get("project_boundaries", {})
    require(project.get("scientific_tcd_admissions_performed") == 0, "GOV04 may not perform a TCD admission")
    for key in ("b4_opened", "production_migration_opened", "production_code_modified", "canonical_tcd_register_modified", "frozen_source_modified", "frozen_testcase_modified"):
        require(project.get(key) is False, f"status project boundary violated: {key}")
    history = status.get("historical_boundaries", {})
    require(history.get("historical_behaviour_without_b2") == "UNKNOWN", "status lost historical UNKNOWN")
    require(history.get("existing_reviews_rewritten") is False, "status rewrites reviews")
    require(history.get("existing_admissions_withdrawn") is False, "status withdraws admissions")
    require(history.get("historical_rg_snapshots_modified") is False, "status modifies historical RG snapshots")

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
        "ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73",
        "ANIMO-B3A01E@5232ef5fa6daafa2296401b19fd9e866a34152bd",
        "ANIMO-B3B04E1@b3f509806119ea2c2aaf0694c08d4a5bb13e6ca3",
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
