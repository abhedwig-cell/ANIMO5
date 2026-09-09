#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-ARCH03 candidate MassLedger design."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "integration" / "animo-architecture"

QFILE = BASE / "ARCH03_LEDGER_QUANTITIES.csv"
CVFILE = BASE / "ARCH03_CONTROL_VOLUMES.csv"
SCHEMAFILE = BASE / "ARCH03_OBSERVER_SCHEMA.csv"
IDFILE = BASE / "ARCH03_IDENTITY_MAP.csv"
PFILE = BASE / "ARCH03_STATE_LEDGER_PROJECTION.csv"
ARCH01_STATE = BASE / "ARCH01_STATE_OWNERSHIP.csv"

REQUIRED_QUANTITIES = {
    "water",
    "nitrogen",
    "phosphorus",
    "organic_matter_mass",
    "crop_dry_matter",
    "carbon_as_CH4_C",
    "nitrogen_as_N2O_N",
}

REQUIRED_CVS = {
    "CV-HYDRO-PROFILE",
    "CV-SOIL-N",
    "CV-SOIL-CROP-N",
    "CV-SOIL-P",
    "CV-SOIL-CROP-P",
    "CV-SOIL-OM",
    "CV-CROP-DM",
    "CV-MATRIX-MACROPORE-OM",
    "CV-MATRIX-MACROPORE-N",
    "CV-MATRIX-MACROPORE-P",
    "CV-GHG-C",
    "CV-GHG-N",
}

REQUIRED_SCHEMA_FIELDS = {
    "ledger_id",
    "trial_or_commit_id",
    "control_volume_id",
    "quantity_id",
    "unit",
    "begin_storage",
    "end_storage",
    "external_input",
    "external_output",
    "internal_transfer_total",
    "closure_residual",
    "closure_tolerance",
    "closure_status",
    "constraint_nonclosure",
    "reaction_bundle_nonclosure",
    "initialization_nonclosure",
    "observer_integrity_status",
    "source_state_snapshot_id",
    "sink_state_snapshot_id",
    "journal_id",
    "schema_id",
    "feature_layout_id",
    "geometry_id",
}

REQUIRED_IDENTITIES = {
    "ID-WATER-PROFILE",
    "ID-INTERNAL-INTERFACE-CANCEL",
    "ID-SOLUTE-LAYER",
    "ID-SOLUTE-PROFILE",
    "ID-MATERIAL-ADDITION",
    "ID-CROP-N",
    "ID-CROP-P",
    "ID-CROP-RESIDUE",
    "ID-CROP-HARVEST",
    "ID-CROP-GRAZING",
    "ID-REDISTRIBUTION",
    "ID-ORG-TRANSFORM",
    "ID-STABLE-DOM-P",
    "ID-N-MINERALIZATION",
    "ID-P-MINERALIZATION",
    "ID-NITRIFICATION",
    "ID-DENITRIFICATION",
    "ID-P-SORPTION",
    "ID-P-INITIAL",
    "ID-DRYDOWN",
    "ID-MACROPORE-WATER",
    "ID-MACROPORE-SOLUTE",
    "ID-REPORT-ACCUM",
}

EXCLUDED_LEDGER_ROLES = {
    "DERIVED_EXCLUDE",
    "DORMANT_EXCLUDE",
    "SCRATCH_EXCLUDE",
    "DIAGNOSTIC_EXCLUDE",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"missing {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def unique(rows: list[dict[str, str]], key: str) -> set[str]:
    values = [r[key] for r in rows]
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {key}")
    if any(not v for v in values):
        raise AssertionError(f"empty {key}")
    return set(values)


def split_refs(value: str) -> set[str]:
    return set(filter(None, value.split(";")))


def main() -> int:
    qrows = read_csv(QFILE)
    cvrows = read_csv(CVFILE)
    srows = read_csv(SCHEMAFILE)
    irows = read_csv(IDFILE)
    prows = read_csv(PFILE)
    arows = read_csv(ARCH01_STATE)

    qids = unique(qrows, "quantity_id")
    cvids = unique(cvrows, "control_volume_id")
    fields = unique(srows, "field_id")
    identities = unique(irows, "identity_id")
    pids = unique(prows, "legacy_state_id")
    arch01_ids = unique(arows, "legacy_state_id")

    assert qids == REQUIRED_QUANTITIES, (qids, REQUIRED_QUANTITIES)
    assert cvids == REQUIRED_CVS, (cvids, REQUIRED_CVS)
    assert fields == REQUIRED_SCHEMA_FIELDS, (fields, REQUIRED_SCHEMA_FIELDS)
    assert identities == REQUIRED_IDENTITIES, (identities, REQUIRED_IDENTITIES)
    assert pids == arch01_ids
    assert len(prows) == 53

    for row in qrows:
        assert row["default_control_volume"] in cvids
        assert row["closure_identity"] == "R=S_end-S_begin-I_external+O_external"
        event_classes = split_refs(row["admitted_event_classes"])
        assert "TT-OBSERVE" not in event_classes
        assert "TT-CONSTRAINT" not in event_classes

    for row in cvrows:
        assert row["quantity_scope"] in qids
        assert "derive" in row["event_classification_rule"].lower() or "internal" in row["event_classification_rule"].lower()

    for row in irows:
        assert row["quantity_id"] in qids
        assert row["primary_control_volume"] in cvids
        assert row["observer_channel"] in {
            "closure_residual",
            "internal_transfer_total",
            "reaction_bundle_nonclosure",
            "initialization_nonclosure",
            "constraint_nonclosure",
            "observer_integrity_status",
        }

    for row in prows:
        quantities = split_refs(row["quantity_ids"])
        volumes = split_refs(row["control_volume_ids"])
        assert quantities <= qids
        assert volumes <= cvids
        if row["ledger_role"] in EXCLUDED_LEDGER_ROLES:
            assert not quantities
            assert not volumes
        else:
            assert quantities
            assert volumes

    tol = next(r for r in srows if r["field_id"] == "closure_tolerance")
    assert tol["required"] == "NO"
    assert tol["physical_role"] == "not_defined_by_ARCH03"

    begin = next(r for r in srows if r["field_id"] == "begin_storage")
    end = next(r for r in srows if r["field_id"] == "end_storage")
    assert "owner state" in begin["source"]
    assert "owner state" in end["source"]

    residual = next(r for r in srows if r["field_id"] == "closure_residual")
    assert residual["rule"] == "end_storage-begin_storage-external_input+external_output"

    print(
        "ARCH03 PASS: "
        f"quantities={len(qrows)} control_volumes={len(cvrows)} "
        f"schema_fields={len(srows)} identities={len(irows)} "
        f"state_projections={len(prows)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ARCH03 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
