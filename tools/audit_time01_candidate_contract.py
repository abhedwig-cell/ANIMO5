#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-TIME01 candidate contracts.

This tool checks specification integrity only. It does not execute ANIMO,
qualify historical behaviour, define numerical tolerances, or admit TIME.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

EXPECTED_SENTINELS = {f"TS01-S{i:02d}" for i in range(1, 27)}
EXPECTED_REQUIREMENTS = {f"TIME-R{i:02d}" for i in range(1, 27)}
REFERENCE_SENTINELS = {"TS01-S21", "TS01-S22", "TS01-S23", "TS01-S24", "TS01-S25"}
REQUIRED_DOCS = [
    "docs/time01/WORK_UNIT_CONTRACT.md",
    "docs/time01/CANDIDATE_TIME_TRANSACTION_MODEL.md",
    "docs/time01/INTERVAL_FRAME_IDENTITY_CONTRACT.md",
    "docs/time01/SCHEDULER_PARTIAL_ORDER_CONTRACT.md",
    "docs/time01/RETRY_REJECT_CHECKPOINT_POLICY.md",
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
        docs: dict[str, str] = {}
        for rel in REQUIRED_DOCS:
            p = root / rel
            if not p.is_file():
                raise AssertionError(f"required document missing: {rel}")
            docs[rel] = p.read_text(encoding="utf-8")
        checks.append({"check": "required_documents_present", "result": "PASS", "count": len(REQUIRED_DOCS)})

        cov_path = root / "integration/animo-time/TIME01_REQUIREMENT_COVERAGE.csv"
        with cov_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if len(rows) != 26:
            raise AssertionError(f"expected 26 coverage rows, observed {len(rows)}")
        sentinel_ids = [r["ts01_sentinel_id"] for r in rows]
        requirement_ids = [r["time01_requirement_id"] for r in rows]
        if set(sentinel_ids) != EXPECTED_SENTINELS or len(set(sentinel_ids)) != 26:
            raise AssertionError("TS01 sentinel coverage is not exact")
        if set(requirement_ids) != EXPECTED_REQUIREMENTS or len(set(requirement_ids)) != 26:
            raise AssertionError("TIME01 requirement IDs are not exact/unique")
        checks.append({"check": "exact_ts01_to_time01_coverage", "result": "PASS", "rows": len(rows)})

        refs = {r["ts01_sentinel_id"] for r in rows if r["evidence_required"] == "REFERENCE_BEHAVIOR"}
        if refs != REFERENCE_SENTINELS:
            raise AssertionError(f"reference-behaviour set changed: {sorted(refs)}")
        for r in rows:
            if r["ts01_sentinel_id"] in REFERENCE_SENTINELS:
                if r["canonical_time_gate_status"] != "BLOCKED_B2":
                    raise AssertionError(f"B2 sentinel not blocked: {r['ts01_sentinel_id']}")
            elif r["canonical_time_gate_status"] == "BLOCKED_B2":
                raise AssertionError(f"non-reference sentinel incorrectly B2-blocked: {r['ts01_sentinel_id']}")
        checks.append({"check": "reference_behaviour_remains_b2_blocked", "result": "PASS"})

        model = docs["docs/time01/CANDIDATE_TIME_TRANSACTION_MODEL.md"]
        need(model, "ACCEPTED_IDLE -> TRIAL_BOUND -> TRIAL_EXECUTING -> TRIAL_READY", "candidate model")
        need(model, "G_MUTATED_EVENT", "candidate model")
        need(model, "G_PREVIOUS_NEIGHBOR", "candidate model")
        need(model, "G_SAME_STEP_DERIVED", "candidate model")
        need(model, "t0 < E <= t1", "candidate model")
        need(model, "t0 <= H < t1", "candidate model")
        need(model, "Rejected physical events never contribute", "candidate model")
        checks.append({"check": "critical_transaction_and_generation_rules_locked", "result": "PASS"})

        scheduler = docs["docs/time01/SCHEDULER_PARTIAL_ORDER_CONTRACT.md"]
        for fragment in [
            "addition precedes ploughing",
            "PREVIOUS_ACCEPTED_NEIGHBOR",
            "SAME_TRIAL_UPSTREAM",
            "Sqnu",
            "actual NH4 transport",
            "coupled per layer",
            "one transfer identity",
            "balance/report boundary used as commit",
        ]:
            need(scheduler, fragment, "scheduler contract")
        checks.append({"check": "critical_source_order_rules_locked", "result": "PASS"})

        retry = docs["docs/time01/RETRY_REJECT_CHECKPOINT_POLICY.md"]
        for fragment in [
            "Every retry receives a new `trial_id`",
            "A shorter/longer proposed interval is a new interval",
            "portable physical checkpoint may be created only while the model is in accepted-idle state",
            "management/event cursor must be serialized or deterministically reconstructed",
            "side-effect free",
        ]:
            need(retry, fragment, "retry/checkpoint policy")
        checks.append({"check": "retry_reject_checkpoint_rules_locked", "result": "PASS"})

        identity = docs["docs/time01/INTERVAL_FRAME_IDENTITY_CONTRACT.md"]
        for fragment in [
            "Hidden epsilon comparison is forbidden",
            "Changing any semantically relevant field or metadata under the same frame ID is forbidden",
            "changed `t1` under the same `interval_id`",
            "undeclared event endpoint class",
        ]:
            need(identity, fragment, "identity contract")
        checks.append({"check": "identity_fail_closed_rules_locked", "result": "PASS"})

        contract = docs["docs/time01/WORK_UNIT_CONTRACT.md"]
        for fragment in [
            "historical_reference_qualified = false",
            "canonical_time_admitted = false",
            "production_implemented = false",
            "production_migration_admitted = false",
        ]:
            need(contract, fragment, "workunit contract")
        checks.append({"check": "qualification_boundary_locked", "result": "PASS"})

        result = {
            "work_unit": "ANIMO-TIME01",
            "audit_type": "CANDIDATE_TIME_TRANSACTION_CONTRACT_STRUCTURAL_AUDIT",
            "result": "PASS",
            "checks": checks,
            "ts01_sentinel_rows": len(rows),
            "historical_reference_qualified": False,
            "canonical_time_admitted": False,
            "production_implemented": False,
        }
    except Exception as exc:
        result = {
            "work_unit": "ANIMO-TIME01",
            "audit_type": "CANDIDATE_TIME_TRANSACTION_CONTRACT_STRUCTURAL_AUDIT",
            "result": "FAIL",
            "error": str(exc),
            "checks": checks,
            "historical_reference_qualified": False,
            "canonical_time_admitted": False,
            "production_implemented": False,
        }

    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
