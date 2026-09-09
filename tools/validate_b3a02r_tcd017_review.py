#!/usr/bin/env python3
import json
from pathlib import Path

BASE = "3ff8f4bda77c631b82110b83317c6a9b42b867ad"
RESULT = "PASS_TCD017_INDEPENDENT_SECOND_LINE_READINESS_REVIEW"
REPORT = Path("docs/b3/TCD017_INDEPENDENT_SECOND_LINE_REVIEW.md")
MACHINE = Path("integration/animo-b3/TCD017_INDEPENDENT_SECOND_LINE_REVIEW.json")


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main():
    require(REPORT.is_file(), f"missing {REPORT}")
    require(MACHINE.is_file(), f"missing {MACHINE}")

    report = REPORT.read_text(encoding="utf-8")
    data = json.loads(MACHINE.read_text(encoding="utf-8"))

    require(data["work_unit"] == "ANIMO-B3A02R", "wrong work unit")
    require(data["frozen_review_object"] == BASE, "wrong frozen review object")
    require(data["result"] == RESULT, "wrong result")
    require(RESULT in report, "report result missing")
    require(data["independence"]["separate_chatgpt_context_from_b3a02_b3d01_authoring"] is True,
            "separate ChatGPT context not asserted")
    require(data["independence"]["organizational_or_human_independence_claimed"] is False,
            "organizational/human independence must not be claimed")

    checks = data["independent_checks"]
    require(len(checks) == 12, "must contain exactly twelve independent checks")
    require([c["id"] for c in checks] == list(range(1, 13)), "check ids must be 1..12")
    require(all(c["status"] == "PASS" for c in checks), "all required checks must PASS for PASS result")

    hist = data["historical_uncertainty"]
    require(hist["b2_exists"] is False, "B2 must remain absent")
    require(hist["historical_revision_53_behaviour"] == "UNKNOWN",
            "historical revision-53 behaviour must remain UNKNOWN")
    require(hist["historical_fidelity_claimed"] is False, "historical fidelity must not be claimed")
    require(hist["synthetic_oracle_promoted_to_b2"] is False, "SYNQ-O002 must not be promoted to B2")

    bounds = data["boundaries"]
    for key in (
        "production_source_modified",
        "physical_state_patch_performed",
        "ploughing_physics_changed",
        "transport_policy_changed",
        "numerical_policy_changed",
        "b3_admission_performed",
        "b4_admission_performed",
    ):
        require(bounds[key] is False, f"{key} must be false")

    require(data["review_decision"]["readiness_review_passed"] is True, "review pass flag missing")
    require(data["review_decision"]["b3_admitted"] is False, "review must not admit B3")

    forbidden = set(data["expected_difference"]["forbidden"])
    for item in ("Bafop", "TCD-027", "TCD-028", "AdStdiorpopl", "Adhuexpopl"):
        require(item in forbidden, f"missing exclusion {item}")

    synq = data["reviewed_authorities"]["synq01"]
    require(synq["oracle"] == "SYNQ-O002", "wrong synthetic oracle")
    gov03 = data["reviewed_authorities"]["gov03"]
    require(gov03["head"] == "cbd262bdabe92923113b7326f2f42822ce9a971c", "wrong GOV03 head")
    require(gov03["closure"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT",
            "wrong GOV03 closure")
    require(gov03["g6u"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS",
            "wrong G6U state")
    require(data["reviewed_authorities"]["b3d01"]["head"] ==
            "6ada2522101587ab74974a70f980b50e64cf9b86", "wrong B3D01 head")
    require(data["reviewed_authorities"]["b3d01"]["disposition_at_review"] == "UNRESOLVED_NOT_ADMITTED",
            "B3D01 admission boundary changed")

    require("raw licensed source" in report.lower(), "raw-source limitation not documented")
    require("not b3 admission" in report.lower(), "non-admission boundary not explicit")

    print("PASS_B3A02R_TCD017_REVIEW_RECORD_VALIDATION")


if __name__ == "__main__":
    main()
