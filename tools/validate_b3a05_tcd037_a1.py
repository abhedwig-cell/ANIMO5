#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3A05 / TCD-037-A1 readiness."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "3e4247928bb43f30def951fa8804560636affbef"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ02 = "1975eda3586d79033be6af745994bb6181a825fc"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"

READINESS_PATH = ROOT / "integration/animo-b3/TCD037_A1_TIER_A_READINESS.json"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3A05_STATUS.json"
DOC_PATH = ROOT / "docs/b3a05/TCD037_A1_TIER_A_READINESS.md"
CONTRACT_PATH = ROOT / "docs/b3a05/WORK_UNIT_CONTRACT.md"

ALLOWED = {
    ".github/workflows/animo-b3a05-tcd037-a1.yml",
    "docs/b3a05/WORK_UNIT_CONTRACT.md",
    "docs/b3a05/TCD037_A1_TIER_A_READINESS.md",
    "integration/animo-b3/TCD037_A1_TIER_A_READINESS.json",
    "integration/animo-b3/ANIMO-B3A05_STATUS.json",
    "tools/validate_b3a05_tcd037_a1.py",
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


def validate_authorities() -> None:
    rg05h = show_json(BASE, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    require(rg05h["work_unit"] == "ANIMO-RG05H", "wrong aggregate authority")
    require(rg05h["work_status"]["qualified"] is True, "RG05H is not qualified")
    require(rg05h["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "RG05H does not bind B3I07")
    require(rg05h["b4_open"] is False and rg05h["production_open"] is False, "later project gate unexpectedly open")

    b3i07 = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    require(b3i07["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 not qualified")
    require("TCD-037-A1" in b3i07["intake"]["child_atoms"], "A1 is not canonical")
    require(b3i07["readiness_routes"]["TCD-037-A1"] == "ANIMO-B3A05", "A1 does not route to B3A05")
    require(b3i07["intake"]["child_class"] == "A_ACCOUNTING_REPORTING_ONLY", "A1 class changed")
    require(b3i07["tier_a_waiver"]["granted"] is False, "B3I07 unexpectedly grants Tier-A waiver")
    require(b3i07["intake"]["child_admission_count"] == 0, "B3I07 already admits a child")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    require(rq["status"] == "QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED", "RUNTIMEQ03 status changed")
    require(rq["semantic_qualification"]["ch4_layer_formation_owner"] == "QPrCH4(Ln)*St", "A1 source owner changed")
    require(rq["expected_difference"]["physical_state"] == "NONE", "RUNTIMEQ03 physical state difference changed")
    require(rq["expected_difference"]["process_flux"] == "NONE", "RUNTIMEQ03 process flux difference changed")
    require(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural-case state changed")
    require(rq["historical_intel_behavior"] == "UNKNOWN", "historical behavior promoted")

    syn = show_json(SYNQ02, "integration/animo-synthetic/ANIMO-SYNQ02_STATUS.json")
    oracle = show_json(SYNQ02, "integration/animo-synthetic/SYNQ02_TCD037_A1_ORACLE.json")
    require(syn["state"] == "QUALIFIED_TCD037_A1_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2", "SYNQ02 not qualified")
    require(syn["target"] == "TCD-037-A1", "wrong SYNQ02 target")
    require(syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "SYNQ02 promoted to B2")
    require(syn["gov04_activation_predicate"] == "PASS_AT_EVIDENCE_LEVEL_REQUIRES_REEVALUATION_IN_B3A05", "SYNQ02 activation handoff changed")
    require(syn["tier_a_waiver_granted"] is False and syn["scientific_admission"] is False, "SYNQ02 overclaims waiver/admission")
    require(oracle["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"] == "PASS", "synthetic activation is not independently qualified")
    require(oracle["gov04_activation_predicate"]["natural_activation_reasonably_available"] is False, "natural case unexpectedly available")
    require(oracle["natural_case"]["translation_performed"] is False, "natural testcase was translated")
    require(oracle["historical_behavior"] == "UNKNOWN", "SYNQ02 promotes historical behavior")
    require(oracle["accounting_contract"]["layer_amount"] == "QPrCH4(Ln) * St", "SYNQ02 amount contract changed")
    require(oracle["allowed_difference_surface"] == EXPECTED_FIELDS, "SYNQ02 expected-difference surface changed")

    synq01 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq01["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM", "SYNQ01 policy authority changed")

    gov03 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    require(gov03["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")
    require(gov03["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 G6U state changed")
    require(gov03["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 unexpectedly recovered B2")

    gov04 = show_text(GOV04, "docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    require("purpose-built synthetic activation" in gov04, "GOV04 synthetic activation alternative missing")
    require("independently qualified for causality and scope" in gov04, "GOV04 independence predicate missing")
    require("If any condition is false or unknown" in gov04, "GOV04 fail-closed Tier-A rule missing")

    b3q = show_text(B3Q01, "docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md")
    schema = show_text(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    require("One record may cite the parent TCD" in b3q, "B3Q01 parent-child atomic record rule missing")
    require("^TCD-[0-9]{3}$" in schema, "B3Q01 top-level TCD id schema changed")


def validate_readiness() -> None:
    rd = json.loads(READINESS_PATH.read_text(encoding="utf-8"))
    st = json.loads(STATUS_PATH.read_text(encoding="utf-8"))

    require(rd["work_unit"] == "ANIMO-B3A05" and rd["target_child_atom"] == "TCD-037-A1", "wrong readiness identity")
    require(rd["target_parent_tcd"] == "TCD-037", "wrong parent TCD")
    require(rd["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "wrong qualification class")
    require(rd["risk_tier_at_readiness"] == "A", "wrong readiness risk tier")
    require(rd["admission_route_if_later_admitted"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "wrong future route")
    require(rd["atomic_claim"]["atomic"] is True, "A1 is not atomic")
    require(rd["atomic_claim"]["source_owner"] == "QPrCH4(Ln) * St", "wrong A1 source owner")
    require(rd["atomic_claim"]["siblings_in_scope"] == [], "sibling scope contamination")
    require(rd["expected_difference"]["allowed_observer_fields"] == EXPECTED_FIELDS, "expected-difference whitelist mismatch")
    require(rd["expected_difference"]["predeclared_before_b3a05"] is True, "difference contract was not predeclared")
    for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy", "unrelated_observer_fields", "sibling_atoms"):
        require(rd["expected_difference"][key] == "NONE", f"unexpected difference in {key}")

    require(rd["coverage"]["natural_active_ghg"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural activation state mismatch")
    require(rd["coverage"]["natural_case_translation_performed"] is False, "testcase translation occurred")
    require(rd["coverage"]["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "synthetic evidence promoted")
    require(rd["coverage"]["synthetic_activation_predicate"] == "PASS", "synthetic activation predicate not passed")
    require(rd["coverage"]["historical_behavior"] == "UNKNOWN", "historical behavior promoted")

    waiver = rd["gov04_tier_a_waiver_predicate"]
    allowed_values = {"PASS", "PASS_IF_EXACT_B3A05_CI_GREEN"}
    for key, value in waiver.items():
        if key in {"readiness_result", "final_waiver_granted", "final_waiver_grant_deferred_to_admission_workunit"}:
            continue
        require(value in allowed_values, f"Tier-A predicate {key} is not PASS: {value}")
    require(waiver["readiness_result"] == "TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS", "wrong waiver predicate result")
    require(waiver["final_waiver_granted"] is False, "B3A05 must not grant final waiver")
    require(waiver["final_waiver_grant_deferred_to_admission_workunit"] is True, "waiver is not deferred")

    binding = rd["b3q01_child_schema_binding"]
    require(binding["schema_change_required"] is False, "B3Q01 schema change introduced")
    require(binding["later_disposition_tcd_ids"] == ["TCD-037"], "later schema parent binding wrong")
    require(binding["canonical_atomic_child_identity"] == "TCD-037-A1", "child binding wrong")
    require(binding["parent_or_sibling_admission_implied"] is False, "parent/sibling admission implied")

    for gate, result in rd["readiness_gates"].items():
        if gate == "INDEPENDENT_SECOND_LINE_REVIEW":
            require(result == "NOT_YET_APPLICABLE_READINESS_TIER_A_WAIVER_PREDICATE_PASS", "independent review gate misrepresented")
        elif gate == "ADMISSION":
            require(result == "NOT_PERFORMED", "B3A05 performed admission")
        else:
            require(result.startswith("PASS"), f"readiness gate {gate} not passed: {result}")

    for key, value in rd["scope_guards"].items():
        require(value is False, f"readiness scope guard opened {key}")
    require(rd["decision"] == "QUALIFIED_TCD037_A1_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION", "wrong readiness decision")
    require(rd["next_work_unit"].startswith("ANIMO-B3D21"), "wrong next workunit")

    require(st["work_unit"] == "ANIMO-B3A05" and st["target_child_atom"] == "TCD-037-A1", "wrong status identity")
    require(st["base"] == f"ANIMO-RG05H@{BASE}", "wrong status base")
    require(st["route"]["historical_behavior"] == "UNKNOWN", "status promotes historical behavior")
    require(st["tier_a_waiver"]["predicate_pass_at_readiness"] is True, "status lacks Tier-A readiness predicate")
    require(st["tier_a_waiver"]["final_waiver_granted"] is False, "status grants final waiver")
    for value in st["scope_guards"].values():
        require(value is False, "status scope guard opened")
    require(st["state"] == "QUALIFIED_TCD037_A1_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION", "wrong status decision")
    require(st["work_status"]["realized"] is True and st["work_status"]["persisted"] is True, "work not persisted")
    require(st["work_status"]["tested"] in {False, True}, "invalid tested lifecycle")
    require(st["work_status"]["qualified"] in {False, True}, "invalid qualified lifecycle")

    doc = DOC_PATH.read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")
    require("does not grant the final waiver" in doc, "readiness document overclaims waiver")
    require("tcd_ids: [\"TCD-037\"]" in doc, "child schema binding missing")
    require("ANIMO-B3D21" in doc and "ANIMO-B3D21" in contract, "next route missing")


def validate_scope() -> None:
    changed = [p.strip() for p in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if p.strip()]
    require(changed, "B3A05 has no artifacts")
    require(set(changed) == ALLOWED, f"B3A05 scope mismatch: {sorted(set(changed) ^ ALLOWED)}")
    forbidden_prefixes = ("src/", "reference/source/", "reference/testcases/")
    for path in changed:
        require(not path.startswith(forbidden_prefixes), f"forbidden production/frozen path changed: {path}")


def main() -> None:
    validate_authorities()
    validate_readiness()
    validate_scope()
    print("ANIMO-B3A05 PASS")
    print("TCD-037-A1 READY: Tier-A waiver predicate PASS at readiness; no waiver/admission issued")
    print("historical behavior: UNKNOWN")
    print("next: ANIMO-B3D21")


if __name__ == "__main__":
    main()
