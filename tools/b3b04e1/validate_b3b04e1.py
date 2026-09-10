#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3B04E1.

Two modes are deliberately distinct:

* default gate: succeeds only when the complete reconstructed replay can be
  executed from provenance-qualified B0 and all replay assertions pass;
* --audit-blocked-state: succeeds only when the repository truthfully records
  that the reconstructed replay is complete locally while controlled immutable
  B0 acquisition is still unproven.

A green blocked-state audit is not evidence qualification. No numerical
tolerance is used anywhere in this validator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

BASE_SHA = "bb001129578457ca8435e39deb2b8586e7ebc6a2"
STATUS_BLOCKED = "FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN"
STATUS_QUALIFIED = "QUALIFIED_EVIDENCE_REPLAYABILITY_ONLY"
DECISION_BLOCKED = "EVIDENCE_REPLAYABILITY_NOT_QUALIFIED"
DECISION_QUALIFIED = "EVIDENCE_REPLAYABILITY_QUALIFIED"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
GUIDE_SHA = "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"
CHECKPOINT_SHA = "833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e"
RECON_CONTINUOUS_SHA = "6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3"
RECON_DEFECTIVE_SHA = "d93ec85c00c9f026d1d215d5aea250192d250775ee1433a7b3754cb090590388"
TARGET_COORDS = ["Conh(0)", "Coni(0)", "Codiorma(0)", "Codiorni(0)", "Codiorpo(0)"]
SOURCE_MEMBERS = {
    "ANIMO_4.1.5.53/Inicalc.for": "306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1",
    "ANIMO_4.1.5.53/input1.for": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95",
    "ANIMO_4.1.5.53/Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058",
    "ANIMO_4.1.5.53/Output_Init.for": "6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f",
    "ANIMO_4.1.5.53/Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
}
REQUIRED_REPLAY_PATHS = [
    "tools/b3b04e1/replay_tcd040.py",
    "integration/animo-b3/b3b04e1/RECONSTRUCTED_REPLAY_LOCAL_RESULT.json",
    "integration/animo-b3/b3b04e1/REPLAY_MANIFEST.json",
]
ALLOWED_CHANGE_PREFIXES = (
    ".github/workflows/animo-b3b04e1-",
    "docs/b3/TCD040_EVIDENCE_REMEDIATION",
    "docs/b3/TCD040_REPLAY_INSTRUCTIONS",
    "integration/animo-b3/ANIMO-B3B04E1_STATUS.json",
    "integration/animo-b3/b3b04e1/",
    "tools/b3b04e1/",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check(condition: bool, code: str, detail: str, failures: list[dict[str, str]]) -> None:
    if not condition:
        failures.append({"code": code, "detail": detail})


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def valid_artifact(path: Path | None, expected: str) -> bool:
    return path is not None and path.is_file() and sha256_file(path) == expected


def check_artifact(path: Path | None, expected: str, code: str, failures: list[dict[str, str]]) -> None:
    if path is None:
        failures.append({"code": code, "detail": "artifact path not supplied"})
        return
    if not path.is_file():
        failures.append({"code": code, "detail": f"artifact absent: {path}"})
        return
    actual = sha256_file(path)
    check(actual == expected, code, f"SHA-256 mismatch: {actual}", failures)


def controlled_storage_proven(register: dict, failures: list[dict[str, str]]) -> None:
    by_id = {item["evidence_id"]: item for item in register.get("artifacts", [])}
    for evidence_id in ["ANIMO-B0-SRC-41553-R53", "ANIMO-B0-TB-202609", "ANIMO-B0-DOC-UG40-2005"]:
        item = by_id.get(evidence_id)
        if item is None:
            failures.append({"code": "B0_EVIDENCE_ID_ABSENT", "detail": evidence_id})
            continue
        cs = item.get("controlled_storage", {})
        ok = (
            cs.get("status") == "PROVEN_CONTROLLED_IMMUTABLE"
            and bool(cs.get("primary_storage_record_id"))
            and bool(cs.get("secondary_storage_record_id"))
            and bool(cs.get("immutability_proof_reference"))
            and cs.get("post_ingest_sha256_verified") is True
            and cs.get("secondary_copy_sha256_verified") is True
            and cs.get("restore_test_passed") is True
            and bool(cs.get("custodian_approval_reference"))
        )
        check(ok, "B0_CONTROLLED_IMMUTABLE_ACQUISITION_NOT_PROVEN", evidence_id, failures)


def verify_source_members(source_zip: Path | None, failures: list[dict[str, str]]) -> None:
    if not valid_artifact(source_zip, SOURCE_SHA):
        return
    assert source_zip is not None
    try:
        with zipfile.ZipFile(source_zip) as zf:
            for member, expected in SOURCE_MEMBERS.items():
                try:
                    payload = zf.read(member)
                except KeyError:
                    failures.append({"code": "SOURCE_MEMBER_ABSENT", "detail": member})
                    continue
                actual = hashlib.sha256(payload).hexdigest()
                check(actual == expected, "SOURCE_MEMBER_SHA_MISMATCH", f"{member}: {actual}", failures)
    except zipfile.BadZipFile as exc:
        failures.append({"code": "SOURCE_ARCHIVE_INVALID", "detail": str(exc)})


def verify_grasspeat(repo_root: Path, testbank_zip: Path | None, failures: list[dict[str, str]]) -> None:
    if not valid_artifact(testbank_zip, TESTBANK_SHA):
        return
    assert testbank_zip is not None
    tool = repo_root / "tools/b3b04e1/extract_grasspeat_activation.py"
    if not tool.is_file():
        failures.append({"code": "GRASSPEAT_INSPECTOR_ABSENT", "detail": str(tool)})
        return
    result = subprocess.run(
        [sys.executable, str(tool), str(testbank_zip)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    check(result.returncode == 0, "GRASSPEAT_WITNESS_REPRODUCTION_FAILED", result.stdout.strip(), failures)


def verify_expectations(expectations: dict, failures: list[dict[str, str]]) -> None:
    split = expectations["split_282"]
    check(split["split_step"] * split["records_per_step"] == split["stage_a_records"],
          "SPLIT282_ARITHMETIC_MISMATCH", "split_step * records_per_step != stage_a_records", failures)
    check(900 * split["records_per_step"] == split["full_trace_records"],
          "TRACE_LENGTH_ARITHMETIC_MISMATCH", "900 * records_per_step != full_trace_records", failures)
    check(split["checkpoint_sha256_reported_by_b3b04"] == CHECKPOINT_SHA,
          "CHECKPOINT_TARGET_SHA_MISMATCH", str(split.get("checkpoint_sha256_reported_by_b3b04")), failures)

    raw_expected = split["checkpoint_binary64_little_endian_hex"]
    for name, value in split["checkpoint_values"].items():
        actual = struct.pack("<d", float(value)).hex()
        check(actual == raw_expected[name], "CHECKPOINT_RAW_BINARY64_MISMATCH", f"{name}: {actual}", failures)

    divergence = split["first_defective_divergence"]
    check(divergence == {
        "reported_record_index": 564,
        "step": 283,
        "phase": 0,
        "layer": 0,
        "coordinates": TARGET_COORDS,
    }, "FIRST_DIVERGENCE_EXPECTATION_MISMATCH", json.dumps(divergence, sort_keys=True), failures)

    check(split["continuous_trace_sha256"] == split["corrected_restore_trace_sha256"],
          "PRIOR_CORRECTED_FULL_TRACE_EXPECTATION_NOT_EXACT", "reported prior hashes differ", failures)
    zero = expectations["split_67_zero_control"]
    check(zero["full_trace_records"] == 1800,
          "SPLIT67_TRACE_LENGTH_EXPECTATION_MISMATCH", str(zero["full_trace_records"]), failures)
    check(zero["continuous_trace_sha256"] == zero["legacy_restart_trace_sha256"],
          "PRIOR_SPLIT67_NEGATIVE_CONTROL_EXPECTATION_MISMATCH", "reported prior hashes differ", failures)

    docs = expectations["documentation_contract"]
    check(docs.get("INITIAL.OUT") == "FORMATTED_RESTART_STYLE_REPRESENTATION",
          "INITIAL_OUT_CLASSIFICATION_MISMATCH", repr(docs.get("INITIAL.OUT")), failures)
    check(docs.get("B3B04_atomic_checkpoint_fixture") == "RAW_BYTE_IDENTITY_EVIDENCE",
          "ATOMIC_CHECKPOINT_CLASSIFICATION_MISMATCH", repr(docs.get("B3B04_atomic_checkpoint_fixture")), failures)
    check(docs.get("INITIAL.OUT_is_raw_byte_checkpoint") is False,
          "INITIAL_OUT_RAW_CHECKPOINT_FALSE_REQUIRED", repr(docs.get("INITIAL.OUT_is_raw_byte_checkpoint")), failures)


def verify_replay_bundle_presence(repo_root: Path, failures: list[dict[str, str]]) -> None:
    for rel in REQUIRED_REPLAY_PATHS:
        check((repo_root / rel).is_file(), "REPLAY_BUNDLE_COMPONENT_ABSENT", rel, failures)


def verify_manifest(manifest: dict, failures: list[dict[str, str]]) -> None:
    check(manifest.get("bundle_mode") == "DETERMINISTIC_RECONSTRUCTION_GENERATOR_PLUS_CRYPTOGRAPHIC_HASHES",
          "REPLAY_MANIFEST_MODE_MISMATCH", repr(manifest.get("bundle_mode")), failures)
    check(manifest.get("scope") == "EVIDENCE_REPLAYABILITY_ONLY",
          "REPLAY_MANIFEST_SCOPE_MISMATCH", repr(manifest.get("scope")), failures)
    inputs = manifest.get("frozen_inputs", {})
    check(inputs.get("source_archive_sha256") == SOURCE_SHA, "REPLAY_MANIFEST_SOURCE_SHA_MISMATCH", repr(inputs.get("source_archive_sha256")), failures)
    check(inputs.get("testbank_archive_sha256") == TESTBANK_SHA, "REPLAY_MANIFEST_TESTBANK_SHA_MISMATCH", repr(inputs.get("testbank_archive_sha256")), failures)
    check(inputs.get("user_guide_pdf_sha256") == GUIDE_SHA, "REPLAY_MANIFEST_GUIDE_SHA_MISMATCH", repr(inputs.get("user_guide_pdf_sha256")), failures)
    split = manifest.get("split_282", {})
    check(split.get("checkpoint_sha256") == CHECKPOINT_SHA and split.get("checkpoint_reproduces_prior_B3B04_hash") is True,
          "REPLAY_MANIFEST_CHECKPOINT_MISMATCH", repr(split.get("checkpoint_sha256")), failures)
    check(split.get("continuous_trace_sha256") == RECON_CONTINUOUS_SHA and split.get("corrected_restore_trace_sha256") == RECON_CONTINUOUS_SHA,
          "REPLAY_MANIFEST_CORRECTED_TRACE_MISMATCH", json.dumps(split, sort_keys=True), failures)
    check(split.get("defective_restart_trace_sha256") == RECON_DEFECTIVE_SHA,
          "REPLAY_MANIFEST_DEFECTIVE_TRACE_MISMATCH", repr(split.get("defective_restart_trace_sha256")), failures)
    zero = manifest.get("split_67_zero_control", {})
    check(zero.get("continuous_trace_sha256") == RECON_CONTINUOUS_SHA and zero.get("legacy_zeroing_trace_sha256") == RECON_CONTINUOUS_SHA and zero.get("full_1800_record_exact_negative_control") is True,
          "REPLAY_MANIFEST_SPLIT67_MISMATCH", json.dumps(zero, sort_keys=True), failures)
    docs = manifest.get("documentation_contract", {})
    check(docs.get("INITIAL.OUT") == "FORMATTED_RESTART_STYLE_REPRESENTATION" and docs.get("B3B04_atomic_checkpoint_fixture") == "RAW_BYTE_IDENTITY_EVIDENCE" and docs.get("INITIAL.OUT_is_raw_byte_checkpoint") is False,
          "REPLAY_MANIFEST_DOCUMENTATION_BOUNDARY_MISMATCH", json.dumps(docs, sort_keys=True), failures)
    gate = manifest.get("qualification_gate", {})
    check(gate.get("deterministic_generator_bundle_complete") is True and gate.get("local_reconstruction_passed") is True,
          "REPLAY_MANIFEST_LOCAL_GATE_INCOMPLETE", json.dumps(gate, sort_keys=True), failures)
    check(gate.get("canonical_tcd_status") == "UNRESOLVED_NOT_ADMITTED",
          "REPLAY_MANIFEST_TCD_STATUS_MISMATCH", repr(gate.get("canonical_tcd_status")), failures)


def verify_local_reconstruction(local: dict, failures: list[dict[str, str]]) -> None:
    check(local.get("evidence_class") == "RECONSTRUCTED_REPLAY_HARNESS_FOR_EXISTING_CLAIM_LOCAL_EXECUTION",
          "LOCAL_REPLAY_EVIDENCE_CLASS_MISMATCH", repr(local.get("evidence_class")), failures)
    check(local.get("qualification_status") == "LOCAL_RECONSTRUCTION_PASS_NOT_INDEPENDENTLY_PROVENANCED",
          "LOCAL_REPLAY_STATUS_MISMATCH", repr(local.get("qualification_status")), failures)
    check(local.get("new_scientific_claim_created") is False,
          "LOCAL_REPLAY_NEW_CLAIM_PROHIBITED", repr(local.get("new_scientific_claim_created")), failures)
    check(local.get("production_source_modified") is False and local.get("frozen_b0_modified") is False,
          "LOCAL_REPLAY_NONINTERFERENCE_REQUIRED", "production/frozen B0 modification flag", failures)

    split = local["split_282"]
    check(split.get("checkpoint_sha256") == CHECKPOINT_SHA and split.get("checkpoint_reproduces_prior_B3B04_sha256") is True,
          "LOCAL_CHECKPOINT_SHA_NOT_REPRODUCED", repr(split.get("checkpoint_sha256")), failures)
    check(split.get("stage_a_records") == 564 and split.get("continuous_trace_size_bytes") == 5464800,
          "LOCAL_SPLIT282_LENGTH_MISMATCH", "expected 564 Stage-A records and 5,464,800-byte full trace", failures)
    check(split.get("continuous_trace_sha256") == RECON_CONTINUOUS_SHA,
          "LOCAL_CONTINUOUS_TRACE_SHA_MISMATCH", repr(split.get("continuous_trace_sha256")), failures)
    check(split.get("corrected_restore_trace_sha256") == RECON_CONTINUOUS_SHA and split.get("corrected_restore_full_trace_exact") is True,
          "LOCAL_CORRECTED_TRACE_NOT_EXACT", repr(split.get("corrected_restore_trace_sha256")), failures)
    check(split.get("defective_restart_trace_sha256") == RECON_DEFECTIVE_SHA,
          "LOCAL_DEFECTIVE_TRACE_SHA_MISMATCH", repr(split.get("defective_restart_trace_sha256")), failures)

    raw = split.get("checkpoint_raw_little_endian_hex", {})
    expected_raw = {
        "Conh(0)": "d154eca7b66a4d3f",
        "Coni(0)": "9cea8abdf062e23e",
        "Codiorma(0)": "f8c17a4b6af2713f",
        "Codiorni(0)": "b4e1ea3e5e14203f",
        "Codiorpo(0)": "bb02ab6430bae93e",
    }
    check(raw == expected_raw, "LOCAL_CHECKPOINT_RAW_BYTES_MISMATCH", json.dumps(raw, sort_keys=True), failures)

    div = split.get("first_defective_divergence", {})
    differences = div.get("differences", [])
    check(div.get("record_index_zero_based") == 564 and div.get("step") == 283 and div.get("phase") == 0 and div.get("layer") == 0,
          "LOCAL_FIRST_DIVERGENCE_IDENTITY_MISMATCH", json.dumps(div, sort_keys=True), failures)
    check([item.get("coordinate") for item in differences] == TARGET_COORDS,
          "LOCAL_FIRST_DIVERGENCE_COORDINATES_MISMATCH", json.dumps(differences, sort_keys=True), failures)
    check(all(item.get("defective_raw_hex") == "0000000000000000" for item in differences),
          "LOCAL_FIRST_DIVERGENCE_ZERO_BYTES_MISMATCH", json.dumps(differences, sort_keys=True), failures)
    check(div.get("all_other_traced_coordinates_exact_at_first_divergence") is True and div.get("Copo_control_exact_at_first_divergence") is True,
          "LOCAL_NEGATIVE_CONTROL_AT_DIVERGENCE_FAILED", json.dumps(div, sort_keys=True), failures)

    zero = local["split_67_zero_control"]
    check(zero.get("stage_a_records") == 134 and zero.get("five_target_checkpoint_values_exact_positive_zero") is True,
          "LOCAL_SPLIT67_CHECKPOINT_CONTROL_FAILED", json.dumps(zero, sort_keys=True), failures)
    check(zero.get("legacy_zeroing_trace_sha256") == RECON_CONTINUOUS_SHA and zero.get("continuous_trace_sha256") == RECON_CONTINUOUS_SHA and zero.get("full_1800_record_exact_negative_control") is True,
          "LOCAL_SPLIT67_FULL_TRACE_CONTROL_FAILED", json.dumps(zero, sort_keys=True), failures)


def verify_documentation_provenance(repo_root: Path, failures: list[dict[str, str]]) -> None:
    instructions = (repo_root / "docs/b3/TCD040_REPLAY_INSTRUCTIONS.md").read_text(encoding="utf-8")
    remediation = (repo_root / "docs/b3/TCD040_EVIDENCE_REMEDIATION.md").read_text(encoding="utf-8")
    joined = instructions + "\n" + remediation
    for required in [
        "physical PDF page 59",
        "section 3.3",
        "INITIAL.OUT = FORMATTED_RESTART_STYLE_REPRESENTATION",
        "B3B04 atomic checkpoint fixture = RAW_BYTE_IDENTITY_EVIDENCE",
    ]:
        check(required in joined, "DOCUMENTATION_PROVENANCE_MARKER_ABSENT", required, failures)


def verify_scope(status: dict, repo_root: Path, require_git: bool, failures: list[dict[str, str]]) -> None:
    guards = status.get("scope_guards", {})
    required_false = [
        "tcd040_admitted", "production_source_patched", "B4_started",
        "canonical_STATE_admission_claimed", "TCD016_composed",
        "crop_restart_architecture_expanded", "central_regie_modified",
        "GOV03_historical_UNKNOWN_modified", "independent_second_line_review_performed",
        "new_scientific_claim_object_created",
    ]
    for key in required_false:
        check(guards.get(key) is False, "SCOPE_GUARD_FALSE_REQUIRED", key, failures)

    if not (repo_root / ".git").exists():
        if require_git:
            failures.append({"code": "GIT_SCOPE_CHECK_UNAVAILABLE", "detail": str(repo_root)})
        return
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{BASE_SHA}...HEAD"],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        failures.append({"code": "GIT_SCOPE_DIFF_FAILED", "detail": result.stdout.strip()})
        return
    changed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    disallowed = [path for path in changed if not path.startswith(ALLOWED_CHANGE_PREFIXES)]
    check(not disallowed, "SCOPE_GUARD_DISALLOWED_PATH", ", ".join(disallowed), failures)


def verify_executable_replay(
    repo_root: Path,
    source_zip: Path | None,
    testbank_zip: Path | None,
    local: dict,
    failures: list[dict[str, str]],
) -> None:
    if not (valid_artifact(source_zip, SOURCE_SHA) and valid_artifact(testbank_zip, TESTBANK_SHA)):
        return
    assert source_zip is not None and testbank_zip is not None
    tool = repo_root / "tools/b3b04e1/replay_tcd040.py"
    with tempfile.TemporaryDirectory(prefix="b3b04e1-replay-") as tmp:
        out = Path(tmp) / "replay"
        result = subprocess.run(
            [sys.executable, str(tool), str(source_zip), str(testbank_zip), str(out)],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        check(result.returncode == 0, "EXECUTABLE_REPLAY_FAILED", result.stdout[-8000:], failures)
        if result.returncode != 0:
            return
        generated_path = out / "TCD040_RECONSTRUCTED_REPLAY_RESULT.json"
        check(generated_path.is_file(), "EXECUTABLE_REPLAY_RESULT_ABSENT", str(generated_path), failures)
        if not generated_path.is_file():
            return
        generated = load_json(generated_path)
        split = generated["split_282"]
        variants = generated["variants"]
        zero = generated["split_67"]
        checks = [
            (split.get("checkpoint_sha256") == CHECKPOINT_SHA, "EXEC_REPLAY_CHECKPOINT_SHA_MISMATCH"),
            (split.get("stage_a_records") == 564, "EXEC_REPLAY_STAGE_A_LENGTH_MISMATCH"),
            (split.get("continuous_records") == 1800, "EXEC_REPLAY_CONTINUOUS_LENGTH_MISMATCH"),
            (split.get("corrected_restore_full_trace_exact") is True, "EXEC_REPLAY_CORRECTED_NOT_EXACT"),
            (variants["continuous282"]["trace"]["sha256"] == local["split_282"]["continuous_trace_sha256"], "EXEC_REPLAY_CONTINUOUS_SHA_MISMATCH"),
            (variants["restore282"]["trace"]["sha256"] == local["split_282"]["corrected_restore_trace_sha256"], "EXEC_REPLAY_RESTORED_SHA_MISMATCH"),
            (variants["legacy282"]["trace"]["sha256"] == local["split_282"]["defective_restart_trace_sha256"], "EXEC_REPLAY_DEFECTIVE_SHA_MISMATCH"),
            (variants["legacy67"]["trace"]["sha256"] == local["split_67_zero_control"]["legacy_zeroing_trace_sha256"], "EXEC_REPLAY_SPLIT67_SHA_MISMATCH"),
            (zero.get("legacy_zeroing_full_trace_exact") is True, "EXEC_REPLAY_SPLIT67_NOT_EXACT"),
        ]
        for ok, code in checks:
            check(ok, code, "generated replay differs from pinned reconstructed local result", failures)
        div = split.get("first_defective_divergence", {})
        check(div.get("record_index_zero_based") == 564 and div.get("step") == 283 and div.get("phase") == 0,
              "EXEC_REPLAY_FIRST_DIVERGENCE_MISMATCH", json.dumps(div, sort_keys=True), failures)
        check([item.get("coordinate") for item in div.get("differences", [])] == TARGET_COORDS,
              "EXEC_REPLAY_FIRST_DIVERGENCE_COORDS_MISMATCH", json.dumps(div, sort_keys=True), failures)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--source-zip", type=Path)
    parser.add_argument("--testbank-zip", type=Path)
    parser.add_argument("--guide-pdf", type=Path)
    parser.add_argument("--audit-blocked-state", action="store_true")
    parser.add_argument("--require-git-scope", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    failures: list[dict[str, str]] = []

    status = load_json(root / "integration/animo-b3/ANIMO-B3B04E1_STATUS.json")
    expectations = load_json(root / "integration/animo-b3/b3b04e1/TCD040_REPLAY_EXPECTATIONS.json")
    local = load_json(root / "integration/animo-b3/b3b04e1/RECONSTRUCTED_REPLAY_LOCAL_RESULT.json")
    manifest = load_json(root / "integration/animo-b3/b3b04e1/REPLAY_MANIFEST.json")
    register = load_json(root / "integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json")

    status_value = status.get("status")
    decision_value = status.get("decision")
    valid_pair = (
        (status_value == STATUS_BLOCKED and decision_value == DECISION_BLOCKED)
        or (status_value == STATUS_QUALIFIED and decision_value == DECISION_QUALIFIED)
    )
    check(valid_pair, "STATUS_DECISION_PAIR_INVALID", f"{status_value!r} / {decision_value!r}", failures)
    if args.audit_blocked_state:
        check(status_value == STATUS_BLOCKED and decision_value == DECISION_BLOCKED,
              "BLOCKED_AUDIT_REQUIRES_BLOCKED_STATUS", f"{status_value!r} / {decision_value!r}", failures)
    check(status.get("canonical_tcd_status") == "UNRESOLVED_NOT_ADMITTED",
          "TCD040_MUST_REMAIN_UNRESOLVED_NOT_ADMITTED", repr(status.get("canonical_tcd_status")), failures)

    verify_expectations(expectations, failures)
    verify_replay_bundle_presence(root, failures)
    verify_manifest(manifest, failures)
    verify_local_reconstruction(local, failures)
    verify_documentation_provenance(root, failures)
    verify_scope(status, root, args.require_git_scope, failures)
    controlled_storage_proven(register, failures)

    check_artifact(args.source_zip, SOURCE_SHA, "SOURCE_ARCHIVE_NOT_INDEPENDENTLY_AVAILABLE_OR_HASH_MISMATCH", failures)
    check_artifact(args.testbank_zip, TESTBANK_SHA, "TESTBANK_ARCHIVE_NOT_INDEPENDENTLY_AVAILABLE_OR_HASH_MISMATCH", failures)
    check_artifact(args.guide_pdf, GUIDE_SHA, "USER_GUIDE_NOT_INDEPENDENTLY_AVAILABLE_OR_HASH_MISMATCH", failures)
    verify_source_members(args.source_zip, failures)
    verify_grasspeat(root, args.testbank_zip, failures)
    verify_executable_replay(root, args.source_zip, args.testbank_zip, local, failures)

    report = {
        "workunit": "ANIMO-B3B04E1",
        "mode": "AUDIT_BLOCKED_STATE" if args.audit_blocked_state else "EVIDENCE_QUALIFICATION_GATE",
        "failure_count": len(failures),
        "failures": failures,
    }

    if args.audit_blocked_state:
        blocker_codes = {item["code"] for item in failures}
        b0_blocked = "B0_CONTROLLED_IMMUTABLE_ACQUISITION_NOT_PROVEN" in blocker_codes
        replay_missing = "REPLAY_BUNDLE_COMPONENT_ABSENT" in blocker_codes
        internal_replay_failure = any(
            code.startswith("LOCAL_")
            or code.startswith("REPLAY_MANIFEST_")
            or code.startswith("DOCUMENTATION_")
            or code.startswith("SCOPE_")
            or code.startswith("GIT_SCOPE_")
            for code in blocker_codes
        )
        ok = b0_blocked and not replay_missing and not internal_replay_failure
        report["audit_status"] = (
            "PASS_LOCAL_RECONSTRUCTION_COMPLETE_CONTROLLED_B0_STILL_BLOCKED"
            if ok
            else "FAIL_BLOCKER_STATE_NOT_AS_EXPECTED"
        )
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if ok else 1

    report["gate_status"] = (
        "PASS_EVIDENCE_REPLAYABILITY_QUALIFIED"
        if not failures
        else "FAIL_CLOSED_EVIDENCE_REPLAYABILITY_NOT_QUALIFIED"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
