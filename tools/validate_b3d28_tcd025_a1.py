#!/usr/bin/env python3
import json, pathlib, subprocess
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE="f4a3056087e5f7bac41b243be1f404739cde52b0"
RG05J="624bbad35add93de29ac89649155d9fa086a73af"
B3A10="872c78b6c020086280e31e1d9a7408e8b5a1afc7"
MASSQ03="68a8c202bd01bf55b31b7c944884fb2f78a6a8e8"
GOV05="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"
DEC="ADMIT_TCD025_A1_RESTRICTED_WATER_LEDGER_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
def fail(m): print("B3D28 FAIL_CLOSED:",m); raise SystemExit(1)
def load(p):
 q=ROOT/p
 if not q.exists(): fail("missing "+p)
 return json.loads(q.read_text())
def git_json(sha,p):
 try: return json.loads(subprocess.check_output(["git","show",f"{sha}:{p}"],cwd=ROOT,text=True))
 except Exception as e: fail(f"cannot load pinned {sha}:{p}: {e}")

c=load("integration/animo-b3/B3D28_TCD025_A1_ADMISSION_CONTRACT.json")
o=load("integration/animo-b3/B3D28_TCD025_A1_ORACLES.json")
f=load("integration/animo-b3/ANIMO-B3D28_AUTHORING_FREEZE.json")
s=load("integration/animo-b3/ANIMO-B3D28_STATUS.json")

if c.get("target_child_atom") != "TCD-025-A1" or c.get("target_parent_tcd") != "TCD-025": fail("target identity mismatch")
if c.get("base_authority") != "ANIMO-B3I08@"+BASE or c.get("aggregate_at_start") != "ANIMO-RG05J@"+RG05J: fail("base/aggregate mismatch")
if c.get("readiness_authority") != "ANIMO-B3A10@"+B3A10 or c.get("control_volume_authority") != "ANIMO-MASSQ03@"+MASSQ03: fail("qualification authority mismatch")
if c.get("governance",{}).get("ANIMO-GOV05") != GOV05: fail("GOV05 pin mismatch")
if c.get("b3_qualification_class") != "A_ACCOUNTING_REPORTING_ONLY" or c.get("review_risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS": fail("class/risk mismatch")
if c.get("atomicity") != "BOUNDED_CHILD_ATOM": fail("atomicity mismatch")
if c.get("historical_behavior") != "UNKNOWN_WITHOUT_B2": fail("historical behavior overclaim")
if c.get("scope",{}).get("inherited_predicate") != PRED or c.get("scope",{}).get("scope_widening_allowed") is not False or c.get("scope",{}).get("partial_saturated_reservoir_cut_admitted") is not False: fail("bounded scope violated")
terms=c.get("source_owned_terms",{})
if terms.get("begin_storage") != "sum(Ln in I) SrWaMpCpOld(Ln)" or terms.get("end_storage") != "sum(Ln in I) sum(active D) SrWaMpCp(D,Ln)": fail("water storage identity mismatch")
if "signed" not in terms.get("vertical_boundary","") or terms.get("direct_external_drain") != "selected-layer sum of FlMpOuDrMp": fail("water boundary/drain owner mismatch")
if c.get("candidate_admitted") is not True or c.get("candidate_decision") != DEC: fail("candidate decision mismatch")
for k in ["residual_derived_flux","absolute_value_boundary_reorientation","double_count_FlMpOuDrSo","sibling_admission","parent_admission","production_authorization","historical_fidelity"]:
 if c.get("forbidden_inferences",{}).get(k) is not False: fail("forbidden inference enabled "+k)

b3a10=git_json(B3A10,"integration/animo-b3/ANIMO-B3A10_STATUS.json")
if b3a10.get("qualified") is not True or b3a10.get("restricted_candidate_ready_for_separate_scoped_admission_workunit") is not True or b3a10.get("parent_tcd025_admission_ready") is not False: fail("B3A10 semantic authority mismatch")
r10=git_json(B3A10,"integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json")
if r10.get("interval_gate",{}).get("required_expression") != PRED or r10.get("interval_gate",{}).get("partial_cut") != "FORBIDDEN_NOT_SOURCE_CLOSED": fail("B3A10 scope mismatch")
i8=git_json(BASE,"integration/animo-b3/ANIMO-B3I08_STATUS.json")
route=git_json(BASE,"integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json")
if i8.get("work_status",{}).get("qualified") is not True or i8.get("parent_admitted") is not False or i8.get("child_admission_count") != 0: fail("B3I08 authority mismatch")
a1=[x for x in route.get("children",[]) if x.get("id")=="TCD-025-A1"]
if len(a1)!=1 or a1[0].get("admission_candidate") is not True or a1[0].get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS" or a1[0].get("scope_expansion_allowed") is not False: fail("A1 routing mismatch")
a5=[x for x in route.get("children",[]) if x.get("id")=="TCD-025-A5"]
if len(a5)!=1 or a5[0].get("state") != "BLOCKED_NOT_SOURCE_CLOSED": fail("A5 blocker lost")

cases={x["id"]:x for x in o.get("cases",[])}
if set(cases)!={"W01","W02","W03","W04","W05","W06","W07","W08"}: fail("oracle set mismatch")
def closed(x): return Fraction(x["old_storage"])+Fraction(x["boundary_in"]) == Fraction(x["new_storage"])+Fraction(x["boundary_out"])+Fraction(x["direct_drain"])
for cid in ["W01","W02","W03"]:
 if not closed(cases[cid]): fail(cid+" water identity failed")
if cases["W04"]["second_external_loss"] != 0: fail("FlMpOuDrSo double-count guard failed")
if Fraction(cases["W05"]["matrix_side"])+Fraction(cases["W05"]["macropore_side"]) != 0: fail("matrix/macropore internal cancellation failed")
if cases["W06"]["expect_in_child_scope"] is not False or cases["W07"]["expect_in_child_scope"] is not True or cases["W08"]["expect_in_child_scope"] is not True: fail("scope controls failed")

if f.get("authoring_complete") is not True or f.get("base_head") != BASE: fail("authoring freeze invalid")
if s.get("hard_boundaries",{}).get("parent_tcd_admitted") is not False or s.get("hard_boundaries",{}).get("sibling_admitted") is not False or s.get("hard_boundaries",{}).get("production_migration_authorized") is not False: fail("status hard boundary violated")
allowed={".github/workflows/animo-b3d28-tcd025-a1.yml","docs/b3d28/WORK_UNIT_CONTRACT.md","docs/b3d28/TCD025_A1_WATER_ADMISSION.md","integration/animo-b3/B3D28_TCD025_A1_ADMISSION_CONTRACT.json","integration/animo-b3/B3D28_TCD025_A1_ORACLES.json","integration/animo-b3/ANIMO-B3D28_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3D28_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D28_STATUS.json","tools/validate_b3d28_tcd025_a1.py"}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=ROOT,text=True).splitlines()
extra=sorted(set(changed)-allowed)
if extra: fail("scope escape: "+", ".join(extra))
for p in changed:
 if p.startswith("src/") or p.startswith("reference/"): fail("forbidden source/reference change "+p)

rp=ROOT/"integration/animo-b3/ANIMO-B3D28_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 r=json.loads(rp.read_text()); h=r.get("reviewed_head")
 if r.get("model") != "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("genuinely_independent") is not False or r.get("assurance") != "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail("review assurance mismatch")
 if r.get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS" or r.get("outcome") != "SELF_REVIEW_PASS_ADMIT_TCD025_A1_WITH_HISTORICAL_UNCERTAINTY": fail("review outcome mismatch")
 if not h: fail("reviewed head missing")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=ROOT,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D28_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D28_STATUS.json"}): fail("substantive change after reviewed head")
 if s.get("state") != "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision") != DEC or s.get("admitted") is not True or s.get("qualified") is not True: fail("final admission state mismatch")
 if s.get("review",{}).get("reviewed_head") != h or s.get("review",{}).get("completed") is not True: fail("status/review mismatch")
 if s.get("admission_effect",{}).get("parent_tcd_admitted") is not False or s.get("admission_effect",{}).get("A5_blocker_disposed") is not False: fail("parent/A5 boundary lost")
 print("B3D28 PASS final TCD025-A1 bounded water admission with historical uncertainty",h)
else:
 if s.get("phase") != "AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("state") != "NOT_YET_ADMITTED": fail("pre-review status invalid")
 print("B3D28 PASS authoring frozen; GOV05 Tier-C adversarial review required")
