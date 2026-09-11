#!/usr/bin/env python3
import json, pathlib, subprocess

R=pathlib.Path(__file__).resolve().parents[1]
BASE="22e4ec3bb88e2e13905ccbbb2f380a9bf235db55"
RG="214062fe773618ea77c7c74867cc8d9a2a4eef6d"
Q03="67a87c6a650d503c1b0968ada2cc5eaa5155aa42"
I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
I05="7fa0162415e02a6f0167e71b48ae38177a9e06e0"
D33="8b2a4071d623bc2e3003dca8977e032d5c0d8c3c"
D34="22e4ec3bb88e2e13905ccbbb2f380a9bf235db55"
D32="4d7c42bb749ed5fbf1c884fba4a26a1a5b898505"
GOV03="cbd262bdabe92923113b7326f2f42822ce9a971c"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"
GOV05="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
DEC="ADMIT_TCD042_RESTRICTED_PARENT_COMPOSITION_B1_E1_POSITIVE_HETOP_NQ03_ENVELOPE_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_D"
PARENT="Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))"
B1="Flpn=0 AND Flux=0 AND Hetop>0"
E1="Flpn=0 AND 0<Flux<1.0d-8 AND Hetop>0 AND 0<P<=3.8510200002999744e-7 AND binary64"

def fail(x):
    print("B3D35 FAIL_CLOSED:",x)
    raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))

c=load("integration/animo-b3/B3D35_TCD042_PARENT_COMPOSITION_CONTRACT.json")
cv=load("integration/animo-b3/B3D35_TCD042_PARENT_COVERAGE.json")
o=load("integration/animo-b3/B3D35_TCD042_PARENT_ORACLES.json")
s=load("integration/animo-b3/ANIMO-B3D35_STATUS.json")
f=load("integration/animo-b3/ANIMO-B3D35_AUTHORING_FREEZE.json")

if c.get("target_parent_tcd")!="TCD-042" or c.get("kind")!="BOUNDED_POSITIVE_HETOP_PARENT_COMPOSITION": fail("parent identity")
if c.get("base_authority")!="ANIMO-B3D34@"+BASE or c.get("aggregate_at_start")!="ANIMO-RG05L@"+RG: fail("base/aggregate")
if c.get("children")!={"TCD-042-B1":"ANIMO-B3D33@"+D33,"TCD-042-E1":"ANIMO-B3D34@"+D34}: fail("children pins")
if c.get("risk_tier")!="D_NON_ATOMIC_PARENT_COMPOSITION_WITH_NUMERICAL_AND_DOMAIN_SEMANTICS" or c.get("risk_rule")!="STRICTEST_APPLICABLE_RISK_TRIGGER_WINS": fail("Tier-D risk")
sc=c.get("supported_scope",{})
if sc.get("parent_predicate")!=PARENT or sc.get("B1_predicate")!=B1 or sc.get("E1_predicate")!=E1 or sc.get("P_definition")!="P=St*Flux/Hetop": fail("scope identity")
for k in ["child_predicates_disjoint","union_equals_supported_parent_scope"]:
    if sc.get(k) is not True: fail("scope composition "+k)
if sc.get("scope_widening_allowed") is not False or sc.get("full_parser_domain_claimed") is not False: fail("scope widening/parser claim")
cs=c.get("composition_semantics",{})
if cs.get("kind")!="DISJOINT_TRIGGER_PARTITION_NOT_NUMERICAL_SUM" or cs.get("double_correction_at_Flux_zero") is not False: fail("composition semantics")
for k in ["B1_readmitted","E1_readmitted","new_numerical_policy","new_physical_state","new_stoichiometric_conversion","new_tolerance_or_threshold"]:
    if cs.get(k) is not False: fail("composition boundary "+k)
ex=c.get("excluded_or_outside_scope",{})
z=ex.get("Hetop_zero",{})
if z.get("state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_PARENT_SCOPE_FOR_FROZEN_REVISION53" or z.get("global_input_invalidity_claimed") is not False or z.get("scientific_semantics_resolved") is not False: fail("Hetop zero exclusion")
p=ex.get("finite_positive_subthreshold_outside_P_envelope",{})
if p.get("state")!="NOT_QUALIFIED_FAIL_CLOSED" or "NOT(0<P<=3.8510200002999744e-7)" not in p.get("predicate",""): fail("outside envelope")
pc=c.get("production_binding_constraint",{})
if pc.get("state")!="CARRIED_FROM_NQ03R_NOT_RESOLVED_HERE" or pc.get("blocks_parent_scientific_admission") is not False or pc.get("blocks_bitwise_production_binding") is not True: fail("production binding constraint")
if c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2" or c.get("formal_disposition")!="HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY": fail("history")
if c.get("candidate_decision")!=DEC or c.get("candidate_admitted") is not True or c.get("production_authorized") is not False or c.get("b4_opened") is not False: fail("candidate decision/boundaries")

# Exact child admissions.
d33=gj(D33,"integration/animo-b3/ANIMO-B3D33_STATUS.json")
if d33.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or d33.get("admitted") is not True or d33.get("qualified") is not True: fail("B3D33 admission")
if d33.get("admission_effect",{}).get("parent_tcd_admitted") is not False or d33.get("supported_scope")!=B1: fail("B3D33 scope/parent")
d34=gj(D34,"integration/animo-b3/ANIMO-B3D34_STATUS.json")
if d34.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or d34.get("admitted") is not True or d34.get("qualified") is not True: fail("B3D34 admission")
if d34.get("supported_scope")!=E1 or d34.get("admission_effect",{}).get("parent_tcd_admitted") is not False: fail("B3D34 scope/parent")
if d34.get("hard_boundaries",{}).get("bitwise_production_binding_authorized") is not False: fail("B3D34 production binding")

# Atomization and routing completeness.
i05=gj(I05,"integration/animo-b3/B3I05_TCD042_ATOMIZATION.json")
atoms={a["atom_id"]:a for a in i05.get("atoms",[])}
if set(atoms)!={"TCD-042-B1","TCD-042-E1"}: fail("B3I05 atom set")
if atoms["TCD-042-B1"].get("scope")!="Flpn=0 AND Flux=0" or atoms["TCD-042-E1"].get("scope")!="Flpn=0 AND 0<Flux<1.0d-8": fail("B3I05 child domains")
if i05.get("allocation_decision",{}).get("new_top_level_tcd_reserved") is not False: fail("B3I05 register")
i10=gj(I10,"integration/animo-b3/B3I10_TCD042_CHILD_SCOPE_ROUTING.json")
ch=i10.get("children",{})
if ch.get("TCD-042-B1",{}).get("supported_revision53_scope")!=B1: fail("B3I10 B1 scope")
if ch.get("TCD-042-E1",{}).get("supported_revision53_scope")!="Flpn=0 AND 0<Flux<1.0d-8 AND Hetop>0 subject to NQ03/NQ03R P envelope": fail("B3I10 E1 scope")
if ch.get("TCD-042-B1",{}).get("scope_widening_allowed") is not False or ch.get("TCD-042-E1",{}).get("scope_widening_allowed") is not False: fail("B3I10 no widening")
h0=i10.get("Hetop_zero_disposition",{})
if h0.get("state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53" or h0.get("global_input_invalidity_claimed") is not False or h0.get("scientific_semantics_resolved") is not False: fail("B3I10 zero boundary")
if i10.get("parent",{}).get("automatic_admission_from_child_scope_routing_forbidden") is not True: fail("B3I10 automatic parent guard")

# Aggregate and global queue are snapshots, not automatic composition authorities.
rg=gj(RG,"integration/animo-reg/ANIMO-RG05L_STATUS.json")
if rg.get("work_status",{}).get("qualified") is not True or rg.get("b3_complete") is not False or rg.get("b4_open") is not False or rg.get("production_open") is not False: fail("RG05L state")
if rg.get("tcd042_state",{}).get("parent_admitted") is not False or rg.get("tcd042_state",{}).get("admitted_children")!=["TCD-042-B1"]: fail("RG05L TCD042 snapshot")
q=gj(Q03,"integration/animo-b3/ANIMO-B3Q03_STATUS.json")
if q.get("current_aggregate_authority")!="ANIMO-RG05L@"+RG or "TCD-042" not in q.get("unadmitted_top_level",[]) or q.get("global_canonical_b3_queue_closed") is not False: fail("B3Q03 snapshot")

# Historical route and Tier-D classification. B3D32 is precedent only; science is not reused.
g3=gj(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
if g3.get("qualified_G6U_state")!="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" or g3.get("hard_boundaries",{}).get("historical_B2_recovered") is not False: fail("GOV03 route")
g4=gj(GOV04,"integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
if g4.get("governance_semantics",{}).get("strictest_applicable_risk_trigger_wins") is not True: fail("GOV04 strictest rule")
td=g4.get("risk_tiers",{}).get("D",{})
if "COMPOSITION" not in td.get("default_qualification_classes",[]) or td.get("automatic_promotion_from_atomic_admission") is not False: fail("GOV04 Tier D composition")
prec=gj(D32,"integration/animo-b3/ANIMO-B3D32_INTERNAL_ADVERSARIAL_REVIEW.json")
if not str(prec.get("risk_tier","")).startswith("D_") or prec.get("counter_hypotheses",[])[7].get("id")!="CH8": fail("B3D32 composition precedent")

# Coverage and B1 diagnostic partition oracles.
if cv.get("supported_parent_predicate")!=PARENT or cv.get("parent")!="TCD-042": fail("coverage parent")
ca={x["child"]:x for x in cv.get("coverage",[])}
if set(ca)!={"TCD-042-B1","TCD-042-E1"} or ca["TCD-042-B1"].get("predicate")!=B1 or ca["TCD-042-E1"].get("predicate")!=E1: fail("coverage children")
a=cv.get("overlap_gap_audit",{})
for k in ["B1_E1_overlap","Flux_zero_double_ownership","missing_state_inside_supported_parent_predicate","excluded_remainder_silently_included","scope_widened"]:
    if a.get(k) is not False: fail("coverage audit "+k)
if a.get("parent_composition_complete_for_supported_revision53_scope") is not True or a.get("full_parser_domain_complete") is not False: fail("coverage completion boundary")
if o.get("kind")!="SYNTHETIC_COMPOSITION_PARTITION_ORACLES_B1_DIAGNOSTIC_NOT_B2" or o.get("invariants",{}).get("not_historical_reference") is not True: fail("oracle evidence class")
ocs={x["id"]:x for x in o.get("cases",[])}
if ocs["C01"].get("expected_owner")!="TCD-042-B1" or ocs["C02"].get("expected_owner")!="TCD-042-E1": fail("positive partition oracles")
for cid in ["C03","C04","C05","C06","C07","C08"]:
    if ocs[cid].get("expected_in_supported_parent") is not False or ocs[cid].get("expected_owner")!="NONE": fail(cid+" exclusion oracle")

if f.get("base_head")!=BASE or f.get("review_must_pin_exact_commit") is not True or f.get("substantive_change_resets_GOV05_review") is not True: fail("freeze contract")

allowed={
 ".github/workflows/animo-b3d35-tcd042-parent-composition.yml",
 "docs/b3d35/WORK_UNIT_CONTRACT.md",
 "integration/animo-b3/B3D35_TCD042_PARENT_COMPOSITION_CONTRACT.json",
 "integration/animo-b3/B3D35_TCD042_PARENT_COVERAGE.json",
 "integration/animo-b3/B3D35_TCD042_PARENT_ORACLES.json",
 "integration/animo-b3/ANIMO-B3D35_AUTHORING_FREEZE.json",
 "integration/animo-b3/ANIMO-B3D35_INTERNAL_ADVERSARIAL_REVIEW.json",
 "integration/animo-b3/ANIMO-B3D35_STATUS.json",
 "tools/validate_b3d35_tcd042_parent.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(changed)-allowed)
if extra: fail("scope escape "+str(extra))
for pth in changed:
    if pth.startswith("src/") or pth.startswith("reference/"): fail("source/reference modified")

rp=R/"integration/animo-b3/ANIMO-B3D35_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
    r=json.loads(rp.read_text()); h=r.get("reviewed_head")
    if r.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("same_agent") is not True or r.get("genuinely_independent") is not False or r.get("independence_claimed") is not False or r.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail("review assurance")
    if r.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD042_RESTRICTED_PARENT_WITH_HISTORICAL_UNCERTAINTY": fail("review outcome")
    if not h: fail("reviewed head missing")
    post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
    if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D35_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D35_STATUS.json"}): fail("post-review substantive change")
    if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True or s.get("parent_tcd_admitted") is not True: fail("final admission state")
    ae=s.get("admission_effect",{})
    if ae.get("parent_tcd_admitted") is not True or ae.get("children_readmitted") is not False or ae.get("Hetop_zero_admitted") is not False or ae.get("outside_NQ03_envelope_admitted") is not False or ae.get("production_authorized") is not False: fail("final admission effect")
    ap=s.get("aggregate_policy",{})
    if ap.get("post_RG05L_new_admissions_if_exact_final_green")!=2 or ap.get("normal_batch_threshold_minimum")!=3 or ap.get("aggregate_update_required_after_exact_final_green") is not False: fail("aggregate cadence")
    print("B3D35 PASS final bounded TCD042 parent composition",h)
else:
    if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_D_ADVERSARIAL_REVIEW" or s.get("state")!="CANDIDATE_NOT_ADMITTED_PENDING_REVIEW" or s.get("admitted") is not False or s.get("qualified") is not False: fail("pre-review state")
    print("B3D35 PASS frozen pending GOV05 Tier-D adversarial review")
