import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "integration/animo-science/SQ07_TCD016_C1_REWETTING_PROCESS_QUALIFICATION.json"
F = ROOT / "integration/animo-science/ANIMO-SQ07_AUTHORING_FREEZE.json"
S = ROOT / "integration/animo-science/ANIMO-SQ07_STATUS.json"
R = ROOT / "integration/animo-science/ANIMO-SQ07_INTERNAL_ADVERSARIAL_REVIEW.json"

EXPECTED = {
    "aggregate": "ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe",
    "global_b3_queue": "ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700",
    "gov05": "ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904",
    "sq06": "ANIMO-SQ06@2dbabfd5f57120c583645415e87f7eb792a8c0d7",
    "massq04": "ANIMO-MASSQ04@3e0f8254d9cd7966a4491b3068d0239b8ccda5f9",
}


def load(p):
    return json.loads(p.read_text())


def main():
    q = load(Q)
    assert q["work_unit"] == "ANIMO-SQ07"
    assert q["target"] == "TCD-016-C1"
    for k, v in EXPECTED.items():
        assert q["authorities"][k] == v
    assert q["candidate_hypotheses"]["R5"]["disposition"] == "SELECTED"
    for k in ("R0", "R1", "R2", "R3", "R4"):
        assert q["candidate_hypotheses"][k]["disposition"].startswith("REJECTED")
    assert q["decision"] == "NO_REWETTING_RECEIVER_ACTIVATION_KINETICS_SCIENTIFICALLY_QUALIFIED"
    assert q["final_qualification"] == "QUALIFIED_NEGATIVE_NO_REWETTING_PROCESS_CONTRACT_CURRENTLY_DEFENSIBLE"
    assert q["positive_process_contract"] is None
    assert q["parameters"] == []
    assert q["external_literature_invoked"] is False
    op = q["operational_semantics_after_negative_qualification"]
    assert op["rewetting_event_emitted"] is False
    assert op["automatic_receiver_selection"] is False
    assert op["automatic_transfer_fraction"] is False
    assert op["automatic_activation_threshold"] is False
    mass = q["mass_state_restart_implications"]
    assert mass["storage_identity"] == "S_NH4=S_aq+S_complex+S_cont"
    assert mass["observer_can_reconstruct_state_from_residual"] is False
    assert q["disposition"]["tcd016_c1_b3"] == "UNRESOLVED_NOT_ADMITTED"
    assert q["disposition"]["parent_tcd016_b3"] == "UNRESOLVED_NOT_ADMITTED"
    assert q["disposition"]["central_queue_mutated"] is False
    assert q["disposition"]["canonical_register_mutated"] is False
    assert q["disposition"]["production_authorized"] is False

    freeze = load(F)
    assert freeze["work_unit"] == "ANIMO-SQ07"
    assert freeze["base_head"] == "2dbabfd5f57120c583645415e87f7eb792a8c0d7"
    assert freeze["review_must_pin_exact_green_authoring_head"] is True
    assert freeze["substantive_change_resets_review"] is True

    status = load(S)
    assert status["work_unit"] == "ANIMO-SQ07"
    assert status["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
    hb = status["hard_boundaries"]
    for key in ("production_source_modified", "frozen_b0_modified", "canonical_register_modified", "central_queue_modified", "central_testbank_registry_modified", "TCD016_C1_admitted", "TCD016_parent_admitted", "TCD016_E1_admitted", "positive_rewetting_contract_qualified", "historical_fidelity_claimed", "whole_model_golden_baseline_created", "tb7_opened", "b4_opened", "production_migration_authorized"):
        assert hb[key] is False

    if R.exists():
        review = load(R)
        assert review["same_agent"] is True
        assert review["genuinely_independent"] is False
        assert review["independence_claimed"] is False
        assert review["selected_hypothesis"] == "R5"
        assert review["outcome"] == "SELF_REVIEW_PASS"
        assert all(v == "PASS" for v in review["adversarial_gates"].values())
        assert status["review"]["completed"] is True
        assert status["qualified"] is True
        assert status["state"] == "QUALIFIED_NEGATIVE_NO_REWETTING_PROCESS_CONTRACT_CURRENTLY_DEFENSIBLE"
    else:
        assert status["review"]["completed"] is False
        assert status["qualified"] is False

    print("PASS SQ07 scientific package validation")


if __name__ == "__main__":
    main()
