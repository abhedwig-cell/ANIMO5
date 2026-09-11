#!/usr/bin/env python3
import json,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="214062fe773618ea77c7c74867cc8d9a2a4eef6d"
Q03="67a87c6a650d503c1b0968ada2cc5eaa5155aa42"
I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
NQ03="8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6"
NQ03R="0153779e9045c6527b7c31156f2295ff44b57eeb"
Q02="1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3"
E01="41e43c6a6888aac5b5b52041bcdd088c7afc68f1"
G3="cbd262bdabe92923113b7326f2f42822ce9a971c"
G4="1bbe4c211197590f346803106e45dca5faae79fc"
G5="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
DEC="QUALIFIED_TCD042_E1_POSITIVE_HETOP_RESTRICTED_NUMERICAL_POLICY_READY_FOR_SEPARATE_GOV05_TIER_C_B3_ADMISSION"
SCOPE="Flpn=0 AND 0<Flux<1.0d-8 AND Hetop>0 AND 0<P<=3.8510200002999744e-7 AND binary64"
def fail(x): print("B3E02 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p):
 try:return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
 except Exception: fail(f"cannot read {s}:{p}")
c=load("integration/animo-b3/B3E02_TCD042_E1_READINESS_CONTRACT.json")
s=load("integration/animo-b3/ANIMO-B3E02_STATUS.json")
rg=gj(BASE,"integration/animo-reg/ANIMO-RG05L_STATUS.json")
q3=gj(Q03,"integration/animo-b3/ANIMO-B3Q03_STATUS.json")
i10=gj(I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
n3=gj(NQ03,"integration/animo-science/ANIMO-NQ03_STATUS.json")
n3r=gj(NQ03R,"integration/animo-science/ANIMO-NQ03R_STATUS.json")
q2=gj(Q02,"integration/animo-b3/ANIMO-B3Q02_STATUS.json")
e1=gj(E01,"integration/animo-b3/ANIMO-B3E01_STATUS.json")
g3=gj(G3,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
g4=gj(G4,"integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
g5=gj(G5,"integration/animo-governance/ANIMO-GOV05_STATUS.json")
if rg.get("state")!="QUALIFIED_SIXTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD025_A4_PARENT_AND_TCD042_B1_NO_PRODUCTION": fail("RG05L state")
if rg.get("tcd042_state",{}).get("parent_admitted") is not False or rg.get("tcd042_state",{}).get("E1_admitted") is not False: fail("RG05L TCD042 boundary")
if q3.get("global_canonical_b3_queue_closed") is not False or "TCD-042" not in q3.get("unadmitted_top_level",[]) or q3.get("b4_allowed") is not False: fail("B3Q03 closure state")
re=i10.get("routing_effect",{})
if re.get("TCD042_E1_remains_separate_with_NQ03_NQ03R_scope") is not True or re.get("Hetop_zero_state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53": fail("B3I10 routing")
if i10.get("parent_tcd_admitted") is not False: fail("B3I10 parent boundary")
if n3.get("status")!="QUALIFIED_RESTRICTED_TCD042_E1_NATURAL_ENVELOPE_NUMERICAL_POLICY_INDEPENDENT_REVIEW_PENDING" or n3.get("work_status",{}).get("qualified") is not True: fail("NQ03 qualification")
pol=n3.get("selected_policy",{})
if pol.get("applicability")!="Flpn=0, 0<Flux<1.0d-8, Hetop>0, 0<P<=3.8510200002999744e-7" or pol.get("precision")!="binary64" or pol.get("outside_envelope")!="NOT_QUALIFIED_FAIL_CLOSED": fail("NQ03 policy scope")
if n3r.get("review_outcome")!="INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY" or n3r.get("work_status",{}).get("qualified") is not True: fail("NQ03R pass")
if n3r.get("scope",{}).get("applicability")!="Flpn=0, 0<Flux<1.0d-8, Hetop>0, 0<P<=3.8510200002999744e-7, binary64": fail("NQ03R scope")
if n3r.get("implementation_order_finding",{}).get("severity")!="NON_BLOCKING_FOR_RESTRICTED_POLICY_BLOCKING_BEFORE_BITWISE_PRODUCTION_BINDING": fail("NQ03R downstream constraint")
if q2.get("status")!="QUALIFIED_ADDITIVE_CANONICAL_CHILD_ATOM_DISPOSITION_CARRIER_NO_ADMISSION" or q2.get("qualified_contract",{}).get("formal_mode")!="FORMAL_DISPOSITION": fail("B3Q02 carrier")
if e1.get("admission",{}).get("full_requested_E1_trigger_admission_ready") is not False: fail("B3E01 historical scope")
if e1.get("blocking_gates",{}).get("full_child_trigger_domain") is None: fail("B3E01 blockers missing")
if g3.get("qualified_G6U_state")!="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS": fail("GOV03 route")
if g4.get("governance_semantics",{}).get("strictest_applicable_risk_trigger_wins") is not True or "NUMERICAL_POLICY" not in g4.get("risk_tiers",{}).get("C",{}).get("forced_tier_triggers",[]): fail("GOV04 Tier C")
if g5.get("assurance_change",{}).get("to")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or g5.get("assurance_change",{}).get("scientific_gate_reduction") is not False: fail("GOV05")
if c.get("supported_scope",{}).get("logical")!=SCOPE or c.get("supported_scope",{}).get("Hetop_zero_supported") is not False: fail("candidate scope")
rec=c.get("b3e01_reconciliation",{})
if rec.get("reuse_old_full_trigger_readiness") is not False or rec.get("old_zero_domain_blocker_resolved_for_bounded_claim") is not True or rec.get("old_historical_route_blocker_resolved_by_GOV03") is not True or rec.get("old_child_carrier_blocker_resolved_by_B3Q02") is not True or rec.get("old_independent_numerical_review_blocker_resolved_by_NQ03R") is not True: fail("fresh reassessment")
if c.get("readiness_candidate",{}).get("decision")!=DEC or c.get("readiness_candidate",{}).get("scientific_admission_performed_here") is not False: fail("candidate decision")
if s.get("decision_candidate")!=DEC or s.get("scientific_admission") is not False or s.get("child_admitted") is not False or s.get("parent_tcd_admitted") is not False or s.get("production_authorized") is not False: fail("status boundaries")
allowed={".github/workflows/animo-b3e02-tcd042-e1-readiness.yml","docs/b3/TCD042_E1_POSITIVE_HETOP_READINESS.md","integration/animo-b3/B3E02_TCD042_E1_READINESS_CONTRACT.json","integration/animo-b3/ANIMO-B3E02_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3E02_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3E02_STATUS.json","tools/validate_b3e02_tcd042_e1.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/"): fail("forbidden source/reference change "+p)
rp=R/"integration/animo-b3/ANIMO-B3E02_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 rv=json.loads(rp.read_text()); h=rv.get("reviewed_head")
 if rv.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or rv.get("genuinely_independent") is not False or rv.get("outcome")!="SELF_REVIEW_PASS_TCD042_E1_POSITIVE_HETOP_READINESS": fail("review")
 if rv.get("counter_hypotheses_tested",0)<4: fail("insufficient counter-hypotheses")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3E02_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3E02_STATUS.json"}): fail("post-review substantive change")
 if s.get("state")!="QUALIFIED_READY_FOR_SEPARATE_B3_ADMISSION_NO_ADMISSION" or s.get("qualified") is not True or s.get("readiness_candidate") is not True or s.get("work_status",{}).get("workunit_complete") is not True: fail("final readiness state")
 print("B3E02 PASS final bounded TCD042-E1 readiness; separate Tier-C admission may proceed; no admission here")
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" or s.get("qualified") is not False: fail("pre-review status")
 print("B3E02 PASS frozen readiness candidate pending GOV05 adversarial review")
