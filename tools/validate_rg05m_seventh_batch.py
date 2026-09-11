#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="214062fe773618ea77c7c74867cc8d9a2a4eef6d"
B3D34="22e4ec3bb88e2e13905ccbbb2f380a9bf235db55"
B3D35="9ca23f41dc3c28af686b1bc0bff8e7d66416d367"
B3D36="b74ec4461ab4d7b62ecfaf175e1eeeec8c58f7b2"
B3I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
S42="Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))"
S29="finite binary64; D>0; T>0; x=Hv*T/D>-1; NQ04 exact zero/series/log1p/large-x evaluation only"
def fail(x): print("RG05M FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
inv=load("integration/animo-reg/RG05M_B3_ADMISSION_INVENTORY.json")
d=load("integration/animo-reg/RG05M_B3_QUEUE_DELTA.json")
s=load("integration/animo-reg/ANIMO-RG05M_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05L_STATUS.json")
oldi=gj(BASE,"integration/animo-reg/RG05L_B3_ADMISSION_INVENTORY.json")
if old.get("scientific_admission_count")!=23 or old.get("historical_uncertainty_admission_count")!=23 or old.get("top_level_admitted_tcd_count")!=14 or old.get("admitted_child_atom_count")!=9: fail("RG05L source counts")
if old.get("b3_complete") is not False or old.get("b4_open") is not False or old.get("production_open") is not False: fail("RG05L downstream state")
if oldi.get("governance",{}).get("normal_batch_min")!=3 or oldi.get("governance",{}).get("normal_batch_max")!=5: fail("batch policy")
# Exact scientific admission authorities
st34=gj(B3D34,"integration/animo-b3/ANIMO-B3D34_STATUS.json")
if st34.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st34.get("admitted") is not True or st34.get("qualified") is not True or st34.get("target_child_atom")!="TCD-042-E1": fail("B3D34 state")
e34=st34.get("admission_effect",{})
if e34.get("child_atom_admitted") is not True or e34.get("parent_tcd_admitted") is not False or e34.get("Hetop_zero_admitted") is not False or e34.get("production_authorized") is not False: fail("B3D34 boundaries")
st35=gj(B3D35,"integration/animo-b3/ANIMO-B3D35_STATUS.json")
if st35.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st35.get("admitted") is not True or st35.get("qualified") is not True or st35.get("target_parent_tcd")!="TCD-042" or st35.get("parent_tcd_admitted") is not True: fail("B3D35 state")
if st35.get("supported_scope")!=S42: fail("B3D35 scope")
e35=st35.get("admission_effect",{})
if e35.get("parent_tcd_admitted") is not True or e35.get("children_readmitted") is not False or e35.get("Hetop_zero_admitted") is not False or e35.get("outside_NQ03_envelope_admitted") is not False or e35.get("production_authorized") is not False: fail("B3D35 boundaries")
st36=gj(B3D36,"integration/animo-b3/ANIMO-B3D36_STATUS.json")
if st36.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st36.get("admitted") is not True or st36.get("qualified") is not True or st36.get("target_tcd")!="TCD-029": fail("B3D36 state")
if st36.get("supported_scope")!=S29: fail("B3D36 scope")
e36=st36.get("admission_effect",{})
if e36.get("tcd029_top_level_admitted") is not True or e36.get("tcd019_admitted_or_modified") is not False or e36.get("Coefdt_admitted") is not False or e36.get("other_iflsol_branches_admitted") is not False or e36.get("production_authorized") is not False: fail("B3D36 boundaries")
if st36.get("aggregate_policy",{}).get("required_next_aggregate")!="ANIMO-RG05M" or st36.get("aggregate_policy",{}).get("normal_batch_threshold_reached_if_green") is not True: fail("B3D36 cadence trigger")
for st,wu in [(st34,"B3D34"),(st35,"B3D35"),(st36,"B3D36")]:
    if st.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail(wu+" historical behavior")
    rv=st.get("review",{})
    if rv.get("completed") is not True or rv.get("genuinely_independent") is not False: fail(wu+" review assurance")
# Routing remains unchanged.
route=gj(B3I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
if route.get("qualified") is not True or route.get("scientific_admission") is not False: fail("B3I10 state")
# Aggregate records
if inv.get("source_aggregate",{}).get("head")!=BASE: fail("inventory source")
bp=inv.get("batch_policy",{})
if bp.get("new_b3_admissions_in_this_batch")!=3 or bp.get("new_atomic_child_admissions")!=1 or bp.get("new_composed_parent_admissions")!=1 or bp.get("new_top_level_standalone_admissions")!=1 or bp.get("normal_threshold_reached") is not True: fail("inventory batch")
post=inv.get("post_state",{})
if post.get("scientific_admissions")!=26 or post.get("historical_uncertainty_admissions")!=26 or post.get("normal_b2_route_admissions")!=0 or post.get("top_level_admitted_tcd_count")!=16 or post.get("admitted_child_atom_count")!=10: fail("inventory post counts")
t42=post.get("tcd042",{})
if t42.get("parent_admitted") is not True or t42.get("admitted_children")!=["TCD-042-B1","TCD-042-E1"] or t42.get("supported_scope")!=S42 or t42.get("Hetop_zero_admitted") is not False or t42.get("outside_NQ03_envelope_admitted") is not False: fail("TCD042 post state")
t29=post.get("tcd029",{})
if t29.get("top_level_admitted") is not True or t29.get("supported_scope")!=S29 or t29.get("tcd019_modified_or_admitted") is not False or t29.get("Coefdt_admitted") is not False or t29.get("other_iflsol_branches_admitted") is not False: fail("TCD029 post state")
if d.get("delta",{}).get("scientific_admissions")!=3 or d.get("delta",{}).get("top_level_admitted_tcds")!=2 or d.get("delta",{}).get("child_atoms")!=1: fail("queue delta")
if d.get("post",{}).get("scientific_admissions")!=26 or d.get("post",{}).get("top_level_admitted_tcd_count")!=16 or d.get("post",{}).get("admitted_child_atom_count")!=10: fail("queue post")
g=d.get("guards",{})
for k in ["automatic_parent_admission","child_readmission","Hetop_zero_inferred_admission","outside_NQ03_envelope_inferred_admission","tcd019_inferred_admission","Coefdt_inferred_admission","other_iflsol_inferred_admission","historical_B2_created","production_authorized","B4_opened","global_canonical_queue_count_recomputed"]:
    if g.get(k) is not False: fail("queue guard "+k)
if s.get("scientific_admission_count")!=26 or s.get("historical_uncertainty_admission_count")!=26 or s.get("normal_b2_admission_count")!=0 or s.get("top_level_admitted_tcd_count")!=16 or s.get("admitted_child_atom_count")!=10: fail("status counts")
if s.get("current_routing_authority")!="ANIMO-B3I10@"+B3I10: fail("routing authority")
if s.get("tcd042_state",{}).get("parent_admitted") is not True or s.get("tcd042_state",{}).get("Hetop_zero_admitted") is not False or s.get("tcd042_state",{}).get("outside_NQ03_envelope_admitted") is not False: fail("status TCD042")
if s.get("tcd029_state",{}).get("top_level_admitted") is not True or s.get("tcd029_state",{}).get("tcd019_modified_or_admitted") is not False: fail("status TCD029")
if s.get("b3_complete") is not False or s.get("b4_open") is not False or s.get("production_open") is not False or s.get("global_canonical_queue_count_recomputed") is not False: fail("downstream opened")
allowed={".github/workflows/animo-rg05m-seventh-batch.yml","docs/governance/ANIMO_RG05M_SEVENTH_BATCHED_ADMISSION_REGIE.md","integration/animo-reg/RG05M_B3_ADMISSION_INVENTORY.json","integration/animo-reg/RG05M_B3_QUEUE_DELTA.json","integration/animo-reg/ANIMO-RG05M_STATUS.json","tools/validate_rg05m_seventh_batch.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-b3/") or p=="docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv": fail("forbidden mutation "+p)
ws=s.get("work_status",{})
if ws.get("qualified") is True:
    if s.get("state")!="QUALIFIED_SEVENTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD042_E1_PARENT_AND_TCD029_NO_PRODUCTION": fail("final state")
    v=s.get("validation",{})
    if v.get("machine_validated") is not True or v.get("candidate_conclusion")!="success" or not v.get("candidate_run_id") or not v.get("tested_candidate_head"): fail("final validation record")
    print("RG05M PASS: B3D34/B3D35/B3D36 integrated; total 26; TCD042 bounded parent and TCD029 admitted; B3/B4/production remain closed")
else:
    if s.get("state")!="PERSISTED_VALIDATION_PENDING" or ws.get("persisted") is not True or ws.get("tested") is not False: fail("precloseout state")
    print("RG05M PASS persisted seventh batch; closeout pending exact validation")
