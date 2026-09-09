import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "audit_stable_dom_plough_accumulators.py"
spec = importlib.util.spec_from_file_location("audit_stable_dom", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class StableDomAccumulatorAuditTests(unittest.TestCase):
    def test_confirms_three_self_reads_without_prior_definition(self):
        src = """
      If (Pl(I) .Gt. 0) Then
      SuStdiorma = SuStdiorma + X
      SuStdiorni = SuStdiorni + Y
      If(Ipo.Eq.1) SuStdiorpo = SuStdiorpo + Z
      End If
"""
        result = mod.analyze_text(src)
        self.assertEqual(result["overall_classification"], "CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION")
        self.assertEqual(result["plough_event_branch_lines"], [2])
        self.assertEqual(result["targets"]["SuStdiorpo"]["first_self_read_assignment"]["line"], 5)

    def test_prior_zero_reset_prevents_confirmation(self):
        src = """
      SuStdiorma = 0.0
      SuStdiorni = 0.0
      SuStdiorpo = 0.0
      If (Pl(I) .Gt. 0) Then
      SuStdiorma = SuStdiorma + X
      SuStdiorni = SuStdiorni + Y
      If(Ipo.Eq.1) SuStdiorpo = SuStdiorpo + Z
      End If
"""
        result = mod.analyze_text(src)
        self.assertNotEqual(result["overall_classification"], "CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION")
        for target in mod.TARGETS:
            self.assertFalse(result["targets"][target]["source_level_use_before_definition_confirmed"])

    def test_nonzero_prior_definition_prevents_confirmation(self):
        src = """
      SuStdiorma = SeedA
      SuStdiorni = SeedN
      SuStdiorpo = SeedP
      SuStdiorma = SuStdiorma + X
      SuStdiorni = SuStdiorni + Y
      SuStdiorpo = SuStdiorpo + Z
"""
        result = mod.analyze_text(src)
        for target in mod.TARGETS:
            self.assertFalse(result["targets"][target]["source_level_use_before_definition_confirmed"])

    def test_fixed_form_comment_does_not_count_as_definition(self):
        src = """
C     SuStdiorma = 0.0
c     SuStdiorni = 0.0
*     SuStdiorpo = 0.0
      SuStdiorma = SuStdiorma + X
      SuStdiorni = SuStdiorni + Y
      SuStdiorpo = SuStdiorpo + Z
"""
        result = mod.analyze_text(src)
        self.assertEqual(result["overall_classification"], "CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION")


if __name__ == "__main__":
    unittest.main()
