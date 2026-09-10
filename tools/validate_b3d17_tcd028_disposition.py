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
EXPECTED_DECISION = "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D17 FAIL_CLOSED: " + msg)


def load_local(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


d = load_local("TCD028_TIER_C_FORMAL_DISPOSITION.json")
s = load_local("ANIMO-B3D17_STATUS.json")

# Workunit and authority identity.
req(d["work_unit"] == "ANIMO-B3D17" and d["target"] == "TCD-028", "wrong workunit or target")
req(d["authoring_base"] == f"ANIMO-RG05F@{RG05F}", "aggregate authoring base drift")
req(d["decision"] == EXPECTED_DECISION, "formal decision drift")
req(d["formal_disposition"] == EXPECTED_DISPOSITION, "formal disposition drift")
req(d["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "B3 qualification class drift")
req(d["gov04_risk_tier"] == "C", "GOV04 risk tier drift")
req(d["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "historical route drift")
req(d["admitted"] is False, "formal disposition workunit performed admission")
req(d["authorities"]["GOV04"] == f"ANIMO-GOV04@{GOV04}", "GOV04 authority drift")
req(d["authorities"]["GOV03"] == f"ANIMO-GOV03@{GOV03}", "GOV03 authority drift")
req(d["authorities"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 authority drift")
req(d["authorities"]["B3I03"] == f"ANIMO-B3I03@{B3I03}", "B3I03 authority drift")
req(d["authorities"]["readiness"] == f"ANIMO-B3B08@{READINESS}", "readiness authority drift")
req(d["authorities"]["independent_review"] == f"ANIMO-B3B08R@{REVIEW}", "independent review authority drift")

# Independent review is complete, PASS, and still explicitly non-admitting.
r = git_show_json(REVIEW, "integration/animo-b3/ANIMO-B3B08R_REVIEW_RESULT.json")
req(r["work_unit"] == "ANIMO-B3B08R" and r["target"] == "TCD-028", "wrong review object")
req(r["semantic_result"] == "PASS", "independent review did not PASS")
req(r["reviewed_object"]["readiness_head"] == READINESS, "reviewed readiness object drift")
req(r["classification"]["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "review class drift")
req(r["classification"]["gov04_risk_tier"] == "C", "review risk tier drift")
req(set(r["classification"]["tier_c_triggers"]) == {"INITIALIZATION_SEMANTICS", "SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY"}, "review Tier-C triggers drift")
req(r["independent_scientific_determination"]["ownership"] == "CURRENT_PLOUGH_EVENT_TRANSACTION_ACCUMULATORS", "review ownership result drift")
req(r["independent_scientific_determination"]["event_start_additive_identity_required"] is True, "review did not require event-start identity")
req(r["scope_and_non_actions"]["b3_admission_performed"] is False, "review performed admission")
req(r["historical_uncertainty"]["historical_revision53_manifestation"] == "UNKNOWN_WITHOUT_B2", "review historical uncertainty drift")
req(r["historical_uncertainty"]["current_gnu_persistence_is_b2"] is False, "review promoted GNU evidence to B2")

# GOV03 route remains historical-uncertainty only.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 route drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "B2 unexpectedly recovered")
req(d["historical_uncertainty"]["qualified_b2_available"] is False, "disposition falsely claims B2")
req(d["historical_uncertainty"]["historical_revision53_manifestation"] == "UNKNOWN_WITHOUT_B2", "disposition overclaims historical behavior")
req(d["historical_uncertainty"]["historical_fidelity_claimed"] is False, "historical fidelity overclaimed")

# GOV04 strictest risk allocation and Tier-C review requirements are retained.
g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["qualification_class_is_not_risk_tier"] is True, "GOV04 class/tier separation missing")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger rule missing")
forced = set(g4["risk_tiers"]["C"]["forced_tier_triggers"])
req("INITIALIZATION_SEMANTICS" in forced and "SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY" in forced, "Tier-C trigger authority drift")
req(g4["risk_tiers"]["C"]["independent_second_line_required"] is True, "Tier-C independent review requirement missing")
req(g4["risk_tiers"]["C"]["admission_workunit_combination_allowed"] == "CONDITIONAL_NOT_DEFAULT", "Tier-C admission combination policy drift")
req(d["gov04_disposition"]["separate_admission_decision_required_by_this_workunit_contract"] is True, "disposition improperly combines admission")
req(d["gov04_disposition"]["tier_d_trigger_found"] is False, "unexpected Tier-D trigger")

# Canonical TCD-028 identity remains OPEN at pinned register authority; this workunit cannot mutate it.
reg_text = git_show(B3I03, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv")
rows = list(csv.DictReader(io.StringIO(reg_text)))
rows28 = [row for row in rows if row.get("ID") == "TCD-028"]
req(len(rows28) == 1, "canonical register does not contain exactly one TCD-028")
req(rows28[0].get("status") == "OPEN", "pinned canonical TCD-028 state is not OPEN")
req(rows28[0].get("process") == "stable DOM plough redistribution accumulator lifecycle", "canonical TCD-028 process identity drift")
req(d["collision_and_live_state"]["canonical_tcd028_state_at_b3i03"] == "OPEN", "recorded canonical state drift")

# Candidate identity remains exactly bounded to the three event-start assignments.
p10c = git_show_json(PREP10C, "integration/animo-prep/PREP10C_EVENT_RESET_CANDIDATE.json")
req(p10c["candidate_transform"]["candidate_addit_sha256"] == d["frozen_identity"]["candidate_addit_sha256"], "candidate Addit hash drift")
req(p10c["frozen_identity"]["addit_member_sha256"] == d["frozen_identity"]["frozen_addit_sha256"], "frozen Addit hash drift")
req(p10c["candidate_transform"]["changes"] == [
    "SuStdiorma = 0.0 at the start of each Pl(I)>0 event",
    "SuStdiorni = 0.0 at the start of each Pl(I)>0 event",
    "If (Ipo.Eq.1) SuStdiorpo = 0.0 at the start of each Pl(I)>0 event"
], "candidate PREP10C change set drift")
req(d["scientific_disposition"]["candidate_insertions"] == [
    "SuStdiorma = 0.0",
    "SuStdiorni = 0.0",
    "If (Ipo.Eq.1) SuStdiorpo = 0.0"
], "formal disposition widened candidate")
req(d["scientific_disposition"]["preserves_conditional_p_semantics"] is True, "P conditional semantics lost")

# Expected-difference and non-admission boundaries remain explicit.
req(d["expected_difference_surface"]["whole_model_equivalence_claimed"] is False, "whole-model equivalence overclaimed")
req(d["expected_difference_surface"]["global_arbitrary_tolerance_allowed"] is False, "arbitrary tolerance admitted")
req("restart serialization/checkpoint representation" in d["expected_difference_surface"]["must_not_change_semantics"], "restart representation boundary missing")
req(len(d["residual_uncertainties"]) >= 4, "residual uncertainty incomplete")
req(d["next_allowed_workunit"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD028", "next-workunit contract drift")
for key, value in d["hard_boundaries"].items():
    req(value is False, f"forbidden disposition side effect recorded: {key}")

# Status must remain a disposition-only record. It may transition from pending to validated without changing the scientific decision.
req(s["work_unit"] == "ANIMO-B3D17" and s["target"] == "TCD-028", "status identity drift")
req(s["decision"] == EXPECTED_DECISION and s["formal_disposition"] == EXPECTED_DISPOSITION, "status decision drift")
req(s["admitted"] is False and s["production_authorized"] is False, "status over-admits")
req(s["independent_review_result"] == "PASS", "status review result drift")
req(s["next_if_validated"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD028", "status next-workunit drift")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden status side effect recorded: {key}")
if s["validation"]["machine_validated"]:
    req(s["validation"]["conclusion"] == "success", "validated status lacks successful conclusion")
    req(s["validation"]["validator"] == "PASS" and s["validation"]["scope_guard"] == "PASS", "validated status lacks PASS checks")
    req(isinstance(s["validation"]["run_id"], int) and isinstance(s["validation"]["job_id"], int), "validated status lacks CI identifiers")

print("B3D17 PASS: TCD-028 Tier-C formal disposition is review-pinned, historically uncertainty-bounded, atomic, and explicitly not admitted.")
