#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="62b4fc36f2a47b67c08eedb095c60a5c059b77d8"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
BOUNDQ01="62b4fc36f2a47b67c08eedb095c60a5c059b77d8"
UBFORCE02="931e32cec69dc78a03015f01190cff97bf1fe1b4"
TIME02="b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("BOUNDQ02 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-boundq02/ANIMO-BOUNDQ02_STATUS.json")
mp=load("integration/animo-boundq02/BOUNDQ02_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

bq1=show_json(BOUNDQ01,"integration/animo-boundq01/ANIMO-BOUNDQ01_STATUS.json")
if bq1.get("state")!="QUALIFIED_REV53_STATIC_BOUNDARY_CHEMISTRY_ADAPTER_TIER_C_REVIEW_REQUIRED":
    fail("BOUNDQ01 state")
if bq1.get("source_grammar_qualified") is not True or bq1.get("typed_adapter_qualified") is not True:
    fail("BOUNDQ01 qualification")

ub2=show_json(UBFORCE02,"integration/animo-ubforce02/ANIMO-UBFORCE02_STATUS.json")
if ub2.get("state")!="QUALIFIED_TCD042_UPPER_SOLUTE_LOAD_RESOLVER_TIER_D_REVIEW_REQUIRED":
    fail("UBFORCE02 state")
if ub2.get("resolver_qualified") is not True:
    fail("UBFORCE02 resolver")

time2=show_json(TIME02,"integration/animo-time/ANIMO-TIME02_STATUS.json")
if time2.get("qualified") is not True:
    fail("TIME02 not qualified")
cand=time2.get("candidate",{})
if cand.get("calendar_contract_id")!="ANIMO_PG_86400_NOLEAPSECONDS_V1":
    fail("TIME02 calendar identity")
if cand.get("epoch")!="0001-01-01T00:00:00" or cand.get("epoch_day_index")!="0":
    fail("TIME02 epoch")
if time2.get("legacy_compatibility_envelope",{}).get("conservative_qualified_year_max")!=3000:
    fail("TIME02 year envelope")
if time2.get("canonical_time_admitted") is not False:
    fail("TIME02 canonical admission overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "C" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier C missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
members=mp.get("source_members",{})
if members.get("Animo.for",{}).get("sha256")!="352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7":
    fail("Animo.for pin")
init=members.get("Init.for",{})
if init.get("sha256")!="287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058":
    fail("Init.for pin")
if init.get("year_origin")!="GDATE(Juda-St, Yr, MONTH, DAY, ...)":
    fail("source interval-origin mapping")
if init.get("slot_formula")!="Yn=Yr-Yrmi+1":
    fail("source slot formula")
if init.get("refresh_predicate")!="Juda-St<=Judami OR (Month==1 AND Day==1)":
    fail("source refresh predicate")
if init.get("refresh_assignments")!=[
    "Coprnhyn=Coprnh(Yn)",
    "Coprniyn=Coprni(Yn)",
    "Coprpoyn=Coprpo(Yn)",
    "Drdepnhyn=Drdepnh(Yn)",
    "Drdepniyn=Drdepni(Yn)"
]:
    fail("source refresh assignments")

cur=mp.get("cursor_semantics",{})
if cur.get("first_interval")!="SELECT_SLOT_FROM_ORIGIN_YEAR":
    fail("first interval cursor semantics")
if cur.get("later_exact_january_first")!="REFRESH_SLOT_FROM_ORIGIN_YEAR":
    fail("Jan1 cursor semantics")
if cur.get("later_non_january_first")!="PRESERVE_ACCEPTED_ACTIVE_SLOT":
    fail("non-Jan1 cursor semantics")
if cur.get("mutate_accepted_cursor_in_binding") is not False:
    fail("accepted cursor mutation")
frame=mp.get("frame_semantics",{})
if frame.get("exact_origin_bound") is not True or frame.get("exact_endpoint_bound") is not True:
    fail("frame identity")
if frame.get("dry_deposition_separate") is not True:
    fail("dry deposition separation")

mod=(R/"prototype/boundq02/mod_animo_static_boundary_year_binding.f90").read_text()
for required in [
    "BOUNDQ02_CALENDAR_ID =",
    "'ANIMO_PG_86400_NOLEAPSECONDS_V1'",
    "if (.not. accepted_cursor%initialized) then",
    "else if (origin_month == 1 .and. origin_day == 1) then",
    "slot = accepted_cursor%active_slot",
    "next_cursor = accepted_cursor",
    "frame%origin_time = origin_time",
    "frame%endpoint_time = endpoint_time",
    "frame%dry_deposition_nh = boundary%dry_deposition_nh(slot)",
    "frame%dry_deposition_ni = boundary%dry_deposition_ni(slot)",
    "call make_tcd042_upper_chemistry_forcing",
    "SUBDAY_BOUNDARY_YEAR_SELECTION_NOT_QUALIFIED",
    "BOUNDQ02_YEAR_SLOT_OUT_OF_RANGE"
]:
    if required not in mod:
        fail("implementation drift "+required)
for forbidden in [
    "slot = origin_year - simulation_start_year + 1 ! every interval",
    "dry_deposition_nh +",
    "dry_deposition_ni +",
    ">runoti:",
    ">irriti:"
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden semantics "+forbidden)

test=(R/"tests/boundq02/test_static_boundary_year_binding.f90").read_text()
for name in [
    "test_first_interval_midyear_selects_origin_year",
    "test_exact_january_first_refreshes_slot",
    "test_skipped_january_first_preserves_legacy_cursor",
    "test_phosphorus_binding_and_dry_dep_separation",
    "test_interval_and_calendar_fail_closed"
]:
    if name not in test:
        fail("missing test "+name)
for day in ["730301_int64","730485_int64","730486_int64"]:
    if day not in test:
        fail("calendar vector missing "+day)

allowed_prefixes=("prototype/boundq02/","tests/boundq02/","docs/boundq02/","integration/animo-boundq02/")
allowed_exact={
 ".github/workflows/animo-boundq02-static-boundary-year-binding.yml",
 "tools/validate_boundq02_static_boundary_year_binding.py"
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
    print("PASS_BOUNDQ02_AUTHORING")
elif st.get("state")=="QUALIFIED_REV53_STATIC_BOUNDARY_YEAR_CURSOR_AND_INTERVAL_BINDING_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-boundq02/ANIMO-BOUNDQ02_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_year_cursor_semantics_qualified") is not True:
        fail("cursor qualification")
    if st.get("exact_calendar_binding_qualified") is not True or st.get("interval_chemistry_frame_qualified") is not True:
        fail("frame qualification")
    if st.get("continuous_civil_year_selection_admitted") is not False:
        fail("continuous year selection overclaim")
    if st.get("canonical_cursor_state_admitted") is not False or st.get("checkpoint_schema_admitted") is not False:
        fail("cursor state/checkpoint overclaim")
    print("PASS_BOUNDQ02_QUALIFIED_YEAR_BINDING")
else:
    fail("unexpected state")
