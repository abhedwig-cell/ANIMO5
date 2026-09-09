#!/usr/bin/env python3
"""Fail-closed audit for persisted ANIMO-IO02 GENERAL qualification evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUAL = ROOT / "integration/animo-io/ANIMO-IO02-QUALIFICATION.json"
GRAMMAR = ROOT / "integration/animo-io/GENERAL-REV53-GRAMMAR.json"
CONTRACT = ROOT / "docs/io/GENERAL_INPUT_CONTRACT.md"

DECISION = (
    "QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_"
    "WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS"
)
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
VFPROJ_SHA = "f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a"
TOP_LEVEL = [">simopt:", ">simtim:", ">outscr:", ">outbal:", ">outsel:", ">outtot:"]
PASS_FILES = {
    "ANIMO_testbank/CranGrass/Input/GENERAL.INP",
    "ANIMO_testbank/CranMais/Input/GENERAL.INP",
    "ANIMO_testbank/LWKM_gras_1040.2021.2045/input/GENERAL.INP",
    "ANIMO_testbank/Puitmijn_Cranendonck_60/input/GENERAL.INP",
    "ANIMO_testbank/RuurloGrass/Input/GENERAL.INP",
    "ANIMO_testbank/STONE_akk_0006.2001.2015/input/GENERAL.INP",
    "ANIMO_testbank/Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA/Input/GENERAL.INP",
}
REQUIRED_PROBES = {
    "top_level_section_physical_reorder": "PASS",
    "intra_simopt_key_reorder": "PASS",
    "missing_label": "PASS",
    "leading_space_in_ordered_key": "PASS",
    "pclass_compatibility_default": "PASS",
    "hydro_year_negative_natural": "PASS",
    "readts_scans_comment_for_first_0_to_3_digit": "PASS",
    "simtim_date_key_name_not_validated": "PASS",
    "repeated_balance_update_dates_source_sort": "PASS",
    "optional_last_outputs_omission": "PASS_WITH_EXPLICIT_HAZARD",
    "printbal_label_mismatch": "PASS",
    "eof_at_required_readop": "PASS",
    "ghg_schema_boundary": "PASS",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


qual = load(QUAL)
grammar = load(GRAMMAR)
if not CONTRACT.exists():
    fail("missing docs/io/GENERAL_INPUT_CONTRACT.md")

if qual.get("workunit") != "ANIMO-IO02":
    fail("qualification workunit mismatch")
if qual.get("schema") != "ANIMO-IO02-Qualification/v1":
    fail("qualification schema mismatch")
if qual.get("decision") != DECISION:
    fail("qualification decision changed")

for key in (
    "production_migration_admitted",
    "grammar_redesign_admitted",
    "ghg_schema_admitted",
    "initial_restart_admitted",
    "binary_hydrology_admitted",
):
    if qual.get(key) is not False:
        fail(f"{key} must remain false")

ids = qual.get("frozen_identities", {})
if ids.get("source_zip_sha256") != SOURCE_SHA:
    fail("source archive identity mismatch")
if ids.get("testbank_zip_sha256") != TESTBANK_SHA:
    fail("testbank identity mismatch")
if ids.get("vfproj_sha256") != VFPROJ_SHA:
    fail("vfproj identity mismatch")

if qual.get("qualified_natural_count") != 7:
    fail("qualified natural count changed")
if qual.get("non_ghg_natural_count") != 8:
    fail("non-GHG natural count changed")
if qual.get("ghg_natural_count_excluded") != 1:
    fail("GHG exclusion count changed")

natural = qual.get("natural_testbank", {})
observed_pass = {
    name
    for name, item in natural.items()
    if item.get("status") == "PASS_SOURCE_COMPATIBLE_BOUNDED_REPRESENTATION"
}
if observed_pass != PASS_FILES:
    fail(f"natural pass set changed: {sorted(observed_pass)}")

grass = natural.get("ANIMO_testbank/GrassPeat/Input/GENERAL.INP", {})
if grass.get("status") != "REJECTED_BY_REV53_SEQUENCE_CONTRACT":
    fail("GrassPeat must remain negative sequence evidence")
if grass.get("error") != "9871" or grass.get("line") != 118:
    fail("GrassPeat negative evidence error/line changed")
if "WFPS=" not in grass.get("message", "") or "O2_content=" not in grass.get("message", ""):
    fail("GrassPeat WFPS/O2 sequence evidence changed")

ghg = natural.get("ANIMO_testbank/GHGMais/Input/general.inp", {})
if ghg.get("status") != "EXCLUDED_GHG_SCHEMA_NOT_ADMITTED":
    fail("GHGMais must remain scope-excluded")
if ghg.get("GreenHouseGasOption") != 1:
    fail("GHGMais routing evidence changed")

probes = qual.get("mutation_probes", {})
if set(probes) != set(REQUIRED_PROBES):
    fail("mutation-probe set changed")
for name, expected_status in REQUIRED_PROBES.items():
    if probes[name].get("status") != expected_status:
        fail(f"probe {name} status changed")

if probes["pclass_compatibility_default"].get("value") != 0:
    fail("PClass compatibility default changed")
if probes["hydro_year_negative_natural"].get("value") != -30:
    fail("HydroYearSwitch=-30 natural evidence changed")
if probes["repeated_balance_update_dates_source_sort"].get("post_parser_value") != [100.0, 300.0]:
    fail("balance date source-sort evidence changed")
optional = probes["optional_last_outputs_omission"]
if optional.get("selected_compartment_output") != "LEGACY_UNDEFINED_IF_OMITTED":
    fail("late optional OutseLn hazard was normalized away")

checks = qual.get("source_contract_checks", {})
required_checks = {
    "revision_53_id",
    "compiled_member_named_input1",
    "real_kind_8",
    "findadr_rewinds",
    "findadr_exact_a8",
    "readop_bang_delimited",
    "readts_digit_scan",
    "optional_readts_defaults",
    "pclass_default_path",
    "hydro_year_default_path",
    "hydro_year_wrong_range_check_preserved",
    "balance_sort",
    "printbal_silent_return",
    "ghg_feature_gate",
    "top_level_parser_call_order",
}
for name in required_checks:
    if checks.get(name) is not True:
        fail(f"source contract check not qualified: {name}")

if grammar.get("workunit") != "ANIMO-IO02":
    fail("grammar workunit mismatch")
authority = grammar.get("authority", {})
if authority.get("source_archive_sha256") != SOURCE_SHA:
    fail("grammar source identity mismatch")
if authority.get("source_revision") != 53 or authority.get("animo_version_branch") != 41:
    fail("grammar revision/version mismatch")
if authority.get("vfproj_sha256") != VFPROJ_SHA:
    fail("grammar vfproj identity mismatch")

top = grammar.get("top_level", {})
if top.get("parser_call_order") != TOP_LEVEL:
    fail("top-level parser call order changed")
if top.get("conditional_call", {}).get("admission") != "ROUTE_ONLY_NOT_NORMALIZED":
    fail("GHG route-only boundary changed")

rep = grammar.get("normalized_representation", {})
if rep.get("not_a_free_order_property_bag") is not True:
    fail("GENERAL may not become a free-order property bag")
if rep.get("no_blanket_numeric_tolerance") is not True:
    fail("blanket numeric tolerance must remain disallowed")
if rep.get("typed_targets") != [
    "ModelConfiguration",
    "SimulationWindow",
    "DiagnosticsConfiguration",
]:
    fail("typed target-object boundary changed")

contract = CONTRACT.read_text(encoding="utf-8")
required_contract_tokens = [
    "Findadr",
    "ReadTs",
    "HydroYearSwitch=-30",
    "LEGACY_UNDEFINED_IF_OMITTED",
    "GHGMais",
    "production input migration",
    "TTUTIL as scientific or numerical authority",
]
for token in required_contract_tokens:
    if token not in contract:
        fail(f"GENERAL contract lost required boundary text: {token}")

print(
    "PASS: ANIMO-IO02 persisted GENERAL qualification reconciled; "
    "7 natural non-GHG files qualified, GrassPeat negative evidence preserved, "
    "GHGMais excluded, 13 mutation probes intact"
)
