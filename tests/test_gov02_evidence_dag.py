import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "gov02_validator", ROOT / "tools/validate_gov02_evidence_dag.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class Gov02EvidenceDagTests(unittest.TestCase):
    def test_policy_is_fail_closed(self):
        self.assertEqual(mod.validate_policy(ROOT), [])

    def test_required_validation_cases(self):
        data = json.loads((ROOT / "integration/animo-governance/GOV02_VALIDATION_CASES.json").read_text())
        observed = {}
        for case in data["cases"]:
            allowed, reasons = mod.evaluate(case)
            observed[case["id"]] = ("ALLOW" if allowed else "REJECT", reasons)

        self.assertEqual(observed["VALID_CLASS_A_HISTORICAL_UNCERTAINTY"][0], "ALLOW")
        self.assertEqual(observed["INVALID_SYNTHETIC_AS_B2"][0], "REJECT")
        self.assertEqual(observed["INVALID_B1_GNU_AS_HISTORICAL_ORACLE"][0], "REJECT")
        self.assertEqual(observed["INVALID_ACQUISITION_NOT_ACTUALLY_ATTEMPTED"][0], "REJECT")
        self.assertEqual(observed["INVALID_CLASS_C_MASS_CLOSURE_ONLY"][0], "REJECT")
        self.assertEqual(observed["INVALID_CLASS_E_SMALLER_RESIDUAL_ONLY"][0], "REJECT")
        self.assertEqual(observed["INVALID_HISTORICAL_EQUIVALENCE_WITHOUT_B2"][0], "REJECT")

    def test_historical_claim_rejects_scientific_oracle_without_b2(self):
        case = {
            "b3_class": "B",
            "claim_type": "HISTORICAL_FIDELITY_CLAIM",
            "route": "B2_BACKED_RECONCILIATION",
            "evidence": [{"class": "ANALYTICAL_ORACLE", "source_kind": "INDEPENDENT_SCIENTIFIC_ORACLE"}],
        }
        allowed, reasons = mod.evaluate(case)
        self.assertFalse(allowed)
        self.assertTrue(any("requires qualified B2" in x for x in reasons))

    def test_valid_independent_historical_reference_can_satisfy_historical_claim(self):
        case = {
            "b3_class": "B",
            "claim_type": "HISTORICAL_FIDELITY_CLAIM",
            "route": "B2_BACKED_RECONCILIATION",
            "evidence": [{"class": "B2", "source_kind": "INDEPENDENT_HISTORICAL_REFERENCE", "qualified": True}],
        }
        allowed, reasons = mod.evaluate(case)
        self.assertTrue(allowed, reasons)


if __name__ == "__main__":
    unittest.main()
