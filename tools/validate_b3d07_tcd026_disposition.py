#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPOSITION = ROOT / "integration/animo-b3/TCD026_B3_DISPOSITION_GOV03.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D07_STATUS.json"
DOC = ROOT / "docs/b3/TCD026_GOV03_FORMAL_DISPOSITION.md"

RG05C = "2d3cc363599ed32b6537f318462c27db5ffaa7c2"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3A04 = "5eaf02298603b85f802d8e35d6a63941d0878879"
B3A04R = "27b1700a330959d1b5eae23a2094cad579630f14"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
DECISION = "UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03"
CANDIDATE = "Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P"


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL_B3D07: " + msg)


def main():
    disposition = json.loads(DISPOSITION.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(disposition["record_id"] == "B3D07-TCD026-GOV03-DISPOSITION", "record id")
    require(disposition["tcd_ids"] == ["TCD-026"], "atomic TCD identity")
    require(disposition["atomicity"] == "ATOMIC", "atomicity")
    require(disposition["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "Class-A identity")
    require(disposition["admission_route"] == ROUTE, "route")
    require(disposition["scope"]["candidate_atomic_observation"] == CANDIDATE, "candidate expression")

    auth = disposition["authorities"]
    require(auth["RG05C"] == RG05C, "RG05C authority")
    require(auth["GOV03"] == GOV03, "GOV03 authority")
    require(auth["B3A04"] == B3A04, "B3A04 authority")
    require(auth["B3A04R_TECH"] == B3A04R, "B3A04R authority")
    require(auth["B3Q01"] == B3Q01, "B3Q01 authority")

    b2 = disposition["identities"]["b2"]
    require(b2["status"] == "UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT", "B2 status")
    require(GOV03 in b2["acquisition_effort_ref"], "GOV03 acquisition ref")

    route = disposition["historical_route"]
    require(route["B2_available"] is False, "B2 unavailable")
    require(route["b2_route_gate"] == "PASS", "route gate PASS")
    require(route["historical_behaviour"] == "UNKNOWN", "historical behaviour unknown")
    require(route["historical_fidelity_claimed"] is False, "no historical fidelity")

    rr = disposition["readiness_reconciliation"]
    require(rr["exact_physical_owner"] == "PASS", "physical owner")
    require(rr["exact_omitted_ledger_term"] == "PASS", "omitted term")
    require(rr["PREP06_synthetic_causal_discriminator"] == "PASS_10_KG_HA", "synthetic activation")
    require(rr["model_produced_restart_activation"] == "PASS_5989_6594_KG_HA", "model-produced activation")
    require(rr["chronological_restart_activation"] == "PASS_642_718929_KG_HA", "chronological activation")
    require(rr["SYNQ01_specific_TCD026_oracle"] == "NONE_REGISTERED_NO_FALSE_ORACLE_CLAIM", "no false SYNQ oracle")
    require("NOT_LEDGER_ORACLE_NOT_B2" in rr["STATEQ02_scope_boundary"], "STATEQ02 boundary")
    require(rr["same_context_technical_review"] == "PASS_TECHNICAL_NOT_INDEPENDENT", "technical review boundary")

    expected = disposition["expected_difference"]
    require(set(expected["changed_surfaces"]) == {
        "ani_omGP.Bal", "ani_omRP.Bal", "ani_omTP.Bal",
        "baomGP.Out", "baomRP.Out", "baomTP.Out"
    }, "six-surface whitelist")
    unchanged = set(expected["required_unchanged"])
    for item in {
        "all physical state trajectories",
        "all process flux trajectories",
        "initialization physics",
        "all numerical tolerances and policies",
        "other organic-matter TCDs",
    }:
        require(item in unchanged, "required unchanged: " + item)

    gates = disposition["gates"]
    require(gates["b2_route"].startswith("PASS"), "B2 route gate")
    require(gates["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "independent review pending")
    require(gates["composition_if_applicable"] == "PASS_NOT_APPLICABLE", "composition not applicable")

    review = disposition["independent_review"]
    require(review["required"] is True, "review required")
    require(review["same_authoring_context_may_count"] is False, "authoring context excluded")
    require(review["technical_review_independent"] is False, "technical review not independent")
    require(review["gate"] == "BLOCKING", "review gate blocking")

    decision = disposition["admission_decision"]
    require(decision["admitted"] is False, "not admitted")
    require(decision["decision"] == DECISION, "bounded decision")
    require(decision["production_patch_authorized"] is False, "no production patch")
    require(decision["production_migration_admitted"] is False, "no production migration")

    require(status["base"]["head"] == RG05C, "status base")
    require(B3A04 in status["readiness_authority"], "status readiness authority")
    require(B3A04R in status["technical_review_authority"], "status technical review authority")
    require(status["route_reconciliation"]["b2_route_gate"] == "PASS", "status route PASS")
    require(status["route_reconciliation"]["historical_behaviour"] == "UNKNOWN", "status historical unknown")
    require(status["scientific_gates"]["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "status review pending")
    require(status["admission"]["admitted"] is False, "status not admitted")

    require("No TCD-026-specific SYNQ01 oracle is registered" in doc, "doc SYNQ boundary")
    require("does not establish exact whole-model continuous-versus-formatted-restart identity" in doc, "doc restart boundary")
    require("cannot satisfy the independent second-line gate" in doc, "doc independence boundary")

    if status["work_status"]["qualified"]:
        require(status["state"] == "QUALIFIED_TCD026_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION", "qualified state")
        require(status["decision"] == DECISION, "qualified decision")
        require(status["work_status"]["tested"] is True, "qualified tested")
        require(status["work_status"]["work_unit_complete"] is True, "qualified complete")

    print("PASS_B3D07_TCD026_GOV03_DISPOSITION")


if __name__ == "__main__":
    main()
