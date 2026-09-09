#!/usr/bin/env python3
"""Extract the shared legacy mass-balance term index map from outbal*.inc.

Qualification tooling only. The source archive is SHA-bound before parsing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import tempfile
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_outbal1(text: str) -> dict[str, int]:
    m = re.search(
        r"Data\s+Stsn_b,Stpn_b,Stsm_b,Inip_x,Inip_l,Inip_p\s*&\s*\n"
        r"\s*&\s*/\s*([^/]+)/",
        text,
        re.IGNORECASE,
    )
    if not m:
        raise ValueError("outbal1 storage-index DATA statement not found")
    values = [int(x) for x in re.findall(r"-?\d+", m.group(1))]
    names = ["Stsn_b", "Stpn_b", "Stsm_b", "Inip_x", "Inip_l", "Inip_p"]
    if len(values) != len(names):
        raise ValueError("unexpected outbal1 storage-index count")
    return dict(zip(names, values))


def parse_outbal2(text: str) -> dict[str, int]:
    m = re.search(r"Data\s+(.*?)\s*&?\s*/\s*(.*?)\s*/", text, re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError("outbal2 DATA statement not found")

    names_text = re.sub(r"!.*", "", m.group(1))
    values_text = re.sub(r"!.*", "", m.group(2))
    names: list[str] = []
    for token in names_text.replace("&", " ").split(","):
        token = token.strip()
        if not token:
            continue
        mm = re.match(r"(\w+)(?:\((\d+)\))?$", token)
        if not mm:
            continue
        names.append(f"{mm.group(1)}({mm.group(2)})" if mm.group(2) else mm.group(1))

    values = [int(x) for x in re.findall(r"\d+", values_text)]
    if len(names) != len(values):
        raise ValueError(f"outbal2 name/value count mismatch: {len(names)} vs {len(values)}")
    return dict(zip(names, values))


def extract_mapping(archive: Path) -> list[tuple[int, str]]:
    digest = sha256_file(archive)
    if digest != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source SHA-256 mismatch: {digest}")

    with tempfile.TemporaryDirectory(prefix="animo_balance_index_") as td:
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(td)
        roots = [p for p in Path(td).iterdir() if p.is_dir()]
        if len(roots) != 1:
            raise ValueError("expected one source root in archive")
        root = roots[0]
        mapping = parse_outbal1((root / "outbal1.inc").read_text("latin-1"))
        mapping.update(parse_outbal2((root / "outbal2.inc").read_text("latin-1")))

    by_index = {index: symbol for symbol, index in mapping.items()}
    if len(by_index) != len(mapping):
        raise ValueError("duplicate balance index")
    if sorted(by_index) != list(range(1, 75)):
        raise ValueError("balance index map is not complete for 1..74")
    return [(index, by_index[index]) for index in range(1, 75)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()

    rows = extract_mapping(args.archive)
    if args.csv:
        with args.csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["index", "symbol"])
            writer.writerows(rows)
    for index, symbol in rows:
        print(f"{index:02d},{symbol}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
