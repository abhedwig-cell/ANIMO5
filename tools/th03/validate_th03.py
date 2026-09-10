#!/usr/bin/env python3
"""Fail-closed static validator for ANIMO-TH03."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "bbdb61be30f08951ba78926a745719cfcb1b64a8"
STATUS = ROOT / "integration/animo-theory/ANIMO-TH03_STATUS.json"
EVIDENCE = ROOT / "integration/animo-theory/TH03_HETOP_RESERVOIR_LINEAGE.json"
DOC = ROOT / "docs/theory/HETOP_RESERVOIR_LINEAGE_PROVENANCE.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def changed_paths() -> list[str]:
    p = subprocess.run(
        ["git", "diff", "--name-only", BASE, "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def main() -> None:
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    d = DOC.read_text(encoding="utf-8")

    require(s["work_unit"] == "ANIMO-TH03", "wrong status owner")
    require(e["work_unit"] == "ANIMO-TH03", "wrong evidence owner")
    require(s["base"]["head"] == BASE, "base head drift")

    r = e["recovered_ANIMO35_process_theory"]
    require(r["surface_addition_reservoir_exists"] is True, "ANIMO 3.5 reservoir lineage not recorded")
    require(r["all_additions_immediately_dissolved_in_reservoir"] is True, "addition dissolution semantics lost")
    require(r["solute_migration_characterized_as_piston_flow"] is True, "piston-flow semantics lost")
    require(r["bookkeeping_store"] is True, "bookkeeping storage semantics lost")
    require(r["endpoint_HETOP_zero_explicitly_defined"] is False, "zero endpoint invented")
    require(r["zero_as_disable_sentinel_explicitly_defined"] is False, "zero sentinel invented")
    require(r["zero_as_instantaneous_release_explicitly_defined"] is False, "instantaneous zero endpoint invented")
    require(r["zero_as_invalid_input_explicitly_defined"] is False, "zero invalidity invented")

    c = e["lineage_reconciliation"]
    require(c["reservoir_concept_predates_ANIMO40"] is True, "pre-4.0 lineage not qualified")
    require(c["HETOP_is_supported_as_capacity_or_release_timescale_parameter"] is True, "HETOP role lost")
    require(c["HETOP_supported_as_feature_flag_or_sentinel"] is False, "unsupported sentinel semantics")
    require(c["zero_endpoint_uniquely_resolved"] is False, "zero endpoint silently resolved")

    b = e["qualified_boundary"]
    require(b["positive_HETOP_B1_and_E1_results_invalidated"] is False, "positive-HETOP child results incorrectly invalidated")
    require(b["NQ03_extended_to_HETOP_zero"] is False, "NQ03 scope silently widened")
    require(b["input_lower_bound_change_authorized"] is False, "input change authorized")
    require(b["zero_capacity_passthrough_authorized"] is False, "zero-capacity policy authorized")
    require(b["new_TCD_authorized"] is False, "new TCD authorized")
    require(b["scientific_admission_authorized"] is False, "scientific admission authorized")
    require(b["production_change_authorized"] is False, "production change authorized")

    require("QUALIFIED_HETOP_RESERVOIR_CONCEPT_LINEAGE_TO_ANIMO35_ZERO_ENDPOINT_UNRESOLVED" in d, "qualified disposition missing from document")
    require("does not define zero as a sentinel" in d, "document lacks sentinel nonclaim")
    require("does not claim that the inclusive `[0.0 ... 0.2]` range itself is proven to originate in 3.5" in d, "document overclaims 3.5 input-range lineage")

    for key, value in s["scope_guards"].items():
        require(value is False, f"scope guard violated: {key}")

    allowed = (
        ".github/workflows/animo-th03-",
        "docs/theory/HETOP_RESERVOIR_LINEAGE_PROVENANCE.md",
        "integration/animo-theory/ANIMO-TH03_STATUS.json",
        "integration/animo-theory/TH03_HETOP_RESERVOIR_LINEAGE.json",
        "tools/th03/",
    )
    changed = changed_paths()
    require(changed, "no TH03 artifacts")
    for path in changed:
        require(path.startswith(allowed), f"scope widened by {path}")
        require(not path.startswith("src/"), "production source modified")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")

    print("TH03 PASS: ANIMO 3.5 HETOP reservoir lineage qualified; zero endpoint remains unresolved and unadmitted")


if __name__ == "__main__":
    main()
