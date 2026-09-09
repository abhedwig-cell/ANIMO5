#!/usr/bin/env python3
"""Fail-closed structural validator for ANIMO-GOV03."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "integration/animo-governance/ANIMO-GOV03_STATUS.json"
EVIDENCE_PATH = ROOT / "integration/animo-governance/GOV03_ACQUISITION_EVIDENCE.json"
DOC_PATH = ROOT / "docs/governance/ANIMO_GOV03_HISTORICAL_B2_ACQUISITION_CLOSURE.md"

RG05_HEAD = "f127528e148b9106149daec02d48ad972581e6df"
GOV02_HEAD = "db7add6f9561730bbf352aa7fd3f3968405cfaa3"
PREP02R_HEAD = "a2fda49871ee3c7104daf7e06cd8dffdac06b125"
CLOSURE = "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
G6U = "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    status = load(STATUS_PATH)
    evidence = load(EVIDENCE_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")

    assert status["work_unit"] == "ANIMO-GOV03"
    assert status["branch"] == "work/animo-gov03-historical-b2-acquisition-closure"
    assert status["base"]["work_unit"] == "ANIMO-RG05"
    assert status["base"]["head"] == RG05_HEAD
    assert status["governance_authority"]["GOV02"] == GOV02_HEAD
    assert status["governance_authority"]["PREP02R"] == PREP02R_HEAD
    assert GOV02_HEAD in status["governance_authority"]["closure_contract_authority"]
    assert status["target_closure_state"] == CLOSURE
    assert status["target_G6U_state"] == G6U

    assert evidence["work_unit"] == "ANIMO-GOV03"
    assert evidence["recorded_date"] == "2026-09-09"
    assert evidence["acquisition_completion_date"] == "2026-09-09"
    assert evidence["proposed_closure_state"] == CLOSURE
    assert evidence["inherited_search_record"]["PREP02R"] == PREP02R_HEAD
    assert evidence["inherited_search_record"]["GOV02"] == GOV02_HEAD

    contacts = {c["name"]: c for c in evidence["project_owner_attestation"]["contacts"]}
    assert set(contacts) == {"Piet Groenendijk", "Leo Renaud", "Marius Heinen"}
    assert "correct route" in contacts["Piet Groenendijk"]["expert_concurrence"]
    for c in contacts.values():
        assert "No additional usable historical ANIMO reference artifacts were recovered" in c["result"]

    mapping = evidence["gov02_reasonable_effort_mapping"]
    assert len(mapping) == 7
    assert all(v.startswith("PASS") for v in mapping.values())
    assert mapping["criterion_6_independent_reviewer_approves_stopping_rationale"] == "PASS_NAMED_EXTERNAL_EXPERT_CONCURRENCE_PIET_GROENENDIJK"

    limits = evidence["evidence_strength_limits"]
    assert all(v is False for v in limits.values())

    hard = status["hard_boundaries"]
    assert all(v is False for v in hard.values())
    assert "does not qualify historical behaviour" in status["qualification_claim"]
    assert "does not qualify historical behaviour" in status["qualification_claim"]

    assert CLOSURE in doc
    assert G6U in doc
    assert "Historical behaviour remains `UNKNOWN`" in doc
    assert "problematic historical executable to B2" in doc
    assert "rebuild to historical B2" in doc
    assert "Piet Groenendijk" in doc
    assert "Leo Renaud" in doc
    assert "Marius Heinen" in doc
    assert "Reopening rule" in doc

    required = {
        "integration/animo-governance/GOV03_ACQUISITION_EVIDENCE.json",
        "integration/animo-governance/ANIMO-GOV03_STATUS.json",
        "docs/governance/ANIMO_GOV03_HISTORICAL_B2_ACQUISITION_CLOSURE.md",
        "tools/validate_gov03_acquisition_closure.py",
        ".github/workflows/animo-gov03-acquisition-closure.yml",
    }
    assert set(status["deliverables"]) == required
    for rel in required:
        assert (ROOT / rel).exists(), rel

    ws = status["work_status"]
    if ws["qualified"]:
        assert status["state"] == "QUALIFIED_HISTORICAL_B2_ACQUISITION_CLOSURE_G6U_ELIGIBLE_NO_B2_NO_ADMISSIONS"
        assert status["decision"] == status["state"]
        assert ws == {"realized": True, "persisted": True, "tested": True, "qualified": True, "work_unit_complete": True}
        val = status["validation"]
        assert val["github_actions_conclusion"] == "success"
        assert val["validator_result"] == "PASS"
        assert val["scope_guard"] == "PASS_GOV03_GOVERNANCE_ONLY"
    else:
        assert status["state"] == "IN_PROGRESS_PERSISTED_ACQUISITION_EVIDENCE_CAPTURED_VALIDATION_PENDING"
        assert status["decision"] == "PENDING_FAIL_CLOSED_VALIDATION"
        assert ws == {"realized": True, "persisted": True, "tested": False, "qualified": False, "work_unit_complete": False}

    print("ANIMO-GOV03 acquisition closure validator: PASS")
    print("named expert/archive acquisition evidence: PASS")
    print("GOV02 seven-condition bounded effort mapping: PASS")
    print("historical B2 recovered: NO")
    print("G6U historical-uncertainty route eligibility candidate: PASS")
    print("scientific/B4/production admissions: 0")


if __name__ == "__main__":
    main()
