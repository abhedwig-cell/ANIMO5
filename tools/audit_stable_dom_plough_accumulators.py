#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

FROZEN_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TARGETS = ("SuStdiorma", "SuStdiorni", "SuStdiorpo")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _code_part(line: str) -> str:
    """Return a conservative fixed-form code fragment for source-level scanning."""
    if not line:
        return ""
    if line[0] in "Cc*!":
        return ""
    return line.split("!", 1)[0]


def _assignment(line: str, target: str) -> tuple[str, str] | None:
    """Find assignment to target anywhere on a source line, including one-line IF."""
    code = _code_part(line)
    m = re.search(rf"(?i)\b({re.escape(target)})\s*=\s*(.*)$", code)
    if not m:
        return None
    return m.group(1), m.group(2).strip()


def _is_zero_expression(expr: str) -> bool:
    compact = re.sub(r"\s+", "", expr).lower()
    return compact in {"0", "0.", "0.0", "0.0e0", "0.0d0", "+0", "+0.", "+0.0"}


def analyze_text(text: str) -> dict:
    lines = text.splitlines()
    plough_lines = [
        i for i, line in enumerate(lines, start=1)
        if re.search(r"(?i)\bif\s*\(\s*pl\s*\(\s*i\s*\)\s*\.gt\.\s*0\s*\)\s*then\b", _code_part(line))
    ]

    targets: dict[str, dict] = {}
    for target in TARGETS:
        assignments = []
        definitions_before_first_self_read = []
        first_self_read = None
        zero_assignments = []

        for lineno, line in enumerate(lines, start=1):
            parsed = _assignment(line, target)
            if not parsed:
                continue
            _, rhs = parsed
            rhs_reads_target = bool(re.search(rf"(?i)\b{re.escape(target)}\b", rhs))
            is_zero = _is_zero_expression(rhs)
            rec = {
                "line": lineno,
                "rhs": rhs,
                "rhs_reads_target": rhs_reads_target,
                "is_explicit_zero": is_zero,
            }
            assignments.append(rec)
            if is_zero:
                zero_assignments.append(lineno)
            if rhs_reads_target and first_self_read is None:
                first_self_read = rec
            elif first_self_read is None:
                definitions_before_first_self_read.append(lineno)

        confirmed = (
            first_self_read is not None
            and not definitions_before_first_self_read
            and not [ln for ln in zero_assignments if ln < first_self_read["line"]]
        )
        targets[target] = {
            "assignment_count": len(assignments),
            "first_self_read_assignment": first_self_read,
            "explicit_definition_lines_before_first_self_read": definitions_before_first_self_read,
            "explicit_zero_assignment_lines": zero_assignments,
            "source_level_use_before_definition_confirmed": confirmed,
        }

    all_confirmed = all(v["source_level_use_before_definition_confirmed"] for v in targets.values())
    return {
        "overall_classification": (
            "CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION"
            if all_confirmed
            else "SOURCE_LEVEL_USE_BEFORE_DEFINITION_NOT_CONFIRMED_FOR_ALL_TARGETS"
        ),
        "plough_event_branch_lines": plough_lines,
        "targets": targets,
    }


def audit_archive(archive: Path) -> dict:
    raw = archive.read_bytes()
    archive_sha = sha256_bytes(raw)
    if archive_sha != FROZEN_SOURCE_SHA256:
        raise ValueError(
            f"source archive SHA-256 mismatch: expected {FROZEN_SOURCE_SHA256}, got {archive_sha}"
        )

    with zipfile.ZipFile(archive) as zf:
        candidates = [n for n in zf.namelist() if n.replace("\\", "/").lower().endswith("/addit.for")]
        if len(candidates) != 1:
            raise ValueError(f"expected exactly one Addit.for member, found {len(candidates)}: {candidates}")
        member = candidates[0]
        data = zf.read(member)

    text = data.decode("cp1252")
    result = analyze_text(text)
    result.update(
        {
            "source_archive_sha256": archive_sha,
            "source_member": member,
            "source_member_size_bytes": len(data),
            "source_member_sha256": sha256_bytes(data),
            "scope_note": (
                "This is a static source-level audit. It confirms reads of the three local accumulators "
                "before any explicit definition in Addit.for. It does not by itself quantify dynamic "
                "numerical impact, compiler-dependent manifestation, testcase activation, or reference-output effect."
            ),
        }
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit stable-DOM plough accumulators in frozen ANIMO revision-53 source.")
    ap.add_argument("archive", type=Path, help="Path to exact ANIMO_4.1.5.53 source ZIP")
    ap.add_argument("--json", type=Path, dest="json_path", help="Optional output JSON path")
    ns = ap.parse_args()

    result = audit_archive(ns.archive)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if ns.json_path:
        ns.json_path.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["overall_classification"] == "CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
