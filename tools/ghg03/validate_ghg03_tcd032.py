#!/usr/bin/env python3
import json
import pathlib
import subprocess

R = pathlib.Path(__file__).resolve().parents[2]
BASE = "83fedc7323cea6da696a81bc64e4e3b13d794880"
GHG01 = "dac7b7b5c591b781b82ec968896edb5957664c88"
B3I01 = "383c7a83e84a578969f92113280dc715b7bdddb4"
B3Q05 = "997d867a2b107ec8e28efce530c82a204719de46"
RG05N = "8758bd30e302b75dd7854ac00fd2e29473669a13"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
DEC = "QUALIFY_TCD032_BOUNDED_C_TRANSFER_OWNERSHIP_IDENTITY_READY_FOR_SEPARATE_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
IDENT = "TCD032_SINGLE_OWNER_METHANOGENESIS_C_TRANSFER_WITH_GROSS_DEBIT_INTERNAL_CREDIT_AND_NET_QJ_DT_CLOSURE"
POLICY = R / "integration/animo-ghg/GHG03_TCD032_C_TRANSFER_POLICY.json"
STATUS = R / "integration/animo-ghg/ANIMO-GHG03_STATUS.json"
FREEZE = R / "integration/animo-ghg/ANIMO-GHG03_AUTHORING_FREEZE.json"
REVIEW = R / "integration/animo-ghg/ANIMO-GHG03_INTERNAL_ADVERSARIAL_REVIEW.json"
ORACLE = R / "tools/ghg03/tcd032_c_transfer_oracle.py"
ALLOWED = {
    ".github/workflows/animo-ghg03-tcd032.yml",
    "docs/ghg/TCD032_METHANOGENESIS_C_TRANSFER_OWNERSHIP_QUALIFICATION.md",
    "integration/animo-ghg/GHG03_TCD032_C_TRANSFER_POLICY.json",
    "integration/animo-ghg/ANIMO-GHG03_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG03_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG03_STATUS.json",
    "tools/ghg03/tcd032_c_transfer_oracle.py",
    "tools/ghg03/validate_ghg03_tcd032.py",
}


def run(*args):
    return subprocess.run(args, cwd=R, check=True, text=True, capture_output=True).stdout


def gj(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def gt(commit, path):
    return run("git", "show", f"{commit}:{path}")


def load(path):
    return json.loads(path.read_text())


def req(cond, msg):
    if not cond:
        raise SystemExit("ANIMO-GHG03 FAIL_CLOSED: " + msg)


for sha in (BASE, GHG01, B3I01, B3Q05, RG05N, GOV03, GOV05):
    subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=R, check=True)

changed = {p for p in run("git", "diff", "--name-only", BASE + "..HEAD").splitlines() if p}
req(changed <= ALLOWED, "scope escape " + str(sorted(changed - ALLOWED)))
for p in changed:
    req(not p.startswith("src/"), "production source modified: " + p)
    req(not p.startswith("reference/"), "frozen reference modified: " + p)
    req(p != "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv", "canonical register modified")
    req(p != "integration/animo-reg/RG05_B3_QUEUE.json", "central queue modified")

base = gj(BASE, "integration/animo-b3/ANIMO-B3D40_STATUS.json")
req(base["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "B3D40 state")
req(base["target_tcd"] == "TCD-033" and base["admitted"] is True and base["qualified"] is True, "TCD033 dependency")
req(base["admitted_atomic_identity"] == "TCD033_CH4_COMPONENT_PARENT_DAUGHTER_PARTITION_QI_EQ_Q_SI_OVER_S", "TCD033 identity")
req(base["admission_effect"]["tcd032_admitted_or_modified"] is False, "B3D40 must not have admitted TCD032")

q = gj(B3Q05, "integration/animo-b3/ANIMO-B3Q05_STATUS.json")
req(q["state"] == "QUALIFIED_ANIMO_B3Q05_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_SIX_TOP_LEVEL_UNADMITTED", "B3Q05 state")
req("TCD-032" in q["unadmitted_top_level"], "TCD032 queue membership")
req(q["b4_allowed"] is False and q["production_allowed"] is False, "downstream gates")

rg = gj(RG05N, "integration/animo-reg/ANIMO-RG05N_STATUS.json")
req(rg["scientific_admission_count"] == 29 and rg["top_level_admitted_tcd_count"] == 19, "RG05N counts")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05N gates")

routing = gj(B3I01, "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json")
entries = [x for x in routing["canonical_routing"] if x.get("canonical_key") == "TCD-032"]
req(len(entries) == 1, "TCD032 routing cardinality")
e = entries[0]
req(e["b3_class"] == "B", "TCD032 B3 class")
req(e["source_local_key"] == "GHG01-LCL-METHANOGENESIS-SOURCE-POOL-TRANSFER", "TCD032 local key")
req("source-pool transfer path incomplete" in e["phenomenon"], "TCD032 phenomenon")
req("C balance closure" in e["dependencies"], "TCD032 C closure dependency")

manifest = gt(GHG01, "reference/source/source_manifest.csv")
for needle in [
    "ANIMO_4.1.5.53/ghgasses.for,30245,6ad8d335,4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93",
    "ANIMO_4.1.5.53/ghg_ch4.for,26809,ee4e83f7,00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
    "ANIMO_4.1.5.53/Rates.for,13995,5ba01247,7a1a8aee4715d85b9b7e9e172f83756e4aee8b8278386c804210ef77dc2a857a",
    "ANIMO_4.1.5.53/resp_miner.for,62997,b3961ade,938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106",
]:
    req(needle in manifest, "frozen source identity missing: " + needle.split(",")[0])

ledger = gt(GHG01, "docs/ghg/GHG_LEDGER_RECONCILIATION.md")
for needle in [
    "Only DOM has an active source depletion path outside `GHG_Miner`",
    "The two calls to `GHG_Miner` in `resp_miner.for` are commented out",
    "SOURCE_CONFIRMED_INCOMPLETE_METHANOGENESIS_SOURCE_POOL_TRANSFER_PATH_REFERENCE_UNEXERCISED",
    "sum(CH4_PRODUCTION_SOURCE_FAMILY) == CH4_PRODUCTION_TOTAL",
]:
    req(needle in ledger, "GHG01 ledger evidence missing: " + needle)

p = load(POLICY)
req(p["target"] == "TCD-032" and p["b3_class"] == "B_LOCAL_SCIENTIFIC_TRANSFER_IDENTITY", "policy target/class")
req(p["review_risk_tier"] == "C_SCIENTIFIC_MASS_TRANSFER_OWNERSHIP", "risk tier")
req(p["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "history")
sc = p["semantic_contract"]
req(sc["gross_source_debit"] == "G_j=Q_j*dt/(f_C*(1-a_j))", "gross debit")
req(sc["internal_humus_credit"] == "I_j=a_j*G_j", "internal credit")
req(sc["family_C_identity"] == "f_C*(G_j-I_j)=Q_j*dt", "family identity")
req(sc["parent_identity_dependency"] == "sum_j(Q_j)=Q_total from admitted TCD-033", "parent dependency")
req(sc["total_C_identity"] == "sum_j(f_C*(G_j-I_j))=Q_total*dt", "total identity")
req(sc["humus_family_policy"] == "a_hu=0", "humus policy")
req(p["ownership_contract"]["DOM_double_debit_forbidden"] is True, "DOM single owner")
req(p["ownership_contract"]["reactivate_GHG_Miner_unchanged"] is False, "no blind reactivation")
req(p["qualified_scope"]["elements"] == ["C"], "C-only scope")
req(p["qualified_scope"]["N_transfer"] is False and p["qualified_scope"]["P_transfer"] is False, "N/P excluded")
req(p["evidence"]["oracle_arithmetic"] == "EXACT_RATIONAL_NO_TOLERANCE", "oracle policy")
req(p["candidate_decision"] == DEC and p["b3_admission_performed"] is False and p["production_authorized"] is False, "candidate boundary")
req(all(v is False for v in p["hard_boundaries"].values()), "policy hard boundaries")

fr = load(FREEZE)
req(fr["target"] == "TCD-032" and fr["base_head"] == BASE, "freeze identity")
req(fr["review_must_pin_exact_green_authoring_head"] is True and fr["substantive_change_resets_GOV05_review"] is True, "freeze review contract")

req(ORACLE.exists(), "oracle missing")
out = run("python", str(ORACLE.relative_to(R)))
for needle in ["TCD032 carbon-transfer ownership oracle PASS", "arithmetic EXACT_RATIONAL_NO_TOLERANCE", "negative_control_double_DOM_debit PASS", "negative_control_missing_internal_credit PASS"]:
    req(needle in out, "oracle output missing " + needle)

s = load(STATUS)
req(s["target"] == "TCD-032" and s["base_authority"] == "ANIMO-B3D40@" + BASE, "status identity")
req(s["qualified_candidate_identity"] == IDENT and s["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "candidate identity/history")
req(s["b3_admission_performed"] is False and s["production_authorized"] is False, "no admission/production")
req(s["tcd033_reopened"] is False and s["tcd034_modified_or_admitted"] is False, "sibling boundary")
req(all(v is False for v in s["hard_boundaries"].values()), "status hard boundaries")

g = gj(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 route")
req(g["hard_boundaries"]["historical_B2_recovered"] is False, "no B2")

if REVIEW.exists():
    rv = load(REVIEW)
    h = rv.get("reviewed_head")
    req(rv.get("target") == "TCD-032", "review target")
    req(rv.get("model") == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "review model")
    req(rv.get("same_agent") is True and rv.get("genuinely_independent") is False and rv.get("independence_claimed") is False, "review independence semantics")
    req(rv.get("assurance") == ASSURANCE, "review assurance")
    req(bool(h) and rv.get("reviewed_head_ci_run") and rv.get("reviewed_head_ci_job") and rv.get("reviewed_head_ci_conclusion") == "success", "review exact-head CI")
    req(rv.get("outcome") == "SELF_REVIEW_PASS_TCD032_BOUNDED_C_TRANSFER_OWNERSHIP_POLICY_WITH_HISTORICAL_UNCERTAINTY", "review outcome")
    post = {x for x in run("git", "diff", "--name-only", h + "..HEAD").splitlines() if x}
    req(post <= {"integration/animo-ghg/ANIMO-GHG03_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-ghg/ANIMO-GHG03_STATUS.json"}, "post-review substantive change")
    req(s["phase"] == "CLOSED_QUALIFIED_SCIENTIFIC_POLICY" and s["state"] == "QUALIFIED_TCD032_BOUNDED_C_TRANSFER_OWNERSHIP_POLICY_READY_FOR_SEPARATE_B3_ADMISSION", "final state")
    req(s["decision"] == DEC and s["qualified"] is True, "final decision")
    req(s["review"]["completed"] is True and s["review"]["genuinely_independent"] is False, "final review state")
    req(s["work_status"] == {"realized": True, "persisted": True, "tested": True, "reviewed": True, "qualified": True, "workunit_complete": True}, "final work status")
    print("ANIMO-GHG03 PASS final qualified TCD032 C-transfer ownership policy; B3 admission remains separate")
else:
    req(s["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW", "candidate phase")
    req(s["qualified"] is False and s["review"]["completed"] is False and s["work_status"]["tested"] is False, "candidate not prematurely qualified")
    print("ANIMO-GHG03 PASS frozen TCD032 candidate pending GOV05 Tier-C adversarial review")
