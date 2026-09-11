#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
ADDITIONS = ROOT / "integration/animo-testbank/fragments/ANIMO-TB03D_REGISTRY_ADDITIONS.json"
BASELINE_BLOB = "a5f279cfa334dc63d3e4e8759370279736d874a0"
TARGET_IDS = ["ATB-ORACLE-002", "ATB-ORACLE-003", "ATB-SPC-003", "ATB-TRN-002", "ATB-CONS-002", "ATB-CONS-003", "ATB-CONS-004", "ATB-CONS-005"]
NONQUALIFIED_IDS = {"ATB-SPC-004", "ATB-SPC-005", "ATB-SPC-006", "ATB-SPC-007"}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    additions = json.loads(ADDITIONS.read_text(encoding="utf-8"))
    entries = additions["entries"]
    ids = [e["test_id"] for e in entries]
    assert ids == TARGET_IDS
    assert len(ids) == len(set(ids)) == 8
    assert not (set(ids) & NONQUALIFIED_IDS)
    assert additions["baseline_registry_blob"] == BASELINE_BLOB

    raw = REGISTRY.read_bytes()
    registry = json.loads(raw)
    existing_ids = [e["test_id"] for e in registry["test_registry"]]
    assert len(existing_ids) == len(set(existing_ids))
    assert not (set(existing_ids) & NONQUALIFIED_IDS)
    present = [x for x in TARGET_IDS if x in existing_ids]
    if present and len(present) != len(TARGET_IDS):
        raise AssertionError(f"partial TB03D consolidation: {present}")

    if not present:
        actual = git_blob_sha(raw)
        assert actual == BASELINE_BLOB, f"baseline registry drift: {actual}"
        if not args.write:
            return 2
        updated = append_entries(raw.decode("utf-8"), entries)
        parsed = json.loads(updated)
        by_id = {e["test_id"]: e for e in parsed["test_registry"]}
        for entry in entries:
            assert by_id[entry["test_id"]] == entry
        assert not (NONQUALIFIED_IDS & set(by_id))
        REGISTRY.write_text(updated, encoding="utf-8")
        print("ANIMO-TB03D central registry materialized")
        return 0

    by_id = {e["test_id"]: e for e in registry["test_registry"]}
    for entry in entries:
        assert by_id[entry["test_id"]] == entry
    print("ANIMO-TB03D central registry already exact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
