import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_balance_indices.py"
spec = importlib.util.spec_from_file_location("audit_balance_indices", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestBalanceIndexAudit(unittest.TestCase):
    def test_outbal1_storage_slots(self):
        text = """      Data Stsn_b,Stpn_b,Stsm_b,Inip_x,Inip_l,Inip_p &
     &    / 36,38,40,45,46,48 /
"""
        self.assertEqual(
            mod.parse_outbal1(text),
            {
                "Stsn_b": 36,
                "Stpn_b": 38,
                "Stsm_b": 40,
                "Inip_x": 45,
                "Inip_l": 46,
                "Inip_p": 48,
            },
        )

    def test_outbal2_array_members(self):
        text = """      Data Topd, Inf(1), Inf(2), Dra4 &
     &     / 1,18,19,74 /
"""
        self.assertEqual(
            mod.parse_outbal2(text),
            {"Topd": 1, "Inf(1)": 18, "Inf(2)": 19, "Dra4": 74},
        )


if __name__ == "__main__":
    unittest.main()
