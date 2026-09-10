#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B10R_STATUS.json"
DOC = ROOT / "docs/b3/ANIMO_B3B10R_TCD031_INDEPENDENT_SECOND_LINE_REVIEW.md"


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")


def main() -> None:
    s = json.loads(STATUS.read_text())
    doc = DOC.read_text()

    require(s["workunit"] == "ANIMO-B3B10R", "wrong workunit")
    require(s["tcd"] == "TCD-031", "wrong TCD")
    require(s["exact_starting_head"] == "eccba6712f65455161d05fa9cdf6aa142f823dd4", "starting head drift")
    require(s["review_status"] == "COMPLETE_FAIL_CLOSED", "review must remain fail closed")
    require(s["review_disposition"] == "REMEDIATION_REQUIRED", "disposition must remain remediation required")
    require(s["gov04_risk_tier"] == "TIER_C", "risk tier must remain C")
    require(s["scientific_falsification"] is False, "failure is evidence/provenance insufficiency, not falsification")
    require(set(s["failure_classification"]) == {"EVIDENCE_INSUFFICIENCY", "PROVENANCE_INSUFFICIENCY"}, "failure classification drift")

    require(s["atomic_correction_identity"] == "COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY", "atomic identity drift")
    require(s["persistent_state_candidate"]["p_off_scalar_count"] == 8, "P-off scalar count must be 8")
    require(s["persistent_state_candidate"]["p_on_scalar_count"] == 12, "P-on scalar count must be 12")
    require(s["persistent_state_candidate"]["domains"] == 2, "both macropore domains required")
    require(s["persistent_state_candidate"]["exact_native_symbol_mapping_independently_primary_source_replayed"] is False, "source replay blocker must not be silently promoted")

    gates = s["review_gates"]
    for key in (
        "complete_source_level_ownership",
        "native_mapoinput_loader",
        "native_Output_Init_serialization_omission",
        "native_Animo_Output_Init_call_surface",
        "native_Init_restore_direction_and_timing",
        "native_RsCoMp_pre_promotion_initialization",
    ):
        require(gates[key].startswith("FAIL_CLOSED_"), f"{key} must remain fail closed")

    for key in (
        "candidate_restore_transaction_kernel_semantics",
        "both_domains_causally_required_kernel_level",
        "six_species_kernel_coverage",
        "conditional_phosphorus_families_covered",
        "exact_bytewise_no_tolerance",
        "fresh_process_stageB",
        "native_bad_emulation_causal_divergence",
        "domain_1_drop_causal_divergence",
        "domain_2_drop_causal_divergence",
        "evidence_boundary_not_overclaimed",
    ):
        require(gates[key] == "PASS", f"qualified immutable gate drift: {key}")

    require(gates["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "must not claim whole-model split evidence")
    require(gates["historical_active_macropore_B2"] == "ABSENT", "must not fabricate B2")
    require(gates["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN", "historical behaviour must remain UNKNOWN")
    require(gates["gov04_tier"] == "PASS_TIER_C", "Tier-C gate drift")

    require(s["stateq04"]["reopen_required"] is False, "STATEQ04 kernel qualification should not be reopened by this disposition")
    require(s["whole_model_evidence_policy"]["required_to_repair_current_independent_source_blocker"] is False, "whole-model split must not be invented as current source-remediation requirement")
    require(s["whole_model_evidence_policy"]["required_before_whole_model_production_restart_equivalence_or_migration_claim"] is True, "production evidence boundary weakened")

    require(s["tcd025_boundary"]["executed_here"] is False, "TCD-025 executed in forbidden scope")
    require(s["tcd025_boundary"]["composition_here"] is False, "TCD-025 composition in forbidden scope")
    require(s["tcd025_boundary"]["may_consume_TCD031_as_certified_dependency_now"] is False, "TCD-025 may not consume failed review as certified dependency")
    require(s["admission"]["atomic_B3_admission_may_open"] is False, "admission must remain closed")
    require(s["admission"]["admission_branch_created"] is False, "admission branch forbidden")

    for key, value in s["scope_guards"].items():
        require(value is False, f"scope guard violated: {key}")

    for token in (
        "Final disposition: `REMEDIATION_REQUIRED`",
        "FAIL_CLOSED_NATIVE_INIT_PRIMARY_REPLAY_UNAVAILABLE",
        "historical revision-53 active-macropore restart behaviour = UNKNOWN",
        "No atomic B3 admission workunit may be opened",
    ):
        require(token in doc, f"review document missing fail-closed token: {token}")

    print("ANIMO-B3B10R review-record validation: PASS (fail-closed REMEDIATION_REQUIRED state is internally consistent)")


if __name__ == "__main__":
    main()
