#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3D26 / TCD-037-A4 atomic admission."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BASE = "840352e615b1ae4c7e30b922378655111dba9257"
B3D21 = "331f6ed91d4a1c15a23ae0c1ad75d1b540f61858"
B3D24 = "0f85d7102945c7c4d77bc49885f9ecca688209e3"
B3D25 = "4da2dd067069944a5e3eeb5f532566a23402bd68"
RG05I = "94afe7d649a8c60758a41996f0059de0acddd2fc"
SYNQ05 = "ca3b6fba99ddc70e1f063ac98088f8825f467c1a"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3Q02 = "1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3"
CARRIER = ROOT / "integration/animo-b3/TCD037_A4_CHILD_ATOM_FORMAL_DISPOSITION.json"
AUDIT = ROOT / "integration/animo-b3/TCD037_A4_TIER_A_WAIVER_AUDIT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D26_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3d26-tcd037-a4.yml",
    "docs/b3d26/WORK_UNIT_CONTRACT.md",
    "docs/b3d26/TCD037_A4_TIER_A_ADMISSION_DECISION.md",
    "integration/animo-b3/TCD037_A4_TIER_A_WAIVER_AUDIT.json",
    "integration/animo-b3/TCD037_A4_CHILD_ATOM_FORMAL_DISPOSITION.json",
    "integration/animo-b3/ANIMO-B3D26_STATUS.json",
    "tools/validate_b3d26_tcd037_a4.py",
}
EXPECTED_PREDICATES = {
    "EXACT_SOURCE_SEAM", "UNAMBIGUOUS_PHYSICAL_AND_ACCOUNTING_OWNERSHIP", "ATOMICITY",
    "EXACT_CONSERVATION_OR_ACCOUNTING_IDENTITY", "EXPECTED_DIFFERENCE_PREDECLARED",
    "PHYSICAL_STATE_NON_INTERFERENCE", "PROCESS_FLUX_NON_INTERFERENCE", "NO_NUMERICAL_POLICY_CHANGE",
    "NO_SOLVER_OR_TOLERANCE_CHANGE", "NO_RESTART_INITIALIZATION_OR_STATE_SEMANTIC_CHANGE",
    "NO_COMPOSITION", "NO_UNRESOLVED_SCIENTIFIC_OR_SOURCE_MEANING_AMBIGUITY", "REPRODUCIBLE_VALIDATOR",
    "SCOPE_GUARD", "NATURAL_OR_QUALIFIED_SYNTHETIC_ACTIVATION", "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2",
    "GOV03_ROUTE_CONDITIONS_RETAINED_WHEN_APPLICABLE", "NO_PRODUCTION_OR_B4_OR_CANONICAL_REGISTER_CHANGE"
}
REUSE_CHECKS = {
    "PIN_IDENTITY", "SCOPE_COMPATIBILITY", "IMMUTABLE_PROVENANCE",
    "NO_SUPERSEDING_OR_CONTRADICTORY_EVIDENCE", "NO_EVIDENCE_STRENGTH_PROMOTION"
}


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D26 FAIL_CLOSED: " + msg)


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def show_json(ref, path):
    return json.loads(run("git", "show", f"{ref}:{path}"))


def main():
    carrier = json.loads(CARRIER.read_text())
    audit = json.loads(AUDIT.read_text())
    status = json.loads(STATUS.read_text())
    req(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT).returncode == 0,
        "B3A09 exact-final readiness head is not ancestor")

    ready = show_json(BASE, "integration/animo-b3/ANIMO-B3A09_STATUS.json")
    req(ready["state"] == "QUALIFIED_TCD037_A4_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION",
        "B3A09 readiness not qualified")
    req(ready["target_child_atom"] == "TCD-037-A4" and ready["tier_a_waiver"]["predicate_pass_at_readiness"] is True,
        "B3A09 target or waiver predicate drift")
    req(ready["tier_a_waiver"]["final_waiver_granted"] is False, "B3A09 improperly granted final waiver")
    req(ready["validator_remediation"]["classification"] == "TOOLING_VALIDATOR_FAILURE" and
        ready["validator_remediation"]["semantic_evidence_omitted"] is False and
        ready["validator_remediation"]["historical_b3i07_routing_rewritten"] is False and
        ready["validator_remediation"]["scientific_predicates_changed"] is False,
        "B3A09 tooling remediation changed semantic evidence or scientific predicates")
    for k, v in ready["scope_guards"].items():
        req(v is False, f"B3A09 scope guard violated: {k}")

    latest = show_json(B3D25, "integration/animo-b3/ANIMO-B3D25_STATUS.json")
    req(latest["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and latest["target_child_atom"] == "TCD-037-A3",
        "B3D25 latest atomic admission drift")
    req(latest["candidate_admission_effect"]["parent_tcd_admitted"] is False and
        latest["candidate_admission_effect"]["a4_admitted"] is False, "A4 or parent already admitted upstream")

    rg = show_json(RG05I, "integration/animo-reg/ANIMO-RG05I_STATUS.json")
    req(rg["state"] == "QUALIFIED_THIRD_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05H_ADMISSIONS_NO_PRODUCTION",
        "RG05I not qualified")
    req(rg["scientific_admission_count"] == 14 and rg["tcd037_state"]["parent_admitted"] is False,
        "RG05I aggregate state drift")
    req(rg["tcd037_state"]["admitted_children"] == ["TCD-037-A1", "TCD-037-A2"],
        "RG05I child snapshot drift")
    req(rg["b4_open"] is False and rg["production_open"] is False, "RG05I downstream gate opened")

    for ref, path, atom in (
        (B3D21, "integration/animo-b3/ANIMO-B3D21_STATUS.json", "TCD-037-A1"),
        (B3D24, "integration/animo-b3/ANIMO-B3D24_STATUS.json", "TCD-037-A2"),
        (B3D25, "integration/animo-b3/ANIMO-B3D25_STATUS.json", "TCD-037-A3"),
    ):
        s = show_json(ref, path)
        req(s["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and s["target_child_atom"] == atom,
            f"existing child authority invalid: {atom}")
        effect = s.get("candidate_admission_effect", s.get("admission_effect", {}))
        req(effect.get("parent_tcd_admitted") is False, f"existing child unexpectedly admits parent: {atom}")

    syn = show_json(SYNQ05, "integration/animo-synthetic/ANIMO-SYNQ05_STATUS.json")
    oracle = show_json(SYNQ05, "integration/animo-synthetic/SYNQ05_TCD037_A4_ORACLE.json")
    req(syn["state"] == "QUALIFIED_TCD037_A4_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2",
        "SYNQ05 not qualified")
    req(syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2" and syn["historical_behavior"] == "UNKNOWN",
        "SYNQ05 evidence strength or history drift")
    req(syn["scientific_admission"] is False and syn["tier_a_waiver_granted"] is False,
        "SYNQ05 overclaims admission or waiver")
    req(syn["allowed_difference_surface"] == ["Bani(N2Oe)"] and syn["testcase_translation_performed"] is False,
        "SYNQ05 scope or testcase boundary drift")
    req(oracle["accounting_contract"]["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St" and
        oracle["accounting_contract"]["observer_increment"] == "10000*(QEmN2ODif+QEmN2OFlw)*St",
        "SYNQ05 accounting identity drift")
    req(oracle["allowed_difference_surface"] == ["Bani(N2Oe)"], "SYNQ05 oracle difference surface widened")
    req(set(oracle["cases"]) == {"EMISSION_NONZERO_PRODUCTION_ZERO", "PRODUCTION_NONZERO_EMISSION_ZERO",
        "COMPONENT_PERMUTED", "RATE_TIME_EQUIVALENT", "SIGNED_UPTAKE", "INACTIVE"},
        "SYNQ05 control coverage drift")

    atomization = show_json(B3I07, "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms = {x["atom_id"]: x for x in atomization["atoms"]}
    a4 = atoms["TCD-037-A4"]
    req(a4["class"] == "A_ACCOUNTING_REPORTING_ONLY" and a4["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St",
        "B3I07 A4 identity drift")
    req(a4["allowed_observer_fields"] == ["Bani(N2Oe)"], "B3I07 A4 surface drift")
    req(a4["historical_behavior"] == "UNKNOWN" and a4["natural_activation"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH",
        "B3I07 A4 history or natural activation drift")
    req(a4["next_work_unit"] == "ANIMO-B3A08 — TCD-037-A4 N2O Atmosphere Emission Observer Tier-A Readiness",
        "historical B3I07 routing was rewritten")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    req(rq["semantic_qualification"]["n2o_atmosphere_emission_owner"] == "(QEmN2ODif+QEmN2OFlw)*St",
        "RUNTIMEQ03 atmosphere-emission owner drift")
    req(rq["semantic_qualification"]["n2o_index0_consumer_mismatch"] is True,
        "RUNTIMEQ03 A4 consumer mismatch no longer established")
    for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy"):
        req(rq["expected_difference"][key] == "NONE", "RUNTIMEQ03 non-interference drift: " + key)
    req(rq["historical_intel_behavior"] == "UNKNOWN", "RUNTIMEQ03 historical behavior promoted")

    g5 = show_json(GOV05, "integration/animo-governance/GOV05_REVIEW_ASSURANCE_MATRIX.json")
    req(g5["tiers"]["A"]["review_mode"] == "GOV04_TIER_A_WAIVER" and
        g5["tiers"]["A"]["all_gov04_waiver_predicates_must_pass"] is True and
        g5["tiers"]["A"]["same_agent_review_required"] is False, "GOV05 Tier-A rule drift")
    req(g5["evidence_reuse"]["policy"] == "GOV04_VERIFY_AND_REUSE" and
        set(g5["evidence_reuse"]["required_checks"]) == REUSE_CHECKS and
        g5["evidence_reuse"]["mechanical_rerun_required_when_immutable_and_unchanged"] is False,
        "GOV05 VERIFY_AND_REUSE policy drift")
    req(g5["governance_semantics"]["scientific_gate_reduction_allowed"] is False and
        g5["governance_semantics"]["historical_behaviour_without_qualified_b2"] == "UNKNOWN",
        "GOV05 scientific/history guard drift")

    g4 = show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
    conds = set(g4["tier_a_independent_review_waiver_conditions"]["conditions"])
    req(g4["tier_a_independent_review_waiver_conditions"]["logic"] == "ALL_MUST_PASS" and conds == EXPECTED_PREDICATES,
        "retained GOV04 Tier-A predicate set drift")
    req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True,
        "GOV04 strictest risk trigger rule lost")

    g3 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT",
        "GOV03 B2 closure drift")
    req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS",
        "GOV03 uncertainty route drift")

    base_schema = show_json(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    carrier_schema = show_json(B3Q02, "integration/animo-b3/B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json")
    Draft202012Validator.check_schema(base_schema)
    Draft202012Validator.check_schema(carrier_schema)
    Draft202012Validator(carrier_schema).validate(carrier)
    Draft202012Validator(base_schema).validate(carrier["b3_disposition"])

    req(carrier["carrier_mode"] == "FORMAL_DISPOSITION" and carrier["parent_tcd_id"] == "TCD-037" and carrier["atom_id"] == "TCD-037-A4",
        "carrier identity invalid")
    req(carrier["qualification_class"] == "A" and carrier["canonical_routing"]["work_unit"] == "ANIMO-B3I07",
        "carrier class or routing invalid")
    req(carrier["b3_disposition"]["tcd_ids"] == ["TCD-037"] and carrier["b3_disposition"]["atomicity"] == "ATOMIC",
        "embedded lineage or atomicity invalid")
    req(carrier["b3_disposition"]["admission_decision"]["decision_scope"] == "CANONICAL_CHILD_ATOM:TCD-037-A4" and
        carrier["b3_disposition"]["admission_decision"]["admitted"] is True and carrier["admission_effect"]["atom_admitted"] is True,
        "A4 admission decision invalid")
    req(carrier["admission_effect"]["parent_admitted"] is False and
        carrier["admission_effect"]["new_top_level_tcd_reserved"] is False and
        carrier["admission_effect"]["canonical_register_append"] is False and
        carrier["admission_effect"]["production_migration_admitted"] is False, "child carrier scope violation")
    ir = carrier["b3_disposition"]["evidence"]["independent_review"]
    req(ir["result"] == "NOT_REVIEWED" and ir["independent_from_correction_authoring"] is False,
        "independent review falsely claimed")
    req(carrier["b3_disposition"]["gates"]["independent_review"]["status"] == "PASS" and
        carrier["b3_disposition"]["gates"]["independent_review"]["applicability"] == "NOT_APPLICABLE",
        "Tier-A review applicability gate invalid")
    req(carrier["b3_disposition"]["evidence"]["expected_difference"]["changed_ledgers_or_reports"] == ["Bani(N2Oe)"],
        "admission difference surface widened")
    req(carrier["b3_disposition"]["class_specific_evidence"]["signed_exchange_semantics_preserved"] is True and
        carrier["b3_disposition"]["class_specific_evidence"]["global_Ly_equals_Ln_theorem_claimed"] is False,
        "A4 class evidence overclaim")

    req(audit["decision_scope"] == "CANONICAL_CHILD_ATOM:TCD-037-A4" and
        audit["final_tier_a_waiver_granted_for_this_atomic_admission_object"] is True,
        "waiver audit result invalid")
    req(set(audit["predicates"]) == EXPECTED_PREDICATES, "waiver predicate set drift")
    for k, v in audit["predicates"].items():
        req(v in {"PASS", "PASS_IF_EXACT_B3D26_CI_GREEN"}, f"waiver predicate not PASS: {k}={v}")
    reuse = audit["evidence_reuse"]
    req(reuse["policy"] == "GOV04_VERIFY_AND_REUSE", "wrong evidence-reuse policy")
    for k in REUSE_CHECKS:
        req(reuse[k] == "PASS", "evidence-reuse check not PASS: " + k)
    req(reuse["mechanical_rerun_required_for_unchanged_immutable_evidence"] is False,
        "immutable unchanged evidence incorrectly requires rerun")
    req(audit["review_process"]["independent_review_performed_here"] is False and
        audit["review_process"]["independence_claimed"] is False, "audit independence overclaim")
    req(audit["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2" and
        audit["historical_revision53_behavior"] == "UNKNOWN" and audit["testcase_translation_performed"] is False,
        "waiver evidence boundary invalid")

    req(status["state"] in {"PERSISTED_VALIDATION_PENDING", "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY"},
        "status lifecycle invalid")
    req(status["target_child_atom"] == "TCD-037-A4" and
        status["tier_a_waiver"]["final_waiver_granted_for_exact_atomic_object"] is True,
        "status waiver or target invalid")
    req(status["evidence_reuse"]["policy"] == "GOV04_VERIFY_AND_REUSE" and
        status["evidence_reuse"]["all_required_checks_pass"] is True,
        "status does not retain VERIFY_AND_REUSE")
    req(status["candidate_admission_effect"]["parent_tcd_admitted"] is False and
        status["candidate_admission_effect"]["all_four_child_atoms_admitted_after_exact_final_green"] is True,
        "status parent or child-completion effect invalid")
    req(status["candidate_admission_effect"]["global_Ly_equals_Ln_theorem_admitted"] is False,
        "status global index theorem overclaim")
    req(status["aggregate_policy"]["pending_atomic_admissions_after_rg05i_if_qualified"] == 2 and
        status["aggregate_policy"]["normal_batch_threshold_reached"] is False and
        status["aggregate_policy"]["next_aggregate_created"] is False, "premature aggregate trigger")
    req(status["parent_routing"]["parent_admitted_by_child_completion"] is False and
        status["parent_routing"]["automatic_parent_composition_allowed"] is False and
        status["parent_routing"]["separate_parent_decision_surface_required_if_all_children_green"] is True,
        "parent admission implied by child completion")
    for k, v in status["hard_boundaries"].items():
        req(v is False, f"hard boundary violated: {k}")

    changed = {x.strip() for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x.strip()}
    req(changed == ALLOWED, "scope differs from exact seven-file B3D26 package: " + repr(sorted(changed)))
    for p in changed:
        req(not p.startswith(("src/", "reference/", "production/")), "protected source/B0 modified: " + p)
        req("THEORY_CODE_DISCREPANCY_REGISTER" not in p, "canonical TCD register modified")
    print("B3D26 PASS: exact TCD-037-A4 child admission satisfies GOV05 VERIFY_AND_REUSE and retained Tier-A waiver; parent/B4/production remain unadmitted")


if __name__ == "__main__":
    main()
