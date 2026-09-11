#!/usr/bin/env python3
import csv
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

R2 = "7648e7b2813f3abc5904e4c34e36072d81d9844f"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
B3B10 = "eccba6712f65455161d05fa9cdf6aa142f823dd4"
B3B10R = "36aad892cac546105dfec0fe43aa34a18e23bcad"
B3B10E1 = "8522752f9941e6fd5b421cf5ac4ef839384d7ce7"
STATEQ04 = "ef9a5998cafae433deeba701a8e9a8a08eacc92f"
EXPECTED_DECISION = "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
EXPECTED_REVIEW = "PASS_TARGETED_INDEPENDENT_REREVIEW_TCD031_SOURCE_PROVENANCE_GATES_CLOSED"
ATOMIC_ID = "COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D22 FAIL_CLOSED: " + msg)


def local_json(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


d = local_json("TCD031_TIER_C_FORMAL_DISPOSITION.json")
s = local_json("ANIMO-B3D22_STATUS.json")

# Workunit identity and exact authoring base.
req(d["work_unit"] == "ANIMO-B3D22" and d["target"] == "TCD-031", "wrong disposition identity")
req(d["branch"] == "work/animo-b3d22-tcd031-gov04-tier-c-disposition", "branch identity drift")
req(d["authoring_base"] == f"ANIMO-B3B10R2@{R2}", "authoring base drift")
subprocess.check_call(["git", "merge-base", "--is-ancestor", R2, "HEAD"])
req(d["current_aggregate_at_open"] == f"ANIMO-RG05H@{RG05H}", "aggregate-at-open pin drift")
req(d["decision"] == EXPECTED_DECISION, "decision drift")
req(d["formal_disposition"] == EXPECTED_DISPOSITION, "formal disposition drift")
req(d["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL", "qualification class drift")
req(d["gov04_risk_tier"] == "C", "GOV04 tier drift")
req(d["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "admission route drift")
req(d["admitted"] is False, "disposition workunit performed admission")

# Exact authority pins.
a = d["authorities"]
req(a["aggregate"] == f"ANIMO-RG05H@{RG05H}", "aggregate authority drift")
req(a["GOV04"] == f"ANIMO-GOV04@{GOV04}", "GOV04 authority drift")
req(a["GOV03"] == f"ANIMO-GOV03@{GOV03}", "GOV03 authority drift")
req(a["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 authority drift")
req(a["routing"] == f"ANIMO-B3I07@{B3I07}", "routing authority drift")
req(a["readiness"] == f"ANIMO-B3B10@{B3B10}", "readiness pin drift")
req(a["first_review"] == f"ANIMO-B3B10R@{B3B10R}", "first review pin drift")
req(a["source_remediation"] == f"ANIMO-B3B10E1@{B3B10E1}", "source remediation pin drift")
req(a["independent_targeted_rereview"] == f"ANIMO-B3B10R2@{R2}", "targeted rereview pin drift")
req(a["STATEQ04"] == f"ANIMO-STATEQ04@{STATEQ04}", "STATEQ04 pin drift")

# R2 must be the completed PASS, while the original fail-closed review remains historical authority.
r2 = git_show_json(R2, "integration/animo-b3/ANIMO-B3B10R2_STATUS.json")
req(r2["workunit"] == "ANIMO-B3B10R2" and r2["tcd"] == "TCD-031", "wrong R2 status identity")
req(r2["review_disposition"] == EXPECTED_REVIEW, "R2 did not PASS targeted rereview")
req(r2["independent_tier_c_review_gate"] == "PASSED", "Tier-C review gate not passed")
req(r2["scientific_falsification"] is False, "R2 records scientific falsification")
req(r2["stateq04_reopen_required"] is False, "R2 requires STATEQ04 reopen")
req(r2["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "R2 whole-model boundary drift")
req(r2["historical_b2"] == "ABSENT", "R2 unexpectedly recovered B2")
req(r2["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN", "R2 historical boundary drift")
for gate, value in r2["original_failed_gates"].items():
    req(value in ("PASS", "PASS_WITH_ANSWER_NO"), f"R2 failed source/provenance gate: {gate}={value}")
req(r2["native_RsCoMp_pre_promotion_answer"] == "NO_WITH_EXACT_PROOF", "RsCoMp pre-promotion conclusion drift")
req(r2["atomic_correction_identity"] == ATOMIC_ID, "R2 atomic identity drift")

r1 = git_show_json(B3B10R, "integration/animo-b3/ANIMO-B3B10R_STATUS.json")
req(r1["review_status"] == "COMPLETE_FAIL_CLOSED", "original B3B10R historical status rewritten")
req(r1["review_disposition"] == "REMEDIATION_REQUIRED", "original B3B10R historical disposition drift")
req(r1["scientific_falsification"] is False, "original review scientific falsification drift")

# Readiness class and atomic state model must remain unchanged.
ready = git_show_json(B3B10, "integration/animo-b3/ANIMO-B3B10_STATUS.json")
req(ready["b3_qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL", "B3B10 class drift")
req(ready["gov04_risk_tier"] == "C", "B3B10 Tier-C classification drift")
req(ready["atomic_scope"]["identity"] == ATOMIC_ID, "B3B10 atomic identity drift")
req(ready["atomic_scope"]["p_off_scalars"] == 8 and ready["atomic_scope"]["p_on_scalars"] == 12, "B3B10 persistent count drift")
req(ready["atomic_scope"]["writer_and_restore_halves_separate_admissions"] is False, "B3B10 permits split atomic admission")

# STATEQ04 candidate semantics define accepted-boundary restoration but are not production authorization.
q4 = git_show_json(STATEQ04, "integration/animo-state/STATEQ04_REMEDIATION_CONTRACT.json")
req(q4["checkpoint_boundary"] == "ACCEPTED_BOUNDARY_ONLY", "STATEQ04 boundary drift")
req(q4["domain_count"] == 2, "STATEQ04 domain count drift")
req(q4["persistent_coordinates"]["p_off_scalar_count"] == 8, "STATEQ04 P-off count drift")
req(q4["persistent_coordinates"]["p_on_scalar_count"] == 12, "STATEQ04 P-on count drift")
req(any("initialize the non-independent RsCoMp runtime result alias from the restored accepted CoMp" in x for x in q4["restore_transaction"]), "STATEQ04 RsCoMp restore transaction missing")
req(q4["production_patch"] is False and q4["canonical_state_admission"] is False, "STATEQ04 over-authorized production/state")

# Formal scientific object is exactly the reviewed atomic correction.
sc = d["atomic_scientific_disposition"]
req(sc["identity"] == ATOMIC_ID, "atomic correction identity drift")
req(sc["domain_count"] == 2 and sc["p_off_scalar_count"] == 8 and sc["p_on_scalar_count"] == 12, "persistent coordinate count drift")
req(sc["phosphorus_condition"] == "IPO.EQ.1", "phosphorus condition drift")
req(sc["result_alias"] == "RsCoMp*", "result alias drift")
req(sc["serializer_only_is_sufficient"] is False, "serializer-only incorrectly accepted")
req(sc["restore_only_is_sufficient"] is False, "restore-only incorrectly accepted")
req(sc["writer_and_restore_halves_are_one_atomic_correction"] is True, "atomicity broken")
req(sc["new_physical_state_introduced"] is False, "unexpected new physical state")

# Claim-scoped split evidence may support disposition while production-bound whole-model equivalence remains explicitly open.
ce = d["claim_scoped_split_evidence"]
req(ce["STATEQ04_candidate_restore_transaction"] == "PASS", "candidate restore transaction not passed")
req(ce["six_species_kernel_coverage"] is True and ce["both_domains_causally_required"] is True, "species/domain causal coverage incomplete")
req(ce["native_bad_emulation_diverges"] is True and ce["domain_drop_controls_diverge"] is True, "negative controls incomplete")
req(ce["comparison_policy"] == "EXACT_BYTEWISE_NO_TOLERANCE", "comparison policy drift")
req(ce["fresh_stage_b_process"] is True, "fresh Stage-B process missing")
req(ce["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "whole-model production split overclaimed")
req(ce["whole_model_production_split_required_for_this_formal_disposition"] is False, "formal-disposition evidence boundary changed")
req(ce["whole_model_production_split_required_before_production_or_migration_equivalence_claim"] is True, "production evidence boundary weakened")

# GOV03 route and historical uncertainty remain fail-closed.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 route drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 now reports historical B2")
h = d["historical_uncertainty"]
req(h["qualified_b2_available"] is False, "disposition falsely claims B2")
req(h["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical behavior overclaimed")
req(h["historical_intent_inferred_from_source"] is False and h["historical_fidelity_claimed"] is False, "historical intent/fidelity overclaimed")

# Current qualified GOV04, not concurrent unqualified GOV05, governs this disposition.
g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger rule missing")
req(g4["risk_tiers"]["C"]["independent_second_line_required"] is True, "GOV04 Tier-C review rule missing")
req(g4["risk_tiers"]["C"]["admission_workunit_combination_allowed"] == "CONDITIONAL_NOT_DEFAULT", "GOV04 Tier-C combination policy drift")
preferred = set(g4["risk_tiers"]["C"]["separate_disposition_admission_preferred_for"])
req("RESTART" in preferred and "CHECKPOINT" in preferred and "STATE" in preferred, "GOV04 separate disposition/admission preference missing")
forced = set(g4["risk_tiers"]["C"]["forced_tier_triggers"])
for trigger in ("RESTART_OR_COLD_START_DISCRIMINATION", "INITIALIZATION_SEMANTICS", "CHECKPOINT_SEMANTICS"):
    req(trigger in forced, f"required Tier-C trigger missing: {trigger}")
req(d["gov04_disposition"]["separate_admission_decision_required_by_this_workunit_contract"] is True, "disposition improperly combines admission")
req(d["gov04_disposition"]["tier_d_trigger_found"] is False, "unexpected Tier-D trigger")
req(d["gov04_disposition"]["production_bound_scope"] is False, "production-bound scope leaked in")
req(d["gov04_disposition"]["numerical_policy_change"] is False and d["gov04_disposition"]["solver_or_tolerance_change"] is False, "numerical policy leaked in")

# Canonical TCD-031 remains OPEN at the latest pinned routing authority; this workunit may not mutate it.
reg_text = git_show(B3I07, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv")
rows = list(csv.DictReader(io.StringIO(reg_text)))
rows31 = [row for row in rows if row.get("ID") == "TCD-031"]
req(len(rows31) == 1, "canonical register does not contain exactly one TCD-031")
req(rows31[0].get("status") == "OPEN", "pinned canonical TCD-031 state is not OPEN")
req(rows31[0].get("process") == "macropore persistent solute restart state", "canonical TCD-031 process identity drift")
req(rows31[0].get("classification") == "RESERVED_POST_G5_MISSING_RESTART_STATE_REPRESENTATION", "canonical TCD-031 classification drift")

# Expected-difference and scope boundaries cannot be widened by disposition.
e = d["expected_difference_surface"]
req(e["whole_model_equivalence_claimed"] is False and e["production_restart_equivalence_claimed"] is False, "whole-model or production equivalence overclaimed")
req(e["global_arbitrary_tolerance_allowed"] is False, "arbitrary numerical tolerance admitted")
req("continuous unsplit execution away from checkpoint and restore paths" in e["must_not_change_semantics"], "continuous-path non-interference missing")
req(d["next_allowed_workunit"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD031", "next-workunit contract drift")
req(d["tcd025_boundary"]["composition_here"] is False and d["tcd025_boundary"]["executed_here"] is False, "TCD-025 leaked into disposition")
for key, value in d["hard_boundaries"].items():
    req(value is False, f"forbidden disposition side effect recorded: {key}")

# Status must remain disposition-only and may only claim qualification after a successful recorded CI run.
req(s["work_unit"] == "ANIMO-B3D22" and s["target"] == "TCD-031", "status identity drift")
req(s["decision"] == EXPECTED_DECISION and s["formal_disposition"] == EXPECTED_DISPOSITION, "status decision drift")
req(s["admitted"] is False and s["production_authorized"] is False, "status over-admits")
req(s["independent_rereview_result"] == EXPECTED_REVIEW, "status R2 result drift")
req(s["atomic_correction_identity"] == ATOMIC_ID, "status atomic identity drift")
req(s["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "status whole-model boundary drift")
req(s["next_if_validated"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD031", "status next-workunit drift")
req(s["concurrent_gov05"]["qualified_as_authority_at_open"] is False and s["concurrent_gov05"]["applied_here"] is False, "unqualified GOV05 applied retroactively")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden status side effect recorded: {key}")
if s["validation"]["machine_validated"]:
    req(s["qualified"] is True, "machine-validated status not qualified")
    req(s["validation"]["conclusion"] == "success", "validated status lacks success")
    req(s["validation"]["validator"] == "PASS" and s["validation"]["scope_guard"] == "PASS", "validated status lacks PASS checks")
    req(isinstance(s["validation"]["run_id"], int) and isinstance(s["validation"]["job_id"], int), "validated status lacks CI identifiers")
else:
    req(s["qualified"] is False and s["validation"]["conclusion"] == "PENDING", "pre-CI status claims qualification")

print("B3D22 PASS: TCD-031 Tier-C formal disposition is review-pinned, atomic, historically uncertainty-bounded, production-bounded, and explicitly not admitted.")
