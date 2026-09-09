#!/usr/bin/env python3
"""Audit parser-visible option contracts against source dispatch and supplied testbank coverage.

Evidence tooling only. The frozen archives are read-only and hash-pinned.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_members(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.lower().endswith((".for", ".f90", ".inc", ".inp", ".ini", ".txt")):
                try:
                    result[name] = archive.read(name).decode("latin1")
                except UnicodeDecodeError:
                    pass
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("testbank_zip", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if sha256(args.source_zip) != SOURCE_SHA256:
        raise SystemExit("source archive SHA-256 mismatch")
    if sha256(args.testbank_zip) != TESTBANK_SHA256:
        raise SystemExit("testbank archive SHA-256 mismatch")

    source = text_members(args.source_zip)
    testbank = text_members(args.testbank_zip)
    input1 = next(
        text for name, text in source.items()
        if name.lower().endswith("/input1.for") or name.lower() == "input1.for"
    )
    animo = next(
        text for name, text in source.items()
        if name.lower().endswith("/animo.for") or name.lower() == "animo.for"
    )
    all_source = "\n".join(source.values())

    check_41 = len(re.findall(
        r"Checkint\([^\n]*'Ioptae'\s*,\s*Ioptae\s*,\s*0\s*,\s*2\s*\)",
        input1, re.IGNORECASE,
    ))
    check_40 = len(re.findall(
        r"Checkint\([^\n]*'Ioptae'\s*,\s*Ioptae\s*,\s*0\s*,\s*1\s*\)",
        input1, re.IGNORECASE,
    ))
    option2_branches = len(re.findall(
        r"\bIoptae\b\s*(?:\.eq\.|==)\s*2", all_source, re.IGNORECASE
    ))
    dispatch_ne_1 = len(re.findall(
        r"\bIoptae\b\s*(?:\.ne\.|/=)\s*1", animo, re.IGNORECASE
    ))
    dispatch_eq_1 = len(re.findall(
        r"\bIoptae\b\s*(?:\.eq\.|==)\s*1", animo, re.IGNORECASE
    ))

    values: list[int] = []
    comments: list[str] = []
    for text in testbank.values():
        for line in text.splitlines():
            match = re.match(r"\s*AerationModel\s*=\s*(\d+)(.*)", line, re.IGNORECASE)
            if match:
                values.append(int(match.group(1)))
                comments.append(match.group(2).strip())

    checks = {
        "animo41_parser_admits_2": check_41 == 1,
        "animo40_parser_stays_0_1": check_40 == 1,
        "main_dispatch_partitions_only_eq1_vs_ne1": dispatch_ne_1 >= 1 and dispatch_eq_1 >= 1,
        "no_explicit_option2_branch_sourcewide": option2_branches == 0,
        "testbank_advertises_option2": (
            len(values) == 12
            and all("2= option + adj. for denitrification" in comment for comment in comments)
        ),
        "testbank_has_no_active_option2_case": sum(value == 2 for value in values) == 0,
    }

    evidence = {
        "evidence_class": "SOURCE_AND_TESTBANK_STATIC_AUDIT",
        "source_sha256": SOURCE_SHA256,
        "testbank_sha256": TESTBANK_SHA256,
        "aeration_model": {
            "animo40_parser_range": "0..1",
            "animo41_parser_range": "0..2",
            "animo41_check_count": check_41,
            "animo40_check_count": check_40,
            "main_dispatch_ioptae_ne_1_count": dispatch_ne_1,
            "main_dispatch_ioptae_eq_1_count": dispatch_eq_1,
            "source_explicit_ioptae_eq_2_count": option2_branches,
            "testbank_records": len(values),
            "testbank_value_counts": dict(Counter(values)),
            "testbank_distinct_comments": sorted(set(comments)),
            "testbank_option2_active_cases": sum(value == 2 for value in values),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }

    output = json.dumps(evidence, indent=2) + "\n"
    print(output, end="")
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    return 0 if evidence["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
