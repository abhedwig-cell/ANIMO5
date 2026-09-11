#!/usr/bin/env python3
import subprocess

BASE = "744c42119ee8cd21de658ef6d9c0ecf4a3f7d2ca"
ALLOWED = {
    ".github/workflows/animo-b3d23-tcd031-admission.yml",
    "docs/b3/TCD031_GOV05_TIER_C_ATOMIC_B3_ADMISSION.md",
    "integration/animo-b3/ANIMO-B3D23_CHECKPOINT.json",
    "integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json",
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
    "integration/animo-b3/ANIMO-B3D23_CHECKPOINT.json",
    "integration/animo-b3/TCD031_B3_ADMISSION_CANDIDATE.json",
    "docs/b3/TCD031_GOV05_TIER_C_ATOMIC_B3_ADMISSION.md",
    "tools/validate_b3d23_tcd031_admission.py",
    "tools/guard_b3d23_tcd031_scope.py",
    ".github/workflows/animo-b3d23-tcd031-admission.yml",
    "integration/animo-b3/ANIMO-B3D23_STATUS.json",
    "integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json",
}
missing = sorted(required - changed)
if missing:
    raise SystemExit("B3D23 SCOPE FAIL_CLOSED: required workunit files absent from branch delta: " + ", ".join(missing))

for forbidden_prefix in ("src/", "reference/", "integration/animo-reg/"):
    bad = sorted(p for p in changed if p.startswith(forbidden_prefix))
    if bad:
        raise SystemExit("B3D23 SCOPE FAIL_CLOSED: forbidden surface changed: " + ", ".join(bad))

print("B3D23 scope PASS: only atomic admission governance artifacts changed")
