#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "integration/animo-science/SQ06_TCD016_C1_DRY_HOLD_PROCESS_QUALIFICATION.json"
FREEZE = ROOT / "integration/animo-science/ANIMO-SQ06_AUTHORING_FREEZE.json"
STATUS = ROOT / "integration/animo-science/ANIMO-SQ06_STATUS.json"
REVIEW = ROOT / "integration/animo-science/ANIMO-SQ06_INTERNAL_ADVERSARIAL_REVIEW.json"
FRAGMENT = ROOT / "integration/animo-testbank/fragments/ANIMO-SQ06_TCD016_C1_DRY_HOLD_NEGATIVE_FRAGMENT.json"
ORACLE = ROOT / "tools/sq06/tcd016_c1_dry_hold_negative_oracle.py"

EXPECTED_AUTHORITIES = {
    "aggregate": "ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe",
    "global_b3_queue": "ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700",
    "gov05": "ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904",
    "gov04": "ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc",
    "gov03": "ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c",
    "b3q01": "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
    "sq01": "ANIMO-SQ01@26d0c74aa440bd73c23709d313e24ea8af2a0bcd",
    "sq02": "ANIMO-SQ02@09ab76f0b44cb72956875fa379d68bbf97f1a0c7",
    "sq03": "ANIMO-SQ03@58dc3c5c108ee97fd6bea107b7a9e686596617b1",
    "sq04": "ANIMO-SQ04@063627cddd478904c437c9c47f02513ef0d9326b",
    "sq05": "ANIMO-SQ05@897ba742630f06381a2b89290db80d5f405ab51d",
    "massq04": "ANIMO-MASSQ04@3e0f8254d9cd7966a4491b3068d0239b8ccda5f9"
}


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def load(path):
    return json.loads(path.read_text())


def validate_package(p):
    require(p["work_unit"] == "ANIMO-SQ06", "wrong work unit")
    require(p["target"] == "TCD-016-C1", "wrong target")
    require(p["scope"] == "MODEL_EVOLUTION_DRY_HOLD_PROCESS_LAW_ONLY", "scope broadened")
    for key, value in EXPECTED_AUTHORITIES.items():
        require(p["authorities"][key] == value, f"authority drift: {key}")
    require(p["decision"] == "NO_DRY_HOLD_PROCESS_LAW_SCIENTIFICALLY_QUALIFIED", "wrong scientific decision")
    require(p["final_qualification"] == "QUALIFIED_NEGATIVE_NO_DRY_HOLD_PROCESS_LAW_CURRENTLY_DEFENSIBLE", "wrong final qualification")
    require(p["positive_process_contract"] is None, "positive process contract introduced")
    require(p["parameters"] == [], "parameter invented")
    require(p["parameter_provenance"] == "NO_PROCESS_PARAMETERS_INTRODUCED_OR_CALIBRATED", "parameter provenance changed")
    require(p["hypotheses"]["H5"]["disposition"] == "SELECTED", "H5 not selected")
    for h in ("H0", "H1", "H2", "H3", "H4"):
        require(p["hypotheses"][h]["disposition"].startswith("REJECTED"), f"{h} is not rejected")
    require(p["hypotheses"]["H0"]["disposition"] != "SELECTED", "H0 promoted by convenience")
    require(p["inherited_contract"]["no_process_update_is_physical_inertness_claim"] is False, "state persistence promoted to physical inertness")
    require(p["inherited_contract"]["chemically_noncommittal"] is True, "chemical identity invented")
    require(p["evidence_hierarchy_application"]["external_literature_invoked"] is False, "external evidence declaration mismatch")
    require(p["dry_hold_operational_semantics_after_negative_qualification"]["process_rate"] is None, "rate law silently introduced")
    require(p["dry_hold_operational_semantics_after_negative_qualification"]["process_transfer"] is None, "process transfer silently introduced")
    require(p["dry_hold_operational_semantics_after_negative_qualification"]["rewetting_semantics"] == "OUT_OF_SCOPE_AND_UNQUALIFIED", "rewetting leaked into scope")
    require(p["mass_state_restart_implications"]["observer_can_reconstruct_missing_state_from_residual"] is False, "observer owns state")
    require(p["disposition"]["tcd016_c1_b3"] == "UNRESOLVED_NOT_ADMITTED", "C1 B3 admission leaked")
    require(p["disposition"]["parent_tcd016_b3"] == "UNRESOLVED_NOT_ADMITTED", "parent B3 admission leaked")
    require(p["disposition"]["canonical_register_mutation"] is False, "canonical mutation declared")
    require(p["disposition"]["global_b3_queue_mutation"] is False, "queue mutation declared")


def validate_freeze(f):
    require(f["work_unit"] == "ANIMO-SQ06", "freeze work unit mismatch")
    require(f["base_head"] == "3e0f8254d9cd7966a4491b3068d0239b8ccda5f9", "freeze base changed")
    require(f["review_must_pin_exact_green_authoring_head"] is True, "review head pin disabled")
    require(f["substantive_change_resets_review"] is True, "review reset disabled")
    require(f["exact_final_head_ci_required"] is True, "exact final CI disabled")
    require("integration/animo-science/ANIMO-SQ06_STATUS.json" in f["post_review_allowed_changes"], "status closeout not allowed")
    require("integration/animo-science/ANIMO-SQ06_INTERNAL_ADVERSARIAL_REVIEW.json" in f["post_review_allowed_changes"], "review closeout not allowed")


def validate_fragment(fragment):
    require(fragment["work_unit"] == "ANIMO-SQ06", "fragment mismatch")
    require(fragment["central_registry_modified"] is False, "central registry mutation")
    require(fragment["whole_model_golden_baseline"] is False, "whole model golden")
    require(fragment["qualification"]["selected_hypothesis"] == "H5", "fragment hypothesis mismatch")
    require(fragment["qualification"]["positive_process_contract_qualified"] is False, "fragment qualifies positive law")
    ids = [e["id"] for e in fragment["entries"]]
    require(len(ids) == len(set(ids)), "duplicate fragment IDs")
    required = {"SQ06-HYP-GATE-001", "SQ06-NOPROCESS-MASS-001", "SQ06-ZERO-MASS-001", "SQ06-TIMESTEP-001", "SQ06-RESTART-001", "SQ06-OBSERVER-001"}
    require(set(ids) == required, "bounded oracle set changed")


def validate_status(status):
    require(status["work_unit"] == "ANIMO-SQ06", "status mismatch")
    require(status["selected_hypothesis"] == "H5", "status hypothesis mismatch")
    require(status["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical behavior promoted")
    require(status["positive_process_contract_qualified"] is False, "positive law status")
    require(status["process_parameters_introduced"] is False, "parameter status")
    require(status["b3_admission_performed"] is False, "B3 admission status")
    require(status["production_authorized"] is False, "production authorization status")
    for key, value in status["hard_boundaries"].items():
        require(value is False, f"hard boundary violated: {key}")

    if status["qualified"]:
        require(status["state"] == "QUALIFIED_NEGATIVE_NO_DRY_HOLD_PROCESS_LAW_CURRENTLY_DEFENSIBLE", "qualified state mismatch")
        require(status["decision"] == "NO_DRY_HOLD_PROCESS_LAW_SCIENTIFICALLY_QUALIFIED", "qualified decision mismatch")
        review = status["review"]
        require(REVIEW.exists(), "qualified status without adversarial review")
        require(review["completed"] is True, "review incomplete")
        require(review["same_agent"] is True, "review mode mismatch")
        require(review["genuinely_independent"] is False, "false independence claim")
        require(review["independence_claimed"] is False, "independence claimed")
        require(review["outcome"] == "SELF_REVIEW_PASS", "review did not pass")
        require(status["work_status"]["tested"] is True, "qualified without tests")
        require(status["work_status"]["reviewed"] is True, "qualified without review")
        require(status["work_status"]["qualified"] is True, "work status not qualified")
    else:
        require(status["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "unexpected pre-review phase")
        require(status["review"]["completed"] is False, "pre-review status says reviewed")


def validate_review(review, status):
    require(review["work_unit"] == "ANIMO-SQ06", "review work unit mismatch")
    require(review["risk_tier"] == "C_SCIENTIFIC_PROCESS_SEMANTICS", "review tier mismatch")
    require(review["review_mode"] == "SAME_AGENT_SECOND_PASS", "review mode mismatch")
    require(review["same_agent"] is True, "same-agent flag missing")
    require(review["genuinely_independent"] is False, "review falsely independent")
    require(review["independence_claimed"] is False, "independence claim forbidden")
    require(review["outcome"] == "SELF_REVIEW_PASS", "review outcome mismatch")
    require(review["selected_hypothesis_after_review"] == "H5", "review changed hypothesis without remediation")
    require(review["substantive_findings"] == [], "unremediated substantive findings")
    required_gates = {
        "NUMERICAL_CONVENIENCE_NOT_PHYSICS", "ABSENCE_OF_EVIDENCE_NOT_HISTORICAL_BEHAVIOUR", "MASS_CLOSURE_NOT_SCIENTIFIC_VALIDITY",
        "NO_REJECTED_REV53_PROCESS_REUSE", "NO_IMPLICIT_RECEIVER", "NO_PARAMETER_INVENTION", "NO_DOUBLE_COUNTING",
        "NO_REWETTING_SCOPE_LEAKAGE", "OBSERVER_NOT_STATE_OWNER", "EXTERNAL_LITERATURE_PROVENANCE", "H0_NOT_PROMOTED_TO_INERTNESS"
    }
    require(set(review["adversarial_gates"].keys()) == required_gates, "review gate set changed")
    require(all(v == "PASS" for v in review["adversarial_gates"].values()), "adversarial gate failed")
    require(review["reviewed_authoring_head"] == status["review"]["reviewed_head"], "reviewed head mismatch")


def main():
    for path in (PACKAGE, FREEZE, STATUS, FRAGMENT, ORACLE):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")
    p, f, status, fragment = map(load, (PACKAGE, FREEZE, STATUS, FRAGMENT))
    validate_package(p)
    validate_freeze(f)
    validate_fragment(fragment)
    validate_status(status)
    subprocess.run([sys.executable, str(ORACLE)], cwd=ROOT, check=True)
    if REVIEW.exists():
        validate_review(load(REVIEW), status)
    print("PASS SQ06 bounded dry-hold qualification package")


if __name__ == "__main__":
    main()
