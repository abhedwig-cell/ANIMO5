import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "audit_fortran_function_interfaces.py"
spec = importlib.util.spec_from_file_location("audit_fortran_function_interfaces", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TestFunctionInterfaceAudit(unittest.TestCase):
    def test_split_decl_names_preserves_names_ignores_shapes(self):
        self.assertEqual(
            mod.split_decl_names("A(10), Dble_trunc, B(0:20), C ! comment"),
            ["a", "dble_trunc", "b", "c"],
        )

    def test_synthetic_mixed_result_declaration(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "f.for").write_text(
                "      Function Foo(X)\n"
                "      Implicit None\n"
                "      Real(8) :: Foo, X\n"
                "      Foo = X\n"
                "      End\n",
                encoding="ascii",
            )
            (root / "caller.for").write_text(
                "      Subroutine Caller(X,Y)\n"
                "      Implicit None\n"
                "      Real :: X,Y,Foo\n"
                "      Y = Foo(X)\n"
                "      End\n",
                encoding="ascii",
            )
            result = mod.analyze(root)
            self.assertEqual(result["function_definition_count"], 1)
            row = result["functions"][0]
            self.assertEqual(row["function"], "foo")
            self.assertEqual(row["definition_result_type"], "real(8)")
            self.assertEqual(row["observed_declaration_types"], ["real", "real(8)"])
            self.assertEqual(row["possible_call_count"], 1)
            self.assertEqual(row["classification"], "MIXED_EXPLICIT_RESULT_DECLARATION")

    def test_synthetic_consistent_integer_function(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "f.f90").write_text(
                "function idx(x)\n"
                "implicit none\n"
                "integer :: idx, x\n"
                "idx = x\n"
                "end\n",
                encoding="ascii",
            )
            result = mod.analyze(root)
            row = result["functions"][0]
            self.assertEqual(row["definition_result_type"], "integer")
            self.assertEqual(
                row["classification"],
                "EXPLICIT_DECLARATIONS_CONSISTENT_WITH_DEFINITION",
            )


if __name__ == "__main__":
    unittest.main()
