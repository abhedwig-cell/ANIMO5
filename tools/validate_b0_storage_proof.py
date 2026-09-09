#!/usr/bin/env python3
"""Fail-closed semantic admission gate for ANIMO-EG01 B0 storage proof.

This tool validates public proof metadata against the canonical B0 register.
It does not authenticate a custodian, storage platform, or proof reference.
Passing this gate is necessary but not sufficient for human qualification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ADMITTED_DECISION = "QUALIFIED_CONTROLLED_IMMUTABLE_B0_RETENTION"
PENDING_DECISION = "QUALIFIED_B0_RETENTION_CONTRACT_IMPLEMENTATION_PENDING_EXTERNAL_CONTROLLED_STORAGE"
PLACEHOLDERS = {
    "",
    "PENDING",
    "TO_BE_COMPLETED_BY_AUTHORIZED_CUSTODIAN",
    "NOT_PROVEN",
    "TBD",
    "TODO",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def _non_placeholder(value: Any) -> bool:
    return isinstance(value, str) and value.strip() not in PLACEHOLDERS


def _register_map(register: dict[str, Any]) -> dict[str, str]:
    artifacts = register.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("B0 register must contain an artifacts array")

    result: dict[str, str] = {}
    for item in artifacts:
        if not isinstance(item, dict) or item.get("evidence_class") != "B0_RAW_IMMUTABLE":
            continue
        evidence_id = item.get("evidence_id")
        digest = item.get("sha256")
        if not isinstance(evidence_id, str) or not isinstance(digest, str):
            raise ValueError("B0 register contains an invalid B0_RAW_IMMUTABLE entry")
        if evidence_id in result:
            raise ValueError(f"B0 register contains duplicate evidence_id: {evidence_id}")
        result[evidence_id] = digest

    if not result:
        raise ValueError("B0 register contains no B0_RAW_IMMUTABLE artifacts")
    return result


def evaluate(proof: dict[str, Any], register: dict[str, Any]) -> dict[str, Any]:
    expected = _register_map(register)
    failures: list[str] = []

    if proof.get("schema_version") != "1.0":
        failures.append("proof schema_version must be 1.0")
    if proof.get("work_unit") != "ANIMO-EG01":
        failures.append("proof work_unit must be ANIMO-EG01")
    if proof.get("proof_status") != "PROVEN_CONTROLLED_IMMUTABLE":
        failures.append("proof_status is not PROVEN_CONTROLLED_IMMUTABLE")

    authority = proof.get("storage_authority")
    if not isinstance(authority, dict):
        failures.append("storage_authority must be an object")
    else:
        for key in (
            "organization_or_authority",
            "custodian_role",
            "primary_storage_control",
            "auditability_statement",
            "retention_policy_reference",
        ):
            if not _non_placeholder(authority.get(key)):
                failures.append(f"storage_authority.{key} is missing or placeholder")
        if authority.get("secondary_failure_domain_independent") is not True:
            failures.append("secondary failure domain independence is not proven")
        if authority.get("least_privilege_access") is not True:
            failures.append("least-privilege access is not proven")

    objects = proof.get("evidence_objects")
    seen: dict[str, dict[str, Any]] = {}
    if not isinstance(objects, list):
        failures.append("evidence_objects must be an array")
        objects = []

    for index, item in enumerate(objects):
        if not isinstance(item, dict):
            failures.append(f"evidence_objects[{index}] must be an object")
            continue
        evidence_id = item.get("evidence_id")
        if not isinstance(evidence_id, str):
            failures.append(f"evidence_objects[{index}].evidence_id is missing")
            continue
        if evidence_id in seen:
            failures.append(f"duplicate evidence_id: {evidence_id}")
            continue
        seen[evidence_id] = item

    expected_ids = set(expected)
    seen_ids = set(seen)
    for missing in sorted(expected_ids - seen_ids):
        failures.append(f"missing required B0 evidence object: {missing}")
    for unexpected in sorted(seen_ids - expected_ids):
        failures.append(f"unexpected evidence object: {unexpected}")

    for evidence_id in sorted(expected_ids & seen_ids):
        item = seen[evidence_id]
        digest = expected[evidence_id]
        prefix = f"{evidence_id}:"

        if item.get("expected_sha256") != digest:
            failures.append(f"{prefix} expected_sha256 differs from B0 register")
        if item.get("post_ingest_sha256") != digest:
            failures.append(f"{prefix} primary retained-byte SHA-256 does not equal B0")
        if item.get("secondary_sha256") != digest:
            failures.append(f"{prefix} secondary retained-byte SHA-256 does not equal B0")
        if item.get("post_ingest_sha256_match") is not True:
            failures.append(f"{prefix} primary SHA-256 match flag is not true")
        if item.get("secondary_sha256_match") is not True:
            failures.append(f"{prefix} secondary SHA-256 match flag is not true")
        if item.get("retention_status") != "PROVEN_CONTROLLED_IMMUTABLE":
            failures.append(f"{prefix} retention_status is not proven")

        for key in (
            "primary_storage_record_id",
            "secondary_storage_record_id",
            "immutability_proof_reference",
            "ingest_timestamp",
        ):
            if not _non_placeholder(item.get(key)):
                failures.append(f"{prefix} {key} is missing or placeholder")

        restore = item.get("restore_test")
        if not isinstance(restore, dict):
            failures.append(f"{prefix} restore_test must be an object")
        else:
            if restore.get("performed") is not True:
                failures.append(f"{prefix} restore test was not performed")
            if restore.get("restored_sha256") != digest:
                failures.append(f"{prefix} restored SHA-256 does not equal B0")
            if restore.get("sha256_match") is not True:
                failures.append(f"{prefix} restore SHA-256 match flag is not true")
            for key in ("timestamp", "proof_reference"):
                if not _non_placeholder(restore.get(key)):
                    failures.append(f"{prefix} restore_test.{key} is missing or placeholder")

    approval = proof.get("custodian_approval")
    if not isinstance(approval, dict):
        failures.append("custodian_approval must be an object")
    else:
        if approval.get("approved") is not True:
            failures.append("custodian approval is not true")
        for key in ("approval_reference", "approval_timestamp"):
            if not _non_placeholder(approval.get(key)):
                failures.append(f"custodian_approval.{key} is missing or placeholder")

    admitted = not failures
    return {
        "work_unit": "ANIMO-EG01",
        "admission_ready": admitted,
        "decision_if_reviewed_and_accepted": ADMITTED_DECISION if admitted else PENDING_DECISION,
        "machine_gate_scope": (
            "metadata consistency against the B0 register only; "
            "custodian identity, storage controls and proof references still require human review"
        ),
        "expected_b0_evidence_ids": sorted(expected),
        "failures": failures,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "proof",
        type=Path,
        help="public ANIMO-EG01 storage proof JSON returned by the custodian",
    )
    parser.add_argument(
        "--register",
        type=Path,
        default=Path("integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json"),
        help="canonical B0 evidence register",
    )
    args = parser.parse_args(argv)

    try:
        proof = _load_json(args.proof)
        register = _load_json(args.register)
        result = evaluate(proof, register)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        result = {
            "work_unit": "ANIMO-EG01",
            "admission_ready": False,
            "decision_if_reviewed_and_accepted": PENDING_DECISION,
            "machine_gate_scope": "input could not be evaluated",
            "expected_b0_evidence_ids": [],
            "failures": [str(exc)],
        }

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["admission_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
