#!/usr/bin/env python3
import json
from pathlib import Path

RESULT = Path("integration/animo-b3/TCD018_INDEPENDENT_REVIEW_RESULT.json")
REPORT = Path("docs/b3/TCD018_INDEPENDENT_SECOND_LINE_REVIEW.md")
EXPECTED_RESULT = "FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW"
EXPECTED_BLOCKERS = [8, 10, 11, 13, 14, 15]
EXPECTED_WHITELIST = [
    "bawaGP.Out",
    "bawaRP.Out",
    "bawaTP.Out",
    "ani_waGP.Bal",
    "ani_waRP.Bal",
    "ani_waTP.Bal",
]
EXPECTED_HEADS = {
    "ANIMO-B3A03": "8eaaca34e4f0d906c2d8245f0df232586efe8ff3",
    "ANIMO-B3A03R_same_context_evidence_only": "0876e6e1b6ce33ee5e7b812ab4107f54760d6b27",
    "ANIMO-B3D05": "2f06cc86225637f8dadfdd969fe48dcf851b9ee2",
    "ANIMO-RG05B": "c353c3179f213c1bf24c48b3c06f8065c760d3e2",
    "ANIMO-GOV03": "cbd262bdabe92923113b7326f2f42822ce9a971c",
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


data = json.loads(RESULT.read_text(encoding="utf-8"))
report = REPORT.read_text(encoding="utf-8")

require(data["overall_result"] == EXPECTED_RESULT, "exact fail-closed result token")
require(data["classification"] == "A_ACCOUNTING_REPORTING_ONLY", "atomic Class-A classification")
require(data["separate_chatgpt_context_from_B3A03_B3D05_authoring"] is True, "separate ChatGPT context statement")
require(data["organizational_or_human_independence_claimed"] is False, "no human/organizational independence claim")
require(data["review_start_head"] == "3096c4dfa6a2cee72504445a71fc211842feb9cd", "clean review start head")
require({k: data["reviewed_heads"][k] for k in EXPECTED_HEADS} == EXPECTED_HEADS, "authority heads pinned exactly")
require(len(data["gates"]) == 21 and set(data["gates"]) == {str(i) for i in range(1, 22)}, "all 21 gates recorded")
require(data["blocking_unresolved_gates"] == EXPECTED_BLOCKERS, "blocking unresolved gates exact")
for gate in EXPECTED_BLOCKERS:
    require(data["gates"][str(gate)].startswith("UNRESOLVED"), f"gate {gate} must remain unresolved")
require(data["exact_declared_whitelist"] == EXPECTED_WHITELIST, "exact six-file whitelist and order")
run = data["isolated_run_reported_not_independently_derived"]
require((run["cases"], run["outputs_compared"], run["equal_after_declared_volatile_normalization"], run["whitelisted_differences"], run["unexpected_differences"]) == (8, 376, 370, 6, 0), "same-context run numbers retained only as reported evidence")
require(run["status"] == "REPORTED_BY_SAME_CONTEXT_EVIDENCE_NOT_PROMOTED_TO_INDEPENDENT_FACT", "same-context evidence not promoted")
require(run["scientific_numeric_tolerance_applied"] is False, "no scientific numeric tolerance")
require(data["residual_boundaries"]["LWKM_approximately_0_0601_mm"] == "CAUSAL_EVIDENCE_NOT_TOLERANCE", "0.0601 mm is not a tolerance")
require(data["residual_boundaries"]["MASSQ01_CranGrass_TITO724_mm"] == -0.0030198960466805147, "MASSQ01 residual exact")
require(data["residual_boundaries"]["MASSQ01_CranGrass_TITO724_class"] == "UNEXPLAINED_RESIDUAL", "MASSQ01 residual remains unexplained")
require(data["residual_boundaries"]["global_water_closure_claimed"] is False, "no global water closure claim")
require(data["historical_route"]["qualified_B2_exists"] is False, "no qualified B2")
require(data["historical_route"]["historical_revision53_behaviour"] == "UNKNOWN", "historical behaviour remains UNKNOWN")
require(data["historical_route"]["TCD018_admitted"] is False, "TCD-018 not admitted")
for key, value in data["hard_boundaries"].items():
    require(value is False, f"hard boundary must remain false: {key}")
require(EXPECTED_RESULT in report, "report contains exact result token")
require("25-row reconciliation artifact was found" not in report, "report must not claim missing evidence exists")
require("No claim of organizational or human independence is made" in report, "report independence boundary")

print("PASS_TCD018_INDEPENDENT_REVIEW_RECORD_VALIDATOR")
