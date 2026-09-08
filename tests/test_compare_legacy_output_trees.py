import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "compare_legacy_output_trees.py"
spec = importlib.util.spec_from_file_location("legacy_compare", TOOL)
legacy_compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy_compare)


class TestLegacyOutputComparator(unittest.TestCase):
    def test_declared_timestamp_difference_normalizes(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir)
            right = Path(right_dir)
            (left / "x.out").write_text(
                " File created on 2026-09-08 at 18:00:00.111 hr.\n"
                " value 1.25\n",
                encoding="latin1",
            )
            (right / "x.out").write_text(
                " File created on 2026-09-08 at 19:00:00.222 hr.\n"
                " value 1.25\n",
                encoding="latin1",
            )

            report = legacy_compare.compare_trees(left, right)
            self.assertEqual(
                report["decision"],
                "MATCH_AFTER_DECLARED_VOLATILE_NORMALIZATION",
            )
            self.assertFalse(report["reference_qualified_by_this_tool"])

    def test_scientific_number_difference_fails_closed(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir)
            right = Path(right_dir)
            (left / "x.out").write_text(
                " File created on 2026-09-08 at 18:00:00.111 hr.\n"
                " value 1.25\n",
                encoding="latin1",
            )
            (right / "x.out").write_text(
                " File created on 2026-09-08 at 19:00:00.222 hr.\n"
                " value 1.26\n",
                encoding="latin1",
            )

            report = legacy_compare.compare_trees(left, right)
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
            detail = report["files"]["x.out"]["numeric_difference_summary"]
            self.assertEqual(detail["different_numeric_tokens"], 1)
            self.assertIn("no acceptance tolerance", detail["note"])

    def test_extra_candidate_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir)
            right = Path(right_dir)
            (left / "x.out").write_text("same\n", encoding="latin1")
            (right / "x.out").write_text("same\n", encoding="latin1")
            (right / "extra.out").write_text("extra\n", encoding="latin1")

            report = legacy_compare.compare_trees(left, right)
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
            self.assertEqual(report["file_set"]["extra_candidate"], ["extra.out"])

    def test_raw_only_does_not_normalize_timestamp(self):
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir)
            right = Path(right_dir)
            (left / "x.out").write_text(
                " ANIMO run start: 2026-09-08  18:00:00.111\n",
                encoding="latin1",
            )
            (right / "x.out").write_text(
                " ANIMO run start: 2026-09-08  19:00:00.222\n",
                encoding="latin1",
            )

            report = legacy_compare.compare_trees(
                left,
                right,
                normalize_volatile=False,
            )
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")


if __name__ == "__main__":
    unittest.main()
