#!/usr/bin/env python3
import csv
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

RG05G = "4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I03 = "814ea660d367494432beb63ea78298d1f6cd73d7"
READINESS = "1b47d6b2e422463b557a48355ad8b4f5bed70ebc"
REVIEW = "c6fcd47f4fb4c0277fa27860ee66dc83a449a038"
EXPECTED_DECISION = "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D19 FAIL_CLOSED: " + msg)


def load_local(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


d = load_local("TCD038_TIER_C_FORMAL_DISPOSITION.json")
s = load_local("ANIMO-B3D19_STATUS.json")

# Identity, base and non-admission boundary.
req(d["work_unit"] == "ANIMO-B3D19" and d["target"] == "TCD-038", "wrong workunit or target")
req(d["authoring_base"] == f"ANIMO-RG05G@{RG05G}", "aggregate authoring base drift")
subprocess.check_call(["git", "merge-base", "--is-ancestor", RG05G, "HEAD"])
req(d["decision"] == EXPECTED_DECISION, "decision drift")
req(d["formal_disposition"] == EXPECTED_DISPOSITION, "formal disposition drift")
req(d["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "B3 class drift")
req(d["gov04_risk_tier"] == "C", "GOV04 risk tier drift")
req(d["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "admission route drift")
req(d["admitted"] is False, "disposition workunit performed B3 admission")
req(d["authorities"]["aggregate"] == f"ANIMO-RG05G@{RG05G}", "aggregate authority pin drift")
req(d["authorities"]["GOV04"] == f"ANIMO-GOV04@{GOV04}", "GOV04 authority drift")
req(d["authorities"]["GOV03"] == f"ANIMO-GOV03@{GOV03}", "GOV03 authority drift")
req(d["authorities"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 authority drift")
req(d["authorities"]["B3I03"] == f"ANIMO-B3I03@{B3I03}", "B3I03 authority drift")
req(d["authorities"]["readiness"] == f"ANIMO-B3B09@{READINESS}", "readiness authority drift")
req(d["authorities"]["independent_review"] == f"ANIMO-B3B09R@{REVIEW}", "review authority drift")

# Independent review is a real PASS and explicitly not an admission.
r = git_show_json(REVIEW, "integration/animo-b3/TCD038_INDEPENDENT_SECOND_LINE_REVIEW.json")
req(r["work_unit"] == "ANIMO-B3B09R", "wrong review workunit")
req(r["canonical_target"]["id"] == "TCD-038", "review target drift")
req(r["decision"]["outcome"] == "PASS", "independent review did not PASS")
req(r["decision"]["admission_performed"] is False, "review performed admission")
req(r["independent_findings"]["restore_direction"]["direction"] == "Rsampl*_act -> Ampl*_act", "restore-direction review drift")
req(r["independent_findings"]["risk_tier"]["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "review B3 class drift")
req(r["independent_findings"]["risk_tier"]["gov04_risk_tier"] == "C", "review risk tier drift")
req(r["independent_findings"]["tcd039_exclusion"]["composition_required"] is False, "review requires TCD-039 composition")
req(r["evidence_strength_bounds"]["historical_revision_53_behavior"] == "UNKNOWN_WITHOUT_B2", "review historical boundary drift")
req(r["evidence_strength_bounds"]["qualified_B2_found_for_TCD038"] is False, "review unexpectedly found B2")

# GOV03 historical-uncertainty route remains authoritative.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 route drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 now reports historical B2")
req(d["historical_uncertainty"]["qualified_b2_available"] is False, "disposition falsely claims B2")
req(d["historical_uncertainty"]["historical_revision53_manifestation"] == "UNKNOWN_WITHOUT_B2", "historical behavior overclaimed")
req(d["historical_uncertainty"]["gnu_diagnostic_is_b2"] is False, "GNU diagnostic evidence promoted to B2")
req(d["historical_uncertainty"]["historical_fidelity_claimed"] is False, "historical fidelity overclaimed")

# GOV04 strictest-trigger and Tier-C independent-review rules remain intact.
g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["qualification_class_is_not_risk_tier"] is True, "GOV04 class/tier separation missing")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger rule missing")
forced = set(g4["risk_tiers"]["C"]["forced_tier_triggers"])
for trigger in ("RESTART_OR_COLD_START_DISCRIMINATION", "INITIALIZATION_SEMANTICS", "CHECKPOINT_SEMANTICS"):
    req(trigger in forced, f"Tier-C trigger missing from GOV04: {trigger}")
req(g4["risk_tiers"]["C"]["independent_second_line_required"] is True, "Tier-C second-line rule missing")
req(g4["risk_tiers"]["C"]["admission_workunit_combination_allowed"] == "CONDITIONAL_NOT_DEFAULT", "Tier-C combination policy drift")
req(d["gov04_disposition"]["separate_admission_decision_required_by_this_workunit_contract"] is True, "disposition improperly combines admission")
req(d["gov04_disposition"]["tier_d_trigger_found"] is False, "unexpected Tier-D trigger")

# Canonical TCD identity remains OPEN at the pinned register; this workunit may not mutate it.
reg_text = git_show(B3I03, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv")
rows = list(csv.DictReader(io.StringIO(reg_text)))
rows38 = [row for row in rows if row.get("ID") == "TCD-038"]
req(len(rows38) == 1, "canonical register does not contain exactly one TCD-038")
req(rows38[0].get("status") == "OPEN", "pinned canonical TCD-038 state is not OPEN")
req(rows38[0].get("process") == "crop actual uptake restart initialization", "canonical TCD-038 process identity drift")
req(d["collision_and_live_state"]["canonical_tcd038_state_at_b3i03"] == "OPEN", "recorded canonical state drift")

# Scientific scope is exactly the reviewed restore-direction correction.
sc = d["scientific_disposition"]
req(sc["required_restore_direction"] == "Rsampl*_act -> Ampl*_act", "formal restore direction drift")
req(sc["candidate_insertions"] == [
    "Amplni_act = Rsamplni_act before the existing nitrogen threshold statement",
    "Amplpo_act = Rsamplpo_act inside Ipo.Eq.1 before the existing phosphorus threshold statement"
], "candidate widened or changed")
req(sc["crop_trigger_retained"] == "Kicr(1).Ne.6 .Or. (Kicr(1).Eq.6 .And. Ioptcu.Eq.1)", "crop trigger drift")
req(sc["small_value_threshold_retained"] == "1.0d-4", "small-value policy drift")
req(sc["phosphorus_guard_retained"] == "Ipo.Eq.1", "P guard drift")
req(sc["checkpoint_representation_changed"] is False, "checkpoint representation changed")
req(sc["checkpoint_restore_semantics_changed"] is True, "restore-semantics effect not recorded")
req(sc["new_state_introduced"] is False, "new state introduced")
req(sc["potential_uptake_in_scope"] is False and sc["tcd039_composed"] is False, "TCD-039 leaked into TCD-038 disposition")

# Expected differences and hard boundaries remain claim-scoped.
req(d["expected_difference_surface"]["whole_model_equivalence_claimed"] is False, "whole-model equivalence overclaimed")
req(d["expected_difference_surface"]["global_arbitrary_tolerance_allowed"] is False, "arbitrary tolerance admitted")
req("potential uptake state owned by TCD-039" in d["expected_difference_surface"]["must_not_change_semantics"], "TCD-039 boundary missing")
req(len(d["residual_uncertainties"]) >= 4, "residual uncertainty incomplete")
req(d["next_allowed_workunit"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD038", "next-workunit contract drift")
for key, value in d["hard_boundaries"].items():
    req(value is False, f"forbidden disposition side effect recorded: {key}")

# Status is disposition-only. It may later become machine-validated without changing the decision.
req(s["work_unit"] == "ANIMO-B3D19" and s["target"] == "TCD-038", "status identity drift")
req(s["decision"] == EXPECTED_DECISION and s["formal_disposition"] == EXPECTED_DISPOSITION, "status decision drift")
req(s["admitted"] is False and s["production_authorized"] is False, "status over-admits")
req(s["independent_review_result"] == "PASS", "status review result drift")
req(s["next_if_validated"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD038", "status next-workunit drift")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden status side effect recorded: {key}")
if s["validation"]["machine_validated"]:
    req(s["validation"]["conclusion"] == "success", "validated status lacks success")
    req(s["validation"]["validator"] == "PASS" and s["validation"]["scope_guard"] == "PASS", "validated status lacks PASS checks")
    req(isinstance(s["validation"]["run_id"], int) and isinstance(s["validation"]["job_id"], int), "validated status lacks CI identifiers")

print("B3D19 PASS: TCD-038 Tier-C formal disposition is review-pinned, historically uncertainty-bounded, atomic, and explicitly not admitted.")
