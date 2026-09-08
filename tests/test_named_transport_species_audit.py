import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_named_transport_species.py"
spec = importlib.util.spec_from_file_location("audit_named_transport_species", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestNamedTransportSpeciesAudit(unittest.TestCase):
    def test_matching_phosphorus_call_is_clean(self):
        source = {
            "x.for": "      Call Transport('PHOSPHORUS',Dummy,Transfop(1))\n"
        }
        result = mod.audit_source(source)
        self.assertEqual(result["named_transport_calls_audited"], 1)
        self.assertEqual(result["species_mismatch_count"], 0)

    def test_wrong_species_in_phosphorus_call_fails_closed(self):
        source = {
            "x.for": "      Call Transport('PHOSPHORUS',Dummy,Transfon(1))\n"
        }
        result = mod.audit_source(source)
        self.assertEqual(result["named_transport_calls_audited"], 1)
        self.assertEqual(result["species_mismatch_count"], 1)

    def test_runtime_substance_label_is_not_guessed(self):
        source = {
            "x.for": "      Call Transport(Substname,Dummy,Transfon(1))\n"
        }
        result = mod.audit_source(source)
        self.assertEqual(result["named_transport_calls_audited"], 0)
        self.assertEqual(result["species_mismatch_count"], 0)


if __name__ == "__main__":
    unittest.main()
