#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3D24 / TCD-037-A2 atomic admission."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
BASE="466718167b22a643b26ee5035a18514987b6e289"
RG05H="3e4247928bb43f30def951fa8804560636affbef"
B3I07="54679c7555a963133dfd686648af334f479c5808"
RQ03="a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ03="0ca6b31dc8d003ab2b86ced29a2ff8923496ee38"
GOV05="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"
GOV03="cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01="846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3Q02="1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3"
WAIVER=ROOT/"integration/animo-b3/TCD037_A2_TIER_A_WAIVER_AUDIT.json"
CARRIER=ROOT/"integration/animo-b3/TCD037_A2_CHILD_ATOM_FORMAL_DISPOSITION.json"
STATUS=ROOT/"integration/animo-b3/ANIMO-B3D24_STATUS.json"
DOC=ROOT/"docs/b3d24/TCD037_A2_TIER_A_ADMISSION_DECISION.md"
CONTRACT=ROOT/"docs/b3d24/WORK_UNIT_CONTRACT.md"
ALLOWED={
 ".github/workflows/animo-b3d24-tcd037-a2.yml",
 "docs/b3d24/WORK_UNIT_CONTRACT.md","docs/b3d24/TCD037_A2_TIER_A_ADMISSION_DECISION.md",
 "integration/animo-b3/TCD037_A2_TIER_A_WAIVER_AUDIT.json",
 "integration/animo-b3/TCD037_A2_CHILD_ATOM_FORMAL_DISPOSITION.json",
 "integration/animo-b3/ANIMO-B3D24_STATUS.json","tools/validate_b3d24_tcd037_a2.py"}
EXPECTED=["Btom(CH4e)","Btom(CO2e) formation-side dissimilation complement only"]

def run(*a): return subprocess.run(a,cwd=ROOT,text=True,capture_output=True,check=True).stdout
def req(x,m):
    if not x: raise AssertionError(m)
def sj(c,p): return json.loads(run("git","show",f"{c}:{p}"))
def st(c,p): return run("git","show",f"{c}:{p}")

def authorities():
    r=sj(BASE,"integration/animo-b3/ANIMO-B3A06_STATUS.json")
    req(r["state"]=="QUALIFIED_TCD037_A2_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION","B3A06 not qualified")
    req(r["target_child_atom"]=="TCD-037-A2" and r["work_status"]["qualified"] and r["work_status"]["work_unit_complete"],"B3A06 identity/lifecycle wrong")
    req(r["tier_a_waiver"]["predicate_pass_at_readiness"] and not r["tier_a_waiver"]["final_waiver_granted"],"B3A06 waiver lifecycle wrong")
    req(r["validation"]["run_id"]==34547343685 and r["validation"]["tested_head"]=="74a12ef80f4dd68a482f267dc2a57606a8cae2fe","B3A06 persisted precloseout evidence changed")

    syn=sj(SYNQ03,"integration/animo-synthetic/ANIMO-SYNQ03_STATUS.json")
    ora=sj(SYNQ03,"integration/animo-synthetic/SYNQ03_TCD037_A2_ORACLE.json")
    req(syn["state"]=="QUALIFIED_TCD037_A2_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2","SYNQ03 not qualified")
    req(syn["evidence_strength"]=="B1_SYNTHETIC_NOT_B2" and syn["historical_behavior"]=="UNKNOWN","SYNQ03 boundary changed")
    req(not syn["tier_a_waiver_granted"] and not syn["scientific_admission"] and not syn["testcase_translation_performed"],"SYNQ03 overclaim")
    req(ora["accounting_contract"]["ch4_formation_total"]=="sum(QPrCH4(1:Nl)*St)","formation owner changed")
    req(ora["accounting_contract"]["ch4_atmosphere_emission_total"]=="(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St","emission owner changed")
    req(ora["allowed_difference_surface"]==EXPECTED and not ora["accounting_contract"]["full_model_co2_ledger_claim"],"SYNQ03 scope changed")

    b=sj(B3I07,"integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms={a["atom_id"]:a for a in b["atoms"]}; req("TCD-037-A2" in atoms,"A2 not canonical")
    a=atoms["TCD-037-A2"]
    req(a["class"]=="A_ACCOUNTING_REPORTING_ONLY" and a["allowed_observer_fields"]==EXPECTED,"A2 class/surface changed")
    req(a["source_owners"]["formation_total"]=="sum(QPrCH4(1:Nl)*St)","routing formation owner changed")
    req(a["source_owners"]["atmosphere_emission"]=="(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St","routing emission owner changed")
    req(not a["wider_ghg_carbon_ledger_claim"],"routing widened carbon-ledger claim")

    q=sj(RQ03,"integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    req(q["semantic_qualification"]["ch4_index0_overloaded"],"RUNTIMEQ03 overload finding lost")
    req(q["historical_intel_behavior"]=="UNKNOWN" and q["natural_active_ghg_case"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH","RUNTIMEQ03 boundary changed")

    g5=sj(GOV05,"integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(g5["work_status"]["qualified"] and g5["work_status"]["work_unit_complete"],"GOV05 not qualified")
    p5=st(GOV05,"docs/governance/ANIMO_GOV05_SINGLE_AGENT_REVIEW_POLICY.md")
    req("The GOV04 Tier-A waiver is retained without weakening" in p5 and "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS" in p5,"GOV05 Tier-A rule missing")
    req("scientific evidence gates themselves are not reduced" in p5,"GOV05 gate preservation missing")
    p4=st(GOV04,"docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    req("If any condition is false or unknown" in p4 and "purpose-built synthetic activation" in p4,"GOV04 Tier-A rule changed")
    g3=sj(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"]=="B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT","GOV03 closure changed")
    req(g3["qualified_G6U_state"]=="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" and not g3["hard_boundaries"]["historical_B2_recovered"],"GOV03 route changed")
    rg=sj(RG05H,"integration/animo-reg/ANIMO-RG05H_STATUS.json")
    req(rg["work_status"]["qualified"] and not rg["b4_open"] and not rg["production_open"],"RG05H invalid")

def schemas_and_carrier():
    cs=sj(B3Q02,"integration/animo-b3/B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json")
    ds=sj(B3Q01,"integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    Draft202012Validator.check_schema(cs); Draft202012Validator.check_schema(ds)
    c=json.loads(CARRIER.read_text()); Draft202012Validator(cs).validate(c); Draft202012Validator(ds).validate(c["b3_disposition"])
    req(c["carrier_mode"]=="FORMAL_DISPOSITION" and c["parent_tcd_id"]=="TCD-037" and c["atom_id"]=="TCD-037-A2","carrier identity wrong")
    req(c["canonical_routing"]["work_unit"]=="ANIMO-B3I07" and c["canonical_routing"]["atomization_ref"]=="integration/animo-b3/B3I07_TCD037_ATOMIZATION.json","carrier routing wrong")
    d=c["b3_disposition"]
    req(d["tcd_ids"]==["TCD-037"] and d["atomicity"]=="ATOMIC" and d["qualification_class"]=="A","embedded disposition identity wrong")
    req(d["admission_route"]==c["route_state"]=="INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY","route mismatch")
    req(d["disposition"]=="HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY","disposition wrong")
    req(d["admission_decision"]["admitted"] and d["admission_decision"]["decision_scope"]=="CANONICAL_CHILD_ATOM:TCD-037-A2","admission scope wrong")
    req(c["admission_effect"]["atom_admitted"] and not c["admission_effect"]["parent_admitted"],"carrier admission effect wrong")
    req(not c["admission_effect"]["new_top_level_tcd_reserved"] and not c["admission_effect"]["canonical_register_append"] and not c["admission_effect"]["production_migration_admitted"],"carrier widened project state")
    ir=d["evidence"]["independent_review"]; ig=d["gates"]["independent_review"]
    req(ir["status"]=="INCOMPLETE" and ir["result"]=="NOT_REVIEWED" and not ir["independent_from_correction_authoring"],"waived review evidence misrepresented")
    req(ig["status"]=="PASS" and ig["applicability"]=="NOT_APPLICABLE","waived review gate wrong")
    for g in d["gates"].values(): req(g["status"]=="PASS","a B3 gate is not PASS")
    req(not d["composition"]["is_composition"] and d["composition"]["component_record_ids"]==[],"composition introduced")

def records():
    w=json.loads(WAIVER.read_text()); s=json.loads(STATUS.read_text())
    req(w["target"]=="CANONICAL_CHILD_ATOM:TCD-037-A2" and w["risk_tier"]=="A","waiver target wrong")
    for k,v in w["predicates"].items(): req(v in {"PASS","PASS_IF_EXACT_B3D24_CI_GREEN"},f"Tier-A predicate {k} not PASS")
    req(w["all_predicates_pass"] and w["final_tier_a_waiver_granted_for_this_atomic_admission_object"],"final Tier-A waiver not granted")
    req(not w["review_gate"]["separate_independent_second_line_required"] and not w["review_gate"]["review_performed"] and not w["review_gate"]["independence_claimed"],"review waiver overclaim")
    req(w["review_gate"]["b3q01_evidence_result"]=="NOT_REVIEWED" and w["review_gate"]["b3q01_gate_applicability"]=="NOT_APPLICABLE","review representation wrong")
    req(w["evidence_boundary"]["synthetic_strength"]=="B1_SYNTHETIC_NOT_B2" and w["evidence_boundary"]["historical_revision53_behavior"]=="UNKNOWN","evidence boundary promoted")
    req(not w["evidence_boundary"]["testcase_translation_performed"] and not w["evidence_boundary"]["full_model_co2_ledger_claim"],"waiver boundary widened")

    req(s["work_unit"]=="ANIMO-B3D24" and s["target_child_atom"]=="TCD-037-A2","status identity wrong")
    req(s["state"] in {"PERSISTED_VALIDATION_PENDING","ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY"},"status lifecycle wrong")
    req(s["tier_a_waiver"]["all_predicates_pass"] and s["tier_a_waiver"]["final_waiver_granted_for_exact_atomic_object"],"status waiver wrong")
    req(not s["tier_a_waiver"]["independence_claimed"],"status claims independence")
    req(s["candidate_admission_effect"]["historical_revision53_behavior"]=="UNKNOWN" and s["candidate_admission_effect"]["synthetic_evidence_strength"]=="B1_SYNTHETIC_NOT_B2","status history/evidence promoted")
    req(not s["candidate_admission_effect"]["parent_tcd_admitted"] and s["candidate_admission_effect"]["sibling_atoms_admitted"]==[],"status admits parent/sibling")
    for v in s["hard_boundaries"].values(): req(v is False,"hard boundary opened")
    doc=DOC.read_text(); con=CONTRACT.read_text()
    req("No independent second-line review is claimed" in doc and "No model-wide CO2-ledger closure" in doc,"decision doc boundary missing")
    req("CANONICAL_CHILD_ATOM:TCD-037-A2" in con,"contract child binding missing")

def scope():
    changed={p for p in run("git","diff","--name-only",BASE,"HEAD").splitlines() if p}
    req(changed==ALLOWED,f"B3D24 scope mismatch: {sorted(changed^ALLOWED)}")
    for p in changed: req(not p.startswith(("src/","reference/source/","reference/testcases/")),f"forbidden path changed: {p}")

def main():
    authorities(); schemas_and_carrier(); records(); scope(); print("ANIMO-B3D24 TCD-037-A2 Tier-A atomic admission validator PASS")
if __name__=="__main__": main()
