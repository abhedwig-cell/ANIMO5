#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-RG05E fifth atomic B3 admission integration."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "integration/animo-reg/ANIMO-RG05E_STATUS.json"
INVENTORY = ROOT / "integration/animo-reg/RG05E_B3_ADMISSION_INVENTORY.json"
QUEUE = ROOT / "integration/animo-reg/RG05E_B3_QUEUE_DELTA.json"
DOC = ROOT / "docs/governance/ANIMO_RG05E_FIFTH_B3_ADMISSION_REGIE.md"

EXPECTED_B3D12 = "5e33c195174e41ea949d5a828d30bb7b9e313a5d"
EXPECTED_RG05D = "f3d6b9780631bd627f8bca0658a8e3878746e666"
EXPECTED_GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
EXPECTED_B3D09 = "2a5abc00a779baaa3fb3fa28b3c051231c286132"
EXPECTED_REVIEW = "a6880282e9ed743f97a3435b55e4fb54f7d55a44"
EXPECTED_READINESS = "b982242949aecab32b9067cf7910ad75abfc2b19"
EXPECTED_B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_DECISION = "ADMIT_TCD015_ATOMIC_CLASS_B_SCIENTIFIC_NITRATE_TRANSPORT_ALGEBRA_CORRECTION_WITH_HISTORICAL_UNCERTAINTY"
EXPECTED_DISPOSITION = "HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY"
EXPECTED_ADMITTED = ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015"]


def fail(msg: str) -> None:
    raise SystemExit("FAIL_RG05E: " + msg)


def req(condition: bool, msg: str) -> None:
    if not condition:
        fail(msg)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(ref: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    req(proc.returncode == 0, f"cannot read pinned authority {ref}:{path}: {proc.stderr.strip()}")
    return proc.stdout


def git_json(ref: str, path: str):
    return json.loads(git_text(ref, path))


def main() -> None:
    status = load(STATUS)
    inv = load(INVENTORY)
    queue = load(QUEUE)
    doc = DOC.read_text(encoding="utf-8")

    b3d12_status = git_json(EXPECTED_B3D12, "integration/animo-b3/ANIMO-B3D12_STATUS.json")
    b3d12_admission = git_json(EXPECTED_B3D12, "integration/animo-b3/TCD015_B3_ADMISSION_CLOSEOUT.json")
    rg05d_status = git_json(EXPECTED_RG05D, "integration/animo-reg/ANIMO-RG05D_STATUS.json")
    rg05d_inv = git_json(EXPECTED_RG05D, "integration/animo-reg/RG05D_B3_ADMISSION_INVENTORY.json")
    rg05d_queue = git_json(EXPECTED_RG05D, "integration/animo-reg/RG05D_B3_QUEUE_DELTA.json")

    # Incoming admission must already be qualified before central integration.
    req(b3d12_status["work_unit"] == "ANIMO-B3D12", "wrong B3D12 status object")
    req(b3d12_status["state"] == "QUALIFIED_TCD015_ATOMIC_B3_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_NO_PRODUCTION_MIGRATION", "B3D12 not qualified")
    req(b3d12_status["decision"] == EXPECTED_DECISION, "B3D12 decision mismatch")
    req(b3d12_status["admission"]["scientific_b3_admission_qualified"] is True, "B3D12 admission flag not qualified")
    req(b3d12_status["work_status"]["tested"] and b3d12_status["work_status"]["qualified"] and b3d12_status["work_status"]["work_unit_complete"], "B3D12 work status incomplete")
    req(b3d12_status["validation"]["github_actions_conclusion"] == "success", "B3D12 missing successful validation")
    req(b3d12_status["validation"]["validator_result"] == "PASS_B3D12_TCD015_ADMISSION", "B3D12 validator result mismatch")
    req(b3d12_status["validation"]["scope_guard"] == "PASS_B3D12_ADMISSION_SCOPE_GUARD", "B3D12 scope guard mismatch")
    req(b3d12_status["admission"]["historical_behaviour_status"] == "UNKNOWN", "B3D12 historical behavior changed")
    req(b3d12_status["admission"]["historical_fidelity_claimed"] is False, "B3D12 historical fidelity claimed")
    req(b3d12_status["admission"]["nitrate_only"] is True, "B3D12 nitrate scope lost")
    req(b3d12_status["admission"]["GreenHouseGasOption_0_only"] is True, "B3D12 GHG0 boundary lost")
    req(b3d12_status["admission"]["GHG_enabled_downstream_qualified"] is False, "B3D12 GHG scope promoted")
    req(all(v is False for v in b3d12_status["hard_boundaries"].values()), "B3D12 hard boundary violated")

    req(b3d12_admission["admission_decision"]["admitted"] is True, "B3D12 machine admission not true")
    req(b3d12_admission["admission_decision"]["decision"] == EXPECTED_DECISION, "B3D12 machine decision mismatch")
    req(b3d12_admission["disposition"] == EXPECTED_DISPOSITION, "B3D12 disposition mismatch")
    req(b3d12_admission["tcd_ids"] == ["TCD-015"], "B3D12 atomic target mismatch")
    req(b3d12_admission["composition"]["is_composition"] is False, "B3D12 unexpectedly compositional")
    req(all(g["status"] == "PASS" for g in b3d12_admission["gates"].values()), "B3D12 admission gates not all PASS")

    # Prior central state is pinned and additive.
    req(rg05d_status["work_unit"] == "ANIMO-RG05D", "wrong RG05D status")
    req(rg05d_status["state"] == "QUALIFIED_POST_RG05C_FOURTH_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION", "RG05D not qualified")
    req(rg05d_status["admission_state"]["scientific_admissions"] == 4, "RG05D prior count mismatch")
    req(rg05d_status["admission_state"]["admitted_tcds"] == ["TCD-017", "TCD-018", "TCD-024", "TCD-026"], "RG05D prior admitted list mismatch")
    req(rg05d_inv["counts"]["scientific_admissions"] == 4, "RG05D inventory count mismatch")
    req(rg05d_queue["post_delta_counts"]["active_queue_entries"] == 21, "RG05D active queue mismatch")
    req(rg05d_queue["post_delta_counts"]["WAITING_ON_ROUTE_AND_REVIEW"] == 3, "RG05D route/review count mismatch")

    # New inventory is exactly one atomic admission larger.
    req(inv["work_unit"] == "ANIMO-RG05E", "inventory work unit")
    req(inv["source_regie_snapshot"]["RG05D"] == EXPECTED_RG05D, "inventory RG05D pin")
    req(inv["source_regie_snapshot"]["prior_scientific_admissions"] == 4, "inventory prior count")
    req(inv["new_admission"]["tcd"] == "TCD-015", "new TCD mismatch")
    req(inv["new_admission"]["admission_authority"] == f"ANIMO-B3D12@{EXPECTED_B3D12}", "new admission authority")
    req(inv["new_admission"]["formal_disposition_authority"] == f"ANIMO-B3D09@{EXPECTED_B3D09}", "B3D09 authority")
    req(inv["new_admission"]["review_authority"] == f"ANIMO-B3B01R@{EXPECTED_REVIEW}", "review authority")
    req(inv["new_admission"]["readiness_authority"] == f"ANIMO-B3B01@{EXPECTED_READINESS}", "readiness authority")
    req(inv["new_admission"]["decision"] == EXPECTED_DECISION, "inventory decision")
    req(inv["new_admission"]["disposition"] == EXPECTED_DISPOSITION, "inventory disposition")
    req(inv["new_admission"]["historical_behaviour"] == "UNKNOWN", "inventory historical behavior")
    req(inv["new_admission"]["historical_prevalence"] == "UNKNOWN", "inventory historical prevalence")
    req(inv["new_admission"]["historical_fidelity_claimed"] is False, "inventory historical fidelity")
    req(inv["new_admission"]["generic_Transsub_change_authorized"] is False, "generic Transsub promotion")
    req(inv["new_admission"]["ghg_enabled_downstream_qualified"] is False, "GHG promotion")
    req(inv["admitted_tcds"] == EXPECTED_ADMITTED, "RG05E admitted list")
    req(inv["counts"]["scientific_admissions"] == 5, "RG05E admission count")
    req(inv["counts"]["atomic_admissions"] == 5, "RG05E atomic count")
    req(inv["counts"]["historical_uncertainty_admissions"] == 5, "RG05E historical uncertainty count")
    req(inv["counts"]["b4_admissions"] == 0 and inv["counts"]["production_migrations"] == 0, "downstream boundary opened")
    req(inv["project_boundary"]["B3_complete"] is False, "B3 incorrectly completed")
    req(inv["project_boundary"]["B4_open"] is False and inv["project_boundary"]["production_open"] is False, "B4 or production opened")

    # Queue delta must remove exactly one waiting route/review item.
    req(queue["work_unit"] == "ANIMO-RG05E", "queue work unit")
    req(len(queue["tcd_deltas"]) == 1 and queue["tcd_deltas"][0]["tcd"] == "TCD-015", "queue must contain one TCD015 delta")
    delta = queue["tcd_deltas"][0]
    req(delta["from_queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW", "wrong prior queue state")
    req(delta["to_state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "wrong target queue state")
    req(delta["admission_authority"] == f"ANIMO-B3D12@{EXPECTED_B3D12}", "queue admission authority")
    req(delta["historical_behaviour"] == "UNKNOWN", "queue historical behavior")

    pre = queue["pre_delta_counts"]
    post = queue["post_delta_counts"]
    req(pre == rg05d_queue["post_delta_counts"], "pre-delta counts must exactly equal RG05D post-delta counts")
    req(post["canonical_tcd_entries"] == 25, "canonical TCD count changed")
    req(post["active_queue_entries"] == 20, "active queue count")
    req(post["scientific_admissions"] == 5, "queue scientific admission count")
    req(post["active_queue_entries"] + post["scientific_admissions"] == post["canonical_tcd_entries"], "20 + 5 != 25")
    req(post["WAITING_ON_ROUTE_AND_REVIEW"] == 2, "route/review count must decrease by one")
    for key in ("READY_FOR_ADMISSION_READINESS", "IN_PROGRESS_ADMISSION_READINESS", "WAITING_ON_THEORY", "WAITING_ON_NUMERICS", "WAITING_ON_STATE", "WAITING_ON_RUNTIME", "WAITING_ON_CHILDREN", "NOT_READY"):
        req(post[key] == pre[key], f"unrelated queue category changed: {key}")
    req(queue["admitted_tcds"] == EXPECTED_ADMITTED, "queue admitted list")
    req(queue["unchanged_high_level_boundaries"]["canonical_tcd_register_tail"] == "TCD-042", "canonical register tail changed")
    req(queue["unchanged_high_level_boundaries"]["TCD043_reserved"] is False, "TCD043 reserved")
    req(queue["unchanged_high_level_boundaries"]["B3_whole_model_baseline_complete"] is False, "B3 baseline completed")
    req(queue["unchanged_high_level_boundaries"]["B4"] == "NOT_ADMITTED", "B4 changed")
    req(queue["unchanged_high_level_boundaries"]["PRODUCTION"] == "NOT_ADMITTED", "production changed")

    # Central status must express the same bounded delta and nothing downstream.
    req(status["work_unit"] == "ANIMO-RG05E", "status work unit")
    req(status["base"]["head"] == EXPECTED_B3D12, "status B3D12 base")
    req(status["base"]["ancestor_rg05d"] == EXPECTED_RG05D, "status RG05D ancestor")
    req(status["authority"]["RG05D"] == EXPECTED_RG05D, "status RG05D authority")
    req(status["authority"]["GOV03"] == EXPECTED_GOV03, "status GOV03 authority")
    req(status["authority"]["B3D12"] == EXPECTED_B3D12, "status B3D12 authority")
    req(status["authority"]["B3D09"] == EXPECTED_B3D09, "status B3D09 authority")
    req(status["authority"]["B3B01R"] == EXPECTED_REVIEW, "status review authority")
    req(status["authority"]["B3B01"] == EXPECTED_READINESS, "status readiness authority")
    req(status["authority"]["B3Q01"] == EXPECTED_B3Q01, "status B3Q01 authority")
    req(status["admission_state"]["scientific_admissions"] == 5, "status admission count")
    req(status["admission_state"]["admitted_tcds"] == EXPECTED_ADMITTED, "status admitted list")
    req(status["admission_state"]["tcd015_decision"] == EXPECTED_DECISION, "status TCD015 decision")
    req(status["admission_state"]["tcd015_historical_behaviour"] == "UNKNOWN", "status historical behavior")
    req(status["admission_state"]["tcd015_nitrate_only"] is True, "status nitrate scope")
    req(status["admission_state"]["tcd015_GreenHouseGasOption_0_only"] is True, "status GHG0 scope")
    req(status["admission_state"]["generic_Transsub_change_authorized"] is False, "status generic Transsub promotion")
    for key in ("b3_whole_model_baseline_complete", "b4_baseline_admitted", "production_migration_admitted", "production_code_modified", "legacy_source_modified", "frozen_testcase_modified", "canonical_tcd_register_modified", "evidence_strength_promoted_by_integration", "composition_admitted"):
        req(status["admission_state"][key] is False, f"status downstream/hard boundary changed: {key}")
    req(status["queue_state"] == post, "status queue state differs from queue delta")
    req(status["gate_snapshot"]["G7"] == "FIVE_ATOMIC_SCIENTIFIC_ADMISSIONS_B3_INCOMPLETE", "G7 state")
    req(status["gate_snapshot"]["B4"] == "NOT_ADMITTED" and status["gate_snapshot"]["PRODUCTION"] == "NOT_ADMITTED", "status opened B4/production")

    for token in ("TCD-015", "20 + 5 = 25", "WAITING_ON_ROUTE_AND_REVIEW", "GreenHouseGasOption=0", "TCD-042", "Production migration remains closed"):
        req(token in doc, f"doc missing {token}")

    if status["state"].startswith("QUALIFIED_"):
        req(status["decision"] == "QUALIFIED_POST_RG05D_FIFTH_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION", "wrong qualified decision")
        req(status["work_status"]["tested"] and status["work_status"]["qualified"] and status["work_status"]["work_unit_complete"], "qualified work status incomplete")
        req(status["validation"]["github_actions_conclusion"] == "success", "qualified status missing green run")
        req(status["validation"]["validator_result"] == "PASS_RG05E_FIFTH_B3_ADMISSION_INTEGRATION", "wrong validator result")
        req(status["validation"]["scope_guard"] == "PASS_RG05E_SCOPE_GUARD", "wrong scope guard")
    else:
        req(status["state"] == "IN_PROGRESS_PERSISTED_FIFTH_B3_ADMISSION_INTEGRATION_VALIDATION_PENDING", "unexpected pending state")
        req(status["decision"] == "PENDING_FAIL_CLOSED_VALIDATION", "unexpected pending decision")

    print("PASS_RG05E_FIFTH_B3_ADMISSION_INTEGRATION")


if __name__ == "__main__":
    main()
