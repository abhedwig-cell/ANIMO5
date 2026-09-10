#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

BASE = "ef9a5998cafae433deeba701a8e9a8a08eacc92f"
ALLOWED = {
    "docs/b3/ANIMO_B3B10_TCD031_TIER_C_READINESS.md",
    "integration/animo-b3/TCD031_TIER_C_READINESS_EVIDENCE.json",
    "integration/animo-b3/TCD031_INDEPENDENT_REVIEW_HANDOFF.json",
    "integration/animo-b3/ANIMO-B3B10_STATUS.json",
    "tools/b3b10/validate_b3b10.py",
    ".github/workflows/animo-b3b10-tcd031.yml",
}


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


status = load("integration/animo-b3/ANIMO-B3B10_STATUS.json")
evidence = load("integration/animo-b3/TCD031_TIER_C_READINESS_EVIDENCE.json")
handoff = load("integration/animo-b3/TCD031_INDEPENDENT_REVIEW_HANDOFF.json")
doc = Path("docs/b3/ANIMO_B3B10_TCD031_TIER_C_READINESS.md").read_text(encoding="utf-8")

require(status["work_unit"] == "ANIMO-B3B10", "wrong work unit")
require(status["target"] == "TCD-031", "wrong target")
require(status["gov04_risk_tier"] == "C", "TCD-031 must remain Tier C")
require(status["b3_qualification_class"].startswith("C_"), "TCD-031 must remain Class C")
require(status["b3_admitted"] is False, "readiness must not admit B3")
require(status["production_authorized"] is False, "readiness must not authorize production")
require(status["independent_review"]["required"] is True, "independent review must be required")
require(status["independent_review"]["authoring_context_may_sign_gate"] is False, "authoring context cannot sign Tier-C review")
require(status["hard_boundaries"]["new_tolerance"] is False, "no tolerance may be invented")
require(status["hard_boundaries"]["tcd025_composed"] is False, "TCD-025 composition forbidden")

require(evidence["persistent_owner"]["domains"] == 2, "expected two macropore domains")
require(evidence["persistent_owner"]["p_off_scalars"] == 8, "expected 8 P-off persistent scalars")
require(evidence["persistent_owner"]["p_on_scalars"] == 12, "expected 12 P-on persistent scalars")
require(evidence["persistent_owner"]["globally_deterministic_reconstruction"] is False, "must not reconstruct missing persistent state")
require(evidence["stateq04_candidate_evidence"]["candidate_restore_all_species_exact"] is True, "candidate restore discriminator missing")
require(evidence["stateq04_candidate_evidence"]["native_bad_alias_control_all_species_diverge"] is True, "native-bad control missing")
require(evidence["stateq04_candidate_evidence"]["domain_drop_control_all_species_diverge"] is True, "domain-drop control missing")
require(evidence["stateq04_candidate_evidence"]["comparison_policy"] == "EXACT_BYTEWISE_NO_TOLERANCE", "comparison policy drift")
require(evidence["historical_uncertainty"]["trusted_active_B2_restart_reference"] is False, "must not fabricate B2")
require(evidence["decision"] == "QUALIFIED_CLASS_C_ADMISSION_READINESS_GOV04_TIER_C_INDEPENDENT_REVIEW_REQUIRED", "unexpected readiness decision")

require(handoff["review_kind"] == "GOV04_TIER_C_GENUINELY_INDEPENDENT_SECOND_LINE", "wrong review kind")
require(handoff["authoring_context_may_sign_gate"] is False, "handoff must preserve independence")
require("review/animo-b3b10r-tcd031-independent-second-line" == handoff["review_branch"], "unexpected review branch")

for marker in [
    "QUALIFIED_CLASS_C_ADMISSION_READINESS_GOV04_TIER_C_INDEPENDENT_REVIEW_REQUIRED",
    "Historical revision-53 behaviour without a trusted active B2 restart reference remains `UNKNOWN`",
    "The authoring context may not sign the Tier-C review gate.",
    "no TCD-025 composition",
]:
    require(marker in doc, f"documentation marker missing: {marker}")

changed = subprocess.run(
    ["git", "diff", "--name-only", f"{BASE}..HEAD"],
    check=True,
    text=True,
    stdout=subprocess.PIPE,
).stdout.splitlines()
unexpected = sorted(set(changed) - ALLOWED)
require(not unexpected, f"scope guard failed, unexpected changed files: {unexpected}")

print("PASS_B3B10_TCD031_TIER_C_READINESS")
print("PASS_B3B10_SCOPE_GUARD")
