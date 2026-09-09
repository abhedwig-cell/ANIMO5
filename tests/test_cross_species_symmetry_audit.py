import importlib.util
import unittest
from pathlib import Path


TOOL = Path(__file__).parents[1] / "tools" / "audit_cross_species_symmetry.py"
SPEC = importlib.util.spec_from_file_location("audit_cross_species_symmetry", TOOL)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CrossSpeciesSymmetryAuditTest(unittest.TestCase):
    def test_tcd023_style_asymmetry_is_flagged(self):
        source = """
      Transfon(17,Ln) = 1.0
      Transfon(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
      Transfop(17,Ln) = 2.0
      Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
"""
        findings, contextual, _ = MODULE.scan_sources({"synthetic.for": source})
        self.assertEqual(len(findings), 1)
        self.assertEqual(contextual, [])
        self.assertEqual(findings[0]["p_line"], 5)
        self.assertEqual(
            findings[0]["stale_n_siblings"],
            [{"n_token": "transfon", "expected_p_token": "transfop"}],
        )

    def test_correct_p_sibling_is_not_flagged(self):
        source = """
      Transfon(17,Ln) = 1.0
      Transfon(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
      Transfop(17,Ln) = 2.0
      Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)
"""
        findings, contextual, _ = MODULE.scan_sources({"synthetic.for": source})
        self.assertEqual(findings, [])
        self.assertEqual(contextual, [])

    def test_reciprocal_nutrient_coupling_is_not_promoted(self):
        source = """
      Rsamplni_pot = Rsamplni_pot - Rsamplni_pot * Pshort / Rsamplpo_pot
      Rsamplpo_pot = Rsamplpo_pot - Rsamplpo_pot * Nshort / Rsamplni_pot
      Rsamplni_act = Rsamplni_act + Rsamplpo_act
      Rsamplpo_act = Rsamplpo_act + Rsamplni_act
"""
        findings, _, _ = MODULE.scan_sources({"synthetic.for": source})
        self.assertEqual(findings, [])

    def test_unrelated_cross_species_ratio_is_not_promoted(self):
        source = """
      Pofrhu(Ln) = Pofrhuma * Nifrhu(Ln) / Nifrhuma
"""
        findings, _, _ = MODULE.scan_sources({"synthetic.for": source})
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
