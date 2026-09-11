#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="bfd736b88b6fc4f2a66970b812172729c1923562"
RG="214062fe773618ea77c7c74867cc8d9a2a4eef6d"
Q03="67a87c6a650d503c1b0968ada2cc5eaa5155aa42"
B3I01="383c7a83e84a578969f92113280dc715b7bdddb4"
GOV03="cbd262bdabe92923113b7326f2f42822ce9a971c"
DEC="ADMIT_TCD029_IFLSOL4_DETCOEF_COEFDC_CANCELLATION_SAFE_BINARY64_POLICY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
IDENT="IFLSOL4_DETCOEF_COEFDC_CANCELLATION_SAFE_BINARY64_EVALUATION_ON_NQ04_QUALIFIED_DOMAIN"

def fail(x): print("B3D36 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))

c=load("integration/animo-b3/B3D36_TCD029_ADMISSION_CONTRACT.json")
s=load("integration/animo-b3/ANIMO-B3D36_STATUS.json")
f=load("integration/animo-b3/ANIMO-B3D36_AUTHORING_FREEZE.json")
if c.get("target_tcd")!="TCD-029" or c.get("atomic_target")!="CANONICAL_TOP_LEVEL_TCD:TCD-029": fail("target")
if c.get("b3_qualification_class")!="E_NUMERICAL_POLICY" or c.get("review_risk_tier")!="C_NUMERICAL_POLICY": fail("class/risk")
if c.get("admitted_identity")!=IDENT or c.get("candidate_decision")!=DEC or c.get("candidate_admitted") is not True: fail("candidate")
if c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2" or c.get("formal_disposition")!="HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY": fail("historical route")
for k in ("production_authorized","b4_opened","canonical_register_modified","aggregate_modified"):
    if c.get(k) is not False: fail("boundary "+k)
expected={"precision":"binary64","finite_inputs":True,"D_gt_0":True,"T_gt_0":True,"x_definition":"x=Hv*T/D","x_gt_minus_1":True,"zero_policy":"ANALYTIC_LIMITS_F_EQ_1_G_EQ_H_EQ_0_5","series_region":"abs(x)<=0.25","series_degree":24,"moderate_region":"0.25<abs(x)<=1","large_region":"abs(x)>1","outside_domain":"NOT_QUALIFIED_FAIL_CLOSED","scope_widening_allowed":False}
if c.get("supported_scope")!=expected: fail("scope drift")
if c.get("selected_policy",{}).get("model_acceptance_tolerance_created") is not False: fail("invented tolerance")
if c.get("qualified_evidence",{}).get("mass_balance_improvement_is_acceptance_criterion") is not False: fail("conservation masking")

n=gj(BASE,"integration/animo-science/ANIMO-NQ04_STATUS.json")
if n.get("target")!="TCD-029" or n.get("state")!="QUALIFIED_TCD029_IFLSOL4_CANCELLATION_SAFE_BINARY64_NUMERICAL_POLICY_READY_FOR_SEPARATE_B3_ADMISSION": fail("NQ04 state")
if n.get("admission",{}).get("tcd029_b3_admitted") is not False or n.get("admission",{}).get("production_implementation_authorized") is not False: fail("NQ04 boundary")
if n.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail("NQ04 history")
np=n.get("qualified_candidate",{})
for k,v in {"identity":"IFLSOL4_DETCOEF_COEFDC_CANCELLATION_SAFE_BINARY64_EVALUATION","domain":"finite binary64; D>0; T>0; x=Hv*T/D>-1","series_region":"abs(x)<=0.25","series_degree":24,"moderate_region":"0.25<abs(x)<=1","large_region":"abs(x)>1","zero_policy":"analytic limits F=1 G=H=0.5","outside_domain":"FAIL_CLOSED_NOT_QUALIFIED"}.items():
    if np.get(k)!=v: fail("NQ04 policy "+k)
no=n.get("oracle",{})
if no.get("deterministic_points")!=4756 or no.get("verification_bound")!="128u relative per dimensionless function" or no.get("verification_bound_is_model_tolerance") is not False: fail("NQ04 oracle")

q=gj(Q03,"integration/animo-b3/ANIMO-B3Q03_STATUS.json")
if q.get("current_aggregate_authority")!="ANIMO-RG05L@"+RG or "TCD-029" not in q.get("unadmitted_top_level",[]): fail("queue")
if q.get("global_canonical_b3_queue_closed") is not False or q.get("b4_allowed") is not False or q.get("production_allowed") is not False: fail("queue gates")
rg=gj(RG,"integration/animo-reg/ANIMO-RG05L_STATUS.json")
if rg.get("work_status",{}).get("qualified") is not True or rg.get("b3_complete") is not False or rg.get("b4_open") is not False or rg.get("production_open") is not False: fail("RG05L")
i=gj(B3I01,"integration/animo-b3/B3I01_CANONICAL_REGISTER_APPEND_STATUS.json")
if i.get("work_unit")!="ANIMO-B3I01" or i.get("status")!="QUALIFIED_CANONICAL_REGISTER_APPEND_TCD028_THROUGH_TCD037_NO_ADMISSIONS" or "TCD-029" not in i.get("registered_ids",[]): fail("canonical allocation")
g=gj(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
if g.get("qualified_G6U_state")!="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" or g.get("hard_boundaries",{}).get("historical_B2_recovered") is not False: fail("GOV03")
if f.get("base_head")!=BASE or f.get("review_must_pin_exact_commit") is not True or f.get("substantive_change_resets_GOV05_review") is not True or f.get("exact_final_head_ci_required") is not True: fail("freeze")

allowed={".github/workflows/animo-b3d36-tcd029.yml","docs/b3d36/WORK_UNIT_CONTRACT.md","integration/animo-b3/B3D36_TCD029_ADMISSION_CONTRACT.json","integration/animo-b3/ANIMO-B3D36_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3D36_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D36_STATUS.json","tools/validate_b3d36_tcd029.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-reg/") or p=="docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv": fail("forbidden mutation "+p)

rp=R/"integration/animo-b3/ANIMO-B3D36_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
    r=json.loads(rp.read_text()); h=r.get("reviewed_authoring_head")
    if r.get("risk_tier")!="C" or r.get("review_mode")!="INTERNAL_ADVERSARIAL_REVIEW" or r.get("assurance_label")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT" or r.get("same_agent") is not True or r.get("independence_claimed") is not False or r.get("outcome")!="SELF_REVIEW_PASS": fail("review")
    if not h: fail("review head")
    post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
    if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D36_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D36_STATUS.json"}): fail("post-review change")
    if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True or s.get("admitted_atomic_identity")!=IDENT: fail("final admission")
    ae=s.get("admission_effect",{})
    if ae.get("tcd029_top_level_admitted") is not True or ae.get("tcd019_admitted_or_modified") is not False or ae.get("Coefdt_admitted") is not False or ae.get("other_iflsol_branches_admitted") is not False or ae.get("production_authorized") is not False: fail("final boundaries")
    ap=s.get("aggregate_policy",{})
    if ap.get("post_RG05L_new_admissions_if_exact_final_green")!=3 or ap.get("normal_batch_threshold_reached_if_green") is not True or ap.get("aggregate_update_required_after_exact_final_green") is not True or ap.get("required_next_aggregate")!="ANIMO-RG05M": fail("aggregate cadence")
    print("B3D36 PASS final TCD029 admission",h)
else:
    if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("state")!="CANDIDATE_NOT_ADMITTED_PENDING_REVIEW" or s.get("admitted") is not False or s.get("qualified") is not False: fail("pre-review state")
    print("B3D36 PASS frozen pending GOV05 Tier-C adversarial review")
