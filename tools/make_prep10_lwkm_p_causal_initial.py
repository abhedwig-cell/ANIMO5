#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_PARENT_SHA256 = "0e6bb1d30c46c3aa8c7dcd077c06845afebcb6bd8b576c0df24e037382dfa483"
EXPECTED_OUTPUT_SHA256 = "1efe16d5e8c3e685ad22168132da4ffa789c4f982e8c178640a97fff14fd4e48"
ACTIVATION_VALUE = 1.0e-4
TARGET_INDICES = (1, 2)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform_initial(raw: bytes) -> bytes:
    lines = raw.decode("latin1").splitlines(keepends=True)
    markers = [i for i, line in enumerate(lines) if line.strip().lower() == ">sdomin:"]
    if len(markers) != 1:
        raise ValueError(f"expected exactly one >sdomin: marker, got {len(markers)}")
    marker = markers[0]
    dop_row = marker + 3
    if dop_row >= len(lines):
        raise ValueError("incomplete >sdomin: block")

    line = lines[dop_row]
    if line.endswith("\r\n"):
        newline = "\r\n"
    elif line.endswith("\n"):
        newline = "\n"
    else:
        newline = ""
    body = line[:-len(newline)] if newline else line
    tokens = body.split()
    if len(tokens) != 31:
        raise ValueError(
            f"expected 31 stable-DOP values for frozen LWKM layout, got {len(tokens)}"
        )
    for index in TARGET_INDICES:
        if float(tokens[index].replace("D", "E").replace("d", "e")) != 0.0:
            raise ValueError(f"expected frozen zero at stable-DOP index {index}")
        tokens[index] = f"{ACTIVATION_VALUE:.6E}"
    lines[dop_row] = "    " + "    ".join(tokens) + newline
    return "".join(lines).encode("latin1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_inp", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    raw = args.initial_inp.read_bytes()
    parent = sha256_bytes(raw)
    if parent != EXPECTED_PARENT_SHA256:
        raise SystemExit(f"parent Initial.inp SHA-256 mismatch: {parent}")

    output = transform_initial(raw)
    digest = sha256_bytes(output)
    if digest != EXPECTED_OUTPUT_SHA256:
        raise SystemExit(
            f"descendant SHA-256 mismatch: expected {EXPECTED_OUTPUT_SHA256}, got {digest}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)
    metadata = {
        "evidence_class": "DIAGNOSTIC_INPUT_DESCENDANT_NOT_B0_NOT_REFERENCE",
        "testcase": "LWKM_gras_1040.2021.2045",
        "parent_sha256": parent,
        "changed_vector": "CoStdiorpo",
        "changed_compartment_indices": list(TARGET_INDICES),
        "activation_value": ACTIVATION_VALUE,
        "output_sha256": digest,
        "size_bytes": len(output),
        "frozen_parent_modified": False,
        "physical_representativeness_claimed": False,
    }
    encoded = json.dumps(metadata, indent=2) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
