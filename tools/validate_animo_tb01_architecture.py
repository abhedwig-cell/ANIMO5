#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-TB01.

This validator qualifies the testbank architecture and its migration metadata only.
It deliberately does not execute or admit scientific production changes.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "94afe7d649a8c60758a41996f0059de0acddd2fc"
FINAL_STATE = (
    "QUALIFIED_ANIMO5_SCIENTIFIC_TESTBANK_ARCHITECTURE_READY_FOR_"
    "INCREMENTAL_IMPLEMENTATION_NO_WHOLE_MODEL_GOLDEN_BASELINE"
)

REQUIRED_FILES = [
    "docs/testing/ANIMO_TESTBANK_ARCHITECTURE.md",
    "docs/testing/ANIMO_TESTBANK_MIGRATION_PLAN.md",
    "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json",
    "integration/animo-testbank/ANIMO_TESTBANK_COVERAGE_MATRIX.json",
    "integration/animo-testbank/ANIMO_TESTBANK_EXPECTATION_PROVENANCE.json",
    "integration/animo-testbank/ANIMO_TESTBANK_EXECUTION_PROFILES.json",
    "integration/animo-testbank/ANIMO-TB01_STATUS.json",
    "tools/validate_animo_tb01_architecture.py",
    ".github/workflows/animo-tb01-testbank-architecture.yml",
]

EXPECTED_LEVELS = {"UT", "CT", "IT", "INV", "RR", "QG"}
EXPECTED_COSTS = {"FAST", "FOCUSED", "BROAD", "QUALIFICATION"}
EXPECTED_PROVENANCE = {
    "ANALYTICAL",
    "THEORY",
    "FROZEN_LEGACY",
    "CORRECTED_LEGACY_REFERENCE",
    "QUALIFIED_GOLDEN_CASE",
    "INVARIANT",
    "UNKNOWN",
}
ORACLE_ORIGIN_EXTENSIONS = {"QUALIFIED_SYNTHETIC_ORACLE"}
EXPECTED_LAYERS = {f"TB-L{i}" for i in range(13)}
EXPECTED_STATE_CLASSES = {
    "PERSISTENT_STATE",
    "DETERMINISTIC_RECONSTRUCTION",
    "EPHEMERAL_WORKSPACE",
    "DERIVED_DIAGNOSTIC",
}
EXPECTED_COMPARISONS = {
    "BIT_EXACT",
    "TEXT_NORMALIZED_EXACT",
    "INTEGER_EXACT",
    "ABS_REL_TOLERANCE",
    "DOMAIN_SPECIFIC_NUMERICAL_CONTRACT",
}
EXPECTED_FAILURES = {
    "SCIENTIFIC_IDENTITY_FAILURE",
    "MASS_CONSERVATION_FAILURE",
    "SPECIES_OWNERSHIP_FAILURE",
    "STATE_RESTART_FAILURE",
    "BOUNDARY_CONTRACT_FAILURE",
    "NUMERICAL_POLICY_FAILURE",
    "ARCHITECTURE_INVARIANT_FAILURE",
    "PROVENANCE_FAILURE",
    "REGRESSION_UNEXPECTED_DIFFERENCE",
    "TOOLING_FAILURE",
}
ASSET_CLASSES = {
    "REUSE_AS_TEST",
    "REUSE_AS_ORACLE",
    "REUSE_AS_FIXTURE",
    "REUSE_AS_RUNNER",
    "REUSE_AS_VALIDATOR",
    "REUSE_AS_PROVENANCE",
    "HISTORICAL_EVIDENCE_ONLY",
    "SUPERSEDED",
    "GAP",
}
REQUIRED_SUBSYSTEMS = {
    "NITROGEN",
    "PHOSPHORUS",
    "CARBON_ORGANIC_MATTER",
    "DOM",
    "PLANT_CROP_UPTAKE",
    "SORPTION",
    "TRANSPORT",
    "MACROPORES",
    "GHG",
}
COVERAGE_DIMENSIONS = {
    "process",
    "species",
    "element",
    "state_owner",
    "boundary",
    "restart",
    "branch_domain",
    "numerical_policy",
    "subsystem_interaction",
    "admitted_tcd_regression",
}
PROFILES = {
    "DEVELOPER_FAST",
    "SCIENTIFIC_FOCUSED",
    "CANONICAL_BROAD",
    "ADMISSION_QUALIFICATION",
    "RELEASE",
    "DEEP_AUDIT",
}
ID_RE = re.compile(r"^ATB-(PROV|ORACLE|SPC|CONS|TRN|STATE|BND|SUB|INT|REG|NUM|ARCH|REL)-[0-9]{3}$")

ALLOWED_CHANGED_EXACT = {
    "docs/testing/ANIMO_TESTBANK_ARCHITECTURE.md",
    "docs/testing/ANIMO_TESTBANK_MIGRATION_PLAN.md",
    "tools/validate_animo_tb01_architecture.py",
    ".github/workflows/animo-tb01-testbank-architecture.yml",
}
ALLOWED_CHANGED_PREFIXES = ("integration/animo-testbank/", "tests/bank/")


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: str) -> dict:
    p = ROOT / path
    if not p.is_file():
        fail(f"missing required JSON: {path}")
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(obj, dict):
        fail(f"top-level JSON must be object: {path}")
    return obj


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_required_files() -> None:
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    require(not missing, f"missing required deliverables: {missing}")


def validate_registry(reg: dict, exp: dict) -> None:
    require(reg.get("architecture_base") == f"ANIMO-RG05I@{BASE}", "wrong architecture base")
    require(set(reg["legacy_taxonomy"]["test_levels"]) == EXPECTED_LEVELS, "legacy UT/CT/IT/INV/RR/QG taxonomy changed")
    require(set(reg["legacy_taxonomy"]["cost_classes"]) == EXPECTED_COSTS, "legacy FAST/FOCUSED/BROAD/QUALIFICATION costs changed")
    require(set(reg["controlled_vocabularies"]["state_class"]) == EXPECTED_STATE_CLASSES, "state classes incomplete")
    require(set(reg["controlled_vocabularies"]["comparison_policy"]) == EXPECTED_COMPARISONS, "comparison policies incomplete")
    require(set(reg["controlled_vocabularies"]["failure_class"]) == EXPECTED_FAILURES, "failure classes incomplete")
    require(set(reg["controlled_vocabularies"]["asset_classification"]) == ASSET_CLASSES, "asset vocabulary changed")

    layers = {x.get("layer") for x in reg.get("layers", [])}
    require(layers == EXPECTED_LAYERS, f"test layers incomplete: {layers}")

    subsystems = {x.get("subsystem") for x in reg.get("subsystem_registry", [])}
    require(REQUIRED_SUBSYSTEMS <= subsystems, f"required subsystems absent: {REQUIRED_SUBSYSTEMS - subsystems}")

    tests = reg.get("test_registry", [])
    require(len(tests) >= 12, "registry is an empty/future-only design")
    ids = [t.get("test_id") for t in tests]
    require(len(ids) == len(set(ids)), "duplicate ATB test IDs")
    for t in tests:
        tid = t.get("test_id", "")
        require(bool(ID_RE.fullmatch(tid)), f"invalid stable test id: {tid}")
        require(t.get("level") in EXPECTED_LEVELS, f"invalid test level: {tid}")
        require(t.get("cost_class") in EXPECTED_COSTS, f"invalid cost class: {tid}")
        require(t.get("layer") in EXPECTED_LAYERS, f"invalid layer: {tid}")
        require(t.get("comparison_policy") in EXPECTED_COMPARISONS, f"comparison policy missing/invalid: {tid}")
        require(bool(t.get("source_identity")), f"source identity missing: {tid}")
        require(bool(t.get("input_identity")), f"input identity missing: {tid}")
        prov = t.get("expected_value_provenance")
        require(bool(prov), f"expected-value provenance missing: {tid}")
        if prov not in EXPECTED_PROVENANCE:
            require(
                prov in ORACLE_ORIGIN_EXTENSIONS and tid.startswith("ATB-ORACLE-") and "SYNQ" in t.get("source_identity", ""),
                f"uncontrolled expected-value provenance/oracle origin: {tid}:{prov}",
            )
        if prov == "UNKNOWN":
            blocks = set(t.get("blocks", []))
            require(not ({"ADMISSION", "RELEASE"} & blocks), f"UNKNOWN used as qualification truth: {tid}")
        if t.get("comparison_policy") == "ABS_REL_TOLERANCE":
            require(bool(t.get("tolerance_justification")), f"tolerance without scientific/numerical justification: {tid}")
        if t.get("expected_value_provenance") == "FROZEN_LEGACY":
            require("BEHAVIOURAL" in t.get("qualification_strength", ""), f"frozen legacy mislabeled as scientific truth: {tid}")

    assets = reg.get("existing_asset_inventory", [])
    require(len(assets) >= 50, f"inventory too small to be meaningful: {len(assets)}")
    for a in assets:
        require(a.get("classification") in ASSET_CLASSES, f"uncontrolled asset classification: {a.get('asset_id')}")
        for field in ("path_or_authority", "scientific_scope", "evidence_strength", "permanence_recommendation", "migration_action", "known_limitations"):
            require(bool(a.get(field)), f"asset {a.get('asset_id')} missing {field}")

    baseline = exp["baseline_availability"]
    require(
        baseline["COMPOSED_WHOLE_MODEL_GOLDEN_BASELINE"]["status"] == "UNAVAILABLE_NOT_AUTHORIZED",
        "whole-model golden baseline was prematurely claimed",
    )
    require(not baseline["COMPOSED_WHOLE_MODEL_GOLDEN_BASELINE"]["machine_usable_for_qualification"], "unavailable whole-model baseline made usable")


def validate_expectations(exp: dict) -> None:
    require(set(exp.get("expected_value_taxonomy", [])) == EXPECTED_PROVENANCE, "historical expected-value taxonomy not preserved")
    require(set(exp.get("oracle_origin_extensions", [])) == ORACLE_ORIGIN_EXTENSIONS, "synthetic oracle origin missing")
    rules = exp.get("governance_rules", {})
    require(rules.get("numerical_expectation_requires_provenance") is True, "numerical provenance is not mandatory")
    require(rules.get("UNKNOWN_may_serve_as_qualification_oracle") is False, "UNKNOWN may serve as qualification oracle")
    require(rules.get("FROZEN_LEGACY_automatically_scientific") is False, "frozen legacy promoted to science")
    require(rules.get("captured_output_automatically_becomes_golden") is False, "captured output may become golden")
    require(rules.get("synthetic_oracle_may_be_counted_as_historical_B2") is False, "synthetic oracle may fabricate B2")
    syn = exp.get("synthetic_oracle_policy", {})
    require(syn.get("must_remain_explicitly_synthetic") is True, "synthetic status can be lost")
    require(syn.get("may_be_relabelled_historical_B2") is False, "synthetic oracle relabeling as B2 allowed")


def validate_coverage(cov: dict) -> None:
    model = cov.get("coverage_model", {})
    require(model.get("source_code_line_coverage_is_primary") is False, "raw source coverage made primary")
    require(set(model.get("dimensions", [])) == COVERAGE_DIMENSIONS, "scientific coverage dimensions incomplete")
    require(set(model.get("supplemental_dimensions", [])) == {"source_code_line_coverage"}, "line coverage not isolated as supplemental")
    rows = cov.get("rows", [])
    row_names = {r.get("subsystem") for r in rows}
    require(REQUIRED_SUBSYSTEMS <= row_names, f"coverage missing subsystems: {REQUIRED_SUBSYSTEMS-row_names}")
    allowed = set(model.get("allowed_status", []))
    for r in rows:
        for dim in COVERAGE_DIMENSIONS:
            require(r.get(dim) in allowed, f"invalid/missing coverage {r.get('subsystem')}:{dim}")
    require(any(r.get("subsystem") == "MACROPORES" for r in rows), "macropore coverage absent")
    require(any(r.get("subsystem") == "GHG" for r in rows), "GHG coverage absent")
    require(cov.get("coverage_rules", {}).get("whole_profile_balance_may_hide_local_compensating_errors") is False, "local balance errors may be hidden")
    require(cov.get("coverage_rules", {}).get("subsystem_restart_may_claim_whole_model_restart") is False, "subsystem restart may imply whole model")


def validate_profiles(profiles: dict) -> None:
    require(set(profiles.get("historical_cost_classes", [])) == EXPECTED_COSTS, "execution profiles rename historical costs")
    items = profiles.get("profiles", [])
    names = {p.get("profile") for p in items}
    require(names == PROFILES, f"execution profiles incomplete: {names}")
    for p in items:
        require(p.get("primary_cost_class") in EXPECTED_COSTS, f"profile cost mapping invalid: {p.get('profile')}")
        if p.get("profile") in {"SCIENTIFIC_FOCUSED", "CANONICAL_BROAD", "ADMISSION_QUALIFICATION", "RELEASE", "DEEP_AUDIT"}:
            require(p.get("immutable_identity_required") is True, f"qualification-capable profile lacks immutable identities: {p.get('profile')}")
    release = next(p for p in items if p["profile"] == "RELEASE")
    require(release.get("availability") == "FUTURE_ONLY_NOT_AUTHORIZED_BY_TB01", "release prematurely opened")
    gates = {g.get("gate"): g for g in profiles.get("gate_requirements", [])}
    require(gates["GOV05_SINGLE_AGENT_ADVERSARIAL_REVIEW"].get("evidence_resolution_mode") == "VERIFY_AND_REUSE", "GOV05 integration does not use VERIFY_AND_REUSE")
    require("NOT_INDEPENDENT" in gates["GOV05_SINGLE_AGENT_ADVERSARIAL_REVIEW"].get("assurance_note", ""), "same-agent review independence caveat missing")
    require(gates["ATOMIC_B3_ADMISSION"].get("opened_by_tb01") is False, "TB01 opened admission")
    require(gates["COMPOSITION"].get("opened_by_tb01") is False, "TB01 opened composition")
    require(gates["B4"].get("availability") == "CLOSED", "TB01 opened B4")
    require(gates["PRODUCTION_RELEASE"].get("availability") == "CLOSED", "TB01 opened production release")
    receipt = profiles.get("qualification_evidence_receipt", {})
    required_receipt = {
        "source_head", "source_tree", "compiler_or_tool_identity", "testbank_manifest_identity",
        "testcase_and_input_hashes", "selected_test_ids", "comparison_policies",
        "result_artifact_hashes", "upstream_authority_pins", "qualification_decision",
    }
    require(required_receipt <= set(receipt.get("required_fields", [])), "qualification receipt lacks immutable identity/result fields")


def validate_status(status: dict, reg: dict) -> None:
    require(status.get("state") == FINAL_STATE, "wrong final state")
    require(status.get("decision") == FINAL_STATE, "wrong final decision")
    require(status.get("architecture_base") == f"ANIMO-RG05I@{BASE}", "status base mismatch")
    require(status.get("architecture", {}).get("existing_assets_inventoried") == len(reg.get("existing_asset_inventory", [])), "status inventory count mismatch")
    require(status.get("architecture", {}).get("layer_count") == 13, "status layer count mismatch")
    require(status.get("architecture", {}).get("state_restart_first_class") is True, "state/restart not first-class")
    require(status.get("architecture", {}).get("species_cnp_first_class") is True, "C/N/P ownership not first-class")
    require(status.get("architecture", {}).get("raw_line_coverage_primary") is False, "raw line coverage marked primary")
    require(status.get("architecture", {}).get("gov05_integration") == "VERIFY_AND_REUSE", "status GOV05 integration mismatch")
    require(status.get("expected_value_governance", {}).get("composed_whole_model_golden_baseline") == "UNAVAILABLE_NOT_AUTHORIZED", "status claims whole-model baseline")
    require(status.get("authority_reconciliation", {}).get("GOV05_assurance") == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "GOV05 assurance misstated")
    require(status.get("frozen_b0_identities", {}).get("external_controlled_immutable_storage_proven") is False, "unproven B0 custody overstated")
    hard = status.get("hard_boundaries", {})
    require(hard and all(v is False for v in hard.values()), f"hard boundary violated: {hard}")
    require(status.get("next_workunits_started_by_tb01") is False, "TB01 automatically started later workunit")
    require(status.get("validation", {}).get("exact_final_head_ci_required") is True, "exact-final-head CI not mandatory")


def validate_docs() -> None:
    arch = (ROOT / "docs/testing/ANIMO_TESTBANK_ARCHITECTURE.md").read_text(encoding="utf-8")
    mig = (ROOT / "docs/testing/ANIMO_TESTBANK_MIGRATION_PLAN.md").read_text(encoding="utf-8")
    required_arch_terms = [
        "TB-L0", "TB-L12", "C/N/P", "PERSISTENT_STATE", "EPHEMERAL_WORKSPACE",
        "FROZEN_LEGACY_BEHAVIOUR", "SCIENTIFICALLY_QUALIFIED_EXPECTED_BEHAVIOUR",
        "COMPOSED_WHOLE_MODEL_GOLDEN_BASELINE", "VERIFY_AND_REUSE", "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT",
        "BIT_EXACT", "ABS_REL_TOLERANCE", "DOMAIN_SPECIFIC_NUMERICAL_CONTRACT",
    ]
    missing = [x for x in required_arch_terms if x not in arch]
    require(not missing, f"architecture document missing required semantics: {missing}")
    for phase in ("TB1", "TB2", "TB3", "TB4", "TB5", "TB6", "TB7", "TB8"):
        require(phase in arch, f"roadmap missing phase {phase}")
    require("adapter-first" in mig.lower(), "migration is not adapter-first")
    require("central registry" in mig.lower(), "parallel registry integration mechanism missing")


def validate_scope_guard() -> None:
    try:
        subprocess.run(["git", "cat-file", "-e", f"{BASE}^{{commit}}"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cp = subprocess.run(["git", "diff", "--name-only", f"{BASE}..HEAD"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as exc:
        fail(f"scope guard could not inspect git history: {exc.stderr}")
    changed = [x.strip() for x in cp.stdout.splitlines() if x.strip()]
    require(changed, "scope guard found no TB01 changes")
    forbidden = []
    for path in changed:
        allowed = path in ALLOWED_CHANGED_EXACT or path.startswith(ALLOWED_CHANGED_PREFIXES)
        if not allowed:
            forbidden.append(path)
    require(not forbidden, f"scope guard: forbidden paths changed: {forbidden}")

    production_prefixes = ("src/", "source/", "animo/", "model/", "fortran/")
    require(not any(p.startswith(production_prefixes) for p in changed), "production scientific source modified")
    finalized_prefixes = (
        "integration/animo-prep/", "integration/animo-synthetic/", "integration/animo-state/",
        "integration/animo-mass/", "integration/animo-eg/", "integration/animo-b3/",
        "integration/animo-governance/", "integration/animo-reg/",
    )
    require(not any(p.startswith(finalized_prefixes) for p in changed), "finalized historical authority/evidence rewritten")
    print(f"scope guard PASS: {len(changed)} changed files, all TB01-bounded")


def main() -> int:
    validate_required_files()
    reg = load_json("integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json")
    cov = load_json("integration/animo-testbank/ANIMO_TESTBANK_COVERAGE_MATRIX.json")
    exp = load_json("integration/animo-testbank/ANIMO_TESTBANK_EXPECTATION_PROVENANCE.json")
    profiles = load_json("integration/animo-testbank/ANIMO_TESTBANK_EXECUTION_PROFILES.json")
    status = load_json("integration/animo-testbank/ANIMO-TB01_STATUS.json")

    validate_expectations(exp)
    validate_registry(reg, exp)
    validate_coverage(cov)
    validate_profiles(profiles)
    validate_status(status, reg)
    validate_docs()
    validate_scope_guard()

    print(f"ANIMO-TB01 validation PASS: {len(reg['test_registry'])} shared test entries, {len(reg['existing_asset_inventory'])} existing assets inventoried")
    print(FINAL_STATE)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(f"ANIMO-TB01 validation FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
