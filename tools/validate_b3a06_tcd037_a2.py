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
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"

READINESS = ROOT / "integration/animo-b3/TCD037_A2_TIER_A_READINESS.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3A06_STATUS.json"
DOC = ROOT / "docs/b3a06/TCD037_A2_TIER_A_READINESS.md"
CONTRACT = ROOT / "docs/b3a06/WORK_UNIT_CONTRACT.md"

ALLOWED = {
    ".github/workflows/animo-b3a06-tcd037-a2.yml",
    "docs/b3a06/WORK_UNIT_CONTRACT.md",
    "docs/b3a06/TCD037_A2_TIER_A_READINESS.md",
    "integration/animo-b3/TCD037_A2_TIER_A_READINESS.json",
    "integration/animo-b3/ANIMO-B3A06_STATUS.json",
    "tools/validate_b3a06_tcd037_a2.py",
}
EXPECTED_FIELDS = ["Btom(CH4e)", "Btom(CO2e) formation-side dissimilation complement only"]


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def req(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def show_json(commit: str, path: str) -> dict:
    return json.loads(run("git", "show", f"{commit}:{path}"))


def show_text(commit: str, path: str) -> str:
    return run("git", "show", f"{commit}:{path}")


def validate_authorities() -> None:
    syn = show_json(BASE, "integration/animo-synthetic/ANIMO-SYNQ03_STATUS.json")
    oracle = show_json(BASE, "integration/animo-synthetic/SYNQ03_TCD037_A2_ORACLE.json")
    req(syn["state"] == "QUALIFIED_TCD037_A2_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2", "SYNQ03 not qualified")
    req(syn["target"] == "TCD-037-A2", "wrong SYNQ03 target")
    req(syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "SYNQ03 evidence strength promoted")
    req(syn["historical_behavior"] == "UNKNOWN", "SYNQ03 historical behaviour promoted")
    req(syn["tier_a_waiver_granted"] is False and syn["scientific_admission"] is False, "SYNQ03 overclaims waiver/admission")
    req(syn["full_carbon_ledger_closure_claimed"] is False, "SYNQ03 overclaims carbon ledger")
    req(syn["testcase_translation_performed"] is False, "SYNQ03 translated testcase")
    req(oracle["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"] == "PASS", "synthetic activation not qualified")
    req(oracle["accounting_contract"]["ch4_formation_total"] == "sum(QPrCH4(1:Nl)*St)", "formation owner changed")
    req(oracle["accounting_contract"]["ch4_atmosphere_emission_total"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "emission owner changed")
    req(oracle["accounting_contract"]["full_model_co2_ledger_claim"] is False, "oracle overclaims CO2 ledger")
    req(oracle["allowed_difference_surface"] == EXPECTED_FIELDS, "SYNQ03 difference surface changed")

    rg = show_json(RG05H, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    req(rg["work_status"]["qualified"] is True, "RG05H not qualified")
    req(rg["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "RG05H routing changed")
    req(rg["b4_open"] is False and rg["production_open"] is False, "later project gate unexpectedly open")

    b3d = show_json(B3D21, "integration/animo-b3/ANIMO-B3D21_STATUS.json")
    req(b3d["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "B3D21 state changed")
    req(b3d["target_child_atom"] == "TCD-037-A1", "B3D21 target changed")
    req(b3d["admission_effect"]["parent_tcd_admitted"] is False, "B3D21 admitted parent")
    req(b3d["admission_effect"]["sibling_atoms_admitted"] == [], "B3D21 admitted A2/A3/A4")

    b3i = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    req(b3i["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 not qualified")
    req("TCD-037-A2" in b3i["intake"]["child_atoms"], "A2 not canonical")
    req(b3i["readiness_routes"]["TCD-037-A2"] == "ANIMO-B3A06", "A2 route changed")
    req(b3i["intake"]["child_class"] == "A_ACCOUNTING_REPORTING_ONLY", "A2 class changed")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    req(rq["semantic_qualification"]["ch4_total_formation_owner"] == "sum(QPrCH4(1:Nl)*St)", "RUNTIMEQ03 formation owner changed")
    req(rq["semantic_qualification"]["ch4_atmosphere_emission_owner"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "RUNTIMEQ03 emission owner changed")
    req(rq["semantic_qualification"]["ch4_index0_overloaded"] is True, "RUNTIMEQ03 overload finding changed")
    req(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural-case state changed")
    req(rq["historical_intel_behavior"] == "UNKNOWN", "history promoted")

    synq01 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    req(synq01["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM", "SYNQ01 changed")

    gov05 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(gov05["decision"] == "QUALIFIED_SINGLE_AGENT_ADVERSARIAL_REVIEW_GOVERNANCE_WITH_EXPLICITLY_REDUCED_INDEPENDENCE_ASSURANCE_NO_SCIENTIFIC_GATE_REDUCTION", "GOV05 decision changed")
    req(gov05["work_status"]["qualified"] is True and gov05["work_status"]["work_unit_complete"] is True, "GOV05 not qualified")
    p5 = show_text(GOV05, "docs/governance/ANIMO_GOV05_SINGLE_AGENT_REVIEW_POLICY.md")
    req("The GOV04 Tier-A waiver is retained without weakening" in p5, "GOV05 Tier-A preservation missing")
    req("STRICTEST_APPLICABLE_RISK_TRIGGER_WINS" in p5, "GOV05 strictest-tier rule missing")
    req("scientific evidence gates themselves are not reduced" in p5, "GOV05 scientific-gate preservation missing")

    p4 = show_text(GOV04, "docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    req("purpose-built synthetic activation" in p4 and "independently qualified for causality and scope" in p4, "GOV04 activation rule missing")
    req("If any condition is false or unknown" in p4, "GOV04 fail-closed Tier-A rule missing")

    g3 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 closure changed")
    req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 route changed")
    req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 unexpectedly recovered B2")

    schema = show_text(B3Q01, "integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    req("^TCD-[0-9]{3}$" in schema, "B3Q01 top-level TCD schema changed")


def validate_records() -> None:
    rd = json.loads(READINESS.read_text(encoding="utf-8"))
    st = json.loads(STATUS.read_text(encoding="utf-8"))
    req(rd["work_unit"] == "ANIMO-B3A06" and rd["target_child_atom"] == "TCD-037-A2", "wrong readiness identity")
    req(rd["risk_tier_at_readiness"] == "A" and rd["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "wrong tier/class")
    req(rd["authorities"]["gov05_current"] == f"ANIMO-GOV05@{GOV05}", "GOV05 not bound")
    req(rd["governance_transition"]["authority_consumed"] is True, "GOV05 transition not consumed")
    req(rd["governance_transition"]["tier_a_rule"] == "GOV04_TIER_A_WAIVER_RETAINED_WITHOUT_WEAKENING", "Tier-A governance changed")
    req(rd["governance_transition"]["scientific_gate_reduction"] is False, "scientific gates reduced")

    claim = rd["atomic_claim"]
    req(claim["atomic"] is True, "A2 not atomic")
    req(claim["formation_total_owner"] == "sum(QPrCH4(1:Nl) * St)", "wrong formation owner")
    req(claim["atmosphere_emission_owner"] == "(QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St", "wrong emission owner")
    req(claim["full_model_co2_ledger_claim"] is False, "full CO2 ledger overclaim")
    req(claim["siblings_in_scope"] == [] and claim["tcd032_036_in_scope"] == [], "scope contamination")

    diff = rd["expected_difference"]
    req(diff["allowed_observer_fields"] == EXPECTED_FIELDS, "difference whitelist changed")
    req(diff["predeclared_before_b3a06"] is True, "difference contract not predeclared")
    for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy", "unrelated_observer_fields", "sibling_atoms", "full_model_co2_ledger"):
        req(diff[key] == "NONE", f"unexpected difference in {key}")

    cov = rd["coverage"]
    req(cov["natural_active_ghg"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural activation changed")
    req(cov["natural_case_translation_performed"] is False, "testcase translated")
    req(cov["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "B1 promoted")
    req(cov["synthetic_activation_predicate"] == "PASS" and cov["historical_behavior"] == "UNKNOWN", "coverage/history gate failed")

    waiver = rd["gov04_tier_a_waiver_predicate"]
    for key, value in waiver.items():
        if key in {"readiness_result", "final_waiver_granted", "final_waiver_grant_deferred_to_admission_workunit"}:
            continue
        req(value in {"PASS", "PASS_IF_EXACT_B3A06_CI_GREEN"}, f"Tier-A predicate {key} not PASS: {value}")
    req(waiver["readiness_result"] == "TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS", "wrong waiver result")
    req(waiver["final_waiver_granted"] is False and waiver["final_waiver_grant_deferred_to_admission_workunit"] is True, "waiver improperly granted")
    req(rd["gov05_tier_a_application"]["separate_review_phase_required_when_all_tier_a_predicates_pass"] is False, "Tier-A review process misrepresented")
    req(rd["gov05_tier_a_application"]["independence_claim_made"] is False, "independence overclaim")
    req(rd["readiness_gates"]["REVIEW_PROCESS"] == "PASS_NOT_APPLICABLE_TIER_A_ALL_WAIVER_PREDICATES_PASS", "review gate wrong")
    req(rd["readiness_gates"]["ADMISSION"] == "NOT_PERFORMED", "admission performed")
    req(rd["b3q01_child_schema_binding"]["later_disposition_tcd_ids"] == ["TCD-037"], "parent binding wrong")
    req(rd["b3q01_child_schema_binding"]["canonical_atomic_child_identity"] == "TCD-037-A2", "child binding wrong")
    req(rd["decision"] == "QUALIFIED_TCD037_A2_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION", "decision changed")
    req(rd["next_work_unit"].startswith("ANIMO-B3D22"), "next route wrong")
    for value in rd["scope_guards"].values():
        req(value is False, "readiness scope guard opened")

    req(st["work_unit"] == "ANIMO-B3A06" and st["target_child_atom"] == "TCD-037-A2", "wrong status identity")
    req(st["authorities"]["gov05_current"] == f"ANIMO-GOV05@{GOV05}", "status lacks GOV05")
    req(st["governance_transition"]["authority_consumed"] is True, "status does not consume GOV05")
    req(st["tier_a_waiver"]["final_waiver_granted"] is False, "status grants final waiver")
    req(st["state"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_TCD037_A2_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION"}, "status lifecycle invalid")
    for value in st["scope_guards"].values():
        req(value is False, "status scope guard opened")

    doc = DOC.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    req("does not grant the final Tier-A waiver" in doc, "doc overclaims waiver")
    req("GOV05 explicitly retains the GOV04 Tier-A waiver without weakening" in doc, "doc misses GOV05 Tier-A rule")
    req("No model-wide CO2-ledger closure is claimed" in doc, "doc misses CO2 boundary")
    req("ANIMO-B3D22" in doc and "ANIMO-B3D22" in contract, "next route missing")


def validate_scope() -> None:
    changed = {p for p in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if p}
    req(changed == ALLOWED, f"B3A06 scope mismatch: {sorted(changed ^ ALLOWED)}")
    for path in changed:
        req(not path.startswith(("src/", "reference/source/", "reference/testcases/")), f"forbidden path changed: {path}")


def main() -> None:
    validate_authorities()
    validate_records()
    validate_scope()
    print("ANIMO-B3A06 TCD-037-A2 GOV05-governed Tier-A readiness validator PASS")


if __name__ == "__main__":
    main()
