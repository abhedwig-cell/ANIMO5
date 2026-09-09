import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "make_prep10_addit_variants.py"
spec = importlib.util.spec_from_file_location("make_prep10_addit_variants", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class AdditVariantTests(unittest.TestCase):
    def _source(self) -> bytes:
        return (
            b"      Subroutine Addit\r\n"
            + mod.BRANCH
            + b"            SuStdiorma = SuStdiorma + X\r\n"
            + b"            SuStdiorni = SuStdiorni + Y\r\n"
            + b"            If (Ipo.Eq.1) SuStdiorpo = SuStdiorpo + Z\r\n"
            + mod.END_LOOP
            + b"          End If\r\n"
            + b"      End\r\n"
        )

    def test_observer_only_adds_before_and_after_writes(self):
        source = self._source()
        observer, reset = mod.make_variants(source)
        self.assertIn(b"PREP10_BEFORE", observer)
        self.assertIn(b"PREP10_AFTER", observer)
        self.assertNotIn(b"SuStdiorma = 0.0", observer)
        self.assertEqual(observer.count(b"\r\n"), source.count(b"\r\n") + 2)
        self.assertNotEqual(observer, reset)

    def test_reset_counterfactual_adds_three_event_resets(self):
        source = self._source()
        _, reset = mod.make_variants(source)
        self.assertIn(b"SuStdiorma = 0.0", reset)
        self.assertIn(b"SuStdiorni = 0.0", reset)
        self.assertIn(b"If (Ipo.Eq.1) SuStdiorpo = 0.0", reset)
        self.assertNotIn(b"PREP10_BEFORE", reset)
        self.assertEqual(reset.count(b"\r\n"), source.count(b"\r\n") + 3)

    def test_fails_closed_when_expected_insertion_point_changes(self):
        source = self._source().replace(mod.BRANCH, b"          If (Pl(I) .Gt. 0) Then\r\n")
        with self.assertRaises(ValueError):
            mod.make_variants(source)


if __name__ == "__main__":
    unittest.main()
