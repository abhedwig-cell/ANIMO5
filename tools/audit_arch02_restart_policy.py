#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-ARCH02 restart policy.

This tool validates the candidate restart policy against the ARCH01 ownership
registry. It does not execute frozen ANIMO source and does not constitute
behavioural reference evidence.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH01 = ROOT / "integration/animo-architecture/ARCH01_STATE_OWNERSHIP.csv"
ARCH02 = ROOT / "integration/animo-architecture/ARCH02_RESTART_POLICY.csv"

REQUIRED_COLUMNS = {
    "legacy_state_id",
    "candidate_field_id",
    "owner_component",
    "restart_class",
    "physical_checkpoint",
    "diagnostic_checkpoint",
    "restart_source",
    "accepted_boundary_required",
    "recompute_after_restore",
    "conditional_feature",
    "open_evidence",
    "notes",
}

DERIVED_OWNERS = {"DerivedViews", "ProcessScratch"}
DIAGNOSTIC_OWNER = "DiagnosticsLedger"
EXTERNAL_OWNER = "HydrologyExchangeState"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fail(msg: str) -> None:
    raise AssertionError(msg)


def main() -> int:
    arch01 = read_csv(ARCH01)
    arch02 = read_csv(ARCH02)

    if not arch02:
        fail("ARCH02 restart policy is empty")
    if set(arch02[0]) != REQUIRED_COLUMNS:
        fail(f"ARCH02 columns differ from required schema: {set(arch02[0])}")

    a1_ids = [r["legacy_state_id"] for r in arch01]
    a2_ids = [r["legacy_state_id"] for r in arch02]
    if len(a1_ids) != len(set(a1_ids)):
        fail("ARCH01 legacy_state_id values are not unique")
    if len(a2_ids) != len(set(a2_ids)):
        fail("ARCH02 legacy_state_id values are not unique")
    if set(a1_ids) != set(a2_ids):
        missing = sorted(set(a1_ids) - set(a2_ids))
        extra = sorted(set(a2_ids) - set(a1_ids))
        fail(f"ARCH02 coverage mismatch; missing={missing}, extra={extra}")

    a1 = {r["legacy_state_id"]: r for r in arch01}
    a2 = {r["legacy_state_id"]: r for r in arch02}

    for sid, row in a2.items():
        owner = a1[sid]["owner_component"]
        if row["candidate_field_id"] != a1[sid]["candidate_field_id"]:
            fail(f"candidate field drift for {sid}")
        if row["owner_component"] != owner:
            fail(f"owner drift for {sid}")
        if row["accepted_boundary_required"] != "YES":
            fail(f"checkpoint boundary must be accepted for {sid}")

        if owner in DERIVED_OWNERS:
            if row["physical_checkpoint"] != "NO":
                fail(f"derived/scratch field checkpointed as physical: {sid}")
            if row["recompute_after_restore"] != "YES":
                fail(f"derived/scratch field not recomputed: {sid}")

        if owner == DIAGNOSTIC_OWNER:
            if row["physical_checkpoint"] != "NO":
                fail(f"diagnostic observer checkpointed as physical: {sid}")
            if row["restart_class"] != "DIAGNOSTIC_CONTINUATION":
                fail(f"diagnostic observer lacks continuation class: {sid}")

        if owner == EXTERNAL_OWNER:
            if row["physical_checkpoint"] != "NO":
                fail(f"hydrology exchange coordinate duplicated in ANIMO checkpoint: {sid}")
            if row["restart_source"] != "EXTERNAL_HYDROLOGY_OWNER":
                fail(f"hydrology exchange coordinate lacks external owner: {sid}")

    physical_yes = sum(r["physical_checkpoint"] == "YES" for r in arch02)
    physical_conditional = sum(r["physical_checkpoint"].startswith("IF_") for r in arch02)
    recomputed = sum(r["recompute_after_restore"] == "YES" for r in arch02)
    diagnostic = sum(r["restart_class"] == "DIAGNOSTIC_CONTINUATION" for r in arch02)

    print(f"PASS ARCH01 rows={len(arch01)} ARCH02 rows={len(arch02)}")
    print(
        "restart policy summary: "
        f"physical_yes={physical_yes} conditional={physical_conditional} "
        f"recomputed={recomputed} diagnostic_continuation={diagnostic}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
