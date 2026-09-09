from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "make_prep10c_corrected_addit.py"
spec = importlib.util.spec_from_file_location("make_prep10c_corrected_addit", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Prep10CCorrectedAdditTests(unittest.TestCase):
    def test_wrong_parent_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            mod.transform(b"not revision 53 Addit.for")

    def test_synthetic_exactly_one_branch_gets_three_resets(self):
        source = b"header\r\n" + mod.BRANCH + b"tail\r\n"
        expected = b"header\r\n" + mod.RESET_BRANCH + b"tail\r\n"
        with patch.object(mod, "EXPECTED_PARENT_SHA256", sha(source)), patch.object(
            mod, "EXPECTED_CANDIDATE_SHA256", sha(expected)
        ):
            candidate = mod.transform(source)
        self.assertEqual(candidate, expected)
        self.assertEqual(candidate.count(b"SuStdiorma = 0.0"), 1)
        self.assertEqual(candidate.count(b"SuStdiorni = 0.0"), 1)
        self.assertEqual(candidate.count(b"If (Ipo.Eq.1) SuStdiorpo = 0.0"), 1)

    def test_ambiguous_insertion_point_fails_closed(self):
        source = mod.BRANCH + mod.BRANCH
        with patch.object(mod, "EXPECTED_PARENT_SHA256", sha(source)):
            with self.assertRaisesRegex(ValueError, "exactly one"):
                mod.transform(source)

    def test_candidate_identity_matches_qualified_prep10_counterfactual(self):
        self.assertEqual(
            mod.EXPECTED_CANDIDATE_SHA256,
            "a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae",
        )


if __name__ == "__main__":
    unittest.main()
