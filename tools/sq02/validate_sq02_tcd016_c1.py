#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

BASE = "11e9bcdc6654e63f84875bf1f28dc54abe725700"
SQ01 = "26d0c74aa440bd73c23709d313e24ea8af2a0bcd"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"

ALLOWED = (
    ".github/workflows/animo-sq02-tcd016-c1.yml",
    "docs/science/TCD016_C1_GOV05_ADVERSARIAL_SCIENTIFIC_REVIEW.md",
    "integration/animo-science/SQ02_TCD016_C1_MODEL_EVOLUTION_DISPOSITION.json",
    "integration/animo-science/ANIMO-SQ02_AUTHORING_FREEZE.json",
    "integration/animo-science/ANIMO-SQ02_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-science/ANIMO-SQ02_STATUS.json",
    "tools/sq02/",
)

REVIEW_REQUIRED_KEYS = {
    "work_unit", "risk_tier", "review_mode", "assurance_label",
    "reviewed_authoring_head", "same_agent", "independence_claimed",
    "review_boundary", "evidence_reuse_checks", "counter_hypothesis",
    "active_controls", "negative_controls", "scientific_gates",
    "adversarial_gates", "tier_c_enhanced", "residual_uncertainty", "outcome"
}


def gj(path):
    return json.loads(Path(path).read_text())


def git_show(sha, path):
    return subprocess.check_output(["git", "show", f"{sha}:{path}"], text=True)


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return [x.strip() for x in out.splitlines() if x.strip()]


def allowed(path):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in ALLOWED)


def validate_generic_gov05_c(review):
    assert set(review) == REVIEW_REQUIRED_KEYS, (set(review) - REVIEW_REQUIRED_KEYS, REVIEW_REQUIRED_KEYS - set(review))
    assert review["risk_tier"] == "C"
    assert review["review_mode"] in {"INTERNAL_ADVERSARIAL_REVIEW", "SAME_AGENT_SECOND_PASS"}
    assert review["assurance_label"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
    assert review["same_agent"] is True
    assert review["independence_claimed"] is False
    assert len(review["reviewed_authoring_head"]) == 40
    int(review["reviewed_authoring_head"], 16)

    rb = review["review_boundary"]
    assert set(rb) == {
        "complete_authoring_package_persisted", "immutable_head_frozen_before_review",
        "source_testbank_evidence_hashes_recorded_before_review", "authoring_completed_before_review",
        "authoring_head_matches_reviewed_head", "moving_tree_reviewed"
    }
    assert rb["complete_authoring_package_persisted"] is True
    assert rb["immutable_head_frozen_before_review"] is True
    assert rb["source_testbank_evidence_hashes_recorded_before_review"] is True
    assert rb["authoring_completed_before_review"] is True
    assert rb["authoring_head_matches_reviewed_head"] is True
    assert rb["moving_tree_reviewed"] is False

    er = review["evidence_reuse_checks"]
    assert set(er) == {"pin_identity", "scope_compatibility", "immutable_provenance", "no_superseding_contradiction", "evidence_strength_preserved"}
    assert all(v == "PASS" for v in er.values())

    ch = review["counter_hypothesis"]
    assert set(ch) == {"tested", "alternative", "test", "result"}
    assert ch["tested"] is True
    assert ch["alternative"] and ch["test"]
    assert ch["result"] in {
        "ALTERNATIVE_REJECTED_BY_PINNED_EVIDENCE",
        "ALTERNATIVE_HAS_HIGHER_INDEPENDENCE_ASSURANCE_BUT_IS_NOT_REQUIRED_BY_GOV05",
        "ALTERNATIVE_REMAINS_PLAUSIBLE_FAIL_CLOSED",
        "CLAIM_FALSIFIED",
    }

    assert isinstance(review["active_controls"], list) and review["active_controls"]
    assert isinstance(review["negative_controls"], list) and review["negative_controls"]
    assert isinstance(review["residual_uncertainty"], list) and review["residual_uncertainty"]

    for gate, rec in review["scientific_gates"].items():
        assert gate and set(rec) == {"applicability", "result", "justification"}
        assert rec["applicability"] in {"APPLICABLE", "NOT_APPLICABLE"}
        assert rec["justification"]
        if rec["applicability"] == "APPLICABLE":
            assert rec["result"] in {"PASS", "FAIL"}
        else:
            assert rec["result"] == "NOT_APPLICABLE"

    assert review["adversarial_gates"]
    assert all(v in {"PASS", "FAIL"} for v in review["adversarial_gates"].values())

    tc = review["tier_c_enhanced"]
    assert set(tc) == {
        "immutable_authoring_checkpoint", "complete_source_state_ownership_reconstruction",
        "first_read_first_write_or_restore_direction_analysis", "counter_hypothesis_test",
        "active_controls", "negative_controls", "split_run_or_restart_evidence",
        "exact_comparison_policy", "no_invented_tolerance", "regression_guard",
        "regression_surface_declared", "exact_final_head_ci_required"
    }
    for k in (
        "immutable_authoring_checkpoint", "complete_source_state_ownership_reconstruction",
        "first_read_first_write_or_restore_direction_analysis", "counter_hypothesis_test",
        "active_controls", "negative_controls", "regression_guard"
    ):
        assert tc[k] == "PASS"
    sr = tc["split_run_or_restart_evidence"]
    assert set(sr) == {"applicability", "result", "justification"}
    assert sr["applicability"] in {"APPLICABLE", "NOT_APPLICABLE"}
    if sr["applicability"] == "APPLICABLE":
        assert sr["result"] == "PASS"
    else:
        assert sr["result"] == "NOT_APPLICABLE"
    assert sr["justification"]
    assert tc["exact_comparison_policy"]
    assert tc["no_invented_tolerance"] is True
    assert tc["regression_surface_declared"] is True
    assert tc["exact_final_head_ci_required"] is True

    assert review["outcome"] in {"SELF_REVIEW_PASS", "FAIL_CLOSED"}
    if review["outcome"] == "SELF_REVIEW_PASS":
        assert all(v == "PASS" for v in review["adversarial_gates"].values())
        assert all(rec["result"] != "FAIL" for rec in review["scientific_gates"].values())


def main():
    disp = gj("integration/animo-science/SQ02_TCD016_C1_MODEL_EVOLUTION_DISPOSITION.json")
    freeze = gj("integration/animo-science/ANIMO-SQ02_AUTHORING_FREEZE.json")
    status = gj("integration/animo-science/ANIMO-SQ02_STATUS.json")

    assert disp["work_unit"] == freeze["work_unit"] == status["work_unit"] == "ANIMO-SQ02"
    assert disp["target"] == freeze["target"] == status["target"] == "TCD-016-C1"
    assert freeze["base_head"] == BASE
    assert disp["base_authority"] == status["base_authority"] == f"ANIMO-B3Q06@{BASE}"
    assert disp["upstream_science_authority"] == status["upstream_science_authority"] == f"ANIMO-SQ01@{SQ01}"
    assert disp["gov05_authority"] == status["gov05_authority"] == f"ANIMO-GOV05@{GOV05}"
    assert disp["b3_framework_authority"] == f"ANIMO-B3Q01@{B3Q01}"

    packet = git_show(SQ01, "docs/science/TCD016_C1_INDEPENDENT_REVIEW_PACKET.md")
    assert "Review status: `PREPARED_NOT_REVIEWED`" in packet
    assert "Candidate status: `MODEL_EXTENSION_HYPOTHESIS_NOT_ADMITTED`" in packet
    assert "`PARENT_TCD016 = UNRESOLVED_NOT_ADMITTED`" in packet
    assert "`TCD-016-E1 = BLOCKED_DEPENDS_ON_TCD016_C1`" in packet

    reconstruction = git_show(SQ01, "docs/science/TCD016_DRY_SOLUTE_STATE_RECONSTRUCTION.md")
    assert "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566" in reconstruction
    assert "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84" in reconstruction
    assert "1.3880242022597072e-5 kg N m-2" in reconstruction
    assert "There is no source-defined layer-0 dry solid or sorbed NH4 owner" in reconstruction

    candidates = git_show(SQ01, "docs/science/TCD016_CONTINUATION_STATE_CANDIDATES.md")
    assert "`PREFERRED_PROPOSED_MODEL_EXTENSION`" in candidates
    assert "`REJECTED_SEMANTIC_ALIASING`" in candidates
    assert "A pre-existing variable is not automatically an admissible physical owner" in candidates

    gov_schema = json.loads(git_show(GOV05, "integration/animo-governance/GOV05_INTERNAL_ADVERSARIAL_REVIEW_SCHEMA.json"))
    assert gov_schema["$id"] == "GOV05_INTERNAL_ADVERSARIAL_REVIEW_SCHEMA.json"
    assert "tier_c_enhanced" in gov_schema["properties"]

    assert disp["evidence_identity"]["canonical_residual_NH4_kgN_m2"] == "1.3880242022597072e-5"
    c = disp["candidate_state"]
    assert c["unit"] == "kg N m-2"
    assert c["chemically_noncommittal"] is True
    assert c["independent_of_aqueous_volume"] is True
    assert c["persistent_state_required_if_implemented"] is True
    assert c["restart_checkpoint_state_required_if_implemented"] is True
    assert c["typed_internal_transfers_required"] is True
    assert c["mass_ledger_observer_only"] is True

    qt = disp["qualified_model_evolution_topology"]
    assert all(v is True for v in qt.values())
    assert all(v is True for v in disp["not_qualified"].values())
    assert disp["disposition"] == "ACCEPT_NONCOMMITTAL_CONSERVATION_STATE_FOR_MODEL_EVOLUTION_WITH_ADDITIONAL_PROCESS_QUALIFICATION"
    assert disp["c1_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert disp["e1_disposition"] == "BLOCKED_DEPENDS_ON_C1_PROCESS_CONTRACT"
    assert disp["parent_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert disp["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
    assert disp["production_authorized"] is False

    assert status["hard_boundaries"]["production_source_modified"] is False
    assert status["hard_boundaries"]["canonical_register_modified"] is False
    assert status["hard_boundaries"]["central_queue_modified"] is False
    assert status["hard_boundaries"]["TCD016_parent_admitted"] is False
    assert status["hard_boundaries"]["TCD016_C1_admitted"] is False
    assert status["hard_boundaries"]["TCD016_E1_admitted"] is False
    assert status["hard_boundaries"]["specific_dry_phase_invented"] is False
    assert status["hard_boundaries"]["rewetting_law_invented"] is False
    assert status["hard_boundaries"]["transition_threshold_qualified"] is False

    bad = [p for p in changed_files() if not allowed(p)]
    assert not bad, f"scope guard failed: {bad}"

    review_path = Path("integration/animo-science/ANIMO-SQ02_INTERNAL_ADVERSARIAL_REVIEW.json")
    if review_path.exists():
        review = gj(review_path)
        validate_generic_gov05_c(review)
        assert review["work_unit"] == "ANIMO-SQ02"
        assert review["reviewed_authoring_head"] == status["review"]["reviewed_head"]
        assert status["review"]["completed"] is True
        assert status["review"]["outcome"] == "SELF_REVIEW_PASS"
        assert status["qualified"] is True
        assert status["state"] == "QUALIFIED_TCD016_C1_NONCOMMITTAL_CONTINUATION_TOPOLOGY_FOR_MODEL_EVOLUTION_PROCESS_LAWS_UNQUALIFIED_NO_B3_ADMISSION"
        assert status["b3_admission_performed"] is False
        assert status["parent_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"

    print("SQ02 TCD016-C1 bounded package validation PASS")


if __name__ == "__main__":
    main()
