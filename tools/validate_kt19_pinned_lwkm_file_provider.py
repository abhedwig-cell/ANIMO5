#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parents[1]
RG08 = "14109956b62376d0d0ab681e8c641c9e71d110bd"
KT08 = "281dc65cbaceaa61d31f9cb731b3c5a733ca5d57"

EXPECTED_SOURCE = "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c"
EXPECTED_ARCHIVE = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_TYPED = "c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4"
EXPECTED_GROUP = "40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34"
EXPECTED_RECORD = "eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1"
EXPECTED_FIXTURE = "6ee314e17bbe8c6aca904ff92403de4997d74734f5ac14bcbf79fed7e33df4df"


def fail(msg: str) -> None:
    print("KT19 FAIL_CLOSED:", msg)
    raise SystemExit(1)


def load(path: str) -> dict:
    return json.loads((R / path).read_text())


def show_json(sha: str, path: str) -> dict:
    return json.loads(
        subprocess.check_output(["git", "show", f"{sha}:{path}"], cwd=R, text=True)
    )


status = load("integration/animo-kt19/ANIMO-KT19_STATUS.json")
evidence = load("integration/animo-kt19/KT19_EXTERNAL_SOURCE_REPLAY.json")
fixture_meta = load("reference/kt19/LWKM_FIRST_PACKET_POWERSTATION_B1.json")
summary = load("reference/kt11/LWKM_SEQUENCE_SUMMARY_KT08.json")

rg08 = show_json(RG08, "integration/animo-reg/ANIMO-RG08_STATUS.json")
if rg08.get("state") != "QUALIFIED_POST_KT18_PROGRAM_REBASELINE_REVIEW_ROUTING_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG08 is not the qualified current rebaseline")
if rg08.get("b4_open") is not False or rg08.get("production_open") is not False:
    fail("RG08 production gates unexpectedly open")
if rg08.get("independent_reviews_completed") is not False:
    fail("RG08 independent review gate unexpectedly satisfied")

kt08 = show_json(KT08, "integration/animo-kt08/ANIMO-KT08_STATUS.json")
if kt08.get("verdict") != "QUALIFIED_B1_FULL_LWKM_EXPLICIT_HYDROLOGY_PRODUCER_SEQUENCE_IDENTITY_AND_TEMPORAL_ENVELOPE_NO_RUNTIME_PROVIDER_OR_B2_EQUIVALENCE":
    fail("KT08 evidence verdict drift")
if kt08.get("evidence_class") != "B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2":
    fail("KT08 evidence class drift")

if summary.get("source_sha256") != EXPECTED_SOURCE:
    fail("KT08 source hash drift")
if summary.get("sequence", {}).get("packet_count") != 1800:
    fail("KT08 packet count drift")
agg = summary.get("aggregate_identity", {})
if agg.get("typed_step_digest_sequence_sha256") != EXPECTED_TYPED:
    fail("KT08 typed sequence identity drift")
if agg.get("dynamic_group_digest_sequence_sha256") != EXPECTED_GROUP:
    fail("KT08 dynamic-group sequence identity drift")
if agg.get("temporal_and_digest_record_sequence_sha256") != EXPECTED_RECORD:
    fail("KT08 temporal/digest sequence identity drift")

if evidence.get("source_container_sha256") != EXPECTED_ARCHIVE:
    fail("external testbank archive identity drift")
if evidence.get("source_sha256") != EXPECTED_SOURCE:
    fail("external source identity drift")
if evidence.get("source_size_bytes") != 2388124:
    fail("external source size drift")
if evidence.get("packet_count") != 1800:
    fail("external replay packet count")
if evidence.get("logical_record_count") != 23417 or evidence.get("physical_block_count") != 23417:
    fail("external replay record counts")
if evidence.get("kt08_identity_match") is not True:
    fail("external replay did not match KT08")
if evidence.get("aggregate_identity") != agg:
    fail("external replay aggregate identity mismatch")
if len(evidence.get("anchor_selection_results", [])) != 8:
    fail("external replay anchor coverage")
if any(a.get("result") != "PASS" for a in evidence.get("anchor_selection_results", [])):
    fail("external replay anchor failure")
if evidence.get("source_bytes_committed_to_repository") is not False:
    fail("B0 source bytes were claimed committed")
if evidence.get("ci_self_contained_full_source_replay") is not False:
    fail("full B0 replay incorrectly claimed CI-self-contained")
if evidence.get("b2_claimed") is not False or evidence.get("production_claimed") is not False:
    fail("external replay overclaim")

provider_path = "prototype/kt19/pinned_lwkm_file_provider.py"
provider_blob = subprocess.check_output(["git", "hash-object", provider_path], cwd=R, text=True).strip()
if evidence.get("provider_git_blob") != provider_blob:
    fail("external replay is not bound to current KT19 provider blob")

provider = (R / provider_path).read_text()
required_provider_tokens = [
    "parse_powerstation_records",
    "parse_swap3_static",
    "parse_dynamic_step",
    "legacy_step_provenance",
    "typed_step_digest",
    "EXPECTED_PACKET_COUNT = 1800",
    "unexpected LWKM source SHA-256",
    "producer chain discontinuity",
    "typed step sequence",
    "dynamic group sequence",
    "temporal/digest sequence",
    "runtime calendar binding mismatch",
    "hydrology packet not found",
]
for token in required_provider_tokens:
    if token not in provider:
        fail("provider contract drift: " + token)

fixture = base64.b64decode(
    (R / "reference/kt19/LWKM_FIRST_PACKET_POWERSTATION_B1.b64").read_text().strip()
)
if hashlib.sha256(fixture).hexdigest() != EXPECTED_FIXTURE:
    fail("derived first-packet fixture hash")
if len(fixture) != 2650:
    fail("derived first-packet fixture size")
if fixture_meta.get("fixture_sha256") != EXPECTED_FIXTURE:
    fail("fixture metadata hash")
if fixture_meta.get("parent_source_sha256") != EXPECTED_SOURCE:
    fail("fixture parent source identity")
if fixture_meta.get("b0_source_committed") is not False or fixture_meta.get("b2_claimed") is not False:
    fail("fixture evidence classification")

for key, value in status.get("hard_boundaries", {}).items():
    if value is not False:
        fail("hard boundary " + key)

allowed_prefixes = (
    "prototype/kt19/",
    "tests/kt19/",
    "docs/kt19/",
    "integration/animo-kt19/",
    "reference/kt19/",
)
allowed_exact = {
    "tools/kt19_verify_pinned_lwkm_provider.py",
    "tools/validate_kt19_pinned_lwkm_file_provider.py",
    ".github/workflows/animo-kt19-pinned-lwkm-file-provider.yml",
}
changed = subprocess.check_output(
    ["git", "diff", "--name-only", RG08 + "..HEAD"], cwd=R, text=True
).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape " + path)
if any(path.lower().endswith((".unf", ".zip")) for path in changed):
    fail("raw B0 binary source committed")

if status.get("state") == "NOT_YET_QUALIFIED":
    if status.get("work_status", {}).get("qualified") is not False:
        fail("authoring qualified too early")
    print("PASS_KT19_AUTHORING")
elif status.get("state") == "QUALIFIED_PINNED_LWKM_FILE_TO_IMMUTABLE_HYDROLOGY_PROVIDER_TIER_C_REVIEW_REQUIRED":
    review = load("integration/animo-kt19/ANIMO-KT19_ADVERSARIAL_REVIEW.json")
    if review.get("outcome") != "SELF_REVIEW_PASS":
        fail("review outcome")
    if review.get("assurance") != "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT":
        fail("review assurance")
    if review.get("genuinely_independent") is not False:
        fail("review independence overclaim")
    if status.get("full_external_source_replay_passed") is not True:
        fail("full external replay lost")
    if status.get("central_kt11_authority_changed") is not False:
        fail("KT11 authority mutation")
    if status.get("independent_review_completed") is not False:
        fail("independent review overclaim")
    if status.get("production_authorized") is not False:
        fail("production overclaim")
    if status.get("work_status", {}).get("qualified") is not True:
        fail("final candidate not qualified")
    print("PASS_KT19_QUALIFIED_PROVIDER_CANDIDATE")
else:
    fail("unexpected KT19 state")
