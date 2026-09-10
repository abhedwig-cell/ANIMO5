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
PREP10 = "65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab"
PREP10C = "549545921dc8175f01d86c283647acd470c14290"
B3D15 = "22e48f7e2c1eaa1245f034de2d909191d9cfa227"
B3D16 = "8650ea9e716336520d8d7df5f9ea2b393d17ab98"
EXPECTED_DECISION = "QUALIFIED_CLASS_B_ADMISSION_READINESS_GOV04_TIER_C_HISTORICAL_UNCERTAINTY_REVIEW_REQUIRED"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3B08 FAIL_CLOSED: " + msg)


def load_local(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


e = load_local("TCD028_READINESS_EVIDENCE.json")
s = load_local("ANIMO-B3B08_STATUS.json")

# Workunit identity and immutable authority basis.
req(e["work_unit"] == "ANIMO-B3B08" and e["target"] == "TCD-028", "wrong workunit or target")
req(e["authoring_base"] == f"ANIMO-RG05F@{RG05F}", "authoring base drift")
req(e["authority_snapshot"]["GOV04"] == f"ANIMO-GOV04@{GOV04}", "GOV04 authority drift")
req(e["authority_snapshot"]["GOV03"] == f"ANIMO-GOV03@{GOV03}", "GOV03 authority drift")
req(e["authority_snapshot"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 authority drift")
req(e["authority_snapshot"]["PREP10"] == f"ANIMO-PREP10@{PREP10}", "PREP10 authority drift")
req(e["authority_snapshot"]["PREP10C_authoritative"] == f"ANIMO-PREP10C@{PREP10C}", "PREP10C authority drift")
req(e["authority_snapshot"]["post_rg05f_atomic_admissions_observed"] == [f"ANIMO-B3D15@{B3D15}:TCD-030", f"ANIMO-B3D16@{B3D16}:TCD-023"], "post-RG05F authority snapshot drift")

# GOV03 changed the historical-route eligibility after PREP10C, but did not create B2.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["work_status"]["qualified"] is True, "GOV03 not qualified")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 G6U route drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 unexpectedly recovered B2")
req(e["historical_route"]["qualified_b2_available"] is False, "B3B08 falsely claims B2")
req(e["historical_route"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty overclaimed")
req(e["historical_route"]["current_gnu_storage_semantics_are_historical_reference"] is False, "GNU evidence promoted to historical reference")

# Canonical identity is TCD-028 and remains OPEN; deprecated TCD-032 proposal is rejected.
reg_text = git_show(B3I03, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv")
rows = list(csv.DictReader(io.StringIO(reg_text)))
rows28 = [r for r in rows if r.get("ID") == "TCD-028"]
req(len(rows28) == 1, "canonical register does not contain exactly one TCD-028")
r28 = rows28[0]
req(r28.get("status") == "OPEN", "TCD-028 is no longer OPEN at pinned canonical authority")
req(r28.get("process") == "stable DOM plough redistribution accumulator lifecycle", "TCD-028 canonical process name drift")
req(r28.get("classification") == "RESERVED_POST_G5_LOCAL_EVENT_ACCUMULATOR_DEFECT", "TCD-028 canonical classification drift")
req(e["collision_and_supersession_check"]["canonical_tcd_id"] == "TCD-028", "wrong canonical TCD identity")
req(e["collision_and_supersession_check"]["deprecated_parallel_prep10c_tcd032_proposal_authoritative"] is False, "deprecated TCD-032 proposal promoted")

# PREP10 source-bound B1 evidence remains exactly at original strength.
p10 = git_show_json(PREP10C, "integration/animo-prep/PREP10_STABLE_DOM_PLOUGH_ACCUMULATOR_AUDIT.json")
req(p10["frozen_identity"]["source_archive_sha256"] == e["frozen_identity"]["source_archive_sha256"], "source archive identity drift")
req(p10["frozen_identity"]["testbank_archive_sha256"] == e["frozen_identity"]["testbank_archive_sha256"], "testbank identity drift")
req(p10["frozen_identity"]["addit_for_sha256"] == e["frozen_identity"]["addit_for_sha256"], "Addit.for identity drift")
req(p10["source_audit"]["member_size_bytes"] == 35615, "Addit.for size drift")
req(p10["source_audit"]["plough_event_branch_line"] == 449, "plough branch location drift")
req([x["first_self_read_assignment_line"] for x in p10["source_audit"]["targets"]] == [475, 477, 479], "first self-read locations drift")
req(all(x["explicit_definition_before_first_self_read"] is False for x in p10["source_audit"]["targets"]), "unexpected predefinition found")
req(p10["frozen_observer_matrix"]["successful_plough_active_cases"] == 4, "frozen activation count drift")
req(p10["frozen_observer_matrix"]["total_observed_plough_events"] == 31, "frozen event count drift")
req(p10["frozen_observer_matrix"]["all_accumulators_zero_before_and_after_every_observed_event"] is True, "frozen non-discrimination changed")
req(p10["controlled_causal_activation"]["cranmais"]["carbon_carryover_observed"] is True, "C carryover not established")
req(p10["controlled_causal_activation"]["cranmais"]["nitrogen_carryover_observed"] is True, "N carryover not established")
req(p10["controlled_causal_activation"]["zuiderzeeland_phosphorus_enabled"]["conditional_phosphorus_carryover_observed"] is True, "conditional P carryover not established")
req(p10["historical_native_runtime_tested"] is False, "PREP10 evidence strength changed to historical")

# PREP10C exact candidate and conservation scope.
p10c = git_show_json(PREP10C, "integration/animo-prep/PREP10C_EVENT_RESET_CANDIDATE.json")
req(p10c["authoritative_parent"]["commit"] == PREP10, "PREP10C authoritative parent drift")
req(p10c["candidate_transform"]["candidate_addit_sha256"] == e["candidate_identity"]["candidate_addit_sha256"], "candidate Addit hash drift")
req(p10c["current_gnu_build_identity"]["candidate_executable_sha256"] == e["candidate_identity"]["candidate_executable_sha256_current_gnu"], "candidate executable hash drift")
req(p10c["candidate_transform"]["byte_identical_to_authoritative_prep10_counterfactual"] is True, "candidate no longer matches PREP10 counterfactual")
req(p10c["conservation_reconciliation"]["closed_current_event_redistribution_identity_restored"] is True, "event-local conservation not closed")
req(p10c["conservation_reconciliation"]["new_physical_storage_introduced"] is False, "candidate introduces new physical storage")
req(p10c["conservation_reconciliation"]["solver_or_tolerance_change_introduced"] is False, "candidate changes solver/tolerance")
req(p10c["frozen_testbank_noninterference"]["successful_cases_compared"] == 8, "non-interference case count drift")
req(p10c["frozen_testbank_noninterference"]["scientifically_or_structurally_different_files"] == 0, "unexpected frozen-testbank scientific difference")

# GOV04 strictest trigger: B3 Class B but scientific risk Tier C.
g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["qualification_class_is_not_risk_tier"] is True, "GOV04 class/tier separation missing")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger principle missing")
forced = set(g4["risk_tiers"]["C"]["forced_tier_triggers"])
req("INITIALIZATION_SEMANTICS" in forced and "SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY" in forced, "required Tier-C triggers absent from GOV04")
req(e["b3_qualification"]["class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "B3 Class B drift")
req(e["gov04_risk"]["selected_tier"] == "C", "TCD-028 risk is not Tier C")
req(e["gov04_risk"]["forced_tier_c_triggers"]["INITIALIZATION_SEMANTICS"] is True, "initialization trigger not applied")
req(e["gov04_risk"]["forced_tier_c_triggers"]["SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY"] is True, "ownership ambiguity trigger not applied")
req(e["gov04_risk"]["independent_second_line_required"] is True, "Tier-C independent review not required")
req(e["gov04_risk"]["separate_disposition_and_admission_preferred"] is True, "Tier-C separation preference lost")

# Candidate must remain the three bounded event-start initializations only.
req(e["candidate_identity"]["trigger"] == "Pl(I) > 0", "trigger drift")
req(e["candidate_identity"]["insertions_at_beginning_of_each_plough_event"] == [
    "SuStdiorma = 0.0",
    "SuStdiorni = 0.0",
    "If (Ipo.Eq.1) SuStdiorpo = 0.0"
], "candidate widened or drifted")
req(e["candidate_identity"]["preserves_conditional_p_semantics"] is True, "conditional phosphorus semantics lost")
req(e["candidate_identity"]["production_candidate_applied"] is False, "candidate improperly applied to production")

# Expected-difference and residual-uncertainty bounds.
exp = e["expected_difference_contract"]
req("restart serialization or checkpoint representation semantics" in exp["must_not_change_as_part_of_tcd028"], "restart representation boundary missing")
req("numerical solver or tolerance policy" in exp["must_not_change_as_part_of_tcd028"], "solver boundary missing")
req(exp["whole_model_equivalence_claimed"] is False, "whole-model equivalence overclaimed")
req(exp["global_arbitrary_tolerance_allowed"] is False, "arbitrary tolerance allowed")
req(len(e["residual_uncertainties"]) >= 4, "residual uncertainty not explicit")

# Authoring context cannot satisfy its own Tier-C review gate or widen scope.
req(s["decision"] == EXPECTED_DECISION, "status decision drift")
req(s["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "status class drift")
req(s["gov04_risk_tier"] == "C", "status risk tier drift")
req(s["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty drift")
req(s["independent_review"]["required"] is True and s["independent_review"]["status"] == "PENDING_NOT_EXECUTED", "independent review improperly completed in authoring context")
req(s["b3_admitted"] is False and s["production_authorized"] is False, "readiness workunit over-admitted")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden side effect recorded: {key}")

print("B3B08 PASS: TCD-028 Class-B readiness is evidence-pinned, GOV04 Tier-C escalated for initialization/ownership semantics, historically uncertainty-bounded, and review/production closed.")
