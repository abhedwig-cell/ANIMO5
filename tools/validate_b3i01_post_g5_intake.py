#!/usr/bin/env python3
"""Validate ANIMO-B3I01 post-G5 canonical intake and register append fail-closed."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
APPEND_ROWS = ROOT / "integration/animo-b3/B3I01_REGISTER_APPEND_ROWS.csv"
ROUTING = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json"
RESERVATIONS = ROOT / "integration/animo-b3/POST_G5_TCD_RESERVATIONS.json"
TCD028 = ROOT / "integration/animo-b3/TCD-028_RESERVATION.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I01_STATUS.json"
RECON = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_RECONCILIATION.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    register = read_csv(REGISTER)
    expected_ids = [f"TCD-{i:03d}" for i in range(1, 38)]
    actual_ids = [row["ID"] for row in register]
    if actual_ids != expected_ids:
        raise AssertionError(f"canonical register IDs are not contiguous TCD-001..037: {actual_ids}")

    append_rows = read_csv(APPEND_ROWS)
    expected_append_ids = [f"TCD-{i:03d}" for i in range(28, 38)]
    if [row["ID"] for row in append_rows] != expected_append_ids:
        raise AssertionError("prepared append rows are not exactly TCD-028..037")

    register_by_id = {row["ID"]: row for row in register}
    for row in append_rows:
        rid = row["ID"]
        if register_by_id[rid] != row:
            raise AssertionError(f"canonical register row differs from prepared fail-closed append row: {rid}")
        if row["status"] != "OPEN":
            raise AssertionError(f"appended row is not OPEN: {rid}")
        if not row["classification"].startswith("RESERVED_POST_G5_"):
            raise AssertionError(f"appended row lost reservation/non-admission classification: {rid}")

    for child in ["TCD-016-C1", "TCD-016-E1", "TCD-009-GHG-GAS-STORE"]:
        if child in actual_ids:
            raise AssertionError(f"child routing atom must not be a top-level register ID: {child}")

    reservations = json.loads(RESERVATIONS.read_text(encoding="utf-8"))
    reserved = [item["tcd_id"] for item in reservations["reservations"]]
    if reserved != [f"TCD-{i:03d}" for i in range(29, 38)]:
        raise AssertionError(f"unexpected B3I01 reservation sequence: {reserved}")
    if reservations.get("new_corrections_admitted") is not False:
        raise AssertionError("reservation batch must admit no corrections")

    tcd028 = json.loads(TCD028.read_text(encoding="utf-8"))
    if tcd028.get("tcd_id") != "TCD-028":
        raise AssertionError("pre-existing reservation is not TCD-028")
    if tcd028.get("admissions", {}).get("b3_admitted") is not False:
        raise AssertionError("TCD-028 reservation must remain non-admitted")

    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    routing_by_key = {item["canonical_key"]: item for item in routing["canonical_routing"]}
    for rid in expected_append_ids:
        if rid not in routing_by_key:
            raise AssertionError(f"registered TCD missing from B3I01 routing: {rid}")
        if routing_by_key[rid].get("admitted") is not False:
            raise AssertionError(f"routing unexpectedly admits {rid}")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    for key in ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted"]:
        if status.get(key) is not False:
            raise AssertionError(f"B3I01 status violates fail-closed flag {key}")

    recon = json.loads(RECON.read_text(encoding="utf-8"))
    canonical = recon.get("canonical_register", {})
    if canonical.get("tail_before") != "TCD-027" or canonical.get("tail_after") != "TCD-037":
        raise AssertionError("register append reconciliation has wrong before/after tails")
    if canonical.get("append_only") is not True or canonical.get("existing_rows_changed") is not False:
        raise AssertionError("register append must be append-only")
    if recon.get("registered_not_admitted") != expected_append_ids:
        raise AssertionError("reconciliation registered ID set mismatch")
    if any(recon.get("admission_state", {}).get(key) is not False for key in [
        "new_corrections_admitted", "b3_baseline_established", "production_migration_admitted",
        "evidence_strength_increased_by_register_append"
    ]):
        raise AssertionError("register append reconciliation must not increase admission/evidence strength")

    print("ANIMO-B3I01 post-G5 intake and canonical register append validation: PASS")


if __name__ == "__main__":
    main()
