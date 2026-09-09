import hashlib
import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "capture_reference_artifact_manifest.py"
spec = importlib.util.spec_from_file_location("artifact_receipt", TOOL)
artifact_receipt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = artifact_receipt
spec.loader.exec_module(artifact_receipt)


class TestReferenceArtifactReceipt(unittest.TestCase):
    def test_single_file_receipt_hashes_without_admission(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "animo41.exe"
            path.write_bytes(b"historical bytes")
            expected = hashlib.sha256(b"historical bytes").hexdigest()

            report = artifact_receipt.capture_artifact(
                path,
                label="received animo41.exe",
                artifact_class="historical_executable",
                expected_sha256=expected,
                captured_at_utc="2026-09-09T00:00:00+00:00",
            )

            self.assertEqual(report["artifact"]["sha256"], expected)
            self.assertFalse(report["reference_admitted"])
            self.assertFalse(report["native_execution_admitted"])
            self.assertFalse(report["receipt_checks"]["artifact_executed_by_this_tool"])

    def test_directory_content_set_is_stable_across_root_names(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir)
            right = Path(right_dir)
            (left / "a.txt").write_text("alpha", encoding="utf-8")
            (left / "sub").mkdir()
            (left / "sub" / "b.bin").write_bytes(b"beta")
            (right / "a.txt").write_text("alpha", encoding="utf-8")
            (right / "sub").mkdir()
            (right / "sub" / "b.bin").write_bytes(b"beta")

            first = artifact_receipt.capture_artifact(
                left,
                label="bundle A",
                artifact_class="historical_output_bundle",
                captured_at_utc="2026-09-09T00:00:00+00:00",
            )
            second = artifact_receipt.capture_artifact(
                right,
                label="bundle B",
                artifact_class="historical_output_bundle",
                captured_at_utc="2026-09-09T00:00:00+00:00",
            )

            self.assertEqual(
                first["artifact"]["content_set_sha256"],
                second["artifact"]["content_set_sha256"],
            )
            self.assertEqual(first["artifact"]["file_count"], 2)

    def test_expected_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "candidate.exe"
            path.write_bytes(b"bytes")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                artifact_receipt.capture_artifact(
                    path,
                    label="candidate",
                    artifact_class="historical_executable",
                    expected_sha256="0" * 64,
                    captured_at_utc="2026-09-09T00:00:00+00:00",
                )

    def test_expected_hash_rejected_for_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "x.txt").write_text("x", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "single-file"):
                artifact_receipt.capture_artifact(
                    root,
                    label="bundle",
                    artifact_class="historical_output_bundle",
                    expected_sha256="0" * 64,
                    captured_at_utc="2026-09-09T00:00:00+00:00",
                )


if __name__ == "__main__":
    unittest.main()
