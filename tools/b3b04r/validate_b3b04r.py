#!/usr/bin/env python3
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "integration/animo-b3/ANIMO-B3B04R_SECOND_LINE_REVIEW.json"
DOC = ROOT / "docs/b3/TCD040_INDEPENDENT_SECOND_LINE_REVIEW.md"


def req(ok, msg):
    if not ok:
        raise SystemExit("FAIL_B3B04R_VALIDATION: " + msg)


e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
doc = DOC.read_text(encoding="utf-8")

req(e["workunit"] == "ANIMO-B3B04R", "wrong workunit")
req(e["target"] == "TCD-040", "wrong target")
req(e["starting_head_verified"] == "4cc782986faf3d3af829f2e16142dd7f8622c6ac", "wrong clean start")
req(e["review_disposition"] == "FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE", "review must fail closed")
req(e["review_pass"] is False, "review must not be PASS")
req(e["scientific_claim_rejected_as_false"] is False, "evidence gap is not scientific falsification")
req(e["canonical_disposition_after_review"] == "UNRESOLVED_NOT_ADMITTED", "TCD-040 must remain unresolved")
req(e["recommend_formal_admission_workunit"] is False, "failed second line cannot recommend admission")

req(e["authorities"] == {
    "B3B04": "19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865",
    "B3D11": "4cc782986faf3d3af829f2e16142dd7f8622c6ac",
    "RG05D": "f3d6b9780631bd627f8bca0658a8e3878746e666",
    "STATEQ01": "4adae99576eb56978da71f7c8a250e4445fd3bc4",
    "STATEQ02": "cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6",
    "B3I04": "400b7cd79f89043e091751707dfa96537587dcf6",
    "B3Q01": "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
    "GOV03": "cbd262bdabe92923113b7326f2f42822ce9a971c",
}, "authority drift")

req(e["issue35"]["read_before_writing"] is True, "issue #35 not read first")
req(e["issue35"]["comments_read_before_writing"] is True, "issue comments not read first")
req(e["issue35"]["comment_count_at_review_start"] == 0, "unexpected issue comment count")

b0 = e["frozen_b0"]
req(b0["source_archive_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "source hash drift")
req(b0["testbank_archive_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "testbank hash drift")
req(not b0["raw_source_archive_accessible_in_repository"], "raw source availability overclaimed")
req(not b0["raw_testbank_archive_accessible_in_repository"], "raw testbank availability overclaimed")
req(not b0["raw_b0_bytes_newly_reinspected_in_this_review"], "raw B0 reinspection overclaimed")

scope = e["atomic_scope"]
req(scope["coordinates"] == [
    ["Conh(0)", "Rsconh(0)"],
    ["Coni(0)", "Rsconi(0)"],
    ["Codiorma(0)", "Rscodiorma(0)"],
    ["Codiorni(0)", "Rscodiorni(0)"],
    ["Codiorpo(0)", "Rscodiorpo(0)"],
], "atomic scope drift")
req(scope["Copo0_negative_control_excluded"] is True, "Copo(0) must stay excluded")
req(scope["TCD016_out_of_scope"] is True, "TCD-016 must stay out of scope")

checks = e["independent_checks"]
req(checks["source_ownership_call_order"]["result"].startswith("PASS_"), "source cross-check missing")
req(checks["source_ownership_call_order"]["destructive_seam"] == "Inicalc.for:125-129", "wrong destructive seam")
req(checks["natural_grasspeat_activation"]["result"] == "PARTIAL_BLOCKED", "GrassPeat blocker hidden")
req(not checks["natural_grasspeat_activation"]["all_five_target_raw_testcase_values_independently_reinspected"], "GrassPeat raw reinspection overclaimed")

split = checks["split282"]
req(split["result"] == "PARTIAL_BLOCKED", "split-282 blocker hidden")
for species, value in split["recorded_accepted_values"].items():
    req(struct.pack("<d", value).hex() == split["independently_regenerated_little_endian_ieee754_hex"][species], "IEEE mismatch " + species)
arith = split["independent_trace_arithmetic"]
req(arith["records_per_step"] * arith["split"] == 564, "split prefix arithmetic wrong")
req(arith["records_total_claimed"] - 564 == 1236, "split suffix arithmetic wrong")
req(split["B3B04_workflow_artifacts_count"] == 0, "B3B04 artifacts blocker drift")
for key in [
    "B3B04_replay_harness_persisted",
    "checkpoint_payload_persisted",
    "full_trace_payloads_persisted",
    "full_1800_record_nonzero_path_reexecuted",
    "first_divergence_step283_phase0_layer0_independently_replayed",
    "corrected_restore_full_trace_exactness_independently_replayed",
    "split67_1800_record_zero_control_independently_replayed",
]:
    req(split[key] is False, "unavailable evidence overclaimed: " + key)
req(split["STATEQ02_zero_path_crosscheck"]["split282_is_not_TCD040_qualification"] is True, "STATEQ02 guard promoted incorrectly")

fmt = checks["formatted_restart_contract"]
req(fmt["result"] == "PARTIAL_BLOCKED", "user-guide blocker hidden")
req(not fmt["user_guide_pdf_directly_reinspected"], "direct guide reinspection overclaimed")
req(fmt["formatted_vs_raw_boundary_independently_supported"] is True, "formatted/raw distinction missing")
req(fmt["INITIAL_OUT_is_raw_byte_atomic_checkpoint"] is False, "INITIAL.OUT promoted to raw checkpoint")

route = checks["GOV03_route"]
req(route["result"] == "PASS", "GOV03 route not verified")
req(route["historical_behaviour"] == "UNKNOWN", "historical behavior must remain UNKNOWN")
for key in ["historical_fidelity_claimed", "historical_prevalence_claimed", "historical_intent_claimed"]:
    req(route[key] is False, "forbidden historical claim: " + key)

r = checks["restore_discriminator"]
req(r["result"] == "PASS_SEMANTIC_TWO_STATE_CONTROL_PLANE_INTENT", "discriminator assessment drift")
req(r["allowed_semantic_states"] == ["COLD_START", "RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE"], "semantic states drift")
req(r["semantic_partition_sufficient"] is True, "two-state semantics not sufficient")
req(r["restore_capable_entrypoint_requires_explicit_recognized_value"] is True, "restore selector not explicit")
req(r["physical_state_coordinate_required"] is False, "selector incorrectly made physical state")
req(r["heuristic_inference_allowed"] is False, "heuristic selector allowed")

seam = checks["atomic_seam"]
req(seam["result"] == "PASS_BOUNDED_SEAM_NO_SCIENTIFIC_DEPENDENCY_EXPANSION", "atomic seam assessment drift")
req(seam["seam"] == "Inicalc.for:125-129 five destructive assignments only", "seam broadened")
req(not seam["other_Inicalc_initialization_conditionalized"], "other Inicalc initialization changed")
req(not seam["Copo0_changed"], "Copo(0) changed")
req(not seam["unconditional_zero_assignment_deletion_qualified"], "unconditional deletion qualified")
req(checks["dependency_expansion"]["required_dependencies"] == [], "scientific scope dependency added")

for key, value in e["hard_boundaries"].items():
    req(value is False, "hard boundary crossed: " + key)

for phrase in [
    "FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE",
    "UNRESOLVED_NOT_ADMITTED",
    "COLD_START",
    "RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE",
    "Historical revision-53 behavior remains `UNKNOWN`",
    "do not substitute for the required nonzero-path replay",
    "does not admit TCD-040",
]:
    req(phrase in doc, "missing document guard: " + phrase)

if e["work_status"]["workunit_complete"]:
    req(e["work_status"]["tested"] is True, "complete review must be tested")
    req(e["work_status"]["qualified"] is True, "review disposition package must be qualified")
    req(e["validation"]["github_actions_conclusion"] == "success", "closeout must record CI success")
    req(e["validation"]["validator_result"] == "PASS_B3B04R_REVIEW_PACKAGE_FAIL_CLOSED", "wrong closeout validator result")
    req(e["validation"]["scope_guard"] == "PASS_B3B04R_SCOPE_GUARD", "wrong closeout scope result")

print("PASS_B3B04R_REVIEW_PACKAGE_FAIL_CLOSED")
