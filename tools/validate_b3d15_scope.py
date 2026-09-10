#!/usr/bin/env python3
import subprocess

BASE = "e64f6ef936a08c8975a2c53000408b67dd03881d"
ALLOWED = {
    ".github/workflows/animo-b3d15-tcd030-admission.yml",
    "docs/b3/TCD030_GOV04_TIER_B_FORMAL_DISPOSITION_AND_ADMISSION.md",
    "integration/animo-b3/TCD030_GOV04_TIER_B_FORMAL_DISPOSITION.json",
    "integration/animo-b3/TCD030_B3_ADMISSION_CLOSEOUT.json",
    "integration/animo-b3/ANIMO-B3D15_STATUS.json",
    "tools/validate_b3d15_tcd030_admission.py",
    "tools/validate_b3d15_scope.py",
}
FORBIDDEN_PREFIXES = (
    "src/",
    "reference/source/",
    "integration/animo-reg/",
)
FORBIDDEN_EXACT = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_01.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_02.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_03.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_04.json",
}


def run(*args):
    return subprocess.check_output(args, text=True).strip()


try:
    subprocess.check_call(["git", "cat-file", "-e", f"{BASE}^{{commit}}"])
except subprocess.CalledProcessError:
    raise SystemExit("B3D15 FAIL_CLOSED: independent-review closeout base is unavailable; checkout must fetch full history")

changed = [p for p in run("git", "diff", "--name-only", f"{BASE}...HEAD").splitlines() if p]
if not changed:
    raise SystemExit("B3D15 FAIL_CLOSED: no B3D15 changes found")

unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3D15 FAIL_CLOSED: out-of-scope changed paths: " + ", ".join(unexpected))

for path in changed:
    if path.startswith(FORBIDDEN_PREFIXES) or path in FORBIDDEN_EXACT or path.lower().endswith((".for", ".f", ".f90", ".f95")):
        raise SystemExit(f"B3D15 FAIL_CLOSED: production/canonical/central-regie path changed: {path}")

required = {
    "docs/b3/TCD030_GOV04_TIER_B_FORMAL_DISPOSITION_AND_ADMISSION.md",
    "integration/animo-b3/TCD030_GOV04_TIER_B_FORMAL_DISPOSITION.json",
    "integration/animo-b3/TCD030_B3_ADMISSION_CLOSEOUT.json",
    "integration/animo-b3/ANIMO-B3D15_STATUS.json",
    "tools/validate_b3d15_tcd030_admission.py",
    "tools/validate_b3d15_scope.py",
}
missing = sorted(required - set(changed))
if missing:
    raise SystemExit("B3D15 FAIL_CLOSED: required admission artifacts missing from workunit diff: " + ", ".join(missing))

print("B3D15 scope PASS: only bounded TCD-030 disposition/admission evidence, validation and workflow paths changed; production, canonical register and central-regie surfaces remain closed.")
