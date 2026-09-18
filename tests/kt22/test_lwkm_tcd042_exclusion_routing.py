import unittest

from prototype.kt21.lwkm_bounded_envelope import (
    CLASS_E1,
    CLASS_OUTSIDE,
    PacketEnvelopeResult,
    TCD042_FLUX_THRESHOLD,
    TCD042_P_MAX,
)
from prototype.kt22.lwkm_tcd042_exclusion_routing import (
    ROUTE_NOT_KT21_OUTSIDE,
    ROUTE_ORDINARY_POSITIVE_FLOW,
    ROUTE_SUBTHRESHOLD_P_OUTSIDE,
    route_kt21_outside,
)


def packet(classification, flux, p):
    return PacketEnvelopeResult(
        index=1,
        endpoint_day=10.0,
        step_days=10.0,
        typed_step_sha256="0" * 64,
        classification=classification,
        runinu_known=True,
        runinu=0.0,
        flpn=0,
        flux=flux,
        p=p,
    )


class TestKT22Routing(unittest.TestCase):
    def test_flux_at_threshold_routes_to_ordinary_positive_flow(self):
        result = route_kt21_outside(
            packet(CLASS_OUTSIDE, TCD042_FLUX_THRESHOLD, 1.0e-5)
        )
        self.assertEqual(result.label, ROUTE_ORDINARY_POSITIVE_FLOW)

    def test_subthreshold_p_exceedance_remains_distinct(self):
        result = route_kt21_outside(
            packet(CLASS_OUTSIDE, 1.0e-10, TCD042_P_MAX * 2.0)
        )
        self.assertEqual(result.label, ROUTE_SUBTHRESHOLD_P_OUTSIDE)

    def test_non_outside_packet_is_not_reclassified(self):
        result = route_kt21_outside(packet(CLASS_E1, 1.0e-12, 1.0e-9))
        self.assertEqual(result.label, ROUTE_NOT_KT21_OUTSIDE)

    def test_malformed_outside_packet_fails_closed(self):
        with self.assertRaises(ValueError):
            route_kt21_outside(packet(CLASS_OUTSIDE, None, None))


if __name__ == "__main__":
    unittest.main()
