#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="6245aad4aca962cb2a63d0394bb7f2baa686457d"
RG08="14109956b62376d0d0ab681e8c641c9e71d110bd"
KT18="42d8837f85acd0c4c9e29b323d8b2cb1bfdd4d72"
KT11="50731bf118deb8ef1029f220a40b39a99240e480"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT20 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-kt20/ANIMO-KT20_STATUS.json")

rg=show_json(RG08,"integration/animo-reg/ANIMO-RG08_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT18_PROGRAM_REBASELINE_REVIEW_ROUTING_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG08 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG08 gates")
if rg.get("central_runtime_admissions_changed") is not False:
    fail("unexpected RG08 central runtime change")

kt19=show_json(BASE,"integration/animo-kt19/ANIMO-KT19_STATUS.json")
if kt19.get("state")!="QUALIFIED_PINNED_LWKM_FILE_TO_IMMUTABLE_HYDROLOGY_PROVIDER_TIER_C_REVIEW_REQUIRED":
    fail("KT19 state")
if kt19.get("pinned_source_sha256")!="b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c":
    fail("KT19 source pin")
if kt19.get("packet_count")!=1800 or kt19.get("kt08_aggregate_identity_matched") is not True:
    fail("KT19 sequence identity")
if kt19.get("b2_claimed") is not False or kt19.get("production_authorized") is not False:
    fail("KT19 claim boundary")

kt18=show_json(KT18,"integration/animo-kt18/ANIMO-KT18_STATUS.json")
if kt18.get("state")!="QUALIFIED_MULTI_PACKET_PROVIDER_TO_ACCEPTED_APPLICATION_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    fail("KT18 state")
if kt18.get("central_kt11_admission_changed") is not False:
    fail("KT18 central KT11 drift")
if kt18.get("independent_review_completed") is not False or kt18.get("production_authorized") is not False:
    fail("KT18 review/production overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier D missing")

py=(R/"prototype/kt20/hydrology_packet_frame.py").read_text()
for required in [
    'FRAME_SCHEMA = "ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1"',
    'FRAME_ROLE = "NONPRODUCTION_ADAPTER_INTERCHANGE_NOT_CANONICAL_FORCING_ABI"',
    'typed_step_digest(packet)',
    'struct.pack(">d", value).hex()',
    'PinnedLWKMFileHydrologyProvider.from_path',
    'provider.select(origin_day, endpoint_day, calendar_id)',
]:
    if required not in py:
        fail("Python frame contract drift: "+required)

f90=(R/"prototype/kt20/mod_animo_kt20_hydrology_packet_frame.f90").read_text()
for required in [
    "ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1",
    "NONPRODUCTION_ADAPTER_INTERCHANGE_NOT_CANONICAL_FORCING_ABI",
    "read(line,'(Z16)'",
    "value=transfer(bits,value)",
    "call validate_hydrology_step_explicit(packet,status)",
    "KT20_HYDROLOGY_PACKET_FRAME_DECODED",
]:
    if required not in f90:
        fail("Fortran frame decoder drift: "+required)

test_py=(R/"tests/kt20/test_kt20_packet_frame.py").read_text()
for required in [
    "test_real_packet_exact_roundtrip",
    "test_synthetic_control_exact_roundtrip",
    "test_payload_bit_mutation_is_detected_by_declared_digest",
    "eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c",
]:
    if required not in test_py:
        fail("Python test gap: "+required)

test_f90=(R/"tests/kt20/test_kt20_packet_bridge.f90").read_text()
for required in [
    "test_real_source_packet_reaches_kt18_and_fails_closed",
    "test_synthetic_control_frame_commits_through_kt18",
    "trace%provider_packet_selected",
    ".not.trace%application_interval_committed",
    "assert_application_origin_unchanged(state)",
    "trace%application_interval_committed",
]:
    if required not in test_f90:
        fail("Fortran bridge test gap: "+required)

if "CANONICAL_PRODUCTION_ABI" in py:
    fail("production ABI string leaked into implementation")

allowed_prefixes=("prototype/kt20/","tests/kt20/","docs/kt20/","integration/animo-kt20/")
allowed_exact={
    ".github/workflows/animo-kt20-kt19-to-kt18-bridge.yml",
    "tools/validate_kt20_kt19_to_kt18_bridge.py",
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)

for k,v in st.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard boundary "+k)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_KT20_AUTHORING")
elif st.get("state")=="QUALIFIED_KT19_PACKET_FRAME_TO_KT18_APPLICATION_BRIDGE_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt20/ANIMO-KT20_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for key in [
        "exact_packet_frame_qualified",
        "python_roundtrip_qualified",
        "fortran_exact_bit_decode_qualified",
        "real_b1_packet_reaches_kt18",
        "real_b1_packet_fail_closed_preserves_application",
        "synthetic_control_commits_through_kt18",
    ]:
        if st.get(key) is not True:
            fail("missing final qualification flag "+key)
    if st.get("full_real_sequence_application_execution_qualified") is not False:
        fail("whole real sequence overclaim")
    if st.get("canonical_forcing_abi_admitted") is not False:
        fail("canonical forcing ABI overclaim")
    if st.get("independent_review_completed") is not False:
        fail("independent review overclaim")
    print("PASS_KT20_QUALIFIED_BRIDGE")
else:
    fail("unexpected state")
