#!/usr/bin/env python3
import json, pathlib, subprocess

R=pathlib.Path(__file__).resolve().parents[1]
BASE="6d05b270e21a41ca626adbb719f8f55bfa9a97b5"
RG07="c60dd36a38a2030e4f4ac1925f95b2966a6d1c87"
KT11="50731bf118deb8ef1029f220a40b39a99240e480"
KT15A="2279a961459211e03550dfda4af09ab4f7f6b9a3"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT18 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def gj(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-kt18/ANIMO-KT18_STATUS.json")
mf=load("integration/animo-kt18/KT18_COMPOSITION_MANIFEST.json")

rg=gj(RG07,"integration/animo-reg/ANIMO-RG07_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT16_PROGRAM_REBASELINE_CANDIDATE_STACK_FROZEN_NO_ADMISSION_OR_PRODUCTION_ADVANCE":
    fail("RG07 state")
if rg.get("central_runtime_admissions_unchanged") is not True:
    fail("RG07 central runtime boundary")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG07 gates")

k11=gj(KT11,"integration/animo-kt11/ANIMO-KT11_TIER_C_ADMISSION_STATUS.json")
if k11.get("state")!="QUALIFIED_BOUNDED_NONPRODUCTION_MULTI_PACKET_PROVIDER_ADMITTED_GOV04_TIER_C":
    fail("KT11 admission state")
if k11.get("admitted") is not True or k11.get("production_authorized") is not False:
    fail("KT11 admission boundary")
if k11.get("frozen_implementation_blob")!="a41d0f61da6dd30a18dbfadbe4b29b00259fa41e":
    fail("KT11 frozen implementation pin")

k15=gj(KT15A,"integration/animo-kt15a/ANIMO-KT15A_STATUS.json")
if k15.get("state")!="QUALIFIED_IMMUTABLE_APPLICATION_CONFIGURATION_BINDING_TIER_D_REVIEW_REQUIRED":
    fail("KT15A state")
if k15.get("immutable_application_config_qualified") is not True:
    fail("KT15A config")
if k15.get("independent_review_completed") is not False or k15.get("production_authorized") is not False:
    fail("KT15A review/production boundary")

gov=gj(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier D missing")

sel=mf.get("selection_contract",{})
if sel.get("key")!=["producer_endpoint_day","producer_step_days"]:
    fail("provider key contract")
for key in ["storage_order_semantic","mutable_cursor"]:
    if sel.get(key) is not False: fail("provider selection overclaim "+key)
for key in ["selected_value_is_copy","provider_forcing_ownership_retained","missing_key_fails_closed","ambiguous_key_fails_closed"]:
    if sel.get(key) is not True: fail("provider selection contract "+key)
di=mf.get("defense_in_depth",{})
if di.get("provider_uses_own_calendar_and_offset") is not True or    di.get("application_nested_kt06_revalidates_against_application_config") is not True or    di.get("disagreement_can_not_publish") is not True:
    fail("defense-in-depth contract")

provider=(R/"prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90").read_text()
for token in [
 "public :: select_multi_packet_hydrology_step_copy",
 "subroutine select_multi_packet_hydrology_step_copy",
 "packet = client%packets(selected_index)",
 "reason = 'MULTI_PACKET_HYDROLOGY_STEP_SELECTED_COPY'",
 "DUPLICATE_PRODUCER_INTERVAL_KEY",
 "HYDROLOGY_PACKET_NOT_FOUND",
 "AMBIGUOUS_HYDROLOGY_PACKET_SELECTION"
]:
    if token not in provider: fail("KT11 selection-copy seam drift "+token)

app=(R/"prototype/kt18/mod_animo_provider_backed_application.f90").read_text()
for token in [
 "call validate_kt15_application_state",
 "call kt15_application_time",
 "call select_multi_packet_hydrology_step_copy",
 "call execute_kt15_atomic_interval",
 "KT18_PROVIDER_SELECTION_FAILED:",
 "KT18_APPLICATION_INTERVAL_FAILED:",
 "KT18_PROVIDER_BACKED_APPLICATION_INTERVAL_COMMITTED"
]:
    if token not in app: fail("KT18 composition drift "+token)

test=(R/"tests/kt18/test_kt18_provider_backed_application.f90").read_text()
for name in [
 "test_out_of_order_provider_two_interval_application",
 "test_missing_provider_packet_preserves_application",
 "test_provider_application_offset_mismatch_preserves_application",
 "test_selected_copy_is_nonowning_and_repeatable"
]:
    if name not in test: fail("missing test "+name)

run=(R/"tests/kt18/run_kt18_tests.sh").read_text()
if "bash tests/kt11/run_kt11_tests.sh" not in run:
    fail("KT11 regression missing")
if "bash tests/kt15/run_kt15_tests.sh" not in run:
    fail("KT15 regression missing")

# Central KT11-A1 is immutable authority. The branch-local module change is
# owned by KT18 and may only add the copy-selection seam.
base_provider=subprocess.check_output(["git","show",f"{BASE}:prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90"],cwd=R,text=True)
if base_provider==provider:
    fail("KT18 provider seam not materialized")
for token in [
 "subroutine initialize_multi_packet_client",
 "subroutine execute_multi_packet_attempt",
 "logical function multi_packet_client_ready"
]:
    if token not in base_provider or token not in provider:
        fail("existing KT11 runtime surface missing "+token)

allowed_prefixes=("prototype/kt18/","tests/kt18/","docs/kt18/","integration/animo-kt18/")
allowed_exact={
 "prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90",
 ".github/workflows/animo-kt18-provider-accepted-application.yml",
 "tools/validate_kt18_provider_application.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)
if any(path.startswith("src/") for path in changed):
    fail("production source modified")

for key,value in st.get("hard_boundaries",{}).items():
    if value is not False:
        fail("hard boundary "+key)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_KT18_AUTHORING")
elif st.get("state")=="QUALIFIED_MULTI_PACKET_PROVIDER_TO_ACCEPTED_APPLICATION_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt18/ANIMO-KT18_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for key in [
      "read_only_provider_selection_copy_qualified",
      "provider_application_interval_composition_qualified",
      "provider_owned_forcing_immutability_qualified",
      "missing_packet_atomic_failure_qualified",
      "provider_application_config_disagreement_failure_qualified",
      "two_interval_provider_application_execution_qualified"
    ]:
        if st.get(key) is not True: fail("qualification flag "+key)
    for key in [
      "central_kt11_admission_changed","canonical_external_forcing_admitted",
      "canonical_application_admitted","independent_review_completed","production_authorized"
    ]:
        if st.get(key) is not False: fail("overclaim "+key)
    print("PASS_KT18_QUALIFIED_PROVIDER_APPLICATION_CANDIDATE")
else:
    fail("unexpected state")
