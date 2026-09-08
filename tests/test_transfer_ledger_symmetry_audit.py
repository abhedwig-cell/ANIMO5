import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_transfer_ledger_symmetry.py"
spec = importlib.util.spec_from_file_location("audit_transfer_ledger_symmetry", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestTransferLedgerSymmetryAudit(unittest.TestCase):
    def test_continuation_is_joined(self):
        text = """      Bafop(24,Ly) = Bafop(24,Ly) + &
     &                 Dum
"""
        self.assertEqual(
            mod.uncommented_fortran_statements(text),
            [(1, "Bafop(24,Ly) = Bafop(24,Ly) + Dum")],
        )

    def test_cross_slot_self_accumulator_is_detected(self):
        text = """
      Bafom(24,Ly)=Bafom(24,Ly)+A
      Bafon(24,Ly)=Bafon(24,Ly)+B
      Bafop(24,Ly)=Bafop(25,Ly)+C
"""
        result = mod.detailed_accumulator_audit(text)
        self.assertEqual(result["cross_slot_self_reference_count"], 1)
        finding = result["cross_slot_self_references"][0]
        self.assertEqual(finding["family"], "bafop")
        self.assertEqual(finding["lhs_slot"], 24)
        self.assertEqual(finding["cross_slot_rhs_slots"], [25])

    def test_matching_accumulators_are_not_flagged(self):
        text = """
      Bafom(18,Ly)=Bafom(18,Ly)+A
      Bafon(18,Ly)=Bafon(18,Ly)+B
      Bafop(18,Ly)=Bafop(18,Ly)+C
"""
        result = mod.detailed_accumulator_audit(text)
        self.assertEqual(result["cross_slot_self_reference_count"], 0)

    def test_initial_exudate_asymmetry_is_statement_local_and_space_insensitive(self):
        initial = """
      Bfom(Inip_x,Ly)=Bfom(Inip_x,Ly)+Os(Ln,Fn)*P
      Bano(Inip_x,Ly)=Bano(Inip_x,Ly)+Ex(Ln)  *Nifrex *P
      Bapo(Inip_x,Ly)=Bapo(Inip_x,Ly)+Ex(Ln) * Pofrex * P
      Other = Ex(Ln)
"""
        final = """
      Bfom(Finp_x,Ly)=Bfom(Finp_x,Ly)+Rsex(Ln)*Z
"""
        result = mod.initial_final_state_audit(initial, final)
        self.assertFalse(result["fresh_om_initial_exudate"]["initial_has_ex"])
        self.assertTrue(result["fresh_om_initial_exudate"]["final_has_rsex"])
        self.assertTrue(result["fresh_om_initial_exudate"]["asymmetric"])
        self.assertTrue(result["organic_n_initial_exudate"]["initial_has_ex_n"])
        self.assertTrue(result["organic_p_initial_exudate"]["initial_has_ex_p"])


if __name__ == "__main__":
    unittest.main()
