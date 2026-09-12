#!/usr/bin/env python3
import json
import pathlib
import subprocess

R = pathlib.Path(__file__).resolve().parents[2]
BASE = "3ac98899dd4e6b7a5133cbecd758fab0b81e945d"
NQ02 = "40a41089020f78ee1d5181b8afc7bdb511af3193"
NQ04 = "bfd736b88b6fc4f2a66970b812172729c1923562"
B3D36 = "b74ec4461ab4d7b62ecfaf175e1eeeec8c58f7b2"
B3Q05 = "997d867a2b107ec8e28efce530c82a204719de46"
RG05N = "8758bd30e302b75dd7854ac00fd2e29473669a13"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
DEC = "QUALIFY_TCD019_RESTRICTED_FAST_LANGMUIR_EXACT_STORAGE_REPRESENTATION_STABLE_NO_LEGACY_FALLBACK_POLICY_READY_FOR_SEPARATE_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
IDENT = "TCD019_FAST_LANGMUIR_EXACT_STORAGE_REPRESENTATION_STABLE_TWO_VARIABLE_ROOT_NO_LEGACY_FALLBACK_BINARY64_POLICY"
POLICY = R / "integration/animo-numerics/NQ05_TCD019_RESTRICTED_POLICY.json"
STATUS = R / "integration/animo-numerics/ANIMO-NQ05_STATUS.json"
FREEZE = R / "integration/animo-numerics/ANIMO-NQ05_AUTHORING_FREEZE.json"
REVIEW = R / "integration/animo-numerics/ANIMO-NQ05_INTERNAL_ADVERSARIAL_REVIEW.json"
ORACLE = R / "tools/nq05/tcd019_restricted_policy_oracle.py"
ALLOWED = {
    ".github/workflows/animo-nq05-tcd019.yml",
    "docs/numerics/TCD019_RESTRICTED_NO_FALLBACK_NUMERICAL_POLICY.md",
    "integration/animo-numerics/NQ05_TCD019_RESTRICTED_POLICY.json",
    "integration/animo-numerics/ANIMO-NQ05_AUTHORING_FREEZE.json",
    "integration/animo-numerics/ANIMO-NQ05_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-numerics/ANIMO-NQ05_STATUS.json",
    "tools/nq05/tcd019_restricted_policy_oracle.py",
    "tools/nq05/validate_nq05_tcd019.py",
}


def run(*args):
    return subprocess.run(args, cwd=R, check=True, text=True, capture_output=True).stdout


def gj(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def gt(commit, path):
    return run("git", "show", f"{commit}:{path}")


def load(path):
    return json.loads(path.read_text())


def req(cond, msg):
    if not cond:
        raise SystemExit("ANIMO-NQ05 FAIL_CLOSED: " + msg)


for sha in (BASE, NQ02, NQ04, B3D36, B3Q05, RG05N, GOV03, GOV05):
    subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=R, check=True)

changed = {p for p in run("git", "diff", "--name-only", BASE + "..HEAD").splitlines() if p}
req(changed <= ALLOWED, "scope escape " + str(sorted(changed - ALLOWED)))
for p in changed:
    req(not p.startswith("src/"), "production source modified: " + p)
    req(not p.startswith("reference/"), "frozen reference modified: " + p)
    req(not p.startswith("integration/animo-reg/"), "central regie modified: " + p)
    req(p != "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv", "canonical register modified")

base = gj(BASE, "integration/animo-b3/ANIMO-B3D41_STATUS.json")
req(base["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "B3D41 state")
req(base["target_tcd"] == "TCD-032" and base["qualified"] is True, "B3D41 identity")
req(base["aggregate_policy"]["post_RG05N_new_admissions_if_exact_final_green"] == 2, "post-RG05N count")
req(base["aggregate_policy"]["normal_batch_threshold_reached_if_exact_final_green"] is False if "normal_batch_threshold_reached_if_exact_final_green" in base["aggregate_policy"] else base["aggregate_policy"]["normal_batch_threshold_reached_if_green"] is False, "RG05O must not already be required")

q = gj(B3Q05, "integration/animo-b3/ANIMO-B3Q05_STATUS.json")
req(q["state"] == "QUALIFIED_ANIMO_B3Q05_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_SIX_TOP_LEVEL_UNADMITTED", "B3Q05 state")
req("TCD-019" in q["unadmitted_top_level"], "TCD019 queue membership")
req(q["b4_allowed"] is False and q["production_allowed"] is False, "downstream gates")

reg = gt(BASE, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv")
req("TCD-019,PO4 nonlinear sorption numerical conservation" in reg, "canonical TCD019 row")
req("CONFIRMED_LEGACY_NUMERICAL_CONSERVATION_POLICY_DEFECT" in [line for line in reg.splitlines() if line.startswith("TCD-019,")][0], "TCD019 classification")

n2 = gj(NQ02, "integration/animo-numerics/ANIMO-NQ02_STATUS.json")
req(n2["target"]["tcd"] == "TCD-019" and n2["target"]["b3_class"] == "E", "NQ02 target")
qo = n2["qualification_outcome"]
req(qo["legacy_policy_classification"] == "LEGACY_NUMERICAL_POLICY_NONCONVERGENT_OR_BIASED", "legacy classification")
req(qo["candidate_route_classification"] == "CONVERGENT_POLICY_CANDIDATE", "candidate route")
req(qo["fast_langmuir_natural_multicase_support"] is True, "natural Langmuir support")
req(qo["fallback_policy_qualified"] is False and qo["specific_production_small_qualified"] is False and qo["specific_fallback_tolerance_qualified"] is False, "NQ02 unresolved solver policy")
req(qo["fast_freundlich_integrated_synthetic_solver_support"] is True and qo["fast_freundlich_natural_or_B2_solver_support"] is False, "Freundlich evidence boundary")
req(qo["historical_b2_equivalence_qualified"] is False, "no historical B2")

fm = gj(NQ02, "integration/animo-numerics/TCD019_FALLBACK_POLICY_MATRIX.json")
req(fm["evidence_class"] == "B1_DIAGNOSTIC_NATURAL_FALLBACK_SENSITIVITY_ONLY", "fallback matrix evidence class")
req(fm["qualification"]["fallback_natural_activation"] is True, "fallback natural activation")
req(fm["qualification"]["fallback_policy_causally_material"] is True, "fallback materiality")
req(fm["qualification"]["fallback_threshold_as_ordinary_accuracy_knob_rejected"] is True, "fallback threshold rejection")
req(fm["qualification"]["fallback_policy_classification"] == "FALLBACK_POLICY_CAUSALLY_MATERIAL_BUT_NOT_YET_QUALIFIED", "fallback matrix classification")
req(fm["qualification"]["specific_fallback_tolerance_qualified"] is False and fm["qualification"]["B3_admitted"] is False and fm["qualification"]["production_migration_admitted"] is False, "fallback matrix remains non-admission evidence")

frl = gj(NQ02, "integration/animo-numerics/TCD019_NEWTON_FALLBACK_RELATION.json")
fq = frl["qualification"]
req(fq["fallback_is_scalarized_original_newton_system"] is False, "fallback equation distinction")
req(fq["fallback_uses_distinct_midpoint_time_closure"] is True, "midpoint closure")
req(fq["inherited_Recfso_path_dependence_naturally_activated"] is True, "history-dependent rate branch")
req(fq["joint_newton_fallback_policy_required"] is True and fq["fallback_policy_qualified"] is False, "joint policy blocker")

n4 = gj(NQ04, "integration/animo-science/ANIMO-NQ04_STATUS.json")
req(n4["state"] == "QUALIFIED_TCD029_IFLSOL4_CANCELLATION_SAFE_BINARY64_NUMERICAL_POLICY_READY_FOR_SEPARATE_B3_ADMISSION", "NQ04 state")
req(n4["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "NQ04 history")
d36 = gj(B3D36, "integration/animo-b3/ANIMO-B3D36_STATUS.json")
req(d36["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and d36["target_tcd"] == "TCD-029", "B3D36 state")
req(d36["admission_effect"]["tcd019_admitted_or_modified"] is False, "B3D36 did not admit TCD019")

rg = gj(RG05N, "integration/animo-reg/ANIMO-RG05N_STATUS.json")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05N gates")
g3 = gj(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 uncertainty route")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 no B2")

p = load(POLICY)
req(p["target"] == "TCD-019" and p["b3_class"] == "E_NUMERICAL_POLICY_RESTRICTED_DOMAIN", "policy identity")
req(p["review_risk_tier"] == "C_NUMERICAL_POLICY", "risk tier")
req(p["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "history")
qs = p["qualified_scope"]
req(qs["fast_sorption"] == "LANGMUIR_ONLY_Optcxfa_EQ_2", "fast Langmuir only")
req(qs["slow_sorption"] == ["LINEAR_Optcxsl_EQ_1", "FREUNDLICH_Optcxsl_EQ_3"], "slow scope")
req(qs["slow_langmuir_tcd024"] is False and qs["fast_freundlich"] is False and qs["legacy_fallback_allowed"] is False, "exclusions")
lp = p["langmuir_storage_policy"]
req(lp["secant"] == "D(C,C0)=a/((1+b*C)*(1+b*C0))" and lp["small_delta_switch"] == "NONE", "threshold-free secant")
req(lp["derivative"] == "dD/dC=-a*b/((1+b*C)^2*(1+b*C0))", "secant derivative")
np = p["nonlinear_equation_policy"]
req(np["target"] == "RECONSTRUCTED_C_UNL_TWO_VARIABLE_F1_F2_SYSTEM", "equation target")
req(np["state_local_slow_rate_selection"] is True and np["inherited_Recfso_from_unsuccessful_path_allowed"] is False, "state-local slow branch")
ac = p["acceptance_contract"]
req(ac["model_tolerance"] == "NONE", "no tolerance")
req(ac["representation_stability_Rsc"] == "fl(Rsc-dR)==Rsc" and ac["representation_stability_Avc"] == "fl(Avc-dA)==Avc", "representation stability")
req("immediate-binary64-neighbour" in ac["discrete_neighbor_residual_guard"], "neighbour guard")
req(ac["failure_to_satisfy"] == "FAIL_CLOSED_NO_ACCEPTED_STATE", "fail closed")
req(p["legacy_fallback_exclusion"]["midpoint_constraint_Rsc_eq_2Avc_minus_Con_admitted"] is False, "midpoint excluded")
req(p["candidate_decision"] == DEC and p["b3_admission_performed"] is False and p["production_authorized"] is False, "candidate boundary")
req(all(v is False for v in p["hard_boundaries"].values()), "policy hard boundaries")

fr = load(FREEZE)
req(fr["target"] == "TCD-019" and fr["base_head"] == BASE, "freeze identity")
req(fr["review_must_pin_exact_green_authoring_head"] is True and fr["substantive_change_resets_GOV05_review"] is True, "freeze review contract")

req(ORACLE.exists(), "oracle missing")
out = run("python", str(ORACLE.relative_to(R)))
for needle in [
    "TCD019 restricted policy oracle PASS",
    "finite_delta_tangent_negative_control PASS",
    "representation_stable_root_control PASS",
    "one_ulp_displaceable_negative_controls PASS",
    "model_tolerance NONE",
    "legacy_fallback_admitted false",
]:
    req(needle in out, "oracle output missing " + needle)

s = load(STATUS)
req(s["target"] == "TCD-019" and s["base_authority"] == "ANIMO-B3D41@" + BASE, "status identity")
req(s["qualified_candidate_identity"] == IDENT and s["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "candidate identity/history")
req(s["b3_admission_performed"] is False and s["production_authorized"] is False, "status no admission/production")
req(all(v is False for v in s["hard_boundaries"].values()), "status hard boundaries")

if REVIEW.exists():
    rv = load(REVIEW)
    h = rv.get("reviewed_head")
    req(rv.get("target") == "TCD-019", "review target")
    req(rv.get("model") == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "review model")
    req(rv.get("same_agent") is True and rv.get("genuinely_independent") is False and rv.get("independence_claimed") is False, "review independence semantics")
    req(rv.get("assurance") == ASSURANCE, "review assurance")
    req(bool(h) and rv.get("reviewed_head_ci_run") and rv.get("reviewed_head_ci_job") and rv.get("reviewed_head_ci_conclusion") == "success", "review exact-head CI")
    req(rv.get("outcome") == "SELF_REVIEW_PASS_TCD019_RESTRICTED_NO_FALLBACK_NUMERICAL_POLICY_WITH_HISTORICAL_UNCERTAINTY", "review outcome")
    post = {x for x in run("git", "diff", "--name-only", h + "..HEAD").splitlines() if x}
    req(post <= {"integration/animo-numerics/ANIMO-NQ05_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-numerics/ANIMO-NQ05_STATUS.json"}, "post-review substantive change")
    req(s["phase"] == "CLOSED_QUALIFIED_SCIENTIFIC_POLICY", "final phase")
    req(s["state"] == "QUALIFIED_TCD019_RESTRICTED_FAST_LANGMUIR_NO_LEGACY_FALLBACK_POLICY_READY_FOR_SEPARATE_B3_ADMISSION", "final state")
    req(s["decision"] == DEC and s["qualified"] is True, "final decision")
    req(s["review"]["completed"] is True and s["review"]["genuinely_independent"] is False, "final review state")
    req(s["work_status"] == {"realized": True, "persisted": True, "tested": True, "reviewed": True, "qualified": True, "workunit_complete": True}, "final work status")
    print("ANIMO-NQ05 PASS final restricted TCD019 policy; B3 admission remains separate")
else:
    req(s["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW", "candidate phase")
    req(s["qualified"] is False and s["review"]["completed"] is False and s["work_status"]["tested"] is False, "candidate not prematurely qualified")
    print("ANIMO-NQ05 PASS frozen restricted TCD019 candidate pending GOV05 Tier-C adversarial review")