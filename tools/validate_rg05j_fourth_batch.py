#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-RG05J fourth batched B3 admission integration."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "integration/animo-reg"
BASE = "94afe7d649a8c60758a41996f0059de0acddd2fc"
B3D25 = "4da2dd067069944a5e3eeb5f532566a23402bd68"
B3D26 = "49e5ef141850296df17317da181a561def239117"
B3D27 = "cb881d0cd3e3c50455614a93b562b32354f0f1a8"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_PRE_TOP = [
    "TCD-017","TCD-018","TCD-024","TCD-026","TCD-015","TCD-027",
    "TCD-041","TCD-030","TCD-023","TCD-028","TCD-038","TCD-031",
]
EXPECTED_POST_TOP = EXPECTED_PRE_TOP + ["TCD-037"]
EXPECTED_PRE_CHILD = ["TCD-037-A1","TCD-037-A2"]
EXPECTED_POST_CHILD = ["TCD-037-A1","TCD-037-A2","TCD-037-A3","TCD-037-A4"]
ALLOWED = {
    ".github/workflows/animo-rg05j-fourth-batch.yml",
    "docs/governance/ANIMO_RG05J_FOURTH_BATCHED_ADMISSION_REGIE.md",
    "integration/animo-reg/ANIMO-RG05J_STATUS.json",
    "integration/animo-reg/RG05J_B3_ADMISSION_INVENTORY.json",
    "integration/animo-reg/RG05J_B3_QUEUE_DELTA.json",
    "tools/validate_rg05j_fourth_batch.py",
}


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("RG05J FAIL_CLOSED: " + msg)


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def show_json(ref: str, path: str) -> dict:
    return json.loads(run("git", "show", f"{ref}:{path}"))


def local(name: str) -> dict:
    return json.loads((REG / name).read_text(encoding="utf-8"))


def main() -> None:
    inv = local("RG05J_B3_ADMISSION_INVENTORY.json")
    delta = local("RG05J_B3_QUEUE_DELTA.json")
    status = local("ANIMO-RG05J_STATUS.json")
    doc = (ROOT / "docs/governance/ANIMO_RG05J_FOURTH_BATCHED_ADMISSION_REGIE.md").read_text(encoding="utf-8")

    req(subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"], cwd=ROOT).returncode == 0, "RG05I is not ancestor")

    rg = show_json(BASE, "integration/animo-reg/ANIMO-RG05I_STATUS.json")
    rg_inv = show_json(BASE, "integration/animo-reg/RG05I_B3_ADMISSION_INVENTORY.json")
    req(rg["state"] == "QUALIFIED_THIRD_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05H_ADMISSIONS_NO_PRODUCTION", "RG05I not qualified")
    req(rg["scientific_admission_count"] == 14 and rg["historical_uncertainty_admission_count"] == 14, "RG05I count drift")
    req(rg["top_level_admitted_tcd_count"] == 12 and rg["admitted_child_atom_count"] == 2, "RG05I object-kind count drift")
    req(rg["tcd037_state"]["parent_admitted"] is False and rg["tcd037_state"]["admitted_children"] == EXPECTED_PRE_CHILD, "RG05I TCD-037 boundary drift")
    req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05I downstream gates changed")
    req(rg_inv["post_state"]["top_level_admitted_tcds"] == EXPECTED_PRE_TOP, "RG05I top-level inventory drift")
    req(rg_inv["post_state"]["admitted_child_atoms"] == EXPECTED_PRE_CHILD, "RG05I child inventory drift")

    g4 = show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
    central = g4["central_regie_integration"]
    req(central["mode"] == "AGGREGATED_ATOMIC_ADMISSION_INTEGRATION", "central-regie mode drift")
    req(central["normal_batch_min"] == 3 and central["normal_batch_max"] == 5, "normal batch cadence drift")
    g5 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(g5["work_status"]["qualified"] is True, "GOV05 not qualified")
    req(g5["assurance_change"]["scientific_gate_reduction"] is False, "GOV05 scientific gates weakened")
    g3 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")

    a3 = show_json(B3D25, "integration/animo-b3/ANIMO-B3D25_STATUS.json")
    req(a3["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and a3["target_child_atom"] == "TCD-037-A3", "B3D25 A3 authority invalid")
    req(a3["candidate_admission_effect"]["child_atom_admitted_after_exact_final_green"] is True, "A3 admission effect absent")
    req(a3["candidate_admission_effect"]["parent_tcd_admitted"] is False and a3["candidate_admission_effect"]["a4_admitted"] is False, "A3 scope widened")
    req(a3["candidate_admission_effect"]["historical_revision53_behavior"] == "UNKNOWN", "A3 history promoted")
    req(a3["candidate_admission_effect"]["production_authorized"] is False, "A3 production authorization invented")

    a4 = show_json(B3D26, "integration/animo-b3/ANIMO-B3D26_STATUS.json")
    req(a4["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and a4["target_child_atom"] == "TCD-037-A4", "B3D26 A4 authority invalid")
    req(a4["candidate_admission_effect"]["child_atom_admitted_after_exact_final_green"] is True, "A4 admission effect absent")
    req(a4["candidate_admission_effect"]["all_four_child_atoms_admitted_after_exact_final_green"] is True, "A4 child-completion state absent")
    req(a4["candidate_admission_effect"]["parent_tcd_admitted"] is False, "A4 automatically admitted parent")
    req(a4["parent_routing"]["determination"] == "SEPARATE_PARENT_TCD037_COMPOSITION_DISPOSITION_ADMISSION_WORKUNIT_REQUIRED", "A4 parent route drift")
    req(a4["candidate_admission_effect"]["production_authorized"] is False, "A4 production authorization invented")

    parent = show_json(B3D27, "integration/animo-b3/ANIMO-B3D27_STATUS.json")
    req(parent["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and parent["target_parent_tcd"] == "TCD-037", "B3D27 parent authority invalid")
    req(parent["parent_tcd_admitted"] is True, "B3D27 parent not admitted")
    req(parent["gov04_risk_tier"] == "TIER_D" and parent["risk_rule"] == "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS", "parent risk route drift")
    req(parent["governance"]["review_mode"] == "SINGLE_AGENT_ADVERSARIAL_REVIEW", "parent GOV05 review mode drift")
    req(parent["governance"]["review_assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "parent review assurance drift")
    req(parent["governance"]["genuinely_independent_review_claimed"] is False, "false independence claim")
    req(parent["admission_predicates"]["all_four_children_exact_final_green"] == "PASS", "parent child predicate failed")
    req(parent["admission_predicates"]["overlap_gap_double_count"] == "PASS", "parent overlap/gap predicate failed")
    req(parent["admission_predicates"]["tier_d_parent_integration"] == "PASS", "parent Tier-D integration predicate failed")
    req(parent["parent_scientific_claim"]["new_physical_process"] is False and parent["parent_scientific_claim"]["new_persistent_state"] is False, "parent scientific scope widened")
    req(parent["parent_scientific_claim"]["complete_ghg_carbon_ledger"] is False and parent["parent_scientific_claim"]["complete_n2o_mass_ledger"] is False, "parent conservation theorem invented")
    req(parent["residual_uncertainty"]["synthetic_parent_oracle_is_b2"] is False, "parent oracle promoted to B2")
    req(parent["residual_uncertainty"]["production_implementation"] == "NOT_AUTHORIZED", "parent production authorization invented")
    req(parent["aggregate_policy"]["next_aggregate_handoff"] == "ANIMO-RG05J_SEPARATE_WORKUNIT_AFTER_EXACT_FINAL_GREEN", "B3D27 aggregate handoff drift")

    b3i = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    req(b3i["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 authority invalid")
    req(b3i["intake"]["parent_tcd"] == "TCD-037", "B3I07 parent identity drift")
    req(b3i["intake"]["canonical_register_tail_after_work"] == "TCD-042", "canonical top-level tail drift")

    req(inv["work_unit"] == "ANIMO-RG05J", "wrong inventory owner")
    req(inv["source_aggregate"]["head"] == BASE and inv["source_aggregate"]["scientific_admissions"] == 14, "inventory source aggregate mismatch")
    req(inv["source_aggregate"]["top_level_admitted_tcds"] == EXPECTED_PRE_TOP, "inventory inherited top-level list drift")
    req(inv["source_aggregate"]["admitted_child_atoms"] == EXPECTED_PRE_CHILD and inv["source_aggregate"]["tcd037_parent_admitted"] is False, "inventory inherited TCD-037 state drift")
    req(inv["batch_policy"]["new_b3_admissions_in_this_batch"] == 3, "batch admission count invalid")
    req(inv["batch_policy"]["new_atomic_child_admissions"] == 2 and inv["batch_policy"]["new_composed_parent_admissions"] == 1, "batch object-kind counts invalid")
    req(inv["batch_policy"]["normal_threshold_reached"] is True and inv["batch_policy"]["early_batch"] is False, "batch trigger invalid")
    req([x["object"] for x in inv["new_admissions"]] == ["TCD-037-A3","TCD-037-A4","TCD-037"], "new admission objects drift")
    req([x["admission_authority"] for x in inv["new_admissions"]] == [f"ANIMO-B3D25@{B3D25}",f"ANIMO-B3D26@{B3D26}",f"ANIMO-B3D27@{B3D27}"], "admission pins drift")
    req([x["exact_final_ci_run"] for x in inv["new_admissions"]] == [34549748497,34554010568,34560197591], "exact-final CI pins drift")
    req(inv["new_admissions"][2]["object_kind"] == "COMPOSED_TOP_LEVEL_TCD_PARENT" and inv["new_admissions"][2]["automatic_parent_admission_by_child_completion"] is False, "parent misclassified or automatic")
    req(inv["new_admissions"][2]["review_assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "parent review assurance lost")
    post = inv["post_state"]
    req(post["scientific_admissions"] == 17 and post["historical_uncertainty_admissions"] == 17 and post["normal_b2_route_admissions"] == 0, "post counts invalid")
    req(post["top_level_admitted_tcds"] == EXPECTED_POST_TOP, "post top-level list invalid")
    req(post["admitted_child_atoms"] == EXPECTED_POST_CHILD, "post child list invalid")
    req(post["tcd037_parent_admitted"] is True and post["tcd037_unadmitted_children"] == [], "post TCD-037 completion invalid")
    req(post["tcd037_parent_authority"] == f"ANIMO-B3D27@{B3D27}", "parent authority pin invalid")
    req(post["b4_admissions"] == 0 and post["production_migrations"] == 0, "later gate count nonzero")
    req(inv["routing_state"]["authority"] == f"ANIMO-B3I07@{B3I07}", "routing authority drift")
    req(inv["routing_state"]["canonical_register_modified_here"] is False and inv["routing_state"]["routing_register_modified_here"] is False, "routing/register mutation")
    req(inv["routing_state"]["tcd037_parent_composition_admitted_by_separate_authority"] is True, "separate parent authority not preserved")
    for k, v in inv["project_boundary"].items():
        if k in {"B3_complete","B4_open","production_open","production_source_modified","frozen_b0_modified","canonical_tcd_register_modified","routing_register_modified","historical_fidelity_claimed","parent_scientific_re_admission_performed"}:
            req(v is False, f"inventory project boundary violated: {k}")

    req(delta["admission_counts"] == {
        "pre_delta_scientific_admissions":14,
        "new_b3_admissions":3,
        "new_atomic_child_admissions":2,
        "new_composed_parent_admissions":1,
        "post_delta_scientific_admissions":17,
    }, "queue delta counts invalid")
    req(delta["new_objects"] == ["TCD-037-A3","TCD-037-A4","TCD-037"], "queue delta object order drift")
    req(delta["top_level_delta"]["new_top_level_admitted_tcds"] == ["TCD-037"], "top-level delta invalid")
    req(delta["top_level_delta"]["new_child_atom_admissions"] == ["TCD-037-A3","TCD-037-A4"], "child delta invalid")
    req(delta["top_level_delta"]["tcd037_parent_admitted"] is True and delta["top_level_delta"]["all_tcd037_children_admitted"] is True, "TCD-037 aggregate completion invalid")
    req(delta["top_level_delta"]["parent_admission_was_automatic_from_child_completion"] is False, "parent admission made automatic")
    req(delta["tcd037_resolution"]["parent_review_independence_claimed"] is False, "parent review independence invented")
    req(delta["canonical_queue_cardinality"]["global_canonical_queue_count_recomputed"] is False, "stale global queue count fabricated")
    req(all(v is False for v in delta["project_gate_delta"].values()), "project gate opened by aggregate")

    req(status["source_aggregate"] == f"ANIMO-RG05I@{BASE}", "status base mismatch")
    req(status["source_aggregate_exact_final_ci"] == "34549097225:success", "status base CI mismatch")
    req(status["new_b3_admissions"] == [f"ANIMO-B3D25@{B3D25}:TCD-037-A3",f"ANIMO-B3D26@{B3D26}:TCD-037-A4",f"ANIMO-B3D27@{B3D27}:TCD-037:PARENT_COMPOSITION"], "status admission pins drift")
    req(status["scientific_admission_count"] == 17 and status["historical_uncertainty_admission_count"] == 17 and status["normal_b2_admission_count"] == 0, "status count drift")
    req(status["top_level_admitted_tcd_count"] == 13 and status["admitted_child_atom_count"] == 4, "status object-kind counts invalid")
    req(status["tcd037_state"]["parent_admitted"] is True and status["tcd037_state"]["admitted_children"] == EXPECTED_POST_CHILD, "status TCD-037 state invalid")
    req(status["tcd037_state"]["automatic_parent_admission_by_child_completion"] is False, "status makes parent automatic")
    req(status["tcd037_state"]["parent_review_assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "status overstates review assurance")
    req(status["b3_complete"] is False and status["b4_open"] is False and status["production_open"] is False, "status opens downstream gate")
    req(status["global_canonical_queue_count_recomputed"] is False, "status fabricates global queue count")
    for k, v in status["hard_boundaries"].items():
        req(v is False, f"status hard boundary violated: {k}")
    req(status["state"] in {"PERSISTED_VALIDATION_PENDING","QUALIFIED_FOURTH_BATCHED_B3_ADMISSION_INTEGRATION_TWO_CHILD_ATOMS_ONE_PARENT_COMPOSITION_NO_PRODUCTION"}, "unexpected lifecycle state")
    if status["state"] == "PERSISTED_VALIDATION_PENDING":
        req(status["validation"]["machine_validated"] is False and status["work_status"]["qualified"] is False, "pending state falsely qualified")
    else:
        req(status["validation"]["machine_validated"] is True, "qualified state not machine validated")
        req(status["validation"]["conclusion"] == "success" and status["validation"]["validator"] == "PASS" and status["validation"]["scope_guard"] == "PASS", "qualified validation fields invalid")
        req(status["validation"]["run_id"] is not None and status["validation"]["job_id"] is not None and status["validation"]["tested_head"], "qualified validation provenance incomplete")
        req(status["work_status"]["tested"] is True and status["work_status"]["qualified"] is True and status["work_status"]["work_unit_complete"] is True, "qualified work status incomplete")

    for pin in (BASE,B3D25,B3D26,B3D27,B3I07,GOV05,GOV04,GOV03):
        req(pin in doc, f"document missing exact authority {pin}")
    req("17 scientific admissions" in doc and "B3 remains incomplete" in doc, "document aggregate outcome incomplete")
    req("PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" in doc, "document overstates parent review assurance")

    changed = [x.strip() for x in run("git","diff","--name-only",BASE,"HEAD").splitlines() if x.strip()]
    req(set(changed) == ALLOWED, "scope differs from exact six-file RG05J governance package: " + repr(sorted(changed)))
    for p in changed:
        req(not p.startswith(("src/","reference/","production/")), "protected source/B0 path changed: " + p)
        req("THEORY_CODE_DISCREPANCY_REGISTER" not in p, "canonical TCD register changed")
        req("ANIMO-B3I07" not in p, "routing authority changed")

    print("RG05J PASS: two exact-final child admissions plus one separately qualified parent composition admission aggregated; total scientific admissions 17; TCD-037 parent and A1-A4 integrated; B3/B4/production remain closed.")


if __name__ == "__main__":
    main()
