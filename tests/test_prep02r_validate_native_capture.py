import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

TOOL = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "prep02r_validate_native_capture.py"
)
spec = importlib.util.spec_from_file_location("prep02r_capture_validator", TOOL)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def synthetic_input_pin() -> dict:
    files = [
        {"path": "Input/A.INP", "size": 1, "sha256": sha256_bytes(b"a")},
        {"path": "animo.ini", "size": 1, "sha256": sha256_bytes(b"i")},
    ]
    return {
        "case_file_content_set_sha256": validator.content_set_sha256(files),
        "files": files,
    }


def write_capture(
    root: Path,
    pin: dict,
    *,
    output_by_run: tuple[bytes, bytes] = (b"same\n", b"same\n"),
    delete_input: bool = False,
    omit_changed_from_manifest: bool = False,
    include_executable: bool = False,
) -> None:
    run_records = []
    for run in (1, 2):
        run_root = root / f"run{run}"
        case_root = run_root / "RuurloGrass"
        (case_root / "Input").mkdir(parents=True)
        if not delete_input:
            (case_root / "Input" / "A.INP").write_bytes(b"a")
        (case_root / "animo.ini").write_bytes(b"i")
        (case_root / "out.txt").write_bytes(output_by_run[run - 1])
        (run_root / "stdout.txt").write_bytes(b"ok\n")
        (run_root / "stderr.txt").write_bytes(b"")

        post = validator.inventory(case_root)
        changed, deleted = validator.delta(pin["files"], post)
        manifest_changed = [] if omit_changed_from_manifest else changed
        run_records.append(
            {
                "run": run,
                "exit_status": 0,
                "input_content_transformed": False,
                "pre_case_content_set_sha256": pin[
                    "case_file_content_set_sha256"
                ],
                "post_case_content_set_sha256": validator.content_set_sha256(post),
                "post_case_file_count": len(post),
                "changed_or_new_case_files": manifest_changed,
                "changed_or_new_content_set_sha256": validator.content_set_sha256(
                    manifest_changed
                ),
                "deleted_case_files": deleted,
                "deleted_content_set_sha256": validator.content_set_sha256(deleted),
                "stdout_sha256": validator.sha256_file(run_root / "stdout.txt"),
                "stderr_sha256": validator.sha256_file(run_root / "stderr.txt"),
            }
        )

    manifest = {
        "schema": validator.SCHEMA,
        "evidence_class": validator.EVIDENCE_CLASS,
        "work_unit": "ANIMO-PREP02R",
        "case": "RuurloGrass",
        "executable": {
            "sha256": validator.EXPECTED_EXE_SHA256,
            "classification": "MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE",
            "bytes_in_transfer_bundle": False,
            "historical_reference_admitted": False,
        },
        "input": {
            "testbank_zip_sha256": validator.EXPECTED_TESTBANK_SHA256,
            "case_content_set_sha256": pin["case_file_content_set_sha256"],
            "hydrology_sha256": validator.EXPECTED_HYDROLOGY_SHA256,
            "input_content_transformed": False,
        },
        "runs": run_records,
        "repeat_determinism": {"classification": "NATIVE_REPEAT_EXACT_RAW"},
    }
    (root / validator.MANIFEST_NAME).write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    if include_executable:
        (root / "run1" / "animo41.exe").write_bytes(b"forbidden")


class TestPrep02RNativeCaptureValidator(unittest.TestCase):
    def setUp(self):
        self.pin = synthetic_input_pin()
        self.original_case_hash = validator.EXPECTED_CASE_CONTENT_SET
        validator.EXPECTED_CASE_CONTENT_SET = self.pin[
            "case_file_content_set_sha256"
        ]
        self.comparator = validator._load_comparator()

    def tearDown(self):
        validator.EXPECTED_CASE_CONTENT_SET = self.original_case_hash

    def test_valid_exact_repeat_capture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_capture(root, self.pin)
            report = validator.validate_capture(root, self.pin, self.comparator)
            self.assertEqual(report["capture_integrity"], "PASS")
            self.assertEqual(
                report["repeat_determinism"]["decision"],
                "NATIVE_REPEAT_EXACT_RAW",
            )
            self.assertFalse(report["reference_admitted"])
            self.assertFalse(report["normal_B2_reference_available"])

    def test_declared_volatile_only_repeat_is_not_numerically_toleranced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_capture(
                root,
                self.pin,
                output_by_run=(
                    b" File created on 2026-09-09 at 10:00:00.111 hr.\n value 1.0\n",
                    b" File created on 2026-09-09 at 11:00:00.222 hr.\n value 1.0\n",
                ),
            )
            report = validator.validate_capture(root, self.pin, self.comparator)
            self.assertEqual(report["capture_integrity"], "PASS")
            self.assertEqual(
                report["repeat_determinism"]["decision"],
                "NATIVE_REPEAT_DECLARED_VOLATILE_ONLY",
            )
            self.assertFalse(
                report["repeat_determinism"]["scientific_numeric_tolerance_applied"]
            )

    def test_unlisted_changed_file_fails_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_capture(root, self.pin, omit_changed_from_manifest=True)
            report = validator.validate_capture(root, self.pin, self.comparator)
            self.assertEqual(report["capture_integrity"], "FAIL")
            self.assertTrue(
                any("changed_records" in error for error in report["errors"])
            )

    def test_declared_file_deletion_is_recomputed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_capture(root, self.pin, delete_input=True)
            report = validator.validate_capture(root, self.pin, self.comparator)
            self.assertEqual(report["capture_integrity"], "PASS")
            self.assertEqual(report["runs"][0]["deleted_file_count"], 1)

    def test_executable_bytes_in_transfer_fail_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_capture(root, self.pin, include_executable=True)
            report = validator.validate_capture(root, self.pin, self.comparator)
            self.assertEqual(report["capture_integrity"], "FAIL")
            self.assertTrue(
                any("forbidden executable" in error for error in report["errors"])
            )


if __name__ == "__main__":
    unittest.main()
