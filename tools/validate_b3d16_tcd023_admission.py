#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

REVIEW_HEAD = "4e277cfe98bf815b09e4d40d4e9f4af61e11a7fb"
READINESS_HEAD = "e76345bf984c58ff0b30a24b39dc8e037a2f4fd6"
RG05F_HEAD = "7c61a5031f41d602e996310df6f3958cbd1b511e"
B3D15_HEAD = "22e48f7e2c1eaa1245f034de2d909191d9cfa227"
GOV04_HEAD = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03_HEAD = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01_HEAD = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
SYNQ01_HEAD = "842f72300fd03ede0b9024537a7ee6126722a121"
EXPECTED_DECISION = "QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B"
EXPECTED_RISK = "B_LOCAL_ALGEBRA_INDEX_SPECIES"
EXPECTED_CLAIM = (
    "In Resp_miner Case(2), change only the two phosphorus daughter-transfer parent selectors so "
    "Transfop(19,Ln) and Transfop(20,Ln) partition Transfop(17,Ln) rather than Transfon(17,Ln)."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_show_json(commit, path):
    text = subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)
    return json.loads(text)


def req(cond, msg):
    if not cond:
        raise SystemExit(f"B3D16 FAIL_CLOSED: {msg}")


review = load(B3 / "TCD023_INDEPENDENT_SECOND_LINE_REVIEW.json")
disp = load(B3 / "TCD023_GOV04_TIER_B_FORMAL_DISPOSITION.json")
adm = load(B3 / "TCD023_B3_ADMISSION_CLOSEOUT.json")
status = load(B3 / "ANIMO-B3D16_STATUS.json")
rg05f = git_show_json(RG05F_HEAD, "integration/animo-reg/ANIMO-RG05F_STATUS.json")
b3d15 = git_show_json(B3D15_HEAD, "integration/animo-b3/ANIMO-B3D15_STATUS.json")

# Branch must descend from the exact independent-review closeout.
req(subprocess.call(["git", "merge-base", "--is-ancestor", REVIEW_HEAD, "HEAD"]) == 0,
    "independent-review closeout is not an ancestor of this workunit")

# Independent review gate.
req(review["work_unit"] == "ANIMO-B3B05R", "wrong independent review workunit")
req(review["semantic_result"] == "PASS", "independent review result is not PASS")
req(review["review_type"] == "GENUINELY_INDEPENDENT_SECOND_LINE_PROCESS_REVIEW", "review type drift")
req(review["reviewed_readiness"]["head"] == READINESS_HEAD, "reviewed readiness head drift")
req(review["reviewed_readiness"]["actions_conclusion_rechecked"] == "success", "readiness CI not rechecked successful")
req(review["independent_review_gate_satisfied"] is True, "review gate not satisfied")
req(review["admission_performed"] is False, "review improperly performed admission")
req(review["production_modification_performed"] is False, "review modified production")

# Live authority pins captured by the independent review and re-used by B3D16.
req(review["live_authorities"]["aggregate_central_regie"] == f"ANIMO-RG05F@{RG05F_HEAD}", "review aggregate authority drift")
req(review["live_authorities"]["GOV04"] == f"ANIMO-GOV04@{GOV04_HEAD}", "review GOV04 authority drift")
req(review["live_authorities"]["GOV03"] == f"ANIMO-GOV03@{GOV03_HEAD}", "review GOV03 authority drift")
req(review["live_authorities"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01_HEAD}", "review B3Q01 authority drift")
req(review["live_authorities"]["SYNQ01"] == f"ANIMO-SYNQ01@{SYNQ01_HEAD}", "review SYNQ01 authority drift")
req(review["live_authorities"]["later_TCD023_disposition_or_admission_found"] is False,
    "review found a conflicting later TCD-023 disposition/admission")

# Aggregate and latest post-aggregate atomic authority.
req(rg05f["work_unit"] == "ANIMO-RG05F", "pinned aggregate is not RG05F")
req(rg05f["work_status"]["qualified"] is True and rg05f["work_status"]["work_unit_complete"] is True,
    "RG05F is not qualified complete")
req(rg05f["batch"]["normal_cadence"] == "3_TO_5_NEW_ATOMIC_ADMISSIONS", "RG05F batching cadence drift")
req(rg05f["aggregate_state"]["admitted_tcds"] == ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015", "TCD-027", "TCD-041"],
    "RG05F admitted-TCD baseline drift")
req(b3d15["work_unit"] == "ANIMO-B3D15" and b3d15["target"] == "TCD-030", "latest sibling atomic admission drift")
req(b3d15["status"] == EXPECTED_DECISION and b3d15["machine_validated"] is True,
    "B3D15 is not qualified machine-validated")
req(b3d15["post_rg05f_atomic_admission_ordinal"] == 1, "B3D15 post-RG05F ordinal drift")
req(b3d15["central_integration_pending"] is True, "B3D15 unexpectedly integrated centrally")

# Claim continuity and authority snapshot.
req(disp["claim"] == EXPECTED_CLAIM and adm["atomic_claim"] == EXPECTED_CLAIM, "atomic claim drift")
req(disp["starting_review_handoff"] == f"ANIMO-B3B05R@{REVIEW_HEAD}", "disposition review head drift")
req(disp["readiness_authority"] == f"ANIMO-B3B05@{READINESS_HEAD}", "disposition readiness head drift")
req(disp["authority_snapshot"]["aggregate_central_regie"] == f"ANIMO-RG05F@{RG05F_HEAD}", "disposition aggregate authority drift")
req(disp["authority_snapshot"]["latest_post_aggregate_atomic_admission"] == f"ANIMO-B3D15@{B3D15_HEAD}", "latest atomic admission pin drift")
req(adm["authorities"]["aggregate_central_regie"] == f"ANIMO-RG05F@{RG05F_HEAD}", "admission aggregate authority drift")
req(adm["authorities"]["latest_pre_b3d16_atomic_admission"] == f"ANIMO-B3D15@{B3D15_HEAD}", "admission predecessor pin drift")
req(adm["authorities"]["independent_review"] == f"ANIMO-B3B05R@{REVIEW_HEAD}", "admission review authority drift")

# GOV04 strict Tier-B route.
req(disp["gov04"]["principle"] == "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS", "GOV04 principle drift")
req(disp["gov04"]["risk_tier"] == "B" and disp["gov04"]["risk_class"] == EXPECTED_RISK, "disposition risk route drift")
req(disp["gov04"]["tier_a_available"] is False, "Tier A incorrectly available")
req(disp["gov04"]["tier_c_trigger_applicable"] is False and disp["gov04"]["tier_d_trigger_applicable"] is False,
    "Tier C/D trigger became applicable")
for key in [
    "persistent_state_ownership_change", "initialization_semantics_change", "restart_or_checkpoint_semantics_change",
    "state_reconstruction_required", "runtime_architecture_change", "branch_threshold_change",
    "numerical_policy_change", "solver_or_tolerance_change", "exact_zero_policy_change", "ambiguous_domain_contract"
]:
    req(disp["gov04"][key] is False, f"stronger risk trigger or wider scope present: {key}")
req(review["risk"]["GOV04_tier"] == "B" and review["risk"]["qualification_class"] == EXPECTED_RISK,
    "independent review no longer supports Tier B")
req(review["risk"]["tier_C_or_D_trigger_found"] is False, "independent review found Tier C/D trigger")
req(adm["risk"]["tier"] == "B" and adm["risk"]["class"] == EXPECTED_RISK, "admission risk route drift")

# Frozen source and exact scientific identity.
pins = {
    "source_zip_sha256": "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
    "testbank_zip_sha256": "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
    "resp_miner_sha256": "938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106"
}
req(review["frozen_B0"]["source_archive_sha256"] == pins["source_zip_sha256"], "review source archive pin drift")
req(review["frozen_B0"]["testbank_archive_sha256"] == pins["testbank_zip_sha256"], "review testbank pin drift")
req(review["frozen_B0"]["source_member_sha256"] == pins["resp_miner_sha256"], "review resp_miner pin drift")
req(review["frozen_B0"]["source_member_size_bytes"] == 62997, "review resp_miner size drift")
for key, value in pins.items():
    req(disp["evidence_pins"][key] == value, f"disposition evidence pin drift: {key}")
    req(adm["evidence"][key] == value, f"admission evidence pin drift: {key}")

sc = disp["scientific_contract"]
req(sc["routine"] == "Resp_miner" and sc["case"] == "Case(2)", "source seam drift")
req(sc["required_identity"] == "Transfop(19)+Transfop(20)=Transfop(17)", "required identity drift")
req(sc["candidate_identity_exact"] is True and sc["scientific_numeric_tolerance_required"] is False,
    "candidate identity is not exact")
req(sc["intended_N_to_P_conversion_at_atomic_seam"] is False, "unexpected N-to-P conversion introduced")
req(review["scientific_findings"]["candidate_identity_exact"] is True, "review did not confirm exact identity")
req(review["scientific_findings"]["intended_N_to_P_conversion_at_atomic_seam_found"] is False,
    "review found an intended N-to-P conversion")

# Natural activation, causal mismatch, downstream effect, and regression surface.
req(disp["natural_activation"]["unique_actual_nonpotential_case2_events"] == 9658, "activation count drift")
req(disp["natural_activation"]["affected_layers"] == [17, 18, 19, 20, 21, 22, 23], "affected-layer drift")
req(review["natural_activation"]["unique_actual_nonpotential_case2_events"] == 9658, "review activation count drift")
req(disp["causality"]["legacy_accumulated_local_P_mismatch_kg_m_minus_2"] == 1.0806894643265774e-11,
    "causal mismatch drift")
req(disp["causality"]["cross_species_parent_selection_causally_explains_mismatch"] is True,
    "cross-species selector no longer explains mismatch")
req(disp["causality"]["candidate_removes_TCD023_causal_contribution"] is True,
    "candidate causal closure missing")
req(disp["causality"]["whole_case_P_residual_exact_zero_claimed"] is False, "whole-case P closure overclaimed")
req(disp["downstream_effect"]["genuinely_nonzero"] is True, "downstream effect lost")
req(disp["downstream_effect"]["tier_A_accounting_only_route_available"] is False, "Tier A incorrectly reopened")
req(disp["downstream_effect"]["max_abs_delta_Tomnpo_kg_m_minus_2_per_step"] == 1.0228664519933892e-14,
    "Tomnpo delta drift")
req(disp["downstream_effect"]["max_abs_delta_Rekopo_kg_m_minus_3_d_minus_1"] == 9.327856586446364e-15,
    "Rekopo delta drift")
req(disp["regression_surface"]["case_count"] == 8, "regression case count drift")
req(disp["regression_surface"]["other_seven_normalized_scientific_differences"] == 0, "unexpected regression difference")
req(disp["regression_surface"]["missing_outputs"] == [] and disp["regression_surface"]["extra_outputs"] == [] and disp["regression_surface"]["unexpected_differences"] == [],
    "regression surface contains unexplained output changes")
req(disp["regression_surface"]["scientific_numeric_tolerance_used"] is False, "scientific tolerance introduced")

# Historical uncertainty and non-composition.
req(review["historical_behavior"]["qualified_B2_found"] is False, "qualified B2 unexpectedly appeared in reviewed evidence")
req(review["historical_behavior"]["revision_53_behavior"] == "UNKNOWN", "review historical behavior overclaimed")
req(disp["historical_route"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "disposition historical behavior overclaimed")
req(disp["historical_route"]["historical_fidelity_claimed"] is False, "disposition claims historical fidelity")
req(adm["historical_uncertainty"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "admission historical behavior overclaimed")
req(adm["historical_uncertainty"]["historical_fidelity_claimed"] is False, "admission claims historical fidelity")
for key in ["TCD-019", "TCD-024", "TCD-027", "TCD-030", "other_stable_DOM_or_P_corrections"]:
    req(disp["non_composition"][key] is False, f"disposition composes {key}")
    req(adm["composition"][key] is False, f"admission composes {key}")

# Formal decision and hard boundaries.
req(disp["formal_disposition"] == "QUALIFY_FOR_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B",
    "formal disposition mismatch")
req(adm["decision"] == EXPECTED_DECISION and adm["admitted"] is True, "atomic admission decision mismatch")
req(adm["independent_second_line_gate"]["gate"] == "PASS", "independent review gate not passed in admission")
for key in ["production_source_modified", "frozen_B0_modified", "composition_performed", "b4_opened", "production_migration_opened", "canonical_tcd_register_modified", "central_rg05_updated"]:
    req(disp[key] is False, f"forbidden disposition side effect: {key}")
for key, value in adm["authorization"].items():
    req(value is False, f"forbidden admission authorization: {key}")
req(adm["central_integration"]["included_in_current_rg05f"] is False, "TCD-023 falsely included in RG05F")
req(adm["central_integration"]["post_rg05f_atomic_admission_ordinal"] == 2, "unexpected post-RG05F ordinal")
req(adm["central_integration"]["normal_batch_cadence"] == "3_TO_5_NEW_ATOMIC_ADMISSIONS", "aggregate cadence mismatch")
req(adm["central_integration"]["early_trigger_identified"] is False, "unjustified early aggregate trigger introduced")
req(adm["central_integration"]["required_later"] is True, "central integration incorrectly closed")

# Status supports both pre-validation and validated closeout states.
req(status["work_unit"] == "ANIMO-B3D16" and status["target"] == "TCD-023", "status identity drift")
req(status["formal_decision"] == EXPECTED_DECISION, "status decision drift")
req(status["starting_review_head"] == REVIEW_HEAD and status["readiness_head"] == READINESS_HEAD, "status evidence head drift")
req(status["aggregate_authority_at_start"] == f"ANIMO-RG05F@{RG05F_HEAD}", "status aggregate pin drift")
req(status["latest_post_rg05f_atomic_admission"] == f"ANIMO-B3D15@{B3D15_HEAD}", "status B3D15 pin drift")
req(status["post_rg05f_atomic_admission_ordinal"] == 2, "status post-RG05F ordinal drift")
req(status["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty drift")
for key in ["production_source_modified", "frozen_B0_modified", "composition_performed", "tcd019_composed", "tcd024_composed", "tcd027_composed", "tcd030_composed", "b4_opened", "production_migration_opened", "canonical_tcd_register_modified", "central_rg05_updated"]:
    req(status[key] is False, f"status records forbidden side effect: {key}")
req(status["central_integration_pending"] is True, "status falsely closes aggregate integration")

if status["machine_validated"]:
    req(status["status"] == EXPECTED_DECISION, "validated status does not carry final decision")
    req(status["ci_validation"]["conclusion"] == "success", "validated status lacks successful CI")
    req(status["ci_validation"]["validator"] == "PASS" and status["ci_validation"]["scope_guard"] == "PASS",
        "validated status lacks validator/scope PASS")
    req(adm["validation_state"] == "VALIDATED_BY_B3D16_MACHINE_GATE", "validated admission state drift")
else:
    req(status["status"] == "ATOMIC_B3_ADMISSION_PACKAGE_PERSISTED_PENDING_MACHINE_VALIDATION",
        "unexpected pre-validation status")
    req(adm["validation_state"] == "PENDING_B3D16_MACHINE_GATE", "pre-validation admission state drift")

print("B3D16 PASS: TCD-023 Tier-B atomic admission package is review-pinned, scientifically bounded, historically uncertainty-bounded, non-composed, and production-closed.")
