#!/usr/bin/env python3
"""Fail-closed structural validator for ANIMO-B3A04R technical review.

This checks persisted review consistency and branch scope only. It is not an
independent second-line review, scientific re-execution, B2 reference,
corrected-legacy admission or production qualification.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B3 = ROOT / "integration" / "animo-b3"
REVIEWED_HEAD = "5eaf02298603b85f802d8e35d6a63941d0878879"
SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
FINAL = "TECHNICAL_REVIEW_PASS_BUT_INDEPENDENT_SECOND_LINE_AND_ROUTE_GATES_NOT_SATISFIED_TCD026_NOT_ADMITTED"
CANDIDATE = "Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P"

ALLOWED_PATHS = {
    ".github/workflows/animo-b3a04r-tcd026-technical-review.yml",
    "docs/b3/TCD026_TECHNICAL_REVIEW.md",
    "integration/animo-b3/ANIMO-B3A04R_STATUS.json",
    "tools/b3a04r/validate_b3a04r.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    status_path = B3 / "ANIMO-B3A04R_STATUS.json"
    with status_path.open(encoding="utf-8") as stream:
        status = json.load(stream)

    require(status["reviewed_head"] == REVIEWED_HEAD, "reviewed B3A04 head drift")
    require(status["frozen_B0"]["source_sha256"] == SOURCE_SHA256, "source hash drift")
    require(status["frozen_B0"]["testbank_sha256"] == TESTBANK_SHA256, "testbank hash drift")
    require(status["atomic_candidate"] == CANDIDATE, "atomic candidate drift")
    require(status["technical_disposition"] == "PASS_TCD026_CLASS_A_TECHNICAL_READINESS_REVIEWED", "technical disposition drift")
    require(status["final_decision"] == FINAL, "final decision drift")
    require(status["review_complete_as_technical_review"] is True, "technical review must remain complete")
    require(status["independent_second_line_complete"] is False, "independent second-line must remain incomplete")
    require(status["admitted"] is False, "TCD-026 must remain not admitted")
    require(status["production_patch_present"] is False, "production patch must remain absent")

    route = status["governance_gates"]
    require(route["valid_admission_route"] == "FAIL_PENDING_NO_VALID_ROUTE", "route unexpectedly opened")
    require(route["independent_second_line_review"] == "FAIL_NOT_INDEPENDENT", "review independence unexpectedly claimed")
    require(route["corrected_legacy_admitted"] is False, "corrected legacy unexpectedly admitted")
    require(route["production_migration_admitted"] is False, "production migration unexpectedly admitted")

    chrono = status["causal_witnesses"]["chronological_1974_1975"]
    require(abs(chrono["initial_Ex_kg_ha"] - 642.718929) < 1e-12, "chronological Ex witness drift")
    require(abs(chrono["candidate_begin_store_increment_kg_ha_printed"] - 642.719) < 1e-12, "chronological ledger increment drift")
    require(chrono["final_restart_state_byte_identical_legacy_vs_candidate"] is True, "candidate changed final restart state")
    require(chrono["unexpected_changed"] == 0, "unexpected candidate output differences")

    restart = status["formatted_restart_negative_control"]
    require(restart["exact_whole_model_identity"] is False, "legacy formatted restart must not become exact checkpoint")
    require(restart["tolerance_used_to_promote_identity"] is False, "formatted restart drift must not be tolerance-masked")
    require(restart["continuous_vs_split_numeric_tokens_compared"] == 564, "restart token witness drift")
    require(restart["different_tokens"] == 32, "restart difference count drift")
    require(restart["max_abs_printed_difference"] == 1.0e-6, "restart max drift witness changed")

    synq = status["authority_rechecks"]["SYNQ01"]
    require(synq["tcd026_specific_oracle"] is False, "unrelated SYNQ oracle promoted to TCD-026")
    stateq = status["authority_rechecks"]["STATEQ02"]
    require(stateq["tcd026_ledger_oracle"] is False, "STATEQ02 promoted to ledger oracle")
    require(stateq["historical_b2_reference"] is False, "STATEQ02 promoted to B2")
    require(stateq["legacy_formatted_restart_identity_oracle"] is False, "STATEQ02 promoted to legacy formatted restart oracle")

    require(all(value is False for value in status["hard_constraints"].values()), "hard constraint violated")

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{REVIEWED_HEAD}...HEAD"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    unexpected = sorted(set(changed) - ALLOWED_PATHS)
    require(not unexpected, f"unexpected B3A04R changed paths: {unexpected}")
    require(not any(path.startswith(("src/", "reference/source/", "reference/testcases/")) for path in changed),
            "B3A04R must not modify production or frozen reference paths")

    print(
        "ANIMO-B3A04R validation PASS: technical review persisted; "
        "independence and route remain fail-closed; no production/frozen-reference changes"
    )


if __name__ == "__main__":
    main()
