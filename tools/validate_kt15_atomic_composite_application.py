#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
STATEQ11="c2bd0d17ac6921fcd9f22d6289a510cae454153d"
BOUNDQ02B="de6eef3122354e74405ff9c92286794714bdee82"
KT14B="46e9e7397be751f245069033bae655b4382b63bd"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"
BASE="c809d1b58af46e7594b2c78b6c033858617b1106"

def fail(msg):
    print("KT15 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def blob(path):
    return subprocess.check_output(["git","hash-object",path],cwd=R,text=True).strip()

st=load("integration/animo-kt15/ANIMO-KT15_STATUS.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

s11=show_json(STATEQ11,"integration/animo-state/ANIMO-STATEQ11_STATUS.json")
if s11.get("state")!="QUALIFIED_COMPOSITE_ACCEPTED_CONTINUATION_IDENTITY_TIER_D_REVIEW_REQUIRED":
    fail("STATEQ11 state")
if s11.get("composite_identity_qualified") is not True:
    fail("STATEQ11 identity")
if s11.get("atomic_group_commit_implemented") is not False:
    fail("STATEQ11 unexpectedly owns commit")
if s11.get("canonical_state_admitted") is not False:
    fail("STATEQ11 canonical-state overclaim")

b=show_json(BOUNDQ02B,"integration/animo-boundq02b/ANIMO-BOUNDQ02B_STATUS.json")
if b.get("state")!="QUALIFIED_OPAQUE_CONTENT_BOUND_STATIC_BOUNDARY_FRAME_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ02B state")
if b.get("opaque_frame_qualified") is not True:
    fail("BOUNDQ02B opaque frame")

k=show_json(KT14B,"integration/animo-kt14b/ANIMO-KT14B_STATUS.json")
if k.get("state")!="QUALIFIED_OPAQUE_BOUNDQ02B_FRAME_TO_KT13A_TCD042_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    fail("KT14B state")
if k.get("opaque_frame_consumption_qualified") is not True or k.get("bounded_tcd042_composition_qualified") is not True:
    fail("KT14B qualification")
if k.get("production_authorized") is not False:
    fail("KT14B production boundary")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

expected_blobs={
 "prototype/stateq11/mod_animo_composite_accepted_continuation.f90":"5450563ac74ff40b7144f5c1ab7805f8d5849862",
 "prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90":"e55a72fd37b20addaf7131ed085b417768b84a1c",
 "prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90":"7c4144785ae023abb3ff3fe4e760519c650626b8",
 "prototype/boundq02b/mod_animo_immutable_static_boundary_frame.f90":"eae62a2ce077e3e568a8a73b25ac45d20c432bae",
 "prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90":"080454a49e123ff4bd86a2fcdac7755b635e8734"
}
for path,sha in expected_blobs.items():
    if blob(path)!=sha:
        fail("authority blob drift "+path)

mod=(R/"prototype/kt15/mod_animo_atomic_composite_application.f90").read_text()
for required in [
    "type(kt15_application_state_t) :: working",
    "immutable_static_boundary_interval_frame_t",
    "make_immutable_static_boundary_interval_frame",
    "working = state",
    "execute_boundary_frame_tcd042_interval(working%science_store",
    "prepare_next_composite_continuation(state%continuation",
    "validate_composite_against_accepted_store(next_continuation, working%science_store",
    "working%continuation = next_continuation",
    "state = working",
    "KT15_ATOMIC_OPAQUE_FRAME_APPLICATION_INTERVAL_COMMITTED"
]:
    if required not in mod:
        fail("atomic composition implementation drift "+required)

for forbidden in [
    "type(static_boundary_interval_frame_t)",
    "bind_static_boundary_interval(",
    "state%science_store = working%science_store",
    "state%continuation = next_continuation",
    "reconstruct_accepted_store_trusted"
]:
    if forbidden.lower() in mod.lower():
        fail("partial/public mutable commit path retained "+forbidden)

if mod.count("state = working") != 1:
    fail("application aggregate publication must occur exactly once")

p_work=mod.find("working = state")
p_science=mod.find("execute_boundary_frame_tcd042_interval(working%science_store")
p_next=mod.find("prepare_next_composite_continuation")
p_publish=mod.find("state = working")
if not (0 <= p_work < p_science < p_next < p_publish):
    fail("atomic publication ordering")

test=(R/"tests/kt15/test_kt15_atomic_composite_application.f90").read_text()
for required in [
    "test_two_interval_atomic_progression",
    "test_science_reject_preserves_full_application_state",
    "test_invalid_content_identity_preserves_application_state",
    "published_generation==2_int64",
    ".not.after%boundary_cursor%initialized",
    "NOT-A-SHA256"
]:
    if required not in test:
        fail("atomic test coverage drift "+required)

if "first_call_runinu" in mod.lower():
    fail("first-call Runinu rule leaked into implementation")

allowed_prefixes=("prototype/kt15/","tests/kt15/","docs/kt15/","integration/animo-kt15/")
allowed_exact={
    "prototype/boundq02b/mod_animo_immutable_static_boundary_frame.f90",
    "prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90",
    ".github/workflows/animo-kt15-atomic-composite-application.yml",
    "tools/validate_kt15_atomic_composite_application.py"
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
    print("PASS_KT15_AUTHORING")
elif st.get("state")=="QUALIFIED_ATOMIC_COMPOSITE_APPLICATION_COMMIT_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt15/ANIMO-KT15_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for field in [
        "application_aggregate_identity_qualified",
        "opaque_boundary_binding_qualified",
        "private_working_science_execution_qualified",
        "atomic_group_publication_qualified",
        "two_interval_continuation_qualified",
        "reject_rollback_qualified"
    ]:
        if st.get(field) is not True:
            fail("qualification flag "+field)
    if st.get("source_hash_verification_qualified") is not False:
        fail("hash verification overclaim")
    if st.get("canonical_state_admitted") is not False or st.get("checkpoint_schema_admitted") is not False:
        fail("state/checkpoint overclaim")
    if st.get("independent_review_completed") is not False:
        fail("independent review overclaim")
    print("PASS_KT15_QUALIFIED_ATOMIC_APPLICATION_COMMIT")
else:
    fail("unexpected state")
