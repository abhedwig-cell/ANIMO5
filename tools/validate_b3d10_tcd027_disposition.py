#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPOSITION = ROOT / "integration/animo-b3/TCD027_B3_DISPOSITION_GOV03.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D10_STATUS.json"
DOC = ROOT / "docs/b3/TCD027_GOV03_FORMAL_DISPOSITION.md"

RG05D = "f3d6b9780631bd627f8bca0658a8e3878746e666"
B3A01 = "b2bac82512fef0fa232e759f0c68b472567c11d5"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B0_SOURCE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
B0_TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
PREP06_BLOB = "5bc14b350b1b60f870ab568d4c8a127275ca8a84"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
DECISION = "UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03"
LEGACY = "Bafop(24,Ly)=Bafop(25,Ly)+Dum"
CANDIDATE = "Bafop(24,Ly)=Bafop(24,Ly)+Dum"
CHANGED = {"transfopGP.Out", "transfopRP.Out", "transfopTP.Out"}


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D10: " + msg)


def refs_contain(refs, value):
    return any(value in ref for ref in refs)


def main():
    require(DISPOSITION.is_file(), "missing disposition")
    require(STATUS.is_file(), "missing status")
    require(DOC.is_file(), "missing disposition document")

    disposition = json.loads(DISPOSITION.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    # B3Q01-shaped unresolved disposition core.
    required_top = {
        "record_id", "record_version", "tcd_ids", "atomicity",
        "qualification_class", "admission_route", "disposition", "scope",
        "identities", "evidence", "class_specific_evidence", "gates",
        "residual_uncertainty", "composition", "admission_decision",
    }
    require(required_top.issubset(disposition), "missing B3 disposition fields")
    require(disposition["record_id"] == "B3D10-TCD027-GOV03-DISPOSITION", "record id")
    require(disposition["record_version"] == 1, "record version")
    require(disposition["tcd_ids"] == ["TCD-027"], "atomic TCD identity")
    require(disposition["atomicity"] == "ATOMIC", "atomicity")
    require(disposition["qualification_class"] == "A", "Class-A identity")
    require(disposition["admission_route"] == ROUTE, "historical uncertainty route")
    require(disposition["disposition"] == "UNRESOLVED_NOT_ADMITTED", "unresolved disposition")

    scope = disposition["scope"]
    require("slot 24" in scope["process"], "slot-24 process scope")
    require("Outbal_calc.for" in scope["code_path"], "source code path")
    require("no physical organic-P control volume is changed" in scope["control_volume"], "reporting-only control-volume boundary")

    b0 = disposition["identities"]["b0"]
    require(b0["source_sha256"] == B0_SOURCE, "B0 source identity")
    require(b0["testbank_sha256"] == B0_TESTBANK, "B0 testbank identity")
    require(b0["testcase_status"] == "FROZEN_CASE_IDENTIFIED", "B0 testcase status")
    require("LWKM_gras_1040.2021.2045" in b0["testcase_identity"], "LWKM testcase identity")

    b1 = disposition["identities"]["b1"]
    require(b1["status"] == "DIAGNOSTIC_NOT_REFERENCE", "B1 status")
    require(B3A01 in b1["evidence_identity"], "B3A01 evidence binding")
    require("not qualified historical B2" in b1["diagnostic_limitations"], "B1 non-B2 boundary")

    b2 = disposition["identities"]["b2"]
    require(b2["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 unavailable status")
    require(GOV03 in b2["acquisition_effort_ref"], "GOV03 acquisition binding")

    ev = disposition["evidence"]
    for key in ["theory", "causal", "conservation", "non_interference"]:
        require(ev[key]["status"] == "PRESENT", key + " evidence present")
    require(ev["coverage"]["branch_activation_proven"] is True, "natural branch activation")
    require("1997" in ev["coverage"]["natural_case_coverage"], "1997 coverage")
    require(ev["independent_review"]["status"] == "INCOMPLETE", "independent review incomplete")
    require(ev["independent_review"]["result"] == "NOT_REVIEWED", "independent review not performed")
    require(ev["independent_review"]["independent_from_correction_authoring"] is False, "no false independence claim")

    hu = ev["historical_uncertainty"]
    require(GOV03 in hu["acquisition_effort_ref"], "historical uncertainty GOV03 ref")
    require("UNKNOWN" in hu["uncertainty_statement"], "historical behaviour unknown")
    require("second-line reviewer" in hu["independent_cross_check_ref"], "cross-check review boundary")
    require("PENDING" in hu["second_line_review_ref"], "second-line pending")

    cls = disposition["class_specific_evidence"]
    require(cls["physical_state_trajectory_unchanged"] is True, "physical state unchanged")
    require(cls["process_flux_trajectory_unchanged"] is True, "process flux unchanged")
    require(cls["intended_ledger_or_report_only"] is True, "reporting-only class")
    require(cls["legacy_expression"] == LEGACY, "legacy expression")
    require(cls["candidate_expression"] == CANDIDATE, "candidate expression")
    require(cls["slot_semantics"] == {"24": "redis_EXP", "25": "redis_OP", "26": "redis_DOP", "27": "redis_HUP"}, "exact slot semantics")
    require(cls["analogue_accumulators"] == [
        "Bafom(24,Ly)=Bafom(24,Ly)+Adexpl(I,Ln)*Z",
        "Bafon(24,Ly)=Bafon(24,Ly)+Dum",
    ], "analogue accumulator identities")
    discr = cls["natural_discriminator"]
    require(discr["case"] == "LWKM_gras_1040.2021.2045", "natural case")
    require(discr["period"] == 1997, "natural period")
    require(discr["legacy_redis_EXP_kg_ha_P"] == -7.0644, "legacy discriminator")
    require(discr["candidate_redis_EXP_kg_ha_P"] == 0.0, "candidate discriminator")
    require(set(cls["changed_reporting_surfaces"]) == CHANGED, "three-file changed surface")

    unchanged = set(cls["unchanged_physical_and_reporting_surfaces"])
    for item in {
        "physical state trajectory", "process flux trajectory",
        "total organic-P balance", "total mass balance",
        "redis_OP", "redis_DOP", "redis_HUP",
        "ordinary non-reporting outputs",
    }:
        require(item in unchanged, "required unchanged: " + item)

    expected = ev["expected_difference"]
    require(expected["changed_states"] == [], "no changed states")
    require(expected["changed_fluxes"] == [], "no changed fluxes")
    reported_files = {item.split(":", 1)[0] for item in expected["changed_ledgers_or_reports"]}
    require(reported_files == CHANGED, "expected difference changed reports")

    gates = disposition["gates"]
    expected_gate_keys = {
        "b0_identity", "b1_evidence", "b2_route", "theory", "causal",
        "conservation", "expected_difference", "non_interference", "coverage",
        "independent_review", "residual_uncertainty", "class_specific",
        "composition_if_applicable",
    }
    require(set(gates) == expected_gate_keys, "exact gate set")
    for key in expected_gate_keys - {"independent_review"}:
        require(gates[key]["status"] == "PASS", "gate PASS: " + key)
    require(gates["independent_review"]["status"] == "FAIL", "review is blocking")
    require(gates["composition_if_applicable"]["applicability"] == "NOT_APPLICABLE", "composition not applicable")
    require(refs_contain(gates["b2_route"]["evidence_refs"], GOV03), "route evidence")
    require(refs_contain(gates["b1_evidence"]["evidence_refs"], PREP06_BLOB), "PREP06 evidence blob")

    composition = disposition["composition"]
    require(composition == {"is_composition": False, "component_record_ids": []}, "no composition")

    decision = disposition["admission_decision"]
    require(decision["admitted"] is False, "not admitted")
    require(decision["decision"] == DECISION, "bounded decision")
    require("TCD-027" in decision["decision_scope"] and "slot 24" in decision["decision_scope"], "decision scope")

    uncertainty = "\n".join(disposition["residual_uncertainty"])
    for token in ["No qualified B2", "UNKNOWN", "not historical B2", "independent second-line", "No production implementation"]:
        require(token in uncertainty, "residual uncertainty token: " + token)

    # Status must bind live authorities and remain fail-closed before or after CI closeout.
    require(status["work_unit"] == "ANIMO-B3D10", "status workunit")
    require(status["base"]["head"] == RG05D, "status RG05D base")
    require(B3A01 in status["readiness_authority"], "status B3A01")
    require(B3Q01 in status["b3_framework"], "status B3Q01")
    require(GOV03 in status["historical_route_authority"], "status GOV03")
    require(status["decision"] == DECISION, "status decision")
    require(status["route_reconciliation"]["b2_route_gate"] == "PASS", "status route open")
    require(status["route_reconciliation"]["historical_behaviour"] == "UNKNOWN", "status historical unknown")
    require(status["source_recheck"]["slot_24"] == "redis_EXP", "status slot 24")
    require(status["source_recheck"]["slot_25"] == "redis_OP", "status slot 25")
    require(status["source_recheck"]["slot_26"] == "redis_DOP", "status slot 26")
    require(status["source_recheck"]["slot_27"] == "redis_HUP", "status slot 27")
    require(status["source_recheck"]["legacy_expression"] == LEGACY, "status legacy expression")
    require(status["source_recheck"]["candidate_expression"] == CANDIDATE, "status candidate expression")
    require(status["source_recheck"]["authoring_recheck_is_independent_second_line"] is False, "status no false review")
    require(set(status["natural_discriminator"]["changed_outputs"]) == CHANGED, "status changed outputs")
    require(status["natural_discriminator"]["common_top_level_outputs_compared"] == 58, "status comparison count")
    require(status["scientific_gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "status review pending")
    require(status["admission"]["admitted"] is False, "status not admitted")
    require(status["admission"]["production_patch_authorized"] is False, "no production patch")
    require(status["admission"]["production_migration_admitted"] is False, "no production migration")
    require(status["admission"]["b4_admitted"] is False, "no B4")
    require(status["admission"]["central_regie_updated"] is False, "no central regie update")
    require(status["admission"]["composition_admitted"] is False, "no composition admission")

    ws = status["work_status"]
    require(ws["realized"] is True and ws["persisted"] is True, "persisted status")
    if ws["qualified"]:
        require(ws["tested"] is True and ws["work_unit_complete"] is True, "qualified work status")
        require(status["state"] == "QUALIFIED_TCD027_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION", "qualified state")
        validation = status["validation"]
        require(validation["tested_head"], "qualified tested head")
        require(validation["github_actions_run_id"], "qualified run id")
        require(validation["github_actions_job_id"], "qualified job id")
        require(validation["github_actions_conclusion"] == "success", "qualified CI conclusion")
        require(validation["validator_result"] == "PASS_B3D10_TCD027_GOV03_DISPOSITION", "qualified validator result")
        require(validation["scope_guard"] == "PASS_B3D10_SCOPE_GUARD", "qualified scope guard")
    else:
        require(ws["tested"] is False and ws["work_unit_complete"] is False, "pre-validation work status")
        require(status["state"] == "PENDING_VALIDATION_TCD027_FORMAL_DISPOSITION_ROUTE_OPEN_REVIEW_PENDING_NO_ADMISSION", "pre-validation state")

    # Human-readable contract must retain the same hard boundaries.
    for token in [
        "slot 24 is `redis_EXP`",
        "legacy `redis_EXP` is approximately `-7.0644 kg/ha P`",
        "candidate `redis_EXP` is `0.0 kg/ha P`",
        "only `transfopGP.Out`, `transfopRP.Out` and `transfopTP.Out` change",
        "No qualified B2 has appeared",
        "remains `UNKNOWN`",
        "does not perform or self-certify the independent review",
    ]:
        require(token in doc, "document boundary: " + token)

    print("PASS_B3D10_TCD027_GOV03_DISPOSITION")


if __name__ == "__main__":
    main()
