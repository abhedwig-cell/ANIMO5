#!/usr/bin/env python3
"""Fail-closed atomic scope guard for ANIMO-B3B05 / TCD-023.

The guard compares the current workunit against the immutable RG05E authoring
base. Only readiness evidence, validation tooling and its workflow may change.
Production source, frozen references, canonical registers and other TCD work
remain outside this workunit.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "eed822037ed8d906a2ab424220597cffac9cca73"

ALLOWED = {
    ".github/workflows/animo-b3b05-tcd023-readiness.yml",
    "docs/b3/TCD023_CLASS_B_ADMISSION_READINESS.md",
    "integration/animo-b3/ANIMO-B3B05_STATUS.json",
    "integration/animo-b3/TCD023_EXPECTED_DIFFERENCE.json",
    "integration/animo-b3/TCD023_INDEPENDENT_RECHECK.json",
    "integration/animo-b3/TCD023_READINESS_FIXTURE.json",
    "integration/animo-b3/TCD023_UPSTREAM_EVIDENCE.json",
    "tools/guard_b3b05_tcd023_scope.py",
    "tools/validate_b3b05_tcd023.py",
}

REQUIRED = {
    "docs/b3/TCD023_CLASS_B_ADMISSION_READINESS.md",
    "integration/animo-b3/ANIMO-B3B05_STATUS.json",
    "integration/animo-b3/TCD023_EXPECTED_DIFFERENCE.json",
    "integration/animo-b3/TCD023_INDEPENDENT_RECHECK.json",
    "integration/animo-b3/TCD023_READINESS_FIXTURE.json",
    "integration/animo-b3/TCD023_UPSTREAM_EVIDENCE.json",
    "tools/guard_b3b05_tcd023_scope.py",
    "tools/validate_b3b05_tcd023.py",
    ".github/workflows/animo-b3b05-tcd023-readiness.yml",
}

PROTECTED_PREFIXES = (
    "src/",
    "reference/",
    "production/",
    "ANIMO_4.1.5.53/",
)
PROTECTED_EXACT = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=True,
    )
    return result.stdout.strip()


def main() -> None:
    # Ensure the immutable base actually exists in this checkout before diffing.
    git("cat-file", "-e", f"{BASE}^{{commit}}")
    changed = {
        line.strip()
        for line in git("diff", "--name-only", BASE, "HEAD").splitlines()
        if line.strip()
    }

    print("ANIMO-B3B05 changed paths relative to RG05E:")
    for path in sorted(changed):
        print(f"  {path}")

    unexpected = changed - ALLOWED
    assert not unexpected, f"unexpected path(s) outside atomic scope: {sorted(unexpected)}"

    missing = {path for path in REQUIRED if not (ROOT / path).is_file()}
    assert not missing, f"required readiness artifact(s) missing: {sorted(missing)}"

    protected = {
        path for path in changed
        if path in PROTECTED_EXACT or path.startswith(PROTECTED_PREFIXES)
    }
    assert not protected, f"protected production/reference path(s) changed: {sorted(protected)}"

    # A TCD023 workunit may not silently carry sibling TCD artifacts.
    sibling_tcd = {
        path for path in changed
        if "TCD019" in path or "TCD024" in path or "TCD027" in path
    }
    assert not sibling_tcd, f"sibling TCD composition detected: {sorted(sibling_tcd)}"

    assert changed <= ALLOWED
    print("ANIMO-B3B05 atomic readiness scope guard: PASS")
    print(f"immutable authoring base: {BASE}")
    print("production/frozen/canonical-register changes: none")
    print("TCD-019/TCD-024/TCD-027 composition: none")


if __name__ == "__main__":
    main()
