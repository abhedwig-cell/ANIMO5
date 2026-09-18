#!/usr/bin/env python3
import hashlib, json, pathlib, re, subprocess

R=pathlib.Path(__file__).resolve().parents[1]
BASE="fb0c0c842aed9a90378aca613279e09a856ad09b"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
BOUNDQ02="fb0c0c842aed9a90378aca613279e09a856ad09b"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"
FIXTURE_SHA="629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169"

def fail(msg):
    print("BOUNDQ02B FAIL_CLOSED:",msg)
    raise SystemExit(1)

def load(path):
    return json.loads((R/path).read_text())

def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-boundq02b/ANIMO-BOUNDQ02B_STATUS.json")
mf=load("integration/animo-boundq02b/BOUNDQ02B_INTEGRITY_MANIFEST.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

bq=show_json(BOUNDQ02,"integration/animo-boundq02/ANIMO-BOUNDQ02_STATUS.json")
if bq.get("state")!="QUALIFIED_REV53_STATIC_BOUNDARY_YEAR_CURSOR_AND_INTERVAL_BINDING_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ02 state")
if bq.get("interval_chemistry_frame_qualified") is not True:
    fail("BOUNDQ02 frame not qualified")
if bq.get("canonical_cursor_state_admitted") is not False:
    fail("BOUNDQ02 cursor state overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "C" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier C missing")

if mf.get("authorities",{}).get("BOUNDQ02")!=BOUNDQ02:
    fail("BOUNDQ02 authority manifest")
if mf.get("upstream_exact_final_ci",{}).get("BOUNDQ02_run")!=35373354465:
    fail("BOUNDQ02 exact-final run")
if mf.get("architecture_repair",{}).get("opaque_private_components") is not True:
    fail("opaque frame repair not declared")
if mf.get("architecture_repair",{}).get("validated_copy_out_access") is not True:
    fail("copy-out access not declared")
if mf.get("content_identity_contract",{}).get("computed_by_boundq02b") is not False:
    fail("hash computation overclaim")
if mf.get("content_identity_contract",{}).get("verified_against_source_bytes_by_boundq02b") is not False:
    fail("hash verification overclaim")

fixture=R/"tests/boundq01/fixtures/static_no_p.inp"
actual=hashlib.sha256(fixture.read_bytes()).hexdigest()
if actual!=FIXTURE_SHA:
    fail("fixture SHA256 drift "+actual)
if mf.get("synthetic_fixture",{}).get("sha256")!=FIXTURE_SHA:
    fail("fixture manifest SHA")

mod=(R/"prototype/boundq02b/mod_animo_immutable_static_boundary_frame.f90").read_text()
for required in [
    "type, public :: immutable_static_boundary_interval_frame_t",
    "private",
    "character(len=64) :: boundary_content_sha256",
    "public :: make_immutable_static_boundary_interval_frame",
    "public :: validate_immutable_static_boundary_interval_frame",
    "public :: inspect_immutable_static_boundary_interval_frame",
    "if (len_trim(value) /= 64) return",
    "forcing_id = 'SHA256='//trim(content_sha256)//':SLOT='//trim(slot_text)",
    "source_id = 'SHA256='//trim(boundary_content_sha256)",
    "call bind_static_boundary_interval(",
    "frame%chemistry = mutable_frame%chemistry",
    "BOUNDQ02B_FRAME_CONTENT_FORCING_ID_MISMATCH",
    "chemistry = frame%chemistry"
]:
    if required not in mod:
        fail("implementation drift "+required)

m=re.search(r"type, public :: immutable_static_boundary_interval_frame_t(.*?)end type immutable_static_boundary_interval_frame_t",mod,re.S|re.I)
if not m or not re.search(r"^\s*private\s*$",m.group(1),re.M|re.I):
    fail("frame components are not private")

for forbidden in [
    "public :: set_immutable_static_boundary",
    "public :: mutate_immutable_static_boundary",
    "read_rev53_static_boundary_chemistry"
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden owner widening "+forbidden)

test=(R/"tests/boundq02b/test_immutable_static_boundary_frame.f90").read_text()
for name in [
    "test_content_bound_frame",
    "test_accessor_returns_copy_not_mutable_frame",
    "test_content_identity_changes_forcing_identity",
    "test_bad_content_identity_rejected",
    "test_exact_interval_identity_rejected_when_stale"
]:
    if name not in test:
        fail("missing test "+name)
for required in [
    "chemistry1%precipitation%nh=999.0_real64",
    "chemistry1%forcing_id='MUTATED-COPY'",
    "'SHA256='//FIXTURE_SHA//':SLOT=1'",
    "uppercase noncanonical content identity rejected"
]:
    if required not in test:
        fail("copy/provenance test drift "+required)

neg=(R/"tests/boundq02b/compile_fail_public_frame_mutation.f90").read_text()
if "frame%selected_slot = 1" not in neg:
    fail("negative compile mutation probe missing")

script=(R/"tests/boundq02b/run_boundq02b_tests.sh").read_text()
if "private frame component was externally writable" not in script:
    fail("compile guard missing")
if "grep -qi \"private\"" not in script:
    fail("negative compile reason guard missing")

allowed_prefixes=("prototype/boundq02b/","tests/boundq02b/","docs/boundq02b/","integration/animo-boundq02b/")
allowed_exact={
 ".github/workflows/animo-boundq02b-immutable-frame.yml",
 "tools/validate_boundq02b_immutable_frame.py"
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
    print("PASS_BOUNDQ02B_AUTHORING")
elif st.get("state")=="QUALIFIED_OPAQUE_CONTENT_BOUND_STATIC_BOUNDARY_FRAME_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-boundq02b/ANIMO-BOUNDQ02B_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("opaque_frame_qualified") is not True or st.get("copy_out_access_qualified") is not True:
        fail("immutability qualification flags")
    if st.get("content_slot_identity_qualified") is not True:
        fail("content-slot identity qualification")
    if st.get("source_hash_verification_qualified") is not False:
        fail("hash verification overclaim")
    if st.get("canonical_forcing_state_admitted") is not False:
        fail("canonical forcing-state overclaim")
    print("PASS_BOUNDQ02B_QUALIFIED_IMMUTABLE_FRAME")
else:
    fail("unexpected state")
