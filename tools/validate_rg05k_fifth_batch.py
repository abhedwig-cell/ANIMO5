#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="624bbad35add93de29ac89649155d9fa086a73af"
B3I08="f4a3056087e5f7bac41b243be1f404739cde52b0"
ADMS={"ANIMO-B3D28":("ce602528d075fc962b0b78759ed0082d1ec78a51","TCD-025-A1",34572641664),"ANIMO-B3D29":("97fd3274acd47bac74939d9dbd55b908043d1521","TCD-025-A2",34572919222),"ANIMO-B3D30":("5da4e4f38ca94630ff857deb66e86f974425f30c","TCD-025-A3",34573179762)}
def fail(x): print("RG05K FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
inv=load("integration/animo-reg/RG05K_B3_ADMISSION_INVENTORY.json"); d=load("integration/animo-reg/RG05K_B3_QUEUE_DELTA.json"); s=load("integration/animo-reg/ANIMO-RG05K_STATUS.json")
old=gj(BASE,"integration/animo-reg/ANIMO-RG05J_STATUS.json"); oldi=gj(BASE,"integration/animo-reg/RG05J_B3_ADMISSION_INVENTORY.json")
if old.get("scientific_admission_count")!=17 or old.get("historical_uncertainty_admission_count")!=17 or old.get("top_level_admitted_tcd_count")!=13 or old.get("admitted_child_atom_count")!=4: fail("RG05J source state mismatch")
if old.get("b3_complete") is not False or old.get("b4_open") is not False or old.get("production_open") is not False: fail("RG05J downstream state mismatch")
if oldi.get("governance",{}).get("normal_batch_min")!=3 or oldi.get("governance",{}).get("normal_batch_max")!=5: fail("batch policy mismatch")
route=gj(B3I08,"integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json"); rs=gj(B3I08,"integration/animo-b3/ANIMO-B3I08_STATUS.json")
if rs.get("work_status",{}).get("qualified") is not True or rs.get("parent_admitted") is not False: fail("B3I08 authority mismatch")
if route.get("parent",{}).get("automatic_admission_from_A1_A4_forbidden") is not True: fail("parent auto-admission guard lost")
a5=[x for x in route.get("children",[]) if x.get("id")=="TCD-025-A5"]
if len(a5)!=1 or a5[0].get("state")!="BLOCKED_NOT_SOURCE_CLOSED": fail("A5 blocker mismatch")
for wu,(sha,obj,run) in ADMS.items():
 st=gj(sha,f"integration/animo-b3/ANIMO-{wu.split('ANIMO-')[1]}_STATUS.json")
 if st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail(wu+" admission state")
 target=st.get("target_child_atom")
 if target!=obj: fail(wu+" object mismatch")
 if st.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail(wu+" historical state")
 rv=st.get("review",{})
 if rv.get("completed") is not True or rv.get("genuinely_independent") is not False or rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail(wu+" review assurance")
 eff=st.get("admission_effect",{})
 if eff.get("parent_tcd_admitted") is not False or eff.get("A5_blocker_disposed") is not False: fail(wu+" parent/A5 boundary")
if inv.get("source_aggregate",{}).get("head")!=BASE or inv.get("batch_policy",{}).get("new_b3_admissions_in_this_batch")!=3 or inv.get("batch_policy",{}).get("normal_threshold_reached") is not True: fail("inventory batch mismatch")
post=inv.get("post_state",{})
if post.get("scientific_admissions")!=20 or post.get("historical_uncertainty_admissions")!=20 or post.get("normal_b2_route_admissions")!=0 or post.get("top_level_admitted_tcd_count")!=13 or post.get("admitted_child_atom_count")!=7: fail("inventory post counts")
t25=post.get("tcd025",{})
if t25.get("parent_admitted") is not False or t25.get("admitted_children") != ["TCD-025-A1","TCD-025-A2","TCD-025-A3"] or t25.get("unadmitted_bounded_children") != ["TCD-025-A4"] or t25.get("blocked_children") != ["TCD-025-A5"]: fail("TCD025 post state")
if d.get("delta",{}).get("scientific_admissions")!=3 or d.get("post",{}).get("scientific_admissions")!=20 or d.get("guards",{}).get("parent_auto_admission") is not False: fail("queue delta mismatch")
if s.get("scientific_admission_count")!=20 or s.get("historical_uncertainty_admission_count")!=20 or s.get("top_level_admitted_tcd_count")!=13 or s.get("admitted_child_atom_count")!=7: fail("status counts")
if s.get("current_routing_authority") != "ANIMO-B3I08@"+B3I08: fail("routing not advanced to B3I08")
if s.get("tcd025_state",{}).get("parent_admitted") is not False or s.get("tcd025_state",{}).get("A4_admitted") is not False or s.get("tcd025_state",{}).get("A5_state")!="BLOCKED_NOT_SOURCE_CLOSED": fail("status TCD025 boundary")
if s.get("b3_complete") is not False or s.get("b4_open") is not False or s.get("production_open") is not False: fail("downstream opened")
allowed={".github/workflows/animo-rg05k-fifth-batch.yml","docs/governance/ANIMO_RG05K_FIFTH_BATCHED_ADMISSION_REGIE.md","integration/animo-reg/RG05K_B3_ADMISSION_INVENTORY.json","integration/animo-reg/RG05K_B3_QUEUE_DELTA.json","integration/animo-reg/ANIMO-RG05K_STATUS.json","tools/validate_rg05k_fifth_batch.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-b3/"): fail("forbidden source/routing/admission mutation "+p)
if s.get("work_status",{}).get("qualified") is True:
 if s.get("state")!="QUALIFIED_FIFTH_BATCHED_B3_ADMISSION_INTEGRATION_THREE_TCD025_CHILD_ATOMS_NO_PARENT_NO_PRODUCTION": fail("final state mismatch")
 print("RG05K PASS: three exact-final TCD025 child admissions integrated; total 20; parent false; A4 open; A5 blocked; B3/B4/production closed")
else:
 if s.get("state")!="PERSISTED_VALIDATION_PENDING": fail("precloseout state mismatch")
 print("RG05K PASS persisted fifth batch; closeout pending exact validation")
