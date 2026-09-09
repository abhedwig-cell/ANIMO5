#!/usr/bin/env python3
"""Fail-closed structural validator for ANIMO-RG05.

RG05 is governance-only. This validator checks non-admission, authority identity,
supersession, gate consistency, queue arithmetic and parallel-routing invariants.
It does not infer scientific truth from integration.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "integration/animo-reg"
STATUS_PATH = REG / "ANIMO-RG05_STATUS.json"
AUTH_PATH = REG / "RG05_WORKUNIT_AUTHORITY.csv"
GATE_PATH = REG / "RG05_GATE_MATRIX.csv"
QUEUE_PATH = REG / "RG05_B3_QUEUE.json"
PAR_PATH = REG / "RG05_PARALLELISM_MATRIX.csv"
DOC_PATH = ROOT / "docs/governance/ANIMO_RG05_PROJECT_REGIE.md"

SOURCE_HASH = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_HASH = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
DOC_HASH = "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"
RG04_HEAD = "cf9975ded20fa64bb8125b3241f2609cbb5b51b3"
REGISTER_HEAD = "814ea660d367494432beb63ea78298d1f6cd73d7"
B3I05_HEAD = "7fa0162415e02a6f0167e71b48ae38177a9e06e0"
NQ03_HEAD = "8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6"
NQ03R_HEAD = "0153779e9045c6527b7c31156f2295ff44b57eeb"
IO02_HEAD = "302d53050d51dacfb68e1ea8d1cc7dd64e985cf3"
B3A04_HEAD = "1192ee77eda47149af1e31a752e09d343edd9273"
B3B02_HEAD = "412bf889ce959d85c651c3b9180dec0a6ff9bb61"
B3B03_HEAD = "446f57f3aeff6e7db56ce473f0724bdb58cad94f"
B3B03R_TECH_HEAD = "02ce1f49582d2b8cb794c3bfb9d674481a2eea1e"
B3B03R_HANDOFF_HEAD = "11db97289ffafdd6281b83f0aa0e96b544d6eb5a"
B3B04_HEAD = "19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865"
B3E01_HEAD = "41e43c6a6888aac5b5b52041bcdd088c7afc68f1"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def as_bool(value: str) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise AssertionError(f"not a strict CSV boolean: {value!r}")


def main() -> None:
    status = load_json(STATUS_PATH)
    queue = load_json(QUEUE_PATH)
    authority_rows = load_csv(AUTH_PATH)
    gate_rows = load_csv(GATE_PATH)
    parallel_rows = load_csv(PAR_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")

    assert status["work_unit"] == "ANIMO-RG05"
    assert status["branch"] == "work/animo-rg05-late-wave-authority-refresh"
    assert status["starting_parent"] == RG04_HEAD
    assert status["governance_only"] is True
    assert status["authority_rule"] == "CONTENT_AND_ANCESTRY_PLUS_EXPLICIT_STATUS_NOT_BRANCH_NAME_NOT_LAST_WRITER_WINS"
    assert status["frozen_identity"] == {
        "source_zip_sha256": SOURCE_HASH,
        "testbank_zip_sha256": TESTBANK_HASH,
        "documentation_sha256": DOC_HASH,
    }

    adm = status["admission_state"]
    assert all(value is False for value in adm.values())
    assert status["gate_snapshot"]["B4"] == "NOT_ADMITTED"
    assert status["gate_snapshot"]["PRODUCTION"] == "NOT_ADMITTED"
    assert status["gate_snapshot"]["G7"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS"
    assert status["gate_snapshot"]["TCD042_PARENT"] == "WAITING_ON_CHILDREN"

    hist = status["historical_route"]
    assert hist["internal_recovery_decision"] == "STOP_FURTHER_INTERNAL_REFERENCE_RECOVERY_AND_PROCEED_WITH_AVAILABLE_EVIDENCE_WITHIN_EXISTING_GOV02_SCOPE"
    assert hist["historical_reference_artifact_obtained"] is False
    assert hist["external_archival_or_provenance_action_sent"] is False
    assert hist["G6H"] == "HISTORICAL_B2_NOT_PASSED_INTERNAL_RECOVERY_STOPPED"
    assert hist["G6U"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT"
    assert hist["forbidden_reclassification"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
    assert "does **not** mean historical reference acquisition has been exhausted" in doc
    assert "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT" in doc

    snap = status["authority_snapshot_pre_validation"]
    assert snap["RG04"] == RG04_HEAD
    assert snap["B3I03_REGISTER"] == REGISTER_HEAD
    assert snap["B3I05"] == B3I05_HEAD
    assert snap["NQ03"] == NQ03_HEAD
    assert snap["NQ03R"] == NQ03R_HEAD
    assert snap["IO02"] == IO02_HEAD
    assert snap["B3A04"] == B3A04_HEAD
    assert snap["B3B02"] == B3B02_HEAD
    assert snap["B3B03"] == B3B03_HEAD
    assert snap["B3B03R_TECH"] == B3B03R_TECH_HEAD
    assert snap["B3B03R_HANDOFF"] == B3B03R_HANDOFF_HEAD
    assert snap["B3B04"] == B3B04_HEAD
    assert snap["B3E01"] == B3E01_HEAD
    assert snap["canonical_tcd_register_tail"] == "TCD-042"

    t42 = status["tcd042"]
    assert t42["canonical_top_level_parent"] == "TCD-042"
    assert t42["canonical_register_tail"] == "TCD-042"
    assert t42["tcd_043_reserved"] is False
    assert t42["shared_domain_owner"] == "TCD-042_HETOP_ZERO_DOMAIN"
    assert "Hetop=0" in t42["shared_domain_finding"]
    assert "documented" in t42["shared_domain_finding"]
    assert set(t42["children"]) == {"TCD-042-B1", "TCD-042-E1"}
    assert t42["children"]["TCD-042-B1"].startswith("PARTIAL_TCD042_B1_CLASS_B_READINESS")
    assert t42["children"]["TCD-042-E1"].startswith("PARTIAL_TCD042_E1_CLASS_E_READINESS")

    auth = {r["workunit"]: r for r in authority_rows}
    required_auth = {
        "RG04", "GOV02", "PREP02R", "STATEQ02", "B3I04", "MASSQ02",
        "B3I03", "B3I03-REGISTER", "UBQ01", "UBQ02", "B3I05",
        "B3B01", "B3A01", "B3A02", "B3A03", "B3A03R", "NQ02",
        "TIME02", "IO01", "ARCHG02", "ARCH05", "NQ03", "NQ03R", "IO02",
        "B3A04", "B3B02", "B3B03", "B3B03R-TECH", "B3B03R-HANDOFF",
        "B3B04", "B3E01",
    }
    assert required_auth.issubset(auth)
    for row in authority_rows:
        for col in ("realized", "persisted", "tested", "qualified", "admitted"):
            as_bool(row[col])
        assert as_bool(row["admitted"]) is False
        assert row["production_effect"] == "NONE"

    assert auth["PREP02R"]["qualified"] == "False"
    assert auth["B3I05"]["current_head"] == B3I05_HEAD
    assert auth["NQ03"]["current_head"] == NQ03_HEAD
    assert auth["NQ03"]["qualified"] == "True"
    assert auth["NQ03R"]["current_head"] == NQ03R_HEAD
    assert auth["NQ03R"]["tested"] == "True" and auth["NQ03R"]["qualified"] == "True"
    assert auth["IO02"]["current_head"] == IO02_HEAD
    assert auth["IO02"]["tested"] == "True" and auth["IO02"]["qualified"] == "True"
    assert auth["IO02"]["current_state"] == "QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS"
    assert auth["B3A04"]["current_head"] == B3A04_HEAD
    assert auth["B3A04"]["current_state"] == "QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING"
    assert auth["B3B02"]["current_head"] == B3B02_HEAD
    assert auth["B3B02"]["qualified"] == "False"
    assert auth["B3B02"]["current_state"].startswith("PARTIAL_TCD042_B1_CLASS_B_READINESS")
    assert auth["B3B03"]["current_head"] == B3B03_HEAD
    assert auth["B3B03"]["tested"] == "True" and auth["B3B03"]["qualified"] == "True"
    assert auth["B3B03R-TECH"]["current_head"] == B3B03R_TECH_HEAD
    assert auth["B3B03R-TECH"]["qualified"] == "True"
    assert auth["B3B03R-HANDOFF"]["current_head"] == B3B03R_HANDOFF_HEAD
    assert auth["B3B03R-HANDOFF"]["qualified"] == "False"
    assert auth["B3B04"]["current_head"] == B3B04_HEAD
    assert auth["B3B04"]["tested"] == "True" and auth["B3B04"]["qualified"] == "True"
    assert auth["B3B04"]["current_state"] == "QUALIFIED_ATOMIC_CLASS_B_RESTART_IDENTITY_READINESS_ONLY_NO_B3_ADMISSION"
    assert auth["B3E01"]["current_head"] == B3E01_HEAD
    assert auth["B3E01"]["tested"] == "True" and auth["B3E01"]["qualified"] == "True"
    assert auth["B3E01"]["current_state"].startswith("PARTIAL_TCD042_E1_CLASS_E_READINESS")

    gates = {r["gate"]: r for r in gate_rows}
    for gate in ("G6H", "G6U", "G7", "GSTATE", "GTIME", "GMASS", "GEX", "GARCH", "TCD042_PARENT", "B4_PROFILE", "PRODUCTION"):
        assert gate in gates
    assert gates["G6H"]["state"] == hist["G6H"]
    assert gates["G6U"]["state"] == hist["G6U"]
    assert gates["G7"]["state"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS"
    assert "TCD-040" in gates["G7"]["qualified_basis"]
    assert gates["TCD042_PARENT"]["state"] == "WAITING_ON_CHILDREN"
    assert "Hetop=0" in gates["TCD042_PARENT"]["remaining_dependencies"]
    assert gates["B4_PROFILE"]["state"] == "NOT_ADMITTED"
    assert gates["PRODUCTION"]["state"] == "NOT_ADMITTED"

    assert queue["canonical_register"]["head"] == REGISTER_HEAD
    assert queue["canonical_register"]["tail"] == "TCD-042"
    assert queue["canonical_register"]["tcd_043_reserved"] is False
    entries = queue["entries"]
    assert len(entries) == 25
    ids = [e["tcd"] for e in entries]
    assert len(ids) == len(set(ids))
    assert ids[0] == "TCD-015" and ids[-1] == "TCD-042"
    counts = Counter(e["queue_state"] for e in entries)
    declared = queue["counts"]
    assert declared["entries"] == 25
    for state in queue["allowed_states"]:
        assert declared[state] == counts.get(state, 0)
    assert declared["scientific_admissions"] == 0
    assert queue["scientific_admissions"] == []
    assert queue["production_migration"] == "NOT_ADMITTED"

    e42 = next(e for e in entries if e["tcd"] == "TCD-042")
    assert e42["queue_state"] == "WAITING_ON_CHILDREN"
    assert "Hetop=0" in " ".join(e42["blockers"])
    children = {c["id"]: c for c in e42["children"]}
    assert children["TCD-042-B1"]["state"] == "WAITING_ON_THEORY"
    assert children["TCD-042-E1"]["state"] == "WAITING_ON_THEORY"
    assert children["TCD-042-B1"]["status"].startswith("PARTIAL_TCD042_B1_CLASS_B_READINESS")
    assert children["TCD-042-E1"]["status"].startswith("PARTIAL_TCD042_E1_CLASS_E_READINESS")
    assert next(e for e in entries if e["tcd"] == "TCD-026")["queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW"
    assert next(e for e in entries if e["tcd"] == "TCD-024")["queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW"
    e40 = next(e for e in entries if e["tcd"] == "TCD-040")
    assert e40["queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW"
    assert "B3B04" in e40["owners"]
    assert "unconditional" in e40["next_action"]

    streams = {r["stream"]: r for r in parallel_rows}
    required_streams = {
        "historical_external_acquisition", "exact_zero_upper_reservoir",
        "finite_positive_upper_reservoir", "tcd042_zero_thickness_domain",
        "nq03_independent_review", "slow_langmuir_index", "nonlinear_p_policy",
        "exudate_initial_ledger", "layer0_restart_identity", "general_input_contract",
        "completed_readiness_reviews", "canonical_state_gate", "canonical_time_gate",
        "canonical_mass_gate", "canonical_exchange_gate", "tcd042_parent",
        "b4_profile", "production",
    }
    assert required_streams.issubset(streams)
    assert streams["exact_zero_upper_reservoir"]["parallel_class"] == "SHARED_PARENT_DISTINCT_ATOM"
    assert streams["finite_positive_upper_reservoir"]["parallel_class"] == "SHARED_PARENT_DISTINCT_ATOM"
    assert streams["tcd042_zero_thickness_domain"]["parallel_class"] == "SHARED_SEMANTIC_OWNER"
    assert "documented" in streams["tcd042_zero_thickness_domain"]["guards"]
    assert streams["nq03_independent_review"]["current_state"].startswith("INDEPENDENT_REVIEW_PASS")
    assert streams["general_input_contract"]["current_state"] == "QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS"
    assert "production migration" in streams["general_input_contract"]["guards"]
    assert streams["layer0_restart_identity"]["current_state"] == "QUALIFIED_ATOMIC_CLASS_B_RESTART_IDENTITY_READINESS_ONLY_NO_B3_ADMISSION"
    assert "unconditional" in streams["layer0_restart_identity"]["guards"]
    assert "TCD-019" in streams["slow_langmuir_index"]["guards"]
    assert streams["tcd042_parent"]["parallel_class"] == "SERIAL_COMPOSITION"
    assert streams["b4_profile"]["parallel_class"] == "SERIAL_GATE"
    assert streams["production"]["parallel_class"] == "SERIAL_GATE"

    required_files = {
        "docs/governance/ANIMO_RG05_PROJECT_REGIE.md",
        "integration/animo-reg/RG05_WORKUNIT_AUTHORITY.csv",
        "integration/animo-reg/RG05_GATE_MATRIX.csv",
        "integration/animo-reg/RG05_B3_QUEUE.json",
        "integration/animo-reg/RG05_PARALLELISM_MATRIX.csv",
        "integration/animo-reg/ANIMO-RG05_STATUS.json",
        "tools/validate_rg05_governance.py",
        ".github/workflows/animo-rg05-governance.yml",
    }
    assert set(status["deliverables"]) == required_files
    for rel in required_files:
        assert (ROOT / rel).exists(), rel

    if status["work_status"]["qualified"]:
        assert status["state"] == "QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS"
        assert status["decision"] == status["state"]
        assert status["work_status"]["tested"] is True
        assert status["work_status"]["work_unit_complete"] is True
        assert status["validation"]["validator_result"] == "PASS"
        assert status["validation"]["github_actions_conclusion"] == "success"
    else:
        assert status["state"] == "IN_PROGRESS_PERSISTED_POST_CLOSEOUT_DELTA_REVALIDATION_PENDING"
        assert status["decision"] == "PENDING_FAIL_CLOSED_REVALIDATION"
        assert status["work_status"]["tested"] is False
        assert status["work_status"]["work_unit_complete"] is False

    print("ANIMO-RG05 governance validator: PASS")
    print("authority-by-content/ancestry and supersession: PASS")
    print("frozen B0 identity: PASS")
    print("G6H/G6U fail-closed route: PASS")
    print("canonical TCD tail and TCD-042 child routing: PASS")
    print("shared Hetop=0 semantic owner: PASS")
    print("bounded IO02 GENERAL qualification: PASS")
    print("TCD-040 atomic restart readiness routing: PASS")
    print("25-entry atomic queue arithmetic: PASS")
    print("parallelism and serialization guards: PASS")
    print("scientific/B4/production admissions: 0")


if __name__ == "__main__":
    main()
