#!/usr/bin/env python3
"""Structural fail-closed validation for ANIMO-RG03 governance artifacts."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "integration" / "animo-reg"
DOC = ROOT / "docs" / "governance"

ALLOWED_QUEUE_STATES = {
    "READY_FOR_ADMISSION_READINESS",
    "WAITING_ON_B2_OR_G6U",
    "WAITING_ON_THEORY",
    "WAITING_ON_NUMERICS",
    "WAITING_ON_STATE",
    "WAITING_ON_RUNTIME",
    "NOT_READY",
}

REQUIRED_TCDS = {
    "TCD-015", "TCD-017", "TCD-018", "TCD-019", "TCD-023", "TCD-024",
    "TCD-025", "TCD-027",
    *{f"TCD-{n:03d}" for n in range(28, 38)},
}

REQUIRED_WORKUNITS = {
    "RG02-G5", "GOV02", "SYNQ01", "B3Q01", "B3I01", "PREP02R",
    "STATEQ01", "TIME02", "MASSQ01",
    "BUILDQ01", "BUILDQ02", "BUILDQ03", "BUILDQ04",
    "ARCHG01", "ARCHG02", "NQ02", "SQ01", "MP01", "MP02", "GHG01",
}

REQUIRED_GATES = {
    "G0-G5", "G6H", "G6U", "G7", "GSTATE", "GTIME", "GMASS", "GEX",
    "GARCH", "B4(profile)", "PRODUCTION",
}


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    queue = load_json(REG / "RG03_B3_QUEUE.json")
    authority = load_csv(REG / "RG03_WORKUNIT_AUTHORITY.csv")
    gates = load_csv(REG / "RG03_GATE_MATRIX.csv")
    status = load_json(REG / "ANIMO-RG03_STATUS.json")
    regie = (DOC / "ANIMO_RG03_PROJECT_REGIE.md").read_text(encoding="utf-8")
    dag = (DOC / "POST_G5_CANONICAL_GATE_DAG.md").read_text(encoding="utf-8")

    require(queue["scientific_admissions"] == [], "RG03 queue must contain no scientific admissions")
    require(queue["production_migration"] == "NOT_ADMITTED", "production migration must remain closed")
    require(queue["canonical_register"]["append_only"] is True, "canonical register integration must be append-only")
    require(queue["canonical_register"]["register_presence_is_admission"] is False, "register identity must not imply admission")
    require(queue["route_state"]["G6H"] == "ACTIVE_B2_ACQUISITION_NOT_PASSED", "G6H must remain active and unpassed")
    require(queue["route_state"]["G6U"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED", "G6U must remain ineligible")
    require(queue["route_state"]["PREP02R_external_request_sent"] is False, "PREP02R request must remain recorded as unsent")
    require(queue["route_state"]["readiness_can_proceed_independently"] is True, "process-scoped readiness must remain possible")

    entries = queue["entries"]
    ids = [e["tcd"] for e in entries]
    require(len(ids) == len(set(ids)), "duplicate TCD entries in RG03 queue")
    require(REQUIRED_TCDS.issubset(ids), f"missing required TCD queue entries: {sorted(REQUIRED_TCDS-set(ids))}")
    require({"TCD-038", "TCD-039", "TCD-040", "TCD-041"}.issubset(ids), "live post-G5 canonical supplements through TCD-041 must be routed")
    for e in entries:
        require(e["queue_state"] in ALLOWED_QUEUE_STATES, f"invalid queue state for {e['tcd']}")
        require(e["admission_route_state"] == "NO_ROUTE_OPEN_G6H_NOT_PASSED_G6U_NOT_ELIGIBLE", f"unexpected admission route for {e['tcd']}")

    by_tcd = {e["tcd"]: e for e in entries}
    require(by_tcd["TCD-027"]["queue_state"] == "WAITING_ON_B2_OR_G6U", "TCD-027 readiness is complete and must be route-blocked")
    require(by_tcd["TCD-019"]["queue_state"] == "WAITING_ON_NUMERICS", "TCD-019 must remain numerical-policy blocked")
    require(by_tcd["TCD-029"]["queue_state"] == "WAITING_ON_NUMERICS", "TCD-029 must remain a separate numerical item")
    require(by_tcd["TCD-025"]["queue_state"] == "WAITING_ON_STATE", "TCD-025 must expose macropore state dependency")

    workunits = [r["workunit"] for r in authority]
    require(len(workunits) == len(set(workunits)), "duplicate workunit authority rows")
    require(REQUIRED_WORKUNITS.issubset(workunits), f"missing required workunit authority rows: {sorted(REQUIRED_WORKUNITS-set(workunits))}")
    by_wu = {r["workunit"]: r for r in authority}
    require(by_wu["PREP02R"]["qualified"] == "False", "PREP02R must not be marked qualified B2")
    require("NON_B2" in by_wu["SYNQ01"]["evidence_class"], "SYNQ01 must remain explicitly non-B2")
    require("not admitted" in by_wu["MASSQ01"]["production_effect"].lower(), "MASSQ01 must not admit canonical MASS")

    gate_ids = [r["gate"] for r in gates]
    require(len(gate_ids) == len(set(gate_ids)), "duplicate gate rows")
    require(REQUIRED_GATES.issubset(gate_ids), f"missing gates: {sorted(REQUIRED_GATES-set(gate_ids))}")
    by_gate = {r["gate"]: r for r in gates}
    require(by_gate["G6H"]["state"] == "ACTIVE_B2_ACQUISITION_NOT_PASSED", "G6H state mismatch")
    require(by_gate["G6U"]["state"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED", "G6U state mismatch")
    require(by_gate["G7"]["state"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS_YET", "G7 must contain no admissions")
    require(by_gate["B4(profile)"]["state"] == "NOT_ADMITTED", "B4 must remain closed")
    require(by_gate["PRODUCTION"]["state"] == "NOT_ADMITTED", "production must remain closed")

    require("not used as a global project stop" in regie, "regie must explicitly retire the global-B2 stop interpretation")
    require("B2_ACQUISITION_STILL_ACTIVE" in regie, "PREP02R active acquisition state missing")
    require("Evidence integration never strengthens evidence" in dag, "DAG evidence-strength invariant missing")
    require("B1 and synthetic evidence cannot be relabelled B2" in dag, "DAG synthetic/B2 invariant missing")
    require("No last-writer-wins merge" in dag, "DAG last-writer-wins invariant missing")

    # Status can be either the persisted pre-test checkpoint or the final closeout.
    require(status["work_unit"] == "ANIMO-RG03", "status work unit mismatch")
    require(status["production_migration"] == "NOT_ADMITTED", "status production gate must remain closed")
    require(status["scientific_admission_performed"] is False, "status must record no scientific admission")
    if status.get("state") == "QUALIFIED_POST_G5_CANONICAL_GATE_RECONCILIATION_NO_SCIENTIFIC_ADMISSIONS":
        require(status.get("tested") is True and status.get("qualified") is True, "final RG03 status must be tested and qualified")

    print(f"RG03 validation PASS: {len(authority)} authority rows, {len(gates)} gates, {len(entries)} queue entries")


if __name__ == "__main__":
    main()
