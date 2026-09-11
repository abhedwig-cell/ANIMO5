#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3A07 / TCD-037-A3 Tier-A readiness."""
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "94afe7d649a8c60758a41996f0059de0acddd2fc"
SYNQ04 = "31d4ac628edf43501b403f0844dd472bcc12644c"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
READINESS = ROOT / "integration/animo-b3/TCD037_A3_TIER_A_READINESS.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3A07_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3a07-tcd037-a3.yml",
    "docs/b3a07/WORK_UNIT_CONTRACT.md",
    "docs/b3a07/TCD037_A3_TIER_A_READINESS.md",
    "integration/animo-b3/TCD037_A3_TIER_A_READINESS.json",
    "integration/animo-b3/ANIMO-B3A07_STATUS.json",
    "tools/validate_b3a07_tcd037_a3.py",
}


def req(c,m):
    if not c: raise SystemExit("B3A07 FAIL_CLOSED: "+m)

def run(*args):
    return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True).stdout

def show_json(ref,path):
    return json.loads(run("git","show",f"{ref}:{path}"))

def main():
    rd=json.loads(READINESS.read_text())
    st=json.loads(STATUS.read_text())

    req(subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"],cwd=ROOT).returncode==0,"RG05I base is not ancestor")
    rg=show_json(BASE,"integration/animo-reg/ANIMO-RG05I_STATUS.json")
    req(rg["state"]=="QUALIFIED_THIRD_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05H_ADMISSIONS_NO_PRODUCTION","RG05I not qualified")
    req(rg["scientific_admission_count"]==14 and rg["tcd037_state"]["parent_admitted"] is False,"RG05I aggregate state drift")
    req(rg["tcd037_state"]["admitted_children"]==["TCD-037-A1","TCD-037-A2"],"RG05I sibling admission state drift")
    req(rg["tcd037_state"]["unadmitted_children"]==["TCD-037-A3","TCD-037-A4"],"A3/A4 aggregate state drift")
    req(rg["b4_open"] is False and rg["production_open"] is False,"RG05I opens downstream gate")

    syn=show_json(SYNQ04,"integration/animo-synthetic/ANIMO-SYNQ04_STATUS.json")
    oracle=show_json(SYNQ04,"integration/animo-synthetic/SYNQ04_TCD037_A3_ORACLE.json")
    req(syn["state"]=="QUALIFIED_TCD037_A3_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2","SYNQ04 not qualified")
    req(syn["target"]=="TCD-037-A3" and syn["evidence_strength"]=="B1_SYNTHETIC_NOT_B2","wrong synthetic target/strength")
    req(syn["gov05_activation_predicate"]=="PASS_AT_EVIDENCE_LEVEL_REQUIRES_REEVALUATION_IN_B3A07","SYNQ04 activation handoff drift")
    req(syn["tier_a_waiver_granted"] is False and syn["scientific_admission"] is False,"SYNQ04 overclaims waiver/admission")
    req(syn["historical_behavior"]=="UNKNOWN" and syn["testcase_translation_performed"] is False,"SYNQ04 history/testcase boundary drift")
    req(oracle["accounting_contract"]["source_owner"]=="QPrN2Oden(Ln)*St","SYNQ04 source owner drift")
    req(oracle["accounting_contract"]["observer_increment"]=="10000*QPrN2Oden(Ln)*St","SYNQ04 observer identity drift")
    req(oracle["allowed_difference_surface"]==["Bani(N2Od)"],"SYNQ04 scope widened")

    b3i=show_json(B3I07,"integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms={x["atom_id"]:x for x in b3i["atoms"]}
    a3=atoms["TCD-037-A3"]
    req(a3["class"]=="A_ACCOUNTING_REPORTING_ONLY" and a3["source_owner"]=="QPrN2Oden(Ln)*St","B3I07 A3 identity drift")
    req(a3["allowed_observer_fields"]==["Bani(N2Od)"],"B3I07 A3 surface drift")
    req(a3["historical_behavior"]=="UNKNOWN" and a3["natural_activation"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH","B3I07 evidence boundary drift")

    rq=show_json(RUNTIMEQ03,"integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    req(rq["semantic_qualification"]["n2o_denitrification_layer_formation_owner"]=="QPrN2Oden(Ln)*St","RUNTIMEQ03 A3 source owner drift")
    req(rq["expected_difference"]["physical_state"]=="NONE" and rq["expected_difference"]["process_flux"]=="NONE","RUNTIMEQ03 non-interference drift")
    req(rq["natural_active_ghg_case"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH" and rq["historical_intel_behavior"]=="UNKNOWN","RUNTIMEQ03 evidence boundary drift")

    s1=show_json(SYNQ01,"integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    req(s1["status"]=="QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM","SYNQ01 policy drift")
    g5=show_json(GOV05,"integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(g5["work_status"]["qualified"] is True and g5["assurance_change"]["scientific_gate_reduction"] is False,"GOV05 invalid/weakened")
    g4=show_json(GOV04,"integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
    req(g4["tier_a_independent_review_waiver_conditions"]["logic"]=="ALL_MUST_PASS","Tier-A waiver logic drift")
    req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True,"strictest trigger rule lost")
    g3=show_json(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"]=="B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT","GOV03 B2 closure drift")
    req(g3["qualified_G6U_state"]=="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS","GOV03 G6U drift")
    schema=run("git","show",f"{B3Q01}:integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    req("^TCD-[0-9]{3}$" in schema,"B3Q01 lineage schema drift")

    req(rd["work_unit"]=="ANIMO-B3A07" and rd["target_child_atom"]=="TCD-037-A3","wrong readiness identity")
    req(rd["target_parent_tcd"]=="TCD-037" and rd["qualification_class"]=="A_ACCOUNTING_REPORTING_ONLY" and rd["risk_tier_at_readiness"]=="A","wrong parent/class/tier")
    claim=rd["atomic_claim"]
    req(claim["atomic"] is True and claim["source_owner"]=="QPrN2Oden(Ln)*St","atomic owner invalid")
    req(claim["local_observer_increment"]=="10000*QPrN2Oden(Ln)*St" and claim["allowed_observer_fields"]==["Bani(N2Od)"],"accounting surface invalid")
    req(claim["global_Ly_equals_Ln_theorem_claimed"] is False,"unsupported global index theorem claimed")
    req(claim["nitrification_observer_in_scope"] is False and claim["atmosphere_emission_observer_in_scope"] is False and claim["reduction_sink_in_scope"] is False,"A3 scope widened")
    acct=rd["accounting_identity"]
    req(acct["observer_increment"]=="Delta Bani(N2Od,Ly)=10000*QPrN2Oden(Ln)*St","readiness observer identity drift")
    req(acct["numerical_acceptance"]=="EXACT_BINARY64_FOR_CHOSEN_DYADIC_SYNTHETIC_VALUES_NO_EMPIRICAL_TOLERANCE","numerical acceptance drift")
    diff=rd["expected_difference"]
    req(diff["allowed_observer_fields"]==["Bani(N2Od)"] and diff["predeclared_before_b3a07"] is True,"expected difference invalid")
    for k in ("physical_state","process_flux","restart_state","solver_or_numerical_policy","Banh_N2On","Bani_N2Oe","QRdN2O","unrelated_observer_fields","sibling_atoms","tcd032_036"):
        req(diff[k]=="NONE",f"unexpected difference {k}")
    cov=rd["coverage"]
    req(cov["synthetic_activation_predicate"]=="PASS" and cov["synthetic_evidence_strength"]=="B1_SYNTHETIC_NOT_B2","coverage predicate invalid")
    req(cov["natural_active_ghg"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH" and cov["natural_case_translation_performed"] is False and cov["historical_behavior"]=="UNKNOWN","coverage/history boundary invalid")
    waiver=rd["gov04_tier_a_waiver_predicate"]
    for k,v in waiver.items():
        if k in {"readiness_result","final_waiver_granted","final_waiver_grant_deferred_to_admission_workunit"}: continue
        req(v in {"PASS","PASS_IF_EXACT_B3A07_CI_GREEN"},f"Tier-A predicate not PASS: {k}={v}")
    req(waiver["readiness_result"]=="TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS" and waiver["final_waiver_granted"] is False and waiver["final_waiver_grant_deferred_to_admission_workunit"] is True,"waiver lifecycle invalid")
    req(rd["aggregate_context"]["scientific_admission_count"]==14 and rd["aggregate_context"]["tcd037_parent_admitted"] is False,"aggregate context invalid")
    req(rd["b3q01_child_schema_binding"]["later_disposition_tcd_ids"]==["TCD-037"] and rd["b3q01_child_schema_binding"]["canonical_atomic_child_identity"]=="TCD-037-A3","child binding invalid")

    req(st["state"] in {"PERSISTED_VALIDATION_PENDING","QUALIFIED_TCD037_A3_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION"},"status lifecycle invalid")
    req(st["target_child_atom"]=="TCD-037-A3" and st["tier_a_waiver"]["final_waiver_granted"] is False,"status target/waiver invalid")
    for k,v in st["scope_guards"].items(): req(v is False,f"scope guard violated: {k}")

    changed=[x.strip() for x in run("git","diff","--name-only",BASE,"HEAD").splitlines() if x.strip()]
    req(set(changed)==ALLOWED,"scope differs from exact six-file B3A07 package: "+repr(sorted(changed)))
    for p in changed:
        req(not p.startswith(("src/","reference/","production/")),"protected source/B0 modified: "+p)
        req("THEORY_CODE_DISCREPANCY_REGISTER" not in p,"canonical TCD register modified")
    print("B3A07 PASS: TCD-037-A3 satisfies retained Tier-A readiness predicate; no admission or final waiver performed")

if __name__=="__main__": main()
