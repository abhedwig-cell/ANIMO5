#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = "f348d0509ddfbb60473d41a7fe25e67d8e088e7f"
ALLOWED = {
    ".github/workflows/animo-b3a01r-tcd027-independent-review.yml",
    "docs/b3/TCD027_INDEPENDENT_SECOND_LINE_REVIEW.md",
    "integration/animo-b3/TCD027_INDEPENDENT_SECOND_LINE_REVIEW.json",
    "tools/check_b3a01r_tcd027_scope.py",
    "tools/validate_b3a01r_tcd027_review.py",
}
FORBIDDEN_PREFIXES = (
    "src/",
    "reference/source/",
    "reference/testcases/",
    "integration/animo-reg/",
)


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def fail(message):
    raise SystemExit("FAIL_B3A01R_SCOPE_GUARD: " + message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE)
    args = parser.parse_args()

    try:
        run("git", "cat-file", "-e", args.base + "^{commit}")
    except subprocess.CalledProcessError:
        fail("review handoff base is not available in checkout: " + args.base)

    raw = run("git", "diff", "--name-status", args.base + "...HEAD")
    entries = []
    if raw:
        for line in raw.splitlines():
            parts = line.split("\t")
            status = parts[0]
            paths = parts[1:]
            if status.startswith("R") or status.startswith("C"):
                fail("renames/copies are not permitted: " + line)
            if len(paths) != 1:
                fail("unexpected diff record: " + line)
            entries.append((status, paths[0]))

    changed = {path for _, path in entries}
    if changed != ALLOWED:
        fail("changed paths differ from exact review-only whitelist: " + repr(sorted(changed)))

    for status, path in entries:
        if status != "A":
            fail("review deliverables must be additions only; found " + status + " for " + path)
        if path.startswith(FORBIDDEN_PREFIXES):
            fail("forbidden production/frozen/regie path changed: " + path)

    production_diff = run("git", "diff", "--name-only", args.base + "...HEAD", "--", "src", "reference/source", "reference/testcases", "integration/animo-reg")
    if production_diff:
        fail("forbidden production/frozen/regie changes detected")

    print("PASS_B3A01R_TCD027_SCOPE_GUARD")


if __name__ == "__main__":
    main()
