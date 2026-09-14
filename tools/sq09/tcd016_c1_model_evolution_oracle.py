#!/usr/bin/env python3
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAGMENT = ROOT / "integration/animo-testbank/fragments/ANIMO-SQ09_TCD016_C1_MODEL_EVOLUTION_FRAGMENT.json"


def D(value):
    return Decimal(str(value))


def apply_rewet_candidate(m_cont, s_aq, surface_aqueous_active):
    """Pure oracle for the selected *candidate* contract, not physical validation."""
    m_cont = D(m_cont)
    s_aq = D(s_aq)
    if m_cont < 0 or s_aq < 0:
        raise ValueError("negative storage is outside the SQ09 candidate oracle")
    if not surface_aqueous_active:
        return Decimal("0"), m_cont, s_aq
    transfer = m_cont
    return transfer, Decimal("0"), s_aq + transfer


def assert_equal(actual, expected, label):
    expected = D(expected)
    assert actual == expected, f"{label}: actual={actual} expected={expected}"


def run_single(entry):
    inp = entry["input"]
    t, m_after, s_after = apply_rewet_candidate(
        inp["M_cont_before"], inp["S_aq_before"], inp["surface_aqueous_active"]
    )
    exp = entry["expected"]
    assert_equal(t, exp["T_rewet"], f"{entry['id']} transfer")
    assert_equal(m_after, exp["M_cont_after"], f"{entry['id']} source")
    assert_equal(s_after, exp["S_aq_after"], f"{entry['id']} receiver")
    before = D(inp["M_cont_before"]) + D(inp["S_aq_before"])
    after = m_after + s_after
    assert before == after, f"{entry['id']} conservation"


def run_sequence(entry):
    first = entry["sequence"][0]
    t, m_cont, s_aq = apply_rewet_candidate(
        first["M_cont_before"], first["S_aq_before"], first["surface_aqueous_active"]
    )
    total_t = t
    total_mass = D(first["M_cont_before"]) + D(first["S_aq_before"])
    assert m_cont + s_aq == total_mass, f"{entry['id']} step-1 conservation"

    for step in entry["sequence"][1:]:
        if "add_new_continuation_mass" in step:
            added = D(step["add_new_continuation_mass"])
            assert added >= 0
            m_cont += added
            total_mass += added
        t, m_cont, s_aq = apply_rewet_candidate(
            m_cont, s_aq, step["surface_aqueous_active"]
        )
        total_t += t
        assert m_cont + s_aq == total_mass, f"{entry['id']} sequence conservation"

    exp = entry["expected_final"]
    assert_equal(total_t, exp["total_T_rewet"], f"{entry['id']} total transfer")
    assert_equal(m_cont, exp["M_cont_after"], f"{entry['id']} final source")
    assert_equal(s_aq, exp["S_aq_after"], f"{entry['id']} final receiver")


def main():
    fragment = json.loads(FRAGMENT.read_text())
    assert fragment["evidence_class"] == "MODEL_EVOLUTION_CONTRACT_ORACLE_ONLY"
    assert fragment["physical_validation_claimed"] is False
    assert fragment["historical_b2_claimed"] is False
    assert fragment["contract"]["activation_threshold"] is None
    assert fragment["contract"]["parameters"] == []

    for entry in fragment["entries"]:
        if "input" in entry:
            run_single(entry)
        else:
            run_sequence(entry)

    print("SQ09_MODEL_EVOLUTION_CONTRACT_ORACLE_PASS")
    print("INTERPRETATION_LIMIT: algebra/state-machine evidence only; no physical or historical validation")


if __name__ == "__main__":
    main()
