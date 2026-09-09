#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "integration/animo-io/ANIMO_INPUT_CONTRACT_MATRIX.csv"
CASES = ROOT / "integration/animo-io/TTUTIL_EQUIVALENCE_CASES.json"
STATUS = ROOT / "integration/animo-io/ANIMO-IO01_STATUS.json"

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

with MATRIX.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
by = {r["family"]: r for r in rows}
missing = required_families - set(by)
if missing: fail(f"missing families: {sorted(missing)}")

for fam in ("HYDRO_BINARY",):
    if by[fam]["ttutil_suitability"] != "BINARY_OR_RUNTIME_FORMAT_NOT_TTUTIL":
        fail(f"{fam} may not be TTUTIL-converted")
for fam in ("RESTART","INI","MAN","CROP_EXT","SOIL_TEMP","WATBAL_CFG"):
    if by[fam]["ttutil_suitability"] != "KEEP_SPECIALIZED_ADAPTER":
        fail(f"{fam} must remain specialized at IO01")
if by["GHG_SCHEMA"]["ttutil_suitability"] != "LINEAGE_UNRESOLVED":
    fail("GHG schema may not be silently normalized")
if "ModelConfiguration" not in by["GEN"]["target_objects"]:
    fail("GEN target object missing")
if by["DIRECT"]["target_objects"] != "LegacyInputBinding":
    fail("direct file must not become a mega-object")

cases = json.loads(CASES.read_text(encoding="utf-8"))
classes = {c["class"] for c in cases["negative_cases"]}
if not required_negative <= classes:
    fail(f"negative matrix missing: {sorted(required_negative-classes)}")

status = json.loads(STATUS.read_text(encoding="utf-8"))
for key in (
    "legacy_scientific_semantics_changed","frozen_source_modified","frozen_testcase_modified",
    "binary_hydrology_converted_to_ttutil","GHGMais_silently_normalized",
    "production_migration_admitted","B4_admitted"):
    if status["non_admissions"].get(key) is not False:
        fail(f"non-admission {key} must be false")

print(f"PASS: {len(rows)} input-family contracts, {len(cases['negative_cases'])} negative cases")
