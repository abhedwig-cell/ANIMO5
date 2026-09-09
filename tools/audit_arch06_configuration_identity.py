#!/usr/bin/env python3
"""Fail-closed structural and deterministic identity audit for ANIMO-ARCH06."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "integration" / "animo-architecture"
FIELDS = BASE / "ARCH06_MANIFEST_FIELDS.csv"
RULES = BASE / "ARCH06_NORMALIZATION_RULES.csv"
DERIV = BASE / "ARCH06_IDENTITY_DERIVATIONS.csv"
VECTORS = BASE / "ARCH06_IDENTITY_TEST_VECTORS.json"
ARCH04_LAYOUT = BASE / "ARCH04_LAYOUT_SCHEMA.csv"
ARCH05_COMPAT = BASE / "ARCH05_COMPATIBILITY_SCHEMA.csv"

DOMAIN = {
    "feature_set_id": ("feature_set", "ANIMO5_ARCH06_FEATURE_SET_V1"),
    "physical_layout_id": ("physical_layout", "ANIMO5_ARCH06_PHYSICAL_LAYOUT_V1"),
    "exchange_binding_id": ("exchange_binding", "ANIMO5_ARCH06_EXCHANGE_BINDING_V1"),
    "configuration_identity": ("configuration", "ANIMO5_ARCH06_CONFIGURATION_V1"),
    "observer_configuration_id": ("observer_configuration", "ANIMO5_ARCH06_OBSERVER_CONFIGURATION_V1"),
}

REQUIRED_RULES = {
    "NR-UNKNOWN-FIELD", "NR-REQUIRED", "NR-NULL-CONDITIONAL", "NR-BOOL", "NR-INT",
    "NR-ENUM", "NR-STRING", "NR-NULL", "NR-ORDER", "NR-RECORD", "NR-DOMAIN",
    "NR-HASH", "NR-NO-FLOAT", "NR-PARAMETER-REFERENCE", "NR-FORCING-REFERENCE",
    "NR-DIAGNOSTIC-SEPARATION", "NR-TRIAL-SEPARATION", "NR-GHG", "NR-MACROPORE",
    "NR-CROP-ANIMO", "NR-CROP-EXTERNAL", "NR-CROP-NONE", "NR-DORMANT-SURFACE",
}

ARCH04_STATIC_REQUIRED = {
    "state_schema_id", "hydrology_mode", "snow_enabled", "surface_reservoir_enabled",
    "stable_dom_enabled", "crop_mode", "ghg_enabled", "ghg_admission_id",
    "macropore_enabled", "macropore_admission_id", "fast_p_site_count", "slow_p_site_count",
    "layer_count", "organic_fraction_count", "geometry_id", "hydrology_exchange_schema_id",
    "crop_exchange_schema_id", "crop_state_schema_id", "ghg_schema_id", "macropore_schema_id",
    "precision_policy_ref", "diagnostics_mode", "observer_schema_id",
}

ARCH05_STATIC_REQUIRED = {
    "geometry_id", "precision_policy_ref", "hydrology_exchange_schema_id", "hydrology_mode",
    "snow_enabled", "macropore_enabled", "macropore_admission_id", "crop_exchange_schema_id",
    "crop_mode", "exchange_contract_schema_id", "transaction_schema_id",
}

FORBIDDEN_STATIC_FIELDS = {
    "interval_id", "trial_id", "t0", "t1", "producer_accepted_snapshot_id",
    "producer_trial_snapshot_id", "producer_frame_id", "crop_producer_accepted_snapshot_id",
    "crop_producer_trial_snapshot_id", "animo_accepted_snapshot_id", "animo_trial_result_id",
    "hydrology_frame_id", "crop_frame_id", "commit_group_id",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"missing {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def unique(rows: list[dict[str, str]], key: str) -> set[str]:
    vals = [r[key] for r in rows]
    if len(vals) != len(set(vals)):
        raise AssertionError(f"duplicate {key}")
    if any(v == "" for v in vals):
        raise AssertionError(f"empty {key}")
    return set(vals)


def scalar_json(value: object) -> str:
    if isinstance(value, str):
        value = unicodedata.normalize("NFC", value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def validate_manifest(manifest: dict[str, object], rows: list[dict[str, str]]) -> None:
    by_id = {r["field_id"]: r for r in rows}
    unknown = set(manifest) - set(by_id)
    if unknown:
        raise AssertionError(f"unknown manifest fields: {sorted(unknown)}")
    missing = {r["field_id"] for r in rows if r["required"] == "YES"} - set(manifest)
    if missing:
        raise AssertionError(f"missing fields: {sorted(missing)}")

    for field, row in by_id.items():
        value = manifest[field]
        kind = row["value_kind"]
        if isinstance(value, float):
            raise AssertionError(f"float forbidden: {field}")
        if kind == "boolean" and type(value) is not bool:
            raise AssertionError(f"boolean required: {field}")
        elif kind == "integer_ge_0" and (type(value) is not int or value < 0):
            raise AssertionError(f"integer_ge_0 required: {field}")
        elif kind == "integer_gt_0" and (type(value) is not int or value <= 0):
            raise AssertionError(f"integer_gt_0 required: {field}")
        elif kind.startswith("enum_"):
            allowed = set(kind.removeprefix("enum_").split("_"))
            if not isinstance(value, str) or value not in allowed or value != value.lower():
                raise AssertionError(f"invalid enum {field}: {value!r}")
        elif kind == "string":
            if not isinstance(value, str) or not value:
                raise AssertionError(f"nonempty string required: {field}")
        elif kind == "nullable_string":
            if value is not None and (not isinstance(value, str) or not value):
                raise AssertionError(f"nullable string required: {field}")

    def must_null(*names: str) -> None:
        for name in names:
            if manifest[name] is not None:
                raise AssertionError(f"{name} must be null")

    def must_nonnull(*names: str) -> None:
        for name in names:
            if manifest[name] is None:
                raise AssertionError(f"{name} must be non-null")

    if manifest["surface_stable_dom_enabled"] is not False:
        raise AssertionError("dormant surface stable DOM must remain disabled")

    if manifest["ghg_enabled"]:
        must_nonnull("ghg_admission_id", "ghg_schema_id")
    else:
        must_null("ghg_admission_id", "ghg_schema_id")

    if manifest["macropore_enabled"]:
        must_nonnull("macropore_admission_id", "macropore_schema_id")
        if manifest["hydrology_mode"] != "detailed":
            raise AssertionError("macropore requires detailed hydrology")
    else:
        must_null("macropore_admission_id", "macropore_schema_id")

    crop_mode = manifest["crop_mode"]
    if crop_mode == "none":
        must_null("crop_exchange_schema_id", "crop_state_schema_id", "crop_external_schema_id", "crop_producer_contract_id")
    elif crop_mode == "animo":
        must_nonnull("crop_state_schema_id")
        must_null("crop_exchange_schema_id", "crop_external_schema_id", "crop_producer_contract_id")
    elif crop_mode == "external":
        must_nonnull("crop_exchange_schema_id", "crop_external_schema_id", "crop_producer_contract_id")
        must_null("crop_state_schema_id")

    if manifest["diagnostics_mode"] == "off":
        must_null("observer_schema_id")
    else:
        must_nonnull("observer_schema_id")


def derive(manifest: dict[str, object], rows: list[dict[str, str]], identity: str) -> str:
    scope, tag = DOMAIN[identity]
    selected = []
    for row in rows:
        scopes = set(filter(None, row["identity_scope"].split(";")))
        if scope in scopes:
            selected.append(row["field_id"])
    body = tag + "\n"
    for field in sorted(selected):
        body += f"{field}={scalar_json(manifest[field])}\n"
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


def main() -> int:
    field_rows = read_csv(FIELDS)
    rule_rows = read_csv(RULES)
    deriv_rows = read_csv(DERIV)
    arch04_rows = read_csv(ARCH04_LAYOUT)
    arch05_rows = read_csv(ARCH05_COMPAT)

    field_ids = unique(field_rows, "field_id")
    rule_ids = unique(rule_rows, "rule_id")
    deriv_ids = unique(deriv_rows, "identity_name")
    assert rule_ids == REQUIRED_RULES, (rule_ids, REQUIRED_RULES)
    assert deriv_ids == set(DOMAIN), (deriv_ids, set(DOMAIN))
    assert not (field_ids & FORBIDDEN_STATIC_FIELDS), "trial-specific fields leaked into static manifest"
    assert ARCH04_STATIC_REQUIRED <= field_ids, "ARCH04 static compatibility coverage incomplete"
    assert ARCH05_STATIC_REQUIRED <= field_ids, "ARCH05 static compatibility coverage incomplete"

    # Ensure diagnostic fields occur only in observer identity scope.
    for row in field_rows:
        scopes = set(filter(None, row["identity_scope"].split(";")))
        if row["namespace"] == "diagnostics":
            assert scopes <= {"observer_configuration"}
        if row["namespace"] != "diagnostics":
            assert "observer_configuration" not in scopes

    with VECTORS.open(encoding="utf-8") as f:
        vectors = json.load(f)
    base = vectors["base_manifest"]
    validate_manifest(base, field_rows)

    positive = 0
    for case in vectors["positive_cases"]:
        manifest = copy.deepcopy(base)
        manifest.update(case["set"])
        validate_manifest(manifest, field_rows)
        got = {name: derive(manifest, field_rows, name) for name in DOMAIN}
        if got != case["expected"]:
            raise AssertionError(f"identity mismatch {case['case_id']}: {got} != {case['expected']}")
        positive += 1

    negative = 0
    for case in vectors["negative_cases"]:
        manifest = copy.deepcopy(base)
        manifest.update(case["set"])
        try:
            validate_manifest(manifest, field_rows)
        except AssertionError:
            negative += 1
        else:
            raise AssertionError(f"negative case unexpectedly valid: {case['case_id']}")

    # Semantic partition checks from golden cases.
    cases = {c["case_id"]: c["expected"] for c in vectors["positive_cases"]}
    base_ids = cases["BASE"]
    diag_ids = cases["DIAGNOSTICS_ONLY_CHANGE"]
    for name in ("feature_set_id", "physical_layout_id", "exchange_binding_id", "configuration_identity"):
        assert base_ids[name] == diag_ids[name], f"diagnostic leakage into {name}"
    assert base_ids["observer_configuration_id"] != diag_ids["observer_configuration_id"]

    param_ids = cases["PARAMETER_SET_CHANGE"]
    assert base_ids["configuration_identity"] != param_ids["configuration_identity"]
    for name in ("feature_set_id", "physical_layout_id", "exchange_binding_id", "observer_configuration_id"):
        assert base_ids[name] == param_ids[name], f"parameter identity leaked into {name}"

    crop_ids = cases["EXTERNAL_CROP_OWNER"]
    for name in ("feature_set_id", "physical_layout_id", "exchange_binding_id", "configuration_identity"):
        assert base_ids[name] != crop_ids[name], f"crop owner change missing from {name}"

    print(
        "ARCH06 PASS: "
        f"fields={len(field_rows)} rules={len(rule_rows)} identities={len(deriv_rows)} "
        f"positive_vectors={positive} negative_vectors={negative}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ARCH06 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
