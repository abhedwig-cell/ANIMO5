#!/usr/bin/env python3
import json
import pathlib
import subprocess

R = pathlib.Path(__file__).resolve().parents[1]
BASE = "9614e4a4733573c865aeece9f5b33628cbc7ee2d"
B3D40 = "83fedc7323cea6da696a81bc64e4e3b13d794880"
B3I01 = "383c7a83e84a578969f92113280dc715b7bdddb4"
B3Q05 = "997d867a2b107ec8e28efce530c82a204719de46"
RG05N = "8758bd30e302b75dd7854ac00fd2e29473669a13"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
DEC = "ADMIT_TCD032_SINGLE_OWNER_METHANOGENESIS_C_TRANSFER_IDENTITY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C"
IDENT = "TCD032_SINGLE_OWNER_METHANOGENESIS_C_TRANSFER_WITH_GROSS_DEBIT_INTERNAL_CREDIT_AND_NET_QJ_DT_CLOSURE"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
REVIEW = R / "integration/animo-b3/ANIMO-B3D41_INTERNAL_ADVERSARIAL_REVIEW.json"


def run(*args):
    return subprocess.run(args, cwd=R, check=True, text=True, capture_output=True).stdout


def gj(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def load(path):
    return json.loads((R / path).read_text())


def req(cond, msg):
    if not cond:
        raise SystemExit("B3D41 FAIL_CLOSED: " + msg)


for sha in (BASE, B3D40, B3I01, B3Q05, RG05N, GOV03):
    subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=R, check=True)

allowed = {
    ".github/workflows/animo-b3d41-tcd032.yml",
    "docs/b3d41/WORK_UNIT_CONTRACT.md",
    "integration/animo-b3/B3D41_TCD032_ADMISSION_CONTRACT.json",
    "integration/animo-b3/ANIMO-B3D41_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3D41_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3D41_STATUS.json",
    "tools/validate_b3d41_tcd032.py",
}
changed = {p for p in run("git", "diff", "--name-only", BASE + "..HEAD").splitlines() if p}
req(changed <= allowed, "scope escape " + str(sorted(changed - allowed)))
for p in changed:
    req(not p.startswith("src/"), "production source modified: " + p)
    req(not p.startswith("reference/"), "frozen reference modified: " + p)
    req(not p.startswith("integration/animo-reg/"), "central regie modified: " + p)
    req(p != "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv", "canonical register modified")

qpol = gj(BASE, "integration/animo-ghg/GHG03_TCD032_C_TRANSFER_POLICY.json")
qst = gj(BASE, "integration/animo-ghg/ANIMO-GHG03_STATUS.json")
req(qst["state"] == "QUALIFIED_TCD032_BOUNDED_C_TRANSFER_OWNERSHIP_POLICY_READY_FOR_SEPARATE_B3_ADMISSION", "GHG03 state")
req(qst["qualified"] is True and qst["b3_admission_performed"] is False and qst["production_authorized"] is False, "GHG03 boundary")
req(qst["qualified_candidate_identity"] == IDENT, "GHG03 identity")
req(qst["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "GHG03 history")
req(qpol["semantic_contract"]["family_C_identity"] == "f_C*(G_j-I_j)=Q_j*dt", "GHG03 family identity")
req(qpol["ownership_contract"]["DOM_double_debit_forbidden"] is True, "GHG03 DOM owner guard")

prev = gj(B3D40, "integration/animo-b3/ANIMO-B3D40_STATUS.json")
req(prev["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and prev["target_tcd"] == "TCD-033", "B3D40 state")
req(prev["aggregate_policy"]["post_RG05N_new_admissions_if_exact_final_green"] == 1, "post-RG05N count before B3D41")
req(prev["admission_effect"]["tcd032_admitted_or_modified"] is False, "TCD032 not already admitted")

queue = gj(B3Q05, "integration/animo-b3/ANIMO-B3Q05_STATUS.json")
req("TCD-032" in queue["unadmitted_top_level"], "TCD032 queue membership")
req(queue["b4_allowed"] is False and queue["production_allowed"] is False, "queue downstream gates")

routing = gj(B3I01, "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json")
entries = [x for x in routing["canonical_routing"] if x.get("canonical_key") == "TCD-032"]
req(len(entries) == 1 and entries[0]["b3_class"] == "B", "TCD032 canonical route")
req(entries[0]["source_local_key"] == "GHG01-LCL-METHANOGENESIS-SOURCE-POOL-TRANSFER", "TCD032 source key")

rg = gj(RG05N, "integration/animo-reg/ANIMO-RG05N_STATUS.json")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05N gates")

g = gj(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 uncertainty route")
req(g["hard_boundaries"]["historical_B2_recovered"] is False, "no B2")

c = load("integration/animo-b3/B3D41_TCD032_ADMISSION_CONTRACT.json")
s = load("integration/animo-b3/ANIMO-B3D41_STATUS.json")
f = load("integration/animo-b3/ANIMO-B3D41_AUTHORING_FREEZE.json")
req(c["target_tcd"] == "TCD-032" and c["atomic_target"] == "CANONICAL_TOP_LEVEL_TCD:TCD-032", "contract target")
req(c["candidate_decision"] == DEC and c["candidate_admitted"] is True, "contract decision")
req(c["admitted_identity"] == IDENT, "contract identity")
req(c["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "contract history")
sc = c["supported_scope"]
req(sc["element"] == "C" and sc["family_C_identity"] == "f_C*(G_j-I_j)=Q_j*dt", "contract C identity")
req(sc["DOM_double_debit_forbidden"] is True and sc["TCD033_parent_identity_dependency"] == "sum_j(Q_j)=Q_total", "contract ownership/dependency")
req(all(v is False for v in c["nonclaims"].values()), "contract nonclaims")
ap = c["aggregate_policy"]
req(ap["post_RG05N_new_admissions_before_this_candidate"] == 1 and ap["post_RG05N_new_admissions_if_exact_final_green"] == 2, "aggregate count")
req(ap["normal_batch_threshold_reached_if_green"] is False and ap["aggregate_update_required_after_exact_final_green"] is False, "aggregate cadence")
req(f["base_head"] == BASE and f["review_must_pin_exact_green_authoring_head"] is True and f["substantive_change_resets_GOV05_review"] is True, "freeze")
req(s["target_tcd"] == "TCD-032" and s["base_authority"] == "ANIMO-GHG03@" + BASE, "status identity")
req(s["candidate_decision"] == DEC and s["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "status candidate")
req(all(v is False for v in s["hard_boundaries"].values()), "status hard boundaries")

if REVIEW.exists():
    r = json.loads(REVIEW.read_text())
    h = r.get("reviewed_head")
    req(r.get("target") == "TCD-032", "review target")
    req(r.get("model") == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "review model")
    req(r.get("same_agent") is True and r.get("genuinely_independent") is False and r.get("independence_claimed") is False, "review independence semantics")
    req(r.get("assurance") == ASSURANCE, "review assurance")
    req(bool(h) and r.get("reviewed_head_ci_run") and r.get("reviewed_head_ci_job") and r.get("reviewed_head_ci_conclusion") == "success", "review exact-head CI")
    req(r.get("outcome") == "SELF_REVIEW_PASS_ADMIT_TCD032_BOUNDED_C_TRANSFER_IDENTITY_WITH_HISTORICAL_UNCERTAINTY", "review outcome")
    post = {x for x in run("git", "diff", "--name-only", h + "..HEAD").splitlines() if x}
    req(post <= {"integration/animo-b3/ANIMO-B3D41_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-b3/ANIMO-B3D41_STATUS.json"}, "post-review substantive change")
    req(s["phase"] == "COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI", "final phase")
    req(s["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and s["decision"] == DEC, "final admission state")
    req(s["admitted"] is True and s["qualified"] is True and s["admitted_atomic_identity"] == IDENT, "final identity")
    ae = s["admission_effect"]
    req(ae["tcd032_top_level_admitted"] is True and ae["tcd033_reopened"] is False and ae["tcd034_admitted_or_modified"] is False and ae["N_or_P_transfer_admitted"] is False and ae["production_authorized"] is False, "final admission boundaries")
    ap = s["aggregate_policy"]
    req(ap["post_RG05N_new_admissions_if_exact_final_green"] == 2 and ap["normal_batch_threshold_reached_if_green"] is False and ap["aggregate_update_required_after_exact_final_green"] is False, "final aggregate cadence")
    req(s["work_status"] == {"realized": True, "persisted": True, "tested": True, "reviewed": True, "qualified": True, "workunit_complete": True}, "final work status")
    print("B3D41 PASS final TCD032 bounded C-transfer admission", h)
else:
    req(s["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW", "candidate phase")
    req(s["state"] == "CANDIDATE_NOT_ADMITTED_PENDING_REVIEW" and s["admitted"] is False and s["qualified"] is False, "candidate not prematurely admitted")
    print("B3D41 PASS frozen TCD032 admission candidate pending GOV05 Tier-C adversarial review")
