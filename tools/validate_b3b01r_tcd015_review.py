#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3B01R independent TCD-015 review.

This validator checks persistence, pins, arithmetic, evidence boundaries and review
scope. A validator PASS is not itself scientific proof and does not perform B3
admission or authorize a production correction.
"""
from __future__ import annotations

import json
from decimal import Decimal as D, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/b3/TCD015_INDEPENDENT_SECOND_LINE_REVIEW.md"
RESULT = ROOT / "integration/animo-b3/TCD015_INDEPENDENT_REVIEW_RESULT.json"
READINESS = ROOT / "integration/animo-b3/TCD015_CLASS_B_READINESS.json"
EXPECTED = ROOT / "integration/animo-b3/TCD015_EXPECTED_DIFFERENCE.json"
COVERAGE = ROOT / "integration/animo-b3/TCD015_BRANCH_COVERAGE_SUPPLEMENT.json"
SOURCE_MANIFEST = ROOT / "reference/source/source_manifest.csv"
NITROGEN = ROOT / "docs/prep01/NITROGEN_BALANCE_DIAGNOSTICS.md"
NH4 = ROOT / "docs/prep01/NH4_DRYDOWN_LEDGER_SEAM.md"
GHG = ROOT / "docs/prep01/GHG_TESTCASE_PROVENANCE.md"
SYNQ = ROOT / "tools/reference/synthetic_oracles.py"
COMPARATOR = ROOT / "tools/compare_legacy_output_trees.py"
GOV03 = ROOT / "integration/animo-governance/GOV03_ACQUISITION_EVIDENCE.json"

EXPECTED_REVIEW_START = "c05486e76993d26771f62f32842508479d14fdde"
EXPECTED_B3B01 = "b982242949aecab32b9067cf7910ad75abfc2b19"
EXPECTED_B3D09 = "2a5abc00a779baaa3fb3fa28b3c051231c286132"
EXPECTED_B3D09_ADMIN = "cf3e2746351c5c75d236e1b63fb0623daa8e7372"
EXPECTED_GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_RG05D = "f3d6b9780631bd627f8bca0658a8e3878746e666"
EXPECTED_SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
EXPECTED_SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_TRANSSUB_SHA = "c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552"
EXPECTED_DISPOSITION = "PASS_TCD015_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION"
EXPECTED_INDEPENDENCE = "SEPARATE_CHATGPT_CONTEXT_ONLY_NO_ORGANIZATIONAL_OR_HUMAN_INDEPENDENCE_CLAIM"

MANDATORY_GATES = {
    "frozen_b0_identity",
    "exact_transsub_member",
    "hv_hv1_definitions",
    "second_reko_reconstruction",
    "candidate_minus_legacy_identity",
    "post_clip_control_flow",
    "nitrate_call_binding",
    "transsub_generic_scope",
    "natural_lwkm_activation",
    "local_duplicate_mass_identity",
    "bapd_batr_relation",
    "execution_only_closure",
    "annual_no3_effect",
    "causal_not_tolerance_or_history",
    "synq_o001_independence",
    "synq_o001_exact_conservation",
    "expected_difference_predeclared",
    "required_unchanged_surface",
    "eight_case_non_interference",
    "comparison_550_files",
    "volatile_only_normalization",
    "no_numerical_tolerance",
    "iflsol_1_natural",
    "iflsol_3_zero_delta",
    "iflsol_4_reachable",
    "iflsol_2_unreachable",
    "iflsol_5_unreachable",
    "no_hidden_reachable_target_mode",
    "nitrate_only_scope",
    "ghg0_boundary",
    "no_policy_redesign",
    "gov03_g6u_route",
    "historical_unknown",
    "pr21_commented_not_independent_evidence",
    "hard_boundary_no_admission",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(text: str, needle: str) -> None:
    assert needle in text, f"missing required evidence text: {needle}"


def main() -> None:
    result = load(RESULT)
    readiness = load(READINESS)
    expected = load(EXPECTED)
    coverage = load(COVERAGE)
    gov03 = load(GOV03)
    report = REPORT.read_text(encoding="utf-8")
    manifest = SOURCE_MANIFEST.read_text(encoding="utf-8")
    nitrogen = NITROGEN.read_text(encoding="utf-8")
    nh4 = NH4.read_text(encoding="utf-8")
    ghg = GHG.read_text(encoding="utf-8")
    synq = SYNQ.read_text(encoding="utf-8")
    comparator = COMPARATOR.read_text(encoding="utf-8")

    assert result["work_unit"] == "ANIMO-B3B01R"
    assert result["target_tcd"] == "TCD-015"
    assert result["class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert result["review_start_head"] == EXPECTED_REVIEW_START
    assert result["review_status"] == "COMPLETED_PASS"
    assert result["semantic_result"] == "PASS"
    assert result["disposition"] == EXPECTED_DISPOSITION
    assert result["independence_scope"] == EXPECTED_INDEPENDENCE
    assert result["overall_technical_second_line_result"] == "PASS"

    heads = result["reviewed_heads"]
    assert heads == {
        "B3B01_readiness": EXPECTED_B3B01,
        "B3D09_scientific_disposition": EXPECTED_B3D09,
        "B3D09_administrative_closeout": EXPECTED_B3D09_ADMIN,
        "GOV03": EXPECTED_GOV03,
        "B3Q01": EXPECTED_B3Q01,
        "RG05D_at_handoff": EXPECTED_RG05D,
        "SYNQ01": EXPECTED_SYNQ01,
    }

    frozen = result["frozen_identity"]
    assert frozen["source_zip_sha256"] == EXPECTED_SOURCE_SHA
    assert frozen["testbank_zip_sha256"] == EXPECTED_TESTBANK_SHA
    assert frozen["source_member"] == "ANIMO_4.1.5.53/Transsub.for"
    assert frozen["source_member_sha256"] == EXPECTED_TRANSSUB_SHA
    require(manifest, "ANIMO_4.1.5.53/Transsub.for")
    require(manifest, EXPECTED_TRANSSUB_SHA)

    atomic = result["atomic_claim"]
    assert atomic["scope"] == "NITRATE_ONLY_SECOND_NEGATIVE_CONCENTRATION_RECONSTRUCTION"
    assert atomic["candidate_minus_legacy"] == "-Avc*Hv"
    assert atomic["local_duplicated_storage_mass"] == "Avc*Hv*St*Ld"
    require(report, EXPECTED_DISPOSITION)
    require(report, "No organizational, institutional or human independence is claimed")
    require(report, "This review does not admit TCD-015")
    require(report, "Historical behavior remains `UNKNOWN`")
    require(report, "GHG-enabled downstream consequences remain unqualified")

    # Recompute the natural local identity with exact decimal arithmetic from the
    # persisted displayed event values. The tiny Reko display gap is recorded,
    # never used as an acceptance tolerance.
    getcontext().prec = 80
    mto = D("0.350588")
    mt = D("0.385095")
    st = D("10")
    ld = D("0.05")
    bapd = D("-0.00084267311478156")
    batr = D("-0.00090054430498043")
    legacy_reko = D("-0.0016853462295631")
    candidate_reko = D("-0.0018010886099609")
    hv = (mt - mto) / st
    ledger = bapd - batr
    avc = ledger / (hv * st * ld)
    predicted = -avc * hv
    observed = candidate_reko - legacy_reko
    assert hv == D("0.0034507")
    assert ledger == D("0.00005787119019887")
    assert avc * hv * st * ld == ledger
    assert observed == D("-0.0001157423803978")
    assert observed - predicted == D("-6.0E-17")
    assert ledger * D("10000") == D("0.5787119019887")
    assert D("0.2") * D("0.1") * D("2") * D("0.1") == D("0.004")

    numeric = result["independent_numeric_recheck"]
    assert D(numeric["Hv_per_day"]) == hv
    assert D(numeric["BAPD_minus_BATR_kg_m2"]) == ledger
    assert D(numeric["observed_candidate_minus_legacy_Reko"]) == observed
    assert D(numeric["display_precision_difference_observed_minus_predicted"]) == observed - predicted
    assert D(numeric["duplicated_mass_kg_ha"]) == ledger * D("10000")

    # Source-bound natural event and generic-use corroboration.
    require(nitrogen, "TITO 2312")
    require(nitrogen, "NITRATE")
    require(nitrogen, "Iflsol=1")
    require(nitrogen, "Avc*(Hv1-Hv)")
    require(nh4, "AMMONIUM")
    require(nh4, "Transsub")
    require(nh4, "Iflsol = 2")

    # Synthetic oracle must remain implementation-independent and exact.
    require(synq, "intentionally imports no ANIMO production or legacy implementation")
    require(synq, "return self.avc * self.hv * self.st * self.ld")
    require(synq, "assert n.duplicated_storage_term() == D(\"0.004\")")
    require(synq, "assert_exact_zero(n.conservative_residual(), \"TCD015 conservative residual\")")

    # Fail closed on comparator policy. No scientific number may be normalized or
    # tolerance-filtered.
    require(comparator, "Scientific numbers are never tolerance-filtered by this tool")
    for rule in (
        "file_creation_timestamp",
        "output_run_start_timestamp",
        "message_run_start_timestamp",
        "message_run_end_timestamp",
        "elapsed_cpu_seconds",
    ):
        require(comparator, rule)
    require(comparator, "diagnostic magnitude only; no acceptance tolerance is applied")

    ni = result["non_interference"]
    assert ni["natural_cases"] == 8
    assert ni["compared_files_excluding_stdout"] == 550
    assert ni["equal_raw"] + ni["equal_after_declared_volatile_normalization_only"] + ni["scientific_differences"] == 550
    assert ni["scientific_differences_outside_predeclared_surface"] == 0
    assert ni["numerical_acceptance_tolerance"] is None

    # The persisted contracts must explicitly preserve the no-tolerance and
    # nitrate-only boundaries.
    expected_text = json.dumps(expected, sort_keys=True)
    readiness_text = json.dumps(readiness, sort_keys=True)
    coverage_text = json.dumps(coverage, sort_keys=True)
    require(expected_text, "NITRATE")
    require(expected_text, "numerical_tolerance")
    require(readiness_text, "GreenHouseGasOption=0")
    require(coverage_text, "508")
    require(coverage_text, "Iflsol")
    require(coverage_text, "NITRATE")
    require(coverage_text, "structurally")

    bc = result["branch_coverage"]
    assert bc["natural_target_hits"] == 508
    assert bc["natural_non_nitrate_target_hits"] == 0
    assert bc["natural_Iflsol_1_hits"] == 486
    assert bc["natural_Iflsol_3_hits"] == 22
    assert bc["hidden_reachable_target_mode_found"] is False

    require(ghg, "GHGMais")
    require(ghg, "revision-53")
    boundaries = result["feature_and_policy_boundaries"]
    assert boundaries["nitrate_only"] is True
    assert boundaries["generic_Transsub_change_authorized"] is False
    assert boundaries["GreenHouseGasOption_0_only"] is True
    assert boundaries["GHG_enabled_downstream_qualified"] is False
    for key in (
        "clipping_policy_redesign",
        "Optneg_change",
        "Vsmall_change",
        "numerical_tolerance_change",
        "solver_change",
        "analytical_branch_policy_change",
    ):
        assert boundaries[key] is False

    route = result["historical_route"]
    assert gov03["proposed_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
    limits = gov03["evidence_strength_limits"]
    assert limits["historical_B2_artifact_obtained"] is False
    assert limits["historical_behaviour_proven"] is False
    assert limits["rebuild_promoted_to_historical_B2"] is False
    assert route["GOV03_closure"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
    assert route["G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS"
    assert route["historical_behavior"] == "UNKNOWN"
    assert route["historical_fidelity_claimed"] is False
    assert route["B2_qualified_for_target_path"] is False

    gates = result["gates"]
    assert set(gates) == MANDATORY_GATES
    assert all(value == "PASS" for value in gates.values())

    # Hard stop: an independent review PASS is not an admission or production
    # change. Any contrary persisted flag makes the validator fail.
    for key in (
        "B3_admitted",
        "corrected_legacy_admitted",
        "production_patch",
        "production_source_modified",
        "production_migration_admitted",
        "canonical_tcd_register_modified",
        "central_RG05_modified",
        "B4_performed",
        "composition_performed",
    ):
        assert result[key] is False, f"hard-boundary violation: {key}"

    print("ANIMO-B3B01R independent TCD-015 review: PASS_COMPLETED_REVIEW_NO_ADMISSION")


if __name__ == "__main__":
    main()
