#!/usr/bin/env python3
"""Fail-closed comparison of ANIMO legacy output trees.

PREP02 qualification tooling only. A successful comparison is evidence about
output equivalence for the supplied directories; it does not qualify either
build as a scientific reference.

Only explicitly known volatile legacy metadata is normalized. Scientific
numbers are never tolerance-filtered by this tool. When numerical differences
exist they are summarized, not accepted.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Iterable


VOLATILE_RULES: list[tuple[str, re.Pattern[str], str]] = [
    (
        "file_creation_timestamp",
        re.compile(
            r"(?m)^ File created on \d{4}-\d{2}-\d{2} at "
            r"\d{2}:\d{2}:\d{2}\.\d+ hr\.$"
        ),
        " File created on <VOLATILE_TIMESTAMP>.",
    ),
    (
        "output_run_start_timestamp",
        re.compile(
            r"(?m)^ \* ANIMO40-run started on: \d{4}-\d{2}-\d{2}  "
            r"\d{2}:\d{2}:\d{2}\.\d+$"
        ),
        " * ANIMO40-run started on: <VOLATILE_TIMESTAMP>",
    ),
    (
        "message_run_start_timestamp",
        re.compile(
            r"(?m)^ ANIMO run start: \d{4}-\d{2}-\d{2}  "
            r"\d{2}:\d{2}:\d{2}\.\d+$"
        ),
        " ANIMO run start: <VOLATILE_TIMESTAMP>",
    ),
    (
        "message_run_end_timestamp",
        re.compile(
            r"(?m)^ ANIMO run End\s+: \d{4}-\d{2}-\d{2}  "
            r"\d{2}:\d{2}:\d{2}\.\d+$"
        ),
        " ANIMO run End  : <VOLATILE_TIMESTAMP>",
    ),
    (
        "elapsed_cpu_seconds",
        re.compile(r"(?m)^ Elapsed:\s+[-+0-9.Ee]+ sec$"),
        " Elapsed: <VOLATILE_CPU_SECONDS> sec",
    ),
]

FLOAT_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"[-+]?(?:(?:\d+\.\d*)|(?:\.\d+)|(?:\d+))(?:[EeDd][-+]?\d+)?"
    r"(?![A-Za-z0-9_.])"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_legacy_text(data: bytes) -> tuple[bytes, dict[str, int]]:
    """Normalize only declared volatile legacy metadata.

    Latin-1 is used as a lossless byte-to-character mapping for the legacy
    formatted outputs. The replacement rules are deliberately anchored to
    complete metadata lines so dates or numbers in scientific output remain
    untouched.
    """
    text = data.decode("latin1")
    counts: dict[str, int] = {}
    for name, pattern, replacement in VOLATILE_RULES:
        text, count = pattern.subn(replacement, text)
        counts[name] = count
    return text.encode("latin1"), counts


def _is_text_like(data: bytes) -> bool:
    return b"\x00" not in data


def _first_differing_lines(a: bytes, b: bytes, limit: int = 5) -> list[dict]:
    if not (_is_text_like(a) and _is_text_like(b)):
        return []
    aa = a.decode("latin1").splitlines()
    bb = b.decode("latin1").splitlines()
    differences: list[dict] = []
    for index in range(max(len(aa), len(bb))):
        left = aa[index] if index < len(aa) else None
        right = bb[index] if index < len(bb) else None
        if left != right:
            differences.append(
                {
                    "line": index + 1,
                    "reference": left,
                    "candidate": right,
                }
            )
            if len(differences) >= limit:
                break
    return differences


def _numeric_difference_summary(a: bytes, b: bytes) -> dict | None:
    if not (_is_text_like(a) and _is_text_like(b)):
        return None

    def values(data: bytes) -> list[float]:
        result: list[float] = []
        for token in FLOAT_TOKEN.findall(data.decode("latin1")):
            try:
                result.append(float(token.replace("D", "E").replace("d", "e")))
            except ValueError:
                pass
        return result

    av = values(a)
    bv = values(b)
    if len(av) != len(bv):
        return {
            "same_numeric_token_count": False,
            "reference_numeric_tokens": len(av),
            "candidate_numeric_tokens": len(bv),
        }
    if not av:
        return {
            "same_numeric_token_count": True,
            "numeric_tokens": 0,
            "different_numeric_tokens": 0,
        }

    different = 0
    max_abs = 0.0
    max_rel = 0.0
    max_abs_index: int | None = None
    for index, (left, right) in enumerate(zip(av, bv)):
        if left != right:
            different += 1
        abs_diff = abs(right - left)
        scale = max(abs(left), abs(right))
        rel_diff = abs_diff / scale if scale else 0.0
        if abs_diff > max_abs:
            max_abs = abs_diff
            max_abs_index = index
        max_rel = max(max_rel, rel_diff)

    return {
        "same_numeric_token_count": True,
        "numeric_tokens": len(av),
        "different_numeric_tokens": different,
        "max_absolute_difference": max_abs,
        "max_relative_difference": max_rel,
        "max_absolute_difference_token_index": max_abs_index,
        "note": "diagnostic magnitude only; no acceptance tolerance is applied",
    }


def compare_file(reference: Path, candidate: Path, normalize_volatile: bool) -> dict:
    left_raw = reference.read_bytes()
    right_raw = candidate.read_bytes()
    result = {
        "reference_sha256": sha256_bytes(left_raw),
        "candidate_sha256": sha256_bytes(right_raw),
        "reference_size": len(left_raw),
        "candidate_size": len(right_raw),
    }

    if left_raw == right_raw:
        result["classification"] = "EQUAL_RAW"
        return result

    left = left_raw
    right = right_raw
    normalization = None
    if normalize_volatile and _is_text_like(left_raw) and _is_text_like(right_raw):
        left, left_counts = normalize_legacy_text(left_raw)
        right, right_counts = normalize_legacy_text(right_raw)
        normalization = {
            "reference_substitutions": left_counts,
            "candidate_substitutions": right_counts,
        }
        result["normalization"] = normalization
        result["reference_normalized_sha256"] = sha256_bytes(left)
        result["candidate_normalized_sha256"] = sha256_bytes(right)
        if left == right:
            result["classification"] = "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY"
            return result

    result["classification"] = "DIFFERENT"
    result["first_differing_lines"] = _first_differing_lines(left, right)
    result["numeric_difference_summary"] = _numeric_difference_summary(left, right)
    return result


def _selected_files(
    root: Path,
    file_list: Iterable[str] | None,
    excludes: list[str],
) -> set[str]:
    if file_list is None:
        names = {
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        }
    else:
        names = {name.strip().replace("\\", "/") for name in file_list if name.strip()}

    return {
        name
        for name in names
        if not any(fnmatch.fnmatch(name, pattern) for pattern in excludes)
    }


def compare_trees(
    reference_root: Path,
    candidate_root: Path,
    *,
    file_list: Iterable[str] | None = None,
    excludes: list[str] | None = None,
    normalize_volatile: bool = True,
) -> dict:
    excludes = excludes or []
    requested = _selected_files(reference_root, file_list, excludes)
    if file_list is None:
        candidate_names = _selected_files(candidate_root, None, excludes)
    else:
        candidate_names = {
            name
            for name in requested
            if (candidate_root / name).is_file()
        }

    reference_names = {name for name in requested if (reference_root / name).is_file()}
    missing_reference = sorted(requested - reference_names)
    missing_candidate = sorted(reference_names - candidate_names)
    extra_candidate = sorted(candidate_names - reference_names) if file_list is None else []
    common = sorted(reference_names & candidate_names)

    files = {
        name: compare_file(
            reference_root / name,
            candidate_root / name,
            normalize_volatile=normalize_volatile,
        )
        for name in common
    }

    raw_equal = sum(item["classification"] == "EQUAL_RAW" for item in files.values())
    volatile_equal = sum(
        item["classification"] == "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY"
        for item in files.values()
    )
    different = sum(item["classification"] == "DIFFERENT" for item in files.values())

    fail_closed = bool(missing_reference or missing_candidate or extra_candidate or different)
    if fail_closed:
        decision = "DIFFERENT_FAIL_CLOSED"
    elif volatile_equal:
        decision = "MATCH_AFTER_DECLARED_VOLATILE_NORMALIZATION"
    else:
        decision = "MATCH_EXACT"

    return {
        "evidence_class": "COMPARATOR_OUTPUT_NOT_REFERENCE_ADMISSION",
        "reference_root": str(reference_root),
        "candidate_root": str(candidate_root),
        "normalize_declared_volatile_metadata": normalize_volatile,
        "excluded_patterns": excludes,
        "file_set": {
            "requested_or_reference_files": len(reference_names),
            "common_files": len(common),
            "missing_reference": missing_reference,
            "missing_candidate": missing_candidate,
            "extra_candidate": extra_candidate,
        },
        "summary": {
            "equal_raw": raw_equal,
            "equal_after_declared_volatile_normalization": volatile_equal,
            "different": different,
        },
        "files": files,
        "decision": decision,
        "reference_qualified_by_this_tool": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_root", type=Path)
    parser.add_argument("candidate_root", type=Path)
    parser.add_argument("--file-list", type=Path)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--raw-only", action="store_true")
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    reference_root = args.reference_root.resolve()
    candidate_root = args.candidate_root.resolve()
    if not reference_root.is_dir() or not candidate_root.is_dir():
        raise SystemExit("reference_root and candidate_root must both be directories")

    file_list = None
    if args.file_list:
        file_list = args.file_list.read_text(encoding="utf-8").splitlines()

    report = compare_trees(
        reference_root,
        candidate_root,
        file_list=file_list,
        excludes=args.exclude,
        normalize_volatile=not args.raw_only,
    )
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["decision"] != "DIFFERENT_FAIL_CLOSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
