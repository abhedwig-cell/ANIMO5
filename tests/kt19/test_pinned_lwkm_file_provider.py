from __future__ import annotations

import base64
from dataclasses import FrozenInstanceError
import hashlib
import json
from pathlib import Path
import unittest

from prototype.kt03.hydrology_step import typed_step_digest
from prototype.kt19.pinned_lwkm_file_provider import (
    EXPECTED_GROUP_SEQUENCE_SHA256,
    EXPECTED_PACKET_COUNT,
    EXPECTED_RECORD_SEQUENCE_SHA256,
    EXPECTED_SOURCE_SHA256,
    EXPECTED_TYPED_SEQUENCE_SHA256,
    ImmutableHydrologyPacketProvider,
    PinnedLWKMFileHydrologyProvider,
    PinnedProviderError,
    decode_unpinned_powerstation_hydrology,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_B64 = ROOT / "reference" / "kt19" / "LWKM_FIRST_PACKET_POWERSTATION_B1.b64"
FIXTURE_META = ROOT / "reference" / "kt19" / "LWKM_FIRST_PACKET_POWERSTATION_B1.json"
KT08_SUMMARY = ROOT / "reference" / "kt11" / "LWKM_SEQUENCE_SUMMARY_KT08.json"


class TestKT19PinnedLWKMFileProvider(unittest.TestCase):
    def _fixture(self) -> bytes:
        return base64.b64decode(FIXTURE_B64.read_text().strip())

    def test_real_source_derived_first_packet_fixture(self):
        raw = self._fixture()
        meta = json.loads(FIXTURE_META.read_text())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), meta["fixture_sha256"])
        self.assertEqual(len(raw), meta["fixture_size_bytes"])

        static, packets, blocks = decode_unpinned_powerstation_hydrology(raw)
        self.assertEqual(static["hlpimp"], 11)
        self.assertEqual(static["nl"], 30)
        self.assertEqual(static["nh"], 30)
        self.assertEqual(static["nudr"], 5)
        self.assertTrue(static["ioptte"])
        self.assertEqual(len(packets), 1)
        self.assertEqual(blocks, 30)

        step = packets[0]
        self.assertEqual(
            typed_step_digest(step),
            "eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c",
        )
        self.assertEqual(step.producer_endpoint_day, 10.0)
        self.assertEqual(step.producer_step_days, 10.0)
        self.assertTrue(step.has_interception_storage_end)
        self.assertTrue(step.has_soil_temperature)

    def test_read_only_selection_semantics_on_real_source_fixture(self):
        _, packets, _ = decode_unpinned_powerstation_hydrology(self._fixture())
        provider = ImmutableHydrologyPacketProvider(
            packets, "ANIMO_TEST_CALENDAR", producer_day_offset=0
        )
        selected = provider.select(0, 10, "ANIMO_TEST_CALENDAR")
        self.assertEqual(
            typed_step_digest(selected),
            "eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c",
        )
        with self.assertRaises(FrozenInstanceError):
            selected.prr = 1.0
        with self.assertRaises(PinnedProviderError):
            provider.select(0, 10, "OTHER_CALENDAR")
        with self.assertRaises(PinnedProviderError):
            provider.select(0, 11, "ANIMO_TEST_CALENDAR")
        with self.assertRaises(PinnedProviderError):
            provider.select(0.0, 10, "ANIMO_TEST_CALENDAR")
        with self.assertRaises(PinnedProviderError):
            provider.select(True, 10, "ANIMO_TEST_CALENDAR")

    def test_provider_rejects_discontinuous_sequence(self):
        _, packets, _ = decode_unpinned_powerstation_hydrology(self._fixture())
        with self.assertRaises(PinnedProviderError):
            ImmutableHydrologyPacketProvider(
                [packets[0], packets[0]], "ANIMO_TEST_CALENDAR"
            )

    def test_pinned_provider_rejects_derived_fixture_as_full_source(self):
        with self.assertRaises(PinnedProviderError) as ctx:
            PinnedLWKMFileHydrologyProvider.from_bytes(
                self._fixture(), "ANIMO_TEST_CALENDAR"
            )
        self.assertIn("unexpected LWKM source SHA-256", str(ctx.exception))

    def test_constants_match_frozen_kt08_sequence_authority(self):
        summary = json.loads(KT08_SUMMARY.read_text())
        self.assertEqual(summary["source_sha256"], EXPECTED_SOURCE_SHA256)
        self.assertEqual(summary["sequence"]["packet_count"], EXPECTED_PACKET_COUNT)
        agg = summary["aggregate_identity"]
        self.assertEqual(
            agg["typed_step_digest_sequence_sha256"],
            EXPECTED_TYPED_SEQUENCE_SHA256,
        )
        self.assertEqual(
            agg["dynamic_group_digest_sequence_sha256"],
            EXPECTED_GROUP_SEQUENCE_SHA256,
        )
        self.assertEqual(
            agg["temporal_and_digest_record_sequence_sha256"],
            EXPECTED_RECORD_SEQUENCE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
