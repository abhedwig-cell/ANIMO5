#!/usr/bin/env python3
import json,pathlib,subprocess
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parents[1]
BASE="f4a3056087e5f7bac41b243be1f404739cde52b0"; A10="872c78b6c020086280e31e1d9a7408e8b5a1afc7"; MASS="68a8c202bd01bf55b31b7c944884fb2f78a6a8e8"; RG="e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"; D28="ce602528d075fc962b0b78759ed0082d1ec78a51"; D29="97fd3274acd47bac74939d9dbd55b908043d1521"; D30="5da4e4f38ca94630ff857deb66e86f974425f30c"; PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"; DEC="ADMIT_TCD025_A4_RESTRICTED_P_LEDGER_DOP_PO4_SEPARATE_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
def fail(x): print("B3D31 FAIL_CLOSED:",x); raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
c=load("integration/animo-b3/B3D31_TCD025_A4_ADMISSION_CONTRACT.json"); o=load("integration/animo-b3/B3D31_TCD025_A4_ORACLES.json"); s=load("integration/animo-b3/ANIMO-B3D31_STATUS.json")
if c.get("source_species") != ["DiorPo","Po"] or c.get("public_family")!="P": fail("species identity")
if c.get("scope",{}).get("predicate")!=PRED or c.get("scope",{}).get("partial_cut_admitted") is not False or c.get("scope",{}).get("scope_widening_allowed") is not False: fail("scope")
if c.get("public_aggregation") != "P = DOP + PO4-P after separate identities": fail("P aggregation")
if c.get("units",{}).get("new_stoichiometric_conversion") is not False or c.get("units",{}).get("atomic_weight_conversion") is not False: fail("units/conversion")
if c.get("candidate_decision")!=DEC or c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2" or c.get("A5_blocker_disposed") is not False: fail("decision/history/A5")
a10=gj(A10,"integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json"); i8=gj(BASE,"integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json"); rg=gj(RG,"integration/animo-reg/ANIMO-RG05K_STATUS.json")
if a10.get("species_mapping",{}).get("P") != ["DiorPo","Po"] or a10.get("species_mapping",{}).get("DOP_PO4_separation_preserved") is not True: fail("B3A10 P mapping")
if a10.get("interval_gate",{}).get("required_expression")!=PRED: fail("B3A10 interval predicate")
a4=[x for x in i8["children"] if x["id"]=="TCD-025-A4"][0]
if a4.get("source_species") != ["DiorPo","Po"] or a4.get("species_separation_required_before_aggregation") is not True or a4.get("admission_candidate") is not True or a4.get("scope_expansion_allowed") is not False: fail("B3I08 A4")
if i8.get("parent",{}).get("automatic_admission_from_A1_A4_forbidden") is not True: fail("parent auto-admission guard")
a5=[x for x in i8["children"] if x["id"]=="TCD-025-A5"][0]
if a5.get("state")!="BLOCKED_NOT_SOURCE_CLOSED": fail("A5 routing state")
if rg.get("state")!="QUALIFIED_FIFTH_BATCHED_B3_ADMISSION_INTEGRATION_THREE_TCD025_CHILD_ATOMS_NO_PARENT_NO_PRODUCTION" or rg.get("scientific_admission_count")!=20 or rg.get("tcd025_state",{}).get("A4_admitted") is not False or rg.get("tcd025_state",{}).get("A5_state")!="BLOCKED_NOT_SOURCE_CLOSED": fail("RG05K state")
for sha in [D28,D29,D30]:
 st=gj(sha,"integration/animo-b3/ANIMO-"+({D28:"B3D28",D29:"B3D29",D30:"B3D30"}[sha])+"_STATUS.json")
 if st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail("prior sibling state")
 if st.get("admission_effect",{}).get("parent_tcd_admitted",st.get("parent_tcd_admitted")) is not False: fail("prior sibling parent boundary")
cs={x["id"]:x for x in o["cases"]}
for cid in ["P01","P02"]:
 sp=cs[cid]["species"]
 for v in sp.values():
  if Fraction(v["old"])+Fraction(v["in"]) != Fraction(v["out"])+Fraction(v["new"]): fail(cid+" species")
 if sum(Fraction(v["old"])+Fraction(v["in"]) for v in sp.values()) != sum(Fraction(v["out"])+Fraction(v["new"]) for v in sp.values()): fail(cid+" aggregate")
if Fraction(cs["P03"]["matrix_side"])+Fraction(cs["P03"]["macropore_side"])!=0 or cs["P04"]["second_external_loss"]!=0: fail("internal/double count")
if cs["P05"]["expect_in_scope"] is not False or cs["P06"]["expect_in_scope"] is not True or cs["P07"]["expect_in_scope"] is not True or cs["P08"]["expect_species_separation"] is not True: fail("scope/separation controls")
if cs["P09"]["stoichiometric_conversion"]!=0 or cs["P09"]["atomic_weight_conversion"]!=0 or cs["P09"]["expect_no_new_conversion"] is not True: fail("conversion control")
allowed={".github/workflows/animo-b3d31-tcd025-a4.yml","docs/b3d31/WORK_UNIT_CONTRACT.md","integration/animo-b3/B3D31_TCD025_A4_ADMISSION_CONTRACT.json","integration/animo-b3/B3D31_TCD025_A4_ORACLES.json","integration/animo-b3/ANIMO-B3D31_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3D31_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D31_STATUS.json","tools/validate_b3d31_tcd025_a4.py"}
ch=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines(); extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
 if p.startswith("src/") or p.startswith("reference/"): fail("source/reference")
rp=R/"integration/animo-b3/ANIMO-B3D31_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
 r=json.loads(rp.read_text()); h=r.get("reviewed_head")
 if r.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("genuinely_independent") is not False or r.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or r.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD025_A4_WITH_HISTORICAL_UNCERTAINTY": fail("review")
 post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
 if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D31_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D31_STATUS.json"}): fail("post-review substance")
 if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True: fail("final")
 if s.get("admission_effect",{}).get("parent_tcd_admitted") is not False or s.get("admission_effect",{}).get("A5_blocker_disposed") is not False: fail("final parent/A5")
 print("B3D31 PASS final TCD025-A4 P admission",h)
else:
 if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("admitted") is not False: fail("pre-review")
 print("B3D31 PASS frozen pending GOV05 review")
