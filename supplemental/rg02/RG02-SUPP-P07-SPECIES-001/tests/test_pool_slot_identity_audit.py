import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_pool_slot_identity.py"
spec = importlib.util.spec_from_file_location("audit_pool_slot_identity", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestPoolSlotIdentityAudit(unittest.TestCase):
    def test_tcd027_is_recognized(self):
        classification, discrepancy = mod.classify(
            "Outbal_calc.for",
            "Bafop",
            24,
            25,
            "Bafop(24,Ly)=Bafop(25,Ly)+Dum",
        )
        self.assertEqual(classification, "CONFIRMED_EXISTING_DISCREPANCY")
        self.assertEqual(discrepancy, "TCD-027")

    def test_transfer_partition_is_intentional(self):
        classification, discrepancy = mod.classify(
            "resp_miner.for",
            "Transfop",
            19,
            17,
            "Transfop(19,Ln)=x*Transfop(17,Ln)",
        )
        self.assertEqual(classification, "INTENTIONAL_TRANSFER_PARTITION")
        self.assertIsNone(discrepancy)

    def test_unknown_cross_slot_fails_closed(self):
        classification, _ = mod.classify(
            "x.for", "Bafop", 21, 22, "Bafop(21,Ly)=Bafop(22,Ly)+Dum"
        )
        self.assertEqual(classification, "UNRESOLVED_CROSS_SLOT_CANDIDATE")

    def test_synthetic_source_reports_unresolved(self):
        report = mod.audit_source({
            "x.for": "Bafop(21,Ly)=Bafop(22,Ly)+Dum\n"
        })
        self.assertEqual(len(report["unresolved_cross_slot_candidates"]), 1)


if __name__ == "__main__":
    unittest.main()
