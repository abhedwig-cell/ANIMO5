#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess

ALLOWED = {
    ".github/workflows/animo-b3b07-tcd041-readiness.yml",
    "docs/b3/TCD041_GHG_LOWER_AIR_BOUNDARY_RISK_AND_READINESS.md",
    "integration/animo-b3/ANIMO-B3B07_STATUS.json",
    "integration/animo-b3/TCD041_RISK_CLASSIFICATION.json",
    "integration/animo-b3/TCD041_EVIDENCE_MATRIX.json",
    "integration/animo-b3/TCD041_INDEPENDENT_REVIEW_HANDOFF.json",
    "tools/b3b07/tcd041_activation_probe.py",
    "tools/validate_b3b07_tcd041.py",
    "tools/validate_b3b07_scope.py",
}
FORBIDDEN_PREFIXES = (
    "ANIMO_4.1.5.53/",
    "source/",
    "src/",
)
FORBIDDEN_EXACT = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()

    out = subprocess.check_output(
        ["git", "diff", "--name-only", f"{args.base}..HEAD"], text=True
    )
    changed = {line.strip() for line in out.splitlines() if line.strip()}

    unexpected = sorted(changed - ALLOWED)
    if unexpected:
        raise SystemExit("B3B07 scope FAIL unexpected paths: " + ", ".join(unexpected))
    if not changed:
        raise SystemExit("B3B07 scope FAIL no workunit files changed")
    for path in changed:
        if path in FORBIDDEN_EXACT or path.startswith(FORBIDDEN_PREFIXES):
            raise SystemExit("B3B07 scope FAIL forbidden path: " + path)
        if path.lower().endswith((".for", ".f90", ".f", ".f95")):
            raise SystemExit("B3B07 scope FAIL production/source Fortran changed: " + path)
    print("ANIMO-B3B07 scope guard PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
