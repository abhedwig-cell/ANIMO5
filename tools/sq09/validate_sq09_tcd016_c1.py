#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "1f13c7cab30772f4aa8d5071b19d13761c2b5f16"
BRANCH = "work/animo-sq09-tcd016-c1-explicit-model-evolution"

Q_PATH = ROOT / "integration/animo-science/SQ09_TCD016_C1_EXPLICIT_MODEL_EVOLUTION_REWETTING_QUALIFICATION.json"
M_PATH = ROOT / "integration/animo-science/SQ09_TCD016_C1_AUTHORITY_EVIDENCE_MATRIX.json"
S_PATH = ROOT / "integration/animo-science/ANIMO-SQ09_STATUS.json"
F_PATH = ROOT / "integration/animo-testbank/fragments/ANIMO-SQ09_TCD016_C1_MODEL_EVOLUTION_FRAGMENT.json"
FREEZE_PATH = ROOT / "integration/animo-science/ANIMO-SQ09_AUTHORING_FREEZE.json"
REVIEW_PATH = ROOT / "integration/animo-science/ANIMO-SQ09_INTERNAL_ADVERSARIAL_REVIEW.json"


def load(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def changed_files(base, head="HEAD"):
    out = git("diff", "--name-only", f"{base}..{head}")
    return [line for line in out.splitlines() if line]


q = load(Q_PATH)
m = load(M_PATH)
s = load(S_PATH)
f = load(F_PATH)

# Identity and immutable authorities.
assert q["work_unit"] == "ANIMO-SQ09"
assert q["target"] == "TCD-016-C1"
assert q["branch"] == BRANCH
assert q["base_head"] == f"ANIMO-B3B14@{BASE}"
assert q["authorities"]["gov06"] == "ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660"
assert q["authorities"]["b3q01"] == "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
assert q["authorities"]["sq07"] == "ANIMO-SQ07@2076c0def17c504a3ba29db02d964d4a6238d2cf"
assert q["authorities"]["sq08"] == "ANIMO-SQ08@f89ec3b0bfd053c2c903cbbcf2243bb4ab4a5741"
assert q["authorities"]["b3b14"] == f"ANIMO-B3B14@{BASE}"

# Authorization is permission to assess model evolution, never evidence or admission.
a = q["authorization"]
assert a["explicit_model_evolution_assessment_authorized"] is True
assert a["authorization_is_scientific_evidence"] is False
assert a["authorization_may_override_class_f_evidence_gates"] is False
assert a["production_authorization"] is False
assert a["b3_admission_authorization"] is False

# GOV06 ownership is narrow and pinned.
o = q["gov06_semantic_contract_ownership"]
assert o["workunit"] == "ANIMO-SQ09"
assert o["parallelism_class"] == "PARALLEL_AFTER_PINNING"
assert len(o["owned_modified_contracts"]) == 1
owned = o["owned_modified_contracts"][0]
assert owned["id"] == "TCD016_C1_EXPLICIT_MODEL_EVOLUTION_REWETTING_CANDIDATE"
assert owned["stability"] == "MOVING"
assert owned["owner"] == "ANIMO-SQ09"
for c in o["consumed_contracts"]:
    assert c["stability"] == "FROZEN"

# Inherited state semantics remain unchanged.
i = q["inherited_state_and_balance"]
assert i["state"] == "M_surface_NH4_non_aqueous_continuation"
assert i["unit"] == "kg N m-2"
assert i["owner"] == "SURFACE_CHEMISTRY_PONDING_CONTROL_VOLUME"
assert i["chemically_noncommittal"] is True
assert i["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
assert i["dry_no_process_rule_status"] == "FAIL_CLOSED_STATE_PERSISTENCE_NOT_PHYSICAL_INERTNESS"

# Candidate M1 is fully explicit but remains a model abstraction without identity claims.
m1 = q["candidate_hypotheses"]["M1_rewettable_surface_NH4_N_residue_equivalent"]
assert m1["disposition"] == "SELECTED_FOR_CLASS_F_ASSESSMENT"
assert m1["model_evolution_identity"] == "REWETTABLE_SURFACE_NH4_N_RESIDUE_EQUIVALENT"
assert m1["identity_type"] == "FUNCTIONAL_CONSTITUTIVE_MODEL_ABSTRACTION"
assert m1["physical_phase_claimed"] is False
assert m1["molecular_speciation_claimed"] is False
assert m1["receiver"] == "SURFACE_AQUEOUS_NH4_STORAGE"
assert m1["activation_threshold"] is None
assert m1["legacy_0_1_mm_threshold_used"] is False
assert m1["legacy_Fu_threshold_used"] is False
assert m1["transfer_law"] == "T_rewet=M_cont_before"
assert m1["source_update"] == "M_cont_after=0"
assert m1["parameters"] == []
assert m1["same_control_volume_transfer"] is True
assert m1["external_boundary_term"] is False
assert "TCD-016-E1" in m1["small_water_consequence"]

# The selected model-evolution contract passes algebraic boundaries but fails scientific Class F gates.
g = q["class_f_gate_matrix"]
assert g["classification"] == "CLASS_F_PHYSICS_OR_MODEL_EVOLUTION"
assert g["scientific_rationale"]["status"] == "PASS_BOUNDED"
assert g["authoritative_theory"]["status"] == "FAIL"
assert g["relationship_to_preserved_b3_baseline"]["status"] == "PASS"
assert g["calibration_and_parameter_implications"]["status"] == "PASS"
assert g["conservation_implications"]["status"] == "PASS"
assert g["validation_evidence_appropriate_to_process"]["status"] == "FAIL"
assert g["expected_changes_over_application_envelope"]["status"] == "PASS_AT_CONTRACT_LEVEL"
assert q["decision"] == "DEFINE_BOUNDED_PARAMETER_FREE_REWETTABLE_RESIDUE_CANDIDATE_BUT_DO_NOT_SCIENTIFICALLY_QUALIFY_FROM_CURRENT_EVIDENCE"
assert q["final_qualification"] == "QUALIFIED_NEGATIVE_CLASS_F_CANDIDATE_NOT_SCIENTIFICALLY_ADMISSIBLE_WITH_CURRENT_EVIDENCE"
assert q["selected_candidate_maturity"] == "RESEARCH_ISOLATED"
assert q["canonical_b3_disposition"] == "PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION"
assert q["scientific_admission_readiness"] is False
assert set(q["blocking_gates"]) == {
    "AUTHORITATIVE_THEORY_OR_EQUIVALENT_TRACEABLE_MATERIAL_TO_PROCESS_BASIS",
    "PROCESS_SPECIFIC_VALIDATION_EVIDENCE_FOR_REWETTING_BEHAVIOR",
}

# No evidence-strength promotion.
e = q["evidence_classification"]
assert e["candidate_definition"] == "MODEL_EVOLUTION_PROPOSAL"
assert e["synthetic_contract_tests"] == "MODEL_EVOLUTION_EVIDENCE_FOR_ALGEBRA_AND_BOUNDARIES_ONLY"
assert e["historical_b2"] == "UNAVAILABLE_FOR_THIS_SCOPE"
assert e["physical_process_validation"] == "MISSING"
assert e["evidence_strength_promotion_forbidden"] is True
assert e["external_literature_invoked"] is False

# C1, parent, E1 and production remain closed/fail-closed.
d = q["disposition"]
assert d["tcd016_c1_b3"] == "UNRESOLVED_NOT_ADMITTED"
assert d["parent_tcd016_b3"] == "UNRESOLVED_NOT_ADMITTED"
assert d["tcd016_e1"] == "BLOCKED_PENDING_SCIENTIFICALLY_QUALIFIED_OR_SEPARATELY_ADMITTED_C1_REWETTING_SEMANTICS"
assert d["candidate_scientific_admission"] == "NOT_READY"
for key in [
    "global_b3_queue_mutated", "canonical_register_mutated", "aggregate_mutated",
    "routing_mutated", "central_testbank_registry_mutated", "production_source_modified",
    "b3_admission_performed", "b4_performed", "production_authorized"
]:
    assert d[key] is False

# Matrix must independently expose the failed theory/validation gates.
assert m["work_unit"] == "ANIMO-SQ09"
assert m["class_f_gate_summary"]["authoritative_theory"] == "FAIL"
assert m["class_f_gate_summary"]["validation_evidence_appropriate_to_process"] == "FAIL"
assert m["evidence_groups"]["B2_historical_behavior"]["status"] == "UNKNOWN_WITHOUT_B2"
assert m["evidence_groups"]["numerical_low_storage_policy"]["status"] == "OUT_OF_SCOPE_TCD016_E1"
assert "cannot" in m["evidence_strength_rule"].lower()

# Bounded fragment is explicitly non-admitting and non-validating.
assert f["work_unit"] == "ANIMO-SQ09"
assert f["evidence_class"] == "MODEL_EVOLUTION_CONTRACT_ORACLE_ONLY"
assert f["candidate"] == "REWETTABLE_SURFACE_NH4_N_RESIDUE_EQUIVALENT"
assert f["maturity"] == "RESEARCH_ISOLATED"
assert f["central_registry_write"] == "FORBIDDEN"
assert f["tb7_opened"] is False
assert f["whole_model_golden_created"] is False
assert f["admission_effect"] == "NONE"
assert f["physical_validation_claimed"] is False
assert f["historical_b2_claimed"] is False
assert f["contract"]["activation_threshold"] is None
assert f["contract"]["parameters"] == []
assert len(f["entries"]) == 5
assert f["expected_workunit_disposition"] == q["final_qualification"]

# Status is consistent with the scientific record.
assert s["work_unit"] == "ANIMO-SQ09"
assert s["target"] == "TCD-016-C1"
assert s["branch"] == BRANCH
assert s["state"] == q["final_qualification"]
assert s["decision"] == q["decision"]
assert s["qualification_kind"] == "NEGATIVE_SCIENTIFIC_QUALIFICATION"
assert s["candidate_maturity"] == "RESEARCH_ISOLATED"
assert s["scientific_admission_readiness"] is False
assert s["canonical_b3_disposition"] == "PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION"
assert s["tcd016_c1_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
assert s["parent_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
assert s["e1_disposition"] == "BLOCKED_PENDING_SCIENTIFICALLY_QUALIFIED_OR_SEPARATELY_ADMITTED_C1_REWETTING_SEMANTICS"
for value in s["hard_boundaries"].values():
    assert value is False

# Run exact arithmetic/state-machine oracle. This is not physical validation.
subprocess.check_call([sys.executable, str(ROOT / "tools/sq09/tcd016_c1_model_evolution_oracle.py")], cwd=ROOT)

# Whole-workunit change surface guard from B3B14.
allowed_exact = {
    ".github/workflows/animo-sq09-tcd016-c1.yml",
    "docs/science/TCD016_C1_EXPLICIT_MODEL_EVOLUTION_REWETTING_CONTRACT.md",
    "integration/animo-science/SQ09_TCD016_C1_EXPLICIT_MODEL_EVOLUTION_REWETTING_QUALIFICATION.json",
    "integration/animo-science/SQ09_TCD016_C1_AUTHORITY_EVIDENCE_MATRIX.json",
    "integration/animo-science/ANIMO-SQ09_STATUS.json",
    "integration/animo-science/ANIMO-SQ09_AUTHORING_FREEZE.json",
    "integration/animo-science/ANIMO-SQ09_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-testbank/fragments/ANIMO-SQ09_TCD016_C1_MODEL_EVOLUTION_FRAGMENT.json",
    "tools/sq09/tcd016_c1_model_evolution_oracle.py",
    "tools/sq09/validate_sq09_tcd016_c1.py",
}
for path in changed_files(BASE):
    assert path in allowed_exact, f"SQ09 scope violation: {path}"
    assert not path.startswith("src/"), f"production source mutation forbidden: {path}"
    assert not path.startswith("integration/animo-reg/"), f"shared B3/regie mutation forbidden: {path}"

# GOV05 freeze/review closeout checks become mandatory only in final phase.
if s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
    assert FREEZE_PATH.exists(), "final phase requires immutable authoring freeze record"
    assert REVIEW_PATH.exists(), "final phase requires GOV05 adversarial review record"
    freeze = load(FREEZE_PATH)
    review = load(REVIEW_PATH)

    assert freeze["work_unit"] == "ANIMO-SQ09"
    assert freeze["base_head"] == BASE
    frozen_head = freeze["authoring_head"]
    frozen_tree = freeze["authoring_tree"]
    assert git("rev-parse", f"{frozen_head}^{{tree}}") == frozen_tree
    assert freeze["authoring_exact_head_ci"]["conclusion"] == "success"
    assert freeze["review_boundary"] == "AUTHORING_FROZEN_NO_SUBSTANTIVE_CHANGE_PERMITTED"

    assert review["work_unit"] == "ANIMO-SQ09"
    assert review["review_mode"] == "SINGLE_AGENT_ADVERSARIAL_REVIEW"
    assert review["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
    assert review["same_agent"] is True
    assert review["genuinely_independent"] is False
    assert review["independence_claimed"] is False
    assert review["reviewed_authoring_head"] == frozen_head
    assert review["reviewed_authoring_tree"] == frozen_tree
    assert review["outcome"] == "SELF_REVIEW_PASS"
    assert review["substantive_remediation_required"] is False
    assert review["reviewed_disposition"] == q["final_qualification"]
    assert review["scientific_admission_readiness"] is False
    for name, result in review["mandatory_adversarial_checks"].items():
        assert result == "PASS", f"adversarial check failed: {name}={result}"

    permitted_post_freeze = {
        "integration/animo-science/ANIMO-SQ09_AUTHORING_FREEZE.json",
        "integration/animo-science/ANIMO-SQ09_INTERNAL_ADVERSARIAL_REVIEW.json",
        "integration/animo-science/ANIMO-SQ09_STATUS.json",
    }
    for path in changed_files(frozen_head):
        assert path in permitted_post_freeze, f"substantive post-freeze change: {path}"

    assert s["review"]["completed"] is True
    assert s["review"]["genuinely_independent"] is False
    assert s["review"]["independence_claimed"] is False
    assert s["review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
    assert s["review"]["outcome"] == "SELF_REVIEW_PASS"
    assert s["work_status"]["tested"] is True
    assert s["work_status"]["reviewed"] is True
    assert s["work_status"]["workunit_complete"] is True
else:
    assert s["phase"] == "AUTHORING_COMPLETE_PENDING_FREEZE_AND_REVIEW"
    assert s["review"]["completed"] is False
    assert s["work_status"]["workunit_complete"] is False

print("SQ09_VALIDATION_PASS")
print(q["final_qualification"])
