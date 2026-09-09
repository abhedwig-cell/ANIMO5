#!/usr/bin/env python3
"""Static validation for ANIMO-B3Q01 governance artifacts."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "integration/animo-b3/B3_DISPOSITION_SCHEMA.json"
CLASSIFICATION_PATH = ROOT / "integration/animo-b3/B3_EXISTING_TCD_CLASSIFICATION.csv"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3Q01_STATUS.json"

EXPECTED_TCDS = {
    "TCD-014", "TCD-015", "TCD-016", "TCD-017", "TCD-018", "TCD-019",
    "TCD-023", "TCD-024", "TCD-025", "TCD-026", "TCD-027",
}
EXPECTED_CLASSES = {"A", "B", "C", "D", "E", "F"}


def gate(status: str = "PASS", applicability: str = "APPLICABLE") -> dict:
    return {
        "status": status,
        "applicability": applicability,
        "justification": "self-test gate",
        "evidence_refs": ["self-test"],
    }


def all_gates(status: str = "PASS") -> dict:
    names = [
        "b0_identity", "b1_evidence", "b2_route", "theory", "causal",
        "conservation", "expected_difference", "non_interference", "coverage",
        "independent_review", "residual_uncertainty", "class_specific",
        "composition_if_applicable",
    ]
    result = {name: gate(status) for name in names}
    result["composition_if_applicable"] = gate(status, "NOT_APPLICABLE")
    return result


def normal_class_a_record() -> dict:
    return {
        "record_id": "SELFTEST-A-NORMAL",
        "record_version": 1,
        "tcd_ids": ["TCD-017"],
        "atomicity": "ATOMIC",
        "qualification_class": "A",
        "admission_route": "NORMAL_B2_AVAILABLE",
        "disposition": "ADMIT_CORRECTED_LEGACY_BEHAVIOUR",
        "scope": {
            "process": "self-test process",
            "code_path": "self-test path",
            "claimed_change": "ledger-only",
            "control_volume": "self-test control volume",
        },
        "identities": {
            "b0": {
                "source_sha256": "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
                "testbank_sha256": "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
                "testcase_status": "FROZEN_CASE_IDENTIFIED",
                "testcase_identity": "self-test case",
                "documentation_or_theory_identity": "self-test theory",
            },
            "b1": {
                "status": "DIAGNOSTIC_NOT_REFERENCE",
                "evidence_identity": "self-test B1",
                "diagnostic_limitations": "not a historical reference",
            },
            "b2": {
                "status": "AVAILABLE_QUALIFIED_REFERENCE",
                "reference_identity": "self-test B2",
                "path_relevance": "path exercised",
            },
        },
        "evidence": {
            "theory": {"status": "PRESENT", "summary": "identity", "refs": ["self-test"]},
            "causal": {"status": "PRESENT", "summary": "causal", "refs": ["self-test"]},
            "conservation": {"status": "PRESENT", "summary": "closed", "refs": ["self-test"]},
            "expected_difference": {
                "changed_states": [],
                "changed_fluxes": [],
                "changed_ledgers_or_reports": ["ledger"],
                "unchanged_surfaces": ["state", "flux"],
            },
            "non_interference": {"status": "PRESENT", "summary": "unchanged", "refs": ["self-test"]},
            "coverage": {
                "natural_case_coverage": "covered",
                "synthetic_case_coverage": "not required",
                "branch_activation_proven": True,
                "refs": ["self-test"],
            },
            "independent_review": {
                "status": "COMPLETE",
                "reviewer_or_workunit": "self-test reviewer",
                "independent_from_correction_authoring": True,
                "scope": "full",
                "result": "PASS",
            },
        },
        "class_specific_evidence": {
            "physical_state_trajectory_unchanged": True,
            "process_flux_trajectory_unchanged": True,
            "intended_ledger_or_report_only": True,
            "conservation_identity_ref": "self-test identity",
            "changed_reporting_surfaces": ["ledger"],
            "unchanged_physical_surfaces": ["state", "flux"],
        },
        "gates": all_gates(),
        "residual_uncertainty": ["NONE_IDENTIFIED_WITHIN_SELF_TEST_SCOPE"],
        "composition": {"is_composition": False, "component_record_ids": []},
        "admission_decision": {
            "admitted": True,
            "decision": "self-test admission",
            "decision_scope": "self-test only",
            "decision_evidence_ref": "self-test",
        },
    }


def uncertainty_class_a_record() -> dict:
    record = normal_class_a_record()
    record["record_id"] = "SELFTEST-A-UNCERTAINTY"
    record["admission_route"] = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
    record["disposition"] = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
    record["identities"]["b2"] = {
        "status": "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT",
        "acquisition_effort_ref": "self-test acquisition log",
    }
    record["evidence"]["historical_uncertainty"] = {
        "acquisition_effort_ref": "self-test acquisition log",
        "stopping_rationale": "self-test exhausted route",
        "scientific_basis_ref": "self-test closed identity",
        "independent_cross_check_ref": "self-test independent check",
        "second_line_review_ref": "self-test review",
        "uncertainty_statement": "historical behaviour unknown",
        "scope_limitations": "self-test scope only",
    }
    record["residual_uncertainty"] = ["HISTORICAL_BEHAVIOUR_UNKNOWN"]
    return record


def assert_invalid(validator: Draft202012Validator, record: dict, label: str) -> None:
    if not list(validator.iter_errors(record)):
        raise AssertionError(f"Expected schema rejection: {label}")


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    for required_class in EXPECTED_CLASSES:
        if required_class not in schema.get("x-class-contracts", {}):
            raise AssertionError(f"Missing class contract {required_class}")

    normal = normal_class_a_record()
    validator.validate(normal)
    validator.validate(uncertainty_class_a_record())

    bad = copy.deepcopy(normal)
    bad["disposition"] = "UNRESOLVED_NOT_ADMITTED"
    assert_invalid(validator, bad, "admitted true with unresolved disposition")

    bad = copy.deepcopy(normal)
    bad["atomicity"] = "REQUIRES_ATOMIZATION"
    assert_invalid(validator, bad, "admitted compound record")

    bad = copy.deepcopy(normal)
    bad["gates"]["conservation"]["status"] = "FAIL"
    assert_invalid(validator, bad, "admitted record with failed gate")

    bad = uncertainty_class_a_record()
    bad["disposition"] = "PRESERVE_HISTORICAL_BEHAVIOUR"
    assert_invalid(validator, bad, "historical preservation without B2")

    bad = copy.deepcopy(normal)
    bad["composition"] = {
        "is_composition": True,
        "component_record_ids": ["only-one"],
        "composition_record_id": "composition-self-test",
    }
    assert_invalid(validator, bad, "composition with fewer than two components")

    with CLASSIFICATION_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    ids = {row["tcd_id"] for row in rows}
    if ids != EXPECTED_TCDS:
        raise AssertionError(f"Unexpected TCD set: {sorted(ids)}")
    if any(row["admitted"].lower() != "false" for row in rows):
        raise AssertionError("B3Q01 classification must not admit a legacy correction")
    if any(row["provisional_class"] not in EXPECTED_CLASSES for row in rows):
        raise AssertionError("Unknown provisional qualification class")

    by_id = {row["tcd_id"]: row for row in rows}
    if by_id["TCD-019"]["provisional_class"] != "E":
        raise AssertionError("TCD-019 must remain Class E")
    if by_id["TCD-019"]["provisional_disposition"] != "NUMERICAL_POLICY_CHANGE_REQUIRES_SEPARATE_QUALIFICATION":
        raise AssertionError("TCD-019 must require separate numerical qualification")
    if by_id["TCD-016"]["provisional_class"] != "C":
        raise AssertionError("TCD-016 must remain Class C")
    if by_id["TCD-014"]["atomicity"] != "REQUIRES_ATOMIZATION":
        raise AssertionError("TCD-014 must be atomized before admission")

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    if status.get("corrected_legacy_admitted") is not False:
        raise AssertionError("B3Q01 must admit no corrected legacy behaviour")
    if status.get("production_migration_admitted") is not False:
        raise AssertionError("B3Q01 must not admit production migration")

    required_docs = [
        ROOT / "docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md",
        ROOT / "docs/governance/B3_QUALIFICATION_CLASSES.md",
        ROOT / "docs/governance/B3_COMPOSITION_RULES.md",
    ]
    for path in required_docs:
        if not path.is_file() or path.stat().st_size == 0:
            raise AssertionError(f"Missing governance document: {path}")

    print("ANIMO-B3Q01 governance validation: PASS")


if __name__ == "__main__":
    main()
