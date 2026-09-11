#!/usr/bin/env python3
"""Fail-closed architecture and scope validator for ANIMO-TB01."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "94afe7d649a8c60758a41996f0059de0acddd2fc"
FINAL_STATE = "QUALIFIED_ANIMO5_SCIENTIFIC_TESTBANK_ARCHITECTURE_READY_FOR_INCREMENTAL_IMPLEMENTATION_NO_WHOLE_MODEL_GOLDEN_BASELINE"

REQUIRED_FILES = {
    "docs/testing/ANIMO_TESTBANK_ARCHITECTURE.md",
    "docs/testing/ANIMO_TESTBANK_MIGRATION_PLAN.md",
    "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json",
    "integration/animo-testbank/ANIMO_TESTBANK_COVERAGE_MATRIX.json",
    "integration/animo-testbank/ANIMO_TESTBANK_EXPECTATION_PROVENANCE.json",
    "integration/animo-testbank/ANIMO_TESTBANK_EXECUTION_PROFILES.json",
    "integration/animo-testbank/ANIMO-TB01_STATUS.json",
    "tools/validate_animo_tb01_architecture.py",
    ".github/workflows/animo-tb01-testbank-architecture.yml",
}
LEVELS = {"UT", "CT", "IT", "INV", "RR", "QG"}
COSTS = {"FAST", "FOCUSED", "BROAD", "QUALIFICATION"}
PROVENANCE = {"ANALYTICAL", "THEORY", "FROZEN_LEGACY", "CORRECTED_LEGACY_REFERENCE", "QUALIFIED_GOLDEN_CASE", "INVARIANT", "UNKNOWN"}
SYNTHETIC_ORIGIN = "QUALIFIED_SYNTHETIC_ORACLE"
LAYERS = {f"TB-L{i}" for i in range(13)}
STATE_CLASSES = {"PERSISTENT_STATE", "DETERMINISTIC_RECONSTRUCTION", "EPHEMERAL_WORKSPACE", "DERIVED_DIAGNOSTIC"}
COMPARISONS = {"BIT_EXACT", "TEXT_NORMALIZED_EXACT", "INTEGER_EXACT", "ABS_REL_TOLERANCE", "DOMAIN_SPECIFIC_NUMERICAL_CONTRACT"}
FAILURES = {"SCIENTIFIC_IDENTITY_FAILURE", "MASS_CONSERVATION_FAILURE", "SPECIES_OWNERSHIP_FAILURE", "STATE_RESTART_FAILURE", "BOUNDARY_CONTRACT_FAILURE", "NUMERICAL_POLICY_FAILURE", "ARCHITECTURE_INVARIANT_FAILURE", "PROVENANCE_FAILURE", "REGRESSION_UNEXPECTED_DIFFERENCE", "TOOLING_FAILURE"}
ASSET_CLASSES = {"REUSE_AS_TEST", "REUSE_AS_ORACLE", "REUSE_AS_FIXTURE", "REUSE_AS_RUNNER", "REUSE_AS_VALIDATOR", "REUSE_AS_PROVENANCE", "HISTORICAL_EVIDENCE_ONLY", "SUPERSEDED", "GAP"}
SUBSYSTEMS = {"NITROGEN", "PHOSPHORUS", "CARBON_ORGANIC_MATTER", "DOM", "PLANT_CROP_UPTAKE", "SORPTION", "TRANSPORT", "MACROPORES", "GHG"}
COVERAGE_DIMS = {"process", "species", "element", "state_owner", "boundary", "restart", "branch_domain", "numerical_policy", "subsystem_interaction", "admitted_tcd_regression"}
PROFILE_NAMES = {"DEVELOPER_FAST", "SCIENTIFIC_FOCUSED", "CANONICAL_BROAD", "ADMISSION_QUALIFICATION", "RELEASE", "DEEP_AUDIT"}
ID_RE = re.compile(r"^ATB-(PROV|ORACLE|SPC|CONS|TRN|STATE|BND|SUB|INT|REG|NUM|ARCH|REL)-[0-9]{3}$")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def load(path: str) -> dict:
    p = ROOT / path
    require(p.is_file(), f"missing {path}")
    try:
        value = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"invalid JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"top level must be object: {path}")
    return value


def validate_files() -> None:
    missing = sorted(p for p in REQUIRED_FILES if not (ROOT / p).is_file())
    require(not missing, f"missing deliverables: {missing}")


def validate_registry(reg: dict, exp: dict) -> None:
    require(reg.get("architecture_base") == f"ANIMO-RG05I@{BASE}", "registry authority base mismatch")
    require(set(reg["legacy_taxonomy"]["test_levels"]) == LEVELS, "historical test-level taxonomy changed")
    require(set(reg["legacy_taxonomy"]["cost_classes"]) == COSTS, "historical cost taxonomy changed")
    cv = reg["controlled_vocabularies"]
    require(set(cv["state_class"]) == STATE_CLASSES, "state taxonomy incomplete")
    require(set(cv["comparison_policy"]) == COMPARISONS, "comparison-policy taxonomy incomplete")
    require(set(cv["failure_class"]) == FAILURES, "failure taxonomy incomplete")
    require(set(cv["asset_classification"]) == ASSET_CLASSES, "asset classification vocabulary changed")
    require({x["layer"] for x in reg.get("layers", [])} == LAYERS, "TB-L0 through TB-L12 not all defined")
    require(SUBSYSTEMS <= {x["subsystem"] for x in reg.get("subsystem_registry", [])}, "required scientific subsystems missing")

    tests = reg.get("test_registry", [])
    require(len(tests) >= 12, "test registry is future-only or too small")
    ids = [x.get("test_id") for x in tests]
    require(len(ids) == len(set(ids)), "duplicate stable test IDs")
    for test in tests:
        tid = test.get("test_id", "")
        require(bool(ID_RE.fullmatch(tid)), f"bad test ID {tid}")
        require(test.get("level") in LEVELS, f"bad level {tid}")
        require(test.get("cost_class") in COSTS, f"bad cost class {tid}")
        require(test.get("layer") in LAYERS, f"bad layer {tid}")
        require(test.get("comparison_policy") in COMPARISONS, f"comparison policy missing {tid}")
        require(bool(test.get("source_identity")), f"source identity missing {tid}")
        require(bool(test.get("input_identity")), f"input identity missing {tid}")
        value_origin = test.get("expected_value_provenance")
        require(bool(value_origin), f"expectation provenance missing {tid}")
        if value_origin not in PROVENANCE:
            require(value_origin == SYNTHETIC_ORIGIN and tid.startswith("ATB-ORACLE-") and "SYNQ" in test.get("source_identity", ""), f"uncontrolled provenance/origin {tid}:{value_origin}")
        if value_origin == "UNKNOWN":
            require(not ({"ADMISSION", "RELEASE"} & set(test.get("blocks", []))), f"UNKNOWN used as qualification truth {tid}")
        if value_origin == "FROZEN_LEGACY":
            require("BEHAVIOURAL" in test.get("qualification_strength", ""), f"legacy output mislabeled scientific {tid}")
        if test.get("comparison_policy") == "ABS_REL_TOLERANCE":
            require(bool(test.get("tolerance_justification")), f"tolerance lacks justification {tid}")

    assets = reg.get("existing_asset_inventory", [])
    require(len(assets) >= 50, f"existing evidence inventory not meaningful: {len(assets)}")
    for asset in assets:
        require(asset.get("classification") in ASSET_CLASSES, f"bad asset classification {asset.get('asset_id')}")
        for field in ("path_or_authority", "scientific_scope", "evidence_strength", "permanence_recommendation", "migration_action", "known_limitations"):
            require(bool(asset.get(field)), f"asset {asset.get('asset_id')} missing {field}")

    whole = exp["baseline_availability"]["COMPOSED_WHOLE_MODEL_GOLDEN_BASELINE"]
    require(whole.get("status") == "UNAVAILABLE_NOT_AUTHORIZED", "whole-model golden baseline claimed")
    require(whole.get("machine_usable_for_qualification") is False, "unavailable whole-model baseline made qualification truth")


def validate_expectations(exp: dict) -> None:
    require(set(exp.get("expected_value_taxonomy", [])) == PROVENANCE, "expected-value taxonomy not preserved")
    require(set(exp.get("oracle_origin_extensions", [])) == {SYNTHETIC_ORIGIN}, "qualified synthetic oracle origin missing")
    rules = exp.get("governance_rules", {})
    for key in ("numerical_expectation_requires_provenance", "numerical_expectation_requires_authority", "numerical_expectation_requires_source_and_input_identity", "numerical_expectation_requires_comparison_policy"):
        require(rules.get(key) is True, f"expectation rule not fail-closed: {key}")
    for key in ("UNKNOWN_may_serve_as_qualification_oracle", "captured_output_automatically_becomes_golden", "FROZEN_LEGACY_automatically_scientific", "synthetic_oracle_may_be_counted_as_historical_B2"):
        require(rules.get(key) is False, f"forbidden expectation promotion enabled: {key}")
    syn = exp.get("synthetic_oracle_policy", {})
    require(syn.get("must_remain_explicitly_synthetic") is True, "synthetic status can be lost")
    require(syn.get("may_be_relabelled_historical_B2") is False, "synthetic evidence can fabricate B2")


def validate_coverage(cov: dict) -> None:
    model = cov.get("coverage_model", {})
    require(model.get("source_code_line_coverage_is_primary") is False, "raw line coverage made scientific completeness metric")
    require(set(model.get("dimensions", [])) == COVERAGE_DIMS, "multidimensional scientific coverage incomplete")
    require(set(model.get("supplemental_dimensions", [])) == {"source_code_line_coverage"}, "line coverage not supplemental only")
    allowed = set(model.get("allowed_status", []))
    rows = cov.get("rows", [])
    require(SUBSYSTEMS <= {r.get("subsystem") for r in rows}, "coverage matrix omits required subsystem")
    for row in rows:
        for dim in COVERAGE_DIMS:
            require(row.get(dim) in allowed, f"invalid coverage cell {row.get('subsystem')}:{dim}")
    rules = cov.get("coverage_rules", {})
    require(rules.get("whole_profile_balance_may_hide_local_compensating_errors") is False, "profile balance may hide local compensation")
    require(rules.get("subsystem_restart_may_claim_whole_model_restart") is False, "subsystem restart can imply whole-model restart")


def validate_profiles(profiles: dict) -> None:
    require(set(profiles.get("historical_cost_classes", [])) == COSTS, "profiles renamed historical costs")
    items = profiles.get("profiles", [])
    require({p.get("profile") for p in items} == PROFILE_NAMES, "execution profiles incomplete")
    for profile in items:
        require(profile.get("primary_cost_class") in COSTS, f"profile lacks historical cost mapping {profile.get('profile')}")
        if profile.get("profile") != "DEVELOPER_FAST":
            require(profile.get("immutable_identity_required") is True, f"qualification-capable profile lacks immutable identities {profile.get('profile')}")
    release = next(p for p in items if p["profile"] == "RELEASE")
    require(release.get("availability") == "FUTURE_ONLY_NOT_AUTHORIZED_BY_TB01", "release profile prematurely opened")
    gates = {g["gate"]: g for g in profiles.get("gate_requirements", [])}
    gov = gates["GOV05_SINGLE_AGENT_ADVERSARIAL_REVIEW"]
    require(gov.get("evidence_resolution_mode") == "VERIFY_AND_REUSE", "GOV05 does not use VERIFY_AND_REUSE")
    require("NOT_INDEPENDENT" in gov.get("assurance_note", ""), "same-agent review assurance overstated")
    require(gates["ATOMIC_B3_ADMISSION"].get("opened_by_tb01") is False, "TB01 opened B3 admission")
    require(gates["COMPOSITION"].get("opened_by_tb01") is False, "TB01 performed/opened composition")
    require(gates["B4"].get("availability") == "CLOSED", "TB01 opened B4")
    require(gates["PRODUCTION_RELEASE"].get("availability") == "CLOSED", "TB01 opened production release")
    receipt_required = {"source_head", "source_tree", "compiler_or_tool_identity", "testbank_manifest_identity", "testcase_and_input_hashes", "selected_test_ids", "comparison_policies", "result_artifact_hashes", "upstream_authority_pins", "qualification_decision"}
    require(receipt_required <= set(profiles.get("qualification_evidence_receipt", {}).get("required_fields", [])), "qualification receipt lacks immutable evidence fields")


def validate_status(status: dict, reg: dict) -> None:
    require(status.get("state") == FINAL_STATE and status.get("decision") == FINAL_STATE, "wrong bounded TB01 decision")
    require(status.get("architecture_base") == f"ANIMO-RG05I@{BASE}", "status authority base mismatch")
    arch = status.get("architecture", {})
    require(arch.get("layer_count") == 13, "status layer count wrong")
    require(arch.get("existing_assets_inventoried") == len(reg.get("existing_asset_inventory", [])), "asset count mismatch")
    require(arch.get("state_restart_first_class") is True and arch.get("species_cnp_first_class") is True, "state or C/N/P ownership is not first-class")
    require(arch.get("raw_line_coverage_primary") is False, "status makes raw coverage primary")
    require(arch.get("gov05_integration") == "VERIFY_AND_REUSE", "status GOV05 integration wrong")
    require(status.get("expected_value_governance", {}).get("composed_whole_model_golden_baseline") == "UNAVAILABLE_NOT_AUTHORIZED", "status claims composed golden baseline")
    require(status.get("authority_reconciliation", {}).get("GOV05_assurance") == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "GOV05 same-agent assurance misstated")
    require(status.get("frozen_b0_identities", {}).get("external_controlled_immutable_storage_proven") is False, "unproven B0 custody overstated")
    hard = status.get("hard_boundaries", {})
    require(hard and all(value is False for value in hard.values()), f"hard boundary violated {hard}")
    require(status.get("next_workunits_started_by_tb01") is False, "TB01 started a follow-on workunit")
    require(status.get("validation", {}).get("exact_final_head_ci_required") is True, "exact-final-head CI not required")


def validate_docs() -> None:
    arch = (ROOT / "docs/testing/ANIMO_TESTBANK_ARCHITECTURE.md").read_text(encoding="utf-8")
    migration = (ROOT / "docs/testing/ANIMO_TESTBANK_MIGRATION_PLAN.md").read_text(encoding="utf-8")
    terms = ["TB-L0", "TB-L12", "C/N/P", "PERSISTENT_STATE", "EPHEMERAL_WORKSPACE", "FROZEN_LEGACY_BEHAVIOUR", "SCIENTIFICALLY_QUALIFIED_EXPECTED_BEHAVIOUR", "COMPOSED_WHOLE_MODEL_GOLDEN_BASELINE", "VERIFY_AND_REUSE", "not genuinely independent", "BIT_EXACT", "ABS_REL_TOLERANCE", "DOMAIN_SPECIFIC_NUMERICAL_CONTRACT"]
    require(not [t for t in terms if t not in arch], "architecture document missing required semantics")
    for phase in ("TB1", "TB2", "TB3", "TB4", "TB5", "TB6", "TB7", "TB8"):
        require(phase in arch, f"roadmap missing {phase}")
    require("adapter-first" in migration.lower(), "migration is not adapter-first")
    require("central registry" in migration.lower(), "parallel central-registry integration rule missing")


def validate_scope() -> None:
    subprocess.run(["git", "cat-file", "-e", f"{BASE}^{{commit}}"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = subprocess.run(["git", "diff", "--name-only", f"{BASE}..HEAD"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    changed = [p for p in result.stdout.splitlines() if p]
    require(changed, "no TB01 changes found")
    exact = {"docs/testing/ANIMO_TESTBANK_ARCHITECTURE.md", "docs/testing/ANIMO_TESTBANK_MIGRATION_PLAN.md", "tools/validate_animo_tb01_architecture.py", ".github/workflows/animo-tb01-testbank-architecture.yml"}
    prefixes = ("integration/animo-testbank/", "tests/bank/")
    forbidden = [p for p in changed if p not in exact and not p.startswith(prefixes)]
    require(not forbidden, f"scope guard rejects changed paths: {forbidden}")
    historical = ("integration/animo-prep/", "integration/animo-synthetic/", "integration/animo-state/", "integration/animo-mass/", "integration/animo-eg/", "integration/animo-b3/", "integration/animo-governance/", "integration/animo-reg/")
    require(not any(p.startswith(historical) for p in changed), "finalized historical authority/evidence rewritten")
    production = ("src/", "source/", "animo/", "model/", "fortran/")
    require(not any(p.startswith(production) for p in changed), "production scientific source modified")
    print(f"scope guard PASS: {len(changed)} TB01-bounded changed files")


def main() -> int:
    validate_files()
    reg = load("integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json")
    cov = load("integration/animo-testbank/ANIMO_TESTBANK_COVERAGE_MATRIX.json")
    exp = load("integration/animo-testbank/ANIMO_TESTBANK_EXPECTATION_PROVENANCE.json")
    profiles = load("integration/animo-testbank/ANIMO_TESTBANK_EXECUTION_PROFILES.json")
    status = load("integration/animo-testbank/ANIMO-TB01_STATUS.json")
    validate_expectations(exp)
    validate_registry(reg, exp)
    validate_coverage(cov)
    validate_profiles(profiles)
    validate_status(status, reg)
    validate_docs()
    validate_scope()
    print(f"ANIMO-TB01 validation PASS: {len(reg['test_registry'])} shared test entries; {len(reg['existing_asset_inventory'])} existing assets inventoried")
    print(FINAL_STATE)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print(f"ANIMO-TB01 validation FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
