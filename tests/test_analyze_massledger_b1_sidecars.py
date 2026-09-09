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
    def make_case(self, start: str, step: str):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "Case"
        root.mkdir()
        (root / massq.START_FILE).write_text(start, encoding="utf-8")
        (root / massq.STEP_FILE).write_text(step, encoding="utf-8")
        return tmp, root

    def test_uses_persisted_begin_not_recomputed_begin_or_residual(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "W 1 1 999 2 1 0 11 12345 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["W"]["max_abs_residual"], 0.0)
            self.assertFalse(report["elements"]["W"]["acceptance_tolerance_applied"])
        finally:
            tmp.cleanup()

    def test_preserves_nonclosure_without_tolerance(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "N 1 1 20 0 0 0 19.5 0 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["N"]["signed_residual_at_max"], 0.5)
        finally:
            tmp.cleanup()

    def test_missing_begin_fails_closed(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "P 2 1 30 0 0 0 30 0 0 0 0 0\n",
        )
        try:
            with self.assertRaisesRegex(ValueError, "missing persisted start snapshot"):
                massq.analyze_case(root)
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
