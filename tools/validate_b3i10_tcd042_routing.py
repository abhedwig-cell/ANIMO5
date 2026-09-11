#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="4d7c42bb749ed5fbf1c884fba4a26a1a5b898505"; I5="7fa0162415e02a6f0167e71b48ae38177a9e06e0"; I6="8f01f0cb366dfa8cc63a184d6f885100899a8cd9"; U4="bbdb61be30f08951ba78926a745719cfcb1b64a8"; B2="690868409aae11297c966eb55419f62ff977c619"; G3="cbd262bdabe92923113b7326f2f42822ce9a971c"; G4="1bbe4c211197590f346803106e45dca5faae79fc"; G5="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
DEC="QUALIFY_TCD042_REV53_CHILD_SCOPES_HETOP_POSITIVE_ZERO_ENDPOINT_EXCLUDED_B1_READY_FOR_SEPARATE_ADMISSION_NO_ADMISSION"
def fail(x): print("B3I10 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p):
 q=R/p
 if not q.exists(): fail("missing "+p)
 return json.loads(q.read_text())
def gj(s,p):
 try:return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
 except Exception:fail(f"cannot read {s}:{p}")
r=load("integration/animo-b3/B3I10_TCD042_CHILD_SCOPE_ROUTING.json"); s=load("integration/animo-b3/ANIMO-B3I10_STATUS.json")
i5=gj(I5,"integration/animo-b3/ANIMO-B3I05_STATUS.json"); i6=gj(I6,"integration/animo-b3/ANIMO-B3I06_STATUS.json"); u4=gj(U4,"integration/animo-science/ANIMO-UBQ04_STATUS.json"); b2=gj(B2,"integration/animo-b3/ANIMO-B3B02_STATUS.json"); g3=gj(G3,"integration/animo-governance/ANIMO-GOV03_STATUS.json"); g4=gj(G4,"integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json"); g5=gj(G5,"integration/animo-governance/ANIMO-GOV05_STATUS.json")
if i5.get("status")!="QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS": fail("B3I05 routing")
if i6.get("decision")!="QUALIFIED_UBQ03_INCREMENTAL_INTAKE_RUNTIME_INPUT_DOMAIN_HAZARD_NO_NEW_TCD_NO_ADMISSION" or i6.get("intake",{}).get("relation_to_tcd042")!="DOMAIN_CONSTRAINT_ONLY_NOT_NEW_CHILD": fail("B3I06 domain intake")
q=u4.get("qualified_findings",{})
if q.get("documented_range_includes_zero") is not True or q.get("zero_endpoint_semantics_explicitly_defined") is not False or q.get("global_zero_thickness_concentration_semantics_unique") is not False or q.get("zero_thickness_policy_selected") is not False: fail("UBQ04 zero semantics")
if b2.get("admission",{}).get("positive_Hetop_subdomain_readiness_qualified") is not True or b2.get("positive_Hetop_exact_zero_limit",{}).get("classification")!="UNIQUE_MATHEMATICAL_LIMIT_FOR_POSITIVE_HETOP": fail("B3B02 positive HETOP readiness")
if g3.get("qualified_G6U_state")!="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS": fail("GOV03 G6U")
if g4.get("governance_semantics",{}).get("strictest_applicable_risk_trigger_wins") is not True or "EXACT_ZERO_OR_SINGULAR_DOMAIN_SEMANTICS" not in g4.get("risk_tiers",{}).get("C",{}).get("forced_tier_triggers",[]): fail("GOV04 Tier C trigger")
if g5.get("assurance_change",{}).get("to")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or g5.get("assurance_change",{}).get("scientific_gate_reduction") is not False: fail("GOV05 review model")
if r.get("base_authority")!="ANIMO-B3D32@"+BASE or r.get("prior_routing_authority")!="ANIMO-B3I05@"+I5: fail("authority pin")
b1=r.get("children",{}).get("TCD-042-B1",{}); e1=r.get("children",{}).get("TCD-042-E1",{}); z=r.get("Hetop_zero_disposition",{})
if b1.get("supported_revision53_scope")!="Flpn=0 AND Flux=0 AND Hetop>0" or b1.get("Hetop_zero_supported") is not False or b1.get("ready_for_separate_bounded_admission_decision") is not True: fail("B1 routed scope")
if "Hetop>0" not in e1.get("supported_revision53_scope","") or e1.get("Hetop_zero_supported") is not False or e1.get("separate_child_preserved") is not True: fail("E1 routed scope")
if z.get("state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53" or z.get("global_input_invalidity_claimed") is not False or z.get("scientific_semantics_resolved") is not False or z.get("new_child_created") is not False or z.get("hidden_epsilon_or_guard_authorized") is not False or z.get("input_validation_change_authorized") is not False: fail("zero endpoint disposition")
if r.get("parent",{}).get("admitted") is not False or r.get("canonical_register",{}).get("modified") is not False or r.get("canonical_register",{}).get("tail_remains")!="TCD-042": fail("parent/register boundary")
if s.get("decision_candidate")!=DEC or s.get("scientific_admission") is not False or s.get("parent_tcd_admitted") is not False: fail("status boundary")
allowed={".github/workflows/animo-b3i10-tcd042-positive-hetop-routing.yml","docs/b3i10/TCD042_POSITIVE_HETOP_CHILD_SCOPE_ROUTING.md","integration/animo-b3/B3I10_TCD042_CHILD_SCOPE_ROUTING.json","integration/animo-b3/ANIMO-B3I10_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3I10_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3I10_STATUS.json","tools/validate_b3i10_tcd042_routing.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for x in ch:
 if x.startswith("src/") or x.startswith("reference/"): fail("forbidden source/reference change")
rp=R/"integration/animo-b3/ANIMO-B3I10_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 rv=json.loads(rp.read_text()); h=rv.get("reviewed_head")
 if rv.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or rv.get("genuinely_independent") is not False or rv.get("outcome")!="SELF_REVIEW_PASS_TCD042_POSITIVE_HETOP_CHILD_SCOPE_ROUTING": fail("review")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3I10_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3I10_STATUS.json"}): fail("post-review substance")
 if s.get("state")!="QUALIFIED_TCD042_POSITIVE_HETOP_CHILD_ROUTING_ZERO_ENDPOINT_EXCLUDED_NO_ADMISSION" or s.get("qualified") is not True or s.get("parent_tcd_admitted") is not False: fail("final status")
 print("B3I10 PASS final positive-HETOP child routing; HETOP zero excluded without invented semantics")
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" or s.get("qualified") is not False: fail("pre-review status")
 print("B3I10 PASS frozen routing candidate pending GOV05 adversarial review")
