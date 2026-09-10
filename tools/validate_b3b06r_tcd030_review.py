#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B06R_STATUS.json"
EVIDENCE = ROOT / "integration/animo-b3/TCD030_INDEPENDENT_REVIEW_EVIDENCE.json"
UPSTREAM = ROOT / "integration/animo-b3/TCD030_SOURCE_EVIDENCE.json"
MANIFEST = ROOT / "reference/source/source_manifest.csv"
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def checkrea(name, value, low, high, nihil=1.0e-30):
    if abs(low - 999.0) > nihil and value < low:
        return {"status": "REJECT", "error": 1992, "diag": name}
    if abs(high - 999.0) > nihil and value > high:
        return {"status": "REJECT", "error": 1993, "diag": name}
    return {"status": "ACCEPT", "error": 0, "diag": None}


def run(ioptmp, nh4, no3, candidate):
    if ioptmp == 0:
        return {"status": "ACCEPT", "error": 0, "diag": None}
    calls = [
        ("CoMpnh(1)", nh4[0]),
        ("CoMpnh(2)", nh4[1]),
        ("CoMpni(1)", no3[0] if candidate else nh4[0]),
        ("CoMpni(2)", no3[1] if candidate else nh4[1]),
    ]
    for name, value in calls:
        result = checkrea(name, value, 0.0, 999.0)
        if result["status"] == "REJECT":
            return result
    return {"status": "ACCEPT", "error": 0, "diag": None}


def main():
    st = load_json(STATUS)
    ev = load_json(EVIDENCE)
    src = load_json(UPSTREAM)

    assert st["work_unit"] == "ANIMO-B3B06R"
    assert st["decision"] == "PASS_INDEPENDENT_SECOND_LINE_REVIEW_TIER_B"
    assert st["gov04_risk_tier"] == "B"
    assert st["historical_behavior"] == "UNKNOWN"
    assert st["historical_b2_qualified"] is False
    for key in (
        "admission_performed", "production_patch_performed", "canonical_register_modified",
        "central_regie_modified", "b4_performed", "migration_performed",
    ):
        assert st[key] is False, key
    assert st["composition"] == {"TCD-025": False, "TCD-031": False}

    # Recheck the pinned source-bound transcript. This validates facts, not
    # the B3B06 readiness decision.
    assert src["target"] == "TCD-030"
    assert src["frozen_b0"]["archive_sha256"] == ev["frozen_b0"]["archive_sha256"]
    assert src["frozen_b0"]["mapoinput_sha256"] == ev["frozen_b0"]["mapoinput_sha256"]
    assert src["frozen_b0"]["input1_sha256"] == ev["frozen_b0"]["input1_sha256"]
    seam = src["exact_seam"]
    r = ev["source_reconstruction"]
    assert seam["routine"] == r["routine"] == "MaPoInput"
    assert seam["trigger"] == r["routine_branch"] == "Nupa.EQ.4"
    assert seam["caller_gate"] == r["caller_gate"] == "Ioptmp.Eq.1"
    assert seam["read_order"] == r["read_value_sequence"] == [
        "CoMpnh(1)", "CoMpnh(2)", "CoMpni(1)", "CoMpni(2)"
    ]
    assert [(x["checked_value_legacy"], x["checked_value_intended"]) for x in seam["faulty_calls"]] == [
        ("CoMpnh(1)", "CoMpni(1)"),
        ("CoMpnh(2)", "CoMpni(2)"),
    ]

    cr = src["checkrea_contract"]
    assert cr["low_guard"] == "Abs(Low-999.).Gt.Nihil .And. Value.Lt.Low"
    assert cr["high_guard"] == "Abs(High-999.).Gt.Nihil .And. Value.Gt.High"
    assert cr["low_failure_error"] == 1992
    assert cr["high_failure_error"] == 1993
    assert cr["sentinel"] == 999.0
    assert checkrea("x", 0.0, 0.0, 999.0)["error"] == 0
    assert checkrea("x", -1.0e-6, 0.0, 999.0)["error"] == 1992
    assert checkrea("x", 1000000.0, 0.0, 999.0)["error"] == 0
    assert checkrea("x", 2.0, 0.0, 1.0)["error"] == 1993

    required = {
        "valid_unequal", "invalid_no3_d1", "invalid_no3_d2", "zero_boundary",
        "just_below_zero", "above_999", "invalid_nh4_control", "inactive"
    }
    seen = set()
    for case in ev["matrix"]:
        seen.add(case["id"])
        legacy = run(case["ioptmp"], case["nh4"], case["no3"], False)
        candidate = run(case["ioptmp"], case["nh4"], case["no3"], True)
        assert legacy == case["legacy"], (case["id"], "legacy", legacy, case["legacy"])
        assert candidate == case["candidate"], (case["id"], "candidate", candidate, case["candidate"])
    assert seen == required

    manifest = MANIFEST.read_text(encoding="utf-8")
    assert "ANIMO_4.1.5.53/mapoinput.for" in manifest
    assert ev["frozen_b0"]["mapoinput_sha256"] in manifest
    assert "ANIMO_4.1.5.53/input1.for" in manifest
    assert ev["frozen_b0"]["input1_sha256"] in manifest

    with REGISTER.open(encoding="utf-8", newline="") as f:
        rows = {row["ID"]: row for row in csv.DictReader(f)}
    for tcd in ("TCD-025", "TCD-030", "TCD-031"):
        assert tcd in rows
    assert "validation" in rows["TCD-030"]["process"].lower()
    assert rows["TCD-030"]["status"] == "OPEN"
    assert "ledger" in (rows["TCD-025"]["process"] + rows["TCD-025"]["difference"]).lower()
    assert "restart" in (rows["TCD-031"]["process"] + rows["TCD-031"]["difference"]).lower()

    assert ev["composition"]["tcd025"]["present"] is False
    assert ev["composition"]["tcd031"]["present"] is False
    assert ev["historical_evidence"]["qualified_b2"] is False
    assert ev["historical_evidence"]["behavior"] == "UNKNOWN"
    assert ev["gov04"]["selected_tier"] == "B"
    assert ev["gov04"]["tier_c_escalation"] is False
    assert ev["review_result"] == st["decision"]

    print("PASS ANIMO-B3B06R independent TCD-030 Tier-B second-line review validator")


if __name__ == "__main__":
    main()
