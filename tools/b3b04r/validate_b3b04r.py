#!/usr/bin/env python3
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "integration/animo-b3/ANIMO-B3B04R_SECOND_LINE_REVIEW.json"
DOC = ROOT / "docs/b3/TCD040_INDEPENDENT_SECOND_LINE_REVIEW.md"


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_B3B04R_VALIDATION: " + message)


e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
doc = DOC.read_text(encoding="utf-8")

require(e["workunit"] == "ANIMO-B3B04R", "wrong workunit")
require(e["target"] == "TCD-040", "wrong target")
require(e["starting_head_verified"] == "4cc782986faf3d3af829f2e16142dd7f8622c6ac", "wrong review start")
require(e["review_disposition"] == "FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE", "review must fail closed")
require(e["review_pass"] is False, "review must not be marked PASS")
require(e["canonical_disposition_after_review"] == "UNRESOLVED_NOT_ADMITTED", "TCD-040 must remain unresolved/not admitted")
require(e["recommend_formal_admission_workunit"] is False, "failed second line must not recommend formal admission")
require(e["scientific_claim_rejected_as_false"] is False, "evidence incompleteness is not proof the scientific claim is false")

expected_authorities = {
    "B3B04": "19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865",
    "B3D11": "4cc782986faf3d3af829f2e16142dd7f8622c6ac",
    "RG05D": "f3d6b9780631bd627f8bca0658a8e3878746e666",
    "STATEQ01": "4adae99576eb56978da71f7c8a250e4445fd3bc4",
    "STATEQ02": "cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6",
    "B3I04": "400b7cd79f89043e091751707dfa96537587dcf6",
    "B3Q01": "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
    "GOV03": "cbd262bdabe92923113b7326f2f42822ce9a971c",
}
require(e["authorities"] == expected_authorities, "authority set drifted")
require(e["issue35"]["read_before_writing"] is True, "issue #35 not recorded as read")
require(e["issue35"]["comments_read_before_writing"] is True, "issue #35 comments not recorded as read")
require(e["issue35"]["comment_count_at_review_start"] == 0, "unexpected issue #35 comment count")

b0 = e["frozen_b0"]
require(b0["source_archive_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "wrong source hash")
require(b0["testbank_archive_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "wrong testbank hash")
require(b0["raw_source_archive_accessible_in_repository"] is False, "must not claim raw source archive is in repository")
require(b0["raw_testbank_archive_accessible_in_repository"] is False, "must not claim raw testbank archive is in repository")
require(b0["raw_b0_bytes_newly_reinspected_in_this_review"] is False, "must not pretend raw B0 reinspection")

scope = e["atomic_scope"]
require(scope["coordinates"] == [
    ["Conh(0)", "Rsconh(0)"],
    ["Coni(0)", "Rsconi(0)"],
    ["Codiorma(0)", "Rscodiorma(0)"],
    ["Codiorni(0)", "Rscodiorni(0)"],
    ["Codiorpo(0)", "Rscodiorpo(0)"],
], "atomic coordinate set changed")
require(scope["Copo0_negative_control_excluded"] is True, "Copo(0) must remain excluded")
require(scope["TCD016_out_of_scope"] is True, "TCD-016 must remain outside scope")

checks = e["independent_checks"]
require(checks["source_ownership_call_order"]["result"].startswith("PASS_"), "source cross-check must pass")
require(checks["source_ownership_call_order"]["destructive_seam"] == "Inicalc.for:125-129", "wrong destructive seam")
require(checks["natural_grasspeat_activation"]["result"] == "PARTIAL_BLOCKED", "GrassPeat independence blocker must remain explicit")
require(checks["natural_grasspeat_activation"]["all_five_target_raw_testcase_values_independently_reinspected"] is False, "must not pretend all five raw testcase values were re-read")

split = checks["split282"]
require(split["result"] == "PARTIAL_BLOCKED", "split-282 must remain partial/blocked")
for species, value in split["recorded_accepted_values"].items():
    raw = struct.pack("<d", value).hex()
    require(raw == split["independently_regenerated_little_endian_ieee754_hex"][species], f"independent IEEE-754 regeneration mismatch for {species}")
require(split["raw_hex_mapping_match"] is True, "raw hex cross-check flag missing")
arith = split["independent_trace_arithmetic"]
require(arith["records_per_step"] * arith["split"] == arith["accepted_prefix_records"], "prefix arithmetic wrong")
require(arith["records_total_claimed"] - arith["accepted_prefix_records"] == arith["post_split_records"], "post-split arithmetic wrong")
require(arith["accepted_prefix_records"] == 564 and arith["post_split_records"] == 1236 and arith["records_total_claimed"] == 1800, "expected trace arithmetic changed")
require(split["B3B04_workflow_artifacts_count"] == 0, "workflow artifact blocker changed")
for key in (
    "B3B04_replay_harness_persisted",
    "checkpoint_payload_persisted",
    "full_trace_payloads_persisted",
    "full_1800_record_nonzero_path_reexecuted",
    "first_divergence_step283_phase0_layer0_independently_replayed",
    "corrected_restore_full_trace_exactness_independently_replayed",
    "split67_1800_record_zero_control_independently_replayed",
):
    require(split[key] is False, "must not overclaim unavailable split evidence: " + key)
require(split["STATEQ02_zero_path_crosscheck"]["split282_is_not_TCD040_qualification"] is True, "STATEQ02 guard must not be promoted")

fmt = checks["formatted_restart_contract"]
require(fmt["result"] == "PARTIAL_BLOCKED", "direct user-guide reinspection blocker must remain explicit")
require(fmt["user_guide_pdf_directly_reinspected"] is False, "must not pretend direct PDF inspection")
require(fmt["formatted_vs_raw_boundary_independently_supported"] is True, "formatted/raw boundary must be independently supported")
require(fmt["INITIAL_OUT_is_raw_byte_atomic_checkpoint"] is False, "INITIAL.OUT must not be promoted to raw checkpoint")

route = checks["GOV03_route"]
require(route["result"] == "PASS", "GOV03 route eligibility must pass")
require(route["historical_behaviour"] == "UNKNOWN", "historical behavior must remain UNKNOWN")
require(route["historical_fidelity_claimed"] is False, "historical fidelity claim forbidden")
require(route["historical_prevalence_claimed"] is False, "historical prevalence claim forbidden")
require(route["historical_intent_claimed"] is False, "historical intent claim forbidden")

r = checks["restore_discriminator"]
require(r["result"] == "PASS_SEMANTIC_TWO_STATE_CONTROL_PLANE_INTENT", "discriminator assessment changed")
require(r["allowed_semantic_states"] == ["COLD_START", "RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE"], "two-state semantic partition changed")
require(r["semantic_partition_sufficient"] is True, "two-state partition not marked sufficient")
require(r["restore_capable_entrypoint_requires_explicit_recognized_value"] is True, "restore intent must be explicit")
require(r["physical_state_coordinate_required"] is False, "selector must not become physical state")
require(r["heuristic_inference_allowed"] is False, "heuristic discriminator forbidden")

seam = checks["atomic_seam"]
require(seam["result"] == "PASS_BOUNDED_SEAM_NO_SCIENTIFIC_DEPENDENCY_EXPANSION", "atomic seam assessment changed")
require(seam["seam"] == "Inicalc.for:125-129 five destructive assignments only", "seam broadened")
require(seam["other_Inicalc_initialization_conditionalized"] is False, "other Inicalc initialization must remain unconditional")
require(seam["Copo0_changed"] is False, "Copo(0) change forbidden")
require(seam["unconditional_zero_assignment_deletion_qualified"] is False, "unconditional deletion must remain unqualified")
require(seam["whole_model_checkpoint_dependency_required_for_atomic_semantics"] is False, "atomic semantics incorrectly made dependent on whole-model checkpoint")
require(seam["new_physical_state_required"] is False, "selector must not introduce physical state")

require(checks["dependency_expansion"]["result"] == "PASS_NO_REQUIRED_SCIENTIFIC_SCOPE_EXPANSION", "dependency assessment changed")
require(checks["dependency_expansion"]["required_dependencies"] == [], "unexpected scientific dependency introduced")

for key, value in e["hard_boundaries"].items():
    require(value is False, "forbidden boundary crossed: " + key)

required_doc = [
    "FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE",
    "UNRESOLVED_NOT_ADMITTED",
    "COLD_START",
    "RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE",
    "Historical revision-53 behavior remains `UNKNOWN`",
    "does not substitute for the required nonzero-path replay",
    "does not admit TCD-040",
]
for phrase in required_doc:
    require(phrase in doc, "missing review document guard: " + phrase)

status = e["work_status"]
validation = e["validation"]
if status["workunit_complete"]:
    require(status["tested"] is True, "complete workunit must be tested")
    require(status["qualified"] is True, "complete review disposition package must be qualified")
    require(validation["github_actions_conclusion"] == "success", "closeout must record successful CI")
    require(validation["validator_result"] == "PASS_B3B04R_REVIEW_PACKAGE_FAIL_CLOSED", "wrong validator closeout result")
    require(validation["scope_guard"] == "PASS_B3B04R_SCOPE_GUARD", "wrong scope guard closeout result")

print("PASS_B3B04R_REVIEW_PACKAGE_FAIL_CLOSED")
