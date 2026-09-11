#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="7146612d5dfa8ad87a4660f0c50c68a5db1e3a29"
B3D37="8bd1d0a5e20e5fa1d15508e0fdf7c69a5150a84f"
B3D38="c6fe71cfd1822aea5d00a802862e4b3a4a991cd2"
B3D39="025bb9e5da84a6a1b55d29681de005fca784f543"
B3I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
B3Q04="dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
I39="TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_OWNER_RESTORE_N_AND_CONDITIONAL_P"
I35="TCD035_GHG_SOIL_LAYER_PHASE_VIEW_RECONSTRUCT_FROM_ACCEPTED_CS_HYDROLOGY_AND_CHECKPOINT_TEMPERATURE"
I36="TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_GHG_RESTART_IDENTITY_FROM_SERIALIZED_TOTAL_SYSTEM_OWNER"
def fail(x): print("RG05N FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
inv=load("integration/animo-reg/RG05N_B3_ADMISSION_INVENTORY.json")
d=load("integration/animo-reg/RG05N_B3_QUEUE_DELTA.json")
s=load("integration/animo-reg/ANIMO-RG05N_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05M_STATUS.json")
oldi=gj(BASE,"integration/animo-reg/RG05M_B3_ADMISSION_INVENTORY.json")
if old.get("scientific_admission_count")!=26 or old.get("historical_uncertainty_admission_count")!=26 or old.get("normal_b2_admission_count")!=0 or old.get("top_level_admitted_tcd_count")!=16 or old.get("admitted_child_atom_count")!=10: fail("RG05M source counts")
if old.get("b3_complete") is not False or old.get("b4_open") is not False or old.get("production_open") is not False: fail("RG05M downstream state")
if oldi.get("governance",{}).get("normal_batch_min")!=3 or oldi.get("governance",{}).get("normal_batch_max")!=5: fail("batch policy")
# Exact admission authorities.
st37=gj(B3D37,"integration/animo-b3/ANIMO-B3D37_STATUS.json")
st38=gj(B3D38,"integration/animo-b3/ANIMO-B3D38_STATUS.json")
st39=gj(B3D39,"integration/animo-b3/ANIMO-B3D39_STATUS.json")
for st,wu,target,ident in [(st37,"B3D37","TCD-039",I39),(st38,"B3D38","TCD-035",I35),(st39,"B3D39","TCD-036",I36)]:
    if st.get("target")!=target or st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail(wu+" admission state")
    if st.get("admitted_identity")!=ident: fail(wu+" identity")
    if st.get("historical_behavior")!="UNKNOWN_WITHOUT_B2" or st.get("production_authorized") is not False: fail(wu+" uncertainty/boundary")
    rv=st.get("review",{})
    if rv.get("completed") is not True or rv.get("same_agent") is not True or rv.get("genuinely_independent") is not False or rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail(wu+" review assurance")
if st37.get("canonical_state_admitted") is not False or st37.get("crop007_resolved") is not False: fail("B3D37 boundaries")
if st38.get("tcd036_modified_or_admitted") is not False or st38.get("canonical_state_admitted") is not False: fail("B3D38 boundaries")
if st39.get("tcd035_reopened") is not False or st39.get("tcd032_034_modified_or_admitted") is not False or st39.get("canonical_state_admitted") is not False or st39.get("whole_model_split_run_claimed") is not False: fail("B3D39 boundaries")
if st39.get("aggregate_policy",{}).get("post_RG05M_if_exact_final_green")!=3 or st39.get("aggregate_policy",{}).get("aggregate_update_required_if_green") is not True or st39.get("aggregate_policy",{}).get("next_aggregate_when_threshold_reached")!="ANIMO-RG05N": fail("B3D39 cadence trigger")
# Routing/queue pins stay unchanged in this aggregate.
route=gj(B3I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
if route.get("qualified") is not True or route.get("scientific_admission") is not False: fail("B3I10 state")
queue=gj(B3Q04,"integration/animo-reg/RG05_B3_QUEUE.json")
if len(queue.get("entries",[]))!=25: fail("B3Q04 queue authority")
# Aggregate records.
if inv.get("source_aggregate",{}).get("head")!=BASE: fail("inventory source")
bp=inv.get("batch_policy",{})
if bp.get("new_b3_admissions_in_this_batch")!=3 or bp.get("new_atomic_child_admissions")!=0 or bp.get("new_composed_parent_admissions")!=0 or bp.get("new_top_level_standalone_admissions")!=3 or bp.get("normal_threshold_reached") is not True: fail("inventory batch")
new=inv.get("new_admissions",[])
if [x.get("object") for x in new] != ["TCD-039","TCD-035","TCD-036"]: fail("inventory objects")
if [x.get("admission_authority") for x in new] != ["ANIMO-B3D37@"+B3D37,"ANIMO-B3D38@"+B3D38,"ANIMO-B3D39@"+B3D39]: fail("inventory authorities")
post=inv.get("post_state",{})
if post.get("scientific_admissions")!=29 or post.get("historical_uncertainty_admissions")!=29 or post.get("normal_b2_route_admissions")!=0 or post.get("top_level_admitted_tcd_count")!=19 or post.get("admitted_child_atom_count")!=10: fail("inventory post counts")
if post.get("tcd039",{}).get("top_level_admitted") is not True or post.get("tcd035",{}).get("top_level_admitted") is not True or post.get("tcd036",{}).get("top_level_admitted") is not True: fail("top-level post states")
t36=post.get("tcd036",{})
if t36.get("ponding_scope")!="ACTIVE_PRE_EXISTING_PONDING_ONLY" or t36.get("species")!=["CH4","N2O"] or t36.get("new_ponding_source_initialization_preserved") is not True or t36.get("dormant_layer0_state_created") is not False: fail("TCD036 post scope")
if d.get("delta",{}).get("scientific_admissions")!=3 or d.get("delta",{}).get("historical_uncertainty_admissions")!=3 or d.get("delta",{}).get("top_level_admitted_tcds")!=3 or d.get("delta",{}).get("child_atoms")!=0: fail("queue delta")
if d.get("post",{}).get("scientific_admissions")!=29 or d.get("post",{}).get("top_level_admitted_tcd_count")!=19 or d.get("post",{}).get("admitted_child_atom_count")!=10: fail("queue post")
for k,v in d.get("guards",{}).items():
    if v is not False: fail("queue guard "+k)
if s.get("scientific_admission_count")!=29 or s.get("historical_uncertainty_admission_count")!=29 or s.get("normal_b2_admission_count")!=0 or s.get("top_level_admitted_tcd_count")!=19 or s.get("admitted_child_atom_count")!=10: fail("status counts")
if s.get("current_routing_authority")!="ANIMO-B3I10@"+B3I10 or s.get("current_queue_authority")!="ANIMO-B3Q04@"+B3Q04: fail("routing/queue authority")
if s.get("tcd039_state",{}).get("top_level_admitted") is not True or s.get("tcd035_state",{}).get("top_level_admitted") is not True or s.get("tcd036_state",{}).get("top_level_admitted") is not True: fail("status TCD states")
if s.get("tcd036_state",{}).get("new_ponding_source_initialization_preserved") is not True or s.get("tcd036_state",{}).get("dormant_layer0_state_created") is not False: fail("status TCD036 lifecycle")
if s.get("b3_complete") is not False or s.get("b4_open") is not False or s.get("production_open") is not False or s.get("global_canonical_queue_count_recomputed") is not False: fail("downstream opened")
allowed={".github/workflows/animo-rg05n-eighth-batch.yml","docs/governance/ANIMO_RG05N_EIGHTH_BATCHED_ADMISSION_REGIE.md","integration/animo-reg/RG05N_B3_ADMISSION_INVENTORY.json","integration/animo-reg/RG05N_B3_QUEUE_DELTA.json","integration/animo-reg/ANIMO-RG05N_STATUS.json","tools/validate_rg05n_eighth_batch.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-b3/") or p=="docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv": fail("forbidden mutation "+p)
ws=s.get("work_status",{})
if ws.get("qualified") is True:
    if s.get("state")!="QUALIFIED_EIGHTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD039_TCD035_TCD036_NO_PRODUCTION": fail("final state")
    v=s.get("validation",{})
    if v.get("machine_validated") is not True or v.get("candidate_conclusion")!="success" or not v.get("candidate_run_id") or not v.get("tested_candidate_head"): fail("final validation record")
    print("RG05N PASS: B3D37/B3D38/B3D39 integrated; total 29; TCD039/TCD035/TCD036 admitted; B3/B4/production remain closed")
else:
    if s.get("state")!="PERSISTED_VALIDATION_PENDING" or ws.get("persisted") is not True or ws.get("tested") is not False: fail("precloseout state")
    print("RG05N PASS persisted eighth batch; closeout pending exact validation")
