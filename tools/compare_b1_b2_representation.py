#!/usr/bin/env python3
"""Fail-closed comparison of ANIMO B2 and B1 representation observations.

This ANIMO-NQ01 tool compares declared non-scientific and representation-level
observations separately from scientific state/flux/ledger values. It defines no
normalization and no numerical tolerance. Any non-exact representation
observation remains fail-closed until separately classified.

A successful result is comparison evidence only. It does not qualify B2,
numerical equivalence, B3 admission or production migration.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any


B1_ROLE = "B1_DIAGNOSTIC"
B2_ROLES = {
    "B2_HISTORICAL_REFERENCE_CANDIDATE",
    "B2_HISTORICAL_REFERENCE_QUALIFIED",
}

DOMAINS = {
    "file_path_compatibility": "FILE_PATH_COMPATIBILITY_DIFFERENCE",
    "formatting": "FORMATTING_DIFFERENCE",
    "binary_record_representation": "BINARY_RECORD_REPRESENTATION_DIFFERENCE",
    "precision_representation": "PRECISION_REPRESENTATION_DIFFERENCE",
}


class RepresentationError(ValueError):
    pass


def load_capture(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RepresentationError(f"cannot read capture {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RepresentationError("capture root must be an object")
    return data


def _obj(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def validate_capture(capture: dict[str, Any], *, side: str) -> list[str]:
    errors: list[str] = []
    role = capture.get("evidence_role")
    if side == "b1" and role != B1_ROLE:
        errors.append(f"B1 role must be {B1_ROLE}, got {role!r}")
    if side == "b2" and role not in B2_ROLES:
        errors.append(f"B2 role must be one of {sorted(B2_ROLES)}, got {role!r}")

    run = _obj(capture.get("run_identity"))
    for field in ("testcase_id", "testcase_archive_sha256", "input_tree_sha256_or_manifest"):
        if field not in run:
            errors.append(f"missing run_identity.{field}")

    observations = capture.get("representation_observations")
    if observations is None:
        errors.append("representation_observations is required for representation comparison")
    elif not isinstance(observations, list):
        errors.append("representation_observations must be an array")
    else:
        for index, item in enumerate(observations):
            if not isinstance(item, dict):
                errors.append(f"representation_observations[{index}] must be an object")
                continue
            domain = item.get("domain")
            if domain not in DOMAINS:
                errors.append(f"representation_observations[{index}] has unknown domain {domain!r}")
            for field in ("subject", "classification", "reference_text"):
                value = item.get(field)
                if not isinstance(value, str) or not value:
                    errors.append(f"representation_observations[{index}].{field} must be non-empty text")
    return errors


def observation_key(item: dict[str, Any]) -> tuple[str, str]:
    return str(item.get("domain")), str(item.get("subject"))


def index_observations(items: list[dict[str, Any]]) -> tuple[dict[tuple[str, str], dict[str, Any]], list[str]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    duplicates: list[str] = []
    for item in items:
        key = observation_key(item)
        if key in index:
            duplicates.append(str(key))
        else:
            index[key] = item
    return index, duplicates


def compare_observation(reference: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    domain = str(reference.get("domain"))
    subject = str(reference.get("subject"))
    result: dict[str, Any] = {
        "domain": domain,
        "subject": subject,
        "reference_classification": reference.get("classification"),
        "candidate_classification": candidate.get("classification"),
        "reference_text": reference.get("reference_text"),
        "candidate_text": candidate.get("reference_text"),
    }

    if (
        reference.get("classification") == candidate.get("classification")
        and reference.get("reference_text") == candidate.get("reference_text")
    ):
        result["classification"] = "EXACT_REPRESENTATION_OBSERVATION_MATCH"
        result["fail_closed"] = False
    else:
        result["classification"] = DOMAINS[domain]
        result["fail_closed"] = True
        result["note"] = (
            "representation difference is not auto-normalized; it requires an explicit "
            "separate disposition before it can be treated as non-scientific"
        )
    return result


def compare_captures(b2: dict[str, Any], b1: dict[str, Any]) -> dict[str, Any]:
    b2_errors = validate_capture(b2, side="b2")
    b1_errors = validate_capture(b1, side="b1")

    b2_run = _obj(b2.get("run_identity"))
    b1_run = _obj(b1.get("run_identity"))
    provenance_errors: list[str] = []
    for field in ("testcase_id", "testcase_archive_sha256", "input_tree_sha256_or_manifest"):
        if b2_run.get(field) != b1_run.get(field):
            provenance_errors.append(f"{field} differs between B2 and B1")

    if b2_errors or b1_errors or provenance_errors:
        return {
            "evidence_class": "REPRESENTATION_COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
            "decision": "SCHEMA_OR_PROVENANCE_FAILURE",
            "b2_validation_errors": b2_errors,
            "b1_validation_errors": b1_errors,
            "provenance_errors": provenance_errors,
            "b2_reference_qualified_by_this_tool": False,
            "numerical_equivalence_qualified_by_this_tool": False,
            "production_migration_admitted": False,
        }

    b2_index, b2_duplicates = index_observations(b2["representation_observations"])
    b1_index, b1_duplicates = index_observations(b1["representation_observations"])
    if b2_duplicates or b1_duplicates:
        return {
            "evidence_class": "REPRESENTATION_COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
            "decision": "SCHEMA_OR_PROVENANCE_FAILURE",
            "duplicate_b2_keys": b2_duplicates,
            "duplicate_b1_keys": b1_duplicates,
            "b2_reference_qualified_by_this_tool": False,
            "numerical_equivalence_qualified_by_this_tool": False,
            "production_migration_admitted": False,
        }

    b2_keys = set(b2_index)
    b1_keys = set(b1_index)
    missing_in_b1 = sorted(str(key) for key in b2_keys - b1_keys)
    unexpected_in_b1 = sorted(str(key) for key in b1_keys - b2_keys)
    comparisons = [
        compare_observation(b2_index[key], b1_index[key])
        for key in sorted(b2_keys & b1_keys)
    ]

    counts = Counter(item["classification"] for item in comparisons)
    domain_counts: dict[str, Counter[str]] = {domain: Counter() for domain in DOMAINS}
    for item in comparisons:
        domain_counts[item["domain"]][item["classification"]] += 1

    fail_closed = bool(missing_in_b1 or unexpected_in_b1) or any(
        item["fail_closed"] for item in comparisons
    )

    return {
        "evidence_class": "REPRESENTATION_COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
        "testcase_id": b2_run.get("testcase_id"),
        "b2_role": b2.get("evidence_role"),
        "b1_role": b1.get("evidence_role"),
        "observation_set": {
            "b2_observations": len(b2_index),
            "b1_observations": len(b1_index),
            "common_observations": len(b2_keys & b1_keys),
            "missing_in_b1": missing_in_b1,
            "unexpected_in_b1": unexpected_in_b1,
        },
        "classification_counts": dict(sorted(counts.items())),
        "domain_counts": {
            domain: dict(sorted(counter.items())) for domain, counter in domain_counts.items()
        },
        "comparisons": comparisons,
        "decision": (
            "DIFFERENT_REPRESENTATION_FAIL_CLOSED"
            if fail_closed
            else "MATCH_EXACT_REPRESENTATION_OBSERVATIONS"
        ),
        "normalization_applied": False,
        "numerical_tolerance_applied": False,
        "b2_reference_qualified_by_this_tool": False,
        "numerical_equivalence_qualified_by_this_tool": False,
        "production_migration_admitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("b2_reference", type=Path)
    parser.add_argument("b1_diagnostic", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    try:
        report = compare_captures(load_capture(args.b2_reference), load_capture(args.b1_diagnostic))
    except RepresentationError as exc:
        report = {
            "evidence_class": "REPRESENTATION_COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
            "decision": "SCHEMA_OR_PROVENANCE_FAILURE",
            "error": str(exc),
            "b2_reference_qualified_by_this_tool": False,
            "numerical_equivalence_qualified_by_this_tool": False,
            "production_migration_admitted": False,
        }

    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    if report["decision"] == "SCHEMA_OR_PROVENANCE_FAILURE":
        return 3
    if report["decision"] == "DIFFERENT_REPRESENTATION_FAIL_CLOSED":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
