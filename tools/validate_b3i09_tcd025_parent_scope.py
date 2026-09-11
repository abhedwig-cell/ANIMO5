#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="0bec1968adbf77fd04c6f46819d704b86482d8b2"; RG="e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"; I8="f4a3056087e5f7bac41b243be1f404739cde52b0"; A10="872c78b6c020086280e31e1d9a7408e8b5a1afc7"; M3="68a8c202bd01bf55b31b7c944884fb2f78a6a8e8"; D28="ce602528d075fc962b0b78759ed0082d1ec78a51"; D29="97fd3274acd47bac74939d9dbd55b908043d1521"; D30="5da4e4f38ca94630ff857deb66e86f974425f30c"; PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"; DEC="QUALIFY_TCD025_A5_PERMANENT_REV53_SCOPE_EXCLUSION_AND_RESTRICTED_PARENT_COMPOSITION_ROUTING_NO_ADMISSION"
def fail(x): print("B3I09 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
r=load("integration/animo-b3/B3I09_TCD025_PARENT_SCOPE_ROUTING.json"); s=load("integration/animo-b3/ANIMO-B3I09_STATUS.json")
i8=gj(I8,"integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json"); a10=gj(A10,"integration/animo-b3/ANIMO-B3A10_STATUS.json"); m3=gj(M3,"integration/animo-mass/ANIMO-MASSQ03_STATUS.json")
if i8.get("parent",{}).get("automatic_admission_from_A1_A4_forbidden") is not True or i8.get("parent",{}).get("A5_disposition_required_before_parent_completion") is not True: fail("B3I08 parent guard")
a5=[x for x in i8.get("children",[]) if x.get("id")=="TCD-025-A5"]
if len(a5)!=1 or a5[0].get("state")!="BLOCKED_NOT_SOURCE_CLOSED" or a5[0].get("admission_candidate") is not False: fail("B3I08 A5 prior state")
if a10.get("parent_tcd025_admission_ready") is not False or a10.get("partial_reservoir_cut_supported") is not False: fail("B3A10 parent boundary")
q=m3.get("qualified_finding",{})
if q.get("boundary_admissibility_expression")!=PRED or q.get("partial_saturated_reservoir_selected_profile_source_closed") is not False or q.get("residual_derived_boundary_completion_allowed") is not False or q.get("boundary_predicate_is_necessary_not_sufficient") is not True: fail("MASSQ03 semantic mismatch")
for sha,obj in [(D28,"TCD-025-A1"),(D29,"TCD-025-A2"),(D30,"TCD-025-A3"),(BASE,"TCD-025-A4")]:
 st=gj(sha,f"integration/animo-b3/ANIMO-B3D{ {'TCD-025-A1':'28','TCD-025-A2':'29','TCD-025-A3':'30','TCD-025-A4':'31'}[obj] }_STATUS.json")
 if st.get("target_child_atom")!=obj or st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail(obj+" exact-final admission")
if r.get("supported_parent_scope",{}).get("boundary_predicate")!=PRED or r.get("supported_parent_scope",{}).get("partial_saturated_reservoir_cut_supported") is not False or r.get("supported_parent_scope",{}).get("scope_widening_allowed") is not False: fail("supported scope")
d=r.get("A5_disposition",{})
if d.get("state")!="PERMANENTLY_EXCLUDED_FROM_SUPPORTED_PARENT_SCOPE_FOR_FROZEN_REVISION53" or d.get("scientifically_source_closed") is not False or d.get("b3_admitted") is not False or d.get("residual_derived_completion_allowed") is not False: fail("A5 disposition")
p=r.get("parent",{})
if p.get("admitted") is not False or p.get("automatic_admission_from_A1_A4_forbidden") is not True or p.get("A5_disposition_complete_for_restricted_parent_scope") is not True or p.get("ready_for_separate_restricted_parent_composition_decision") is not True: fail("parent routing")
reg=r.get("canonical_register",{})
if reg.get("canonical_register_modified") is not False or reg.get("new_top_level_tcd_reserved") is not False or reg.get("tail_remains")!="TCD-042": fail("canonical register")
if s.get("decision_candidate")!=DEC or s.get("scientific_admission") is not False or s.get("parent_tcd_admitted") is not False or s.get("A5_b3_admitted") is not False: fail("status boundaries")
allowed={".github/workflows/animo-b3i09-tcd025-parent-scope.yml","docs/b3i09/TCD025_A5_SCOPE_DISPOSITION.md","integration/animo-b3/B3I09_TCD025_PARENT_SCOPE_ROUTING.json","integration/animo-b3/ANIMO-B3I09_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3I09_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3I09_STATUS.json","tools/validate_b3i09_tcd025_parent_scope.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for x in ch:
 if x.startswith("src/") or x.startswith("reference/"): fail("forbidden source/reference change")
rp=R/"integration/animo-b3/ANIMO-B3I09_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 rv=json.loads(rp.read_text()); h=rv.get("reviewed_head")
 if rv.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or rv.get("genuinely_independent") is not False or rv.get("outcome")!="SELF_REVIEW_PASS_A5_EXCLUSION_RESTRICTED_PARENT_ROUTING": fail("review")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3I09_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3I09_STATUS.json"}): fail("post-review substance")
 if s.get("state")!="QUALIFIED_A5_EXCLUDED_RESTRICTED_PARENT_READY_FOR_SEPARATE_COMPOSITION_NO_ADMISSION" or s.get("qualified") is not True or s.get("parent_tcd_admitted") is not False: fail("final status")
 print("B3I09 PASS final A5 excluded for frozen revision53 supported parent scope; parent composition routed separately")
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" or s.get("qualified") is not False: fail("pre-review status")
 print("B3I09 PASS frozen routing candidate pending GOV05 adversarial review")
