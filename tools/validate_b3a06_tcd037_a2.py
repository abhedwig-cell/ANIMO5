#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3A06 / TCD-037-A2 readiness."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "0ca6b31dc8d003ab2b86ced29a2ff8923496ee38"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"
B3D21 = "331f6ed91d4a1c15a23ae0c1ad75d1b540f61858"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"

READINESS_PATH = ROOT / "integration/animo-b3/TCD037_A2_TIER_A_READINESS.json"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3A06_STATUS.json"
DOC_PATH = ROOT / "docs/b3a06/TCD037_A2_TIER_A_READINESS.md"
CONTRACT_PATH = ROOT / "docs/b3a06/WORK_UNIT_CONTRACT.md"

ALLOWED = {
    ".github/workflows/animo-b3a06-tcd037-a2.yml",
    "docs/b3a06/WORK_UNIT_CONTRACT.md",
    "docs/b3a06/TCD037_A2_TIER_A_READINESS.md",
    "integration/animo-b3/TCD037_A2_TIER_A_READINESS.json",
    "integration/animo-b3/ANIMO-B3A06_STATUS.json",
    "tools/validate_b3a06_tcd037_a2.py",
}

EXPECTED_FIELDS = [
    "Btom(CH4e)",
    "Btom(CO2e) formation-side dissimilation complement only",
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
    syn = show_json(BASE, "integration/animo-synthetic/ANIMO-SYNQ03_STATUS.json")
    oracle = show_json(BASE, "integration/animo-synthetic/SYNQ03_TCD037_A2_ORACLE.json")
    require(syn["state"] == "QUALIFIED_TCD037_A2_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2", "SYNQ03 not qualified")
    require(syn["target"] == "TCD-037-A2", "wrong SYNQ03 target")
    require(syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "SYNQ03 promoted to B2")
    require(syn["gov04_activation_predicate"] == "PASS_AT_EVIDENCE_LEVEL_REQUIRES_REEVALUATION_IN_B3A06", "SYNQ03 activation handoff changed")
    require(syn["tier_a_waiver_granted"] is False and syn["scientific_admission"] is False, "SYNQ03 overclaims waiver/admission")
    require(syn["historical_behavior"] == "UNKNOWN", "SYNQ03 promotes historical behavior")
    require(syn["full_carbon_ledger_closure_claimed"] is False, "SYNQ03 overclaims carbon-ledger closure")
    require(syn["testcase_translation_performed"] is False, "SYNQ03 translated testcase")

    require(oracle["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"] == "PASS", "synthetic activation is not independently qualified")
    require(oracle["gov04_activation_predicate"]["natural_activation_reasonably_available"] is False, "natural case unexpectedly available")
    require(oracle["natural_case"]["translation_performed"] is False, "natural testcase was translated")
    require(oracle["historical_behavior"] == "UNKNOWN", "oracle promotes historical behavior")
    require(oracle["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "oracle promotes evidence strength")
    require(oracle["accounting_contract"]["ch4_formation_total"] == "sum(QPrCH4(1:Nl)*St)", "formation owner contract changed")
    require(oracle["accounting_contract"]["ch4_atmosphere_emission_total"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "emission owner contract changed")
    require(oracle["accounting_contract"]["full_model_co2_ledger_claim"] is False, "oracle makes full CO2 ledger claim")
    require(oracle["allowed_difference_surface"] == EXPECTED_FIELDS, "SYNQ03 expected-difference surface changed")

    rg = show_json(RG05H, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    require(rg["work_unit"] == "ANIMO-RG05H", "wrong aggregate authority")
    require(rg["work_status"]["qualified"] is True, "RG05H is not qualified")
    require(rg["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "RG05H does not bind B3I07")
    require(rg["b4_open"] is False and rg["production_open"] is False, "later project gate unexpectedly open")

    b3d21 = show_json(B3D21, "integration/animo-b3/ANIMO-B3D21_STATUS.json")
    require(b3d21["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "B3D21 sibling admission changed")
    require(b3d21["target_child_atom"] == "TCD-037-A1", "B3D21 target changed")
    require(b3d21["admission_effect"]["parent_tcd_admitted"] is False, "B3D21 admitted TCD-037 parent")
    require(b3d21["admission_effect"]["sibling_atoms_admitted"] == [], "B3D21 admitted sibling unexpectedly")

    b3i = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    require(b3i["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 not qualified")
    require("TCD-037-A2" in b3i["intake"]["child_atoms"], "A2 is not canonical")
    require(b3i["readiness_routes"]["TCD-037-A2"] == "ANIMO-B3A06", "A2 does not route to B3A06")
    require(b3i["intake"]["child_class"] == "A_ACCOUNTING_REPORTING_ONLY", "A2 class changed")
    require(b3i["tier_a_waiver"]["granted"] is False, "B3I07 unexpectedly grants Tier-A waiver")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    require(rq["status"] == "QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED", "RUNTIMEQ03 status changed")
    require(rq["semantic_qualification"]["ch4_total_formation_owner"] == "sum(QPrCH4(1:Nl)*St)", "A2 formation owner changed")
    require(rq["semantic_qualification"]["ch4_atmosphere_emission_owner"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "A2 emission owner changed")
    require(rq["semantic_qualification"]["ch4_index0_overloaded"] is True, "A2 overload finding changed")
    require(rq["expected_difference"]["physical_state"] == "NONE", "RUNTIMEQ03 physical state difference changed")
    require(rq["expected_difference"]["process_flux"] == "NONE", "RUNTIMEQ03 process flux difference changed")
    require(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural-case state changed")
    require(rq["historical_intel_behavior"] == "UNKNOWN", "historical behavior promoted")

    synq01 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq01["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM", "SYNQ01 policy authority changed")

    gov03 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    require(gov03["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")
    require(gov03["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 G6U state changed")
    require(gov03["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 unexpectedly recovered B2")

    gov04 = show_text(GOV04, "docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    require("purpose-built synthetic activation" in gov04, "GOV04 synthetic activation alternative missing")
    require("independently qualified for causality and scope" in gov04, "GOV04 synthetic activation predicate missing")
    require("If any condition is false or unknown" in gov04, "GOV04 fail-closed Tier-A rule missing")
    require("Tier A: evidence qualification, technical review, disposition and admission closeout may be combined" in gov04, "GOV04 Tier-A route changed")

    b3q = show_text(B3Q01, "docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md")
    schema = show_text(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    require("One record may cite the parent TCD" in b3q, "B3Q01 parent-child atomic record rule missing")
    require("^TCD-[0-9]{3}$" in schema, "B3Q01 top-level TCD id schema changed")


def validate_readiness() -> None:
    rd = json.loads(READINESS_PATH.read_text(encoding="utf-8"))
    st = json.loads(STATUS_PATH.read_text(encoding="utf-8"))

    require(rd["work_unit"] == "ANIMO-B3A06" and rd["target_child_atom"] == "TCD-037-A2", "wrong readiness identity")
    require(rd["target_parent_tcd"] == "TCD-037", "wrong parent TCD")
    require(rd["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "wrong qualification class")
    require(rd["risk_tier_at_readiness"] == "A", "wrong readiness risk tier")
    require(rd["admission_route_if_later_admitted"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "wrong future route")

    claim = rd["atomic_claim"]
    require(claim["atomic"] is True, "A2 is not atomic")
    require(claim["formation_total_owner"] == "sum(QPrCH4(1:Nl) * St)", "wrong A2 formation owner")
    require(claim["atmosphere_emission_owner"] == "(QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St", "wrong A2 emission owner")
    require(claim["full_model_co2_ledger_claim"] is False, "A2 overclaims full CO2 ledger")
    require(claim["siblings_in_scope"] == [] and claim["tcd032_036_in_scope"] == [], "scope contamination")

    acct = rd["accounting_identity"]
    require(acct["formation_total"] == "F_CH4 = sum(QPrCH4(1:Nl) * St)", "readiness formation identity changed")
    require(acct["atmosphere_emission_total"] == "E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St", "readiness emission identity changed")
    require(acct["btom_ch4e_increment"] == "Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom", "CH4e accounting relation changed")
    require(acct["btom_co2e_formation_side_increment"] == "Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom", "CO2e accounting relation changed")
    require(acct["numerical_acceptance"] == "EXACT_BINARY64_FOR_CHOSEN_DYADIC_SYNTHETIC_VALUES_NO_EMPIRICAL_TOLERANCE", "numerical acceptance changed")

    diff = rd["expected_difference"]
    require(diff["allowed_observer_fields"] == EXPECTED_FIELDS, "expected-difference whitelist mismatch")
    require(diff["predeclared_before_b3a06"] is True, "difference contract was not predeclared")
    for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy", "unrelated_observer_fields", "sibling_atoms", "full_model_co2_ledger"):
        require(diff[key] == "NONE", f"unexpected difference in {key}")

    cov = rd["coverage"]
    require(cov["natural_active_ghg"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural activation state mismatch")
    require(cov["natural_case_translation_performed"] is False, "testcase translation occurred")
    require(cov["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "synthetic evidence promoted")
    require(cov["synthetic_activation_predicate"] == "PASS", "synthetic activation predicate not passed")
    require(cov["historical_behavior"] == "UNKNOWN", "historical behavior promoted")
    require(cov["synthetic_cases"] == ["DIVERGENT_ACTIVE", "FORMATION_ONLY", "EMISSION_ONLY", "EQUAL_TOTALS_CONTROL", "RATE_TIME_EQUIVALENT", "INACTIVE"], "synthetic case set changed")

    waiver = rd["gov04_tier_a_waiver_predicate"]
    allowed_values = {"PASS", "PASS_IF_EXACT_B3A06_CI_GREEN"}
    for key, value in waiver.items():
        if key in {"readiness_result", "final_waiver_granted", "final_waiver_grant_deferred_to_admission_workunit"}:
            continue
        require(value in allowed_values, f"Tier-A predicate {key} is not PASS: {value}")
    require(waiver["readiness_result"] == "TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS", "wrong waiver predicate result")
    require(waiver["final_waiver_granted"] is False, "B3A06 must not grant final waiver")
    require(waiver["final_waiver_grant_deferred_to_admission_workunit"] is True, "waiver is not deferred")

    binding = rd["b3q01_child_schema_binding"]
    require(binding["schema_change_required"] is False, "B3Q01 schema change introduced")
    require(binding["later_disposition_tcd_ids"] == ["TCD-037"], "later schema parent binding wrong")
    require(binding["canonical_atomic_child_identity"] == "TCD-037-A2", "child binding wrong")
    require(binding["parent_or_sibling_admission_implied"] is False, "parent/sibling admission implied")

    for gate, result in rd["readiness_gates"].items():
        if gate == "INDEPENDENT_SECOND_LINE_REVIEW":
            require(result == "NOT_YET_APPLICABLE_READINESS_TIER_A_WAIVER_PREDICATE_PASS", "review gate misrepresented")
        elif gate == "ADMISSION":
            require(result == "NOT_PERFORMED", "B3A06 performed admission")
        else:
            require(result.startswith("PASS"), f"readiness gate {gate} not passed: {result}")

    for key, value in rd["scope_guards"].items():
        require(value is False, f"readiness scope guard opened {key}")
    require(rd["decision"] == "QUALIFIED_TCD037_A2_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION", "wrong readiness decision")
    require(rd["next_work_unit"].startswith("ANIMO-B3D22"), "wrong next workunit")

    require(st["work_unit"] == "ANIMO-B3A06" and st["target_child_atom"] == "TCD-037-A2", "wrong status identity")
    require(st["base"] == f"ANIMO-SYNQ03@{BASE}", "wrong status base")
    require(st["route"]["historical_behavior"] == "UNKNOWN", "status promotes historical behavior")
    require(st["tier_a_waiver"]["predicate_pass_at_readiness"] is True, "status lacks Tier-A readiness predicate")
    require(st["tier_a_waiver"]["final_waiver_granted"] is False, "status grants final waiver")
    require(st["governance_observation"]["gov05_consumed_as_authority"] is False, "unqualified GOV05 consumed")
    for value in st["scope_guards"].values():
        require(value is False, "status scope guard opened")
    require(st["state"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_TCD037_A2_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION"}, "wrong status lifecycle")
    require(st["work_status"]["realized"] is True and st["work_status"]["persisted"] is True, "work not persisted")
    require(st["work_status"]["tested"] in {False, True}, "invalid tested lifecycle")
    require(st["work_status"]["qualified"] in {False, True}, "invalid qualified lifecycle")

    doc = DOC_PATH.read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")
    require("does not grant the final waiver" in doc, "readiness document overclaims waiver")
    require('tcd_ids: ["TCD-037"]' in doc, "child schema binding missing")
    require("No model-wide CO2-ledger closure is claimed" in doc, "CO2 ledger boundary missing")
    require("ANIMO-B3D22" in doc and "ANIMO-B3D22" in contract, "next route missing")


def validate_scope() -> None:
    changed = [p.strip() for p in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if p.strip()]
    require(changed, "B3A06 has no artifacts")
    require(set(changed) == ALLOWED, f"B3A06 scope mismatch: {sorted(set(changed) ^ ALLOWED)}")
    forbidden_prefixes = ("src/", "reference/source/", "reference/testcases/")
    for path in changed:
        require(not path.startswith(forbidden_prefixes), f"forbidden production/frozen path changed: {path}")


def main() -> None:
    validate_authorities()
    validate_readiness()
    validate_scope()
    print("ANIMO-B3A06 TCD-037-A2 readiness validator PASS")


if __name__ == "__main__":
    main()
