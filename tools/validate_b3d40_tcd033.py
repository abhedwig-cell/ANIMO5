#!/usr/bin/env python3
import json
import pathlib
import subprocess

R = pathlib.Path(__file__).resolve().parents[1]
BASE = "28306877152972a9a8ba1a19e1c61fda56b658a0"
RG = "8758bd30e302b75dd7854ac00fd2e29473669a13"
Q05 = "997d867a2b107ec8e28efce530c82a204719de46"
B3I01 = "383c7a83e84a578969f92113280dc715b7bdddb4"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
DEC = "ADMIT_TCD033_CH4_COMPONENT_PARENT_DAUGHTER_PARTITION_IDENTITY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
IDENT = "TCD033_CH4_COMPONENT_PARENT_DAUGHTER_PARTITION_QI_EQ_Q_SI_OVER_S"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"


def fail(x):
    print("B3D40 FAIL_CLOSED:", x)
    raise SystemExit(1)


def load(p):
    return json.loads((R / p).read_text())


def gj(s, p):
    return json.loads(subprocess.check_output(["git", "show", f"{s}:{p}"], cwd=R, text=True))


c = load("integration/animo-b3/B3D40_TCD033_ADMISSION_CONTRACT.json")
s = load("integration/animo-b3/ANIMO-B3D40_STATUS.json")
f = load("integration/animo-b3/ANIMO-B3D40_AUTHORING_FREEZE.json")

if c.get("target_tcd") != "TCD-033" or c.get("atomic_target") != "CANONICAL_TOP_LEVEL_TCD:TCD-033":
    fail("target")
if c.get("b3_qualification_class") != "B_LOCAL_SCIENTIFIC_IDENTITY" or c.get("review_risk_tier") != "C_SCIENTIFIC_MASS_TRANSFER_PARTITION_IDENTITY":
    fail("class/risk")
if c.get("admitted_identity") != IDENT or c.get("candidate_decision") != DEC or c.get("candidate_admitted") is not True:
    fail("candidate identity/decision")
if c.get("historical_behavior") != "UNKNOWN_WITHOUT_B2" or c.get("formal_disposition") != "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY":
    fail("historical route")
for k in ("production_authorized", "b4_opened", "canonical_register_modified", "aggregate_modified", "whole_model_golden_baseline_created"):
    if c.get(k) is not False:
        fail("boundary " + k)
sc = c.get("supported_scope", {})
expected = {
    "routine": "CH4produc",
    "species": "CH4_C",
    "A_definition": "A=1-Rdfaox",
    "S_definition": "S=sum_i(S_i) for the existing pre-aeration methanogenic source-family contributions",
    "existing_early_return": "A<1.0e-8 implies Q=0 and all Q_i=0",
    "zero_substrate": "S=0 implies Q=0 and all Q_i=0",
    "positive_substrate": "Q_i=Q*S_i/S",
    "equivalent_form": "Q_i=E*A*S_i",
    "parent_daughter_identity": "sum_i(Q_i)=Q",
    "source_share_identity": "Q_i/Q_j=S_i/S_j where defined",
    "component_units": "kg_C_m-2_d-1",
    "parent_units": "kg_C_m-2_d-1",
}
for k, v in expected.items():
    if sc.get(k) != v:
        fail("scope " + k)
if not all(x in sc.get("outside_scope", []) for x in [
    "TCD-032 comprehensive methanogenesis source-pool transfer activation/ownership",
    "TCD-034 plant-growth temperature indexing semantics",
    "production implementation",
]):
    fail("outside-scope list")
qe = c.get("qualified_evidence", {})
if qe.get("GHG02_exact_final") != "ANIMO-GHG02@" + BASE or qe.get("GHG02_exact_final_ci") != "34654987849:success":
    fail("GHG02 evidence pin")
if qe.get("full_anaerobic_legacy_compatibility") is not True or qe.get("partial_anaerobic_legacy_negative_control") is not True or qe.get("zero_substrate_domain_negative_control") is not True:
    fail("controls")
if qe.get("historical_B2_created") is not False or qe.get("whole_model_mass_balance_used_as_acceptance_criterion") is not False:
    fail("evidence boundary")

# Exact-final scientific qualification authority.
g = gj(BASE, "integration/animo-ghg/ANIMO-GHG02_STATUS.json")
if g.get("target") != "TCD-033" or g.get("state") != "QUALIFIED_TCD033_SCIENTIFIC_PARTITION_POLICY_NO_B3_ADMISSION" or g.get("qualified") is not True:
    fail("GHG02 state")
if g.get("decision") != "QUALIFIED_TCD033_CH4_COMPONENT_PARENT_DAUGHTER_PARTITION_IDENTITY_READY_FOR_SEPARATE_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY":
    fail("GHG02 decision")
if g.get("b3_admission_performed") is not False or g.get("production_authorized") is not False:
    fail("GHG02 boundary")
if g.get("historical_behavior") != "UNKNOWN_WITHOUT_B2":
    fail("GHG02 history")
qi = g.get("qualified_identity", {})
for k, v in {
    "anaerobic_early_return": "if A < 1.0e-8 then Q=0 and all Q_i=0",
    "zero_substrate": "if S=0 then Q=0 and all Q_i=0",
    "positive_substrate": "Q_i=Q*S_i/S",
    "equivalent_form": "Q_i=E*A*S_i",
    "parent_daughter_closure": "sum_i(Q_i)=Q",
}.items():
    if qi.get(k) != v:
        fail("GHG02 identity " + k)
rv = g.get("review", {})
if rv.get("completed") is not True or rv.get("genuinely_independent") is not False or rv.get("outcome") != "SELF_REVIEW_PASS_TCD033_SCIENTIFIC_PARTITION_POLICY_WITH_HISTORICAL_UNCERTAINTY":
    fail("GHG02 review")
if g.get("validation", {}).get("authoring_conclusion") != "success":
    fail("GHG02 validation")

# Current queue/aggregate must still be open and TCD033 unadmitted before this candidate.
q = gj(Q05, "integration/animo-b3/ANIMO-B3Q05_STATUS.json")
if q.get("current_aggregate_authority") != "ANIMO-RG05N@" + RG or "TCD-033" not in q.get("unadmitted_top_level", []):
    fail("B3Q05 queue")
if q.get("global_canonical_b3_queue_closed") is not False or q.get("b4_allowed") is not False or q.get("production_allowed") is not False:
    fail("B3Q05 downstream gates")
rg = gj(RG, "integration/animo-reg/ANIMO-RG05N_STATUS.json")
if rg.get("work_status", {}).get("qualified") is not True or rg.get("scientific_admission_count") != 29 or rg.get("top_level_admitted_tcd_count") != 19:
    fail("RG05N counts/state")
if rg.get("b3_complete") is not False or rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG05N downstream state")

route = gj(B3I01, "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json")
entries = [x for x in route.get("canonical_routing", []) if x.get("canonical_key") == "TCD-033"]
if len(entries) != 1:
    fail("canonical allocation cardinality")
e = entries[0]
if e.get("b3_class") != "B" or e.get("source_local_key") != "GHG01-LCL-CH4-PRODUCTION-COMPONENT-PARTITION" or e.get("qualification_owner") != "PROPOSED_ANIMO-GHG02":
    fail("canonical allocation")

gov = gj(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
if gov.get("qualified_G6U_state") != "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" or gov.get("hard_boundaries", {}).get("historical_B2_recovered") is not False:
    fail("GOV03 historical-uncertainty route")

if f.get("base_head") != BASE or f.get("review_must_pin_exact_commit") is not True or f.get("substantive_change_resets_GOV05_review") is not True or f.get("exact_final_head_ci_required") is not True:
    fail("freeze")

allowed = {
    ".github/workflows/animo-b3d40-tcd033.yml",
    "docs/b3d40/WORK_UNIT_CONTRACT.md",
    "integration/animo-b3/B3D40_TCD033_ADMISSION_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3D40_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3D40_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3D40_STATUS.json",
    "tools/validate_b3d40_tcd033.py",
}
ch = subprocess.check_output(["git", "diff", "--name-only", BASE + "..HEAD"], cwd=R, text=True).splitlines()
extra = sorted(set(ch) - allowed)
if extra:
    fail("scope escape " + str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-reg/") or p == "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv":
        fail("forbidden mutation " + p)

rp = R / "integration/animo-b3/ANIMO-B3D40_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
    r = json.loads(rp.read_text())
    h = r.get("reviewed_authoring_head")
    if r.get("risk_tier") != "C" or r.get("review_mode") != "SAME_AGENT_SECOND_PASS" or r.get("assurance") != ASSURANCE:
        fail("review metadata")
    if r.get("same_agent") is not True or r.get("genuinely_independent") is not False or r.get("independence_claimed") is not False:
        fail("review independence semantics")
    if r.get("outcome") != "SELF_REVIEW_PASS_ADMIT_TCD033_WITH_HISTORICAL_UNCERTAINTY":
        fail("review outcome")
    if not h or not r.get("reviewed_head_ci_run") or not r.get("reviewed_head_ci_job") or r.get("reviewed_head_ci_conclusion") != "success":
        fail("reviewed head CI")
    post = subprocess.check_output(["git", "diff", "--name-only", h + "..HEAD"], cwd=R, text=True).splitlines()
    if sorted(set(post) - {"integration/animo-b3/ANIMO-B3D40_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-b3/ANIMO-B3D40_STATUS.json"}):
        fail("post-review substantive change")
    if s.get("state") != "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision") != DEC or s.get("admitted") is not True or s.get("qualified") is not True or s.get("admitted_atomic_identity") != IDENT:
        fail("final admission")
    ae = s.get("admission_effect", {})
    if ae.get("tcd033_top_level_admitted") is not True or ae.get("tcd032_admitted_or_modified") is not False or ae.get("tcd034_admitted_or_modified") is not False or ae.get("total_CH4_production_law_reopened") is not False or ae.get("production_authorized") is not False:
        fail("final admission boundaries")
    ap = s.get("aggregate_policy", {})
    if ap.get("post_RG05N_new_admissions_if_exact_final_green") != 1 or ap.get("normal_batch_threshold_reached_if_green") is not False or ap.get("aggregate_update_required_after_exact_final_green") is not False or ap.get("next_aggregate_if_threshold_later_reached") != "ANIMO-RG05O":
        fail("aggregate cadence")
    if s.get("work_status") != {"realized": True, "persisted": True, "tested": True, "reviewed": True, "qualified": True, "workunit_complete": True}:
        fail("final work status")
    print("B3D40 PASS final TCD033 admission", h)
else:
    if s.get("phase") != "AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("state") != "CANDIDATE_NOT_ADMITTED_PENDING_REVIEW" or s.get("admitted") is not False or s.get("qualified") is not False:
        fail("pre-review state")
    print("B3D40 PASS frozen candidate pending GOV05 Tier-C adversarial review")
