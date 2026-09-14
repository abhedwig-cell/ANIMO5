#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"
EXPECTED = "QUALIFIED_TCD016_PARENT_NOT_READY_EXPLICIT_MODEL_EVOLUTION_DECISION_REQUIRED"
FROZEN_AUTHORING_HEAD = "568421dbad50a561261f28fb63b772451a518cdf"
FROZEN_AUTHORING_TREE = "8d4c8a38dd609c20ef264994623ecdd705246683"

def load(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))

required = [
    "B3B14_TCD016_PARENT_RECONSTRUCTION.json",
    "B3B14_AUTHORITY_EVIDENCE_MATRIX.json",
    "B3B14_UNRESOLVED_BLOCKER_CLASSIFICATION.json",
    "B3B14_CHILD_PARENT_COMPOSITION.json",
    "B3B14_MASS_STATE_RESTART_READINESS.json",
    "B3B14_TCD016_PARENT_READINESS_DECISION.json",
    "B3B14_GOV05_ADVERSARIAL_REVIEW.json",
    "ANIMO-B3B14_AUTHORING_FREEZE.json",
    "ANIMO-B3B14_STATUS.json",
]
for name in required:
    assert (B3 / name).is_file(), name

status = load("ANIMO-B3B14_STATUS.json")
decision = load("B3B14_TCD016_PARENT_READINESS_DECISION.json")
blockers = load("B3B14_UNRESOLVED_BLOCKER_CLASSIFICATION.json")
composition = load("B3B14_CHILD_PARENT_COMPOSITION.json")
state = load("B3B14_MASS_STATE_RESTART_READINESS.json")
auth = load("B3B14_AUTHORITY_EVIDENCE_MATRIX.json")
parent = load("B3B14_TCD016_PARENT_RECONSTRUCTION.json")
review = load("B3B14_GOV05_ADVERSARIAL_REVIEW.json")
freeze = load("ANIMO-B3B14_AUTHORING_FREEZE.json")

assert status["status"] == "QUALIFIED_CLOSURE_READINESS_COMPLETE"
assert status["primary_disposition"] == EXPECTED
assert decision["primary_disposition"] == EXPECTED
assert decision["readiness"] is False
assert decision["b3_admission_performed"] is False
assert decision["production_authorized"] is False
assert blockers["minimal_blocker_class"] == "EXPLICIT_MODEL_EVOLUTION_AUTHORIZATION_REQUIRED"
assert composition["parent_definition_narrowed"] is False
assert composition["parent_surface_gates"]["rewetting_boundary"].startswith("FAIL_")
assert parent["known_child_set_complete_for_readiness_review"] is True
assert parent["implicit_child_missing"] is False
assert auth["gov06_ownership"]["owned_contract"] == "TCD016_PARENT_READINESS_SYNTHESIS"
assert auth["gov06_ownership"]["parallelism"] == "PARALLEL_AFTER_PINNING"
assert state["typed_transfer_rules"]["mass_observer_can_reconstruct_physical_state"] is False
rewet = [r for r in state["matrix"] if r["operation"] == "continue_rewet"]
assert len(rewet) == 1 and rewet[0]["status"] == "ADMISSION_BLOCKING"
assert status["historical_behavior"] == "UNKNOWN_WITHOUT_B2"

assert freeze["authoring_head"] == FROZEN_AUTHORING_HEAD
assert freeze["authoring_tree"] == FROZEN_AUTHORING_TREE
assert freeze["scientific_semantics_mutated_after_previous_freeze"] is False
assert review["reviewed_authoring_head"] == FROZEN_AUTHORING_HEAD
assert review["reviewed_authoring_tree"] == FROZEN_AUTHORING_TREE
assert review["assurance_label"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
assert review["independent_from_correction_authoring"] is False
assert review["review_result"] == "SELF_REVIEW_PASS"
assert review["substantive_remediation_required"] is False
assert review["reviewed_primary_disposition"] == EXPECTED
assert review["pre_review_exact_head_ci"]["conclusion"] == "success"
assert review["state_mass_restart_review"]["continue_rewet"].startswith("FAIL_ADMISSION_BLOCKING")
assert review["historical_evidence_review"]["status"] == "UNKNOWN_WITHOUT_B2"
assert review["supersession_check"]["later_tcd016_science_authority_found"] is False

mandatory_review_checks = [
    "desire_to_close_b3_mistaken_for_evidence",
    "mass_closure_mistaken_for_physics",
    "negative_qualification_mistaken_for_failure",
    "negative_qualification_mistaken_for_positive_inertness",
    "unknown_historical_behavior_silently_ignored",
    "child_evidence_promoted_to_parent",
    "original_discrepancy_silently_narrowed",
    "state_representation_mistaken_for_process_definition",
    "noncommittal_identity_mistaken_for_NH4_speciation",
    "restart_sufficiency_assumed",
    "missing_process_law_auto_blocking",
    "missing_process_law_auto_nonblocking",
    "b3_readiness_confused_with_b3_admission",
    "same_agent_review_mislabeled_independent",
]
for key in mandatory_review_checks:
    assert review["mandatory_adversarial_checks"][key].startswith("PASS"), key

for k in ["b3_admission_performed","tcd_register_mutated","b3_queue_mutated","aggregate_mutated","routing_mutated","production_source_modified","b4_opened","tb7_opened","production_authorized"]:
    assert status[k] is False, k

fragment = json.loads((ROOT / "integration" / "animo-testbank" / "fragments" / "ANIMO-B3B14_TCD016_PARENT_READINESS_FRAGMENT.json").read_text(encoding="utf-8"))
assert fragment["opens_tb7"] is False
assert fragment["whole_model_golden_baseline"] is False
assert fragment["central_testbank_registry_mutated"] is False
assert fragment["readiness_oracle"]["expected_primary_disposition"] == EXPECTED

text = (ROOT / "docs" / "science" / "TCD016_PARENT_CLOSURE_READINESS_SYNTHESIS.md").read_text(encoding="utf-8")
for phrase in [
    "They are not sufficient for `continue` across rewetting",
    "not a physical inertness law",
    "UNKNOWN_WITHOUT_B2",
    EXPECTED,
    "No B3 admission is performed here",
]:
    assert phrase in text, phrase

# GOV05 allows administrative closeout after a passing review only if substantive
# reviewed files remain unchanged. Verify every post-freeze change is administrative.
changed = subprocess.check_output(
    ["git", "diff", "--name-only", f"{FROZEN_AUTHORING_HEAD}..HEAD"],
    cwd=ROOT,
    text=True,
).splitlines()
allowed_post_freeze = {
    "integration/animo-b3/ANIMO-B3B14_AUTHORING_FREEZE.json",
    "integration/animo-b3/B3B14_GOV05_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3B14_STATUS.json",
    "tools/validate_b3b14_tcd016_parent_readiness.py",
}
unexpected = sorted(set(changed) - allowed_post_freeze)
assert not unexpected, f"substantive post-freeze change(s): {unexpected}"

print("ANIMO-B3B14 parent readiness package + GOV05 review: PASS")
