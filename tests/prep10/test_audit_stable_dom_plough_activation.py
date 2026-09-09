import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "audit_stable_dom_plough_activation.py"
spec = importlib.util.spec_from_file_location("audit_stable_dom_activation", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class StableDomPloughActivationTests(unittest.TestCase):
    def test_counts_repeated_cranmais_plough_signature(self):
        text = """
>add001:
  1      0.00   0   2 0.00
>add002:
  1      0.00   0   2 0.00
"""
        result = mod.analyze_management(text)
        self.assertEqual(result["plough_request_count"], 2)
        self.assertTrue(result["repeated_plough_requests_present"])

    def test_initial_sdomin_zero_block(self):
        text = """
>sdomin:
 0.0 0.0
 0.000E+00 0.0
 0.0 0.0
"""
        result = mod.analyze_initial(text)
        self.assertEqual(result["value_count"], 6)
        self.assertTrue(result["all_values_zero"])

    def test_nonzero_sdomin_is_detected(self):
        text = """
>sdomin:
 0.0 1.0E-4
 0.0 0.0
 0.0 0.0
"""
        result = mod.analyze_initial(text)
        self.assertFalse(result["all_values_zero"])


if __name__ == "__main__":
    unittest.main()
