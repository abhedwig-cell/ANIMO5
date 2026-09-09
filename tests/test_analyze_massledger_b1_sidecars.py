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
    def make_case(self, start: str, chem_start: str, step: str, cfracom: float = 0.58):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "Case"
        (root / "Input").mkdir(parents=True)
        (root / massq.START_FILE).write_text(start, encoding="utf-8")
        (root / massq.CHEM_START_FILE).write_text(chem_start, encoding="utf-8")
        (root / massq.STEP_FILE).write_text(step, encoding="utf-8")
        (root / "animo.ini").write_text(
            'Animo41\nMAT="Input/material.inp"\nEND\n', encoding="latin1"
        )
        (root / "Input" / "MATERIAL.INP").write_text(
            f">orgcom: definition\n  {cfracom}\n", encoding="latin1"
        )
        return tmp, root

    def test_water_uses_persisted_start(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "1 1 999 999 999 0 0\n",
            "W 1 1 999 2 1 0 11 12345 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["W"]["max_abs_residual"], 0.0)
            self.assertEqual(
                report["elements"]["W"]["begin_storage_source_at_max"],
                massq.START_FILE,
            )
        finally:
            tmp.cleanup()

    def test_chemical_interval_uses_process_start_snapshot(self):
        tmp, root = self.make_case(
            "1 1 10 90 90 90 0 0\n",
            "1 1 19.5 30 40 0 0\n",
            "N 1 1 999 0 0 0 19.5 999 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["N"]["max_abs_residual"], 0.0)
            self.assertEqual(
                report["elements"]["N"]["begin_storage_source_at_max"],
                massq.CHEM_START_FILE,
            )
        finally:
            tmp.cleanup()

    def test_preserves_nonclosure_without_tolerance(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "1 1 20 30 40 0 0\n",
            "N 1 1 20 0 0 0 19.5 0 0 0 0 0\n",
        )
        try:
            report = massq.analyze_case(root)
            self.assertEqual(report["elements"]["N"]["signed_residual_at_max"], 0.5)
            self.assertFalse(report["elements"]["N"]["acceptance_tolerance_applied"])
        finally:
            tmp.cleanup()

    def test_missing_chemical_start_fails_closed(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n2 1 10 20 30 40 0 0\n",
            "1 1 20 30 40 0 0\n",
            "P 1 1 30 0 0 0 30 0 0 0 0 0\n"
            "P 2 1 30 0 0 0 30 0 0 0 0 0\n",
        )
        try:
            with self.assertRaisesRegex(ValueError, "missing chemical start snapshot"):
                massq.analyze_case(root)
        finally:
            tmp.cleanup()

    def test_soil_organic_carbon_projection_uses_source_cfracom(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "1 1 20 30 40 0 0\n",
            "O 1 1 40 0 0 0 39.5 0 0 0 0 0\n",
            cfracom=0.58,
        )
        try:
            report = massq.analyze_case(root)
            self.assertAlmostEqual(report["elements"]["C"]["signed_residual_at_max"], 0.29)
            self.assertEqual(report["elements"]["C"]["Cfracom"], 0.58)
            self.assertFalse(report["elements"]["C"]["whole_system_elemental_carbon_claim"])
        finally:
            tmp.cleanup()

    def test_invalid_cfracom_fails_closed(self):
        tmp, root = self.make_case(
            "1 1 10 20 30 40 0 0\n",
            "1 1 20 30 40 0 0\n",
            "O 1 1 40 0 0 0 40 0 0 0 0 0\n",
            cfracom=1.2,
        )
        try:
            with self.assertRaisesRegex(ValueError, "Cfracom outside"):
                massq.analyze_case(root)
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
