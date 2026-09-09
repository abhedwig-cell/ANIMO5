#!/usr/bin/env python3
"""Fail-closed structural validation for ANIMO-STATEQ02 persisted evidence.

This validator does not reproduce the B0 executable split-run because the frozen
source/testbank archives are intentionally not stored in the repository. It
checks that the persisted qualification record is internally consistent,
retains the exact-comparison contract, and does not broaden the admitted scope.
"""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "integration" / "animo-state"
DOC = ROOT / "docs" / "state" / "RESTRICTED_CORE_SPLIT_RUN_QUALIFICATION.md"
BASE = "4adae99576eb56978da71f7c8a250e4445fd3bc4"
FINAL = "QUALIFIED_RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_CANONICAL_STATE_ADMISSION_PENDING"
SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_scope() -> None:
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASE}...HEAD"], cwd=ROOT, text=True
    ).splitlines()
    allowed_exact = {
        ".github/workflows/animo-stateq02-restricted-core.yml",
        "docs/state/RESTRICTED_CORE_SPLIT_RUN_QUALIFICATION.md",
        "integration/animo-state/ANIMO-STATEQ02_STATUS.json",
        "integration/animo-state/STATEQ02_CHECKPOINT_DIFFS.csv",
        "integration/animo-state/STATEQ02_SPLIT_RUN_MATRIX.json",
        "tools/stateq02/validate_stateq02.py",
    }
    require(set(changed).issubset(allowed_exact), f"unexpected STATEQ02 changed paths: {sorted(set(changed)-allowed_exact)}")
    require(not any(p.startswith("src/") for p in changed), "STATEQ02 must not modify production source")
    require(not any(p.startswith("reference/source/") or p.startswith("reference/testcases/") for p in changed),
            "STATEQ02 must not modify frozen source/testcase reference paths")


def main() -> None:
    status = load_json(STATE / "ANIMO-STATEQ02_STATUS.json")
    matrix = load_json(STATE / "STATEQ02_SPLIT_RUN_MATRIX.json")
    diffs = load_csv(STATE / "STATEQ02_CHECKPOINT_DIFFS.csv")
    doc = DOC.read_text(encoding="utf-8")

    require(status["status"] == FINAL, "final status mismatch")
    require(matrix["status"] == FINAL, "matrix status mismatch")
    require(status["source_hash"] == SOURCE_SHA256, "source hash mismatch")
    require(status["testbank_hash"] == TESTBANK_SHA256, "testbank hash mismatch")
    require(matrix["source_archive_sha256"] == SOURCE_SHA256, "matrix source hash mismatch")
    require(matrix["testbank_archive_sha256"] == TESTBANK_SHA256, "matrix testbank hash mismatch")
    require(status["canonical_state_admission"] == "PENDING", "canonical STATE must remain pending")
    require(status["whole_model_state_claim"] is False, "whole-model STATE claim must remain false")
    require(status["production_implementation"] == "NONE", "production implementation must remain NONE")
    require(status["execution_completed"] is True, "executable campaign must be recorded complete")
    require(status["comparison_policy"] == "EXACT_BITWISE_NO_TOLERANCE", "comparison policy must stay exact")

    cases = matrix["cases"]
    splits = [c for c in cases if c["case_id"].startswith("STATEQ02-SPLIT-")]
    guards = [c for c in cases if c["case_id"].startswith("STATEQ02-GUARD-")]
    require({c["split_step"] for c in splits} == {66, 67, 68, 71, 72}, "required split boundaries missing")
    require(len(guards) == 1 and guards[0]["split_step"] == 282, "required rejection sentinel missing")

    classes = {cls for c in splits for cls in c["boundary_classes"]}
    for required in (
        "ORDINARY_INTERIOR",
        "MANAGEMENT_ADJACENT",
        "YEAR_BOUNDARY",
        "P_ACTIVE",
        "UPPER_RESERVOIR_NONZERO",
        "ZERO_SURFACE_STORAGE_NEGATIVE_CONTROL",
    ):
        require(required in classes, f"required boundary class missing: {required}")

    for c in splits:
        require(c["accepted_restore_snapshot_exact"] is True, f"restore not exact: {c['case_id']}")
        require(c["future_physical_trace_exact"] is True, f"future trace not exact: {c['case_id']}")
        require(c["max_abs_difference"] == 0.0, f"nonzero difference: {c['case_id']}")
        require(c["comparison_policy"] == "EXACT_BITWISE_NO_TOLERANCE", f"tolerance policy drift: {c['case_id']}")
        require(c["profile_guards"]["IoptGHG"] == 0, "GHG must stay disabled")
        require(c["profile_guards"]["IoptMP"] == 0, "macropores must stay disabled")
        require(c["profile_guards"]["surface_Pnt"] == 0.0 and c["profile_guards"]["surface_Snt"] == 0.0,
                "qualified split must stay on exact zero-surface guard")
        require(c["profile_guards"]["layer0_restart_solutes"] == "EXACT_ZERO",
                "TCD-040 active path must stay excluded")
        require(c["p_state"]["site_resolved_checkpointed"] is True, "P site state must be explicit")
        require(c["crop_mode"] == "EXTERNAL", "qualified crop mode must remain external")

    split67 = next(c for c in splits if c["split_step"] == 67)
    require(split67["future_records_compared"] == 833 and split67["future_end_step"] == 900,
            "full remaining-horizon witness drift")

    guard = guards[0]
    require(guard["surface_Pnt"] > 0.0, "rejection sentinel must have positive surface storage")
    require(guard["layer0_restart_solutes_nonzero"] is True, "rejection sentinel must activate nonzero layer0 path")
    require(guard["stage_a_exit_code"] == 95, "rejection sentinel exit code mismatch")
    require(guard["checkpoint_created"] is False, "rejected sentinel must not create checkpoint")

    hard = matrix["hard_rules"]
    require(all(v is False for v in hard.values()), "one or more hard-rule prohibitions were violated")
    require(matrix["canonical_state_admission"] == "PENDING", "matrix must not admit canonical STATE")
    require(matrix["whole_model_state_claim"] is False, "matrix must not claim whole-model STATE")

    for row in diffs:
        require(row["equal"].lower() == "true", f"non-equal persisted diff row: {row['case_id']} {row['coordinate_group']}")
        require("TOLERANCE" in row["policy"], "comparison policy field missing")
        require(row["policy"] in {"NO_TOLERANCE"}, "unexpected comparison policy")
        if row["comparison_mode"] == "EXACT_BITWISE":
            require(float(row["max_abs_difference"]) == 0.0, "exact-bitwise row has nonzero difference")

    for token in (
        FINAL,
        "833 remaining accepted records",
        "exit code `95`",
        "canonical STATE admission = PENDING",
        "whole-model STATE claim = false",
        "production implementation = NONE",
    ):
        require(token in doc, f"qualification document missing invariant: {token}")

    validate_scope()
    print(f"STATEQ02 validation PASS: {len(splits)} exact split runs, {len(diffs)} persisted comparison rows, 1 fail-closed sentinel")


if __name__ == "__main__":
    main()
