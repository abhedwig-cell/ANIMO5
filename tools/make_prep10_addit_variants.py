#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_ADDIT_SHA256 = "e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d"

BRANCH = b"          If (Pl(I) .Gt. 0)  Then\r\n\r\n!     Summation of materials in ploughing layer (including reservoir)\r\n"
END_LOOP = b"            End Do\r\n\r\n            Sumo = 0.0\r\n"

OBSERVER_BRANCH = b"          If (Pl(I) .Gt. 0)  Then\r\n            Write(*,*) 'PREP10_BEFORE',I,Pl(I),SuStdiorma,SuStdiorni,SuStdiorpo\r\n\r\n!     Summation of materials in ploughing layer (including reservoir)\r\n"
OBSERVER_END = b"            End Do\r\n            Write(*,*) 'PREP10_AFTER',I,Pl(I),SuStdiorma,SuStdiorni,SuStdiorpo\r\n\r\n            Sumo = 0.0\r\n"
RESET_BRANCH = b"          If (Pl(I) .Gt. 0)  Then\r\n            SuStdiorma = 0.0\r\n            SuStdiorni = 0.0\r\n            If (Ipo.Eq.1) SuStdiorpo = 0.0\r\n\r\n!     Summation of materials in ploughing layer (including reservoir)\r\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_variants(source: bytes) -> tuple[bytes, bytes]:
    if source.count(BRANCH) != 1:
        raise ValueError(f"expected exactly one plough branch insertion point, got {source.count(BRANCH)}")
    if source.count(END_LOOP) != 1:
        raise ValueError(f"expected exactly one post-accumulation insertion point, got {source.count(END_LOOP)}")
    observer = source.replace(BRANCH, OBSERVER_BRANCH, 1).replace(END_LOOP, OBSERVER_END, 1)
    reset = source.replace(BRANCH, RESET_BRANCH, 1)
    return observer, reset


def main() -> int:
    ap = argparse.ArgumentParser(description="Create PREP10 observer and reset-counterfactual Addit.for working-copy variants.")
    ap.add_argument("addit_for", type=Path, help="Exact extracted B0 Addit.for working copy")
    ap.add_argument("output_dir", type=Path)
    ns = ap.parse_args()

    source = ns.addit_for.read_bytes()
    actual = sha256_bytes(source)
    if actual != EXPECTED_ADDIT_SHA256:
        raise SystemExit(f"Addit.for SHA-256 mismatch: expected {EXPECTED_ADDIT_SHA256}, got {actual}")
    if b"\r\n" not in source:
        raise SystemExit("expected CRLF-preserved frozen Addit.for working copy")

    observer, reset = make_variants(source)
    ns.output_dir.mkdir(parents=True, exist_ok=True)
    observer_path = ns.output_dir / "Addit_observer.for"
    reset_path = ns.output_dir / "Addit_reset_counterfactual.for"
    observer_path.write_bytes(observer)
    reset_path.write_bytes(reset)

    result = {
        "evidence_class": "DIAGNOSTIC_WORKING_COPY_TRANSFORMS",
        "parent_addit_sha256": actual,
        "parent_size_bytes": len(source),
        "parent_crlf_count": source.count(b"\r\n"),
        "observer": {
            "path": observer_path.name,
            "sha256": sha256_bytes(observer),
            "size_bytes": len(observer),
            "crlf_count": observer.count(b"\r\n"),
            "semantic_change": "writes accumulator values immediately before and after the plough accumulation loop; no model-state assignment added"
        },
        "reset_counterfactual": {
            "path": reset_path.name,
            "sha256": sha256_bytes(reset),
            "size_bytes": len(reset),
            "crlf_count": reset.count(b"\r\n"),
            "semantic_change": "sets the three stable-DOM plough accumulators to zero at the start of each plough event; diagnostic counterfactual only, not corrected-legacy admission"
        },
        "frozen_source_modified": False
    }
    print(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
