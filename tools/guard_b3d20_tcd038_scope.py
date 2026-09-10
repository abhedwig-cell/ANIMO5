#!/usr/bin/env python3
import subprocess

BASE = "8deb1f45c58a9fa3151abc6422aa4f0e55d73a35"
ALLOWED = {
    ".github/workflows/animo-b3d20-tcd038-admission.yml",
    "docs/b3/TCD038_B3_ADMISSION_CLOSEOUT.md",
    "integration/animo-b3/ANIMO-B3D20_STATUS.json",
    "integration/animo-b3/TCD038_B3_ADMISSION_CLOSEOUT.json",
    "tools/guard_b3d20_tcd038_scope.py",
    "tools/validate_b3d20_tcd038_admission.py",
}

changed = subprocess.check_output(
    ["git", "diff", "--name-only", f"{BASE}...HEAD"], text=True
).splitlines()

unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3D20 SCOPE FAIL: unexpected paths: " + ", ".join(unexpected))

required = ALLOWED
missing = sorted(required - set(changed))
if missing:
    raise SystemExit("B3D20 SCOPE FAIL: incomplete admission package: " + ", ".join(missing))

for prefix in (
    "src/",
    "production/",
    "reference/",
    "ANIMO_4.1.5.53/",
    "docs/state/",
    "integration/animo-state/",
    "integration/animo-reg/",
    "docs/governance/ANIMO_RG05",
):
    if any(path.startswith(prefix) for path in changed):
        raise SystemExit(f"B3D20 SCOPE FAIL: protected path changed under {prefix}")

protected_exact = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/B3_DISPOSITION_SCHEMA.json",
    "integration/animo-reg/RG05_WORKUNIT_AUTHORITY.csv",
    "integration/animo-reg/RG05_B3_QUEUE.json",
    "integration/animo-reg/RG05_GATE_MATRIX.csv",
}
if any(path in protected_exact for path in changed):
    raise SystemExit("B3D20 SCOPE FAIL: canonical register, state, or central-regie artifact changed")

print("B3D20 SCOPE PASS: only atomic admission evidence/tooling changed; no source, frozen B0, canonical register/STATE, TCD-039 composition, B4, production, migration, or RG05H mutation.")
