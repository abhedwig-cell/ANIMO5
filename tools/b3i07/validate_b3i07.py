#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3I07."""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "8f01f0cb366dfa8cc63a184d6f885100899a8cd9"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3I07_STATUS.json"
ATOM = ROOT / "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json"
CROSSWALK = ROOT / "integration/animo-b3/B3I07_RUNTIMEQ03_FINDING_CROSSWALK.csv"
DOC = ROOT / "docs/b3/POST_RUNTIMEQ03_TCD037_GHG_BALANCE_OBSERVER_ROUTING.md"

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


def changed_paths() -> list[str]:
    return [x.strip() for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x.strip()]


def runtimeq03_status() -> dict:
    text = run("git", "show", f"{RUNTIMEQ03}:integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    return json.loads(text)


def main() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    atom = json.loads(ATOM.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    with CROSSWALK.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    rq = runtimeq03_status()
    require(rq["work_unit"] == "ANIMO-RUNTIMEQ03", "wrong external evidence owner")
    require(rq["tcd"] == "TCD-037", "RUNTIMEQ03 target changed")
    require(rq["status"] == "QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED", "RUNTIMEQ03 status changed")
    require(rq["parent_atomic"] is False and rq["parent_atomization_required"] is True, "RUNTIMEQ03 atomicity changed")
    require(rq["canonical_child_atoms_allocated"] is False, "RUNTIMEQ03 unexpectedly allocated canonical children")
    require(rq["proposed_child_ids"] == EXPECTED_CHILDREN, "RUNTIMEQ03 proposed child set changed")
    require(rq["proposed_child_risk_tier"] == "TIER_A_CANDIDATE", "RUNTIMEQ03 proposed risk changed")
    require(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural GHG evidence state changed")
    require(rq["synthetic_evidence"] == "B1_ONLY_NOT_INDEPENDENT_B2", "synthetic evidence strength changed")
    require(rq["historical_intel_behavior"] == "UNKNOWN", "historical behaviour promoted")
    require(rq["scientific_admission"] is False and rq["production_patch"] is False, "RUNTIMEQ03 scope unexpectedly widened")

    require(atom["work_unit"] == "ANIMO-B3I07", "wrong atomization owner")
    require(atom["parent_tcd"] == "TCD-037", "wrong parent")
    alloc = atom["allocation_decision"]
    require(alloc["new_top_level_tcd_reserved"] is False, "new top-level TCD reserved")
    require(alloc["tcd_043_reserved"] is False, "TCD-043 reserved")
    require(alloc["child_atom_keys_are_top_level_register_rows"] is False, "child keys promoted to top-level rows")
    require(alloc["canonical_register_append_performed"] is False, "canonical register append performed")
    require(alloc["canonical_register_tail_before"] == "TCD-042" and alloc["canonical_register_tail_after"] == "TCD-042", "top-level register tail changed")
    require(alloc["parent_atomic"] is False, "compound parent declared atomic")
    require(alloc["parent_state"] == "ATOMIZED_A1_A2_A3_A4_ACCOUNTING_OBSERVER_CHILDREN_NO_ADMISSION", "unexpected parent state")

    atoms = atom["atoms"]
    require([x["atom_id"] for x in atoms] == EXPECTED_CHILDREN, "canonical child set/order mismatch")
    for child in atoms:
        cid = child["atom_id"]
        require(child["class"] == "A_ACCOUNTING_REPORTING_ONLY", f"{cid} wrong B3 class")
        require(child["risk_tier"] == "TIER_A_CANDIDATE", f"{cid} risk promoted or changed")
        require(child["risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE", f"{cid} waiver state changed")
        require(child["admitted"] is False, f"{cid} admitted in routing workunit")
        require(child["tier_a_waiver_granted"] is False, f"{cid} waiver granted in routing workunit")
        require(child["historical_behavior"] == "UNKNOWN", f"{cid} historical behaviour promoted")
        require(child["natural_activation"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", f"{cid} natural activation invented")
        require(child["next_work_unit"].startswith(EXPECTED_ROUTES[cid] + " "), f"{cid} next owner mismatch")

    gates = atom["tier_a_readiness_common_gates"]
    require(gates["source_seam_pinned"] is True, "source seam pin lost")
    require(gates["accounting_ownership_resolved_at_child_scope"] is True, "accounting ownership not preserved")
    require(gates["physical_owner_state_noninterference_direction_qualified"] is True, "state noninterference direction lost")
    require(gates["process_flux_noninterference_direction_qualified"] is True, "flux noninterference direction lost")
    require(gates["composition_present"] is False, "composition introduced")
    require(gates["structural_expected_difference_surface_pinned"] is True, "expected-difference surface lost")
    require(gates["correction_specific_identity_demonstrated"] is False, "routing workunit fabricated correction proof")
    require(gates["correction_specific_validator_passed"] is False, "routing workunit fabricated correction validator")
    require(gates["independently_qualified_synthetic_activation_if_needed"] is False, "same-context B1 promoted to independent activation evidence")
    require(gates["natural_active_ghg_case_available"] is False, "natural active GHG case fabricated")
    require(gates["tier_a_waiver_complete"] is False, "Tier-A waiver prematurely completed")

    for key, value in atom["invariants"].items():
        require(value is False or (key == "evidence_strength_promoted" and value is False), f"atomization invariant violated: {key}")

    require(status["work_unit"] == "ANIMO-B3I07", "wrong status owner")
    require(status["base"]["head"] == BASE, "wrong canonical predecessor")
    require(status["evidence"]["runtimeq03_head"] == RUNTIMEQ03, "wrong RUNTIMEQ03 pin")
    require(status["intake"]["child_atoms"] == EXPECTED_CHILDREN, "status child set mismatch")
    require(status["intake"]["child_class"] == "A_ACCOUNTING_REPORTING_ONLY", "status class mismatch")
    require(status["intake"]["child_risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE", "status risk mismatch")
    require(status["readiness_routes"] == EXPECTED_ROUTES, "readiness route partition mismatch")
    require(status["tier_a_waiver"]["granted"] is False, "status grants Tier-A waiver")
    require(status["tier_a_waiver"]["state"] == "NOT_AVAILABLE_READINESS_GATES_PENDING", "unexpected waiver state")
    require(status["intake"]["new_top_level_tcd_count"] == 0, "status allocates new TCD")
    require(status["intake"]["tcd_043_reserved"] is False, "status reserves TCD-043")
    require(status["intake"]["canonical_register_append_performed"] is False, "status appends register")
    require(status["intake"]["parent_admitted"] is False and status["intake"]["child_admission_count"] == 0, "status claims admission")
    require(status["status"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION"}, "unexpected status lifecycle")

    for key, value in status["scope_guards"].items():
        require(value is False, f"status scope guard violated: {key}")

    require(len(rows) == 4, "crosswalk must contain exactly four child rows")
    require([r["child_atom"] for r in rows] == EXPECTED_CHILDREN, "crosswalk child set mismatch")
    for row in rows:
        cid = row["child_atom"]
        require(row["parent_tcd"] == "TCD-037", "crosswalk parent mismatch")
        require(row["b3_class"] == "A_ACCOUNTING_REPORTING_ONLY", f"{cid} crosswalk class mismatch")
        require(row["gov04_risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE", f"{cid} crosswalk risk mismatch")
        require(row["natural_activation"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", f"{cid} crosswalk activation mismatch")
        require(row["historical_behavior"] == "UNKNOWN", f"{cid} crosswalk historical promotion")
        require(row["next_work_unit"] == EXPECTED_ROUTES[cid], f"{cid} crosswalk next route mismatch")
        require(row["admission"] == "false" and row["new_top_level_tcd"] == "false" and row["tcd_043_reserved"] == "false", f"{cid} crosswalk scope violation")

    require("TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE" in doc, "document must preserve no-waiver state")
    require("TCD-043 remains unreserved" in doc, "document must keep TCD-043 unreserved")
    require("same-context synthetic B1" in doc, "document must preserve synthetic-evidence limitation")
    for cid, route in EXPECTED_ROUTES.items():
        require(cid in doc and route in doc, f"document missing route for {cid}")

    allowed = (
        ".github/workflows/animo-b3i07-tcd037-routing.yml",
        "docs/b3/POST_RUNTIMEQ03_TCD037_GHG_BALANCE_OBSERVER_ROUTING.md",
        "integration/animo-b3/B3I07_RUNTIMEQ03_FINDING_CROSSWALK.csv",
        "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json",
        "integration/animo-b3/ANIMO-B3I07_STATUS.json",
        "tools/b3i07/validate_b3i07.py",
    )
    changed = changed_paths()
    require(changed, "no B3I07 artifacts")
    for path in changed:
        require(path in allowed, f"B3I07 scope widened by {path}")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical top-level register modified")
        require(not path.startswith("src/"), "production source modified")

    print("B3I07 PASS: TCD-037 atomized into four canonical Class-A child targets; Tier-A waivers pending; no admission or top-level TCD change")


if __name__ == "__main__":
    main()
