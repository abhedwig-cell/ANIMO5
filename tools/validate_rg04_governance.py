#!/usr/bin/env python3
"""Fail-closed structural validation for ANIMO-RG04 governance reconciliation."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "integration" / "animo-reg"
DOC = ROOT / "docs" / "governance"

EXPECTED_COUNTS = {
    "entries": 25,
    "READY_FOR_ADMISSION_READINESS": 7,
    "WAITING_ON_ROUTE_AND_REVIEW": 4,
    "WAITING_ON_THEORY": 4,
    "WAITING_ON_NUMERICS": 2,
    "WAITING_ON_STATE": 5,
    "WAITING_ON_RUNTIME": 2,
    "WAITING_ON_ATOMIZATION": 1,
    "NOT_READY": 0,
    "scientific_admissions": 0,
}

ALLOWED_QUEUE_STATES = {
    "READY_FOR_ADMISSION_READINESS",
    "WAITING_ON_ROUTE_AND_REVIEW",
    "WAITING_ON_THEORY",
    "WAITING_ON_NUMERICS",
    "WAITING_ON_STATE",
    "WAITING_ON_RUNTIME",
    "WAITING_ON_ATOMIZATION",
    "NOT_READY",
}

REQUIRED_WORKUNITS = {
    "RG03", "PREP02R", "STATEQ02", "MASSQ02", "B3I03", "B3I03-REGISTER",
    "B3B01", "B3A02", "B3A03", "B3A03R", "B3A01", "UBQ01",
}

REQUIRED_GATES = {
    "G0-G5", "G6H", "G6U", "G7", "GSTATE", "GTIME", "GMASS", "GEX",
    "GARCH", "B4(profile)", "PRODUCTION",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    queue = load_json(REG / "RG04_B3_QUEUE.json")
    authority = load_csv(REG / "RG04_WORKUNIT_AUTHORITY.csv")
    gates = load_csv(REG / "RG04_GATE_MATRIX.csv")
    status = load_json(REG / "ANIMO-RG04_STATUS.json")
    regie = (DOC / "ANIMO_RG04_PROJECT_REGIE.md").read_text(encoding="utf-8")

    # Canonical discrepancy identity and non-admission invariants.
    require(queue["canonical_register"]["tail"] == "TCD-042", "RG04 canonical tail must be TCD-042")
    require(queue["canonical_register"]["head"] == "814ea660d367494432beb63ea78298d1f6cd73d7", "unexpected canonical register head")
    require(queue["canonical_register"]["append_only"] is True, "canonical register must remain append-only")
    require(queue["canonical_register"]["register_presence_is_admission"] is False, "register presence must not imply admission")
    require(queue["scientific_admissions"] == [], "RG04 must contain no scientific admissions")
    require(queue["production_migration"] == "NOT_ADMITTED", "production migration must remain closed")

    entries = queue["entries"]
    ids = [e["tcd"] for e in entries]
    require(len(ids) == 25, "RG04 queue must contain 25 entries")
    require(len(ids) == len(set(ids)), "duplicate TCD ids in RG04 queue")
    require(ids[-1] == "TCD-042", "TCD-042 must be the final RG04 queue entry")
    require("TCD-042" in ids, "TCD-042 missing from queue")
    for e in entries:
        require(e["queue_state"] in ALLOWED_QUEUE_STATES, f"invalid queue state for {e['tcd']}")
        require(e["admission_route_state"] == "NO_ROUTE_OPEN", f"unexpected open admission route for {e['tcd']}")

    actual_counts = {key: 0 for key in EXPECTED_COUNTS}
    actual_counts["entries"] = len(entries)
    actual_counts["scientific_admissions"] = len(queue["scientific_admissions"])
    for e in entries:
        actual_counts[e["queue_state"]] += 1
    for key, expected in EXPECTED_COUNTS.items():
        require(actual_counts[key] == expected, f"queue count mismatch for {key}: {actual_counts[key]} != {expected}")
        require(queue["counts"][key] == expected, f"persisted count mismatch for {key}")

    by_tcd = {e["tcd"]: e for e in entries}
    for tcd in ("TCD-015", "TCD-017", "TCD-018", "TCD-027"):
        require(by_tcd[tcd]["queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW", f"{tcd} must be route/review blocked")
    require(by_tcd["TCD-042"]["queue_state"] == "WAITING_ON_ATOMIZATION", "TCD-042 must remain atomization-blocked")
    require("UBQ01" in by_tcd["TCD-042"]["owners"], "TCD-042 must route through UBQ01")

    # Historical route remains fail-closed despite native/build recovery.
    route = queue["route_state"]
    require(route["G6H"] == "PARTIAL_RECOVERY_HISTORICAL_B2_NOT_PASSED", "G6H state mismatch")
    require(route["G6U"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED", "G6U state mismatch")
    require(route["PREP02R_external_request_sent"] is False, "external archival request must remain recorded as unsent")
    require(route["historical_reference_artifact_obtained"] is False, "historical reference must remain absent")
    require(route["modern_native_rebuild_obtained"] is True, "modern native recovery must be recorded")
    require(route["modern_native_rebuild_is_historical_B2"] is False, "modern native rebuild must not be promoted to B2")

    # Authority table is explicit and non-duplicated.
    workunits = [r["workunit"] for r in authority]
    require(len(workunits) == len(set(workunits)), "duplicate RG04 authority rows")
    require(REQUIRED_WORKUNITS.issubset(workunits), f"missing RG04 authority rows: {sorted(REQUIRED_WORKUNITS-set(workunits))}")
    by_wu = {r["workunit"]: r for r in authority}
    require(by_wu["PREP02R"]["qualified"] == "False", "PREP02R must not be marked qualified B2")
    require(by_wu["STATEQ02"]["qualified"] == "True", "STATEQ02 executable restricted profile must be recorded qualified")
    require(by_wu["MASSQ02"]["qualified"] == "True", "MASSQ02 readiness must be recorded qualified")
    require(by_wu["UBQ01"]["completed"] == "False", "UBQ01 must remain in progress")
    require("NOT_INDEPENDENT" in by_wu["B3A03R"]["evidence_class"], "B3A03R must not be mistaken for independent review")

    # Gate matrix must preserve exact current dispositions.
    gate_ids = [r["gate"] for r in gates]
    require(len(gate_ids) == len(set(gate_ids)), "duplicate RG04 gate rows")
    require(REQUIRED_GATES.issubset(gate_ids), f"missing RG04 gates: {sorted(REQUIRED_GATES-set(gate_ids))}")
    by_gate = {r["gate"]: r for r in gates}
    require(by_gate["GSTATE"]["state"] == "RESTRICTED_CORE_EXECUTABLE_SPLIT_RUN_QUALIFIED_ADMISSION_PENDING", "GSTATE state mismatch")
    require(by_gate["GMASS"]["state"] == "TYPED_EVENT_AND_RESIDUAL_CAUSALITY_QUALIFIED_ADMISSION_PENDING", "GMASS state mismatch")
    require(by_gate["G7"]["state"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS_YET", "G7 must remain unadmitted")
    require(by_gate["B4(profile)"]["state"] == "NOT_ADMITTED", "B4 must remain closed")
    require(by_gate["PRODUCTION"]["state"] == "NOT_ADMITTED", "production must remain closed")

    # Human regie must state the critical non-promotions.
    require("2026 development rebuild" in regie, "regie must distinguish modern native rebuild from historical oracle")
    require("833 remaining accepted records" in regie, "STATEQ02 strongest executable witness missing")
    require("unexplained residual count is now zero" in regie, "MASSQ02 residual reconciliation missing")
    require("TCD-042" in regie and "atomization" in regie, "TCD-042 routing missing")
    require("RG04 itself must not admit any correction or canonical gate" in regie, "RG04 non-admission invariant missing")

    # Status is either persisted pre-test or final closeout; both must stay non-admitting.
    require(status["work_unit"] == "ANIMO-RG04", "status workunit mismatch")
    require(status["production_migration"] == "NOT_ADMITTED", "status production state mismatch")
    require(status["scientific_admission_performed"] is False, "status may not record scientific admission")
    require(status["canonical_state_admitted"] is False, "canonical STATE must remain unadmitted")
    require(status["canonical_mass_admitted"] is False, "canonical MASS must remain unadmitted")
    require(status["authority_snapshot"]["canonical_tcd_register_tail"] == "TCD-042", "status canonical tail mismatch")
    if status["state"] == "QUALIFIED_LATE_WAVE_STATE_MASS_B2_RECONCILIATION_NO_ADMISSIONS":
        require(status["tested"] is True and status["qualified"] is True and status["work_unit_complete"] is True, "final RG04 status must be tested/qualified/complete")

    print("RG04 validation PASS: 25 queue entries, TCD-042 canonical, no admissions")


if __name__ == "__main__":
    main()
