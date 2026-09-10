#!/usr/bin/env python3
import subprocess

BASE = "3587c7a94a992f3779034c4c1e5f4134192d54f3"
ALLOWED = {
    ".github/workflows/animo-b3d14-tcd041-admission.yml",
    "docs/b3/TCD041_GOV04_TIER_B_FORMAL_DISPOSITION_AND_ADMISSION.md",
    "integration/animo-b3/TCD041_GOV04_TIER_B_FORMAL_DISPOSITION.json",
    "integration/animo-b3/TCD041_B3_ADMISSION_CLOSEOUT.json",
    "integration/animo-b3/ANIMO-B3D14_STATUS.json",
    "tools/validate_b3d14_tcd041_admission.py",
    "tools/validate_b3d14_scope.py",
}
FORBIDDEN_PREFIXES = ("src/", "reference/source/", "integration/animo-reg/")
FORBIDDEN_EXACT = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_04.json",
}


def run(*args):
    return subprocess.check_output(args, text=True).strip()

try:
    subprocess.check_call(["git", "cat-file", "-e", f"{BASE}^{{commit}}"])
except subprocess.CalledProcessError:
    raise SystemExit("B3D14 FAIL_CLOSED: review-handoff base commit is unavailable; checkout must fetch full history")

changed = [p for p in run("git", "diff", "--name-only", f"{BASE}...HEAD").splitlines() if p]
if not changed:
    raise SystemExit("B3D14 FAIL_CLOSED: no B3D14 changes found")

unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3D14 FAIL_CLOSED: out-of-scope changed paths: " + ", ".join(unexpected))

for path in changed:
    if path.startswith(FORBIDDEN_PREFIXES) or path in FORBIDDEN_EXACT or path.lower().endswith((".for", ".f", ".f90", ".f95")):
        raise SystemExit(f"B3D14 FAIL_CLOSED: production/canonical path changed: {path}")

required = {
    "docs/b3/TCD041_GOV04_TIER_B_FORMAL_DISPOSITION_AND_ADMISSION.md",
    "integration/animo-b3/TCD041_GOV04_TIER_B_FORMAL_DISPOSITION.json",
    "integration/animo-b3/TCD041_B3_ADMISSION_CLOSEOUT.json",
    "integration/animo-b3/ANIMO-B3D14_STATUS.json",
    "tools/validate_b3d14_tcd041_admission.py",
    "tools/validate_b3d14_scope.py",
}
missing = sorted(required - set(changed))
if missing:
    raise SystemExit("B3D14 FAIL_CLOSED: required admission artifacts missing from workunit diff: " + ", ".join(missing))

print("B3D14 scope PASS: only bounded disposition/admission evidence, validation and workflow paths changed; production and central-regie surfaces remain closed.")
