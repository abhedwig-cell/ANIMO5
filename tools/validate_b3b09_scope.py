#!/usr/bin/env python3
import subprocess

BASE = "7c61a5031f41d602e996310df6f3958cbd1b511e"
ALLOWED = {
    ".github/workflows/animo-b3b09-tcd038-readiness.yml",
    "docs/b3/TCD038_GOV04_TIER_C_ADMISSION_READINESS.md",
    "integration/animo-b3/TCD038_READINESS_EVIDENCE.json",
    "integration/animo-b3/ANIMO-B3B09_STATUS.json",
    "integration/animo-b3/TCD038_INDEPENDENT_REVIEW_HANDOFF.json",
    "tools/validate_b3b09_tcd038_readiness.py",
    "tools/validate_b3b09_scope.py",
}
FORBIDDEN_PREFIXES = (
    "src/",
    "reference/",
    "integration/animo-reg/",
    "docs/state/",
    "integration/animo-state/",
    "docs/b4/",
    "integration/animo-b4/",
    "production/",
)
FORBIDDEN_EXACT = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_01.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_02.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_03.json",
    "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_04.json",
    "integration/animo-reg/ANIMO-RG05F_STATUS.json",
    "integration/animo-reg/ANIMO-RG05G_STATUS.json",
}


def run(*args):
    return subprocess.check_output(args, text=True).strip()

try:
    subprocess.check_call(["git", "cat-file", "-e", f"{BASE}^{{commit}}"])
except subprocess.CalledProcessError:
    raise SystemExit("B3B09 FAIL_CLOSED: RG05F base unavailable; full history is required")

changed = [p for p in run("git", "diff", "--name-only", f"{BASE}...HEAD").splitlines() if p]
if not changed:
    raise SystemExit("B3B09 FAIL_CLOSED: no readiness changes found")

unexpected = sorted(set(changed) - ALLOWED)
if unexpected:
    raise SystemExit("B3B09 FAIL_CLOSED: out-of-scope changed paths: " + ", ".join(unexpected))

for path in changed:
    if path.startswith(FORBIDDEN_PREFIXES) or path in FORBIDDEN_EXACT or path.lower().endswith((".for", ".f", ".f90", ".f95")):
        raise SystemExit("B3B09 FAIL_CLOSED: production/source/reference/state/canonical/central-regie surface changed: " + path)

required = {
    "docs/b3/TCD038_GOV04_TIER_C_ADMISSION_READINESS.md",
    "integration/animo-b3/TCD038_READINESS_EVIDENCE.json",
    "integration/animo-b3/ANIMO-B3B09_STATUS.json",
    "tools/validate_b3b09_tcd038_readiness.py",
    "tools/validate_b3b09_scope.py",
}
missing = sorted(required - set(changed))
if missing:
    raise SystemExit("B3B09 FAIL_CLOSED: required readiness artifacts missing: " + ", ".join(missing))

print("B3B09 scope PASS: only bounded TCD-038 readiness evidence, documentation, validation, optional review handoff and workflow paths changed; production source, B0, TCD-039, canonical STATE/register, central regie, B4 and production migration remain closed.")
