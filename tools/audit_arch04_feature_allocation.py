#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-ARCH04 candidate feature/allocation design."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "integration" / "animo-architecture"

ARCH01 = BASE / "ARCH01_STATE_OWNERSHIP.csv"
FEATURES = BASE / "ARCH04_FEATURES.csv"
ALLOC = BASE / "ARCH04_STATE_ALLOCATION.csv"
INTERACTIONS = BASE / "ARCH04_FEATURE_INTERACTIONS.csv"
LAYOUT = BASE / "ARCH04_LAYOUT_SCHEMA.csv"

REQUIRED_FEATURES = {
    "FT-CORE-SOIL-CHEMISTRY",
    "FT-HYDRO-DETAILED",
    "FT-HYDRO-AGGREGATED",
    "FT-SNOW",
    "FT-SURFACE-RESERVOIR",
    "FT-STABLE-DOM-SOIL",
    "FT-CROP",
    "FT-GHG",
    "FT-MACROPORE",
    "FT-P-FAST-SITES",
    "FT-P-SLOW-SITES",
    "FT-DIAGNOSTICS",
    "FT-SURFACE-STABLE-DOM-DORMANT",
}

REQUIRED_LAYOUT_FIELDS = {
    "layout_schema_id",
    "state_schema_id",
    "feature_set_id",
    "hydrology_mode",
    "snow_enabled",
    "surface_reservoir_enabled",
    "stable_dom_enabled",
    "crop_mode",
    "ghg_enabled",
    "ghg_admission_id",
    "macropore_enabled",
    "macropore_admission_id",
    "fast_p_site_count",
    "slow_p_site_count",
    "layer_count",
    "organic_fraction_count",
    "geometry_id",
    "hydrology_exchange_schema_id",
    "crop_exchange_schema_id",
    "crop_state_schema_id",
    "ghg_schema_id",
    "macropore_schema_id",
    "precision_policy_ref",
    "physical_layout_id",
    "diagnostics_mode",
    "observer_schema_id",
    "observer_layout_id",
}

ALLOCATION_CLASSES = {
    "MODEL_PERSISTENT",
    "CONDITIONAL_PERSISTENT",
    "CONDITIONAL_OWNER_PERSISTENT",
    "EXTERNAL_COORDINATE",
    "DERIVED_VIEW",
    "STEP_LOCAL_SCRATCH",
    "DIAGNOSTIC_OBSERVER",
    "UNSUPPORTED_DORMANT",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"missing {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def unique(rows: list[dict[str, str]], key: str) -> set[str]:
    values = [r[key] for r in rows]
    if any(not v for v in values):
        raise AssertionError(f"empty {key}")
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {key}")
    return set(values)


def main() -> int:
    arch01 = read_csv(ARCH01)
    features = read_csv(FEATURES)
    alloc = read_csv(ALLOC)
    interactions = read_csv(INTERACTIONS)
    layout = read_csv(LAYOUT)

    arch01_ids = unique(arch01, "legacy_state_id")
    alloc_ids = unique(alloc, "legacy_state_id")
    assert arch01_ids == alloc_ids
    assert len(alloc_ids) == 53

    a1_fields = {r["legacy_state_id"]: r["candidate_field_id"] for r in arch01}
    a4_fields = {r["legacy_state_id"]: r["candidate_field_id"] for r in alloc}
    assert a1_fields == a4_fields

    fids = unique(features, "feature_id")
    assert fids == REQUIRED_FEATURES

    layout_fields = unique(layout, "field_id")
    assert layout_fields == REQUIRED_LAYOUT_FIELDS

    classes = {r["allocation_class"] for r in alloc}
    assert classes <= ALLOCATION_CLASSES
    assert ALLOCATION_CLASSES <= classes

    for row in interactions:
        assert row["left_feature"] in fids
        assert row["right_feature"] in fids

    dormant = next(r for r in alloc if r["legacy_state_id"] == "TOP-SDOM-DORMANT")
    assert dormant["allocation_class"] == "UNSUPPORTED_DORMANT"
    assert dormant["activation_expression"] == "forbidden"

    for state_id in ("GHG-CH4-SYS", "GHG-N2O-SYS"):
        row = next(r for r in alloc if r["legacy_state_id"] == state_id)
        assert "feature_admitted" in row["activation_expression"]
        assert row["allocation_class"] == "CONDITIONAL_PERSISTENT"

    for state_id in ("W-MACROPORE", "MP-DOM-C", "MP-DON", "MP-DOP", "MP-NH4", "MP-NO3", "MP-PO4"):
        row = next(r for r in alloc if r["legacy_state_id"] == state_id)
        assert "feature_admitted" in row["activation_expression"]
        assert row["allocation_class"] == "CONDITIONAL_PERSISTENT"

    crop_persistent = [r for r in alloc if r["legacy_state_id"] in {
        "CROP-SHOOT-DM", "CROP-ROOT-DM", "CROP-N-ACT", "CROP-P-ACT"
    }]
    assert all(r["allocation_class"] == "CONDITIONAL_OWNER_PERSISTENT" for r in crop_persistent)
    assert all(r["activation_expression"] == "crop_mode=animo" for r in crop_persistent)

    diagnostic = [r for r in alloc if r["allocation_class"] == "DIAGNOSTIC_OBSERVER"]
    assert {r["legacy_state_id"] for r in diagnostic} == {"REPORT-MAIN-BAL", "REPORT-DETAILED-TRANS"}

    external = [r for r in alloc if r["allocation_class"] == "EXTERNAL_COORDINATE"]
    assert {r["legacy_state_id"] for r in external} == {"W-INTERCEPTION", "W-SNOW", "W-POND", "W-MATRIX"}
    assert all(r["allocator"] == "external_hydrology_owner" for r in external)

    physical_layout = next(r for r in layout if r["field_id"] == "physical_layout_id")
    diag_mode = next(r for r in layout if r["field_id"] == "diagnostics_mode")
    observer_layout = next(r for r in layout if r["field_id"] == "observer_layout_id")
    assert physical_layout["scope"] == "physical"
    assert diag_mode["scope"] == "observer"
    assert observer_layout["scope"] == "observer"

    precision = next(r for r in layout if r["field_id"] == "precision_policy_ref")
    assert "ARCH04 does not define precision" in precision["rule"]

    hydro = next(r for r in interactions if r["interaction_id"] == "INT-HYDRO-MODE")
    assert hydro["relation"] == "EXCLUSIVE"

    print(
        "ARCH04 PASS: "
        f"state_families={len(alloc)} features={len(features)} "
        f"interactions={len(interactions)} layout_fields={len(layout)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ARCH04 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
