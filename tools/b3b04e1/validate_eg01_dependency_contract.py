#!/usr/bin/env python3
"""Validate the pinned ANIMO-EG01 dependency contract for B3B04E1.

This validator proves only that B3B04E1 has an explicit, internally consistent,
fail-closed dependency on the current EG01 custody interface. It does not prove
controlled B0 custody and cannot qualify TCD-040 evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EG01_HEAD = "a818b5a37b80ed92aded0b9c404990d356eb2300"
PENDING_DECISION = "QUALIFIED_B0_RETENTION_CONTRACT_IMPLEMENTATION_PENDING_EXTERNAL_CONTROLLED_STORAGE"
TERMINAL_DECISION = "QUALIFIED_CONTROLLED_IMMUTABLE_B0_RETENTION"
EXPECTED_PINS = {
    "integration/animo-eg/ANIMO-EG01_STATUS.json": "49798ff3d0a7bc85014b35239159c616dffbd888",
    "integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json": "a53bb0cc695aa2ba7c8b2096e86b4e4aacf13a1e",
    "integration/evidence/ANIMO_B0_STORAGE_PROOF_SCHEMA.json": "795ba2fc027e6ca918d152c2e449cd0aa03787fe",
    "tools/validate_b0_storage_proof.py": "c739ea62977e170f19e97b7fd1cd47c60c0a22d9",
    "docs/eg01/B0_CUSTODIAN_HANDOFF.md": "8961a45b674a666fad9415fa034fa375982d2b8a",
}
EXPECTED_B0 = {
    "ANIMO-B0-SRC-41553-R53": "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
    "ANIMO-B0-TB-202609": "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
    "ANIMO-B0-DOC-UG40-2005": "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON must be an object")
    return value


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.repo_root.resolve()
    failures: list[str] = []

    contract_path = root / "integration/animo-b3/b3b04e1/EG01_DEPENDENCY_CONTRACT.json"
    try:
        contract = load_json(contract_path)
        eg01 = load_json(root / "integration/animo-eg/ANIMO-EG01_STATUS.json")
        register = load_json(root / "integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "failures": [str(exc)]}, indent=2, sort_keys=True))
        return 2

    if contract.get("schema_version") != "1.0":
        failures.append("dependency contract schema_version must be 1.0")
    if contract.get("workunit") != "ANIMO-B3B04E1":
        failures.append("dependency contract workunit mismatch")
    if contract.get("target") != "TCD-040" or contract.get("scope") != "EVIDENCE_REPLAYABILITY_ONLY":
        failures.append("dependency contract target/scope mismatch")

    dependency = contract.get("dependency", {})
    expected_dependency = {
        "workunit": "ANIMO-EG01",
        "issue": 5,
        "current_authority_head": EG01_HEAD,
        "current_decision": PENDING_DECISION,
        "current_controlled_immutable_storage_proven": False,
        "required_terminal_decision": TERMINAL_DECISION,
        "required_terminal_controlled_immutable_storage_proven": True,
    }
    for key, value in expected_dependency.items():
        if dependency.get(key) != value:
            failures.append(f"dependency.{key} mismatch: {dependency.get(key)!r}")

    if eg01.get("decision") != PENDING_DECISION:
        failures.append(f"local EG01 decision drifted from pinned pending interface: {eg01.get('decision')!r}")
    if eg01.get("controlled_immutable_storage_proven") is not False:
        failures.append("local EG01 current controlled_immutable_storage_proven must remain false at this pin")

    pins = contract.get("interface_pins", {})
    pin_paths = {
        "eg01_status": "integration/animo-eg/ANIMO-EG01_STATUS.json",
        "b0_evidence_register": "integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json",
        "storage_proof_schema": "integration/evidence/ANIMO_B0_STORAGE_PROOF_SCHEMA.json",
        "semantic_proof_gate": "tools/validate_b0_storage_proof.py",
        "custodian_handoff": "docs/eg01/B0_CUSTODIAN_HANDOFF.md",
    }
    for key, rel in pin_paths.items():
        entry = pins.get(key, {})
        if entry.get("path") != rel:
            failures.append(f"interface_pins.{key}.path mismatch")
            continue
        expected = EXPECTED_PINS[rel]
        if entry.get("git_blob_sha") != expected:
            failures.append(f"interface_pins.{key}.git_blob_sha mismatch")
        path = root / rel
        if not path.is_file():
            failures.append(f"pinned interface file absent: {rel}")
        else:
            actual = git_blob_sha(path)
            if actual != expected:
                failures.append(f"pinned interface content drift: {rel}: {actual}")

    if contract.get("required_evidence_objects") != EXPECTED_B0:
        failures.append("required_evidence_objects do not equal the frozen B0 identities")

    register_map = {
        item.get("evidence_id"): item.get("sha256")
        for item in register.get("artifacts", [])
        if isinstance(item, dict) and item.get("evidence_class") == "B0_RAW_IMMUTABLE"
    }
    if register_map != EXPECTED_B0:
        failures.append("canonical B0 register identities differ from the dependency contract")

    rules = contract.get("fail_closed_rules", {})
    required_false = [
        "machine_proof_gate_alone_is_sufficient",
        "transient_hash_matching_bytes_are_controlled_custody_proof",
        "synthetic_proof_is_real_storage_evidence",
        "raw_b0_public_republication_authorized",
        "future_eg01_interface_drift_may_be_consumed_silently",
        "tcd040_may_be_admitted_by_this_dependency_contract",
        "second_line_reconsideration_may_start_before_full_b3b04e1_gate_pass",
    ]
    for key in required_false:
        if rules.get(key) is not False:
            failures.append(f"fail_closed_rules.{key} must be false")
    if rules.get("future_eg01_interface_drift_requires_explicit_reinspection_and_repin") is not True:
        failures.append("future EG01 interface drift must require explicit reinspection and repin")

    sequence = contract.get("resume_acceptance_sequence")
    if not isinstance(sequence, list) or len(sequence) != 7:
        failures.append("resume_acceptance_sequence must contain exactly seven ordered gates")
    if contract.get("current_state") != "BLOCKED_WAITING_FOR_EXTERNAL_CONTROLLED_B0_CUSTODY_PROOF":
        failures.append("current_state must remain blocked waiting for external custody proof")

    result = {
        "workunit": "ANIMO-B3B04E1",
        "dependency": "ANIMO-EG01",
        "status": "PASS_PINNED_EXTERNAL_DEPENDENCY_CONTRACT" if not failures else "FAIL_PINNED_EXTERNAL_DEPENDENCY_CONTRACT",
        "qualification_effect": "NONE_DEPENDENCY_CONTRACT_ONLY",
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
