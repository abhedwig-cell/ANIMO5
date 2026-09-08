import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_balance_deviations.py"
spec = importlib.util.spec_from_file_location("audit_balance_deviations", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestBalanceDeviationAudit(unittest.TestCase):
    def test_parse_water_record1(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bawaTP.Out"
            p.write_text(
                "header\n"
                " 1  1992      1   1  0.0 0.0  10.0 11.0 0.0 0.0  -2.50E-03  1.25E-02\n",
                encoding="ascii",
            )
            rows = mod.parse_file(p, -2, -1)
            self.assertEqual(len(rows), 1)
            self.assertAlmostEqual(rows[0]["period_deviation"], -0.0025)
            self.assertAlmostEqual(rows[0]["cumulative_deviation"], 0.0125)
            self.assertEqual(rows[0]["year"], 1992)

    def test_baom_three_residual_pairs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            case = root / "Case"
            case.mkdir()
            (case / "baomTP.Out").write_text(
                " 1  2000  365 365  1 2 3 4 5 6  1.0E-8 2.0E-8  3.0E-9 4.0E-9  5.0E-4 6.0E-4\n",
                encoding="ascii",
            )
            result = mod.audit(root, ["Case"])
            self.assertAlmostEqual(result["balances"]["fresh_organic_matter"]["max_abs_period_deviation"], 1.0e-8)
            self.assertAlmostEqual(result["balances"]["humus"]["max_abs_period_deviation"], 3.0e-9)
            self.assertAlmostEqual(result["balances"]["dissolved_organic_matter"]["max_abs_period_deviation"], 5.0e-4)

    def test_no_threshold_is_applied(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "Case").mkdir()
            result = mod.audit(root, ["Case"])
            self.assertEqual(
                result["evidence_class"],
                "DIAGNOSTIC_OUTPUT_RESIDUAL_ENVELOPE_NOT_ACCEPTANCE_THRESHOLD",
            )


if __name__ == "__main__":
    unittest.main()
