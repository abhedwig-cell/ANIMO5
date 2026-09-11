#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3B10R2 persisted rereview evidence.

This validator deliberately does not pretend to replay the frozen source archive: the
archive is not committed because redistribution rights are not established. The
independent reviewer-local source replay is recorded in the evidence matrix. CI checks
that the persisted rereview, immutable pins, boundaries and remediation contract are
internally consistent and that B3B10R has not been rewritten.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3B10R2_STATUS.json"
MATRIX_PATH = ROOT / "integration/animo-b3/ANIMO-B3B10R2_EVIDENCE_MATRIX.json"
CHECKPOINT_PATH = ROOT / "integration/animo-b3/ANIMO-B3B10R2_CHECKPOINT.json"
DOC_PATH = ROOT / "docs/b3/ANIMO_B3B10R2_TCD031_TARGETED_INDEPENDENT_REREVIEW.md"
E1_STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3B10E1_STATUS.json"
E1_MANIFEST_PATH = ROOT / "integration/animo-b3/ANIMO-B3B10E1_MANIFEST.json"
R1_STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3B10R_STATUS.json"

EXPECTED_START = "8522752f9941e6fd5b421cf5ac4ef839384d7ce7"
EXPECTED_CHECKPOINT = "a20325d819c92bc49aebafd720ad045c635fb5f1"
EXPECTED_DISPOSITION = "PASS_TARGETED_INDEPENDENT_REREVIEW_TCD031_SOURCE_PROVENANCE_GATES_CLOSED"
EXPECTED_ARCHIVE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_INDEX = "be4182c7438650f86399f912c57bbad42adf71fc362b694537f2db4d64c816fc"
EXPECTED_TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"

EXPECTED_MEMBERS = {
    "mapoinput.for": "081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065",
    "Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058",
    "Output_Init.for": "6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f",
    "Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
    "MAPOTRANSPORT.FOR": "735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da",
    "Transca.for": "7f31150050bd41aef203587818cde94cf689e6288094b2ad84aea34732b07ff9",
    "Transgen.for": "cd5efa76c1a4840b50901ee5015940b74c5fe4df79aca43d53a4a4cb77b9fecb",
    "input1.for": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95",
    "Hydro_detailed.for": "f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d",
}

EXPECTED_PINS = {
    "ANIMO-B3B10": "eccba6712f65455161d05fa9cdf6aa142f823dd4",
    "ANIMO-B3B10R": "36aad892cac546105dfec0fe43aa34a18e23bcad",
    "ANIMO-B3Q01": "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
    "ANIMO-GOV03": "cbd262bdabe92923113b7326f2f42822ce9a971c",
    "ANIMO-GOV04": "1bbe4c211197590f346803106e45dca5faae79fc",
    "ANIMO-MASSQ02": "56a11b524d03c33ee4ab9b1cd13b2cd523d543fc",
    "ANIMO-MP01": "7b5979dd6301b9d55d23e8c22948a0dba24b229b",
    "ANIMO-MP02": "6b0f2e7470f13baeb6612b0bddb662a497dea528",
    "ANIMO-STATEQ03": "10c50e65d1369d5f3b26736c4b12d3a482379eb5",
    "ANIMO-STATEQ04": "ef9a5998cafae433deeba701a8e9a8a08eacc92f",
}

EXPECTED_PROBE_IDS = {
    "SRC-MAPO-001", "SRC-MAPO-002", "SRC-MAPO-003", "SRC-MAPO-004",
    "SRC-OUTINIT-001", "SRC-OUTINIT-002", "SRC-ANIMO-001",
    "SRC-INIT-001", "SRC-INIT-002", "SRC-RSCOMP-001", "SRC-RSCOMP-002",
    "SRC-HYDRO-001", "SRC-HYDRO-002", "SRC-HYDRO-003",
    "SRC-ITREC-001", "SRC-ITREC-002",
}


def die(msg: str) -> None:
    raise AssertionError(msg)


def load(path: Path) -> dict:
    if not path.is_file():
        die(f"missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, msg: str) -> None:
    if not condition:
        die(msg)


def main() -> int:
    status = load(STATUS_PATH)
    matrix = load(MATRIX_PATH)
    checkpoint = load(CHECKPOINT_PATH)
    e1_status = load(E1_STATUS_PATH)
    e1_manifest = load(E1_MANIFEST_PATH)
    r1_status = load(R1_STATUS_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.is_file() else ""

    require(status["workunit"] == "ANIMO-B3B10R2", "wrong status workunit")
    require(matrix["workunit"] == "ANIMO-B3B10R2", "wrong matrix workunit")
    require(status["tcd"] == matrix["tcd"] == "TCD-031", "wrong TCD")
    require(status["exact_starting_head"] == matrix["exact_starting_head"] == EXPECTED_START,
            "starting head changed")
    require(status["persist_early_checkpoint_commit"] == matrix["persist_early_checkpoint"] == EXPECTED_CHECKPOINT,
            "persist-early checkpoint pin changed")
    require(checkpoint["exact_starting_head"] == EXPECTED_START, "checkpoint base changed")
    require(checkpoint["checkpoint_status"] == "IN_PROGRESS_FAIL_CLOSED", "checkpoint history changed")

    require(status["review_disposition"] == matrix["targeted_rereview_disposition"] == EXPECTED_DISPOSITION,
            "rereview disposition mismatch")
    require(status["independent_tier_c_review_gate"] == "PASSED", "Tier-C review gate not passed")
    require(status["gov04_risk_tier"] == "TIER_C", "risk tier changed")
    require(status["scientific_falsification"] is False, "unexpected scientific falsification")

    provenance = matrix["archive_provenance"]
    require(provenance["archive_sha256"] == EXPECTED_ARCHIVE, "archive SHA mismatch")
    require(provenance["archive_sha256_independently_recomputed"] is True, "archive not independently replayed")
    require(provenance["source_member_count"] == 63, "source-member count mismatch")
    require(provenance["source_member_index_sha256"] == EXPECTED_INDEX, "source index SHA mismatch")
    require(provenance["source_member_index_independently_recomputed"] is True, "source index not independently replayed")
    require(provenance["testbank_sha256"] == EXPECTED_TESTBANK, "testbank SHA mismatch")
    require(provenance["testbank_sha256_independently_recomputed"] is True, "testbank not independently replayed")
    require(provenance["mechanical_binding_result"] == "PASS_ARCHIVE_HASH_TO_MEMBER_HASH_TO_NORMALIZED_SLICE_HASH_TO_PROBE_CLAIM",
            "mechanical provenance chain not closed")
    require(provenance["claim_records_depend_only_on_hand_transcription"] is False,
            "hand transcription is being treated as primary evidence")
    require(provenance["repository_visible_primary_source"] is False, "source archive unexpectedly treated as repository primary source")
    require(provenance["redistribution_rights_established"] is False, "redistribution rights were silently upgraded")

    require(matrix["relevant_member_hashes"] == EXPECTED_MEMBERS, "requested member hashes changed")
    slices = matrix["normalized_probe_slice_replay"]
    require(slices.get("all_committed_probe_slice_hashes_match_independent_replay") is True,
            "probe-slice replay not complete")
    require(EXPECTED_PROBE_IDS.issubset(slices.keys()), "required probe ids missing")

    gates = matrix["failed_gate_rereview"]
    for name in (
        "complete_source_level_ownership",
        "native_mapoinput_loader",
        "native_Output_Init_serialization_omission",
        "native_Animo_Output_Init_call_surface",
        "native_Init_restore_direction_and_timing",
        "native_RsCoMp_pre_promotion_initialization",
    ):
        require(gates[name]["status"] == "PASS", f"targeted gate not PASS: {name}")
    require(gates["native_RsCoMp_pre_promotion_initialization"]["answer"] == "NO",
            "RsCoMp pre-promotion answer must be exact NO, not UNKNOWN")

    ownership = matrix["ownership_reconstruction"]
    require(ownership["result"] == "PASS" and ownership["ownership_ambiguity"] is False,
            "ownership remains ambiguous")
    require(matrix["persistent_state_count"] == {
        "domains": [1, 2],
        "p_off_scalar_count": 8,
        "p_on_scalar_count": 12,
        "phosphorus_condition": "IPO.EQ.1",
        "result": "PASS",
    }, "persistent state count/condition changed")
    require(matrix["atomic_correction"]["identity"] ==
            "COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY",
            "atomic correction identity changed")
    require(matrix["atomic_correction"]["result"] == "PASS", "atomicity not passed")

    reuse = matrix["reused_prior_pass_gates"]
    require(reuse["pins"] == EXPECTED_PINS, "reused evidence pins changed")
    require(reuse["source_and_testcase_identity_unchanged"] is True, "source/testcase identity changed")
    require(reuse["claim_scope_unchanged"] is True, "claim scope changed")
    require(reuse["no_superseding_or_contradictory_evidence_found"] is True,
            "superseding/contradictory evidence unresolved")
    for gate_name, gate_state in reuse["gates"].items():
        require(gate_state.startswith("REUSED_PASS_EXACT_PIN_UNCHANGED"),
                f"reuse regression guard failed: {gate_name}")

    require(matrix["historical_B2"]["active_macropore_B2_reference"] == "ABSENT", "historical B2 state changed")
    require(matrix["historical_B2"]["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN",
            "historical unknown boundary lost")
    require(matrix["whole_model_boundary"]["whole_model_active_production_split_equivalence"] == "NOT_PROVEN",
            "whole-model boundary overclaimed")
    require(matrix["stateq04"]["reopen_required"] is False, "STATEQ04 unexpectedly reopened")
    require(matrix["gov04"]["risk_tier"] == "TIER_C", "matrix risk tier changed")
    require(matrix["tcd025_boundary"]["executed_here"] is False and matrix["tcd025_boundary"]["composition_here"] is False,
            "TCD-025 scope creep")

    require(e1_status["disposition"] == "QUALIFIED_SOURCE_PROVENANCE_REMEDIATION_READY_FOR_TARGETED_INDEPENDENT_REREVIEW",
            "B3B10E1 remediation disposition changed")
    require(e1_status["scientific_admission"] is False, "B3B10E1 unexpectedly admitted science")
    require("not a scientific review PASS" in e1_status["ci_interpretation"], "B3B10E1 CI boundary lost")
    require(e1_manifest["exact_starting_head"] == "36aad892cac546105dfec0fe43aa34a18e23bcad",
            "B3B10E1 no longer rooted at B3B10R")
    require(e1_manifest["frozen_source_archive"]["sha256"] == EXPECTED_ARCHIVE,
            "B3B10E1 archive pin changed")
    require(e1_manifest["generated_artifacts"]["SOURCE_MEMBER_INDEX.json"] == EXPECTED_INDEX,
            "B3B10E1 source-index artifact pin changed")

    require(r1_status["review_disposition"] == "REMEDIATION_REQUIRED", "original B3B10R was rewritten")
    require(r1_status["review_status"] == "COMPLETE_FAIL_CLOSED", "original B3B10R historical state changed")
    require(r1_status["scientific_falsification"] is False, "original B3B10R falsification state changed")
    require(set(r1_status["failure_classification"]) == {"EVIDENCE_INSUFFICIENCY", "PROVENANCE_INSUFFICIENCY"},
            "original B3B10R failure classification changed")

    status_guards = status["scope_guards"]
    require(all(v is False for v in status_guards.values()), "one or more status scope guards violated")
    matrix_guards = matrix["scope_guards"]
    require(all(v is False for v in matrix_guards.values()), "one or more matrix scope guards violated")
    require(status["admission"]["B3_admission_performed"] is False, "B3 admission performed in rereview")
    require(status["whole_model_active_production_split_equivalence"] == "NOT_PROVEN", "status whole-model boundary overclaimed")
    require(status["historical_revision53_active_macropore_restart_behaviour"] == "UNKNOWN", "status historical boundary overclaimed")

    required_doc_strings = (
        EXPECTED_DISPOSITION,
        "whole-model active production split equivalence = NOT PROVEN",
        "B3 admission: `NOT YET PERFORMED`",
        "Production patch: `NOT PERFORMED`",
        "historical revision-53 active macropore restart behaviour = UNKNOWN",
        "COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY",
        "Native `RsCoMp*` pre-promotion initialization: PASS, answer NO",
    )
    for text in required_doc_strings:
        require(text in doc, f"required review-document boundary missing: {text}")

    archive_name = "ANIMO_4.1.5.53(3).zip"
    committed_archive_candidates = [p for p in ROOT.rglob(archive_name) if p.is_file()]
    require(not committed_archive_candidates, "frozen source archive must not be committed by B3B10R2")

    print("PASS_B3B10R2_TARGETED_INDEPENDENT_REREVIEW_PACKAGE")
    print(f"disposition={EXPECTED_DISPOSITION}")
    print("ci_boundary=persisted-package-and-pins-only; independent source replay is not replaced by CI")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL_CLOSED_B3B10R2: {exc}", file=sys.stderr)
        raise SystemExit(1)
