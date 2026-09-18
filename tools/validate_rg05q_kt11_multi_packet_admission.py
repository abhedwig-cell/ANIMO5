#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="9a8d0d886f745be91153f47437cb0de2b3076ab2"
KT11="50731bf118deb8ef1029f220a40b39a99240e480"
REVIEW="dc91b04cd01230fcffbde12fcc8423e35d98bf85"
DISP="1bd1232bba2cb2fa576a60742d8f968ea441c252"
KT06="56384db4107aed484218363e26dbb7be7f51e8de"
FROZEN_BLOB="a41d0f61da6dd30a18dbfadbe4b29b00259fa41e"
KT06_BLOB="9a24ea833291f761d2fa76ca4cc9fee28436c614"

def fail(x):
    print("RG05Q FAIL_CLOSED:",x)
    raise SystemExit(1)

def load(p):
    return json.loads((R/p).read_text())

def gj(s,p):
    return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))

a=load("integration/animo-reg/RG05Q_KT11_MULTI_PACKET_ADMISSION_ATTACHMENT.json")
s=load("integration/animo-reg/ANIMO-RG05Q_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05P_STATUS.json")

if old.get("state")!="QUALIFIED_KT06_GOV04_TIER_C_RUNTIME_ADMISSION_INTEGRATED_NO_B3_OR_PRODUCTION_EFFECT":
    fail("RG05P state")

for k,v in [
    ("scientific_admission_count",32),
    ("historical_uncertainty_admission_count",32),
    ("top_level_admitted_tcd_count",22),
    ("admitted_child_atom_count",10)
]:
    if old.get(k)!=v or s.get(k)!=v:
        fail("unchanged count "+k)

oldkt06=old.get("central_runtime_authorities",{}).get("kt06",{})
newkt06=s.get("central_runtime_authorities",{}).get("kt06",{})
if oldkt06.get("admitted") is not True or newkt06.get("admitted") is not True:
    fail("KT06 inherited admission")
if oldkt06.get("frozen_implementation_blob")!=KT06_BLOB or newkt06.get("frozen_implementation_blob")!=KT06_BLOB:
    fail("KT06 inherited frozen blob")
if newkt06.get("authority")!="ANIMO-KT06-A1@"+KT06:
    fail("KT06 inherited authority")

adm=gj(KT11,"integration/animo-kt11/ANIMO-KT11_TIER_C_ADMISSION_STATUS.json")
if adm.get("admitted") is not True or adm.get("production_authorized") is not False:
    fail("KT11 admission boundary")
if adm.get("decision")!="ADMIT_ANIMO_KT11_BOUNDED_NONPRODUCTION_MULTI_PACKET_PROVIDER_GOV04_TIER_C":
    fail("KT11 decision")
if adm.get("independent_review_result")!="PASS_CLAIM_UNCHANGED":
    fail("KT11 independent review")
if adm.get("frozen_implementation_blob")!=FROZEN_BLOB:
    fail("KT11 frozen blob")
if adm.get("kt06_dependency_authority")!="ANIMO-KT06-A1@"+KT06:
    fail("KT11 KT06 dependency")

rv=gj(REVIEW,"integration/animo-kt11/ANIMO-KT11_INDEPENDENT_REVIEW_CHECKPOINT.json")
if rv.get("principal_verdict")!="PASS_CLAIM_UNCHANGED":
    fail("review verdict")
if rv.get("material_findings")!=[]:
    fail("review material findings")

dp=gj(DISP,"integration/animo-kt11/ANIMO-KT11_TIER_C_DISPOSITION_STATUS.json")
if dp.get("validation",{}).get("independent_review_gate")!="PASS":
    fail("formal disposition review gate")
if dp.get("validation",{}).get("scope_widening") is not False:
    fail("formal disposition scope")
if dp.get("frozen_implementation_blob")!=FROZEN_BLOB:
    fail("formal disposition frozen blob")

if a.get("runtime_authority")!="ANIMO-KT11-A1@"+KT11:
    fail("attachment authority")
if a.get("frozen_implementation",{}).get("blob")!=FROZEN_BLOB:
    fail("attachment frozen identity")
if a.get("kt06_dependency")!="ANIMO-KT06-A1@"+KT06:
    fail("attachment KT06 dependency")

ce=a.get("central_regie_effect",{})
if ce.get("b3_scientific_admission_count_change")!=0:
    fail("B3 count change")
if ce.get("b3_queue_change") is not False:
    fail("B3 queue change")
if ce.get("canonical_tcd_register_change") is not False:
    fail("TCD register change")
if ce.get("production_authorized") is not False:
    fail("production authorization")
if ce.get("composition_beyond_kt11_admitted") is not False:
    fail("composition widening")

kt11central=s.get("central_runtime_authorities",{}).get("kt11",{})
if kt11central.get("admitted") is not True:
    fail("central KT11 admission")
if kt11central.get("risk_tier")!="C":
    fail("central KT11 tier")
if kt11central.get("production_authorized") is not False:
    fail("central KT11 production")
if kt11central.get("authority")!="ANIMO-KT11-A1@"+KT11:
    fail("central KT11 authority")
if kt11central.get("frozen_implementation_blob")!=FROZEN_BLOB:
    fail("central KT11 frozen blob")

hb=s.get("hard_boundaries",{})
for k in (
    "scientific_readmission_performed",
    "production_source_modified",
    "canonical_tcd_register_modified",
    "queue_authority_modified",
    "kt06_scope_widened",
    "kt11_scope_widened",
    "scientific_execution_composed",
    "dynamic_provider_admitted",
    "retry_timestep_semantics_admitted",
    "b4_open",
    "production_open"
):
    if hb.get(k) is not False:
        fail("hard boundary "+k)

if s.get("b3_queue_changed") is not False:
    fail("queue change")

allowed={
    ".github/workflows/animo-rg05q-kt11-multi-packet-admission.yml",
    "docs/governance/ANIMO_RG05Q_KT11_MULTI_PACKET_ADMISSION_INTEGRATION.md",
    "integration/animo-reg/RG05Q_KT11_MULTI_PACKET_ADMISSION_ATTACHMENT.json",
    "integration/animo-reg/ANIMO-RG05Q_STATUS.json",
    "tools/validate_rg05q_kt11_multi_packet_admission.py"
}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(ch)-allowed)
if extra:
    fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("prototype/") or p.startswith("reference/") or p.startswith("integration/animo-b3/") or p=="docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv":
        fail("forbidden mutation "+p)

ws=s.get("work_status",{})
if ws.get("qualified") is True:
    if s.get("state")!="QUALIFIED_KT11_GOV04_TIER_C_MULTI_PACKET_ADMISSION_INTEGRATED_NO_B3_OR_PRODUCTION_EFFECT":
        fail("final state")
    v=s.get("validation",{})
    if v.get("machine_validated") is not True:
        fail("machine validation")
    if v.get("candidate_conclusion")!="success":
        fail("candidate conclusion")
    if not v.get("candidate_run_id") or not v.get("candidate_job_id") or not v.get("tested_candidate_head"):
        fail("final validation identity")
    if v.get("validator")!="PASS" or v.get("scope_guard")!="PASS":
        fail("final validator")
    print("RG05Q PASS: KT11 bounded multi-packet runtime authority integrated; B3 counts/queue and production unchanged")
else:
    if s.get("state")!="PERSISTED_VALIDATION_PENDING":
        fail("precloseout state")
    if ws.get("persisted") is not True or ws.get("tested") is not False:
        fail("precloseout work status")
    print("RG05Q PASS persisted KT11 admission integration; exact-head closeout pending")
