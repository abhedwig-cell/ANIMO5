#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
FRAGMENT = ROOT / "integration/animo-testbank/fragments/ANIMO-TB06A_NUMERICAL_COMPILER_RUNTIME_FRAGMENT.json"
HANDOFF = ROOT / "integration/animo-testbank/fragments/ANIMO-TB06B_CONVERGENCE_HANDOFF.json"
TB06A_STATUS = ROOT / "integration/animo-testbank/ANIMO-TB06A_STATUS.json"
STATUS = ROOT / "integration/animo-testbank/ANIMO-TB06B_STATUS.json"


def load(p):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    reg = load(REGISTRY)
    frag = load(FRAGMENT)
    handoff = load(HANDOFF)
    tb06a = load(TB06A_STATUS)
    status = load(STATUS)

    assert tb06a["state"] == "QUALIFIED_TB06A_BOUNDED_NUMERICAL_COMPILER_RUNTIME_FRAGMENT_PACKAGE"
    assert handoff["base_registry_authority"] == "ANIMO-TB05C@788247b4346bedbb79749d5ce5daef3f99283f8d"
    assert handoff["registry_write"] == "FORBIDDEN_IN_TB06B"

    central = {e["test_id"] for e in reg["test_registry"]}
    entries = frag["entries"]
    ids = [e["test_id"] for e in entries]
    assert len(ids) == len(set(ids))
    assert not (set(ids) & central), f"TB06A fragment collides with central registry: {set(ids) & central}"

    qualified = set(handoff["qualified_for_serial_consolidation"])
    gaps = set(handoff["preserve_without_promotion"])
    assert qualified == {"ATB-NUM-002", "ATB-NUM-003", "ATB-NUM-004", "ATB-ARCH-003"}
    assert gaps == {"ATB-NUM-005", "ATB-ARCH-004"}

    by_id = {e["test_id"]: e for e in entries}
    for tid in qualified:
        assert by_id[tid]["status"] == "QUALIFIED_FRAGMENT_ENTRY"
    for tid in gaps:
        assert by_id[tid]["status"] == "GAP"
        assert by_id[tid]["expected_value_provenance"] == "UNKNOWN"

    available = central | qualified
    for tid, deps in handoff["dependency_plan"].items():
        assert tid in qualified
        for dep in deps:
            assert dep in available, f"unresolved dependency {tid} -> {dep}"

    norm = handoff["normalization_semantics"]
    assert norm["scientific_claim_redefinition"] is False
    assert norm["source_identity_redefinition"] is False
    assert norm["expected_value_provenance_redefinition"] is False
    assert norm["comparison_policy_redefinition"] is False
    assert norm["TCD_specific_constants_promoted"] is False
    assert norm["global_tolerance_created"] is False

    assert status["gov05_adversarial_self_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
    for obj in (handoff["hard_boundaries"], status["hard_boundaries"]):
        for key, value in obj.items():
            assert value is False, f"hard boundary must remain false: {key}"

    print("ANIMO-TB06B TB6 fragment convergence readiness validation: PASS")


if __name__ == "__main__":
    main()
