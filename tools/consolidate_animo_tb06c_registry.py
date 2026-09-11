#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
TRANSFORM = ROOT / "integration/animo-testbank/fragments/ANIMO-TB06C_REGISTRY_TRANSFORM.json"
BASELINE_BLOB = "9b5078ea4c4f22f0215fead27a96580eeb613a9b"
TB06A_HEAD = "1ae7afbe540f3e5b53331137016db2936ff79cae"
TB06A_FRAGMENT = "integration/animo-testbank/fragments/ANIMO-TB06A_NUMERICAL_COMPILER_RUNTIME_FRAGMENT.json"
TB06B_HEAD = "7666c016e77d3743210b6f3135e53e9db87d75cc"
TB06B_HANDOFF = "integration/animo-testbank/fragments/ANIMO-TB06B_CONVERGENCE_HANDOFF.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_json(ref: str, path: str) -> dict:
    text = subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)
    return json.loads(text)


def find_array(text: str, key: str) -> tuple[int, int]:
    pos = text.index(f'"{key}"')
    start = text.index("[", pos)
    depth = 0
    quoted = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return start, i
    raise RuntimeError("unterminated test_registry array")


def append_entries(text: str, entries: list[dict]) -> str:
    start, end = find_array(text, "test_registry")
    body = text[start + 1:end]
    prefix = (body.rstrip() + ",\n") if body.strip() else "\n"
    blocks = []
    for entry in entries:
        rendered = json.dumps(entry, indent=2, ensure_ascii=False)
        blocks.append("\n".join("    " + line for line in rendered.splitlines()))
    return text[:start + 1] + prefix + ",\n".join(blocks) + "\n  " + text[end:]


def source_and_handoff() -> tuple[dict, dict]:
    fragment = git_json(TB06A_HEAD, TB06A_FRAGMENT)
    handoff = git_json(TB06B_HEAD, TB06B_HANDOFF)
    assert fragment["producer_workunit"] == "ANIMO-TB06A"
    assert handoff["work_unit"] == "ANIMO-TB06B"
    return fragment, handoff


def expected_entries() -> list[dict]:
    transform = json.loads(TRANSFORM.read_text(encoding="utf-8"))
    fragment, handoff = source_and_handoff()
    targets = transform["qualified_entry_ids"]
    assert targets == handoff["qualified_for_serial_consolidation"]
    assert set(transform["preserved_gap_ids"]) == set(handoff["preserve_without_promotion"])
    assert transform["serial_base_registry_blob"] == BASELINE_BLOB

    by_source_id = {e["test_id"]: e for e in fragment["entries"]}
    assert len(by_source_id) == len(fragment["entries"])
    out: list[dict] = []
    origin = f"ANIMO-TB06A@{TB06A_HEAD}:{TB06A_FRAGMENT}@blob:3ae41fd750dc6a3304d4a39eafd64fec983ad442"
    for test_id in targets:
        source = by_source_id[test_id]
        assert source["status"] == "QUALIFIED_FRAGMENT_ENTRY"
        meta = handoff["registry_metadata_normalization"][test_id]
        entry = copy.deepcopy(source)
        additions = {
            "title": transform["titles"][test_id],
            "level": meta["level"],
            "input_identity": transform["mechanical_transform"]["add_input_identity"],
            "dependencies": handoff["dependency_plan"][test_id],
            "cost_class": meta["cost_class"],
            "execution_profile": meta["execution_profile"],
            "subsystem": meta["subsystem"],
            "failure_class": meta["failure_class"],
            "qualification_strength": transform["mechanical_transform"]["add_qualification_strength"],
            "admission_effect": transform["mechanical_transform"]["add_admission_effect"],
            "registry_source_fragment": origin,
            "registry_consolidation": transform["mechanical_transform"]["add_registry_consolidation"],
        }
        overlap = set(entry) & set(additions)
        if overlap:
            raise AssertionError(f"would overwrite source fields for {test_id}: {sorted(overlap)}")
        entry.update(additions)
        out.append(entry)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    transform = json.loads(TRANSFORM.read_text(encoding="utf-8"))
    targets = transform["qualified_entry_ids"]
    gaps = set(transform["preserved_gap_ids"])
    expected = expected_entries()
    assert [e["test_id"] for e in expected] == targets
    assert len(targets) == len(set(targets)) == 4
    assert set(targets).isdisjoint(gaps)

    raw = REGISTRY.read_bytes()
    registry = json.loads(raw)
    existing_ids = [e["test_id"] for e in registry["test_registry"]]
    assert len(existing_ids) == len(set(existing_ids)), "duplicate central registry IDs"
    existing = set(existing_ids)
    assert not (existing & gaps), f"GAP IDs present in registry: {sorted(existing & gaps)}"
    present = [x for x in targets if x in existing]
    if present and len(present) != len(targets):
        raise AssertionError(f"partial TB06C consolidation: {present}")

    if not present:
        actual = git_blob_sha(raw)
        assert actual == BASELINE_BLOB, f"serial base registry drift: {actual}"
        # This is the explicit rebase check: TB06B was qualified against TB05C,
        # while TB06C writes on the newer TB05D serial registry. No target/GAP
        # collision is allowed and all declared dependencies must already close
        # in the union of the current registry plus these four entries.
        closure = existing | set(targets)
        for entry in expected:
            missing = set(entry["dependencies"]) - closure
            assert not missing, f"unclosed dependency for {entry['test_id']}: {sorted(missing)}"
            assert not (set(entry["dependencies"]) & gaps)
        if not args.write:
            return 2
        updated = append_entries(raw.decode("utf-8"), expected)
        parsed = json.loads(updated)
        by_id = {e["test_id"]: e for e in parsed["test_registry"]}
        assert len(by_id) == len(parsed["test_registry"])
        for entry in expected:
            assert by_id[entry["test_id"]] == entry
        assert not (set(by_id) & gaps)
        REGISTRY.write_text(updated, encoding="utf-8")
        print("ANIMO-TB06C central registry materialized")
        return 0

    by_id = {e["test_id"]: e for e in registry["test_registry"]}
    for entry in expected:
        assert by_id[entry["test_id"]] == entry
    print("ANIMO-TB06C central registry already exact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
