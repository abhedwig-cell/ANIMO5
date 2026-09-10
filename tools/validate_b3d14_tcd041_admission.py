#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"


def load(name):
    with (B3 / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def req(cond, msg):
    if not cond:
        raise SystemExit(f"B3D14 FAIL_CLOSED: {msg}")

review = load("TCD041_INDEPENDENT_SECOND_LINE_REVIEW.json")
handoff = load("TCD041_INDEPENDENT_SECOND_LINE_REVIEW_HANDOFF.json")
disp = load("TCD041_GOV04_TIER_B_FORMAL_DISPOSITION.json")
adm = load("TCD041_B3_ADMISSION_CLOSEOUT.json")
status = load("ANIMO-B3D14_STATUS.json")

EXPECTED_REVIEW_HEAD = "3587c7a94a992f3779034c4c1e5f4134192d54f3"
EXPECTED_READINESS_HEAD = "6523c8a4dbf7a742b61e0c236af0ef5093b534aa"
EXPECTED_RG = "ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73"
EXPECTED_PREV = "ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4"
EXPECTED_DECISION = "QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B"
EXPECTED_REVIEW_OUTCOME = "PASS_TIER_B_READY_FOR_POST_REVIEW_DISPOSITION"
EXPECTED_RISK = "B_LOCAL_ALGEBRA_INDEX_SPECIES"
EXPECTED_CLAIM = "Define the revision-53 GHG lower external advective air-boundary coordinate Flair(Nl+1) as the already source-implied closed-boundary value zero before its same-call first use."
PINS = {
    "source_zip_sha256": "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
    "testbank_zip_sha256": "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
    "ghgasses_sha256": "4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93",
    "ghgtransport_sha256": "d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6",
    "ghgtranssub_sha256": "48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c",
}

# Separate review gate and provenance.
req(review["work_unit"] == "ANIMO-B3B07R", "wrong independent review workunit")
req(review["independence"]["separate_chatgpt_context"] is True, "review is not separate-context")
req(review["independence"]["authoring_conclusion_inherited"] is False, "review inherited authoring conclusion")
req(review["starting_handoff"]["expected_head"] == EXPECTED_READINESS_HEAD, "review expected readiness head drift")
req(review["starting_handoff"]["live_verified_head_before_write"] == EXPECTED_READINESS_HEAD, "review did not verify readiness head")
req(review["starting_handoff"]["match"] is True, "review readiness head mismatch")
req(review["outcome"] == EXPECTED_REVIEW_OUTCOME, "independent review did not pass Tier B")
req(review["admission_decision_performed"] is False, "review improperly performed admission")
req(handoff["review_outcome"] == EXPECTED_REVIEW_OUTCOME, "review handoff outcome mismatch")
req(handoff["work_status"]["second_line_decision_complete"] is True, "review not complete")
req(handoff["work_status"]["evidence_pinned"] is True, "review evidence not pinned")
req(handoff["permitted_next_step"]["may_combine_disposition_and_atomic_admission_closeout_under_gov04_tier_b"] is True,
    "combined Tier-B disposition/admission not permitted by review handoff")

# Claim and immutable authorities.
req(disp["claim"] == EXPECTED_CLAIM and adm["atomic_claim"] == EXPECTED_CLAIM, "atomic claim drift")
req(disp["starting_review_handoff"] == f"ANIMO-B3B07R@{EXPECTED_REVIEW_HEAD}", "disposition review head drift")
req(adm["authorities"]["independent_review"] == f"ANIMO-B3B07R@{EXPECTED_REVIEW_HEAD}", "admission review head drift")
req(disp["readiness_authority"] == f"ANIMO-B3B07@{EXPECTED_READINESS_HEAD}", "readiness authority drift")
req(disp["authority_snapshot"]["aggregate_central_regie"] == EXPECTED_RG, "aggregate authority drift")
req(adm["authorities"]["aggregate_central_regie"] == EXPECTED_RG, "admission aggregate authority drift")
req(adm["authorities"]["latest_pre_b3d14_atomic_admission"] == EXPECTED_PREV, "predecessor admission drift")

# GOV04 strict Tier-B route. Any Tier-C trigger invalidates this workunit.
req(disp["gov04"]["principle"] == "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS", "GOV04 principle drift")
req(disp["gov04"]["risk_tier"] == "B", "risk tier is not B")
req(disp["gov04"]["risk_class"] == EXPECTED_RISK, "risk class drift")
req(disp["gov04"]["tier_c_trigger_applicable"] is False, "Tier-C trigger became applicable")
req(review["gov04_risk_test"]["result"] == "GOV04_TIER_B__B_LOCAL_ALGEBRA_INDEX_SPECIES", "review Tier-B result mismatch")
req(not any(review["gov04_risk_test"]["tier_c_triggers"].values()), "review contains an applicable Tier-C trigger")
req(adm["risk"]["tier"] == "B" and adm["risk"]["class"] == EXPECTED_RISK, "admission risk route drift")
req(adm["risk"]["tier_c_trigger_applicable"] is False, "admission records a Tier-C trigger")

# Scientific identity and first-use defect.
sc = disp["scientific_contract"]
req(sc["coordinate"] == "Flair(Nl+1)", "wrong boundary coordinate")
req(sc["required_boundary_value"] == 0.0, "closed lower boundary value is not zero")
req(sc["persistent_model_state"] is False and sc["cross_call_state"] is False and sc["checkpoint_or_restart_coordinate"] is False,
    "boundary coordinate acquired persistent/restart semantics")
req(disp["causal_defect"]["result"] == "UNCONDITIONAL_TASK1_FIRST_READ_WITHOUT_SOURCE_ASSIGNMENT_FOR_NL_GE_1",
    "causal first-read defect drift")
req(adm["scientific_identity"]["required_value"] == 0.0, "admission boundary value drift")
req(adm["scientific_identity"]["persistent_state"] is False, "admission promotes coordinate to persistent state")

# Evidence pin equality across review, disposition and admission.
for key, value in PINS.items():
    req(review["evidence_reuse"][key] == value, f"review pin drift: {key}")
    req(disp["evidence_pins"][key] == value, f"disposition pin drift: {key}")
    req(adm["evidence"][key] == value, f"admission pin drift: {key}")

# Historical uncertainty must not be laundered into B2.
req(disp["activation"]["synthetic_evidence_class"] == "B1_CAUSAL_AND_COVERAGE_ONLY_NOT_B2", "synthetic evidence promoted")
req(adm["evidence"]["synthetic_activation_is_b2"] is False, "synthetic evidence promoted to B2")
req(disp["historical_route"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical behaviour overclaimed")
req(adm["historical_uncertainty"]["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "admission historical behaviour overclaimed")
req(disp["historical_route"]["historical_fidelity_claimed"] is False, "historical fidelity claimed")
req(adm["historical_uncertainty"]["historical_fidelity_claimed"] is False, "admission historical fidelity claimed")

# Atomicity, bounded conservation and non-composition.
req(disp["tcd032_037"]["dependency_required"] is False, "hidden TCD-032..037 dependency")
req(disp["tcd032_037"]["composition_required"] is False, "TCD-032..037 composition required")
req(adm["bounded_claims"]["tcd032_037_dependency"] is False, "admission introduces TCD-032..037 dependency")
req(adm["bounded_claims"]["tcd032_037_composition"] is False, "admission composes TCD-032..037")
req(disp["conservation"]["full_ghg_carbon_or_nitrogen_ledger_closure_claimed"] is False, "full GHG ledger closure overclaimed")
req(adm["bounded_claims"]["whole_ghg_equivalence_claimed"] is False, "whole-GHG equivalence overclaimed")

# Formal decision and hard boundaries.
req(disp["formal_disposition"] == "QUALIFY_FOR_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B", "formal disposition mismatch")
req(adm["decision"] == EXPECTED_DECISION and adm["admitted"] is True, "atomic admission decision mismatch")
for key in ["production_source_modified", "composition_performed", "b4_opened", "production_migration_opened", "canonical_tcd_register_modified", "central_rg05_updated"]:
    req(disp[key] is False, f"forbidden disposition side effect: {key}")
for key, value in adm["authorization"].items():
    req(value is False, f"forbidden admission authorization: {key}")
req(adm["central_integration"]["included_in_current_rg05e"] is False, "TCD-041 falsely included in RG05E")
req(adm["central_integration"]["required_next"] is True, "central-regie integration not left pending")

req(status["formal_decision"] == EXPECTED_DECISION, "status decision mismatch")
req(status["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty drift")
for key in ["production_source_modified", "composition_performed", "b4_opened", "production_migration_opened", "canonical_tcd_register_modified", "central_rg05_updated"]:
    req(status[key] is False, f"status records forbidden side effect: {key}")

print("B3D14 PASS: TCD-041 Tier-B atomic admission is internally consistent, evidence-pinned, historically uncertainty-bounded, and production-closed.")
