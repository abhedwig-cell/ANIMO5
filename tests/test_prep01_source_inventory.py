import hashlib
import importlib.util
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'audit_source_archive.py'
spec = importlib.util.spec_from_file_location('audit_source_archive', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

EXPECTED_HASH = '183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566'
EXPECTED_MANIFEST = ROOT / 'reference' / 'source' / 'source_manifest.csv'
ARCHIVE = Path(os.environ.get('ANIMO_LEGACY_SOURCE_ZIP', '/mnt/data/ANIMO_4.1.5.53(3).zip'))


@unittest.skipUnless(ARCHIVE.exists(), 'legacy source archive not mounted')
class TestSourceInventory(unittest.TestCase):
    def test_archive_hash(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), EXPECTED_HASH)

    def test_manifest_exact(self):
        generated = mod.build_manifest(ARCHIVE)
        self.assertEqual(generated, EXPECTED_MANIFEST.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
