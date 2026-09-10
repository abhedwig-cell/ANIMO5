#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "integration/animo-b3/ANIMO-B3B08R_REVIEW_RESULT.json"
REPORT = ROOT / "docs/b3/TCD028_INDEPENDENT_TIER_C_REVIEW.md"


def require(cond, msg):
    if not cond:
        raise SystemExit(f"FAIL: {msg}")


def main():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    report = REPORT.read_text(encoding="utf-8")

    require(data["work_unit"] == "ANIMO-B3B08R", "wrong work unit")
    require(data["target"] == "TCD-028", "wrong target")
    require(data["semantic_result"] in {"PASS", "FAIL", "INCOMPLETE"}, "invalid semantic result")
    require(data["semantic_result"] == "PASS", "persisted review is not PASS")

    obj = data["reviewed_object"]
    require(obj["readiness_head"] == "310d7117da739d19eebb718129ac9494cac854a1", "readiness head moved")
    require(obj["validated_substantive_evidence_head"] == "0145b80e7e308d82995f783cc4febb3b4c9da6ad", "substantive evidence head moved")
    require(obj["readiness_ci_run"] == 34490160286, "wrong readiness run")
    require(obj["readiness_ci_job"] == 102914502580, "wrong readiness job")
    require(obj["readiness_ci_conclusion"] == "success", "readiness CI not successful")

    auth = data["live_authorities"]
    require(auth["aggregate_central_regie"] == "ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e", "aggregate authority mismatch")
    require(auth["post_rg05f_atomic_admissions"] == [
        "ANIMO-B3D15@22e48f7e2c1eaa1245f034de2d909191d9cfa227:TCD-030",
        "ANIMO-B3D16@8650ea9e716336520d8d7df5f9ea2b393d17ab98:TCD-023",
    ], "post-RG05F admissions mismatch")
    require(auth["gov04"] == "ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc", "GOV04 mismatch")
    require(auth["gov03"] == "ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c", "GOV03 mismatch")
    require(auth["b3q01"] == "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54", "B3Q01 mismatch")
    require(auth["b3i01"] == "ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4", "B3I01 mismatch")
    require(auth["b3i03"] == "ANIMO-B3I03@814ea660d367494432beb63ea78298d1f6cd73d7", "B3I03 mismatch")
    require(auth["prep10"] == "ANIMO-PREP10@65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab", "PREP10 mismatch")
    require(auth["prep10c"] == "ANIMO-PREP10C@549545921dc8175f01d86c283647acd470c14290", "PREP10C mismatch")
    require(auth["canonical_tcd028_state"] == "OPEN", "canonical TCD-028 state is not OPEN")
    require(not auth["newer_tcd028_authority_found"], "newer TCD-028 authority found")

    pins = data["source_and_candidate_pins"]
    require(pins["frozen_addit_sha256"] == "e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d", "frozen Addit mismatch")
    require(pins["candidate_addit_sha256"] == "a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae", "candidate Addit mismatch")
    require(pins["candidate_change"] == [
        "SuStdiorma = 0.0",
        "SuStdiorni = 0.0",
        "If (Ipo.Eq.1) SuStdiorpo = 0.0",
    ], "candidate is not the exact three-reset object")

    science = data["independent_scientific_determination"]
    require(science["ownership"] == "CURRENT_PLOUGH_EVENT_TRANSACTION_ACCUMULATORS", "ownership not resolved event-local")
    require(science["cumulative_cross_event_storage_intended"] is False, "cumulative storage interpretation remains enabled")
    require(science["event_start_additive_identity_required"] is True, "zero identity not required")
    require(science["stale_prior_is_redistributed_again_if_present"] is True, "stale prior causal identity absent")
    require(science["zero_initialization_removes_only_stale_prior_term"] is True, "reset scope not atomic")

    cls = data["classification"]
    require(cls["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "wrong B3 class")
    require(cls["gov04_risk_tier"] == "C", "wrong GOV04 risk tier")
    require(set(cls["tier_c_triggers"]) == {
        "INITIALIZATION_SEMANTICS",
        "SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY",
    }, "Tier-C trigger set mismatch")
    require(cls["stronger_gov04_trigger_found"] is False, "stronger GOV04 trigger unresolved")

    hist = data["historical_uncertainty"]
    require(hist["qualified_b2_available"] is False, "unexpected B2 claim")
    require(hist["historical_revision53_manifestation"] == "UNKNOWN_WITHOUT_B2", "historical boundary weakened")
    require(hist["current_gnu_persistence_is_b2"] is False, "GNU evidence promoted to B2")
    require(hist["historical_fidelity_claimed"] is False, "historical fidelity improperly claimed")

    nonint = data["frozen_testbank_non_interference"]
    require(nonint["scientific_or_structural_differences"] == 0, "frozen non-interference mismatch")
    require(nonint["interpretation"] == "SUPPORTING_NON_INTERFERENCE_ONLY_NON_DISCRIMINATING_FOR_TCD028", "frozen matrix limitation missing")

    actions = data["scope_and_non_actions"]
    require(all(v is False for v in actions.values()), "review contains a forbidden admission/migration mutation")

    required_report_tokens = [
        "Review result: `PASS`",
        "CURRENT_PLOUGH_EVENT_TRANSACTION_ACCUMULATORS",
        "B_LOCAL_ALGEBRA_INDEX_SPECIES",
        "GOV04 risk tier: `C`",
        "UNKNOWN_WITHOUT_B2",
        "supporting scope/non-interference evidence only",
        "no B3 admission",
        "separate Tier-C formal-disposition workunit",
    ]
    # Ownership label is described in prose rather than as a machine token.
    required_report_tokens[1] = "current-event transaction accumulators"
    for token in required_report_tokens:
        require(token in report, f"report missing required token: {token}")

    print("PASS_B3B08R_TCD028_INDEPENDENT_TIER_C_REVIEW")


if __name__ == "__main__":
    main()
