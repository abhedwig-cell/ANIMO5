#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="df2310cc69e3fe16187ba2235843222f8acfb726"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
KT13A="df2310cc69e3fe16187ba2235843222f8acfb726"
BOUNDQ02="fb0c0c842aed9a90378aca613279e09a856ad09b"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT14 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def blob(path):
    return subprocess.check_output(["git","hash-object",path],cwd=R,text=True).strip()

st=load("integration/animo-kt14/ANIMO-KT14_STATUS.json")
mf=load("integration/animo-kt14/KT14_COMPOSITION_MANIFEST.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

k13=show_json(KT13A,"integration/animo-kt13a/ANIMO-KT13A_STATUS.json")
if k13.get("state")!="QUALIFIED_KT13_COMPOSITION_COHERENCE_REMEDIATION_INDEPENDENT_TIER_D_REVIEW_STILL_REQUIRED":
    fail("KT13A state")
if k13.get("work_status",{}).get("qualified") is not True:
    fail("KT13A not qualified")
if k13.get("scope",{}).get("production_changed") is not False:
    fail("KT13A production boundary")

bq=show_json(BOUNDQ02,"integration/animo-boundq02/ANIMO-BOUNDQ02_STATUS.json")
if bq.get("state")!="QUALIFIED_REV53_STATIC_BOUNDARY_YEAR_CURSOR_AND_INTERVAL_BINDING_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ02 state")
if bq.get("interval_chemistry_frame_qualified") is not True:
    fail("BOUNDQ02 frame qualification")
if bq.get("continuous_civil_year_selection_admitted") is not False:
    fail("BOUNDQ02 year-selection overclaim")
if bq.get("canonical_cursor_state_admitted") is not False:
    fail("BOUNDQ02 cursor state overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

if mf.get("authorities",{}).get("KT13A")!=KT13A or mf.get("authorities",{}).get("BOUNDQ02")!=BOUNDQ02:
    fail("authority manifest")
if mf.get("exact_final_upstream_evidence",{}).get("BOUNDQ02_run")!=35373354465:
    fail("BOUNDQ02 exact-final run pin")
if mf.get("exact_final_upstream_evidence",{}).get("BOUNDQ02_conclusion")!="success":
    fail("BOUNDQ02 exact-final conclusion")
if mf.get("exact_final_upstream_evidence",{}).get("KT13A_run")!=35370974894:
    fail("KT13A exact-final run pin")

expected_blobs={
 "prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90":"6b381ec9b37528b0decee8a2fa484e8124fc767d",
 "prototype/boundq02/mod_animo_static_boundary_year_binding.f90":"2b7441c9909022dcb16b3ca2f35ee08d079269b8",
 "prototype/kt13/mod_animo_tcd042_bounded_composition.f90":"6e2e4c73e9b43f5d1bda58dc9387a56be8b2e2b1",
 "tests/boundq01/fixtures/static_no_p.inp":"d1f71677b69199a0c3b5f9b0a9b92d47c06e82c0"
}
for path,sha in expected_blobs.items():
    if blob(path)!=sha:
        fail("frozen upstream blob drift "+path)

mod=(R/"prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90").read_text()
for required in [
 "call validate_static_boundary_interval_frame(",
 "if (.not. frame_ok) then",
 "KT14_BOUNDARY_INTERVAL_FRAME_INVALID",
 "trace%boundary_frame_validated = .true.",
 "trace%dry_deposition_nh = boundary_frame%dry_deposition_nh",
 "trace%dry_deposition_ni = boundary_frame%dry_deposition_ni",
 "boundary_frame%chemistry",
 "call execute_bounded_tcd042_composed_interval(",
 "KT14_BOUNDARY_FRAME_TCD042_INTERVAL_COMMITTED"
]:
    if required not in mod:
        fail("composition wiring drift "+required)
for forbidden in [
 "dry_deposition_nh +",
 "dry_deposition_ni +",
 "read_rev53_static_boundary_chemistry",
 "bind_static_boundary_interval(",
 "initialize_boundary_year_cursor"
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden ownership/wiring "+forbidden)

test=(R/"tests/kt14/test_kt14_boundary_frame_composition.f90").read_text()
for name in [
 "test_valid_exact_frame_commits",
 "test_stale_frame_rejects_before_science",
 "test_mutated_frame_provenance_rejects",
 "test_dry_deposition_is_not_wet_advective_forcing"
]:
    if name not in test:
        fail("missing test "+name)
for required in [
 "frame%chemistry%forcing_id='MUTATED'",
 "trace%science%science_runtime_committed",
 "transfer(c1,0_int64)==transfer(c2,0_int64)",
 "transfer(trace1%science%selected_load_rate,0_int64)=="
]:
    if required not in test:
        fail("adversarial test oracle missing "+required)

allowed_prefixes=("prototype/kt14/","tests/kt14/","docs/kt14/","integration/animo-kt14/")
allowed_exact={
 ".github/workflows/animo-kt14-boundary-frame-composition.yml",
 "tools/validate_kt14_boundary_frame_composition.py",
 "prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90",
 "prototype/boundq02/mod_animo_static_boundary_year_binding.f90",
 "tests/boundq01/fixtures/static_no_p.inp"
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
    print("PASS_KT14_AUTHORING")
elif st.get("state")=="QUALIFIED_BOUNDQ02_EXACT_FRAME_TO_KT13A_TCD042_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt14/ANIMO-KT14_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("boundary_frame_identity_qualified") is not True or st.get("chemistry_time_binding_qualified") is not True:
        fail("frame/time qualification")
    if st.get("bounded_tcd042_composition_qualified") is not True:
        fail("composition qualification")
    if st.get("year_cursor_atomic_commit_qualified") is not False or st.get("multi_interval_continuation_qualified") is not False:
        fail("continuation overclaim")
    if st.get("independent_review_completed") is not False:
        fail("independence overclaim")
    print("PASS_KT14_QUALIFIED_EXACT_FRAME_COMPOSITION")
else:
    fail("unexpected state")
