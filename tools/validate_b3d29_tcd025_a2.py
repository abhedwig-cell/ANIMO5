#!/usr/bin/env python3
import json,pathlib,subprocess
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parents[1]
BASE="f4a3056087e5f7bac41b243be1f404739cde52b0"; A10="872c78b6c020086280e31e1d9a7408e8b5a1afc7"; D28="ce602528d075fc962b0b78759ed0082d1ec78a51"; DEC="ADMIT_TCD025_A2_RESTRICTED_DOM_LEDGER_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"; PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"
def fail(x): print("B3D29 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
c=load("integration/animo-b3/B3D29_TCD025_A2_ADMISSION_CONTRACT.json"); o=load("integration/animo-b3/B3D29_TCD025_A2_ORACLES.json"); s=load("integration/animo-b3/ANIMO-B3D29_STATUS.json")
if c.get("target_child_atom")!="TCD-025-A2" or c.get("source_species")!=["DiorMa"]: fail("identity/species")
if c.get("scope",{}).get("predicate")!=PRED or c.get("scope",{}).get("partial_cut_admitted") is not False or c.get("scope",{}).get("scope_widening_allowed") is not False: fail("scope")
if c.get("candidate_decision")!=DEC or c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail("decision/history")
a10=gj(A10,"integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json"); i8=gj(BASE,"integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json"); d28=gj(D28,"integration/animo-b3/ANIMO-B3D28_STATUS.json")
if a10.get("species_mapping",{}).get("DOM") != ["DiorMa"] or a10.get("interval_gate",{}).get("required_expression")!=PRED: fail("B3A10 mismatch")
a2=[x for x in i8["children"] if x["id"]=="TCD-025-A2"][0]
if a2.get("admission_candidate") is not True or a2.get("source_species")!=["DiorMa"] or a2.get("scope_expansion_allowed") is not False: fail("B3I08 A2 route")
if d28.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or d28.get("admission_effect",{}).get("parent_tcd_admitted") is not False: fail("D28 exact sibling state")
cs={x["id"]:x for x in o["cases"]}
for k in ["D01","D02"]:
 x=cs[k]
 if Fraction(x["old"])+Fraction(x["boundary_in"]) != Fraction(x["new"])+Fraction(x["boundary_out"])+Fraction(x["direct_drain"]): fail(k)
if Fraction(cs["D03"]["matrix_side"])+Fraction(cs["D03"]["macropore_side"])!=0 or cs["D04"]["second_external_loss"]!=0: fail("internal transfer/drain guard")
if cs["D05"]["expect_in_scope"] is not False or cs["D06"]["expect_in_scope"] is not True or cs["D07"]["expect_in_scope"] is not True: fail("scope controls")
allowed={".github/workflows/animo-b3d29-tcd025-a2.yml","docs/b3d29/WORK_UNIT_CONTRACT.md","integration/animo-b3/B3D29_TCD025_A2_ADMISSION_CONTRACT.json","integration/animo-b3/B3D29_TCD025_A2_ORACLES.json","integration/animo-b3/ANIMO-B3D29_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3D29_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D29_STATUS.json","tools/validate_b3d29_tcd025_a2.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/"): fail("source/reference change")
rp=R/"integration/animo-b3/ANIMO-B3D29_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 r=json.loads(rp.read_text()); h=r.get("reviewed_head")
 if r.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("genuinely_independent") is not False or r.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD025_A2_WITH_HISTORICAL_UNCERTAINTY": fail("review")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D29_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D29_STATUS.json"}): fail("post-review substance")
 if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True: fail("final")
 print("B3D29 PASS final TCD025-A2 DOM admission",h)
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("admitted") is not False: fail("pre-review")
 print("B3D29 PASS frozen pending GOV05 review")
