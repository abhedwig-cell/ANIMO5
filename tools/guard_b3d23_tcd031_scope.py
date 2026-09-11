#!/usr/bin/env python3
import subprocess

BASE = "b68ebd807fbac2f8e8305417329e390fdab758d2"
ALLOWED = {
    ".github/workflows/animo-b3d23-tcd031-admission.yml",
    "docs/b3/TCD031_GOV05_TIER_C_ATOMIC_B3_ADMISSION.md",
    "integration/animo-b3/ANIMO-B3D23_CHECKPOINT.json",
    "integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3D23_RECONCILIATION.json",
    "integration/animo-b3/ANIMO-B3D23_STATUS.json",
    "integration/animo-b3/TCD031_B3_ADMISSION_CANDIDATE.json",
    "tools/guard_b3d23_tcd031_scope.py",
    "tools/validate_b3d23_tcd031_admission.py",
}

out = subprocess.check_output(["git", "diff", "--name-only", BASE, "HEAD"], text=True)
changed = {line.strip() for line in out.splitlines() if line.strip()}
unexpected = sorted(changed - ALLOWED)
if unexpected:
    raise SystemExit("B3D23 SCOPE FAIL_CLOSED: unexpected changed files: " + ", ".join(unexpected))

required = {
    ".github/workflows/animo-b3d23-tcd031-admission.yml",
    "docs/b3/TCD031_GOV05_TIER_C_ATOMIC_B3_ADMISSION.md",
    "integration/animo-b3/ANIMO-B3D23_CHECKPOINT.json",
    "integration/animo-b3/ANIMO-B3D23_RECONCILIATION.json",
    "integration/animo-b3/ANIMO-B3D23_STATUS.json",
    "integration/animo-b3/TCD031_B3_ADMISSION_CANDIDATE.json",
    "tools/guard_b3d23_tcd031_scope.py",
    "tools/validate_b3d23_tcd031_admission.py",
}
missing = sorted(required - changed)
if missing:
    raise SystemExit("B3D23 SCOPE FAIL_CLOSED: required workunit files absent from final-B3D22 delta: " + ", ".join(missing))

for forbidden_prefix in (
    "src/",
    "reference/",
    "integration/animo-reg/",
    "integration/animo-state/",
    "integration/animo-governance/",
):
    bad = sorted(p for p in changed if p.startswith(forbidden_prefix))
    if bad:
        raise SystemExit("B3D23 SCOPE FAIL_CLOSED: forbidden surface changed: " + ", ".join(bad))

protected_exact = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/B3_DISPOSITION_SCHEMA.json",
    "integration/animo-b3/ANIMO-B3B10R_STATUS.json",
    "integration/animo-b3/ANIMO-B3B10R2_STATUS.json",
}
if protected_exact & changed:
    raise SystemExit("B3D23 SCOPE FAIL_CLOSED: protected historical/register/schema artifact changed")

print("B3D23 scope PASS: only TCD-031 atomic admission governance artifacts changed from final B3D22 authority")
