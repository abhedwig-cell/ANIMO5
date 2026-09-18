#!/usr/bin/env python3
import json, pathlib, subprocess, re
R=pathlib.Path(__file__).resolve().parents[1]
BASE="50731bf118deb8ef1029f220a40b39a99240e480"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
KT12="8f0e8e4bfd0b391b781f7c69b7d2063d5cf8705e"
B3D35="9ca23f41dc3c28af686b1bc0bff8e7d66416d367"
KT06="56384db4107aed484218363e26dbb7be7f51e8de"
KT11="50731bf118deb8ef1029f220a40b39a99240e480"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("HYDROQ01 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-hydroq01/ANIMO-HYDROQ01_STATUS.json")
mp=load("integration/animo-hydroq01/HYDROQ01_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

kt12=show_json(KT12,"integration/animo-kt12/ANIMO-KT12_STATUS.json")
if kt12.get("state")!="QUALIFIED_BOUNDED_TCD042_TRANSACTION_RUNTIME_CLIENT_DIRECT_KT11_SCIENCE_COMPOSITION_BLOCKED_TIER_D_REVIEW_REQUIRED":
    fail("KT12 state")
if kt12.get("direct_kt11_composition_ready") is not False:
    fail("KT12 composition unexpectedly ready")

p=show_json(B3D35,"integration/animo-b3/ANIMO-B3D35_STATUS.json")
expected="Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))"
if p.get("supported_scope")!=expected or p.get("admitted") is not True:
    fail("TCD042 parent authority")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier D missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
members=mp.get("source_members",{})
pins={
 "Hydro_detailed.for":"f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d",
 "MODFLUX.FOR":"0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d",
 "UBoundconc.for":"b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7"
}
for name,sha in pins.items():
    if members.get(name,{}).get("sha256")!=sha:
        fail("source member pin "+name)
inv=mp.get("derived_bounded_invariant",{})
if inv.get("result")!=["Rurv=exact zero","Flib(1)>=0","TCD042 Flux=Flib(1)"]:
    fail("derived bounded invariant")
if mp.get("ownership",{}).get("interchangeable") is not False:
    fail("raw/resolved ownership collapse")

mod=(R/"prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90").read_text()
for required in [
 "ANIMO_TCD042_RESOLVED_UPPER_HYDROLOGY_V1",
 "ANIMO_RESOLVED_HYDROLOGY_UNITS_V1",
 "REV53_HYDRO_DETAILED_THEN_MODFLUX",
 "character(len=96) :: execution_id",
 "real(real64) :: flib_top",
 "real(real64) :: rurv",
 "if (value%flpn /= 0)",
 "value%flib_top < 0.0_real64",
 "exact_binary_zero(value%rurv)",
 "SUBDAY_RESOLVED_HYDROLOGY_NOT_QUALIFIED"
]:
    if required not in mod:
        fail("contract implementation drift "+required)

for forbidden in ["call hydro_detailed","call modflux","subroutine hydro_detailed","subroutine modflux"]:
    if forbidden in mod.lower():
        fail("forbidden science implementation "+forbidden)

allowed_prefixes=(
 "prototype/hydroq01/","tests/hydroq01/","docs/hydroq01/","integration/animo-hydroq01/",
)
allowed_exact={
 ".github/workflows/animo-hydroq01-resolved-upper-hydrology.yml",
 "tools/validate_hydroq01_resolved_upper_hydrology.py"
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
    print("PASS_HYDROQ01_AUTHORING")
elif st.get("state")=="QUALIFIED_TCD042_POST_HYDRO_DETAILED_RESOLVED_UPPER_HYDROLOGY_CONTRACT_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-hydroq01/ANIMO-HYDROQ01_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("typed_contract_qualified") is not True or st.get("source_mapping_qualified") is not True:
        fail("final qualification flags")
    if st.get("hydro_detailed_execution_qualified") is not False or st.get("modflux_execution_qualified") is not False:
        fail("execution overclaim")
    if st.get("direct_kt11_to_kt12_composition_unlocked") is not False:
        fail("composition unlocked prematurely")
    print("PASS_HYDROQ01_QUALIFIED_CONTRACT")
else:
    fail("unexpected state")
