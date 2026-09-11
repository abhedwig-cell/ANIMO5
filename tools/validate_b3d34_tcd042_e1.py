#!/usr/bin/env python3
import json, pathlib, subprocess

R=pathlib.Path(__file__).resolve().parents[1]
BASE="c08b7bd398a79f776a1e296308e3f381ecd85922"
RG="214062fe773618ea77c7c74867cc8d9a2a4eef6d"
Q03="67a87c6a650d503c1b0968ada2cc5eaa5155aa42"
I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
NQ03="8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6"
NQ03R="0153779e9045c6527b7c31156f2295ff44b57eeb"
Q02="1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3"
GOV03="cbd262bdabe92923113b7326f2f42822ce9a971c"
DEC="ADMIT_TCD042_E1_POSITIVE_HETOP_RESTRICTED_NUMERICAL_POLICY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
SCOPE="Flpn=0 AND 0<Flux<1.0d-8 AND Hetop>0 AND 0<P<=3.8510200002999744e-7 AND binary64"

def fail(x):
    print("B3D34 FAIL_CLOSED:",x)
    raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))

c=load("integration/animo-b3/B3D34_TCD042_E1_ADMISSION_CONTRACT.json")
s=load("integration/animo-b3/ANIMO-B3D34_STATUS.json")
f=load("integration/animo-b3/ANIMO-B3D34_AUTHORING_FREEZE.json")

if c.get("target_parent_tcd")!="TCD-042" or c.get("target_child_atom")!="TCD-042-E1" or c.get("atomic_target")!="CANONICAL_CHILD_ATOM:TCD-042-E1": fail("target identity")
if c.get("b3_qualification_class")!="E_NUMERICAL_POLICY" or c.get("review_risk_tier")!="C_NUMERICAL_POLICY": fail("class/risk")
sc=c.get("supported_scope",{})
if sc.get("predicate")!=SCOPE or sc.get("P_definition")!="P=St*Flux/Hetop": fail("scope predicate")
for k in ["positive_Hetop_only","finite_positive_subthreshold_flux_only","natural_P_envelope_only","binary64_only","Hetop_zero_excluded","Flux_zero_excluded_to_TCD042_B1","Flpn_nonzero_excluded"]:
    if sc.get(k) is not True: fail("scope gate "+k)
if sc.get("scope_widening_allowed") is not False: fail("scope widening")
pol=c.get("selected_policy",{})
expected={"name":"NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY","A1":"exp(-P)","f":"1-P/2+P^2/6","g":"1/2-P/6+P^2/24","A2":"(St/Hetop)*f","B1":"f","B2":"(St/Hetop)*g","outside_envelope":"NOT_QUALIFIED_FAIL_CLOSED"}
if pol!=expected: fail("policy identity")
if c.get("formal_disposition")!="HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY" or c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail("historical disposition")
if c.get("candidate_decision")!=DEC or c.get("candidate_admitted") is not True: fail("candidate decision")
for k in ["parent_tcd_admitted","TCD042_B1_readmitted","Hetop_zero_admitted","production_authorized","b4_opened"]:
    if c.get(k) is not False: fail("hard candidate boundary "+k)
pc=c.get("production_binding_constraint",{})
if pc.get("state")!="CARRIED_NOT_RESOLVED_HERE" or pc.get("blocks_scientific_b3_admission_of_restricted_policy") is not False or pc.get("blocks_bitwise_production_binding") is not True: fail("production binding constraint")

# Reconstruct upstream evidence exactly rather than inheriting a conclusion blindly.
e=gj(BASE,"integration/animo-b3/ANIMO-B3E02_STATUS.json")
if e.get("state")!="QUALIFIED_READY_FOR_SEPARATE_B3_ADMISSION_NO_ADMISSION" or e.get("qualified") is not True or e.get("scientific_admission") is not False: fail("B3E02 readiness")
if e.get("supported_scope")!=SCOPE or e.get("parent_tcd_admitted") is not False or e.get("production_authorized") is not False: fail("B3E02 scope/boundary")

rg=gj(RG,"integration/animo-reg/ANIMO-RG05L_STATUS.json")
if rg.get("work_status",{}).get("qualified") is not True or rg.get("b3_complete") is not False or rg.get("b4_open") is not False or rg.get("production_open") is not False: fail("RG05L state")
t42=rg.get("tcd042_state",{})
if t42.get("parent_admitted") is not False or t42.get("E1_admitted") is not False or t42.get("Hetop_zero_admitted") is not False or "TCD-042-B1" not in t42.get("admitted_children",[]): fail("RG05L TCD042 state")

q=gj(Q03,"integration/animo-b3/ANIMO-B3Q03_STATUS.json")
if q.get("current_aggregate_authority")!="ANIMO-RG05L@"+RG or q.get("global_canonical_b3_queue_closed") is not False or "TCD-042" not in q.get("unadmitted_top_level",[]): fail("B3Q03 negative closure")
if q.get("production_allowed") is not False or q.get("b4_allowed") is not False: fail("B3Q03 project gate")

i=gj(I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
if i.get("qualified") is not True or i.get("scientific_admission") is not False: fail("B3I10 state")
re=i.get("routing_effect",{})
if re.get("TCD042_E1_remains_separate_with_NQ03_NQ03R_scope") is not True: fail("B3I10 E1 routing")
if re.get("TCD042_B1_supported_scope")!="Flpn=0 AND Flux=0 AND Hetop>0" or re.get("Hetop_zero_state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53": fail("B3I10 boundary routing")
if re.get("Hetop_zero_scientific_semantics_resolved") is not False: fail("B3I10 zero semantics")

n=gj(NQ03,"integration/animo-science/ANIMO-NQ03_STATUS.json")
np=n.get("selected_policy",{})
if n.get("target")!="TCD-042-E1" or n.get("class")!="E_NUMERICAL_POLICY": fail("NQ03 target/class")
if np.get("applicability")!="Flpn=0, 0<Flux<1.0d-8, Hetop>0, 0<P<=3.8510200002999744e-7" or np.get("precision")!="binary64": fail("NQ03 applicability")
for k,v in expected.items():
    if k in ("name","outside_envelope"):
        if np.get(k)!=v: fail("NQ03 policy "+k)
    elif np.get(k)!=v: fail("NQ03 coefficient "+k)
qb=n.get("qualification_basis",{})
if qb.get("high_precision_oracle_digits")!=100 or qb.get("dense_envelope_probe_points")!=2008 or qb.get("natural_records")!=1238 or qb.get("natural_cases")!=6: fail("NQ03 evidence counts")
if qb.get("P_max")!=3.8510200002999744e-7 or qb.get("series2_binary64_matches_rounded_100_digit_reference_on_dense_envelope") is not True or qb.get("exact_zero_continuity_matches_TCD042_B1") is not True: fail("NQ03 numerical qualification")

nr=gj(NQ03R,"integration/animo-science/ANIMO-NQ03R_STATUS.json")
if nr.get("review_outcome")!="INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY" or nr.get("target")!="TCD-042-E1": fail("NQ03R outcome")
ir=nr.get("independent_reconstruction",{})
if ir.get("oracle_decimal_digits")!=120 or ir.get("probe_points_unique")!=2008 or ir.get("horner_degree2_matches_rounded_120_digit_oracle_all_probes") is not True or ir.get("conservation_identity_verified") is not True: fail("NQ03R reconstruction")
io=nr.get("implementation_order_finding",{})
if io.get("severity")!="NON_BLOCKING_FOR_RESTRICTED_POLICY_BLOCKING_BEFORE_BITWISE_PRODUCTION_BINDING" or io.get("unique_points_with_any_literal_order_mismatch")!=129: fail("NQ03R implementation order")
if nr.get("scope",{}).get("outside_envelope")!="NOT_QUALIFIED_FAIL_CLOSED": fail("NQ03R envelope")

q2=gj(Q02,"integration/animo-b3/ANIMO-B3Q02_STATUS.json")
qc=q2.get("qualified_contract",{})
if q2.get("decision")!="QUALIFIED_ADDITIVE_CANONICAL_CHILD_ATOM_DISPOSITION_CARRIER_NO_ADMISSION" or qc.get("formal_mode")!="FORMAL_DISPOSITION": fail("B3Q02 carrier")
if qc.get("parent_admission_implied") is not False or qc.get("new_top_level_tcd_implied") is not False or qc.get("production_migration_implied") is not False: fail("B3Q02 carrier boundaries")

g=gj(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
if g.get("qualified_G6U_state")!="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" or g.get("hard_boundaries",{}).get("historical_B2_recovered") is not False: fail("GOV03 G6U")

fi=c.get("frozen_identity",{})
if n.get("frozen_identity",{}).get("source_sha256")!=fi.get("source_sha256") or n.get("frozen_identity",{}).get("testbank_sha256")!=fi.get("testbank_sha256"): fail("B0 identity")
if f.get("base_head")!=BASE or f.get("review_must_pin_exact_commit") is not True or f.get("substantive_change_resets_GOV05_review") is not True: fail("freeze contract")

allowed={
 ".github/workflows/animo-b3d34-tcd042-e1.yml",
 "docs/b3d34/WORK_UNIT_CONTRACT.md",
 "integration/animo-b3/B3D34_TCD042_E1_ADMISSION_CONTRACT.json",
 "integration/animo-b3/ANIMO-B3D34_AUTHORING_FREEZE.json",
 "integration/animo-b3/ANIMO-B3D34_INTERNAL_ADVERSARIAL_REVIEW.json",
 "integration/animo-b3/ANIMO-B3D34_STATUS.json",
 "tools/validate_b3d34_tcd042_e1.py"
}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/"): fail("source/reference modified")

rp=R/"integration/animo-b3/ANIMO-B3D34_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
    r=json.loads(rp.read_text()); h=r.get("reviewed_head")
    if r.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("same_agent") is not True or r.get("genuinely_independent") is not False or r.get("independence_claimed") is not False or r.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail("review assurance")
    if r.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD042_E1_POSITIVE_HETOP_WITH_HISTORICAL_UNCERTAINTY": fail("review outcome")
    if not h: fail("reviewed head missing")
    post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
    if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D34_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D34_STATUS.json"}): fail("post-review substantive change")
    if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True: fail("final admission state")
    ae=s.get("admission_effect",{})
    if ae.get("child_atom_admitted") is not True or ae.get("parent_tcd_admitted") is not False or ae.get("TCD042_B1_readmitted") is not False or ae.get("Hetop_zero_admitted") is not False or ae.get("production_authorized") is not False: fail("final admission boundaries")
    ap=s.get("aggregate_policy",{})
    if ap.get("post_RG05L_new_admissions_if_exact_final_green")!=1 or ap.get("normal_batch_threshold_minimum")!=3 or ap.get("aggregate_update_required_after_exact_final_green") is not False: fail("aggregate cadence")
    print("B3D34 PASS final bounded TCD042-E1 admission",h)
else:
    if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("state")!="CANDIDATE_NOT_ADMITTED_PENDING_REVIEW" or s.get("admitted") is not False or s.get("qualified") is not False: fail("pre-review state")
    print("B3D34 PASS frozen pending GOV05 Tier-C adversarial review")
