#!/usr/bin/env python3
"""Fail-closed readiness validator for ANIMO-B3B05 / TCD-023.

This validator checks the persisted admission-readiness evidence only. It does
not patch production source, execute the independent second-line review, claim
historical fidelity, admit B3, start B4, or update central regie.
"""
from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path

D = Decimal
ROOT = Path(__file__).resolve().parents[1]

SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
RESP_SHA = "938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106"
BASE = "eed822037ed8d906a2ab424220597cffac9cca73"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
PREP01_EXE = "0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e"
EXPECTED_CHANGED = ["ani_pLO.Bal", "ani_pTP.Bal", "bapoLO.Out", "bapoTP.Out", "message.out"]
EXPECTED_LAYERS = [17, 18, 19, 20, 21, 22, 23]
EXPECTED_CASES = {
    "CranGrass",
    "CranMais",
    "GrassPeat",
    "LWKM_gras_1040.2021.2045",
    "Puitmijn_Cranendonck_60",
    "RuurloGrass",
    "STONE_akk_0006.2001.2015",
    "Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA",
}
LEGACY = [
    "Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)",
    "Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)",
]
CANDIDATE = [
    "Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)",
    "Transfop(20,Ln) = AsfaSDO * Transfop(17,Ln)",
]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def dec(value) -> Decimal:
    return D(str(value))


def main() -> None:
    fixture = load("integration/animo-b3/TCD023_READINESS_FIXTURE.json")
    expected = load("integration/animo-b3/TCD023_EXPECTED_DIFFERENCE.json")
    status = load("integration/animo-b3/ANIMO-B3B05_STATUS.json")
    upstream = load("integration/animo-b3/TCD023_UPSTREAM_EVIDENCE.json")
    recheck = load("integration/animo-b3/TCD023_INDEPENDENT_RECHECK.json")
    prep04 = load("integration/animo-prep/PREP04_STABLE_DOM_P_PARTITION.json")
    prep05 = load("integration/animo-prep/PREP05_CROSS_SPECIES_SYMMETRY_AUDIT.json")
    prep01 = load("integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json")
    gov03 = load("integration/animo-governance/ANIMO-GOV03_STATUS.json")

    # Workunit identity and fail-closed boundaries.
    assert status["work_unit"] == "ANIMO-B3B05"
    assert status["target_tcd"] == "TCD-023"
    assert status["readiness_qualified"] is True
    assert status["b3_admitted"] is False
    assert status["production_authorized"] is False
    assert status["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert status["GOV04_risk_tier"] == "B"
    assert status["Tier_A_waiver_used"] is False
    assert status["historical_revision_53_behaviour"] == "UNKNOWN"
    assert status["historical_fidelity_claimed"] is False
    assert status["authoring_base"] == {"authority": "ANIMO-RG05E", "head": BASE}
    assert status["authorities"]["GOV04"] == f"ANIMO-GOV04@{GOV04}"
    assert status["authorities"]["GOV03"] == f"ANIMO-GOV03@{GOV03}"
    assert status["authorities"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}"
    assert status["authorities"]["SYNQ01"] == f"ANIMO-SYNQ01@{SYNQ01}"
    assert status["atomic_candidate"]["legacy"] == LEGACY
    assert status["atomic_candidate"]["candidate"] == CANDIDATE
    assert status["atomic_candidate"]["required_identity"] == "Transfop(19)+Transfop(20)=Transfop(17)"

    scope = status["scope"]
    assert scope["TCD019"] == "EXCLUDED"
    assert scope["TCD024"] == "EXCLUDED"
    assert scope["TCD027"] == "EXCLUDED"
    assert scope["other_stable_DOM_or_P_corrections"] == "EXCLUDED"
    for key in (
        "production_source_modification",
        "frozen_B0_modification",
        "canonical_TCD_register_modification",
        "B4",
        "production_migration",
        "central_RG05_update",
    ):
        assert scope[key] is False, f"scope boundary unexpectedly true: {key}"

    required_gate_values = status["readiness_gates"]
    for key in (
        "B0_IDENTITY", "B1_CAUSAL_EVIDENCE", "ATOMICITY",
        "EXACT_CAUSAL_CODE_PATH_AND_TRIGGER", "MATHEMATICAL_OR_SPECIES_IDENTITY",
        "EXPECTED_DIFFERENCE_PREDECLARED", "BRANCH_ACTIVATION",
        "CONSERVATION_WHERE_APPLICABLE", "RESIDUAL_UNCERTAINTY_EXPLICIT",
        "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2",
        "NO_NUMERICAL_STATE_RESTART_OR_PRODUCTION_SCOPE_CREEP",
    ):
        assert required_gate_values[key] == "PASS"
    assert required_gate_values["B2_ROUTE_OR_GOV03_HISTORICAL_UNCERTAINTY_ROUTE"] == "PASS_GOV03_G6U_HISTORICAL_UNKNOWN"
    assert required_gate_values["NON_INTERFERENCE"] == "PASS_WITH_PREDECLARED_LOCAL_PROCESS_EFFECT"
    assert required_gate_values["ONE_GENUINELY_INDEPENDENT_SECOND_LINE_REVIEW"] == "PENDING_NOT_EXECUTED"

    # Immutable authority and evidence pins.
    assert upstream["immutable_authoring_base"]["head"] == BASE
    pins = upstream["pinned_authorities"]
    assert pins["risk_tier_governance"]["head"] == GOV04
    assert pins["historical_uncertainty_route"]["head"] == GOV03
    assert pins["b3_framework"]["head"] == B3Q01
    assert pins["synthetic_oracles"]["head"] == SYNQ01
    assert pins["synthetic_oracles"]["applicable_oracle_ids"] == ["SYNQ-O004", "SYNQ-O005"]
    assert pins["prep04"]["machine_blob_sha"] == "2a6086134517c1d0fa309447cd7ff14976ae9a15"
    assert pins["prep04"]["human_blob_sha"] == "142888d54a598aef2c503a78a1bcdc53f3bc08db"
    assert pins["prep05_cross_species_symmetry"]["blob_sha"] == "4eaaf156ffa4b34108407a6ecc28afedfa2b6bce"
    assert pins["canonical_tcd_register"]["aggregate_head"] == BASE
    assert pins["canonical_tcd_register"]["blob_sha"] == "e6c2dec78f718f9ffb70af8910f0ec483e676e63"
    assert pins["canonical_tcd_register"]["target_row_status"] == "OPEN"
    assert pins["canonical_tcd_register"]["target_row_classification"] == "CONFIRMED_LEGACY_CROSS_SPECIES_ALGEBRA_DEFECT_LOW_RATE_STATE_COUPLING"

    b0 = upstream["frozen_B0"]
    assert b0["source_archive_sha256"] == SOURCE_SHA
    assert b0["testbank_archive_sha256"] == TESTBANK_SHA
    assert b0["source_member_sha256"] == RESP_SHA
    assert b0["source_member_size_bytes"] == 62997
    assert b0["local_archive_recheck"] == "PASS_EXACT_ARCHIVE_AND_MEMBER_SHA256_MATCH"

    source_marker = (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text(encoding="utf-8").strip()
    testbank_marker = (ROOT / "reference/testcases/ANIMO_testbank.zip.sha256").read_text(encoding="utf-8").strip()
    assert source_marker.split()[0] == SOURCE_SHA
    assert testbank_marker.split()[0] == TESTBANK_SHA

    with (ROOT / "reference/source/source_manifest.csv").open(newline="", encoding="utf-8") as stream:
        rows = [r for r in csv.DictReader(stream) if r["path"] == "ANIMO_4.1.5.53/resp_miner.for"]
    assert len(rows) == 1
    assert rows[0]["sha256"] == RESP_SHA
    assert int(rows[0]["size_bytes"]) == 62997

    # Canonical TCD row remains OPEN and unchanged by this workunit.
    with (ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv").open(newline="", encoding="utf-8") as stream:
        tcd_rows = [r for r in csv.DictReader(stream) if r["ID"] == "TCD-023"]
    assert len(tcd_rows) == 1
    tcd = tcd_rows[0]
    assert tcd["status"] == "OPEN"
    assert tcd["classification"] == "CONFIRMED_LEGACY_CROSS_SPECIES_ALGEBRA_DEFECT_LOW_RATE_STATE_COUPLING"
    assert "Transfon17" in tcd["legacy_implementation"]
    assert "tiny process-source changes" in tcd["impact"]

    # PREP04 is B1 diagnostic input, not a historical reference.
    assert prep04["source_sha256"] == SOURCE_SHA
    assert prep04["testbank_sha256"] == TESTBANK_SHA
    assert prep04["reference_qualified"] is False
    assert prep04["finding"]["proposed_id"] == "TCD-023"
    assert prep04["finding"]["frozen_expressions"] == LEGACY
    assert prep04["finding"]["diagnostic_correction"] == CANDIDATE
    assert prep04["finding"]["classification"] == "CONFIRMED_LEGACY_CROSS_SPECIES_ALGEBRA_DEFECT_LOW_RATE_STATE_COUPLING"
    assert prep04["reachability"]["actual_nonpotential_case2_events"] == 9658
    assert prep04["reachability"]["layers"] == EXPECTED_LAYERS
    assert prep04["local_mass_evidence"]["required_identity"] == "Transfop(19)+Transfop(20)=Transfop(17)"
    assert dec(prep04["local_mass_evidence"]["baseline_accumulated_mismatch_kg_m-2_P"]) == D("1.0806894643265774e-11")
    assert prep04["state_source_sensitivity"]["state_trajectory_unchanged"] is False
    assert dec(prep04["state_source_sensitivity"]["max_abs_delta_Tomnpo_kg_m-2_per_step"]) == D("1.0228664519933892e-14")
    assert dec(prep04["state_source_sensitivity"]["max_abs_delta_Rekopo_kg_m-3_d-1"]) == D("9.327856586446364e-15")
    assert prep04["regression_surface"]["successful_completions"] == 8
    assert prep04["regression_surface"]["normalized_changed_files"] == EXPECTED_CHANGED
    assert prep04["regression_surface"]["other_seven_cases_normalized_differences"] == 0
    assert prep04["production_migration_admitted"] is False

    # Orthogonal source-structure cross-check and legitimate-coupling controls.
    assert prep05["source_zip_sha256"] == SOURCE_SHA
    assert prep05["high_confidence_statement_count"] == 2
    assert prep05["independent_new_finding_count"] == 0
    statements = prep05["high_confidence_statements"]
    assert {item["p_line"] for item in statements} == {564, 565}
    assert all(item["file"] == "resp_miner.for" for item in statements)
    assert all(item["expected_p_sibling"] == "Transfop(17,Ln)" for item in statements)
    assert all(item["mapped_discrepancy"] == "TCD-023" for item in statements)
    assert "reciprocal N/P uptake-limitation coupling" in prep05["reviewed_contextual_coupling"]["Upintg_Plant"]
    assert "explicit N/P ratio relationship" in prep05["reviewed_contextual_coupling"]["Inicalc_Pofrhu"]
    assert prep05["reference_qualified"] is False

    # Exact-decimal independent discriminator. No tolerance is used.
    inp = fixture["normalized_case2_inputs"]
    mofr = D(inp["mofr"])
    rate = D(inp["recfSDO_d_minus_1"])
    hest = D(inp["Hest_m_d"])
    nconc = D(inp["AvcoStdiorni_kg_N_m_minus_3"])
    pconc = D(inp["AvcoStdiorpo_kg_P_m_minus_3"])
    a = D(inp["AsfaSDO"])
    n17 = mofr * rate * nconc * hest
    p17 = mofr * rate * pconc * hest
    p19 = (D(1) - a) * p17
    p20 = a * p17
    legacy19 = (D(1) - a) * n17
    legacy20 = a * n17
    assert n17 == D(fixture["expected_parents"]["Transfon17_kg_N_m_minus_2"])
    assert p17 == D(fixture["expected_parents"]["Transfop17_kg_P_m_minus_2"])
    assert p19 == D(fixture["candidate_expected"]["Transfop19_kg_P_m_minus_2"])
    assert p20 == D(fixture["candidate_expected"]["Transfop20_kg_P_m_minus_2"])
    assert p19 + p20 - p17 == D(0)
    assert legacy19 == D(fixture["legacy_cross_species_expected"]["Transfop19_numeric_from_Transfon17"])
    assert legacy20 == D(fixture["legacy_cross_species_expected"]["Transfop20_numeric_from_Transfon17"])
    assert legacy19 + legacy20 - p17 == D(fixture["legacy_cross_species_expected"]["daughter_sum_minus_Transfop17_numeric"])
    assert fixture["acceptance"]["numeric_tolerance_allowed"] is False
    assert fixture["negative_controls"]["AsfaSDO_zero"]["candidate_identity_still_closes"] is True
    assert fixture["negative_controls"]["AsfaSDO_one"]["candidate_identity_still_closes"] is True
    assert fixture["negative_controls"]["equal_N_and_P_parent_numeric_values"]["expected_discriminator"] is False
    assert fixture["negative_controls"]["P_parent_zero_N_parent_nonzero"]["expected_discriminator"] is True

    # Independent authoring replay must match the natural causal surface.
    assert recheck["method"]["source_archive_sha256"] == SOURCE_SHA
    assert recheck["method"]["testbank_sha256"] == TESTBANK_SHA
    assert recheck["method"]["source_member_sha256"] == RESP_SHA
    assert recheck["independent_second_line_review"] is False
    assert recheck["build_reproducibility"]["baseline_executable_sha256"] == PREP01_EXE
    assert recheck["build_reproducibility"]["matches_pinned_PREP01_deterministic_executable_sha256"] is True
    src = recheck["independent_source_recheck"]
    assert src["case2_selector"] == "Recfhu < 1e-12 AND RecfHUSDO < 1e-12 AND recfSDO >= 1e-12"
    assert src["legacy_P_daughter_19"] == LEGACY[0]
    assert src["legacy_P_daughter_20"] == LEGACY[1]
    assert src["candidate_P_daughter_19"] == CANDIDATE[0]
    assert src["candidate_P_daughter_20"] == CANDIDATE[1]
    assert src["raw_archive_line_locations"] == {
        "Case2": 518, "Transfom17": 550, "Transfon17": 556,
        "Transfop17": 563, "legacy_P_daughter_19": 564,
        "legacy_P_daughter_20": 565, "Tomnpo": 1042, "Rekopo": 1270,
    }
    assert src["other_active_stable_DOM_P_cases_use_Transfop17_for_P_daughters"] is True
    assert src["implicit_NP_conversion_factor_at_seam_found"] is False
    assert recheck["species_identity"]["numeric_tolerance_needed_for_mathematical_identity"] is False

    natural = recheck["natural_activation_independent_replay"]
    assert natural["phosphorus_cycle_active"] is True
    assert natural["unique_time_layer_Case2_events"] == 9658
    assert natural["affected_layers"] == EXPECTED_LAYERS
    assert dec(natural["accumulated_legacy_local_P_identity_mismatch_kg_m_minus_2"]) == D("1.0806894643265774e-11")
    assert natural["matches_PREP04_activation_count"] is True
    assert natural["matches_PREP04_layers"] is True
    assert natural["matches_PREP04_mismatch_values"] is True

    downstream = recheck["downstream_unrounded_effect_independent_replay"]
    assert downstream["unique_changed_time_layer_keys"] == 9658
    assert downstream["changed_layers"] == EXPECTED_LAYERS
    assert dec(downstream["max_abs_delta_Tomnpo_kg_m_minus_2_per_step"]) == D("1.0228664519933892e-14")
    assert dec(downstream["max_abs_delta_Rekopo_kg_m_minus_3_d_minus_1"]) == D("9.327856586446364e-15")
    assert downstream["physical_or_process_effect_exactly_zero"] is False

    regression = recheck["eight_case_regression_replay"]
    assert regression["comparison_has_scientific_numeric_tolerance"] is False
    assert regression["volatile_metadata_normalization_only"] is True
    assert set(regression["cases"]) == EXPECTED_CASES
    assert all(item["successful_completion"] for item in regression["cases"].values())
    assert regression["cases"]["Puitmijn_Cranendonck_60"]["normalized_scientific_differences"] == EXPECTED_CHANGED
    assert all(
        item["normalized_scientific_differences"] == []
        for name, item in regression["cases"].items()
        if name != "Puitmijn_Cranendonck_60"
    )
    assert regression["unexpected_changed_files"] == []
    assert regression["missing_candidate_outputs"] == []
    assert regression["extra_candidate_outputs"] == []

    # Expected-difference and escalation contract is predeclared.
    assert expected["candidate_change"]["legacy"] == LEGACY
    assert expected["candidate_change"]["candidate"] == CANDIDATE
    assert expected["candidate_change"]["production_source_edit_authorized"] is False
    nat_expected = expected["natural_Puitmijn_reference_surface_from_PREP04"]
    assert nat_expected["expected_normalized_changed_files"] == EXPECTED_CHANGED
    assert nat_expected["unrounded_Tomnpo_and_Rekopo_expected_changed"] is True
    assert nat_expected["other_seven_PREP02_compatible_cases_expected_normalized_differences"] == 0
    assert expected["comparison_policy"]["scientific_numeric_tolerance"] is None
    assert expected["comparison_policy"]["rounded_output_used_as_equivalence_proof"] is False
    assert expected["comparison_policy"]["unrounded_affected_source_or_state_comparison_required"] is True
    assert expected["conservation_contract"]["whole_case_residual_zero_required"] is False
    assert expected["scope_escalation"] == {
        "state_or_restart_semantics_found": "ESCALATE_FROM_GOV04_TIER_B",
        "numerical_policy_or_solver_change_found": "ESCALATE_FROM_GOV04_TIER_B",
        "composition_with_other_TCD_found": "ESCALATE_TO_GOV04_TIER_D",
        "production_bound_change_found": "ESCALATE_TO_GOV04_TIER_D",
    }

    # GOV03 preserves historical uncertainty. PREP01 remains diagnostic only.
    assert gov03["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
    assert gov03["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS"
    assert prep01["source"]["sha256"] == SOURCE_SHA
    assert prep01["diagnostic_build"]["deterministic_executable_sha256"] == PREP01_EXE
    assert prep01["diagnostic_build"]["scientific_reference_qualified"] is False
    assert prep01["reproducibility"]["qualified_as_reference"] is False
    assert prep01["decision"] == "DIAGNOSTIC_EXECUTION_REPRODUCIBLE_FOR_8_OF_9_CASES_REFERENCE_NOT_QUALIFIED"

    # GOV04 Tier-B risk recheck: local process effect is real, but no stronger trigger exists.
    risk = recheck["risk_recheck"]
    assert risk["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert risk["GOV04_tier"] == "B"
    assert risk["Tier_A_waiver_applicable"] is False
    assert risk["Tier_C_or_D_forced_trigger_found"] is False
    for key in (
        "state_semantics_change", "restart_or_initialization_semantics_change",
        "numerical_policy_change", "solver_or_tolerance_change", "composition",
        "production_bound_change",
    ):
        assert risk[key] is False, f"unexpected GOV04 escalation trigger: {key}"

    report = (ROOT / "docs/b3/TCD023_CLASS_B_ADMISSION_READINESS.md").read_text(encoding="utf-8")
    assert "qualified as an atomic `B_LOCAL_ALGEBRA_INDEX_SPECIES`" in report
    assert "historical revision-53 behaviour = UNKNOWN" in report
    assert "exactly one genuinely independent second-line review" in report

    validation = status["validation"]
    assert validation["validator"] == "tools/validate_b3b05_tcd023.py"
    assert validation["workflow"] == ".github/workflows/animo-b3b05-tcd023-readiness.yml"
    assert validation["green_GitHub_Actions_required_before_review_handoff"] is True
    handoff = status["independent_review_handoff"]
    assert handoff["required_count"] == 1
    assert handoff["review_workunit"] == "ANIMO-B3B05R"
    assert handoff["executed_in_this_context"] is False
    assert handoff["same_authoring_context_may_sign"] is False

    print("ANIMO-B3B05 TCD-023 readiness validator: PASS")
    print("frozen B0 and resp_miner identity: PASS")
    print("species-local P partition identity: PASS_EXACT_NO_TOLERANCE")
    print("SYNQ-O004/O005 applicability pins: PASS")
    print("natural Puitmijn activation: 9658 events, layers 17..23")
    print("tiny nonzero Tomnpo/Rekopo process effect: CONFIRMED_TIER_A_EXCLUDED")
    print("eight-case expected-difference surface: PASS")
    print("GOV04 risk tier: B")
    print("historical revision-53 behaviour: UNKNOWN")
    print("independent second-line review: PENDING_NOT_EXECUTED")
    print("B3 admission performed: false")


if __name__ == "__main__":
    main()
