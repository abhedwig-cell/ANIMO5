#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-GOV02 evidence governance."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

SCIENTIFIC_ORACLES = {
    "ANALYTICAL_ORACLE",
    "CONSERVATION_ORACLE",
    "METAMORPHIC_ORACLE",
    "INDEPENDENT_NUMERICAL_ORACLE",
    "HIGH_PRECISION_ORACLE",
    "THEORY_DERIVED_ORACLE",
}

ACQ_REQUIRED = {
    "targeted_wur_request_sent_verified_route",
    "response_or_documented_unrecoverable",
    "additional_plausible_route_attempted_or_not_applicable_with_reason",
    "public_search_history_recorded",
    "stopping_rationale_independently_reviewed",
    "no_known_high_probability_route_skipped",
}

HU_ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
HU_ENTRY = "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def valid_b2_evidence(case: dict) -> bool:
    for item in case.get("evidence", []):
        if item.get("class") == "B2" and item.get("source_kind") == "INDEPENDENT_HISTORICAL_REFERENCE":
            return True
    return False


def invalid_b2_promotion(case: dict) -> bool:
    for item in case.get("evidence", []):
        if item.get("class") == "B2" and item.get("source_kind") != "INDEPENDENT_HISTORICAL_REFERENCE":
            return True
    return False


def has_scientific_oracle(case: dict) -> bool:
    return any(item.get("class") in SCIENTIFIC_ORACLES for item in case.get("evidence", []))


def evaluate(case: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    if invalid_b2_promotion(case):
        reasons.append("B2 may only be an independent historical reference; synthetic/B1 promotion rejected")

    claim = case.get("claim_type")
    b3_class = case.get("b3_class")
    route = case.get("route")

    historical_required = claim == "HISTORICAL_FIDELITY_CLAIM" or (
        claim == "REPRESENTATION_EQUIVALENCE_CLAIM"
        and case.get("representation_reference") == "HISTORICAL_BEHAVIOUR"
    )
    if historical_required and not valid_b2_evidence(case):
        reasons.append("historical fidelity/equivalence claim requires qualified B2 evidence")

    if route == HU_ROUTE:
        if case.get("acquisition_state") != HU_ENTRY:
            reasons.append("historical-uncertainty route requires unavailable-after-reasonable-effort closure")
        acq = case.get("acquisition_evidence", {})
        missing = sorted(k for k in ACQ_REQUIRED if acq.get(k) is not True)
        if missing:
            reasons.append("reasonable B2 acquisition effort incomplete: " + ",".join(missing))
        for key in (
            "b1_causality",
            "expected_difference_predeclared",
            "non_interference",
            "path_coverage",
            "independent_cross_check",
            "independent_second_line_review",
        ):
            if case.get(key) is not True:
                reasons.append(f"historical-uncertainty route missing {key}")
        if not has_scientific_oracle(case):
            reasons.append("historical-uncertainty route lacks an accepted scientific-oracle class")

    if b3_class == "A" and route == HU_ROUTE:
        if case.get("closed_conservation_identity") is not True:
            reasons.append("Class A no-B2 route requires a closed conservation identity")
        if case.get("physical_state_flux_non_interference") is not True:
            reasons.append("Class A no-B2 route requires physical state/flux non-interference")

    if b3_class == "C" and route == HU_ROUTE:
        if case.get("state_model_authority") is not True:
            reasons.append("Class C missing-state claim requires independent state-model/theory authority")

    if b3_class == "E":
        if case.get("smaller_residual_only") is True:
            reasons.append("smaller residual is not a numerical-policy correctness oracle")
        for key in (
            "numerical_formulation_authority",
            "convergence_study",
            "precision_discretization_study",
            "independent_numerical_review",
        ):
            if case.get(key) is not True:
                reasons.append(f"Class E numerical policy missing {key}")

    if b3_class == "F" and route == HU_ROUTE:
        reasons.append("Class F physics/model evolution cannot use historical-uncertainty as a legacy-correction shortcut")

    return (not reasons), reasons


def validate_policy(root: Path) -> list[str]:
    errors: list[str] = []
    dag = load_json(root / "integration/animo-governance/ANIMO_EVIDENCE_DAG.json")

    assertions = dag.get("governance_assertions", {})
    for key in (
        "B2_devalued",
        "synthetic_evidence_promoted_to_B2",
        "historical_uncertainty_route_weakened",
        "new_TCD_admissions",
        "B3_global_baseline_established",
        "B4_admitted",
        "production_migration_admitted",
    ):
        if assertions.get(key) is not False:
            errors.append(f"governance assertion {key} must be false")

    if dag.get("current_prep02r_policy_state") != "B2_ACQUISITION_STILL_ACTIVE":
        errors.append("current PREP02R policy state must remain B2_ACQUISITION_STILL_ACTIVE")
    if dag.get("current_prep02r_route_eligible") is not False:
        errors.append("current PREP02R historical-uncertainty route must be ineligible")

    oracle_classes = set(dag.get("scientific_oracle_classes", []))
    if oracle_classes != SCIENTIFIC_ORACLES:
        errors.append("scientific oracle taxonomy differs from reconciled SYNQ01 classes")

    forbidden = set(dag.get("forbidden_promotions", []))
    for needed in (
        "SYNTHETIC_EVIDENCE_TO_B2",
        "B1_OUTPUT_TO_B2",
        "B2_AGREEMENT_TO_SCIENTIFIC_CORRECTNESS",
        "SMALLER_RESIDUAL_TO_NUMERICAL_CORRECTNESS",
        "MASS_CLOSURE_ONLY_TO_CLASS_C_STATE_AUTHORITY",
    ):
        if needed not in forbidden:
            errors.append(f"missing forbidden promotion {needed}")

    routes = dag.get("routes", {})
    hu = routes.get(HU_ROUTE, {})
    if hu.get("entry_prep02r_state") != HU_ENTRY:
        errors.append("historical-uncertainty entry state is weakened or incorrect")
    if hu.get("evidence_burden_lower_than_b2_backed_route") is not False:
        errors.append("historical-uncertainty route may not lower evidence burden")
    if hu.get("historical_fidelity_claim_admitted") is not False:
        errors.append("historical-uncertainty route may not admit historical fidelity")

    matrix_path = root / "integration/animo-governance/B2_REQUIREMENT_MATRIX.csv"
    with matrix_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    classes = {row["b3_class"] for row in rows}
    for needed in {"ALL", "A", "B", "C", "D", "E", "F"}:
        if needed not in classes:
            errors.append(f"B2 matrix missing class {needed}")

    return errors


def run_cases(root: Path) -> tuple[list[dict], list[str]]:
    data = load_json(root / "integration/animo-governance/GOV02_VALIDATION_CASES.json")
    results = []
    errors = []
    for case in data.get("cases", []):
        allowed, reasons = evaluate(case)
        observed = "ALLOW" if allowed else "REJECT"
        expected = case.get("expected")
        results.append({"id": case.get("id"), "expected": expected, "observed": observed, "reasons": reasons})
        if observed != expected:
            errors.append(f"{case.get('id')}: expected {expected}, observed {observed}: {'; '.join(reasons)}")
    return results, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write-result", type=Path)
    args = parser.parse_args()

    policy_errors = validate_policy(args.root)
    results, case_errors = run_cases(args.root)
    errors = policy_errors + case_errors
    payload = {
        "work_unit": "ANIMO-GOV02",
        "validator": "tools/validate_gov02_evidence_dag.py",
        "result": "PASS" if not errors else "FAIL",
        "cases": results,
        "errors": errors,
    }
    if args.write_result:
        args.write_result.parent.mkdir(parents=True, exist_ok=True)
        args.write_result.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
