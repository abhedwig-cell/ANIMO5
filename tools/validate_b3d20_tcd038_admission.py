#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

BASE = "8deb1f45c58a9fa3151abc6422aa4f0e55d73a35"
RG05G = "4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
READINESS = "1b47d6b2e422463b557a48355ad8b4f5bed70ebc"
REVIEW = "c6fcd47f4fb4c0277fa27860ee66dc83a449a038"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I03 = "814ea660d367494432beb63ea78298d1f6cd73d7"
STATEQ01 = "4adae99576eb56978da71f7c8a250e4445fd3bc4"
STATEQ02 = "cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6"
B3I04 = "400b7cd79f89043e091751707dfa96537587dcf6"
B3I05_TCD042 = "1f94a6e08db5d73e8935fb095de9ef9798f6544c"
B3I05_UBQ02 = "7fa0162415e02a6f0167e71b48ae38177a9e06e0"
B3I06 = "8f01f0cb366dfa8cc63a184d6f885100899a8cd9"

DECISION = "ADMIT_TCD038_ATOMIC_CROP_ACTUAL_UPTAKE_RESTART_INITIALIZATION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_C"
FINAL_STATE = "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY"
DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D20 FAIL_CLOSED: " + msg)


def local_json(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


m = local_json("TCD038_B3_ADMISSION_CLOSEOUT.json")
s = local_json("ANIMO-B3D20_STATUS.json")

# The admission branch must retain the exact qualified B3D19 final head in its ancestry.
subprocess.check_call(["git", "merge-base", "--is-ancestor", BASE, "HEAD"])
d = git_show_json(BASE, "integration/animo-b3/TCD038_TIER_C_FORMAL_DISPOSITION.json")
dstatus = git_show_json(BASE, "integration/animo-b3/ANIMO-B3D19_STATUS.json")

req(d["work_unit"] == "ANIMO-B3D19" and d["target"] == "TCD-038", "wrong formal-disposition authority")
req(d["decision"] == "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION", "B3D19 decision drift")
req(d["formal_disposition"] == DISPOSITION, "B3D19 disposition drift")
req(d["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "B3D19 qualification class drift")
req(d["gov04_risk_tier"] == "C", "B3D19 GOV04 tier drift")
req(d["next_allowed_workunit"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD038", "B3D19 does not hand off to this gate")
req(dstatus["validation"]["machine_validated"] is True, "B3D19 status is not machine validated")
req(dstatus["validation"]["conclusion"] == "success", "B3D19 recorded validation is not successful")

# Reuse, but independently re-pin, readiness and second-line result.
b = git_show_json(READINESS, "integration/animo-b3/ANIMO-B3B09_STATUS.json")
req(b["work_unit"] == "ANIMO-B3B09" and b["target"] == "TCD-038", "wrong readiness authority")
req(b["readiness_qualified"] is True, "B3B09 readiness is not qualified")
req(b["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "readiness class drift")
req(b["gov04_risk_tier"] == "C", "readiness risk-tier drift")
req(b["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "readiness historical boundary drift")
req(b["restart_state_contract"]["required_restore_direction"] == "Rsampl*_act -> Ampl*_act", "readiness restore direction drift")
req(b["restart_state_contract"]["potential_uptake_in_scope"] is False, "readiness leaked TCD-039 potential uptake into scope")

r = git_show_json(REVIEW, "integration/animo-b3/TCD038_INDEPENDENT_SECOND_LINE_REVIEW.json")
req(r["work_unit"] == "ANIMO-B3B09R", "wrong independent-review workunit")
req(r["canonical_target"]["id"] == "TCD-038", "review target drift")
req(r["decision"]["outcome"] == "PASS", "independent second-line did not PASS")
req(r["decision"]["admission_performed"] is False, "review improperly performed admission")
req(r["independent_findings"]["restore_direction"]["direction"] == "Rsampl*_act -> Ampl*_act", "review restore direction drift")
req(r["independent_findings"]["risk_tier"]["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "review B3 class drift")
req(r["independent_findings"]["risk_tier"]["gov04_risk_tier"] == "C", "review GOV04 tier drift")
req(r["independent_findings"]["tcd039_exclusion"]["composition_required"] is False, "review requires TCD-039 composition")
req(r["evidence_strength_bounds"]["historical_revision_53_behavior"] == "UNKNOWN_WITHOUT_B2", "review historical uncertainty drift")
req(r["evidence_strength_bounds"]["qualified_B2_found_for_TCD038"] is False, "review unexpectedly found qualified B2")

# GOV03 and GOV04 remain controlling.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 uncertainty route drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 now reports historical B2")

g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger rule missing")
req(g4["governance_semantics"]["qualification_class_is_not_risk_tier"] is True, "GOV04 class/tier separation missing")
forced = set(g4["risk_tiers"]["C"]["forced_tier_triggers"])
for trigger in ("RESTART_OR_COLD_START_DISCRIMINATION", "INITIALIZATION_SEMANTICS", "CHECKPOINT_SEMANTICS"):
    req(trigger in forced, f"GOV04 Tier-C trigger missing: {trigger}")
req(g4["risk_tiers"]["C"]["independent_second_line_required"] is True, "GOV04 Tier-C second-line requirement missing")

# Machine-readable admission must match the live-rechecked authority set.
req(m["work_unit"] == "ANIMO-B3D20" and m["target"] == "TCD-038", "wrong admission record identity")
req(m["decision"] == DECISION, "admission decision drift")
req(m["result_after_final_head_green"] == FINAL_STATE, "final admission state drift")
req(m["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "admission qualification class drift")
req(m["gov04_risk_tier"] == "C", "admission risk tier drift")
req(m["formal_disposition"] == DISPOSITION, "admission historical disposition drift")
req(m["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "admission route drift")
req(m["verify_and_reuse"]["governance_mode"] == "VERIFY_AND_REUSE", "VERIFY_AND_REUSE not preserved")
req(m["verify_and_reuse"]["readiness_reopened"] is False, "readiness was reopened")
req(m["verify_and_reuse"]["independent_review_reopened"] is False, "independent review was reopened")
req(m["verify_and_reuse"]["formal_disposition_reopened"] is False, "formal disposition was reopened")
req(m["verify_and_reuse"]["superseding_contradiction_found"] is False, "record reports a superseding contradiction")

expected_authorities = {
    "aggregate": f"ANIMO-RG05G@{RG05G}",
    "readiness": f"ANIMO-B3B09@{READINESS}",
    "independent_review": f"ANIMO-B3B09R@{REVIEW}",
    "formal_disposition": f"ANIMO-B3D19@{BASE}",
    "GOV04": f"ANIMO-GOV04@{GOV04}",
    "GOV03": f"ANIMO-GOV03@{GOV03}",
    "B3Q01": f"ANIMO-B3Q01@{B3Q01}",
    "B3I03": f"ANIMO-B3I03@{B3I03}",
    "STATEQ01": f"ANIMO-STATEQ01@{STATEQ01}",
    "STATEQ02": f"ANIMO-STATEQ02@{STATEQ02}",
    "B3I04": f"ANIMO-B3I04@{B3I04}",
    "B3I05_TCD042_ROUTING": f"ANIMO-B3I05@{B3I05_TCD042}",
    "B3I05_UBQ02_ROUTING": f"ANIMO-B3I05@{B3I05_UBQ02}",
    "B3I06": f"ANIMO-B3I06@{B3I06}",
}
req(m["authorities"] == expected_authorities, "authority pins changed")
req(m["base"]["formal_disposition"] == f"ANIMO-B3D19@{BASE}", "formal-disposition base drift")
req(m["base"]["aggregate_at_start"] == f"ANIMO-RG05G@{RG05G}", "aggregate-at-start drift")

lr = m["live_recheck_before_branch_creation"]
req(lr["b3d20_or_later_tcd038_admission_found"] is False, "pre-existing later TCD-038 admission recorded")
req(lr["newer_aggregate_than_rg05g_found"] is False, "newer aggregate recorded")
req(lr["b3d19_final_head_matches"] is True, "B3D19 final-head check failed")
req(lr["b3d19_final_ci"] == {"run_id": 34531475001, "head": BASE, "conclusion": "success"}, "B3D19 final CI evidence drift")
req(lr["b3b09_head_matches"] is True and lr["b3b09r_head_matches"] is True, "readiness/review live pin mismatch")
req(lr["b3b09r_result"] == "PASS", "live review result not PASS")
req(lr["b3b09r_ci"]["run_id"] == 34528522077 and lr["b3b09r_ci"]["conclusion"] == "success", "review CI evidence drift")
req(lr["tcd038_issue_search"]["review_issue"] == 47, "review issue drift")
req(lr["tcd038_issue_search"]["review_issue_result"] == "PASS", "review issue no longer records PASS in admission evidence")
req(lr["tcd038_issue_search"]["new_conflicting_or_superseding_tcd038_evidence_found"] is False, "conflicting TCD-038 evidence recorded")
req(lr["later_state_or_routing_contradiction_found"] is False, "later state/routing contradiction recorded")

# Exact atomic candidate and boundary.
sc = m["admitted_scope"]
req(sc["persistent_coordinate"] == "CUMULATIVE_ACTUAL_CROP_UPTAKE", "persistent coordinate drift")
req(sc["required_restore_direction"] == "Rsampl*_act -> Ampl*_act", "restore direction drift")
req(sc["candidate_insertions"] == [
    "Amplni_act = Rsamplni_act before the existing nitrogen threshold statement",
    "Amplpo_act = Rsamplpo_act inside Ipo.Eq.1 before the existing phosphorus threshold statement",
], "atomic candidate changed or widened")
req(sc["crop_trigger_retained"] == "Kicr(1).Ne.6 .Or. (Kicr(1).Eq.6 .And. Ioptcu.Eq.1)", "crop trigger changed")
req(sc["small_value_threshold_retained"] == "1.0d-4", "small-value threshold changed")
req(sc["phosphorus_guard_retained"] == "Ipo.Eq.1", "P guard changed")
req(sc["checkpoint_representation_changed"] is False, "checkpoint representation changed")
req(sc["checkpoint_restore_semantics_changed"] is True, "restore-semantic correction missing")
req(sc["new_state_introduced"] is False, "new state introduced")
req(sc["potential_uptake_in_scope"] is False and sc["tcd039_composed"] is False, "TCD-039 composition leaked in")
req(sc["general_crop_checkpoint_redesign"] is False, "scope broadened into general crop checkpoint redesign")

# Expected-difference and non-interference contract.
ed = m["expected_difference_surface"]
req(ed["whole_model_equivalence_claimed"] is False, "whole-model equivalence overclaimed")
req(ed["global_arbitrary_tolerance_allowed"] is False, "arbitrary global tolerance admitted")
for item in (
    "crop trigger definition",
    "1.0d-4 small-value policy",
    "Ipo.Eq.1 phosphorus applicability",
    "potential uptake state owned by TCD-039",
    "checkpoint serialization representation",
    "numerical precision policy",
    "solver/tolerance policy",
    "unrelated state and process semantics",
    "frozen B0 identities",
):
    req(item in ed["must_not_change_semantics"], f"non-interference boundary missing: {item}")

ni = m["state_restart_non_interference"]
req(ni["STATEQ01_promoted_to_tcd038_proof"] is False, "STATEQ01 overpromoted")
req(ni["STATEQ02_promoted_to_tcd038_proof"] is False, "STATEQ02 overpromoted")
req(ni["canonical_state_promoted"] is False, "canonical STATE promoted")
req(ni["checkpoint_layout_changed"] is False, "checkpoint layout changed")
req(ni["unrelated_restore_coordinates_changed"] is False, "unrelated restore coordinate changed")

hu = m["historical_uncertainty"]
req(hu["qualified_b2_available"] is False, "qualified B2 unexpectedly asserted")
req(hu["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical behavior overclaimed")
req(hu["gnu_diagnostic_is_b2"] is False, "GNU diagnostic promoted to B2")
req(hu["historical_fidelity_claimed"] is False, "historical fidelity overclaimed")
req(len(m["residual_uncertainties"]) >= 4, "residual uncertainty incomplete")

for key, value in m["hard_boundaries"].items():
    req(value is False, f"forbidden admission side effect recorded: {key}")
req(m["finalization_rule"]["qualified_state_requires_green_workflow_on_exact_final_head"] is True, "final-head green gate missing")
req(m["finalization_rule"]["qualified_state"] == FINAL_STATE, "finalization target drift")
req(m["finalization_rule"]["next_aggregate_created_here"] is False, "aggregate creation leaked into B3D20")
req(m["finalization_rule"]["stop_after_atomic_admission"] is True, "stop boundary missing")

# Status can be pending on the evidence-package head or final on the status-only closeout head.
req(s["work_unit"] == "ANIMO-B3D20" and s["target"] == "TCD-038", "status identity drift")
req(s["decision"] == DECISION, "status decision drift")
req(s["target_state_after_green_final_head"] == FINAL_STATE, "status final-state target drift")
req(s["formal_disposition"] == DISPOSITION, "status disposition drift")
req(s["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES" and s["gov04_risk_tier"] == "C", "status class/tier drift")
req(s["governance_mode"] == "VERIFY_AND_REUSE", "status governance mode drift")
req(s["production_authorized"] is False, "status authorizes production")
req(s["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical boundary drift")
req(s["stop_condition"] == "STOP_AFTER_FINAL_QUALIFIED_ATOMIC_ADMISSION_NO_RG05H", "status stop condition drift")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden status side effect recorded: {key}")

if s["state"] == "PENDING_FINAL_HEAD_MACHINE_VALIDATION":
    req(s["admitted"] is False and s["qualified"] is False, "pending status already effective")
    req(s["validation"]["machine_validated"] is False, "pending status claims validation")
elif s["state"] == FINAL_STATE:
    req(s["admitted"] is True and s["qualified"] is True, "final status is not admitted and qualified")
    v = s["validation"]
    req(v["machine_validated"] is True, "final status lacks machine validation")
    req(v["conclusion"] == "success", "final status lacks successful evidence run")
    req(v["validator"] == "PASS" and v["scope_guard"] == "PASS", "final status lacks PASS checks")
    req(isinstance(v["run_id"], int) and isinstance(v["job_id"], int), "final status lacks CI identifiers")
    req(isinstance(v["evidence_head"], str) and len(v["evidence_head"]) == 40, "final status lacks evidence head")
else:
    req(False, "unrecognized status state")

print("B3D20 PASS: TCD-038 atomic Tier-C admission is authority-pinned, VERIFY_AND_REUSE bounded, historically uncertainty-preserving, and non-production.")
