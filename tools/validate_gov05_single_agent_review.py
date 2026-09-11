#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-GOV05 single-agent adversarial review governance."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "331f6ed91d4a1c15a23ae0c1ad75d1b540f61858"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"

POLICY = ROOT / "docs/governance/ANIMO_GOV05_SINGLE_AGENT_REVIEW_POLICY.md"
MATRIX = ROOT / "integration/animo-governance/GOV05_REVIEW_ASSURANCE_MATRIX.json"
STATUS = ROOT / "integration/animo-governance/ANIMO-GOV05_STATUS.json"
SCHEMA = ROOT / "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW_SCHEMA.json"
TRANSITION = ROOT / "integration/animo-governance/GOV05_OPEN_REVIEW_TRANSITION.json"
REVIEW = ROOT / "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW.json"
WORKFLOW = ROOT / ".github/workflows/animo-gov05-single-agent-review.yml"

ALLOWED_BRANCH_DIFF = {
    "docs/governance/ANIMO_GOV05_SINGLE_AGENT_REVIEW_POLICY.md",
    "integration/animo-governance/GOV05_REVIEW_ASSURANCE_MATRIX.json",
    "integration/animo-governance/ANIMO-GOV05_STATUS.json",
    "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW_SCHEMA.json",
    "integration/animo-governance/GOV05_OPEN_REVIEW_TRANSITION.json",
    "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_gov05_single_agent_review.py",
    ".github/workflows/animo-gov05-single-agent-review.yml",
}
SUBSTANTIVE_REVIEWED_PATHS = {
    "docs/governance/ANIMO_GOV05_SINGLE_AGENT_REVIEW_POLICY.md",
    "integration/animo-governance/GOV05_REVIEW_ASSURANCE_MATRIX.json",
    "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW_SCHEMA.json",
    "integration/animo-governance/GOV05_OPEN_REVIEW_TRANSITION.json",
    "tools/validate_gov05_single_agent_review.py",
    ".github/workflows/animo-gov05-single-agent-review.yml",
}
POST_REVIEW_ALLOWED = {
    "integration/animo-governance/ANIMO-GOV05_STATUS.json",
    "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW.json",
}

EXPECTED_SOURCE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_GUIDE = "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"

TIER_A_PREDICATES = [
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
]
TIER_B_GOV04 = [
    "B0_IDENTITY",
    "B1_CAUSAL_EVIDENCE",
    "B2_ROUTE_OR_GOV03_HISTORICAL_UNCERTAINTY_ROUTE",
    "ATOMICITY",
    "EXACT_CAUSAL_CODE_PATH_AND_TRIGGER",
    "MATHEMATICAL_OR_SPECIES_IDENTITY",
    "EXPECTED_DIFFERENCE_PREDECLARED",
    "BRANCH_ACTIVATION",
    "CONSERVATION_WHERE_APPLICABLE",
    "NON_INTERFERENCE",
    "ONE_GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW",
    "RESIDUAL_UNCERTAINTY_EXPLICIT",
    "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2",
    "NO_NUMERICAL_STATE_RESTART_OR_PRODUCTION_SCOPE_CREEP",
]
TIER_C_GOV04 = [
    "B0_IDENTITY",
    "B1_CAUSAL_EVIDENCE_WHERE_APPLICABLE",
    "B2_ROUTE_OR_GOV03_HISTORICAL_UNCERTAINTY_ROUTE",
    "AUTHORITATIVE_THEORY_OR_EXACT_DOMAIN_CONTRACT",
    "STATE_OWNERSHIP_AND_UNITS_WHERE_APPLICABLE",
    "INITIALIZATION_AND_RESTART_SEMANTICS_WHERE_APPLICABLE",
    "NUMERICAL_POLICY_AND_CONVERGENCE_EVIDENCE_WHERE_APPLICABLE",
    "FAILURE_AND_FALLBACK_BEHAVIOUR_WHERE_APPLICABLE",
    "EXPECTED_DIFFERENCE_PREDECLARED",
    "CONSERVATION",
    "NON_INTERFERENCE",
    "EDGE_AND_BOUNDARY_CASE_COVERAGE",
    "GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW",
    "RESIDUAL_UNCERTAINTY_EXPLICIT",
    "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2",
    "NO_PRODUCTION_AUTHORIZATION",
]
TIER_D_GOV04 = [
    "ALL_COMPONENT_ADMISSIONS_PINNED",
    "NO_CONTRADICTORY_ASSUMPTIONS",
    "NO_DOUBLE_CORRECTION",
    "NO_CANCELLATION_MASKING",
    "EXPECTED_COMBINED_DIFFERENCE_PREDECLARED",
    "COMBINED_CONSERVATION",
    "COMBINED_NON_INTERFERENCE",
    "INTERACTION_AND_ORDERING_COVERAGE",
    "UNCERTAINTY_PROPAGATION",
    "GENUINELY_INDEPENDENT_REVIEW",
    "COMPOSITION_QUALIFICATION",
    "INTEGRATION_QUALIFICATION",
    "EXPLICIT_PRODUCTION_AUTHORIZATION_WHEN_PRODUCTION_BOUND",
]
TIER_C_EXTRA = [
    "IMMUTABLE_AUTHORING_CHECKPOINT",
    "COMPLETE_SOURCE_AND_PERSISTENT_STATE_OWNERSHIP_RECONSTRUCTION",
    "FIRST_READ_FIRST_WRITE_OR_RESTORE_DIRECTION_ANALYSIS",
    "COUNTER_HYPOTHESIS_TEST",
    "ACTIVE_CONTROLS",
    "NEGATIVE_CONTROLS",
    "SPLIT_RUN_OR_RESTART_EVIDENCE_WHERE_APPLICABLE",
    "EXACT_COMPARISON_POLICY_EXPLICITLY_JUSTIFIED",
    "NO_INVENTED_TOLERANCE",
    "REGRESSION_GUARD",
    "DECLARED_REGRESSION_SURFACE",
    "EXACT_FINAL_HEAD_CI",
]
TIER_D_SURFACES = [
    "COMPOSITION_QUALIFICATION",
    "INTEGRATION_QUALIFICATION",
    "B4_DECISION",
    "PRODUCTION_AUTHORIZATION",
]
BOUNDARY = [
    "PERSIST_COMPLETE_AUTHORING_AND_EVIDENCE_PACKAGE",
    "FREEZE_IMMUTABLE_AUTHORING_HEAD",
    "RECORD_SOURCE_TESTBANK_AND_EVIDENCE_HASHES",
    "COMPLETE_AUTHORING_PHASE",
    "REVIEW_EXACT_FROZEN_AUTHORING_HEAD_ONLY",
]
ADVERSARIAL = [
    "RECONSTRUCT_CLAIM_FROM_PINNED_SOURCE_AND_EVIDENCE",
    "SEARCH_FOR_COUNTEREXAMPLES_AND_CONTRADICTIONS",
    "TEST_STRONGEST_PLAUSIBLE_ALTERNATIVE_INTERPRETATION",
    "VERIFY_OWNERSHIP_UNITS_SIGN_AND_LIFECYCLE_AS_APPLICABLE",
    "VERIFY_FIRST_READ_FIRST_WRITE_OR_RESTORE_DIRECTION_AS_APPLICABLE",
    "VERIFY_EXPECTED_DIFFERENCE_CONTRACT",
    "VERIFY_NON_INTERFERENCE_CONTRACT",
    "INSPECT_ACTIVE_CONTROLS",
    "INSPECT_NEGATIVE_CONTROLS",
    "INSPECT_REGRESSION_SURFACE_AND_SCOPE_GUARD",
    "VERIFY_CONSERVATION_OR_ACCOUNTING_WHERE_APPLICABLE",
    "CLASSIFY_RESIDUAL_UNCERTAINTY",
    "FAIL_CLOSED_ON_CONTRADICTORY_OR_INSUFFICIENT_EVIDENCE",
]
REVIEW_GATES = {
    "POLICY_CLAIM_RECONSTRUCTION",
    "COUNTER_HYPOTHESIS_TEST",
    "GOV04_GATE_PRESERVATION",
    "ASSURANCE_LABELING",
    "TIER_A_WAIVER_PRESERVATION",
    "TIER_B_PROTOCOL",
    "TIER_C_ENHANCED_PROTOCOL",
    "TIER_D_DECISION_SURFACE_SEPARATION",
    "B3Q01_COMPATIBILITY",
    "HISTORICAL_UNKNOWN_PRESERVED",
    "VERIFY_AND_REUSE",
    "TRANSITION_IMMUTABILITY",
    "NO_PRODUCTION_OR_TCD_CHANGE",
    "NEGATIVE_CONTROL_VALIDATOR",
    "REGRESSION_SCOPE",
    "RESIDUAL_UNCERTAINTY",
}
REVIEW_SCIENTIFIC_GATES = {
    "SCIENTIFIC_GATE_SET_PRESERVED",
    "SOURCE_AND_EVIDENCE_PROVENANCE_ENFORCED",
    "OWNERSHIP_UNITS_LIFECYCLE_ENFORCED_WHERE_APPLICABLE",
    "EXPECTED_DIFFERENCE_ENFORCED",
    "CONSERVATION_ENFORCED_WHERE_APPLICABLE",
    "NON_INTERFERENCE_ENFORCED",
    "STATE_RESTART_NUMERICAL_GATES_ENFORCED_WHERE_APPLICABLE",
    "NEGATIVE_CONTROLS_AND_REGRESSION_ENFORCED",
    "HISTORICAL_UNKNOWN_WITHOUT_B2_ENFORCED",
    "PRODUCTION_AUTHORIZATION_SEPARATION_ENFORCED",
}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise ValidationError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p


def changed_paths(a: str, b: str) -> set[str]:
    out = git("diff", "--name-only", a, b).stdout
    return {line.strip() for line in out.splitlines() if line.strip()}


def validate_matrix(m: dict) -> None:
    require(m.get("policy_id") == "ANIMO-GOV05", "wrong policy id")
    require(m.get("policy_name") == "SINGLE_AGENT_ADVERSARIAL_REVIEW", "wrong policy name")
    sem = m.get("governance_semantics", {})
    require(sem.get("scientific_gate_reduction_allowed") is False, "scientific gate reduction enabled")
    require(sem.get("historical_behaviour_without_qualified_b2") == "UNKNOWN", "historical UNKNOWN invariant lost")
    require(sem.get("same_agent_review_mode") == "SINGLE_AGENT_ADVERSARIAL_REVIEW", "same-agent mode missing")
    require(sem.get("same_agent_assurance") == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "same-agent assurance label wrong")
    require(sem.get("independence_assurance_relative_to_gov04_separate_context") == "LOWER", "reduced independence not explicit")
    require(sem.get("same_agent_review_is_independent") is False, "same-agent review claims independence")
    require(sem.get("user_created_review_chat_required") is False, "user-created review chat still required")
    require(m.get("mandatory_review_boundary") == BOUNDARY, "mandatory review boundary changed or unordered")
    require(m.get("mandatory_adversarial_actions") == ADVERSARIAL, "mandatory adversarial actions incomplete")

    preserve = m.get("gov04_gate_preservation", {})
    require(preserve.get("A", {}).get("waiver_predicates") == TIER_A_PREDICATES, "Tier A waiver predicates reduced or changed")
    for tier, expected, old_gate, new_gate in (
        ("B", TIER_B_GOV04, "ONE_GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW", "ONE_MANDATORY_INTERNAL_ADVERSARIAL_REVIEW"),
        ("C", TIER_C_GOV04, "GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW", "ENHANCED_INTERNAL_ADVERSARIAL_REVIEW"),
        ("D", TIER_D_GOV04, "GENUINELY_INDEPENDENT_REVIEW", "SEQUENTIAL_SINGLE_AGENT_ADVERSARIAL_REVIEW_WITH_DISTINCT_DECISION_SURFACES"),
    ):
        block = preserve.get(tier, {})
        require(block.get("gov04_required_gates") == expected, f"Tier {tier} GOV04 gate inventory changed")
        repl = block.get("review_process_gate_replacement", {})
        require(repl.get("from") == old_gate and repl.get("to") == new_gate, f"Tier {tier} review-process replacement wrong")
        require(repl.get("scientific_evidence_gate_removed") is False, f"Tier {tier} claims a scientific evidence gate was removed")
        require(repl.get("independence_assurance_reduced") is True, f"Tier {tier} reduced independence not explicit")

    tiers = m.get("tiers", {})
    require(set(tiers) == {"A", "B", "C", "D"}, "every tier must have explicit assurance")
    for tier in "ABCD":
        require(bool(tiers[tier].get("assurance_level")), f"Tier {tier} assurance level missing")
    require(tiers["A"].get("review_mode") == "GOV04_TIER_A_WAIVER", "Tier A waiver not retained")
    require(tiers["A"].get("all_gov04_waiver_predicates_must_pass") is True, "Tier A waiver weakened")
    require(tiers["B"].get("review_mode") == "ONE_MANDATORY_INTERNAL_ADVERSARIAL_REVIEW", "Tier B mode wrong")
    require(tiers["B"].get("immutable_authoring_checkpoint_required") is True, "Tier B immutable checkpoint missing")
    require(tiers["B"].get("assurance_level") == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "Tier B independence overclaimed")
    require(tiers["C"].get("review_mode") == "ENHANCED_INTERNAL_ADVERSARIAL_REVIEW", "Tier C mode wrong")
    require(tiers["C"].get("lower_independence_assurance_than_gov04") is True, "Tier C lower assurance not explicit")
    require(tiers["C"].get("mandatory_additional_gates") == TIER_C_EXTRA, "Tier C enhanced gates incomplete")
    require(tiers["D"].get("decision_surfaces_must_remain_separate") == TIER_D_SURFACES, "Tier D decision surfaces collapsed")
    require(tiers["D"].get("immutable_checkpoint_required_per_surface") is True, "Tier D per-surface immutable checkpoint missing")
    require(tiers["D"].get("ordinary_authoring_may_not_authorize_production") is True, "ordinary authoring can authorize production")

    compat = m.get("b3q01_compatibility", {})
    require(compat.get("schema_rewritten") is False, "finalized B3Q01 schema rewritten")
    require(compat.get("same_agent_encoding_requires_independent_from_correction_authoring_false") is True, "B3Q01 compatibility could overclaim independence")
    require(compat.get("pass_requires_pinned_gov05_internal_adversarial_review") is True, "B3Q01 compatibility does not require GOV05 review proof")
    require(compat.get("legacy_field_name_confers_independence") is False, "legacy field name confers independence")

    reuse = m.get("evidence_reuse", {})
    require(reuse.get("policy") == "GOV04_VERIFY_AND_REUSE", "VERIFY_AND_REUSE not retained")
    require(set(reuse.get("required_checks", [])) == {"PIN_IDENTITY", "SCOPE_COMPATIBILITY", "IMMUTABLE_PROVENANCE", "NO_SUPERSEDING_OR_CONTRADICTORY_EVIDENCE", "NO_EVIDENCE_STRENGTH_PROMOTION"}, "reuse safeguards incomplete")

    failure = m.get("failure_policy", {})
    require(failure.get("self_review_pass_requires_all_applicable_scientific_gates_pass") is True, "self-review pass can bypass gates")
    require(failure.get("incomplete_evidence") == "FAIL_CLOSED", "incomplete evidence does not fail closed")
    require(failure.get("contradictory_evidence") == "FAIL_CLOSED", "contradictory evidence does not fail closed")
    require(failure.get("request_new_user_review_chat") is False, "manual review chat fallback remains")

    term = m.get("terminology", {})
    require(set(term.get("prohibited_same_agent_claims", [])) == {"genuinely independent", "independent second-line", "organizationally independent", "human independent"}, "same-agent prohibited terminology incomplete")
    require(term.get("historical_review_wording_rewritten") is False, "historical review wording may be rewritten")

    trans = m.get("transition", {})
    for key in ("gov04_historically_valid", "completed_independent_reviews_remain_valid", "existing_admissions_remain_valid", "open_handoff_cancellation_requires_live_eligibility_check"):
        require(trans.get(key) is True, f"transition invariant missing: {key}")
    for key in ("fail_or_incomplete_reviews_rewritten", "old_incomplete_review_may_be_converted_to_pass", "finalized_scientific_work_reopened_only_for_review_style"):
        require(trans.get(key) is False, f"transition invariant violated: {key}")

    for key, value in m.get("hard_boundaries", {}).items():
        require(value is False, f"GOV05 hard boundary violated: {key}")


def validate_status(s: dict, reviewed_head: str) -> None:
    require(s.get("work_unit") == "ANIMO-GOV05", "wrong status work_unit")
    require(s.get("authoring_base") == f"ANIMO-B3D21@{BASE}", "wrong authoring base")
    require(s.get("aggregate_authority_at_start") == f"ANIMO-RG05H@{RG05H}", "wrong aggregate authority")
    auth = s.get("governance_authorities", {})
    require(auth.get("GOV04") == f"ANIMO-GOV04@{GOV04}", "GOV04 pin changed")
    require(auth.get("GOV03") == f"ANIMO-GOV03@{GOV03}", "GOV03 pin changed")
    require(auth.get("B3Q01") == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 pin changed")
    ids = s.get("frozen_evidence_identities", {})
    require(ids.get("source_archive", {}).get("sha256") == EXPECTED_SOURCE, "source hash changed")
    require(ids.get("testbank", {}).get("sha256") == EXPECTED_TESTBANK, "testbank hash changed")
    require(ids.get("user_guide", {}).get("sha256") == EXPECTED_GUIDE, "guide hash changed")
    rb = s.get("review_boundary", {})
    require(rb.get("immutable_authoring_head") == reviewed_head, "status does not pin reviewed authoring head")
    require(rb.get("review_started") is True, "status does not record completed review phase")
    require(rb.get("review_completed") is True, "status does not record completed review")
    require(s.get("decision") == "QUALIFIED_SINGLE_AGENT_ADVERSARIAL_REVIEW_GOVERNANCE_WITH_EXPLICITLY_REDUCED_INDEPENDENCE_ASSURANCE_NO_SCIENTIFIC_GATE_REDUCTION", "final GOV05 decision wrong")
    for key, value in s.get("hard_boundaries", {}).items():
        require(value is False, f"status hard boundary violated: {key}")
    ws = s.get("work_status", {})
    require(all(ws.get(k) is True for k in ("realized", "persisted", "tested", "qualified", "work_unit_complete")), "work status incomplete")
    val = s.get("validation", {})
    require(val.get("exact_final_head_ci_required") is True, "exact final head CI requirement missing")
    require(val.get("conclusion") == "EXACT_FINAL_HEAD_CI_REQUIRED_THIS_COMMIT_IS_QUALIFIED_ONLY_IF_WORKFLOW_SUCCEEDS", "final validation boundary unclear")


def validate_scientific_gate_records(gates: dict, allow_fail: bool) -> None:
    require(isinstance(gates, dict) and gates, "scientific gates missing")
    for name, gate in gates.items():
        require(isinstance(gate, dict), f"scientific gate {name} is not structured")
        applicability = gate.get("applicability")
        result = gate.get("result")
        require(bool(gate.get("justification")), f"scientific gate {name} justification missing")
        require(applicability in {"APPLICABLE", "NOT_APPLICABLE"}, f"scientific gate {name} applicability invalid")
        if applicability == "APPLICABLE":
            require(result in ({"PASS", "FAIL"} if allow_fail else {"PASS"}), f"applicable scientific gate {name} did not pass")
        else:
            require(result == "NOT_APPLICABLE", f"not-applicable scientific gate {name} result mismatch")


def validate_review(r: dict) -> str:
    require(r.get("work_unit") == "ANIMO-GOV05", "review work_unit wrong")
    require(r.get("risk_tier") == "GOVERNANCE", "GOV05 self-review risk tier must be GOVERNANCE")
    require(r.get("review_mode") == "INTERNAL_ADVERSARIAL_REVIEW", "review mode wrong")
    require(r.get("assurance_label") == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance wrong")
    require(r.get("same_agent") is True, "same-agent fact not recorded")
    require(r.get("independence_claimed") is False, "same-agent review claims independence")
    head = r.get("reviewed_authoring_head", "")
    require(len(head) == 40 and all(c in "0123456789abcdef" for c in head), "reviewed authoring head invalid")

    boundary = r.get("review_boundary", {})
    for key in ("complete_authoring_package_persisted", "immutable_head_frozen_before_review", "source_testbank_evidence_hashes_recorded_before_review", "authoring_completed_before_review", "authoring_head_matches_reviewed_head"):
        require(boundary.get(key) is True, f"review boundary failed: {key}")
    require(boundary.get("moving_tree_reviewed") is False, "moving tree was reviewed")

    reuse = r.get("evidence_reuse_checks", {})
    for key in ("pin_identity", "scope_compatibility", "immutable_provenance", "no_superseding_contradiction", "evidence_strength_preserved"):
        require(reuse.get(key) == "PASS", f"review reuse check failed: {key}")

    counter = r.get("counter_hypothesis", {})
    require(counter.get("tested") is True, "counter hypothesis not tested")
    require(bool(counter.get("alternative")) and bool(counter.get("test")), "counter hypothesis is not substantive")
    require(counter.get("result") == "ALTERNATIVE_HAS_HIGHER_INDEPENDENCE_ASSURANCE_BUT_IS_NOT_REQUIRED_BY_GOV05", "counter-hypothesis result must acknowledge higher GOV04 independence assurance")

    require(isinstance(r.get("active_controls"), list) and r["active_controls"], "active controls missing")
    require(isinstance(r.get("negative_controls"), list) and len(r["negative_controls"]) >= 5, "negative controls incomplete")

    scientific = r.get("scientific_gates", {})
    require(set(scientific) == REVIEW_SCIENTIFIC_GATES, "GOV05 review scientific gate inventory incomplete or widened")
    validate_scientific_gate_records(scientific, allow_fail=False)

    gates = r.get("adversarial_gates", {})
    require(set(gates) == REVIEW_GATES, "review gate inventory incomplete or widened")
    require(all(value == "PASS" for value in gates.values()), "not every GOV05 adversarial gate passed")
    require(r.get("outcome") == "SELF_REVIEW_PASS", "review outcome is not SELF_REVIEW_PASS")
    require(isinstance(r.get("residual_uncertainty"), list) and len(r["residual_uncertainty"]) >= 4, "residual uncertainty incomplete")
    return head


def validate_transition(t: dict) -> None:
    require(t.get("work_unit") == "ANIMO-GOV05", "transition work_unit wrong")
    items = {item.get("id"): item for item in t.get("items", [])}
    for needed in ("issue-44", "issue-12", "issue-8", "issue-42", "issue-5", "ANIMO-B3B10R2", "ANIMO-NQ03R"):
        require(needed in items, f"transition snapshot missing {needed}")
    require(items["issue-44"].get("not_required_under_gov05_cancellation") is False, "completed TCD-041 review was reclassified as GOV05 cancellation")
    require(items["issue-12"].get("not_required_under_gov05_cancellation") is False, "completed TCD-028-lineage review was reclassified as GOV05 cancellation")
    require(items["issue-42"].get("old_fail_rewritten") is False, "TCD-040 historical FAIL rewritten")
    require("DO_NOT_INTERRUPT" in items["ANIMO-B3B10R2"].get("transition", ""), "in-flight GOV04 review not protected")
    future = t.get("future_default", {})
    require(future.get("user_created_review_chat_required") is False, "future transition still requires manual review chat")
    require(future.get("historical_fail_or_incomplete_promoted_to_pass") is False, "transition can promote historical fail/incomplete")


def validate_schema(s: dict) -> None:
    required = set(s.get("required", []))
    for key in ("risk_tier", "counter_hypothesis", "active_controls", "negative_controls", "scientific_gates", "adversarial_gates", "outcome"):
        require(key in required, f"generic review schema does not require {key}")
    props = s.get("properties", {})
    require(props.get("same_agent", {}).get("const") is True, "schema does not force same_agent=true")
    require(props.get("independence_claimed", {}).get("const") is False, "schema permits independence claim")
    require(props.get("active_controls", {}).get("minItems") == 1, "schema permits no active control")
    require(props.get("negative_controls", {}).get("minItems") == 1, "schema permits no negative control")
    require("scientific_gates" in props and "tier_c_enhanced" in props and "tier_d_surface" in props, "schema lacks fail-closed tier structures")
    require(props.get("outcome", {}).get("enum") == ["SELF_REVIEW_PASS", "FAIL_CLOSED"], "schema outcome surface changed")
    all_of = s.get("allOf", [])
    require(len(all_of) >= 4, "schema conditional fail-closed rules incomplete")
    text = json.dumps(s, sort_keys=True)
    for token in (
        "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT",
        "tier_c_enhanced",
        "tier_d_surface",
        "surface_not_collapsed",
        "ordinary_authoring_authorizes_production",
        "no_invented_tolerance",
        "SELF_REVIEW_PASS",
        '"const": "FAIL"',
    ):
        require(token in text, f"schema missing conditional safety token: {token}")


def negative_control_self_tests(matrix: dict) -> None:
    mutations = []
    x = copy.deepcopy(matrix)
    x["governance_semantics"]["same_agent_review_is_independent"] = True
    mutations.append((x, "independence overclaim"))
    x = copy.deepcopy(matrix)
    x["tiers"]["C"]["mandatory_additional_gates"] = TIER_C_EXTRA[:-1]
    mutations.append((x, "Tier C gate removal"))
    x = copy.deepcopy(matrix)
    x["tiers"]["D"]["decision_surfaces_must_remain_separate"] = TIER_D_SURFACES[:-1]
    mutations.append((x, "Tier D production collapse"))
    x = copy.deepcopy(matrix)
    x["governance_semantics"]["historical_behaviour_without_qualified_b2"] = "KNOWN"
    mutations.append((x, "historical UNKNOWN promotion"))
    x = copy.deepcopy(matrix)
    x["gov04_gate_preservation"]["B"]["gov04_required_gates"] = TIER_B_GOV04[:-1]
    mutations.append((x, "GOV04 gate inventory removal"))
    for mutated, label in mutations:
        try:
            validate_matrix(mutated)
        except ValidationError:
            continue
        raise ValidationError(f"negative control unexpectedly passed: {label}")


def review_negative_control_self_tests(review: dict) -> None:
    tests = []
    x = copy.deepcopy(review)
    x["independence_claimed"] = True
    tests.append((x, "same-agent independence claim"))
    x = copy.deepcopy(review)
    x["adversarial_gates"]["GOV04_GATE_PRESERVATION"] = "FAIL"
    tests.append((x, "adversarial gate fail hidden by pass outcome"))
    x = copy.deepcopy(review)
    x["scientific_gates"]["NON_INTERFERENCE_ENFORCED"]["result"] = "FAIL"
    tests.append((x, "scientific gate fail hidden by pass outcome"))
    x = copy.deepcopy(review)
    x["negative_controls"] = []
    tests.append((x, "missing negative controls"))
    x = copy.deepcopy(review)
    x["counter_hypothesis"]["result"] = "ALTERNATIVE_REJECTED_BY_PINNED_EVIDENCE"
    tests.append((x, "overstated counter-hypothesis rejection"))
    for mutated, label in tests:
        try:
            validate_review(mutated)
        except ValidationError:
            continue
        raise ValidationError(f"review negative control unexpectedly passed: {label}")


def main() -> None:
    for path in (POLICY, MATRIX, STATUS, SCHEMA, TRANSITION, REVIEW, WORKFLOW):
        require(path.exists(), f"required artifact missing: {path.relative_to(ROOT)}")

    matrix = load_json(MATRIX)
    status = load_json(STATUS)
    schema = load_json(SCHEMA)
    transition = load_json(TRANSITION)
    review = load_json(REVIEW)

    validate_matrix(matrix)
    validate_schema(schema)
    validate_transition(transition)
    reviewed_head = validate_review(review)
    validate_status(status, reviewed_head)
    negative_control_self_tests(matrix)
    review_negative_control_self_tests(review)

    current = git("rev-parse", "HEAD").stdout.strip()
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        require(env_sha == current, "workflow checkout is not exact GITHUB_SHA")

    require(git("cat-file", "-e", f"{reviewed_head}^{{commit}}", check=False).returncode == 0, "reviewed authoring head is not available")
    require(git("merge-base", "--is-ancestor", reviewed_head, current, check=False).returncode == 0, "reviewed authoring head is not an ancestor of final head")

    branch_changes = changed_paths(BASE, current)
    require(branch_changes <= ALLOWED_BRANCH_DIFF, f"scope guard: forbidden branch changes: {sorted(branch_changes - ALLOWED_BRANCH_DIFF)}")
    require(SUBSTANTIVE_REVIEWED_PATHS <= branch_changes, "required GOV05 substantive files missing from branch diff")

    post_review = changed_paths(reviewed_head, current)
    require(post_review <= POST_REVIEW_ALLOWED, f"substantive files changed after immutable review boundary: {sorted(post_review - POST_REVIEW_ALLOWED)}")
    for path in SUBSTANTIVE_REVIEWED_PATHS:
        require(git("diff", "--quiet", reviewed_head, current, "--", path, check=False).returncode == 0, f"reviewed substantive file changed after checkpoint: {path}")

    protected_prefixes = ("src/", "reference/", "docs/b3/", "integration/animo-b3/", "integration/animo-reg/")
    protected_exact = {"docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"}
    for path in branch_changes:
        require(path not in protected_exact and not path.startswith(protected_prefixes), f"protected scientific/history surface modified: {path}")

    source_manifest = (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text(encoding="utf-8").strip()
    test_manifest = (ROOT / "reference/testcases/ANIMO_testbank.zip.sha256").read_text(encoding="utf-8").strip()
    guide_manifest = (ROOT / "reference/documentation/animo_user_guide_4_0.pdf.sha256").read_text(encoding="utf-8").strip()
    require(source_manifest.startswith(EXPECTED_SOURCE), "repository source manifest hash mismatch")
    require(test_manifest.startswith(EXPECTED_TESTBANK), "repository testbank manifest hash mismatch")
    require(guide_manifest.startswith(EXPECTED_GUIDE), "repository user-guide manifest hash mismatch")

    policy_text = POLICY.read_text(encoding="utf-8")
    for token in (
        "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT",
        "lower independence assurance than the GOV04 separate-context process",
        "The scientific evidence gates themselves are not reduced",
        "historical revision-53 behaviour remains `UNKNOWN`",
        "Production authorization may not be collapsed",
    ):
        require(token in policy_text, f"policy text missing required assurance boundary: {token}")

    print(f"PASS: ANIMO-GOV05 governance is fail-closed and exact-head validated at {current} after review of immutable authoring head {reviewed_head}.")


if __name__ == "__main__":
    try:
        main()
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
