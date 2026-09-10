#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "integration/animo-b3/TCD027_INDEPENDENT_SECOND_LINE_REVIEW.json"
REPORT = ROOT / "docs/b3/TCD027_INDEPENDENT_SECOND_LINE_REVIEW.md"

HANDOFF = "f348d0509ddfbb60473d41a7fe25e67d8e088e7f"
B3A01 = "b2bac82512fef0fa232e759f0c68b472567c11d5"
B3D10 = "a7b11b334f8b2604d5036edc04365006800944e0"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
PREP06 = "9b1f1ea51c24fb82823290193651830dc61ea3c8"
B0_SOURCE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
B0_TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
OUTBAL_CALC = "4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981"
OUTBAL_WRITE = "cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea"
LEGACY = "Bafop(24,Ly)=Bafop(25,Ly)+Dum"
CANDIDATE = "Bafop(24,Ly)=Bafop(24,Ly)+Dum"
CHANGED = {"transfopGP.Out", "transfopRP.Out", "transfopTP.Out"}
EXPECTED_INCOMPLETE = {2, 3, 5, 20}
EXPECTED_PASS = set(range(1, 25)) - EXPECTED_INCOMPLETE


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_B3A01R: " + message)


def main():
    require(RESULT.is_file(), "missing machine-readable review result")
    require(REPORT.is_file(), "missing human-readable review report")

    data = json.loads(RESULT.read_text(encoding="utf-8"))
    report = REPORT.read_text(encoding="utf-8")

    require(data["record_id"] == "ANIMO-B3A01R-TCD027-INDEPENDENT-SECOND-LINE", "record id")
    require(data["record_version"] == 1, "record version")
    require(data["work_unit"] == "ANIMO-B3A01R", "work unit")
    require(data["tcd_ids"] == ["TCD-027"], "atomic TCD identity")
    require(data["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "Class-A scope")
    require(data["result"] in {"PASS", "FAIL", "INCOMPLETE"}, "semantic result vocabulary")
    require(data["result"] == "INCOMPLETE", "expected fail-closed result")
    require(data["review_evidence_only"] is True, "review evidence boundary")
    require(data["admitted"] is False, "must not admit TCD-027")

    scope = data["review_scope"]
    require(scope["routine"] == "Outbal_calc.for", "routine scope")
    require("slot 24 redis_EXP" in scope["channel"], "slot-24 channel scope")
    require(scope["legacy_expression"] == LEGACY, "legacy expression")
    require(scope["candidate_expression"] == CANDIDATE, "candidate expression")
    require(scope["production_physics_in_scope"] is False, "no physics scope")
    require(scope["composition_in_scope"] is False, "no composition scope")

    independence = data["independence"]
    require(independence["separate_chatgpt_context"] is True, "separate-context independence")
    require(independence["human_independence_claimed"] is False, "no human-independence claim")
    require(independence["organizational_independence_claimed"] is False, "no organizational-independence claim")
    require(independence["b3d10_authoring_source_recheck_is_supporting_only"] is True, "B3D10 support-only boundary")
    require(independence["b3d10_authoring_source_recheck_satisfies_independent_gate"] is False, "B3D10 must not satisfy review gate")

    heads = data["reviewed_heads"]
    require(heads == {
        "review_handoff": HANDOFF,
        "ANIMO-B3A01": B3A01,
        "ANIMO-B3D10": B3D10,
        "ANIMO-GOV03": GOV03,
        "ANIMO-B3Q01": B3Q01,
        "ANIMO-PREP06_evidence_head": PREP06,
    }, "exact reviewed heads")

    evidence = data["evidence_identities"]
    require(evidence["frozen_b0_source_sha256"] == B0_SOURCE, "B0 source identity")
    require(evidence["frozen_b0_testbank_sha256"] == B0_TESTBANK, "B0 testbank identity")
    require(evidence["Outbal_calc_for_sha256"] == OUTBAL_CALC, "Outbal_calc member identity")
    require(evidence["Outbal_write_for_sha256"] == OUTBAL_WRITE, "Outbal_write member identity")
    require(evidence["review_contract_blob_sha"] == "6a31e6ae33c1c12d889f6b05cba009eba5e42466", "review contract blob")
    require(evidence["PREP06_TCD027_diagnostic_blob_sha"] == "5bc14b350b1b60f870ab568d4c8a127275ca8a84", "PREP06 diagnostic blob")
    require(evidence["PREP06_source_reverification_blob_sha"] == "bd0ec232f3de269c0f4251c30761b528a8d28e65", "PREP06 source reverify blob")
    require(evidence["PREP06_transfer_ledger_blob_sha"] == "9caf62061ffbfefd28940b9ac170d6ae12b4d638", "PREP06 transfer ledger blob")
    require(evidence["GOV03_acquisition_evidence_blob_sha"] == "160eda7632235cc1558f1dde89ea4d7fd5e2e380", "GOV03 acquisition blob")
    require(evidence["GOV03_status_blob_sha"] == "b85af297731f8bd84feddaf3aa23685549129496", "GOV03 status blob")
    require(evidence["documentation_readme_blob_sha"] == "473cb61c2baa4ddf70c1d9806a2211a53b1ed08f", "documentation role blob")

    access = data["independent_source_access"]
    require(access["frozen_source_bytes_available_in_public_repository"] is False, "source bytes availability must remain explicit")
    require(access["b3d10_substitution_for_missing_source_derivative_allowed"] is False, "no B3D10 substitution")

    checks = data["checks"]
    require(len(checks) == 24, "exact 24-item review surface")
    require({item["id"] for item in checks} == set(range(1, 25)), "check ids 1..24")
    by_id = {item["id"]: item for item in checks}
    require({i for i, item in by_id.items() if item["result"] == "INCOMPLETE"} == EXPECTED_INCOMPLETE, "exact incomplete checks")
    require({i for i, item in by_id.items() if item["result"] == "PASS"} == EXPECTED_PASS, "exact pass checks")
    require(not any(item["result"] == "FAIL" for item in checks), "no contradictory-evidence FAIL was found")
    require(all(item["result"] in {"PASS", "FAIL", "INCOMPLETE"} for item in checks), "check result vocabulary")
    require("Dum" in by_id[2]["basis"] and "unavailable" in by_id[2]["basis"], "check 2 unresolved source reason")
    require("no independent source-bound extract" in by_id[3]["basis"], "check 3 unresolved source reason")
    require("P25/P26/P27" in by_id[5]["basis"], "check 5 unresolved source reason")
    require("checks 2, 3 and 5" in by_id[20]["basis"], "check 20 dependency")

    diagnostic = data["diagnostic_boundary"]
    require(diagnostic["case"] == "LWKM_gras_1040.2021.2045", "natural case")
    require(diagnostic["period"] == 1997, "natural period")
    require(diagnostic["legacy_redis_EXP_kg_ha_P_approx"] == -7.0644, "legacy discriminator")
    require(diagnostic["candidate_redis_EXP_kg_ha_P"] == 0.0, "candidate discriminator")
    require(diagnostic["is_tolerance"] is False, "discriminator is not tolerance")
    require(diagnostic["is_historical_oracle"] is False, "discriminator is not historical oracle")
    require(diagnostic["common_top_level_outputs_compared"] == 58, "58 common outputs")
    require(set(diagnostic["changed_outputs"]) == CHANGED, "exact changed-output whitelist")
    required_unchanged = {
        "physical state trajectory", "process flux trajectory", "total organic-P balance",
        "total mass balance", "redis_OP", "redis_DOP", "redis_HUP",
        "ordinary non-reporting outputs",
    }
    require(set(diagnostic["unchanged"]) == required_unchanged, "exact unchanged surface")

    reassessment = data["b3q01_reassessment"]
    require(reassessment["historical_uncertainty_route_live"] is True, "historical uncertainty route live")
    require(reassessment["GOV03_acquisition_closure_sufficient_for_route_eligibility"] is True, "GOV03 route eligibility")
    require(reassessment["historical_behaviour"] == "UNKNOWN", "historical behaviour unknown")
    require(reassessment["qualified_B2_available"] is False, "no B2")
    require(reassessment["independent_second_line_fully_closed"] is False, "review not fully closed")
    require(reassessment["admission_conclusion"] == "NOT_EVALUATED_OR_PERFORMED_BY_THIS_REVIEW", "no admission conclusion")

    uncertainty = "\n".join(data["residual_uncertainties"])
    for token in ["Dum", "Outbal_write.for", "slot-25", "UNKNOWN", "B0 retention"]:
        require(token in uncertainty, "residual uncertainty token: " + token)

    boundaries = data["hard_boundaries"]
    for key, value in boundaries.items():
        require(value is False, "hard boundary must remain false: " + key)

    for token in [
        "Semantic result: `INCOMPLETE`",
        "B3D10 authoring-context source recheck was treated as supporting evidence only",
        "The correct semantic result is therefore `INCOMPLETE`, not `FAIL`",
        "Historical revision-53 behaviour remains `UNKNOWN`",
        "TCD-027 is not admitted",
        "No production patch is authorized",
    ]:
        require(token in report, "report boundary: " + token)

    print("PASS_B3A01R_TCD027_INDEPENDENT_REVIEW_INCOMPLETE")


if __name__ == "__main__":
    main()
