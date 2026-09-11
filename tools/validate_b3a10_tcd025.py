#!/usr/bin/env python3
import json, pathlib, subprocess
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "624bbad35add93de29ac89649155d9fa086a73af"
B3A08 = "7a7309e913e8216a20ac134539470e3e5eb4302f"
MASSQ03 = "68a8c202bd01bf55b31b7c944884fb2f78a6a8e8"
AUTHORITIES = {
    "ANIMO-B3A08":B3A08,
    "ANIMO-MASSQ03":MASSQ03,
    "ANIMO-GOV05":"f65a47724e4a4fca7f2d8b8d6de9eeee51867904",
    "ANIMO-GOV04":"1bbe4c211197590f346803106e45dca5faae79fc",
    "ANIMO-GOV03":"cbd262bdabe92923113b7326f2f42822ce9a971c",
    "ANIMO-B3Q01":"846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
    "ANIMO-MP01":"7b5979dd6301b9d55d23e8c22948a0dba24b229b",
    "ANIMO-MP02":"6b0f2e7470f13baeb6612b0bddb662a497dea528",
    "ANIMO-MASSQ02":"56a11b524d03c33ee4ab9b1cd13b2cd523d543fc",
    "ANIMO-B3D23":"6c9ab83952b53566b878b533c08e3cb10074f399",
}

def fail(msg):
    print("B3A10 FAIL_CLOSED:", msg)
    raise SystemExit(1)
def load(path):
    p=ROOT/path
    if not p.exists(): fail("missing "+path)
    return json.loads(p.read_text(encoding="utf-8"))
def git_json(sha,path):
    try: text=subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=ROOT,text=True)
    except subprocess.CalledProcessError: fail(f"cannot read pinned upstream {sha}:{path}")
    try: return json.loads(text)
    except Exception as e: fail(f"invalid upstream JSON {sha}:{path}: {e}")

contract=load("integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json")
ownership=load("integration/animo-b3/TCD025_LEDGER_TERM_OWNERSHIP.json")
oracles=load("integration/animo-b3/TCD025_RESTRICTED_ORACLE_CASES.json")
freeze=load("integration/animo-b3/ANIMO-B3A10_AUTHORING_FREEZE.json")
status=load("integration/animo-b3/ANIMO-B3A10_STATUS.json")

if contract.get("work_unit") != "ANIMO-B3A10" or contract.get("target") != "TCD-025": fail("wrong identity")
if contract.get("base_authority") != "ANIMO-RG05J@"+BASE: fail("wrong aggregate base")
if contract.get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS": fail("wrong risk tier")
for k,v in AUTHORITIES.items():
    if contract.get("consumed_authorities",{}).get(k) != v: fail("authority mismatch "+k)
    if subprocess.run(["git","cat-file","-e",v+"^{commit}"],cwd=ROOT).returncode != 0: fail("missing pinned commit "+k)

b3a08=git_json(B3A08,"integration/animo-b3/ANIMO-B3A08_STATUS.json")
if b3a08.get("qualified") is not True or b3a08.get("state") != "NOT_READY_FOR_B3_ADMISSION": fail("B3A08 semantic authority mismatch")
if b3a08.get("decision") != "QUALIFIED_TCD025_TIER_A_WAIVER_UNAVAILABLE_ESCALATE_TIER_C_SELECTED_PROFILE_CONTROL_VOLUME_QUALIFICATION": fail("B3A08 decision mismatch")
if b3a08.get("risk_tier_candidate") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS": fail("B3A08 risk mismatch")

mq=git_json(MASSQ03,"integration/animo-mass/ANIMO-MASSQ03_STATUS.json")
mc=git_json(MASSQ03,"integration/animo-mass/MASSQ03_TCD025_CONTROL_VOLUME_CONTRACT.json")
ms=git_json(MASSQ03,"integration/animo-mass/MASSQ03_SOURCE_SEAM_EVIDENCE.json")
if mq.get("qualified") is not True or mq.get("b3_admitted") is not False: fail("MASSQ03 qualification/admission mismatch")
if mq.get("decision") != "QUALIFIED_TCD025_SELECTED_PROFILE_MACROPORE_BOUNDARY_ADMISSIBILITY_PARTIAL_SATURATED_RESERVOIR_CUTS_NOT_SOURCE_CLOSED_NO_ADMISSION": fail("MASSQ03 decision mismatch")
if mq.get("review_governance",{}).get("review_completed") is not True or mq.get("review_governance",{}).get("genuinely_independent") is not False: fail("MASSQ03 review assurance mismatch")
expr="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"
if mc.get("qualified_predicate",{}).get("expression") != expr: fail("MASSQ03 predicate mismatch")
if mc.get("qualified_predicate",{}).get("necessary_for_exact_selected_profile_species_observer") is not True: fail("MASSQ03 necessity lost")
if mc.get("qualified_predicate",{}).get("sufficient_for_complete_TCD025_observer") is not False: fail("MASSQ03 sufficiency overclaimed")
if mc.get("qualified_predicate",{}).get("partial_saturated_reservoir_cut") != "NOT_SOURCE_CLOSED": fail("MASSQ03 partial cut changed")
if ms.get("frozen_source_archive_sha256") != "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566": fail("source identity mismatch")
for name,sha in {"Outbal_calc.for":"4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981","MAPOHYDRO.FOR":"86659aaac3e48439252c37490d44f214945dfe8f1d49d14876a40abc03e3722a","MAPOTRANSPORT.FOR":"735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da"}.items():
    if ms.get("member_hashes",{}).get(name) != sha: fail("source seam hash mismatch "+name)

ig=contract.get("interval_gate",{})
if ig.get("required_expression") != expr or ig.get("partial_cut") != "FORBIDDEN_NOT_SOURCE_CLOSED": fail("partial-cut prohibition weakened")
if ig.get("gate_is_necessary_not_sufficient") is not True: fail("boundary gate overclaimed sufficient")
ct=contract.get("correction_terms",{})
if ct.get("water_storage_old_selected") != "sum over Ln in I of SrWaMpCpOld(Ln)": fail("old selected water storage not exact")
if ct.get("water_storage_new_selected") != "sum over Ln in I and active D of SrWaMpCp(D,Ln)": fail("new selected water storage not exact")
if "signed" not in ct.get("water_vertical_boundary","") or "signed" not in ct.get("species_unsaturated_boundary",""): fail("boundary sign ownership missing")
if contract.get("restricted_candidate_scientifically_specified") is not True or contract.get("parent_tcd025_admission_ready") is not False: fail("readiness boundary mismatch")
if contract.get("b3_admitted") is not False or contract.get("production_authorized") is not False: fail("forbidden admission state")
fm=contract.get("forbidden_inferences",{})
for key in ["residual_derived_missing_flux","geometric_fraction_of_mixed_saturated_species_storage","absolute_value_boundary_flux_reorientation","double_count_FlMpOuDrSo","collapse_NH4_and_NO3_before_species_identity","whole_profile_only_silently_substituted_for_canonical_claim"]:
    if fm.get(key) is not False: fail("forbidden inference enabled: "+key)
if contract.get("species_mapping",{}).get("N") != ["DiorNi","Nh","Ni"]: fail("N mapping mismatch")
if contract.get("species_mapping",{}).get("P") != ["DiorPo","Po"]: fail("P mapping mismatch")

terms=ownership.get("terms",[])
if not any(t.get("source") == "sum_I SrWaMpCpOld(Ln)" for t in terms): fail("old water storage owner missing")
if not any(t.get("source") == "sum_I sum_D SrWaMpCp(D,Ln)" for t in terms): fail("new water storage owner missing")
if not any(t.get("source") == "FlMpOuDrSo" and t.get("role") == "internal/routed transfer" for t in terms): fail("FlMpOuDrSo ownership missing")
if not any(t.get("source") == "TpAm=AvCoML*FlMpVt(next)*St" for t in terms): fail("TpAm boundary owner missing")
if ownership.get("public_family_aggregation",{}).get("N") != "DiorNi + Nh + Ni after separate identities": fail("public N aggregation mismatch")

cases={c["id"]:c for c in oracles.get("cases",[])}
if set(cases) != {"R01","R02","R03","R04","R05","R06","R07","R08","R09"}: fail("oracle case set mismatch")
def closed(rec): return Fraction(rec["old"])+Fraction(rec["inputs"]) == Fraction(rec["outputs"])+Fraction(rec["new"])
for cid in ["R01","R02"]:
    if not closed(cases[cid]): fail(cid+" exact identity failed")
for cid in ["R03","R04"]:
    sp=cases[cid]["species"]
    if not all(closed(v) for v in sp.values()): fail(cid+" species identity failed")
    if sum(Fraction(v["old"])+Fraction(v["inputs"]) for v in sp.values()) != sum(Fraction(v["outputs"])+Fraction(v["new"]) for v in sp.values()): fail(cid+" aggregate identity failed")
if Fraction(cases["R05"]["matrix_side"])+Fraction(cases["R05"]["macropore_side"]) != 0: fail("matrix/macropore transfer does not cancel")
if cases["R06"]["external_macropore_loss_from_this_term"] != 0: fail("FlMpOuDrSo double counted")
if cases["R07"]["expect_admissible"] is not False or cases["R08"]["expect_admissible"] is not True or cases["R09"]["expect_admissible"] is not True: fail("boundary controls wrong")

if freeze.get("authoring_complete") is not True or freeze.get("superseded_freeze_head") != "b74a949e8852e4dab73c2aec9bb243897f409e8e": fail("remediated authoring freeze not declared")
if status.get("adversarial_precheck_history",{}).get("precheck_outcome") != "FAIL_CLOSED_REMEDIATION_REQUIRED": fail("precheck remediation history missing")
if status.get("b3_admitted") is not False or status.get("production_authorized") is not False: fail("status admits forbidden downstream state")

allowed={
 ".github/workflows/animo-b3a10-tcd025-restricted-readiness.yml","docs/b3a10/WORK_UNIT_CONTRACT.md","docs/b3a10/TCD025_RESTRICTED_CORRECTION_READINESS.md","integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json","integration/animo-b3/TCD025_LEDGER_TERM_OWNERSHIP.json","integration/animo-b3/TCD025_RESTRICTED_ORACLE_CASES.json","integration/animo-b3/ANIMO-B3A10_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3A10_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3A10_STATUS.json","tools/validate_b3a10_tcd025.py"}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=ROOT,text=True).splitlines()
extra=sorted(set(changed)-allowed)
if extra: fail("scope escape: "+", ".join(extra))
for p in changed:
    if p.startswith("src/") or p.startswith("reference/"): fail("forbidden source/reference change: "+p)

review_path=ROOT/"integration/animo-b3/ANIMO-B3A10_INTERNAL_ADVERSARIAL_REVIEW.json"
if review_path.exists():
    review=json.loads(review_path.read_text(encoding="utf-8")); h=review.get("reviewed_head")
    if review.get("model") != "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" or review.get("genuinely_independent") is not False: fail("wrong review model/assurance")
    if review.get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS": fail("review tier mismatch")
    if review.get("outcome") != "SELF_REVIEW_PASS_RESTRICTED_CORRECTION_READY_PARENT_SCOPE_BLOCKED": fail("review outcome mismatch")
    if not h: fail("reviewed head missing")
    post=subprocess.check_output(["git","diff","--name-only",h+"..HEAD"],cwd=ROOT,text=True).splitlines()
    if sorted(set(post)-{"integration/animo-b3/ANIMO-B3A10_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3A10_STATUS.json"}): fail("substantive change after review checkpoint")
    if status.get("phase") != "CLOSED_QUALIFIED_RESTRICTED_CORRECTION_READINESS" or status.get("qualified") is not True: fail("final readiness status mismatch")
    if status.get("restricted_candidate_ready_for_separate_scoped_admission_workunit") is not True: fail("restricted scoped admission handoff missing")
    if status.get("parent_tcd025_admission_ready") is not False: fail("parent readiness overclaimed")
    if status.get("review_governance",{}).get("reviewed_head") != h: fail("status/review head mismatch")
    print("B3A10 PASS final restricted TCD025 correction readiness; parent scope remains blocked",h)
else:
    if status.get("phase") != "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" or status.get("qualified") is not False: fail("pre-review phase invalid")
    print("B3A10 PASS remediated authoring frozen; GOV05 Tier-C adversarial review required")
