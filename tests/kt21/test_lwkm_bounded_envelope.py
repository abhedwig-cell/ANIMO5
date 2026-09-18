from __future__ import annotations

import base64
from dataclasses import replace
from pathlib import Path
import unittest

from prototype.kt19.pinned_lwkm_file_provider import (
    decode_unpinned_powerstation_hydrology,
)
from prototype.kt20.hydrology_packet_frame import synthetic_commit_control_packet
from prototype.kt21.lwkm_bounded_envelope import (
    CLASS_BLOCKED_RUNINU,
    CLASS_EXACT_ZERO,
    EnvelopeConfig,
    characterize_packets,
)

ROOT=Path(__file__).resolve().parents[2]
REAL_B64=ROOT/"reference"/"kt19"/"LWKM_FIRST_PACKET_POWERSTATION_B1.b64"


class TestKT21LWKMEnvelope(unittest.TestCase):
    def test_first_real_packet_is_blocked_by_source_undefined_runinu(self):
        raw=base64.b64decode(REAL_B64.read_text().strip())
        static,packets,_=decode_unpinned_powerstation_hydrology(raw)
        self.assertEqual(len(packets),1)
        initial_surface=static["initial_surface_record"]
        summary,results=characterize_packets(
            packets,
            initial_pn=initial_surface[2],
            initial_sic=initial_surface[1],
            initial_snla=0.0,
            initial_mofro=tuple(static["initial_moisture"]),
            config=EnvelopeConfig(he_top=0.02,lefrrv=0.2,lefrso=0.25),
        )
        self.assertEqual(summary.blocked_first_call_runinu,1)
        self.assertEqual(summary.deterministic_packet_count,0)
        self.assertEqual(results[0].classification,CLASS_BLOCKED_RUNINU)
        self.assertFalse(results[0].runinu_known)
        self.assertIsNone(results[0].flux)

    def test_positive_runoff_resets_runinu_then_near_zero_is_deterministic(self):
        p0=synthetic_commit_control_packet()
        p0=replace(p0,producer_endpoint_day=1.0,producer_step_days=1.0,runoff=0.0)
        p1=replace(
            p0,
            producer_endpoint_day=2.0,
            runoff=2.0**-20,
            prr=2.0**-20 + 2.0**-30,
        )
        p2=replace(
            p0,
            producer_endpoint_day=3.0,
            prr=0.0,
            runoff=0.0,
            evso=0.0,
            flab=tuple(0.0 for _ in range(p0.layer_count+1)),
            flev=tuple(0.0 for _ in range(p0.layer_count)),
        )
        summary,results=characterize_packets(
            (p0,p1,p2),
            initial_pn=0.0,
            initial_sic=0.0,
            initial_snla=0.0,
            initial_mofro=tuple(0.5 for _ in range(p0.layer_count)),
            config=EnvelopeConfig(he_top=1.0,lefrrv=0.0,lefrso=0.0),
        )
        self.assertEqual(results[0].classification,CLASS_BLOCKED_RUNINU)
        self.assertFalse(results[0].runinu_known)
        self.assertTrue(results[1].runinu_known)
        self.assertEqual(results[1].runinu,0.0)
        self.assertTrue(results[2].runinu_known)
        self.assertEqual(results[2].runinu,0.0)
        self.assertNotEqual(results[2].classification,CLASS_BLOCKED_RUNINU)
        self.assertEqual(summary.first_runinu_reset_index,1)

    def test_exact_zero_after_known_runinu(self):
        p=synthetic_commit_control_packet()
        p=replace(
            p,
            producer_endpoint_day=1.0,
            prr=0.0,
            runoff=2.0**-20,
            mofrt=tuple(0.5 for _ in range(p.layer_count)),
        )
        p2=replace(
            p,
            producer_endpoint_day=2.0,
            runoff=0.0,
            prr=0.0,
        )
        summary,results=characterize_packets(
            (p,p2),
            initial_pn=0.0,
            initial_sic=0.0,
            initial_snla=0.0,
            initial_mofro=tuple(0.5 for _ in range(p.layer_count)),
            config=EnvelopeConfig(he_top=1.0,lefrrv=0.0,lefrso=0.0),
        )
        self.assertTrue(results[1].runinu_known)
        self.assertEqual(results[1].classification,CLASS_EXACT_ZERO)
        self.assertGreaterEqual(summary.exact_zero_count,1)


if __name__=="__main__":
    unittest.main()
