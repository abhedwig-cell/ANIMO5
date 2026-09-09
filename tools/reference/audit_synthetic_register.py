#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

REQUIRED = {
    "oracle_id", "process", "target_tcd", "evidence_class", "oracle_level",
    "mathematical_formulation", "inputs", "expected_relation_result", "derivation",
    "independent_implementation_identity", "precision", "units", "applicable_branch_path",
    "assumptions", "B1_result", "pass_fail", "independence_threats",
    "independence_audit", "independence_classification", "what_it_proves",
    "what_it_does_not_prove"
}
ALLOWED_EVIDENCE = {
    "B1_DIAGNOSTIC_OBSERVATION", "SYNTHETIC_CAUSAL_CASE", "ANALYTICAL_ORACLE",
    "CONSERVATION_ORACLE", "METAMORPHIC_ORACLE", "INDEPENDENT_NUMERICAL_ORACLE",
    "HIGH_PRECISION_ORACLE", "THEORY_DERIVED_ORACLE"
}
ALLOWED_INDEPENDENCE = {
    "STRONGLY_INDEPENDENT", "PARTIALLY_INDEPENDENT", "STRUCTURALLY_CORRELATED", "NOT_AN_ORACLE"
}


def audit(register: dict) -> dict:
    errors = []
    records = register.get("oracles", [])
    ids = []
    for i, rec in enumerate(records):
        missing = sorted(REQUIRED - set(rec))
        if missing:
            errors.append(f"record {i} missing fields: {missing}")
        oid = rec.get("oracle_id")
        ids.append(oid)
        if rec.get("evidence_class") not in ALLOWED_EVIDENCE:
            errors.append(f"{oid}: invalid/forbidden evidence_class={rec.get('evidence_class')}")
        if rec.get("evidence_class") == "B2_HISTORICAL_REFERENCE":
            errors.append(f"{oid}: synthetic oracle classified as B2")
        if rec.get("independence_classification") not in ALLOWED_INDEPENDENCE:
            errors.append(f"{oid}: invalid independence classification")
        if rec.get("pass_fail") != "PASS":
            errors.append(f"{oid}: oracle test is not PASS")
        ia = rec.get("independence_audit", {})
        for key in (
            "shares_code_with_animo", "shares_control_flow", "shares_indexing",
            "shares_convergence_logic", "shares_approximations", "equation_independently_reconstructed"
        ):
            if key not in ia:
                errors.append(f"{oid}: independence_audit missing {key}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate oracle_id")
    boundary = register.get("evidence_boundary", {})
    for key in (
        "B2_reference_created", "historical_behaviour_claimed", "corrected_legacy_admitted",
        "production_migration_admitted", "B3_admission_performed"
    ):
        if boundary.get(key) is not False:
            errors.append(f"evidence_boundary.{key} must be false")
    return {
        "audit": "ANIMO-SYNQ01 synthetic register structural audit",
        "record_count": len(records),
        "unique_oracle_ids": len(set(ids)),
        "forbidden_B2_records": sum(1 for r in records if r.get("evidence_class") == "B2_HISTORICAL_REFERENCE"),
        "errors": errors,
        "result": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: audit_synthetic_register.py REGISTER.json OUTPUT.json", file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    result = audit(json.loads(src.read_text(encoding="utf-8")))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
