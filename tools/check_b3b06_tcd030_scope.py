#!/usr/bin/env python3
import subprocess
from pathlib import Path

BASE = "eed822037ed8d906a2ab424220597cffac9cca73"
ALLOWED = {
    ".github/workflows/animo-b3b06-tcd030-readiness.yml",
    "docs/b3/TCD030_MACROPORE_NO3_VALIDATION_READINESS.md",
    "integration/animo-b3/ANIMO-B3B06_STATUS.json",
    "integration/animo-b3/TCD030_SOURCE_EVIDENCE.json",
    "integration/animo-b3/TCD030_VALIDATION_MATRIX.json",
    "tools/check_b3b06_tcd030_scope.py",
    "tools/validate_b3b06_tcd030.py",
}


def main():
    root = Path(__file__).resolve().parents[1]
    out = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASE}..HEAD"],
        cwd=root,
        text=True,
    )
    changed = {line.strip() for line in out.splitlines() if line.strip()}
    unexpected = changed - ALLOWED
    missing = ALLOWED - changed
    if unexpected:
        raise SystemExit("FAIL unexpected B3B06 paths: " + ", ".join(sorted(unexpected)))
    if missing:
        raise SystemExit("FAIL expected B3B06 paths missing from branch diff: " + ", ".join(sorted(missing)))
    print("PASS ANIMO-B3B06 scope guard")


if __name__ == "__main__":
    main()
