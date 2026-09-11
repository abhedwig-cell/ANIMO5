#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from consolidate_animo_tb05d_registry import expected_entries, load_source_entries

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
HANDOFF = ROOT / "integration/animo-testbank/fragments/ANIMO-TB05C_CONVERGENCE_HANDOFF.json"
TRANSFORM = ROOT / "integration/animo-testbank/fragments/ANIMO-TB05D_REGISTRY_TRANSFORM.json"
SOURCE_PINS = ROOT / "integration/animo-testbank/ANIMO-TB05D_SOURCE_PINS.json"
STATUS = ROOT / "integration/animo-testbank/ANIMO-TB05D_STATUS.json"
AUDITS = ROOT / "integration/animo-testbank/ANIMO-TB05D_AUDITS.json"
DIFF = ROOT / "integration/animo-testbank/ANIMO-TB05D_REGISTRY_DIFF.json"
BASE_HEAD = "788247b4346bedbb79749d5ce5daef3f99283f8d"
BASE_REGISTRY_BLOB = "4c78cdb542c5ff4ce898c033eb99dd7b2daa7c2c"
ADDED_KEYS = {
    "title", "level", "input_identity", "dependencies", "cost_class",
    "execution_profile", "subsystem", "failure_class", "qualification_strength",
    "admission_effect", "registry_source_fragment", "registry_consolidation",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_json(ref: str, path: str) -> dict:
    text = subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)
    return json.loads(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["materialization", "final"], default="materialization")
    args = parser.parse_args()

    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    transform = json.loads(TRANSFORM.read_text(encoding="utf-8"))
    source_pins = json.loads(SOURCE_PINS.read_text(encoding="utf-8"))
    assert transform["base_authority"] == f"ANIMO-TB05C@{BASE_HEAD}"
    assert transform["base_registry_blob"] == BASE_REGISTRY_BLOB
    assert source_pins["serial_base"]["authority"] == f"ANIMO-TB05C@{BASE_HEAD}"
    assert source_pins["serial_base"]["central_registry_blob"] == BASE_REGISTRY_BLOB
    assert source_pins["serial_base"]["exact_head_ci_conclusion"] == "success"

    targets = transform["qualified_entry_ids"]
    gaps = set(transform["preserved_gap_ids"])
    assert targets == handoff["qualified_for_serial_consolidation"]
    assert set(source_pins["qualified_ids"]) == set(targets)
    assert set(source_pins["preserved_gaps"]) == gaps
    assert set(handoff["preserve_without_promotion"]) == gaps
    assert len(targets) == len(set(targets)) == 12

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ids = [e["test_id"] for e in registry["test_registry"]]
    assert len(ids) == len(set(ids)), "duplicate central registry IDs"
    by_id = {e["test_id"]: e for e in registry["test_registry"]}
    missing = set(targets) - set(by_id)
    assert not missing, f"missing consolidated IDs: {sorted(missing)}"
    assert not (gaps & set(by_id)), f"GAP entries were promoted: {sorted(gaps & set(by_id))}"

    expected = expected_entries()
    expected_by_id = {e["test_id"]: e for e in expected}
    assert list(expected_by_id) == targets
    for test_id in targets:
        assert by_id[test_id] == expected_by_id[test_id], f"registry entry drift for {test_id}"
        assert by_id[test_id]["admission_effect"] == "NONE"
        assert by_id[test_id]["registry_consolidation"] == "ANIMO-TB05D"

    # Prove append-only behaviour at parsed-registry level.
    baseline = git_json(BASE_HEAD, "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json")
    reduced = dict(registry)
    reduced["test_registry"] = [e for e in registry["test_registry"] if e["test_id"] not in set(targets)]
    assert reduced == baseline, "central registry changed outside the twelve qualified additions"
    assert git_blob_sha(subprocess.check_output(["git", "show", f"{BASE_HEAD}:integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"], cwd=ROOT)) == BASE_REGISTRY_BLOB

    # Prove source-entry fields survive the transform without overwrite.
    source_entries, _origins = load_source_entries(handoff)
    for test_id in targets:
        source = source_entries[test_id]
        registered = by_id[test_id]
        stripped = {k: v for k, v in registered.items() if k not in ADDED_KEYS}
        assert stripped == source, f"source scientific fields changed during consolidation for {test_id}"
        assert registered["source_identity"] == source["source_identity"]
        assert registered["expected_value_provenance"] == source["expected_value_provenance"]
        assert registered["comparison_policy"] == source["comparison_policy"]
        assert registered["applicability_pins"] == source["applicability_pins"]
        assert registered["failure_semantics"] == source["failure_semantics"]
        assert registered["permanence"] == source["permanence"]

    closure = set(by_id)
    for test_id in targets:
        deps = by_id[test_id]["dependencies"]
        assert set(deps) <= closure, f"dependency closure broken for {test_id}"
        assert not (set(deps) & gaps), f"{test_id} depends on GAP entry"
        assert deps == handoff["dependency_plan"][test_id]

    # Explicit non-promotion boundaries.
    assert by_id["ATB-STATE-004"]["applicability_pins"]["whole_model_state_claim"] is False
    assert by_id["ATB-STATE-006"]["applicability_pins"]["whole_model_active_split"] is False
    assert by_id["ATB-BND-002"]["applicability_pins"]["finite_positive_subthreshold_included"] is False
    assert by_id["ATB-BND-005"]["applicability_pins"]["production_patch_admitted"] is False
    assert by_id["ATB-SUB-004"]["applicability_pins"]["historical_B2"] is False
    assert by_id["ATB-SUB-004"]["applicability_pins"]["behavioural_golden_reference"] is False
    assert by_id["ATB-SUB-005"]["applicability_pins"]["whole_model_active_split"] is False
    assert by_id["ATB-SUB-008"]["applicability_pins"]["b3_admitted"] is False
    assert by_id["ATB-SUB-008"]["applicability_pins"]["production_ready"] is False
    assert by_id["ATB-SUB-009"]["applicability_pins"]["scientific_admission"] is False
    assert by_id["ATB-SUB-010"]["applicability_pins"]["production_patch_admitted"] is False

    if args.phase == "final":
        assert STATUS.exists() and AUDITS.exists() and DIFF.exists(), "final TB05D evidence package incomplete"
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        audits = json.loads(AUDITS.read_text(encoding="utf-8"))
        diff = json.loads(DIFF.read_text(encoding="utf-8"))
        assert status["work_unit"] == "ANIMO-TB05D"
        assert status["state"] == "QUALIFIED_ANIMO_TB05D_SERIAL_REGISTRY_CONSOLIDATION"
        assert status["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert status["qualified_entries"] == targets
        assert set(status["preserved_gaps"]) == gaps
        assert status["work_status"] == {"realized": True, "persisted": True, "tested": True, "qualified": True, "complete": True}
        assert audits["gov05_adversarial_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert audits["overall_result"] == "PASS"
        assert diff["added_test_ids"] == targets
        assert diff["removed_test_ids"] == []
        assert diff["modified_preexisting_test_ids"] == []
        assert diff["base_registry_blob"] == BASE_REGISTRY_BLOB
        assert diff["result_registry_blob"] == git_blob_sha(REGISTRY.read_bytes())

    print("QUALIFIED_ANIMO_TB05D_SERIAL_REGISTRY_CONSOLIDATION" if args.phase == "final" else "ANIMO-TB05D materialization validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
