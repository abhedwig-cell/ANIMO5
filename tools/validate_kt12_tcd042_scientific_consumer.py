#!/usr/bin/env python3
import json, pathlib, re, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="50731bf118deb8ef1029f220a40b39a99240e480"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
RG05M="7146612d5dfa8ad87a4660f0c50c68a5db1e3a29"
B3D35="9ca23f41dc3c28af686b1bc0bff8e7d66416d367"
B3D33="8b2a4071d623bc2e3003dca8977e032d5c0d8c3c"
B3D34="22e4ec3bb88e2e13905ccbbb2f380a9bf235db55"
UBQ01="6895b67799f26888025eced7188e7190b2a0d07d"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT12 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    out=subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True)
    return json.loads(out)

status=load("integration/animo-kt12/ANIMO-KT12_STATUS.json")
rec=load("integration/animo-kt12/ANIMO-KT12_RECONCILIATION.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 not qualified")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 production gate unexpectedly open")

m=show_json(RG05M,"integration/animo-reg/ANIMO-RG05M_STATUS.json")
t=m.get("tcd042_state",{})
if t.get("parent_admitted") is not True:
    fail("TCD042 parent not admitted in aggregate lineage")
if t.get("Hetop_zero_admitted") is not False or t.get("production_authorized") is not False:
    fail("TCD042 aggregate scope widened")

p=show_json(B3D35,"integration/animo-b3/ANIMO-B3D35_STATUS.json")
expected_scope="Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))"
if p.get("admitted") is not True or p.get("parent_tcd_admitted") is not True:
    fail("B3D35 parent admission")
if p.get("supported_scope")!=expected_scope:
    fail("B3D35 scope mismatch")
if p.get("admission_effect",{}).get("production_authorized") is not False:
    fail("B3D35 production boundary")

b1=show_json(B3D33,"integration/animo-b3/ANIMO-B3D33_STATUS.json")
if b1.get("admitted") is not True or b1.get("supported_scope")!="Flpn=0 AND Flux=0 AND Hetop>0":
    fail("B1 admission")

e1=show_json(B3D34,"integration/animo-b3/ANIMO-B3D34_STATUS.json")
if e1.get("admitted") is not True:
    fail("E1 admission")
if "0<Flux<1.0d-8" not in e1.get("supported_scope",""):
    fail("E1 scope")

ubq=show_json(UBQ01,"integration/animo-science/ANIMO-UBQ01_STATUS.json")
atom=ubq.get("atomization",{})
if atom.get("exact_zero_end_state")!="C1=C0+Load*St/Hetop":
    fail("UBQ01 exact-zero equation")
if atom.get("exact_zero_average_state")!="Cavg=C0+Load*St/(2*Hetop)":
    fail("UBQ01 exact-zero average")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("GOV04 Tier D missing")

kt05=(R/"prototype/kt05/mod_animo_hydrology_adapter.f90").read_text()
carrier=re.search(r"type, public :: hydrology_step_t(.*?)end type hydrology_step_t",kt05,re.S|re.I)
if not carrier:
    fail("KT05 carrier missing")
body=carrier.group(1).lower()
for forbidden in [" flib", " rurv", " flpn"]:
    if forbidden in body:
        fail("KT05 unexpectedly carries resolved field "+forbidden.strip())
if "real(real64), allocatable :: flab(:)" not in body:
    fail("KT05 raw Flab missing")

kt05_contract=(R/"docs/kt05/WORK_UNIT_CONTRACT.md").read_text()
for phrase in ["runoff partitioning","Modflux","accepted"]:
    if phrase not in kt05_contract:
        fail("KT05 ownership exclusion drift: "+phrase)

mod=(R/"prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90").read_text()
for required in [
    "TCD042_P_MAX = 3.8510200002999744e-7_real64",
    "TCD042_FLUX_THRESHOLD = 1.0e-8_real64",
    "if (hydrology%flpn /= 0) return",
    "if (hydrology%rurv /= 0.0_real64) return",
    "flux = max(0.0_real64, flux_sum)",
    "a2 = st / self%hetop",
    "b2 = st / (2.0_real64 * self%hetop)",
    "f = 1.0_real64 - p / 2.0_real64 + p * p / 6.0_real64",
    "g = 0.5_real64 - p / 6.0_real64 + p * p / 24.0_real64"
]:
    if required not in mod:
        fail("KT12 implementation contract drift: "+required)

if rec.get("direct_composition",{}).get("ready") is not False:
    fail("direct KT11 composition incorrectly ready")
if rec.get("direct_composition",{}).get("blocker")!="NO_QUALIFIED_POST_HYDRO_DETAILED_RESOLVED_HYDROLOGY_OUTPUT_AUTHORITY":
    fail("direct composition blocker")
if rec.get("kt05_boundary",{}).get("raw_flab1_is_not_authoritative_tcd042_flux") is not True:
    fail("raw Flab shortcut not rejected")

allowed_prefixes=(
    "prototype/kt12/","tests/kt12/","docs/kt12/","integration/animo-kt12/",
)
allowed_exact={
    ".github/workflows/animo-kt12-tcd042-scientific-consumer.yml",
    "tools/validate_kt12_tcd042_scientific_consumer.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)
if any(p.startswith("src/") for p in changed):
    fail("production source modified")

for k,v in status.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard boundary "+k)

if status.get("state")=="NOT_YET_QUALIFIED":
    if status.get("work_status",{}).get("qualified") is not False:
        fail("authoring qualified too early")
    print("PASS_KT12_AUTHORING_CONTRACT")
elif status.get("state")=="QUALIFIED_BOUNDED_TCD042_TRANSACTION_RUNTIME_CLIENT_DIRECT_KT11_SCIENCE_COMPOSITION_BLOCKED_TIER_D_REVIEW_REQUIRED":
    review=load("integration/animo-kt12/ANIMO-KT12_ADVERSARIAL_REVIEW.json")
    if review.get("outcome")!="SELF_REVIEW_PASS":
        fail("self review outcome")
    if review.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or review.get("genuinely_independent") is not False:
        fail("review assurance")
    if status.get("review",{}).get("independent_tier_d_review_required_for_admission") is not True:
        fail("independent Tier D gate removed")
    if status.get("work_status",{}).get("qualified") is not True:
        fail("final candidate not qualified")
    print("PASS_KT12_BOUNDED_SCIENTIFIC_RUNTIME_CANDIDATE")
else:
    fail("unexpected status state")
