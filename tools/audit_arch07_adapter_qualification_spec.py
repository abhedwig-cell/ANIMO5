#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-ARCH07 adapter qualification specification."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "integration" / "animo-architecture"

FIELDS05 = BASE / "ARCH05_EXCHANGE_FIELDS.csv"
RULES05 = BASE / "ARCH05_TRANSACTION_RULES.csv"
TESTS07 = BASE / "ARCH07_TEST_CASES.csv"
FIELD_COV07 = BASE / "ARCH07_FIELD_COVERAGE.csv"
RULE_COV07 = BASE / "ARCH07_TRANSACTION_RULE_COVERAGE.csv"
STATUS05 = BASE / "ANIMO-ARCH05_STATUS.json"
STATUS06 = BASE / "ANIMO-ARCH06_STATUS.json"

ALLOWED_TIERS = {
    "SPEC_STRUCTURAL",
    "ADAPTER_RUNTIME",
    "COUPLED_RUNTIME",
    "REFERENCE_BEHAVIOR",
    "SCIENTIFIC_ADMISSION",
}

REQUIRED_TEST_IDS = {
    "H001", "H002", "H003", "H004", "H005", "H006", "H007", "H008",
    "H009", "H010", "H011", "H012", "H013", "H014", "H015", "H016",
    "C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008",
    "C009", "C010", "C011", "C012",
    "T001", "T002", "T003", "T004", "T005", "T006", "T007", "T008", "T009",
    "I001", "I002", "I003", "I004",
}

REQUIRED_CATEGORIES = {
    "valid_detailed_frame", "valid_aggregated_frame", "missing_required_field",
    "forbidden_conditional_field", "unit_mismatch", "shape_mismatch", "sign_normalization",
    "frame_immutability", "accepted_generation_mismatch", "layout_mismatch",
    "configuration_mismatch", "chemical_boundary_separation", "interception_storage_ledger",
    "macropore_disabled", "macropore_without_admission", "macropore_future_extension",
    "valid_external_crop_frame", "owner_mode_mismatch", "demand_unit_shape_mismatch",
    "root_distribution_contract", "realized_n_uptake_link", "realized_p_uptake_link",
    "rejected_uptake_result", "residue_explicit_bundle", "residue_delta_inference_forbidden",
    "export_explicit_bundle", "state_observation_nonownership", "begin_trial_binding",
    "reject_atomicity", "accept_commit_barrier", "retry_identity", "diagnostic_nonownership",
    "checkpoint_owner_split", "precision_reference_mismatch", "split_run_equivalence",
    "rollback_replay_equivalence", "diagnostic_identity_invariance", "parameter_configuration_change",
    "feature_layout_change", "schema_version_change",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"missing {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def unique(rows: list[dict[str, str]], key: str) -> set[str]:
    values = [row[key] for row in rows]
    if any(not value for value in values):
        raise AssertionError(f"empty {key}")
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {key}")
    return set(values)


def refs(cell: str) -> set[str]:
    return set(filter(None, cell.split(";")))


def main() -> int:
    legacy_fields = read_csv(FIELDS05)
    legacy_rules = read_csv(RULES05)
    tests = read_csv(TESTS07)
    field_cov = read_csv(FIELD_COV07)
    rule_cov = read_csv(RULE_COV07)

    field_ids = unique(legacy_fields, "field_id")
    rule_ids = unique(legacy_rules, "rule_id")
    test_ids = unique(tests, "test_id")
    covered_fields = unique(field_cov, "field_id")
    covered_rules = unique(rule_cov, "rule_id")

    assert len(field_ids) == 42, len(field_ids)
    assert len(rule_ids) == 18, len(rule_ids)
    assert test_ids == REQUIRED_TEST_IDS, (test_ids, REQUIRED_TEST_IDS)
    assert covered_fields == field_ids, (covered_fields ^ field_ids)
    assert covered_rules == rule_ids, (covered_rules ^ rule_ids)

    categories = {row["category"] for row in tests}
    assert REQUIRED_CATEGORIES <= categories, REQUIRED_CATEGORIES - categories

    by_test = {row["test_id"]: row for row in tests}
    by_field = {row["field_id"]: row for row in field_cov}
    by_rule = {row["rule_id"]: row for row in rule_cov}

    for row in field_cov:
        ids = refs(row["direct_test_ids"])
        assert ids, f"no tests for field {row['field_id']}"
        assert ids <= test_ids, f"unknown test refs for {row['field_id']}: {ids - test_ids}"
        dimensions = refs(row["coverage_dimensions"])
        assert dimensions, f"no dimensions for {row['field_id']}"
        assert "presence" in ";".join(dimensions) or "observation" in ";".join(dimensions) or "bundle" in ";".join(dimensions) or "trial_result" in dimensions or "blocked_presence" in dimensions, row["field_id"]

    for row in rule_cov:
        ids = refs(row["qualification_test_ids"])
        assert ids, f"no tests for rule {row['rule_id']}"
        assert ids <= test_ids, f"unknown test refs for {row['rule_id']}: {ids - test_ids}"
        assert row["coverage_assertion"], row["rule_id"]
        assert row["evidence_required"], row["rule_id"]

    for row in tests:
        assert row["evidence_tier"] in ALLOWED_TIERS, row["test_id"]
        assert row["runtime_required"] in {"YES", "NO"}, row["test_id"]
        if row["evidence_tier"] == "SPEC_STRUCTURAL":
            assert row["runtime_required"] == "NO", row["test_id"]
        else:
            assert row["runtime_required"] == "YES", row["test_id"]
            assert row["gate_dependency"] != "NONE", row["test_id"]
        if row["evidence_tier"] in {"REFERENCE_BEHAVIOR", "SCIENTIFIC_ADMISSION"}:
            assert row["expected_outcome"].startswith("DEFER_"), row["test_id"]
        text = " ".join(row.values()).lower()
        assert "epsilon=" not in text and "tolerance=" not in text and "1e-" not in text, row["test_id"]

    # Sensitive source-bound seams remain visible in exact field coverage.
    for field in ("HYD-INTERCEPTION-BEGIN", "HYD-INTERCEPTION-END", "HYD-EVAP-INTERCEPTION"):
        assert "TCD-018" in by_field[field]["blocked_or_open_evidence"]
        assert "H013" in refs(by_field[field]["direct_test_ids"])

    mp_fields = {f for f in field_ids if f.startswith("HYD-MP-")}
    assert len(mp_fields) == 5, mp_fields
    for field in mp_fields:
        assert "TCD-025" in by_field[field]["blocked_or_open_evidence"]
        assert {"H014", "H015", "H016"} <= refs(by_field[field]["direct_test_ids"])

    # Typed-event linkage and no-delta-inference are explicit for crop transfers.
    assert "C005" in refs(by_field["CROP-N-UPTAKE-REALIZED"]["direct_test_ids"])
    assert "C006" in refs(by_field["CROP-P-UPTAKE-REALIZED"]["direct_test_ids"])
    assert {"C008", "C009"} <= refs(by_field["CROP-RESIDUE-INPUT-BUNDLE"]["direct_test_ids"])
    assert "C010" in refs(by_field["CROP-EXTERNAL-EXPORT-BUNDLE"]["direct_test_ids"])

    # Every ARCH05 transaction rule is directly represented, including rollback and owner boundaries.
    for rule in (
        "TR-HYDRO-READONLY", "TR-CROP-READONLY", "TR-RESULT-SEPARATION", "TR-REJECT",
        "TR-COMMIT-BARRIER", "TR-RETRY", "TR-MACROPORE-BLOCK", "TR-CHECKPOINT-OWNER",
        "TR-PRECISION-REFERENCE",
    ):
        assert rule in by_rule
        assert refs(by_rule[rule]["qualification_test_ids"])

    # Deferred cases must remain deferred, not structural PASS claims.
    assert by_test["H016"]["expected_outcome"] == "DEFER_UNTIL_ADMITTED"
    assert by_test["T008"]["expected_outcome"] == "DEFER_RUNTIME_COMPARISON"
    assert by_test["T009"]["expected_outcome"] == "DEFER_RUNTIME_COMPARISON"

    # Upstream qualified candidate status files must still exist. This is lineage, not canonical admission.
    assert STATUS05.is_file()
    assert STATUS06.is_file()

    print(
        "ARCH07 PASS: "
        f"arch05_fields={len(field_ids)} arch05_rules={len(rule_ids)} "
        f"tests={len(test_ids)} field_coverage={len(covered_fields)} rule_coverage={len(covered_rules)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ARCH07 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
