#!/usr/bin/env python3
"""Fail-closed reconciliation audit for ANIMO-IO02 closeout."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "integration/animo-io/ANIMO-IO02-CLOSEOUT.json"
QUAL = ROOT / "integration/animo-io/ANIMO-IO02-QUALIFICATION.json"
GRAMMAR = ROOT / "integration/animo-io/GENERAL-REV53-GRAMMAR.json"
CONTRACT = ROOT / "docs/io/GENERAL_INPUT_CONTRACT.md"
DOC = ROOT / "docs/io/ANIMO-IO02-CLOSEOUT.md"

STATUS = "CLOSEOUT_READY_BOUNDED_GENERAL_REPRESENTATION_QUALIFICATION_COMPLETE"
DECISION = (
    "QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_"
    "WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS"
)
UPSTREAM = "2bcf65360b08d278f28f1cc61ac96714db4793a3"
BASELINE = "06c0371b72df9415bc76562188b10266fc8826db"
RUN_ID = 34386275458
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
VFPROJ_SHA = "f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a"
DOC_SHA = "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"


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
qual = load(QUAL)
grammar = load(GRAMMAR)
for path in (CONTRACT, DOC):
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")

if closeout.get("work_unit") != "ANIMO-IO02":
    fail("closeout work_unit mismatch")
if closeout.get("status") != STATUS:
    fail("closeout status mismatch")
if closeout.get("decision") != DECISION:
    fail("closeout decision mismatch")
if qual.get("decision") != DECISION:
    fail("qualification and closeout decisions disagree")
if closeout.get("upstream_io01_head") != UPSTREAM:
    fail("IO01 upstream identity changed")
if closeout.get("qualification_baseline_head") != BASELINE:
    fail("qualification baseline head changed")

ci = closeout.get("qualification_baseline_ci", {})
if ci.get("run_id") != RUN_ID or ci.get("conclusion") != "success":
    fail("qualification baseline CI mismatch")
if ci.get("unit_tests") != 11:
    fail("qualification baseline unit-test count changed")
if ci.get("persisted_qualification_audit") != "PASS":
    fail("persisted qualification audit not recorded as PASS")

frozen = closeout.get("frozen_identity", {})
expected_frozen = {
    "revision_53_source_zip_sha256": SOURCE_SHA,
    "animo_testbank_sha256": TESTBANK_SHA,
    "animo_vfproj_sha256": VFPROJ_SHA,
    "documentation_sha256": DOC_SHA,
}
for key, expected in expected_frozen.items():
    if frozen.get(key) != expected:
        fail(f"frozen identity mismatch: {key}")
if frozen.get("frozen_bytes_modified") is not False:
    fail("closeout may not modify frozen bytes")

scope = closeout.get("qualified_scope", {})
if scope.get("family") != "GENERAL.INP":
    fail("closeout family changed")
if scope.get("source_revision") != 53 or scope.get("animo_version_branch") != 41:
    fail("source revision/version changed")
if scope.get("ghg_schema") is not False:
    fail("GHG schema must remain unqualified")
if scope.get("natural_non_ghg_files_qualified") != 7:
    fail("natural qualification count changed")
if scope.get("natural_non_ghg_files_examined") != 8:
    fail("natural non-GHG examined count changed")
if scope.get("ghg_natural_files_excluded") != 1:
    fail("GHG natural exclusion count changed")
if scope.get("mutation_probes") != 13:
    fail("mutation probe count changed")
if scope.get("typed_targets") != [
    "ModelConfiguration",
    "SimulationWindow",
    "DiagnosticsConfiguration",
]:
    fail("typed target boundary changed")

core = closeout.get("core_contract", {})
if core.get("top_level_complete_block_physical_order") != "NOT_AUTHORITATIVE_BECAUSE_FINDADR_REWINDS":
    fail("top-level physical-order finding changed")
if core.get("within_section_record_order") != "STRICT_SEQUENTIAL":
    fail("within-section strict ordering changed")
if core.get("free_order_property_bag") is not False:
    fail("free-order property bag may not be admitted")
if core.get("source_observed_defaults_only") is not True:
    fail("source-observed-default boundary changed")
if core.get("byte_round_trip_identity_claimed") is not False:
    fail("byte round-trip identity was not qualified")
if core.get("semantic_representation_equivalence") is not True:
    fail("semantic representation equivalence must remain qualified")
if core.get("blanket_numeric_tolerance") is not False:
    fail("blanket numeric tolerance may not be introduced")
if core.get("ttutil_numeric_or_scientific_authority") is not False:
    fail("TTUTIL may not become numeric/scientific authority")

negative = closeout.get("natural_evidence", {}).get("negative_sequence_evidence", {})
if negative.get("case") != "GrassPeat" or negative.get("error") != "9871":
    fail("GrassPeat negative evidence changed")
if negative.get("line") != 118 or negative.get("unexpected") != "WFPS=" or negative.get("expected") != "O2_content=":
    fail("GrassPeat sequence location/content changed")
if negative.get("admission") is not False:
    fail("GrassPeat may not be silently admitted")

ghg = closeout.get("natural_evidence", {}).get("scope_exclusion", {})
if ghg.get("case") != "GHGMais" or ghg.get("GreenHouseGasOption") != 1:
    fail("GHGMais scope evidence changed")

if len(closeout.get("explicit_hazard_exclusions", [])) != 6:
    fail("explicit hazard exclusions changed")

non_admissions = closeout.get("non_admissions", {})
required_false = [
    "production_input_migration",
    "GENERAL_grammar_redesign",
    "free_order_GENERAL",
    "silent_default_insertion_beyond_source",
    "GHGMais_schema_admission",
    "generic_GHG_schema_admission",
    "binary_hydrology",
    "INITIAL_migration",
    "restart_checkpoint_migration",
    "broad_IO01_reopen",
    "TTUTIL_scientific_authority",
    "TTUTIL_numeric_authority",
    "undefined_storage_normalized_to_values",
    "production_activation",
    "canonical_merge_admitted_by_IO02_alone",
]
for key in required_false:
    if non_admissions.get(key) is not False:
        fail(f"closeout non-admission {key} must remain false")

if grammar.get("normalized_representation", {}).get("not_a_free_order_property_bag") is not True:
    fail("grammar manifest no longer forbids free ordering")
if qual.get("qualified_natural_count") != 7:
    fail("qualification evidence no longer agrees with closeout")
if len(qual.get("mutation_probes", {})) != 13:
    fail("qualification mutation evidence no longer agrees with closeout")

closeout_doc = DOC.read_text(encoding="utf-8")
for token in (
    STATUS,
    DECISION,
    str(RUN_ID),
    "GrassPeat",
    "GHGMais",
    "not a free-order key/value object",
    "production input migration",
):
    if token not in closeout_doc:
        fail(f"closeout doc lost required token: {token}")

print(
    "PASS: ANIMO-IO02 closeout reconciled; bounded GENERAL representation qualified, "
    "strict sequential semantics and hazard exclusions preserved, no production migration admitted"
)
