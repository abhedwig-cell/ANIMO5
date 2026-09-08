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

        parsed, blocks = conv.parse_powerstation_records(bytes(legacy))
        self.assertEqual(parsed, records)
        self.assertEqual(blocks, 3)

        encoded = conv.encode_gfortran_records(parsed)
        pos = 0
        recovered = []
        for expected in records:
            n = struct.unpack("<i", encoded[pos:pos + 4])[0]
            pos += 4
            recovered.append(encoded[pos:pos + n])
            pos += n
            self.assertEqual(struct.unpack("<i", encoded[pos:pos + 4])[0], n)
            pos += 4
        self.assertEqual(recovered, records)

    def test_powerstation_continuation_and_128_byte_terminal_block(self):
        first = bytes(range(128)) + bytes(range(12))
        second = bytes(range(128))
        legacy = bytearray([0x4B])
        legacy += bytes([0x81]) + first[:128] + bytes([0x81])
        legacy += bytes([12]) + first[128:] + bytes([12])
        legacy += bytes([0x80]) + second + bytes([0x80])
        legacy += bytes([0x82])

        parsed, blocks = conv.parse_powerstation_records(bytes(legacy))
        self.assertEqual(parsed, [first, second])
        self.assertEqual(blocks, 3)

    def test_ruurlo_record_identity_when_local_testbank_is_mounted(self):
        candidates = [
            Path("/mnt/data/animo_testbank/ANIMO_testbank/RuurloGrass/Input/SWATRE.UNF"),
            Path("/mnt/data/ANIMO_testbank/RuurloGrass/Input/SWATRE.UNF"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            self.skipTest("local ANIMO testbank not mounted")

        records, blocks = conv.parse_powerstation_records(path.read_bytes())
        self.assertEqual(len(records), 11691)
        self.assertEqual(blocks, 11691)
        self.assertEqual(records[0], struct.pack("<iifff", 1980, 1985, 1.0, 120.0, 1.0))
        self.assertEqual(sorted(set(map(len, records))), [8, 12, 20, 24, 40, 80, 84])

    def test_ghg_multiblock_record_identity_when_local_testbank_is_mounted(self):
        candidates = [
            Path("/mnt/data/animo_testbank/ANIMO_testbank/GHGMais/Input/result.bun"),
            Path("/mnt/data/ANIMO_testbank/GHGMais/Input/result.bun"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            self.skipTest("local ANIMO testbank not mounted")

        records, blocks = conv.parse_powerstation_records(path.read_bytes())
        self.assertEqual(len(records), 40189)
        self.assertEqual(blocks, 43841)
        self.assertEqual(
            sorted(set(map(len, records))),
            [4, 8, 12, 16, 20, 72, 80, 128, 132],
        )


if __name__ == "__main__":
    unittest.main()
