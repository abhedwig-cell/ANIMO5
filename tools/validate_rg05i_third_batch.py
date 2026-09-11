#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-RG05I third batched atomic admission integration."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "integration/animo-reg"
BASE = "3e4247928bb43f30def951fa8804560636affbef"
B3D21 = "331f6ed91d4a1c15a23ae0c1ad75d1b540f61858"
B3D24 = "0f85d7102945c7c4d77bc49885f9ecca688209e3"
B3D23 = "6c9ab83952b53566b878b533c08e3cb10074f399"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
SYNQ04 = "31d4ac628edf43501b403f0844dd472bcc12644c"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_PRE = ["TCD-017","TCD-018","TCD-024","TCD-026","TCD-015","TCD-027","TCD-041","TCD-030","TCD-023","TCD-028","TCD-038"]
EXPECTED_POST_TOP = EXPECTED_PRE + ["TCD-031"]
EXPECTED_CHILD = ["TCD-037-A1","TCD-037-A2"]
ALLOWED = {
    ".github/workflows/animo-rg05i-third-batch.yml",
    "docs/governance/ANIMO_RG05I_THIRD_BATCHED_ADMISSION_REGIE.md",
    "integration/animo-reg/ANIMO-RG05I_STATUS.json",
    "integration/animo-reg/RG05I_B3_ADMISSION_INVENTORY.json",
    "integration/animo-reg/RG05I_B3_QUEUE_DELTA.json",
    "tools/validate_rg05i_third_batch.py",
}


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("RG05I FAIL_CLOSED: " + msg)


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def show_json(ref: str, path: str) -> dict:
    return json.loads(run("git", "show", f"{ref}:{path}"))


def local(name: str) -> dict:
    return json.loads((REG / name).read_text(encoding="utf-8"))


def main() -> None:
    inv = local("RG05I_B3_ADMISSION_INVENTORY.json")
    delta = local("RG05I_B3_QUEUE_DELTA.json")
    status = local("ANIMO-RG05I_STATUS.json")
    doc = (ROOT / "docs/governance/ANIMO_RG05I_THIRD_BATCHED_ADMISSION_REGIE.md").read_text(encoding="utf-8")

    req(subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"],cwd=ROOT).returncode == 0, "RG05H is not ancestor")
    rg = show_json(BASE, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    rg_inv = show_json(BASE, "integration/animo-reg/RG05H_B3_ADMISSION_INVENTORY.json")
    req(rg["state"] == "QUALIFIED_EARLY_AGGREGATE_ROUTING_REFRESH_PLUS_ONE_POST_RG05G_ATOMIC_ADMISSION_NO_PRODUCTION", "RG05H not qualified")
    req(rg["scientific_admission_count"] == 11 and rg["historical_uncertainty_admission_count"] == 11, "RG05H count drift")
    req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05H downstream gates changed")
    req(rg_inv["admitted_tcds"] == EXPECTED_PRE and rg_inv["counts"]["scientific_admissions"] == 11, "RG05H inventory drift")

    g4 = show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
    central = g4["central_regie_integration"]
    req(central["mode"] == "AGGREGATED_ATOMIC_ADMISSION_INTEGRATION", "aggregate mode drift")
    req(central["normal_batch_min"] == 3 and central["normal_batch_max"] == 5, "normal batch cadence drift")
    g5 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(g5["work_status"]["qualified"] is True, "GOV05 not qualified")
    req(g5["assurance_change"]["scientific_gate_reduction"] is False, "GOV05 scientific gates weakened")
    g3 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 B2 closure changed")

    a1 = show_json(B3D21, "integration/animo-b3/ANIMO-B3D21_STATUS.json")
    req(a1["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and a1["target_child_atom"] == "TCD-037-A1", "B3D21 A1 authority invalid")
    req(a1["admission_effect"]["child_atom_admitted"] is True and a1["admission_effect"]["parent_tcd_admitted"] is False, "A1 child/parent admission boundary invalid")
    req(a1["admission_effect"]["historical_revision53_behavior"] == "UNKNOWN", "A1 history promoted")
    req(a1["hard_boundaries"]["production_source_modified"] is False, "A1 production scope widened")

    a2 = show_json(B3D24, "integration/animo-b3/ANIMO-B3D24_STATUS.json")
    req(a2["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and a2["target_child_atom"] == "TCD-037-A2", "B3D24 A2 authority invalid")
    req(a2["candidate_admission_effect"]["child_atom_admitted_after_exact_final_green"] is True, "A2 admission effect absent")
    req(a2["candidate_admission_effect"]["parent_tcd_admitted"] is False and a2["candidate_admission_effect"]["sibling_atoms_admitted"] == [], "A2 scope widened")
    req(a2["candidate_admission_effect"]["historical_revision53_behavior"] == "UNKNOWN", "A2 history promoted")

    a31 = show_json(B3D23, "integration/animo-b3/ANIMO-B3D23_STATUS.json")
    req(a31["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and a31["target"] == "TCD-031", "B3D23 TCD-031 authority invalid")
    req(a31["admitted"] is True and a31["qualified"] is True, "TCD-031 not admitted/qualified")
    req(a31["risk_tier"] == "C", "TCD-031 risk tier drift")
    req(a31["historical_boundary"]["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "TCD-031 history promoted")
    req(a31["production_authorized"] is False, "TCD-031 production authorization invented")

    b3i = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    req(b3i["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 authority invalid")
    req(b3i["intake"]["parent_tcd"] == "TCD-037" and b3i["intake"]["parent_admitted"] is False, "TCD-037 parent route corrupted")
    req(b3i["intake"]["canonical_register_tail_after_work"] == "TCD-042", "canonical top-level tail drift")

    syn = show_json(SYNQ04, "integration/animo-synthetic/ANIMO-SYNQ04_STATUS.json")
    req(syn["state"] == "QUALIFIED_TCD037_A3_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2", "SYNQ04 continuation evidence invalid")
    req(syn["scientific_admission"] is False and syn["tier_a_waiver_granted"] is False, "SYNQ04 incorrectly treated as admission")
    req(syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2" and syn["historical_behavior"] == "UNKNOWN", "SYNQ04 evidence strength/history drift")

    req(inv["work_unit"] == "ANIMO-RG05I", "wrong inventory owner")
    req(inv["source_aggregate"]["head"] == BASE and inv["source_aggregate"]["scientific_admissions"] == 11, "inventory source aggregate mismatch")
    req(inv["source_aggregate"]["top_level_admitted_tcds"] == EXPECTED_PRE, "inventory inherited top-level list drift")
    req(inv["batch_policy"]["new_admissions_in_this_batch"] == 3 and inv["batch_policy"]["normal_threshold_reached"] is True and inv["batch_policy"]["early_batch"] is False, "batch policy invalid")
    req([x["object"] for x in inv["new_admissions"]] == ["TCD-037-A1","TCD-037-A2","TCD-031"], "new admission objects drift")
    req([x["admission_authority"] for x in inv["new_admissions"]] == [f"ANIMO-B3D21@{B3D21}",f"ANIMO-B3D24@{B3D24}",f"ANIMO-B3D23@{B3D23}"], "admission pins drift")
    req([x["exact_final_ci_run"] for x in inv["new_admissions"]] == [34540047043,34547891772,34548360916], "exact-final CI pins drift")
    post = inv["post_state"]
    req(post["scientific_admissions"] == 14 and post["atomic_admissions"] == 14 and post["historical_uncertainty_admissions"] == 14 and post["normal_b2_route_admissions"] == 0, "post counts invalid")
    req(post["top_level_admitted_tcds"] == EXPECTED_POST_TOP, "post top-level list invalid")
    req(post["admitted_child_atoms"] == EXPECTED_CHILD and post["tcd037_parent_admitted"] is False, "child/parent aggregate boundary invalid")
    req(post["tcd037_unadmitted_children"] == ["TCD-037-A3","TCD-037-A4"], "remaining child route drift")
    req(post["b4_admissions"] == 0 and post["production_migrations"] == 0, "later gate count nonzero")
    req(inv["routing_state"]["authority"] == f"ANIMO-B3I07@{B3I07}" and inv["routing_state"]["canonical_register_modified_here"] is False, "routing/register mutation")
    for k,v in inv["project_boundary"].items():
        if k in {"B3_complete","B4_open","production_open","production_source_modified","frozen_b0_modified","canonical_tcd_register_modified","composition_admitted","historical_fidelity_claimed"}:
            req(v is False, f"inventory project boundary violated: {k}")

    req(delta["admission_counts"] == {"pre_delta_scientific_admissions":11,"new_atomic_admissions":3,"post_delta_scientific_admissions":14}, "queue delta counts invalid")
    req(delta["top_level_delta"]["new_top_level_admitted_tcds"] == ["TCD-031"], "top-level delta invalid")
    req(delta["top_level_delta"]["new_child_atom_admissions"] == EXPECTED_CHILD and delta["top_level_delta"]["tcd037_parent_admitted"] is False, "child delta invalid")
    req(delta["canonical_queue_cardinality"]["global_canonical_queue_count_recomputed"] is False, "stale global queue count fabricated")
    req(delta["non_admission_continuation_observed"]["authority"] == f"ANIMO-SYNQ04@{SYNQ04}" and delta["non_admission_continuation_observed"]["counts_as_admission"] is False, "SYNQ04 miscounted")

    req(status["source_aggregate"] == f"ANIMO-RG05H@{BASE}", "status base mismatch")
    req(status["new_atomic_admissions"] == [f"ANIMO-B3D21@{B3D21}:TCD-037-A1",f"ANIMO-B3D24@{B3D24}:TCD-037-A2",f"ANIMO-B3D23@{B3D23}:TCD-031"], "status admission pins drift")
    req(status["scientific_admission_count"] == 14 and status["historical_uncertainty_admission_count"] == 14 and status["normal_b2_admission_count"] == 0, "status count drift")
    req(status["top_level_admitted_tcd_count"] == 12 and status["admitted_child_atom_count"] == 2, "status object-kind counts invalid")
    req(status["tcd037_state"]["parent_admitted"] is False and status["tcd037_state"]["admitted_children"] == EXPECTED_CHILD, "status parent/child boundary invalid")
    req(status["b3_complete"] is False and status["b4_open"] is False and status["production_open"] is False, "status opens downstream gate")
    req(status["global_canonical_queue_count_recomputed"] is False, "status fabricates global queue count")
    for k,v in status["hard_boundaries"].items():
        req(v is False, f"status hard boundary violated: {k}")
    req(status["state"] in {"PERSISTED_VALIDATION_PENDING","QUALIFIED_THIRD_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05H_ADMISSIONS_NO_PRODUCTION"}, "unexpected lifecycle state")

    for pin in (B3D21,B3D24,B3D23,B3I07,SYNQ04,GOV05,GOV04,GOV03):
        req(pin in doc, f"document missing exact authority {pin}")
    req("14 scientific admissions" in doc and "B3 remains incomplete" in doc, "document aggregate outcome incomplete")

    changed = [x.strip() for x in run("git","diff","--name-only",BASE,"HEAD").splitlines() if x.strip()]
    req(set(changed) == ALLOWED, "scope differs from exact six-file RG05I governance package: " + repr(sorted(changed)))
    for p in changed:
        req(not p.startswith(("src/","reference/","production/")), "protected source/B0 path changed: " + p)
        req("THEORY_CODE_DISCREPANCY_REGISTER" not in p, "canonical TCD register changed")

    print("RG05I PASS: exactly three exact-final post-RG05H admissions aggregated; total scientific admissions 14; TCD-037 parent remains unadmitted; B3/B4/production remain closed.")


if __name__ == "__main__":
    main()
