#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-RG02 G5 stream attachment.

This validates provenance/attachment integrity only. It does not execute ANIMO,
qualify B2 behaviour, admit B3/B4, qualify canonical TIME, or authorize production.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

EXPECTED = {
    "TH01": ("work/animo-th01-rev53-theory-provenance", "a3360415364ef4a66a81d7b6715bcd400829df1b"),
    "TH02": ("work/animo-th02-rev41-lineage-recovery", "f7f3722b14f65340dc6d67a8f80d74f5d0ebb158"),
    "TQ01": ("work/animo-tq01-testcase-qualification", "5c43ee16df37a0a1357614fdec527f25e5ca8c16"),
    "NQ01": ("work/animo-nq01-numerical-qualification-architecture", "e558dff12b127e0662cad62beea7527b42ad89ac"),
    "NQ02": ("work/animo-nq02-tcd019-nonlinear-p-qualification", "e180f7d4898530f704652cb0cfa3834d4de16966"),
    "TS01": ("work/animo-ts01-temporal-semantics", "ed12a678cfba19ce851eb2f380e6da3f49203fe4"),
    "TIME01": ("work/animo-time01-generic-time-transaction-contract", "246128dd14732173a6f27c15c923970d50c14e2a"),
    "ARCHG01": ("work/animo-archg01-candidate-architecture-consolidation", "5cef7969ee921acd2044521cc7636d388aa02efe"),
    "SQ01": ("work/animo-sq01-tcd016-dry-solute-state", "16ca38663b0c72a06b5787d1f4addcde1429f5b8"),
    "MP01": ("work/animo-mp01-macropore-qualification", "7b5979dd6301b9d55d23e8c22948a0dba24b229b"),
    "GHG01": ("work/animo-ghg01-ghg-qualification", "f952bf28c03de911f331762d56613c394529c25a"),
    "B3Q01": ("work/animo-b3q01-scientific-admission-framework", "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"),
}

REQUIRED_GATES = {
    "THEORY", "TESTING", "NUMERICAL", "TEMPORAL", "ARCHITECTURE",
    "TCD016_SCIENCE", "MACROPORE", "GHG", "B3_GOVERNANCE",
    "G6_B2", "G7_B3", "G8_ARCHITECTURE", "G9_B4", "G10_PRODUCTION",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    root = args.root
    checks: list[dict] = []

    try:
        register_path = root / "integration/animo-reg/g5/ANIMO_RG02_G5_STREAM_REGISTER.csv"
        gate_path = root / "integration/animo-reg/g5/ANIMO_RG02_G5_GATE_MATRIX.csv"
        doc_path = root / "docs/governance/ANIMO_RG02_G5_STREAM_ATTACHMENT.md"
        contract_path = root / "docs/governance/ANIMO_RG02_G5_WORK_UNIT_CONTRACT.md"
        for p in [register_path, gate_path, doc_path, contract_path]:
            if not p.is_file():
                raise AssertionError(f"missing required G5 artifact: {p.relative_to(root)}")
        checks.append({"check": "required_artifacts_present", "result": "PASS", "count": 4})

        with register_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        by_id = {r["stream_id"]: r for r in rows}
        if len(rows) != len(EXPECTED) or set(by_id) != set(EXPECTED):
            raise AssertionError(f"stream set mismatch: expected={sorted(EXPECTED)} observed={sorted(by_id)}")
        for sid, (branch, head) in EXPECTED.items():
            row = by_id[sid]
            if row["branch"] != branch:
                raise AssertionError(f"branch mismatch for {sid}: {row['branch']}")
            if row["live_head"] != head:
                raise AssertionError(f"head mismatch for {sid}: {row['live_head']}")
            if not row["status_path"].strip() or not row["qualification_state"].strip():
                raise AssertionError(f"missing status evidence for {sid}")
        checks.append({"check": "exact_stream_branch_head_attachment", "result": "PASS", "streams": len(rows)})

        forbidden_b2 = {"QUALIFIED", "B2_QUALIFIED", "HISTORICAL_REFERENCE_QUALIFIED"}
        for row in rows:
            if row["b2_status"] in forbidden_b2:
                raise AssertionError(f"G5 must not promote B2: {row['stream_id']}={row['b2_status']}")
            if row["b3_status"] == "ADMITTED":
                raise AssertionError(f"G5 must not promote B3: {row['stream_id']}")
        if by_id["TIME01"]["canonical_gate_status"] != "CANONICAL_TIME_NOT_ADMITTED":
            raise AssertionError("TIME01 must remain noncanonical")
        if by_id["B3Q01"]["b3_status"] != "FRAMEWORK_ONLY_NO_BASELINE":
            raise AssertionError("B3Q01 must remain framework-only in G5")
        checks.append({"check": "no_evidence_strength_promotion", "result": "PASS"})

        arch_note = by_id["ARCHG01"]["notes"]
        if "predate TIME01" not in arch_note or "reconciliation required" not in arch_note:
            raise AssertionError("ARCHG01 stale temporal snapshot/revalidation requirement not explicit")
        nq02_note = by_id["NQ02"]["notes"]
        if "not a global NQ02 branch-authority reassignment" not in nq02_note:
            raise AssertionError("NQ02 local G5 authority scope not explicit")
        checks.append({"check": "authority_scope_and_revalidation_guards", "result": "PASS"})

        with gate_path.open(newline="", encoding="utf-8") as f:
            gate_rows = list(csv.DictReader(f))
        gates = {r["gate_or_domain"]: r for r in gate_rows}
        if set(gates) != REQUIRED_GATES:
            raise AssertionError(f"gate matrix mismatch: missing={sorted(REQUIRED_GATES-set(gates))} extra={sorted(set(gates)-REQUIRED_GATES)}")
        for gid in ["G6_B2", "G7_B3", "G8_ARCHITECTURE", "G9_B4", "G10_PRODUCTION"]:
            if gates[gid]["g5_state"] not in {"BLOCKED", "NOT_ESTABLISHED", "NOT_ADMITTED"}:
                raise AssertionError(f"downstream gate improperly advanced: {gid}={gates[gid]['g5_state']}")
        checks.append({"check": "downstream_gates_fail_closed", "result": "PASS"})

        doc = doc_path.read_text(encoding="utf-8")
        for fragment in [
            "attachment without collapse",
            "canonical_time_admitted = false",
            "ARCHG01 live candidate architecture + completed TS01 + TIME01",
            "not a global NQ02 branch-authority reassignment",
            "b3_baseline_established = false",
            "G10 production migration remains not admitted",
            "QUALIFIED_INDEPENDENT_STREAM_ATTACHMENT_NO_SCIENTIFIC_COLLAPSE",
        ]:
            if fragment not in doc:
                raise AssertionError(f"missing governance guard in attachment document: {fragment}")
        checks.append({"check": "governance_guards_present", "result": "PASS"})

        contract = contract_path.read_text(encoding="utf-8")
        for fragment in [
            "b4_baseline_admitted = false",
            "production_migration_admitted = false",
            "No legacy source modification",
            "No historical testcase modification",
        ]:
            if fragment not in contract:
                raise AssertionError(f"missing qualification boundary in G5 contract: {fragment}")
        checks.append({"check": "qualification_boundary_locked", "result": "PASS"})

        result = {
            "work_unit": "ANIMO-RG02-G5",
            "audit_type": "INDEPENDENT_STREAM_ATTACHMENT_STRUCTURAL_AUDIT",
            "result": "PASS",
            "checks": checks,
            "stream_count": len(rows),
            "b2_reference_qualified": False,
            "b3_scientific_admission": False,
            "canonical_time_admitted": False,
            "b4_baseline_admitted": False,
            "production_migration_admitted": False,
        }
    except Exception as exc:
        result = {
            "work_unit": "ANIMO-RG02-G5",
            "audit_type": "INDEPENDENT_STREAM_ATTACHMENT_STRUCTURAL_AUDIT",
            "result": "FAIL",
            "error": str(exc),
            "checks": checks,
            "b2_reference_qualified": False,
            "b3_scientific_admission": False,
            "canonical_time_admitted": False,
            "b4_baseline_admitted": False,
            "production_migration_admitted": False,
        }

    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
