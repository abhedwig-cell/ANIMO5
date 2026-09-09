#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-ARCHG02 temporal revalidation.

This validates candidate architecture revalidation integrity only. It does not
execute ANIMO, qualify B2 behaviour, admit canonical STATE/TIME, admit B3/B4,
or authorize production migration.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

EXPECTED_IDS = {f"ARCHG02-R{i:02d}" for i in range(1, 22)}
EXPECTED_SEAMS = {
    "hydrology_exchange", "mineral_nitrogen", "phosphorus", "organic_matter",
    "crop", "management", "dissolved_organic", "ghg", "macropores",
    "restart_checkpoint", "mass_ledger", "external_exchange",
    "overall_candidate_architecture",
}
REQUIRED_FILES = [
    "docs/architecture/ANIMO_ARCHG02_WORK_UNIT_CONTRACT.md",
    "docs/architecture/ANIMO5_FINAL_TEMPORAL_REVALIDATION.md",
    "integration/animo-architecture/ARCHG02_TEMPORAL_REVALIDATION_MATRIX.csv",
    "integration/animo-architecture/ARCHG02_MIGRATION_SEAM_READINESS.csv",
]


def need(text: str, fragment: str, where: str) -> None:
    if fragment not in text:
        raise AssertionError(f"missing required fragment in {where}: {fragment}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    root = args.root
    checks: list[dict] = []

    try:
        for rel in REQUIRED_FILES:
            if not (root / rel).is_file():
                raise AssertionError(f"required artifact missing: {rel}")
        checks.append({"check": "required_artifacts_present", "result": "PASS", "count": len(REQUIRED_FILES)})

        contract = (root / REQUIRED_FILES[0]).read_text(encoding="utf-8")
        pins = {
            "ARCHG01": "5cef7969ee921acd2044521cc7636d388aa02efe",
            "TS01": "ed12a678cfba19ce851eb2f380e6da3f49203fe4",
            "TIME01": "246128dd14732173a6f27c15c923970d50c14e2a",
            "RG02 G5": "b289174f4378dcbfcfea9c0d77d0665b3b6c2603",
        }
        for label, head in pins.items():
            need(contract, head, f"work-unit contract {label} pin")
        checks.append({"check": "authoritative_input_heads_pinned", "result": "PASS", "count": len(pins)})

        matrix_path = root / "integration/animo-architecture/ARCHG02_TEMPORAL_REVALIDATION_MATRIX.csv"
        with matrix_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        by_id = {(r["item_id"] or "").strip(): r for r in rows}
        if len(rows) != 21 or set(by_id) != EXPECTED_IDS:
            raise AssertionError(f"temporal matrix coverage mismatch: rows={len(rows)} ids={sorted(by_id)}")
        if len(by_id) != len(rows):
            raise AssertionError("duplicate ARCHG02 item_id")
        checks.append({"check": "exact_temporal_revalidation_coverage", "result": "PASS", "rows": len(rows)})

        def disposition(rid: str) -> str:
            return (by_id[rid]["disposition"] or "").strip()

        contradicted = "CONTRADICTED_AS_LITERAL_LEGACY_BUT_VALID_CANDIDATE_ABSTRACTION"
        for rid in ["ARCHG02-R02", "ARCHG02-R03"]:
            if disposition(rid) != contradicted:
                raise AssertionError(f"literal legacy contradiction guard changed for {rid}")
        for rid in ["ARCHG02-R04", "ARCHG02-R05", "ARCHG02-R07", "ARCHG02-R08"]:
            if disposition(rid) != "SOURCE_CONSTRAINT_NOW_RESOLVED":
                raise AssertionError(f"source-bound resolution lost for {rid}")
        for rid in ["ARCHG02-R10", "ARCHG02-R11", "ARCHG02-R12", "ARCHG02-R13", "ARCHG02-R17"]:
            if disposition(rid) != "CANDIDATE_POLICY_NOW_SPECIFIED_NONCANONICAL":
                raise AssertionError(f"candidate policy/noncanonical boundary changed for {rid}")
        if disposition("ARCHG02-R15") != "REMAINS_BLOCKED_B2":
            raise AssertionError("split-run B2 blocker lost")
        if disposition("ARCHG02-R16") != "REMAINS_BLOCKED_CANONICAL_STATE_TIME":
            raise AssertionError("canonical STATE/TIME blocker lost")
        for rid in ["ARCHG02-R19", "ARCHG02-R20", "ARCHG02-R21"]:
            if disposition(rid) != "REMAINS_BLOCKED_SCIENTIFIC_OR_NUMERICAL":
                raise AssertionError(f"scientific/numerical blocker lost for {rid}")
        checks.append({"check": "critical_temporal_dispositions_locked", "result": "PASS"})

        seam_path = root / "integration/animo-architecture/ARCHG02_MIGRATION_SEAM_READINESS.csv"
        with seam_path.open(newline="", encoding="utf-8") as f:
            seam_rows = list(csv.DictReader(f))
        seams = {(r["seam"] or "").strip(): r for r in seam_rows}
        if set(seams) != EXPECTED_SEAMS or len(seam_rows) != len(EXPECTED_SEAMS):
            raise AssertionError(f"migration seam coverage mismatch: observed={sorted(seams)}")
        for seam, row in seams.items():
            if (row["production_admitted"] or "").strip() != "NO":
                raise AssertionError(f"production improperly admitted for seam {seam}")
        if (seams["overall_candidate_architecture"]["archg02_temporal_revalidation"] or "").strip() != "REVALIDATED_WITH_FINAL_TS01_TIME01_CONSTRAINTS":
            raise AssertionError("overall revalidation disposition changed")
        checks.append({"check": "migration_seams_remain_nonproduction", "result": "PASS", "seams": len(seam_rows)})

        doc = (root / "docs/architecture/ANIMO5_FINAL_TEMPORAL_REVALIDATION.md").read_text(encoding="utf-8")
        for fragment in [
            "modern abstraction rather than a literal description of revision-53 storage mechanics",
            "does not execute one literal atomic end-of-step commit",
            "A retry receives a fresh `trial_id`",
            "canonical TIME admission",
            "strong continuous-versus-split behavioural equivalence",
            "No final TS01/TIME01 result requires abandoning the ARCHG01 object graph",
            "QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED_AGAINST_FINAL_TS01_TIME01_PRODUCTION_NOT_ADMITTED",
            "does not admit canonical TIME, B3, B4 or production migration",
        ]:
            need(doc, fragment, "final temporal revalidation")
        checks.append({"check": "architecture_revalidation_guards_present", "result": "PASS"})

        for fragment in [
            "no canonical STATE or TIME admission",
            "no B2 promotion",
            "no B3/B4 admission",
            "no production migration admission",
            "no silent rewrite of ARCHG01 historical artifacts",
        ]:
            need(contract, fragment, "work-unit contract qualification boundary")
        checks.append({"check": "qualification_boundary_locked", "result": "PASS"})

        result = {
            "work_unit": "ANIMO-ARCHG02",
            "audit_type": "FINAL_TS01_TIME01_CANDIDATE_ARCHITECTURE_REVALIDATION_STRUCTURAL_AUDIT",
            "result": "PASS",
            "checks": checks,
            "temporal_revalidation_rows": len(rows),
            "migration_seam_rows": len(seam_rows),
            "historical_reference_qualified": False,
            "canonical_state_admitted": False,
            "canonical_time_admitted": False,
            "b3_scientific_admission": False,
            "b4_baseline_admitted": False,
            "production_migration_admitted": False,
            "runtime_scheduler_executed": False,
        }
    except Exception as exc:
        result = {
            "work_unit": "ANIMO-ARCHG02",
            "audit_type": "FINAL_TS01_TIME01_CANDIDATE_ARCHITECTURE_REVALIDATION_STRUCTURAL_AUDIT",
            "result": "FAIL",
            "error": str(exc),
            "checks": checks,
            "historical_reference_qualified": False,
            "canonical_state_admitted": False,
            "canonical_time_admitted": False,
            "b3_scientific_admission": False,
            "b4_baseline_admitted": False,
            "production_migration_admitted": False,
            "runtime_scheduler_executed": False,
        }

    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
