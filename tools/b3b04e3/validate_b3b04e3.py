#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "integration/animo-b3/b3b04e3/TCD040_RECONSTRUCTED_REPLAY_RESULT.json"
COMPARISON = ROOT / "integration/animo-b3/b3b04e3/TCD040_RECONSTRUCTED_REPLAY_COMPARISON.json"
MANIFEST = ROOT / "integration/animo-b3/b3b04e3/TCD040_RECONSTRUCTED_REPLAY_MANIFEST.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B04E3_STATUS.json"
GENERATOR = ROOT / "tools/b3b04e3/run_reconstructed_replay.py"
COMPARATOR = ROOT / "tools/b3b04e3/compare_reconstructed_replay.py"
DOC = ROOT / "docs/b3/TCD040_RECONSTRUCTED_REPLAY_E3.md"

EXPECTED_SOURCE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_CK282 = "833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e"
EXPECTED_CORE = "73b705924f4932dcca65aaa0a1eef90097aba0b6"

errors: list[str] = []

def req(cond: bool, message: str) -> None:
    if not cond:
        errors.append(message)

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

for path in [RESULT, COMPARISON, MANIFEST, STATUS, GENERATOR, COMPARATOR, DOC]:
    req(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

if errors:
    for e in errors:
        print("FAIL:", e)
    raise SystemExit(1)

result = json.loads(RESULT.read_text())
cmp = json.loads(COMPARISON.read_text())
manifest = json.loads(MANIFEST.read_text())
status = json.loads(STATUS.read_text())
generator_text = GENERATOR.read_text()
comparator_text = COMPARATOR.read_text()
doc_text = DOC.read_text()

req(status["workunit"] == "ANIMO-B3B04E3" and status["target"] == "TCD-040", "wrong status identity")
req(status["base"].endswith("01e6df610d236bac19d17f16d109a4e0e676ccfa"), "wrong E2 base")
req(status["harness_source_commit"] == EXPECTED_CORE, "wrong harness source commit")
req(status["decision"] == "RECONSTRUCTED_REPLAY_IMPLEMENTED_SESSION_LOCAL_SEMANTIC_MATCH_CONTROLLED_B0_CUSTODY_PENDING", "wrong workunit decision")

req(result["workunit"] == "ANIMO-B3B04E3" and result["target"] == "TCD-040", "wrong result identity")
req(result["frozen_b0"]["source_sha256"] == EXPECTED_SOURCE, "wrong source pin")
req(result["frozen_b0"]["testbank_sha256"] == EXPECTED_TESTBANK, "wrong testbank pin")
req(result["generator_expected_scientific_results_loaded"] is False, "generator expected-result quarantine failed")
req(result["execution_context"]["controlled_immutable_B0_storage_proven"] is False, "local bytes promoted to controlled custody")
req(result["execution_context"]["independent_replay_qualified"] is False, "local replay promoted to independent qualification")
req(result["continuous"]["records"] == 1800, "wrong continuous record count")
req(result["split282"]["stageA_records"] == 564, "wrong split282 Stage-A count")
req(result["split282"]["checkpoint"]["file_sha256"] == EXPECTED_CK282, "split282 checkpoint hash changed")
req(result["split282"]["checkpoint"]["file_size_bytes"] == 48 and result["split282"]["checkpoint"]["payload_size_bytes"] == 40, "checkpoint serialization changed")
req(result["split282"]["corrected_restore_full_trace_exact"] is True, "corrected restore not exact")
req(result["split282"]["defective_comparison"]["changed_records"] == 1236, "wrong defective changed record count")
first = result["split282"]["defective_comparison"]["first_divergence"]
req(first["record_index"] == 564 and first["step"] == 283 and first["phase"] == 0, "wrong first divergence topology")
req({(x[0], x[1]) for x in first["coordinates"]} == {(n, 0) for n in ["NH4","NO3","DOM","DON","DOP"]}, "wrong first divergence coordinates")
req(result["split282"]["Copo0_modified_at_boundary"] is False, "Copo layer0 control modified")
req(result["split67_zero_control"]["stageA_records"] == 134, "wrong split67 Stage-A count")
req(result["split67_zero_control"]["checkpoint"]["all_exact_positive_zero"] is True, "split67 checkpoint not exact zero")
req(result["split67_zero_control"]["defective_zero_application_full_trace_exact"] is True, "split67 zero operation not identity")
req(result["trace_schema"]["original_B3B04_trace_serializer_reconstructed"] is False, "original trace serializer overclaim")

req(cmp["result"] == "PASS_B3B04E3_RECONSTRUCTED_REPLAY_SEMANTICS", "persisted comparison did not pass")
req(cmp["failures"] == [] and cmp["scientific_semantic_match"] is True, "comparison contains failures")
req(cmp["original_trace_serialization_bytes_reconstructed"] is False, "comparison overclaims original trace recovery")

req(manifest["harness_source_commit"] == EXPECTED_CORE, "manifest core commit mismatch")
req(manifest["generated_artifacts_not_republished"] == result["generated_artifacts"], "artifact hash manifest differs from result")
req(manifest["authoring_execution"]["controlled_immutable_B0_storage_proven"] is False, "manifest custody overclaim")
req(manifest["authoring_execution"]["independent_replay_qualified"] is False, "manifest independent qualification overclaim")
for rel, expected in manifest["harness_content_sha256"].items():
    req(sha(ROOT / rel) == expected, f"harness content hash mismatch: {rel}")

# Generator must not know any frozen expected output values or the E1 target file.
for forbidden in [
    "TCD040_REPLAY_EXPECTATIONS",
    EXPECTED_CK282,
    "29055b1be962d9550781b87f56ab34cd44630965439e21b6e5375954a6144a48",
    "920cc04388d812e5668edab3e654b7e006926522bbe61923b1a202b346cf4e38",
]:
    req(forbidden not in generator_text, f"expected-result leakage into generator: {forbidden}")
req("TCD040_REPLAY_EXPECTATIONS" in comparator_text, "comparator does not clearly hold expected-result boundary")

for key, value in status["qualification_boundaries"].items():
    req(value is False, f"qualification boundary widened: {key}")
req(status["ci"]["fresh_B0_replay_in_public_CI"] is False, "CI falsely claims fresh B0 replay")
req("NOT_QUALIFIED_FOR_INDEPENDENT_REPLAY" in doc_text, "documentation missing independent-replay boundary")
req("ANIMO-EG01" in doc_text, "documentation missing EG01 blocker")

if errors:
    print("B3B04E3 validation FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)
print("PASS_B3B04E3_RECONSTRUCTED_REPLAY_PACKAGE")
