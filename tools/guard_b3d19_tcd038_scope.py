#!/usr/bin/env python3
import subprocess

BASE = "4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
ALLOWED = {
    ".github/workflows/animo-b3d19-tcd038-disposition.yml",
    "docs/b3/TCD038_GOV04_TIER_C_FORMAL_DISPOSITION.md",
    "integration/animo-b3/ANIMO-B3D19_STATUS.json",
    "integration/animo-b3/TCD038_TIER_C_FORMAL_DISPOSITION.json",
    "tools/guard_b3d19_tcd038_scope.py",
    "tools/validate_b3d19_tcd038_disposition.py",
}

changed = subprocess.check_output(
    ["git", "diff", "--name-only", f"{BASE}...HEAD"], text=True
).splitlines()
unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3D19 SCOPE FAIL: unexpected paths: " + ", ".join(unexpected))

for prefix in ("src/", "production/", "reference/", "ANIMO_4.1.5.53/"):
    if any(path.startswith(prefix) for path in changed):
        raise SystemExit(f"B3D19 SCOPE FAIL: protected path changed under {prefix}")

protected_exact = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/B3_DISPOSITION_SCHEMA.json",
}
if any(path in protected_exact for path in changed):
    raise SystemExit("B3D19 SCOPE FAIL: canonical register/schema changed")

print("B3D19 SCOPE PASS: disposition-only paths changed; no source, B0, canonical register/state, TCD-039 composition, B4, production, or central-regie mutation.")
