#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "104100f5ceeaf0c13b4bca6ec0a0d641824014a6"
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
EXPECTED_REGISTRY_BLOB = "caf0ff601da27c9b810b992b923bfdac62f4f7d1"
SOURCE_PINS = ROOT / "integration/animo-testbank/ANIMO-TB07A_SOURCE_PINS.json"
AUDIT = ROOT / "integration/animo-testbank/ANIMO-TB07A_PREREQUISITE_AUDIT.json"
STATUS = ROOT / "integration/animo-testbank/ANIMO-TB07A_STATUS.json"

TB01 = "15a17bfa2c321d08f3ac89f334986c0ae8429045"
RG05J = "624bbad35add93de29ac89649155d9fa086a73af"
B3D27 = "cb881d0cd3e3c50455614a93b562b32354f0f1a8"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"

EXPECTED_STATE = "QUALIFIED_ANIMO_TB07A_PREREQUISITE_GATE_BLOCKED_B3_COMPOSITION_INCOMPLETE"
EXPECTED_DECISION = "DO_NOT_CREATE_COMPOSED_REGRESSION_BASELINE_UNTIL_SEPARATE_B3_COMPOSITION_COMPLETENESS_AUTHORITY_EXISTS"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"

ALLOWED = {
    ".github/workflows/animo-tb07a-composed-regression-readiness.yml",
    "integration/animo-testbank/ANIMO-TB07A_SOURCE_PINS.json",
    "integration/animo-testbank/ANIMO-TB07A_PREREQUISITE_AUDIT.json",
    "integration/animo-testbank/ANIMO-TB07A_STATUS.json",
    "tools/validate_animo_tb07a.py",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def git_json(head: str, path: str) -> dict:
    raw = run("git", "show", f"{head}:{path}")
    return json.loads(raw)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require_commit(sha: str) -> None:
    subprocess.check_call(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=ROOT)


def main() -> int:
    for sha in (BASE, TB01, RG05J, B3D27, GOV05, B3Q01, B3I07):
        require_commit(sha)

    subprocess.check_call(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT)
    changed = {x for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x}
    unexpected = changed - ALLOWED
    assert not unexpected, f"TB07A scope violation: {sorted(unexpected)}"
    assert "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json" not in changed
    assert not any(path.startswith("src/") for path in changed)

    registry_raw = REGISTRY.read_bytes()
    assert git_blob_sha(registry_raw) == EXPECTED_REGISTRY_BLOB, "central registry drift"

    pins = json.loads(SOURCE_PINS.read_text(encoding="utf-8"))
    assert pins["work_unit"] == "ANIMO-TB07A"
    assert pins["branch"] == "work/animo-tb07a-composed-regression-baseline-readiness"
    assert pins["testbank_base"]["authority"] == f"ANIMO-TB06C@{BASE}"
    assert pins["testbank_base"]["exact_final_ci_run"] == 34568860576
    assert pins["testbank_base"]["exact_final_ci_conclusion"] == "success"
    assert pins["testbank_base"]["registry_blob"] == EXPECTED_REGISTRY_BLOB
    assert pins["architecture_authority"]["authority"] == f"ANIMO-TB01@{TB01}"
    assert pins["current_aggregate_authority"]["authority"] == f"ANIMO-RG05J@{RG05J}"
    assert pins["current_aggregate_authority"]["exact_final_ci_run"] == 34568286088
    assert pins["current_aggregate_authority"]["exact_final_ci_conclusion"] == "success"
    assert pins["bounded_parent_composition_authority"]["authority"] == f"ANIMO-B3D27@{B3D27}"
    assert pins["bounded_parent_composition_authority"]["exact_final_ci_run"] == 34560197591
    assert pins["governance"]["GOV05"] == f"ANIMO-GOV05@{GOV05}"
    assert pins["governance"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}"
    assert pins["governance"]["routing"] == f"ANIMO-B3I07@{B3I07}"
    assert pins["governance"]["assurance"] == ASSURANCE
    assert pins["live_discovery"]["qualified_B3_composition_completeness_authority_found"] is False

    tb01 = git_json(TB01, "integration/animo-testbank/ANIMO-TB01_STATUS.json")
    assert tb01["state"] == "QUALIFIED_ANIMO5_SCIENTIFIC_TESTBANK_ARCHITECTURE_READY_FOR_INCREMENTAL_IMPLEMENTATION_NO_WHOLE_MODEL_GOLDEN_BASELINE"
    assert "TB7 composed regression baseline only after separate composition authority" in tb01["implementation_roadmap"]
    assert tb01["expected_value_governance"]["composed_whole_model_golden_baseline"] == "UNAVAILABLE_NOT_AUTHORIZED"
    assert tb01["hard_boundaries"]["corrected_whole_model_golden_baseline_created"] is False

    rg05j = git_json(RG05J, "integration/animo-reg/ANIMO-RG05J_STATUS.json")
    assert rg05j["state"] == "QUALIFIED_FOURTH_BATCHED_B3_ADMISSION_INTEGRATION_TWO_CHILD_ATOMS_ONE_PARENT_COMPOSITION_NO_PRODUCTION"
    assert rg05j["b3_complete"] is False
    assert rg05j["b4_open"] is False
    assert rg05j["production_open"] is False
    assert rg05j["tcd037_state"]["parent_admitted"] is True
    assert rg05j["tcd037_state"]["scientific_scope"] == "BOUNDED_COMPOSED_GHG_OBSERVER_ACCOUNTING_CONTRACT"
    assert rg05j["tcd037_state"]["complete_ghg_conservation_claimed"] is False
    assert rg05j["tcd037_state"]["historical_b2_claimed"] is False
    assert rg05j["tcd037_state"]["production_authorized"] is False

    b3d27 = git_json(B3D27, "integration/animo-b3/ANIMO-B3D27_STATUS.json")
    assert b3d27["parent_tcd_admitted"] is True
    assert b3d27["parent_scientific_claim"]["kind"] == "BOUNDED_COMPOSED_GHG_OBSERVER_ACCOUNTING_CONTRACT"
    assert b3d27["parent_scientific_claim"]["complete_ghg_carbon_ledger"] is False
    assert b3d27["parent_scientific_claim"]["complete_n2o_mass_ledger"] is False
    assert b3d27["residual_uncertainty"]["whole_model_ghg_conservation"] == "NOT_CLAIMED"
    assert b3d27["residual_uncertainty"]["historical_intel_or_reference_behaviour"] == "UNKNOWN"
    assert b3d27["hard_boundaries"]["whole_model_golden_baseline"] is False
    assert b3d27["hard_boundaries"]["historical_b2_claim"] is False
    assert b3d27["hard_boundaries"]["production_migration"] is False

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["work_unit"] == "ANIMO-TB07A"
    assert audit["assurance"] == ASSURANCE
    assert audit["decision"] == EXPECTED_DECISION
    assert audit["prerequisite_evaluation"]["current_aggregate_declares_B3_complete"]["result"] == "FAIL_CLOSED_FALSE"
    assert audit["prerequisite_evaluation"]["TB7_composed_baseline_may_be_created_now"]["result"] == "BLOCKED"
    assert audit["prerequisite_evaluation"]["separate_qualified_B3_composition_completeness_authority_found"]["result"] == "FAIL_CLOSED_NOT_FOUND"
    assert audit["registry_guard"]["expected_registry_blob"] == EXPECTED_REGISTRY_BLOB
    assert audit["registry_guard"]["central_registry_write_allowed"] is False
    assert all(v is False for v in audit["baseline_guard"].values())
    assert audit["gov05_adversarial_self_review"]["assurance"] == ASSURANCE
    assert audit["gov05_adversarial_self_review"]["result"] == "PASS_FAIL_CLOSED_PREREQUISITE_DECISION"
    assert all(v is False for v in audit["gov05_adversarial_self_review"]["questions"].values())
    assert all(v is False for v in audit["hard_boundaries"].values())

    if STATUS.exists():
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        assert status["work_unit"] == "ANIMO-TB07A"
        assert status["state"] == EXPECTED_STATE
        assert status["decision"] == EXPECTED_DECISION
        assert status["assurance"] == ASSURANCE
        assert status["registry"]["blob"] == EXPECTED_REGISTRY_BLOB
        assert status["registry"]["modified"] is False
        assert status["composition_readiness"]["B3_complete"] is False
        assert status["composition_readiness"]["TB7_baseline_authorized"] is False
        assert status["work_status"]["qualified"] is True
        assert status["work_status"]["complete"] is True
        assert all(v is False for v in status["hard_boundaries"].values())

    print("ANIMO-TB07A prerequisite gate validated: TB7 baseline creation remains fail-closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
