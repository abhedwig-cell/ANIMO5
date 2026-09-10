#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3D21 / TCD-037-A1 atomic B3 admission."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BASE = "5915333feed06e0c03280cb8fdfeff8dd1be9e9a"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ02 = "1975eda3586d79033be6af745994bb6181a825fc"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3Q02 = "1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3"

WAIVER_PATH = ROOT / "integration/animo-b3/TCD037_A1_TIER_A_WAIVER_AUDIT.json"
CARRIER_PATH = ROOT / "integration/animo-b3/TCD037_A1_CHILD_ATOM_FORMAL_DISPOSITION.json"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3D21_STATUS.json"
DOC_PATH = ROOT / "docs/b3d21/TCD037_A1_TIER_A_ADMISSION_DECISION.md"
CONTRACT_PATH = ROOT / "docs/b3d21/WORK_UNIT_CONTRACT.md"

ALLOWED_PATHS = {
    ".github/workflows/animo-b3d21-tcd037-a1.yml",
    "docs/b3d21/WORK_UNIT_CONTRACT.md",
    "docs/b3d21/TCD037_A1_TIER_A_ADMISSION_DECISION.md",
    "integration/animo-b3/TCD037_A1_TIER_A_WAIVER_AUDIT.json",
    "integration/animo-b3/TCD037_A1_CHILD_ATOM_FORMAL_DISPOSITION.json",
    "integration/animo-b3/ANIMO-B3D21_STATUS.json",
    "tools/validate_b3d21_tcd037_a1.py",
}

EXPECTED_FIELDS = [
    "Bfom(CH4f)",
    "Bahu(CH4f)",
    "Bdom(CH4f)",
    "Bfom(CO2f)",
    "Bahu(CO2f)",
    "Bdom(CO2f)",
]


def run(*args: str) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)
    return p.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def show_text(commit: str, path: str) -> str:
    return run("git", "show", f"{commit}:{path}")


def show_json(commit: str, path: str) -> dict:
    return json.loads(show_text(commit, path))


def validate_base_and_authorities() -> None:
    # Exact base must be a parent ancestor of this branch and must itself be the closed B3A05 authority.
    require(run("git", "merge-base", "--is-ancestor", BASE, "HEAD") == "", "B3A05 base is not an ancestor")
    b3a05 = show_json(BASE, "integration/animo-b3/ANIMO-B3A05_STATUS.json")
    readiness = show_json(BASE, "integration/animo-b3/TCD037_A1_TIER_A_READINESS.json")
    require(b3a05["work_unit"] == "ANIMO-B3A05", "wrong B3A05 base")
    require(b3a05["state"] == "QUALIFIED_TCD037_A1_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION", "B3A05 not qualified")
    require(b3a05["target_child_atom"] == "TCD-037-A1", "wrong B3A05 target")
    require(b3a05["tier_a_waiver"]["predicate_pass_at_readiness"] is True, "B3A05 Tier-A predicate did not pass")
    require(b3a05["tier_a_waiver"]["final_waiver_granted"] is False, "B3A05 already granted a final waiver")
    require(b3a05["work_status"]["qualified"] is True and b3a05["work_status"]["work_unit_complete"] is True, "B3A05 lifecycle incomplete")
    require(readiness["decision"] == "QUALIFIED_TCD037_A1_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION", "readiness decision mismatch")
    require(readiness["gov04_tier_a_waiver_predicate"]["readiness_result"] == "TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS", "readiness waiver audit mismatch")

    rg = show_json(RG05H, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    require(rg["work_status"]["qualified"] is True, "RG05H not qualified")
    require(rg["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "RG05H routing authority changed")
    require(rg["b4_open"] is False and rg["production_open"] is False, "RG05H opened forbidden later gate")

    atomization = show_json(B3I07, "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    status = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    require(status["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 status changed")
    require(atomization["parent_tcd"] == "TCD-037", "wrong atomization parent")
    require(atomization["allocation_decision"]["parent_atomic"] is False, "parent unexpectedly atomic")
    require(atomization["allocation_decision"]["child_atom_keys_are_top_level_register_rows"] is False, "child promoted to top-level TCD")
    require(atomization["allocation_decision"]["new_top_level_tcd_reserved"] is False, "new top-level TCD reserved")
    atoms = {x["atom_id"]: x for x in atomization["atoms"]}
    require(set(atoms) == {"TCD-037-A1", "TCD-037-A2", "TCD-037-A3", "TCD-037-A4"}, "canonical sibling set changed")
    a1 = atoms["TCD-037-A1"]
    require(a1["class"] == "A_ACCOUNTING_REPORTING_ONLY", "A1 class changed")
    require(a1["source_owner"] == "QPrCH4(Ln)*St", "A1 owner changed")
    require(a1["allowed_observer_fields"] == EXPECTED_FIELDS, "A1 observer field set changed")
    require(a1["admitted"] is False and a1["tier_a_waiver_granted"] is False, "routing workunit already admitted/waived A1")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    require(rq["semantic_qualification"]["ch4_layer_formation_owner"] == "QPrCH4(Ln)*St", "RUNTIMEQ03 owner changed")
    require(rq["expected_difference"]["physical_state"] == "NONE" and rq["expected_difference"]["process_flux"] == "NONE", "RUNTIMEQ03 non-interference changed")
    require(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "RUNTIMEQ03 natural case changed")
    require(rq["historical_intel_behavior"] == "UNKNOWN", "RUNTIMEQ03 historical behavior promoted")

    syn = show_json(SYNQ02, "integration/animo-synthetic/ANIMO-SYNQ02_STATUS.json")
    oracle = show_json(SYNQ02, "integration/animo-synthetic/SYNQ02_TCD037_A1_ORACLE.json")
    require(syn["state"] == "QUALIFIED_TCD037_A1_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2", "SYNQ02 not qualified")
    require(syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "SYNQ02 promoted to B2")
    require(syn["tier_a_waiver_granted"] is False and syn["scientific_admission"] is False, "SYNQ02 exceeded evidence scope")
    require(oracle["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"] == "PASS", "synthetic activation not independently qualified")
    require(oracle["gov04_activation_predicate"]["natural_activation_reasonably_available"] is False, "natural activation unexpectedly available")
    require(oracle["natural_case"]["translation_performed"] is False, "testcase translation occurred")
    require(oracle["accounting_contract"]["layer_amount"] == "QPrCH4(Ln) * St", "oracle owner mismatch")
    require(oracle["allowed_difference_surface"] == EXPECTED_FIELDS, "oracle difference surface mismatch")
    require(oracle["historical_behavior"] == "UNKNOWN", "oracle promotes historical behavior")

    synq01 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq01["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM", "SYNQ01 policy changed")

    g3 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    require(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")
    require(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 G6U changed")
    require(g3["hard_boundaries"]["historical_B2_recovered"] is False, "B2 unexpectedly recovered")

    g4 = show_text(GOV04, "docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    for phrase in (
        "purpose-built synthetic activation",
        "independently qualified for causality and scope",
        "If any condition is false or unknown",
        "NOT_REVIEWED",
        "NOT_APPLICABLE",
    ):
        require(phrase in g4, f"GOV04 Tier-A contract missing phrase: {phrase}")

    b3q1 = show_text(B3Q01, "docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md")
    require("INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY" in b3q1, "historical uncertainty route missing")
    require("One record may cite the parent TCD" in b3q1, "B3Q01 atomic child lineage rule missing")

    b3q2 = show_text(B3Q02, "docs/governance/B3_CHILD_ATOM_DISPOSITION_CARRIER.md")
    require("FORMAL_DISPOSITION" in b3q2 and "ATOMIC_DISPOSITION_TARGET" in b3q2, "B3Q02 child carrier contract missing")


def validate_waiver() -> dict:
    waiver = json.loads(WAIVER_PATH.read_text(encoding="utf-8"))
    require(waiver["work_unit"] == "ANIMO-B3D21", "wrong waiver workunit")
    require(waiver["target_parent_tcd"] == "TCD-037" and waiver["target_child_atom"] == "TCD-037-A1", "wrong waiver target")
    require(waiver["strictest_applicable_gov04_risk_tier"] == "A", "strictest risk tier not A")
    require(waiver["atomic_claim"]["atomic"] is True, "waiver target not atomic")
    require(waiver["atomic_claim"]["source_owner"] == "QPrCH4(Ln) * St", "waiver owner mismatch")
    require(waiver["atomic_claim"]["allowed_observer_fields"] == EXPECTED_FIELDS, "waiver field whitelist mismatch")
    require(waiver["atomic_claim"]["parent_admission_implied"] is False and waiver["atomic_claim"]["sibling_admission_implied"] is False, "waiver leaks to parent/siblings")
    require(waiver["atomic_claim"]["composition_present"] is False, "waiver includes composition")
    for name, value in waiver["tier_a_conditions"].items():
        require(value == "PASS", f"Tier-A waiver condition {name} is not PASS")
    wd = waiver["waiver_decision"]
    require(wd["all_conditions_explicit_pass"] is True, "not all Tier-A conditions passed")
    require(wd["independent_second_line_review_required"] is False, "second-line incorrectly required")
    require(wd["independent_second_line_review_waived_under_gov04"] is True, "GOV04 waiver not recorded")
    require(wd["final_tier_a_waiver_granted_for_this_atomic_admission_object"] is True, "final Tier-A waiver not granted")
    require(wd["waiver_scope"] == "CANONICAL_CHILD_ATOM:TCD-037-A1", "waiver scope mismatch")
    require(wd["waiver_does_not_apply_to_parent_or_siblings"] is True, "waiver leaks to parent/siblings")
    require(waiver["activation_evidence"]["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "waiver promotes synthetic evidence")
    require(waiver["activation_evidence"]["historical_behavior"] == "UNKNOWN", "waiver promotes historical behavior")
    require(waiver["historical_uncertainty"]["qualified_b2_available"] is False, "waiver claims B2")
    require(waiver["historical_uncertainty"]["historical_revision53_behavior"] == "UNKNOWN", "waiver claims historical behavior")
    for key, value in waiver["hard_boundaries"].items():
        require(value is False, f"waiver hard boundary opened: {key}")
    return waiver


def validate_carrier_and_disposition(waiver: dict) -> None:
    carrier = json.loads(CARRIER_PATH.read_text(encoding="utf-8"))
    carrier_schema = json.loads(show_text(B3Q02, "integration/animo-b3/B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json"))
    disposition_schema = json.loads(show_text(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json"))
    Draft202012Validator.check_schema(carrier_schema)
    Draft202012Validator.check_schema(disposition_schema)
    Draft202012Validator(carrier_schema).validate(carrier)
    disposition = carrier["b3_disposition"]
    Draft202012Validator(disposition_schema).validate(disposition)

    require(carrier["carrier_mode"] == "FORMAL_DISPOSITION", "carrier is not formal")
    require(carrier["parent_tcd_id"] == "TCD-037" and carrier["atom_id"] == "TCD-037-A1", "carrier target mismatch")
    require(carrier["qualification_class"] == "A", "carrier class mismatch")
    require(carrier["route_state"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "carrier route mismatch")
    require(carrier["canonical_routing"]["work_unit"] == "ANIMO-B3I07", "carrier routing workunit mismatch")
    require(carrier["canonical_routing"]["status_ref"] == "integration/animo-b3/ANIMO-B3I07_STATUS.json", "carrier routing status ref mismatch")
    require(carrier["canonical_routing"]["atomization_ref"] == "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json", "carrier atomization ref mismatch")
    require(carrier["canonical_routing"]["parent_is_top_level_tcd"] is True and carrier["canonical_routing"]["atom_is_top_level_tcd"] is False, "carrier top-level identity wrong")

    require(disposition["tcd_ids"] == ["TCD-037"], "embedded disposition must carry parent lineage only")
    require(disposition["atomicity"] == "ATOMIC", "embedded disposition is not atomic")
    require(disposition["qualification_class"] == "A", "embedded disposition class mismatch")
    require(disposition["admission_route"] == carrier["route_state"], "embedded route mismatch")
    require(disposition["disposition"] == "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY", "wrong disposition")
    require(disposition["admission_decision"]["admitted"] is True, "A1 not admitted")
    require(disposition["admission_decision"]["decision_scope"] == "CANONICAL_CHILD_ATOM:TCD-037-A1", "admission scope does not bind exact child")
    require(disposition["admission_decision"]["decision"] == "ADMIT_TCD037_A1_CH4_LAYER_FORMATION_OBSERVER_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_A_WAIVER", "admission decision changed")

    review = disposition["evidence"]["independent_review"]
    require(review["status"] == "INCOMPLETE", "waived review must not claim COMPLETE")
    require(review["result"] == "NOT_REVIEWED", "waived review must record NOT_REVIEWED")
    require(review["independent_from_correction_authoring"] is False, "waived review must not claim independence")
    review_gate = disposition["gates"]["independent_review"]
    require(review_gate["status"] == "PASS" and review_gate["applicability"] == "NOT_APPLICABLE", "Tier-A waived review gate must be PASS/N-A")
    require("GOV04 Tier-A" in review_gate["justification"], "waived review gate lacks GOV04 justification")
    require(waiver["waiver_decision"]["final_tier_a_waiver_granted_for_this_atomic_admission_object"] is True, "review waiver not machine-backed")

    require(disposition["identities"]["b1"]["status"] == "DIAGNOSTIC_NOT_REFERENCE", "B1 status changed")
    require(disposition["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 status changed")
    require(disposition["identities"]["b2"]["acquisition_effort_ref"] == f"ANIMO-GOV03@{GOV03}", "B2 acquisition ref mismatch")
    hu = disposition["evidence"]["historical_uncertainty"]
    require("UNKNOWN" in hu["uncertainty_statement"], "historical uncertainty hidden")
    require("NOT_APPLICABLE_UNDER_GOV04_TIER_A_WAIVER" in hu["second_line_review_ref"], "historical uncertainty block does not record waiver")

    diff = disposition["evidence"]["expected_difference"]
    require(diff["changed_states"] == [] and diff["changed_fluxes"] == [], "Class A disposition changes state/flux")
    require(diff["changed_ledgers_or_reports"] == EXPECTED_FIELDS, "embedded difference whitelist mismatch")
    require(disposition["class_specific_evidence"]["physical_state_trajectory_unchanged"] is True, "state non-interference false")
    require(disposition["class_specific_evidence"]["process_flux_trajectory_unchanged"] is True, "flux non-interference false")
    require(disposition["class_specific_evidence"]["intended_ledger_or_report_only"] is True, "Class A report-only contract false")
    require(disposition["class_specific_evidence"]["changed_reporting_surfaces"] == EXPECTED_FIELDS, "Class A reporting surface mismatch")

    for name, gate in disposition["gates"].items():
        require(gate["status"] == "PASS", f"embedded gate {name} is not PASS")
    require(disposition["composition"] == {"is_composition": False, "component_record_ids": []}, "composition introduced")

    effect = carrier["admission_effect"]
    require(effect["atom_admitted"] is True, "carrier does not admit atom")
    require(effect["parent_admitted"] is False, "carrier admits parent")
    require(effect["new_top_level_tcd_reserved"] is False, "carrier reserves top-level TCD")
    require(effect["canonical_register_append"] is False, "carrier appends canonical register")
    require(effect["production_migration_admitted"] is False, "carrier opens production migration")
    require(carrier["residual_blockers"] == [], "unexpected blockers remain inside atomic B3 admission scope")


def validate_status_and_scope() -> None:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    require(status["work_unit"] == "ANIMO-B3D21", "wrong status workunit")
    require(status["target_parent_tcd"] == "TCD-037" and status["target_child_atom"] == "TCD-037-A1", "wrong status target")
    require(status["target_state_after_green_final_head"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "wrong target state")
    require(status["formal_disposition"] == "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY", "status disposition mismatch")
    require(status["gov04_risk_tier"] == "A", "status risk tier mismatch")
    require(status["tier_a_waiver"]["all_predicates_pass"] is True, "status waiver predicate false")
    require(status["tier_a_waiver"]["final_waiver_granted_for_exact_atomic_object"] is True, "status final waiver false")
    require(status["tier_a_waiver"]["independent_review_evidence_result"] == "NOT_REVIEWED", "status review result wrong")
    require(status["tier_a_waiver"]["independent_review_gate"] == "PASS_NOT_APPLICABLE", "status review gate wrong")
    require(status["admission_effect"]["child_atom_admitted"] is True, "status atom admission false")
    require(status["admission_effect"]["parent_tcd_admitted"] is False and status["admission_effect"]["sibling_atoms_admitted"] == [], "status leaks admission")
    require(status["admission_effect"]["historical_revision53_behavior"] == "UNKNOWN", "status promotes historical behavior")
    require(status["admission_effect"]["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "status promotes synthetic evidence")
    require(status["aggregate_policy"]["pending_atomic_admissions_after_rg05h_if_qualified"] == 1, "unexpected post-RG05H admission count")
    require(status["aggregate_policy"]["normal_batch_threshold_reached"] is False, "batch threshold unexpectedly reached")
    require(status["aggregate_policy"]["real_project_gate_changed"] is False, "project gate unexpectedly changed")
    require(status["aggregate_policy"]["aggregate_update_required_now"] is False and status["aggregate_policy"]["rg05i_created"] is False, "premature aggregate update")
    for key, value in status["hard_boundaries"].items():
        require(value is False, f"status hard boundary opened: {key}")

    changed = [x for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x]
    require(set(changed) == ALLOWED_PATHS, f"B3D21 changed-path scope mismatch: {sorted(set(changed) ^ ALLOWED_PATHS)}")
    for path in changed:
        require(not path.startswith(("src/", "reference/source/", "reference/testcases/")), f"forbidden source/frozen path changed: {path}")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")
        require(not path.startswith("integration/animo-reg/"), "aggregate snapshot modified")
        require("B3_DISPOSITION_SCHEMA.json" not in path and "B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json" not in path, "finalized governance schema modified")

    doc = DOC_PATH.read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")
    require("Historical revision-53 behaviour therefore remains exactly" in doc and "UNKNOWN" in doc, "decision doc hides historical uncertainty")
    require("parent `TCD-037 = NOT_ADMITTED_AS_A_COMPOUND_PARENT`" in doc, "parent non-admission not explicit")
    require("RG05I" in contract and "RG05I" in doc, "aggregate non-action not explicit")


def main() -> None:
    validate_base_and_authorities()
    waiver = validate_waiver()
    validate_carrier_and_disposition(waiver)
    validate_status_and_scope()
    print("ANIMO-B3D21 PASS")
    print("TCD-037-A1: ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY")
    print("GOV04 Tier-A independent-review waiver: PASS for exact atomic object")
    print("parent TCD-037: NOT ADMITTED")
    print("siblings A2/A3/A4: NOT ADMITTED")
    print("historical revision-53 behavior: UNKNOWN")
    print("production/B4/aggregate update: NOT AUTHORIZED")


if __name__ == "__main__":
    main()
