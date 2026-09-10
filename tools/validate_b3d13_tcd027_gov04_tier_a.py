#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAIVER = ROOT / "integration/animo-b3/TCD027_GOV04_TIER_A_WAIVER_AUDIT.json"
ADMISSION = ROOT / "integration/animo-b3/TCD027_B3_ADMISSION_CLOSEOUT_GOV04.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D13_STATUS.json"

GOV04 = "ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc"
RG05E = "ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73"
B3A01 = "ANIMO-B3A01@b2bac82512fef0fa232e759f0c68b472567c11d5"
B3D10 = "ANIMO-B3D10@a7b11b334f8b2604d5036edc04365006800944e0"
GOV03 = "ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c"
B3A01E = "ANIMO-B3A01E@5232ef5fa6daafa2296401b19fd9e866a34152bd"
B3A01R = "ANIMO-B3A01R@510c9313926457cd9bfd8e71a551255297bdfbb3"
R2 = "ANIMO-B3A01R2@428e0212082bbf80a2b07683d5b58588e7645095"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
CALC_SHA = "4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981"
WRITE_SHA = "cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea"
DECISION = "ADMIT_TCD027_ATOMIC_CLASS_A_REPORTING_CORRECTION_UNDER_GOV04_TIER_A_WAIVER_WITH_HISTORICAL_UNCERTAINTY"
WAIVER_DECISION = "GOV04_TIER_A_WAIVER_ALL_CONDITIONS_PASS"

EXPECTED_WAIVER_CONDITIONS = {
    "EXACT_SOURCE_SEAM",
    "UNAMBIGUOUS_PHYSICAL_AND_ACCOUNTING_OWNERSHIP",
    "ATOMICITY",
    "EXACT_CONSERVATION_OR_ACCOUNTING_IDENTITY",
    "EXPECTED_DIFFERENCE_PREDECLARED",
    "PHYSICAL_STATE_NON_INTERFERENCE",
    "PROCESS_FLUX_NON_INTERFERENCE",
    "NO_NUMERICAL_POLICY_CHANGE",
    "NO_SOLVER_OR_TOLERANCE_CHANGE",
    "NO_RESTART_INITIALIZATION_OR_STATE_SEMANTIC_CHANGE",
    "NO_COMPOSITION",
    "NO_UNRESOLVED_SCIENTIFIC_OR_SOURCE_MEANING_AMBIGUITY",
    "REPRODUCIBLE_VALIDATOR",
    "SCOPE_GUARD",
    "NATURAL_OR_QUALIFIED_SYNTHETIC_ACTIVATION",
    "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2",
    "GOV03_ROUTE_CONDITIONS_RETAINED_WHEN_APPLICABLE",
    "NO_PRODUCTION_OR_B4_OR_CANONICAL_REGISTER_CHANGE",
}
EXPECTED_REUSE_CONDITIONS = {
    "EXACT_SAME_SOURCE_AND_TESTCASE_IDENTITY",
    "CLAIM_SCOPE_UNCHANGED_AND_NOT_WIDENED",
    "EVIDENCE_ARTIFACT_IMMUTABLE_AND_PINNED",
    "PROVENANCE_FULLY_PINNED",
    "NO_SUPERSEDING_OR_CONTRADICTORY_EVIDENCE",
}
EXPECTED_CHANGED = ["transfopGP.Out", "transfopRP.Out", "transfopTP.Out"]


def load(path):
    if not path.exists():
        raise SystemExit(f"MISSING: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require(cond, msg):
    if not cond:
        raise SystemExit(f"FAIL_B3D13: {msg}")


def main():
    waiver = load(WAIVER)
    adm = load(ADMISSION)
    status = load(STATUS)

    require(waiver["workunit"] == "ANIMO-B3D13", "wrong waiver workunit")
    require(waiver["target"] == "TCD-027", "wrong waiver target")
    require(waiver["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "wrong qualification class")
    require(waiver["risk_tier"] == "A", "risk tier is not A")
    require(waiver["policy_authority"] == GOV04, "GOV04 head mismatch")
    require(waiver["central_regie_at_start"] == RG05E, "RG05E head mismatch")
    require(waiver["readiness_authority"] == B3A01, "B3A01 head mismatch")
    require(waiver["route_authority"] == B3D10, "B3D10 head mismatch")
    require(waiver["historical_route_authority"] == GOV03, "GOV03 head mismatch")
    require(waiver["evidence_remediation_authority"] == B3A01E, "B3A01E head mismatch")
    require(waiver["prior_review_authority"] == B3A01R, "B3A01R head mismatch")
    require(waiver["prior_review_semantic_result_retained"] == "INCOMPLETE", "prior review must remain INCOMPLETE")
    require(waiver["parked_r2_handoff"] == R2, "R2 handoff mismatch")

    fi = waiver["frozen_identity"]
    require(fi["source_archive_sha256"] == SOURCE_SHA, "source B0 mismatch")
    require(fi["testbank_sha256"] == TESTBANK_SHA, "testbank B0 mismatch")
    require(fi["outbal_calc_member_sha256"] == CALC_SHA, "Outbal_calc member mismatch")
    require(fi["outbal_write_member_sha256"] == WRITE_SHA, "Outbal_write member mismatch")

    claim = waiver["atomic_claim"]
    require(claim["legacy"] == "Bafop(24,Ly)=bafop(25,Ly) + Dum", "legacy seam mismatch")
    require(claim["candidate"] == "Bafop(24,Ly)=Bafop(24,Ly)+Dum", "candidate seam mismatch")
    require(claim["local_increment"] == "Dum = Adexpl(I,Ln)*Pofrex*Z", "Dum construction mismatch")
    for key in ("physical_state_change", "process_flux_change", "numerical_policy_change", "restart_or_initialization_semantic_change", "composition"):
        require(claim[key] is False, f"scope creep flag {key}")

    reuse = waiver["verify_and_reuse"]
    require(reuse["mode"] == "VERIFY_AND_REUSE", "reuse mode mismatch")
    require(set(reuse["conditions"]) == EXPECTED_REUSE_CONDITIONS, "reuse condition set mismatch")
    require(all(v == "PASS" for v in reuse["conditions"].values()), "not all reuse conditions pass")
    require(reuse["prior_review_incomplete_items"] == [2, 3, 5, 20], "prior incomplete item set changed")
    require(set(reuse["remediation_closure"]) == {
        "2_LOCAL_DUM_AND_SEAM", "3_OUTBAL_WRITE_SLOT_MAPPING", "5_P_SLOT25_26_27_SELF_ACCUMULATORS", "20_B3Q01_ROUTE_SUFFICIENCY"
    }, "remediation closure set mismatch")
    require(all(v.startswith("PASS_") for v in reuse["remediation_closure"].values()), "remediation closure not all PASS")

    sem = waiver["source_semantics_reverified"]
    require([sem["slot_24_label"], sem["slot_25_label"], sem["slot_26_label"], sem["slot_27_label"]] == ["redis_EXP", "redis_OP", "redis_DOP", "redis_HUP"], "slot mapping mismatch")
    for key in ("slot_25_self_accumulates", "slot_26_self_accumulates", "slot_27_self_accumulates", "organic_matter_slot24_analogue_self_accumulates", "organic_n_slot24_analogue_self_accumulates", "cross_slot_24_from_25_is_unique_structural_defect"):
        require(sem[key] is True, f"source semantic condition failed: {key}")
    require(sem["unresolved_source_meaning_ambiguity"] is False, "source ambiguity remains")

    ni = waiver["activation_and_non_interference"]
    require(ni["natural_case"] == "LWKM_gras_1040.2021.2045" and ni["period"] == 1997, "natural activation mismatch")
    require(ni["changed_outputs"] == EXPECTED_CHANGED, "changed-output whitelist mismatch")
    require(ni["common_top_level_outputs_compared"] == 58, "comparison count mismatch")
    for key in ("physical_state_trajectory_unchanged", "process_flux_trajectory_unchanged", "total_organic_P_balance_unchanged", "total_mass_balance_unchanged", "redis_OP_unchanged", "redis_DOP_unchanged", "redis_HUP_unchanged", "ordinary_non_reporting_outputs_unchanged"):
        require(ni[key] is True, f"non-interference failed: {key}")
    require(ni["numeric_acceptance_tolerance_used"] is False, "numeric tolerance introduced")

    wc = waiver["tier_a_waiver_conditions"]
    require(set(wc) == EXPECTED_WAIVER_CONDITIONS, "Tier-A waiver condition set mismatch")
    require(all(v == "PASS" for v in wc.values()), "not all Tier-A waiver conditions pass")
    require(waiver["waiver_decision"] == WAIVER_DECISION, "waiver decision mismatch")
    require(waiver["independent_second_line_required_for_this_admission"] is False, "independent review incorrectly required")
    require(waiver["independent_second_line_performed_by_b3d13"] is False, "B3D13 falsely claims independent review")
    require(waiver["historical_behaviour"] == "UNKNOWN", "historical behaviour must remain UNKNOWN")
    require(waiver["historical_fidelity_claimed"] is False, "historical fidelity claimed")
    require(waiver["scope_escalation_triggered"] is False, "Tier-A escalation triggered")

    require(adm["record_id"] == "B3D13-TCD027-GOV04-TIER-A-ADMISSION", "record id mismatch")
    require(adm["tcd_ids"] == ["TCD-027"], "admission target mismatch")
    require(adm["atomicity"] == "ATOMIC", "not atomic")
    require(adm["qualification_class"] == "A", "B3Q01 class mismatch")
    require(adm["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "route mismatch")
    require(adm["disposition"] == "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY", "disposition mismatch")
    require(adm["identities"]["b0"]["source_sha256"] == SOURCE_SHA, "admission source hash mismatch")
    require(adm["identities"]["b0"]["testbank_sha256"] == TESTBANK_SHA, "admission testbank hash mismatch")
    require(adm["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 status mismatch")
    require(adm["identities"]["b2"]["acquisition_effort_ref"] == GOV03, "B2 acquisition ref mismatch")

    ir = adm["evidence"]["independent_review"]
    require(ir["status"] == "COMPLETE", "GOV04 compatibility independent-review status mismatch")
    require(ir["result"] == "NOT_REVIEWED", "independent review result must be NOT_REVIEWED")
    require(ir["independent_from_correction_authoring"] is False, "false independence claim")

    gates = adm["gates"]
    required_gate_names = {"b0_identity", "b1_evidence", "b2_route", "theory", "causal", "conservation", "expected_difference", "non_interference", "coverage", "independent_review", "residual_uncertainty", "class_specific", "composition_if_applicable"}
    require(set(gates) == required_gate_names, "B3Q01 gate set mismatch")
    require(all(g["status"] == "PASS" for g in gates.values()), "not all B3Q01 gates PASS")
    require(gates["independent_review"]["applicability"] == "NOT_APPLICABLE", "independent review applicability must be NOT_APPLICABLE")
    require(gates["independent_review"]["justification"] == WAIVER_DECISION, "independent review waiver justification mismatch")
    require(gates["composition_if_applicable"]["applicability"] == "NOT_APPLICABLE", "composition gate must be not applicable")

    require(adm["evidence"]["expected_difference"]["changed_states"] == [], "state change declared")
    require(adm["evidence"]["expected_difference"]["changed_fluxes"] == [], "flux change declared")
    require(adm["evidence"]["expected_difference"]["changed_ledgers_or_reports"] == [
        "detailed organic-P redis_EXP reporting in transfopGP.Out",
        "detailed organic-P redis_EXP reporting in transfopRP.Out",
        "detailed organic-P redis_EXP reporting in transfopTP.Out",
    ], "expected difference surface mismatch")

    require(adm["composition"] == {"is_composition": False, "component_record_ids": []}, "composition present")
    dec = adm["admission_decision"]
    require(dec["admitted"] is True, "TCD-027 not admitted")
    require(dec["decision"] == DECISION, "admission decision mismatch")

    residual = " ".join(adm["residual_uncertainty"])
    require("UNKNOWN" in residual, "historical UNKNOWN missing")
    require("INCOMPLETE" in residual, "prior INCOMPLETE review history missing")
    require("production" in residual.lower(), "production boundary missing")

    require(status["workunit"] == "ANIMO-B3D13", "status workunit mismatch")
    require(status["target"] == "TCD-027", "status target mismatch")
    require(status["decision"] in {"PENDING_FAIL_CLOSED_VALIDATION", DECISION}, "unexpected status decision")
    require(status["historical_behaviour"] == "UNKNOWN", "status historical behaviour mismatch")
    require(status["production_patch_authorized"] is False, "production patch authorized")
    require(status["b4_admitted"] is False, "B4 admitted")
    require(status["composition_admitted"] is False, "composition admitted")
    require(status["central_regie_updated"] is False, "central regie updated inside atomic workunit")

    print("PASS_B3D13_TCD027_GOV04_TIER_A_ADMISSION")


if __name__ == "__main__":
    main()
