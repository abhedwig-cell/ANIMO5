#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "ad1701e72ac51f61f81cc4e9a1857ab14bb8d8d8"
ALLOWED = {
    ".github/workflows/animo-b3d18-tcd028-admission.yml",
    "docs/b3/TCD028_B3_ADMISSION_CLOSEOUT.md",
    "integration/animo-b3/ANIMO-B3D18_STATUS.json",
    "integration/animo-b3/TCD028_B3_ADMISSION_CLOSEOUT.json",
    "tools/guard_b3d18_tcd028_scope.py",
    "tools/validate_b3d18_tcd028_admission.py",
}

changed = subprocess.check_output(
    ["git", "diff", "--name-only", f"{BASE}...HEAD"], text=True
).splitlines()
unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3D18 SCOPE FAIL: unexpected paths: " + ", ".join(unexpected))

for prefix in ("src/", "production/", "reference/", "ANIMO_4.1.5.53/"):
    if any(path.startswith(prefix) for path in changed):
        raise SystemExit(f"B3D18 SCOPE FAIL: protected path changed under {prefix}")

if "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" in changed:
    raise SystemExit("B3D18 SCOPE FAIL: canonical TCD register changed")
if "integration/animo-b3/B3_DISPOSITION_SCHEMA.json" in changed:
    raise SystemExit("B3D18 SCOPE FAIL: B3 schema changed")

print("B3D18 SCOPE PASS: admission-only files changed; no source, B0, canonical-register, composition, B4, production, or central-regie mutation.")
