#!/usr/bin/env python3
"""Fail-closed technical review validation for ANIMO-B3B03R.

This validator does not satisfy reviewer independence and does not admit B3.
"""
from __future__ import annotations

import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B03R_STATUS.json"
REVIEW = ROOT / "docs/b3/TCD024_SECOND_LINE_TECHNICAL_REVIEW.md"


def main() -> None:
    # Re-run the complete candidate readiness validator from the reviewed tree.
    runpy.run_path(str(ROOT / "tools/validate_b3b03_tcd024.py"), run_name="__main__")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    text = REVIEW.read_text(encoding="utf-8")

    assert status["work_unit"] == "ANIMO-B3B03R"
    assert status["reviewed_head"] == "446f57f3aeff6e7db56ce473f0724bdb58cad94f"
    assert status["target_tcd"] == "TCD-024"
    assert status["class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert status["independent_second_line_gate_satisfied"] is False
    assert status["route_state"]["normal_B2_available"] is False
    assert status["route_state"]["historical_uncertainty_route_available"] is False
    assert status["route_state"]["historical_prevalence"] == "UNKNOWN"
    assert status["admitted"] is False
    assert status["production_migration_admitted"] is False

    scope = status["review_scope"]
    assert scope["legacy_expression"] == "Yy = One + Parcxsl(3,I) * Avc"
    assert scope["candidate_atomic_expression"] == "Yy = One + Parcxsl(3,J) * Avc"
    for key in (
        "modify_TCD019",
        "joint_TCD019_TCD024_admission",
        "solver_redesign",
        "tolerance",
        "production_patch",
        "B3_admission",
    ):
        assert scope[key] is False

    assert "PASS_TCD024_ATOMIC_CLASS_B_READINESS_TECHNICALLY_RECONFIRMED" in text
    assert "FAIL_PENDING_NO_VALID_ADMISSION_ROUTE" in text
    assert "FAIL_NOT_INDEPENDENT" in text
    assert "historical_prevalence = UNKNOWN" in text
    assert "work/animo-nq02-tcd019-nonlinear-p-qualification" in text
    assert "40a41089020f78ee1d5181b8afc7bdb511af3193" in text
    assert "9ca37e90115faab9604a3f3051a8246b5e3a0813" in text
    assert "tolerance" in text.lower()

    print("ANIMO-B3B03R technical review validator: PASS")
    print("reviewer independence gate: FAIL_NOT_INDEPENDENT retained")
    print("admission route: FAIL_PENDING_NO_VALID_ADMISSION_ROUTE retained")
    print("B3 admission performed: false")


if __name__ == "__main__":
    main()
