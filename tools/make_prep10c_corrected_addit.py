#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_PARENT_SHA256 = "e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d"
EXPECTED_CANDIDATE_SHA256 = "a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae"

BRANCH = (
    b"          If (Pl(I) .Gt. 0)  Then\r\n\r\n"
    b"!     Summation of materials in ploughing layer (including reservoir)\r\n"
)
RESET_BRANCH = (
    b"          If (Pl(I) .Gt. 0)  Then\r\n"
    b"            SuStdiorma = 0.0\r\n"
    b"            SuStdiorni = 0.0\r\n"
    b"            If (Ipo.Eq.1) SuStdiorpo = 0.0\r\n\r\n"
    b"!     Summation of materials in ploughing layer (including reservoir)\r\n"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(source: bytes) -> bytes:
    actual = sha256_bytes(source)
    if actual != EXPECTED_PARENT_SHA256:
        raise ValueError(
            f"Addit.for SHA-256 mismatch: expected {EXPECTED_PARENT_SHA256}, got {actual}"
        )
    count = source.count(BRANCH)
    if count != 1:
        raise ValueError(f"expected exactly one plough branch insertion point, got {count}")
    candidate = source.replace(BRANCH, RESET_BRANCH, 1)
    candidate_hash = sha256_bytes(candidate)
    if candidate_hash != EXPECTED_CANDIDATE_SHA256:
        raise ValueError(
            f"candidate SHA-256 mismatch: expected {EXPECTED_CANDIDATE_SHA256}, got {candidate_hash}"
        )
    return candidate


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create the PREP10C event-reset corrected-legacy candidate Addit.for working copy."
    )
    ap.add_argument("addit_for", type=Path, help="Exact extracted revision-53 Addit.for")
    ap.add_argument("output", type=Path)
    ap.add_argument("--manifest", type=Path)
    ns = ap.parse_args()

    source = ns.addit_for.read_bytes()
    candidate = transform(source)
    ns.output.parent.mkdir(parents=True, exist_ok=True)
    ns.output.write_bytes(candidate)

    manifest = {
        "work_unit": "ANIMO-PREP10C",
        "evidence_class": "CORRECTED_LEGACY_CANDIDATE_NOT_ADMITTED",
        "parent_member": "ANIMO_4.1.5.53/Addit.for",
        "parent_sha256": EXPECTED_PARENT_SHA256,
        "parent_size_bytes": len(source),
        "candidate_sha256": sha256_bytes(candidate),
        "candidate_size_bytes": len(candidate),
        "candidate_crlf_count": candidate.count(b"\r\n"),
        "qualified_prep10_reset_counterfactual_sha256": EXPECTED_CANDIDATE_SHA256,
        "byte_identical_to_qualified_prep10_reset_counterfactual": True,
        "change": [
            "set SuStdiorma to zero at the start of each Pl(I)>0 event",
            "set SuStdiorni to zero at the start of each Pl(I)>0 event",
            "set SuStdiorpo to zero at the start of each Pl(I)>0 event when Ipo=1"
        ],
        "frozen_source_modified": False,
        "corrected_legacy_admitted": False,
        "production_migration_admitted": False
    }
    encoded = json.dumps(manifest, indent=2) + "\n"
    if ns.manifest:
        ns.manifest.parent.mkdir(parents=True, exist_ok=True)
        ns.manifest.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
