#!/usr/bin/env python3
"""Fail-closed structural audit for the ANIMO-TS01 scheduler sentinel matrix.

This checks specification integrity only. It does not execute ANIMO, qualify
historical behaviour, define numerical tolerance, or admit canonical TIME.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

EXPECTED_IDS = {f"TS01-S{i:02d}" for i in range(1, 27)}
ALLOWED_TIERS = {
    "SOURCE_STATIC",
    "SYNTHETIC_CAUSAL",
    "ARCH_CONTRACT",
    "REFERENCE_BEHAVIOR",
    "SCIENTIFIC_ADMISSION",
}
ALLOWED_B2 = {"NOT_B2", "REQUIRES_B2"}
REQUIRED_COLUMNS = {
    "sentinel_id",
    "seam",
    "trigger",
    "required_order_or_rule",
    "read_generation",
    "write_or_effect",
    "evidence_tier",
    "b2_status",
    "dependency",
    "source_anchor",
    "failure_mode",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    checks: list[dict] = []
    result: dict
    try:
        with args.matrix.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = set(reader.fieldnames or [])
            if columns != REQUIRED_COLUMNS:
                raise AssertionError(
                    f"column mismatch: missing={sorted(REQUIRED_COLUMNS-columns)} extra={sorted(columns-REQUIRED_COLUMNS)}"
                )
            rows = list(reader)

        ids = [r["sentinel_id"] for r in rows]
        if len(rows) != 26:
            raise AssertionError(f"expected 26 sentinel rows, observed {len(rows)}")
        if len(ids) != len(set(ids)):
            raise AssertionError("duplicate sentinel_id")
        if set(ids) != EXPECTED_IDS:
            raise AssertionError(
                f"sentinel coverage mismatch: missing={sorted(EXPECTED_IDS-set(ids))} extra={sorted(set(ids)-EXPECTED_IDS)}"
            )
        checks.append({"check": "exact_sentinel_coverage", "result": "PASS", "rows": len(rows)})

        for r in rows:
            if not all((r[c] or "").strip() for c in REQUIRED_COLUMNS):
                raise AssertionError(f"empty required field in {r['sentinel_id']}")
            if r["evidence_tier"] not in ALLOWED_TIERS:
                raise AssertionError(f"invalid evidence tier in {r['sentinel_id']}: {r['evidence_tier']}")
            if r["b2_status"] not in ALLOWED_B2:
                raise AssertionError(f"invalid b2 status in {r['sentinel_id']}: {r['b2_status']}")
            if r["evidence_tier"] == "REFERENCE_BEHAVIOR" and r["b2_status"] != "REQUIRES_B2":
                raise AssertionError(f"reference behaviour must require B2: {r['sentinel_id']}")
            if r["evidence_tier"] != "REFERENCE_BEHAVIOR" and r["b2_status"] == "REQUIRES_B2":
                raise AssertionError(f"only reference behaviour may be marked REQUIRES_B2: {r['sentinel_id']}")
        checks.append({"check": "tier_and_b2_consistency", "result": "PASS"})

        by_id = {r["sentinel_id"]: r for r in rows}
        if by_id["TS01-S03"]["required_order_or_rule"] != "t0 < E <= t1":
            raise AssertionError("management endpoint convention changed")
        if by_id["TS01-S04"]["required_order_or_rule"] != "t0 <= H < t1":
            raise AssertionError("harvest endpoint convention changed")
        if "addition before ploughing" not in by_id["TS01-S05"]["required_order_or_rule"]:
            raise AssertionError("same-row add-before-plough rule missing")
        if by_id["TS01-S10"]["read_generation"] != "G_PREVIOUS_NEIGHBOR":
            raise AssertionError("Resp_miner previous-neighbour generation changed")
        if "Sqnu" not in by_id["TS01-S11"]["required_order_or_rule"]:
            raise AssertionError("generic transport Sqnu ordering missing")
        if "couples transport sorption/desorption precipitation per layer" not in by_id["TS01-S13"]["required_order_or_rule"]:
            raise AssertionError("P coupled-layer rule missing")
        if by_id["TS01-S16"]["write_or_effect"] != "G_REPORT_ONLY":
            raise AssertionError("report reset must remain report-only")
        if by_id["TS01-S18"]["read_generation"] != "G_ACTUAL_RESULT":
            raise AssertionError("final serialization must read actual result generation")
        checks.append({"check": "critical_temporal_rules_locked", "result": "PASS"})

        reference_ids = {r["sentinel_id"] for r in rows if r["evidence_tier"] == "REFERENCE_BEHAVIOR"}
        expected_reference = {"TS01-S21", "TS01-S22", "TS01-S23", "TS01-S24", "TS01-S25"}
        if reference_ids != expected_reference:
            raise AssertionError(
                f"reference sentinel set changed: expected={sorted(expected_reference)} observed={sorted(reference_ids)}"
            )
        checks.append({"check": "reference_tests_remain_blocked", "result": "PASS"})

        if any(r["evidence_tier"] == "SCIENTIFIC_ADMISSION" for r in rows):
            raise AssertionError("no scientific-admission sentinel should be claimed by TS01 continuation")
        checks.append({"check": "no_scientific_admission_claim", "result": "PASS"})

        result = {
            "work_unit": "ANIMO-TS01",
            "audit_type": "SCHEDULER_SENTINEL_SPEC_STRUCTURAL_AUDIT",
            "result": "PASS",
            "rows": len(rows),
            "checks": checks,
            "historical_reference_qualified": False,
            "canonical_time_admitted": False,
            "production_implementation": False,
        }
    except Exception as exc:
        result = {
            "work_unit": "ANIMO-TS01",
            "audit_type": "SCHEDULER_SENTINEL_SPEC_STRUCTURAL_AUDIT",
            "result": "FAIL",
            "error": str(exc),
            "checks": checks,
            "historical_reference_qualified": False,
            "canonical_time_admitted": False,
            "production_implementation": False,
        }

    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
