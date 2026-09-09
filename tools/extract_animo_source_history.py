#!/usr/bin/env python3
"""Extract source-history provenance from the frozen ANIMO revision-53 archive.

This tool is evidence-only. It does not modify source members.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import sys
import zipfile

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
FIELDS = [
    "file",
    "id_revision",
    "id_date",
    "id_author",
    "headurl_tag",
    "history_years",
    "explicit_release_markers",
    "notable_scope",
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_member(name: str, data: bytes) -> dict[str, str]:
    text = data.decode("latin1", errors="replace")
    lines = text.splitlines()
    head = "\n".join(lines[:200])

    id_revision = ""
    id_date = ""
    id_author = ""
    id_match = re.search(r"\$Id:\s*([^\r\n$]+)", head, re.I)
    if id_match:
        id_text = id_match.group(1).strip()
        parsed = re.search(
            r"\b(\d+)\s+(\d{4}-\d{2}-\d{2})\s+\S+\s+([A-Za-z0-9_.-]+)\s*$",
            id_text,
        )
        if parsed:
            id_revision, id_date, id_author = parsed.groups()

    headurl_tag = ""
    headurl_match = re.search(r"\$HeadURL:\s*([^\r\n$]+)", head, re.I)
    if headurl_match:
        tag_match = re.search(r"/tags/([^/\s]+)", headurl_match.group(1), re.I)
        if tag_match:
            headurl_tag = tag_match.group(1)

    years = sorted(set(re.findall(r"\b(19\d{2}|20\d{2})\b", head)))

    markers: list[str] = []
    seen: set[str] = set()
    for line in lines[:200]:
        cleaned = line.strip(" !.\t")
        if re.search(r"Release\s+of\s+ANIMO", line, re.I) or re.search(
            r"ANIMO\s*3\.7\.5", line, re.I
        ):
            if cleaned not in seen:
                seen.add(cleaned)
                markers.append(cleaned)

    low = head.lower()
    filename = os.path.basename(name)
    scopes: list[str] = []
    if "stable dom" in low or "sdo-pool" in low or "recfsdo" in low:
        scopes.append("stable_DOM")
    if "ghg" in low or "greenhouse" in low:
        scopes.append("GHG")
    if "macropore" in low or "mapo" in filename.lower():
        scopes.append("macropore")
    if "emw2012" in low or "pclass" in low or "pklasse" in low:
        scopes.append("PClass_EMW2012")
    if "soiltemp" in low or filename.lower() == "input_soiltemp.for":
        scopes.append("soil_temperature")

    return {
        "file": filename,
        "id_revision": id_revision,
        "id_date": id_date,
        "id_author": id_author,
        "headurl_tag": headurl_tag,
        "history_years": "|".join(years),
        "explicit_release_markers": " | ".join(markers),
        "notable_scope": "|".join(scopes),
    }


def extract(path: str) -> list[dict[str, str]]:
    actual = sha256_file(path)
    if actual != EXPECTED_SOURCE_SHA256:
        raise ValueError(
            f"source SHA-256 mismatch: expected {EXPECTED_SOURCE_SHA256}, got {actual}"
        )

    rows: list[dict[str, str]] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            rows.append(parse_member(name, zf.read(name)))
    return rows


def render_csv(rows: list[dict[str, str]]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip")
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        rows = extract(args.source_zip)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    csv_text = render_csv(rows)
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            f.write(csv_text)
    else:
        sys.stdout.write(csv_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
