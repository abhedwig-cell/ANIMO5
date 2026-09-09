#!/usr/bin/env python3
"""Fail-closed structural audit for ANIMO-RG02 G5 stream attachment.

This validates provenance and attachment integrity only. It does not execute
ANIMO, qualify B2 behaviour, admit B3/B4, qualify canonical STATE/TIME, or
authorize production.
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
    "TIMEQ01": ("work/animo-timeq01-runtime-transaction-qualification", "ddd5de478165d51a53352033bc92c55ce672d3aa"),
    "ARCHG01": ("work/animo-archg01-candidate-architecture-consolidation", "5cef7969ee921acd2044521cc7636d388aa02efe"),
    "SQ01": ("work/animo-sq01-tcd016-dry-solute-state", "26d0c74aa440bd73c23709d313e24ea8af2a0bcd"),
    "MP01": ("work/animo-mp01-macropore-qualification", "7b5979dd6301b9d55d23e8c22948a0dba24b229b"),
    "MP02": ("work/animo-mp02-whole-case-activation", "6b0f2e7470f13baeb6612b0bddb662a497dea528"),
    "GHG01": ("work/animo-ghg01-ghg-qualification", "9791188672066cf8c0d97cb4dee68d8cdf2e1f4f"),
    "B3Q01": ("work/animo-b3q01-scientific-admission-framework", "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"),
}

REQUIRED_GATES = {
    "THEORY", "TESTING", "NUMERICAL", "TEMPORAL", "ARCHITECTURE",
    "TCD016_SCIENCE", "MACROPORE", "GHG", "B3_GOVERNANCE",
    "G6_B2", "G7_B3", "G8_ARCHITECTURE", "G9_B4", "G10_PRODUCTION",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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
        mp02_attachment_path = root / "integration/animo-reg/g5/ANIMO_RG02_G5_MP02_ATTACHMENT.json"
        timeq01_attachment_path = root / "integration/animo-reg/g5/ANIMO_RG02_G5_TIMEQ01_ATTACHMENT.json"
        required_paths = [
            register_path,
            gate_path,
            doc_path,
            contract_path,
            mp02_attachment_path,
            timeq01_attachment_path,
        ]
        for p in required_paths:
            require(p.is_file(), f"missing required G5 artifact: {p.relative_to(root)}")
        checks.append({"check": "required_artifacts_present", "result": "PASS", "count": len(required_paths)})

        with register_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        by_id = {r["stream_id"]: r for r in rows}
        require(len(rows) == len(EXPECTED), f"stream count mismatch: expected={len(EXPECTED)} observed={len(rows)}")
        require(set(by_id) == set(EXPECTED), f"stream set mismatch: expected={sorted(EXPECTED)} observed={sorted(by_id)}")
        for sid, (branch, head) in EXPECTED.items():
            row = by_id[sid]
            require(row["branch"] == branch, f"branch mismatch for {sid}: {row['branch']}")
            require(row["live_head"] == head, f"head mismatch for {sid}: {row['live_head']}")
            require(bool(row["status_path"].strip()), f"missing status path for {sid}")
            require(bool(row["qualification_state"].strip()), f"missing qualification state for {sid}")
        checks.append({"check": "exact_stream_branch_head_attachment", "result": "PASS", "streams": len(rows)})

        forbidden_b2 = {"QUALIFIED", "B2_QUALIFIED", "HISTORICAL_REFERENCE_QUALIFIED"}
        for row in rows:
            require(row["b2_status"] not in forbidden_b2, f"G5 must not promote B2: {row['stream_id']}={row['b2_status']}")
            require(row["b3_status"] != "ADMITTED", f"G5 must not promote B3: {row['stream_id']}")
        require(by_id["TIME01"]["canonical_gate_status"] == "CANONICAL_TIME_NOT_ADMITTED", "TIME01 must remain noncanonical")
        require(by_id["TIMEQ01"]["canonical_gate_status"] == "CANONICAL_TIME_NOT_ADMITTED", "TIMEQ01 must not admit canonical TIME")
        require(by_id["TIMEQ01"]["b2_status"] == "NOT_QUALIFIED", "TIMEQ01 synthetic runtime evidence must not become B2")
        require(by_id["TIMEQ01"]["b3_status"] == "NOT_ADMITTED", "TIMEQ01 must not become B3")
        require(by_id["B3Q01"]["b3_status"] == "FRAMEWORK_ONLY_NO_BASELINE", "B3Q01 must remain framework-only in G5")
        require(by_id["MP02"]["b2_status"] == "NOT_QUALIFIED" and by_id["MP02"]["b3_status"] == "NOT_ADMITTED", "MP02 complete-case B1 must not be promoted")
        checks.append({"check": "no_evidence_strength_promotion", "result": "PASS"})

        require("not a global NQ02 branch-authority reassignment" in by_id["NQ02"]["notes"], "NQ02 local authority scope not explicit")
        require("revalidation was resolved by ARCHG02" in by_id["ARCHG01"]["notes"], "ARCHG02 temporal revalidation resolution not explicit")
        for fragment in ["complete-case synthetic B1", "not proven historical Intel behaviour", "no B2/B3 promotion"]:
            require(fragment in by_id["MP02"]["notes"], f"MP02 evidence guard missing: {fragment}")
        for fragment in ["19/19 synthetic", "no ANIMO process kernel", "historical behavioural equivalence"]:
            require(fragment in by_id["TIMEQ01"]["notes"], f"TIMEQ01 evidence guard missing: {fragment}")
        checks.append({"check": "authority_scope_and_revalidation_guards", "result": "PASS"})

        with gate_path.open(newline="", encoding="utf-8") as f:
            gate_rows = list(csv.DictReader(f))
        gates = {r["gate_or_domain"]: r for r in gate_rows}
        require(set(gates) == REQUIRED_GATES, f"gate matrix mismatch: missing={sorted(REQUIRED_GATES-set(gates))} extra={sorted(set(gates)-REQUIRED_GATES)}")
        for gid in ["G6_B2", "G7_B3", "G8_ARCHITECTURE", "G9_B4", "G10_PRODUCTION"]:
            require(gates[gid]["g5_state"] in {"BLOCKED", "NOT_ESTABLISHED", "NOT_ADMITTED"}, f"downstream gate advanced: {gid}={gates[gid]['g5_state']}")
        require("TIMEQ01" in gates["TEMPORAL"]["input_streams"], "TIMEQ01 missing from TEMPORAL gate")
        require("ARCHG02" in gates["ARCHITECTURE"]["input_streams"] and "TIMEQ01" in gates["ARCHITECTURE"]["input_streams"], "ARCHG02/TIMEQ01 missing from architecture gate")
        require("ARCHG02" in gates["G8_ARCHITECTURE"]["input_streams"] and "TIMEQ01" in gates["G8_ARCHITECTURE"]["input_streams"], "ARCHG02/TIMEQ01 missing from G8")
        require("MP02" in gates["MACROPORE"]["input_streams"] and "MP02" in gates["NUMERICAL"]["input_streams"], "MP02 missing from macropore/numerical handoff")
        checks.append({"check": "downstream_gates_fail_closed", "result": "PASS"})

        doc = doc_path.read_text(encoding="utf-8")
        for fragment in [
            "attachment without collapse",
            "TIMEQ01@ddd5de478165d51a53352033bc92c55ce672d3aa",
            "19 of 19 contract tests",
            "ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7",
            "G8 still NOT_ADMITTED",
            "b3_baseline_established = false",
            "G10 production migration remains not admitted",
            "QUALIFIED_INDEPENDENT_STREAM_ATTACHMENT_NO_SCIENTIFIC_COLLAPSE",
            "MP02",
            "complete ANIMO orchestration B1",
            "hidden task-state/build-contract dependency",
        ]:
            require(fragment in doc, f"missing governance guard in attachment document: {fragment}")
        checks.append({"check": "governance_guards_present", "result": "PASS"})

        contract = contract_path.read_text(encoding="utf-8")
        for fragment in [
            "b4_baseline_admitted = false",
            "production_migration_admitted = false",
            "No legacy source modification",
            "No historical testcase modification",
        ]:
            require(fragment in contract, f"missing qualification boundary in G5 contract: {fragment}")
        checks.append({"check": "qualification_boundary_locked", "result": "PASS"})

        mp02_attachment = json.loads(mp02_attachment_path.read_text(encoding="utf-8"))
        require(mp02_attachment.get("head") == EXPECTED["MP02"][1], "MP02 attachment head mismatch")
        require(mp02_attachment.get("b2_historically_referenced") is False, "MP02 attachment must preserve B2=false")
        require(mp02_attachment.get("b3_admitted") is False, "MP02 attachment must preserve B3=false")
        require(mp02_attachment.get("tcd025", {}).get("correction_admitted") is False, "MP02 must not admit TCD025 correction")
        handoffs = mp02_attachment.get("new_governance_handoffs", [])
        require(len(handoffs) == 2 and all(h.get("canonical_tcd_allocated_here") is False for h in handoffs), "MP02 handoffs must preserve canonical TCD ownership")
        checks.append({"check": "mp02_attachment_boundaries", "result": "PASS"})

        timeq = json.loads(timeq01_attachment_path.read_text(encoding="utf-8"))
        require(timeq.get("head") == EXPECTED["TIMEQ01"][1], "TIMEQ01 attachment head mismatch")
        require(timeq.get("decision") == "QUALIFIED_CANDIDATE_RUNTIME_TRANSACTION_AND_SCHEDULER_TRACE_FIXTURE_NON_B2_NONPRODUCTION", "TIMEQ01 decision mismatch")
        require(timeq.get("verification", {}).get("conclusion") == "success", "TIMEQ01 CI not successful")
        require(timeq.get("verification", {}).get("tests_passed") == 19 and timeq.get("verification", {}).get("tests_failed") == 0, "TIMEQ01 test count mismatch")
        require(timeq.get("evidence", {}).get("class") == "ARCH_RUNTIME_SYNTHETIC", "TIMEQ01 evidence class mismatch")
        require(timeq.get("evidence", {}).get("b2_reference") is False, "TIMEQ01 attachment must preserve B2=false")
        effect = timeq.get("g5_effect", {})
        for key in ["canonical_state_admitted", "canonical_time_admitted", "b3_scientific_admission", "b4_baseline_admitted", "production_migration_admitted"]:
            require(effect.get(key) is False, f"TIMEQ01 attachment improper admission: {key}")
        require(effect.get("actual_animo_process_kernel_connected") is False and effect.get("real_external_owner_adapter_executed") is False, "TIMEQ01 must not claim real kernel/adapter execution")
        checks.append({"check": "timeq01_attachment_boundaries", "result": "PASS"})

        result = {
            "work_unit": "ANIMO-RG02-G5",
            "audit_type": "INDEPENDENT_STREAM_ATTACHMENT_STRUCTURAL_AUDIT",
            "result": "PASS",
            "checks": checks,
            "stream_count": len(rows),
            "b2_reference_qualified": False,
            "b3_scientific_admission": False,
            "canonical_state_admitted": False,
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
            "canonical_state_admitted": False,
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
