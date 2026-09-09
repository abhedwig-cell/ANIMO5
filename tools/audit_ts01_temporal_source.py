#!/usr/bin/env python3
"""Fail-closed static source audit for ANIMO-TS01.

This tool does not execute or modify the frozen ANIMO source. It verifies that the
source anchors on which the TS01 temporal reconstruction depends are present and
ordered as documented. It is source-bound diagnostic tooling, not B2 evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(root: Path, name: str) -> str:
    p = root / name
    if not p.is_file():
        raise AssertionError(f"missing required source file: {name}")
    return p.read_text(encoding="latin-1")


def pos(text: str, needle: str, label: str) -> int:
    i = text.lower().find(needle.lower())
    if i < 0:
        raise AssertionError(f"missing source anchor {label}: {needle}")
    return i


def ordered(text: str, anchors: list[tuple[str, str]]) -> list[dict]:
    hits = []
    last = -1
    for label, needle in anchors:
        i = pos(text, needle, label)
        if i <= last:
            raise AssertionError(f"source order violation at {label}")
        hits.append({"label": label, "offset": i})
        last = i
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-zip", required=True, type=Path)
    ap.add_argument("--source-root", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    checks: list[dict] = []
    try:
        observed_hash = sha256(args.source_zip)
        if observed_hash != EXPECTED_SOURCE_SHA256:
            raise AssertionError(
                f"frozen source hash mismatch: {observed_hash} != {EXPECTED_SOURCE_SHA256}"
            )
        checks.append({"check": "frozen_source_sha256", "result": "PASS", "observed": observed_hash})

        animo = read(args.source_root, "Animo.for")
        init = read(args.source_root, "Init.for")
        addit = read(args.source_root, "Addit.for")
        input_addit = read(args.source_root, "Input_addit.for")
        transport = read(args.source_root, "TRANSPORT.FOR")
        resp = read(args.source_root, "resp_miner.for")
        transgen = read(args.source_root, "Transgen.for")
        output_init = read(args.source_root, "Output_Init.for")
        outbal_calc = read(args.source_root, "Outbal_calc.for")
        outbal_write = read(args.source_root, "Outbal_write.for")

        main_order = ordered(animo, [
            ("loop", "Do While (Juda<Judama)"),
            ("clock_advance", "Sttot = Sttot + 1"),
            ("init", "Call Init"),
            ("input_hydro", "Call Input_hydro"),
            ("addit", "Call Addit"),
            ("ubound", "Call Uboundconc"),
            ("uptake_parameters", "Call Uptpar_"),
            ("rates1", "Call Rates1"),
            ("potential_transca", "Call Transca"),
            ("potential_resp", "Call Resp_miner"),
            ("potential_nh4", "Call Transport"),
            ("rates2", "Call Rates2"),
        ])
        # The repeated calls after Rates2 need scoped searches rather than global find.
        rates2_offset = main_order[-1]["offset"]
        tail = animo[rates2_offset:]
        tail_order = ordered(tail, [
            ("actual_transca", "Call Transca"),
            ("actual_resp", "Call Resp_miner"),
            ("actual_nh4", "CAll Transport"),
            ("denitr", "Call Denitr"),
            ("correction1", "Call Correction(1"),
            ("actual_no3", "Call Transport"),
            ("correction2", "Call Correction(2"),
            ("transgen", "Call Transgen"),
            ("upintg", "Call Upintg_"),
            ("outbal_calc", "Call Outbal_calc"),
            ("outbal_write", "Call Outbal_write"),
            ("outsel", "Call Outsel"),
        ])
        checks.append({"check": "main_timestep_call_order", "result": "PASS", "anchors": main_order + tail_order})

        management_pred = "If(Juda.ge.Tinead .and. (Juda-St).lt.Tinead) Then"
        pos(animo, management_pred, "management_event_predicate")
        checks.append({"check": "management_interval_predicate", "result": "PASS", "semantic_interval": "(t0,t1]"})

        harvest_a = "Juda.Gt.Tiha(Manper)"
        harvest_b = "(Juda-St).Le.Tiha(Manper)"
        pos(addit, harvest_a, "harvest_end_predicate")
        pos(addit, harvest_b, "harvest_start_predicate")
        checks.append({"check": "harvest_interval_predicate", "result": "PASS", "semantic_interval": "[t0,t1)"})

        add_pos = pos(addit, "Do 200   I = 1,Nuad", "management_row_loop")
        plough_pos = pos(addit, "Ploughing (includes emptying of reservoir)", "ploughing")
        if plough_pos <= add_pos:
            raise AssertionError("ploughing source block does not follow management addition block")
        checks.append({"check": "same_row_add_then_plough", "result": "PASS"})

        for needle, label in [
            ("Conhtop = Rsconhtop", "surface_result_to_start"),
            ("Mofro(Ln) = Mofrt(Ln)", "water_end_to_start"),
            ("Conh(Ln) = Rsconh(Ln)", "nh4_result_to_start"),
            ("Coni(Ln) = Rsconi(Ln)", "no3_result_to_start"),
            ("Copo(Ln) = Rscopo(Ln)", "p_result_to_start"),
            ("Amcxfa(I,Ln) = Rsamcxfa(I,Ln)", "fast_p_site_result_to_start"),
            ("Amcxsl(I,Ln) = Rsamcxsl(I,Ln)", "slow_p_site_result_to_start"),
        ]:
            pos(init, needle, label)
        checks.append({"check": "result_to_current_staging", "result": "PASS"})

        pos(init, "before the additions are executed in subroutine ADDIT", "pre_addition_balance_reset_comment")
        checks.append({"check": "management_reporting_reset_before_addit", "result": "PASS"})

        pos(resp, "COINBE= conc from previous timestep", "previous_step_neighbor_comment")
        pos(resp, "Coinab = Conh(Ln-1)", "nh4_previous_neighbor")
        pos(resp, "Coinbe = Conh(Ln+1)", "nh4_previous_neighbor_below")
        pos(resp, "Coinab = Copo(Ln-1)", "p_previous_neighbor")
        pos(resp, "Coinbe = Copo(Ln+1)", "p_previous_neighbor_below")
        pos(resp, "Do While (iter.Le.2", "immobilization_two_pass")
        checks.append({"check": "resp_miner_previous_step_neighbor_and_iteration", "result": "PASS"})

        pos(transport, "Ln = Sqnu(K)", "transport_sqnu")
        pos(transport, "Cob(Ln+1) = Avco(Ln)", "transport_same_step_downstream")
        pos(transport, "Coo(Ln) = Avco(Ln)", "transport_same_step_upstream")
        pos(transport, "Se(Ln)*Flev(Ln)", "transport_crop_uptake")
        checks.append({"check": "transport_flow_order_and_crop_sink", "result": "PASS"})

        pos(transgen, "Ln = Sqnu(K)", "p_sqnu")
        pos(transgen, "Call Transorp", "p_transorp")
        pos(transgen, "Cob(Ln+1) = Avcopo(Ln)", "p_neighbor_average")
        checks.append({"check": "p_transport_phase_coupling", "result": "PASS"})

        pos(outbal_calc, "Optout(Ly) = 0", "balance_period_flag")
        pos(outbal_calc, "Tiyr-0.5*St.Lt. T .And. Tiyr+0.5*St.Ge.T", "balance_half_step_boundary")
        pos(outbal_write, "Bawa(Stsn_b,Ly)=bawa(Stsn_e,Ly)", "balance_storage_rollover")
        checks.append({"check": "report_period_post_step_reset", "result": "PASS"})

        pos(output_init, "Rsamplpo_act = 0.0", "restart_serializer_crop_p_clamp")
        pos(output_init, "!      If (Ioptmp.Eq.1) Then", "commented_macropore_restart")
        pos(output_init, "(RsCsCH4(Ln),Ln=0,Nl)", "ghg_restart_ch4")
        pos(output_init, "(RsCsN2O(Ln),Ln=0,Nl)", "ghg_restart_n2o")
        checks.append({"check": "restart_serializer_boundaries", "result": "PASS"})

        pos(input_addit, "Adnr = Adnr + 1", "management_cursor_advance")
        pos(input_addit, "Tinead = Tinead + Judami - 0.5", "management_next_time_absolute")
        checks.append({"check": "management_cursor_advances_on_read", "result": "PASS"})

        result = {
            "work_unit": "ANIMO-TS01",
            "audit_type": "STATIC_SOURCE_ORDER_AND_TEMPORAL_ANCHOR_AUDIT",
            "result": "PASS",
            "frozen_source_sha256": observed_hash,
            "historical_reference_qualified": False,
            "source_executed": False,
            "source_modified": False,
            "testcase_modified": False,
            "checks": checks,
        }
    except Exception as exc:
        result = {
            "work_unit": "ANIMO-TS01",
            "audit_type": "STATIC_SOURCE_ORDER_AND_TEMPORAL_ANCHOR_AUDIT",
            "result": "FAIL",
            "historical_reference_qualified": False,
            "source_executed": False,
            "source_modified": False,
            "testcase_modified": False,
            "error": str(exc),
            "checks": checks,
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
