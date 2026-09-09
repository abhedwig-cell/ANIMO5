#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_RECORD_TYPE = "INDEPENDENT_B3_REVIEW_REQUEST_NOT_DISPOSITION"
EXPECTED_DISPOSITION = "UNRESOLVED_NOT_ADMITTED"
EXPECTED_BLOCKED_ROUTE = "NO_B3_ADMISSION_ROUTE_CURRENTLY_ELIGIBLE"
EXPECTED_TCD_STATUS = "RESERVED_PENDING_CANONICAL_REGISTER_APPEND_NOT_ADMITTED"


class ReviewRequestError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewRequestError(message)


def validate(record: dict) -> None:
    _require(record.get("record_type") == EXPECTED_RECORD_TYPE, "unexpected record_type")
    _require(record.get("status") == "READY_FOR_INDEPENDENT_REVIEW_NOT_REVIEWED_NOT_ADMITTED", "unexpected request status")

    b3 = record.get("b3_context") or {}
    hist = record.get("historical_reference_dependency") or {}
    reviewer = record.get("reviewer") or {}
    gates = record.get("required_review_gates") or {}

    _require(b3.get("current_disposition") == EXPECTED_DISPOSITION, "request must remain unresolved/not admitted")
    _require(b3.get("tcd_reservation_status") == EXPECTED_TCD_STATUS, "unexpected TCD reservation state")
    _require(b3.get("tcd_reservation_canonical_append_proven") is False, "request must not claim canonical TCD append")

    _require(hist.get("historical_reference_artifact_obtained") is False, "route snapshot unexpectedly claims historical artifact")
    _require(hist.get("reference_qualified") is False, "route snapshot unexpectedly claims qualified B2")
    _require(hist.get("normal_b2_route_eligible") is False, "normal B2 route must remain ineligible in this snapshot")
    _require(hist.get("historical_uncertainty_route_acquisition_precondition_exhausted") is False, "historical-uncertainty acquisition precondition must remain unexhausted in this snapshot")
    _require(hist.get("route_conclusion") == EXPECTED_BLOCKED_ROUTE, "route conclusion is not fail-closed")

    _require(gates.get("historical_route_eligibility") == "BLOCKED_PREP02R_ARTIFACT_NOT_OBTAINED_AND_ACQUISITION_NOT_EXHAUSTED", "historical route gate is inconsistent")

    # This file is a request, never a disposition/admission record.
    for field in ("corrected_legacy_admitted", "b3_admitted", "production_migration_admitted"):
        _require(record.get(field) is False, f"{field} must remain false in a review request")

    review_completed = record.get("review_completed")
    independent_completed = record.get("independent_second_line_review_completed")
    _require(review_completed is False, "this frozen request snapshot must remain not reviewed")
    _require(independent_completed is False, "this frozen request snapshot must not self-claim independent review")
    _require(record.get("review_outcome") is None, "review outcome must be null before independent review")

    for field in ("identity", "independent_workunit", "reviewed_candidate_commit", "review_date", "independence_statement"):
        _require(reviewer.get(field) is None, f"reviewer.{field} must remain null before independent review")

    for name, value in gates.items():
        if name == "historical_route_eligibility":
            continue
        _require(value == "PENDING", f"gate {name} must remain PENDING before independent review")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate PREP10C independent-review request as a fail-closed pre-review snapshot.")
    ap.add_argument("record", type=Path)
    args = ap.parse_args()
    data = json.loads(args.record.read_text(encoding="utf-8"))
    try:
        validate(data)
    except ReviewRequestError as exc:
        raise SystemExit(f"PREP10C review-request validation failed: {exc}")
    print("PREP10C review-request validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
