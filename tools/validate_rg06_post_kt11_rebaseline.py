#!/usr/bin/env python3
import json, pathlib, subprocess, re
R=pathlib.Path(__file__).resolve().parents[1]
RG05Q="3402666360d3e30105712b121a98fc4b9055926f"
RG05O="bc9e6ed997a078336645210ebb4d99ae976893fe"
B3Q06="11e9bcdc6654e63f84875bf1f28dc54abe725700"
SQ11="afdfa2e61d4a9c7e45214e096696ce8632f5c504"
GHG14="b82e5de364396eef3132f33cc48f8c28ab5aa04e"
EG01="a818b5a37b80ed92aded0b9c404990d356eb2300"
RG05M="7146612d5dfa8ad87a4660f0c50c68a5db1e3a29"
KT06="56384db4107aed484218363e26dbb7be7f51e8de"
KT11="50731bf118deb8ef1029f220a40b39a99240e480"

def fail(x):
    print("RG06 FAIL_CLOSED:",x)
    raise SystemExit(1)
def load(p):
    return json.loads((R/p).read_text())
def gj(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def remote_heads():
    out=subprocess.check_output(["git","ls-remote","--heads","origin"],cwd=R,text=True)
    d={}
    for line in out.splitlines():
        if line.strip():
            sha,ref=line.split("\t",1); d[ref]=sha
    return d

rb=load("integration/animo-reg/RG06_PROGRAM_REBASELINE.json")
st=load("integration/animo-reg/ANIMO-RG06_STATUS.json")

q=gj(B3Q06,"integration/animo-b3/ANIMO-B3Q06_STATUS.json")
if q.get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]: fail("B3Q06 unresolved set")
if q.get("whole_b3_composition_complete") is not False: fail("B3 completeness")
if q.get("tb7_allowed") is not False or q.get("b4_allowed") is not False or q.get("production_allowed") is not False: fail("B3Q06 gates")

sq=gj(SQ11,"integration/animo-science/ANIMO-SQ11_STATUS.json")
if sq.get("state")!="QUALIFIED_EXPERIMENT_DESIGN_READY_EXTERNAL_EVIDENCE_EXECUTION_REQUIRED": fail("SQ11 state")
if sq.get("physical_evidence_generated") is not False or sq.get("parent_b3_disposition")!="UNRESOLVED_NOT_ADMITTED": fail("SQ11 boundary")

g=gj(GHG14,"integration/animo-ghg/ANIMO-GHG14_STATUS.json")
if g.get("state")!="QUALIFIED_CLASS_F_READINESS_REASSESSMENT_NOT_READY_NO_ADMISSION": fail("GHG14 state")
if g.get("remaining_material_gate_count")!=3 or g.get("b3_admission_performed") is not False: fail("GHG14 gates")

eg=gj(EG01,"integration/animo-eg/ANIMO-EG01_STATUS.json")
if eg.get("controlled_immutable_storage_proven") is not False: fail("EG01 external storage unexpectedly proven")
if eg.get("reference_admitted") is not False: fail("EG01 reference promotion")

m=gj(RG05M,"integration/animo-reg/ANIMO-RG05M_STATUS.json")
t=m.get("tcd042_state",{})
if t.get("parent_admitted") is not True: fail("TCD042 parent not admitted")
if t.get("Hetop_zero_admitted") is not False or t.get("production_authorized") is not False: fail("TCD042 scope widening")

qreg=gj(RG05Q,"integration/animo-reg/ANIMO-RG05Q_STATUS.json")
if qreg.get("state")!="QUALIFIED_KT11_GOV04_TIER_C_MULTI_PACKET_ADMISSION_INTEGRATED_NO_B3_OR_PRODUCTION_EFFECT": fail("RG05Q state")
if qreg.get("b3_queue_changed") is not False: fail("RG05Q B3 mutation")
if qreg.get("central_runtime_authorities",{}).get("kt06",{}).get("authority")!="ANIMO-KT06-A1@"+KT06: fail("KT06 central pin")
if qreg.get("central_runtime_authorities",{}).get("kt11",{}).get("authority")!="ANIMO-KT11-A1@"+KT11: fail("KT11 central pin")

if rb.get("current_b3_queue",{}).get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]: fail("rebaseline unresolved set")
if rb.get("project_gates",{}).get("b3_complete") is not False: fail("rebaseline B3")
if rb.get("project_gates",{}).get("tb7_open") is not False or rb.get("project_gates",{}).get("b4_open") is not False or rb.get("project_gates",{}).get("production_open") is not False: fail("rebaseline gates")
if rb.get("denominator_status")!="DENOMINATOR_NOT_YET_QUALIFIED": fail("denominator")
if rb.get("first_real_scientific_consumer_candidate",{}).get("object")!="TCD-042": fail("KT12 candidate")
if rb.get("first_real_scientific_consumer_candidate",{}).get("production_authorized") is not False: fail("KT12 production")

heads=remote_heads()
if heads.get("refs/heads/work/animo-rg05q-kt11-multi-packet-admission-integration")!=RG05Q: fail("RG05Q live head drift")
if heads.get("refs/heads/work/animo-sq11-tcd016-c1-drydown-rewetting-experiment-design")!=SQ11: fail("SQ11 live head drift")
if heads.get("refs/heads/work/animo-ghg14-tcd034-class-f-readiness-reassessment")!=GHG14: fail("GHG14 live head drift")
if heads.get("refs/heads/work/animo-ghg15-tcd034-spruce-file-level-joinability")!=GHG14: fail("GHG15 advanced; fresh rebaseline required")
if heads.get("refs/heads/work/animo-eg01-controlled-b0-retention")!=EG01: fail("EG01 live head drift")
for ref in heads:
    m2=re.search(r"refs/heads/work/animo-b3d(\d+)-",ref)
    if m2 and int(m2.group(1))>42: fail("newer B3 admission branch detected "+ref)
    m3=re.search(r"refs/heads/work/animo-rg05([a-z])-",ref)
    if m3 and m3.group(1)>"q": fail("newer RG05 branch detected "+ref)

allowed={
 ".github/workflows/animo-rg06-post-kt11-program-rebaseline.yml",
 "docs/governance/ANIMO_RG06_POST_KT11_PROGRAM_REBASELINE.md",
 "integration/animo-reg/RG06_PROGRAM_REBASELINE.json",
 "integration/animo-reg/ANIMO-RG06_STATUS.json",
 "integration/animo-reg/ANIMO-RG06_ADVERSARIAL_REVIEW.json",
 "tools/validate_rg06_post_kt11_rebaseline.py"
}
ch=subprocess.check_output(["git","diff","--name-only",RG05Q+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("prototype/") or p.startswith("reference/") or p.startswith("integration/animo-b3/"):
        fail("forbidden mutation "+p)

for k,v in st.get("hard_boundaries",{}).items():
    if v is not False: fail("hard boundary "+k)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False: fail("authoring qualification flag")
    print("RG06 PASS authoring rebaseline")
elif st.get("state")=="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    rv=load("integration/animo-reg/ANIMO-RG06_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS": fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False: fail("review assurance")
    if st.get("review",{}).get("completed") is not True: fail("review completion")
    if st.get("work_status",{}).get("qualified") is not True or st.get("work_status",{}).get("workunit_complete") is not True: fail("final work status")
    print("RG06 PASS qualified post-KT11 program rebaseline")
else:
    fail("unexpected state")
