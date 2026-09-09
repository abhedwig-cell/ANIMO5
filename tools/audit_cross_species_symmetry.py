#!/usr/bin/env python3
"""Audit nearby N/P sibling assignments for asymmetric cross-species reuse.

Qualification tooling only. The frozen source archive is never modified.

The heuristic is deliberately conservative:
- infer closely named N/P sibling identifiers from the source itself;
- compare nearby assignments to matching N and P left-hand-side siblings;
- transform the N right-hand side to its P sibling form;
- flag only high-similarity P assignments that retain N sibling identifiers;
- suppress reciprocal cross-coupling where the N assignment intentionally uses
  P siblings while the P assignment intentionally uses N siblings.

A finding is static evidence only and does not by itself establish a defect.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

EXPECTED_SOURCE_SHA256 = (
    "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
)
ASSIGN_RE = re.compile(r"(?i)^([A-Za-z]\w*)\s*(\([^=]*\))?\s*=\s*(.*)$")
SUBSTITUTIONS = (
    ("nifr", "pofr"),
    ("orgn", "orgp"),
    ("ni", "po"),
    ("on", "op"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def logical_lines(text: str) -> list[tuple[int, str]]:
    """Join the free-form continuation style used in the supplied source."""
    result: list[tuple[int, str]] = []
    current = ""
    start_line = 0

    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("!"):
            continue
        if "!" in stripped:
            stripped = stripped.split("!", 1)[0].rstrip()
        if not current:
            start_line = line_number
        if stripped.startswith("&"):
            stripped = stripped[1:].lstrip()
        continued = stripped.endswith("&")
        if continued:
            stripped = stripped[:-1].rstrip()
        current += (" " if current else "") + stripped
        if not continued:
            result.append((start_line, current))
            current = ""

    if current:
        result.append((start_line, current))
    return result


def infer_pairs(identifiers: set[str]) -> dict[str, str]:
    """Infer conservative N-to-P sibling identifier pairs."""
    pairs: dict[str, str] = {}
    for n_name in identifiers:
        for n_fragment, p_fragment in SUBSTITUTIONS:
            for match in re.finditer(n_fragment, n_name):
                p_name = (
                    n_name[: match.start()]
                    + p_fragment
                    + n_name[match.end() :]
                )
                if p_name not in identifiers:
                    continue
                similarity = difflib.SequenceMatcher(None, n_name, p_name).ratio()
                if similarity >= 0.75:
                    pairs[n_name] = p_name

    # Core transformation families remain explicit positive controls.
    for n_name, p_name in (
        ("transfon", "transfop"),
        ("tomnni", "tomnpo"),
        ("rekoni", "rekopo"),
    ):
        if n_name in identifiers and p_name in identifiers:
            pairs[n_name] = p_name
    return pairs


def replace_siblings(text: str, pairs: dict[str, str]) -> str:
    result = text
    for n_name, p_name in sorted(
        pairs.items(), key=lambda item: -len(item[0])
    ):
        result = re.sub(
            r"(?i)\b" + re.escape(n_name) + r"\b", p_name, result
        )
    return result


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def scan_sources(
    files: dict[str, str],
    *,
    threshold: float = 0.90,
    proximity: int = 30,
) -> tuple[list[dict], list[dict], dict[str, str]]:
    identifiers = {
        token.lower()
        for text in files.values()
        for token in re.findall(r"\b[A-Za-z]\w*\b", text)
    }
    pairs = infer_pairs(identifiers)
    inverse_pairs = {p_name: n_name for n_name, p_name in pairs.items()}

    findings: list[dict] = []
    contextual: list[dict] = []

    for filename, text in files.items():
        assignments: list[dict] = []
        for line_number, statement in logical_lines(text):
            match = ASSIGN_RE.match(statement)
            if not match:
                continue
            assignments.append(
                {
                    "line": line_number,
                    "lhs": match.group(1).lower(),
                    "subscripts": re.sub(
                        r"\s+", "", match.group(2) or ""
                    ).lower(),
                    "rhs": match.group(3),
                    "statement": statement,
                }
            )

        lookup: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for assignment in assignments:
            lookup[(assignment["lhs"], assignment["subscripts"])].append(
                assignment
            )

        for p_assignment in assignments:
            p_lhs = p_assignment["lhs"]
            if p_lhs not in inverse_pairs:
                continue
            n_lhs = inverse_pairs[p_lhs]
            siblings = lookup.get((n_lhs, p_assignment["subscripts"]), [])

            for n_assignment in siblings:
                if abs(p_assignment["line"] - n_assignment["line"]) > proximity:
                    continue

                expected_p_rhs = replace_siblings(n_assignment["rhs"], pairs)
                similarity = difflib.SequenceMatcher(
                    None,
                    normalized(expected_p_rhs),
                    normalized(p_assignment["rhs"]),
                ).ratio()

                p_rhs_tokens = {
                    token.lower()
                    for token in re.findall(
                        r"\b[A-Za-z]\w*\b", p_assignment["rhs"]
                    )
                }
                n_rhs_tokens = {
                    token.lower()
                    for token in re.findall(
                        r"\b[A-Za-z]\w*\b", n_assignment["rhs"]
                    )
                }

                stale_siblings = []
                for n_name, p_name in pairs.items():
                    if n_name not in p_rhs_tokens:
                        continue
                    if not re.search(
                        r"(?i)\b" + re.escape(p_name) + r"\b",
                        expected_p_rhs,
                    ):
                        continue
                    stale_siblings.append(
                        {
                            "n_token": n_name,
                            "expected_p_token": p_name,
                        }
                    )

                if not stale_siblings:
                    continue

                reciprocal = any(
                    p_name in n_rhs_tokens
                    for n_name, p_name in pairs.items()
                    if n_name in p_rhs_tokens
                )

                record = {
                    "file": Path(filename).name,
                    "n_line": n_assignment["line"],
                    "p_line": p_assignment["line"],
                    "n_statement": n_assignment["statement"],
                    "p_statement": p_assignment["statement"],
                    "expected_p_rhs_from_n_sibling": expected_p_rhs,
                    "structural_similarity": similarity,
                    "stale_n_siblings": stale_siblings,
                    "reciprocal_cross_coupling": reciprocal,
                }

                if similarity >= threshold and not reciprocal:
                    record["classification"] = (
                        "HIGH_CONFIDENCE_CROSS_SPECIES_SIBLING_ASYMMETRY"
                    )
                    findings.append(record)
                else:
                    record["classification"] = (
                        "CONTEXTUAL_CROSS_SPECIES_COUPLING_NOT_PROMOTED"
                    )
                    contextual.append(record)

    return findings, contextual, pairs


def audit_zip(path: Path, threshold: float = 0.90) -> dict:
    actual_sha = sha256(path)
    if actual_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"source archive SHA-256 mismatch: {actual_sha}")

    files: dict[str, str] = {}
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if Path(info.filename).suffix.lower() not in {".for", ".f90"}:
                continue
            files[info.filename] = archive.read(info).decode("latin1")

    findings, contextual, pairs = scan_sources(files, threshold=threshold)
    return {
        "evidence_class": (
            "SOURCE_BOUND_STATIC_CROSS_SPECIES_SYMMETRY_AUDIT_"
            "NOT_DEFECT_ADMISSION_BY_ITSELF"
        ),
        "source_zip_sha256": actual_sha,
        "fortran_files_scanned": len(files),
        "threshold": threshold,
        "inferred_sibling_pairs": len(pairs),
        "high_confidence_candidate_count": len(findings),
        "high_confidence_candidates": findings,
        "contextual_not_promoted_count": len(contextual),
        "contextual_not_promoted": contextual,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--threshold", type=float, default=0.90)
    args = parser.parse_args()

    result = audit_zip(args.source_zip, threshold=args.threshold)
    encoded = json.dumps(result, indent=2) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
