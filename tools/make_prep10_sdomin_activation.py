#!/usr/bin/env python3
"""Create a controlled PREP10 sdomin diagnostic input descendant.

This tool never edits B0 in place. It consumes an extracted/working-copy ANIMO
Initial.inp, verifies the exact parent SHA-256 supplied by the caller, changes
only selected tokens in the three lines immediately following the unique
>sdomin: marker, and writes a new file plus an optional transform manifest.

The default amplitudes are diagnostic activation values only. They carry no
claim of scientific realism and do not create B0, reference, corrected-legacy,
or ANIMO5 production evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

NUMBER = re.compile(rb"[-+]?(?:(?:\d+\.\d*)|(?:\.\d+)|(?:\d+))(?:[EeDd][-+]?\d+)?")
DEFAULT_VALUES = {
    "stable_dom": "1.000000E-04",
    "stable_don": "1.000000E-05",
    "stable_dop": "1.000000E-06",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_indices(text: str) -> list[int]:
    values = [int(item.strip()) for item in text.split(",") if item.strip()]
    if not values or any(value < 0 for value in values):
        raise ValueError("indices must contain one or more non-negative integers")
    if len(set(values)) != len(values):
        raise ValueError("indices must be unique")
    return values


def replace_selected_tokens(
    line: bytes,
    *,
    indices: list[int],
    replacement: str,
    require_zero: bool = True,
) -> tuple[bytes, list[str]]:
    matches = list(NUMBER.finditer(line))
    if max(indices) >= len(matches):
        raise ValueError(
            f"requested index {max(indices)} but line has only {len(matches)} numeric tokens"
        )

    replacement_bytes = replacement.encode("ascii")
    old_values: list[str] = []
    chunks: list[bytes] = []
    cursor = 0
    selected = set(indices)
    for index, match in enumerate(matches):
        chunks.append(line[cursor : match.start()])
        token = match.group(0)
        if index in selected:
            old_text = token.decode("ascii")
            old_values.append(old_text)
            if require_zero and float(old_text.replace("D", "E").replace("d", "e")) != 0.0:
                raise ValueError(
                    f"selected sdomin token {index} is not zero: {old_text}"
                )
            if len(replacement_bytes) != len(token):
                raise ValueError(
                    "replacement token width differs from parent token width; "
                    "this controlled transform requires byte-length preservation"
                )
            chunks.append(replacement_bytes)
        else:
            chunks.append(token)
        cursor = match.end()
    chunks.append(line[cursor:])
    return b"".join(chunks), old_values


def transform(
    data: bytes,
    *,
    expected_parent_sha256: str,
    indices: list[int],
    dom: str = DEFAULT_VALUES["stable_dom"],
    don: str = DEFAULT_VALUES["stable_don"],
    dop: str = DEFAULT_VALUES["stable_dop"],
) -> tuple[bytes, dict]:
    actual_parent = sha256_bytes(data)
    if actual_parent != expected_parent_sha256.lower():
        raise ValueError(
            f"parent SHA-256 mismatch: expected {expected_parent_sha256}, got {actual_parent}"
        )

    lines = data.splitlines(keepends=True)
    marker_indices = [
        index for index, line in enumerate(lines) if line.strip().lower() == b">sdomin:"
    ]
    if len(marker_indices) != 1:
        raise ValueError(f"expected exactly one >sdomin: marker, got {len(marker_indices)}")
    marker = marker_indices[0]
    if marker + 3 >= len(lines):
        raise ValueError("incomplete sdomin block")

    definitions = [
        ("stable_dom", dom),
        ("stable_don", don),
        ("stable_dop", dop),
    ]
    changes = []
    for offset, (species, replacement) in enumerate(definitions, start=1):
        line_index = marker + offset
        replaced, old_values = replace_selected_tokens(
            lines[line_index],
            indices=indices,
            replacement=replacement,
            require_zero=True,
        )
        lines[line_index] = replaced
        changes.append(
            {
                "species": species,
                "line_1_based": line_index + 1,
                "indices_0_based": indices,
                "old_values": old_values,
                "new_value": replacement,
            }
        )

    descendant = b"".join(lines)
    if len(descendant) != len(data):
        raise ValueError("controlled transform unexpectedly changed file size")

    manifest = {
        "evidence_class": "DIAGNOSTIC_INPUT_DESCENDANT_NOT_B0_NOT_REFERENCE",
        "transform": "PREP10_STABLE_DOM_CONTROLLED_ACTIVATION",
        "parent_sha256": actual_parent,
        "descendant_sha256": sha256_bytes(descendant),
        "size_bytes": len(descendant),
        "sdomin_marker_line_1_based": marker + 1,
        "indices_0_based": indices,
        "changes": changes,
        "scientific_realism_claimed": False,
        "b0_modified": False,
        "reference_qualified": False,
        "corrected_legacy_admitted": False,
        "production_migration_admitted": False,
    }
    return descendant, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_initial", type=Path)
    parser.add_argument("output_initial", type=Path)
    parser.add_argument("--expected-parent-sha256", required=True)
    parser.add_argument("--indices", default="0,1,2")
    parser.add_argument("--dom", default=DEFAULT_VALUES["stable_dom"])
    parser.add_argument("--don", default=DEFAULT_VALUES["stable_don"])
    parser.add_argument("--dop", default=DEFAULT_VALUES["stable_dop"])
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    try:
        indices = parse_indices(args.indices)
        descendant, manifest = transform(
            args.input_initial.read_bytes(),
            expected_parent_sha256=args.expected_parent_sha256,
            indices=indices,
            dom=args.dom,
            don=args.don,
            dop=args.dop,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    args.output_initial.parent.mkdir(parents=True, exist_ok=True)
    args.output_initial.write_bytes(descendant)
    encoded = json.dumps(manifest, indent=2) + "\n"
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
