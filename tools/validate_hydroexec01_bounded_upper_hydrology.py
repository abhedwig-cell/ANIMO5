#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="08d5b8301c217cf9d33d2bf248be133f2b5243fc"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
HYDROQ01="5301d90024c64057f2cb88fda1dbaa93aabfca47"
HYDROQ02="08d5b8301c217cf9d33d2bf248be133f2b5243fc"
B3D35="9ca23f41dc3c28af686b1bc0bff8e7d66416d367"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("HYDROEXEC01 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-hydroexec01/ANIMO-HYDROEXEC01_STATUS.json")
mp=load("integration/animo-hydroexec01/HYDROEXEC01_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 gates")

h1=show_json(HYDROQ01,"integration/animo-hydroq01/ANIMO-HYDROQ01_STATUS.json")
if h1.get("state")!="QUALIFIED_TCD042_POST_HYDRO_DETAILED_RESOLVED_UPPER_HYDROLOGY_CONTRACT_TIER_D_REVIEW_REQUIRED":
    fail("HYDROQ01 state")
if h1.get("typed_contract_qualified") is not True:
    fail("HYDROQ01 contract")

h2=show_json(HYDROQ02,"integration/animo-hydroq02/ANIMO-HYDROQ02_STATUS.json")
if h2.get("state")!="QUALIFIED_TCD042_RESOLVED_RUPR_RUNINU_LOAD_CONTEXT_TIER_D_REVIEW_REQUIRED":
    fail("HYDROQ02 state")
if h2.get("typed_context_qualified") is not True:
    fail("HYDROQ02 contract")
if h2.get("near_zero_runinu_semantics_repaired") is not False:
    fail("HYDROQ02 near-zero repair")

p=show_json(B3D35,"integration/animo-b3/ANIMO-B3D35_STATUS.json")
if p.get("admitted") is not True:
    fail("TCD042 parent not admitted")
if p.get("admission_effect",{}).get("production_authorized") is not False:
    fail("TCD042 production boundary")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
if mp.get("precision_evidence",{}).get("vfproj_sha256")!="f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a":
    fail("vfproj precision pin")
if mp.get("precision_evidence",{}).get("historical_setting")!="RealKIND=realKIND8":
    fail("historical precision setting")
members=mp.get("source_members",{})
if members.get("Hydro_detailed.for",{}).get("sha256")!="f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d":
    fail("Hydro_detailed pin")
if members.get("MODFLUX.FOR",{}).get("sha256")!="0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d":
    fail("Modflux pin")
nz=mp.get("near_zero_runoff",{})
if nz.get("revision53_Runinu_assignment")!="ABSENT" or nz.get("prototype_semantics")!="PRESERVE_EXPLICIT_CALL_ENTRY_RUNINU":
    fail("near-zero source semantics")
if nz.get("silent_zero_repair") is not False:
    fail("near-zero repair introduced")
if mp.get("positive_runoff_singularity",{}).get("scientific_repair_claimed") is not False:
    fail("singularity repair claim")

mod=(R/"prototype/hydroexec01/mod_animo_bounded_no_ponding_upper_hydrology.f90").read_text()
required=[
 "REV53_PONDING_THRESHOLD = 1.0e-4_real64",
 "REV53_RUNOFF_NEAR_ZERO = 1.0e-8_real64",
 "diagnostics%runinu = start_context%runinu_call_entry",
 "diagnostics%runinu = -projection%ru",
 "diagnostics%rupr = (1.0_real64 - start_context%lefrrv) * projection%ru",
 "diagnostics%rurv = (1.0_real64 - start_context%lefrso)",
 "diagnostics%rupr = min(diagnostics%rupr +",
 "diagnostics%rurv = 0.0_real64",
 "diagnostics%ruso = projection%ru - diagnostics%rupr",
 "projection%flab(2) + diagnostics%ruso + projection%evso",
 "diagnostics%evso_resolved = max(0.0_real64, projection%evso - diagnostics%dif)",
 "diagnostics%flib_top_resolved = max(0.0_real64, diagnostics%flab_top_resolved)",
 "PRODUCER_STEP_DOES_NOT_MATCH_KT02_INTERVAL",
 "UNQUALIFIED_REV53_RUPR_PARTITION_SINGULARITY"
]
for x in required:
    if x not in mod:
        fail("implementation drift "+x)
for forbidden in [
 "call mapohydro","subroutine mapohydro","call hydro_detailed","subroutine hydro_detailed",
 "call modflux","subroutine modflux","runinu = 0.0_real64 ! near-zero"
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden implementation "+forbidden)

test=(R/"tests/hydroexec01/test_bounded_no_ponding_upper_hydrology.f90").read_text()
if "3E10000000000000" not in test:
    fail("exact TCD042-scale binary64 oracle missing")
for name in [
 "test_near_zero_preserves_runinu_call_entry",
 "test_negative_runoff",
 "test_positive_runoff",
 "test_ponding_rejected",
 "test_step_mismatch_rejected",
 "test_partition_singularity_rejected"
]:
    if name not in test:
        fail("missing test "+name)

allowed_prefixes=("prototype/hydroexec01/","tests/hydroexec01/","docs/hydroexec01/","integration/animo-hydroexec01/")
allowed_exact={
 ".github/workflows/animo-hydroexec01-bounded-upper-hydrology.yml",
 "tools/validate_hydroexec01_bounded_upper_hydrology.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)

for k,v in st.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard boundary "+k)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_HYDROEXEC01_AUTHORING")
elif st.get("state")=="QUALIFIED_BOUNDED_REV53_NO_PONDING_UPPER_HYDROLOGY_EXECUTION_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-hydroexec01/ANIMO-HYDROEXEC01_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_mapping_qualified") is not True or st.get("bounded_execution_qualified") is not True:
        fail("qualification flags")
    if st.get("full_hydro_detailed_qualified") is not False:
        fail("full Hydro_detailed overclaim")
    if st.get("runinu_canonical_state_ownership_qualified") is not False:
        fail("Runinu ownership overclaim")
    print("PASS_HYDROEXEC01_QUALIFIED_BOUNDED_EXECUTION")
else:
    fail("unexpected state")
