#!/usr/bin/env python3
"""Audit nested labeled-DO loops for same-position loop-index substitutions.

Qualification tooling only. The source archive is not modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_SOURCE_SHA256 = (
    "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
)
DO_RE = re.compile(r"^\s*Do\s+(\d+)\s+([A-Za-z]\w*)\s*=\s*", re.I)
ARRAY_RE = re.compile(r"\b([A-Za-z]\w*)\s*\(([^\n()]*)\)")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_text(filename: str, text: str) -> list[dict]:
    """Find arrays whose same argument position switches loop index.

    The heuristic is intentionally narrow. In an inner labeled-DO loop it
    reports only when the same array and same argument position is indexed
    with both the inner loop variable and a surrounding loop variable.
    Legitimate multidimensional patterns such as A(outer, inner) therefore do
    not trigger merely because both loop variables occur in the same array.
    """
    lines = text.splitlines()
    loops: list[tuple[int, int, str, str]] = []

    for index, line in enumerate(lines):
        if line.lstrip().startswith("!"):
            continue
        match = DO_RE.match(line)
        if not match:
            continue
        label, variable = match.group(1), match.group(2).upper()
        end_re = re.compile(r"^\s*" + re.escape(label) + r"\b")
        end = None
        for candidate in range(index + 1, len(lines)):
            if end_re.match(lines[candidate]):
                end = candidate
                break
        if end is not None:
            loops.append((index, end, variable, label))

    findings: list[dict] = []
    for start, end, inner, label in loops:
        outers = [loop for loop in loops if loop[0] < start and loop[1] >= end]
        if not outers:
            continue
        outer_variables = {loop[2] for loop in outers}
        counts: dict[tuple[str, int], Counter] = defaultdict(Counter)
        occurrences: dict[tuple[str, int], list[dict]] = defaultdict(list)

        for line_index in range(start + 1, end):
            code = lines[line_index].split("!")[0]
            for match in ARRAY_RE.finditer(code):
                array = match.group(1)
                arguments = [part.strip().upper() for part in match.group(2).split(",")]
                for position, argument in enumerate(arguments, 1):
                    if argument == inner or argument in outer_variables:
                        key = (array.lower(), position)
                        counts[key][argument] += 1
                        occurrences[key].append(
                            {
                                "line": line_index + 1,
                                "text": code.strip(),
                                "index_variable": argument,
                            }
                        )

        for (array, position), counter in counts.items():
            if not counter[inner]:
                continue
            for outer in sorted(outer_variables):
                if not counter[outer]:
                    continue
                findings.append(
                    {
                        "file": filename,
                        "inner_loop": {
                            "variable": inner,
                            "label": label,
                            "start_line": start + 1,
                            "end_line": end + 1,
                        },
                        "outer_loop_variable": outer,
                        "array": array,
                        "argument_position": position,
                        "inner_index_uses": counter[inner],
                        "outer_index_uses": counter[outer],
                        "occurrences": occurrences[(array, position)],
                        "classification": (
                            "SAME_ARRAY_ARGUMENT_POSITION_SWITCHES_BETWEEN_"
                            "INNER_AND_OUTER_LOOP_INDEX"
                        ),
                    }
                )

    return findings


def audit_zip(path: Path) -> dict:
    actual_sha = sha256(path)
    if actual_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"source archive SHA-256 mismatch: {actual_sha}")

    candidates: list[dict] = []
    files_scanned = 0
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if Path(info.filename).suffix.lower() not in {".for", ".f90"}:
                continue
            files_scanned += 1
            candidates.extend(
                scan_text(Path(info.filename).name, archive.read(info).decode("latin1"))
            )

    return {
        "evidence_class": (
            "SOURCE_BOUND_STATIC_INDEX_AUDIT_NOT_DEFECT_ADMISSION_BY_ITSELF"
        ),
        "source_zip_sha256": actual_sha,
        "fortran_files_scanned": files_scanned,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    result = audit_zip(args.source_zip)
    encoded = json.dumps(result, indent=2) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
