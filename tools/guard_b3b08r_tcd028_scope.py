#!/usr/bin/env python3
import subprocess

BASE = "71340e036504695ba7177f31c0be9345895680b3"
ALLOWED = {
    "docs/b3/TCD028_INDEPENDENT_TIER_C_REVIEW.md",
    "integration/animo-b3/ANIMO-B3B08R_REVIEW_RESULT.json",
    "tools/validate_b3b08r_tcd028_review.py",
    "tools/guard_b3b08r_tcd028_scope.py",
    ".github/workflows/animo-b3b08r-tcd028-independent-review.yml",
}


def main():
    output = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASE}..HEAD"],
        text=True,
    )
    changed = {line.strip() for line in output.splitlines() if line.strip()}
    if changed != ALLOWED:
        missing = sorted(ALLOWED - changed)
        extra = sorted(changed - ALLOWED)
        raise SystemExit(
            "FAIL_B3B08R_SCOPE_GUARD "
            f"missing={missing} extra={extra} changed={sorted(changed)}"
        )
    print("PASS_B3B08R_TCD028_REVIEW_SCOPE_GUARD")


if __name__ == "__main__":
    main()
