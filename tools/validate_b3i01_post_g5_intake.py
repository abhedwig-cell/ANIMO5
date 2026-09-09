#!/usr/bin/env python3
"""Validate ANIMO-B3I01 post-G5 canonical intake and register appends fail-closed."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
APPEND_ROWS = ROOT / "integration/animo-b3/B3I01_REGISTER_APPEND_ROWS.csv"
APPEND_ROWS_SUPP1 = ROOT / "integration/animo-b3/B3I01_REGISTER_APPEND_SUPPLEMENT_01_ROWS.csv"
ROUTING = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json"
ROUTING_SUPP1 = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_01.json"
RESERVATIONS = ROOT / "integration/animo-b3/POST_G5_TCD_RESERVATIONS.json"
RESERVATIONS_SUPP1 = ROOT / "integration/animo-b3/POST_G5_TCD_RESERVATIONS_SUPPLEMENT_01.json"
TCD028 = ROOT / "integration/animo-b3/TCD-028_RESERVATION.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I01_STATUS.json"
RECON = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_RECONCILIATION.json"
RECON_SUPP1 = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_SUPPLEMENT_01_RECONCILIATION.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def assert_non_admission(record: dict, keys: list[str], label: str) -> None:
    for key in keys:
        if record.get(key) is not False:
            raise AssertionError(f"{label} violates fail-closed flag {key}")


def main() -> None:
    register = read_csv(REGISTER)
    expected_ids = [f"TCD-{i:03d}" for i in range(1, 40)]
    actual_ids = [row["ID"] for row in register]
    if actual_ids != expected_ids:
        raise AssertionError(f"canonical register IDs are not contiguous TCD-001..039: {actual_ids}")

    base_append_rows = read_csv(APPEND_ROWS)
    expected_base_append_ids = [f"TCD-{i:03d}" for i in range(28, 38)]
    if [row["ID"] for row in base_append_rows] != expected_base_append_ids:
        raise AssertionError("prepared base append rows are not exactly TCD-028..037")

    supp_rows = read_csv(APPEND_ROWS_SUPP1)
    expected_supp_ids = ["TCD-038", "TCD-039"]
    if [row["ID"] for row in supp_rows] != expected_supp_ids:
        raise AssertionError("supplement append rows are not exactly TCD-038..039")

    register_by_id = {row["ID"]: row for row in register}
    for row in base_append_rows + supp_rows:
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
        raise AssertionError(f"unexpected initial B3I01 reservation sequence: {reserved}")
    assert_non_admission(
        reservations,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted"],
        "initial reservation batch",
    )

    supp_res = json.loads(RESERVATIONS_SUPP1.read_text(encoding="utf-8"))
    supp_reserved = [item["tcd_id"] for item in supp_res["reservations"]]
    if supp_reserved != expected_supp_ids:
        raise AssertionError(f"unexpected supplemental reservation sequence: {supp_reserved}")
    if supp_res.get("authority", {}).get("canonical_register_tail_observed") != "TCD-037":
        raise AssertionError("supplement reservation did not observe TCD-037 as prior canonical tail")
    assert_non_admission(
        supp_res,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_reservation"],
        "supplement reservation batch",
    )

    tcd028 = json.loads(TCD028.read_text(encoding="utf-8"))
    if tcd028.get("tcd_id") != "TCD-028":
        raise AssertionError("pre-existing reservation is not TCD-028")
    if tcd028.get("admissions", {}).get("b3_admitted") is not False:
        raise AssertionError("TCD-028 reservation must remain non-admitted")

    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    routing_by_key = {item["canonical_key"]: item for item in routing["canonical_routing"]}
    for rid in expected_base_append_ids:
        if rid not in routing_by_key:
            raise AssertionError(f"registered TCD missing from initial B3I01 routing: {rid}")
        if routing_by_key[rid].get("admitted") is not False:
            raise AssertionError(f"initial routing unexpectedly admits {rid}")

    routing_supp = json.loads(ROUTING_SUPP1.read_text(encoding="utf-8"))
    routing_supp_by_key = {item["canonical_key"]: item for item in routing_supp["canonical_routing_additions"]}
    for rid in ["TCD-031", "TCD-038", "TCD-039"]:
        if rid not in routing_supp_by_key:
            raise AssertionError(f"supplement routing missing {rid}")
        if routing_supp_by_key[rid].get("admitted") is not False:
            raise AssertionError(f"supplement routing unexpectedly admits {rid}")
    if routing_supp.get("source_local_label_reconciliation", {}).get("PREP12_source_local_TCD-032") != "TCD-031":
        raise AssertionError("PREP12 local TCD-032 must map by phenomenon to canonical TCD-031")
    if routing_supp.get("source_local_label_reconciliation", {}).get("PREP12_source_local_TCD-033") != "TCD-038":
        raise AssertionError("PREP12 local TCD-033 must map to canonical TCD-038")
    if routing_supp.get("source_local_label_reconciliation", {}).get("PREP12_source_local_TCD-034") != "TCD-039":
        raise AssertionError("PREP12 local TCD-034 must map to canonical TCD-039")
    runtime = {item["local_key"]: item for item in routing_supp["runtime_routing_additions"]}
    if runtime["BUILDQ01-LCL-MAPOHYDRO-LNBOMPMX-CROSS-TASK-LIFETIME"].get("existing_tcd") != "TCD-011":
        raise AssertionError("LnBoMpMx storage-duration candidate must map to TCD-011")
    if runtime["BUILDQ01-LCL-MAPOHYDRO-INDEX0-BOUNDS-ORDER"].get("disposition") != "BUILD_RUNTIME_HAZARD_NOT_TCD":
        raise AssertionError("MAPOHYDRO bounds-order seam must remain a runtime hazard without TCD")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert_non_admission(
        status,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted"],
        "B3I01 initial status",
    )

    recon = json.loads(RECON.read_text(encoding="utf-8"))
    canonical = recon.get("canonical_register", {})
    if canonical.get("tail_before") != "TCD-027" or canonical.get("tail_after") != "TCD-037":
        raise AssertionError("initial register append reconciliation has wrong before/after tails")
    if canonical.get("append_only") is not True or canonical.get("existing_rows_changed") is not False:
        raise AssertionError("initial register append must be append-only")
    if recon.get("registered_not_admitted") != expected_base_append_ids:
        raise AssertionError("initial reconciliation registered ID set mismatch")
    assert_non_admission(
        recon.get("admission_state", {}),
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_register_append"],
        "initial register reconciliation",
    )

    recon_supp = json.loads(RECON_SUPP1.read_text(encoding="utf-8"))
    canonical_supp = recon_supp.get("canonical_register", {})
    if canonical_supp.get("tail_before") != "TCD-037" or canonical_supp.get("tail_after") != "TCD-039":
        raise AssertionError("supplement register append reconciliation has wrong before/after tails")
    if canonical_supp.get("append_only") is not True or canonical_supp.get("existing_rows_changed") is not False:
        raise AssertionError("supplement register append must be append-only")
    if recon_supp.get("registered_not_admitted") != expected_supp_ids:
        raise AssertionError("supplement reconciliation registered ID set mismatch")
    assert_non_admission(
        recon_supp.get("admission_state", {}),
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_register_append"],
        "supplement register reconciliation",
    )

    print("ANIMO-B3I01 post-G5 intake and canonical register append validation: PASS through TCD-039")


if __name__ == "__main__":
    main()
