from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "validate_prep10c_review_request.py"
RECORD_PATH = ROOT / "integration" / "animo-prep" / "PREP10C_B3_REVIEW_REQUEST.json"

spec = importlib.util.spec_from_file_location("validate_prep10c_review_request", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class Prep10CReviewRequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def test_current_request_passes(self):
        mod.validate(copy.deepcopy(self.valid))

    def test_cannot_self_claim_b3_admission(self):
        record = copy.deepcopy(self.valid)
        record["b3_admitted"] = True
        with self.assertRaisesRegex(mod.ReviewRequestError, "b3_admitted"):
            mod.validate(record)

    def test_cannot_open_normal_route_without_reference(self):
        record = copy.deepcopy(self.valid)
        record["historical_reference_dependency"]["normal_b2_route_eligible"] = True
        with self.assertRaisesRegex(mod.ReviewRequestError, "normal B2 route"):
            mod.validate(record)

    def test_cannot_claim_independent_review_in_pre_review_snapshot(self):
        record = copy.deepcopy(self.valid)
        record["independent_second_line_review_completed"] = True
        with self.assertRaisesRegex(mod.ReviewRequestError, "independent review"):
            mod.validate(record)

    def test_tcd_reservation_is_not_canonical_append(self):
        record = copy.deepcopy(self.valid)
        record["b3_context"]["tcd_reservation_canonical_append_proven"] = True
        with self.assertRaisesRegex(mod.ReviewRequestError, "canonical TCD append"):
            mod.validate(record)

    def test_historical_uncertainty_requires_exhaustion(self):
        record = copy.deepcopy(self.valid)
        record["historical_reference_dependency"]["historical_uncertainty_route_acquisition_precondition_exhausted"] = True
        with self.assertRaisesRegex(mod.ReviewRequestError, "unexhausted"):
            mod.validate(record)


if __name__ == "__main__":
    unittest.main()
