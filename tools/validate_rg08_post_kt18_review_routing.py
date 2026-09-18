#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]

RG07="c60dd36a38a2030e4f4ac1925f95b2966a6d1c87"
KT17="6d05b270e21a41ca626adbb719f8f55bfa9a97b5"
KT18="42d8837f85acd0c4c9e29b323d8b2cb1bfdd4d72"
B3Q06="11e9bcdc6654e63f84875bf1f28dc54abe725700"

def fail(msg):
    print("RG08 FAIL_CLOSED:", msg)
    raise SystemExit(1)

def load(path):
    return json.loads((R/path).read_text())

def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

status=load("integration/animo-reg/ANIMO-RG08_STATUS.json")
reb=load("integration/animo-reg/RG08_PROGRAM_REBASELINE.json")
bundle=load("integration/animo-reg/RG08_INDEPENDENT_REVIEW_BUNDLE.json")

rg07=show_json(RG07,"integration/animo-reg/ANIMO-RG07_STATUS.json")
if rg07.get("state")!="QUALIFIED_POST_KT16_PROGRAM_REBASELINE_CANDIDATE_STACK_FROZEN_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG07 predecessor not qualified")
if rg07.get("b4_open") is not False or rg07.get("production_open") is not False:
    fail("RG07 production gates unexpectedly open")

kt17=show_json(KT17,"integration/animo-kt17/ANIMO-KT17_STATUS.json")
if kt17.get("state")!="QUALIFIED_ACCEPTED_CHECKPOINT_MANIFEST_SHA256_INTEGRITY_AND_IDENTITY_BINDING_TIER_D_REVIEW_REQUIRED":
    fail("KT17 state mismatch")
if kt17.get("independent_review_completed") is not False or kt17.get("production_authorized") is not False:
    fail("KT17 admission/review overclaim")

kt18=show_json(KT18,"integration/animo-kt18/ANIMO-KT18_STATUS.json")
if kt18.get("state")!="QUALIFIED_MULTI_PACKET_PROVIDER_TO_ACCEPTED_APPLICATION_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    fail("KT18 state mismatch")
if kt18.get("independent_review_completed") is not False or kt18.get("production_authorized") is not False:
    fail("KT18 admission/review overclaim")

b3=show_json(B3Q06,"integration/animo-b3/ANIMO-B3Q06_STATUS.json")
if b3.get("whole_b3_composition_complete") is not False:
    fail("B3 unexpectedly complete")
if b3.get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]:
    fail("B3 unresolved frontier drift")
if b3.get("decision")!="B3_COMPOSITION_INCOMPLETE_DO_NOT_OPEN_TB7_B4_OR_PRODUCTION":
    fail("B3 closure decision drift")

central=reb.get("central_admitted_runtime_authorities",{})
if central.get("kt06")!="ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de":
    fail("KT06 central authority drift")
if central.get("kt11")!="ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480":
    fail("KT11 central authority drift")
if central.get("changed_by_rg08") is not False:
    fail("RG08 must not alter central runtime authority")

if reb.get("current_scientific_aggregate",{}).get("unadmitted_top_level")!=["TCD-016","TCD-034","TCD-040"]:
    fail("RG08 scientific frontier")
gates=reb.get("project_gates",{})
for key in ["b3_complete","tb7_open","b4_open","production_open","status_a_claimed","status_aa_claimed"]:
    if gates.get(key) is not False:
        fail("project gate unexpectedly open: "+key)
if gates.get("denominator_status")!="DENOMINATOR_NOT_YET_QUALIFIED":
    fail("denominator status")

if bundle.get("bundle_role")!="INDEPENDENT_REVIEW_LOGISTICS_ONLY":
    fail("review bundle role")
if bundle.get("assurance_created_by_bundle")!="NONE":
    fail("review bundle creates assurance")
if bundle.get("genuinely_independent_reviewer_required") is not True:
    fail("independent reviewer gate missing")

tier_c=bundle.get("tier_c_targets",[])
tier_d=bundle.get("tier_d_targets",[])
if len(tier_c)!=6 or len(tier_d)!=14:
    fail("review target count drift")
ids=[x.get("id") for x in tier_c+tier_d]
if len(ids)!=len(set(ids)):
    fail("duplicate review targets")
for required in ["STATEQ08","STATEQ09","STATEQ10","BOUNDQ01","BOUNDQ02","BOUNDQ02B",
                 "KT12","HYDROQ01","HYDROQ02","HYDROEXEC01","UBFORCE01","UBFORCE02",
                 "KT13A","STATEQ11","KT14B","KT15","KT15A","KT16","KT17","KT18"]:
    if required not in ids:
        fail("missing review target "+required)

ext=reb.get("external_provider_materialization_boundary",{})
if ext.get("pinned_lwkm_swatre_unf_sha256")!="b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c":
    fail("pinned external provider source hash")
if ext.get("packet_count")!=1800 or ext.get("complete_sequence_identity_qualified_as_b1") is not True:
    fail("KT08 source-sequence evidence")
if ext.get("raw_b0_source_committed_to_repo") is not False:
    fail("raw B0 source unexpectedly committed")
if ext.get("kt18_runtime_file_decoder_implemented") is not False:
    fail("runtime file decoder overclaim")

for k,v in status.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard boundary "+k)

allowed_prefixes=("integration/animo-reg/","docs/governance/")
allowed_exact={
    ".github/workflows/animo-rg08-post-kt18-review-routing.yml",
    "tools/validate_rg08_post_kt18_review_routing.py"
}
changed=subprocess.check_output(["git","diff","--name-only",KT18+"..HEAD"],cwd=R,text=True).splitlines()
for p in changed:
    if p in allowed_exact or p.startswith(allowed_prefixes):
        continue
    fail("scope escape "+p)

if status.get("state")=="NOT_YET_QUALIFIED":
    if status.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_RG08_AUTHORING")
elif status.get("state")=="QUALIFIED_POST_KT18_PROGRAM_REBASELINE_REVIEW_ROUTING_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    review=load("integration/animo-reg/ANIMO-RG08_ADVERSARIAL_REVIEW.json")
    if review.get("outcome")!="SELF_REVIEW_PASS":
        fail("self review outcome")
    if review.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or review.get("genuinely_independent") is not False:
        fail("self review assurance")
    if status.get("independent_reviews_completed") is not False:
        fail("independent review falsely completed")
    if status.get("work_status",{}).get("qualified") is not True:
        fail("final status not qualified")
    print("PASS_RG08_QUALIFIED_REBASELINE")
else:
    fail("unexpected RG08 state")
