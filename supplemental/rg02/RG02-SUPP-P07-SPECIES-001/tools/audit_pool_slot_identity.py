#!/usr/bin/env python3
"""Audit numeric same-array cross-slot assignments in frozen ANIMO revision-53."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
SOURCE_SUFFIXES = {".for", ".f90"}
LHS = re.compile(r"^([A-Za-z][A-Za-z0-9_]*)\s*\(\s*(\d+)\s*,[^)]*\)\s*=\s*(.*)$", re.I)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def logical_statements(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    buf = ""
    start: int | None = None
    for line_no, raw in enumerate(text.splitlines(), 1):
        if raw and raw[0] in "cC*!":
            continue
        code = raw.split("!", 1)[0].rstrip()
        if not code.strip():
            continue
        trailing = code.endswith("&")
        if trailing:
            code = code[:-1]
        part = code.lstrip()
        if part.startswith("&"):
            part = part[1:].lstrip()
        if not buf:
            buf = part
            start = line_no
        else:
            buf += " " + part
        if trailing:
            continue
        assert start is not None
        for statement in buf.split(";"):
            if statement.strip():
                out.append((start, statement.strip()))
        buf = ""
        start = None
    if buf and start is not None:
        for statement in buf.split(";"):
            if statement.strip():
                out.append((start, statement.strip()))
    return out


def classify(filename: str, array: str, lhs_slot: int, rhs_slot: int, statement: str) -> tuple[str, str | None]:
    array_key = array.lower()
    if filename.lower() == "outbal_calc.for" and array_key == "bafop" and lhs_slot == 24 and rhs_slot == 25:
        return "CONFIRMED_EXISTING_DISCREPANCY", "TCD-027"
    if array_key in {"transfom", "transfon", "transfop"} and lhs_slot in {19, 20} and rhs_slot == 17:
        return "INTENTIONAL_TRANSFER_PARTITION", None
    return "UNRESOLVED_CROSS_SLOT_CANDIDATE", None


def audit_source(source: dict[str, str]) -> dict:
    findings: list[dict] = []
    for filename in sorted(source):
        for line_no, statement in logical_statements(source[filename]):
            match = LHS.match(statement)
            if not match:
                continue
            array, lhs_slot_text, rhs = match.groups()
            lhs_slot = int(lhs_slot_text)
            refs = [
                int(value)
                for value in re.findall(
                    r"\b" + re.escape(array) + r"\s*\(\s*(\d+)\s*,",
                    rhs,
                    re.I,
                )
            ]
            for rhs_slot in refs:
                if rhs_slot == lhs_slot:
                    continue
                classification, discrepancy = classify(
                    filename, array, lhs_slot, rhs_slot, statement
                )
                findings.append(
                    {
                        "file": filename,
                        "line": line_no,
                        "array": array,
                        "lhs_slot": lhs_slot,
                        "rhs_slot": rhs_slot,
                        "classification": classification,
                        "existing_discrepancy": discrepancy,
                        "statement": statement,
                    }
                )

    counts: dict[str, int] = {}
    for item in findings:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
    unresolved = [
        item
        for item in findings
        if item["classification"] == "UNRESOLVED_CROSS_SLOT_CANDIDATE"
    ]
    return {
        "evidence_class": "SOURCE_BOUND_NUMERIC_CROSS_SLOT_AUDIT_NOT_REFERENCE",
        "source_sha256_required": EXPECTED_SOURCE_SHA256,
        "same_array_cross_slot_findings": len(findings),
        "classification_counts": dict(sorted(counts.items())),
        "findings": findings,
        "unresolved_cross_slot_candidates": unresolved,
        "decision": (
            "UNRESOLVED_CROSS_SLOT_CANDIDATES_REQUIRE_REVIEW"
            if unresolved
            else "NO_NEW_CROSS_SLOT_DEFECT_BEYOND_TCD027"
        ),
        "production_migration_admitted": False,
    }


def load_source(zip_path: Path) -> dict[str, str]:
    actual_hash = sha256_file(zip_path)
    if actual_hash != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source ZIP hash mismatch: {actual_hash}")
    source: dict[str, str] = {}
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            name = Path(info.filename).name
            if Path(name).suffix.lower() in SOURCE_SUFFIXES:
                source[name] = zf.read(info).decode("latin1")
    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = audit_source(load_source(args.source_zip))
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 2 if report["unresolved_cross_slot_candidates"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
