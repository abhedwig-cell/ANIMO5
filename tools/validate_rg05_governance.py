#!/usr/bin/env python3
"""Fail-closed structural validator for ANIMO-RG05.

RG05 is governance-only. This validator checks frozen identity, authority heads,
non-admission, queue arithmetic, TCD-042 child/domain governance and serialized
gate ownership. It does not infer scientific truth from integration.
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
EXPECTED_HEADS = {
    "B3I05": "7fa0162415e02a6f0167e71b48ae38177a9e06e0",
    "NQ03": "8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6",
    "NQ03R": "0153779e9045c6527b7c31156f2295ff44b57eeb",
    "IO02": "ea2a5fcce7baaddb80b02fe6ca4334e262f3d60d",
    "B3A04": "5eaf02298603b85f802d8e35d6a63941d0878879",
    "B3A04R": "27b1700a330959d1b5eae23a2094cad579630f14",
    "B3B02": "690868409aae11297c966eb55419f62ff977c619",
    "B3B03": "446f57f3aeff6e7db56ce473f0724bdb58cad94f",
    "B3B03R_TECH": "02ce1f49582d2b8cb794c3bfb9d674481a2eea1e",
    "B3B03R_HANDOFF": "11db97289ffafdd6281b83f0aa0e96b544d6eb5a",
    "B3B04": "19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865",
    "B3E01": "41e43c6a6888aac5b5b52041bcdd088c7afc68f1",
    "B3Q02": "1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3",
    "UBQ03": "ca55248f2382000288488659571b645fd5a8043b",
    "B3I06": "8f01f0cb366dfa8cc63a184d6f885100899a8cd9",
}


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

    # Identity and governance-only boundary.
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
    assert all(value is False for value in status["admission_state"].values())
    assert status["gate_snapshot"]["G7"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS"
    assert status["gate_snapshot"]["B4"] == "NOT_ADMITTED"
    assert status["gate_snapshot"]["PRODUCTION"] == "NOT_ADMITTED"

    # Historical route must remain fail closed.
    hist = status["historical_route"]
    assert hist["historical_reference_artifact_obtained"] is False
    assert hist["external_archival_or_provenance_action_sent"] is False
    assert hist["G6H"] == "HISTORICAL_B2_NOT_PASSED_INTERNAL_RECOVERY_STOPPED"
    assert hist["G6U"] == "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT"
    assert hist["forbidden_reclassification"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT"
    assert "does **not** mean historical reference acquisition has been exhausted" in doc
    assert "NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT" in doc

    # Live authority freeze.
    snap = status["authority_snapshot_pre_validation"]
    assert snap["RG04"] == RG04_HEAD
    assert snap["B3I03_REGISTER"] == REGISTER_HEAD
    assert snap["canonical_tcd_register_tail"] == "TCD-042"
    for key, expected in EXPECTED_HEADS.items():
        assert snap[key] == expected, (key, snap.get(key), expected)

    # TCD-042 parent/child/domain governance.
    t42 = status["tcd042"]
    assert t42["canonical_top_level_parent"] == "TCD-042"
    assert t42["canonical_register_tail"] == "TCD-042"
    assert t42["tcd_043_reserved"] is False
    assert t42["shared_domain_owner"] == "TCD-042_HETOP_ZERO_DOMAIN"
    assert "Hetop=0" in t42["shared_domain_finding"]
    assert "documented" in t42["shared_domain_finding"]
    assert t42["child_disposition_carrier"] == "QUALIFIED_ADDITIVE_CANONICAL_CHILD_ATOM_DISPOSITION_CARRIER_NO_ADMISSION"
    assert t42["zero_thickness_characterization"] == "QUALIFIED_CHARACTERIZATION_HETOP_ZERO_PARSER_ADMISSIBLE_CONDITIONALLY_UNDEFINED_NO_GLOBAL_ZERO_THICKNESS_POLICY"
    assert t42["zero_thickness_intake"] == "QUALIFIED_UBQ03_INCREMENTAL_INTAKE_RUNTIME_INPUT_DOMAIN_HAZARD_NO_NEW_TCD_NO_ADMISSION"
    assert set(t42["children"]) == {"TCD-042-B1", "TCD-042-E1"}
    assert t42["children"]["TCD-042-B1"].startswith("PARTIAL_TCD042_B1_CLASS_B_READINESS")
    assert t42["children"]["TCD-042-E1"].startswith("PARTIAL_TCD042_E1_CLASS_E_READINESS")

    # Authority table is strict and admission-free.
    auth = {r["workunit"]: r for r in authority_rows}
    required_auth = {
        "RG04", "GOV02", "PREP02R", "STATEQ02", "B3I04", "MASSQ02",
        "B3I03", "B3I03-REGISTER", "UBQ01", "UBQ02", "B3I05",
        "B3B01", "B3A01", "B3A02", "B3A03", "B3A03R", "NQ02",
        "TIME02", "IO01", "ARCHG02", "ARCH05", "NQ03", "NQ03R", "IO02",
        "B3A04", "B3A04R", "B3B02", "B3B03", "B3B03R-TECH",
        "B3B03R-HANDOFF", "B3B04", "B3E01", "B3Q02", "UBQ03", "B3I06",
    }
    assert required_auth.issubset(auth)
    for row in authority_rows:
        for col in ("realized", "persisted", "tested", "qualified", "admitted"):
            as_bool(row[col])
        assert as_bool(row["admitted"]) is False
        assert row["production_effect"] == "NONE"

    for key in ("B3I05", "NQ03", "NQ03R", "IO02", "B3A04", "B3A04R",
                "B3B03", "B3B04", "B3E01", "B3Q02", "UBQ03", "B3I06"):
        snap_key = key
        if key == "B3A04R":
            expected = EXPECTED_HEADS["B3A04R"]
        else:
            expected = EXPECTED_HEADS[key]
        assert auth[key]["current_head"] == expected
        assert auth[key]["qualified"] == "True"
    assert auth["B3B02"]["current_head"] == EXPECTED_HEADS["B3B02"]
    assert auth["B3B02"]["qualified"] == "False"
    assert auth["B3B02"]["current_state"].startswith("PARTIAL_TCD042_B1_CLASS_B_READINESS")
    assert auth["B3Q02"]["current_state"] == "QUALIFIED_ADDITIVE_CANONICAL_CHILD_ATOM_DISPOSITION_CARRIER_NO_ADMISSION"
    assert auth["UBQ03"]["current_state"] == "QUALIFIED_CHARACTERIZATION_HETOP_ZERO_PARSER_ADMISSIBLE_CONDITIONALLY_UNDEFINED_NO_GLOBAL_ZERO_THICKNESS_POLICY"
    assert auth["B3I06"]["current_state"] == "QUALIFIED_UBQ03_INCREMENTAL_INTAKE_RUNTIME_INPUT_DOMAIN_HAZARD_NO_NEW_TCD_NO_ADMISSION"
    assert "not independent" in auth["B3A04R"]["authority_basis"]

    # Gate matrix.
    gates = {r["gate"]: r for r in gate_rows}
    for gate in ("G6H", "G6U", "G7", "GSTATE", "GTIME", "GMASS", "GEX",
                 "GARCH", "TCD042_PARENT", "B4_PROFILE", "PRODUCTION"):
        assert gate in gates
    assert gates["G6H"]["state"] == hist["G6H"]
    assert gates["G6U"]["state"] == hist["G6U"]
    assert gates["G7"]["state"] == "NO_ATOMIC_SCIENTIFIC_ADMISSIONS"
    assert "B3Q02" in gates["G7"]["qualified_basis"]
    assert "UBQ03" in gates["G7"]["qualified_basis"]
    assert "B3I06" in gates["G7"]["qualified_basis"]
    assert gates["TCD042_PARENT"]["state"] == "WAITING_ON_CHILDREN"
    assert "theory/provenance" in gates["TCD042_PARENT"]["remaining_dependencies"]
    assert gates["B4_PROFILE"]["state"] == "NOT_ADMITTED"
    assert gates["PRODUCTION"]["state"] == "NOT_ADMITTED"

    # Queue identity and arithmetic.
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

    e26 = next(e for e in entries if e["tcd"] == "TCD-026")
    assert e26["queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW"
    assert "B3A04R" in e26["owners"]
    e40 = next(e for e in entries if e["tcd"] == "TCD-040")
    assert e40["queue_state"] == "WAITING_ON_ROUTE_AND_REVIEW"
    assert "unconditionally" in e40["next_action"]
    e42 = next(e for e in entries if e["tcd"] == "TCD-042")
    assert e42["queue_state"] == "WAITING_ON_CHILDREN"
    assert {"B3Q02", "UBQ03", "B3I06"}.issubset(set(e42["owners"]))
    blockers42 = " ".join(e42["blockers"])
    assert "no global zero-thickness policy" in blockers42
    assert "creates no new child or top-level TCD" in blockers42
    assert "resolves the formal child-carrier governance gap" in blockers42
    children = {c["id"]: c for c in e42["children"]}
    assert children["TCD-042-B1"]["state"] == "WAITING_ON_THEORY"
    assert children["TCD-042-E1"]["state"] == "WAITING_ON_THEORY"

    # Parallelism/serialization.
    streams = {r["stream"]: r for r in parallel_rows}
    required_streams = {
        "historical_external_acquisition", "exact_zero_upper_reservoir",
        "finite_positive_upper_reservoir", "tcd042_zero_thickness_domain",
        "child_atom_disposition_carrier", "nq03_independent_review",
        "slow_langmuir_index", "nonlinear_p_policy", "exudate_initial_ledger",
        "layer0_restart_identity", "general_input_contract",
        "completed_readiness_reviews", "canonical_state_gate", "canonical_time_gate",
        "canonical_mass_gate", "canonical_exchange_gate", "tcd042_parent",
        "b4_profile", "production",
    }
    assert required_streams.issubset(streams)
    assert streams["tcd042_zero_thickness_domain"]["workunit"] == "UBQ03+B3I06"
    assert streams["tcd042_zero_thickness_domain"]["parallel_class"] == "SHARED_SEMANTIC_OWNER"
    assert streams["tcd042_zero_thickness_domain"]["current_state"] == "QUALIFIED_CHARACTERIZATION_AND_INTAKE_MODEL_SEMANTICS_UNRESOLVED"
    assert streams["child_atom_disposition_carrier"]["workunit"] == "B3Q02"
    assert streams["child_atom_disposition_carrier"]["parallel_class"] == "SAFE_PARALLEL"
    assert "READINESS_ONLY" in streams["child_atom_disposition_carrier"]["guards"]
    assert streams["exudate_initial_ledger"]["workunit"] == "B3A04+B3A04R"
    assert "not independent" in streams["exudate_initial_ledger"]["guards"]
    assert streams["general_input_contract"]["current_state"] == "QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS"
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

    # Closeout-state self-consistency.
    if status["work_status"]["qualified"]:
        expected_state = "QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS"
        assert status["state"] == expected_state
        assert status["decision"] == expected_state
        assert status["work_status"]["tested"] is True
        assert status["work_status"]["work_unit_complete"] is True
        assert status["validation"]["validator_result"] == "PASS"
        assert status["validation"]["github_actions_conclusion"] == "success"
        assert status["validation"]["scope_guard"] == "PASS"
    else:
        assert status["state"] == "IN_PROGRESS_PERSISTED_POST_CLOSEOUT_DELTA_REVALIDATION_PENDING"
        assert status["decision"] == "PENDING_FAIL_CLOSED_REVALIDATION"
        assert status["work_status"]["tested"] is False
        assert status["work_status"]["work_unit_complete"] is False

    print("ANIMO-RG05 governance validator: PASS")
    print("final live authority freeze incl. B3A04R/B3Q02/UBQ03/B3I06: PASS")
    print("frozen B0 identity and governance-only scope: PASS")
    print("G6H/G6U fail-closed historical route: PASS")
    print("TCD-042 child carrier + zero-thickness characterization/intake: PASS")
    print("25-entry queue arithmetic and TCD-043 non-reservation: PASS")
    print("parallelism and serialized owner gates: PASS")
    print("scientific/B4/production admissions: 0")


if __name__ == "__main__":
    main()
