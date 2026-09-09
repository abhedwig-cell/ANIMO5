#!/usr/bin/env python3
"""Validate B3I01 supplement-03 BUILDQ03 runtime routing fail-closed."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
ROUTING = ROOT / "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER_SUPPLEMENT_03.json"
CROSSWALK = ROOT / "integration/animo-b3/POST_G5_LOCAL_FINDING_CROSSWALK_SUPPLEMENT_03.csv"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I01_SUPPLEMENT_03_STATUS.json"


def main() -> None:
    with REGISTER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["ID"] for row in rows]
    expected = [f"TCD-{i:03d}" for i in range(1, 41)]
    if ids != expected:
        raise AssertionError("supplement-03 must not change canonical register TCD-001..040")

    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    if routing.get("supplement") != "POST_G5_LIVE_INTAKE_SUPPLEMENT_03":
        raise AssertionError("wrong supplement identity")
    action = routing.get("canonical_register_action", {})
    if action.get("append_required") is not False:
        raise AssertionError("supplement-03 must not require register append")
    if action.get("register_tail_unchanged") != "TCD-040":
        raise AssertionError("canonical tail must remain TCD-040")
    if action.get("new_top_level_tcd_allocated") is not False:
        raise AssertionError("supplement-03 must allocate no new TCD")

    strengthen = routing.get("existing_tcd_evidence_strengthening", [])
    if len(strengthen) != 1 or strengthen[0].get("canonical_key") != "TCD-011":
        raise AssertionError("supplement-03 must strengthen TCD-011 only")
    tcd011 = strengthen[0]
    if tcd011.get("disposition") != "STRENGTHEN_EXISTING_TCD_EVIDENCE_ONLY":
        raise AssertionError("unexpected TCD-011 disposition")
    if len(tcd011.get("qualified_families", [])) != 6:
        raise AssertionError("TCD-011 strengthening must carry six qualified GHG families")
    if tcd011.get("historical_intel_equivalence") is not False:
        raise AssertionError("historical Intel equivalence must remain open")
    if tcd011.get("tcd_closed") is not False or tcd011.get("admitted") is not False:
        raise AssertionError("TCD-011 must remain open and not admitted")

    runtime = routing.get("runtime_routing_additions", [])
    if len(runtime) != 1:
        raise AssertionError("supplement-03 must contain exactly one new runtime route")
    hazard = runtime[0]
    if hazard.get("local_key") != "BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED":
        raise AssertionError("unexpected runtime local key")
    if hazard.get("disposition") != "BUILD_RUNTIME_INITIALIZATION_HAZARD_NOT_TCD_PENDING_BOUNDARY_SEMANTICS":
        raise AssertionError("unexpected Flair hazard disposition")
    if hazard.get("canonical_tcd") is not None:
        raise AssertionError("Flair hazard must not have a canonical TCD yet")
    if hazard.get("admitted") is not False:
        raise AssertionError("Flair hazard must not be admitted")
    if "not admitted" not in hazard.get("diagnostic_control_not_semantics", ""):
        raise AssertionError("diagnostic zero-boundary control must remain explicitly non-semantic")

    with CROSSWALK.open(newline="", encoding="utf-8") as handle:
        crosswalk = list(csv.DictReader(handle))
    if len(crosswalk) != 2:
        raise AssertionError("supplement-03 crosswalk must contain exactly two rows")
    by_key = {row["local_key"]: row for row in crosswalk}
    if by_key["GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE"]["canonical_tcd_id"] != "TCD-011":
        raise AssertionError("GHG hidden-task family must map to TCD-011")
    flair = by_key["BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED"]
    if flair["canonical_tcd_id"] != "":
        raise AssertionError("Flair hazard crosswalk must not allocate a TCD")
    if flair["canonical_disposition"] != "BUILD_RUNTIME_INITIALIZATION_HAZARD_NOT_TCD_PENDING_BOUNDARY_SEMANTICS":
        raise AssertionError("Flair crosswalk disposition mismatch")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    for key in [
        "new_corrections_admitted",
        "b3_baseline_established",
        "production_migration_admitted",
        "production_code_modified",
        "source_correction",
    ]:
        if status.get(key) is not False:
            raise AssertionError(f"supplement-03 violates fail-closed flag {key}")
    if status.get("canonical_register", {}).get("tail_after_supplement") != "TCD-040":
        raise AssertionError("status must preserve TCD-040 register tail")
    if status.get("runtime_hazard_action", {}).get("diagnostic_zero_boundary_admitted") is not False:
        raise AssertionError("diagnostic zero-boundary value must not be admitted")

    print("ANIMO-B3I01 supplement-03 BUILDQ03 runtime routing validation: PASS")


if __name__ == "__main__":
    main()
