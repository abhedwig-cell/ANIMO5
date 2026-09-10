#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3D12 TCD-015 B3 admission closeout.

This validator reconciles the persisted admission record against exact pinned
readiness, disposition, governance and independent-review objects. A validator
PASS is necessary for B3D12 qualification but does not authorize production
source changes, B4 or composition.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMISSION = ROOT / "integration/animo-b3/TCD015_B3_ADMISSION_CLOSEOUT.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D12_STATUS.json"
DOC = ROOT / "docs/b3/TCD015_B3_ADMISSION_CLOSEOUT.md"

EXPECTED_BASE = "cf3e2746351c5c75d236e1b63fb0623daa8e7372"
EXPECTED_SCIENTIFIC_DISPOSITION = "2a5abc00a779baaa3fb3fa28b3c051231c286132"
EXPECTED_READINESS = "b982242949aecab32b9067cf7910ad75abfc2b19"
EXPECTED_REVIEW = "a6880282e9ed743f97a3435b55e4fb54f7d55a44"
EXPECTED_GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
EXPECTED_RG05D = "f3d6b9780631bd627f8bca0658a8e3878746e666"
EXPECTED_REVIEW_RUN = 34455556365
EXPECTED_ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
EXPECTED_DECISION = "ADMIT_TCD015_ATOMIC_CLASS_B_SCIENTIFIC_NITRATE_TRANSPORT_ALGEBRA_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
EXPECTED_REVIEW_DISPOSITION = "PASS_TCD015_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION"
EXPECTED_SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_TRANSSUB_SHA = "c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552"


def fail(msg: str) -> None:
    raise SystemExit("FAIL_B3D12: " + msg)


def require(condition: bool, msg: str) -> None:
    if not condition:
        fail(msg)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(ref: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(proc.returncode == 0, f"cannot read pinned object {ref}:{path}: {proc.stderr.strip()}")
    return proc.stdout


def git_json(ref: str, path: str):
    return json.loads(git_text(ref, path))


def main() -> None:
    admission = load(ADMISSION)
    status = load(STATUS)
    doc = DOC.read_text(encoding="utf-8")

    d09 = git_json(EXPECTED_BASE, "integration/animo-b3/TCD015_B3_DISPOSITION_GOV03.json")
    readiness = git_json(EXPECTED_READINESS, "integration/animo-b3/TCD015_CLASS_B_READINESS.json")
    review = git_json(EXPECTED_REVIEW, "integration/animo-b3/TCD015_INDEPENDENT_REVIEW_RESULT.json")
    gov03 = git_json(EXPECTED_GOV03, "integration/animo-governance/GOV03_ACQUISITION_EVIDENCE.json")
    b3_framework = git_text(EXPECTED_B3Q01, "docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md")
    b3_classes = git_text(EXPECTED_B3Q01, "docs/governance/B3_QUALIFICATION_CLASSES.md")
    synq = git_text(EXPECTED_SYNQ01, "tools/reference/synthetic_oracles.py")

    require(admission["record_id"] == "B3D12-TCD015-GOV03-ADMISSION", "record id")
    require(admission["tcd_ids"] == ["TCD-015"], "atomic TCD identity")
    require(admission["atomicity"] == "ATOMIC", "atomicity")
    require(admission["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "Class-B identity")
    require(admission["admission_route"] == EXPECTED_ROUTE, "admission route")
    require(admission["disposition"] == EXPECTED_DISPOSITION, "admission disposition")

    auth = admission["authorities"]
    require(auth["B3D09_scientific_disposition"] == EXPECTED_SCIENTIFIC_DISPOSITION, "B3D09 scientific authority")
    require(auth["B3D09_administrative_closeout"] == EXPECTED_BASE, "B3D09 administrative authority")
    require(auth["B3B01_readiness"] == EXPECTED_READINESS, "B3B01 readiness authority")
    require(auth["B3B01R_independent_review"] == EXPECTED_REVIEW, "B3B01R review authority")
    require(auth["GOV03"] == EXPECTED_GOV03, "GOV03 authority")
    require(auth["B3Q01"] == EXPECTED_B3Q01, "B3Q01 authority")
    require(auth["SYNQ01"] == EXPECTED_SYNQ01, "SYNQ01 authority")
    require(auth["RG05D_at_admission_start"] == EXPECTED_RG05D, "RG05D authority")

    scope = admission["scope"]
    require("NITRATE" in scope["claim"], "nitrate-only claim")
    require(scope["candidate_minus_legacy"] == "-Avc*Hv", "candidate-minus-legacy identity")
    require("Hv1-Hv" in scope["candidate_atomic_correction"], "candidate expression")
    require("-Avc*Hv1" in scope["legacy_expression"], "legacy expression")

    b0 = admission["identities"]["b0"]
    require(b0["source_sha256"] == EXPECTED_SOURCE_SHA, "source archive identity")
    require(b0["testbank_sha256"] == EXPECTED_TESTBANK_SHA, "testbank identity")
    require(b0["source_member"] == "ANIMO_4.1.5.53/Transsub.for", "Transsub member")
    require(b0["source_member_sha256"] == EXPECTED_TRANSSUB_SHA, "Transsub member hash")
    require(admission["identities"]["b1"]["status"] == "DIAGNOSTIC_NOT_REFERENCE", "B1 evidence semantics")
    require(admission["identities"]["b2"]["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 status")
    require(EXPECTED_GOV03 in admission["identities"]["b2"]["acquisition_effort_ref"], "B2 acquisition authority")

    # Reconcile against the exact formal disposition. The only blocking D09 gate
    # was the then-pending independent review; all scientific/route gates were
    # already closed and the scope was nitrate-only, GHG0-only.
    require(d09["tcd_ids"] == ["TCD-015"], "D09 target")
    require(d09["atomicity"] == "ATOMIC", "D09 atomicity")
    require(d09["admission_route"] == EXPECTED_ROUTE, "D09 route")
    require(d09["scope"]["species_scope"] == "NITRATE_ONLY", "D09 nitrate scope")
    require(d09["scope"]["feature_scope"] == "CORE_NITRATE_TRANSPORT_GREENHOUSEGASOPTION_0", "D09 GHG0 scope")
    require(d09["scope"]["candidate_delta_reko"] == "-Avc*Hv", "D09 algebraic delta")
    require(d09["historical_route"]["b2_route_gate"] == "PASS", "D09 historical route gate")
    require(d09["historical_route"]["historical_behaviour"] == "UNKNOWN", "D09 historical behavior")
    require(d09["historical_route"]["historical_fidelity_claimed"] is False, "D09 no historical fidelity")
    require(d09["gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "D09 original review blocker retained")
    for gate_name, gate_value in d09["gates"].items():
        if gate_name == "independent_review":
            continue
        require(str(gate_value).startswith("PASS"), f"D09 gate not closed: {gate_name}")

    # Reconcile the exact independent review that resolves the D09 blocker.
    require(review["work_unit"] == "ANIMO-B3B01R", "review workunit")
    require(review["target_tcd"] == "TCD-015", "review target")
    require(review["review_status"] == "COMPLETED_PASS", "review completed PASS")
    require(review["semantic_result"] == "PASS", "review semantic PASS")
    require(review["disposition"] == EXPECTED_REVIEW_DISPOSITION, "review disposition")
    require(review["overall_technical_second_line_result"] == "PASS", "review overall result")
    require(all(v == "PASS" for v in review["gates"].values()), "all independent review gates PASS")
    require(review["B3_admitted"] is False, "review itself did not admit")
    require(review["production_patch"] is False, "review itself did not patch production")
    require(review["feature_and_policy_boundaries"]["nitrate_only"] is True, "review nitrate-only")
    require(review["feature_and_policy_boundaries"]["generic_Transsub_change_authorized"] is False, "review no generic Transsub")
    require(review["feature_and_policy_boundaries"]["GreenHouseGasOption_0_only"] is True, "review GHG0-only")
    require(review["historical_route"]["historical_behavior"] == "UNKNOWN", "review historical unknown")
    require(review["historical_route"]["historical_fidelity_claimed"] is False, "review no historical fidelity")

    # Readiness evidence remains causal/diagnostic and is not promoted to B2.
    require(readiness["work_unit"] == "ANIMO-B3B01", "readiness workunit")
    require(readiness["target_tcd"] == "TCD-015", "readiness target")
    require(readiness["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "readiness class")

    # GOV03 and B3Q01 route rules are pinned rather than paraphrased from status.
    require(gov03["proposed_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 closure")
    require(gov03["evidence_strength_limits"]["historical_B2_artifact_obtained"] is False, "no historical B2 artifact")
    require(gov03["evidence_strength_limits"]["historical_behaviour_proven"] is False, "historical behaviour not proven")
    require(EXPECTED_ROUTE in b3_framework, "B3Q01 historical-uncertainty route")
    require("A record is admitted only when all mandatory gates for its class and route are explicitly `PASS`" in b3_framework, "B3Q01 fail-closed admission rule")
    require("Class B: Local algebra, index or species correction" in b3_classes, "B3Q01 Class-B contract")
    require("duplicated algebraic term" in b3_classes, "Class-B duplicated-term category")
    require("return self.avc * self.hv * self.st * self.ld" in synq, "SYNQ-O001 duplicated storage identity")

    evidence = admission["evidence"]
    require(evidence["exact_identity_and_causality"]["status"] == "PRESENT", "causal evidence present")
    require(evidence["conservation"]["status"] == "PRESENT", "conservation evidence present")
    require("Avc*Hv*St*Ld" in evidence["conservation"]["summary"], "local conservation identity")

    coverage = evidence["coverage"]
    require(coverage["natural_positive_activation"] is True, "natural positive activation")
    require(coverage["natural_target_entries"] == 508, "508 target entries")
    require(coverage["natural_non_nitrate_entries"] == 0, "no natural non-nitrate target entries")
    require(coverage["natural_Iflsol_1_entries"] == 486, "Iflsol=1 coverage")
    require(coverage["natural_Iflsol_3_entries"] == 22, "Iflsol=3 coverage")
    require(coverage["Iflsol_4_isolated_harness"] == "PASS_REACHABLE_NONZERO_DELTA", "Iflsol=4 coverage")
    require(coverage["hidden_reachable_target_mode_found"] is False, "no hidden reachable target mode")

    ni = evidence["non_interference"]
    require(ni["status"] == "PRESENT", "non-interference evidence present")
    for token in ("550 files", "430 raw equal", "99 equal", "21 scientifically different", "no numerical acceptance tolerance"):
        require(token in ni["summary"], f"non-interference summary token: {token}")

    ir = evidence["independent_review"]
    require(ir["status"] == "COMPLETE", "independent review complete")
    require(ir["result"] == "PASS", "independent review PASS")
    require(ir["disposition"] == EXPECTED_REVIEW_DISPOSITION, "independent review disposition in admission")
    require(ir["workflow_run"] == EXPECTED_REVIEW_RUN, "independent review workflow run")
    require(ir["independent_from_correction_authoring"] is True, "separate review context")
    require(EXPECTED_REVIEW in ir["reviewer_or_workunit"], "review head pinned in admission")
    require("no organizational, institutional or human independence claimed" in ir["scope"], "independence boundary")

    hist = evidence["historical_uncertainty"]
    require(hist["historical_behaviour"] == "UNKNOWN", "historical behaviour remains unknown")
    require(hist["historical_prevalence"] == "UNKNOWN", "historical prevalence remains unknown")
    require(hist["historical_fidelity_claimed"] is False, "no historical fidelity")
    require("GHG-enabled" in hist["scope_limitations"], "GHG uncertainty retained")
    require("macropore" in hist["scope_limitations"], "macropore uncertainty retained")

    gates = admission["gates"]
    expected_gates = {
        "b0_identity", "b1_evidence", "b2_route", "theory_or_exact_identity",
        "causal", "conservation", "expected_difference", "non_interference",
        "coverage", "independent_review", "residual_uncertainty", "class_specific",
        "composition_if_applicable",
    }
    require(set(gates) == expected_gates, "complete admission gate set")
    require(all(v["status"] == "PASS" for v in gates.values()), "all admission gates PASS")
    require(gates["composition_if_applicable"]["applicability"] == "NOT_APPLICABLE", "composition not applicable")

    class_specific = admission["class_specific_evidence"]
    require(class_specific["exact_causal_codepath"] == "PASS", "Class-B codepath")
    require(class_specific["candidate_minus_legacy_identity"] == "PASS_EXACT_MINUS_AVC_HV", "Class-B delta identity")
    require(class_specific["conservation"] == "PASS_EXACT_NO_TOLERANCE", "Class-B conservation")
    require(class_specific["generic_Transsub_change_authorized"] is False, "no generic Transsub authorization")
    require(class_specific["GreenHouseGasOption_0_only"] is True, "GHG0-only class boundary")

    require(admission["composition"]["is_composition"] is False, "no composition")
    require(admission["composition"]["component_record_ids"] == [], "no composition components")

    decision = admission["admission_decision"]
    require(decision["admitted"] is True, "admission decision true")
    require(decision["decision"] == EXPECTED_DECISION, "bounded admission decision")
    require("TCD-015 atomic nitrate-only" in decision["decision_scope"], "decision scope")
    for key in (
        "historical_fidelity_claimed", "production_patch_authorized",
        "production_migration_admitted", "B4_admitted", "composition_admitted",
    ):
        require(decision[key] is False, f"admission hard boundary: {key}")

    require(status["work_unit"] == "ANIMO-B3D12", "status workunit")
    require(status["base"]["head"] == EXPECTED_BASE, "status base head")
    require(status["base"]["scientific_disposition_head"] == EXPECTED_SCIENTIFIC_DISPOSITION, "status scientific disposition")
    require(status["review_authority"]["head"] == EXPECTED_REVIEW, "status review head")
    require(status["review_authority"]["semantic_result"] == "PASS", "status review PASS")
    require(status["review_authority"]["workflow_run"] == EXPECTED_REVIEW_RUN, "status review run")
    require(status["admission_route"] == EXPECTED_ROUTE, "status route")
    require(status["intended_final_disposition"] == EXPECTED_DISPOSITION, "status disposition")
    require(status["intended_admission_decision"] == EXPECTED_DECISION, "status intended decision")
    require(all(v is False for v in status["hard_boundaries"].values()), "status hard boundaries false")

    require(EXPECTED_DECISION in doc, "doc decision")
    require("Historical revision-53 behaviour and prevalence remain **UNKNOWN**" in doc, "doc historical uncertainty")
    require("does **not** authorize" in doc, "doc hard boundary")
    require("shared generic routine" in doc, "doc generic Transsub boundary")
    require("GreenHouseGasOption=0" in doc, "doc GHG0 boundary")

    if status["work_status"]["qualified"]:
        require(status["state"] == "QUALIFIED_TCD015_ATOMIC_B3_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_NO_PRODUCTION_MIGRATION", "qualified state")
        require(status["decision"] == EXPECTED_DECISION, "qualified decision")
        require(status["admission"]["scientific_b3_admission_qualified"] is True, "qualified admission flag")
        require(status["work_status"]["tested"] is True, "qualified status tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified status complete")
    else:
        require(status["state"] == "IN_PROGRESS_PERSISTED_TCD015_ADMISSION_VALIDATION_PENDING", "pending state")
        require(status["decision"] == "PENDING_FAIL_CLOSED_VALIDATION", "pending decision")
        require(status["admission"]["scientific_b3_admission_qualified"] is False, "pending admission flag")

    print("PASS_B3D12_TCD015_ADMISSION")


if __name__ == "__main__":
    main()
