#!/usr/bin/env python3
"""Fail-closed structural validation for ANIMO-BUILDQ04 artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-build/ANIMO-BUILDQ04_STATUS.json"
MATRIX = ROOT / "integration/animo-build/BUILDQ04_GHG_BOTTOM_BOUNDARY_MATRIX.json"


def main() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))

    if status.get("status") != "QUALIFIED_ZERO_BOTTOM_AIR_ADVECTIVE_BOUNDARY_CONTRACT_LOCAL_INITIALIZATION_DEFECT_CANDIDATE_HISTORICAL_INTEL_OPEN":
        raise AssertionError("unexpected BUILDQ04 gate")
    if status.get("target", {}).get("local_key") != "BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED":
        raise AssertionError("wrong source local key")
    qualification = status.get("qualification", {})
    if qualification.get("first_read_scope") != "UNCONDITIONAL_TASK1_FIRST_READ_WITHOUT_SOURCE_ASSIGNMENT_FOR_NL_GE_1":
        raise AssertionError("first-read scope is not the qualified unconditional scope")
    if qualification.get("qualified_boundary_contract") != "FLAIR_NLPLUS1_EQUALS_ZERO_FOR_CLOSED_LOWER_GHG_AIR_BOUNDARY":
        raise AssertionError("wrong lower boundary contract")
    if qualification.get("boundary_value") != 0.0:
        raise AssertionError("qualified lower boundary value must be exactly zero")
    if qualification.get("historical_intel_effect") != "UNKNOWN":
        raise AssertionError("historical Intel effect must remain unknown")

    b3 = status.get("b3_handoff", {})
    if b3.get("provisional_class") != "B":
        raise AssertionError("BUILDQ04 handoff must remain provisional Class B")
    if b3.get("recommended_disposition") != "NEW_CANONICAL_TCD_CANDIDATE_PENDING_CENTRAL_COLLISION_CHECK_AND_RESERVATION":
        raise AssertionError("unexpected B3 disposition")
    if b3.get("canonical_id_allocated_by_buildq04") is not False:
        raise AssertionError("BUILDQ04 must not allocate a canonical TCD")

    for key in ["corrected_legacy_admitted", "b3_scientific_admitted", "production_migration_admitted", "production_code_modified"]:
        if status.get(key) is not False:
            raise AssertionError(f"fail-closed flag violated: {key}")

    topology = matrix.get("source_topology", {})
    if topology.get("la_after_decrement_invariant") != "0 <= La <= Nl-1":
        raise AssertionError("La invariant missing")
    if topology.get("bottom_transform_read") != "Flair(Nl+1)":
        raise AssertionError("wrong first-read coordinate")
    boundary = matrix.get("boundary_identity", {})
    if boundary.get("qualified_value") != 0.0:
        raise AssertionError("matrix lower boundary must be zero")
    probe = matrix.get("boundary_sensitivity_probe", {})
    if probe.get("output_rows") != 60:
        raise AssertionError("boundary sensitivity matrix must contain 60 rows")
    if probe.get("byte_identical_O0_O2") is not True:
        raise AssertionError("explicit boundary sensitivity O0/O2 matrix must be byte-identical")
    if matrix.get("provisional_b3", {}).get("class") != "B":
        raise AssertionError("matrix B3 class mismatch")
    if matrix.get("admission", {}).get("new_canonical_tcd_allocated") is not False:
        raise AssertionError("matrix must not allocate a TCD")

    print("ANIMO-BUILDQ04 structural qualification validation: PASS")


if __name__ == "__main__":
    main()
