#!/usr/bin/env python3
"""Source-bound audit for the accepted-boundary NH4 adsorption reconstruction.

Qualification tooling only. This script verifies the exact frozen revision-53
source identity and the assignment structure supporting STATEQ01 N-002 as a
physical storage view with no independent accepted-boundary degree of freedom.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
ROOT = "ANIMO_4.1.5.53/"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    args = parser.parse_args()

    source_zip = args.source_zip.resolve()
    actual = sha256(source_zip)
    if actual != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"source archive SHA-256 mismatch: {actual}")

    with zipfile.ZipFile(source_zip) as archive:
        files = {
            name[len(ROOT):]: archive.read(name).decode("latin1", "ignore")
            for name in archive.namelist()
            if name.startswith(ROOT) and name.lower().endswith((".for", ".f90"))
        }

    required_fragments = {
        "Inicalc.for": [
            "Cxnh(Ln)=Rhbd(Ln)*Socfnh(Ln)*He(Ln)*Conh(Ln)",
        ],
        "TRANSPORT.FOR": [
            "Rscx(Ln)=He(Ln)*Rhbd(Ln)*Socf(Ln)*Rsc",
            "Rsco(Ln)=Rsc",
        ],
        "UBoundconc.for": [
            "Cxnh(1)=He(1)*Rhbd(1)*Socfnh(1)*Conh(1)",
        ],
        "Addit.for": [
            "Cxnh(Ln)=He(Ln)*Rhbd(Ln)*Socfnh(Ln)*Conh(Ln)",
            "Cxnh(Ln)=Rhbd(Ln)*Socfnh(Ln)*Conh(Ln)*He(Ln)",
        ],
        "Init.for": [
            "Cxnh(Ln)=Rscxnh(Ln)",
        ],
    }

    checks = []
    for filename, fragments in required_fragments.items():
        text = normalized(files[filename])
        for fragment in fragments:
            present = normalized(fragment) in text
            checks.append({"file": filename, "fragment": fragment, "present": present})
            if not present:
                raise SystemExit(f"missing required source fragment in {filename}: {fragment}")

    # Rscxnh is an actual argument at the AMMONIUM Transport call and is not
    # assigned independently elsewhere except initialization/reset/copy sites.
    rscxnh_assignment_sites = []
    assignment_re = re.compile(r"(?im)^\s*rscxnh\s*\([^\n=]*\)\s*=")
    for filename, text in files.items():
        for match in assignment_re.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            rscxnh_assignment_sites.append({"file": filename, "line": line})

    # Revision 53 should not contain a direct independent Rscxnh mutation in a
    # process routine. Init may reset it before the first transport calculation.
    allowed_direct_files = {"Init.for"}
    unexpected = [x for x in rscxnh_assignment_sites if x["file"] not in allowed_direct_files]
    if unexpected:
        raise SystemExit(f"unexpected direct Rscxnh assignment site(s): {unexpected}")

    result = {
        "workunit": "ANIMO-STATEQ01",
        "evidence_class": "SOURCE_BOUND_CHECKPOINT_RECONSTRUCTION_AUDIT",
        "source_sha256": actual,
        "required_fragments": checks,
        "direct_rscxnh_assignment_sites": rscxnh_assignment_sites,
        "unexpected_direct_process_assignments": unexpected,
        "conclusion": "NH4_ADSORBED_ACCEPTED_BOUNDARY_COORDINATE_HAS_SOURCE_DEFINED_EQUILIBRIUM_RECONSTRUCTION",
        "b3_split_run_admitted": False,
        "production_change": False,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
