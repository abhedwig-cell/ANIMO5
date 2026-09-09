#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-ARCH05 candidate exchange contracts."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "integration" / "animo-architecture"
PREP = ROOT / "integration" / "animo-prep"

DOMAINS = ARCH / "ARCH05_EXCHANGE_DOMAINS.csv"
FIELDS = ARCH / "ARCH05_EXCHANGE_FIELDS.csv"
RULES = ARCH / "ARCH05_TRANSACTION_RULES.csv"
COMPAT = ARCH / "ARCH05_COMPATIBILITY_SCHEMA.csv"
ARCH04_LAYOUT = ARCH / "ARCH04_LAYOUT_SCHEMA.csv"
PREP06_TRANSFERS = PREP / "PREP06_TRANSFER_LEDGER.csv"
INVARIANTS = ROOT / "docs" / "architecture" / "ANIMO5_ARCHITECTURE_INVARIANTS.md"

REQUIRED_DOMAINS = {"EX-HYDROLOGY", "EX-CROP-EXTERNAL", "EX-ORCHESTRATION"}

REQUIRED_HYDRO_FIELDS = {
    "HYD-MATRIX-WATER-BEGIN",
    "HYD-MATRIX-WATER-END",
    "HYD-VERTICAL-WATER",
    "HYD-DRAIN-OUT",
    "HYD-DRAIN-IN",
    "HYD-BOTTOM-WATER",
    "HYD-RUNOFF-OUT",
    "HYD-RUNON-IN",
    "HYD-PRECIP-IN",
    "HYD-IRRIGATION-IN",
}

REQUIRED_DETAILED_STORAGE = {
    "HYD-INTERCEPTION-BEGIN",
    "HYD-INTERCEPTION-END",
    "HYD-POND-BEGIN",
    "HYD-POND-END",
}

REQUIRED_MACRO_FIELDS = {
    "HYD-MP-WATER-BEGIN",
    "HYD-MP-WATER-END",
    "HYD-MP-INFIL",
    "HYD-MP-MATRIX-X",
    "HYD-MP-DIRECT-DRAIN",
}

REQUIRED_CROP_FIELDS = {
    "CROP-ACTIVE",
    "CROP-N-DEMAND",
    "CROP-P-DEMAND",
    "CROP-N-UPTAKE-REALIZED",
    "CROP-P-UPTAKE-REALIZED",
    "CROP-RESIDUE-INPUT-BUNDLE",
    "CROP-EXTERNAL-EXPORT-BUNDLE",
}

REQUIRED_RULES = {
    "TR-BEGIN-IDENTITY",
    "TR-ACCEPTED-START",
    "TR-HYDRO-READONLY",
    "TR-CROP-READONLY",
    "TR-RESULT-SEPARATION",
    "TR-REJECT",
    "TR-COMMIT-BARRIER",
    "TR-RETRY",
    "TR-UNITS",
    "TR-GEOMETRY",
    "TR-SIGN",
    "TR-MACROPORE-BLOCK",
    "TR-CHEM-BOUNDARY-SEPARATION",
    "TR-CROP-RESIDUE-EXPLICIT",
    "TR-CROP-EXPORT-EXPLICIT",
    "TR-DIAGNOSTIC-NONOWNERSHIP",
    "TR-CHECKPOINT-OWNER",
    "TR-PRECISION-REFERENCE",
}

REQUIRED_COMPAT = {
    "exchange_contract_schema_id",
    "transaction_schema_id",
    "interval_id",
    "trial_id",
    "t0",
    "t1",
    "physical_layout_id",
    "geometry_id",
    "feature_set_id",
    "precision_policy_ref",
    "producer_model_id",
    "producer_model_version",
    "producer_accepted_snapshot_id",
    "producer_frame_id",
    "hydrology_exchange_schema_id",
    "hydrology_mode",
    "macropore_enabled",
    "crop_exchange_schema_id",
    "crop_mode",
    "animo_accepted_snapshot_id",
    "hydrology_frame_id",
    "configuration_identity",
    "commit_group_id",
}

REQUIRED_PREP06_TRANSFERS = {
    "W-VERTICAL-MATRIX",
    "W-LATERAL-DRAIN",
    "W-LATERAL-INFIL",
    "W-BOTTOM-DOWN",
    "W-BOTTOM-UP",
    "W-RUNOFF",
    "W-RUNON",
    "CROP-N-UPTAKE",
    "CROP-P-UPTAKE",
    "ROOT-DEATH-DM",
    "HARVEST-EXPORT-DM",
    "GRAZING-EXPORT-DM",
}


def rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"missing {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def unique(values: list[str], label: str) -> set[str]:
    if any(not value for value in values):
        raise AssertionError(f"empty {label}")
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {label}")
    return set(values)


def main() -> int:
    domains = rows(DOMAINS)
    fields = rows(FIELDS)
    rules = rows(RULES)
    compat = rows(COMPAT)
    arch04 = rows(ARCH04_LAYOUT)
    prep06 = rows(PREP06_TRANSFERS)

    domain_ids = unique([r["exchange_domain_id"] for r in domains], "exchange_domain_id")
    field_ids = unique([r["field_id"] for r in fields], "field_id")
    rule_ids = unique([r["rule_id"] for r in rules], "rule_id")
    compat_ids = unique([r["field_id"] for r in compat], "compat field_id")
    prep_ids = unique([r["transfer_id"] for r in prep06], "PREP06 transfer_id")
    arch04_ids = unique([r["field_id"] for r in arch04], "ARCH04 layout field_id")

    assert domain_ids == REQUIRED_DOMAINS, (domain_ids, REQUIRED_DOMAINS)
    assert REQUIRED_HYDRO_FIELDS <= field_ids
    assert REQUIRED_DETAILED_STORAGE <= field_ids
    assert REQUIRED_MACRO_FIELDS <= field_ids
    assert REQUIRED_CROP_FIELDS <= field_ids
    assert rule_ids == REQUIRED_RULES, (rule_ids, REQUIRED_RULES)
    assert REQUIRED_COMPAT <= compat_ids
    assert REQUIRED_PREP06_TRANSFERS <= prep_ids

    for row in fields:
        assert row["domain"] in domain_ids
        assert row["owner"] and row["consumer"]
        assert row["checkpoint_role"]
        if row["domain"] == "EX-HYDROLOGY":
            assert row["owner"] == "external_hydrology_owner"
            assert row["consumer"] == "ANIMO"
            assert row["checkpoint_role"] != "ANIMO_checkpoint"
        if row["domain"] == "EX-CROP-EXTERNAL" and row["direction"] == "producer_to_animo":
            assert row["owner"] == "external_crop_owner"
            assert row["consumer"] == "ANIMO"

    for fid in {"CROP-N-UPTAKE-REALIZED", "CROP-P-UPTAKE-REALIZED"}:
        row = next(r for r in fields if r["field_id"] == fid)
        assert row["direction"] == "animo_to_producer"
        assert row["owner"] == "ANIMO"
        assert row["consumer"] == "external_crop_owner"
        assert row["temporal_role"] == "trial_result"

    for fid in REQUIRED_MACRO_FIELDS:
        row = next(r for r in fields if r["field_id"] == fid)
        assert row["qualification_status"] == "BLOCKED_ACTIVE_CASE_AND_LEDGER"
        assert "TCD-025" in row["open_evidence"]

    interception = next(r for r in fields if r["field_id"] == "HYD-INTERCEPTION-BEGIN")
    assert "TCD-018" in interception["open_evidence"]

    crop_residue = next(r for r in fields if r["field_id"] == "CROP-RESIDUE-INPUT-BUNDLE")
    assert "NO_INFERENCE_FROM_STATE_DELTA" in crop_residue["qualification_status"]

    for required in {
        "hydrology_exchange_schema_id",
        "crop_exchange_schema_id",
        "physical_layout_id",
        "geometry_id",
        "precision_policy_ref",
    }:
        assert required in arch04_ids, f"ARCH04 missing compatibility anchor {required}"

    precision = next(r for r in compat if r["field_id"] == "precision_policy_ref")
    assert "no precision or tolerance" in precision["rule"]

    crop_mode = next(r for r in compat if r["field_id"] == "crop_mode")
    assert "external" in crop_mode["rule"]

    invariant_text = INVARIANTS.read_text(encoding="utf-8")
    for expected in (
        "SWAP-ANIMO coupling uses explicit exchange contracts",
        "ANIMO does not depend on internal SWAP state",
        "SWAP does not depend on internal ANIMO state",
        "WOFOST coupling uses explicit ownership and exchange contracts",
    ):
        assert expected in invariant_text, f"missing architecture invariant: {expected}"

    reject = next(r for r in rules if r["rule_id"] == "TR-REJECT")
    assert "accepted" in reject["required_behavior"].lower()
    assert "partial" in reject["forbidden_behavior"].lower()

    barrier = next(r for r in rules if r["rule_id"] == "TR-COMMIT-BARRIER")
    assert "one logical accepted interval" in barrier["required_behavior"]

    print(
        "ARCH05 PASS: "
        f"domains={len(domains)} fields={len(fields)} rules={len(rules)} "
        f"compat_fields={len(compat)} prep06_transfers={len(prep06)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError) as exc:
        print(f"ARCH05 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
