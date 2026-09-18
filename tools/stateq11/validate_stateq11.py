#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[2]
BASE="fb0c0c842aed9a90378aca613279e09a856ad09b"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
S8="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
S9="f6e91fc1cb664d67caccc02e6ab21525a768d006"
S10="614391014438b2cc4445d2d6a8008c3f0f1c45d0"
BQ2="fb0c0c842aed9a90378aca613279e09a856ad09b"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("STATEQ11 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def blob(path):
    return subprocess.check_output(["git","hash-object",path],cwd=R,text=True).strip()

st=load("integration/animo-state/ANIMO-STATEQ11_STATUS.json")
mf=load("integration/animo-state/STATEQ11_COMPOSITION_MANIFEST.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

s8=show_json(S8,"integration/animo-state/ANIMO-STATEQ08_STATUS.json")
if s8.get("continuation_classification_qualified") is not True:
    fail("STATEQ08 continuation classification")
if s8.get("first_call_runinu_value")!="UNQUALIFIED_SOURCE_UNDEFINED":
    fail("STATEQ08 first-call Runinu boundary")
if s8.get("canonical_state_admitted") is not False:
    fail("STATEQ08 canonical state overclaim")

s9=show_json(S9,"integration/animo-state/ANIMO-STATEQ09_STATUS.json")
if s9.get("typed_origin_state_qualified") is not True or s9.get("source_transfer_semantics_qualified") is not True:
    fail("STATEQ09 qualification")
if s9.get("initial_condition_qualified") is not False:
    fail("STATEQ09 initial-condition overclaim")

s10=show_json(S10,"integration/animo-state/ANIMO-STATEQ10_STATUS.json")
if s10.get("typed_first_origin_qualified") is not True or s10.get("dble_trunc_semantics_qualified") is not True:
    fail("STATEQ10 qualification")
if s10.get("first_call_runinu_qualified") is not False:
    fail("STATEQ10 Runinu overclaim")

bq=show_json(BQ2,"integration/animo-boundq02/ANIMO-BOUNDQ02_STATUS.json")
if bq.get("interval_chemistry_frame_qualified") is not True or bq.get("source_year_cursor_semantics_qualified") is not True:
    fail("BOUNDQ02 qualification")
if bq.get("canonical_cursor_state_admitted") is not False:
    fail("BOUNDQ02 cursor admission overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

auth=mf.get("authorities",{})
for name,sha in {"RG06":RG06,"STATEQ08":S8,"STATEQ09":S9,"STATEQ10":S10,"BOUNDQ02":BQ2}.items():
    if auth.get(name)!=sha:
        fail("authority manifest "+name)
expected_runs={
 "STATEQ08":35368900188,
 "STATEQ09":35370652476,
 "STATEQ10":35371035447,
 "BOUNDQ02":35373354465
}
for name,run in expected_runs.items():
    if mf.get("exact_final_ci",{}).get(name,{}).get("run")!=run or        mf.get("exact_final_ci",{}).get(name,{}).get("conclusion")!="success":
        fail("exact-final CI manifest "+name)

expected_blobs={
 "prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90":"e55a72fd37b20addaf7131ed085b417768b84a1c",
 "prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90":"7c4144785ae023abb3ff3fe4e760519c650626b8",
 "prototype/boundq02/mod_animo_static_boundary_year_binding.f90":"2b7441c9909022dcb16b3ca2f35ee08d079269b8"
}
for path,sha in expected_blobs.items():
    if blob(path)!=sha:
        fail("frozen upstream blob drift "+path)

mod=(R/"prototype/stateq11/mod_animo_composite_accepted_continuation.f90").read_text()
for required in [
 "character(len=TRANSIENT_ID_LEN) :: lineage_id",
 "integer(int64) :: generation = -1_int64",
 "type(TimeCoordinate) :: accepted_time",
 "type(detailed_hydrology_origin_state_t) :: hydrology_origin",
 "real(real64) :: runinu_call_entry",
 "type(boundary_year_cursor_t) :: boundary_cursor",
 "call validate_first_detailed_hydrology_origin",
 "call advance_origin_from_accepted_endpoint",
 "candidate%generation = current%generation + 1_int64",
 "candidate%runinu_call_entry = runinu_next",
 "candidate%boundary_cursor = next_boundary_cursor",
 "accepted_store_generation(store)",
 "accepted_store_lineage(store)",
 "call time_equal(value%accepted_time, store_time"
]:
    if required not in mod:
        fail("composite implementation drift "+required)

for forbidden in [
 "runinu_call_entry = 0.0_real64 ! first-call",
 "checkpoint",
 "commit_trial(",
 "bind_static_boundary_interval("
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden ownership/commit semantics "+forbidden)

test=(R/"tests/stateq11/test_composite_accepted_continuation.f90").read_text()
for name in [
 "test_first_origin_composite_matches_store",
 "test_next_candidate_advances_all_sidecar_state",
 "test_stale_generation_rejected",
 "test_time_mismatch_rejected",
 "test_invalid_next_cursor_rejected"
]:
    if name not in test:
        fail("missing test "+name)
if "3E10000000000000" not in test or "3E20000000000000" not in test:
    fail("explicit Runinu binary64 oracle missing")

allowed_prefixes=(
 "prototype/stateq11/","tests/stateq11/","tools/stateq11/",
 "docs/state/ANIMO_STATEQ11_","integration/animo-state/ANIMO-STATEQ11",
 "integration/animo-state/STATEQ11_"
)
allowed_exact={
 ".github/workflows/animo-stateq11-composite-continuation.yml",
 "prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90",
 "prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90"
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
    print("PASS_STATEQ11_AUTHORING")
elif st.get("state")=="QUALIFIED_COMPOSITE_ACCEPTED_CONTINUATION_IDENTITY_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-state/ANIMO-STATEQ11_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for key in [
      "composite_identity_qualified","first_origin_bridge_qualified",
      "endpoint_to_origin_advance_qualified","runinu_continuation_binding_qualified",
      "boundary_cursor_binding_qualified","accepted_store_coherence_qualified"
    ]:
        if st.get(key) is not True:
            fail("qualification flag "+key)
    if st.get("atomic_group_commit_implemented") is not False:
        fail("atomic commit overclaim")
    if st.get("canonical_state_admitted") is not False or st.get("checkpoint_schema_admitted") is not False:
        fail("canonical state/checkpoint overclaim")
    print("PASS_STATEQ11_QUALIFIED_COMPOSITE_IDENTITY")
else:
    fail("unexpected state")
