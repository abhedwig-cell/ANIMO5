#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="931e32cec69dc78a03015f01190cff97bf1fe1b4"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
KT06="56384db4107aed484218363e26dbb7be7f51e8de"
KT12="8f0e8e4bfd0b391b781f7c69b7d2063d5cf8705e"
H1="5301d90024c64057f2cb88fda1dbaa93aabfca47"
H2="08d5b8301c217cf9d33d2bf248be133f2b5243fc"
HEX="182dac2fc34ca42ed798203e90efeca1221f21e8"
UB1="9f9204ba53169285ac84272704de14836962ef41"
UB2="931e32cec69dc78a03015f01190cff97bf1fe1b4"
S8="e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07"
B3D35="9ca23f41dc3c28af686b1bc0bff8e7d66416d367"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT13 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))
def blob(path):
    return subprocess.check_output(["git","hash-object",path],cwd=R,text=True).strip()

st=load("integration/animo-kt13/ANIMO-KT13_STATUS.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("program gates")

kt12=show_json(KT12,"integration/animo-kt12/ANIMO-KT12_STATUS.json")
if kt12.get("state")!="QUALIFIED_BOUNDED_TCD042_TRANSACTION_RUNTIME_CLIENT_DIRECT_KT11_SCIENCE_COMPOSITION_BLOCKED_TIER_D_REVIEW_REQUIRED":
    fail("KT12 state")

h1=show_json(H1,"integration/animo-hydroq01/ANIMO-HYDROQ01_STATUS.json")
if h1.get("typed_contract_qualified") is not True or h1.get("source_mapping_qualified") is not True:
    fail("HYDROQ01 qualification")
h2=show_json(H2,"integration/animo-hydroq02/ANIMO-HYDROQ02_STATUS.json")
if h2.get("typed_context_qualified") is not True or h2.get("near_zero_runinu_semantics_repaired") is not False:
    fail("HYDROQ02 qualification")

hx=show_json(HEX,"integration/animo-hydroexec01/ANIMO-HYDROEXEC01_STATUS.json")
if hx.get("state")!="QUALIFIED_BOUNDED_REV53_NO_PONDING_UPPER_HYDROLOGY_EXECUTION_TIER_D_REVIEW_REQUIRED":
    fail("HYDROEXEC01 state")
if hx.get("bounded_execution_qualified") is not True:
    fail("HYDROEXEC01 bounded execution")
if hx.get("runinu_canonical_state_ownership_qualified") is not False:
    fail("HYDROEXEC01 Runinu ownership")

ub1=show_json(UB1,"integration/animo-ubforce01/ANIMO-UBFORCE01_STATUS.json")
if ub1.get("typed_contract_qualified") is not True:
    fail("UBFORCE01 contract")
ub2=show_json(UB2,"integration/animo-ubforce02/ANIMO-UBFORCE02_STATUS.json")
if ub2.get("state")!="QUALIFIED_TCD042_UPPER_SOLUTE_LOAD_RESOLVER_TIER_D_REVIEW_REQUIRED":
    fail("UBFORCE02 state")
if ub2.get("resolver_qualified") is not True:
    fail("UBFORCE02 resolver")

s8=show_json(S8,"integration/animo-state/ANIMO-STATEQ08_STATUS.json")
if s8.get("state")!="QUALIFIED_RUNINU_DETAILED_HYDROLOGY_EXECUTION_CONTINUATION_TIER_C_REVIEW_REQUIRED":
    fail("STATEQ08 state")
if s8.get("continuation_classification_qualified") is not True:
    fail("STATEQ08 classification")
if s8.get("canonical_state_admitted") is not False or s8.get("model_evolution_zeroing_admitted") is not False:
    fail("STATEQ08 state/model-evolution overclaim")

p=show_json(B3D35,"integration/animo-b3/ANIMO-B3D35_STATUS.json")
expected="Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))"
if p.get("supported_scope")!=expected or p.get("admitted") is not True:
    fail("TCD042 parent authority")
if p.get("admission_effect",{}).get("production_authorized") is not False:
    fail("TCD042 production boundary")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

expected_blobs={
 "prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90":"9a24ea833291f761d2fa76ca4cc9fee28436c614",
 "prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90":"e9ef255f9905e5b4fe3d8761f2ecd7105a6451ad",
 "prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90":"081e6b45e777ebccb852b3d1adde05ed6baaeb6a",
 "prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90":"786dce177c50c91149dad33289306f935b61b354",
 "prototype/hydroexec01/mod_animo_bounded_no_ponding_upper_hydrology.f90":"b4b621d1957291b7cf26931fe065d2cbcb89e71c",
 "prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90":"fbe12e01df715ed7c95c59f5dd6b1ee73604034f",
 "prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90":"a82bd7ef40ce18ddb00e45933290d1999de05884"
}
for path,sha in expected_blobs.items():
    if blob(path)!=sha:
        fail("frozen implementation drift "+path)

mod=(R/"prototype/kt13/mod_animo_tcd042_bounded_composition.f90").read_text()
for required in [
 "binding_client%forcing = selected_packet",
 "call binding_client%execute_attempt",
 "call project_hydro_detailed_explicit",
 "call resolve_rev53_no_ponding_upper_hydrology",
 "load_hydrology%rupr = runoff_context%rupr",
 "load_hydrology%runinu = runoff_context%runinu",
 "call resolve_tcd042_upper_loads",
 "call select_tcd042_load_channel",
 "call configure_tcd042_client",
 "call run_interval",
 "KT13_BOUNDED_TCD042_INTERVAL_COMMITTED"
]:
    if required not in mod:
        fail("composition wiring drift "+required)

for forbidden in [
 "initialize_multi_packet_client",
 "Hydro_detailed(",
 "subroutine Hydro_detailed",
 "Runinu = 0.0_real64 ! near-zero",
 "BOUNDARY.INP"
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden composition semantics "+forbidden)

test=(R/"tests/kt13/test_kt13_bounded_composition.f90").read_text()
for name in [
 "test_finite_positive_end_to_end_commit",
 "test_runinu_continuation_is_material",
 "test_kt06_binding_failure_preserves_store",
 "test_tcd042_scope_reject_preserves_store"
]:
    if name not in test:
        fail("missing test "+name)
for bits in ["3E10000000000000","3E20000000000000"]:
    if bits not in test:
        fail("missing exact binary64 composition oracle "+bits)

allowed_prefixes=("prototype/kt13/","tests/kt13/","docs/kt13/","integration/animo-kt13/")
allowed_exact={
 ".github/workflows/animo-kt13-bounded-tcd042-composition.yml",
 "tools/validate_kt13_bounded_tcd042_composition.py",
 "prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90",
 "prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90",
 "prototype/hydroexec01/mod_animo_bounded_no_ponding_upper_hydrology.f90"
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
    print("PASS_KT13_AUTHORING")
elif st.get("state")=="QUALIFIED_BOUNDED_SELECTED_PACKET_TCD042_END_TO_END_COMPOSITION_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt13/ANIMO-KT13_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    if st.get("selected_packet_binding_qualified") is not True:
        fail("binding qualification flag")
    if st.get("bounded_hydrology_composition_qualified") is not True:
        fail("hydrology qualification flag")
    if st.get("bounded_load_composition_qualified") is not True:
        fail("load qualification flag")
    if st.get("transaction_science_composition_qualified") is not True:
        fail("science composition flag")
    if st.get("multi_interval_state_continuation_qualified") is not False:
        fail("multi-interval overclaim")
    if st.get("independent_review_completed") is not False:
        fail("independent review overclaim")
    print("PASS_KT13_QUALIFIED_BOUNDED_COMPOSITION")
else:
    fail("unexpected state")
