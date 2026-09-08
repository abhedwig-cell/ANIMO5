import importlib.util
import struct
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "convert_legacy_unformatted.py"
spec = importlib.util.spec_from_file_location("conv", TOOL)
conv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conv)


class TestLegacyUnformatted(unittest.TestCase):
    def test_synthetic_payload_preservation(self):
        records = [b"abc", bytes(range(20)), b""]
        legacy = bytearray([0x4B])
        for record in records:
            legacy += bytes([len(record)]) + record + bytes([len(record)])
        legacy += bytes([0x82])

        parsed = conv.parse_simple_legacy_records(bytes(legacy))
        self.assertEqual(parsed, records)

        encoded = conv.encode_gfortran_records(parsed)
        pos = 0
        recovered = []
        for expected in records:
            n = struct.unpack("<i", encoded[pos:pos+4])[0]
            pos += 4
            recovered.append(encoded[pos:pos+n])
            pos += n
            self.assertEqual(struct.unpack("<i", encoded[pos:pos+4])[0], n)
            pos += 4
        self.assertEqual(recovered, records)

    def test_ruurlo_record_identity_when_local_testbank_is_mounted(self):
        candidates = [
            Path("/mnt/data/animo_testbank/ANIMO_testbank/RuurloGrass/Input/SWATRE.UNF"),
            Path("/mnt/data/ANIMO_testbank/RuurloGrass/Input/SWATRE.UNF"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            self.skipTest("local ANIMO testbank not mounted")

        records = conv.parse_simple_legacy_records(path.read_bytes())
        self.assertEqual(len(records), 11691)
        self.assertEqual(records[0], struct.pack("<iifff", 1980, 1985, 1.0, 120.0, 1.0))
        self.assertEqual(sorted(set(map(len, records))), [8, 12, 20, 24, 40, 80, 84])

    def test_extended_marker_fails_closed_when_ghg_case_is_mounted(self):
        candidates = [
            Path("/mnt/data/animo_testbank/ANIMO_testbank/GHGMais/Input/result.bun"),
            Path("/mnt/data/ANIMO_testbank/GHGMais/Input/result.bun"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            self.skipTest("local ANIMO testbank not mounted")

        with self.assertRaises(conv.LegacyRecordError):
            conv.parse_simple_legacy_records(path.read_bytes())


if __name__ == "__main__":
    unittest.main()
