#!/usr/bin/env python3
from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "integration/animo-io/ANIMO_INPUT_CONTRACT_MATRIX.csv"
CASES = ROOT / "integration/animo-io/TTUTIL_EQUIVALENCE_CASES.json"
STATUS = ROOT / "integration/animo-io/ANIMO-IO01_STATUS.json"
DIRECT = ROOT / "integration/animo-io/DIRECT-PILOT-QUALIFICATION.json"
MAT_LINEAGE = ROOT / "integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json"
MAT_QUAL = ROOT / "integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json"
MAT_STATUS = ROOT / "integration/animo-io/MATERIAL-PILOT-B-STATUS.json"

required_families = {
    "DIRECT","GEN","MAT","PLA","SOI","BOU","INI","MAN","CHE",
    "CROP_EXT","SOIL_TEMP","WATBAL_CFG","HYDRO_BINARY","RESTART","GHG_SCHEMA"
}
required_negative = {
    "omitted_mandatory_field","duplicate_field","malformed_number","malformed_table",
    "wrong_count","unknown_key_legacy_quirk","versioned_schema_mismatch","missing_column",
    "empty_value","comment_whitespace_variant","repeated_section_legacy_quirk",
    "inconsistent_cardinality","missing_conditional_section"
}


def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(1)


def load_json(path):
    if not path.exists():
        fail(f"missing required evidence file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


with MATRIX.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
by = {r["family"]: r for r in rows}
missing = required_families - set(by)
if missing:
    fail(f"missing families: {sorted(missing)}")

if by["HYDRO_BINARY"]["ttutil_suitability"] != "BINARY_OR_RUNTIME_FORMAT_NOT_TTUTIL":
    fail("HYDRO_BINARY may not be TTUTIL-converted")
for fam in ("RESTART","INI","MAN","CROP_EXT","SOIL_TEMP","WATBAL_CFG"):
    if by[fam]["ttutil_suitability"] != "KEEP_SPECIALIZED_ADAPTER":
        fail(f"{fam} must remain specialized at IO01")
if by["GHG_SCHEMA"]["ttutil_suitability"] != "LINEAGE_UNRESOLVED":
    fail("GHG schema may not be silently normalized")
if "ModelConfiguration" not in by["GEN"]["target_objects"]:
    fail("GEN target object missing")
if by["DIRECT"]["target_objects"] != "LegacyInputBinding":
    fail("direct file must not become a mega-object")

cases = load_json(CASES)
classes = {c["class"] for c in cases["negative_cases"]}
if not required_negative <= classes:
    fail(f"negative matrix missing: {sorted(required_negative-classes)}")

# Persisted DIRECT Pilot A must remain narrow and field-exact.
direct = load_json(DIRECT)
if direct.get("result") != "PASS":
    fail("DIRECT Pilot A evidence is not PASS")
if direct.get("field_exact_equivalence_pass") != direct.get("cases"):
    fail("DIRECT Pilot A is not field-exact for all recorded natural cases")
if not direct.get("details") or not all(
    item.get("field_exact_equivalent") is True for item in direct["details"]
):
    fail("DIRECT Pilot A contains a non-field-exact case")
if "no model physics" not in direct.get("qualification_scope", ""):
    fail("DIRECT Pilot A scope widened beyond parser representation")

# Natural Ruurlo old/new lineage is the authority for sparse omitted-cell zeros.
lineage = load_json(MAT_LINEAGE)
if lineage.get("result") != "PASS":
    fail("Ruurlo MATERIAL lineage audit is not PASS")
checks = lineage.get("checks", {})
for key in (
    "FR_full_matrix_after_sparse_zero_fill",
    "FRca_full_matrix_after_sparse_zero_fill",
    "Nm", "Nf", "Fror", "Frnh", "Frni", "Recfav", "Nifr",
):
    if checks.get(key) is not True:
        fail(f"Ruurlo MATERIAL lineage check {key} is not true")
rule = lineage.get("sparse_zero_rule", {})
if rule.get("status") != "SUPPORTED_BY_EXACT_NATURAL_CASE_LINEAGE_EQUIVALENCE":
    fail("sparse zero rule lost its natural-lineage qualification")
if lineage.get("dimensions", {}).get("sparse_omitted_cells_each") != 130:
    fail("unexpected Ruurlo sparse omitted-cell count")

# MATERIAL Pilot B exact route must be exact with no tolerance. Direct TTUTIL
# DOUBLE is deliberately negative evidence and may not silently become admitted.
mat = load_json(MAT_QUAL)
expected_mat_decision = (
    "QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS"
)
if mat.get("result") != "PASS" or mat.get("decision") != expected_mat_decision:
    fail("MATERIAL Pilot B qualification decision mismatch")
exact = mat.get("exact_numeric_native_adapter", {})
if exact.get("field_exact_equivalent") is not True:
    fail("MATERIAL exact numeric native adapter is not field-exact")
if exact.get("numeric_tolerance_used") is not False:
    fail("MATERIAL Pilot B may not use a numeric tolerance")
if "CHARACTER" not in exact.get("transport", ""):
    fail("MATERIAL exact path must retain TTUTIL CHARACTER numeric-token transport")
typed = mat.get("typed_ttutil_double_comparison", {})
if typed.get("decision") != "REJECT_TYPED_DOUBLE_FOR_FIELD_EXACT_REPRESENTATION":
    fail("typed TTUTIL DOUBLE negative evidence was lost")
if typed.get("field_exact_equivalent") is not False:
    fail("typed TTUTIL DOUBLE must remain non-field-exact for recorded Ruurlo evidence")
if typed.get("numeric_mismatch_count", 0) <= 0:
    fail("typed TTUTIL DOUBLE mismatch evidence unexpectedly empty")
if typed.get("max_ulp_distance") != 1:
    fail("recorded typed TTUTIL DOUBLE max ULP distance changed")
for key in ("production_migration", "GHG_schema", "binary_hydrology", "model_output_equivalence", "B4"):
    if mat.get("non_admissions", {}).get(key) is not False:
        fail(f"MATERIAL Pilot B non-admission {key} must remain false")
if len(mat.get("runtime_hazard_exclusions", [])) < 2:
    fail("MATERIAL Pilot B runtime-hazard exclusions missing")

# The dedicated Pilot B status must agree with the persisted qualification.
# This guards against a stale STARTED/qualified=false file surviving after closeout.
mat_status = load_json(MAT_STATUS)
if mat_status.get("qualified") is not True:
    fail("MATERIAL Pilot B status is stale or not qualified")
if mat_status.get("status") != expected_mat_decision:
    fail("MATERIAL Pilot B status classification disagrees with qualification evidence")
if mat_status.get("qualification", {}).get("result") != "PASS":
    fail("MATERIAL Pilot B status does not record PASS")
if mat_status.get("qualification", {}).get("field_exact_equivalent") is not True:
    fail("MATERIAL Pilot B status lost field-exact qualification")
if mat_status.get("qualification", {}).get("numeric_tolerance_used") is not False:
    fail("MATERIAL Pilot B status may not admit a numeric tolerance")
if mat_status.get("evidence", {}).get("qualification") != "integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json":
    fail("MATERIAL Pilot B status qualification evidence pointer mismatch")
if len(mat_status.get("runtime_hazards", [])) < 2:
    fail("MATERIAL Pilot B status lost runtime-hazard routing")
for key in (
    "GHGMais_included", "GHG_lineage_normalized", "legacy_science_changed",
    "frozen_bytes_modified", "production_migration_admitted",
    "model_output_equivalence_claimed", "binary_hydrology_converted_to_ttutil",
    "B4_admitted",
):
    if mat_status.get("non_admissions", {}).get(key) is not False:
        fail(f"MATERIAL Pilot B status non-admission {key} must remain false")

status = load_json(STATUS)
if status.get("material_pilot_representation_candidate_qualified") is not True:
    fail("ANIMO-IO01 status disagrees with qualified MATERIAL Pilot B status")
if status.get("material_pilot", {}).get("classification") != expected_mat_decision:
    fail("ANIMO-IO01 MATERIAL classification disagrees with Pilot B evidence")
for key in (
    "legacy_scientific_semantics_changed","frozen_source_modified","frozen_testcase_modified",
    "binary_hydrology_converted_to_ttutil","GHGMais_silently_normalized",
    "production_migration_admitted","B4_admitted"):
    if status["non_admissions"].get(key) is not False:
        fail(f"non-admission {key} must be false")

print(
    f"PASS: {len(rows)} input-family contracts, "
    f"{len(cases['negative_cases'])} negative cases, DIRECT Pilot A, "
    "Ruurlo MATERIAL lineage, MATERIAL Pilot B, status reconciliation"
)
