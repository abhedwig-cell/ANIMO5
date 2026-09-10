#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "integration/animo-b3/TCD030_SOURCE_EVIDENCE.json"
MATRIX = ROOT / "integration/animo-b3/TCD030_VALIDATION_MATRIX.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B06_STATUS.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def checkrea(name, value, low=0.0, high=999.0):
    nihil = 1.0e-30
    if abs(low - 999.0) > nihil and value < low:
        return {"accepted": False, "error": 1992, "diagnostic_variable": name}
    if abs(high - 999.0) > nihil and value > high:
        return {"accepted": False, "error": 1993, "diagnostic_variable": name}
    return {"accepted": True, "error": 0, "diagnostic_variable": None}


def run_model(ioptmp, nh4, no3, candidate):
    if ioptmp == 0:
        return {"accepted": True, "error": 0, "diagnostic_variable": None, "path": "MPNITR_NOT_CALLED"}

    sequence = [
        ("CoMpnh(1)", nh4[0]),
        ("CoMpnh(2)", nh4[1]),
        ("CoMpni(1)", no3[0] if candidate else nh4[0]),
        ("CoMpni(2)", no3[1] if candidate else nh4[1]),
    ]
    for name, value in sequence:
        result = checkrea(name, value)
        if not result["accepted"]:
            return result
    return {"accepted": True, "error": 0, "diagnostic_variable": None}


def comparable(actual, expected):
    for key, value in expected.items():
        if actual.get(key) != value:
            return False
    return True


def main():
    ev = load(EVIDENCE)
    mx = load(MATRIX)
    st = load(STATUS)

    assert ev["target"] == mx["target"] == st["target"] == "TCD-030"
    assert st["b3_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert st["gov04_risk_tier"] == "B"
    assert st["tier_c_escalation_triggered"] is False
    assert st["historical_behavior"] == "UNKNOWN"
    assert st["historical_b2_qualified"] is False
    assert st["decision"] == "PASS_ATOMIC_TIER_B_READINESS_REQUIRES_ONE_INDEPENDENT_SECOND_LINE_REVIEW"
    assert st["independent_review"]["required_by_gov04"] is True
    assert st["independent_review"]["performed_in_this_context"] is False

    seam = ev["exact_seam"]
    assert seam["routine"] == "MaPoInput"
    assert seam["trigger"] == "Nupa.EQ.4"
    assert seam["caller_gate"] == "Ioptmp.Eq.1"
    assert seam["read_order"] == ["CoMpnh(1)", "CoMpnh(2)", "CoMpni(1)", "CoMpni(2)"]
    assert seam["lower_bound"] == 0.0
    assert seam["high_argument"] == 999.0
    assert seam["high_argument_semantics"] == "NO_HIGH_LIMIT_SENTINEL"
    assert [(x["checked_value_legacy"], x["checked_value_intended"]) for x in seam["faulty_calls"]] == [
        ("CoMpnh(1)", "CoMpni(1)"),
        ("CoMpnh(2)", "CoMpni(2)"),
    ]

    assert checkrea("x", 0.0)["accepted"] is True
    assert checkrea("x", -1.0e-6)["error"] == 1992
    assert checkrea("x", 1000000.0)["accepted"] is True

    for case in mx["cases"]:
        legacy = run_model(case["ioptmp"], case["nh4"], case["no3"], False)
        candidate = run_model(case["ioptmp"], case["nh4"], case["no3"], True)
        assert comparable(legacy, case["legacy"]), (case["id"], "legacy", legacy, case["legacy"])
        assert comparable(candidate, case["candidate"]), (case["id"], "candidate", candidate, case["candidate"])

    assert mx["expected_difference_contract"]["allowed"] == [
        "INPUT_ACCEPTANCE_REJECTION",
        "DIRECT_VALIDATION_DIAGNOSTIC",
    ]
    forbidden = set(mx["expected_difference_contract"]["forbidden"])
    required_forbidden = {
        "PHYSICAL_TRANSPORT_ALGEBRA",
        "PERSISTENT_STATE_LAYOUT_OR_SEMANTICS",
        "RESTART_SEMANTICS",
        "NUMERICAL_POLICY",
        "SOLVER_OR_TOLERANCE",
        "TCD025_LEDGER_COMPOSITION",
        "TCD031_PERSISTENT_STATE_COMPOSITION",
    }
    assert required_forbidden <= forbidden
    assert mx["expected_difference_contract"]["production_patch_in_this_workunit"] is False
    assert mx["comparison_domain"]["trajectory_equivalence_claimed_for_divergence_domain"] is False
    assert mx["control_flow_observation"]["overall_parser_newly_accepts_any_case_due_to_tcd030_fix"] is False

    assert ev["ownership"]["persistent_state_semantics_changed"] is False
    assert ev["canonical_identity"]["admitted"] is False

    print("PASS ANIMO-B3B06 TCD-030 atomic Tier-B readiness validator")


if __name__ == "__main__":
    main()
