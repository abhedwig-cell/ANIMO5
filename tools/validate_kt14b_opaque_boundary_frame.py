#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="3e4dc99baa5c343041857f8cd44cd316481fb478"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
KT13A="df2310cc69e3fe16187ba2235843222f8acfb726"
BOUNDQ02B="de6eef3122354e74405ff9c92286794714bdee82"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT14B FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def blob(path):
    return subprocess.check_output(["git","hash-object",path],cwd=R,text=True).strip()

st=load("integration/animo-kt14b/ANIMO-KT14B_STATUS.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

k=show_json(KT13A,"integration/animo-kt13a/ANIMO-KT13A_STATUS.json")
if k.get("state")!="QUALIFIED_KT13_COMPOSITION_COHERENCE_REMEDIATION_INDEPENDENT_TIER_D_REVIEW_STILL_REQUIRED":
    fail("KT13A state")

b=show_json(BOUNDQ02B,"integration/animo-boundq02b/ANIMO-BOUNDQ02B_STATUS.json")
if b.get("state")!="QUALIFIED_OPAQUE_CONTENT_BOUND_STATIC_BOUNDARY_FRAME_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ02B state")
if b.get("opaque_frame_qualified") is not True or b.get("copy_out_access_qualified") is not True:
    fail("BOUNDQ02B opaque/copyout qualification")
if b.get("source_hash_verification_qualified") is not False:
    fail("BOUNDQ02B source hash verification overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

if blob("prototype/boundq02b/mod_animo_immutable_static_boundary_frame.f90")!="eae62a2ce077e3e568a8a73b25ac45d20c432bae":
    fail("BOUNDQ02B implementation blob drift")

mod=(R/"prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90").read_text()
for required in [
    "immutable_static_boundary_interval_frame_t",
    "inspect_immutable_static_boundary_interval_frame",
    "boundary_content_sha256",
    "trace%boundary_content_sha256 = content_sha256",
    "trace%dry_deposition_nh = dry_nh",
    "execute_bounded_tcd042_composed_interval"
]:
    if required not in mod:
        fail("opaque composition implementation drift "+required)
for forbidden in [
    "type(static_boundary_interval_frame_t)",
    "validate_static_boundary_interval_frame",
    "boundary_frame%chemistry",
    "boundary_frame%dry_deposition_nh",
    "boundary_frame%selected_slot"
]:
    if forbidden.lower() in mod.lower():
        fail("direct mutable frame access retained "+forbidden)

test=(R/"tests/kt14/test_kt14_boundary_frame_composition.f90").read_text()
for required in [
    "immutable_static_boundary_interval_frame_t",
    "make_immutable_static_boundary_interval_frame",
    "test_valid_opaque_frame_commits",
    "test_stale_opaque_frame_rejects_before_science",
    "test_content_identity_is_bound_and_science_value_stable",
    "test_dry_deposition_is_not_wet_advective_forcing",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
]:
    if required not in test:
        fail("opaque test coverage drift "+required)
if "frame%chemistry" in test.lower() or "frame%dry_deposition" in test.lower():
    fail("test illegally mutates opaque frame")

allowed_prefixes=("docs/kt14b/","integration/animo-kt14b/")
allowed_exact={
    "prototype/boundq02b/mod_animo_immutable_static_boundary_frame.f90",
    "prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90",
    "tests/kt14/test_kt14_boundary_frame_composition.f90",
    "tests/kt14/run_kt14_tests.sh",
    ".github/workflows/animo-kt14b-opaque-boundary-frame.yml",
    "tools/validate_kt14b_opaque_boundary_frame.py"
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
    print("PASS_KT14B_AUTHORING")
elif st.get("state")=="QUALIFIED_OPAQUE_BOUNDQ02B_FRAME_TO_KT13A_TCD042_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt14b/ANIMO-KT14B_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for field in [
        "opaque_frame_consumption_qualified",
        "content_identity_propagation_qualified",
        "copy_out_only_boundary_access_qualified",
        "dry_deposition_separation_qualified",
        "bounded_tcd042_composition_qualified"
    ]:
        if st.get(field) is not True:
            fail("qualification flag "+field)
    if st.get("independent_review_completed") is not False:
        fail("independent review overclaim")
    print("PASS_KT14B_QUALIFIED_OPAQUE_COMPOSITION")
else:
    fail("unexpected state")
