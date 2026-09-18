#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="b019ac4507648e57c196a8a62806d804f39014a2"
RG09=BASE
KT19="6245aad4aca962cb2a63d0394bb7f2baa686457d"
STATEQ08="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
HYDROEXEC01="182dac2fc34ca42ed798203e90efeca1221f21e8"
B3D35="9ca23f41dc3c28af686b1bc0bff8e7d66416d367"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT21 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-kt21/ANIMO-KT21_STATUS.json")
ev=load("integration/animo-kt21/KT21_LWKM_EXTERNAL_CHARACTERIZATION.json")

rg=show_json(RG09,"integration/animo-reg/ANIMO-RG09_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT20_REAL_SOURCE_PROVIDER_BRIDGE_REBASELINE_REVIEW_GATE_FROZEN_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG09 state")
if rg.get("b3_complete") is not False or rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG09 gates")

kt19=show_json(KT19,"integration/animo-kt19/ANIMO-KT19_STATUS.json")
if kt19.get("state")!="QUALIFIED_PINNED_LWKM_FILE_TO_IMMUTABLE_HYDROLOGY_PROVIDER_TIER_C_REVIEW_REQUIRED":
    fail("KT19 state")
if kt19.get("pinned_source_sha256")!="b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c":
    fail("KT19 source identity")

s8=show_json(STATEQ08,"integration/animo-state/ANIMO-STATEQ08_STATUS.json")
if s8.get("state")!="QUALIFIED_RUNINU_DETAILED_HYDROLOGY_EXECUTION_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    fail("STATEQ08 state")
if s8.get("first_call_runinu_value")!="UNQUALIFIED_SOURCE_UNDEFINED":
    fail("STATEQ08 first-call Runinu boundary")
if s8.get("model_evolution_zeroing_admitted") is not False:
    fail("Runinu zeroing unexpectedly admitted")

hx=show_json(HYDROEXEC01,"integration/animo-hydroexec01/ANIMO-HYDROEXEC01_STATUS.json")
if hx.get("bounded_execution_qualified") is not True:
    fail("HYDROEXEC01 bounded execution")
if hx.get("runinu_canonical_state_ownership_qualified") is not False:
    fail("HYDROEXEC01 Runinu ownership")

p=show_json(B3D35,"integration/animo-b3/ANIMO-B3D35_STATUS.json")
scope="Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))"
if p.get("supported_scope")!=scope or p.get("admitted") is not True:
    fail("TCD042 parent scope")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "C" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier C missing")

if ev.get("evidence_class")!="B1_DIAGNOSTIC_CHARACTERIZATION_DERIVED_FROM_PINNED_B0_NOT_B2":
    fail("evidence class")
if ev.get("hydrology_source",{}).get("sha256")!="b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c":
    fail("hydrology source pin")
if ev.get("soil_configuration_source",{}).get("sha256")!="57f2173723172bb5f92621786f7a49b23b8f497ee3554f25a36ea19ae0968f3c":
    fail("soil source pin")
cfg=ev.get("soil_configuration_source",{}).get("values",{})
if cfg!={"layer_count":30,"Hetop_m":0.02,"He0_m":0.2,"Lefrrv":0.2,"Lefrso":0.25,"Rodp_m":0.25}:
    fail("soil configuration mapping")
res=ev.get("result",{})
expected={
    "packet_count":1800,
    "blocked_first_call_runinu":347,
    "deterministic_packet_count":1453,
    "ponding_count":2,
    "exact_zero_count":36,
    "e1_hydrology_envelope_count":14,
    "tcd042_hydrology_outside_admitted_scope_count":1401,
    "runoff_partition_singularity_count":0,
    "hydrology_envelope_intersection_count":50,
}
if res!=expected:
    fail("external characterization counts")
if res["blocked_first_call_runinu"]+res["deterministic_packet_count"]!=res["packet_count"]:
    fail("characterization partition")
if res["ponding_count"]+res["exact_zero_count"]+res["e1_hydrology_envelope_count"]+res["tcd042_hydrology_outside_admitted_scope_count"]!=res["deterministic_packet_count"]:
    fail("deterministic classification partition")

anchors=ev.get("first_anchors",{})
if anchors.get("first_runinu_reset",{}).get("index_zero_based")!=347:
    fail("first Runinu reset index")
if anchors.get("first_runinu_reset",{}).get("typed_step_sha256")!="d2f7a4e37d1d9f3b31f7e8a3b758448d424e5bc601617d01ae3a057c7d189099":
    fail("first reset typed identity")
if anchors.get("first_exact_zero",{}).get("index_zero_based")!=404:
    fail("first exact-zero index")
if anchors.get("first_e1",{}).get("index_zero_based")!=665:
    fail("first E1 index")
if anchors.get("first_ponding",{}).get("index_zero_based")!=1001:
    fail("first ponding index")

interp=ev.get("interpretation",{})
if interp.get("no_scientific_admission") is not True:
    fail("scientific admission boundary")
if "does not imply" not in interp.get("not_sequential_application",""):
    fail("sequential application nonclaim")

tool=(R/"prototype/kt21/lwkm_bounded_envelope.py").read_text()
for required in [
    'CLASS_BLOCKED_RUNINU = "BLOCKED_FIRST_CALL_RUNINU"',
    'REV53_RUNOFF_NEAR_ZERO = 1.0e-8',
    'TCD042_FLUX_THRESHOLD = 1.0e-8',
    'TCD042_P_MAX = 3.8510200002999744e-7',
    'runinu_known = False',
    'elif -REV53_RUNOFF_NEAR_ZERO < ru < REV53_RUNOFF_NEAR_ZERO:',
    'runinu = 0.0',
    'flux = max(0.0, flab_top)',
    'p = st * flux / config.he_top',
]:
    if required not in tool:
        fail("characterizer drift "+required)
if "first_call_runinu=0" in tool.lower() or "runinu = 0.0  # default" in tool.lower():
    fail("hidden first-call Runinu assumption")

allowed_prefixes=("prototype/kt21/","tests/kt21/","docs/kt21/","integration/animo-kt21/")
allowed_exact={
    ".github/workflows/animo-kt21-lwkm-envelope-characterization.yml",
    "tools/validate_kt21_lwkm_envelope.py",
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
    print("PASS_KT21_AUTHORING")
elif st.get("state")=="QUALIFIED_PINNED_LWKM_BOUNDED_TCD042_HYDROLOGY_ENVELOPE_CHARACTERIZATION_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-kt21/ANIMO-KT21_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("pinned_source_characterization_qualified") is not True:
        fail("characterization flag")
    if st.get("first_call_runinu_uncertainty_preserved") is not True:
        fail("Runinu uncertainty flag")
    if st.get("post_reset_deterministic_envelope_qualified") is not True:
        fail("deterministic envelope flag")
    if st.get("sequential_real_application_qualified") is not False or st.get("b2_claimed") is not False:
        fail("sequential/B2 overclaim")
    print("PASS_KT21_QUALIFIED_CHARACTERIZATION")
else:
    fail("unexpected state")
