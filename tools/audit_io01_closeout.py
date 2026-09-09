#!/usr/bin/env python3
"""Fail-closed reconciliation audit for the ANIMO-IO01 closeout artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "integration/animo-io/ANIMO-IO01-CLOSEOUT.json"
STATUS = ROOT / "integration/animo-io/ANIMO-IO01_STATUS.json"
DIRECT = ROOT / "integration/animo-io/DIRECT-PILOT-QUALIFICATION.json"
MAT = ROOT / "integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json"
LINEAGE = ROOT / "integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json"
DOC = ROOT / "docs/io/ANIMO-IO01-CLOSEOUT.md"

EXPECTED_DECISION = (
    "QUALIFIED_LEGACY_INPUT_CONTRACT_TTUTIL_SOURCE_DIRECT_AND_BOUNDED_"
    "MATERIAL_REPRESENTATION_PILOTS"
)
EXPECTED_MAT_DECISION = (
    "QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS"
)
EXPECTED_BASELINE = "b45ff9b522155bba5b3ddf555a0f9535593333b9"
EXPECTED_SWAP_SHA = "2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360"
EXPECTED_TTUTIL_SHA = "ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193"
EXPECTED_TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


closeout = load(CLOSEOUT)
status = load(STATUS)
direct = load(DIRECT)
mat = load(MAT)
lineage = load(LINEAGE)

if not DOC.exists():
    fail("missing docs/io/ANIMO-IO01-CLOSEOUT.md")

if closeout.get("work_unit") != "ANIMO-IO01":
    fail("closeout work_unit mismatch")
if closeout.get("status") != "CLOSEOUT_READY_BOUNDED_REPRESENTATION_QUALIFICATION_COMPLETE":
    fail("closeout status widened or regressed")
if closeout.get("decision") != EXPECTED_DECISION:
    fail("closeout decision mismatch")
if status.get("decision") != EXPECTED_DECISION:
    fail("global IO01 status decision disagrees with closeout")
if closeout.get("qualification_baseline_head") != EXPECTED_BASELINE:
    fail("qualification baseline head changed")
ci = closeout.get("qualification_baseline_ci", {})
if ci.get("run_id") != 34337491169 or ci.get("conclusion") != "success":
    fail("qualification baseline CI evidence mismatch")

frozen = closeout.get("frozen_identity", {})
if frozen.get("animo_testbank_sha256") != EXPECTED_TESTBANK_SHA:
    fail("closeout testbank identity mismatch")
if frozen.get("frozen_bytes_modified") is not False:
    fail("closeout may not modify frozen bytes")

ttutil = closeout.get("ttutil", {})
if ttutil.get("official_swap_package_sha256") != EXPECTED_SWAP_SHA:
    fail("SWAP package identity mismatch")
if ttutil.get("embedded_archive_sha256") != EXPECTED_TTUTIL_SHA:
    fail("embedded TTUTIL identity mismatch")
if ttutil.get("version") != "4.27" or ttutil.get("fortran_units") != 153:
    fail("TTUTIL version/unit-count mismatch")
if ttutil.get("source_vendored") is not False:
    fail("closeout may not claim TTUTIL source vendoring")

if direct.get("result") != "PASS" or direct.get("field_exact_equivalence_pass") != 10:
    fail("DIRECT Pilot A qualification evidence changed")
if closeout.get("pilot_A", {}).get("field_exact_pass") != 10:
    fail("closeout DIRECT Pilot A count mismatch")

if mat.get("result") != "PASS" or mat.get("decision") != EXPECTED_MAT_DECISION:
    fail("MATERIAL Pilot B qualification evidence changed")
pilot_b = closeout.get("pilot_B", {})
if pilot_b.get("field_exact") is not True or pilot_b.get("numeric_tolerance_used") is not False:
    fail("closeout MATERIAL exactness/tolerance policy mismatch")
if pilot_b.get("typed_double_mismatch_count") != 26:
    fail("closeout lost typed DOUBLE negative evidence")
if pilot_b.get("typed_double_max_ulp_distance") != 1:
    fail("closeout typed DOUBLE ULP evidence mismatch")

if lineage.get("result") != "PASS":
    fail("Ruurlo lineage evidence changed")
if lineage.get("dimensions", {}).get("sparse_omitted_cells_each") != 130:
    fail("Ruurlo omitted-cell count mismatch")
if closeout.get("pilot_B", {}).get("sparse_dimensions", {}).get("omitted_cells_each") != 130:
    fail("closeout sparse omitted-cell count mismatch")

hazards = closeout.get("runtime_hazards", [])
if [item.get("id") for item in hazards] != ["MAT-RH-001", "MAT-RH-002"]:
    fail("runtime-hazard handoff changed")
for hazard in hazards:
    if hazard.get("local_TCD_assigned") is not False:
        fail(f"{hazard.get('id')} may not receive a local canonical TCD in IO01")
    route = hazard.get("route", [])
    if "ANIMO-BUILDQ01" not in route:
        fail(f"{hazard.get('id')} lost BUILDQ01 routing")

non_admissions = closeout.get("non_admissions", {})
required_false = (
    "generic_production_ttutil_runtime_adapter",
    "production_input_migration",
    "GENERAL_migration",
    "generic_MATERIAL_beyond_bounded_Ruurlo_scope",
    "GHG_schema_migration",
    "SOIL_migration",
    "PLANT_migration",
    "BOUNDARY_migration",
    "CHEMISTRY_migration",
    "INITIAL_generic_migration",
    "restart_checkpoint_generic_migration",
    "MANAGEMENT_generic_migration",
    "external_crop_generic_migration",
    "soil_temperature_generic_migration",
    "WATBAL_generic_migration",
    "binary_hydrology_ttutil_conversion",
    "model_output_equivalence_claimed",
    "scientific_semantics_changed",
    "B4_admitted",
    "canonical_merge_admitted_by_IO01_alone",
)
for key in required_false:
    if non_admissions.get(key) is not False:
        fail(f"closeout non-admission {key} must remain false")

handoff = closeout.get("handoff", {})
if handoff.get("runtime_semantics") != "ANIMO-BUILDQ01":
    fail("runtime handoff target mismatch")
if handoff.get("canonical_discrepancy_intake") != "ANIMO-B3I01":
    fail("discrepancy intake handoff target mismatch")
if handoff.get("future_input_family_extension") != "NEW_SCOPED_WORK_UNIT_REQUIRED":
    fail("closeout may not silently reopen IO01 for new input families")

print(
    "PASS: ANIMO-IO01 closeout reconciled; Pilots A/B bounded, "
    "non-admissions preserved, MAT-RH-001/002 handed off"
)
