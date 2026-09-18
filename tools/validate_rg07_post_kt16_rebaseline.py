#!/usr/bin/env python3
import json, pathlib, subprocess, re

R=pathlib.Path(__file__).resolve().parents[1]
BASE="7cd863b71a7a7fcc985514a8af28dcb69cae999a"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
RG05O="bc9e6ed997a078336645210ebb4d99ae976893fe"
B3Q06="11e9bcdc6654e63f84875bf1f28dc54abe725700"
B3B14="1f13c7cab30772f4aa8d5071b19d13761c2b5f16"
GHG14="b82e5de364396eef3132f33cc48f8c28ab5aa04e"
B3B04E3="fedf2177b8228507beb91d7318b5f4dec5078241"
KT06="56384db4107aed484218363e26dbb7be7f51e8de"
KT11="50731bf118deb8ef1029f220a40b39a99240e480"
KT13A="df2310cc69e3fe16187ba2235843222f8acfb726"
STATEQ09="f6e91fc1cb664d67caccc02e6ab21525a768d006"
STATEQ10="614391014438b2cc4445d2d6a8008c3f0f1c45d0"
BOUNDQ01="62b4fc36f2a47b67c08eedb095c60a5c059b77d8"
BOUNDQ02="fb0c0c842aed9a90378aca613279e09a856ad09b"
BOUNDQ02B="de6eef3122354e74405ff9c92286794714bdee82"
STATEQ11="c2bd0d17ac6921fcd9f22d6289a510cae454153d"
KT14B="46e9e7397be751f245069033bae655b4382b63bd"
KT15="d3a51aad084969a753cb5b54c604ebefba4b26c6"
KT15A="2279a961459211e03550dfda4af09ab4f7f6b9a3"
KT16="7cd863b71a7a7fcc985514a8af28dcb69cae999a"

def fail(msg):
    print("RG07 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def gj(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def remote_heads():
    out=subprocess.check_output(["git","ls-remote","--heads","origin"],cwd=R,text=True)
    d={}
    for line in out.splitlines():
        if line.strip():
            sha,ref=line.split("\t",1); d[ref]=sha
    return d

rb=load("integration/animo-reg/RG07_PROGRAM_REBASELINE.json")
st=load("integration/animo-reg/ANIMO-RG07_STATUS.json")

rg6=gj(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg6.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 predecessor state")

q=gj(B3Q06,"integration/animo-b3/ANIMO-B3Q06_STATUS.json")
if q.get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]:
    fail("B3Q06 unresolved set")
if q.get("whole_b3_composition_complete") is not False:
    fail("B3 unexpectedly complete")
if q.get("tb7_allowed") is not False or q.get("b4_allowed") is not False or q.get("production_allowed") is not False:
    fail("B3Q06 gates")

t16=gj(KT16,"integration/animo-kt16/ANIMO-KT16_STATUS.json")
if t16.get("state")!="QUALIFIED_ACCEPTED_APPLICATION_CHECKPOINT_SPLIT_RUN_RESTART_TIER_D_REVIEW_REQUIRED":
    fail("KT16 state")
for k in ["accepted_boundary_checkpoint_qualified","typed_checkpoint_record_qualified","trusted_restore_path_qualified","exact_split_run_equivalence_qualified","corrupt_checkpoint_rejection_qualified","expected_config_restore_binding_qualified"]:
    if t16.get(k) is not True: fail("KT16 missing qualification "+k)
for k in ["file_format_qualified","integrity_hash_qualified","canonical_checkpoint_admitted","canonical_state_admitted","historical_b2_restart_equivalence_claimed","independent_review_completed","production_authorized"]:
    if t16.get(k) is not False: fail("KT16 overclaim "+k)

t15a=gj(KT15A,"integration/animo-kt15a/ANIMO-KT15A_STATUS.json")
if t15a.get("state")!="QUALIFIED_IMMUTABLE_APPLICATION_CONFIGURATION_BINDING_TIER_D_REVIEW_REQUIRED":
    fail("KT15A state")
if t15a.get("source_hash_verification_qualified") is not False:
    fail("KT15A source hash unexpectedly qualified")

t15=gj(KT15,"integration/animo-kt15/ANIMO-KT15_STATUS.json")
if t15.get("state")!="QUALIFIED_ATOMIC_COMPOSITE_APPLICATION_COMMIT_TIER_D_REVIEW_REQUIRED":
    fail("KT15 state")
if t15.get("atomic_group_publication_qualified") is not True or t15.get("two_interval_continuation_qualified") is not True:
    fail("KT15 application semantics")

t14b=gj(KT14B,"integration/animo-kt14b/ANIMO-KT14B_STATUS.json")
if t14b.get("state")!="QUALIFIED_OPAQUE_BOUNDQ02B_FRAME_TO_KT13A_TCD042_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    fail("KT14B state")
if t14b.get("opaque_frame_consumption_qualified") is not True:
    fail("KT14B opaque frame")

sq11=gj(STATEQ11,"integration/animo-state/ANIMO-STATEQ11_STATUS.json")
if sq11.get("state")!="QUALIFIED_COMPOSITE_ACCEPTED_CONTINUATION_IDENTITY_TIER_D_REVIEW_REQUIRED":
    fail("STATEQ11 state")
if sq11.get("atomic_group_commit_implemented") is not False:
    fail("STATEQ11 scope overclaim")

b2b=gj(BOUNDQ02B,"integration/animo-boundq02b/ANIMO-BOUNDQ02B_STATUS.json")
if b2b.get("state")!="QUALIFIED_OPAQUE_CONTENT_BOUND_STATIC_BOUNDARY_FRAME_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ02B state")
if b2b.get("source_hash_verification_qualified") is not False:
    fail("BOUNDQ02B source hash unexpectedly qualified")

b2=gj(BOUNDQ02,"integration/animo-boundq02/ANIMO-BOUNDQ02_STATUS.json")
if b2.get("state")!="QUALIFIED_REV53_STATIC_BOUNDARY_YEAR_CURSOR_AND_INTERVAL_BINDING_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ02 state")
if b2.get("canonical_cursor_state_admitted") is not False:
    fail("BOUNDQ02 cursor admission overclaim")

b1=gj(BOUNDQ01,"integration/animo-boundq01/ANIMO-BOUNDQ01_STATUS.json")
if b1.get("state")!="QUALIFIED_REV53_STATIC_BOUNDARY_CHEMISTRY_ADAPTER_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ01 state")

s9=gj(STATEQ09,"integration/animo-state/ANIMO-STATEQ09_STATUS.json")
if s9.get("state")!="QUALIFIED_DETAILED_HYDROLOGY_ACCEPTED_ENDPOINT_TO_NEXT_ORIGIN_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    fail("STATEQ09 state")
if s9.get("canonical_state_admitted") is not False:
    fail("STATEQ09 canonical state overclaim")

s10=gj(STATEQ10,"integration/animo-state/ANIMO-STATEQ10_STATUS.json")
if s10.get("state")!="QUALIFIED_FIRST_INTERVAL_DETAILED_HYDROLOGY_ORIGIN_NORMALIZATION_TIER_C_REVIEW_REQUIRED":
    fail("STATEQ10 state")
if s10.get("first_call_runinu_qualified") is not False:
    fail("STATEQ10 first-call Runinu overclaim")

k13=gj(KT13A,"integration/animo-kt13a/ANIMO-KT13A_STATUS.json")
if k13.get("state")!="QUALIFIED_KT13_COMPOSITION_COHERENCE_REMEDIATION_INDEPENDENT_TIER_D_REVIEW_STILL_REQUIRED":
    fail("KT13A state")
if k13.get("scope",{}).get("admission_performed") is not False:
    fail("KT13A admission overclaim")

t16b=rb.get("strongest_current_bounded_application_claim",{})
if t16b.get("authority")!="ANIMO-KT16@"+KT16:
    fail("rebaseline strongest application authority")

if rb.get("current_scientific_aggregate",{}).get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]:
    fail("rebaseline unresolved set")
if rb.get("project_gates",{}).get("b3_complete") is not False:
    fail("rebaseline B3")
for k in ["tb7_open","b4_open","production_open","status_a_claimed","status_aa_claimed"]:
    if rb.get("project_gates",{}).get(k) is not False:
        fail("rebaseline project gate "+k)
if rb.get("project_gates",{}).get("denominator_status")!="DENOMINATOR_NOT_YET_QUALIFIED":
    fail("denominator")

if rb.get("central_admitted_runtime_authorities",{}).get("kt06")!="ANIMO-KT06-A1@"+KT06:
    fail("central KT06 pin")
if rb.get("central_admitted_runtime_authorities",{}).get("kt11")!="ANIMO-KT11-A1@"+KT11:
    fail("central KT11 pin")

f16=rb.get("scientific_frontier",{}).get("TCD-016",{})
if f16.get("authority")!="ANIMO-B3B14@"+B3B14 or f16.get("b3_admitted") is not False:
    fail("TCD016 frontier")
f34=rb.get("scientific_frontier",{}).get("TCD-034",{})
if f34.get("authority")!="ANIMO-GHG14@"+GHG14 or len(f34.get("remaining_material_gates",[]))!=3:
    fail("TCD034 frontier")
f40=rb.get("scientific_frontier",{}).get("TCD-040",{})
if f40.get("authority")!="ANIMO-B3B04E3@"+B3B04E3 or f40.get("b3_admitted") is not False:
    fail("TCD040 frontier")

heads=remote_heads()
pins={
 "work/animo-kt16-accepted-application-checkpoint-restart":KT16,
 "work/animo-kt15a-immutable-application-config":KT15A,
 "work/animo-kt15-atomic-composite-application-commit":KT15,
 "work/animo-kt14b-opaque-boundary-frame-composition":KT14B,
 "work/animo-boundq02b-immutable-boundary-frame":BOUNDQ02B,
 "work/animo-boundq02-static-boundary-year-binding":BOUNDQ02,
 "work/animo-stateq11-composite-accepted-continuation":STATEQ11,
 "work/animo-stateq10-first-interval-detailed-hydrology-origin":STATEQ10,
 "work/animo-stateq09-detailed-hydrology-origin-continuation":STATEQ09,
 "work/animo-kt13a-composition-coherence-remediation":KT13A,
 "work/animo-boundq01-tcd042-static-boundary-chemistry":BOUNDQ01,
 "work/animo-b3b14-tcd016-parent-closure-readiness":B3B14,
 "work/animo-ghg14-tcd034-class-f-readiness-reassessment":GHG14,
 "work/animo-ghg15-tcd034-spruce-file-level-joinability":GHG14,
 "work/animo-b3b04e3-tcd040-reconstructed-replay-harness":B3B04E3
}
for name,sha in pins.items():
    if heads.get("refs/heads/"+name)!=sha:
        fail("live head drift "+name)

for ref in heads:
    m=re.search(r"refs/heads/work/animo-rg0?7",ref)
    if m and ref!="refs/heads/work/animo-rg07-post-kt16-program-rebaseline":
        fail("newer competing RG07 branch "+ref)
    m2=re.search(r"refs/heads/work/animo-kt(\d+)",ref)
    if m2 and int(m2.group(1))>16:
        fail("post-KT16 runtime branch detected; rebaseline is stale: "+ref)

allowed={
 ".github/workflows/animo-rg07-post-kt16-program-rebaseline.yml",
 "docs/governance/ANIMO_RG07_POST_KT16_PROGRAM_REBASELINE.md",
 "integration/animo-reg/RG07_PROGRAM_REBASELINE.json",
 "integration/animo-reg/ANIMO-RG07_STATUS.json",
 "integration/animo-reg/ANIMO-RG07_ADVERSARIAL_REVIEW.json",
 "tools/validate_rg07_post_kt16_rebaseline.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(changed)-allowed)
if extra: fail("scope escape "+str(extra))
for p in changed:
    if p.startswith("src/") or p.startswith("prototype/") or p.startswith("integration/animo-b3/"):
        fail("forbidden mutation "+p)

for k,v in st.get("hard_boundaries",{}).items():
    if v is not False: fail("hard boundary "+k)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False: fail("authoring qualification flag")
    print("RG07 PASS authoring rebaseline")
elif st.get("state")=="QUALIFIED_POST_KT16_PROGRAM_REBASELINE_CANDIDATE_STACK_FROZEN_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    rv=load("integration/animo-reg/ANIMO-RG07_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS": fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("review",{}).get("completed") is not True: fail("review completion")
    if st.get("work_status",{}).get("qualified") is not True or st.get("work_status",{}).get("workunit_complete") is not True:
        fail("final work status")
    print("RG07 PASS qualified post-KT16 program rebaseline")
else:
    fail("unexpected state")
