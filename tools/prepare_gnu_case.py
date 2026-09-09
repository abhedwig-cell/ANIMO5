#!/usr/bin/env python3
"""Prepare an execution-only GNU/Linux testcase copy from the frozen ANIMO testbank.

Qualification tooling only. The frozen testbank ZIP is never modified. The adapter
makes only runtime-compatibility changes that are recorded in metadata:

* Windows path separators in the direct file are changed to '/';
* case-insensitive Windows path resolution is materialized as exact-path file copies;
* quoted two-character PrintBalLabel values are unquoted because GNU list-directed
  internal READ rejects the Intel/Windows-era ``'RP'!comment`` form while the
  character payload is unchanged;
* PowerStation-compatible sequential-unformatted hydrology framing is converted to
  GNU record framing without changing logical-record payload bytes.

The resulting case remains DIAGNOSTIC_NOT_REFERENCE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import zipfile
from pathlib import Path

EXPECTED_TESTBANK_SHA256 = (
    "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
)
INPUT_KEYS = {
    "GEN", "MAT", "PLA", "SOI", "BOU", "INI", "MAN", "SWU",
    "WAI", "WAU", "CHE", "CRU",
}
PATH_LINE = re.compile(r'^\s*([A-Za-z]{3})\s*=\s*"([^"]+)"')
PRINT_BAL_LABEL = re.compile(
    r"(?im)^(\s*PrintBalLabel\s*=\s*)'([^'\r\n]{1,2})'"
)
HEADER = 0x4B
TRAILER = 0x82
CONTINUATION = 0x81
MAX_BLOCK_DATA = 128


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_powerstation_records(data: bytes) -> tuple[list[bytes], int]:
    if not data or data[0] != HEADER or data[-1] != TRAILER:
        raise ValueError("not a complete PowerStation-compatible file")
    pos = 1
    records: list[bytes] = []
    current = bytearray()
    blocks = 0
    while pos < len(data):
        marker = data[pos]
        pos += 1
        if marker == TRAILER:
            if current or pos != len(data):
                raise ValueError("invalid trailer position")
            return records, blocks
        if marker > CONTINUATION:
            raise ValueError(f"invalid block marker 0x{marker:02x}")
        payload_length = MAX_BLOCK_DATA if marker == CONTINUATION else marker
        if pos + payload_length >= len(data):
            raise ValueError("truncated block")
        current.extend(data[pos:pos + payload_length])
        pos += payload_length
        trailing = data[pos]
        pos += 1
        if trailing != marker:
            raise ValueError("block marker mismatch")
        blocks += 1
        if marker != CONTINUATION:
            records.append(bytes(current))
            current.clear()
    raise ValueError("missing trailer")


def encode_gfortran_records(records: list[bytes]) -> bytes:
    out = bytearray()
    for payload in records:
        length = len(payload)
        out += struct.pack("<i", length)
        out += payload
        out += struct.pack("<i", length)
    return bytes(out)


def find_case_insensitive(root: Path, relative: Path) -> Path | None:
    current = root
    for part in relative.parts:
        if not current.is_dir():
            return None
        exact = current / part
        if exact.exists():
            current = exact
            continue
        matches = [
            path for path in current.iterdir()
            if path.name.casefold() == part.casefold()
        ]
        if len(matches) != 1:
            return None
        current = matches[0]
    return current


def adapt_print_bal_labels(path: Path) -> tuple[int, str, str]:
    before = path.read_bytes()
    text = before.decode("latin1")
    adapted, count = PRINT_BAL_LABEL.subn(r"\1\2", text)
    after = adapted.encode("latin1")
    if count:
        path.write_bytes(after)
    return count, sha256_bytes(before), sha256_bytes(after)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("testbank_zip", type=Path)
    parser.add_argument("case")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    archive_path = args.testbank_zip.resolve()
    actual_hash = sha256_file(archive_path)
    if actual_hash != EXPECTED_TESTBANK_SHA256:
        raise SystemExit(f"testbank SHA-256 mismatch: {actual_hash}")

    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    prefix = f"ANIMO_testbank/{args.case}/"
    with zipfile.ZipFile(archive_path) as archive:
        members = [
            member
            for member in archive.infolist()
            if not member.is_dir() and member.filename.startswith(prefix)
        ]
        if not members:
            raise SystemExit(f"case not found in frozen testbank: {args.case}")
        for member in members:
            relative = Path(member.filename[len(prefix):])
            target = output_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))

    direct_candidates = [
        path
        for path in output_dir.iterdir()
        if path.is_file() and path.name.casefold() == "animo.ini"
    ]
    if len(direct_candidates) != 1:
        raise SystemExit(
            "expected exactly one root direct file named animo.ini "
            "(case-insensitive)"
        )
    direct_file = direct_candidates[0]
    direct_before = direct_file.read_bytes()
    direct_text = direct_before.decode("latin1")
    separator_replacements = direct_text.count("\\")
    direct_text = direct_text.replace("\\", "/")
    direct_file.write_bytes(direct_text.encode("latin1"))

    entries: dict[str, str] = {}
    for line in direct_text.splitlines():
        match = PATH_LINE.match(line)
        if match:
            entries[match.group(1).upper()] = match.group(2)

    aliases = []
    missing = []
    for key, value in entries.items():
        relative = Path(value)
        target = output_dir / relative
        if key in INPUT_KEYS:
            source = find_case_insensitive(output_dir, relative)
            if source is None or not source.is_file():
                missing.append({"key": key, "path": value})
                continue
            if source != target:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                aliases.append(
                    {
                        "key": key,
                        "requested": value,
                        "source": source.relative_to(output_dir).as_posix(),
                    }
                )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)

    general_info = None
    if "GEN" in entries:
        general_path = output_dir / Path(entries["GEN"])
        if general_path.exists():
            count, before_hash, after_hash = adapt_print_bal_labels(general_path)
            general_info = {
                "path": entries["GEN"],
                "quoted_printbal_labels_unquoted": count,
                "before_sha256": before_hash,
                "after_sha256": after_hash,
                "character_payload_changed": False,
            }

    hydrology_info = None
    if "SWU" in entries:
        hydrology_path = output_dir / Path(entries["SWU"])
        if hydrology_path.exists():
            before = hydrology_path.read_bytes()
            if before and before[0] == HEADER and before[-1] == TRAILER:
                records, blocks = parse_powerstation_records(before)
                after = encode_gfortran_records(records)
                hydrology_path.write_bytes(after)
                hydrology_info = {
                    "path": entries["SWU"],
                    "source_sha256": sha256_bytes(before),
                    "target_sha256": sha256_bytes(after),
                    "logical_record_count": len(records),
                    "physical_block_count": blocks,
                    "payload_sha256": sha256_bytes(b"".join(records)),
                    "logical_payload_modified": False,
                }

    metadata = {
        "evidence_class": "DIAGNOSTIC_NOT_REFERENCE",
        "testbank_sha256": EXPECTED_TESTBANK_SHA256,
        "case": args.case,
        "frozen_testbank_modified": False,
        "direct_file": {
            "path": direct_file.relative_to(output_dir).as_posix(),
            "before_sha256": sha256_bytes(direct_before),
            "after_sha256": sha256_file(direct_file),
            "windows_path_separator_replacements": separator_replacements,
        },
        "case_insensitive_path_aliases": aliases,
        "missing_optional_or_unresolved_references": missing,
        "print_balance_label_runtime_adaptation": general_info,
        "hydrology_record_adaptation": hydrology_info,
        "scientific_input_values_changed": False,
        "reference_qualified": False,
    }
    (output_dir / "PREP02_case_adapter.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
