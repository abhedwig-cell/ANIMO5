from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[2] / "tools" / "stateq01"
sys.path.insert(0, str(TOOLS))

from checkpoint_serializer_purity_harness import (  # noqa: E402
    SerializerPurityError,
    qualification_serialize_accepted_state,
)


def accepted_fixture():
    identity = {
        "profile_id": "CORE_CNP_SUBSURFACE_ONLY",
        "accepted_generation_id": "gen-final-17",
        "accepted_time": {
            "calendar_contract_id": "ANIMO_PG_86400_NOLEAPSECONDS_V1",
            "day_index": "730120",
            "subday_numerator": "0",
            "subday_denominator": "1",
        },
        "configuration_identity": "cfg-A",
        "physical_layout_id": "layout-A",
    }
    physical = {
        "nh4": [1.25, 0.75],
        "no3": [2.0, 1.5],
        "organic_c": [[10.0, 8.0], [4.0, 3.0]],
        "upper_boundary": {
            "nh4": 0.5,
            "no3": 0.6,
            "dom": 0.7,
            "don": 0.8,
            "po4": 0.9,
            "dop": 1.0,
        },
        # Sensitivity sentinel for the TS01 Output_Init side-effect pattern.
        # This field is not an admission of crop state into the restricted core.
        "serializer_negative_value_sentinel": -0.125,
    }
    continuation = {
        "management_schedule_identity": "mgmt-A",
        "next_management_event_id": "add004",
    }
    diagnostics = {
        "report_period_id": "report-3",
        "n_balance_accumulator": 123.0,
    }
    return identity, physical, continuation, diagnostics


class CheckpointSerializerPurityTests(unittest.TestCase):
    def test_rc_r8_physical_state_not_mutated(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        original = deepcopy(physical)
        qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        )
        self.assertEqual(physical, original)

    def test_rc_r8_continuation_not_mutated(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        original = deepcopy(continuation)
        qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        )
        self.assertEqual(continuation, original)

    def test_identity_header_not_mutated(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        original = deepcopy(identity)
        qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        )
        self.assertEqual(identity, original)

    def test_negative_value_is_preserved_not_clamped(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        projection = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        )
        decoded = json.loads(projection.payload_bytes)
        self.assertEqual(decoded["physical_state"]["serializer_negative_value_sentinel"], -0.125)
        self.assertEqual(physical["serializer_negative_value_sentinel"], -0.125)

    def test_repeated_serialization_is_byte_stable_for_same_fixture(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        first = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        ).payload_bytes
        second = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        ).payload_bytes
        self.assertEqual(first, second)

    def test_key_order_does_not_change_qualification_bytes(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        reordered = dict(reversed(list(physical.items())))
        a = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        ).payload_bytes
        b = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=reordered,
            continuation_state=continuation,
        ).payload_bytes
        self.assertEqual(a, b)

    def test_diagnostic_state_omitted_without_mutation_when_not_requested(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        original = deepcopy(diagnostics)
        projection = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
            diagnostic_state=diagnostics,
            include_diagnostics=False,
        )
        decoded = json.loads(projection.payload_bytes)
        self.assertNotIn("diagnostic_observer_state", decoded)
        self.assertEqual(diagnostics, original)

    def test_diagnostic_state_included_separately_without_mutation(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        original = deepcopy(diagnostics)
        projection = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
            diagnostic_state=diagnostics,
            include_diagnostics=True,
        )
        decoded = json.loads(projection.payload_bytes)
        self.assertEqual(decoded["diagnostic_observer_state"], diagnostics)
        self.assertEqual(diagnostics, original)

    def test_missing_requested_diagnostics_rejected_without_mutation(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        originals = tuple(deepcopy(x) for x in (identity, physical, continuation))
        with self.assertRaises(SerializerPurityError):
            qualification_serialize_accepted_state(
                identity_header=identity,
                physical_state=physical,
                continuation_state=continuation,
                diagnostic_state=None,
                include_diagnostics=True,
            )
        self.assertEqual((identity, physical, continuation), originals)

    def test_nan_rejected_without_mutation(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        physical["bad"] = float("nan")
        original_keys = set(physical.keys())
        with self.assertRaises(SerializerPurityError):
            qualification_serialize_accepted_state(
                identity_header=identity,
                physical_state=physical,
                continuation_state=continuation,
            )
        self.assertEqual(set(physical.keys()), original_keys)
        self.assertTrue(physical["bad"] != physical["bad"])

    def test_infinity_rejected_without_mutation(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        physical["bad"] = float("inf")
        with self.assertRaises(SerializerPurityError):
            qualification_serialize_accepted_state(
                identity_header=identity,
                physical_state=physical,
                continuation_state=continuation,
            )
        self.assertEqual(physical["bad"], float("inf"))

    def test_unsupported_object_rejected_without_mutation(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        physical["bad"] = {"not-a-json-set"}
        with self.assertRaises(SerializerPurityError):
            qualification_serialize_accepted_state(
                identity_header=identity,
                physical_state=physical,
                continuation_state=continuation,
            )
        self.assertEqual(physical["bad"], {"not-a-json-set"})

    def test_serialized_bytes_are_detached_from_later_state_mutation(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        projection = qualification_serialize_accepted_state(
            identity_header=identity,
            physical_state=physical,
            continuation_state=continuation,
        )
        before = projection.payload_bytes
        physical["nh4"][0] = 999.0
        self.assertEqual(projection.payload_bytes, before)
        self.assertNotEqual(json.loads(before)["physical_state"]["nh4"][0], 999.0)

    def test_sensitivity_legacy_style_in_place_clamp_would_be_detected(self):
        identity, physical, continuation, diagnostics = accepted_fixture()
        before = deepcopy(physical)
        # This deliberately models the kind of in-place Output_Init side effect
        # TS01 found. It is not used by the serializer under test.
        if physical["serializer_negative_value_sentinel"] < 0:
            physical["serializer_negative_value_sentinel"] = 0.0
        self.assertNotEqual(physical, before)


if __name__ == "__main__":
    unittest.main()
