#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B07_STATUS.json"
RISK = ROOT / "integration/animo-b3/TCD041_RISK_CLASSIFICATION.json"
EVIDENCE = ROOT / "integration/animo-b3/TCD041_EVIDENCE_MATRIX.json"
HANDOFF = ROOT / "integration/animo-b3/TCD041_INDEPENDENT_REVIEW_HANDOFF.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"B3B07 validation FAIL: {message}")


def main() -> int:
    status = load(STATUS)
    risk = load(RISK)
    evidence = load(EVIDENCE)
    handoff = load(HANDOFF)

    require(status["work_unit"] == "ANIMO-B3B07", "wrong work unit")
    require(status["target"] == "TCD-041", "wrong target")
    require(status["status"] == "READY_FOR_GOV04_TIER_B_INDEPENDENT_SECOND_LINE_REVIEW_NO_ADMISSION", "unexpected status")
    require(status["admitted"] is False, "readiness workunit may not admit TCD-041")
    require(status["production_source_modified"] is False, "production source modification forbidden")
    require(status["b4_opened"] is False, "B4 must remain closed")
    require(status["central_regie_updated"] is False, "RG05 update forbidden")

    require(risk["policy"] == "ANIMO-GOV04", "GOV04 not pinned")
    require(risk["strictest_applicable_risk_trigger_wins"] is True, "strictest-trigger rule missing")
    require(risk["risk_tier"] == "B", "TCD-041 must remain explicitly classified")
    require(risk["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "unexpected B3 class")
    require(risk["decision"] == "TIER_B_LOCAL_BOUNDARY_WIRING_NOT_PERSISTENT_STATE_INITIALIZATION", "unexpected risk decision")

    tier_c = risk["gov04_tier_c_forced_triggers"]
    expected_triggers = {
        "RESTART_OR_COLD_START_DISCRIMINATION",
        "INITIALIZATION_SEMANTICS",
        "CANONICAL_STATE_OWNERSHIP",
        "CHECKPOINT_SEMANTICS",
        "MISSING_OR_REDEFINED_PHYSICAL_STATE",
        "NUMERICAL_POLICY",
        "SOLVER_OR_TOLERANCE_CHANGE",
        "RUNTIME_BRANCHING_WITH_BEHAVIOURAL_EFFECT",
        "EXACT_ZERO_OR_SINGULAR_DOMAIN_SEMANTICS",
        "AMBIGUOUS_DOMAIN_CONTRACT",
        "SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY",
    }
    require(set(tier_c) == expected_triggers, "Tier C trigger set incomplete or expanded")
    for key, item in tier_c.items():
        require(item["applicable"] is False, f"Tier C trigger became applicable: {key}")
        require(bool(item["rationale"].strip()), f"missing rationale for {key}")

    source = evidence["source_contract"]
    require(source["coordinate"] == "Flair(Nl+1)", "wrong boundary coordinate")
    require(source["unit"] == "m/d (m3 air m-2 d-1)", "wrong unit")
    require(source["direction"] == "DOWNWARD_POSITIVE", "wrong sign convention")
    require(source["required_value"] == 0.0, "closed lower boundary must be zero")
    require(source["persistent_model_state"] is False, "boundary scratch must not be promoted to persistent state")
    require(source["restart_serialized"] is False, "boundary scratch must not be promoted to restart state")
    require(source["recomputed_each_active_task1"] is True, "lifecycle must be explicit")

    require(evidence["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty must remain explicit")
    require(evidence["activation"]["evidence_class"] == "B1_SYNTHETIC_SOURCE_SEAM_ACTIVATION_NOT_B2", "synthetic activation must not be promoted")
    require(evidence["activation"]["source_guard"] == "IoptGHG >= 1", "wrong GHG activation guard")
    require(evidence["activation"]["inactive_control"] == "IoptGHG = 0", "inactive control missing")
    require(evidence["dependencies_on_tcd_032_to_037"] == [], "TCD-032 through TCD-037 composition is forbidden")

    gates = evidence["readiness_gates"]
    for gate, result in gates.items():
        require(result == "PASS", f"readiness gate not PASS: {gate}={result}")

    require(handoff["review_work_unit"] == "ANIMO-B3B07R", "exactly one review handoff must target B3B07R")
    require(handoff["risk_tier"] == "B", "review handoff must preserve Tier B")
    require(handoff["review_required"] is True, "Tier B independent review required")
    require(handoff["review_performed_in_b3b07"] is False, "same context may not perform independent review")
    require(handoff["may_admit"] is False, "review handoff is not an admission object")
    require(handoff["historical_behaviour"] == "UNKNOWN_WITHOUT_B2", "handoff must preserve historical uncertainty")

    expected_authorities = {
        "aggregate_central_regie": "ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73",
        "post_aggregate_atomic_admission": "ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4",
        "GOV04": "ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc",
        "GOV03": "ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c",
        "B3Q01": "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
        "BUILDQ04": "ANIMO-BUILDQ04@0ae1e58f80ca01c1b6eced7ac0d6e5c031827676",
        "BUILDQ03": "ANIMO-BUILDQ03@5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47",
        "GHG01": "ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88",
        "B3I01_TCD041_routing": "ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4",
    }
    require(status["authorities"] == expected_authorities, "authority pin mismatch")
    require(handoff["authorities"] == expected_authorities, "handoff authority pin mismatch")

    print("ANIMO-B3B07 TCD-041 readiness validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
