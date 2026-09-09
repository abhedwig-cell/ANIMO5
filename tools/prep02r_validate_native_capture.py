#!/usr/bin/env python3
"""Validate and classify a PREP02R Ruurlo native capture bundle.

This tool validates capture integrity, recomputes the frozen-input delta for both
runs, and classifies repeat determinism. It never admits the received executable
or any output as a historical B2 reference.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Iterable

SCHEMA = "animo-prep02r-ruurlo-native-harness-capture-v1"
EVIDENCE_CLASS = "CROSS_RUNTIME_DIAGNOSTIC_NATIVE_NOT_REFERENCE_ADMISSION"
EXPECTED_EXE_SHA256 = "40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d"
EXPECTED_TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_CASE_CONTENT_SET = "0f12d19f74e6640b6d17f8f401ac9c294e35ae13064205ed4d1821d6a15c9ac9"
EXPECTED_HYDROLOGY_SHA256 = "36d8dbeee7a46c769026c7441ea607160a715768571ba3e048b32ee2ace74d13"
MANIFEST_NAME = "PREP02R_RUURLO_NATIVE_CAPTURE.json"
FORBIDDEN_TRANSFER_BASENAMES = {"animo41.exe"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_set_sha256(records: Iterable[dict]) -> str:
    digest = hashlib.sha256()
    for item in sorted(records, key=lambda row: row["path"].encode("utf-8")):
        digest.update(item["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(item["size"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(item["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def inventory(root: Path) -> list[dict]:
    records = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return sorted(records, key=lambda row: row["path"].encode("utf-8"))


def record_map(records: Iterable[dict]) -> dict[str, dict]:
    return {item["path"]: item for item in records}


def delta(baseline: list[dict], post: list[dict]) -> tuple[list[dict], list[dict]]:
    before = record_map(baseline)
    after = record_map(post)
    changed_or_new = [
        item
        for item in post
        if item["path"] not in before
        or item["sha256"] != before[item["path"]]["sha256"]
    ]
    deleted = [item for item in baseline if item["path"] not in after]
    return changed_or_new, deleted


def _load_comparator() -> object:
    tool = Path(__file__).resolve().with_name("compare_legacy_output_trees.py")
    if not tool.is_file():
        raise FileNotFoundError(f"missing comparator beside validator: {tool}")
    spec = importlib.util.spec_from_file_location("prep02r_legacy_compare", tool)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _safe_extract(zip_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            name = PurePosixPath(info.filename.replace("\\", "/"))
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"unsafe ZIP member path: {info.filename}")
            mode = (info.external_attr >> 16) & 0o170000
            if mode == 0o120000:
                raise ValueError(f"symlink ZIP member rejected: {info.filename}")
        archive.extractall(destination)


def _capture_root(path: Path, temp_root: Path) -> Path:
    if path.is_dir():
        return path.resolve()
    if not path.is_file() or not zipfile.is_zipfile(path):
        raise ValueError("capture_path must be a directory or ZIP archive")
    _safe_extract(path, temp_root)
    if (temp_root / MANIFEST_NAME).is_file():
        return temp_root
    candidates = [p for p in temp_root.iterdir() if p.is_dir()]
    if len(candidates) == 1 and (candidates[0] / MANIFEST_NAME).is_file():
        return candidates[0]
    raise ValueError(f"{MANIFEST_NAME} not found at capture root")


def _check_equal(errors: list[str], label: str, actual, expected) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def validate_capture(capture_root: Path, input_pin: dict, comparator: object) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = capture_root / MANIFEST_NAME
    if not manifest_path.is_file():
        return {
            "capture_integrity": "FAIL",
            "errors": [f"missing {MANIFEST_NAME}"],
        }
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))

    _check_equal(errors, "schema", manifest.get("schema"), SCHEMA)
    _check_equal(
        errors,
        "evidence_class",
        manifest.get("evidence_class"),
        EVIDENCE_CLASS,
    )
    _check_equal(errors, "work_unit", manifest.get("work_unit"), "ANIMO-PREP02R")
    _check_equal(errors, "case", manifest.get("case"), "RuurloGrass")

    exe = manifest.get("executable", {})
    _check_equal(errors, "executable.filename", exe.get("filename"), "animo41.exe")
    _check_equal(errors, "executable.sha256", exe.get("sha256"), EXPECTED_EXE_SHA256)
    _check_equal(
        errors,
        "executable.classification",
        exe.get("classification"),
        "MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE",
    )
    _check_equal(
        errors,
        "executable.bytes_in_transfer_bundle",
        exe.get("bytes_in_transfer_bundle"),
        False,
    )
    _check_equal(
        errors,
        "executable.historical_reference_admitted",
        exe.get("historical_reference_admitted"),
        False,
    )
    _check_equal(
        errors,
        "executable.native_execution_attempt_admitted",
        exe.get("native_execution_attempt_admitted"),
        True,
    )

    inp = manifest.get("input", {})
    _check_equal(
        errors,
        "input.testbank_zip_sha256",
        inp.get("testbank_zip_sha256"),
        EXPECTED_TESTBANK_SHA256,
    )
    _check_equal(
        errors,
        "input.case_content_set_sha256",
        inp.get("case_content_set_sha256"),
        EXPECTED_CASE_CONTENT_SET,
    )
    _check_equal(
        errors,
        "input.hydrology_sha256",
        inp.get("hydrology_sha256"),
        EXPECTED_HYDROLOGY_SHA256,
    )
    _check_equal(
        errors,
        "input.input_content_transformed",
        inp.get("input_content_transformed"),
        False,
    )

    _check_equal(
        errors,
        "input pin case content set",
        input_pin.get("case_file_content_set_sha256"),
        EXPECTED_CASE_CONTENT_SET,
    )
    baseline = input_pin.get("files", [])
    if content_set_sha256(baseline) != EXPECTED_CASE_CONTENT_SET:
        errors.append(
            "input pin file inventory does not reproduce pinned Ruurlo content-set hash"
        )

    forbidden = []
    for path in capture_root.rglob("*"):
        if path.is_file() and path.name.casefold() in FORBIDDEN_TRANSFER_BASENAMES:
            forbidden.append(path.relative_to(capture_root).as_posix())
    if forbidden:
        errors.append(
            f"forbidden executable bytes present in transfer bundle: {forbidden}"
        )
    if (capture_root / "_frozen_testbank_extract").exists():
        errors.append(
            "temporary frozen testbank extraction directory present in transfer bundle"
        )

    runs = manifest.get("runs")
    if not isinstance(runs, list) or len(runs) != 2:
        errors.append("manifest must contain exactly two runs")
        runs = []

    run_reports = []
    for expected_run, run in enumerate(runs, start=1):
        if run.get("run") != expected_run:
            errors.append(f"run order/id mismatch at entry {expected_run}")
        run_root = capture_root / f"run{expected_run}"
        case_root = run_root / "RuurloGrass"
        stdout_path = run_root / "stdout.txt"
        stderr_path = run_root / "stderr.txt"
        if not case_root.is_dir():
            errors.append(f"run{expected_run}: missing RuurloGrass directory")
            continue
        if not stdout_path.is_file() or not stderr_path.is_file():
            errors.append(f"run{expected_run}: missing stdout.txt or stderr.txt")
            continue

        post = inventory(case_root)
        changed, deleted = delta(baseline, post)
        manifest_changed = run.get("changed_or_new_case_files", [])
        manifest_deleted = run.get("deleted_case_files", [])

        checks = {
            "pre_file_count": run.get("pre_case_file_count") == len(baseline),
            "pre_content_set": run.get("pre_case_content_set_sha256")
            == EXPECTED_CASE_CONTENT_SET,
            "post_content_set": run.get("post_case_content_set_sha256")
            == content_set_sha256(post),
            "post_file_count": run.get("post_case_file_count") == len(post),
            "changed_records": manifest_changed == changed,
            "changed_content_set": run.get("changed_or_new_content_set_sha256")
            == content_set_sha256(changed),
            "deleted_records": manifest_deleted == deleted,
            "deleted_content_set": run.get("deleted_content_set_sha256")
            == content_set_sha256(deleted),
            "stdout_size": run.get("stdout_size") == stdout_path.stat().st_size,
            "stdout_sha256": run.get("stdout_sha256") == sha256_file(stdout_path),
            "stderr_size": run.get("stderr_size") == stderr_path.stat().st_size,
            "stderr_sha256": run.get("stderr_sha256") == sha256_file(stderr_path),
            "input_content_transformed": run.get("input_content_transformed") is False,
        }
        for name, passed in checks.items():
            if not passed:
                errors.append(f"run{expected_run}: {name} check failed")
        if run.get("exit_status") != 0:
            warnings.append(
                f"run{expected_run}: nonzero exit status {run.get('exit_status')}"
            )
        run_reports.append(
            {
                "run": expected_run,
                "post_file_count": len(post),
                "changed_or_new_file_count": len(changed),
                "deleted_file_count": len(deleted),
                "exit_status": run.get("exit_status"),
                "checks": checks,
            }
        )

    repeat = {"decision": "NOT_EVALUATED"}
    if len(runs) == 2 and all(
        (capture_root / f"run{i}" / "RuurloGrass").is_dir() for i in (1, 2)
    ):
        tree_report = comparator.compare_trees(
            capture_root / "run1" / "RuurloGrass",
            capture_root / "run2" / "RuurloGrass",
        )
        stdout_report = comparator.compare_file(
            capture_root / "run1" / "stdout.txt",
            capture_root / "run2" / "stdout.txt",
            normalize_volatile=True,
        )
        stderr_report = comparator.compare_file(
            capture_root / "run1" / "stderr.txt",
            capture_root / "run2" / "stderr.txt",
            normalize_volatile=True,
        )
        classifications = [
            tree_report["decision"],
            stdout_report["classification"],
            stderr_report["classification"],
        ]
        if tree_report["decision"] == "MATCH_EXACT" and all(
            c == "EQUAL_RAW" for c in classifications[1:]
        ):
            repeat_decision = "NATIVE_REPEAT_EXACT_RAW"
        elif tree_report["decision"] in {
            "MATCH_EXACT",
            "MATCH_AFTER_DECLARED_VOLATILE_NORMALIZATION",
        } and all(
            c in {
                "EQUAL_RAW",
                "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY",
            }
            for c in classifications[1:]
        ):
            repeat_decision = "NATIVE_REPEAT_DECLARED_VOLATILE_ONLY"
        else:
            repeat_decision = "NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED"
        repeat = {
            "decision": repeat_decision,
            "tree_comparison": tree_report,
            "stdout_comparison": stdout_report,
            "stderr_comparison": stderr_report,
            "scientific_numeric_tolerance_applied": False,
        }
        manifest_repeat = manifest.get("repeat_determinism", {}).get(
            "classification"
        )
        run1 = runs[0]
        run2 = runs[1]
        expected_manifest_repeat = (
            "NATIVE_REPEAT_EXACT_RAW"
            if run1.get("post_case_content_set_sha256")
            == run2.get("post_case_content_set_sha256")
            and run1.get("stdout_sha256") == run2.get("stdout_sha256")
            and run1.get("stderr_sha256") == run2.get("stderr_sha256")
            else "NATIVE_REPEAT_DIFFERENT_REQUIRES_DECLARED_VOLATILE_CLASSIFICATION"
        )
        if manifest_repeat != expected_manifest_repeat:
            errors.append(
                "manifest repeat classification inconsistent with captured raw hashes: "
                f"expected {expected_manifest_repeat}, got {manifest_repeat!r}"
            )

    reference = manifest.get("reference_admission", {})
    _check_equal(
        errors,
        "reference_admission.historical_reference_environment_qualified",
        reference.get("historical_reference_environment_qualified"),
        False,
    )
    _check_equal(
        errors,
        "reference_admission.normal_B2_reference_available",
        reference.get("normal_B2_reference_available"),
        False,
    )
    _check_equal(
        errors,
        "reference_admission.decision",
        reference.get("decision"),
        "NOT_A_REFERENCE_ADMISSION_ACTION",
    )
    _check_equal(
        errors,
        "production_migration_admitted",
        manifest.get("production_migration_admitted"),
        False,
    )

    integrity = "PASS" if not errors else "FAIL"
    if integrity == "FAIL":
        decision = "CAPTURE_INTEGRITY_FAIL_CLOSED"
    elif repeat.get("decision") == "NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED":
        decision = (
            "CAPTURE_VALID_REPEAT_DIFFERENT_FAIL_CLOSED_NOT_REFERENCE_ADMISSION"
        )
    else:
        decision = (
            "CAPTURE_VALID_REPEAT_QUALIFIED_CROSS_RUNTIME_DIAGNOSTIC_"
            "NOT_REFERENCE_ADMISSION"
        )

    return {
        "schema": "animo-prep02r-native-capture-validation-v1",
        "evidence_class": "CAPTURE_VALIDATION_NOT_REFERENCE_ADMISSION",
        "capture_integrity": integrity,
        "errors": errors,
        "warnings": warnings,
        "runs": run_reports,
        "repeat_determinism": repeat,
        "reference_admitted": False,
        "normal_B2_reference_available": False,
        "scientific_numeric_tolerance_applied": False,
        "decision": decision,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capture_path", type=Path)
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

    comparator = _load_comparator()
    input_pin = json.loads(args.input_pin.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="prep02r-native-capture-") as tmp:
        try:
            root = _capture_root(args.capture_path.resolve(), Path(tmp))
            report = validate_capture(root, input_pin, comparator)
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            report = {
                "schema": "animo-prep02r-native-capture-validation-v1",
                "evidence_class": "CAPTURE_VALIDATION_NOT_REFERENCE_ADMISSION",
                "capture_integrity": "FAIL",
                "errors": [str(exc)],
                "reference_admitted": False,
                "normal_B2_reference_available": False,
                "decision": "CAPTURE_INTEGRITY_FAIL_CLOSED",
            }

    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    if report.get("capture_integrity") != "PASS":
        return 2
    if (
        report.get("repeat_determinism", {}).get("decision")
        == "NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED"
    ):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
