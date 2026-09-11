#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

START = "744c42119ee8cd21de658ef6d9c0ecf4a3f7d2ca"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
B3B10 = "eccba6712f65455161d05fa9cdf6aa142f823dd4"
B3B10R = "36aad892cac546105dfec0fe43aa34a18e23bcad"
B3B10E1 = "8522752f9941e6fd5b421cf5ac4ef839384d7ce7"
B3B10R2 = "7648e7b2813f3abc5904e4c34e36072d81d9844f"
STATEQ03 = "10c50e65d1369d5f3b26736c4b12d3a482379eb5"
STATEQ04 = "ef9a5998cafae433deeba701a8e9a8a08eacc92f"
MP01 = "7b5979dd6301b9d55d23e8c22948a0dba24b229b"
MP02 = "6b0f2e7470f13baeb6612b0bddb662a497dea528"
MASSQ02 = "56a11b524d03c33ee4ab9b1cd13b2cd523d543fc"
EG01 = "a818b5a37b80ed92aded0b9c404990d356eb2300"

SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
DECISION = "ADMIT_TCD031_ATOMIC_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
FINAL_STATE = "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
GOV05_DECISION = "QUALIFIED_SINGLE_AGENT_ADVERSARIAL_REVIEW_GOVERNANCE_WITH_EXPLICITLY_REDUCED_INDEPENDENCE_ASSURANCE_NO_SCIENTIFIC_GATE_REDUCTION"
R2_PASS = "PASS_TARGETED_INDEPENDENT_REREVIEW_TCD031_SOURCE_PROVENANCE_GATES_CLOSED"
ATOMIC = "COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D23 FAIL_CLOSED: " + msg)


def local_json(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


def diff_names(base, head="HEAD"):
    out = subprocess.check_output(["git", "diff", "--name-only", base, head], text=True)
    return {line.strip() for line in out.splitlines() if line.strip()}


# Branch lineage must start from the exact qualified B3D22 head.
subprocess.check_call(["git", "merge-base", "--is-ancestor", START, "HEAD"])

candidate = local_json("TCD031_B3_ADMISSION_CANDIDATE.json")
status = local_json("ANIMO-B3D23_STATUS.json")
review_path = B3 / "ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json"
req(review_path.exists(), "GOV05 internal adversarial review artifact is missing")
review = json.loads(review_path.read_text(encoding="utf-8"))

# Formal-disposition authority and exact handoff.
disp = git_show_json(START, "integration/animo-b3/TCD031_TIER_C_FORMAL_DISPOSITION.json")
dstat = git_show_json(START, "integration/animo-b3/ANIMO-B3D22_STATUS.json")
req(disp["work_unit"] == "ANIMO-B3D22" and disp["target"] == "TCD-031", "wrong B3D22 authority")
req(disp["decision"] == "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION", "B3D22 decision drift")
req(disp["formal_disposition"] == DISPOSITION, "B3D22 formal disposition drift")
req(disp["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL", "B3D22 qualification class drift")
req(disp["gov04_risk_tier"] == "C", "B3D22 risk tier drift")
req(disp["next_allowed_workunit"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD031", "B3D22 does not hand off to a separate TCD-031 admission")
req(disp["atomic_scientific_disposition"]["identity"] == ATOMIC, "atomic scientific identity drift")
req(dstat["qualified"] is True and dstat["admitted"] is False, "B3D22 status is not qualified disposition-only")

# GOV05 must itself be qualified and preserve reduced independence assurance.
g5 = git_show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
req(g5["decision"] == GOV05_DECISION, "GOV05 decision drift")
req(g5["review_boundary"]["review_completed"] is True, "GOV05 review boundary incomplete")
req(g5["review_boundary"]["review_outcome"] == "SELF_REVIEW_PASS", "GOV05 did not SELF_REVIEW_PASS")
req(g5["assurance_change"]["to"] == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "GOV05 review model drift")
req(g5["assurance_change"]["independence_assurance_reduced"] is True, "GOV05 reduced-independence statement missing")
req(g5["assurance_change"]["scientific_gate_reduction"] is False, "GOV05 unexpectedly reduces scientific gates")

# Preserve and re-pin the historical genuinely independent R2 result without relabelling it.
r2 = git_show_json(B3B10R2, "integration/animo-b3/ANIMO-B3B10R2_STATUS.json")
req(r2["review_disposition"] == R2_PASS, "B3B10R2 PASS drift")
req(r2["independent_tier_c_review_gate"] == "PASSED", "B3B10R2 independent Tier-C gate drift")
req(r2["scientific_falsification"] is False, "B3B10R2 records scientific falsification")
req(r2["atomic_correction_identity"] == ATOMIC, "B3B10R2 atomic identity drift")
req(r2["ownership_result"] == "PASS_UNAMBIGUOUS_AT_REQUIRED_TCD031_SCOPE", "ownership result drift")
req(r2["native_RsCoMp_pre_promotion_answer"] == "NO_WITH_EXACT_PROOF", "RsCoMp pre-promotion result drift")
req(r2["persistent_state"] == {"domains": 2, "p_off_scalars": 8, "p_on_scalars": 12, "phosphorus_condition": "IPO.EQ.1"}, "persistent state contract drift")
req(r2["stateq04_reopen_required"] is False, "R2 unexpectedly requires STATEQ04 reopen")
req(r2["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "R2 whole-model evidence strength drift")
req(r2["production_restart_equivalence"] == "NOT_PROVEN", "R2 production restart evidence strength drift")

# The first failed review remains historical fact and is not rewritten.
r1 = git_show_json(B3B10R, "integration/animo-b3/ANIMO-B3B10R_STATUS.json")
req(r1["review_status"] == "COMPLETE_FAIL_CLOSED", "historical B3B10R fail-closed status was rewritten")
req(r1["review_disposition"] == "REMEDIATION_REQUIRED", "historical B3B10R disposition was rewritten")

# Candidate identity and authority pins.
req(candidate["work_unit"] == "ANIMO-B3D23" and candidate["target"] == "TCD-031", "wrong candidate identity")
req(candidate["exact_starting_head"] == START, "starting head drift")
req(candidate["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL", "candidate qualification class drift")
req(candidate["risk_tier"] == "C", "candidate risk tier drift")
req(candidate["formal_disposition"] == DISPOSITION, "candidate disposition drift")
req(candidate["candidate_decision"] == DECISION, "candidate decision drift")
req(candidate["candidate_result_after_review_and_exact_final_head_green"] == FINAL_STATE, "candidate target state drift")
req(candidate["candidate_is_effective_before_review"] is False, "candidate improperly claims pre-review effect")
req(candidate["current_review_governance"] == "GOV05_SINGLE_AGENT_ADVERSARIAL_REVIEW", "wrong current review governance")
req(candidate["same_agent_assurance"] == ASSURANCE, "same-agent assurance drift")

expected_authorities = {
    "aggregate": f"ANIMO-RG05H@{RG05H}",
    "GOV05": f"ANIMO-GOV05@{GOV05}",
    "GOV04_historical": f"ANIMO-GOV04@{GOV04}",
    "GOV03": f"ANIMO-GOV03@{GOV03}",
    "B3Q01": f"ANIMO-B3Q01@{B3Q01}",
    "routing": f"ANIMO-B3I07@{B3I07}",
    "formal_disposition": f"ANIMO-B3D22@{START}",
    "readiness": f"ANIMO-B3B10@{B3B10}",
    "first_fail_closed_review": f"ANIMO-B3B10R@{B3B10R}",
    "source_remediation": f"ANIMO-B3B10E1@{B3B10E1}",
    "historical_genuine_independent_rereview": f"ANIMO-B3B10R2@{B3B10R2}",
    "STATEQ03": f"ANIMO-STATEQ03@{STATEQ03}",
    "STATEQ04": f"ANIMO-STATEQ04@{STATEQ04}",
    "MP01": f"ANIMO-MP01@{MP01}",
    "MP02": f"ANIMO-MP02@{MP02}",
    "MASSQ02": f"ANIMO-MASSQ02@{MASSQ02}",
    "frozen_B0_retention": f"ANIMO-EG01@{EG01}",
}
req(candidate["authorities"] == expected_authorities, "authority pins changed")
req(candidate["exact_head_ci_prerequisites"]["B3D22"] == {"head": START, "run_id": 34546812652, "conclusion": "success"}, "B3D22 CI pin drift")
req(candidate["exact_head_ci_prerequisites"]["GOV05"] == {"head": GOV05, "run_id": 34546470484, "conclusion": "success"}, "GOV05 CI pin drift")
req(candidate["exact_head_ci_prerequisites"]["B3B10R2"] == {"head": B3B10R2, "run_id": 34545898592, "conclusion": "success"}, "B3B10R2 CI pin drift")
req(candidate["frozen_identity"] == {"source_archive_sha256": SOURCE_SHA, "testbank_archive_sha256": TESTBANK_SHA}, "frozen identity drift")

# Exact Class-C state/restart scope.
sc = candidate["admitted_scope_candidate"]
req(sc["atomic_identity"] == ATOMIC, "admitted atomic identity drift")
req(sc["domain_count"] == 2 and sc["p_off_scalar_count"] == 8 and sc["p_on_scalar_count"] == 12, "domain/scalar contract drift")
req(sc["phosphorus_condition"] == "IPO.EQ.1", "phosphorus condition drift")
req(sc["result_alias"] == "RsCoMp*", "result alias drift")
req(sc["native_promotion_direction"] == "CoMp* <- RsCoMp*", "native promotion direction drift")
req(sc["native_valid_RsCoMp_pre_promotion_restore_or_initialization"] is False, "native RsCoMp pre-promotion initialization overclaimed")
req(sc["serializer_only_is_sufficient"] is False and sc["restore_only_is_sufficient"] is False, "atomic writer/restore contract weakened")
req(sc["writer_and_restore_halves_are_one_atomic_correction"] is True, "atomic correction split")
req(sc["new_physical_state_introduced"] is False, "new physical state introduced")
req(len(sc["persistent_owner"]) == 6, "persistent-owner family count drift")
req(len(sc["required_checkpoint_semantics"]) == 5, "checkpoint semantic contract incomplete")

reuse = candidate["evidence_reuse"]
req(reuse["mode"] == "VERIFY_AND_REUSE_IMMUTABLE_PINS", "VERIFY_AND_REUSE mode missing")
for key in ("formal_disposition_reopened", "historical_independent_rereview_reopened", "stateq04_reopened", "source_provenance_replay_reopened", "evidence_strength_promoted", "superseding_or_contradictory_tcd031_evidence_found"):
    req(reuse[key] is False, f"reuse boundary violated: {key}")
req(reuse["historical_review_status_preserved"] is True, "historical independent review not preserved")

# GOV05 Tier-C authoring requirements must be explicitly present before review.
tierc = candidate["gov05_tier_c_authoring_contract"]
req(tierc["immutable_authoring_checkpoint_required"] is True, "immutable authoring checkpoint not required")
req(tierc["complete_source_and_persistent_state_ownership"] == "PINNED_PASS_B3B10R2", "ownership evidence missing")
req(tierc["first_read_first_write_or_restore_direction"] == "PINNED_PASS_B3B10R2", "restore-direction evidence missing")
req(len(tierc["counter_hypothesis"].strip()) > 40, "counter-hypothesis too weak or absent")
req(len(tierc["counter_hypothesis_test_basis"]) >= 4, "counter-hypothesis test basis incomplete")
req(len(tierc["active_controls"]) >= 1 and len(tierc["negative_controls"]) >= 3, "active/negative control contract incomplete")
req(tierc["split_run_or_restart_evidence"] == "STATEQ04_CLAIM_SCOPED_KERNEL_PASS", "restart evidence drift")
req(tierc["comparison_policy"] == "EXACT_BYTEWISE_NO_TOLERANCE", "comparison policy drift")
req(tierc["invented_tolerance"] is False, "invented tolerance allowed")
req(tierc["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "whole-model equivalence overclaimed")
req(tierc["production_restart_equivalence"] == "NOT_PROVEN", "production restart equivalence overclaimed")

hu = candidate["historical_uncertainty"]
req(hu["qualified_b2_available"] is False, "qualified B2 unexpectedly claimed")
req(hu["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty drift")
req(hu["historical_fidelity_claimed"] is False, "historical fidelity overclaimed")
req(hu["uncertainty_propagates_forward"] is True, "historical uncertainty not propagated")

ed = candidate["expected_difference_surface"]
req(ed["whole_model_equivalence_claimed"] is False, "whole-model equivalence claimed")
req(ed["production_restart_equivalence_claimed"] is False, "production restart equivalence claimed")
req(ed["global_arbitrary_tolerance_allowed"] is False, "global arbitrary tolerance allowed")
for item in (
    "continuous unsplit execution away from checkpoint and restore paths",
    "cold-start INITIAL.INP CoMp mapping",
    "two-domain physical meaning",
    "phosphorus applicability condition IPO.EQ.1",
    "external hydrology ownership and compatibility requirements",
    "current-interval workspace ownership",
    "numerical precision policy",
    "solver or tolerance policy",
    "frozen B0 identities",
):
    req(item in ed["must_not_change_semantics"], f"non-interference boundary missing: {item}")

# The same-agent review must review an immutable authoring head and must not call itself independent.
req(review["work_unit"] == "ANIMO-B3D23" and review["target"] == "TCD-031", "wrong review identity")
req(review["review_type"] == "SINGLE_AGENT_ADVERSARIAL_REVIEW", "wrong review type")
req(review["assurance"] == ASSURANCE, "review assurance drift")
req(review["genuinely_independent"] is False, "same-agent review falsely claims independence")
req(review["historical_independent_review_preserved"] == f"ANIMO-B3B10R2@{B3B10R2}", "historical independent review pin drift")
req(review["outcome"] == "SELF_REVIEW_PASS", "internal adversarial review did not PASS")
req(review["scientific_falsification"] is False, "review found scientific falsification")
req(review["superseding_or_contradictory_evidence_found"] is False, "review found superseding or contradictory evidence")
req(review["stateq04_reopen_required"] is False, "review requires STATEQ04 reopen")
req(review["reviewed_candidate_decision"] == DECISION, "reviewed candidate decision drift")
req(review["reviewed_atomic_identity"] == ATOMIC, "reviewed atomic identity drift")
req(len(review["counter_hypotheses_tested"]) >= 3, "adversarial counter-hypotheses incomplete")
req(len(review["active_controls_checked"]) >= 1 and len(review["negative_controls_checked"]) >= 3, "review control checks incomplete")
req(review["comparison_policy_checked"] == "EXACT_BYTEWISE_NO_TOLERANCE", "review comparison policy drift")
req(review["invented_tolerance_found"] is False, "review found invented tolerance")
req(review["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "review overclaims whole-model equivalence")
req(review["production_restart_equivalence"] == "NOT_PROVEN", "review overclaims production restart equivalence")
req(review["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "review overclaims historical behavior")
req(review["historical_fidelity_claimed"] is False, "review overclaims historical fidelity")
req(review["b3q01_independent_review_compatibility"]["independent_from_correction_authoring"] is False, "B3Q01 compatibility slot falsely claims independence")
req(review["b3q01_independent_review_compatibility"]["result"] == "PASS", "B3Q01 compatibility process gate did not PASS")
req(review["b3q01_independent_review_compatibility"]["interpretation"] == "GOV05_PROCESS_GATE_ONLY_NOT_EVIDENCE_OF_INDEPENDENCE", "compatibility slot interpretation drift")
for gate, value in review["gate_results"].items():
    req(value == "PASS", f"review gate not PASS: {gate}={value}")

reviewed_head = review["reviewed_authoring_head"]
req(isinstance(reviewed_head, str) and len(reviewed_head) == 40, "invalid reviewed authoring head")
subprocess.check_call(["git", "merge-base", "--is-ancestor", reviewed_head, "HEAD"])
subprocess.check_call(["git", "merge-base", "--is-ancestor", START, reviewed_head])

# Candidate and substantive authoring must be unchanged after the reviewed checkpoint.
reviewed_candidate = git_show_json(reviewed_head, "integration/animo-b3/TCD031_B3_ADMISSION_CANDIDATE.json")
req(reviewed_candidate == candidate, "candidate changed after reviewed immutable authoring head")
post_review_changes = diff_names(reviewed_head)
allowed_post_review = {
    "integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3D23_STATUS.json",
}
req(post_review_changes <= allowed_post_review, "substantive files changed after review: " + ", ".join(sorted(post_review_changes - allowed_post_review)))
req("integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json" in post_review_changes, "review artifact is not post-checkpoint")

# Final status is administrative closeout of the reviewed candidate only.
req(status["work_unit"] == "ANIMO-B3D23" and status["target"] == "TCD-031", "wrong final status identity")
req(status["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI", "final phase drift")
req(status["state"] == FINAL_STATE, "final state drift")
req(status["decision"] == DECISION, "final decision drift")
req(status["formal_disposition"] == DISPOSITION, "final status disposition drift")
req(status["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL", "final status class drift")
req(status["risk_tier"] == "C", "final status risk tier drift")
req(status["starting_authority"] == f"ANIMO-B3D22@{START}", "final starting authority drift")
req(status["governance_authority"] == f"ANIMO-GOV05@{GOV05}", "final GOV05 authority drift")
req(status["historical_independent_review_authority"] == f"ANIMO-B3B10R2@{B3B10R2}", "final historical review pin drift")
req(status["review_model"] == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "final review model drift")
req(status["review_assurance"] == ASSURANCE, "final review assurance drift")
req(status["review_boundary"]["complete_authoring_package_persisted"] is True, "authoring package not marked persisted")
req(status["review_boundary"]["immutable_authoring_head"] == reviewed_head, "status/review head mismatch")
req(status["review_boundary"]["review_completed"] is True and status["review_boundary"]["review_outcome"] == "SELF_REVIEW_PASS", "review closeout incomplete")
req(status["admitted"] is True and status["qualified"] is True, "final B3 admission not qualified")
req(status["production_authorized"] is False, "production improperly authorized")
req(status["stateq04_reopen_required"] is False, "STATEQ04 reopen unexpectedly required")
req(status["historical_boundary"]["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "final historical boundary drift")
for key, value in status["unproven_boundaries"].items():
    req(value == "NOT_PROVEN", f"unproven boundary promoted: {key}")
for key, value in status["hard_boundaries"].items():
    req(value is False, f"hard boundary violated: {key}")
req(status["validation"]["exact_final_head_ci_required"] is True, "exact final head CI not required")

# Frozen archive manifests in this branch must retain the pinned identities.
source_manifest = (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text(encoding="utf-8")
test_manifest = (ROOT / "reference/testcases/ANIMO_testbank.zip.sha256").read_text(encoding="utf-8")
req(SOURCE_SHA in source_manifest, "source archive manifest identity drift")
req(TESTBANK_SHA in test_manifest, "testbank manifest identity drift")

# TCD-025 is only a later consumer, never composed here.
req(candidate["tcd025_boundary"]["executed_here"] is False and candidate["tcd025_boundary"]["composition_here"] is False, "TCD-025 leaked into B3D23")

print("B3D23 PASS: TCD-031 GOV05 Tier-C atomic B3 admission package is internally consistent")
print("reviewed_authoring_head=" + reviewed_head)
print("assurance=" + ASSURANCE)
print("historical_B3B10R2 remains genuinely independent history; B3D23 same-agent review is not independent")
print("qualified state is effective only if this exact final HEAD workflow concludes success")
