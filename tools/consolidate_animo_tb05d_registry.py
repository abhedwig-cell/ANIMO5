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
HANDOFF = ROOT / "integration/animo-testbank/fragments/ANIMO-TB05C_CONVERGENCE_HANDOFF.json"
TRANSFORM = ROOT / "integration/animo-testbank/fragments/ANIMO-TB05D_REGISTRY_TRANSFORM.json"
BASELINE_BLOB = "4c78cdb542c5ff4ce898c033eb99dd7b2daa7c2c"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_text(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)


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
    rendered_blocks = []
    for entry in entries:
        rendered = json.dumps(entry, indent=2, ensure_ascii=False)
        rendered_blocks.append("\n".join("    " + line for line in rendered.splitlines()))
    return text[:start + 1] + prefix + ",\n".join(rendered_blocks) + "\n  " + text[end:]


def load_source_entries(handoff: dict) -> tuple[dict[str, dict], dict[str, str]]:
    entries: dict[str, dict] = {}
    origins: dict[str, str] = {}
    for work_unit, pin in handoff["fragment_pins"].items():
        fragment = json.loads(git_text(pin["head"], pin["fragment_path"]))
        for entry in fragment["entries"]:
            test_id = entry["test_id"]
            if test_id in entries:
                raise AssertionError(f"duplicate source test ID: {test_id}")
            entries[test_id] = entry
            origins[test_id] = (
                f"{work_unit}@{pin['head']}:{pin['fragment_path']}@blob:{pin['fragment_blob']}"
            )
    return entries, origins


def expected_entries() -> list[dict]:
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    transform = json.loads(TRANSFORM.read_text(encoding="utf-8"))
    target_ids = transform["qualified_entry_ids"]
    assert target_ids == handoff["qualified_for_serial_consolidation"]
    assert set(transform["preserved_gap_ids"]) == set(handoff["preserve_without_promotion"])
    assert transform["base_registry_blob"] == BASELINE_BLOB
    assert transform["base_authority"] == "ANIMO-TB05C@788247b4346bedbb79749d5ce5daef3f99283f8d"

    source_entries, origins = load_source_entries(handoff)
    out: list[dict] = []
    for test_id in target_ids:
        source = source_entries[test_id]
        assert source["status"] == "QUALIFIED_FRAGMENT_ENTRY"
        entry = copy.deepcopy(source)
        meta = handoff["registry_metadata_normalization"][test_id]
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
            "registry_source_fragment": origins[test_id],
            "registry_consolidation": transform["mechanical_transform"]["add_registry_consolidation"],
        }
        overlap = set(entry) & set(additions)
        if overlap:
            raise AssertionError(f"mechanical transform would overwrite source fields for {test_id}: {sorted(overlap)}")
        entry.update(additions)
        out.append(entry)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    transform = json.loads(TRANSFORM.read_text(encoding="utf-8"))
    targets = transform["qualified_entry_ids"]
    gaps = set(transform["preserved_gap_ids"])
    expected = expected_entries()
    assert [e["test_id"] for e in expected] == targets
    assert len(targets) == len(set(targets)) == 12
    assert gaps == set(handoff["preserve_without_promotion"])

    raw = REGISTRY.read_bytes()
    registry = json.loads(raw)
    existing_ids = [e["test_id"] for e in registry["test_registry"]]
    assert len(existing_ids) == len(set(existing_ids)), "central registry contains duplicate test IDs"
    existing = set(existing_ids)
    assert not (existing & gaps), f"GAP IDs must remain outside central registry: {sorted(existing & gaps)}"
    present = [x for x in targets if x in existing]
    if present and len(present) != len(targets):
        raise AssertionError(f"partial TB05D consolidation: {present}")

    if not present:
        actual_blob = git_blob_sha(raw)
        assert actual_blob == BASELINE_BLOB, f"baseline registry drift: {actual_blob}"
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
        print("ANIMO-TB05D central registry materialized")
        return 0

    by_id = {e["test_id"]: e for e in registry["test_registry"]}
    for entry in expected:
        assert by_id[entry["test_id"]] == entry
    print("ANIMO-TB05D central registry already exact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
