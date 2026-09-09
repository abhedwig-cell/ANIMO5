#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_PARENT_SHA256 = "8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201"
VARIANTS = {
    "dom": {
        "values": (1e-2, 0.0, 0.0),
        "expected_sha256": "d66acd69d62c2cfded22d581048a25b365b81d9972aa1a3a31fd55047d712f04",
    },
    "don": {
        "values": (0.0, 1e-3, 0.0),
        "expected_sha256": "a3e1349bba096d769438e62635f9408046d858c611ebdf5decb498afd1f30455",
    },
    "dop": {
        "values": (0.0, 0.0, 1e-4),
        "expected_sha256": "e9b3024ee98536ef563ac7929ce2af082c4b5d54b71bf36e02441ef77f1846a3",
    },
    "combined": {
        "values": (1e-2, 1e-3, 1e-4),
        "expected_sha256": "3e11b78441d30d207420c96adf55dd3dd5c4d1430febdaf166bead8254602c73",
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform_initial(raw: bytes, values: tuple[float, float, float]) -> bytes:
    lines = raw.decode("latin1").splitlines(keepends=True)
    markers = [i for i, line in enumerate(lines) if line.strip().lower() == ">sdomin:"]
    if len(markers) != 1:
        raise ValueError(f"expected exactly one >sdomin: marker, got {len(markers)}")
    marker = markers[0]
    if marker + 3 >= len(lines):
        raise ValueError("incomplete >sdomin: block")

    for row, value in zip(range(marker + 1, marker + 4), values):
        line = lines[row]
        if line.endswith("\r\n"):
            newline = "\r\n"
        elif line.endswith("\n"):
            newline = "\n"
        else:
            newline = ""
        body = line[:-len(newline)] if newline else line
        tokens = body.split()
        if len(tokens) != 23:
            raise ValueError(
                f"expected 23 values on sdomin row {row + 1}, got {len(tokens)}"
            )
        tokens[1] = f"{value:.6E}"
        tokens[2] = f"{value:.6E}"
        lines[row] = "    " + "    ".join(
            f"{float(token):.6E}" for token in tokens
        ) + newline

    return "".join(lines).encode("latin1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_inp", type=Path)
    parser.add_argument("variant", choices=sorted(VARIANTS))
    parser.add_argument("output", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    raw = args.initial_inp.read_bytes()
    parent = sha256_bytes(raw)
    if parent != EXPECTED_PARENT_SHA256:
        raise SystemExit(f"parent Initial.inp SHA-256 mismatch: {parent}")

    spec = VARIANTS[args.variant]
    output = transform_initial(raw, spec["values"])
    digest = sha256_bytes(output)
    if digest != spec["expected_sha256"]:
        raise SystemExit(
            "descendant SHA-256 mismatch: "
            f"expected {spec['expected_sha256']}, got {digest}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)

    metadata = {
        "evidence_class": "DIAGNOSTIC_INPUT_DESCENDANT_NOT_B0_NOT_REFERENCE",
        "parent_sha256": parent,
        "variant": args.variant,
        "changed_compartment_indices": [1, 2],
        "values": {
            "CoStdiorma": spec["values"][0],
            "CoStdiorni": spec["values"][1],
            "CoStdiorpo": spec["values"][2],
        },
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
