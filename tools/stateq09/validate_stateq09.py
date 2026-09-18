#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[2]
BASE="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
STATEQ08="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("STATEQ09 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-state/ANIMO-STATEQ09_STATUS.json")
mp=load("integration/animo-state/STATEQ09_HYDROLOGY_ORIGIN_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 gates")

s8=show_json(STATEQ08,"integration/animo-state/ANIMO-STATEQ08_STATUS.json")
if s8.get("state")!="QUALIFIED_RUNINU_DETAILED_HYDROLOGY_EXECUTION_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    fail("STATEQ08 state")
if s8.get("canonical_state_admitted") is not False:
    fail("STATEQ08 canonical state overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "C" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier C missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
members=mp.get("source_members",{})
if members.get("Animo.for",{}).get("sha256")!="352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7":
    fail("Animo.for pin")
if members.get("Init.for",{}).get("sha256")!="287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058":
    fail("Init.for pin")
assignments=members.get("Init.for",{}).get("bounded_assignments",[])
for expected in [
    "Mofro(Ln)=Mofrt(Ln), Ln=1..Nl",
    "Snla=Snt when Iopthyvs=1",
    "Sic=Sict when Iopthyvs=1 and Hlpimp=11",
    "Pn=Pnt"
]:
    if expected not in assignments:
        fail("missing source assignment "+expected)

route=mp.get("bounded_route",{})
if route!={"Iwa":2,"Iopthyvs":1,"Hlpimp":11}:
    fail("bounded route drift")
state=mp.get("state_classification",{})
if state.get("Runinu")!="EXCLUDED_SEPARATE_STATEQ08_EXECUTION_CONTINUATION":
    fail("Runinu ownership merge")
if mp.get("first_interval_initialization",{}).get("qualified_here") is not False:
    fail("initial condition overclaim")
if mp.get("restart_dependency",{}).get("canonical_checkpoint_schema_admitted") is not False:
    fail("checkpoint admission overclaim")

mod=(R/"prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90").read_text()
for required in [
    "Mofro(Ln) = Mofrt(Ln), Ln=1..Nl",
    "Snla = Snt",
    "Sic  = Sict",
    "Pn   = Pnt",
    "call make_detailed_hydrology_origin_state(",
    "MISSING_DETAILED_HYDROLOGY_MOFRO_PROFILE",
    "NONFINITE_DETAILED_HYDROLOGY_ORIGIN_STATE"
]:
    if required not in mod:
        fail("implementation/source mapping drift "+required)

if "runinu" in mod.lower():
    fail("Runinu leaked into STATEQ09 bundle")

test=(R/"tests/stateq09/test_detailed_hydrology_origin_state.f90").read_text()
for name in [
    "test_exact_endpoint_to_origin_transfer",
    "test_profile_length_preserved",
    "test_nonfinite_rejected",
    "test_unallocated_profile_rejected"
]:
    if name not in test:
        fail("missing test "+name)

allowed_prefixes=(
    "prototype/stateq09/","tests/stateq09/","tools/stateq09/",
    "docs/state/ANIMO_STATEQ09_","integration/animo-state/ANIMO-STATEQ09",
    "integration/animo-state/STATEQ09_"
)
allowed_exact={".github/workflows/animo-stateq09-hydrology-origin-continuation.yml"}
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
    print("PASS_STATEQ09_AUTHORING")
elif st.get("state")=="QUALIFIED_DETAILED_HYDROLOGY_ACCEPTED_ENDPOINT_TO_NEXT_ORIGIN_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-state/ANIMO-STATEQ09_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_transfer_semantics_qualified") is not True or st.get("typed_origin_state_qualified") is not True:
        fail("qualification flags")
    if st.get("canonical_state_admitted") is not False or st.get("checkpoint_schema_admitted") is not False:
        fail("state/checkpoint overclaim")
    if st.get("initial_condition_qualified") is not False:
        fail("initial condition overclaim")
    print("PASS_STATEQ09_QUALIFIED_CONTINUATION")
else:
    fail("unexpected state")
