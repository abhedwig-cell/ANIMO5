#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
ADDITIONS_PATH = "integration/animo-testbank/fragments/ANIMO-TB03D_REGISTRY_ADDITIONS.json"
PINS_PATH = "integration/animo-testbank/ANIMO-TB03D_SOURCE_PINS.json"
AUDITS_PATH = "integration/animo-testbank/ANIMO-TB03D_AUDITS.json"
STATUS_PATH = "integration/animo-testbank/ANIMO-TB03D_STATUS.json"
DIFF_PATH = "integration/animo-testbank/ANIMO-TB03D_REGISTRY_DIFF.json"

BASE = "a989541c265213bde0bae3f0e2db28fcaf9c0579"
BASELINE_REGISTRY_BLOB = "a5f279cfa334dc63d3e4e8759370279736d874a0"
TB01 = "15a17bfa2c321d08f3ac89f334986c0ae8429045"
TB02 = "54a565c2f7f2a29817ae027cc18bee1613ce568d"
TB03A = "a37f07b15ae50d6fbb526cef3215fb58702e85aa"
TB03B = "48a3036501e9e871608ab920f46dde5570ebf369"
TB03C = BASE
TB04A = "ad9683716e1a41a6f6b3d32ff1012bfa215c27db"
TB04B = "82213ad143bd5f0fa5c500303a8a4f1d35dd3f0c"
TB05A = "e3d537935104b4a7253a5287f8fbf7df7e7459e2"

A_PATH = "integration/animo-testbank/fragments/ANIMO-TB03A_CNP_SPECIES_ORACLE_FRAGMENT.json"
B_PATH = "integration/animo-testbank/fragments/ANIMO-TB03B_FRAGMENT.json"
C_PATH = "integration/animo-testbank/fragments/ANIMO-TB03C_CONVERGENCE_HANDOFF.json"
B_DOC = "docs/testbank/ANIMO-TB03B_TRANSACTION_CONSERVATION_ADOPTION.md"
TB04A_PATH = "integration/animo-testbank/fragments/ANIMO-TB04A_STATE_RESTART_FRAGMENT.json"
TB04B_PATH = "integration/animo-testbank/fragments/ANIMO-TB04B_BOUNDARY_INITIALIZATION_FRAGMENT.json"
TB05A_PATH = "integration/animo-testbank/fragments/ANIMO-TB05A_MACROPORE_SUBSYSTEM_FRAGMENT.json"

A_BLOB = "aa11d224964bdc5f1d529d823f774afc18994bbd"
B_BLOB = "4b1f1a0ef11a02a76dbb33f9168dbb1f552ade7e"
C_BLOB = "03de5deece36a28ad1610420d6756425b09711fe"
B_DOC_BLOB = "ccebee70007680d061ff7e4dffd320fce87fe5a7"

TARGET_IDS = [
    "ATB-ORACLE-002",
    "ATB-ORACLE-003",
    "ATB-SPC-003",
    "ATB-TRN-002",
    "ATB-CONS-002",
    "ATB-CONS-003",
    "ATB-CONS-004",
    "ATB-CONS-005",
]
A_QUALIFIED = {"ATB-ORACLE-002", "ATB-ORACLE-003", "ATB-SPC-003"}
B_QUALIFIED = {"ATB-TRN-002", "ATB-CONS-002", "ATB-CONS-003", "ATB-CONS-004", "ATB-CONS-005"}
NONQUALIFIED = {
    "ATB-SPC-004": "CANDIDATE",
    "ATB-SPC-005": "CANDIDATE",
    "ATB-SPC-006": "CANDIDATE",
    "ATB-SPC-007": "GAP",
}


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git_show(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)


def git_json(ref: str, path: str) -> dict:
    return json.loads(git_show(ref, path))


def git_blob(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{ref}:{path}"], cwd=ROOT, text=True).strip()


def local_blob(path: str) -> str:
    data = (ROOT / path).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def index(entries: list[dict]) -> dict[str, dict]:
    ids = [e["test_id"] for e in entries]
    assert len(ids) == len(set(ids)), "duplicate central registry ID"
    return {e["test_id"]: e for e in entries}


def assert_source_fields_preserved(source: dict, central: dict) -> None:
    for key, value in source.items():
        assert key in central, f"{central.get('test_id')} dropped source field {key}"
        assert central[key] == value, f"{central.get('test_id')} provenance/scientific drift in {key}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["materialization", "final"], default="final")
    args = parser.parse_args()

    registry = load(REGISTRY_PATH)
    additions = load(ADDITIONS_PATH)
    pins = load(PINS_PATH)
    current_entries = registry["test_registry"]
    current = index(current_entries)

    base_registry = git_json(BASE, REGISTRY_PATH)
    base = index(base_registry["test_registry"])
    assert git_blob(BASE, REGISTRY_PATH) == BASELINE_REGISTRY_BLOB
    assert git_blob(TB01, REGISTRY_PATH) == BASELINE_REGISTRY_BLOB

    # No central metadata or pre-existing registry entry may change.
    assert set(registry) == set(base_registry), "top-level registry schema changed"
    for key in registry:
        if key != "test_registry":
            assert registry[key] == base_registry[key], f"central registry metadata changed: {key}"
    assert set(current) == set(base) | set(TARGET_IDS), "registry diff is not exactly eight qualified TB3 IDs"
    for test_id, entry in base.items():
        assert current[test_id] == entry, f"pre-existing registry entry changed: {test_id}"

    payload_entries = additions["entries"]
    payload_ids = [e["test_id"] for e in payload_entries]
    assert payload_ids == TARGET_IDS
    assert additions["baseline_registry_blob"] == BASELINE_REGISTRY_BLOB
    assert additions["hard_boundaries"]["new_scientific_test_ids_created"] is False
    for entry in payload_entries:
        assert current[entry["test_id"]] == entry, f"central entry differs from serial payload: {entry['test_id']}"
        assert entry["admission_effect"] == "NONE"

    # Exact sibling source-fragment identities and source-field preservation.
    assert git_blob(TB03A, A_PATH) == A_BLOB
    assert git_blob(TB03B, B_PATH) == B_BLOB
    assert git_blob(TB03C, C_PATH) == C_BLOB
    assert git_blob(TB03B, B_DOC) == B_DOC_BLOB
    a_doc = git_json(TB03A, A_PATH)
    b_doc = git_json(TB03B, B_PATH)
    c_doc = git_json(TB03C, C_PATH)
    a = {e["test_id"]: e for e in a_doc["entries"]}
    b = {e["test_id"]: e for e in b_doc["entries"]}
    assert A_QUALIFIED == set(c_doc["source_fragments"][0]["qualified_entry_ids"])
    assert B_QUALIFIED == set(c_doc["source_fragments"][1]["qualified_entry_ids"])
    assert set(c_doc["convergence_result"]["qualified_handoff_entry_ids"]) == set(TARGET_IDS)
    assert c_doc["convergence_result"]["inter_fragment_id_collision"] is False
    assert c_doc["convergence_result"]["central_registry_id_collision"] is False
    assert c_doc["convergence_result"]["central_registry_ready_for_separate_serial_consolidation"] is True

    for test_id in A_QUALIFIED:
        assert_source_fields_preserved(a[test_id], current[test_id])
    for test_id in B_QUALIFIED:
        assert_source_fields_preserved(b[test_id], current[test_id])
        assert current[test_id]["permanence_decision"] == "PERMANENT_REUSABLE_CROSS_CASE_CONTRACT"
        assert current[test_id]["permanence_source"].startswith(B_DOC + "@blob:" + B_DOC_BLOB)
        assert "TB03B did not encode central" in current[test_id]["registry_metadata_normalization"]

    # Candidate/GAP preservation. Conservation aggregation cannot promote SPC-004.
    for test_id, expected_status in NONQUALIFIED.items():
        assert a[test_id]["status"] == expected_status
        assert test_id not in current
    assert current["ATB-CONS-004"]["species"] == "NH4-N and NO3-N separate"
    assert "species-resolved" in current["ATB-CONS-004"]["residual_equation"]

    # Dependency closure against unchanged baseline + exactly the eight additions.
    all_ids = set(current)
    for test_id in TARGET_IDS:
        for dep in current[test_id].get("dependencies", []):
            assert dep in all_ids, f"unresolved dependency {test_id} -> {dep}"
    assert current["ATB-TRN-002"]["dependencies"] == ["ATB-TRN-001"]
    assert current["ATB-CONS-002"]["dependencies"] == ["ATB-TRN-002", "ATB-CONS-001"]
    assert current["ATB-CONS-004"]["dependencies"] == ["ATB-SPC-001", "ATB-TRN-002"]

    # Central architecture authorities stay byte-identical.
    assert local_blob("integration/animo-testbank/ANIMO_TESTBANK_COVERAGE_MATRIX.json") == "0cd42a372e78af509ce600862ac04a688e5173c6"
    assert local_blob("integration/animo-testbank/ANIMO_TESTBANK_EXPECTATION_PROVENANCE.json") == "6d9722c5e04e28cbb97ce21fcd3140a1ff671c02"
    assert local_blob("integration/animo-testbank/ANIMO_TESTBANK_EXECUTION_PROFILES.json") == "5645035d56c43d3b3a231a0ecc40af4c3d3f38a5"
    provenance = load("integration/animo-testbank/ANIMO_TESTBANK_EXPECTATION_PROVENANCE.json")
    assert provenance["governance_rules"]["synthetic_oracle_may_be_counted_as_historical_B2"] is False
    assert provenance["synthetic_oracle_policy"]["may_be_relabelled_historical_B2"] is False
    assert current["ATB-ORACLE-002"]["expected_value_provenance"] == "QUALIFIED_SYNTHETIC_ORACLE"
    assert current["ATB-ORACLE-003"]["expected_value_provenance"] == "QUALIFIED_SYNTHETIC_ORACLE"

    # Newer fragment IDs are disjoint and their branches had not serially written the central registry.
    newer = [
        (TB04A, TB04A_PATH, {"ATB-STATE-003", "ATB-STATE-004", "ATB-STATE-005", "ATB-STATE-006", "ATB-STATE-007"}),
        (TB04B, TB04B_PATH, {"ATB-BND-002", "ATB-BND-003", "ATB-BND-004", "ATB-BND-005", "ATB-BND-006"}),
        (TB05A, TB05A_PATH, {"ATB-SUB-003", "ATB-SUB-004", "ATB-SUB-005", "ATB-SUB-006", "ATB-SUB-007"}),
    ]
    for ref, path, expected_ids in newer:
        doc = git_json(ref, path)
        ids = {e["test_id"] for e in doc["entries"]}
        assert ids == expected_ids
        assert not (ids & set(TARGET_IDS))
        assert git_blob(ref, REGISTRY_PATH) == BASELINE_REGISTRY_BLOB

    # Pin file must match live-authority facts used by this workunit.
    assert pins["live_check"]["tb02"]["head"] == TB02
    assert pins["live_check"]["tb03a"]["fragment_blob"] == A_BLOB
    assert pins["live_check"]["tb03b"]["fragment_blob"] == B_BLOB
    assert pins["live_check"]["tb03c"]["handoff_blob"] == C_BLOB
    assert pins["live_check_conclusions"]["post_tb03c_central_registry_write_detected"] is False

    # Scope barriers: local/profile contracts stay bounded; testbank registration is not admission.
    assert current["ATB-CONS-003"]["qualification_strength"] == "PROFILE_CONSERVATION_CONTRACT_ONLY_NO_WHOLE_MODEL_C_CLAIM"
    assert all(current[test_id]["admission_effect"] == "NONE" for test_id in TARGET_IDS)
    registry_text = (ROOT / REGISTRY_PATH).read_text(encoding="utf-8")
    added_text = json.dumps([current[x] for x in TARGET_IDS])
    assert "HISTORICAL_B2" not in added_text
    assert "QUALIFIED_GOLDEN_CASE" not in added_text
    assert "whole-model golden" not in added_text.lower()

    if args.phase == "final":
        audits = load(AUDITS_PATH)
        status = load(STATUS_PATH)
        diff = load(DIFF_PATH)
        assert audits["phase"] == "FINAL"
        for name in ["collision_audit", "dependency_closure_audit", "provenance_preservation_audit", "candidate_gap_preservation_audit", "scope_semantics_audit"]:
            assert audits[name]["result"] == "PASS"
        assert audits["gov05_adversarial_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert audits["gov05_adversarial_review"]["result"] == "PASS"
        assert status["state"] == "QUALIFIED_ANIMO_TB03D_SERIAL_REGISTRY_CONSOLIDATION"
        assert status["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert status["hard_boundaries"]["tcd_admission_performed"] is False
        assert status["hard_boundaries"]["whole_model_golden_baseline_created"] is False
        assert status["hard_boundaries"]["tb04_modified"] is False
        assert status["qualification"]["exact_final_head_ci_required"] is True
        assert diff["baseline_registry_blob"] == BASELINE_REGISTRY_BLOB
        assert diff["added_test_ids"] == TARGET_IDS
        assert diff["removed_test_ids"] == []
        assert diff["modified_preexisting_test_ids"] == []
        assert diff["changed_top_level_registry_metadata"] == []
        assert diff["final_registry_blob"] == local_blob(REGISTRY_PATH)

    print(f"ANIMO-TB03D serial registry validation ({args.phase}): PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
