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
APPEND_ROWS_SUPP2 = ROOT / "integration/animo-b3/B3I01_REGISTER_APPEND_SUPPLEMENT_02_ROWS.csv"
ROUTING = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json"
ROUTING_SUPP1 = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_01.json"
ROUTING_SUPP2 = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_02.json"
RESERVATIONS = ROOT / "integration/animo-b3/POST_G5_TCD_RESERVATIONS.json"
RESERVATIONS_SUPP1 = ROOT / "integration/animo-b3/POST_G5_TCD_RESERVATIONS_SUPPLEMENT_01.json"
RESERVATIONS_SUPP2 = ROOT / "integration/animo-b3/POST_G5_TCD_RESERVATIONS_SUPPLEMENT_02.json"
TCD028 = ROOT / "integration/animo-b3/TCD-028_RESERVATION.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I01_STATUS.json"
STATUS_SUPP2 = ROOT / "integration/animo-b3/ANIMO-B3I01_SUPPLEMENT_02_STATUS.json"
RECON = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_RECONCILIATION.json"
RECON_SUPP1 = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_SUPPLEMENT_01_RECONCILIATION.json"
RECON_SUPP2 = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_SUPPLEMENT_02_RECONCILIATION.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def assert_non_admission(record: dict, keys: list[str], label: str) -> None:
    for key in keys:
        if record.get(key) is not False:
            raise AssertionError(f"{label} violates fail-closed flag {key}")


def main() -> None:
    register = read_csv(REGISTER)
    expected_ids = [f"TCD-{i:03d}" for i in range(1, 41)]
    actual_ids = [row["ID"] for row in register]
    if actual_ids != expected_ids:
        raise AssertionError(f"canonical register IDs are not contiguous TCD-001..040: {actual_ids}")

    base_append_rows = read_csv(APPEND_ROWS)
    expected_base_append_ids = [f"TCD-{i:03d}" for i in range(28, 38)]
    if [row["ID"] for row in base_append_rows] != expected_base_append_ids:
        raise AssertionError("prepared base append rows are not exactly TCD-028..037")

    supp1_rows = read_csv(APPEND_ROWS_SUPP1)
    expected_supp1_ids = ["TCD-038", "TCD-039"]
    if [row["ID"] for row in supp1_rows] != expected_supp1_ids:
        raise AssertionError("supplement-01 append rows are not exactly TCD-038..039")

    supp2_rows = read_csv(APPEND_ROWS_SUPP2)
    expected_supp2_ids = ["TCD-040"]
    if [row["ID"] for row in supp2_rows] != expected_supp2_ids:
        raise AssertionError("supplement-02 append rows are not exactly TCD-040")

    register_by_id = {row["ID"]: row for row in register}
    for row in base_append_rows + supp1_rows + supp2_rows:
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

    supp1_res = json.loads(RESERVATIONS_SUPP1.read_text(encoding="utf-8"))
    supp1_reserved = [item["tcd_id"] for item in supp1_res["reservations"]]
    if supp1_reserved != expected_supp1_ids:
        raise AssertionError(f"unexpected supplement-01 reservation sequence: {supp1_reserved}")
    if supp1_res.get("authority", {}).get("canonical_register_tail_observed") != "TCD-037":
        raise AssertionError("supplement-01 reservation did not observe TCD-037 as prior canonical tail")
    assert_non_admission(
        supp1_res,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_reservation"],
        "supplement-01 reservation batch",
    )

    supp2_res = json.loads(RESERVATIONS_SUPP2.read_text(encoding="utf-8"))
    supp2_reserved = [item["tcd_id"] for item in supp2_res["reservations"]]
    if supp2_reserved != expected_supp2_ids:
        raise AssertionError(f"unexpected supplement-02 reservation sequence: {supp2_reserved}")
    if supp2_res.get("authority", {}).get("canonical_register_tail_observed") != "TCD-039":
        raise AssertionError("supplement-02 reservation did not observe TCD-039 as prior canonical tail")
    if supp2_res["reservations"][0].get("provisional_b3_class") != "B":
        raise AssertionError("TCD-040 must remain provisional Class B at intake")
    if "Copo(0)" in supp2_res["reservations"][0].get("affected_coordinates", []):
        raise AssertionError("TCD-040 must not include Copo(0)")
    assert_non_admission(
        supp2_res,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_reservation"],
        "supplement-02 reservation batch",
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

    routing_supp1 = json.loads(ROUTING_SUPP1.read_text(encoding="utf-8"))
    routing_supp1_by_key = {item["canonical_key"]: item for item in routing_supp1["canonical_routing_additions"]}
    for rid in ["TCD-031", "TCD-038", "TCD-039"]:
        if rid not in routing_supp1_by_key:
            raise AssertionError(f"supplement-01 routing missing {rid}")
        if routing_supp1_by_key[rid].get("admitted") is not False:
            raise AssertionError(f"supplement-01 routing unexpectedly admits {rid}")
    if routing_supp1.get("source_local_label_reconciliation", {}).get("PREP12_source_local_TCD-032") != "TCD-031":
        raise AssertionError("PREP12 local TCD-032 must map by phenomenon to canonical TCD-031")
    if routing_supp1.get("source_local_label_reconciliation", {}).get("PREP12_source_local_TCD-033") != "TCD-038":
        raise AssertionError("PREP12 local TCD-033 must map to canonical TCD-038")
    if routing_supp1.get("source_local_label_reconciliation", {}).get("PREP12_source_local_TCD-034") != "TCD-039":
        raise AssertionError("PREP12 local TCD-034 must map to canonical TCD-039")
    runtime = {item["local_key"]: item for item in routing_supp1["runtime_routing_additions"]}
    if runtime["BUILDQ01-LCL-MAPOHYDRO-LNBOMPMX-CROSS-TASK-LIFETIME"].get("existing_tcd") != "TCD-011":
        raise AssertionError("LnBoMpMx storage-duration candidate must map to TCD-011")
    if runtime["BUILDQ01-LCL-MAPOHYDRO-INDEX0-BOUNDS-ORDER"].get("disposition") != "BUILD_RUNTIME_HAZARD_NOT_TCD":
        raise AssertionError("MAPOHYDRO bounds-order seam must remain a runtime hazard without TCD")

    routing_supp2 = json.loads(ROUTING_SUPP2.read_text(encoding="utf-8"))
    routing_supp2_by_key = {item["canonical_key"]: item for item in routing_supp2["canonical_routing_additions"]}
    if list(routing_supp2_by_key) != expected_supp2_ids:
        raise AssertionError(f"supplement-02 routing must contain only TCD-040: {list(routing_supp2_by_key)}")
    tcd040_route = routing_supp2_by_key["TCD-040"]
    if tcd040_route.get("admitted") is not False:
        raise AssertionError("supplement-02 routing unexpectedly admits TCD-040")
    if tcd040_route.get("source_key") != "RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING":
        raise AssertionError("TCD-040 routing lost STATEQ01 source-local identity")
    if tcd040_route.get("b3_class") != "B":
        raise AssertionError("TCD-040 routing must remain provisional Class B")
    if tcd040_route.get("excluded_coordinate") != "Copo(0)":
        raise AssertionError("TCD-040 routing must explicitly exclude Copo(0)")
    atomicity = routing_supp2.get("atomicity_decision", {})
    if atomicity.get("top_level_ids_allocated") != 1 or atomicity.get("species_split") is not False:
        raise AssertionError("TCD-040 atomicity decision is not preserved")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert_non_admission(
        status,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted"],
        "B3I01 initial status",
    )

    status_supp2 = json.loads(STATUS_SUPP2.read_text(encoding="utf-8"))
    assert_non_admission(
        status_supp2,
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted"],
        "B3I01 supplement-02 status",
    )
    if status_supp2.get("production_code_modified") is not False or status_supp2.get("source_correction") is not False:
        raise AssertionError("supplement-02 must not modify production/source behaviour")

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

    recon_supp1 = json.loads(RECON_SUPP1.read_text(encoding="utf-8"))
    canonical_supp1 = recon_supp1.get("canonical_register", {})
    if canonical_supp1.get("tail_before") != "TCD-037" or canonical_supp1.get("tail_after") != "TCD-039":
        raise AssertionError("supplement-01 register append reconciliation has wrong before/after tails")
    if canonical_supp1.get("append_only") is not True or canonical_supp1.get("existing_rows_changed") is not False:
        raise AssertionError("supplement-01 register append must be append-only")
    if recon_supp1.get("registered_not_admitted") != expected_supp1_ids:
        raise AssertionError("supplement-01 reconciliation registered ID set mismatch")
    assert_non_admission(
        recon_supp1.get("admission_state", {}),
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_register_append"],
        "supplement-01 register reconciliation",
    )

    recon_supp2 = json.loads(RECON_SUPP2.read_text(encoding="utf-8"))
    canonical_supp2 = recon_supp2.get("canonical_register", {})
    if canonical_supp2.get("tail_before") != "TCD-039" or canonical_supp2.get("tail_after") != "TCD-040":
        raise AssertionError("supplement-02 register append reconciliation has wrong before/after tails")
    if canonical_supp2.get("blob_before") != "264ea7d0dd5764d837b40f19d6ba70152be2e743":
        raise AssertionError("supplement-02 reconciliation is not bound to the TCD-039 register blob")
    if canonical_supp2.get("blob_after") != "fb44f54aabcf9cd9ee8a8a52bbec78e5cdf06c25":
        raise AssertionError("supplement-02 reconciliation is not bound to the TCD-040 register blob")
    if canonical_supp2.get("append_only") is not True or canonical_supp2.get("existing_rows_changed") is not False:
        raise AssertionError("supplement-02 register append must be append-only")
    if recon_supp2.get("registered_not_admitted") != expected_supp2_ids:
        raise AssertionError("supplement-02 reconciliation registered ID set mismatch")
    if recon_supp2.get("atomicity", {}).get("explicitly_excluded_coordinate") != "Copo(0)":
        raise AssertionError("supplement-02 reconciliation lost Copo(0) exclusion")
    assert_non_admission(
        recon_supp2.get("admission_state", {}),
        ["new_corrections_admitted", "b3_baseline_established", "production_migration_admitted", "evidence_strength_increased_by_register_append"],
        "supplement-02 register reconciliation",
    )

    print("ANIMO-B3I01 post-G5 intake and canonical register append validation: PASS through TCD-040")


if __name__ == "__main__":
    main()
