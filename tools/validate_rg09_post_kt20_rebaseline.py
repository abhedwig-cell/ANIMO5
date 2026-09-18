#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="c41a28580421bf4dce770e438535ba92a57567cd"
RG08="14109956b62376d0d0ab681e8c641c9e71d110bd"
KT19="6245aad4aca962cb2a63d0394bb7f2baa686457d"
KT20="c41a28580421bf4dce770e438535ba92a57567cd"

def fail(msg):
    print("RG09 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-reg/ANIMO-RG09_STATUS.json")
rb=load("integration/animo-reg/RG09_PROGRAM_REBASELINE.json")
routing=load("integration/animo-reg/RG09_INDEPENDENT_REVIEW_ROUTING.json")

rg8=show_json(RG08,"integration/animo-reg/ANIMO-RG08_STATUS.json")
if rg8.get("state")!="QUALIFIED_POST_KT18_PROGRAM_REBASELINE_REVIEW_ROUTING_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG08 state")
if rg8.get("b3_complete") is not False or rg8.get("b4_open") is not False or rg8.get("production_open") is not False:
    fail("RG08 program gates")

kt19=show_json(KT19,"integration/animo-kt19/ANIMO-KT19_STATUS.json")
if kt19.get("state")!="QUALIFIED_PINNED_LWKM_FILE_TO_IMMUTABLE_HYDROLOGY_PROVIDER_TIER_C_REVIEW_REQUIRED":
    fail("KT19 state")
if kt19.get("pinned_source_sha256")!="b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c":
    fail("KT19 source identity")
if kt19.get("b2_claimed") is not False or kt19.get("production_authorized") is not False:
    fail("KT19 boundary")

kt20=show_json(KT20,"integration/animo-kt20/ANIMO-KT20_STATUS.json")
if kt20.get("state")!="QUALIFIED_KT19_PACKET_FRAME_TO_KT18_APPLICATION_BRIDGE_TIER_D_REVIEW_REQUIRED":
    fail("KT20 state")
for key in [
    "exact_packet_frame_qualified",
    "real_b1_packet_reaches_kt18",
    "real_b1_packet_fail_closed_preserves_application",
    "synthetic_control_commits_through_kt18",
]:
    if kt20.get(key) is not True:
        fail("KT20 missing qualification "+key)
if kt20.get("full_real_sequence_application_execution_qualified") is not False:
    fail("KT20 whole-sequence overclaim")
if kt20.get("canonical_forcing_abi_admitted") is not False:
    fail("KT20 forcing ABI overclaim")
if kt20.get("independent_review_completed") is not False:
    fail("KT20 independent review overclaim")

if rb.get("predecessor")!="ANIMO-RG08@"+RG08:
    fail("rebaseline predecessor")
if rb.get("authoring_base")!="ANIMO-KT20@"+KT20:
    fail("rebaseline base")
if rb.get("authoring_base_exact_final_ci")!=35404974857:
    fail("KT20 exact-final CI binding")
central=rb.get("central_admitted_runtime_authorities",{})
if central.get("kt06")!="ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de":
    fail("central KT06 authority")
if central.get("kt11")!="ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480":
    fail("central KT11 authority")
if central.get("changed_by_rg09") is not False:
    fail("central authority promoted")
agg=rb.get("current_scientific_aggregate",{})
if agg.get("top_level_total")!=25 or agg.get("admitted_top_level")!=22:
    fail("scientific aggregate count")
if agg.get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]:
    fail("scientific frontier set")
if agg.get("b3_complete") is not False:
    fail("B3 incorrectly complete")

ri=rb.get("real_source_interpretation",{})
if ri.get("provider_evidence_is_not_scientific_admission") is not True:
    fail("provider/science authority separation")
if ri.get("first_real_packet_outside_current_bounded_application") is not True:
    fail("real packet disposition missing")
if ri.get("full_sequence_application_claim") is not False:
    fail("full-sequence claim")

if routing.get("role")!="INDEPENDENT_REVIEW_LOGISTICS_ONLY_NOT_REVIEW_NOT_ADMISSION":
    fail("review routing role")
if routing.get("automatic_admission") is not False:
    fail("automatic admission")
waves=routing.get("review_order",[])
if len(waves)!=3:
    fail("review waves")
all_targets=[t.split("@",1)[0] for w in waves for t in w.get("targets",[])]
for target in [
    "STATEQ08","STATEQ09","STATEQ10","BOUNDQ01","BOUNDQ02","BOUNDQ02B","KT19",
    "KT12","HYDROQ01","HYDROQ02","HYDROEXEC01","UBFORCE01","UBFORCE02",
    "KT13A","STATEQ11","KT14B","KT15","KT15A","KT16","KT17","KT18","KT20"
]:
    if target not in all_targets:
        fail("review target missing "+target)

for k,v in st.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard boundary "+k)

allowed_prefixes=("integration/animo-reg/ANIMO-RG09","integration/animo-reg/RG09_","docs/regie/ANIMO_RG09")
allowed_exact={
    ".github/workflows/animo-rg09-post-kt20-rebaseline.yml",
    "tools/validate_rg09_post_kt20_rebaseline.py",
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_RG09_AUTHORING")
elif st.get("state")=="QUALIFIED_POST_KT20_REAL_SOURCE_PROVIDER_BRIDGE_REBASELINE_REVIEW_GATE_FROZEN_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    rv=load("integration/animo-reg/ANIMO-RG09_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("independent_reviews_completed") is not False:
        fail("independent review overclaim")
    if st.get("candidate_auto_admission_performed") is not False:
        fail("auto admission")
    if st.get("central_runtime_admissions_changed") is not False:
        fail("central admissions changed")
    print("PASS_RG09_QUALIFIED_REBASELINE")
else:
    fail("unexpected state")
