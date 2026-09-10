#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-RG05H."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
B3D20 = "4f0a352bd354c971db0d972967296bf64505da5b"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"

STATUS_PATH = ROOT / "integration/animo-reg/ANIMO-RG05H_STATUS.json"
INV_PATH = ROOT / "integration/animo-reg/RG05H_B3_ADMISSION_INVENTORY.json"
ROUTE_PATH = ROOT / "integration/animo-reg/RG05H_ROUTING_AUTHORITY_REFRESH.json"
DOC_PATH = ROOT / "docs/governance/ANIMO_RG05H_ROUTING_REFRESH_AND_TCD038_ADMISSION_REGIE.md"

EXPECTED_ADMITTED = [
    "TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015", "TCD-027",
    "TCD-041", "TCD-030", "TCD-023", "TCD-028", "TCD-038"
]
EXPECTED_CHILDREN = ["TCD-037-A1", "TCD-037-A2", "TCD-037-A3", "TCD-037-A4"]
EXPECTED_ROUTES = {
    "TCD-037-A1": "ANIMO-B3A05",
    "TCD-037-A2": "ANIMO-B3A06",
    "TCD-037-A3": "ANIMO-B3A07",
    "TCD-037-A4": "ANIMO-B3A08",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(*args: str) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)
    return p.stdout


def show_json(commit: str, path: str) -> dict:
    return json.loads(run("git", "show", f"{commit}:{path}"))


def changed_paths() -> list[str]:
    return [p.strip() for p in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if p.strip()]


def main() -> None:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    inv = json.loads(INV_PATH.read_text(encoding="utf-8"))
    route = json.loads(ROUTE_PATH.read_text(encoding="utf-8"))
    doc = DOC_PATH.read_text(encoding="utf-8")

    rg05g = show_json(BASE, "integration/animo-reg/ANIMO-RG05G_STATUS.json")
    require(rg05g["work_unit"] == "ANIMO-RG05G", "wrong source aggregate")
    require(rg05g["scientific_admission_count"] == 10, "RG05G scientific admission count changed")
    require(rg05g["historical_uncertainty_admission_count"] == 10, "RG05G historical uncertainty count changed")
    require(rg05g["b3_complete"] is False and rg05g["b4_open"] is False and rg05g["production_open"] is False, "RG05G project gate changed unexpectedly")

    b3d20 = show_json(B3D20, "integration/animo-b3/ANIMO-B3D20_STATUS.json")
    require(b3d20["work_unit"] == "ANIMO-B3D20" and b3d20["target"] == "TCD-038", "wrong B3D20 target")
    require(b3d20["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "TCD-038 not finally admitted")
    require(b3d20["admitted"] is True and b3d20["qualified"] is True, "TCD-038 admission not qualified")
    require(b3d20["gov04_risk_tier"] == "C", "TCD-038 risk tier changed")
    require(b3d20["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "TCD-038 historical state promoted")
    require(b3d20["production_authorized"] is False, "TCD-038 production authorization invented")
    require(b3d20["hard_boundaries"]["central_regie_updated"] is False, "B3D20 claims its own central integration")

    b3i07 = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    require(b3i07["work_unit"] == "ANIMO-B3I07", "wrong routing authority")
    require(b3i07["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 not qualified")
    require(b3i07["work_status"]["qualified"] is True and b3i07["work_status"]["work_unit_complete"] is True, "B3I07 incomplete")
    require(b3i07["intake"]["parent_tcd"] == "TCD-037", "B3I07 parent changed")
    require(b3i07["intake"]["child_atoms"] == EXPECTED_CHILDREN, "B3I07 child map changed")
    require(b3i07["intake"]["child_risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE", "B3I07 waiver/risk state changed")
    require(b3i07["tier_a_waiver"]["granted"] is False, "B3I07 Tier-A waiver unexpectedly granted")
    require(b3i07["intake"]["child_admission_count"] == 0 and b3i07["intake"]["parent_admitted"] is False, "B3I07 contains admission")
    require(b3i07["intake"]["canonical_register_tail_after_work"] == "TCD-042", "top-level canonical tail changed")
    require(b3i07["intake"]["tcd_043_reserved"] is False, "TCD-043 unexpectedly reserved")

    gov04_text = run("git", "show", f"{GOV04}:docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    require("canonical routing" in gov04_text, "GOV04 early aggregate routing trigger unavailable")
    require("An earlier aggregate update is always allowed when it materially reduces ambiguity." in gov04_text, "GOV04 early aggregate ambiguity rule unavailable")

    require(inv["work_unit"] == "ANIMO-RG05H", "wrong inventory owner")
    require(inv["source_aggregate"]["head"] == BASE, "inventory source aggregate mismatch")
    require(inv["source_aggregate"]["scientific_admissions"] == 10, "inventory inherited admission count mismatch")
    require(inv["batch_policy"]["new_admissions_in_this_refresh"] == 1, "RG05H must integrate exactly one new admission")
    require(inv["batch_policy"]["normal_threshold_reached"] is False and inv["batch_policy"]["early_batch"] is True, "early aggregate policy mismatch")
    require(inv["batch_policy"]["early_trigger"] == "CANONICAL_ROUTING_CHANGED_AND_CURRENT_CENTRAL_SNAPSHOT_WOULD_OTHERWISE_BE_MISLEADING", "wrong early aggregate trigger")
    require(len(inv["new_admissions"]) == 1 and inv["new_admissions"][0]["tcd"] == "TCD-038", "unexpected admission set")
    require(inv["new_admissions"][0]["admission_authority"] == f"ANIMO-B3D20@{B3D20}", "wrong TCD-038 authority")
    require(inv["new_admissions"][0]["historical_behaviour"] == "UNKNOWN_WITHOUT_B2", "TCD-038 history promoted in inventory")
    require(inv["admitted_tcds"] == EXPECTED_ADMITTED, "aggregate admitted TCD sequence mismatch")
    counts = inv["counts"]
    require(counts["scientific_admissions"] == 11 and counts["atomic_admissions"] == 11, "aggregate scientific count mismatch")
    require(counts["historical_uncertainty_admissions"] == 11 and counts["normal_b2_route_admissions"] == 0, "aggregate historical route count mismatch")
    require(counts["b4_admissions"] == 0 and counts["production_migrations"] == 0, "aggregate opens later gate")
    rafter = inv["routing_authority_after_refresh"]
    require(rafter["work_unit"] == "ANIMO-B3I07" and rafter["head"] == B3I07, "inventory routing authority mismatch")
    require(rafter["canonical_children"] == EXPECTED_CHILDREN, "inventory child routing mismatch")
    require(rafter["child_risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE", "inventory grants waiver")
    require(rafter["child_admission_count"] == 0, "inventory claims child admission")
    require(rafter["canonical_top_level_tail"] == "TCD-042" and rafter["tcd_043_reserved"] is False, "inventory mutates top-level identity")
    require(inv["queue_policy"]["global_canonical_queue_count_recomputed"] is False, "unsafe queue count recomputed")
    require(inv["project_boundary"]["B3_complete"] is False and inv["project_boundary"]["B4_open"] is False and inv["project_boundary"]["production_open"] is False, "inventory opens project gate")

    require(route["work_unit"] == "ANIMO-RG05H", "wrong route refresh owner")
    require(route["source_aggregate"] == f"ANIMO-RG05G@{BASE}", "route refresh base mismatch")
    require(route["new_latest_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "route refresh authority mismatch")
    require(route["governance_trigger"]["trigger"] == "CANONICAL_ROUTING_CHANGED", "route refresh trigger mismatch")
    require(route["governance_trigger"]["early_aggregate_allowed"] is True, "early refresh not marked allowed")
    require(route["governance_trigger"]["normal_three_admission_threshold_reached"] is False, "normal batch threshold incorrectly claimed")
    t37 = route["tcd037"]
    require(t37["top_level_parent"] == "TCD-037" and t37["top_level_parent_admitted"] is False and t37["parent_atomic"] is False, "TCD-037 parent scope corrupted")
    require(t37["canonical_child_keys"] == EXPECTED_CHILDREN, "route child keys mismatch")
    require(t37["child_keys_are_top_level_tcd_rows"] is False, "child keys promoted to top-level TCDs")
    require(t37["child_risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE" and t37["tier_a_waiver_granted"] is False, "route grants Tier-A waiver")
    require(t37["child_admission_count"] == 0, "route claims child admission")
    require(t37["readiness_routes"] == EXPECTED_ROUTES, "route partition mismatch")
    require(t37["evidence_limits"]["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural active GHG case fabricated")
    require(t37["evidence_limits"]["synthetic_evidence"] == "B1_ONLY_NOT_INDEPENDENT_B2", "synthetic evidence promoted")
    require(t37["evidence_limits"]["historical_behavior"] == "UNKNOWN", "TCD-037 historical behavior promoted")
    require(route["canonical_top_level_register"]["modified"] is False, "top-level register modified")
    require(route["canonical_top_level_register"]["tail"] == "TCD-042" and route["canonical_top_level_register"]["tcd_043_reserved"] is False, "top-level identity changed")
    for key, value in route["nonclaims"].items():
        require(value is False, f"route nonclaim violated: {key}")

    require(status["work_unit"] == "ANIMO-RG05H", "wrong status owner")
    require(status["source_aggregate"] == f"ANIMO-RG05G@{BASE}", "status source aggregate mismatch")
    require(status["aggregate_trigger"] == "CANONICAL_ROUTING_CHANGED_AND_CURRENT_CENTRAL_SNAPSHOT_WOULD_OTHERWISE_BE_MISLEADING", "status trigger mismatch")
    require(status["new_atomic_admissions"] == [f"ANIMO-B3D20@{B3D20}:TCD-038"], "status admission set mismatch")
    require(status["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "status routing authority mismatch")
    require(status["routing_change"]["children"] == EXPECTED_CHILDREN, "status child map mismatch")
    require(status["routing_change"]["tier_a_waiver_granted"] is False and status["routing_change"]["child_admission_count"] == 0, "status grants child waiver/admission")
    require(status["scientific_admission_count"] == 11 and status["historical_uncertainty_admission_count"] == 11 and status["normal_b2_admission_count"] == 0, "status counts mismatch")
    require(status["b3_complete"] is False and status["b4_open"] is False and status["production_open"] is False, "status opens project gate")
    require(status["global_canonical_queue_count_recomputed"] is False, "status claims global queue recompute")
    for key, value in status["hard_boundaries"].items():
        require(value is False, f"status hard boundary violated: {key}")
    require(status["state"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_EARLY_AGGREGATE_ROUTING_REFRESH_PLUS_ONE_POST_RG05G_ATOMIC_ADMISSION_NO_PRODUCTION"}, "unexpected status lifecycle")
    require(status["decision"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_EARLY_AGGREGATE_ROUTING_REFRESH_PLUS_ONE_POST_RG05G_ATOMIC_ADMISSION_NO_PRODUCTION"}, "unexpected decision lifecycle")

    require("ANIMO-B3D20@4f0a352bd354c971db0d972967296bf64505da5b" in doc, "document missing TCD-038 authority")
    require("ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808" in doc, "document missing B3I07 authority")
    require("CANONICAL_ROUTING_CHANGED_AND_CURRENT_CENTRAL_SNAPSHOT_WOULD_OTHERWISE_BE_MISLEADING" in doc, "document missing early trigger")
    require("normal three-admission threshold" in doc.lower() or "normal three-admission" in doc.lower(), "document must disclaim normal threshold")
    require("no waiver may be assumed" in doc.lower(), "document must preserve Tier-A waiver gate")

    allowed = {
        ".github/workflows/animo-rg05h-routing-refresh.yml",
        "docs/governance/ANIMO_RG05H_ROUTING_REFRESH_AND_TCD038_ADMISSION_REGIE.md",
        "integration/animo-reg/ANIMO-RG05H_STATUS.json",
        "integration/animo-reg/RG05H_B3_ADMISSION_INVENTORY.json",
        "integration/animo-reg/RG05H_ROUTING_AUTHORITY_REFRESH.json",
        "tools/validate_rg05h_routing_refresh.py",
    }
    changed = changed_paths()
    require(changed, "no RG05H artifacts")
    for path in changed:
        require(path in allowed, f"RG05H scope widened by {path}")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")
        require(not path.startswith("src/"), "production source modified")
        require(not path.startswith("reference/"), "frozen/reference evidence modified")

    print("RG05H PASS: early central routing refresh + qualified TCD-038 atomic admission integrated; 11 admissions; B3 incomplete; no production")


if __name__ == "__main__":
    main()
