#!/usr/bin/env python3
"""Inspect the frozen GrassPeat initial-condition witness for TCD-040.

This tool does not contain or republish the testbank. It requires the caller to
supply the exact frozen testbank archive and fails closed on the archive and
member SHA-256 pins before interpreting the fixed GrassPeat layout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
MEMBER = "ANIMO_testbank/GrassPeat/Input/INITIAL.INP"
MEMBER_SHA256 = "969301b01c1d5e08aec70c9ad7f30a6a2d24555f4e2d8ea1acb1b557adc97753"
EXPECTED = {
    "Conh(0)": 0.006885736,
    "Coni(0)": 0.0005743774,
    "Codiorma(0)": 0.09904185,
    "Codiorni(0)": 0.005673512,
    "Codiorpo(0)": 0.0005456775,
    "Copo(0)": 0.003703004,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def numeric_records_after(lines: list[str], label: str) -> list[list[float]]:
    try:
        i = next(i for i, line in enumerate(lines) if line.strip().lower() == label.lower())
    except StopIteration as exc:
        raise SystemExit(f"required label absent: {label}") from exc
    records: list[list[float]] = []
    for line in lines[i + 1 :]:
        stripped = line.strip()
        if stripped.startswith(">"):
            break
        if not stripped or stripped.startswith("-"):
            continue
        try:
            records.append([float(token.replace("D", "E").replace("d", "e")) for token in stripped.split()])
        except ValueError:
            continue
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("testbank_zip", type=Path)
    args = parser.parse_args()

    archive = args.testbank_zip.resolve()
    actual = sha256_file(archive)
    if actual != TESTBANK_SHA256:
        raise SystemExit(f"testbank SHA-256 mismatch: {actual}")

    with zipfile.ZipFile(archive) as zf:
        try:
            payload = zf.read(MEMBER)
        except KeyError as exc:
            raise SystemExit(f"required member absent: {MEMBER}") from exc

    member_hash = sha256_bytes(payload)
    if member_hash != MEMBER_SHA256:
        raise SystemExit(f"GrassPeat INITIAL.INP SHA-256 mismatch: {member_hash}")

    text = payload.decode("latin1")
    lines = text.splitlines()
    ammoni = numeric_records_after(lines, ">ammoni:")
    nitrat = numeric_records_after(lines, ">nitrat:")
    orgsol = numeric_records_after(lines, ">orgsol:")
    inipho = numeric_records_after(lines, ">inipho:")

    if len(ammoni) < 1 or len(ammoni[0]) < 2:
        raise SystemExit("unexpected >ammoni: record layout")
    if len(nitrat) < 1 or len(nitrat[0]) < 2:
        raise SystemExit("unexpected >nitrat: record layout")
    if len(orgsol) < 2 or min(len(orgsol[0]), len(orgsol[1])) < 2:
        raise SystemExit("unexpected >orgsol: record layout")
    # Exact pinned GrassPeat layout under INPO=1:
    # record 0 INPO; 1 COPO; 2 one fast site; 3..5 three slow sites;
    # 6 precipitated P; 7 dissolved organic P.
    if len(inipho) != 8 or int(inipho[0][0]) != 1 or len(inipho[1]) < 2 or len(inipho[7]) < 2:
        raise SystemExit("unexpected >inipho: record layout")

    observed = {
        "Conh(0)": ammoni[0][1],
        "Coni(0)": nitrat[0][1],
        "Codiorma(0)": orgsol[0][1],
        "Codiorni(0)": orgsol[1][1],
        "Codiorpo(0)": inipho[7][1],
        "Copo(0)": inipho[1][1],
    }
    if observed != EXPECTED:
        raise SystemExit(f"GrassPeat layer-0 witness mismatch: {observed!r}")

    print(json.dumps({
        "testbank_sha256": actual,
        "member": MEMBER,
        "member_sha256": member_hash,
        "layer0_input_values": observed,
        "negative_control": "Copo(0)",
        "status": "HASH_PINNED_GRASSPEAT_INPUT_WITNESS_MATCH",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
