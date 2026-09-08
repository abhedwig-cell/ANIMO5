#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZIP = ROOT / "reference" / "testcases" / "ANIMO_testbank.zip"
ZIP = Path(os.environ.get("ANIMO_TESTBANK_ZIP", DEFAULT_ZIP))
EXPECTED_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"

class Prep01InventoryTests(unittest.TestCase):
    def test_persisted_archive_identity(self):
        sha_record=(ROOT / "reference" / "testcases" / "ANIMO_testbank.zip.sha256").read_text().split()[0]
        self.assertEqual(sha_record, EXPECTED_SHA256)

    def test_persisted_inventory_basics(self):
        data=json.loads((ROOT / "reference" / "testcases" / "testbank_inventory.json").read_text())
        self.assertEqual(data["archive"]["sha256"], EXPECTED_SHA256)
        self.assertEqual(data["archive"]["case_count"], 9)
        self.assertEqual(data["archive"]["file_count"], 119)
        self.assertEqual(data["summary"]["cases_with_no_output_directory_files"], 9)
        self.assertTrue(data["summary"]["all_cases_blocked_without_animo_executable"])

    def test_external_archive_sha256_when_available(self):
        if not ZIP.is_file():
            self.skipTest("binary testcase archive is external to the GitHub bootstrap")
        self.assertEqual(hashlib.sha256(ZIP.read_bytes()).hexdigest(), EXPECTED_SHA256)

    def test_inventory_reproduces_when_archive_available(self):
        if not ZIP.is_file():
            self.skipTest("binary testcase archive is external to the GitHub bootstrap")
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            subprocess.run([
                sys.executable, str(ROOT / "tools" / "audit_testbank.py"), str(ZIP),
                "--json", str(td / "inventory.json"),
                "--manifest-csv", str(td / "manifest.csv"),
                "--cases-csv", str(td / "cases.csv"),
            ], check=True, stdout=subprocess.DEVNULL)
            data=json.loads((td / "inventory.json").read_text())
            self.assertEqual(data["archive"]["sha256"], EXPECTED_SHA256)
            self.assertEqual(data["archive"]["case_count"], 9)
            self.assertEqual(data["archive"]["file_count"], 119)

if __name__ == "__main__":
    unittest.main()
