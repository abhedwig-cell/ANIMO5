#!/usr/bin/env python3
"""Fail-closed governance validator for ANIMO-B3I05.

B3I05 atomizes canonical parent TCD-042 into governed child correction atoms.
It creates no new top-level TCD, no register append, no scientific admission and
no production change.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B3 = ROOT / "integration" / "animo-b3"
DOC = ROOT / "docs" / "b3" / "POST_UBQ02_INCREMENTAL_NUMERICAL_INTAKE.md"
ATOM = B3 / "B3I05_TCD042_ATOMIZATION.json"
CROSSWALK = B3 / "B3I05_UBQ02_FINDING_CROSSWALK.csv"
STATUS = B3 / "ANIMO-B3I05_STATUS.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    atom = json.loads(ATOM.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    with CROSSWALK.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    require(atom["work_unit"] == "ANIMO-B3I05", "wrong atomization workunit")
    require(atom["parent_tcd"] == "TCD-042", "wrong parent TCD")
    reg = atom["canonical_register"]
    require(reg["head"] == "814ea660d367494432beb63ea78298d1f6cd73d7", "canonical register authority changed")
    require(reg["tail_before"] == "TCD-042" and reg["tail_after"] == "TCD-042", "canonical tail changed")
    require(reg["append_performed"] is False, "B3I05 may not append canonical register")

    decision = atom["allocation_decision"]
    require(decision["new_top_level_tcd_reserved"] is False, "new top-level TCD reserved")
    require(decision["tcd_043_reserved"] is False, "TCD-043 must remain unreserved")
    require(decision["child_atom_keys_are_top_level_register_rows"] is False, "child keys cannot masquerade as top-level TCD rows")
    require(decision["parent_state"] == "ATOMIZED_B1_EXACT_ZERO_PLUS_E1_FINITE_POSITIVE_NO_ADMISSION", "parent atomization state mismatch")

    atoms = {item["atom_id"]: item for item in atom["atoms"]}
    require(set(atoms) == {"TCD-042-B1", "TCD-042-E1"}, "expected exactly B1 and E1 child atoms")

    b1 = atoms["TCD-042-B1"]
    require(b1["class"] == "B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT", "B1 class mismatch")
    require(b1["scope"] == "Flpn=0 AND Flux=0", "B1 scope mismatch")
    require(b1["causal_identity_qualified"] is True, "B1 causal identity must remain qualified")
    require(b1["numerical_policy_selection_required"] is False, "B1 incorrectly coupled to numerical-policy selection")
    require(b1["admitted"] is False, "B1 may not be admitted by intake")

    e1 = atoms["TCD-042-E1"]
    require(e1["class"] == "E_NUMERICAL_POLICY", "E1 class mismatch")
    require(e1["scope"] == "Flpn=0 AND 0<Flux<1.0d-8", "E1 scope mismatch")
    require(e1["numerical_seam_characterized"] is True, "E1 characterization lost")
    require(e1["selected_numerical_policy"] is False, "E1 numerical policy selected inside intake")
    require(e1["tolerance_admitted"] is False, "E1 tolerance admitted")
    require(e1["threshold_admitted"] is False, "E1 threshold admitted")
    require(e1["admitted"] is False, "E1 may not be admitted by intake")

    facts = atom["ubq02_facts_preserved"]
    require(facts["natural_subthreshold_records"] == 1238, "UBQ02 reachability count changed")
    require(facts["natural_cases"] == 6, "UBQ02 active-case count changed")
    require(facts["binary64_direct_one_minus_exp_zero_records"] == 1189, "UBQ02 cancellation count changed")
    require(facts["natural_nonzero_mineral_N_load_records"] == 4, "UBQ02 natural materiality count changed")
    require(facts["stable_comparison_candidate_is_production_policy"] is False, "comparison candidate promoted to policy")

    for key, value in atom["invariants"].items():
        if key in {"parent_tcd_fully_qualified", "parent_tcd_admitted", "canonical_register_changed", "scientific_admission_performed", "numerical_policy_admitted", "production_source_modified", "production_migration_admitted", "evidence_strength_promoted"}:
            require(value is False, f"forbidden invariant became true: {key}")
    require(atom["invariants"]["new_tcd_count"] == 0, "new top-level TCD count must be zero")

    require(len(rows) == 5, "crosswalk row count mismatch")
    require(all(row["parent_tcd"] == "TCD-042" for row in rows), "crosswalk widened beyond TCD-042")
    require({row["atom_id"] for row in rows} == {"TCD-042-B1", "TCD-042-E1"}, "crosswalk atom identities mismatch")
    require(all(row["new_top_level_tcd"] == "false" for row in rows), "crosswalk reserves new top-level TCD")
    require(all(row["canonical_register_append"] == "false" for row in rows), "crosswalk claims canonical append")
    require(all(row["admission"] == "false" for row in rows), "crosswalk claims admission")

    require("TCD-042-B1" in doc and "TCD-042-E1" in doc, "document lacks child atom keys")
    require("does **not** reserve `TCD-043`" in doc, "document must explicitly keep TCD-043 unreserved")
    require("no global tolerance exists" in doc, "NQ01 no-tolerance rule missing")

    require(status["work_unit"] == "ANIMO-B3I05", "status workunit mismatch")
    require(status["intake"]["new_top_level_tcd_count"] == 0, "status new TCD count mismatch")
    require(status["intake"]["tcd_043_reserved"] is False, "status reserves TCD-043")
    require(status["intake"]["canonical_register_append_performed"] is False, "status claims register append")
    require(status["intake"]["canonical_register_tail_after_work"] == "TCD-042", "status canonical tail mismatch")
    require(status["admission_state"]["scientific_admission_performed"] is False, "status claims scientific admission")
    require(status["admission_state"]["numerical_policy_admitted"] is False, "status claims numerical policy admission")
    require(status["admission_state"]["production_code_modified"] is False, "status claims production modification")

    print("B3I05 validation PASS: TCD-042 atomized into B1/E1 children; no new TCD, admission or production change")


if __name__ == "__main__":
    main()
