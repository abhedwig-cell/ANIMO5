#!/usr/bin/env python3
import json, pathlib, re, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="d3a51aad084969a753cb5b54c604ebefba4b26c6"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
KT15="d3a51aad084969a753cb5b54c604ebefba4b26c6"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT15A FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-kt15a/ANIMO-KT15A_STATUS.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 production gates")

kt15=show_json(KT15,"integration/animo-kt15/ANIMO-KT15_STATUS.json")
if kt15.get("state")!="QUALIFIED_ATOMIC_COMPOSITE_APPLICATION_COMMIT_TIER_D_REVIEW_REQUIRED":
    fail("KT15 authority state")
for field in [
    "application_aggregate_identity_qualified",
    "opaque_boundary_binding_qualified",
    "private_working_science_execution_qualified",
    "atomic_group_publication_qualified",
    "two_interval_continuation_qualified",
    "reject_rollback_qualified"
]:
    if kt15.get(field) is not True:
        fail("KT15 missing qualification flag "+field)
if kt15.get("production_authorized") is not False:
    fail("KT15 production boundary")
if kt15.get("canonical_state_admitted") is not False or kt15.get("checkpoint_schema_admitted") is not False:
    fail("KT15 state/checkpoint overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier D missing")

mod=(R/"prototype/kt15/mod_animo_atomic_composite_application.f90").read_text()
required=[
    "type, public :: kt15_application_config_t",
    "private\n    character(len=56) :: schema_id",
    "type(kt15_application_config_t) :: config",
    "public :: make_kt15_application_config",
    "public :: validate_kt15_application_config",
    "public :: same_kt15_application_config",
    "public :: snapshot_kt15_application_config",
    "integer(int64) :: producer_day_offset",
    "type(kt15_static_hydrology_config_t) :: static_hydrology",
    "character(len=64) :: boundary_content_sha256",
    "integer :: simulation_start_year",
    "integer :: load_channel"
]
# The exact-real helper uses variables a/b, so validate separately below.
for text in required:
    if text not in mod:
        fail("immutable config implementation drift "+text)
if "a = transfer(left, a)" not in mod or "b = transfer(right, b)" not in mod:
    fail("exact binary64 equality helper missing")
if "exact_real64_equal(left%static_hydrology%he_top" not in mod:
    fail("exact config geometry equality missing")
if "canonical_sha256(config%boundary_content_sha256)" not in mod:
    fail("canonical declared boundary identity validation missing")

app_match=re.search(r"type, public :: kt15_application_state_t(.*?)end type kt15_application_state_t",mod,re.S|re.I)
if not app_match or "private" not in app_match.group(1).lower() or "type(kt15_application_config_t) :: config" not in app_match.group(1):
    fail("application state does not privately own config")

exec_match=re.search(r"subroutine execute_kt15_atomic_interval\((.*?)\)\n(.*?)end subroutine execute_kt15_atomic_interval",mod,re.S|re.I)
if not exec_match:
    fail("execute_kt15_atomic_interval missing")
sig=" ".join(exec_match.group(1).replace("&"," ").split()).lower()
body=exec_match.group(2)
for oldarg in [
    "runtime_calendar_contract_id","producer_day_offset","static_hydrology",
    "boundary_content_sha256","simulation_start_year","load_channel"
]:
    if oldarg in sig:
        fail("interval-invariant configuration still accepted as execute argument: "+oldarg)
for required_use in [
    "state%config%runtime_calendar_contract_id",
    "state%config%producer_day_offset",
    "state%config%static_hydrology%he_top",
    "state%config%static_hydrology%lefrrv",
    "state%config%static_hydrology%lefrso",
    "state%config%boundary_content_sha256",
    "state%config%simulation_start_year",
    "state%config%load_channel"
]:
    if required_use not in body:
        fail("execute path does not use accepted config field "+required_use)

if "KT15_CONFIG_ACCEPTED_TIME_CALENDAR_MISMATCH" not in mod:
    fail("accepted time/config calendar binding missing")
if mod.count("state = working") != 1:
    fail("atomic aggregate publication count changed")
if "working = state" not in mod:
    fail("private working aggregate missing")

for forbidden in ["sha256sum","openssl dgst","hashlib","source_hash_verified"]:
    if forbidden.lower() in mod.lower():
        fail("source-byte hash verification leaked into KT15A: "+forbidden)

test=(R/"tests/kt15/test_kt15_atomic_composite_application.f90").read_text()
for required_test in [
    "test_two_interval_atomic_progression",
    "test_science_reject_preserves_full_application_state",
    "test_invalid_config_rejected_before_application_state",
    "test_config_is_immutable_across_intervals",
    "snapshot_kt15_application_config",
    "same_kt15_application_config",
    "invalid boundary content identity rejected by config",
    "missing calendar rejected by config",
    "invalid load channel rejected by config"
]:
    if required_test not in test:
        fail("KT15A test coverage drift "+required_test)

allowed_prefixes=("docs/kt15a/","integration/animo-kt15a/")
allowed_exact={
    "prototype/kt15/mod_animo_atomic_composite_application.f90",
    "tests/kt15/test_kt15_atomic_composite_application.f90",
    ".github/workflows/animo-kt15a-immutable-application-config.yml",
    "tools/validate_kt15a_immutable_application_config.py"
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
    print("PASS_KT15A_AUTHORING")
elif st.get("state")=="QUALIFIED_IMMUTABLE_APPLICATION_CONFIGURATION_BINDING_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt15a/ANIMO-KT15A_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for field in [
        "immutable_application_config_qualified",
        "accepted_state_config_binding_qualified",
        "exact_config_equality_qualified",
        "multi_interval_config_stability_qualified"
    ]:
        if st.get(field) is not True:
            fail("qualification flag "+field)
    if st.get("source_hash_verification_qualified") is not False:
        fail("source hash verification overclaim")
    if st.get("checkpoint_schema_admitted") is not False or st.get("canonical_state_admitted") is not False:
        fail("state/checkpoint overclaim")
    if st.get("independent_review_completed") is not False:
        fail("independent review overclaim")
    print("PASS_KT15A_QUALIFIED_IMMUTABLE_APPLICATION_CONFIG")
else:
    fail("unexpected state")
