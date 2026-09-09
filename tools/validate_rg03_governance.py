#!/usr/bin/env python3
"""Structural fail-closed validation for ANIMO-RG03 governance artifacts."""
from __future__ import annotations

import csv
import json
from collections import Counter
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
    "TCD-025", "TCD-027", "TCD-042",
    *{f"TCD-{n:03d}" for n in range(28, 42)},
}

REQUIRED_WORKUNITS = {
    "RG02-G5", "GOV02", "SYNQ01", "B3Q01", "B3I01", "B3I01-REGISTER",
    "B3I02", "B3I03", "B3I03-REGISTER", "PREP02R",
    "B3A01", "B3B01", "B3A02", "B3A03",
    "STATEQ01", "STATEQ02", "TIME02", "TIMEQ01", "TIMEQ02", "MASSQ01", "MASSQ02",
    "BUILDQ01", "BUILDQ02", "BUILDQ03", "BUILDQ04",
    "ARCHG01", "ARCHG02", "NQ02", "SQ01", "MP01", "MP02", "GHG01",
}

REQUIRED_GATES = {
    "G0-G5", "G6H", "G6U", "G7", "GSTATE", "GTIME", "GMASS", "GEX",
    "GARCH", "B4(profile)", "PRODUCTION",
}

EXPECTED_QUEUE_COUNTS = {
    "READY_FOR_ADMISSION_READINESS": 7,
    "WAITING_ON_B2_OR_G6U": 4,
    "WAITING_ON_THEORY": 4,
    "WAITING_ON_NUMERICS": 2,
    "WAITING_ON_STATE": 5,
    "WAITING_ON_RUNTIME": 2,
    "NOT_READY": 1,
}

EXPECTED_GSTATE = "RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_QUALIFIED_ADMISSION_BLOCKED"
EXPECTED_GMASS = "TYPED_EVENT_PROJECTION_AND_RESIDUAL_RECONCILIATION_QUALIFIED_ADMISSION_BLOCKED"
EXPECTED_REGISTER_BRANCH = "work/animo-b3i03-canonical-register-append"
EXPECTED_REGISTER_HEAD = "814ea660d367494432beb63ea78298d1f6cd73d7"


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
    require(queue["canonical_register"]["branch"] == EXPECTED_REGISTER_BRANCH, "canonical register branch mismatch")
    require(queue["canonical_register"]["head"] == EXPECTED_REGISTER_HEAD, "canonical register head mismatch")
    require(queue["canonical_register"]["tail"] == "TCD-042", "canonical register must include qualified append through TCD-042")
    require(queue["canonical_register"]["preexisting_logical_rows_unchanged"] is True, "TCD-042 append must preserve prior logical rows")
    require(queue["route_state"]["G6H"] == "ACTIVE_B2_ACQUISITION_NOT_PASSED", "G6H must remain active and unpassed")
    require(queue["route_state"]["G6U"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED", "G6U must remain ineligible")
    require(queue["route_state"]["PREP02R_external_request_sent"] is False, "PREP02R request must remain recorded as unsent")
    require(queue["route_state"]["readiness_can_proceed_independently"] is True, "process-scoped readiness must remain possible")

    refresh = queue.get("post_closeout_refresh")
    require(isinstance(refresh, dict), "post-closeout refresh evidence must be recorded")
    require(refresh["canonical_register_tail_changed"] is True, "third refresh must record the qualified TCD-042 append")
    require(refresh["scientific_admission_performed"] is False, "register append must perform no scientific admission")
    require(refresh["evidence_strength_increased"] is False, "register append must not increase evidence strength")
    require(refresh["B3B01"]["tested"] is True, "B3B01 green CI evidence must remain recorded")
    require(refresh["B3A02"]["tested"] is True, "B3A02 green CI evidence must remain recorded")
    require(refresh["B3A03"]["tested"] is False, "B3A03 must not be promoted to tested without observed CI")
    require(refresh["B3I02"]["tested"] is True, "B3I02 green CI evidence must remain recorded")
    require(refresh["STATEQ02"]["tested"] is True and refresh["STATEQ02"]["admitted"] is False, "STATEQ02 must be qualified/tested but non-admitted")
    require(refresh["MASSQ02"]["tested"] is True and refresh["MASSQ02"]["admitted"] is False, "MASSQ02 must be qualified/tested but non-admitted")
    require(refresh["B3I03"]["tested"] is True and refresh["B3I03"]["reserved_tcd"] == "TCD-042", "B3I03 intake reservation must remain explicit")
    require(refresh["B3I03_REGISTER"]["tested"] is True and refresh["B3I03_REGISTER"]["canonical_register_append_performed"] is True, "B3I03 append follow-up must be explicit")
    require(refresh["B3I03_REGISTER"]["tail_before"] == "TCD-041" and refresh["B3I03_REGISTER"]["tail_after"] == "TCD-042", "TCD-042 append tail transition mismatch")
    require(refresh["noncanonical_reservations"] == [], "no noncanonical TCD reservation remains after qualified append")
    require(refresh["in_progress_excluded"]["UBQ01"]["status"] == "IN_PROGRESS_CHECKPOINT", "UBQ01 must be tracked as in-progress successor, not qualified authority")

    entries = queue["entries"]
    ids = [e["tcd"] for e in entries]
    require(len(ids) == len(set(ids)), "duplicate TCD entries in RG03 queue")
    require(REQUIRED_TCDS.issubset(ids), f"missing required TCD queue entries: {sorted(REQUIRED_TCDS-set(ids))}")
    require({"TCD-038", "TCD-039", "TCD-040", "TCD-041", "TCD-042"}.issubset(ids), "canonical supplements through TCD-042 must be routed")
    require(queue.get("noncanonical_reservations", []) == [], "canonical TCD-042 must not remain duplicated as a noncanonical reservation")
    for e in entries:
        require(e["queue_state"] in ALLOWED_QUEUE_STATES, f"invalid queue state for {e['tcd']}")
        require(e["admission_route_state"] == "NO_ROUTE_OPEN_G6H_NOT_PASSED_G6U_NOT_ELIGIBLE", f"unexpected admission route for {e['tcd']}")

    queue_counts = Counter(e["queue_state"] for e in entries)
    for state, expected in EXPECTED_QUEUE_COUNTS.items():
        require(queue_counts.get(state, 0) == expected, f"queue count mismatch for {state}: {queue_counts.get(state, 0)} != {expected}")

    by_tcd = {e["tcd"]: e for e in entries}
    for tcd in ("TCD-015", "TCD-017", "TCD-018", "TCD-027"):
        require(by_tcd[tcd]["queue_state"] == "WAITING_ON_B2_OR_G6U", f"{tcd} readiness is complete and must be route-blocked")
    require(by_tcd["TCD-019"]["queue_state"] == "WAITING_ON_NUMERICS", "TCD-019 must remain numerical-policy blocked")
    require(by_tcd["TCD-029"]["queue_state"] == "WAITING_ON_NUMERICS", "TCD-029 must remain a separate numerical item")
    require(by_tcd["TCD-025"]["queue_state"] == "WAITING_ON_STATE", "TCD-025 must expose macropore state dependency")
    require(by_tcd["TCD-040"]["queue_state"] == "READY_FOR_ADMISSION_READINESS", "STATEQ02 sentinel must not silently close TCD-040")
    require(by_tcd["TCD-042"]["queue_state"] == "NOT_READY", "TCD-042 must fail closed until UBQ01 atomizes boundary/owner semantics")
    require("UBQ01" in by_tcd["TCD-042"]["owners"], "TCD-042 queue entry must route to UBQ01")

    workunits = [r["workunit"] for r in authority]
    require(len(workunits) == len(set(workunits)), "duplicate workunit authority rows")
    require(REQUIRED_WORKUNITS.issubset(workunits), f"missing required workunit authority rows: {sorted(REQUIRED_WORKUNITS-set(workunits))}")
    require(len(authority) == 32, f"expected 32 authority rows after TCD-042 canonical append, got {len(authority)}")
    by_wu = {r["workunit"]: r for r in authority}
    require(by_wu["PREP02R"]["qualified"] == "False", "PREP02R must not be marked qualified B2")
    require("NON_B2" in by_wu["SYNQ01"]["evidence_class"], "SYNQ01 must remain explicitly non-B2")
    require("not admitted" in by_wu["MASSQ01"]["production_effect"].lower(), "MASSQ01 must not admit canonical MASS")
    for wu in ("B3B01", "B3A02", "B3A03", "B3I02", "B3I03", "B3I03-REGISTER", "STATEQ02", "MASSQ02"):
        require(by_wu[wu]["qualified"] == "True", f"{wu} refresh authority must be qualified")
    require(by_wu["B3B01"]["tested"] == "True", "B3B01 must retain observed green CI")
    require(by_wu["B3A02"]["tested"] == "True", "B3A02 must retain observed green CI")
    require(by_wu["B3A03"]["tested"] == "False", "B3A03 must remain explicitly CI-unobserved")
    require(by_wu["B3I02"]["tested"] == "True", "B3I02 must retain observed green CI")
    require(by_wu["B3I03"]["tested"] == "True", "B3I03 must retain observed green CI")
    require(by_wu["B3I03-REGISTER"]["tested"] == "True", "B3I03 canonical append must retain validation evidence")
    require(by_wu["B3I03-REGISTER"]["authoritative_head"] == EXPECTED_REGISTER_HEAD, "B3I03 canonical append head mismatch")
    require(by_wu["STATEQ02"]["tested"] == "True", "STATEQ02 executable qualification must remain tested")
    require(by_wu["MASSQ02"]["tested"] == "True", "MASSQ02 qualification must remain tested")
    require("NOT_B2" in by_wu["STATEQ02"]["evidence_class"], "STATEQ02 must remain explicitly non-B2")
    require("NON_B2" in by_wu["MASSQ02"]["evidence_class"], "MASSQ02 must remain explicitly non-B2")

    gate_ids = [r["gate"] for r in gates]
    require(len(gate_ids) == len(set(gate_ids)), "duplicate gate rows")
    require(REQUIRED_GATES.issubset(gate_ids), f"missing gates: {sorted(REQUIRED_GATES-set(gate_ids))}")
    by_gate = {r["gate"]: r for r in gates}
    require(by_gate["G6H"]["state"] == "ACTIVE_B2_ACQUISITION_NOT_PASSED", "G6H state mismatch")
    require(by_gate["G6U"]["state"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED", "G6U state mismatch")
    require(by_gate["G7"]["state"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS_YET", "G7 must contain no admissions")
    require(by_gate["GSTATE"]["state"] == EXPECTED_GSTATE, "GSTATE state mismatch")
    require(by_gate["GMASS"]["state"] == EXPECTED_GMASS, "GMASS state mismatch")
    require(by_gate["B4(profile)"]["state"] == "NOT_ADMITTED", "B4 must remain closed")
    require(by_gate["PRODUCTION"]["state"] == "NOT_ADMITTED", "production must remain closed")

    require("not used as a global project stop" in regie, "regie must explicitly retire the global-B2 stop interpretation")
    require("B2_ACQUISITION_STILL_ACTIVE" in regie, "PREP02R active acquisition state missing")
    require("TCD-015 through `B3B01`" in regie, "regie must record completed TCD-015 readiness")
    require("TCD-017 through `B3A02`" in regie, "regie must record completed TCD-017 readiness")
    require("TCD-018 through `B3A03`" in regie, "regie must record completed TCD-018 readiness")
    require("STATEQ02" in regie and "833 remaining accepted records" in regie, "regie must record restricted-core executable STATE evidence")
    require("MASSQ02" in regie and "zero unexplained records" in regie, "regie must record MASSQ02 causal reconciliation")
    require("QUALIFIED_CANONICAL_REGISTER_APPEND_TCD042_NO_ADMISSIONS" in regie, "regie must record the qualified TCD-042 canonical append")
    require("25 entries through `TCD-042`" in regie, "regie must record 25-entry canonical queue through TCD-042")
    require("ANIMO-UBQ01" in regie and "IN_PROGRESS_CHECKPOINT" in regie, "regie must route canonical TCD-042 to in-progress UBQ01")
    require("Evidence integration never strengthens evidence" in dag, "DAG evidence-strength invariant missing")
    require("B1 and synthetic evidence cannot be relabelled B2" in dag, "DAG synthetic/B2 invariant missing")
    require("No last-writer-wins merge" in dag, "DAG last-writer-wins invariant missing")
    require(EXPECTED_REGISTER_HEAD in dag and "register tail `TCD-042`" in dag, "DAG must bind the current canonical append head/tail")
    require("canonical TCD append establishes identity only" in dag, "DAG must keep register identity separate from scientific admission")

    require(status["work_unit"] == "ANIMO-RG03", "status work unit mismatch")
    require(status["production_migration"] == "NOT_ADMITTED", "status production gate must remain closed")
    require(status["scientific_admission_performed"] is False, "status must record no scientific admission")
    require(status["authority_snapshot"]["workunit_rows"] == 32, "status authority row count mismatch")
    require(status["authority_snapshot"]["canonical_tcd_register_branch"] == EXPECTED_REGISTER_BRANCH, "status canonical branch mismatch")
    require(status["authority_snapshot"]["canonical_tcd_register_head"] == EXPECTED_REGISTER_HEAD, "status canonical head mismatch")
    require(status["authority_snapshot"]["canonical_tcd_register_tail"] == "TCD-042", "status canonical tail mismatch")
    require(status["authority_snapshot"]["noncanonical_reservations"] == [], "status must not retain TCD-042 as noncanonical after append")
    require(status["gate_reconciliation"]["GSTATE"] == EXPECTED_GSTATE, "status GSTATE mismatch")
    require(status["gate_reconciliation"]["GMASS"] == EXPECTED_GMASS, "status GMASS mismatch")
    require(status["b3_queue"]["entries"] == 25, "status canonical queue entry count mismatch")
    require(status["b3_queue"]["READY_FOR_ADMISSION_READINESS"] == 7, "status READY queue count mismatch")
    require(status["b3_queue"]["WAITING_ON_B2_OR_G6U"] == 4, "status route-blocked queue count mismatch")
    require(status["b3_queue"]["NOT_READY"] == 1, "status NOT_READY queue count mismatch")
    require(status["b3_queue"]["noncanonical_reservations"] == [], "status must have no noncanonical reservations after append")
    if status.get("state") == "QUALIFIED_POST_G5_CANONICAL_GATE_RECONCILIATION_NO_SCIENTIFIC_ADMISSIONS":
        require(status.get("tested") is True and status.get("qualified") is True, "final RG03 status must be tested and qualified")

    print(f"RG03 validation PASS: {len(authority)} authority rows, {len(gates)} gates, {len(entries)} canonical queue entries through TCD-042")


if __name__ == "__main__":
    main()
