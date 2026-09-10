#!/usr/bin/env python3
"""Fail-closed scope guard for ANIMO-B3B09R.

Only review evidence, its validators, and its workflow may differ from the exact
clean B3B09 handoff. Production, frozen reference, canonical registers, state
admission, aggregate integration, and unrelated files are forbidden.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "1b47d6b2e422463b557a48355ad8b4f5bed70ebc"
ALLOWED = {
    "docs/b3/TCD038_INDEPENDENT_SECOND_LINE_REVIEW.md",
    "integration/animo-b3/TCD038_INDEPENDENT_SECOND_LINE_REVIEW.json",
    "tools/validate_b3b09r_tcd038_review.py",
    "tools/validate_b3b09r_scope.py",
    ".github/workflows/animo-b3b09r-tcd038-independent-second-line.yml",
}
FORBIDDEN_PREFIXES = (
    "reference/",
    "src/",
    "source/",
    "production/",
)
FORBIDDEN_EXACT = {
    "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv",
    "integration/animo-state/ANIMO-STATEQ01_STATUS.json",
    "integration/animo-state/ANIMO-STATEQ02_STATUS.json",
    "integration/animo-reg/ANIMO-RG05G_STATUS.json",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


# Exact ancestry is mandatory. A merge/rebase that drops the clean handoff is a failure.
proc = subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=False)
if proc.returncode != 0:
    fail("exact B3B09 handoff is not an ancestor of HEAD")

changed = {line for line in git("diff", "--name-only", f"{BASE}..HEAD").splitlines() if line}
if changed != ALLOWED:
    missing = sorted(ALLOWED - changed)
    extra = sorted(changed - ALLOWED)
    fail(f"review change set is not exact; missing={missing}, extra={extra}")

for path in changed:
    if path in FORBIDDEN_EXACT or path.startswith(FORBIDDEN_PREFIXES):
        fail(f"forbidden review-scope change: {path}")

# All review files are additive relative to the clean handoff. Replacing or deleting
# pre-existing evidence would make the independent review non-auditable.
status_lines = [line for line in git("diff", "--name-status", f"{BASE}..HEAD").splitlines() if line]
for line in status_lines:
    parts = line.split("\t")
    status = parts[0]
    paths = parts[1:]
    if status != "A":
        fail(f"non-additive change detected: {line}")
    if len(paths) != 1 or paths[0] not in ALLOWED:
        fail(f"unexpected name-status record: {line}")

print("PASS: B3B09R scope is exactly five additive review-only files from the clean B3B09 handoff.")
