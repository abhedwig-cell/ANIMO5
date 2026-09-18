#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="8f0e8e4bfd0b391b781f7c69b7d2063d5cf8705e"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
ARCH05="99b6098a19db405ce34928af89bb78b856dce7cd"
IO01="2bcf65360b08d278f28f1cc61ac96714db4793a3"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("UBFORCE01 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-ubforce01/ANIMO-UBFORCE01_STATUS.json")
mp=load("integration/animo-ubforce01/UBFORCE01_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

arch=show_json(ARCH05,"integration/animo-architecture/ANIMO-ARCH05_STATUS.json")
if arch.get("qualified") is not True:
    fail("ARCH05 not qualified")
hydro=(subprocess.check_output(["git","show",f"{ARCH05}:docs/arch05/HYDROLOGY_EXCHANGE_CONTRACT.md"],cwd=R,text=True))
if "Solute boundary composition is separate" not in hydro:
    fail("ARCH05 solute-separation rule missing")

io=show_json(IO01,"integration/animo-io/ANIMO-IO01_STATUS.json")
if io.get("qualified") is not True:
    fail("IO01 not qualified")
if io.get("non_admissions",{}).get("BOUNDARY_migration") is not False:
    fail("BOUNDARY migration unexpectedly admitted")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier D missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
members=mp.get("source_members",{})
if members.get("UBoundconc.for",{}).get("sha256")!="b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7":
    fail("UBoundconc pin")
if members.get("input1.for",{}).get("sha256")!="041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95":
    fail("input1 pin")
ub=members.get("UBoundconc.for",{})
if ub.get("bounded_route")!="Iwa=2 AND Iopthyvs=1":
    fail("bounded route")
if ub.get("dry_deposition")!="SEPARATE_STATE_PULSE_BEFORE_LOAD_CALCULATION_NOT_INCLUDED_IN_LOAD1_TO_LOAD6":
    fail("dry deposition ownership")
if len(ub.get("load_channels",{}))!=6:
    fail("load-channel mapping")
if mp.get("contract_boundary",{}).get("already_resolved_load_carrier_owned_here") is not True:
    fail("carrier ownership")
for k in ["raw_boundary_parser_owned_here","raw_hydrology_owned_here","load_formula_execution_owned_here","dry_deposition_owned_here"]:
    if mp.get("contract_boundary",{}).get(k) is not False:
        fail("ownership overclaim "+k)

mod=(R/"prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90").read_text()
for required in [
 "ANIMO_TCD042_UPPER_SOLUTE_LOADS_V1",
 "KG_CONSTITUENT_M-2_D-1",
 "REV53_IWA2_IOPTHYVS1_DETAILED",
 "character(len=96) :: forcing_execution_id",
 "real(real64) :: load1_nh",
 "real(real64) :: load2_ni",
 "real(real64) :: load3_diorma",
 "real(real64) :: load4_diorni",
 "logical :: phosphorus_enabled",
 "logical :: has_phosphorus_loads",
 "real(real64) :: load5_po",
 "real(real64) :: load6_diorpo",
 "SUBDAY_UPPER_LOAD_FORCING_NOT_QUALIFIED",
 "INACTIVE_PHOSPHORUS_LOADS_MUST_BE_EXACT_ZERO"
]:
    if required not in mod:
        fail("implementation drift "+required)
for forbidden in ["Coprnhyn","Prr-Rupr","Prirr*","Runon*","Runinu*","Drdep"]:
    if forbidden in mod:
        fail("source resolver leaked into carrier "+forbidden)

allowed_prefixes=("prototype/ubforce01/","tests/ubforce01/","docs/ubforce01/","integration/animo-ubforce01/")
allowed_exact={
 ".github/workflows/animo-ubforce01-upper-solute-load.yml",
 "tools/validate_ubforce01_upper_solute_load.py"
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
    print("PASS_UBFORCE01_AUTHORING")
elif st.get("state")=="QUALIFIED_TCD042_UPPER_SOLUTE_LOAD_FORCING_CONTRACT_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-ubforce01/ANIMO-UBFORCE01_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_mapping_qualified") is not True or st.get("typed_contract_qualified") is not True:
        fail("qualification flags")
    if st.get("boundary_parser_qualified") is not False or st.get("load_resolver_execution_qualified") is not False:
        fail("execution overclaim")
    if st.get("direct_kt12_forcing_composition_unlocked") is not False:
        fail("composition unlocked prematurely")
    print("PASS_UBFORCE01_QUALIFIED_CONTRACT")
else:
    fail("unexpected state")
