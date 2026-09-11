#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from consolidate_animo_tb06c_registry import expected_entries, source_and_handoff

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
TRANSFORM = ROOT / "integration/animo-testbank/fragments/ANIMO-TB06C_REGISTRY_TRANSFORM.json"
SOURCE_PINS = ROOT / "integration/animo-testbank/ANIMO-TB06C_SOURCE_PINS.json"
STATUS = ROOT / "integration/animo-testbank/ANIMO-TB06C_STATUS.json"
AUDITS = ROOT / "integration/animo-testbank/ANIMO-TB06C_AUDITS.json"
DIFF = ROOT / "integration/animo-testbank/ANIMO-TB06C_REGISTRY_DIFF.json"
BASE_HEAD = "e0d96fc279ef35966a0d5dd37462fa0cded2cc1e"
BASE_BLOB = "9b5078ea4c4f22f0215fead27a96580eeb613a9b"
TB06B_HEAD = "7666c016e77d3743210b6f3135e53e9db87d75cc"
TB06A_HEAD = "1ae7afbe540f3e5b53331137016db2936ff79cae"
TB05D_IDS = {
    "ATB-STATE-003", "ATB-STATE-004", "ATB-STATE-005", "ATB-STATE-006",
    "ATB-BND-002", "ATB-BND-005", "ATB-SUB-003", "ATB-SUB-004",
    "ATB-SUB-005", "ATB-SUB-008", "ATB-SUB-009", "ATB-SUB-010",
}
ADDED_KEYS = {
    "title", "level", "input_identity", "dependencies", "cost_class",
    "execution_profile", "subsystem", "failure_class", "qualification_strength",
    "admission_effect", "registry_source_fragment", "registry_consolidation",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_bytes(ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT)


def git_json(ref: str, path: str) -> dict:
    return json.loads(git_bytes(ref, path).decode("utf-8"))


def git_blob_at(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{ref}:{path}"], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["materialization", "final"], default="materialization")
    args = parser.parse_args()

    transform = json.loads(TRANSFORM.read_text(encoding="utf-8"))
    pins = json.loads(SOURCE_PINS.read_text(encoding="utf-8"))
    assert transform["serial_base_authority"] == f"ANIMO-TB05D@{BASE_HEAD}"
    assert transform["serial_base_registry_blob"] == BASE_BLOB
    assert transform["convergence_authority"] == f"ANIMO-TB06B@{TB06B_HEAD}"
    assert pins["serial_base"]["authority"] == f"ANIMO-TB05D@{BASE_HEAD}"
    assert pins["serial_base"]["exact_head_ci_conclusion"] == "success"
    assert pins["convergence"]["authority"] == f"ANIMO-TB06B@{TB06B_HEAD}"
    assert pins["convergence"]["exact_head_ci_conclusion"] == "success"
    assert pins["source_fragment"]["head"] == TB06A_HEAD
    assert pins["source_fragment"]["ci_conclusion"] == "success"
    assert git_blob_at(TB06A_HEAD, pins["source_fragment"]["fragment_path"]) == pins["source_fragment"]["fragment_blob"]
    assert git_blob_at(TB06A_HEAD, pins["source_fragment"]["status_path"]) == pins["source_fragment"]["status_blob"]
    assert git_blob_at(TB06B_HEAD, pins["convergence"]["handoff_path"]) == pins["convergence"]["handoff_blob"]

    targets = transform["qualified_entry_ids"]
    gaps = set(transform["preserved_gap_ids"])
    assert len(targets) == len(set(targets)) == 4
    assert set(targets).isdisjoint(gaps)
    source_fragment, handoff = source_and_handoff()
    assert handoff["qualified_for_serial_consolidation"] == targets
    assert set(handoff["preserve_without_promotion"]) == gaps
    assert handoff["normalization_semantics"]["global_tolerance_created"] is False
    assert handoff["normalization_semantics"]["TCD_specific_constants_promoted"] is False

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ids = [e["test_id"] for e in registry["test_registry"]]
    assert len(ids) == len(set(ids)), "duplicate registry IDs"
    by_id = {e["test_id"]: e for e in registry["test_registry"]}
    assert TB05D_IDS <= set(by_id), "TB05D serial base entries missing"
    assert not (gaps & set(by_id)), f"GAP entries promoted: {sorted(gaps & set(by_id))}"
    missing = set(targets) - set(by_id)
    assert not missing, f"missing TB06C entries: {sorted(missing)}"

    expected = expected_entries()
    expected_by_id = {e["test_id"]: e for e in expected}
    assert list(expected_by_id) == targets
    source_by_id = {e["test_id"]: e for e in source_fragment["entries"]}
    for test_id in targets:
        registered = by_id[test_id]
        assert registered == expected_by_id[test_id], f"registered entry drift: {test_id}"
        stripped = {k: v for k, v in registered.items() if k not in ADDED_KEYS}
        assert stripped == source_by_id[test_id], f"source fields changed: {test_id}"
        assert registered["admission_effect"] == "NONE"
        assert registered["registry_consolidation"] == "ANIMO-TB06C"
        deps = registered["dependencies"]
        assert deps == handoff["dependency_plan"][test_id]
        assert set(deps) <= set(by_id), f"unclosed dependency for {test_id}"
        assert not (set(deps) & gaps)

    # The serial writer rebases a TB06B convergence decision originally made on
    # TB05C onto the newer TB05D registry. Prove that this rebase is registry-only:
    # TB05D additions exist, and none collides with TB06 target/GAP IDs.
    assert TB05D_IDS.isdisjoint(set(targets) | gaps)
    baseline = git_json(BASE_HEAD, "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json")
    reduced = dict(registry)
    reduced["test_registry"] = [e for e in registry["test_registry"] if e["test_id"] not in set(targets)]
    assert reduced == baseline, "registry changed beyond four TB06C additions"
    assert git_blob_sha(git_bytes(BASE_HEAD, "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json")) == BASE_BLOB

    # High-risk non-promotion guards copied from source applicability.
    assert by_id["ATB-NUM-002"]["applicability_pins"]["global_numeric_tolerance_defined"] is False
    assert by_id["ATB-NUM-002"]["applicability_pins"]["scientific_difference_auto_accepted"] is False
    assert by_id["ATB-NUM-004"]["applicability_pins"]["TCD042_specific_polynomial_promoted_to_general_oracle"] is False
    assert by_id["ATB-NUM-004"]["applicability_pins"]["TCD042_specific_threshold_promoted_to_general_policy"] is False
    assert by_id["ATB-ARCH-003"]["applicability_pins"]["historical_compiler_behaviour_can_define_ownership"] is False
    assert by_id["ATB-ARCH-003"]["applicability_pins"]["restart_state_inference_from_workspace_forbidden"] is True
    assert by_id["ATB-ARCH-003"]["applicability_pins"]["TCD037_accounting_mapping_promoted_here"] is False

    if args.phase == "final":
        assert STATUS.exists() and AUDITS.exists() and DIFF.exists(), "final evidence package incomplete"
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        audits = json.loads(AUDITS.read_text(encoding="utf-8"))
        diff = json.loads(DIFF.read_text(encoding="utf-8"))
        assert status["state"] == "QUALIFIED_ANIMO_TB06C_SERIAL_REGISTRY_CONSOLIDATION"
        assert status["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert status["qualified_entries"] == targets
        assert set(status["preserved_gaps"]) == gaps
        assert status["work_status"] == {"realized": True, "persisted": True, "tested": True, "qualified": True, "complete": True}
        assert audits["overall_result"] == "PASS"
        assert audits["gov05_adversarial_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert diff["added_test_ids"] == targets
        assert diff["removed_test_ids"] == []
        assert diff["modified_preexisting_test_ids"] == []
        assert diff["base_registry_blob"] == BASE_BLOB
        assert diff["result_registry_blob"] == git_blob_sha(REGISTRY.read_bytes())

    print("QUALIFIED_ANIMO_TB06C_SERIAL_REGISTRY_CONSOLIDATION" if args.phase == "final" else "ANIMO-TB06C materialization validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
