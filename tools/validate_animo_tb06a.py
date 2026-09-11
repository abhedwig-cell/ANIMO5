#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / "integration/animo-testbank/fragments/ANIMO-TB06A_NUMERICAL_COMPILER_RUNTIME_FRAGMENT.json"
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
STATUS = ROOT / "integration/animo-testbank/ANIMO-TB06A_STATUS.json"


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    frag = load(FRAGMENT)
    reg = load(REGISTRY)
    status = load(STATUS)

    assert frag["fragment_id"] == "ANIMO-TB06A-NUMERICAL-COMPILER-RUNTIME"
    assert frag["producer_workunit"] == "ANIMO-TB06A"
    assert frag["base_authority"] == "ANIMO-TB05B@fe0a5aae6382cf37e1ad233655f313f5fa60f874"
    assert frag["central_registry_write"] == "FORBIDDEN_BY_FRAGMENT_PRODUCER"

    entries = frag["entries"]
    ids = [e["test_id"] for e in entries]
    assert len(ids) == len(set(ids))

    central_ids = {e["test_id"] for e in reg["test_registry"]}
    assert not (set(ids) & central_ids), f"fragment IDs collide with central registry: {set(ids) & central_ids}"

    required = {
        "test_id", "layer", "owner", "status", "source_identity",
        "expected_value_provenance", "comparison_policy", "claim",
        "applicability_pins", "failure_semantics", "permanence"
    }
    for e in entries:
        assert required <= set(e), f"missing fields for {e.get('test_id')}"
        assert e["status"] in {"QUALIFIED_FRAGMENT_ENTRY", "GAP"}

    by_id = {e["test_id"]: e for e in entries}
    assert by_id["ATB-NUM-002"]["status"] == "QUALIFIED_FRAGMENT_ENTRY"
    assert by_id["ATB-NUM-003"]["status"] == "QUALIFIED_FRAGMENT_ENTRY"
    assert by_id["ATB-NUM-004"]["status"] == "QUALIFIED_FRAGMENT_ENTRY"
    assert by_id["ATB-ARCH-003"]["status"] == "QUALIFIED_FRAGMENT_ENTRY"
    assert by_id["ATB-NUM-005"]["status"] == "GAP"
    assert by_id["ATB-ARCH-004"]["status"] == "GAP"

    n2 = by_id["ATB-NUM-002"]
    assert n2["applicability_pins"]["global_numeric_tolerance_defined"] is False
    assert n2["applicability_pins"]["rounded_report_only_oracle_rejected"] is True

    n3 = by_id["ATB-NUM-003"]
    assert n3["applicability_pins"]["post_hoc_subject_selection_forbidden"] is True

    n4 = by_id["ATB-NUM-004"]
    assert n4["applicability_pins"]["NQ03R_used_as_methodological_exemplar_only"] is True
    assert n4["applicability_pins"]["TCD042_specific_polynomial_promoted_to_general_oracle"] is False
    assert n4["applicability_pins"]["TCD042_specific_threshold_promoted_to_general_policy"] is False

    a3 = by_id["ATB-ARCH-003"]
    assert a3["applicability_pins"]["historical_compiler_behaviour_can_define_ownership"] is False
    assert a3["applicability_pins"]["restart_state_inference_from_workspace_forbidden"] is True

    for key, value in frag["hard_boundaries"].items():
        assert value is False, f"hard boundary must remain false: {key}"

    assert status["gov05_adversarial_self_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
    for key, value in status["hard_boundaries"].items():
        assert value is False, f"status hard boundary must remain false: {key}"

    print("ANIMO-TB06A bounded numerical/compiler/runtime fragment validation: PASS")


if __name__ == "__main__":
    main()
