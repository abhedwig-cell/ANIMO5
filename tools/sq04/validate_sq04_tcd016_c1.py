#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

BASE = "58dc3c5c108ee97fd6bea107b7a9e686596617b1"
B3Q06 = "11e9bcdc6654e63f84875bf1f28dc54abe725700"
RG05O = "bc9e6ed997a078336645210ebb4d99ae976893fe"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "integration/animo-science/SQ04_TCD016_C1_EXISTING_PROCESS_REUSE_AUDIT.json"
FREEZE = ROOT / "integration/animo-science/ANIMO-SQ04_AUTHORING_FREEZE.json"
STATUS = ROOT / "integration/animo-science/ANIMO-SQ04_STATUS.json"
REVIEW = ROOT / "integration/animo-science/ANIMO-SQ04_INTERNAL_ADVERSARIAL_REVIEW.json"

ALLOWED = {
    "docs/science/TCD016_C1_EXISTING_PROCESS_REUSE_AUDIT.md",
    "integration/animo-science/SQ04_TCD016_C1_EXISTING_PROCESS_REUSE_AUDIT.json",
    "integration/animo-science/ANIMO-SQ04_AUTHORING_FREEZE.json",
    "integration/animo-science/ANIMO-SQ04_STATUS.json",
    "integration/animo-science/ANIMO-SQ04_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/sq04/validate_sq04_tcd016_c1.py",
    ".github/workflows/animo-sq04-tcd016-c1.yml",
}

EXPECTED_SOURCE = {
    "ANIMO_4.1.5.53/Addit.for": "e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d",
    "ANIMO_4.1.5.53/Input_addit.for": "83b15da4ecefb73559dc99f4f82d4fb2b21f72a35fa03bb53a2dd11b9a450989",
    "ANIMO_4.1.5.53/Outbal_calc.for": "4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981",
    "ANIMO_4.1.5.53/Rates.for": "7a1a8aee4715d85b9b7e9e172f83756e4aee8b8278386c804210ef77dc2a857a",
    "ANIMO_4.1.5.53/resp_miner.for": "938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106",
    "ANIMO_4.1.5.53/Denitr.for": "d4232485cf4dcb755f9a070509d74f5bf1ae22835c2e29df5502d2f307b97e3c",
    "ANIMO_4.1.5.53/UBoundconc.for": "b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7",
    "ANIMO_4.1.5.53/Inicalc.for": "306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1",
    "ANIMO_4.1.5.53/MODFLUX.FOR": "0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d",
    "ANIMO_4.1.5.53/Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
    "ANIMO_4.1.5.53/TRANSPORT.FOR": "3f597b896ab5514e0b836f5547b342e317b03c8e3e58e053e113bd1c17e2f998",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_map():
    with open(ROOT / "reference/source/source_manifest.csv", newline="", encoding="utf-8-sig") as f:
        return {row["path"]: row["sha256"] for row in csv.DictReader(f)}


def changed_paths():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], cwd=ROOT, text=True)
    return {x.strip() for x in out.splitlines() if x.strip()}


def validate_review(r):
    assert r["work_unit"] == "ANIMO-SQ04"
    assert r["risk_tier"] == "C"
    assert r["review_mode"] == "SAME_AGENT_SECOND_PASS"
    assert r["assurance_label"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
    assert r["same_agent"] is True
    assert r["independence_claimed"] is False
    assert r["outcome"] == "SELF_REVIEW_PASS"
    assert r["review_boundary"] == {
        "complete_authoring_package_persisted": True,
        "immutable_head_frozen_before_review": True,
        "source_testbank_evidence_hashes_recorded_before_review": True,
        "authoring_completed_before_review": True,
        "authoring_head_matches_reviewed_head": True,
        "moving_tree_reviewed": False,
    }
    assert all(v == "PASS" for v in r["evidence_reuse_checks"].values())
    assert r["counter_hypothesis"]["tested"] is True
    assert r["counter_hypothesis"]["result"] in {
        "ALTERNATIVE_REJECTED_BY_PINNED_EVIDENCE",
        "ALTERNATIVE_REMAINS_PLAUSIBLE_FAIL_CLOSED",
    }
    assert r["active_controls"] and r["negative_controls"]
    for gate in r["scientific_gates"].values():
        if gate["applicability"] == "APPLICABLE":
            assert gate["result"] == "PASS"
        else:
            assert gate["applicability"] == "NOT_APPLICABLE"
            assert gate["result"] == "NOT_APPLICABLE"
    assert all(v == "PASS" for v in r["adversarial_gates"].values())
    tc = r["tier_c_enhanced"]
    for key in [
        "immutable_authoring_checkpoint",
        "complete_source_state_ownership_reconstruction",
        "first_read_first_write_or_restore_direction_analysis",
        "counter_hypothesis_test",
        "active_controls",
        "negative_controls",
        "regression_guard",
    ]:
        assert tc[key] == "PASS"
    assert tc["split_run_or_restart_evidence"]["applicability"] == "NOT_APPLICABLE"
    assert tc["split_run_or_restart_evidence"]["result"] == "NOT_APPLICABLE"
    assert tc["no_invented_tolerance"] is True
    assert tc["regression_surface_declared"] is True
    assert tc["exact_final_head_ci_required"] is True
    assert r["residual_uncertainty"]


def main():
    a = load(AUDIT)
    f = load(FREEZE)
    s = load(STATUS)

    assert a["work_unit"] == f["work_unit"] == s["work_unit"] == "ANIMO-SQ04"
    assert a["target"] == f["target"] == s["target"] == "TCD-016-C1"
    assert f["base_head"] == BASE
    assert a["base_authority"] == s["base_authority"] == f"ANIMO-SQ03@{BASE}"
    assert a["global_b3_authority"] == s["global_b3_authority"] == f"ANIMO-B3Q06@{B3Q06}"
    assert a["aggregate_authority"] == s["aggregate_authority"] == f"ANIMO-RG05O@{RG05O}"
    assert a["gov05_authority"] == s["gov05_authority"] == f"ANIMO-GOV05@{GOV05}"
    assert a["source_archive_sha256"] == f["source_archive_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
    assert a["testbank_archive_sha256"] == f["testbank_archive_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"

    manifest = manifest_map()
    for path, sha in EXPECTED_SOURCE.items():
        assert manifest.get(path) == sha, (path, manifest.get(path), sha)
        assert a["source_files"].get(path) == sha

    scan = a["session_local_source_search"]
    assert scan["archive_hash_reverified"] is True
    assert set(scan["search_terms"]) == {"Frvo", "NH3", "ammonia", "volatilization"}
    assert set(scan["Frvo_symbol_files"]) == {
        "ANIMO_4.1.5.53/Addit.for",
        "ANIMO_4.1.5.53/Animo.for",
        "ANIMO_4.1.5.53/Animo.inc",
        "ANIMO_4.1.5.53/Input_addit.for",
        "ANIMO_4.1.5.53/Outbal_calc.for",
        "ANIMO_4.1.5.53/Output2.for",
    }
    assert scan["generic_state_dependent_surface_NH4_volatilization_operator_found"] is False
    assert scan["raw_source_republished"] is False

    routes = a["audited_routes"]
    assert set(routes) == {
        "management_addition_volatilization_Frvo",
        "soil_nitrification_transformation",
        "soil_NH4_sorption",
        "top_reservoir_Conhtop",
        "aqueous_transport",
    }
    allowed_dispositions = {
        "NOT_REUSABLE_UNCHANGED",
        "NOT_REUSABLE_UNCHANGED_AS_CONTINUATION_OWNER",
        "NOT_A_CONTINUATION_PROCESS_LAW",
    }
    for name, route in routes.items():
        assert route["source_contract"]
        assert route["evidence"]
        assert route["continuation_mismatch"]
        assert route["disposition"] in allowed_dispositions, (name, route["disposition"])
        assert "REUSABLE_UNCHANGED" not in route["disposition"].replace("NOT_REUSABLE_UNCHANGED", "")

    assert a["bounded_conclusion"] == s["bounded_conclusion"] == "NO_AUDITED_EXISTING_REV53_NH4_ROUTE_IS_SEMANTICALLY_REUSABLE_UNCHANGED_FOR_TCD016_C1_CONTINUATION_STATE"
    assert a["adaptation_may_be_qualified_later"] is True
    assert a["unchanged_reuse_qualified"] is False
    assert a["specific_new_process_law_qualified"] is False
    assert a["historical_behavior"] == s["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
    assert a["c1_b3_disposition"] == s["c1_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert a["parent_b3_disposition"] == s["parent_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert a["e1_disposition"] == s["e1_disposition"] == "BLOCKED_PENDING_CONCRETE_PHYSICAL_ACTIVATION_AND_PROCESS_LAW"
    assert a["production_authorized"] is False
    assert all(v is False for v in s["hard_boundaries"].values())

    unexpected = changed_paths() - ALLOWED
    assert not unexpected, f"scope guard failed: {sorted(unexpected)}"

    if REVIEW.exists():
        r = load(REVIEW)
        validate_review(r)
        assert s["review"]["completed"] is True
        assert s["review"]["reviewed_head"] == r["reviewed_authoring_head"]
        assert s["qualified"] is True
        assert s["state"] == "QUALIFIED_TCD016_C1_EXISTING_PROCESS_REUSE_AUDIT_NO_UNCHANGED_REUSE_NO_B3_ADMISSION"
        assert s["decision"] == "QUALIFY_EXISTING_PROCESS_REUSE_AUDIT_NO_AUDITED_ROUTE_REUSABLE_UNCHANGED_ADAPTED_OR_NEW_PROCESS_SEMANTICS_REQUIRE_SEPARATE_QUALIFICATION"
        assert s["b3_admission_performed"] is False
        assert s["production_authorized"] is False
    else:
        assert s["qualified"] is False
        assert s["decision"] is None
        assert s["review"]["completed"] is False

    print("SQ04 TCD016-C1 existing-process reuse audit validation PASS")


if __name__ == "__main__":
    main()
