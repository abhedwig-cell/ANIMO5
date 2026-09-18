#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="5301d90024c64057f2cb88fda1dbaa93aabfca47"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("HYDROQ02 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-hydroq02/ANIMO-HYDROQ02_STATUS.json")
mp=load("integration/animo-hydroq02/HYDROQ02_SOURCE_MAPPING.json")

base=show_json(BASE,"integration/animo-hydroq01/ANIMO-HYDROQ01_STATUS.json")
if base.get("state")!="QUALIFIED_TCD042_POST_HYDRO_DETAILED_RESOLVED_UPPER_HYDROLOGY_CONTRACT_TIER_D_REVIEW_REQUIRED":
    fail("HYDROQ01 base state")
if base.get("typed_contract_qualified") is not True:
    fail("HYDROQ01 carrier not qualified")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

sm=mp.get("source_member",{})
if sm.get("sha256")!="f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d":
    fail("Hydro_detailed pin")
routes=mp.get("runoff_routes",[])
if len(routes)!=3:
    fail("runoff route count")
near=[x for x in routes if x.get("predicate")=="-1.0d-8<Ru<1.0d-8"]
if len(near)!=1 or near[0].get("runinu_assignment")!="ABSENT_IN_LOCAL_BRANCH":
    fail("near-zero Runinu source finding")
sem=mp.get("contract_semantics",{})
if sem.get("raw_ru_reconstruction") is not False:
    fail("raw Ru reconstruction")
if sem.get("historical_near_zero_branch_repaired") is not False:
    fail("near-zero branch repaired")
if sem.get("sign_constraints_added") is not False:
    fail("sign semantics invented")

mod=(R/"prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90").read_text()
for required in [
 "ANIMO_TCD042_RUNOFF_LOAD_CONTEXT_V1",
 "REV53_POST_HYDRO_DETAILED_RUNOFF_PARTITION",
 "real(real64) :: rupr",
 "real(real64) :: runinu",
 "hydrology_execution_id",
 "RUNOFF_CONTEXT_EXECUTION_ID_MISMATCH",
 "SUBDAY_RUNOFF_CONTEXT_NOT_QUALIFIED"
]:
    if required not in mod:
        fail("implementation drift "+required)
for forbidden in ["max(0", "1.0e-8", "lefr", "runoff", "runinu = -", "rupr ="]:
    if forbidden.lower() in mod.lower():
        fail("hydrology reconstruction leaked into context "+forbidden)

allowed_prefixes=("prototype/hydroq02/","tests/hydroq02/","docs/hydroq02/","integration/animo-hydroq02/")
allowed_exact={
 ".github/workflows/animo-hydroq02-runoff-load-context.yml",
 "tools/validate_hydroq02_runoff_load_context.py"
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
    print("PASS_HYDROQ02_AUTHORING")
elif st.get("state")=="QUALIFIED_TCD042_RESOLVED_RUPR_RUNINU_LOAD_CONTEXT_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-hydroq02/ANIMO-HYDROQ02_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_mapping_qualified") is not True or st.get("typed_context_qualified") is not True:
        fail("qualification flags")
    if st.get("runoff_partition_execution_qualified") is not False or st.get("near_zero_runinu_semantics_repaired") is not False:
        fail("scope overclaim")
    print("PASS_HYDROQ02_QUALIFIED_CONTEXT")
else:
    fail("unexpected state")
