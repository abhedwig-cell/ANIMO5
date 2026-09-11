#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3D27 TCD-037 parent composition admission."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "49e5ef141850296df17317da181a561def239117"
C1_HEAD = "17387b7282a6f5b40fec290bd4c28cc6cef8f767"
C2_HEAD = "f2d209754b0f96ac20b9642de91bcfbda1116cab"
BRANCH = "work/animo-b3d27-tcd037-parent-composition-gov05-tier-d-admission"


def load_json(path: str):
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head")
    args = parser.parse_args()

    status = load_json("integration/animo-b3/ANIMO-B3D27_STATUS.json")
    evidence = load_json("integration/animo-b3/TCD037_PARENT_COMPOSITION_EVIDENCE_MATRIX.json")
    coverage = load_json("integration/animo-b3/TCD037_CHILD_TO_PARENT_COVERAGE_MATRIX.json")
    overlap = load_json("integration/animo-b3/TCD037_PARENT_OVERLAP_GAP_AUDIT.json")
    oracle_evidence = load_json("integration/animo-b3/TCD037_PARENT_COMPOSITION_ORACLE_EVIDENCE.json")
    review = load_json("integration/animo-b3/TCD037_PARENT_GOV05_REVIEW.json")
    integration = load_json("integration/animo-b3/B3D27_PARENT_INTEGRATION_QUALIFICATION.json")
    checkpoint = load_json("integration/animo-b3/B3D27_PARENT_COMPOSITION_CHECKPOINT.json")

    require(status["work_unit"] == "ANIMO-B3D27", "wrong work unit")
    require(status["target_parent_tcd"] == "TCD-037", "wrong parent target")
    require(status["branch"] == BRANCH, "wrong branch identity")
    require(status["base_head"] == BASE_HEAD, "wrong base head")
    require(status["composition_authoring_head"] == C1_HEAD, "wrong C1 authoring head")
    require(status["adversarial_review_head"] == C2_HEAD, "wrong C2 review head")

    require(evidence["base_head"] == BASE_HEAD, "evidence base mismatch")
    require(evidence["risk"]["gov04_tier"] == "TIER_D", "parent must be Tier D")
    require(evidence["risk"]["rule"] == "STRICTEST_APPLICABLE_RISK_TRIGGER_WINS", "risk rule missing")
    require(evidence["verify_and_reuse"]["superseding_contradiction_found"] is False, "contradictory evidence present")
    require(evidence["verify_and_reuse"]["evidence_strength_promoted"] is False, "evidence strength promoted")
    require(evidence["parent_claim"]["formation_equals_emission_claim"] is False, "formation/emission collapse")
    require(evidence["parent_claim"]["climate_co2_equivalent_claim"] is False, "false climate CO2e claim")
    require(evidence["signed_exchange"]["sign_preserved"] is True, "signed exchange not preserved")
    require(evidence["units"]["cross_element_sum_allowed"] is False, "cross-element sum incorrectly allowed")
    require(evidence["dependencies"]["new_child_atom_required"] is False, "unexpected new child requirement")

    expected_children = {
        "TCD-037-A1": ("ANIMO-B3D21@331f6ed91d4a1c15a23ae0c1ad75d1b540f61858", 34540047043),
        "TCD-037-A2": ("ANIMO-B3D24@0f85d7102945c7c4d77bc49885f9ecca688209e3", 34547891772),
        "TCD-037-A3": ("ANIMO-B3D25@4da2dd067069944a5e3eeb5f532566a23402bd68", 34549748497),
        "TCD-037-A4": ("ANIMO-B3D26@49e5ef141850296df17317da181a561def239117", 34554010568),
    }
    for atom, (authority, run_id) in expected_children.items():
        child = evidence["child_admissions"][atom]
        require(child["authority"] == authority, f"{atom} authority mismatch")
        require(child["exact_final_ci_run"] == run_id, f"{atom} CI pin mismatch")
        require(child["ci_conclusion"] == "success", f"{atom} CI not successful")

    require(len(coverage["children"]) == 4, "coverage matrix must have four children")
    require(all(row["coverage"] == "COMPLETE" for row in coverage["children"]), "incomplete child coverage")
    require(coverage["coverage_checks"]["new_child_required"] is False, "coverage requests a new child")
    require(overlap["result"] == "PASS_NO_PARENT_COMPOSITION_GAP_OR_DOUBLE_COUNT_WITHIN_BOUNDED_CLAIM", "overlap/gap audit failed")
    require(overlap["new_child_atom_required"] is False, "overlap audit requests a new child")

    require(oracle_evidence["oracle_blob_sha"] == "9834f7b229eaea88068310ae3f3c4d61418844e7", "oracle identity mismatch")
    require(oracle_evidence["result"] == "PASS_BOUNDED_PARENT_COMPOSITION_PROOF", "parent oracle evidence not pass")
    require(oracle_evidence["b2_strength"] is False, "oracle incorrectly promoted to B2")

    require(checkpoint["checkpoint"] == "C1_PARENT_COMPOSITION_AUTHORING_RESTARTED_AFTER_PRE_REVIEW_EVIDENCE_GAP", "wrong C1 checkpoint")
    require(checkpoint["superseded_authoring_head"] == "74711b4ce5ada0e8748014dff0f7c131bdde96ad", "missing pre-review remediation provenance")
    require(checkpoint["same_agent_review_may_be_called_independent"] is False, "same-agent review mislabeled")

    require(review["reviewed_authoring_head"] == C1_HEAD, "review did not target exact C1")
    require(review["assurance_mode"] == "SINGLE_AGENT_ADVERSARIAL_REVIEW", "wrong review mode")
    require(review["assurance_strength"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "wrong assurance strength")
    require(review["genuinely_independent"] is False, "same-agent review claimed independent")
    require(review["gov04_risk_tier"] == "TIER_D", "review risk tier mismatch")
    require(review["substantive_change_required_after_review"] is False, "review requires remediation")
    require(review["review_disposition"] == "PASS_GOV05_SINGLE_AGENT_ADVERSARIAL_PARENT_COMPOSITION_REVIEW_NOT_INDEPENDENT", "review did not pass")

    require(integration["input_authoring_head"] == C1_HEAD, "integration input mismatch")
    require(integration["result"] == "QUALIFIED_TCD037_PARENT_COMPOSITION_INTEGRATION_READY_FOR_FORMAL_B3_ADMISSION_DECISION", "integration qualification failed")
    require(integration["new_scientific_process_introduced"] is False, "new physics introduced")
    require(integration["new_state_introduced"] is False, "new state introduced")
    require(integration["new_numerical_policy_introduced"] is False, "new numerical policy introduced")
    require(integration["later_tier_d_surfaces"]["b4"] == "NOT_PERFORMED_NOT_AUTHORIZED", "B4 accidentally authorized")
    require(integration["later_tier_d_surfaces"]["production_authorization"] == "NOT_PERFORMED_NOT_AUTHORIZED", "production accidentally authorized")

    hard = status["hard_boundaries"]
    for key in (
        "production_source_modified", "frozen_b0_modified", "child_admissions_reopened",
        "canonical_tcd_register_modified", "aggregate_modified", "b4", "production_migration",
        "whole_model_golden_baseline", "historical_b2_claim", "global_Ly_equals_Ln_theorem",
        "central_regie_rewrite"
    ):
        require(hard[key] is False, f"forbidden boundary crossed: {key}")

    require(status["aggregate_policy"]["aggregate_updated_in_this_workunit"] is False, "aggregate updated in B3D27")
    require(status["aggregate_policy"]["current_aggregate"] == "ANIMO-RG05I@94afe7d649a8c60758a41996f0059de0acddd2fc", "RG05I pin mismatch")
    require(status["aggregate_policy"]["next_aggregate_handoff"] == "ANIMO-RG05J_SEPARATE_WORKUNIT_AFTER_EXACT_FINAL_GREEN", "missing RG05J handoff")

    allowed_states = {"PERSISTED_VALIDATION_PENDING", "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY"}
    require(status["state"] in allowed_states, "invalid status state")
    if status["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY":
        require(status["parent_tcd_admitted"] is True, "final state without parent admission")
        require(status["decision"] == "ADMIT_TCD037_PARENT_GHG_OBSERVER_COMPOSITION_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_D", "wrong final decision")
        require(status["validation"]["machine_validated"] is True, "final state not machine validated")
        require(status["work_status"]["qualified"] is True, "final state not qualified")
        require(status["work_status"]["work_unit_complete"] is True, "final work unit incomplete")
    else:
        require(status["parent_tcd_admitted"] is False, "pending state already marks parent admitted")
        require(status["decision"] == "PENDING_EXACT_HEAD_VALIDATION", "pending state has wrong decision")

    # Execute the independent bounded parent composition oracle.
    subprocess.run([sys.executable, str(ROOT / "tools/b3d27/tcd037_parent_composition_oracle.py")], cwd=ROOT, check=True)

    head = git("rev-parse", "HEAD")
    if args.expected_head:
        require(head == args.expected_head, f"exact-head mismatch: {head} != {args.expected_head}")

    changed = [line for line in git("diff", "--name-only", f"{BASE_HEAD}..{head}").splitlines() if line]
    allowed_prefixes = (
        "docs/b3/TCD037_PARENT_",
        "integration/animo-b3/TCD037_",
        "integration/animo-b3/B3D27_",
        "tools/b3d27/",
    )
    allowed_exact = {
        "integration/animo-b3/ANIMO-B3D27_STATUS.json",
        "tools/validate_b3d27_tcd037_parent.py",
        ".github/workflows/animo-b3d27-tcd037-parent-composition.yml",
    }
    for path in changed:
        require(path in allowed_exact or path.startswith(allowed_prefixes), f"out-of-scope changed path: {path}")
    require("integration/animo-reg/ANIMO-RG05I_STATUS.json" not in changed, "RG05I modified")

    print(f"ANIMO-B3D27 validator: PASS at {head}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"ANIMO-B3D27 validator: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
