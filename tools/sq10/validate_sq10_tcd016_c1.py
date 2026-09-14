#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "d7f63e56daef8285e6a137774c703131a1100fa2"
BRANCH = "work/animo-sq10-tcd016-c1-model-evolution-evidence-validation"

D_PATH = ROOT / "integration/animo-science/SQ10_TCD016_C1_EXTERNAL_EVIDENCE_DOSSIER.json"
Q_PATH = ROOT / "integration/animo-science/SQ10_TCD016_C1_EVIDENCE_QUALIFICATION.json"
S_PATH = ROOT / "integration/animo-science/ANIMO-SQ10_STATUS.json"
FREEZE_PATH = ROOT / "integration/animo-science/ANIMO-SQ10_AUTHORING_FREEZE.json"
REVIEW_PATH = ROOT / "integration/animo-science/ANIMO-SQ10_INTERNAL_ADVERSARIAL_REVIEW.json"


def load(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def changed_files(base, head="HEAD"):
    out = git("diff", "--name-only", f"{base}..{head}")
    return [x for x in out.splitlines() if x]


d = load(D_PATH)
q = load(Q_PATH)
s = load(S_PATH)

assert d["work_unit"] == q["work_unit"] == s["work_unit"] == "ANIMO-SQ10"
assert d["target"] == q["target"] == s["target"] == "TCD-016-C1"
assert d["branch"] == s["branch"] == BRANCH
assert d["base_head"] == q["base_head"] == s["base_head"] == f"ANIMO-SQ09@{BASE}"
assert d["candidate"] == q["candidate"]["id"] == s["candidate"] == "REWETTABLE_SURFACE_NH4_N_RESIDUE_EQUIVALENT"
assert d["candidate_maturity"] == q["candidate"]["maturity_after"] == s["candidate_maturity"] == "RESEARCH_ISOLATED"

# External evidence must remain bounded and mapped, never promoted merely because it is peer reviewed.
assert d["bounded_search_protocol"]["absence_claim_limit"].startswith("NO_QUALIFYING_EVIDENCE_FOUND_IN_THIS_BOUNDED_SEARCH")
assert len(d["sources"]) >= 5
source_ids = {x["id"] for x in d["sources"]}
assert source_ids == {"EXT-01", "EXT-02", "EXT-03", "EXT-04", "EXT-05"}
for src in d["sources"]:
    assert src["doi"]
    assert src["source_type"].startswith("PEER_REVIEWED")
    assert "reason_not_qualifying" in src
    assert src["candidate_mapping"].startswith("NONQUALIFYING")

assert d["evidence_synthesis"]["critical_mapping_gap"]
assert d["evidence_synthesis"]["process_validation_gap"]
assert d["class_f_gate_effect"]["authoritative_theory_or_traceable_material_to_process_basis"] == "FAIL_REMAINS"
assert d["class_f_gate_effect"]["process_specific_validation_evidence_for_rewetting_behavior"] == "FAIL_REMAINS"
assert d["class_f_gate_effect"]["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
assert d["final_evidence_disposition"] == "QUALIFIED_EVIDENCE_ACQUISITION_COMPLETE_NO_CLASS_F_UNLOCK"
assert d["candidate_scientific_admission_readiness"] is False
assert len(d["next_empirical_evidence_requirement"]["minimum_observables"]) >= 6
assert len(d["next_empirical_evidence_requirement"]["candidate_discrimination"]) >= 5

# GOV06 ownership and Class-F gate outcome.
o = q["gov06_semantic_contract_ownership"]
assert o["owned_contract"] == "TCD016_C1_MODEL_EVOLUTION_EXTERNAL_EVIDENCE_ASSESSMENT"
assert o["owner"] == "ANIMO-SQ10"
assert o["parallelism_class"] == "PARALLEL_AFTER_PINNING"
assert q["candidate"]["candidate_contract_modified"] is False
assert q["authorities"]["gov06"] == "ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660"
assert q["authorities"]["b3q01"] == "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
assert q["authorities"]["sq09"] == f"ANIMO-SQ09@{BASE}"

for key in ["authoritative_theory", "validation_evidence_appropriate_to_process"]:
    assert q["class_f_gate_matrix_after_acquisition"][key]["status"] == "FAIL"
assert q["decision"] == "EVIDENCE_ACQUISITION_COMPLETE_RETAIN_FAIL_CLOSED_CLASS_F_BLOCKERS_AND_DEFINE_TARGETED_EMPIRICAL_DISCRIMINATION_REQUIREMENT"
assert q["final_qualification"] == "QUALIFIED_EVIDENCE_ACQUISITION_COMPLETE_NO_CLASS_F_UNLOCK"
assert q["scientific_admission_readiness"] is False
assert set(q["blocking_gates"]) == {
    "AUTHORITATIVE_THEORY_OR_EQUIVALENT_TRACEABLE_MATERIAL_TO_PROCESS_BASIS",
    "PROCESS_SPECIFIC_VALIDATION_EVIDENCE_FOR_REWETTING_BEHAVIOR",
}
for value in q["evidence_strength_controls"].values():
    if isinstance(value, bool):
        assert value is True
assert q["evidence_strength_controls"]["historical_behavior"] == "UNKNOWN_WITHOUT_B2"

# Status and hard boundaries.
assert s["state"] == q["final_qualification"]
assert s["decision"] == q["decision"]
assert s["qualification_kind"] == "NEGATIVE_SCIENTIFIC_EVIDENCE_QUALIFICATION"
assert s["scientific_admission_readiness"] is False
assert s["tcd016_c1_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
assert s["parent_b3_disposition"] == "UNRESOLVED_NOT_ADMITTED"
assert s["e1_disposition"] == "BLOCKED_PENDING_SCIENTIFICALLY_QUALIFIED_OR_SEPARATELY_ADMITTED_C1_REWETTING_SEMANTICS"
for value in s["hard_boundaries"].values():
    assert value is False
for value in d["hard_boundaries"].values():
    assert value is False
for value in q["hard_boundaries"].values():
    assert value is False

# Whole-workunit scope guard from SQ09 final head.
allowed = {
    ".github/workflows/animo-sq10-tcd016-c1-evidence-validation.yml",
    "docs/science/TCD016_C1_EXTERNAL_EVIDENCE_ACQUISITION_AND_VALIDATION.md",
    "integration/animo-science/SQ10_TCD016_C1_EXTERNAL_EVIDENCE_DOSSIER.json",
    "integration/animo-science/SQ10_TCD016_C1_EVIDENCE_QUALIFICATION.json",
    "integration/animo-science/ANIMO-SQ10_STATUS.json",
    "integration/animo-science/ANIMO-SQ10_AUTHORING_FREEZE.json",
    "integration/animo-science/ANIMO-SQ10_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/sq10/validate_sq10_tcd016_c1.py",
}
for path in changed_files(BASE):
    assert path in allowed, f"SQ10 scope violation: {path}"
    assert not path.startswith("src/"), path
    assert not path.startswith("integration/animo-reg/"), path
    assert not path.startswith("integration/animo-testbank/"), path

if s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
    freeze = load(FREEZE_PATH)
    review = load(REVIEW_PATH)
    assert freeze["work_unit"] == "ANIMO-SQ10"
    assert freeze["base_head"] == BASE
    assert git("rev-parse", f"{freeze['authoring_head']}^{{tree}}") == freeze["authoring_tree"]
    assert freeze["authoring_exact_head_ci"]["conclusion"] == "success"
    assert freeze["review_boundary"] == "AUTHORING_FROZEN_NO_SUBSTANTIVE_CHANGE_PERMITTED"
    assert review["work_unit"] == "ANIMO-SQ10"
    assert review["review_mode"] == "SINGLE_AGENT_ADVERSARIAL_REVIEW"
    assert review["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
    assert review["same_agent"] is True
    assert review["genuinely_independent"] is False
    assert review["independence_claimed"] is False
    assert review["reviewed_authoring_head"] == freeze["authoring_head"]
    assert review["reviewed_authoring_tree"] == freeze["authoring_tree"]
    assert review["reviewed_disposition"] == q["final_qualification"]
    assert review["scientific_admission_readiness"] is False
    assert review["outcome"] == "SELF_REVIEW_PASS"
    assert review["substantive_remediation_required"] is False
    for name, result in review["mandatory_adversarial_checks"].items():
        assert result == "PASS", f"review check failed: {name}={result}"
    permitted = {
        "integration/animo-science/ANIMO-SQ10_AUTHORING_FREEZE.json",
        "integration/animo-science/ANIMO-SQ10_INTERNAL_ADVERSARIAL_REVIEW.json",
        "integration/animo-science/ANIMO-SQ10_STATUS.json",
    }
    for path in changed_files(freeze["authoring_head"]):
        assert path in permitted, f"substantive post-freeze change: {path}"
    assert s["review"]["completed"] is True
    assert s["review"]["outcome"] == "SELF_REVIEW_PASS"
    assert s["work_status"]["tested"] is True
    assert s["work_status"]["reviewed"] is True
    assert s["work_status"]["workunit_complete"] is True
else:
    assert s["phase"] == "AUTHORING_COMPLETE_PENDING_FREEZE_AND_REVIEW"
    assert s["review"]["completed"] is False
    assert s["work_status"]["workunit_complete"] is False

print("SQ10_VALIDATION_PASS")
print(q["final_qualification"])
