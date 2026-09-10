#!/usr/bin/env python3
"""Fail-closed semantic validator for ANIMO-B3B09R TCD-038 second-line review."""

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "integration/animo-b3/TCD038_INDEPENDENT_SECOND_LINE_REVIEW.json"
HUMAN_PATH = ROOT / "docs/b3/TCD038_INDEPENDENT_SECOND_LINE_REVIEW.md"
REGISTER_PATH = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
B0_HASH_PATH = ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256"

EXPECTED_START = "1b47d6b2e422463b557a48355ad8b4f5bed70ebc"
EXPECTED_AGGREGATE = "ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
PREP12_SHA = "3d86de057247adcfeefb82c11d7cf7d5b2cbdf73"
PREP12_EVIDENCE_PATH = "integration/animo-prep12/source/PREP10_PLANT_UPTAKE_RESTART_CONTINUITY.json"
EXPECTED_SOURCE_HASH = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_TESTBANK_HASH = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - fail-closed diagnostic
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")


def git_show_json(commit: str, path: str):
    """Read a pinned authority directly from repository history, not from review-tree copies."""
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"cannot read pinned authority {commit}:{path}: {proc.stderr.strip()}")
    try:
        return json.loads(proc.stdout)
    except Exception as exc:  # pragma: no cover
        fail(f"cannot parse pinned authority {commit}:{path}: {exc}")


review = load_json(REVIEW_PATH)

require(review.get("work_unit") == "ANIMO-B3B09R", "wrong work_unit")
require(review.get("branch") == "review/animo-b3b09r-tcd038-independent-second-line", "wrong review branch")
require(review.get("review_type") == "GOV04_TIER_C_INDEPENDENT_SECOND_LINE", "wrong review type")

ind = review.get("independence", {})
require(ind.get("separate_review_context") is True, "independent review context not recorded")
require(ind.get("independence_strength") == "PROCESS_INDEPENDENCE_ONLY", "independence strength overclaimed or missing")
require(ind.get("human_or_organizational_independence_claimed") is False, "human/organizational independence must not be claimed")

pre = review.get("live_prewrite_recheck", {})
require(pre.get("starting_head_expected") == EXPECTED_START, "unexpected starting-head pin")
require(pre.get("starting_head_observed") == EXPECTED_START, "review did not start from exact B3B09 handoff")
require(pre.get("starting_head_match") is True, "starting head mismatch")
require(pre.get("issue_47_comments_at_recheck") == 0, "pre-write issue comment count changed from recorded observation")
require(pre.get("later_dedicated_tcd038_branch_or_issue_found") is False, "later TCD-038 work requires review re-evaluation")
require(pre.get("current_aggregate_authority") == EXPECTED_AGGREGATE, "aggregate authority pin differs from reviewed authority")

ready = review.get("readiness_validation", {})
require(ready.get("run_id") == 34524511092, "readiness run id mismatch")
require(ready.get("job_id") == 103029989632, "readiness job id mismatch")
require(ready.get("head") == EXPECTED_START, "readiness run not bound to exact handoff head")
require(ready.get("conclusion") == "success", "readiness run was not successful")
require(ready.get("used_as") == "READINESS_PACKAGE_INTEGRITY_ONLY_NOT_SECOND_LINE_CONCLUSION", "readiness evidence strength promoted")

b0 = review.get("frozen_b0", {})
require(b0.get("source_archive_sha256") == EXPECTED_SOURCE_HASH, "frozen source hash mismatch")
require(b0.get("testbank_sha256") == EXPECTED_TESTBANK_HASH, "frozen testbank hash mismatch")
require(b0.get("modified_by_review") is False, "review claims frozen B0 modification")
require(B0_HASH_PATH.read_text(encoding="utf-8").strip().startswith(EXPECTED_SOURCE_HASH), "repository B0 source hash no longer matches review pin")

canonical = review.get("canonical_target", {})
require(canonical.get("id") == "TCD-038", "wrong canonical target")
require(canonical.get("status") == "OPEN", "TCD-038 source register status was not reviewed as OPEN")
require(canonical.get("separate_neighbor") == "TCD-039", "TCD-039 separation missing")
require(canonical.get("tcd039_composed") is False, "TCD-039 composition is forbidden")

findings = review.get("independent_findings", {})
required_findings = {
    "lifecycle_ownership",
    "restore_direction",
    "legacy_erase_mechanism",
    "risk_tier",
    "cold_start_restart_semantics",
    "guards_preserved",
    "tcd039_exclusion",
    "state_evidence_strength",
    "expected_differences",
    "non_interference",
    "superseding_or_contradictory_evidence",
}
require(required_findings.issubset(findings), "one or more mandatory independent findings are absent")
for name in sorted(required_findings):
    require(findings[name].get("result") == "PASS", f"mandatory finding {name} is not PASS")

life = findings["lifecycle_ownership"]
require(life.get("independent_owner_count") == 1, "lifecycle ownership is not singular")
require("Amplni_act" in life.get("accepted_aliases", []), "Amplni_act accepted alias missing")
require("Rsamplni_act" in life.get("result_serialized_aliases", []), "Rsamplni_act result/serialized alias missing")

restore = findings["restore_direction"]
require(restore.get("direction") == "Rsampl*_act -> Ampl*_act", "restore direction changed or ambiguous")

erase = findings["legacy_erase_mechanism"]
require(erase.get("natural_nonzero_cases", 0) >= 4, "natural reachability evidence weakened")
require(erase.get("post_Inicalc_actual_uptake_erased_to_zero") is True, "legacy erase mechanism not established")
require(erase.get("evidence_strength") == "B1_SOURCE_BOUND_DIAGNOSTIC_NOT_B2", "legacy diagnostic evidence promoted beyond B1")

risk = findings["risk_tier"]
require(risk.get("b3_qualification_class") == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "B3 qualification class changed")
require(risk.get("gov04_risk_tier") == "C", "GOV04 risk tier must be C")
require(risk.get("strictest_trigger_wins") is True, "strictest-trigger-wins not applied")
required_tier_c_triggers = {
    "RESTART_OR_COLD_START_DISCRIMINATION",
    "INITIALIZATION_SEMANTICS",
    "CHECKPOINT_SEMANTICS",
}
require(required_tier_c_triggers.issubset(set(risk.get("tier_c_triggers", []))), "required Tier-C triggers missing")

sem = findings["cold_start_restart_semantics"]
require(sem.get("shared_surface") == ">orgpla:", "wrong initialization/restart surface")
require(sem.get("dedicated_discriminator") is False, "unexpected restart discriminator claimed")
require(sem.get("representation_change") is False, "checkpoint representation change is outside TCD-038")
require(sem.get("restore_semantics_change") is True, "restore-semantic effect not recorded")

guards = findings["guards_preserved"]
require(guards.get("threshold") == "1.0d-4", "small-value threshold changed")
require(guards.get("crop_trigger") == "Kicr(1).Ne.6 .Or. (Kicr(1).Eq.6 .And. Ioptcu.Eq.1)", "crop trigger changed")
require(guards.get("p_guard") == "Ipo.Eq.1", "P guard changed")
require(guards.get("guard_widening") is False, "guard widening is outside atomic scope")

t39 = findings["tcd039_exclusion"]
require(t39.get("potential_uptake_state_added") is False, "potential-uptake state added")
require(t39.get("checkpoint_fields_added") is False, "checkpoint fields added")
require(t39.get("composition_required") is False, "TCD-039 composition required")

state = findings["state_evidence_strength"]
require(state.get("STATEQ01") == "ROUTE_AND_STATE_CONTEXT_ONLY_NOT_TCD038_CAUSAL_SPLIT_RUN_PROOF", "STATEQ01 evidence promoted")
require(state.get("STATEQ02") == "RESTRICTED_CORE_EXACT_SPLIT_RUN_WITH_EXTERNAL_CROP_SURFACE_AND_UNRESOLVED_INTERNAL_CROP_RESTART_STATE_EXCLUDED", "STATEQ02 evidence boundary changed")
require(state.get("STATEQ02_later_closeout_effect") == "NO_STRENGTH_PROMOTION_FOR_TCD038", "later STATEQ02 closeout improperly promoted")
require(state.get("whole_trajectory_equivalence_claimed") is False, "whole-trajectory equivalence must remain unclaimed")

expected = findings["expected_differences"]
require(expected.get("qualified_full_horizon_magnitude") is False, "full-horizon magnitude overclaimed")
require(expected.get("new_tolerance_defined") is False, "review must define no tolerance")

ni = findings["non_interference"]
for key in (
    "production_source_modified",
    "frozen_b0_modified",
    "canonical_state_admitted",
    "canonical_tcd_register_modified",
    "aggregate_modified",
    "b4_or_production_opened",
    "numerical_policy_changed",
    "solver_changed",
    "tolerance_changed",
    "checkpoint_representation_changed",
):
    require(ni.get(key) is False, f"non-interference invariant failed: {key}")

new = findings["superseding_or_contradictory_evidence"]
require(new.get("material_contradiction_found") is False, "material contradictory evidence recorded")
require(new.get("later_tcd038_work_found") is False, "later TCD-038 work recorded")
require(new.get("later_routing_changes_claim") is False, "later routing changes reviewed claim")

strength = review.get("evidence_strength_bounds", {})
require(strength.get("PREP10") == "DIAGNOSTIC_NOT_REFERENCE_PLUS_SOURCE_BOUND", "PREP10 strength promoted")
require(strength.get("PREP12") == "PROVENANCE_PRESERVING_REHOME_ONLY_NO_NEW_SCIENTIFIC_STRENGTH", "PREP12 strength promoted")
require(strength.get("historical_revision_53_behavior") == "UNKNOWN_WITHOUT_B2", "historical behavior must remain UNKNOWN_WITHOUT_B2")
require(strength.get("qualified_B2_found_for_TCD038") is False, "unexpected qualified B2 claimed")
require(strength.get("gnu_diagnostic_treated_as_historical_B2") is False, "GNU diagnostic evidence treated as historical B2")

# Verify the primary rehomed PREP10 evidence at the exact PREP12 authority. The
# review tree need not duplicate that artifact; checkout fetch-depth 0 makes the
# pinned authority directly auditable through git history.
prep = git_show_json(PREP12_SHA, PREP12_EVIDENCE_PATH)
require(review.get("authorities", {}).get("PREP12") == PREP12_SHA, "review PREP12 pin differs from validator authority")
require(prep.get("evidence_class") == "DIAGNOSTIC_NOT_REFERENCE_PLUS_SOURCE_BOUND", "PREP10/PREP12 source evidence class changed")
require(prep.get("source_archive_sha256") == EXPECTED_SOURCE_HASH, "PREP10 source hash mismatch")
require(prep.get("testbank_sha256") == EXPECTED_TESTBANK_HASH, "PREP10 testbank hash mismatch")
require(prep.get("reference_qualified") is False, "PREP10 diagnostic evidence is not reference-qualified")
require(prep.get("production_migration_admitted") is False, "PREP10 must not admit production migration")
t33 = prep.get("TCD_033", {})
require(t33.get("classification") == "CONFIRMED_LEGACY_PLANT_ACTUAL_UPTAKE_RESTART_INITIALIZATION_DIRECTION_DEFECT", "PREP10 actual-uptake defect classification changed")
cases = t33.get("natural_case_replication", [])
require(len(cases) >= 4, "fewer than four natural TCD-038 witnesses")
for case in cases:
    require(case.get("initial_Rsamplni_act_kg_m2_N", 0.0) > 0.0, "natural N witness is not nonzero")
    require(case.get("post_Inicalc_Amplni_act") == 0.0, "natural N witness no longer demonstrates immediate erase")
require(prep.get("TCD_034", {}).get("production_correction_admitted") is False, "neighboring potential-uptake correction unexpectedly admitted")

# Verify TCD-038 and TCD-039 remain separate rows in the canonical discrepancy register.
with REGISTER_PATH.open(newline="", encoding="utf-8") as handle:
    rows = {row["ID"]: row for row in csv.DictReader(handle)}
require("TCD-038" in rows, "TCD-038 missing from canonical discrepancy register")
require("TCD-039" in rows, "TCD-039 missing from canonical discrepancy register")
require(rows["TCD-038"]["process"] == "crop actual uptake restart initialization", "canonical TCD-038 process changed")
require(rows["TCD-038"]["status"] == "OPEN", "canonical TCD-038 must remain OPEN after review")
require(rows["TCD-039"]["process"] == "crop potential uptake restart continuation", "TCD-039 identity changed")

human = HUMAN_PATH.read_text(encoding="utf-8")
for token in (
    "Decision: `PASS`",
    "UNKNOWN_WITHOUT_B2",
    "TCD-039 is fully excluded",
    "PASS_INDEPENDENT_REVIEW_EVIDENCE_ONLY_NO_B3_ADMISSION",
):
    require(token in human, f"human-readable evidence missing required boundary: {token}")

decision = review.get("decision", {})
require(decision.get("outcome") == "PASS", "machine-readable review outcome is not PASS")
require(decision.get("meaning") == "INDEPENDENT_REVIEW_EVIDENCE_ONLY_NO_B3_ADMISSION", "PASS meaning widened")
require(decision.get("tier") == "GOV04_TIER_C", "review decision tier changed")
for key in ("admission_performed", "production_authorized", "composition_authorized", "central_integration_authorized"):
    require(decision.get(key) is False, f"review improperly authorizes {key}")

print("PASS: ANIMO-B3B09R TCD-038 independent Tier-C review evidence is internally consistent and fail-closed.")
