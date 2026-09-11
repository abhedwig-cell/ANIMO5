#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="44f29974a1f49cffd36f67857a1ed2c919978a07"; RG="e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"; I8="f4a3056087e5f7bac41b243be1f404739cde52b0"; A10="872c78b6c020086280e31e1d9a7408e8b5a1afc7"; M3="68a8c202bd01bf55b31b7c944884fb2f78a6a8e8"; D28="ce602528d075fc962b0b78759ed0082d1ec78a51"; D29="97fd3274acd47bac74939d9dbd55b908043d1521"; D30="5da4e4f38ca94630ff857deb66e86f974425f30c"; D31="0bec1968adbf77fd04c6f46819d704b86482d8b2"; PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"; DEC="ADMIT_TCD025_RESTRICTED_PARENT_COMPOSITION_A1_A4_WITH_A5_REV53_EXCLUSION_HISTORICAL_UNCERTAINTY_GOV05_TIER_D"
def fail(x): print("B3D32 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
c=load("integration/animo-b3/B3D32_TCD025_PARENT_COMPOSITION_CONTRACT.json"); cv=load("integration/animo-b3/B3D32_TCD025_PARENT_COVERAGE.json"); o=load("integration/animo-b3/B3D32_TCD025_PARENT_ORACLES.json"); s=load("integration/animo-b3/ANIMO-B3D32_STATUS.json")
i9=gj(BASE,"integration/animo-b3/ANIMO-B3I09_STATUS.json"); route=gj(BASE,"integration/animo-b3/B3I09_TCD025_PARENT_SCOPE_ROUTING.json")
if i9.get("state")!="QUALIFIED_A5_EXCLUDED_RESTRICTED_PARENT_READY_FOR_SEPARATE_COMPOSITION_NO_ADMISSION" or i9.get("qualified") is not True or i9.get("parent_tcd_admitted") is not False: fail("B3I09 authority")
if route.get("supported_parent_scope",{}).get("boundary_predicate")!=PRED or route.get("A5_disposition",{}).get("state")!="PERMANENTLY_EXCLUDED_FROM_SUPPORTED_PARENT_SCOPE_FOR_FROZEN_REVISION53": fail("B3I09 routing semantics")
for sha,num,obj in [(D28,"28","TCD-025-A1"),(D29,"29","TCD-025-A2"),(D30,"30","TCD-025-A3"),(D31,"31","TCD-025-A4")]:
 st=gj(sha,f"integration/animo-b3/ANIMO-B3D{num}_STATUS.json")
 if st.get("target_child_atom")!=obj or st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail(obj+" admission")
if c.get("candidate_decision")!=DEC or c.get("supported_scope",{}).get("boundary_predicate")!=PRED or c.get("supported_scope",{}).get("partial_saturated_reservoir_cut_supported") is not False: fail("contract scope")
sem=c.get("composition_semantics",{})
if sem.get("kind")!="CONJUNCTION_VECTOR_NOT_CROSS_FAMILY_SCALAR_SUM" or sem.get("cross_family_summation") is not False or sem.get("new_stoichiometric_conversion") is not False or sem.get("new_atomic_weight_conversion") is not False: fail("composition semantics")
if c.get("A5",{}).get("included_in_parent") is not False or c.get("A5",{}).get("b3_admitted") is not False or c.get("A5",{}).get("scientifically_source_closed") is not False: fail("A5 boundary")
if [x.get("family") for x in cv.get("coverage",[])] != ["water","DOM","N","P"] or cv.get("parent_composition_complete_for_supported_revision53_scope") is not True: fail("coverage")
if cv.get("overlap_gap_audit",{}).get("cross_family_scalar_balance_created") is not False or cv.get("overlap_gap_audit",{}).get("child_scope_widened") is not False: fail("overlap/scope")
cs={x["id"]:x for x in o.get("cases",[])}
if cs["PC01"]["expect_parent_in_scope"] is not True or cs["PC02"]["expect_parent_in_scope"] is not False or cs["PC03"]["expect_parent_pass"] is not False or cs["PC04"]["expect_parent_pass"] is not False or cs["PC05"]["expect_allowed"] is not False or cs["PC06"]["expect_restricted_parent_composable"] is not True or cs["PC07"]["expect_allowed"] is not False: fail("parent oracle controls")
if s.get("risk_tier")!="D_NON_ATOMIC_PARENT_COMPOSITION_WITH_SHARED_CONTROL_VOLUME_SEMANTICS" or s.get("risk_rule")!="STRICTEST_APPLICABLE_RISK_TRIGGER_WINS" or s.get("candidate_decision")!=DEC: fail("risk/decision")
if s.get("aggregate_policy",{}).get("batch_size_if_parent_exact_final_green")!=2 or s.get("aggregate_policy",{}).get("aggregate_update_required_here") is not False: fail("aggregate cadence")
allowed={".github/workflows/animo-b3d32-tcd025-parent-composition.yml","docs/b3d32/TCD025_RESTRICTED_PARENT_COMPOSITION.md","integration/animo-b3/B3D32_TCD025_PARENT_COMPOSITION_CONTRACT.json","integration/animo-b3/B3D32_TCD025_PARENT_COVERAGE.json","integration/animo-b3/B3D32_TCD025_PARENT_ORACLES.json","integration/animo-b3/ANIMO-B3D32_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3D32_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D32_STATUS.json","tools/validate_b3d32_tcd025_parent.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-reg/"): fail("forbidden mutation "+p)
rp=R/"integration/animo-b3/ANIMO-B3D32_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 rv=json.loads(rp.read_text()); h=rv.get("reviewed_head")
 if rv.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or rv.get("genuinely_independent") is not False or rv.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD025_RESTRICTED_PARENT_WITH_HISTORICAL_UNCERTAINTY": fail("review")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D32_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D32_STATUS.json"}): fail("post-review substance")
 if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True or s.get("parent_tcd_admitted") is not True: fail("final")
 print("B3D32 PASS final restricted TCD025 parent composition admission")
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_D_ADVERSARIAL_REVIEW" or s.get("admitted") is not False: fail("pre-review")
 print("B3D32 PASS frozen restricted parent candidate pending GOV05 Tier-D adversarial review")
