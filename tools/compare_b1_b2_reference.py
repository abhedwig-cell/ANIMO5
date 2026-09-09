#!/usr/bin/env python3
"""Fail-closed structured ANIMO B1 versus B2 reference comparator.

ANIMO-NQ01 qualification tooling. This tool deliberately defines no numerical
acceptance tolerance. Exact scientific equality is reported when present. Any
non-exact floating scientific value is classified as an unqualified numerical
difference and causes a fail-closed comparison result.

The tool does not qualify B2 provenance, B3 scientific admission or B4
migration. It only produces comparison evidence from capture files that follow
the ANIMO-NQ01 reference capture contract.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.1.0"
B1_ROLE = "B1_DIAGNOSTIC"
B2_ROLES = {
    "B2_HISTORICAL_REFERENCE_CANDIDATE",
    "B2_HISTORICAL_REFERENCE_QUALIFIED",
}

EXACT_CLASSES = {
    "ARTIFACT_IDENTITY",
    "BINARY_RECORD_REPRESENTATION",
    "DISCRETE_CONTROL_FLOW",
    "INTEGER_OPTION_STATE",
}

FLOAT_SCIENTIFIC_CLASSES = {
    "EXACT_ACCOUNTING_IDENTITY",
    "PHYSICAL_STORAGE_STATE",
    "INTERNAL_TRANSFER_FLUX",
    "EXTERNAL_BOUNDARY_FLUX",
    "CUMULATIVE_LEDGER",
    "NONLINEAR_SOLVER_STATE",
    "DIAGNOSTIC_RESIDUAL",
}

NONSCIENTIFIC_REPRESENTATION_CLASSES = {
    "TIMING_OR_NONSCIENTIFIC_METADATA",
}

FORMATTED_REPORT_CLASS = "FORMATTED_REPORT_VALUE"

CLASS_TO_DOMAIN = {
    "ARTIFACT_IDENTITY": "file_path_compatibility",
    "BINARY_RECORD_REPRESENTATION": "binary_record_representation",
    "DISCRETE_CONTROL_FLOW": "control_flow_branch",
    "INTEGER_OPTION_STATE": "control_flow_branch",
    "EXACT_ACCOUNTING_IDENTITY": "ledger_trajectory",
    "PHYSICAL_STORAGE_STATE": "state_trajectory",
    "INTERNAL_TRANSFER_FLUX": "flux_trajectory",
    "EXTERNAL_BOUNDARY_FLUX": "flux_trajectory",
    "CUMULATIVE_LEDGER": "ledger_trajectory",
    "NONLINEAR_SOLVER_STATE": "control_flow_branch",
    "DIAGNOSTIC_RESIDUAL": "precision_representation",
    "FORMATTED_REPORT_VALUE": "formatting",
    "TIMING_OR_NONSCIENTIFIC_METADATA": "formatting",
}

ALL_DOMAINS = (
    "file_path_compatibility",
    "formatting",
    "binary_record_representation",
    "precision_representation",
    "state_trajectory",
    "flux_trajectory",
    "ledger_trajectory",
    "control_flow_branch",
)


class CaptureError(ValueError):
    pass


def load_capture(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CaptureError(f"cannot read capture {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CaptureError(f"capture root must be an object: {path}")
    return data


def _require(mapping: dict[str, Any], field: str, context: str) -> Any:
    if field not in mapping:
        raise CaptureError(f"missing {context}.{field}")
    return mapping[field]


def _nested(mapping: dict[str, Any], key: str) -> dict[str, Any]:
    value = mapping.get(key)
    return value if isinstance(value, dict) else {}


def validate_capture_minimum(capture: dict[str, Any], *, expected_side: str) -> list[str]:
    """Validate fields needed for deterministic fail-closed comparison.

    Full JSON Schema validation is intentionally not bundled into this stdlib-only
    tool. The repository schema remains the authoritative complete contract.
    This validator nevertheless enforces the safety-critical precision rules that
    prevent rounded report values from masquerading as unrounded scientific data.
    """
    errors: list[str] = []
    try:
        version = _require(capture, "schema_version", "capture")
        role = _require(capture, "evidence_role", "capture")
        run_identity = _require(capture, "run_identity", "capture")
        capture_contract = _require(capture, "capture_contract", "capture")
        records = _require(capture, "records", "capture")

        if version != SCHEMA_VERSION:
            errors.append(f"unsupported schema_version {version!r}; expected {SCHEMA_VERSION!r}")
        if expected_side == "b1" and role != B1_ROLE:
            errors.append(f"B1 capture role must be {B1_ROLE}, got {role!r}")
        if expected_side == "b2" and role not in B2_ROLES:
            errors.append(f"B2 capture role must be one of {sorted(B2_ROLES)}, got {role!r}")

        if not isinstance(run_identity, dict):
            errors.append("run_identity must be an object")
        else:
            for field in (
                "run_id",
                "testcase_id",
                "executable_sha256",
                "testcase_archive_sha256",
                "input_tree_sha256_or_manifest",
                "environment_id",
            ):
                if field not in run_identity:
                    errors.append(f"missing run_identity.{field}")
            if run_identity.get("input_content_transformed") is True:
                errors.append("input_content_transformed must be false for the frozen first-reference path")

        rounded_report_only = False
        if not isinstance(capture_contract, dict):
            errors.append("capture_contract must be an object")
        else:
            for field in (
                "observer_only",
                "ordinary_output_reproduced_before_observer_trust",
                "rounded_report_only",
                "precision_capture_method",
            ):
                if field not in capture_contract:
                    errors.append(f"missing capture_contract.{field}")
            rounded_report_only = capture_contract.get("rounded_report_only") is True

        if not isinstance(records, list):
            errors.append("records must be an array")
        else:
            scientific_float_records = 0
            for index, record in enumerate(records):
                if not isinstance(record, dict):
                    errors.append(f"records[{index}] must be an object")
                    continue
                for field in (
                    "record_id",
                    "variable_class",
                    "quantity_name",
                    "units",
                    "temporal",
                    "location",
                    "scientific_context",
                    "execution_context",
                    "precision",
                    "value",
                ):
                    if field not in record:
                        errors.append(f"records[{index}] missing {field}")

                variable_class = record.get("variable_class")
                if variable_class in FLOAT_SCIENTIFIC_CLASSES:
                    scientific_float_records += 1
                    precision = record.get("precision")
                    if not isinstance(precision, dict):
                        errors.append(f"records[{index}].precision must be an object")
                    else:
                        for field in ("storage_kind", "bits", "capture_is_round_trip"):
                            if field not in precision:
                                errors.append(f"records[{index}] missing precision.{field}")
                        if precision.get("capture_is_round_trip") is not True:
                            errors.append(
                                f"records[{index}] scientific floating capture is not proven round-trip"
                            )

            if rounded_report_only and scientific_float_records:
                errors.append(
                    "rounded_report_only capture cannot supply floating scientific records as an unrounded oracle"
                )
    except CaptureError as exc:
        errors.append(str(exc))
    return errors


def record_key(record: dict[str, Any]) -> tuple[Any, ...]:
    temporal = _nested(record, "temporal")
    location = _nested(record, "location")
    scientific = _nested(record, "scientific_context")
    execution = _nested(record, "execution_context")
    return (
        record.get("variable_class"),
        record.get("quantity_name"),
        record.get("units"),
        temporal.get("checkpoint"),
        temporal.get("simulation_year"),
        temporal.get("simulation_time_day"),
        temporal.get("step_index"),
        temporal.get("period_id"),
        location.get("layer"),
        location.get("compartment"),
        location.get("species"),
        location.get("site_or_fraction"),
        scientific.get("state_id"),
        scientific.get("transfer_id"),
        scientific.get("ledger_id"),
        scientific.get("cumulative"),
        scientific.get("boundary"),
        execution.get("accepted_state"),
        execution.get("trial_state"),
        execution.get("iteration_index"),
    )


def index_records(records: Iterable[dict[str, Any]]) -> tuple[dict[tuple[Any, ...], dict[str, Any]], list[str]]:
    index: dict[tuple[Any, ...], dict[str, Any]] = {}
    duplicates: list[str] = []
    for record in records:
        key = record_key(record)
        if key in index:
            duplicates.append(str(key))
        else:
            index[key] = record
    return index, duplicates


def _value_text(record: dict[str, Any]) -> str:
    value = _nested(record, "value")
    text = value.get("text")
    return text if isinstance(text, str) else ""


def _decimal_value(record: dict[str, Any]) -> Decimal | None:
    value = _nested(record, "value")
    candidates = [value.get("decimal_text")]
    if value.get("encoding") in {"decimal_text", "integer_decimal"}:
        candidates.append(value.get("text"))
    for candidate in candidates:
        if not isinstance(candidate, str) or not candidate.strip():
            continue
        try:
            return Decimal(candidate.replace("D", "E").replace("d", "e"))
        except InvalidOperation:
            continue
    return None


def _binary_hex(record: dict[str, Any]) -> str | None:
    value = _nested(record, "value")
    candidate = value.get("binary_hex")
    if isinstance(candidate, str) and candidate:
        return candidate.lower()
    if value.get("encoding") in {"ieee_binary32_hex", "ieee_binary64_hex", "raw_hex"}:
        text = value.get("text")
        if isinstance(text, str) and text:
            return text.lower()
    return None


def _numeric_difference(left: Decimal, right: Decimal) -> dict[str, str]:
    abs_diff = abs(right - left)
    scale = max(abs(left), abs(right))
    rel_diff = Decimal(0) if scale == 0 else abs_diff / scale
    return {
        "reference_decimal": str(left),
        "candidate_decimal": str(right),
        "absolute_difference": str(abs_diff),
        "relative_difference": str(rel_diff),
        "note": "diagnostic magnitude only; no numerical tolerance is defined or applied",
    }


def _execution_path_difference(reference: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any] | None:
    reference_execution = _nested(reference, "execution_context")
    candidate_execution = _nested(candidate, "execution_context")
    differences: dict[str, dict[str, Any]] = {}
    for field in ("branch_id", "fallback_id"):
        left = reference_execution.get(field)
        right = candidate_execution.get(field)
        if left != right:
            differences[field] = {"reference": left, "candidate": right}
    return differences or None


def _accounting_identity_difference(reference: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any] | None:
    reference_scientific = _nested(reference, "scientific_context")
    candidate_scientific = _nested(candidate, "scientific_context")
    differences: dict[str, dict[str, Any]] = {}
    for field in ("ledger_member_id", "ledger_sign", "index_mapping_id"):
        left = reference_scientific.get(field)
        right = candidate_scientific.get(field)
        if left != right:
            differences[field] = {"reference": left, "candidate": right}
    return differences or None


def compare_record(reference: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    variable_class = str(reference.get("variable_class"))
    domain = CLASS_TO_DOMAIN.get(variable_class, "precision_representation")
    result: dict[str, Any] = {
        "record_key": list(record_key(reference)),
        "variable_class": variable_class,
        "difference_domain": domain,
        "reference_record_id": reference.get("record_id"),
        "candidate_record_id": candidate.get("record_id"),
    }

    if candidate.get("variable_class") != variable_class:
        result["classification"] = "SCHEMA_OR_KEY_CLASS_MISMATCH"
        result["fail_closed"] = True
        return result

    if reference.get("units") != candidate.get("units"):
        result["classification"] = "UNIT_MISMATCH"
        result["fail_closed"] = True
        result["reference_units"] = reference.get("units")
        result["candidate_units"] = candidate.get("units")
        return result

    path_difference = _execution_path_difference(reference, candidate)
    if path_difference is not None:
        result["classification"] = "CONTROL_FLOW_DIFFERENCE"
        result["difference_domain"] = "control_flow_branch"
        result["execution_path_difference"] = path_difference
        result["fail_closed"] = True
        return result

    if variable_class == "EXACT_ACCOUNTING_IDENTITY":
        accounting_difference = _accounting_identity_difference(reference, candidate)
        if accounting_difference is not None:
            result["classification"] = "ACCOUNTING_IDENTITY_DIFFERENCE"
            result["difference_domain"] = "ledger_trajectory"
            result["accounting_identity_difference"] = accounting_difference
            result["fail_closed"] = True
            return result

    left_text = _value_text(reference)
    right_text = _value_text(candidate)

    if variable_class in EXACT_CLASSES:
        if left_text == right_text:
            result["classification"] = "EXACT_MATCH"
            result["fail_closed"] = False
        else:
            result["classification"] = (
                "CONTROL_FLOW_DIFFERENCE"
                if variable_class in {"DISCRETE_CONTROL_FLOW", "INTEGER_OPTION_STATE"}
                else "EXACT_REPRESENTATION_DIFFERENCE"
            )
            result["fail_closed"] = True
            result["reference_value"] = left_text
            result["candidate_value"] = right_text
        return result

    if variable_class in NONSCIENTIFIC_REPRESENTATION_CLASSES:
        if left_text == right_text:
            result["classification"] = "EXACT_MATCH"
        else:
            result["classification"] = "REPRESENTATION_ONLY_DIFFERENCE"
            result["reference_value"] = left_text
            result["candidate_value"] = right_text
        result["fail_closed"] = False
        return result

    if variable_class == FORMATTED_REPORT_CLASS:
        if left_text == right_text:
            result["classification"] = "EXACT_MATCH"
            result["fail_closed"] = False
        else:
            result["classification"] = "FORMATTED_REPORT_DIFFERENCE_FAIL_CLOSED"
            result["reference_value"] = left_text
            result["candidate_value"] = right_text
            result["note"] = (
                "formatted report differences are comparison evidence but are not automatically "
                "representation-only; scientific versus lexical cause must be classified separately"
            )
            result["fail_closed"] = True
        return result

    if variable_class in FLOAT_SCIENTIFIC_CLASSES:
        left_decimal = _decimal_value(reference)
        right_decimal = _decimal_value(candidate)
        if left_decimal is not None and right_decimal is not None:
            if left_decimal == right_decimal:
                result["classification"] = "EXACT_MATCH"
                result["fail_closed"] = False
            else:
                result["classification"] = "UNQUALIFIED_NUMERICAL_DIFFERENCE"
                result["fail_closed"] = True
                result["numeric_difference"] = _numeric_difference(left_decimal, right_decimal)
            return result

        left_hex = _binary_hex(reference)
        right_hex = _binary_hex(candidate)
        if left_hex is not None and right_hex is not None and left_hex == right_hex:
            result["classification"] = "EXACT_MATCH"
            result["fail_closed"] = False
            result["comparison_basis"] = "exact_binary_representation"
            return result

        result["classification"] = "PRECISION_REPRESENTATION_DIFFERENCE"
        result["fail_closed"] = True
        result["reference_value"] = _nested(reference, "value")
        result["candidate_value"] = _nested(candidate, "value")
        result["note"] = "no common exact numeric representation available for comparison"
        return result

    result["classification"] = "UNKNOWN_VARIABLE_CLASS"
    result["fail_closed"] = True
    return result


def _representation_observation_summary(
    b2: dict[str, Any], b1: dict[str, Any]
) -> tuple[list[dict[str, Any]], Counter[str]]:
    observations: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for side, capture in (("b2", b2), ("b1", b1)):
        items = capture.get("representation_observations", [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            domain = item.get("domain")
            if domain not in ALL_DOMAINS:
                domain = "precision_representation"
            observations.append({"side": side, **item})
            counts[str(domain)] += 1
    return observations, counts


def compare_captures(b2: dict[str, Any], b1: dict[str, Any]) -> dict[str, Any]:
    b2_errors = validate_capture_minimum(b2, expected_side="b2")
    b1_errors = validate_capture_minimum(b1, expected_side="b1")
    provenance_errors: list[str] = []

    b2_run = _nested(b2, "run_identity")
    b1_run = _nested(b1, "run_identity")
    if b2_run.get("testcase_id") != b1_run.get("testcase_id"):
        provenance_errors.append("testcase_id differs between B2 and B1 capture")
    if b2_run.get("testcase_archive_sha256") != b1_run.get("testcase_archive_sha256"):
        provenance_errors.append("testcase_archive_sha256 differs between B2 and B1 capture")
    if b2_run.get("input_tree_sha256_or_manifest") != b1_run.get("input_tree_sha256_or_manifest"):
        provenance_errors.append("input_tree_sha256_or_manifest differs between B2 and B1 capture")

    if b2_errors or b1_errors or provenance_errors:
        return {
            "evidence_class": "COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
            "decision": "SCHEMA_OR_PROVENANCE_FAILURE",
            "b2_validation_errors": b2_errors,
            "b1_validation_errors": b1_errors,
            "provenance_errors": provenance_errors,
            "numerical_equivalence_qualified_by_this_tool": False,
            "production_migration_admitted": False,
        }

    b2_index, b2_duplicates = index_records(b2.get("records", []))
    b1_index, b1_duplicates = index_records(b1.get("records", []))
    if b2_duplicates or b1_duplicates:
        return {
            "evidence_class": "COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
            "decision": "SCHEMA_OR_PROVENANCE_FAILURE",
            "duplicate_b2_keys": b2_duplicates,
            "duplicate_b1_keys": b1_duplicates,
            "numerical_equivalence_qualified_by_this_tool": False,
            "production_migration_admitted": False,
        }

    b2_keys = set(b2_index)
    b1_keys = set(b1_index)
    missing_in_b1 = sorted((str(key) for key in b2_keys - b1_keys))
    unexpected_in_b1 = sorted((str(key) for key in b1_keys - b2_keys))

    comparisons = [
        compare_record(b2_index[key], b1_index[key])
        for key in sorted(b2_keys & b1_keys, key=str)
    ]

    classification_counts = Counter(item["classification"] for item in comparisons)
    domain_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for item in comparisons:
        domain_counts[item["difference_domain"]][item["classification"]] += 1

    representation_observations, representation_counts = _representation_observation_summary(b2, b1)

    has_record_failures = any(item.get("fail_closed") for item in comparisons)
    has_key_failures = bool(missing_in_b1 or unexpected_in_b1)
    has_representation_only = any(
        item["classification"] == "REPRESENTATION_ONLY_DIFFERENCE" for item in comparisons
    )

    if has_record_failures or has_key_failures:
        decision = "DIFFERENT_FAIL_CLOSED"
    elif has_representation_only:
        decision = "MATCH_SCIENTIFIC_RECORDS_REPRESENTATION_DIFFERS"
    elif b2.get("evidence_role") == "B2_HISTORICAL_REFERENCE_CANDIDATE":
        decision = "MATCH_EXACT_B2_CANDIDATE_NOT_QUALIFIED"
    else:
        decision = "MATCH_EXACT_COMPARISON_EVIDENCE"

    unrounded_scientific_records = sum(
        1 for item in b2_index.values() if item.get("variable_class") in FLOAT_SCIENTIFIC_CLASSES
    )

    return {
        "evidence_class": "COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
        "schema_version": SCHEMA_VERSION,
        "b2_role": b2.get("evidence_role"),
        "b1_role": b1.get("evidence_role"),
        "testcase_id": b2_run.get("testcase_id"),
        "b2_run_id": b2_run.get("run_id"),
        "b1_run_id": b1_run.get("run_id"),
        "record_set": {
            "b2_records": len(b2_index),
            "b1_records": len(b1_index),
            "common_records": len(b2_keys & b1_keys),
            "missing_in_b1": missing_in_b1,
            "unexpected_in_b1": unexpected_in_b1,
            "unrounded_scientific_b2_records": unrounded_scientific_records,
        },
        "classification_counts": dict(sorted(classification_counts.items())),
        "difference_domains": {
            domain: dict(sorted(domain_counts.get(domain, Counter()).items()))
            for domain in ALL_DOMAINS
        },
        "representation_observations": representation_observations,
        "representation_observation_counts": dict(sorted(representation_counts.items())),
        "comparisons": comparisons,
        "decision": decision,
        "global_numeric_tolerance_applied": False,
        "qualified_numeric_tolerance_applied": False,
        "non_exact_scientific_values_are_accepted": False,
        "rounded_report_values_treated_as_unrounded_oracle": False,
        "b2_reference_qualified_by_this_tool": False,
        "numerical_equivalence_qualified_by_this_tool": False,
        "production_migration_admitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("b2_reference", type=Path, help="structured B2 capture JSON")
    parser.add_argument("b1_diagnostic", type=Path, help="structured B1 capture JSON")
    parser.add_argument("--json", type=Path, help="optional report path")
    args = parser.parse_args()

    try:
        b2 = load_capture(args.b2_reference)
        b1 = load_capture(args.b1_diagnostic)
        report = compare_captures(b2, b1)
    except CaptureError as exc:
        report = {
            "evidence_class": "COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
            "decision": "SCHEMA_OR_PROVENANCE_FAILURE",
            "error": str(exc),
            "numerical_equivalence_qualified_by_this_tool": False,
            "production_migration_admitted": False,
        }

    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")

    if report["decision"] == "SCHEMA_OR_PROVENANCE_FAILURE":
        return 3
    if report["decision"] == "DIFFERENT_FAIL_CLOSED":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
