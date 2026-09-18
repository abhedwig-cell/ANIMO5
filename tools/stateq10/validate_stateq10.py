#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[2]
BASE="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
STATEQ08="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("STATEQ10 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-state/ANIMO-STATEQ10_STATUS.json")
mp=load("integration/animo-state/STATEQ10_FIRST_ORIGIN_SOURCE_MAPPING.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

s8=show_json(STATEQ08,"integration/animo-state/ANIMO-STATEQ08_STATUS.json")
if s8.get("state")!="QUALIFIED_RUNINU_DETAILED_HYDROLOGY_EXECUTION_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    fail("STATEQ08 state")
if s8.get("first_call_runinu_value")!="UNQUALIFIED_SOURCE_UNDEFINED":
    fail("STATEQ08 first-call Runinu boundary")
if s8.get("canonical_state_admitted") is not False:
    fail("STATEQ08 canonical state overclaim")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "C" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier C missing")

if mp.get("source_archive_sha256")!="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive pin")
members=mp.get("source_members",{})
inp=members.get("input1.for",{})
if inp.get("sha256")!="041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95":
    fail("input1 pin")
if inp.get("mapped_lines")!="2629-2648":
    fail("input1 mapped range")
if inp.get("bounded_route")!="Hlpimp=11 AND Iopthyvs=1":
    fail("input route")
expected_assign=[
    "Mofro(Ln)=Dble_trunc(SMofro(Ln))",
    "Sic=Dble_trunc(sSic)",
    "Pn=Dble_trunc(SPn)",
    "Snla=Dble_trunc(SSnla)"
]
if inp.get("assignments")!=expected_assign:
    fail("input assignments")
fn=members.get("Function.for",{})
if fn.get("sha256")!="8d18e2558b43d38382033ed43a77bf00a71995804a20db0253f3a9795d748e59":
    fail("Function.for pin")
if fn.get("function")!="Dble_trunc" or fn.get("input_type")!="REAL(4)" or fn.get("output_type")!="REAL(8)":
    fail("Dble_trunc type contract")
if fn.get("integer_part")!="KINT(R4)" or fn.get("final_rounding")!="KIDNNT(R8)":
    fail("Dble_trunc intrinsic mapping")

typed=mp.get("typed_first_origin",{})
if typed.get("fields")!=["Pn","Sic","Snla","Mofro(1:Nl)"]:
    fail("typed origin fields")
if typed.get("Runinu_included") is not False:
    fail("Runinu leaked into first-origin type")
scope=mp.get("scope_boundary",{})
if scope.get("parser_qualified") is not False or scope.get("b2_claimed") is not False:
    fail("parser/B2 overclaim")

mod=(R/"prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90").read_text()
for required in [
    "i = int(r4, kind=int64)",
    "r = mod(r4, one)",
    "if (exact_real32_zero(r)) then",
    "help = -log10(abs(r))",
    "i4 = int(help - 0.9999999_real32, kind=int32)",
    "scale4 = 10.0_real32 ** (i4 + 7_int32)",
    "rounded = nint(r8, kind=int64)",
    "value = real(rounded, real64) / real(scale4, real64) + real(i, real64)",
    "value%pn = normalize_rev53_real4(spn)",
    "value%sic = normalize_rev53_real4(ssic)",
    "value%snla = normalize_rev53_real4(ssnla)",
    "value%mofro(ln) = normalize_rev53_real4(smofro(ln))"
]:
    if required not in mod:
        fail("implementation/source mapping drift "+required)
if "runinu" in mod.lower():
    fail("Runinu leaked into STATEQ10")

test=(R/"tests/stateq10/test_first_detailed_hydrology_origin.f90").read_text()
for bits in [
    "3FBF9ADD6678041E",
    "405EDD3BE0157EED",
    "BF202E85D6418B53",
    "3FF0000000000000"
]:
    if bits not in test:
        fail("Dble_trunc exact oracle missing "+bits)
for name in [
    "test_dble_trunc_exact_oracles",
    "test_first_origin_normalization",
    "test_nonfinite_rejected",
    "test_unallocated_profile_rejected"
]:
    if name not in test:
        fail("missing test "+name)

allowed_prefixes=(
    "prototype/stateq10/","tests/stateq10/","tools/stateq10/",
    "docs/state/ANIMO_STATEQ10_","integration/animo-state/ANIMO-STATEQ10",
    "integration/animo-state/STATEQ10_"
)
allowed_exact={".github/workflows/animo-stateq10-first-detailed-origin.yml"}
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
    print("PASS_STATEQ10_AUTHORING")
elif st.get("state")=="QUALIFIED_FIRST_INTERVAL_DETAILED_HYDROLOGY_ORIGIN_NORMALIZATION_TIER_C_REVIEW_REQUIRED":
    rv=load("integration/animo-state/ANIMO-STATEQ10_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("source_mapping_qualified") is not True or st.get("dble_trunc_semantics_qualified") is not True or st.get("typed_first_origin_qualified") is not True:
        fail("qualification flags")
    if st.get("file_parser_qualified") is not False or st.get("first_call_runinu_qualified") is not False:
        fail("scope overclaim")
    if st.get("canonical_state_admitted") is not False or st.get("historical_b2_claimed") is not False:
        fail("state/B2 overclaim")
    print("PASS_STATEQ10_QUALIFIED_FIRST_ORIGIN")
else:
    fail("unexpected state")
