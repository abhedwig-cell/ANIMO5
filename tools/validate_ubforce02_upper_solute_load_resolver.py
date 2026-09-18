#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="9f9204ba53169285ac84272704de14836962ef41"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
ARCH05="99b6098a19db405ce34928af89bb78b856dce7cd"
IO01="2bcf65360b08d278f28f1cc61ac96714db4793a3"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("UBFORCE02 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-ubforce02/ANIMO-UBFORCE02_STATUS.json")
mp=load("integration/animo-ubforce02/UBFORCE02_SOURCE_MAPPING.json")

base=show_json(BASE,"integration/animo-ubforce01/ANIMO-UBFORCE01_STATUS.json")
if base.get("state")!="QUALIFIED_TCD042_UPPER_SOLUTE_LOAD_FORCING_CONTRACT_TIER_D_REVIEW_REQUIRED":
    fail("UBFORCE01 base state")
if base.get("typed_contract_qualified") is not True:
    fail("UBFORCE01 carrier not qualified")
if base.get("production_authorized") is not False:
    fail("UBFORCE01 production boundary")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 gates")

arch=show_json(ARCH05,"integration/animo-architecture/ANIMO-ARCH05_STATUS.json")
if arch.get("qualified") is not True:
    fail("ARCH05 not qualified")
doc=subprocess.check_output(["git","show",f"{ARCH05}:docs/arch05/HYDROLOGY_EXCHANGE_CONTRACT.md"],cwd=R,text=True)
if "Solute boundary composition is separate" not in doc:
    fail("ARCH05 chemistry ownership rule")

io_close=show_json(IO01,"integration/animo-io/ANIMO-IO01-CLOSEOUT.json")
if io_close.get("non_admissions",{}).get("BOUNDARY_migration") is not False:
    fail("BOUNDARY migration unexpectedly admitted")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive")
sm=mp.get("source_member",{})
if sm.get("sha256")!="b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7":
    fail("UBoundconc pin")
if sm.get("route")!="Iwa=2 AND Iopthyvs=1":
    fail("source route")
eq=mp.get("equations",{})
required_eq={
 "Wpr":"Prr-Rupr+Prsn",
 "Load1":"Wpr*Coprnhyn + Prirr*Coirrnh + Runon*Corunonnh + Runinu*Coidnh",
 "Load2":"Wpr*Coprniyn + Prirr*Coirrni + Runon*Corunonni + Runinu*Coidni",
 "Load3":"Prirr*Codiormairr + Runon*Codiormarunon + Runinu*Codiormaid",
 "Load4":"Prirr*Codiorniirr + Runon*Codiornirunon + Runinu*Codiorniid",
 "Load5_if_Ipo1":"Wpr*Coprpoyn + Prirr*Coirrpo + Runon*Corunonpo + Runinu*Coidpo",
 "Load6_if_Ipo1":"Prirr*Codiorpoirr + Runon*Codiorporunon + Runinu*Codiorpoid"
}
if eq!=required_eq:
    fail("equation mapping drift")
hc=mp.get("hydrology_context",{})
if hc.get("inferred_from_raw_runoff") is not False:
    fail("Rupr/Runinu inference introduced")
if mp.get("dry_deposition",{}).get("included") is not False:
    fail("dry deposition included")
if mp.get("numerical_policy",{}).get("tolerance_used") is not False:
    fail("tolerance introduced")

mod=(R/"prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90").read_text()
for required in [
 "precipitation_term = hydrology%prr - hydrology%rupr + hydrology%prsn",
 "hydrology%prirr * chemistry%irrigation%nh",
 "hydrology%runon * chemistry%runon%nh",
 "hydrology%runinu * chemistry%runin%nh",
 "hydrology%prirr * chemistry%irrigation%doma",
 "hydrology%runon * chemistry%runon%don",
 "hydrology%runinu * chemistry%runin%dop",
 "INACTIVE_PHOSPHORUS_CHEMISTRY_MUST_BE_EXACT_ZERO"
]:
    if required not in mod:
        fail("implementation mapping drift "+required)

for forbidden in ["Drdep", "dry deposition", "hydrology%runoff", "max(0.0_real64", "1.0e-8"]:
    if forbidden.lower() in mod.lower():
        fail("forbidden semantics in resolver "+forbidden)

test=(R/"tests/ubforce02/test_upper_solute_load_resolver.f90").read_text()
for bits in [
 "3FF6E147AE147AE2","3FFA8F5C28F5C290","3FF8F5C28F5C28F6",
 "3FFAE147AE147AE2","40010A3D70A3D70A","3FFEB851EB851EB8"
]:
    if bits not in test:
        fail("exact binary64 oracle missing "+bits)
if "<1.0e-" in test.replace(" ","").lower():
    fail("tolerance oracle found")

allowed_prefixes=("prototype/ubforce02/","tests/ubforce02/","docs/ubforce02/","integration/animo-ubforce02/")
allowed_exact={
 ".github/workflows/animo-ubforce02-upper-solute-load-resolver.yml",
 "tools/validate_ubforce02_upper_solute_load_resolver.py"
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
    print("PASS_UBFORCE02_AUTHORING")
elif st.get("state")=="QUALIFIED_TCD042_UPPER_SOLUTE_LOAD_RESOLVER_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-ubforce02/ANIMO-UBFORCE02_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_mapping_qualified") is not True or st.get("resolver_qualified") is not True:
        fail("qualification flags")
    if st.get("chemistry_parser_qualified") is not False or st.get("hydrology_partition_resolver_qualified") is not False:
        fail("scope overclaim")
    print("PASS_UBFORCE02_QUALIFIED_RESOLVER")
else:
    fail("unexpected state")
