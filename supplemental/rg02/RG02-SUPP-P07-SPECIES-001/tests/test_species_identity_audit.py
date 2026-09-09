import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_species_identity.py"
spec = importlib.util.spec_from_file_location("audit_species_identity", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestSpeciesIdentityAudit(unittest.TestCase):
    def test_known_tcd023_is_confirmed(self):
        item = mod.classify_cross_assignment(
            "resp_miner.for",
            564,
            "Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)",
        )
        self.assertIsNotNone(item)
        self.assertEqual(item["classification"], "CONFIRMED_EXISTING_DISCREPANCY")
        self.assertEqual(item["existing_discrepancy"], "TCD-023")

    def test_intentional_stoichiometric_conversion_is_not_unresolved(self):
        item = mod.classify_cross_assignment(
            "Grassprd.for",
            300,
            "Pofrsh = (Pofrshma + Pofrshmi) / (Nifrshma + Nifrshmi) * Orgnsh",
        )
        self.assertIsNotNone(item)
        self.assertTrue(item["classification"].startswith("INTENTIONAL_"))

    def test_dormant_surface_binding_is_classified_latent(self):
        item = mod.classify_cross_assignment(
            "Outsel.for",
            1091,
            "Rudon = Rudon + Rurv*(Avcodiorni(0)+AvcoStdiorma(0))*1.d+4*St",
        )
        self.assertIsNotNone(item)
        self.assertEqual(
            item["classification"],
            "LATENT_DORMANT_STABLE_SURFACE_DON_BINDING",
        )

    def test_unknown_cross_species_expression_fails_closed(self):
        item = mod.classify_cross_assignment(
            "Some.for", 1, "Transfop(1,Ln) = Transfon(1,Ln)"
        )
        self.assertIsNotNone(item)
        self.assertEqual(
            item["classification"], "UNRESOLVED_CROSS_SPECIES_CANDIDATE"
        )

    def test_local_call_species_mismatch_is_detected(self):
        source = {
            "x.for": """
      Subroutine Foo(Transfon)
      Return
      End
      Subroutine Bar(Transfop)
      Call Foo(Transfop)
      Return
      End
"""
        }
        definitions = mod.parse_local_subroutines(source)
        result = mod.audit_calls(source, definitions)
        self.assertEqual(result["strong_species_mismatch_count"], 1)
        mismatch = result["strong_species_mismatches"][0]
        self.assertEqual(mismatch["formal_species"], "N")
        self.assertEqual(mismatch["actual_species"], "P")

    def test_matching_local_call_is_not_flagged(self):
        source = {
            "x.for": """
      Subroutine Foo(Transfon)
      Return
      End
      Subroutine Bar(Transfon)
      Call Foo(Transfon)
      Return
      End
"""
        }
        definitions = mod.parse_local_subroutines(source)
        result = mod.audit_calls(source, definitions)
        self.assertEqual(result["strong_species_mismatch_count"], 0)


if __name__ == "__main__":
    unittest.main()
