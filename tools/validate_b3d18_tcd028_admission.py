#!/usr/bin/env python3
import csv
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

RG05F = "7c61a5031f41d602e996310df6f3958cbd1b511e"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I03 = "814ea660d367494432beb63ea78298d1f6cd73d7"
PREP10C = "549545921dc8175f01d86c283647acd470c14290"
READINESS = "310d7117da739d19eebb718129ac9494cac854a1"
REVIEW = "3281f98feef7af4822e85a0f011ede0b779de07b"
DISPOSITION = "ad1701e72ac51f61f81cc4e9a1857ab14bb8d8d8"
B3D15 = "22e48f7e2c1eaa1245f034de2d909191d9cfa227"
B3D16 = "8650ea9e716336520d8d7df5f9ea2b393d17ab98"
EXPECTED_DECISION = "ADMIT_TCD028_ATOMIC_CLASS_B_STABLE_DOM_EVENT_ACCUMULATOR_RESET_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_C"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D18 FAIL_CLOSED: " + msg)


def load_local(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


a = load_local("TCD028_B3_ADMISSION_CLOSEOUT.json")
s = load_local("ANIMO-B3D18_STATUS.json")

# Workunit and exact admission identity.
req(a["work_unit"] == "ANIMO-B3D18" and a["target"] == "TCD-028", "wrong workunit or target")
req(a["decision"] == EXPECTED_DECISION, "admission decision drift")
req(a["disposition"] == EXPECTED_DISPOSITION, "admission disposition drift")
req(a["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "qualification class drift")
req(a["gov04_risk_tier"] == "C", "GOV04 risk tier drift")
req(a["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "admission route drift")
req(a["admitted"] is True, "TCD-028 not admitted by admission closeout")
req(a["base"]["formal_disposition"] == f"ANIMO-B3D17@{DISPOSITION}", "formal-disposition base drift")
req(a["base"]["aggregate_at_start"] == f"ANIMO-RG05F@{RG05F}", "aggregate-at-start drift")
req(subprocess.run(["git", "merge-base", "--is-ancestor", DISPOSITION, "HEAD"]).returncode == 0, "B3D17 is not ancestor of admission branch")

# Immutable authority pins.
req(a["authorities"]["readiness"] == f"ANIMO-B3B08@{READINESS}", "readiness authority drift")
req(a["authorities"]["independent_review"] == f"ANIMO-B3B08R@{REVIEW}", "review authority drift")
req(a["authorities"]["formal_disposition"] == f"ANIMO-B3D17@{DISPOSITION}", "disposition authority drift")
req(a["authorities"]["GOV04"] == f"ANIMO-GOV04@{GOV04}", "GOV04 authority drift")
req(a["authorities"]["GOV03"] == f"ANIMO-GOV03@{GOV03}", "GOV03 authority drift")
req(a["authorities"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 authority drift")
req(a["authorities"]["B3I03"] == f"ANIMO-B3I03@{B3I03}", "B3I03 authority drift")

# Disposition is green, exact, and non-admitting; admission must not silently widen it.
d = git_show_json(DISPOSITION, "integration/animo-b3/TCD028_TIER_C_FORMAL_DISPOSITION.json")
ds = git_show_json(DISPOSITION, "integration/animo-b3/ANIMO-B3D17_STATUS.json")
req(d["decision"] == "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION", "B3D17 decision drift")
req(d["formal_disposition"] == EXPECTED_DISPOSITION, "B3D17 formal disposition drift")
req(d["admitted"] is False, "B3D17 unexpectedly admitted TCD-028")
req(ds["validation"]["machine_validated"] is True, "B3D17 not machine validated")
req(ds["validation"]["conclusion"] == "success", "B3D17 final status not successful")
req(ds["validation"]["validator"] == "PASS" and ds["validation"]["scope_guard"] == "PASS", "B3D17 validation gates not PASS")
req(d["scientific_disposition"]["candidate_insertions"] == a["admitted_scope"]["candidate_insertions"], "admission candidate widens disposition")
req(d["scientific_disposition"]["ownership"] == a["admitted_scope"]["ownership"], "admission ownership drifts disposition")

# Independent Tier-C review remains PASS for the same readiness object and scope.
r = git_show_json(REVIEW, "integration/animo-b3/ANIMO-B3B08R_REVIEW_RESULT.json")
req(r["semantic_result"] == "PASS", "independent review is not PASS")
req(r["reviewed_object"]["readiness_head"] == READINESS, "reviewed readiness identity drift")
req(r["classification"]["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "review class drift")
req(r["classification"]["gov04_risk_tier"] == "C", "review risk tier drift")
req(set(r["classification"]["tier_c_triggers"]) == {"INITIALIZATION_SEMANTICS", "SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY"}, "review Tier-C triggers drift")
req(r["independent_scientific_determination"]["ownership"] == "CURRENT_PLOUGH_EVENT_TRANSACTION_ACCUMULATORS", "review ownership conclusion drift")
req(r["independent_scientific_determination"]["event_start_additive_identity_required"] is True, "review event-start identity no longer PASS")
req(r["scope_and_non_actions"]["b3_admission_performed"] is False, "review itself performed admission")

# Historical-uncertainty route remains exact and must not be converted to fidelity.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 G6U drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "historical B2 unexpectedly recovered")
req(a["historical_uncertainty"]["qualified_b2_available"] is False, "admission falsely claims B2")
req(a["historical_uncertainty"]["historical_revision53_manifestation"] == "UNKNOWN_WITHOUT_B2", "historical behavior overclaimed")
req(a["historical_uncertainty"]["current_gnu_persistence_is_b2"] is False, "GNU persistence promoted to B2")
req(a["historical_uncertainty"]["historical_fidelity_claimed"] is False, "historical fidelity overclaimed")

# GOV04 risk allocation and separate Tier-C stages remain respected.
g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["qualification_class_is_not_risk_tier"] is True, "GOV04 class/tier separation missing")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger rule missing")
req(g4["risk_tiers"]["C"]["independent_second_line_required"] is True, "Tier-C review requirement missing")
req(g4["risk_tiers"]["C"]["admission_workunit_combination_allowed"] == "CONDITIONAL_NOT_DEFAULT", "Tier-C combination policy drift")
req(a["gates"]["independent_second_line"] == "PASS_ANIMO_B3B08R", "independent review gate not consumed")
req(a["gates"]["formal_disposition"] == "PASS_ANIMO_B3D17", "formal disposition gate not consumed")

# Candidate remains the exact PREP10C bounded transform.
p10c = git_show_json(PREP10C, "integration/animo-prep/PREP10C_EVENT_RESET_CANDIDATE.json")
req(p10c["candidate_transform"]["candidate_addit_sha256"] == a["frozen_identity"]["candidate_addit_sha256"], "candidate Addit hash drift")
req(p10c["frozen_identity"]["addit_member_sha256"] == a["frozen_identity"]["frozen_addit_sha256"], "frozen Addit hash drift")
req(a["admitted_scope"]["candidate_insertions"] == [
    "SuStdiorma = 0.0",
    "SuStdiorni = 0.0",
    "If (Ipo.Eq.1) SuStdiorpo = 0.0"
], "admitted change set widened")
req(a["admitted_scope"]["preserves_existing_current_event_summation"] is True, "current-event summation changed")
req(a["admitted_scope"]["preserves_existing_redistribution_equations"] is True, "redistribution equations changed")
req(a["admitted_scope"]["preserves_conditional_p_semantics"] is True, "conditional P semantics changed")
req(a["admitted_scope"]["new_physical_state"] is False, "new physical state introduced")
req(a["admitted_scope"]["restart_serialization_or_checkpoint_representation_changed"] is False, "restart representation changed")
req(a["admitted_scope"]["numerical_policy_changed"] is False, "numerical policy changed")
req(a["admitted_scope"]["solver_or_tolerance_changed"] is False, "solver/tolerance changed")

# Canonical register remains administratively OPEN; admission branch must not mutate it.
reg_text = git_show(B3I03, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv")
rows = list(csv.DictReader(io.StringIO(reg_text)))
rows28 = [row for row in rows if row.get("ID") == "TCD-028"]
req(len(rows28) == 1 and rows28[0].get("status") == "OPEN", "pinned canonical TCD-028 row is not uniquely OPEN")
req(rows28[0].get("process") == "stable DOM plough redistribution accumulator lifecycle", "canonical TCD-028 identity drift")

# Expected-difference and hard scope boundaries.
req(a["expected_difference_surface"]["global_arbitrary_tolerance_allowed"] is False, "arbitrary scientific tolerance allowed")
req(a["expected_difference_surface"]["whole_model_equivalence_claimed"] is False, "whole-model equivalence overclaimed")
req("restart serialization/checkpoint representation" in a["expected_difference_surface"]["must_not_change_semantics"], "restart representation boundary missing")
req(len(a["residual_uncertainty"]) >= 4, "residual uncertainty incomplete")
for key, value in a["hard_boundaries"].items():
    req(value is False, f"forbidden admission side effect recorded: {key}")

# Pending post-RG05F admission queue reaches normal aggregate threshold, but is not integrated here.
post = a["post_rg05f_atomic_admissions_after_this_workunit"]
req(post[0] == f"ANIMO-B3D15@{B3D15}:TCD-030", "post-RG05F TCD-030 authority drift")
req(post[1] == f"ANIMO-B3D16@{B3D16}:TCD-023", "post-RG05F TCD-023 authority drift")
req(post[2].endswith(":TCD-028"), "TCD-028 not represented as third post-RG05F admission")
req(g4["central_regie_integration"]["normal_batch_min"] == 3, "GOV04 normal batch minimum drift")
req(a["aggregate_policy_effect"]["pending_atomic_admission_count_after_this_workunit"] == 3, "pending atomic admission count drift")
req(a["aggregate_policy_effect"]["normal_aggregate_integration_threshold_reached"] is True, "aggregate threshold not marked reached")
req(a["aggregate_policy_effect"]["aggregate_integration_performed_here"] is False, "admission workunit performed aggregate integration")

# Status may move from persisted/pending to validated without changing the admitted science.
req(s["work_unit"] == "ANIMO-B3D18" and s["target"] == "TCD-028", "status identity drift")
req(s["decision"] == EXPECTED_DECISION and s["disposition"] == EXPECTED_DISPOSITION, "status decision drift")
req(s["admitted"] is True and s["production_authorized"] is False, "status admission/production state invalid")
req(s["formal_disposition_authority"] == f"ANIMO-B3D17@{DISPOSITION}", "status disposition authority drift")
req(s["independent_review_authority"] == f"ANIMO-B3B08R@{REVIEW}", "status review authority drift")
req(s["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty drift")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden status side effect recorded: {key}")
if s["validation"]["machine_validated"]:
    req(s["validation"]["conclusion"] == "success", "validated status lacks successful conclusion")
    req(s["validation"]["validator"] == "PASS" and s["validation"]["scope_guard"] == "PASS", "validated status lacks PASS checks")
    req(isinstance(s["validation"]["run_id"], int) and isinstance(s["validation"]["job_id"], int), "validated status lacks CI ids")

print("B3D18 PASS: TCD-028 is atomically B3-admitted under the reviewed Tier-C historical-uncertainty route, with production/B4/register/composition still closed.")
