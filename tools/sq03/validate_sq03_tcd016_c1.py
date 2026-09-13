#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

BASE = "09ab76f0b44cb72956875fa379d68bbf97f1a0c7"
SQ02 = BASE
B3Q06 = "11e9bcdc6654e63f84875bf1f28dc54abe725700"
RG05O = "bc9e6ed997a078336645210ebb4d99ae976893fe"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "integration/animo-science/SQ03_TCD016_C1_PROCESS_ENVELOPE.json"
FREEZE = ROOT / "integration/animo-science/ANIMO-SQ03_AUTHORING_FREEZE.json"
STATUS = ROOT / "integration/animo-science/ANIMO-SQ03_STATUS.json"
REVIEW = ROOT / "integration/animo-science/ANIMO-SQ03_INTERNAL_ADVERSARIAL_REVIEW.json"

ALLOWED = {
    "docs/science/TCD016_C1_PROCESS_ENVELOPE.md",
    "integration/animo-science/SQ03_TCD016_C1_PROCESS_ENVELOPE.json",
    "integration/animo-science/ANIMO-SQ03_AUTHORING_FREEZE.json",
    "integration/animo-science/ANIMO-SQ03_STATUS.json",
    "integration/animo-science/ANIMO-SQ03_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/sq03/tcd016_c1_process_envelope_oracle.py",
    "tools/sq03/validate_sq03_tcd016_c1.py",
    ".github/workflows/animo-sq03-tcd016-c1.yml",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def changed_paths():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], cwd=ROOT, text=True)
    return {x.strip() for x in out.splitlines() if x.strip()}


def validate_review(r):
    assert r["work_unit"] == "ANIMO-SQ03"
    assert r["risk_tier"] == "C"
    assert r["review_mode"] == "SAME_AGENT_SECOND_PASS"
    assert r["assurance_label"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
    assert r["same_agent"] is True
    assert r["independence_claimed"] is False
    assert r["outcome"] == "SELF_REVIEW_PASS"

    assert r["review_boundary"] == {
        "complete_authoring_package_persisted": True,
        "immutable_head_frozen_before_review": True,
        "source_testbank_evidence_hashes_recorded_before_review": True,
        "authoring_completed_before_review": True,
        "authoring_head_matches_reviewed_head": True,
        "moving_tree_reviewed": False,
    }
    assert all(v == "PASS" for v in r["evidence_reuse_checks"].values())
    ch = r["counter_hypothesis"]
    assert ch["tested"] is True and ch["alternative"] and ch["test"]
    assert ch["result"] in {"ALTERNATIVE_REJECTED_BY_PINNED_EVIDENCE", "ALTERNATIVE_REMAINS_PLAUSIBLE_FAIL_CLOSED"}
    assert r["active_controls"] and r["negative_controls"]
    for gate in r["scientific_gates"].values():
        if gate["applicability"] == "APPLICABLE":
            assert gate["result"] == "PASS"
        else:
            assert gate["applicability"] == "NOT_APPLICABLE"
            assert gate["result"] == "NOT_APPLICABLE"
        assert gate["justification"]
    assert all(v == "PASS" for v in r["adversarial_gates"].values())
    tc = r["tier_c_enhanced"]
    for key in [
        "immutable_authoring_checkpoint",
        "complete_source_state_ownership_reconstruction",
        "first_read_first_write_or_restore_direction_analysis",
        "counter_hypothesis_test",
        "active_controls",
        "negative_controls",
        "regression_guard",
    ]:
        assert tc[key] == "PASS"
    assert tc["split_run_or_restart_evidence"]["applicability"] == "NOT_APPLICABLE"
    assert tc["split_run_or_restart_evidence"]["result"] == "NOT_APPLICABLE"
    assert tc["no_invented_tolerance"] is True
    assert tc["regression_surface_declared"] is True
    assert tc["exact_final_head_ci_required"] is True
    assert r["residual_uncertainty"]


def main():
    c = load(CONTRACT)
    f = load(FREEZE)
    s = load(STATUS)

    assert c["work_unit"] == f["work_unit"] == s["work_unit"] == "ANIMO-SQ03"
    assert c["target"] == f["target"] == s["target"] == "TCD-016-C1"
    assert f["base_head"] == BASE
    assert c["base_authority"] == s["base_authority"] == f"ANIMO-SQ02@{SQ02}"
    assert c["global_b3_authority"] == s["global_b3_authority"] == f"ANIMO-B3Q06@{B3Q06}"
    assert c["aggregate_authority"] == s["aggregate_authority"] == f"ANIMO-RG05O@{RG05O}"
    assert c["gov05_authority"] == s["gov05_authority"] == f"ANIMO-GOV05@{GOV05}"
    assert c["historical_behavior"] == s["historical_behavior"] == "UNKNOWN_WITHOUT_B2"

    q = c["qualified_process_envelope"]
    assert q["continuation_state"] == "M_surface_NH4_non_aqueous_continuation"
    assert q["unit"] == "kg N m-2"
    assert q["no_admitted_process_update"] == "M_cont_after=M_cont_before"
    assert q["persistence_semantics"] == "EPISTEMIC_FAIL_CLOSED_STATE_PERSISTENCE_NOT_PHYSICAL_INERTNESS_CLAIM"
    assert q["implicit_state_mutation_allowed"] is False
    assert q["mass_ledger_may_create_or_infer_transfers"] is False
    assert q["all_nonzero_changes_require_typed_transfer"] is True
    assert len(q["typed_transfer_required_fields"]) == 8

    rw = c["rewetting_interface"]
    assert rw["lower_bound"] == "0"
    assert rw["upper_bound"] == "M_cont_before"
    assert rw["source_update"] == "M_cont_after=M_cont_before-T_rewet"
    assert rw["receiver_rule"] == "SUM_DECLARED_RECEIVER_GAINS_EQUALS_T_rewet"
    assert rw["receiver_neutral"] is True
    assert rw["surface_aqueous_receiver_required"] is False
    for key in [
        "specific_receiver_qualified",
        "specific_function_qualified",
        "instantaneous_dissolution_qualified",
        "transfer_fraction_qualified",
        "timescale_qualified",
        "concentration_law_qualified",
    ]:
        assert rw[key] is False
    assert rw["partial_transfer_restart_persistence_required"] is True
    assert rw["ordering_must_be_explicit"] is True

    ap = c["activation_policy"]
    assert ap["any_receiving_state_must_be_scientifically_admitted"] is True
    assert ap["aqueous_receiver_requires_admitted_hydrological_state"] is True
    assert ap["legacy_0_1_mm_threshold_promoted_to_physical_trigger"] is False
    assert ap["legacy_Fu_threshold_promoted_to_physical_trigger"] is False
    assert ap["numerical_threshold_may_define_new_phase_theory"] is False

    assert set(c["candidate_process_families"].values()) == {"UNQUALIFIED", "UNQUALIFIED_FUNCTION_BOUNDED_INTERFACE_ONLY"}
    rem = c["authoring_remediation"]
    assert rem["superseded_green_head"] == "606fe29b48013397ab7ed5905132e815e6fbc456"
    assert "RECEIVER_ASSUMPTION_TOO_NARROW" in rem["reason"]
    assert c["exact_comparison_policy"] == "EXACT_DECIMAL_IDENTITIES_NO_TOLERANCE"
    assert c["c1_b3_disposition"] == s["c1_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert c["parent_b3_disposition"] == s["parent_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert c["e1_disposition"] == s["e1_disposition"] == "BLOCKED_PENDING_CONCRETE_PHYSICAL_ACTIVATION_AND_PROCESS_LAW"
    assert c["production_authorized"] is False

    assert all(v is False for v in s["hard_boundaries"].values())
    unexpected = changed_paths() - ALLOWED
    assert not unexpected, f"scope guard failed: {sorted(unexpected)}"

    if REVIEW.exists():
        r = load(REVIEW)
        validate_review(r)
        assert s["review"]["completed"] is True
        assert s["review"]["reviewed_head"] == r["reviewed_authoring_head"]
        assert s["qualified"] is True
        assert s["state"] == "QUALIFIED_TCD016_C1_FAIL_CLOSED_PROCESS_ENVELOPE_SPECIFIC_PROCESS_LAWS_UNQUALIFIED_NO_B3_ADMISSION"
        assert s["decision"] == "QUALIFY_FAIL_CLOSED_PROCESS_ENVELOPE_STATE_PERSISTENCE_AND_RECEIVER_NEUTRAL_BOUNDED_TYPED_TRANSFER_INTERFACE_KEEP_SPECIFIC_PROCESS_LAWS_UNQUALIFIED"
        assert s["b3_admission_performed"] is False
        assert s["production_authorized"] is False
    else:
        assert s["qualified"] is False
        assert s["decision"] is None
        assert s["review"]["completed"] is False

    print("SQ03 TCD016-C1 process-envelope validation PASS")


if __name__ == "__main__":
    main()
