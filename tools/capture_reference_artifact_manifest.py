#!/usr/bin/env python3
"""Capture a fail-closed receipt manifest for external ANIMO reference artifacts.

This tool hashes received bytes and records provenance claims without copying or
executing the artifact. Its output is evidence for later review only. It has no
reference-admission authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

EVIDENCE_CLASS = "RECEIPT_MANIFEST_NOT_REFERENCE_ADMISSION"
TRUST_CLASS = "UNASSESSED_RECEIVED_ARTIFACT"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class FileRecord:
    relative_path: str
    size: int
    sha256: str

    def as_dict(self) -> dict:
        return {
            "relative_path": self.relative_path,
            "size": self.size,
            "sha256": self.sha256,
        }


def _file_records(root: Path) -> list[FileRecord]:
    if root.is_file():
        return [FileRecord(root.name, root.stat().st_size, sha256_file(root))]
    if not root.is_dir():
        raise ValueError(f"artifact path does not exist or is unsupported: {root}")

    records: list[FileRecord] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        records.append(
            FileRecord(
                path.relative_to(root).as_posix(),
                path.stat().st_size,
                sha256_file(path),
            )
        )
    if not records:
        raise ValueError("artifact directory contains no files")
    return records


def content_set_sha256(records: Iterable[FileRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(record.relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record.size).encode("ascii"))
        digest.update(b"\0")
        digest.update(record.sha256.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def capture_artifact(
    artifact_path: Path,
    *,
    label: str,
    artifact_class: str,
    claimed_version: str | None = None,
    claimed_revision: str | None = None,
    provenance_note: str | None = None,
    expected_sha256: str | None = None,
    captured_at_utc: str | None = None,
) -> dict:
    artifact_path = artifact_path.resolve()
    records = _file_records(artifact_path)
    is_single_file = artifact_path.is_file()

    actual_single_sha = records[0].sha256 if is_single_file else None
    if expected_sha256 is not None:
        if not is_single_file:
            raise ValueError("--expected-sha256 is valid only for a single-file artifact")
        if actual_single_sha.lower() != expected_sha256.lower():
            raise ValueError(
                f"SHA-256 mismatch: expected {expected_sha256.lower()}, "
                f"got {actual_single_sha.lower()}"
            )

    captured_at_utc = captured_at_utc or datetime.now(timezone.utc).isoformat()
    return {
        "schema": "animo-prep02r-reference-artifact-receipt-v1",
        "evidence_class": EVIDENCE_CLASS,
        "captured_at_utc": captured_at_utc,
        "artifact": {
            "label": label,
            "artifact_class": artifact_class,
            "container_type": "file" if is_single_file else "directory",
            "claimed_version": claimed_version,
            "claimed_revision": claimed_revision,
            "provenance_note": provenance_note,
            "file_count": len(records),
            "total_size": sum(item.size for item in records),
            "sha256": actual_single_sha,
            "content_set_sha256": content_set_sha256(records),
            "files": [item.as_dict() for item in records],
        },
        "receipt_checks": {
            "bytes_hashed_before_execution": True,
            "expected_sha256_supplied": expected_sha256 is not None,
            "expected_sha256_matched": True if expected_sha256 is not None else None,
            "artifact_executed_by_this_tool": False,
            "artifact_copied_by_this_tool": False,
        },
        "trust_classification": TRUST_CLASS,
        "reference_admitted": False,
        "native_execution_admitted": False,
        "note": (
            "Receipt and hashing only. Provenance and lineage must be reviewed "
            "before any native execution or reference-admission decision."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_path", type=Path)
    parser.add_argument("--label", required=True)
    parser.add_argument(
        "--artifact-class",
        required=True,
        choices=[
            "historical_executable",
            "project_build_metadata",
            "historical_output_bundle",
            "compiler_or_environment_artifact",
            "other",
        ],
    )
    parser.add_argument("--claimed-version")
    parser.add_argument("--claimed-revision")
    parser.add_argument("--provenance-note")
    parser.add_argument("--expected-sha256")
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()

    try:
        manifest = capture_artifact(
            args.artifact_path,
            label=args.label,
            artifact_class=args.artifact_class,
            claimed_version=args.claimed_version,
            claimed_revision=args.claimed_revision,
            provenance_note=args.provenance_note,
            expected_sha256=args.expected_sha256,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    encoded = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
