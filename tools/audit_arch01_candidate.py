#!/usr/bin/env python3
"""Fail-closed consistency audit for ANIMO-ARCH01 candidate architecture.

This checks design artefacts only. It does not execute frozen ANIMO, qualify a
historical reference, admit canonical STATE/TIME gates, or implement production.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

STATE_COLUMNS = [
    "legacy_state_id", "candidate_field_id", "owner_component", "ownership_kind",
    "persistence", "transaction_role", "conserved_quantity", "activation",
    "admission_status", "open_evidence",
]
TRANSFER_COLUMNS = [
    "transfer_type_id", "semantic_class", "physical_event", "source_requirement",
    "sink_requirement", "conserved_quantity_rule", "species_rule",
    "transaction_rule", "ledger_rule", "prep06_examples", "qualification_boundary",
]
REQUIRED_TRANSFER_TYPES = {
    "TT-INTERNAL", "TT-BOUNDARY-IN", "TT-BOUNDARY-OUT", "TT-MANAGEMENT-IN",
    "TT-MANAGEMENT-OUT", "TT-PHASE", "TT-REACTION", "TT-CROP",
    "TT-MACROPORE", "TT-INITIALIZATION", "TT-CONSTRAINT", "TT-OBSERVE",
}
REQUIRED_OPEN_EVIDENCE = {
    "TCD-008", "TCD-014", "TCD-015", "TCD-016", "TCD-017", "TCD-018",
    "TCD-019", "TCD-021", "TCD-023", "TCD-024", "TCD-025", "TCD-026",
    "TCD-027", "TCD-028", "TCD-029",
}


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames or [], list(reader)


def audit(root: Path) -> dict:
    prep = root / "integration/animo-prep/PREP06_CONSERVED_STATE_INVENTORY.csv"
    states_path = root / "integration/animo-architecture/ARCH01_STATE_OWNERSHIP.csv"
    transfers_path = root / "integration/animo-architecture/ARCH01_TRANSFER_TYPES.csv"
    dag_path = root / "docs/governance/MIGRATION_DAG.md"

    prep_fields, prep_rows = read_csv(prep)
    state_fields, states = read_csv(states_path)
    transfer_fields, transfers = read_csv(transfers_path)
    dag = dag_path.read_text(encoding="utf-8")

    errors: list[str] = []
    prep_ids = [row["state_id"] for row in prep_rows]
    state_ids = [row["legacy_state_id"] for row in states]
    field_ids = [row["candidate_field_id"] for row in states]
    transfer_ids = [row["transfer_type_id"] for row in transfers]

    if state_fields != STATE_COLUMNS:
        errors.append("ARCH01 state columns do not match required schema/order")
    if transfer_fields != TRANSFER_COLUMNS:
        errors.append("ARCH01 transfer columns do not match required schema/order")
    if len(prep_ids) != 53:
        errors.append(f"expected 53 PREP06 state/non-state rows, got {len(prep_ids)}")
    if sorted(prep_ids) != sorted(state_ids):
        missing = sorted(set(prep_ids) - set(state_ids))
        extra = sorted(set(state_ids) - set(prep_ids))
        errors.append(f"ARCH01 coverage mismatch missing={missing} extra={extra}")
    if len(state_ids) != len(set(state_ids)):
        errors.append("duplicate legacy_state_id in ARCH01 state registry")
    if len(field_ids) != len(set(field_ids)):
        errors.append("duplicate candidate_field_id in ARCH01 state registry")
    if set(transfer_ids) != REQUIRED_TRANSFER_TYPES:
        errors.append("typed transfer class set is incomplete or contains unreviewed extras")
    if len(transfer_ids) != len(set(transfer_ids)):
        errors.append("duplicate transfer_type_id")

    by_state = {row["legacy_state_id"]: row for row in states}
    for sid in ("REPORT-MAIN-BAL", "REPORT-DETAILED-TRANS"):
        row = by_state[sid]
        if row["ownership_kind"] != "REPORTING_OBSERVER" or row["admission_status"] != "NOT_STATE":
            errors.append(f"{sid} incorrectly promoted to state")
    for sid in ("RATE-N-MIN", "RATE-P-MIN"):
        row = by_state[sid]
        if row["ownership_kind"] != "STEP_LOCAL_SCRATCH" or row["transaction_role"] != "TRIAL_ONLY":
            errors.append(f"{sid} must remain trial-local scratch")
    dormant = by_state["TOP-SDOM-DORMANT"]
    if dormant["persistence"] != "NOT_RUNTIME_STATE" or dormant["admission_status"] != "NOT_SUPPORTED_UNTIL_QUALIFIED":
        errors.append("dormant stable surface state was promoted")
    if by_state["GHG-CH4-WATER"]["persistence"] != "DERIVED" or by_state["GHG-N2O-WATER"]["persistence"] != "DERIVED":
        errors.append("GHG water-phase views must remain derived")
    if "BLOCKED" not in by_state["W-MACROPORE"]["admission_status"]:
        errors.append("macropore feature must remain blocked for canonical admission")

    by_transfer = {row["transfer_type_id"]: row for row in transfers}
    for tid in ("TT-CONSTRAINT", "TT-OBSERVE"):
        if by_transfer[tid]["physical_event"].lower() != "false":
            errors.append(f"{tid} must not be a normal physical transfer")
    if "discard" not in by_transfer["TT-INTERNAL"]["transaction_rule"].lower() or "commit" not in by_transfer["TT-INTERNAL"]["transaction_rule"].lower():
        errors.append("internal transfer transaction rule lacks reject/commit semantics")
    if "cross-quantity" not in by_transfer["TT-REACTION"]["species_rule"].lower():
        errors.append("reaction type lacks explicit cross-quantity protection")
    if "QM --> STATE" not in dag:
        errors.append("migration DAG no longer exposes QM -> STATE serial gate")

    evidence_text = ";".join(row["open_evidence"] for row in states) + ";" + ";".join(
        row["qualification_boundary"] for row in transfers
    )
    mapped = sorted(tcd for tcd in REQUIRED_OPEN_EVIDENCE if tcd in evidence_text)
    missing_evidence = sorted(REQUIRED_OPEN_EVIDENCE - set(mapped))
    if missing_evidence:
        errors.append("missing architecture evidence mappings: " + ",".join(missing_evidence))

    return {
        "evidence_class": "ARCH01_CANDIDATE_ARCHITECTURE_CONSISTENCY_NOT_REFERENCE",
        "prep06_rows": len(prep_rows),
        "arch01_state_rows": len(states),
        "arch01_transfer_type_rows": len(transfers),
        "prep06_state_coverage_exact": sorted(prep_ids) == sorted(state_ids),
        "unique_candidate_field_ids": len(field_ids) == len(set(field_ids)),
        "required_transfer_types_exact": set(transfer_ids) == REQUIRED_TRANSFER_TYPES,
        "mapped_open_evidence": mapped,
        "missing_open_evidence": missing_evidence,
        "canonical_state_gate_admitted": False,
        "reference_qualified": False,
        "production_implemented": False,
        "production_migration_admitted": False,
        "errors": errors,
        "passed": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = audit(args.root.resolve())
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
