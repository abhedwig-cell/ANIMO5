import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools/stateq07/tcd036_ponding_layer0_oracle.py"
spec = importlib.util.spec_from_file_location("tcd036_oracle", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TCD036PondingLayer0Tests(unittest.TestCase):
    def test_full_oracle_bank(self):
        r = mod.validate_cases()
        self.assertEqual(r["cases"], 34)
        self.assertGreater(r["pre_existing_nonzero_divergence_cases"], 0)
        self.assertGreater(r["new_event_controls"], 0)
        self.assertGreater(r["absent_ponding_controls"], 0)
        self.assertGreater(r["zero_gas_controls"], 0)

    def test_pre_existing_ponding_identity(self):
        r = mod.restart_layer0(0.125, True, 1.0e-3)
        self.assertEqual(r["mode"], "PRE_EXISTING_PONDING_RESTART_IDENTITY")
        self.assertEqual(r["co0"], 0.125)

    def test_zero_reset_is_wrong_for_nonzero_pre_existing_ponding(self):
        q = mod.restart_layer0(0.125, True, 1.0e-3)["co0"]
        z = mod.zero_reset_legacy_view(0.125, True, 1.0e-3)
        self.assertNotEqual(q, z)

    def test_new_ponding_keeps_source_initialization(self):
        r = mod.restart_layer0(0.125, True, 5.0e-5, new_event_value=0.01)
        self.assertEqual(r["mode"], "NEW_PONDING_SOURCE_INITIALIZATION")
        self.assertEqual(r["co0"], 0.01)

    def test_no_ponding_does_not_create_dormant_state(self):
        r = mod.restart_layer0(0.125, False, 0.0)
        self.assertEqual(r["owner"], 0.0)
        self.assertEqual(r["co0"], 0.0)


if __name__ == "__main__":
    unittest.main()
