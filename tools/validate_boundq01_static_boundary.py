#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="931e32cec69dc78a03015f01190cff97bf1fe1b4"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
IO01="2bcf65360b08d278f28f1cc61ac96714db4793a3"
ARCH05="99b6098a19db405ce34928af89bb78b856dce7cd"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("BOUNDQ01 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(p):
    return json.loads((R/p).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-boundq01/ANIMO-BOUNDQ01_STATUS.json")
nat=load("integration/animo-boundq01/BOUNDQ01_NATURAL_TESTBANK_SCAN.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 gates")

io=show_json(IO01,"integration/animo-io/ANIMO-IO01-CLOSEOUT.json")
if io.get("non_admissions",{}).get("BOUNDARY_migration") is not False:
    fail("IO01 boundary nonadmission")
arch=show_json(ARCH05,"integration/animo-architecture/ANIMO-ARCH05_STATUS.json")
if arch.get("qualified") is not True:
    fail("ARCH05")
gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "C" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier C")

if nat.get("testbank_sha256")!="44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84":
    fail("testbank pin")
if nat.get("natural_boundary_file_count")!=9 or nat.get("static_option_cases")!=9:
    fail("natural case count")
if nat.get("dynamic_runon_cases")!=0 or nat.get("dynamic_irrigation_cases")!=0:
    fail("natural option scan")
if {c.get("ipo") for c in nat.get("cases",[])}!={0,1}:
    fail("natural IPO coverage")
for c in nat.get("cases",[]):
    if c.get("ioptidti")!=0 or c.get("ioptirti")!=0:
        fail("natural dynamic option")
    if c.get("labels")!=[">optibc:",">topbou:",">latbou:",">botbou:"]:
        fail("label sequence inventory "+c.get("case","?"))

mod=(R/"prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90").read_text()
for required in [
 "line(1:8) == label",
 "if (value%ioptidti /= 0 .or. value%ioptirti /= 0)",
 "read(unit, *, iostat=ios) value%precipitation_nh",
 "read(unit, *, iostat=ios) value%dry_deposition_nh",
 "read(unit, *, iostat=ios) run_nh, run_ni",
 "read(unit, *, iostat=ios) irr_nh, irr_ni",
 "call find_first_label(unit, '>latbou:', status)",
 "read(unit, *, iostat=ios) in_nh, in_ni",
 "within(value%precipitation_nh,0.0_real64,1.0_real64)",
 "within(value%dry_deposition_nh,0.0_real64,100.0_real64)",
 "999.0_real64,10.0_real64,10.0_real64",
 "1.0_real64,10.0_real64,0.1_real64",
 "value%runin%don > 1.0_real64"
]:
    if required not in mod:
        fail("implementation drift "+required)

for forbidden in [">runoti:",">irriti:","BOUNDARY.INP parser migration admitted","call uboundconc"]:
    if forbidden.lower() in mod.lower():
        fail("scope widening "+forbidden)

allowed_prefixes=("prototype/boundq01/","tests/boundq01/","docs/boundq01/","integration/animo-boundq01/")
allowed_exact={
 ".github/workflows/animo-boundq01-static-boundary-chemistry.yml",
 "tools/validate_boundq01_static_boundary.py"
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
    print("PASS_BOUNDQ01_AUTHORING")
elif st.get("state")=="QUALIFIED_REV53_STATIC_BOUNDARY_CHEMISTRY_ADAPTER_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-boundq01/ANIMO-BOUNDQ01_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_grammar_qualified") is not True or st.get("typed_adapter_qualified") is not True:
        fail("qualification flags")
    if st.get("dynamic_runon_qualified") is not False or st.get("dynamic_irrigation_qualified") is not False:
        fail("dynamic scope overclaim")
    print("PASS_BOUNDQ01_QUALIFIED_STATIC_ADAPTER")
else:
    fail("unexpected state")
