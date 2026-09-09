import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_option_dispatch_contracts.py"
SPEC = importlib.util.spec_from_file_location("audit_option_dispatch_contracts", TOOL)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class TestOptionDispatchContracts(unittest.TestCase):
    def test_checkint(self):
        text = "Call Checkint(Uoer,Error,Label,'Foo',Foo,1,3)"
        self.assertTrue(mod.has_checkint(text, "Foo", 1, 3))
        self.assertFalse(mod.has_checkint(text, "Foo", 0, 3))

    def test_eq_values(self):
        text = "If(X.Eq.1)Then\nElse If (X == 3) Then\nEnd If"
        self.assertEqual(mod.eq_values(text, "X"), {1, 3})

    def test_rel(self):
        self.assertTrue(mod.has_rel("If (X.Ne.1) Then", "X", "ne", 1))

    def test_full_frozen_audit_when_archives_are_available(self):
        source = Path("/mnt/data/ANIMO_4.1.5.53(3).zip")
        testbank = Path("/mnt/data/ANIMO_testbank.zip")
        if not source.exists() or not testbank.exists():
            self.skipTest("frozen session archives not mounted")
        evidence = mod.audit(source, testbank)
        self.assertTrue(evidence["all_checks_pass"], evidence)
        self.assertEqual(evidence["checks_total"], 20)
        self.assertEqual(evidence["checks_passed"], 20)
        self.assertEqual(evidence["interpretation"]["new_alias_defects_found"], 0)


if __name__ == "__main__":
    unittest.main()
