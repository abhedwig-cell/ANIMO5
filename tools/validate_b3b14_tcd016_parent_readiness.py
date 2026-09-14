#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"
EXPECTED = "QUALIFIED_TCD016_PARENT_NOT_READY_EXPLICIT_MODEL_EVOLUTION_DECISION_REQUIRED"

def load(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))

required = [
    "B3B14_TCD016_PARENT_RECONSTRUCTION.json",
    "B3B14_AUTHORITY_EVIDENCE_MATRIX.json",
    "B3B14_UNRESOLVED_BLOCKER_CLASSIFICATION.json",
    "B3B14_CHILD_PARENT_COMPOSITION.json",
    "B3B14_MASS_STATE_RESTART_READINESS.json",
    "B3B14_TCD016_PARENT_READINESS_DECISION.json",
    "ANIMO-B3B14_STATUS.json",
]
for name in required:
    assert (B3 / name).is_file(), name

status = load("ANIMO-B3B14_STATUS.json")
decision = load("B3B14_TCD016_PARENT_READINESS_DECISION.json")
blockers = load("B3B14_UNRESOLVED_BLOCKER_CLASSIFICATION.json")
composition = load("B3B14_CHILD_PARENT_COMPOSITION.json")
state = load("B3B14_MASS_STATE_RESTART_READINESS.json")
auth = load("B3B14_AUTHORITY_EVIDENCE_MATRIX.json")
parent = load("B3B14_TCD016_PARENT_RECONSTRUCTION.json")

assert status["primary_disposition"] == EXPECTED
assert decision["primary_disposition"] == EXPECTED
assert decision["readiness"] is False
assert decision["b3_admission_performed"] is False
assert decision["production_authorized"] is False
assert blockers["minimal_blocker_class"] == "EXPLICIT_MODEL_EVOLUTION_AUTHORIZATION_REQUIRED"
assert composition["parent_definition_narrowed"] is False
assert composition["parent_surface_gates"]["rewetting_boundary"].startswith("FAIL_")
assert parent["known_child_set_complete_for_readiness_review"] is True
assert parent["implicit_child_missing"] is False
assert auth["gov06_ownership"]["owned_contract"] == "TCD016_PARENT_READINESS_SYNTHESIS"
assert auth["gov06_ownership"]["parallelism"] == "PARALLEL_AFTER_PINNING"
assert state["typed_transfer_rules"]["mass_observer_can_reconstruct_physical_state"] is False
rewet = [r for r in state["matrix"] if r["operation"] == "continue_rewet"]
assert len(rewet) == 1 and rewet[0]["status"] == "ADMISSION_BLOCKING"
assert status["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
for k in ["b3_admission_performed","tcd_register_mutated","b3_queue_mutated","aggregate_mutated","routing_mutated","production_source_modified","b4_opened","tb7_opened","production_authorized"]:
    assert status[k] is False, k

fragment = json.loads((ROOT / "integration" / "animo-testbank" / "fragments" / "ANIMO-B3B14_TCD016_PARENT_READINESS_FRAGMENT.json").read_text(encoding="utf-8"))
assert fragment["opens_tb7"] is False
assert fragment["whole_model_golden_baseline"] is False
assert fragment["central_testbank_registry_mutated"] is False
assert fragment["readiness_oracle"]["expected_primary_disposition"] == EXPECTED

text = (ROOT / "docs" / "science" / "TCD016_PARENT_CLOSURE_READINESS_SYNTHESIS.md").read_text(encoding="utf-8")
for phrase in [
    "mass/state sufficiency does not establish a scientific rewetting lifecycle",
    "not a physical inertness law",
    "UNKNOWN_WITHOUT_B2",
    EXPECTED,
    "No B3 admission is performed here",
]:
    assert phrase in text, phrase

print("ANIMO-B3B14 parent readiness package: PASS")
