#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3E01 TCD-042-E1 admission readiness.

The validator checks the inherited NQ03/NQ03R/B3I05 evidence, the current B3
schema, pinned GOV02/PREP02R governance state and the cross-stream Hetop=0
source-domain finding. It does not admit B3 and does not validate production
code because B3E01 contains no production patch.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B3E01_BASE = "0153779e9045c6527b7c31156f2295ff44b57eeb"
B3B02_HEAD = "412bf889ce959d85c651c3b9180dec0a6ff9bb61"
PREP02R_HEAD = "a2fda49871ee3c7104daf7e06cd8dffdac06b125"
GOV02_HEAD = "db7add6f9561730bbf352aa7fd3f3968405cfaa3"

READINESS = ROOT / "integration/animo-b3/TCD042_E1_CLASS_E_READINESS.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3E01_STATUS.json"
B3I05 = ROOT / "integration/animo-b3/ANIMO-B3I05_STATUS.json"
ATOMIZATION = ROOT / "integration/animo-b3/B3I05_TCD042_ATOMIZATION.json"
SCHEMA = ROOT / "integration/animo-b3/B3_DISPOSITION_SCHEMA.json"
NQ03 = ROOT / "integration/animo-science/ANIMO-NQ03_STATUS.json"
NQ03R = ROOT / "integration/animo-science/ANIMO-NQ03R_STATUS.json"
DOC = ROOT / "docs/b3/TCD042_E1_CLASS_E_ADMISSION_READINESS.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git_show_json(commit: str, path: str) -> dict:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def changed_paths(base: str, head: str = "HEAD") -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    b3i05 = json.loads(B3I05.read_text(encoding="utf-8"))
    atomization = json.loads(ATOMIZATION.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    nq03 = json.loads(NQ03.read_text(encoding="utf-8"))
    nq03r = json.loads(NQ03R.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(readiness["work_unit"] == "ANIMO-B3E01", "wrong readiness workunit")
    require(readiness["target_parent"] == "TCD-042", "wrong parent")
    require(readiness["target_atom"] == "TCD-042-E1", "wrong child atom")
    require(readiness["class"] == "E_NUMERICAL_POLICY", "wrong qualification class")
    require(readiness["requested_trigger"] == "Flpn=0 AND 0<Flux<1.0d-8", "trigger widened or changed")

    # Canonical child routing must remain exactly B1 plus E1 and must not create TCD-043.
    require(b3i05["status"] == "QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS", "B3I05 qualified routing lost")
    require(b3i05["work_status"]["qualified"] is True and b3i05["work_status"]["work_unit_complete"] is True, "B3I05 not complete")
    atoms = {item["atom_id"]: item for item in atomization["atoms"]}
    require(set(atoms) == {"TCD-042-B1", "TCD-042-E1"}, "canonical child set changed")
    require(atomization["allocation_decision"]["tcd_043_reserved"] is False, "TCD-043 reserved")
    require(atomization["allocation_decision"]["child_atom_keys_are_top_level_register_rows"] is False, "child keys promoted to top-level TCD rows")

    # NQ03 and NQ03R must establish the restricted Class-E policy and review, not admission.
    require(nq03["target"] == "TCD-042-E1", "NQ03 target drift")
    require(nq03["class"] == "E_NUMERICAL_POLICY", "NQ03 class drift")
    require(nq03["selected_policy"]["name"] == "NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY", "selected policy identity drift")
    require("Hetop>0" in nq03["selected_policy"]["applicability"], "NQ03 positive-Hetop domain lost")
    require(nq03["selected_policy"]["outside_envelope"] == "NOT_QUALIFIED_FAIL_CLOSED", "NQ03 outside-envelope fail-closed rule lost")
    require(nq03["admission"]["numerical_policy_admitted_to_B3"] is False, "NQ03 improperly admitted policy")
    require(nq03["scope_guards"]["tcd042_b1_modified"] is False, "NQ03 reopened B1")

    require(nq03r["review_outcome"] == "INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY", "NQ03R review no longer passes")
    require(nq03r["work_status"]["qualified"] is True and nq03r["work_status"]["work_unit_complete"] is True, "NQ03R not complete")
    require(nq03r["review_contract"]["methodological_independence_satisfied"] is True, "NQ03R methodological independence lost")
    require(nq03r["review_contract"]["organizational_independence_claimed"] is False, "NQ03R overclaims organizational independence")
    finding = nq03r["implementation_order_finding"]
    require(finding["severity"] == "NON_BLOCKING_FOR_RESTRICTED_POLICY_BLOCKING_BEFORE_BITWISE_PRODUCTION_BINDING", "implementation-order finding changed")
    require(finding["unique_points_with_any_literal_order_mismatch"] == 129, "implementation-order mismatch count changed")

    # Pinned cross-stream source-domain evidence: parser accepts Hetop=0.
    b3b02 = git_show_json(B3B02_HEAD, "integration/animo-b3/ANIMO-B3B02_STATUS.json")
    domain = b3b02["domain_precondition"]
    require(domain["legacy_input_accepts_Hetop_zero"] is True, "peer source-domain evidence no longer accepts Hetop=0")
    require(domain["input_source"] == "input1.for:1826-1829", "Hetop source location changed")
    require(domain["input_lower_bound"] == 0.0, "Hetop lower bound changed")
    require(domain["candidate_division_by_zero_at_Hetop_zero"] is True, "positive-Hetop domain issue disappeared")

    recon = readiness["domain_reconciliation"]
    require(recon["nq03_requires_Hetop_positive"] is True, "readiness lost NQ03 positive-Hetop precondition")
    require(recon["legacy_input_accepts_Hetop_zero"] is True, "readiness lost parser domain fact")
    require(recon["full_B3I05_E1_trigger_covered_by_NQ03"] is False, "full child domain incorrectly marked covered")
    require(recon["zero_thickness_semantics"] == "FAIL_CLOSED_UNRESOLVED", "zero-thickness semantics incorrectly resolved")
    require(recon["silent_Hetop_guard_authorized"] is False, "silent Hetop guard authorized")

    # Live PREP02R authority is pinned and must keep both admission routes closed.
    prep = git_show_json(PREP02R_HEAD, "integration/animo-prep/PREP02R_STATUS.json")
    require(prep["status"] == "PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED", "PREP02R state changed from pinned readiness authority")
    effect = prep["reference_effect"]
    require(effect["normal_B2_reference_available"] is False, "normal B2 unexpectedly available")
    require(effect["historical_uncertainty_route_eligible"] is False, "historical-uncertainty route unexpectedly eligible")
    require(prep["public_and_external_acquisition"]["external_request_sent"] is False, "external request state differs from readiness snapshot")
    require(prep["received_native_executable_review"]["historical_release_binary"] is False, "2026 native rebuild misclassified as historical")

    internal = git_show_json(PREP02R_HEAD, "integration/animo-prep/PREP02R_INTERNAL_RECOVERY_DISPOSITION_20260909.json")
    require(internal["gov02_state"]["b2_acquisition_state"] == "B2_ACQUISITION_STILL_ACTIVE", "internal stop incorrectly closes B2 acquisition")
    require(internal["gov02_state"]["historical_uncertainty_route_eligible"] is False, "internal stop incorrectly activates historical uncertainty route")

    gov02 = git_show_json(GOV02_HEAD, "integration/animo-governance/ANIMO-GOV02_STATUS.json")
    require(gov02["qualified"] is True, "GOV02 authority not qualified")
    require("separate numerical formulation" in gov02["class_policy"]["E"], "GOV02 Class-E policy changed")
    require("independent numerical review" in gov02["class_policy"]["E"], "GOV02 independent numerical review rule missing")

    route = readiness["governance_route"]
    require(route["normal_B2_reference_available"] is False, "readiness claims normal B2")
    require(route["historical_uncertainty_route_eligible"] is False, "readiness claims historical uncertainty eligibility")
    require(route["normal_route"].startswith("FAIL_CLOSED"), "normal route not fail closed")
    require(route["historical_uncertainty_route"].startswith("FAIL_CLOSED"), "historical uncertainty route not fail closed")

    # Current formal disposition schema cannot directly encode the B3I05 child key.
    tcd_pattern = schema["properties"]["tcd_ids"]["items"]["pattern"]
    require(tcd_pattern == "^TCD-[0-9]{3}$", "B3Q01 tcd_ids pattern changed; readiness must be re-evaluated")
    require(re.fullmatch(tcd_pattern, "TCD-042") is not None, "parent no longer matches B3 schema")
    require(re.fullmatch(tcd_pattern, "TCD-042-E1") is None, "child now matches schema; carrier blocker must be revisited")
    carrier = readiness["formal_disposition_carrier"]
    require(carrier["child_atom_matches_current_tcd_id_pattern"] is False, "readiness child/schema mismatch lost")
    require(carrier["parent_only_substitution_used"] is False, "readiness silently substitutes parent for child")
    require(carrier["treatment"].startswith("FAIL_CLOSED"), "formal child carrier not fail closed")

    gates = readiness["readiness_gates"]
    for key in (
        "frozen_B0_identity", "canonical_child_routing", "governing_equation",
        "legacy_policy_reconstructed", "conditioning_coordinate", "high_precision_oracle",
        "independent_numerical_review", "natural_reachability"
    ):
        require(gates[key].startswith("PASS"), f"required qualified gate lost: {key}")
    for key in (
        "implementation_order_for_production_binding", "full_child_trigger_domain",
        "zero_thickness_semantics", "normal_B2_route", "historical_uncertainty_route",
        "formal_child_disposition_carrier", "independent_B3_disposition_review"
    ):
        require(gates[key].startswith("FAIL_CLOSED"), f"blocking gate unexpectedly passed: {key}")

    admission = readiness["admission"]
    require(admission["restricted_positive_Hetop_numerical_policy_qualified"] is True, "restricted policy qualification lost")
    require(admission["full_requested_E1_trigger_admission_ready"] is False, "full E1 trigger incorrectly admission-ready")
    for key in ("corrected_legacy_admitted", "parent_tcd_admitted", "numerical_policy_admitted_to_B3", "production_binding_authorized", "production_migration_admitted"):
        require(admission[key] is False, f"unexpected admission/authorization: {key}")

    # Status may be persisted pre-closeout or final, but it may never claim admission.
    require(status["work_unit"] == "ANIMO-B3E01", "wrong status workunit")
    require(status["target_atom"] == "TCD-042-E1", "wrong status target atom")
    for key, value in status["scope_guards"].items():
        require(value is False, f"status scope guard violated: {key}")

    # Workunit must remain additive and outside production source / canonical register.
    allowed = (
        ".github/workflows/animo-b3e01-",
        "docs/b3/TCD042_E1_CLASS_E_ADMISSION_READINESS.md",
        "integration/animo-b3/ANIMO-B3E01_STATUS.json",
        "integration/animo-b3/TCD042_E1_CLASS_E_READINESS.json",
        "tools/b3e01/",
    )
    changed = changed_paths(B3E01_BASE)
    require(changed, "B3E01 contains no artifacts")
    for path in changed:
        require(path.startswith(allowed), f"B3E01 scope widened by {path}")
        require(not path.startswith("src/"), "B3E01 modified production source")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "B3E01 modified canonical TCD register")
        require("TCD042_ZERO" not in path, "B3E01 modified TCD-042-B1 artifact")

    require("Hetop=0" in doc or "Hetop = 0" in doc, "readiness document omits zero-thickness blocker")
    require("TCD-043" in doc, "readiness document must explicitly preserve no-new-TCD rule")
    require("No corrected-legacy admission" in doc, "readiness document lacks non-admission closeout")

    print("B3E01 PASS: restricted positive-Hetop E1 policy qualified, but full child domain, B2/GOV02 route, formal child disposition and B3 review remain fail closed; no admission or production change")


if __name__ == "__main__":
    main()
