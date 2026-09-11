#!/usr/bin/env python3
import json, pathlib, subprocess
from fractions import Fraction

R=pathlib.Path(__file__).resolve().parents[1]
I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
RG="e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"
UBQ01="6895b67799f26888025eced7188e7190b2a0d07d"
B3B02="690868409aae11297c966eb55419f62ff977c619"
UBQ04="bbdb61be30f08951ba78926a745719cfcb1b64a8"
GOV03="cbd262bdabe92923113b7326f2f42822ce9a971c"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"
GOV05="f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
B3Q01="846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
D31="0bec1968adbf77fd04c6f46819d704b86482d8b2"
D32="4d7c42bb749ed5fbf1c884fba4a26a1a5b898505"
DEC="ADMIT_TCD042_B1_POSITIVE_HETOP_EXACT_ZERO_LOCAL_ALGEBRA_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
SCOPE="Flpn=0 AND Flux=0 AND Hetop>0"

def fail(x):
    print("B3D33 FAIL_CLOSED:",x)
    raise SystemExit(1)
def load(p): return json.loads((R/p).read_text())
def gj(s,p): return json.loads(subprocess.check_output(["git","show",f"{s}:{p}"],cwd=R,text=True))
def F(x): return Fraction(str(x))

c=load("integration/animo-b3/B3D33_TCD042_B1_ADMISSION_CONTRACT.json")
o=load("integration/animo-b3/B3D33_TCD042_B1_ORACLES.json")
s=load("integration/animo-b3/ANIMO-B3D33_STATUS.json")

if c.get("target_child_atom")!="TCD-042-B1" or c.get("target_parent_tcd")!="TCD-042": fail("target identity")
if c.get("supported_scope",{}).get("predicate")!=SCOPE: fail("supported scope")
sc=c["supported_scope"]
for k in ["exact_zero_only","positive_Hetop_only","Hetop_zero_excluded","finite_positive_flux_excluded","Flpn_nonzero_excluded"]:
    if sc.get(k) is not True: fail("scope gate "+k)
if sc.get("scope_widening_allowed") is not False: fail("scope widening")
if c.get("exact_zero_algebra")!={"A1":"1","A2":"St/Hetop","B1":"1","B2":"St/(2*Hetop)","C1":"C0+Load*St/Hetop","Cavg":"C0+Load*St/(2*Hetop)"}: fail("exact-zero algebra")
if c.get("conservation_identity")!="Hetop*C1=Hetop*C0+St*Load" or c.get("same_step_export")!="St*Flux*Cavg=0 exactly": fail("identity/export")
if c.get("candidate_decision")!=DEC or c.get("historical_behavior")!="UNKNOWN_WITHOUT_B2": fail("decision/history")
if c.get("parent_tcd_admitted") is not False or c.get("TCD042_E1_admitted") is not False or c.get("production_authorized") is not False: fail("scope boundary")
z=c.get("zero_endpoint_treatment",{})
if z.get("state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53" or z.get("global_input_invalidity_claimed") is not False or z.get("scientific_semantics_resolved") is not False or z.get("input_validation_changed") is not False or z.get("zero_thickness_policy_selected") is not False: fail("zero endpoint treatment")

# Reconstruct exact authorities rather than inheriting conclusions blindly.
i10=gj(I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
if i10.get("qualified") is not True or i10.get("scientific_admission") is not False: fail("B3I10 state")
re=i10.get("routing_effect",{})
if re.get("TCD042_B1_supported_scope")!=SCOPE or re.get("TCD042_B1_ready_for_separate_bounded_admission") is not True or re.get("TCD042_E1_remains_separate_with_NQ03_NQ03R_scope") is not True: fail("B3I10 routing")
if re.get("Hetop_zero_state")!="EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53" or re.get("Hetop_zero_global_input_invalidity_claimed") is not False or re.get("Hetop_zero_scientific_semantics_resolved") is not False: fail("B3I10 zero boundary")

u=gj(UBQ01,"integration/animo-science/ANIMO-UBQ01_STATUS.json")
atom=u.get("atomization",{})
if atom.get("qualified_candidate_class")!="B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT" or atom.get("exact_zero_end_state")!="C1=C0+Load*St/Hetop" or atom.get("exact_zero_average_state")!="Cavg=C0+Load*St/(2*Hetop)" or atom.get("exact_zero_conservation")!="Hetop*C1=Hetop*C0+St*Load": fail("UBQ01 science")
fe=u.get("frozen_identity",{})
if fe.get("source_sha256")!=c["frozen_identity"]["source_sha256"] or fe.get("testbank_sha256")!=c["frozen_identity"]["testbank_sha256"] or fe.get("documentation_sha256")!=c["frozen_identity"]["documentation_sha256"]: fail("B0 identity")
ne=u.get("executable_evidence",{}).get("natural_isolated_probe",{})
if ne.get("all_prior_records_bitwise_equal") is not True or ne.get("formula_predictions_bitwise_equal") is not True or ne.get("zero_load_control_bitwise_equal") is not True or ne.get("positive_flow_control_bitwise_equal") is not True: fail("UBQ01 natural controls")

b=gj(B3B02,"integration/animo-b3/ANIMO-B3B02_STATUS.json")
ad=b.get("admission",{})
if ad.get("positive_Hetop_subdomain_readiness_qualified") is not True or ad.get("readiness_qualified_for_full_requested_trigger") is not False: fail("B3B02 bounded readiness")
if b.get("domain_precondition",{}).get("full_requested_trigger_domain_resolved") is not False: fail("B3B02 full-domain guard")

q4=gj(UBQ04,"integration/animo-science/ANIMO-UBQ04_STATUS.json")
qf=q4.get("qualified_findings",{})
if qf.get("global_zero_thickness_concentration_semantics_unique") is not False or qf.get("zero_thickness_policy_selected") is not False or qf.get("NQ03_small_P_policy_extendable_to_Hetop_zero") is not False: fail("UBQ04 zero semantics")

g3=gj(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
if g3.get("qualified_G6U_state")!="ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS" or g3.get("hard_boundaries",{}).get("historical_B2_recovered") is not False: fail("GOV03 historical route")

rg=gj(RG,"integration/animo-reg/ANIMO-RG05K_STATUS.json")
if rg.get("work_status",{}).get("qualified") is not True or rg.get("b4_open") is not False or rg.get("production_open") is not False or rg.get("scientific_admission_count")!=20: fail("RG05K gate state")
for sha,w in [(D31,"B3D31"),(D32,"B3D32")]:
    st=gj(sha,f"integration/animo-b3/ANIMO-{w}_STATUS.json")
    if st.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or st.get("admitted") is not True or st.get("qualified") is not True: fail(w+" prior admission")

# Exact rational oracles.
cs={x["id"]:x for x in o["cases"]}
z1=cs["Z01"]
H,St,C0,L=map(F,[z1["Hetop"],z1["St"],z1["C0"],z1["Load"]])
if F(z1["expected"]["C1"]) != C0+L*St/H or F(z1["expected"]["Cavg"]) != C0+L*St/(2*H): fail("Z01 concentration")
if F(z1["expected"]["old_storage"])+F(z1["expected"]["input"]) != F(z1["expected"]["new_storage"]): fail("Z01 conservation")
if F(z1["expected"]["same_step_export"])!=0: fail("Z01 export")
z2=cs["Z02"]
if F(z2["Load"])!=0 or F(z2["expected"]["C1"])!=F(z2["C0"]) or F(z2["expected"]["Cavg"])!=F(z2["C0"]): fail("Z02 zero-load control")
z3=cs["Z03"]
for name,v in z3["species"].items():
    H=F(z3["Hetop"]); St=F(z3["St"]); C0=F(v["C0"]); L=F(v["Load"])
    if F(v["C1"])!=C0+L*St/H or F(v["Cavg"])!=C0+L*St/(2*H): fail("Z03 "+name+" concentration")
    if F(v["old_storage"])+F(v["input"])!=F(v["new_storage"]): fail("Z03 "+name+" conservation")
if z3.get("expect_species_separation") is not True or F(z3["same_step_export"])!=0: fail("Z03 separation/export")
for cid in ["Z04","Z05","Z06"]:
    if cs[cid].get("expect_in_scope") is not False: fail(cid+" exclusion")
if cs["Z04"].get("expect_semantics_invented") is not False or cs["Z05"].get("owner")!="TCD-042-E1": fail("exclusion ownership")
if F(cs["Z07"]["expected_export"])!=0: fail("Z07 export")

allowed={
 ".github/workflows/animo-b3d33-tcd042-b1.yml",
 "docs/b3d33/WORK_UNIT_CONTRACT.md",
 "integration/animo-b3/B3D33_TCD042_B1_ADMISSION_CONTRACT.json",
 "integration/animo-b3/B3D33_TCD042_B1_ORACLES.json",
 "integration/animo-b3/ANIMO-B3D33_AUTHORING_FREEZE.json",
 "integration/animo-b3/ANIMO-B3D33_INTERNAL_ADVERSARIAL_REVIEW.json",
 "integration/animo-b3/ANIMO-B3D33_STATUS.json",
 "tools/validate_b3d33_tcd042_b1.py"
}
ch=subprocess.check_output(["git","diff","--name-only",I10+"..HEAD"],cwd=R,text=True).splitlines()
extra=sorted(set(ch)-allowed)
if extra: fail("scope escape "+str(extra))
for p in ch:
    if p.startswith("src/") or p.startswith("reference/"): fail("source/reference modified")

rp=R/"integration/animo-b3/ANIMO-B3D33_INTERNAL_ADVERSARIAL_REVIEW.json"
if rp.exists():
    r=json.loads(rp.read_text()); h=r.get("reviewed_head")
    if r.get("model")!="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or r.get("genuinely_independent") is not False or r.get("same_agent") is not True or r.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail("review assurance")
    if r.get("outcome")!="SELF_REVIEW_PASS_ADMIT_TCD042_B1_POSITIVE_HETOP_WITH_HISTORICAL_UNCERTAINTY": fail("review outcome")
    if not h: fail("reviewed head missing")
    post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=R,text=True).splitlines()
    if sorted(set(post)-{"integration/animo-b3/ANIMO-B3D33_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3D33_STATUS.json"}): fail("post-review substantive change")
    if s.get("state")!="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" or s.get("decision")!=DEC or s.get("admitted") is not True or s.get("qualified") is not True: fail("final admission state")
    ae=s.get("admission_effect",{})
    if ae.get("child_atom_admitted") is not True or ae.get("parent_tcd_admitted") is not False or ae.get("TCD042_E1_admitted") is not False or ae.get("Hetop_zero_admitted") is not False or ae.get("production_authorized") is not False: fail("final admission boundaries")
    ap=s.get("aggregate_policy",{})
    if ap.get("batch_size_if_B3D33_exact_final_green")!=3 or ap.get("normal_batch_threshold_minimum")!=3 or ap.get("aggregate_update_required_after_exact_final_green") is not True or ap.get("aggregate_update_performed_here") is not False: fail("aggregate cadence")
    print("B3D33 PASS final bounded TCD042-B1 admission",h)
else:
    if s.get("phase")!="AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW" or s.get("admitted") is not False or s.get("qualified") is not False: fail("pre-review state")
    print("B3D33 PASS frozen pending GOV05 Tier-C adversarial review")
