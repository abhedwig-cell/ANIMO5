#!/usr/bin/env python3
import json, pathlib, subprocess

R=pathlib.Path(__file__).resolve().parents[1]
BASE="c60dd36a38a2030e4f4ac1925f95b2966a6d1c87"
RG07="c60dd36a38a2030e4f4ac1925f95b2966a6d1c87"
KT16="7cd863b71a7a7fcc985514a8af28dcb69cae999a"
ARCH02="a079d93c965f6073586c55ee4b3544dd8873b723"

def fail(msg):
    print("KT17 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def gj(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-kt17/ANIMO-KT17_STATUS.json")
mf=load("integration/animo-kt17/KT17_INTEGRITY_MANIFEST.json")

rg=gj(RG07,"integration/animo-reg/ANIMO-RG07_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT16_PROGRAM_REBASELINE_CANDIDATE_STACK_FROZEN_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG07 state")
if rg.get("latest_bounded_application_candidate")!="ANIMO-KT16@"+KT16:
    fail("RG07 KT16 route")
if rg.get("central_runtime_admissions_unchanged") is not True:
    fail("RG07 central admission boundary")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG07 production gates")

k16=gj(KT16,"integration/animo-kt16/ANIMO-KT16_STATUS.json")
if k16.get("state")!="QUALIFIED_ACCEPTED_APPLICATION_CHECKPOINT_SPLIT_RUN_RESTART_TIER_D_REVIEW_REQUIRED":
    fail("KT16 state")
for key in ["file_format_qualified","integrity_hash_qualified","canonical_checkpoint_admitted",
            "canonical_state_admitted","historical_b2_restart_equivalence_claimed",
            "independent_review_completed","production_authorized"]:
    if k16.get(key) is not False:
        fail("KT16 boundary drift "+key)

a2=gj(ARCH02,"integration/animo-architecture/ANIMO-ARCH02_STATUS.json")
if a2.get("candidate_design_only") is not True or a2.get("canonical_state_gate_admitted") is not False:
    fail("ARCH02 authority boundary")
if a2.get("production_migration_admitted") is not False:
    fail("ARCH02 production boundary")

ic=mf.get("integrity_contract",{})
if ic.get("hash_algorithm")!="SHA-256":
    fail("hash algorithm")
if ic.get("canonicalization")!="ANIMO_KT17_CANON_ASCII_V1":
    fail("canonicalization")
if ic.get("canonicalization_role")!="IN_MEMORY_HASH_PREIMAGE_ONLY_NOT_CHECKPOINT_FILE_FORMAT":
    fail("canonicalization/file boundary")
for key in ["config_hash_recomputed","checkpoint_payload_hash_recomputed","manifest_hash_recomputed"]:
    if ic.get(key) is not True:
        fail("integrity recomputation "+key)

ev=mf.get("fixed_evidence_identity",{})
expected={
 "source_archive_sha256":"183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
 "testbank_sha256":"44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
 "documentation_sha256":"ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301"
}
for key,value in expected.items():
    if ev.get(key)!=value: fail("evidence pin "+key)
if ev.get("bytes_rehashed_by_runtime") is not False:
    fail("source byte verification overclaim")
if mf.get("build_identity",{}).get("runtime_self_attestation") is not False:
    fail("build self-attestation overclaim")

sha=(R/"prototype/kt17/mod_animo_sha256.f90").read_text()
for token in [
 "428A2F98","71374491","C67178F2",
 "6A09E667","BB67AE85","5BE0CD19",
 "function sha256_ascii",
 "virtual_byte",
 "write(hex,'(8(Z8.8))')"
]:
    if token not in sha:
        fail("SHA256 implementation drift "+token)

integrity=(R/"prototype/kt17/mod_animo_checkpoint_manifest_integrity.f90").read_text()
for token in [
 "ANIMO_KT17_ACCEPTED_CHECKPOINT_ENVELOPE_V1",
 "ANIMO_KT17_CANON_ASCII_V1",
 expected["source_archive_sha256"],
 expected["testbank_sha256"],
 expected["documentation_sha256"],
 "canonical_kt15_config_hash",
 "canonical_kt16_checkpoint_hash",
 "checkpoint_payload_sha256",
 "manifest_sha256",
 "KT17_EXPECTED_BUILD_ID_MISMATCH",
 "KT17_APPLICATION_CONFIG_INTEGRITY_MISMATCH",
 "KT17_CHECKPOINT_PAYLOAD_INTEGRITY_MISMATCH",
 "KT17_MANIFEST_INTEGRITY_MISMATCH",
 "restore_kt16_application_checkpoint"
]:
    if token not in integrity:
        fail("integrity implementation drift "+token)

kt15=(R/"prototype/kt15/mod_animo_atomic_composite_application.f90").read_text()
if "public :: inspect_kt15_application_config" not in kt15:
    fail("read-only config inspector missing")
for token in [
 "KT15_CONFIG_INSPECTION_INVALID_CONFIG",
 "KT15_APPLICATION_CONFIG_INSPECTED_READ_ONLY"
]:
    if token not in kt15:
        fail("config inspector drift "+token)

test=(R/"tests/kt17/test_kt17_checkpoint_manifest_integrity.f90").read_text()
vectors=[
 "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
 "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
 "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
]
for v in vectors:
    if v not in test: fail("SHA256 KAT missing "+v)
for name in [
 "test_encode_verify_restore",
 "test_payload_tamper_rejected",
 "test_manifest_identity_tamper_rejected",
 "test_expected_build_and_config_mismatch_rejected"
]:
    if name not in test: fail("missing test "+name)

run=(R/"tests/kt17/run_kt17_tests.sh").read_text()
if "bash tests/kt15/run_kt15_tests.sh" not in run or "bash tests/kt16/run_kt16_tests.sh" not in run:
    fail("KT15/KT16 regression reruns missing")

# KT17 has no file I/O implementation. Internal formatted WRITE in the SHA
# hex formatter is allowed; OPEN/CLOSE and external READ are not.
for path in [
 "prototype/kt17/mod_animo_sha256.f90",
 "prototype/kt17/mod_animo_checkpoint_manifest_integrity.f90"
]:
    txt=(R/path).read_text().lower()
    for forbidden in ["open(","close(","access=","form='unformatted'","stream'"]:
        if forbidden in txt:
            fail("file I/O token in "+path+": "+forbidden)

allowed_prefixes=("prototype/kt17/","tests/kt17/","docs/kt17/","integration/animo-kt17/")
allowed_exact={
 "prototype/kt15/mod_animo_atomic_composite_application.f90",
 ".github/workflows/animo-kt17-checkpoint-manifest-integrity.yml",
 "tools/validate_kt17_checkpoint_manifest_integrity.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)
if any(path.startswith("src/") for path in changed):
    fail("production source modified")

# The only upstream module change is the explicit read-only inspector.
base_kt15=subprocess.check_output(["git","show",f"{BASE}:prototype/kt15/mod_animo_atomic_composite_application.f90"],cwd=R,text=True)
if base_kt15==kt15:
    fail("KT15 inspection seam not materialized")
for anchor in [
 "subroutine execute_kt15_atomic_interval",
 "subroutine initialize_kt15_application_state",
 "logical function same_kt15_application_config"
]:
    # Existing runtime surfaces must still be present; behavior regression is
    # additionally covered by the compiled KT15/KT16 harnesses.
    if anchor not in base_kt15 or anchor not in kt15:
        fail("KT15 runtime surface drift "+anchor)

for key,value in st.get("hard_boundaries",{}).items():
    if value is not False:
        fail("hard boundary "+key)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_KT17_AUTHORING")
elif st.get("state")=="QUALIFIED_ACCEPTED_CHECKPOINT_MANIFEST_SHA256_INTEGRITY_AND_IDENTITY_BINDING_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt17/ANIMO-KT17_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for key in [
      "sha256_implementation_qualified","canonical_config_integrity_qualified",
      "canonical_checkpoint_payload_integrity_qualified","manifest_integrity_qualified",
      "expected_build_identity_binding_qualified","evidence_identity_binding_qualified"
    ]:
        if st.get(key) is not True: fail("final qualification flag "+key)
    for key in [
      "source_bytes_rehashed_by_runtime","executable_build_self_attested","file_format_qualified",
      "canonical_checkpoint_admitted","canonical_state_admitted",
      "historical_b2_restart_equivalence_claimed","independent_review_completed","production_authorized"
    ]:
        if st.get(key) is not False: fail("final overclaim "+key)
    print("PASS_KT17_QUALIFIED_INTEGRITY_CANDIDATE")
else:
    fail("unexpected state")
