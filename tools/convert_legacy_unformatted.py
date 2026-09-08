#!/usr/bin/env python3
"""Convert the observed legacy ANIMO/SWATRE single-byte record framing to
GNU Fortran's default 4-byte unformatted sequential record framing.

Qualification tooling only. This does not modify legacy scientific source.

Observed admitted framing in the PREP01 testbank:
  0x4b file header
  repeated: <1-byte record length><payload><same 1-byte record length>
  0x82 file trailer

The tool deliberately fails closed on high-bit/extended markers. The GHGMais
`result.bun` contains such records and is not admitted by this converter yet.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

HEADER = 0x4B
TRAILER = 0x82


class LegacyRecordError(ValueError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_simple_legacy_records(data: bytes) -> list[bytes]:
    if not data or data[0] != HEADER:
        raise LegacyRecordError("missing observed 0x4b legacy file header")
    if data[-1] != TRAILER:
        raise LegacyRecordError("missing observed 0x82 legacy file trailer")

    pos = 1
    records: list[bytes] = []
    while pos < len(data):
        marker = data[pos]
        pos += 1
        if marker == TRAILER:
            if pos != len(data):
                raise LegacyRecordError("bytes present after 0x82 file trailer")
            return records
        if marker & 0x80:
            raise LegacyRecordError(
                f"extended/high-bit record marker 0x{marker:02x} at offset {pos-1} is not admitted"
            )
        n = marker
        if pos + n >= len(data):
            raise LegacyRecordError(f"truncated record at offset {pos-1}")
        payload = data[pos:pos+n]
        pos += n
        trailing = data[pos]
        pos += 1
        if trailing != marker:
            raise LegacyRecordError(
                f"record marker mismatch at offset {pos-n-2}: 0x{marker:02x}/0x{trailing:02x}"
            )
        records.append(payload)
    raise LegacyRecordError("missing 0x82 file trailer")


def encode_gfortran_records(records: list[bytes]) -> bytes:
    out = bytearray()
    for payload in records:
        n = len(payload)
        out += struct.pack("<i", n)
        out += payload
        out += struct.pack("<i", n)
    return bytes(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    source = args.source.read_bytes()
    records = parse_simple_legacy_records(source)
    target = encode_gfortran_records(records)
    args.target.write_bytes(target)

    metadata = {
        "source": str(args.source),
        "target": str(args.target),
        "source_sha256": sha256(source),
        "target_sha256": sha256(target),
        "source_size": len(source),
        "target_size": len(target),
        "record_count": len(records),
        "record_lengths": sorted(set(map(len, records))),
        "transformation": "record-framing-only; payload bytes unchanged",
    }
    if args.metadata:
        args.metadata.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
