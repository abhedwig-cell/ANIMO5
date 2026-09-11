#!/usr/bin/env python3
import subprocess

BASE = "7648e7b2813f3abc5904e4c34e36072d81d9844f"
ALLOWED = {
    ".github/workflows/animo-b3d22-tcd031-disposition.yml",
    "docs/b3/TCD031_GOV04_TIER_C_FORMAL_DISPOSITION.md",
    "integration/animo-b3/ANIMO-B3D22_CHECKPOINT.json",
    "integration/animo-b3/ANIMO-B3D22_STATUS.json",
    "integration/animo-b3/TCD031_TIER_C_FORMAL_DISPOSITION.json",
    "tools/guard_b3d22_tcd031_scope.py",
    "tools/validate_b3d22_tcd031_disposition.py",
}

changed = subprocess.check_output(
    ["git", "diff", "--name-only", f"{BASE}...HEAD"], text=True
).splitlines()
unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3D22 SCOPE FAIL: unexpected paths: " + ", ".join(unexpected))

for prefix in ("src/", "production/", "reference/", "ANIMO_4.1.5.53/"):
    if any(path.startswith(prefix) for path in changed):
        raise SystemExit(f"B3D22 SCOPE FAIL: protected path changed under {prefix}")

protected_exact = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/B3_DISPOSITION_SCHEMA.json",
    "integration/animo-state/STATEQ04_REMEDIATION_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3B10R_STATUS.json",
    "integration/animo-b3/ANIMO-B3B10R2_STATUS.json",
}
if any(path in protected_exact for path in changed):
    raise SystemExit("B3D22 SCOPE FAIL: protected authority/register/schema changed")

print("B3D22 SCOPE PASS: disposition-only paths changed; no source, B0, canonical register/state, TCD-025 composition, B3 admission, B4, production, tolerance, or central-regie mutation.")
