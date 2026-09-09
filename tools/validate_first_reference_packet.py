#!/usr/bin/env python3
"""Validate completeness and fail-closed governance of an ANIMO first-reference packet.

ANIMO-NQ01 preparation tooling. This validator checks that the evidence packet
needed for the first PREP02R B2-versus-B1 comparison is structurally complete
and does not silently relax the numerical qualification policy.

A valid packet is not a claim of numerical equivalence, B2 qualification, B3
admission or production migration. Comparison results may legitimately be
fail-closed while the packet itself is complete evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PACKET_SCHEMA_VERSION = "1.2.0"
FROZEN_TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
PINNED_B1_EXECUTABLE_SHA256 = "0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e"
PREFERRED_FIRST_CASE = "RuurloGrass"
REPRESENTATION_REGISTRY = "integration/animo-numerics/FIRST_REFERENCE_REPRESENTATION_SURFACE.json"
REPRESENTATION_REGISTRY_PATH = Path(__file__).parents[1] / REPRESENTATION_REGISTRY
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

B2_ROLES = {
    "B2_HISTORICAL_REFERENCE_CANDIDATE",
    "B2_HISTORICAL_REFERENCE_QUALIFIED",
}

FORMATTED_DECISIONS = {
    "MATCH_EXACT",
    "MATCH_AFTER_DECLARED_VOLATILE_NORMALIZATION",
    "DIFFERENT_FAIL_CLOSED",
}

REPRESENTATION_DECISIONS = {
    "MATCH_EXACT_REPRESENTATION_OBSERVATIONS",
    "DIFFERENT_REPRESENTATION_FAIL_CLOSED",
    "SCHEMA_OR_PROVENANCE_FAILURE",
}

REPRESENTATION_NOT_RUN = "NOT_RUN_NO_STRUCTURED_REPRESENTATION_CAPTURE"

REPRESENTATION_OMISSION_REASONS = {
    "NOT_APPLICABLE_TO_CASE",
    "NOT_JOINTLY_OBSERVABLE",
    "OBSERVER_NOT_ADMITTED",
    "HISTORICAL_BUILD_METADATA_UNAVAILABLE",
}

STRUCTURED_DECISIONS = {
    "MATCH_EXACT_COMPARISON_EVIDENCE",
    "MATCH_EXACT_B2_CANDIDATE_NOT_QUALIFIED",
    "MATCH_SCIENTIFIC_RECORDS_REPRESENTATION_DIFFERS",
    "DIFFERENT_FAIL_CLOSED",
    "SCHEMA_OR_PROVENANCE_FAILURE",
}

REPEAT_DECISIONS = {
    "NOT_RUN_WITH_RATIONALE",
    "NATIVE_REPEAT_EXACT",
    "NATIVE_REPEAT_DECLARED_VOLATILE_ONLY",
    "NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED",
}


def _obj(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA256_RE.fullmatch(value))


def _representation_key(value: Any) -> tuple[str, str] | None:
    if not isinstance(value, dict):
        return None
    domain = value.get("domain")
    subject = value.get("subject")
    if not _nonempty_string(domain) or not _nonempty_string(subject):
        return None
    return str(domain), str(subject)


def _load_representation_registry_keys() -> set[tuple[str, str]]:
    try:
        data = json.loads(REPRESENTATION_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read representation registry {REPRESENTATION_REGISTRY}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("subjects"), list):
        raise ValueError("representation registry must contain a subjects array")

    keys: set[tuple[str, str]] = set()
    for index, item in enumerate(data["subjects"]):
        key = _representation_key(item)
        if key is None:
            raise ValueError(f"representation registry subject {index} lacks domain or subject")
        if key in keys:
            raise ValueError(f"representation registry contains duplicate subject {key}")
        keys.add(key)
    if not keys:
        raise ValueError("representation registry contains no subjects")
    return keys


def load_packet(path: Path) -> dict[str, Any]:
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read packet {path}: {exc}") from exc
    if not isinstance(packet, dict):
        raise ValueError("packet root must be a JSON object")
    return packet


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        registry_keys = _load_representation_registry_keys()
    except ValueError as exc:
        errors.append(str(exc))
        registry_keys = set()

    if packet.get("packet_schema_version") != PACKET_SCHEMA_VERSION:
        errors.append(f"packet_schema_version must be {PACKET_SCHEMA_VERSION!r}")

    if packet.get("work_unit") != "ANIMO-NQ01":
        errors.append("work_unit must be 'ANIMO-NQ01'")

    testcase_id = packet.get("testcase_id")
    if testcase_id != PREFERRED_FIRST_CASE:
        errors.append(
            f"first-reference packet testcase_id must currently be {PREFERRED_FIRST_CASE!r}"
        )

    inputs = _obj(packet.get("inputs"))
    if inputs.get("testbank_archive_sha256") != FROZEN_TESTBANK_SHA256:
        errors.append("testbank_archive_sha256 does not match the frozen ANIMO testbank")
    if inputs.get("input_content_transformed") is not False:
        errors.append("input_content_transformed must be false for the preferred frozen path")
    if not _nonempty_string(inputs.get("input_tree_manifest")):
        errors.append("inputs.input_tree_manifest is required")
    if not _nonempty_string(inputs.get("hydrology_identity_or_manifest")):
        errors.append("inputs.hydrology_identity_or_manifest is required")

    b2 = _obj(packet.get("b2"))
    if b2.get("evidence_role") not in B2_ROLES:
        errors.append("b2.evidence_role must be an explicit B2 candidate or qualified role")
    if not _sha256(b2.get("artifact_sha256")):
        errors.append("b2.artifact_sha256 must be a lowercase SHA-256")
    for field in (
        "receipt_manifest",
        "lineage_classification",
        "ordinary_run_manifest",
        "raw_output_tree_manifest",
    ):
        if not _nonempty_string(b2.get(field)):
            errors.append(f"b2.{field} is required")
    if b2.get("execution_attempt_permitted_by_prep02r") is not True:
        errors.append("PREP02R must explicitly permit the native execution attempt")
    repeat = b2.get("repeat_determinism")
    if repeat not in REPEAT_DECISIONS:
        errors.append("b2.repeat_determinism has an unknown or missing classification")
    if repeat == "NOT_RUN_WITH_RATIONALE" and not _nonempty_string(b2.get("repeat_rationale")):
        errors.append("repeat_rationale is required when native repeat was not run")

    b1 = _obj(packet.get("b1"))
    if b1.get("evidence_role") != "B1_DIAGNOSTIC":
        errors.append("b1.evidence_role must remain B1_DIAGNOSTIC")
    if b1.get("executable_sha256") != PINNED_B1_EXECUTABLE_SHA256:
        errors.append("b1.executable_sha256 does not match the pinned diagnostic executable")
    for field in ("run_manifest", "raw_output_tree_manifest"):
        if not _nonempty_string(b1.get(field)):
            errors.append(f"b1.{field} is required")

    formatted = _obj(packet.get("formatted_tree_comparison"))
    if not _nonempty_string(formatted.get("result_artifact")):
        errors.append("formatted_tree_comparison.result_artifact is required")
    if formatted.get("decision") not in FORMATTED_DECISIONS:
        errors.append("formatted_tree_comparison.decision is missing or unknown")

    observer = _obj(packet.get("observer"))
    observer_used = observer.get("used")
    if observer_used not in {True, False}:
        errors.append("observer.used must be boolean")
    if observer_used is True:
        if observer.get("ordinary_output_non_interference_passed") is not True:
            errors.append("observer use requires ordinary-output non-interference to pass")
        for field in (
            "observer_patch_sha256",
            "b2_structured_capture",
            "b1_structured_capture",
        ):
            value = observer.get(field)
            if field.endswith("sha256"):
                if not _sha256(value):
                    errors.append(f"observer.{field} must be a lowercase SHA-256")
            elif not _nonempty_string(value):
                errors.append(f"observer.{field} is required when observer capture is used")
    else:
        if observer.get("ordinary_output_non_interference_passed") is True:
            warnings.append("observer non-interference is marked passed although observer.used is false")

    representation_scope = _obj(packet.get("representation_scope"))
    if representation_scope.get("registry") != REPRESENTATION_REGISTRY:
        errors.append(f"representation_scope.registry must be {REPRESENTATION_REGISTRY!r}")

    observed_items = representation_scope.get("jointly_observed_subjects")
    omitted_items = representation_scope.get("omitted_subjects")
    if not isinstance(observed_items, list):
        errors.append("representation_scope.jointly_observed_subjects must be an array")
        observed_items = []
    if not isinstance(omitted_items, list):
        errors.append("representation_scope.omitted_subjects must be an array")
        omitted_items = []

    observed_keys: set[tuple[str, str]] = set()
    omitted_keys: set[tuple[str, str]] = set()
    for index, item in enumerate(observed_items):
        key = _representation_key(item)
        if key is None:
            errors.append(f"jointly_observed_subjects[{index}] lacks domain or subject")
            continue
        if key in observed_keys:
            errors.append(f"duplicate jointly observed representation subject {key}")
        observed_keys.add(key)

    for index, item in enumerate(omitted_items):
        key = _representation_key(item)
        if key is None:
            errors.append(f"omitted_subjects[{index}] lacks domain or subject")
            continue
        if key in omitted_keys:
            errors.append(f"duplicate omitted representation subject {key}")
        omitted_keys.add(key)
        if not isinstance(item, dict) or item.get("reason_class") not in REPRESENTATION_OMISSION_REASONS:
            errors.append(f"omitted_subjects[{index}] has missing or invalid reason_class")
        if not isinstance(item, dict) or not _nonempty_string(item.get("rationale")):
            errors.append(f"omitted_subjects[{index}] requires a non-empty rationale")

    overlap = observed_keys & omitted_keys
    if overlap:
        errors.append(f"representation subjects cannot be both observed and omitted: {sorted(overlap)}")

    if registry_keys:
        unknown = (observed_keys | omitted_keys) - registry_keys
        missing = registry_keys - (observed_keys | omitted_keys)
        if unknown:
            errors.append(f"representation scope contains subjects outside the predefined registry: {sorted(unknown)}")
        if missing:
            errors.append(f"representation scope does not disposition all predefined subjects: {sorted(missing)}")

    representation = _obj(packet.get("representation_comparison"))
    representation_decision = representation.get("decision")
    if representation_decision == REPRESENTATION_NOT_RUN:
        if representation.get("result_artifact") not in {None, ""}:
            errors.append(
                "representation_comparison.result_artifact must be null when representation comparison was not run"
            )
        if observed_keys:
            errors.append(
                "jointly observed representation subjects exist, so representation comparison must be run"
            )
        if observer_used is True:
            errors.append(
                "observer structured captures exist, so representation comparison must be run rather than marked unavailable"
            )
    elif representation_decision in REPRESENTATION_DECISIONS:
        if not _nonempty_string(representation.get("result_artifact")):
            errors.append(
                "representation_comparison.result_artifact is required when representation comparison was run"
            )
        if not observed_keys:
            errors.append(
                "representation comparison cannot be run without at least one jointly observed predefined subject"
            )
    else:
        errors.append("representation_comparison.decision is missing or unknown")

    structured = _obj(packet.get("structured_comparison"))
    if observer_used is True:
        if not _nonempty_string(structured.get("result_artifact")):
            errors.append("structured_comparison.result_artifact is required when observer capture is used")
        if structured.get("decision") not in STRUCTURED_DECISIONS:
            errors.append("structured_comparison.decision is missing or unknown")
    else:
        if structured.get("decision") not in {None, "NOT_RUN_NO_UNROUNDED_CAPTURE"}:
            errors.append("structured comparison cannot claim a result without observer/unrounded capture")
        if structured.get("decision") == "NOT_RUN_NO_UNROUNDED_CAPTURE" and structured.get("result_artifact") not in {None, ""}:
            errors.append(
                "structured_comparison.result_artifact must be null when unrounded comparison was not run"
            )

    policy = _obj(packet.get("policy_assertions"))
    required_false = (
        "global_numeric_tolerance_applied",
        "legacy_residual_used_as_tolerance",
        "rounded_report_treated_as_unrounded_oracle",
        "representation_difference_auto_accepted",
        "b1_classified_as_independent_reference",
        "production_migration_admitted",
    )
    for field in required_false:
        if policy.get(field) is not False:
            errors.append(f"policy_assertions.{field} must be false")

    if policy.get("numerical_equivalence_qualified_by_packet") is not False:
        errors.append("the packet validator cannot qualify numerical equivalence")

    disposition = _obj(packet.get("disposition"))
    if disposition.get("b2_reference_status") not in {
        "CANDIDATE_NOT_QUALIFIED",
        "PROVENANCE_QUALIFIED_REFERENCE",
    }:
        errors.append("disposition.b2_reference_status must be explicit")
    if not _nonempty_string(disposition.get("next_action")):
        errors.append("disposition.next_action is required")

    packet_complete = not errors
    return {
        "evidence_class": "FIRST_REFERENCE_PACKET_COMPLETENESS_NOT_NUMERICAL_ADMISSION",
        "packet_schema_version": PACKET_SCHEMA_VERSION,
        "testcase_id": testcase_id,
        "representation_registry_subjects": len(registry_keys),
        "representation_jointly_observed_subjects": len(observed_keys),
        "representation_omitted_subjects": len(omitted_keys),
        "packet_complete": packet_complete,
        "errors": errors,
        "warnings": warnings,
        "comparison_may_still_be_fail_closed": True,
        "representation_difference_auto_accepted": False,
        "numerical_equivalence_qualified_by_this_tool": False,
        "b2_reference_qualified_by_this_tool": False,
        "production_migration_admitted": False,
        "decision": "PACKET_COMPLETE" if packet_complete else "PACKET_INCOMPLETE_FAIL_CLOSED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    try:
        report = validate_packet(load_packet(args.packet))
    except ValueError as exc:
        report = {
            "evidence_class": "FIRST_REFERENCE_PACKET_COMPLETENESS_NOT_NUMERICAL_ADMISSION",
            "packet_complete": False,
            "errors": [str(exc)],
            "warnings": [],
            "representation_difference_auto_accepted": False,
            "numerical_equivalence_qualified_by_this_tool": False,
            "b2_reference_qualified_by_this_tool": False,
            "production_migration_admitted": False,
            "decision": "PACKET_INCOMPLETE_FAIL_CLOSED",
        }

    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["packet_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
