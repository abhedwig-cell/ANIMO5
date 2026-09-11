#!/usr/bin/env python3
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.stateq05.tcd039_continuation_oracle import (  # noqa: E402
    advance_from_layers,
    apply_n_shortage,
    apply_p_shortage,
    demand_deficit,
    restore_working,
    split_witness,
)

BASE = "dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
CONTRACT_PATH = ROOT / "integration/animo-state/TCD039_POTENTIAL_UPTAKE_CONTINUATION_CONTRACT.json"
ORACLE_PATH = ROOT / "integration/animo-state/TCD039_POTENTIAL_UPTAKE_ORACLE_CASES.json"
STATUS_PATH = ROOT / "integration/animo-state/ANIMO-STATEQ05_STATUS.json"
MANIFEST_PATH = ROOT / "reference/source/source_manifest.csv"

ALLOWED = {
    ".github/workflows/animo-stateq05-tcd039-continuation.yml",
    "docs/stateq05/TCD039_POTENTIAL_UPTAKE_CONTINUATION.md",
    "docs/stateq05/WORK_UNIT_CONTRACT.md",
    "integration/animo-state/TCD039_POTENTIAL_UPTAKE_CONTINUATION_CONTRACT.json",
    "integration/animo-state/TCD039_POTENTIAL_UPTAKE_ORACLE_CASES.json",
    "integration/animo-state/ANIMO-STATEQ05_STATUS.json",
    "integration/animo-state/ANIMO-STATEQ05_AUTHORING_FREEZE.json",
    "integration/animo-state/ANIMO-STATEQ05_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/stateq05/tcd039_continuation_oracle.py",
    "tools/validate_stateq05_tcd039.py",
    "tests/stateq05/test_tcd039_continuation_oracle.py",
}


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return {line.strip() for line in out.splitlines() if line.strip()}


def validate_scope():
    changed = changed_files()
    unexpected = sorted(changed - ALLOWED)
    require(not unexpected, f"scope violation: {unexpected}")
    require("tools/validate_stateq05_tcd039.py" in changed, "validator not persisted")
    require("integration/animo-state/TCD039_POTENTIAL_UPTAKE_CONTINUATION_CONTRACT.json" in changed, "contract missing")
    return sorted(changed)


def validate_manifest(contract):
    rows = {}
    with MANIFEST_PATH.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows[row["path"]] = row["sha256"]
    for path, expected in contract["source_files"].items():
        require(rows.get(path) == expected, f"source manifest mismatch for {path}")


def validate_contract(contract):
    require(contract["work_unit"] == "ANIMO-STATEQ05", "wrong workunit")
    require(contract["tcd"] == "TCD-039", "wrong TCD")
    require(contract["base_authority"] == f"ANIMO-B3Q04@{BASE}", "wrong base authority")
    require(contract["aggregate_authority"] == "ANIMO-RG05M@7146612d5dfa8ad87a4660f0c50c68a5db1e3a29", "wrong aggregate")
    require(contract["governance_authority"] == "ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904", "wrong GOV05")
    require(contract["state_evidence_authority"] == "ANIMO-STATEQ01@4adae99576eb56978da71f7c8a250e4445fd3bc4", "wrong STATEQ01")
    require(contract["profile"]["guard"] == "Ioptplant == 1", "internal crop guard missing")
    owners = contract["logical_continuation_owners"]
    require(len(owners) == 2, "TCD039 must stay at two logical potential-uptake owners")
    require(owners[0]["accepted_owner"] == "Rsamplni_pot", "N owner mismatch")
    require(owners[0]["working_alias"] == "Amplni_pot", "N alias mismatch")
    require(owners[1]["accepted_owner"] == "Rsamplpo_pot", "P owner mismatch")
    require(owners[1]["working_alias"] == "Amplpo_pot", "P alias mismatch")
    require(owners[1]["feature_guard"] == "Ipo == 1", "P guard missing")
    require(all(o["zero_reset_allowed"] is False for o in owners), "zero reset must be forbidden")
    require(contract["admission_performed"] is False, "STATEQ05 must not admit TCD039")
    excluded = " ".join(contract["excluded_scope"])
    require("CROP-007" in excluded, "CROP-007 exclusion missing")
    require("TCD-038" in excluded, "TCD-038 exclusion missing")
    require(contract["evidence_strength"]["oracle"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2", "oracle overclaim")
    require(contract["evidence_strength"]["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical overclaim")


def validate_oracles(oracle):
    require(oracle["evidence_class"] == "B1_SOURCE_DERIVED_SYNTHETIC_NOT_B2", "oracle evidence class")
    ids = [c["id"] for c in oracle["cases"]]
    require(ids == [f"S05-O{i}" for i in range(1, 10)], "oracle IDs not exact")

    for case in oracle["cases"]:
        kind = case["kind"]
        if kind == "demand":
            require(demand_deficit(case["potential"], case["actual"]) == case["expected_deficit"], f"{case['id']} demand mismatch")
        elif kind == "zero_reset_negative":
            wanted = demand_deficit(case["potential"], case["actual"])
            reset = demand_deficit(0.0, case["actual"])
            require(wanted != reset, f"{case['id']} zero reset did not diverge")
        elif kind == "advance":
            got = advance_from_layers(case["prior"], case["flev"], case["coma"], case["st"])
            require(got == case["expected"], f"{case['id']} advance mismatch")
            require(advance_from_layers(0.0, case["flev"], case["coma"], case["st"]) != got, f"{case['id']} prior owner irrelevant")
        elif kind == "n_shortage":
            n, p = apply_n_shortage(case["n_actual"], case["n_potential"], case["p_potential"], case["miup"])
            require(n != case["n_potential"] and p != case["p_potential"], f"{case['id']} shortage did not mutate potential state")
        elif kind == "p_shortage":
            n, p = apply_p_shortage(case["p_actual"], case["p_potential"], case["n_potential"], case["miup"])
            require(n != case["n_potential"] and p != case["p_potential"], f"{case['id']} P shortage did not mutate potential state")
        elif kind == "split_exact":
            a, b = split_witness(False)
            require(a == b, f"{case['id']} exact owner split mismatch")
        elif kind == "split_zero_negative":
            a, b = split_witness(True)
            require(a != b, f"{case['id']} zero reset unexpectedly equivalent")
        elif kind == "p_guard":
            require(restore_working(0.01, case["p_owner"], case["ipo"])["Amplpo_pot"] is None, f"{case['id']} P guard failed")
        else:
            raise AssertionError(f"unknown oracle kind {kind}")


def validate_status(status):
    require(status["work_unit"] == "ANIMO-STATEQ05", "status workunit")
    require(status["tcd"] == "TCD-039", "status TCD")
    require(status["risk_tier"] == "C_PERSISTENT_CONTINUATION_STATE_RESTART_SEMANTICS", "risk tier mismatch")
    require(status["scientific_admission_performed"] is False, "readiness cannot admit")
    require(status["production_source_modified"] is False, "production source boundary")
    require(status["frozen_b0_modified"] is False, "B0 boundary")
    require(status["canonical_register_modified"] is False, "register boundary")
    require(status["canonical_state_admitted"] is False, "STATE boundary")
    require(status["b4_opened"] is False and status["production_authorized"] is False, "downstream boundary")
    phase = status["phase"]
    require(phase in {"SUBSTANTIVE_AUTHORING_COMPLETE_PENDING_FREEZE", "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW", "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI"}, f"unexpected phase {phase}")
    if phase == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
        review = status["review"]
        require(review["completed"] is True, "final status without review")
        require(review["same_agent"] is True and review["genuinely_independent"] is False, "review independence overclaim")
        require(review["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "assurance mismatch")


def main():
    changed = validate_scope()
    contract = load(CONTRACT_PATH)
    oracle = load(ORACLE_PATH)
    status = load(STATUS_PATH)
    validate_manifest(contract)
    validate_contract(contract)
    validate_oracles(oracle)
    validate_status(status)
    print("PASS ANIMO-STATEQ05 TCD-039 bounded continuation ownership qualification")
    print(f"changed_files={len(changed)}")


if __name__ == "__main__":
    main()
