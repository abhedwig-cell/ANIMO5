import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "analyze_massledger_b1_sidecars.py"
spec = importlib.util.spec_from_file_location("massq", MODULE_PATH)
massq = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(massq)


class AnalyzeMassLedgerSidecarsTest(unittest.TestCase):
    def make_case(self, start: str, result_begin: str, step: str):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "Case"
        root.mkdir()
        (root / massq.START_FILE).write_text(start, encoding="utf-8")
        (root / massq.RESULT_BEGIN_FILE).write_text(result_begin, encoding="utf-8")
        (root / massq.STEP_FILE).write_text(step, encoding="utf-8")
        return tmp, root

    def test_water_uses_persisted_start(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "1 1 999 999 999\n",
            "W 1 1 999 2 1 0 11 12345 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["W"]["max_abs_residual"], 0.0)
        finally:
            tmp.cleanup()

    def test_first_chemical_interval_uses_initialized_start(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "1 1 0 0 0\n",
            "N 1 1 999 0 0 0 20 999 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["N"]["max_abs_residual"], 0.0)
            self.assertEqual(
                report["elements"]["N"]["begin_storage_source_at_max"],
                massq.START_FILE,
            )
        finally:
            tmp.cleanup()

    def test_subsequent_chemical_interval_uses_previous_result_state(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n2 1 10 90 90 90 0 0\n",
            "1 1 0 0 0\n2 1 19.5 30 40\n",
            "N 1 1 20 0 0 0 20 0 0 0 0 0\n"
            "N 2 1 999 0 0 0 19.5 999 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["N"]["max_abs_residual"], 0.0)
        finally:
            tmp.cleanup()

    def test_preserves_nonclosure_without_tolerance(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n2 1 10 20 30 40 0 0\n",
            "1 1 0 0 0\n2 1 20 30 40\n",
            "N 1 1 20 0 0 0 20 0 0 0 0 0\n"
            "N 2 1 20 0 0 0 19.5 0 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["N"]["signed_residual_at_max"], 0.5)
            self.assertFalse(report["elements"]["N"]["acceptance_tolerance_applied"])
        finally:
            tmp.cleanup()

    def test_missing_previous_result_fails_closed(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n2 1 10 20 30 40 0 0\n",
            "1 1 0 0 0\n",
            "P 1 1 30 0 0 0 30 0 0 0 0 0\n"
            "P 2 1 30 0 0 0 30 0 0 0 0 0\n",
        )
        try:
            with self.assertRaisesRegex(ValueError, "missing previous-result begin snapshot"):
                massq.analyze_case(root)
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
