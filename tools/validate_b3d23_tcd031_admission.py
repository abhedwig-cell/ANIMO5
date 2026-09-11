#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

B3D22 = "b68ebd807fbac2f8e8305417329e390fdab758d2"
HIST_START = "744c42119ee8cd21de658ef6d9c0ecf4a3f7d2ca"
OLD_FREEZE = "048855e7d0bbcb21b79b906b8c11ab09be98870a"
MERGE = "6fe7b43bbe209328b086058bfeefb907677aaa9b"
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
R2_PASS = "PASS_TARGETED_INDEPENDENT_REREVIEW_TCD031_SOURCE_PROVENANCE_GATES_CLOSED"
ATOMIC = "COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D23 FAIL_CLOSED: " + msg)


def jlocal(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


def jshow(ref, path):
    return json.loads(subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True))


def changed(base, head="HEAD"):
    out = subprocess.check_output(["git", "diff", "--name-only", base, head], text=True)
    return {x.strip() for x in out.splitlines() if x.strip()}


# Final disposition authority must be in lineage. Historical concurrent start remains history only.
subprocess.check_call(["git", "merge-base", "--is-ancestor", B3D22, "HEAD"])
subprocess.check_call(["git", "merge-base", "--is-ancestor", HIST_START, "HEAD"])
subprocess.check_call(["git", "merge-base", "--is-ancestor", MERGE, "HEAD"])

candidate = jlocal("TCD031_B3_ADMISSION_CANDIDATE.json")
status = jlocal("ANIMO-B3D23_STATUS.json")
recon = jlocal("ANIMO-B3D23_RECONCILIATION.json")
review_path = B3 / "ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json"
req(review_path.exists(), "internal adversarial review artifact missing")
review = json.loads(review_path.read_text(encoding="utf-8"))

# Non-destructive reconciliation must be explicit and must invalidate the old freeze for final review.
req(recon["work_unit"] == "ANIMO-B3D23" and recon["target"] == "TCD-031", "wrong reconciliation identity")
req(recon["original_branch_start"] == HIST_START, "historical start drift")
req(recon["original_authoring_freeze_head"] == OLD_FREEZE, "old freeze drift")
req(recon["final_formal_disposition_authority"] == f"ANIMO-B3D22@{B3D22}", "final B3D22 reconciliation pin drift")
req(recon["final_formal_disposition_exact_head_ci"] == "34547171960:success", "B3D22 final CI pin drift")
req(recon["reconciliation_merge_commit"] == MERGE, "reconciliation merge pin drift")
req(recon["reconciliation_method"] == "MERGE_PRESERVE_CONCURRENT_HISTORY_NO_FORCE_PUSH", "destructive reconciliation detected")
req(recon["original_checkpoint_rewritten"] is False and recon["historical_concurrent_authoring_preserved"] is True, "concurrent history not preserved")
req(recon["scientific_scope_changed_by_reconciliation"] is False and recon["admission_decision_changed_by_reconciliation"] is False, "reconciliation changed science or decision")
req(recon["review_reset"]["required"] is True and recon["review_reset"]["old_freeze_may_be_used_for_final_review"] is False, "old review freeze not invalidated")
req(recon["review_reset"]["new_immutable_authoring_head_required"] is True, "new authoring freeze not required")
for k, v in recon["hard_boundaries"].items(): req(v is False, f"reconciliation hard boundary violated: {k}")

# Final B3D22 must be qualified, disposition-only, and scientifically identical to the candidate.
disp = jshow(B3D22, "integration/animo-b3/TCD031_TIER_C_FORMAL_DISPOSITION.json")
dstat = jshow(B3D22, "integration/animo-b3/ANIMO-B3D22_STATUS.json")
req(disp["decision"] == "QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION", "B3D22 decision drift")
req(disp["formal_disposition"] == DISPOSITION, "B3D22 disposition drift")
req(disp["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL", "B3D22 class drift")
req(disp["gov04_risk_tier_retained_by_gov05"] == "C", "B3D22 Tier-C drift")
req(disp["atomic_scientific_disposition"]["identity"] == ATOMIC, "B3D22 atomic identity drift")
req(disp["atomic_scientific_disposition"]["domain_count"] == 2, "B3D22 domain count drift")
req(disp["atomic_scientific_disposition"]["p_off_scalar_count"] == 8 and disp["atomic_scientific_disposition"]["p_on_scalar_count"] == 12, "B3D22 state count drift")
req(disp["next_allowed_workunit"] == "SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD031", "B3D22 handoff drift")
req(dstat["qualified"] is True and dstat["admitted"] is False and dstat["production_authorized"] is False, "B3D22 is not qualified disposition-only")

# GOV05 is current. Same-agent review is not independent; completed R2 remains valid historical GOV04 assurance.
g5 = jshow(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
g5m = jshow(GOV05, "integration/animo-governance/GOV05_REVIEW_ASSURANCE_MATRIX.json")
req(g5["work_status"]["qualified"] is True and g5["work_status"]["work_unit_complete"] is True, "GOV05 not qualified")
req(g5["assurance_change"]["to"] == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "GOV05 review model drift")
req(g5["assurance_change"]["independence_assurance_reduced"] is True, "GOV05 reduced-assurance boundary missing")
req(g5["assurance_change"]["scientific_gate_reduction"] is False, "GOV05 scientific gate reduction detected")
req(g5m["governance_semantics"]["same_agent_review_is_independent"] is False, "GOV05 falsely permits same-agent independence")
req(g5m["transition"]["completed_independent_reviews_remain_valid"] is True, "GOV05 no longer preserves completed R2")

# Historical R2 and original fail-closed review stay pinned and unchanged.
r2 = jshow(B3B10R2, "integration/animo-b3/ANIMO-B3B10R2_STATUS.json")
req(r2["review_disposition"] == R2_PASS and r2["independent_tier_c_review_gate"] == "PASSED", "R2 PASS drift")
req(r2["atomic_correction_identity"] == ATOMIC, "R2 atomic identity drift")
req(r2["native_RsCoMp_pre_promotion_answer"] == "NO_WITH_EXACT_PROOF", "R2 RsCoMp result drift")
req(r2["ownership_result"] == "PASS_UNAMBIGUOUS_AT_REQUIRED_TCD031_SCOPE", "R2 ownership drift")
req(r2["persistent_state"] == {"domains": 2, "p_off_scalars": 8, "p_on_scalars": 12, "phosphorus_condition": "IPO.EQ.1"}, "R2 persistent-state drift")
req(r2["whole_model_active_production_split_equivalence"] == "NOT_PROVEN" and r2["production_restart_equivalence"] == "NOT_PROVEN", "R2 evidence boundary promoted")
req(r2["historical_b2"] == "ABSENT" and r2["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN", "R2 historical boundary drift")
r1 = jshow(B3B10R, "integration/animo-b3/ANIMO-B3B10R_STATUS.json")
req(r1["review_status"] == "COMPLETE_FAIL_CLOSED" and r1["review_disposition"] == "REMEDIATION_REQUIRED", "historical B3B10R rewritten")

# Candidate must pin the final B3D22, not the historical concurrent start.
req(candidate["work_unit"] == "ANIMO-B3D23" and candidate["target"] == "TCD-031", "wrong candidate identity")
req(candidate["historical_branch_start"] == HIST_START, "candidate historical start drift")
req(candidate["effective_formal_disposition_authority"] == f"ANIMO-B3D22@{B3D22}", "candidate effective B3D22 drift")
req(candidate["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL" and candidate["risk_tier"] == "C", "candidate class/tier drift")
req(candidate["formal_disposition"] == DISPOSITION and candidate["candidate_decision"] == DECISION, "candidate disposition/decision drift")
req(candidate["candidate_result_after_review_and_exact_final_head_green"] == FINAL_STATE, "candidate final-state drift")
req(candidate["candidate_is_effective_before_review"] is False, "candidate claims pre-review admission")
req(candidate["same_agent_assurance"] == ASSURANCE, "candidate assurance drift")
req(candidate["authorities"]["formal_disposition"] == f"ANIMO-B3D22@{B3D22}", "candidate formal-disposition authority drift")
req(candidate["exact_head_ci_prerequisites"]["B3D22"] == {"head": B3D22, "run_id": 34547171960, "conclusion": "success"}, "candidate B3D22 CI prerequisite drift")
req(candidate["exact_head_ci_prerequisites"]["GOV05"] == {"head": GOV05, "run_id": 34546470484, "conclusion": "success"}, "candidate GOV05 CI prerequisite drift")
req(candidate["exact_head_ci_prerequisites"]["B3B10R2"] == {"head": B3B10R2, "run_id": 34545898592, "conclusion": "success"}, "candidate R2 CI prerequisite drift")
req(candidate["frozen_identity"] == {"source_archive_sha256": SOURCE_SHA, "testbank_archive_sha256": TESTBANK_SHA}, "frozen identity drift")
req(candidate["reconciliation"]["new_immutable_authoring_head_required_after_reconciliation"] is True, "candidate does not require review reset")

sc = candidate["admitted_scope_candidate"]
req(sc["atomic_identity"] == ATOMIC and sc["domain_count"] == 2, "candidate atomic/domain drift")
req(sc["p_off_scalar_count"] == 8 and sc["p_on_scalar_count"] == 12 and sc["phosphorus_condition"] == "IPO.EQ.1", "candidate state/P contract drift")
req(sc["result_alias"] == "RsCoMp*" and sc["native_promotion_direction"] == "CoMp* <- RsCoMp*", "candidate alias/promotion drift")
req(sc["native_valid_RsCoMp_pre_promotion_restore_or_initialization"] is False, "candidate native RsCoMp initialization overclaimed")
req(sc["serializer_only_is_sufficient"] is False and sc["restore_only_is_sufficient"] is False, "half-correction accepted")
req(sc["writer_and_restore_halves_are_one_atomic_correction"] is True and sc["new_physical_state_introduced"] is False, "atomicity/state boundary drift")

reuse = candidate["evidence_reuse"]
req(reuse["mode"] == "VERIFY_AND_REUSE_IMMUTABLE_PINS", "reuse mode drift")
for k in ("formal_disposition_reopened", "historical_independent_rereview_reopened", "stateq04_reopened", "source_provenance_replay_reopened", "evidence_strength_promoted", "superseding_or_contradictory_tcd031_evidence_found"):
    req(reuse[k] is False, f"reuse boundary violated: {k}")
req(reuse["historical_review_status_preserved"] is True, "historical R2 status not preserved")

tierc = candidate["gov05_tier_c_authoring_contract"]
req(tierc["immutable_authoring_checkpoint_required"] is True, "immutable review checkpoint not required")
req(tierc["complete_source_and_persistent_state_ownership"] == "PINNED_PASS_B3B10R2", "ownership evidence drift")
req(tierc["first_read_first_write_or_restore_direction"] == "PINNED_PASS_B3B10R2", "lifecycle evidence drift")
req(len(tierc["counter_hypothesis"].strip()) > 40 and len(tierc["counter_hypothesis_test_basis"]) >= 4, "counter-hypothesis contract incomplete")
req(len(tierc["active_controls"]) >= 1 and len(tierc["negative_controls"]) >= 3, "control contract incomplete")
req(tierc["comparison_policy"] == "EXACT_BYTEWISE_NO_TOLERANCE" and tierc["invented_tolerance"] is False, "comparison/tolerance policy drift")
req(tierc["whole_model_active_production_split_equivalence"] == "NOT_PROVEN" and tierc["production_restart_equivalence"] == "NOT_PROVEN", "production boundary overclaimed")

hu = candidate["historical_uncertainty"]
req(hu["qualified_b2_available"] is False and hu["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty overclaimed")
req(hu["historical_fidelity_claimed"] is False, "historical fidelity claimed")
for k, v in candidate["hard_boundaries"].items(): req(v is False, f"candidate hard boundary violated: {k}")
req(candidate["tcd025_boundary"]["executed_here"] is False and candidate["tcd025_boundary"]["composition_here"] is False, "TCD-025 leaked into admission")

# Final same-agent review must cover the new reconciled immutable head, not the old 048855 head.
req(review["work_unit"] == "ANIMO-B3D23" and review["target"] == "TCD-031", "wrong review identity")
req(review["review_type"] == "SINGLE_AGENT_ADVERSARIAL_REVIEW", "wrong review type")
req(review["assurance"] == ASSURANCE and review["genuinely_independent"] is False, "review assurance falsely independent")
req(review["historical_independent_review_preserved"] == f"ANIMO-B3B10R2@{B3B10R2}", "historical R2 pin drift in review")
req(review["outcome"] == "SELF_REVIEW_PASS", "new internal adversarial review did not PASS")
req(review["scientific_falsification"] is False and review["superseding_or_contradictory_evidence_found"] is False, "review found falsification/contradiction")
req(review["stateq04_reopen_required"] is False, "review requires STATEQ04 reopen")
req(review["reviewed_candidate_decision"] == DECISION and review["reviewed_atomic_identity"] == ATOMIC, "reviewed decision/atomic identity drift")
req(len(review["counter_hypotheses_tested"]) >= 4, "adversarial counter-hypotheses incomplete")
req(len(review["active_controls_checked"]) >= 1 and len(review["negative_controls_checked"]) >= 3, "review controls incomplete")
req(review["comparison_policy_checked"] == "EXACT_BYTEWISE_NO_TOLERANCE" and review["invented_tolerance_found"] is False, "review comparison/tolerance drift")
req(review["whole_model_active_production_split_equivalence"] == "NOT_PROVEN" and review["production_restart_equivalence"] == "NOT_PROVEN", "review overclaims production equivalence")
req(review["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2" and review["historical_fidelity_claimed"] is False, "review historical overclaim")
compat = review["b3q01_independent_review_compatibility"]
req(compat["independent_from_correction_authoring"] is False and compat["result"] == "PASS", "compatibility gate falsely independent or not PASS")
req(compat["interpretation"] == "GOV05_PROCESS_GATE_ONLY_NOT_EVIDENCE_OF_INDEPENDENCE", "compatibility interpretation drift")
for k, v in review["gate_results"].items(): req(v == "PASS", f"review gate not PASS: {k}={v}")

reviewed_head = review["reviewed_authoring_head"]
req(isinstance(reviewed_head, str) and len(reviewed_head) == 40, "invalid reviewed authoring head")
req(reviewed_head != OLD_FREEZE, "superseded pre-reconciliation authoring head reused")
subprocess.check_call(["git", "merge-base", "--is-ancestor", B3D22, reviewed_head])
subprocess.check_call(["git", "merge-base", "--is-ancestor", reviewed_head, "HEAD"])
reviewed_candidate = jshow(reviewed_head, "integration/animo-b3/TCD031_B3_ADMISSION_CANDIDATE.json")
req(reviewed_candidate == candidate, "candidate changed after reviewed reconciled authoring head")
post = changed(reviewed_head)
allowed_post = {"integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-b3/ANIMO-B3D23_STATUS.json"}
req(post <= allowed_post, "substantive files changed after review head: " + ", ".join(sorted(post - allowed_post)))
req("integration/animo-b3/ANIMO-B3D23_INTERNAL_ADVERSARIAL_REVIEW.json" in post, "new review artifact is not post-freeze")

# Administrative closeout only after review PASS.
req(status["work_unit"] == "ANIMO-B3D23" and status["target"] == "TCD-031", "wrong status identity")
req(status["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI", "final phase drift")
req(status["state"] == FINAL_STATE and status["decision"] == DECISION, "final admission state/decision drift")
req(status["formal_disposition"] == DISPOSITION and status["qualification_class"] == "C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL" and status["risk_tier"] == "C", "final disposition/class/tier drift")
req(status["effective_formal_disposition_authority"] == f"ANIMO-B3D22@{B3D22}", "final B3D22 authority drift")
req(status["governance_authority"] == f"ANIMO-GOV05@{GOV05}", "final GOV05 authority drift")
req(status["historical_independent_review_authority"] == f"ANIMO-B3B10R2@{B3B10R2}", "final R2 pin drift")
req(status["review_model"] == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" and status["review_assurance"] == ASSURANCE, "final review assurance drift")
rb = status["review_boundary"]
req(rb["complete_reconciled_authoring_package_persisted"] is True and rb["immutable_authoring_head"] == reviewed_head, "final review-head binding incomplete")
req(rb["review_completed"] is True and rb["review_outcome"] == "SELF_REVIEW_PASS", "final review closeout incomplete")
req(status["admitted"] is True and status["qualified"] is True and status["production_authorized"] is False, "admission qualification/production boundary drift")
req(status["stateq04_reopen_required"] is False, "final status requires STATEQ04 reopen")
req(status["historical_boundary"]["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN_WITHOUT_B2", "final historical boundary drift")
for k, v in status["unproven_boundaries"].items(): req(v == "NOT_PROVEN", f"unproven boundary promoted: {k}")
for k, v in status["hard_boundaries"].items(): req(v is False, f"status hard boundary violated: {k}")
req(status["validation"]["exact_final_head_ci_required"] is True, "exact final-head CI not required")

# Frozen identity manifests remain unchanged.
req(SOURCE_SHA in (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text(), "source identity manifest drift")
req(TESTBANK_SHA in (ROOT / "reference/testcases/ANIMO_testbank.zip.sha256").read_text(), "testbank identity manifest drift")

print("B3D23 PASS: reconciled TCD-031 Tier-C atomic B3 admission is review-bound, historically uncertainty-bounded, and not production authorization")
print("reviewed_authoring_head=" + reviewed_head)
print("same-agent GOV05 review is not independent; historical B3B10R2 remains genuinely independent GOV04 evidence")
