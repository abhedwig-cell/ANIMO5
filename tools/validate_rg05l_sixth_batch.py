#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"
B3I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
ADMS={
 "ANIMO-B3D31":("0bec1968adbf77fd04c6f46819d704b86482d8b2","TCD-025-A4",34583130973),
 "ANIMO-B3D32":("4d7c42bb749ed5fbf1c884fba4a26a1a5b898505","TCD-025",34586116849),
 "ANIMO-B3D33":("8b2a4071d623bc2e3003dca8977e032d5c0d8c3c","TCD-042-B1",34588335817),
}
def fail(x): print("RG05L FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
inv=load("integration/animo-reg/RG05L_B3_ADMISSION_INVENTORY.json")
d=load("integration/animo-reg/RG05L_B3_QUEUE_DELTA.json")
s=load("integration/animo-reg/ANIMO-RG05L_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05K_STATUS.json")
oldi=gj(BASE,"integration/animo-reg/RG05K_B3_ADMISSION_INVENTORY.json")
if old.get("scientific_admission_count")!=20 or old.get("historical_uncertainty_admission_count")!=20 or old.get("top_level_admitted_tcd_count")!=13 or old.get("admitted_child_atom_count")!=7: fail("RG05K source counts")
if old.get("b3_complete") is not False or old.get("b4_open") is not False or old.get("production_open") is not False: fail("RG05K downstream state")
if oldi.get("governance",{}).get("normal_batch_min")!=3 or oldi.get("governance",{}).get("normal_batch_max")!=5: fail("batch policy")
route=gj(B3I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
if route.get("qualified") is not True or route.get("scientific_admission") is not False: fail("B3I10 qualification")
re=route.get("routing_effect",{})
if re.get("TCD042_B1_supported_scope")!="Flpn=0 AND Flux=0 AND Hetop>0" or re.get("TCD042_B1_ready_for_separate_bounded_admission") is not True or re.get("Hetop_zero_state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53": fail("B3I10 scope")
# B3D31 child admission
st31=gj(ADMS["ANIMO-B3D31"][0],"integration/animo-b3/ANIMO-B3D31_STATUS.json")
if st31.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st31.get("admitted") is not True or st31.get("qualified") is not True or st31.get("target_child_atom")!="TCD-025-A4": fail("B3D31 state")
if st31.get("admission_effect",{}).get("parent_tcd_admitted") is not False or st31.get("admission_effect",{}).get("A5_blocker_disposed") is not False: fail("B3D31 boundaries")
# B3D32 bounded parent composition
st32=gj(ADMS["ANIMO-B3D32"][0],"integration/animo-b3/ANIMO-B3D32_STATUS.json")
if st32.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st32.get("admitted") is not True or st32.get("qualified") is not True or st32.get("target_parent_tcd")!="TCD-025" or st32.get("parent_tcd_admitted") is not True: fail("B3D32 parent state")
e32=st32.get("admission_effect",{})
if e32.get("A5_b3_admitted") is not False or e32.get("A5_revision53_scope_exclusion_preserved") is not True or e32.get("production_authorized") is not False: fail("B3D32 boundaries")
# B3D33 bounded child admission
st33=gj(ADMS["ANIMO-B3D33"][0],"integration/animo-b3/ANIMO-B3D33_STATUS.json")
if st33.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st33.get("admitted") is not True or st33.get("qualified") is not True or st33.get("target_child_atom")!="TCD-042-B1": fail("B3D33 state")
e33=st33.get("admission_effect",{})
if e33.get("child_atom_admitted") is not True or e33.get("parent_tcd_admitted") is not False or e33.get("TCD042_E1_admitted") is not False or e33.get("Hetop_zero_admitted") is not False or e33.get("production_authorized") is not False: fail("B3D33 boundaries")
for st,wu in [(st31,"B3D31"),(st32,"B3D32"),(st33,"B3D33")]:
 if st.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail(wu+" historical behavior")
 rv=st.get("review",{})
 if rv.get("completed") is not True or rv.get("genuinely_independent") is not False or rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail(wu+" review assurance")
if inv.get("source_aggregate",{}).get("head")!=BASE or inv.get("batch_policy",{}).get("new_b3_admissions_in_this_batch")!=3 or inv.get("batch_policy",{}).get("normal_threshold_reached") is not True: fail("inventory batch")
if inv.get("batch_policy",{}).get("new_atomic_child_admissions")!=2 or inv.get("batch_policy",{}).get("new_composed_parent_admissions")!=1: fail("inventory object kinds")
post=inv.get("post_state",{})
if post.get("scientific_admissions")!=23 or post.get("historical_uncertainty_admissions")!=23 or post.get("normal_b2_route_admissions")!=0 or post.get("top_level_admitted_tcd_count")!=14 or post.get("admitted_child_atom_count")!=9: fail("inventory post counts")
t25=post.get("tcd025",{})
if t25.get("parent_admitted") is not True or t25.get("admitted_children") != ["TCD-025-A1","TCD-025-A2","TCD-025-A3","TCD-025-A4"] or t25.get("excluded_children") != ["TCD-025-A5"] or t25.get("A5_state")!="PERMANENTLY_EXCLUDED_FROM_SUPPORTED_PARENT_SCOPE_FOR_FROZEN_REVISION53": fail("TCD025 post state")
t42=post.get("tcd042",{})
if t42.get("parent_admitted") is not False or t42.get("admitted_children") != ["TCD-042-B1"] or t42.get("E1_admitted") is not False or t42.get("Hetop_zero_admitted") is not False: fail("TCD042 post state")
if d.get("delta",{}).get("scientific_admissions")!=3 or d.get("delta",{}).get("top_level_admitted_tcds")!=1 or d.get("delta",{}).get("child_atoms")!=2 or d.get("post",{}).get("scientific_admissions")!=23: fail("queue delta")
g=d.get("guards",{})
if any(g.get(k) is not False for k in ["automatic_parent_admission","A5_b3_admission","TCD042_parent_auto_admission","TCD042_E1_inferred_admission","Hetop_zero_inferred_admission","historical_B2_created","production_authorized","B4_opened","global_canonical_queue_count_recomputed"]): fail("queue guards")
if s.get("scientific_admission_count")!=23 or s.get("historical_uncertainty_admission_count")!=23 or s.get("top_level_admitted_tcd_count")!=14 or s.get("admitted_child_atom_count")!=9: fail("status counts")
if s.get("current_routing_authority")!="ANIMO-B3I10@"+B3I10: fail("routing authority")
if s.get("tcd025_state",{}).get("parent_admitted") is not True or s.get("tcd025_state",{}).get("A5_b3_admitted") is not False: fail("status TCD025")
if s.get("tcd042_state",{}).get("parent_admitted") is not False or s.get("tcd042_state",{}).get("E1_admitted") is not False or s.get("tcd042_state",{}).get("Hetop_zero_admitted") is not False: fail("status TCD042")
if s.get("b3_complete") is not False or s.get("b4_open") is not False or s.get("production_open") is not False or s.get("global_canonical_queue_count_recomputed") is not False: fail("downstream opened")
allowed={".github/workflows/animo-rg05l-sixth-batch.yml","docs/governance/ANIMO_RG05L_SIXTH_BATCHED_ADMISSION_REGIE.md","integration/animo-reg/RG05L_B3_ADMISSION_INVENTORY.json","integration/animo-reg/RG05L_B3_QUEUE_DELTA.json","integration/animo-reg/ANIMO-RG05L_STATUS.json","tools/validate_rg05l_sixth_batch.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-b3/"): fail("forbidden source/routing/admission mutation "+p)
if s.get("work_status",{}).get("qualified") is True:
 if s.get("state")!="QUALIFIED_SIXTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD025_A4_PARENT_AND_TCD042_B1_NO_PRODUCTION": fail("final state")
 print("RG05L PASS: exact-final B3D31/B3D32/B3D33 integrated; total 23; TCD025 parent bounded admitted; TCD042 parent/E1/Hetop0 excluded; B3/B4/production closed")
else:
 if s.get("state")!="PERSISTED_VALIDATION_PENDING": fail("precloseout state")
 print("RG05L PASS persisted sixth batch; closeout pending exact validation")
