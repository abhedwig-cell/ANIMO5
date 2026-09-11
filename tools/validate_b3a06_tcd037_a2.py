#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3A06 / TCD-037-A2 readiness."""
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE="0ca6b31dc8d003ab2b86ced29a2ff8923496ee38"
RG05H="3e4247928bb43f30def951fa8804560636affbef"
B3D21="331f6ed91d4a1c15a23ae0c1ad75d1b540f61858"
B3I07="54679c7555a963133dfd686648af334f479c5808"
RQ03="a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01="842f72300fd03ede0b9024537a7ee6126722a121"
GOV05="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"
GOV03="cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01="846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
READINESS=ROOT/"integration/animo-b3/TCD037_A2_TIER_A_READINESS.json"
STATUS=ROOT/"integration/animo-b3/ANIMO-B3A06_STATUS.json"
DOC=ROOT/"docs/b3a06/TCD037_A2_TIER_A_READINESS.md"
CONTRACT=ROOT/"docs/b3a06/WORK_UNIT_CONTRACT.md"
ALLOWED={
 ".github/workflows/animo-b3a06-tcd037-a2.yml",
 "docs/b3a06/WORK_UNIT_CONTRACT.md","docs/b3a06/TCD037_A2_TIER_A_READINESS.md",
 "integration/animo-b3/TCD037_A2_TIER_A_READINESS.json","integration/animo-b3/ANIMO-B3A06_STATUS.json",
 "tools/validate_b3a06_tcd037_a2.py"}
EXPECTED=["Btom(CH4e)","Btom(CO2e) formation-side dissimilation complement only"]

def run(*a): return subprocess.run(a,cwd=ROOT,text=True,capture_output=True,check=True).stdout
def req(x,m):
    if not x: raise AssertionError(m)
def sj(c,p): return json.loads(run("git","show",f"{c}:{p}"))
def st(c,p): return run("git","show",f"{c}:{p}")

def authorities():
    s=sj(BASE,"integration/animo-synthetic/ANIMO-SYNQ03_STATUS.json")
    o=sj(BASE,"integration/animo-synthetic/SYNQ03_TCD037_A2_ORACLE.json")
    req(s["state"]=="QUALIFIED_TCD037_A2_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2","SYNQ03 not qualified")
    req(s["target"]=="TCD-037-A2" and s["evidence_strength"]=="B1_SYNTHETIC_NOT_B2","SYNQ03 identity/strength changed")
    req(s["historical_behavior"]=="UNKNOWN" and not s["tier_a_waiver_granted"] and not s["scientific_admission"],"SYNQ03 overclaim")
    req(not s["full_carbon_ledger_closure_claimed"] and not s["testcase_translation_performed"],"SYNQ03 scope widened")
    req(o["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"]=="PASS","synthetic activation not qualified")
    req(o["accounting_contract"]["ch4_formation_total"]=="sum(QPrCH4(1:Nl)*St)","formation owner changed")
    req(o["accounting_contract"]["ch4_atmosphere_emission_total"]=="(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St","emission owner changed")
    req(not o["accounting_contract"]["full_model_co2_ledger_claim"] and o["allowed_difference_surface"]==EXPECTED,"oracle scope changed")

    rg=sj(RG05H,"integration/animo-reg/ANIMO-RG05H_STATUS.json")
    req(rg["work_status"]["qualified"] and rg["current_routing_authority"]==f"ANIMO-B3I07@{B3I07}","RG05H invalid")
    req(not rg["b4_open"] and not rg["production_open"],"later project gate open")
    d=sj(B3D21,"integration/animo-b3/ANIMO-B3D21_STATUS.json")
    req(d["state"]=="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and d["target_child_atom"]=="TCD-037-A1","B3D21 changed")
    req(not d["admission_effect"]["parent_tcd_admitted"] and d["admission_effect"]["sibling_atoms_admitted"]==[],"B3D21 widened")
    b=sj(B3I07,"integration/animo-b3/ANIMO-B3I07_STATUS.json")
    req("TCD-037-A2" in b["intake"]["child_atoms"] and b["readiness_routes"]["TCD-037-A2"]=="ANIMO-B3A06","A2 routing changed")
    req(b["intake"]["child_class"]=="A_ACCOUNTING_REPORTING_ONLY","A2 class changed")
    q=sj(RQ03,"integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    req(q["semantic_qualification"]["ch4_total_formation_owner"]=="sum(QPrCH4(1:Nl)*St)","RQ03 formation changed")
    req(q["semantic_qualification"]["ch4_atmosphere_emission_owner"]=="(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St","RQ03 emission changed")
    req(q["semantic_qualification"]["ch4_index0_overloaded"],"RQ03 overload finding lost")
    req(q["natural_active_ghg_case"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH" and q["historical_intel_behavior"]=="UNKNOWN","RQ03 evidence boundary changed")
    req(sj(SYNQ01,"integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")["status"]=="QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM","SYNQ01 changed")

    g5=sj(GOV05,"integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(g5["decision"]=="QUALIFIED_SINGLE_AGENT_ADVERSARIAL_REVIEW_GOVERNANCE_WITH_EXPLICITLY_REDUCED_INDEPENDENCE_ASSURANCE_NO_SCIENTIFIC_GATE_REDUCTION","GOV05 decision changed")
    req(g5["work_status"]["qualified"] and g5["work_status"]["work_unit_complete"],"GOV05 not qualified")
    p5=st(GOV05,"docs/governance/ANIMO_GOV05_SINGLE_AGENT_REVIEW_POLICY.md")
    req("The GOV04 Tier-A waiver is retained without weakening" in p5 and "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS" in p5,"GOV05 Tier-A rule missing")
    req("scientific evidence gates themselves are not reduced" in p5,"GOV05 gate preservation missing")
    p4=st(GOV04,"docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    req("purpose-built synthetic activation" in p4 and "independently qualified for causality and scope" in p4 and "If any condition is false or unknown" in p4,"GOV04 Tier-A rule changed")
    g3=sj(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"]=="B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT","GOV03 closure changed")
    req(g3["qualified_G6U_state"]=="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" and not g3["hard_boundaries"]["historical_B2_recovered"],"GOV03 route changed")
    req("^TCD-[0-9]{3}$" in st(B3Q01,"integration/animo-b3/B3_DISPOSITION_SCHEMA.json"),"B3Q01 schema changed")

def records():
    r=json.loads(READINESS.read_text()); s=json.loads(STATUS.read_text())
    req(r["work_unit"]=="ANIMO-B3A06" and r["target_child_atom"]=="TCD-037-A2","wrong readiness identity")
    req(r["qualification_class"]=="A_ACCOUNTING_REPORTING_ONLY" and r["risk_tier_at_readiness"]=="A","wrong class/tier")
    req(r["authorities"]["gov05_current"]==f"ANIMO-GOV05@{GOV05}" and r["governance_transition"]["authority_consumed"],"GOV05 not consumed")
    req(r["governance_transition"]["tier_a_rule"]=="GOV04_TIER_A_WAIVER_RETAINED_WITHOUT_WEAKENING" and not r["governance_transition"]["scientific_gate_reduction"],"governance weakened")
    c=r["atomic_claim"]
    req(c["atomic"] and c["formation_total_owner"]=="sum(QPrCH4(1:Nl) * St)","formation claim wrong")
    req(c["atmosphere_emission_owner"]=="(QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St","emission claim wrong")
    req(not c["full_model_co2_ledger_claim"] and c["siblings_in_scope"]==[] and c["tcd032_036_in_scope"]==[],"claim scope widened")
    d=r["expected_difference"]
    req(d["allowed_observer_fields"]==EXPECTED and d["predeclared_before_b3a06"],"difference contract wrong")
    for k in ("physical_state","process_flux","restart_state","solver_or_numerical_policy","unrelated_observer_fields","sibling_atoms","full_model_co2_ledger"): req(d[k]=="NONE",f"unexpected difference {k}")
    v=r["gov04_tier_a_waiver_predicate"]
    for k,x in v.items():
        if k not in {"readiness_result","final_waiver_granted","final_waiver_grant_deferred_to_admission_workunit"}: req(x in {"PASS","PASS_IF_EXACT_B3A06_CI_GREEN"},f"Tier-A {k} not PASS")
    req(v["readiness_result"]=="TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS" and not v["final_waiver_granted"] and v["final_waiver_grant_deferred_to_admission_workunit"],"waiver lifecycle wrong")
    req(not r["gov05_tier_a_application"]["separate_review_phase_required_when_all_tier_a_predicates_pass"] and not r["gov05_tier_a_application"]["independence_claim_made"],"Tier-A review overclaim")
    req(r["readiness_gates"]["ADMISSION"]=="NOT_PERFORMED","admission performed")
    req(r["b3q01_child_schema_binding"]["later_disposition_tcd_ids"]==["TCD-037"] and r["b3q01_child_schema_binding"]["canonical_atomic_child_identity"]=="TCD-037-A2","child binding wrong")
    ids=r["identifier_collision_check"]
    req(ids["ANIMO-B3D22"].startswith("ALLOCATED_TO_TCD031") and ids["ANIMO-B3D23"].startswith("ALLOCATED_TO_TCD031"),"collision record incomplete")
    req(ids["ANIMO-B3D24"].startswith("FREE_AT_LAST_B3A06_CLOSEOUT_CHECK"),"B3D24 candidate state missing")
    req(r["next_work_unit"].startswith("ANIMO-B3D24"),"next route wrong")
    for x in r["scope_guards"].values(): req(x is False,"readiness scope opened")

    req(s["work_unit"]=="ANIMO-B3A06" and s["target_child_atom"]=="TCD-037-A2","status identity wrong")
    req(s["authorities"]["gov05_current"]==f"ANIMO-GOV05@{GOV05}" and s["governance_transition"]["authority_consumed"],"status GOV05 wrong")
    req(not s["tier_a_waiver"]["final_waiver_granted"],"status grants waiver")
    req(s["identifier_collision_check"]["ANIMO-B3D23"].startswith("ALLOCATED_TO_TCD031"),"status collision missing")
    req(s["next_if_exact_head_ci_green"].startswith("ANIMO-B3D24"),"status route wrong")
    req(s["state"] in {"PERSISTED_VALIDATION_PENDING","QUALIFIED_TCD037_A2_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION"},"status lifecycle wrong")
    for x in s["scope_guards"].values(): req(x is False,"status scope opened")
    doc=DOC.read_text(); con=CONTRACT.read_text()
    req("does not grant the final Tier-A waiver" in doc and "No model-wide CO2-ledger closure is claimed" in doc,"doc boundary missing")
    req("ANIMO-B3D23` allocated" in doc and "ANIMO-B3D24" in doc and "ANIMO-B3D24" in con,"identifier routing doc wrong")

def scope():
    changed={p for p in run("git","diff","--name-only",BASE,"HEAD").splitlines() if p}
    req(changed==ALLOWED,f"scope mismatch: {sorted(changed^ALLOWED)}")
    for p in changed: req(not p.startswith(("src/","reference/source/","reference/testcases/")),f"forbidden path {p}")

def main():
    authorities(); records(); scope(); print("ANIMO-B3A06 TCD-037-A2 Tier-A readiness validator PASS")
if __name__=="__main__": main()
