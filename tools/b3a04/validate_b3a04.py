#!/usr/bin/env python3
"""Fail-closed structural validator for ANIMO-B3A04 TCD-026 readiness evidence.

This validator checks persisted evidence consistency and branch scope. It does not
re-execute the frozen B0 diagnostic campaign and is not an independent scientific
second-line review, historical B2 reference, corrected-legacy admission, or
production qualification.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B3 = ROOT / "integration" / "animo-b3"
BASE = "383c7a83e84a578969f92113280dc715b7bdddb4"
FINAL = "QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING"
SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
CANDIDATE = "Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P"

ALLOWED_PATHS = {
    ".github/workflows/animo-b3a04-tcd026-readiness.yml",
    "docs/b3/TCD026_CLASS_A_ADMISSION_READINESS.md",
    "docs/b3/TCD026_SECOND_LINE_REVIEW_PACKET.md",
    "integration/animo-b3/ANIMO-B3A04_STATUS.json",
    "integration/animo-b3/TCD026_CHRONOLOGICAL_RESTART_PROBE.json",
    "integration/animo-b3/TCD026_CHRONOLOGICAL_RESTART_PROBE_PLAN.json",
    "integration/animo-b3/TCD026_CLASS_A_READINESS.json",
    "integration/animo-b3/TCD026_EXPECTED_DIFFERENCE.json",
    "integration/animo-b3/TCD026_MODEL_PRODUCED_STATE_REPLAY.json",
    "integration/animo-b3/TCD026_SECOND_LINE_REVIEW_REQUEST.json",
    "tools/b3a04/validate_b3a04.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(name: str):
    with (B3 / name).open(encoding="utf-8") as stream:
        return json.load(stream)


def validate_scope() -> list[str]:
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASE}...HEAD"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    unexpected = sorted(set(changed) - ALLOWED_PATHS)
    require(not unexpected, f"unexpected ANIMO-B3A04 changed paths: {unexpected}")
    require(
        not any(
            path.startswith(("src/", "reference/source/", "reference/testcases/"))
            for path in changed
        ),
        "ANIMO-B3A04 must not modify production or frozen reference paths",
    )
    return changed


def main() -> None:
    status = load_json("ANIMO-B3A04_STATUS.json")
    readiness = load_json("TCD026_CLASS_A_READINESS.json")
    expected = load_json("TCD026_EXPECTED_DIFFERENCE.json")
    replay = load_json("TCD026_MODEL_PRODUCED_STATE_REPLAY.json")
    chrono = load_json("TCD026_CHRONOLOGICAL_RESTART_PROBE.json")
    plan = load_json("TCD026_CHRONOLOGICAL_RESTART_PROBE_PLAN.json")
    review = load_json("TCD026_SECOND_LINE_REVIEW_REQUEST.json")

    for obj, label in ((status, "status"), (readiness, "readiness")):
        require(obj["frozen_B0"]["source_sha256"] == SOURCE_SHA256, f"{label} source hash drift")
        require(obj["frozen_B0"]["testbank_sha256"] == TESTBANK_SHA256, f"{label} testbank hash drift")

    require(status["decision"] == FINAL, "status final decision drift")
    require(readiness["readiness_decision"]["status"] == FINAL, "readiness final decision drift")
    require(status["admitted"] is False, "B3A04 must remain not admitted")
    require(readiness["readiness_decision"]["admitted"] is False, "readiness must remain not admitted")
    require(status["production_patch_present"] is False, "production patch must remain absent")
    require(status["production_migration_admitted"] is False, "production migration must remain blocked")

    require(expected["candidate_ledger_observation"] == CANDIDATE, "candidate expression drift")
    require(expected["unexpected_difference_policy"] == "FAIL_CLOSED", "difference policy must fail closed")
    require(expected["numeric_tolerance_policy"] == "NO_TOLERANCE_FOR_SCOPE_OR_NON_INTERFERENCE_CLAIMS", "tolerance policy drift")
    require(expected["physical_state_patch"] is False, "expected contract must not patch state")
    require(expected["initialization_physics_change"] is False, "expected contract must not change initialization physics")

    require(
        chrono["status"] == "PASS_TCD026_CHRONOLOGICAL_FORMATTED_RESTART_ACTIVATION_FULL_SPLIT_IDENTITY_NOT_CLAIMED",
        "chronological probe status drift",
    )
    require(
        chrono["chronology"]["segment_B"]["initial_in_sha256"]
        == chrono["chronology"]["segment_A"]["model_produced_initial_out_sha256"],
        "chronological restart state hash mismatch",
    )
    require(chrono["chronology"]["segment_B"]["initial_in_byte_identical_to_segment_A_initial_out"] is True,
            "Segment-B input must be exact Segment-A output bytes")
    require(abs(chrono["tcd026_discriminator"]["segment_B_beginning_model_produced_Ex_kg_ha"] - 642.718929) < 1e-12,
            "chronological model-produced Ex witness drift")
    require(abs(chrono["tcd026_discriminator"]["printed_begin_store_increment_kg_ha"] - 642.719) < 1e-12,
            "chronological beginning-store increment drift")
    require(chrono["tcd026_discriminator"]["small_candidate_residual_is_tolerance"] is False,
            "candidate residual must not become a tolerance")
    require(chrono["candidate_non_interference"]["final_restart_state_byte_identical"] is True,
            "candidate changed chronological final restart state")
    require(chrono["candidate_non_interference"]["unexpected_changed_outputs"] == [],
            "unexpected chronological candidate outputs recorded")
    require(chrono["continuous_vs_formatted_restart_crosscheck"]["byte_identical"] is False,
            "legacy formatted restart must not be promoted to exact identity")
    require(chrono["continuous_vs_formatted_restart_crosscheck"]["numeric_tokens_compared"] == 564,
            "formatted-restart token witness drift")
    require(chrono["continuous_vs_formatted_restart_crosscheck"]["printed_numeric_tokens_different"] == 32,
            "formatted-restart difference count drift")
    require(chrono["continuous_vs_formatted_restart_crosscheck"]["max_abs_printed_numeric_difference"] == 1.0e-6,
            "formatted-restart maximum printed drift witness changed")
    require(chrono["continuous_vs_formatted_restart_crosscheck"]["whole_model_split_run_identity_claimed"] is False,
            "whole-model formatted restart identity must remain unclaimed")

    require(plan["status"] == "EXECUTED_PASS_TCD026_ACTIVATION_FULL_SPLIT_IDENTITY_NOT_CLAIMED",
            "chronological probe plan/result state drift")
    require(plan["fail_closed"] is True, "chronological plan must remain fail closed")

    require(replay["chronological_split_run_claimed"] is False, "non-chronological replay scope drift")
    require(replay["historical_reference_claimed"] is False, "replay must not become historical reference")

    stateq = readiness["authorities"]["STATEQ02"]
    require(stateq["tcd026_ledger_oracle"] is False, "STATEQ02 must not become TCD-026 ledger oracle")
    require(stateq["B2_reference"] is False, "STATEQ02 must not become B2")

    require(readiness["gates"]["valid_admission_route"] == "PENDING_BLOCKED", "admission route unexpectedly opened")
    require(readiness["gates"]["independent_second_line_review"] == "REQUEST_PREPARED_NOT_COMPLETED",
            "independent review gate drift")
    require(review["authoring_counts_as_independent_review"] is False, "authoring must not count as review")
    require(review["review_complete"] is False, "review must remain incomplete")
    require(review["current_outcome"] == "INCOMPLETE_REVIEW", "review outcome unexpectedly changed")

    require(all(value is False for value in readiness["hard_constraints"].values()),
            "one or more readiness hard constraints violated")
    require(all(value is False for value in status["hard_constraints"].values()),
            "one or more status hard constraints violated")

    changed = validate_scope()
    print(
        "ANIMO-B3A04 validation PASS: "
        f"{len(changed)} scoped paths; chronological TCD-026 activation retained; "
        "formatted whole-model restart identity not claimed; route/review gates remain blocked"
    )


if __name__ == "__main__":
    main()
