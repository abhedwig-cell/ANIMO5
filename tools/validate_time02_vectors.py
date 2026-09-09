#!/usr/bin/env python3
"""Validate ANIMO-TIME02 exact-time contract vectors.

This is a synthetic qualification tool. It does not execute ANIMO physics and does
not constitute B2 reference evidence or canonical TIME admission.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

CALENDAR_ID = "ANIMO_PG_86400_NOLEAPSECONDS_V1"
DAY_SECONDS = 86400


def coord_value(obj: dict) -> Fraction:
    day = int(obj["day_index"])
    num = int(obj.get("subday_numerator", "0"))
    den = int(obj.get("subday_denominator", "1"))
    if den <= 0:
        raise AssertionError("subday denominator must be positive")
    if num < 0 or num >= den:
        raise AssertionError("subday fraction must satisfy 0 <= numerator < denominator")
    if math.gcd(num, den) != 1:
        raise AssertionError("subday fraction must be reduced")
    return Fraction(day, 1) + Fraction(num, den)


def value_to_coord(value: Fraction) -> dict:
    day = value.numerator // value.denominator
    frac = value - day
    return {
        "day_index": str(day),
        "subday_numerator": str(frac.numerator),
        "subday_denominator": str(frac.denominator),
    }


def parse_civil(text: str) -> Fraction:
    dt = datetime.fromisoformat(text)
    day_index = dt.date().toordinal() - 1
    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    return Fraction(day_index, 1) + Fraction(seconds, DAY_SECONDS)


def validate_calendar_vector(v: dict) -> None:
    if v["class"] == "calendar_round_trip":
        actual = value_to_coord(parse_civil(v["input_civil"]))
        assert actual == v["expected_coordinate"], (v["id"], actual)
        assert v["expected"] == "ACCEPT_VALID_LEAP_DATE"
    else:
        assert v["class"] == "calendar_validation"
        try:
            datetime.fromisoformat(v["input_civil"])
        except ValueError:
            assert v["expected"] == "REJECT_INVALID_GREGORIAN_DATE"
        else:
            raise AssertionError(f"{v['id']}: invalid date unexpectedly parsed")


def validate_management(v: dict) -> None:
    t0 = coord_value(v["t0"])
    t1 = coord_value(v["t1"])
    event = coord_value(v["event"])
    assert t1 > t0
    selected = t0 < event <= t1
    assert v["predicate"] == "t0 < E <= t1"
    assert selected is v["expected_selected"], v["id"]


def validate_harvest(v: dict) -> None:
    t0 = coord_value(v["t0"])
    t1 = coord_value(v["t1"])
    event = coord_value(v["event"])
    assert t1 > t0
    selected = t0 <= event < t1
    assert v["predicate"] == "t0 <= H < t1"
    assert selected is v["expected_selected"], v["id"]


def validate_year_transition(v: dict) -> None:
    t0 = coord_value(v["t0"])
    t1 = coord_value(v["t1"])
    assert t1 - t0 == 1
    assert value_to_coord(parse_civil("2000-01-01T00:00:00")) == v["t1"]
    assert v["expected"] == [
        "PRIOR_YEAR_CLOSEOUT_AFTER_PHYSICAL_T1",
        "NEXT_INTERVAL_NEW_YEAR_START_AT_SAME_EXACT_T1",
    ]


def validate_split(v: dict) -> None:
    split = coord_value(v["split"])
    assert split.denominator >= 1
    owner = {e["event_class"]: e["expected_owner"] for e in v["events"]}
    assert owner == {
        "management": "INTERVAL_ENDING_AT_SPLIT",
        "harvest": "INTERVAL_STARTING_AT_SPLIT",
    }
    assert v["expected"] == "NO_REPLAY_NO_SKIP_AFTER_RESTORE"
    assert v["b2_evidence"] is False


def validate_retry(v: dict) -> None:
    t0 = coord_value(v["accepted_t0"])
    old_t1 = coord_value(v["original_t1"])
    new_t1 = coord_value(v["retry_t1"])
    assert old_t1 > t0 and new_t1 > t0 and old_t1 != new_t1
    assert v["expected"] == [
        "NEW_INTERVAL_ID",
        "FRESH_TRIAL_ID",
        "REBIND_ALL_INTERVAL_SCOPED_FRAMES",
        "RECOMPUTE_EVENT_MEMBERSHIP",
    ]


def validate_hydrology(v: dict) -> None:
    cls = v["class"]
    if cls == "hydrology_frame_exact_match":
        assert coord_value(v["interval_t0"]) == coord_value(v["frame_t0"])
        assert coord_value(v["interval_t1"]) == coord_value(v["frame_t1"])
        assert v["expected"] == "BIND_ALLOWED_IF_OTHER_IDENTITIES_MATCH"
    elif cls == "hydrology_frame_t1_mismatch":
        delta = coord_value(v["interval_t1"]) - coord_value(v["frame_t1"])
        assert delta == Fraction(1, DAY_SECONDS)
        assert v["expected"] == "REJECT_BEFORE_PROCESS_EXECUTION"
        assert v["floating_tolerance_allowed"] is False
    else:
        assert cls == "hydrology_calendar_contract_mismatch"
        assert v["interval_calendar_contract_id"] == CALENDAR_ID
        assert v["frame_calendar_contract_id"] != CALENDAR_ID
        assert v["expected"] == "REJECT_BEFORE_PROCESS_EXECUTION"


def validate_mapping(v: dict) -> None:
    if v["class"] == "legacy_management_integer_day_mapping":
        start = Fraction(int(v["simulation_start"]["day_index"]), 1)
        raw = Fraction(Decimal(v["legacy_Tinead_input"]))
        actual = value_to_coord(start + raw - Fraction(1, 2))
        assert actual == v["expected_coordinate"], (v["id"], actual)
        assert parse_civil(v["expected_civil"]) == coord_value(v["expected_coordinate"])
    else:
        assert v["class"] == "legacy_crop_date_mapping"
        noon = parse_civil(v["input_date"] + "T12:00:00")
        assert value_to_coord(noon) == v["expected_coordinate"]
        assert parse_civil(v["expected_civil"]) == noon


def validate_vector(v: dict) -> None:
    cls = v["class"]
    if cls.startswith("calendar_"):
        validate_calendar_vector(v)
    elif cls == "year_transition":
        validate_year_transition(v)
    elif cls.startswith("management_"):
        validate_management(v)
    elif cls.startswith("harvest_"):
        validate_harvest(v)
    elif cls == "split_restart_boundary":
        validate_split(v)
    elif cls == "changed_t1_retry":
        validate_retry(v)
    elif cls.startswith("hydrology_"):
        validate_hydrology(v)
    elif cls.startswith("legacy_"):
        validate_mapping(v)
    else:
        raise AssertionError(f"Unhandled TIME02 vector class: {cls}")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "integration/animo-time/TIME02_TEST_VECTORS.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["work_unit"] == "ANIMO-TIME02"
    assert data["evidence_class"] == "SYNTHETIC_CONTRACT_VECTORS_NON_B2"
    assert data["calendar_contract_id"] == CALENDAR_ID
    assert data["exact_second"] == {"subday_numerator": "1", "subday_denominator": "86400"}

    ids = [v["id"] for v in data["vectors"]]
    assert len(ids) == len(set(ids)), "duplicate vector id"

    for vector in data["vectors"]:
        validate_vector(vector)

    result = {
        "work_unit": "ANIMO-TIME02",
        "result": "PASS",
        "vectors_total": len(data["vectors"]),
        "vectors_passed": len(data["vectors"]),
        "vectors_failed": 0,
        "comparison_mode": "EXACT_INTEGER_RATIONAL_NO_FLOAT_TOLERANCE",
        "b2_evidence": False,
        "canonical_time_admitted": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
