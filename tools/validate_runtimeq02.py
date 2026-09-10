#!/usr/bin/env python3
"""Fail-closed structural and scope validator for ANIMO-RUNTIMEQ02."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
BRANCH = "work/animo-runtimeq02-tcd037-ghg-balance-array-lifetime"
STATUS_PATH = ROOT / "integration/animo-runtime/ANIMO-RUNTIMEQ02_STATUS.json"
MATRIX_PATH = ROOT / "integration/animo-runtime/TCD037_GHG_BALANCE_OWNERSHIP_MATRIX.json"
DOC_PATH = ROOT / "docs/runtime/TCD037_GHG_BALANCE_WORKING_ARRAY_OWNERSHIP_QUALIFICATION.md"
CONTRACT_PATH = ROOT / "docs/runtime/ANIMO-RUNTIMEQ02_WORK_UNIT_CONTRACT.md"
PROBE_PATH = ROOT / "tools/runtimeq02/runtimeq02_observer_lifetime_probe.f90"
WORKFLOW_PATH = ROOT / ".github/workflows/animo-runtimeq02-tcd037-ghg-balance-array-lifetime.yml"

ALLOWED_PATHS = {
    ".github/workflows/animo-runtimeq02-tcd037-ghg-balance-array-lifetime.yml",
    "docs/runtime/ANIMO-RUNTIMEQ02_WORK_UNIT_CONTRACT.md",
    "docs/runtime/TCD037_GHG_BALANCE_WORKING_ARRAY_OWNERSHIP_QUALIFICATION.md",
    "integration/animo-runtime/ANIMO-RUNTIMEQ02_STATUS.json",
    "integration/animo-runtime/TCD037_GHG_BALANCE_OWNERSHIP_MATRIX.json",
    "tools/runtimeq02/runtimeq02_observer_lifetime_probe.f90",
    "tools/validate_runtimeq02.py",
}


def fail(message: str) -> None:
    raise SystemExit(f"RUNTIMEQ02 FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_scope() -> None:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{BASE}..HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot evaluate scope against authoring base {BASE}: {exc}")

    changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    unexpected = sorted(changed - ALLOWED_PATHS)
    require(not unexpected, f"out-of-scope paths changed: {unexpected}")
    require(
        {
            "docs/runtime/TCD037_GHG_BALANCE_WORKING_ARRAY_OWNERSHIP_QUALIFICATION.md",
            "integration/animo-runtime/ANIMO-RUNTIMEQ02_STATUS.json",
            "integration/animo-runtime/TCD037_GHG_BALANCE_OWNERSHIP_MATRIX.json",
            "tools/runtimeq02/runtimeq02_observer_lifetime_probe.f90",
        }.issubset(changed),
        "qualification evidence set is incomplete",
    )


def validate_status(status: dict) -> None:
    require(status.get("work_unit") == "ANIMO-RUNTIMEQ02", "wrong work unit")
    require(status.get("tcd") == "TCD-037", "wrong TCD")
    require(status.get("branch") == BRANCH, "wrong branch")
    require(
        status.get("status")
        == "QUALIFIED_SOURCE_RUNTIME_OWNERSHIP_TIER_C_ACCOUNTING_SEMANTICS_PENDING",
        "unexpected closeout status",
    )
    require(
        status.get("authoring_base") == f"ANIMO-RG05G@{BASE}",
        "authoring base drift",
    )
    require(
        status.get("canonical_routing_authority")
        == "ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9",
        "canonical routing authority drift",
    )
    require(
        status.get("frozen_source_sha256")
        == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
        "frozen source identity drift",
    )

    ownership = status.get("runtime_ownership_result", {})
    require(
        ownership.get("AmCH4")
        == "PROCEDURE_LOCAL_UNDEFINED_ON_ENTRY_WITH_NO_SOURCE_PRODUCER",
        "AmCH4 ownership must fail closed",
    )
    require(
        ownership.get("AmN2Odeni")
        == "PROCEDURE_LOCAL_UNDEFINED_ON_ENTRY_WITH_NO_SOURCE_PRODUCER",
        "AmN2Odeni ownership must fail closed",
    )
    require(
        ownership.get("AmN2Onitr")
        == "ACTIVE_OUTBAL_CALL_LOCAL_TIMESTEP_AMOUNT_SCRATCH",
        "AmN2Onitr positive-control lifetime drift",
    )
    require(ownership.get("silent_persistence_is_valid_ownership") is False, "persistence cannot be ownership")
    require(ownership.get("restart_checkpoint_state_involved") is False, "working arrays must not become checkpoint state")
    require(ownership.get("scoped_observer_non_interference") is True, "observer non-interference is not recorded PASS")

    evidence = status.get("evidence", {})
    require(evidence.get("first_write_before_first_read_AmCH4") is False, "AmCH4 first-write finding drift")
    require(evidence.get("first_write_before_first_read_AmN2Odeni") is False, "AmN2Odeni first-write finding drift")
    require(evidence.get("first_write_before_first_read_AmN2Onitr") is True, "AmN2Onitr first-write positive control drift")
    require(evidence.get("complete_writer_reader_inventory") is True, "writer/reader inventory incomplete")
    require(evidence.get("control_flow_reachability") is True, "control-flow reachability incomplete")
    require(evidence.get("inactive_ghg_control") == "PASS", "inactive GHG control not PASS")
    require(
        evidence.get("natural_active_ghg_case") == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH",
        "natural active-GHG limitation must remain explicit",
    )
    require(evidence.get("synthetic_active_ghg_discriminator") == "PASS_B1_CAUSAL_ONLY", "B1 discriminator missing")
    require(evidence.get("multi_step_lifetime_discriminator") == "PASS", "lifetime discriminator missing")
    require(evidence.get("repeated_call_discriminator") == "PASS", "repeated-call discriminator missing")
    require(evidence.get("observer_non_interference") == "PASS", "observer non-interference missing")
    require(evidence.get("historical_intel_behavior") == "UNKNOWN", "historical behavior must remain UNKNOWN")

    expected = status.get("expected_difference", {})
    require(expected.get("qualification_branch") == "NO_PRODUCTION_DIFFERENCE", "qualification expected-difference drift")
    require(
        expected.get("future_correction_whitelist") == "BLOCKED_PENDING_ACCOUNTING_SEMANTICS",
        "future correction whitelist must remain blocked",
    )

    gov04 = status.get("gov04", {})
    require(gov04.get("risk_tier") == "C", "GOV04 risk tier must be C")
    require(gov04.get("tier_a_waiver") == "NOT_AVAILABLE", "Tier-A waiver must remain unavailable")

    require(status.get("admission_readiness") is False, "TCD-037 must not be admission-ready")
    require(status.get("scientific_admission") is False, "scientific admission is forbidden")
    require(status.get("production_patch") is False, "production patch is forbidden")
    require(status.get("b4") is False, "B4 opening is forbidden")
    require(status.get("rg05h_update") is False, "RG05H update is forbidden")
    require(status.get("composition") == [], "TCD composition is forbidden")
    require(status.get("tier_a_combination_safe_now") is False, "readiness/admission combination must not be enabled")
    require(
        status.get("next_work_unit")
        == "ANIMO-RUNTIMEQ03 — TCD-037 GHG Balance Observer Accounting-Semantics & Index-0 Producer Mapping Qualification",
        "next routing drift",
    )


def validate_matrix(matrix: dict) -> None:
    require(matrix.get("schema") == "ANIMO_RUNTIME_OWNERSHIP_MATRIX_V1", "wrong matrix schema")
    require(matrix.get("work_unit") == "ANIMO-RUNTIMEQ02", "matrix work unit mismatch")
    require(matrix.get("tcd") == "TCD-037", "matrix TCD mismatch")
    require(matrix.get("authoring_base", {}).get("sha") == BASE, "matrix authoring base drift")

    symbols = matrix.get("symbols", {})
    require(set(symbols) == {"AmCH4", "AmN2Odeni", "AmN2Onitr"}, "working-array set drift")

    amch4 = symbols["AmCH4"]
    require(amch4.get("scope") == "PROCEDURE_LOCAL", "AmCH4 scope drift")
    require(amch4.get("active_writers") == [], "AmCH4 must have no active source writer")
    require(amch4.get("active_readers") == ["Outbal_calc.for:636", "Outbal_calc.for:653"], "AmCH4 reader inventory drift")
    require(amch4.get("first_write_before_first_read") is False, "AmCH4 first-read classification drift")
    require(amch4.get("persistent_model_state") is False, "AmCH4 must not be persistent ModelState")
    require(amch4.get("checkpoint_state") is False, "AmCH4 must not be checkpoint state")

    deni = symbols["AmN2Odeni"]
    require(deni.get("scope") == "PROCEDURE_LOCAL", "AmN2Odeni scope drift")
    require(deni.get("active_writers") == [], "AmN2Odeni must have no active source writer")
    require(deni.get("active_readers") == ["Outbal_calc.for:1133", "Outbal_calc.for:1135"], "AmN2Odeni reader inventory drift")
    require(deni.get("first_write_before_first_read") is False, "AmN2Odeni first-read classification drift")
    require(deni.get("persistent_model_state") is False, "AmN2Odeni must not be persistent ModelState")
    require(deni.get("checkpoint_state") is False, "AmN2Odeni must not be checkpoint state")

    nitr = symbols["AmN2Onitr"]
    require(nitr.get("scope") == "PROCEDURE_LOCAL", "AmN2Onitr scope drift")
    require(
        nitr.get("active_writers")
        == ["Outbal_calc.for:186", "Outbal_calc.for:188", "Outbal_calc.for:191"],
        "AmN2Onitr writer inventory drift",
    )
    require(nitr.get("first_write_before_first_read") is True, "AmN2Onitr must remain the positive control")
    require(nitr.get("persistent_model_state") is False, "AmN2Onitr must not be persistent ModelState")
    require(nitr.get("checkpoint_state") is False, "AmN2Onitr must not be checkpoint state")

    call_surface = matrix.get("call_surface", {})
    require(call_surface.get("missing_working_arrays_are_formal_arguments") is False, "interface result drift")
    require(call_surface.get("physical_ghg_production_arrays_are_passed_to_outbal_calc") is False, "physical producer interface drift")
    require(call_surface.get("suspect_reads_guard") == "IoptGHG >= 1", "GHG control guard drift")

    runtime = matrix.get("runtime_evidence", {})
    require(runtime.get("natural_active_ghg") == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural GHG limitation drift")
    require(runtime.get("inactive_ghg_control") == "PASS", "inactive control not PASS")
    require(runtime.get("synthetic_source_shaped_activation") == "PASS_B1_CAUSAL_ONLY", "synthetic activation not bounded as B1")
    require(runtime.get("multi_call_lifetime_discriminator") == "PASS", "multi-call discriminator missing")
    require(runtime.get("counterfactual_persistence_stale_reuse_discriminator") == "PASS", "stale-persistence discriminator missing")
    require(runtime.get("historical_intel_behavior") == "UNKNOWN", "historical Intel behavior must remain UNKNOWN")

    accounting = matrix.get("accounting_semantics", {})
    require(accounting.get("index0_and_emission_mapping_qualified") is False, "index-0 mapping must remain unresolved")
    require(accounting.get("exact_accounting_owner") == "UNRESOLVED_INDEX0_AND_EMISSION_MAPPING", "accounting owner drift")
    require(accounting.get("silent_qpr_times_st_substitution_allowed") is False, "unqualified QPr*St substitution is forbidden")

    observer = matrix.get("observer_non_interference", {})
    require(observer.get("physical_state_change_from_tcd037_working_arrays") is False, "physical-state interference detected")
    require(observer.get("process_flux_change_from_tcd037_working_arrays") is False, "process-flux interference detected")
    require(observer.get("balance_accumulator_mutation") is True, "observer accumulator ownership missing")

    risk = matrix.get("gov04", {})
    require(risk.get("risk_tier") == "C", "matrix GOV04 tier must be C")
    require(risk.get("tier_a_waiver_available") is False, "matrix Tier-A waiver must be unavailable")
    require(risk.get("independent_second_line_required_before_admission") is True, "Tier-C independent review requirement lost")

    admission = matrix.get("admission", {})
    require(admission.get("runtime_ownership_qualified") is True, "runtime ownership not qualified")
    require(admission.get("tcd037_admission_readiness") is False, "admission readiness must remain false")
    require(admission.get("scientific_admission_performed") is False, "scientific admission forbidden")
    require(admission.get("production_patch_performed") is False, "production patch forbidden")
    require(admission.get("b4_opened") is False, "B4 opening forbidden")
    require(admission.get("rg05h_updated") is False, "RG05H update forbidden")
    require(admission.get("composed_tcds") == [], "TCD composition forbidden")


def validate_docs() -> None:
    for path in (DOC_PATH, CONTRACT_PATH, PROBE_PATH):
        require(path.exists(), f"missing required artifact {path.relative_to(ROOT)}")

    doc = DOC_PATH.read_text(encoding="utf-8")
    require("QUALIFIED_SOURCE_RUNTIME_OWNERSHIP_TIER_C_ACCOUNTING_SEMANTICS_PENDING" in doc, "qualification status absent from narrative")
    require("UNRESOLVED_INDEX0_AND_EMISSION_MAPPING" in doc, "accounting blocker absent from narrative")
    require("EXPECTED_PRODUCTION_DIFFERENCE = NONE" in doc, "qualification expected-difference contract absent")
    require("GOV04_TIER_C_RUNTIME_SOURCE_OWNERSHIP_AMBIGUITY" in doc, "Tier-C classification absent")
    require("ANIMO-RUNTIMEQ03" in doc, "next routing absent")


def main() -> None:
    status = load_json(STATUS_PATH)
    matrix = load_json(MATRIX_PATH)
    validate_status(status)
    validate_matrix(matrix)
    validate_docs()
    validate_scope()
    print("ANIMO-RUNTIMEQ02 validator: PASS")


if __name__ == "__main__":
    main()
