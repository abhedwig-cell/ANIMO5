#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3I06."""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "ca55248f2382000288488659571b645fd5a8043b"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I06_STATUS.json"
CROSSWALK = ROOT / "integration/animo-b3/B3I06_UBQ03_FINDING_CROSSWALK.csv"
DOC = ROOT / "docs/b3/POST_UBQ03_HETOP_ZERO_INCREMENTAL_INTAKE.md"
UBQ03 = ROOT / "integration/animo-science/UBQ03_HETOP_ZERO_DOMAIN.json"
B3I05 = ROOT / "integration/animo-b3/B3I05_TCD042_ATOMIZATION.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def changed_paths() -> list[str]:
    p = subprocess.run(["git", "diff", "--name-only", BASE, "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def main() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    ubq03 = json.loads(UBQ03.read_text(encoding="utf-8"))
    atom = json.loads(B3I05.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    with CROSSWALK.open(newline="", encoding="utf-8") as h:
        rows = list(csv.DictReader(h))

    require(ubq03["decision"] == "QUALIFIED_CHARACTERIZATION_HETOP_ZERO_PARSER_ADMISSIBLE_CONDITIONALLY_UNDEFINED_NO_GLOBAL_ZERO_THICKNESS_POLICY", "UBQ03 authority changed")
    require(ubq03["parser_contract"]["hetop_zero_accepted"] is True, "UBQ03 zero-domain evidence lost")
    require(ubq03["direct_division_site_count"] == 9, "UBQ03 division inventory changed")
    require(ubq03["canonical_disposition"]["new_top_level_tcd_reserved"] is False, "UBQ03 unexpectedly allocated TCD")

    require(atom["parent_tcd"] == "TCD-042", "canonical parent changed")
    require({x["atom_id"] for x in atom["atoms"]} == {"TCD-042-B1", "TCD-042-E1"}, "canonical TCD-042 child set changed")
    require(atom["allocation_decision"]["tcd_043_reserved"] is False, "B3I05 TCD-043 invariant changed")

    require(status["work_unit"] == "ANIMO-B3I06", "wrong status owner")
    intake = status["intake"]
    require(intake["new_findings"] == 1, "B3I06 must remain incremental single-finding intake")
    require(intake["new_top_level_tcd_count"] == 0, "B3I06 allocated new TCD")
    require(intake["tcd_043_reserved"] is False, "B3I06 reserved TCD-043")
    require(intake["canonical_register_append_performed"] is False, "B3I06 appended register")
    require(intake["relation_to_tcd042"] == "DOMAIN_CONSTRAINT_ONLY_NOT_NEW_CHILD", "UBQ03 incorrectly routed as TCD-042 child")
    require(intake["disposition"] == "RUNTIME_INPUT_DOMAIN_HAZARD_PENDING_AUTHORITATIVE_ZERO_THICKNESS_MODEL_SEMANTICS", "unexpected intake disposition")

    require(len(rows) == 1, "crosswalk must contain exactly one incremental finding")
    row = rows[0]
    require(row["finding_id"] == "UBQ03-HETOP-0001", "wrong finding identity")
    require(row["new_top_level_tcd"] == "false", "crosswalk allocates new TCD")
    require(row["tcd_043_reserved"] == "false", "crosswalk reserves TCD-043")
    require(row["admission"] == "false", "crosswalk claims admission")
    require(row["canonical_disposition"] == intake["disposition"], "crosswalk/status disposition mismatch")

    require("not as a new TCD-042 child" in doc, "document must reject silent TCD-042 child routing")
    require("does not reserve `TCD-043`" in doc, "document must explicitly keep TCD-043 unreserved")
    require("input-contract correction" in doc and "zero-capacity" in doc, "document must preserve alternative remedy classes")

    for key, value in status["scope_guards"].items():
        require(value is False, f"scope guard violated: {key}")

    allowed = (
        ".github/workflows/animo-b3i06-",
        "docs/b3/POST_UBQ03_HETOP_ZERO_INCREMENTAL_INTAKE.md",
        "integration/animo-b3/B3I06_UBQ03_FINDING_CROSSWALK.csv",
        "integration/animo-b3/ANIMO-B3I06_STATUS.json",
        "tools/b3i06/",
    )
    changed = changed_paths()
    require(changed, "no B3I06 artifacts")
    for path in changed:
        require(path.startswith(allowed), f"B3I06 scope widened by {path}")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical register modified")
        require(not path.startswith("src/"), "production source modified")

    print("B3I06 PASS: UBQ03 routed as unresolved runtime/input-domain hazard; no TCD-043, no TCD-042 child widening, no admission")


if __name__ == "__main__":
    main()
