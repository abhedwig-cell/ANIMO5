#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="bc9e6ed997a078336645210ebb4d99ae976893fe"
KT06="56384db4107aed484218363e26dbb7be7f51e8de"
REVIEW="0d3906e0b54f21eb1a19f8137f1aabef4edff567"
DISP="b75fc91d812be689aecf2894c50b37c926e9c5fd"
FROZEN_BLOB="9a24ea833291f761d2fa76ca4cc9fee28436c614"
def fail(x): print("RG05P FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
a=load("integration/animo-reg/RG05P_KT06_RUNTIME_ADMISSION_ATTACHMENT.json")
s=load("integration/animo-reg/ANIMO-RG05P_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05O_STATUS.json")
if old.get("state")!="QUALIFIED_NINTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD033_TCD032_TCD019_NO_PRODUCTION": fail("RG05O state")
for k,v in [("scientific_admission_count",32),("historical_uncertainty_admission_count",32),("top_level_admitted_tcd_count",22),("admitted_child_atom_count",10)]:
    if old.get(k)!=v or s.get(k)!=v: fail("unchanged count "+k)
adm=gj(KT06,"integration/animo-kt06/ANIMO-KT06_TIER_C_ADMISSION_STATUS.json")
if adm.get("admitted") is not True or adm.get("production_authorized") is not False: fail("KT06 admission boundary")
if adm.get("decision")!="ADMIT_ANIMO_KT06_BOUNDED_NONPRODUCTION_RUNTIME_BINDING_GOV04_TIER_C": fail("KT06 decision")
if adm.get("independent_review_result")!="PASS_CLAIM_UNCHANGED": fail("KT06 independent review")
if adm.get("frozen_implementation_blob")!=FROZEN_BLOB: fail("KT06 frozen blob")
rv=gj(REVIEW,"integration/animo-kt06/ANIMO-KT06_INDEPENDENT_REVIEW_CHECKPOINT.json")
if rv.get("principal_verdict")!="PASS_CLAIM_UNCHANGED" or rv.get("material_findings")!=[]: fail("review checkpoint")
dp=gj(DISP,"integration/animo-kt06/ANIMO-KT06_TIER_C_DISPOSITION_STATUS.json")
if dp.get("validation",{}).get("independent_review_gate")!="PASS" or dp.get("validation",{}).get("scope_widening") is not False: fail("formal disposition")
if a.get("runtime_authority")!="ANIMO-KT06-A1@"+KT06: fail("attachment authority")
if a.get("frozen_implementation",{}).get("blob")!=FROZEN_BLOB: fail("attachment frozen identity")
ce=a.get("central_regie_effect",{})
if ce.get("b3_scientific_admission_count_change")!=0 or ce.get("b3_queue_change") is not False or ce.get("canonical_tcd_register_change") is not False or ce.get("production_authorized") is not False: fail("central effect")
hb=s.get("hard_boundaries",{})
for k in ("scientific_readmission_performed","production_source_modified","canonical_tcd_register_modified","queue_authority_modified","kt06_scope_widened","multi_packet_provider_admitted","scientific_execution_composed","b4_open","production_open"):
    if hb.get(k) is not False: fail("hard boundary "+k)
if s.get("b3_queue_changed") is not False: fail("queue change")
allowed={
".github/workflows/animo-rg05p-kt06-runtime-admission.yml",
"docs/governance/ANIMO_RG05P_KT06_RUNTIME_ADMISSION_INTEGRATION.md",
"integration/animo-reg/RG05P_KT06_RUNTIME_ADMISSION_ATTACHMENT.json",
"integration/animo-reg/ANIMO-RG05P_STATUS.json",
"tools/validate_rg05p_kt06_runtime_admission.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("prototype/") or p.startswith("reference/") or p.startswith("integration/animo-b3/") or p=="docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv": fail("forbidden mutation "+p)
ws=s.get("work_status",{})
if ws.get("qualified") is True:
    if s.get("state")!="QUALIFIED_KT06_GOV04_TIER_C_RUNTIME_ADMISSION_INTEGRATED_NO_B3_OR_PRODUCTION_EFFECT": fail("final state")
    v=s.get("validation",{})
    if v.get("machine_validated") is not True or v.get("candidate_conclusion")!="success" or not v.get("candidate_run_id") or not v.get("tested_candidate_head") or v.get("validator")!="PASS" or v.get("scope_guard")!="PASS": fail("final validation record")
    print("RG05P PASS: KT06 bounded runtime authority integrated; B3 counts/queue and production unchanged")
else:
    if s.get("state")!="PERSISTED_VALIDATION_PENDING" or ws.get("persisted") is not True or ws.get("tested") is not False: fail("precloseout state")
    print("RG05P PASS persisted KT06 runtime admission integration; exact-head closeout pending")
