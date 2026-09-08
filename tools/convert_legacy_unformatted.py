#!/usr/bin/env python3
"""Convert Microsoft/Intel Fortran PowerStation-compatible sequential
unformatted records to GNU Fortran's default record framing.

Qualification tooling only. This does not modify legacy scientific source or
logical-record payload bytes.

PowerStation-compatible framing used by the supplied ANIMO hydrology files:
  0x4b file header
  repeated physical blocks:
      marker 0..128 : that many payload bytes and end of logical record
      marker 129    : 128 payload bytes and continuation of logical record
      trailing marker equal to the leading marker
  0x82 file trailer

A logical record may therefore contain more than one physical block. The
converter joins those physical blocks and writes one GNU logical record with
4-byte little-endian record markers around the unchanged payload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

HEADER = 0x4B
TRAILER = 0x82
CONTINUATION = 0x81
MAX_BLOCK_DATA = 128


class LegacyRecordError(ValueError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_powerstation_records(data: bytes) -> tuple[list[bytes], int]:
    """Return logical payload records and physical-block count.

    The parser fails closed on malformed framing. Payload bytes are never
    interpreted or modified.
    """
    if not data or data[0] != HEADER:
        raise LegacyRecordError("missing PowerStation 0x4b file header")
    if data[-1] != TRAILER:
        raise LegacyRecordError("missing PowerStation 0x82 file trailer")

    pos = 1
    records: list[bytes] = []
    current = bytearray()
    physical_blocks = 0

    while pos < len(data):
        marker_offset = pos
        marker = data[pos]
        pos += 1

        if marker == TRAILER:
            if current:
                raise LegacyRecordError(
                    "file trailer encountered inside continued logical record"
                )
            if pos != len(data):
                raise LegacyRecordError("bytes present after 0x82 file trailer")
            return records, physical_blocks

        if marker > CONTINUATION:
            raise LegacyRecordError(
                f"invalid physical-block marker 0x{marker:02x} at offset {marker_offset}"
            )

        payload_length = MAX_BLOCK_DATA if marker == CONTINUATION else marker
        if pos + payload_length >= len(data):
            raise LegacyRecordError(
                f"truncated physical block at offset {marker_offset}"
            )

        current += data[pos:pos + payload_length]
        pos += payload_length

        trailing = data[pos]
        pos += 1
        if trailing != marker:
            raise LegacyRecordError(
                f"physical-block marker mismatch at offset {marker_offset}: "
                f"0x{marker:02x}/0x{trailing:02x}"
            )

        physical_blocks += 1
        if marker != CONTINUATION:
            records.append(bytes(current))
            current.clear()

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
    records, physical_blocks = parse_powerstation_records(source)
    target = encode_gfortran_records(records)
    args.target.write_bytes(target)

    metadata = {
        "source": str(args.source),
        "target": str(args.target),
        "source_sha256": sha256(source),
        "target_sha256": sha256(target),
        "source_size": len(source),
        "target_size": len(target),
        "logical_record_count": len(records),
        "physical_block_count": physical_blocks,
        "logical_record_lengths": sorted(set(map(len, records))),
        "transformation": (
            "PowerStation physical-block framing to GNU logical-record framing; "
            "logical-record payload bytes unchanged"
        ),
    }
    if args.metadata:
        args.metadata.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
