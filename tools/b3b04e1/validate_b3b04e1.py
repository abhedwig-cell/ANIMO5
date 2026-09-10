#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3B04E1.

The validator has two deliberately different exits:

* default gate mode: success only when the independently replayable evidence
  bundle is complete and all qualification prerequisites are satisfied;
* --audit-blocked-state: success only when the repository truthfully records
  the present fail-closed blocker state. This mode must never be interpreted as
  evidence qualification.

No tolerance comparison is used anywhere in this validator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

BASE_SHA = "bb001129578457ca8435e39deb2b8586e7ebc6a2"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
GUIDE_SHA = "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"
SOURCE_MEMBERS = {
    "ANIMO_4.1.5.53/Inicalc.for": "306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1",
    "ANIMO_4.1.5.53/input1.for": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95",
    "ANIMO_4.1.5.53/Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058",
    "ANIMO_4.1.5.53/Output_Init.for": "6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f",
    "ANIMO_4.1.5.53/Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
}
REQUIRED_REPLAY_PATHS = [
    "tools/b3b04e1/replay_tcd040.py",
    "integration/animo-b3/b3b04e1/REPLAY_MANIFEST.json",
    "integration/animo-b3/b3b04e1/payloads/checkpoint_split282.bin",
    "integration/animo-b3/b3b04e1/payloads/continuous.trace",
    "integration/animo-b3/b3b04e1/payloads/defective_restart.trace",
    "integration/animo-b3/b3b04e1/payloads/corrected_restore.trace",
    "integration/animo-b3/b3b04e1/payloads/split67_control.trace",
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


def check_optional_artifact(path: Path | None, expected: str, code: str, failures: list[dict[str, str]]) -> None:
    if path is None:
        failures.append({"code": code, "detail": "artifact path not supplied to validator"})
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
    if source_zip is None or not source_zip.is_file() or sha256_file(source_zip) != SOURCE_SHA:
        return
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
    if testbank_zip is None or not testbank_zip.is_file() or sha256_file(testbank_zip) != TESTBANK_SHA:
        return
    tool = repo_root / "tools/b3b04e1/extract_grasspeat_activation.py"
    if not tool.is_file():
        failures.append({"code": "GRASSPEAT_INSPECTOR_ABSENT", "detail": str(tool)})
        return
    result = subprocess.run([sys.executable, str(tool), str(testbank_zip)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check(result.returncode == 0, "GRASSPEAT_WITNESS_REPRODUCTION_FAILED", result.stdout.strip(), failures)


def verify_expectations(expectations: dict, failures: list[dict[str, str]]) -> None:
    split = expectations["split_282"]
    check(split["split_step"] * split["records_per_step"] == split["stage_a_records"],
          "SPLIT282_ARITHMETIC_MISMATCH", "split_step * records_per_step != stage_a_records", failures)
    check(900 * split["records_per_step"] == split["full_trace_records"],
          "TRACE_LENGTH_ARITHMETIC_MISMATCH", "900 * records_per_step != full_trace_records", failures)

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
        "coordinates": ["Conh(0)", "Coni(0)", "Codiorma(0)", "Codiorni(0)", "Codiorpo(0)"],
    }, "FIRST_DIVERGENCE_EXPECTATION_MISMATCH", json.dumps(divergence, sort_keys=True), failures)

    check(split["continuous_trace_sha256"] == split["corrected_restore_trace_sha256"],
          "CORRECTED_FULL_TRACE_EXPECTATION_NOT_EXACT", "reported hashes differ", failures)
    zero = expectations["split_67_zero_control"]
    check(zero["full_trace_records"] == 1800,
          "SPLIT67_TRACE_LENGTH_EXPECTATION_MISMATCH", str(zero["full_trace_records"]), failures)
    check(zero["continuous_trace_sha256"] == zero["legacy_restart_trace_sha256"],
          "SPLIT67_NEGATIVE_CONTROL_EXPECTATION_MISMATCH", "reported hashes differ", failures)

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
        cwd=repo_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        failures.append({"code": "GIT_SCOPE_DIFF_FAILED", "detail": result.stdout.strip()})
        return
    changed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    disallowed = [path for path in changed if not path.startswith(ALLOWED_CHANGE_PREFIXES)]
    check(not disallowed, "SCOPE_GUARD_DISALLOWED_PATH", ", ".join(disallowed), failures)


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
    register = load_json(root / "integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json")

    check(status.get("status") == "FAIL_CLOSED_INDEPENDENT_REPLAY_BUNDLE_NOT_QUALIFIED",
          "STATUS_FAIL_CLOSED_REQUIRED", repr(status.get("status")), failures)
    check(status.get("canonical_tcd_status") == "UNRESOLVED_NOT_ADMITTED",
          "TCD040_MUST_REMAIN_UNRESOLVED_NOT_ADMITTED", repr(status.get("canonical_tcd_status")), failures)

    verify_expectations(expectations, failures)
    verify_scope(status, root, args.require_git_scope, failures)
    controlled_storage_proven(register, failures)
    verify_replay_bundle_presence(root, failures)

    check_optional_artifact(args.source_zip, SOURCE_SHA, "SOURCE_ARCHIVE_NOT_INDEPENDENTLY_AVAILABLE_OR_HASH_MISMATCH", failures)
    check_optional_artifact(args.testbank_zip, TESTBANK_SHA, "TESTBANK_ARCHIVE_NOT_INDEPENDENTLY_AVAILABLE_OR_HASH_MISMATCH", failures)
    check_optional_artifact(args.guide_pdf, GUIDE_SHA, "USER_GUIDE_NOT_INDEPENDENTLY_AVAILABLE_OR_HASH_MISMATCH", failures)
    verify_source_members(args.source_zip, failures)
    verify_grasspeat(root, args.testbank_zip, failures)

    report = {
        "workunit": "ANIMO-B3B04E1",
        "mode": "AUDIT_BLOCKED_STATE" if args.audit_blocked_state else "EVIDENCE_QUALIFICATION_GATE",
        "failure_count": len(failures),
        "failures": failures,
    }

    if args.audit_blocked_state:
        blocker_codes = {item["code"] for item in failures}
        required_blockers = {
            "B0_CONTROLLED_IMMUTABLE_ACQUISITION_NOT_PROVEN",
            "REPLAY_BUNDLE_COMPONENT_ABSENT",
        }
        ok = required_blockers.issubset(blocker_codes)
        report["audit_status"] = "PASS_EXPECTED_FAIL_CLOSED_STATE" if ok else "FAIL_BLOCKER_STATE_NOT_AS_EXPECTED"
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if ok else 1

    report["gate_status"] = "PASS_EVIDENCE_REPLAYABILITY_QUALIFIED" if not failures else "FAIL_CLOSED_EVIDENCE_REPLAYABILITY_NOT_QUALIFIED"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
