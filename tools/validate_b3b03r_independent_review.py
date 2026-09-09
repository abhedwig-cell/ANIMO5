#!/usr/bin/env python3
"""Fail-closed contract validator for ANIMO-B3B03R independent review handoff.

This validator does not perform the independent review. It validates either:
1. a structurally complete pending handoff; or
2. a completed independent technical review record with all mandatory gates PASS.

It never admits B3 and never authorizes a production patch.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "integration/animo-b3/TCD024_INDEPENDENT_REVIEW_RESULT.json"
HANDOFF = ROOT / "integration/animo-b3/ANIMO-B3B03R_REVIEW_HANDOFF.json"
PACKET = ROOT / "docs/b3/TCD024_SECOND_LINE_REVIEW_PACKET.md"
CANDIDATE_STATUS = ROOT / "integration/animo-b3/ANIMO-B3B03_STATUS.json"

EXPECTED_CANDIDATE = "446f57f3aeff6e7db56ce473f0724bdb58cad94f"
EXPECTED_TECHNICAL = "02ce1f49582d2b8cb794c3bfb9d674481a2eea1e"
EXPECTED_RUN = 34383614846
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
    assert result["reviewed_candidate_head"] == EXPECTED_CANDIDATE
    assert result["route_state_at_review"] in {
        "NORMAL_B2_AVAILABLE",
        "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY",
        "BLOCKED_NO_VALID_ADMISSION_ROUTE",
    }

    if status == "COMPLETED_PASS":
        assert all(v == "PASS" for v in gates.values())
        assert result["overall_technical_second_line_result"] == "PASS"
        print("ANIMO-B3B03R independent review execution contract: PASS_COMPLETED_REVIEW")
    else:
        assert any(v == "FAIL" for v in gates.values())
        assert result["overall_technical_second_line_result"] == "FAIL"
        print("ANIMO-B3B03R independent review execution contract: PASS_FAIL_CLOSED_REVIEW")


if __name__ == "__main__":
    main()
