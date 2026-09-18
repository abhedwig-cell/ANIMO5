#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[2]
BASE="26f6e61da328a5578b9c4b332de04eb99a3ac04f"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
HYDROQ02="08d5b8301c217cf9d33d2bf248be133f2b5243fc"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("STATEQ08 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-state/ANIMO-STATEQ08_STATUS.json")
mp=load("integration/animo-state/STATEQ08_RUNINU_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

h2=show_json(HYDROQ02,"integration/animo-hydroq02/ANIMO-HYDROQ02_STATUS.json")
if h2.get("state")!="QUALIFIED_TCD042_RESOLVED_RUPR_RUNINU_LOAD_CONTEXT_TIER_D_REVIEW_REQUIRED":
    fail("HYDROQ02 state")
if h2.get("near_zero_runinu_semantics_repaired") is not False:
    fail("HYDROQ02 source semantics already repaired")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
tiers=gov.get("policy",{}).get("risk_tiers",[])
if "C" not in tiers:
    fail("GOV04 Tier C missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
pins={
 "Animo.inc":"0f8b58e522ac2cdae95e8ae727dbf3ecea942e39c4d117b6bcae955d80fb69a2",
 "Animo.for":"352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
 "Hydro_detailed.for":"f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d",
 "Hydro_aggregated.for":"55a5f54a571b6461c7d45c9f4ac80ffb708f4ff79807d37c9c3878d3f88f0b36",
 "UBoundconc.for":"b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7",
 "TRANSPORT.FOR":"3f597b896ab5514e0b836f5547b342e317b03c8e3e58e053e113bd1c17e2f998",
 "Outbal_calc.for":"4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981"
}
for name,sha in pins.items():
    if mp.get("source_members",{}).get(name,{}).get("sha256")!=sha:
        fail("source member pin "+name)

cls=mp.get("classification",{})
if cls.get("continuation_critical_for_exact_detailed_source_execution") is not True:
    fail("continuation critical classification")
if cls.get("conserved_physical_storage") is not False:
    fail("physical-storage overclaim")
if cls.get("report_only_diagnostic") is not False:
    fail("diagnostic-only misclassification")
if cls.get("candidate_class")!="EXECUTION_CONTINUATION_STATE":
    fail("candidate class")
if cls.get("canonical_state_admitted") is not False:
    fail("canonical state admitted")
if mp.get("first_call_initialization",{}).get("source_defined") is not False:
    fail("first-call initialization overclaim")
if mp.get("first_call_initialization",{}).get("b2_claim") is not False:
    fail("B2 overclaim")
if mp.get("model_evolution_boundary",{}).get("deterministic_zeroing_in_near_zero_branch")!="NOT_AUTHORIZED_BY_STATEQ08":
    fail("model-evolution zeroing authorized")

probe=(R/"tests/stateq08/fixtures/runinu_continuation_probe.f90").read_text()
for required in [
 "runinu = -ru",
 "Exact source property under test: no Runinu assignment here.",
 "runinu = 0.0_real64",
 "omitted Runinu continuation did not diverge",
 "Runinu changes UBoundconc run-in load contribution",
 "aggregated nonnegative branch resets Runinu unlike detailed near-zero branch"
]:
    if required not in probe:
        fail("probe drift "+required)
if "1.0e-8_real64" not in probe:
    fail("near-zero threshold missing")

allowed_prefixes=("tests/stateq08/","docs/state/ANIMO_STATEQ08_","integration/animo-state/ANIMO-STATEQ08","integration/animo-state/STATEQ08_","tools/stateq08/")
allowed_exact={".github/workflows/animo-stateq08-runinu-continuation.yml"}
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
    print("PASS_STATEQ08_AUTHORING")
elif st.get("state")=="QUALIFIED_RUNINU_DETAILED_HYDROLOGY_EXECUTION_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-state/ANIMO-STATEQ08_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_semantics_qualified") is not True or st.get("continuation_classification_qualified") is not True:
        fail("qualification flags")
    if st.get("canonical_state_admitted") is not False or st.get("model_evolution_zeroing_admitted") is not False:
        fail("state/model-evolution overclaim")
    print("PASS_STATEQ08_QUALIFIED_CONTINUATION")
else:
    fail("unexpected state")
