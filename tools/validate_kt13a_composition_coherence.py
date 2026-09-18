#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="51baa9851d5bed0b711199835bb817b22514c511"

def fail(msg):
    print("KT13A FAIL_CLOSED:",msg)
    raise SystemExit(1)

st=json.loads((R/"integration/animo-kt13a/ANIMO-KT13A_STATUS.json").read_text())
finding=json.loads((R/"integration/animo-kt13a/KT13A_MATERIAL_FINDING_F01.json").read_text())
handoff=json.loads((R/"integration/animo-kt13a/KT13A_INDEPENDENT_REVIEW_HANDOFF.json").read_text())
mod=(R/"prototype/kt13/mod_animo_tcd042_bounded_composition.f90").read_text()
test=(R/"tests/kt13/test_kt13_bounded_composition.f90").read_text()

for required in [
    "logical function exact_binary64_equal(left, right)",
    "exact_binary64_equal(hetop, start_context%he_top)",
    "KT13_HETOP_GEOMETRY_MISMATCH",
    "trace%science_runtime_committed = .true.",
    "trace%postcommit_diagnostics_valid = diag_valid",
    "KT13_INTERVAL_COMMITTED_POSTCOMMIT_DIAGNOSTICS_INVALID"
]:
    if required not in mod:
        fail("missing remediation "+required)

after_run=mod.split("call run_interval",1)[1]
if "success = .false." in after_run:
    fail("postcommit success can still be rewritten false")

for required in [
    "test_hetop_geometry_mismatch_preserves_store",
    "KT13_HETOP_GEOMETRY_MISMATCH",
    "3FF0000000400000",
    "3FF0000000200000",
    "postcommit diagnostics valid"
]:
    if required not in test:
        fail("missing test/oracle "+required)

allowed_prefixes=("prototype/kt13/","tests/kt13/","docs/kt13a/","integration/animo-kt13a/")
allowed_exact={
 ".github/workflows/animo-kt13a-composition-coherence.yml",
 "tools/validate_kt13a_composition_coherence.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)

if any(st.get("scope",{}).get(k) is not False for k in [
    "science_formula_changed","upstream_frozen_modules_changed","tcd042_scope_widened",
    "production_changed","admission_performed"]):
    fail("scope overclaim")

if finding.get("original_target",{}).get("module_blob")!="f11b1a444db839994e7a5d4de00380eb8a6849a4":
    fail("original KT13 finding pin")
if finding.get("remediation",{}).get("exact_binary64_identity_guard_added") is not True:
    fail("finding remediation")
if handoff.get("same_agent_review_satisfies_independence") is not False:
    fail("review independence overclaim")
for key in ["canonical_species_binding","boundary_parser","chemistry_time_provider",
            "first_call_Runinu_value","multi_interval_state_continuation",
            "canonical_Runinu_state","B2_historical_equivalence","production"]:
    if handoff.get("explicit_nonclaims",{}).get(key) is not False:
        fail("review nonclaim "+key)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_KT13A_AUTHORING")
elif st.get("state")=="QUALIFIED_KT13_COMPOSITION_COHERENCE_REMEDIATION_INDEPENDENT_TIER_D_REVIEW_STILL_REQUIRED":
    if st.get("remediation",{}).get("exact_binary64_hetop_binding_required") is not True:
        fail("geometry remediation not qualified")
    if st.get("review",{}).get("independent_tier_d_review_still_required") is not True:
        fail("independent gate lost")
    print("PASS_KT13A_QUALIFIED_REMEDIATION")
else:
    fail("unexpected state")
