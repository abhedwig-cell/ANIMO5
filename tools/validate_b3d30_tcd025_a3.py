#!/usr/bin/env python3
import json,pathlib,subprocess
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parents[1]; BASE="f4a3056087e5f7bac41b243be1f404739cde52b0"; A10="872c78b6c020086280e31e1d9a7408e8b5a1afc7"; D28="ce602528d075fc962b0b78759ed0082d1ec78a51"; D29="97fd3274acd47bac74939d9dbd55b908043d1521"; PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"; DEC="ADMIT_TCD025_A3_RESTRICTED_N_LEDGER_DON_NH4_NO3_SEPARATE_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
def fail(x): print("B3D30 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
c=load("integration/animo-b3/B3D30_TCD025_A3_ADMISSION_CONTRACT.json"); o=load("integration/animo-b3/B3D30_TCD025_A3_ORACLES.json"); s=load("integration/animo-b3/ANIMO-B3D30_STATUS.json")
if c.get("source_species") != ["DiorNi","Nh","Ni"] or c.get("public_family")!="N": fail("species identity")
if c.get("scope",{}).get("predicate")!=PRED or c.get("scope",{}).get("partial_cut_admitted") is not False or c.get("scope",{}).get("scope_widening_allowed") is not False: fail("scope")
if c.get("public_aggregation") != "N = DON + NH4-N + NO3-N after separate identities" or c.get("units",{}).get("new_stoichiometric_conversion") is not False: fail("N aggregation/units")
if c.get("candidate_decision")!=DEC or c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail("decision/history")
a10=gj(A10,"integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json"); i8=gj(BASE,"integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json"); d28=gj(D28,"integration/animo-b3/ANIMO-B3D28_STATUS.json"); d29=gj(D29,"integration/animo-b3/ANIMO-B3D29_STATUS.json")
if a10.get("species_mapping",{}).get("N") != ["DiorNi","Nh","Ni"] or a10.get("species_mapping",{}).get("NH4_NO3_separation_preserved") is not True: fail("B3A10 N mapping")
a3=[x for x in i8["children"] if x["id"]=="TCD-025-A3"][0]
if a3.get("source_species") != ["DiorNi","Nh","Ni"] or a3.get("species_separation_required_before_aggregation") is not True or a3.get("admission_candidate") is not True: fail("B3I08 A3")
for d in [d28,d29]:
 if d.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or d.get("parent_tcd_admitted",d.get("admission_effect",{}).get("parent_tcd_admitted")) is not False: fail("prior sibling state")
cs={x["id"]:x for x in o["cases"]}
for cid in ["N01","N02"]:
 sp=cs[cid]["species"]
 for v in sp.values():
  if Fraction(v["old"])+Fraction(v["in"]) != Fraction(v["out"])+Fraction(v["new"]): fail(cid+" species")
 if sum(Fraction(v["old"])+Fraction(v["in"]) for v in sp.values()) != sum(Fraction(v["out"])+Fraction(v["new"]) for v in sp.values()): fail(cid+" aggregate")
if Fraction(cs["N03"]["matrix_side"])+Fraction(cs["N03"]["macropore_side"])!=0 or cs["N04"]["second_external_loss"]!=0: fail("internal/double count")
if cs["N05"]["expect_in_scope"] is not False or cs["N06"]["expect_in_scope"] is not True or cs["N07"]["expect_in_scope"] is not True or cs["N08"]["expect_species_separation"] is not True: fail("controls")
allowed={".github/workflows/animo-b3d30-tcd025-a3.yml","docs/b3d30/WORK_UNIT_CONTRACT.md","integration/animo-b3/B3D30_TCD025_A3_ADMISSION_CONTRACT.json","integration/animo-b3/B3D30_TCD025_A3_ORACLES.json","integration/animo-b3/ANIMO-B3D30_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3D30_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D30_STATUS.json","tools/validate_b3d30_tcd025_a3.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/"): fail("source/reference")
rp=R/"integration/animo-b3/ANIMO-B3D30_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 r=json.loads(rp.read_text()); h=r.get("reviewed_head")
 if r.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("genuinely_independent") is not False or r.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD025_A3_WITH_HISTORICAL_UNCERTAINTY": fail("review")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D30_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D30_STATUS.json"}): fail("post-review substance")
 if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True: fail("final")
 print("B3D30 PASS final TCD025-A3 N admission",h)
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("admitted") is not False: fail("pre-review")
 print("B3D30 PASS frozen pending GOV05 review")
