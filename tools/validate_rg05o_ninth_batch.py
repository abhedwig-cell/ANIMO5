#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="8758bd30e302b75dd7854ac00fd2e29473669a13"
B3D40="83fedc7323cea6da696a81bc64e4e3b13d794880"
B3D41="3ac98899dd4e6b7a5133cbecd758fab0b81e945d"
B3D42="86474df11ecf104797df9df3b8d53fcf2e847873"
B3I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
B3Q05="997d867a2b107ec8e28efce530c82a204719de46"
I33="TCD033_CH4_COMPONENT_PARENT_DAUGHTER_PARTITION_QI_EQ_Q_SI_OVER_S"
I32="TCD032_SINGLE_OWNER_METHANOGENESIS_C_TRANSFER_WITH_GROSS_DEBIT_INTERNAL_CREDIT_AND_NET_QJ_DT_CLOSURE"
I19="TCD019_FAST_LANGMUIR_EXACT_STORAGE_REPRESENTATION_STABLE_TWO_VARIABLE_ROOT_NO_LEGACY_FALLBACK_BINARY64_POLICY"
def fail(x): print("RG05O FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
inv=load("integration/animo-reg/RG05O_B3_ADMISSION_INVENTORY.json")
d=load("integration/animo-reg/RG05O_B3_QUEUE_DELTA.json")
s=load("integration/animo-reg/ANIMO-RG05O_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05N_STATUS.json")
if old.get("scientific_admission_count")!=29 or old.get("historical_uncertainty_admission_count")!=29 or old.get("normal_b2_admission_count")!=0 or old.get("top_level_admitted_tcd_count")!=19 or old.get("admitted_child_atom_count")!=10: fail("RG05N source counts")
if old.get("b3_complete") is not False or old.get("b4_open") is not False or old.get("production_open") is not False: fail("RG05N downstream state")
st40=gj(B3D40,"integration/animo-b3/ANIMO-B3D40_STATUS.json")
st41=gj(B3D41,"integration/animo-b3/ANIMO-B3D41_STATUS.json")
st42=gj(B3D42,"integration/animo-b3/ANIMO-B3D42_STATUS.json")
for st,wu,target,ident in [(st40,"B3D40","TCD-033",I33),(st41,"B3D41","TCD-032",I32),(st42,"B3D42","TCD-019",I19)]:
    t=st.get("target_tcd",st.get("target"))
    if t!=target or st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail(wu+" admission state")
    identv=st.get("admitted_atomic_identity",st.get("admitted_identity"))
    if identv!=ident: fail(wu+" identity")
    if st.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail(wu+" history")
    if st.get("admission_effect",{}).get("production_authorized",st.get("production_authorized")) is not False: fail(wu+" production boundary")
    rv=st.get("review",{})
    if rv.get("completed") is not True or rv.get("same_agent") is not True or rv.get("genuinely_independent") is not False: fail(wu+" review semantics")
if st42.get("hard_boundaries",{}).get("legacy_fallback_admitted") is not False: fail("B3D42 fallback boundary")
if st42.get("aggregate_policy",{}).get("post_RG05N_new_admissions_if_exact_final_green")!=3 or st42.get("aggregate_policy",{}).get("required_next_aggregate")!="ANIMO-RG05O": fail("B3D42 cadence trigger")
queue=gj(B3Q05,"integration/animo-b3/ANIMO-B3Q05_STATUS.json")
if queue.get("unadmitted_top_level")!=["TCD-016","TCD-019","TCD-032","TCD-033","TCD-034","TCD-040"]: fail("B3Q05 source queue")
if inv.get("source_aggregate",{}).get("head")!=BASE: fail("inventory source")
bp=inv.get("batch_policy",{})
if bp.get("new_b3_admissions_in_this_batch")!=3 or bp.get("new_atomic_child_admissions")!=0 or bp.get("new_composed_parent_admissions")!=0 or bp.get("new_top_level_standalone_admissions")!=3 or bp.get("normal_threshold_reached") is not True: fail("inventory batch")
new=inv.get("new_admissions",[])
if [x.get("object") for x in new] != ["TCD-033","TCD-032","TCD-019"]: fail("inventory objects")
if [x.get("admission_authority") for x in new] != ["ANIMO-B3D40@"+B3D40,"ANIMO-B3D41@"+B3D41,"ANIMO-B3D42@"+B3D42]: fail("inventory authorities")
post=inv.get("post_state",{})
if post.get("scientific_admissions")!=32 or post.get("historical_uncertainty_admissions")!=32 or post.get("normal_b2_route_admissions")!=0 or post.get("top_level_admitted_tcd_count")!=22 or post.get("admitted_child_atom_count")!=10: fail("inventory post counts")
if not all(post.get(k) is True for k in ("tcd033_top_level_admitted","tcd032_top_level_admitted","tcd019_top_level_admitted")): fail("inventory top-level post states")
if d.get("delta",{}).get("objects")!=["TCD-033","TCD-032","TCD-019"] or d.get("delta",{}).get("scientific_admissions")!=3 or d.get("delta",{}).get("top_level_admitted_tcds")!=3: fail("queue delta")
if d.get("post",{}).get("known_remaining_from_b3q05_after_exact_admission_delta")!=["TCD-016","TCD-034","TCD-040"] or d.get("post",{}).get("global_queue_recomputed") is not False: fail("queue post")
for k,v in d.get("guards",{}).items():
    if v is not False: fail("queue guard "+k)
if s.get("scientific_admission_count")!=32 or s.get("historical_uncertainty_admission_count")!=32 or s.get("normal_b2_admission_count")!=0 or s.get("top_level_admitted_tcd_count")!=22 or s.get("admitted_child_atom_count")!=10: fail("status counts")
if s.get("current_routing_authority")!="ANIMO-B3I10@"+B3I10 or s.get("current_queue_authority")!="ANIMO-B3Q05@"+B3Q05: fail("routing/queue authority")
if s.get("known_remaining_unadmitted_from_b3q05_delta")!=["TCD-016","TCD-034","TCD-040"]: fail("known remaining queue delta")
if s.get("b3_complete") is not False or s.get("b4_open") is not False or s.get("production_open") is not False or s.get("global_canonical_queue_count_recomputed") is not False: fail("downstream opened")
allowed={".github/workflows/animo-rg05o-ninth-batch.yml","docs/governance/ANIMO_RG05O_NINTH_BATCHED_ADMISSION_REGIE.md","integration/animo-reg/RG05O_B3_ADMISSION_INVENTORY.json","integration/animo-reg/RG05O_B3_QUEUE_DELTA.json","integration/animo-reg/ANIMO-RG05O_STATUS.json","tools/validate_rg05o_ninth_batch.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-b3/") or p=="docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv": fail("forbidden mutation "+p)
ws=s.get("work_status",{})
if ws.get("qualified") is True:
    if s.get("state")!="QUALIFIED_NINTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD033_TCD032_TCD019_NO_PRODUCTION": fail("final state")
    v=s.get("validation",{})
    if v.get("machine_validated") is not True or v.get("candidate_conclusion")!="success" or not v.get("candidate_run_id") or not v.get("tested_candidate_head") or v.get("validator")!="PASS" or v.get("scope_guard")!="PASS": fail("final validation record")
    print("RG05O PASS: B3D40/B3D41/B3D42 integrated; total 32; TCD033/TCD032/TCD019 admitted; B3/B4/production remain closed")
else:
    if s.get("state")!="PERSISTED_VALIDATION_PENDING" or ws.get("persisted") is not True or ws.get("tested") is not False: fail("precloseout state")
    print("RG05O PASS persisted ninth batch; closeout pending exact validation")
