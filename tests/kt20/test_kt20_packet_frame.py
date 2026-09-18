from __future__ import annotations

import base64
from pathlib import Path
import tempfile
import unittest

from prototype.kt03.hydrology_step import typed_step_digest
from prototype.kt19.pinned_lwkm_file_provider import (
    decode_unpinned_powerstation_hydrology,
)
from prototype.kt20.hydrology_packet_frame import (
    FRAME_ROLE,
    PacketFrameError,
    export_hydrology_packet_frame,
    parse_hydrology_packet_frame,
    synthetic_commit_control_packet,
)

ROOT = Path(__file__).resolve().parents[2]
REAL_B64 = ROOT / "reference" / "kt19" / "LWKM_FIRST_PACKET_POWERSTATION_B1.b64"
FIRST_TYPED = "eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c"


class TestKT20PacketFrame(unittest.TestCase):
    def real_packet(self):
        raw = base64.b64decode(REAL_B64.read_text().strip())
        _, packets, _ = decode_unpinned_powerstation_hydrology(raw)
        self.assertEqual(len(packets), 1)
        return packets[0]

    def test_real_packet_exact_roundtrip(self):
        packet = self.real_packet()
        self.assertEqual(typed_step_digest(packet), FIRST_TYPED)
        frame = export_hydrology_packet_frame(packet)
        restored = parse_hydrology_packet_frame(frame)
        self.assertEqual(restored, packet)
        self.assertEqual(typed_step_digest(restored), FIRST_TYPED)
        self.assertIn(FRAME_ROLE, frame)

    def test_synthetic_control_exact_roundtrip(self):
        packet = synthetic_commit_control_packet()
        frame = export_hydrology_packet_frame(packet)
        restored = parse_hydrology_packet_frame(frame)
        self.assertEqual(restored, packet)
        self.assertEqual(typed_step_digest(restored), typed_step_digest(packet))

    def test_payload_bit_mutation_is_detected_by_declared_digest(self):
        packet = self.real_packet()
        frame = export_hydrology_packet_frame(packet)
        lines = frame.splitlines()
        # First scalar after seven header/dimension lines is endpoint-day bits.
        self.assertEqual(len(lines[7]), 16)
        lines[7] = ("0" if lines[7][0] != "0" else "1") + lines[7][1:]
        with self.assertRaises(PacketFrameError):
            parse_hydrology_packet_frame("\n".join(lines) + "\n")

    def test_noncanonical_role_rejected(self):
        frame = export_hydrology_packet_frame(synthetic_commit_control_packet())
        with self.assertRaises(PacketFrameError):
            parse_hydrology_packet_frame(
                frame.replace(FRAME_ROLE, "CANONICAL_PRODUCTION_ABI", 1)
            )


if __name__ == "__main__":
    unittest.main()
