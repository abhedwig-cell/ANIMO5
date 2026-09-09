from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "audit_prep10c_plough_conservation.py"
spec = importlib.util.spec_from_file_location("audit_prep10c_plough_conservation", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class Prep10CConservationAuditTests(unittest.TestCase):
    def test_matching_lines_normalizes_whitespace_and_case(self):
        lines = mod.normalized_lines(b"  Bo(0)   =  0.0\r\nBO(0)=1.0\r\n")
        self.assertEqual(mod.matching_lines(lines, "bo(0) = 0.0"), [1])

    def test_require_hit_rejects_wrong_count(self):
        lines = ["do ln = 1,pl(i)", "do ln = 1,pl(i)"]
        with self.assertRaisesRegex(ValueError, "expected 1"):
            mod.require_hit(lines, "Do Ln = 1,Pl(I)")

    def test_require_hit_can_select_second_expected_occurrence(self):
        lines = ["do ln = 1,pl(i)", "x", "do ln = 1,pl(i)"]
        self.assertEqual(
            mod.require_hit(lines, "Do Ln = 1,Pl(I)", expected_count=2, select=1),
            3,
        )

    def test_wrong_archive_hash_fails_before_zip_read(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "not-source.zip"
            path.write_bytes(b"not the frozen source")
            with self.assertRaisesRegex(ValueError, "source archive SHA-256 mismatch"):
                mod.audit(path)


if __name__ == "__main__":
    unittest.main()
