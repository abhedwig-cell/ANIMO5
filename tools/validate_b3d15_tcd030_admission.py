#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

REVIEW_HEAD = "e64f6ef936a08c8975a2c53000408b67dd03881d"
READINESS_HEAD = "98235bad7d7fb25b5053e9101c52c0ee3226692a"
RG05F_HEAD = "7c61a5031f41d602e996310df6f3958cbd1b511e"
GOV04_HEAD = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03_HEAD = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01_HEAD = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I03_REGISTER_HEAD = "814ea660d367494432beb63ea78298d1f6cd73d7"
EXPECTED_DECISION = "QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B"
EXPECTED_RISK = "B_LOCAL_ALGEBRA_INDEX_SPECIES"
EXPECTED_REVIEW = "PASS_INDEPENDENT_SECOND_LINE_REVIEW_TIER_B"
EXPECTED_CLAIM = (
    "In revision 53 macropore initial-input validation, keep the existing >MPnitr: read ownership unchanged "
    "and change only the two NO3-labelled Checkrea value selectors from CoMpnh(1) and CoMpnh(2) to the "
    "corresponding NO3 values CoMpni(1) and CoMpni(2)."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_show_json(commit, path):
    text = subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)
    return json.loads(text)


def req(cond, msg):
    if not cond:
        raise SystemExit(f"B3D15 FAIL_CLOSED: {msg}")


review_status = load(B3 / "ANIMO-B3B06R_STATUS.json")
review = load(B3 / "TCD030_INDEPENDENT_REVIEW_EVIDENCE.json")
disp = load(B3 / "TCD030_GOV04_TIER_B_FORMAL_DISPOSITION.json")
adm = load(B3 / "TCD030_B3_ADMISSION_CLOSEOUT.json")
status = load(B3 / "ANIMO-B3D15_STATUS.json")
rg05f = git_show_json(RG05F_HEAD, "integration/animo-reg/ANIMO-RG05F_STATUS.json")

# Independent review must be complete, separate-context and machine-qualified.
req(review_status["work_unit"] == "ANIMO-B3B06R", "wrong review workunit")
req(review_status["decision"] == EXPECTED_REVIEW, "review did not end in the required Tier-B PASS")
req(review_status["qualified"] is True and review_status["tested"] is True, "review is not qualified and tested")
req(review_status["review_independence"] == "SEPARATE_CHATGPT_CONTEXT_INDEPENDENT_REEVALUATION", "review independence contract missing")
req(review_status["admission_performed"] is False, "review improperly performed admission")
req(review["review_state"] == "QUALIFIED_COMPLETE", "review evidence not complete")
req(review["review_result"] == EXPECTED_REVIEW, "review evidence result mismatch")
req(review["review_ci"]["retest_required"] is False, "review still requires fail-closed retest")
passes = [a for a in review["review_ci"]["attempts"] if a.get("conclusion") == "success"]
req(any(a.get("run_id") == 34482752015 and a.get("validator") == "PASS" and a.get("scope_guard") == "PASS" for a in passes),
    "qualified independent review CI run not pinned")

# The first failed review CI must remain visible and must not be misreported as scientific falsification.
failures = [a for a in review["review_ci"]["attempts"] if a.get("conclusion") == "failure"]
req(any(a.get("run_id") == 34482162963 and a.get("classification") == "TOOLING_VALIDATOR_FAILURE" for a in failures),
    "fail-closed review tooling history was lost")

# Authority pins and current aggregate snapshot.
req(review["authority_pins"]["readiness"] == READINESS_HEAD, "readiness pin drift")
req(review["authority_pins"]["current_aggregate_regie"] == RG05F_HEAD, "review aggregate pin drift")
req(review["authority_pins"]["gov04"] == GOV04_HEAD, "GOV04 pin drift")
req(review["authority_pins"]["gov03"] == GOV03_HEAD, "GOV03 pin drift")
req(review["authority_pins"]["b3q01"] == B3Q01_HEAD, "B3Q01 pin drift")
req(review["authority_pins"]["b3i03_register_append"] == B3I03_REGISTER_HEAD, "canonical register pin drift")
req(rg05f["work_unit"] == "ANIMO-RG05F", "pinned aggregate is not RG05F")
req(rg05f["work_status"]["qualified"] is True, "RG05F is not qualified")
req(rg05f["aggregate_state"]["admitted_tcds"] == ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015", "TCD-027", "TCD-041"],
    "RG05F admitted-TCD baseline drift")
req(rg05f["batch"]["normal_cadence"] == "3_TO_5_NEW_ATOMIC_ADMISSIONS", "RG05F batching cadence drift")

# Claim and review-to-disposition continuity.
req(disp["claim"] == EXPECTED_CLAIM, "formal disposition claim drift")
req(adm["atomic_claim"] == EXPECTED_CLAIM, "admission claim drift")
req(disp["starting_review_handoff"] == f"ANIMO-B3B06R@{REVIEW_HEAD}", "review head drift")
req(disp["readiness_authority"] == f"ANIMO-B3B06@{READINESS_HEAD}", "readiness authority drift")
req(disp["independent_review"]["outcome"] == EXPECTED_REVIEW, "disposition review outcome mismatch")
req(disp["independent_review"]["separate_chatgpt_context"] is True, "disposition lost review independence")
req(disp["independent_review"]["realized_count"] == 1, "wrong independent-review count")
req(adm["independent_second_line_gate"]["gate"] == "PASS", "independent review gate not passed")
req(adm["independent_second_line_gate"]["review_outcome"] == EXPECTED_REVIEW, "admission review outcome mismatch")
req(adm["independent_second_line_gate"]["review_admission_decision_performed"] is False, "review/admission roles collapsed")

# GOV04 strict Tier-B route. Any Tier-C trigger or wider scope fails closed.
req(disp["gov04"]["principle"] == "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS", "GOV04 principle drift")
req(disp["gov04"]["risk_tier"] == "B", "risk tier is not B")
req(disp["gov04"]["risk_class"] == EXPECTED_RISK, "risk class drift")
req(disp["gov04"]["tier_c_trigger_applicable"] is False, "Tier-C trigger became applicable")
for key in [
    "persistent_state_initialization_semantics_change", "restart_or_checkpoint_semantics_change",
    "state_reconstruction_required", "runtime_architecture_change", "numerical_policy_change",
    "solver_or_tolerance_change"
]:
    req(disp["gov04"][key] is False, f"Tier-C or wider-scope condition present: {key}")
req(review["gov04"]["selected_tier"] == "B" and review["gov04"]["tier_c_escalation"] is False,
    "review risk result no longer supports Tier B")
req(adm["risk"]["tier"] == "B" and adm["risk"]["class"] == EXPECTED_RISK, "admission risk route drift")
req(adm["risk"]["tier_c_trigger_applicable"] is False, "admission records Tier C")

# Exact species ownership and selector seam.
sc = disp["scientific_contract"]
req(sc["routine"] == "MaPoInput" and sc["routine_branch"] == "Nupa.EQ.4", "source seam drift")
req(sc["caller_gate"] == "Ioptmp.Eq.1", "activation gate drift")
req(sc["read_value_sequence"] == ["CoMpnh(1)", "CoMpnh(2)", "CoMpni(1)", "CoMpni(2)"], "read ownership/order drift")
req(sc["physical_assignment_already_correct"] is True and sc["effect_class"] == "VALIDATION_ONLY", "scope is no longer validation-only")
expected_selectors = [
    ("CoMpnh(1)", "CoMpni(1)", "CoMpni(1)"),
    ("CoMpnh(2)", "CoMpni(2)", "CoMpni(2)"),
]
actual_selectors = [(x["legacy_value_selector"], x["corrected_value_selector"], x["diagnostic_label"]) for x in sc["selector_corrections"]]
req(actual_selectors == expected_selectors, "selector correction widened or drifted")

# Checkrea semantics including 999 sentinel and boundaries.
cr = disp["checkrea_contract"]
req(cr["low_argument"] == 0.0 and cr["high_argument"] == 999.0, "Checkrea arguments drift")
req(cr["high_999_is_sentinel"] is True, "999.0 misclassified as an active upper bound")
req(cr["zero_accepted"] is True and cr["greater_than_999_accepted"] is True, "boundary/sentinel semantics drift")
req(cr["negative_error"] == 1992, "negative-value error path drift")
req(cr["upper_error_1993_reachable_on_tcd030_path"] is False, "unreachable upper error was promoted")
req(cr["read_error_8500_part_of_tcd030"] is False, "parse-error path was incorrectly composed")

# Independent review matrix must cover the predeclared controls.
required_matrix = {"valid_unequal", "invalid_no3_d1", "invalid_no3_d2", "zero_boundary", "just_below_zero", "above_999", "invalid_nh4_control", "inactive"}
rows = {r["id"]: r for r in review["matrix"]}
req(required_matrix == set(rows), "review matrix coverage drift")
req(rows["invalid_no3_d1"]["legacy"]["status"] == "ACCEPT" and rows["invalid_no3_d1"]["candidate"]["error"] == 1992, "domain-1 NO3 divergence not established")
req(rows["invalid_no3_d2"]["legacy"]["status"] == "ACCEPT" and rows["invalid_no3_d2"]["candidate"]["error"] == 1992, "domain-2 NO3 divergence not established")
req(rows["invalid_nh4_control"]["legacy"] == rows["invalid_nh4_control"]["candidate"], "NH4 control unexpectedly diverges")
req(rows["above_999"]["candidate"]["status"] == "ACCEPT", "999 sentinel control failed")
req(rows["inactive"]["legacy"] == rows["inactive"]["candidate"], "inactive control unexpectedly diverges")

# Expected differences, historical uncertainty and non-composition remain bounded.
exp = disp["expected_difference"]
req(exp["allowed_differences"] == ["INPUT_ACCEPTANCE_REJECTION", "DIRECT_VALIDATION_DIAGNOSTIC_AND_ERROR_RETURN"], "expected-difference surface widened")
for key in ["physical_state_assignment_change", "transport_algebra_change", "persistent_state_change", "restart_change", "solver_or_numerical_policy_change"]:
    req(exp[key] is False, f"forbidden scientific change admitted: {key}")
req(exp["trajectory_equivalence_claimed_for_divergence_domain"] is False, "invalid trajectory-equivalence claim")
req(disp["control_flow_nuance"]["invalid_nh4_already_rejected_before_tcd030_seam"] is True, "NH4 control-flow nuance lost")
req(disp["control_flow_nuance"]["newly_accepted_whole_routine_case_created_by_correction"] is False, "incorrect newly-accepted case claimed")
req(disp["historical_route"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical behavior overclaimed")
req(disp["historical_route"]["historical_fidelity_claimed"] is False, "historical fidelity claimed")
req(adm["historical_uncertainty"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "admission historical behavior overclaimed")
req(adm["composition"]["TCD-025"] is False and adm["composition"]["TCD-031"] is False, "TCD-025 or TCD-031 composition introduced")

# Frozen source identities are unchanged across review and disposition/admission.
pins = {
    "source_zip_sha256": "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
    "mapoinput_sha256": "081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065",
    "input1_sha256": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95"
}
for key, val in pins.items():
    review_key = "archive_sha256" if key == "source_zip_sha256" else key
    req(review["frozen_b0"][review_key] == val, f"review source pin drift: {key}")
    req(disp["evidence_pins"][key] == val, f"disposition source pin drift: {key}")
    req(adm["evidence"][key] == val, f"admission source pin drift: {key}")

# Formal decision and hard boundaries.
req(disp["formal_disposition"] == "QUALIFY_FOR_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B", "formal disposition mismatch")
req(adm["decision"] == EXPECTED_DECISION and adm["admitted"] is True, "atomic admission decision mismatch")
for key in ["production_source_modified", "composition_performed", "b4_opened", "production_migration_opened", "canonical_tcd_register_modified", "central_rg05_updated"]:
    req(disp[key] is False, f"forbidden disposition side effect: {key}")
for key, value in adm["authorization"].items():
    req(value is False, f"forbidden admission authorization: {key}")
req(adm["central_integration"]["included_in_current_rg05f"] is False, "TCD-030 falsely included in RG05F")
req(adm["central_integration"]["post_rg05f_atomic_admission_ordinal"] == 1, "unexpected post-RG05F ordinal")
req(adm["central_integration"]["normal_batch_cadence"] == "3_TO_5_NEW_ATOMIC_ADMISSIONS", "aggregate batching cadence mismatch")
req(adm["central_integration"]["required_later"] is True, "central integration incorrectly closed")

req(status["formal_decision"] == EXPECTED_DECISION, "status decision mismatch")
req(status["starting_review_head"] == REVIEW_HEAD, "status review head mismatch")
req(status["aggregate_authority_at_start"] == f"ANIMO-RG05F@{RG05F_HEAD}", "status aggregate authority mismatch")
req(status["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty drift")
req(status["post_rg05f_atomic_admission_ordinal"] == 1, "status post-RG05F ordinal drift")
for key in ["production_source_modified", "composition_performed", "tcd025_composed", "tcd031_composed", "b4_opened", "production_migration_opened", "canonical_tcd_register_modified", "central_rg05_updated"]:
    req(status[key] is False, f"status records forbidden side effect: {key}")

# Permit either the pre-validation or qualified closeout state so the same gate validates the closeout commit.
req(status["status"] in {"ADMISSION_DECISION_PERSISTED_MACHINE_VALIDATION_PENDING", "QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B"}, "invalid B3D15 status state")
req(adm["validation_state"] in {"PENDING_B3D15_MACHINE_GATE", "VALIDATED_BY_B3D15_MACHINE_GATE"}, "invalid admission validation state")

print("B3D15 PASS: TCD-030 Tier-B atomic admission is review-gated, source-pinned, validation-only, historically uncertainty-bounded, non-composed and production-closed.")
