import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "prepare_gnu_case.py"
SPEC = importlib.util.spec_from_file_location("prepare_gnu_case", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestPrepareGnuCase(unittest.TestCase):
    def test_printbal_unquotes_payload_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "GENERAL.INP"
            path.write_bytes(
                b"PrintBalLabel=      'RP'! 2-character identifier\r\n"
                b"PrintBalWater=1!x\r\n"
            )
            count, before_hash, after_hash = MODULE.adapt_print_bal_labels(path)
            self.assertEqual(count, 1)
            self.assertEqual(
                path.read_bytes(),
                b"PrintBalLabel=      RP! 2-character identifier\r\n"
                b"PrintBalWater=1!x\r\n",
            )
            self.assertNotEqual(before_hash, after_hash)

    def test_case_insensitive_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Input").mkdir()
            (root / "Input" / "GENERAL.INP").write_text("x", encoding="utf-8")
            result = MODULE.find_case_insensitive(root, Path("input/general.inp"))
            self.assertEqual(result, root / "Input" / "GENERAL.INP")

    def test_multiblock_payload_preserved(self):
        records = [b"a" * 130, b"xyz"]
        raw = bytearray([MODULE.HEADER])
        for payload in records:
            position = 0
            while len(payload) - position > 128:
                raw.append(MODULE.CONTINUATION)
                raw.extend(payload[position:position + 128])
                raw.append(MODULE.CONTINUATION)
                position += 128
            tail = payload[position:]
            raw.append(len(tail))
            raw.extend(tail)
            raw.append(len(tail))
        raw.append(MODULE.TRAILER)

        parsed, blocks = MODULE.parse_powerstation_records(bytes(raw))
        self.assertEqual(parsed, records)
        self.assertEqual(blocks, 3)
        encoded = MODULE.encode_gfortran_records(parsed)
        self.assertIn(b"a" * 130, encoded)


if __name__ == "__main__":
    unittest.main()
