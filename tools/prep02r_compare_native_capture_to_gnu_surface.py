#!/usr/bin/env python3
"""Compare a validated PREP02R native Ruurlo capture with the explicit GNU surface.

This is cross-runtime diagnostic comparison only. It does not admit either side
as historical B2 evidence and never applies a scientific numerical tolerance.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

EXPECTED_SURFACE_SCHEMA = "animo-prep02r-gnu-ruurlo-file-surface-v1"
EXPECTED_SURFACE_CLASS = "GNU_DIAGNOSTIC_COMPARISON_SURFACE_NOT_HISTORICAL_REFERENCE"
EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_GNU_EXE_SHA256 = "0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _content_set_sha256(records: list[dict]) -> str:
    digest = hashlib.sha256()
    for item in sorted(records, key=lambda row: row["path"].encode("utf-8")):
        digest.update(item["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(item["normalized_size"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(item["normalized_sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def validate_surface(surface: dict) -> list[str]:
    errors: list[str] = []
    expected_pairs = {
        "schema": EXPECTED_SURFACE_SCHEMA,
        "evidence_class": EXPECTED_SURFACE_CLASS,
        "work_unit": "ANIMO-PREP02R",
        "case": "RuurloGrass",
        "source_zip_sha256": EXPECTED_SOURCE_SHA256,
        "testbank_zip_sha256": EXPECTED_TESTBANK_SHA256,
        "gnu_diagnostic_executable_sha256": EXPECTED_GNU_EXE_SHA256,
        "historical_reference_admitted": False,
        "normal_B2_reference_available": False,
    }
    for key, expected in expected_pairs.items():
        if surface.get(key) != expected:
            errors.append(f"surface {key}: expected {expected!r}, got {surface.get(key)!r}")

    files = surface.get("files")
    if not isinstance(files, list) or not files:
        errors.append("surface files must be a non-empty list")
        return errors
    paths = [item.get("path") for item in files]
    if any(not isinstance(path, str) or not path for path in paths):
        errors.append("surface contains invalid path")
    if len(paths) != len(set(paths)):
        errors.append("surface contains duplicate paths")
    for item in files:
        if not isinstance(item.get("normalized_size"), int) or item["normalized_size"] < 0:
            errors.append(f"surface invalid normalized_size for {item.get('path')!r}")
        digest = item.get("normalized_sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append(f"surface invalid normalized_sha256 for {item.get('path')!r}")

    expected_set = surface.get("surface_definition", {}).get(
        "normalized_surface_content_set_sha256"
    )
    actual_set = _content_set_sha256(files)
    if expected_set != actual_set:
        errors.append(
            "surface normalized content-set hash mismatch: "
            f"expected {expected_set!r}, recomputed {actual_set!r}"
        )
    declared_count = surface.get("surface_definition", {}).get("changed_or_new_file_count")
    if declared_count != len(files):
        errors.append(
            f"surface file count mismatch: declared {declared_count!r}, actual {len(files)}"
        )
    if surface.get("volatile_normalization", {}).get(
        "scientific_numeric_tolerance_applied"
    ) is not False:
        errors.append("surface must declare scientific_numeric_tolerance_applied=false")
    return errors


def _normalize_bytes(data: bytes, comparator: object) -> tuple[bytes, dict]:
    if b"\x00" in data:
        return data, {}
    return comparator.normalize_legacy_text(data)


def compare_case_to_surface(
    case_root: Path,
    baseline: list[dict],
    surface: dict,
    comparator: object,
    validator: object,
) -> dict:
    post = validator.inventory(case_root)
    changed, deleted = validator.delta(baseline, post)
    expected = {item["path"]: item for item in surface["files"]}
    actual_paths = {item["path"] for item in changed}
    expected_paths = set(expected)
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)

    files: dict[str, dict] = {}
    different: list[str] = []
    for path in sorted(expected_paths & actual_paths):
        data = (case_root / path).read_bytes()
        normalized, substitutions = _normalize_bytes(data, comparator)
        actual_size = len(normalized)
        actual_sha = sha256_bytes(normalized)
        target = expected[path]
        equal = (
            actual_size == target["normalized_size"]
            and actual_sha == target["normalized_sha256"]
        )
        if not equal:
            different.append(path)
        files[path] = {
            "classification": "MATCH" if equal else "DIFFERENT",
            "native_normalized_size": actual_size,
            "native_normalized_sha256": actual_sha,
            "gnu_normalized_size": target["normalized_size"],
            "gnu_normalized_sha256": target["normalized_sha256"],
            "volatile_substitutions": substitutions,
        }

    if missing or extra or deleted or different:
        decision = "DIFFERENT_FAIL_CLOSED"
    else:
        decision = "MATCH_EXPLICIT_GNU_SURFACE"
    return {
        "post_file_count": len(post),
        "changed_or_new_file_count": len(changed),
        "deleted_file_count": len(deleted),
        "deleted_files": [item["path"] for item in deleted],
        "missing_expected_paths": missing,
        "extra_native_paths": extra,
        "different_normalized_files": different,
        "files": files,
        "scientific_numeric_tolerance_applied": False,
        "decision": decision,
    }


def _load_tool(filename: str, module_name: str) -> object:
    path = Path(__file__).resolve().with_name(filename)
    if not path.is_file():
        raise FileNotFoundError(f"missing required tool beside comparator: {path}")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capture_path", type=Path)
    parser.add_argument(
        "--gnu-surface",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "integration"
        / "animo-prep"
        / "PREP02R_GNU_RUURLO_FILE_SURFACE_20260909.json",
    )
    parser.add_argument(
        "--input-pin",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "integration"
        / "animo-prep"
        / "PREP02R_RUURLO_NATIVE_INPUT_PIN_20260909.json",
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    try:
        validator = _load_tool(
            "prep02r_validate_native_capture.py", "prep02r_native_validator"
        )
        comparator = validator._load_comparator()
        surface = json.loads(args.gnu_surface.read_text(encoding="utf-8"))
        surface_errors = validate_surface(surface)
        input_pin = json.loads(args.input_pin.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix="prep02r-native-gnu-") as tmp:
            root = validator._capture_root(args.capture_path.resolve(), Path(tmp))
            validation = validator.validate_capture(root, input_pin, comparator)
            repeat_decision = validation.get("repeat_determinism", {}).get("decision")
            eligible = (
                not surface_errors
                and validation.get("capture_integrity") == "PASS"
                and repeat_decision
                in {"NATIVE_REPEAT_EXACT_RAW", "NATIVE_REPEAT_DECLARED_VOLATILE_ONLY"}
            )
            run_reports = []
            if eligible:
                baseline = input_pin["files"]
                for run in (1, 2):
                    run_reports.append(
                        compare_case_to_surface(
                            root / f"run{run}" / "RuurloGrass",
                            baseline,
                            surface,
                            comparator,
                            validator,
                        )
                    )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {
            "schema": "animo-prep02r-native-vs-gnu-surface-v1",
            "evidence_class": "CROSS_RUNTIME_DIAGNOSTIC_COMPARISON_NOT_REFERENCE_ADMISSION",
            "errors": [str(exc)],
            "historical_reference_admitted": False,
            "normal_B2_reference_available": False,
            "decision": "COMPARISON_INPUT_FAIL_CLOSED",
        }
    else:
        errors = list(surface_errors)
        if validation.get("capture_integrity") != "PASS":
            errors.append("native capture integrity is not PASS")
        if repeat_decision not in {
            "NATIVE_REPEAT_EXACT_RAW",
            "NATIVE_REPEAT_DECLARED_VOLATILE_ONLY",
        }:
            errors.append(
                f"native repeat is not qualified for comparison: {repeat_decision!r}"
            )
        if errors:
            decision = "COMPARISON_BLOCKED_FAIL_CLOSED"
        elif all(item["decision"] == "MATCH_EXPLICIT_GNU_SURFACE" for item in run_reports):
            decision = (
                "CROSS_RUNTIME_MATCH_ON_EXPLICIT_GNU_SURFACE_"
                "NOT_HISTORICAL_REFERENCE"
            )
        else:
            decision = (
                "CROSS_RUNTIME_DIFFERENT_FAIL_CLOSED_NOT_HISTORICAL_REFERENCE"
            )
        report = {
            "schema": "animo-prep02r-native-vs-gnu-surface-v1",
            "evidence_class": "CROSS_RUNTIME_DIAGNOSTIC_COMPARISON_NOT_REFERENCE_ADMISSION",
            "surface_validation_errors": surface_errors,
            "native_capture_validation_decision": validation.get("decision"),
            "native_repeat_decision": repeat_decision,
            "errors": errors,
            "runs": run_reports if not errors else [],
            "scientific_numeric_tolerance_applied": False,
            "historical_reference_admitted": False,
            "normal_B2_reference_available": False,
            "production_migration_admitted": False,
            "decision": decision,
        }

    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["decision"].startswith("CROSS_RUNTIME_MATCH_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
