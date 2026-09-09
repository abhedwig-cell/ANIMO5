#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3B03R independent second-line review.

This validator validates either a structurally complete pending handoff or a
completed review record. It does not perform B3 admission and does not authorize
or modify production source.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "integration/animo-b3/TCD024_INDEPENDENT_REVIEW_RESULT.json"
HANDOFF = ROOT / "integration/animo-b3/ANIMO-B3B03R_REVIEW_HANDOFF.json"
PACKET = ROOT / "docs/b3/TCD024_SECOND_LINE_REVIEW_PACKET.md"
REPORT = ROOT / "docs/b3/TCD024_INDEPENDENT_SECOND_LINE_REVIEW.md"
CANDIDATE_STATUS = ROOT / "integration/animo-b3/ANIMO-B3B03_STATUS.json"

EXPECTED_CANDIDATE = "446f57f3aeff6e7db56ce473f0724bdb58cad94f"
EXPECTED_TECHNICAL = "02ce1f49582d2b8cb794c3bfb9d674481a2eea1e"
EXPECTED_RUN = 34383614846
EXPECTED_REVIEW_START = "07e440bb42d58facad6b4e5408dd57a0d8f82daf"
EXPECTED_GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_B3D03 = "a3e194573b3a7ce95d5ef15fc179ddb3a613d8a6"
EXPECTED_B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_NQ02 = "40a41089020f78ee1d5181b8afc7bdb511af3193"
EXPECTED_SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
EXPECTED_SYNQ01_TREE = "124364c008cdca511f024b3b7d7677572c6ac0c7"
EXPECTED_SYNQ_ORACLE_BLOB = "4c215d19844614de8868380fb03f93268ea4c5d8"

MANDATORY_GATES = {
    "frozen_canonical_identity",
    "exact_source_seam",
    "class_B_atomicity",
    "unequal_site_discriminator",
    "unrounded_state_transfer_evidence",
    "multi_site_conservation_identity",
    "active_inactive_controls",
    "TCD019_separation",
    "expected_difference_non_interference",
    "natural_activation_limitation_retained",
    "historical_prevalence_UNKNOWN_retained",
    "live_admission_route_rechecked",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    result = load(RESULT)
    handoff = load(HANDOFF)
    candidate = load(CANDIDATE_STATUS)
    packet = PACKET.read_text(encoding="utf-8")

    assert result["work_unit"] == "ANIMO-B3B03R"
    assert result["target_tcd"] == "TCD-024"
    assert result["class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert result["candidate_head"] == EXPECTED_CANDIDATE
    assert result["technical_review_head"] == EXPECTED_TECHNICAL
    assert result["technical_review_validation_run"] == EXPECTED_RUN
    assert result["technical_review_validation_conclusion"] == "success"
    assert candidate["status"] == "QUALIFIED_TCD024_CLASS_B_ADMISSION_READINESS_HISTORICAL_ROUTE_BLOCKED_SECOND_LINE_REVIEW_PENDING"
    assert candidate["admitted"] is False
    assert candidate["production_migration_admitted"] is False

    assert handoff["candidate_head"] == EXPECTED_CANDIDATE
    assert handoff["technical_review_head"] == EXPECTED_TECHNICAL
    assert handoff["technical_review_validation_run"] == EXPECTED_RUN
    assert handoff["technical_review_validation_conclusion"] == "success"
    assert handoff["independent_review_must_not_be_inferred_from_technical_review"] is True

    assert "independent from ANIMO-B3B03 authoring" in packet
    assert "historical_prevalence = UNKNOWN" in packet
    assert "Do not broaden the review into TCD-019" in packet
    assert "A passing independent review still does not admit TCD-024" in packet

    gates = result["gates"]
    assert set(gates) == MANDATORY_GATES
    assert result["historical_prevalence"] == "UNKNOWN"
    assert result["B3_admitted"] is False
    assert result["production_patch"] is False
    assert result["production_migration_admitted"] is False

    status = result["review_status"]
    if status == "PENDING_INDEPENDENT_REVIEW":
        assert result["reviewer_independent_from_B3B03_authoring"] is None
        assert result["reviewer_identity_or_workunit"] is None
        assert result["reviewed_candidate_head"] is None
        assert all(v == "PENDING" for v in gates.values())
        assert result["overall_technical_second_line_result"] == "PENDING"
        assert result["route_state_at_review"] == "PENDING_LIVE_RECHECK"
        print("ANIMO-B3B03R independent review execution contract: PASS_PENDING_HANDOFF")
        return

    assert status in {"COMPLETED_PASS", "COMPLETED_FAIL"}
    assert result["reviewer_independent_from_B3B03_authoring"] is True
    assert isinstance(result["reviewer_identity_or_workunit"], str) and result["reviewer_identity_or_workunit"].strip()
    assert result["independence_scope"] == "SEPARATE_CHATGPT_CONTEXT_ONLY_NO_ORGANIZATIONAL_OR_HUMAN_INDEPENDENCE_CLAIM"
    assert result["reviewed_candidate_head"] == EXPECTED_CANDIDATE
    assert result["review_start_head"] == EXPECTED_REVIEW_START
    assert result["historical_fidelity_claimed"] is False
    assert result["B2_qualified_for_target_path"] is False
    assert result["natural_positive_Optcxsl2_activation_in_frozen_testbank"] is False
    assert result["route_state_at_review"] in {
        "NORMAL_B2_AVAILABLE",
        "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY",
        "BLOCKED_NO_VALID_ADMISSION_ROUTE",
    }

    pins = result["live_pins"]
    assert pins["GOV03_head"] == EXPECTED_GOV03
    assert pins["B3D03_head"] == EXPECTED_B3D03
    assert pins["B3Q01_head"] == EXPECTED_B3Q01
    assert pins["NQ02_head"] == EXPECTED_NQ02
    assert pins["SYNQ01_commit_head"] == EXPECTED_SYNQ01
    assert pins["SYNQ01_tree_sha"] == EXPECTED_SYNQ01_TREE
    assert pins["SYNQ01_oracle_register_blob"] == EXPECTED_SYNQ_ORACLE_BLOB

    report = REPORT.read_text(encoding="utf-8")
    assert "PASS_TCD024_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION" in report
    assert EXPECTED_CANDIDATE in report
    assert EXPECTED_GOV03 in report
    assert EXPECTED_B3D03 in report
    assert EXPECTED_SYNQ01 in report
    assert EXPECTED_SYNQ01_TREE in report
    assert "historical prevalence remains `UNKNOWN`" in report
    assert "No organizational or human independence is claimed" in report
    assert "No B3 admission is performed" in report
    assert "No production source is modified" in report

    if status == "COMPLETED_PASS":
        assert all(v == "PASS" for v in gates.values())
        assert result["overall_technical_second_line_result"] == "PASS"
        assert result["route_state_at_review"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
        print("ANIMO-B3B03R independent review execution contract: PASS_COMPLETED_REVIEW")
    else:
        assert any(v == "FAIL" for v in gates.values())
        assert result["overall_technical_second_line_result"] == "FAIL"
        print("ANIMO-B3B03R independent review execution contract: PASS_FAIL_CLOSED_REVIEW")


if __name__ == "__main__":
    main()
