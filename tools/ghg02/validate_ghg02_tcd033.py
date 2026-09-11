#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "997d867a2b107ec8e28efce530c82a204719de46"
RG05N = "8758bd30e302b75dd7854ac00fd2e29473669a13"
B3I01 = "383c7a83e84a578969f92113280dc715b7bdddb4"
GHG01 = "dac7b7b5c591b781b82ec968896edb5957664c88"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
POLICY = ROOT / "integration/animo-ghg/GHG02_TCD033_PARTITION_POLICY.json"
MATRIX = ROOT / "integration/animo-ghg/GHG02_TCD033_ORACLE_MATRIX.csv"
FREEZE = ROOT / "integration/animo-ghg/ANIMO-GHG02_AUTHORING_FREEZE.json"
STATUS = ROOT / "integration/animo-ghg/ANIMO-GHG02_STATUS.json"
REVIEW = ROOT / "integration/animo-ghg/ANIMO-GHG02_INTERNAL_ADVERSARIAL_REVIEW.json"
ORACLE = ROOT / "tools/ghg02/tcd033_partition_oracle.py"
ALLOWED = {
    ".github/workflows/animo-ghg02-tcd033.yml",
    "docs/ghg/TCD033_CH4_COMPONENT_PARTITION_QUALIFICATION.md",
    "integration/animo-ghg/GHG02_TCD033_PARTITION_POLICY.json",
    "integration/animo-ghg/GHG02_TCD033_ORACLE_MATRIX.csv",
    "integration/animo-ghg/ANIMO-GHG02_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG02_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG02_STATUS.json",
    "tools/ghg02/tcd033_partition_oracle.py",
    "tools/ghg02/validate_ghg02_tcd033.py",
}


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout


def gj(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def gt(commit, path):
    return run("git", "show", f"{commit}:{path}")


def load(path):
    return json.loads(path.read_text())


def req(condition, message):
    if not condition:
        raise SystemExit("ANIMO-GHG02 FAIL_CLOSED: " + message)


for sha in (BASE, RG05N, B3I01, GHG01, GOV05):
    subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=ROOT, check=True)

changed = {p for p in run("git", "diff", "--name-only", BASE + "..HEAD").splitlines() if p}
req(changed <= ALLOWED, "scope escape " + str(sorted(changed - ALLOWED)))
for p in changed:
    req(not p.startswith("src/"), "production source modified: " + p)
    req(not p.startswith("reference/"), "frozen reference modified: " + p)
    req(p != "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv", "canonical register modified")
    req(p != "integration/animo-reg/RG05_B3_QUEUE.json", "central queue modified")

base = gj(BASE, "integration/animo-b3/ANIMO-B3Q05_STATUS.json")
req(base["state"] == "QUALIFIED_ANIMO_B3Q05_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_SIX_TOP_LEVEL_UNADMITTED", "B3Q05 state")
req("TCD-033" in base["unadmitted_top_level"] and base["global_canonical_b3_queue_closed"] is False, "TCD033 must remain unadmitted at base")
req(base["tb7_allowed"] is False and base["b4_allowed"] is False and base["production_allowed"] is False, "B3Q05 downstream gate")

rg = gj(RG05N, "integration/animo-reg/ANIMO-RG05N_STATUS.json")
req(rg["scientific_admission_count"] == 29 and rg["top_level_admitted_tcd_count"] == 19, "RG05N counts")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05N project gate")

routing = gj(B3I01, "integration/animo-b3/CANONICAL_TCD_ROUTING_REGISTER.json")
entries = [x for x in routing["canonical_routing"] if x.get("canonical_key") == "TCD-033"]
req(len(entries) == 1, "TCD033 canonical routing cardinality")
e = entries[0]
req(e["b3_class"] == "B", "TCD033 B3 class")
req(e["qualification_owner"] == "PROPOSED_ANIMO-GHG02", "TCD033 owner")
req(e["source_local_key"] == "GHG01-LCL-CH4-PRODUCTION-COMPONENT-PARTITION", "TCD033 local key")
req("does not close to total under partial anaerobiosis" in e["phenomenon"], "TCD033 phenomenon")
req("partition identity test" in e["dependencies"], "TCD033 partition dependency")

manifest = gt(BASE, "reference/source/source_manifest.csv")
req("ANIMO_4.1.5.53/ghg_ch4.for,26809,ee4e83f7,00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98" in manifest, "ghg_ch4 source identity")
recon = gt(GHG01, "docs/ghg/GHG_CH4_PRODUCTION_AND_SUBSTRATE_RECONCILIATION.md")
for needle in [
    "QPrCH4 = E * A * S",
    "sum_i(QPrCH4_i) = E*S = QPrCH4/A",
    "SOURCE_CONFIRMED_CH4_PRODUCTION_COMPONENT_PARTITION_NONCLOSURE",
    "QPrCH4Do(Ln)",
    "No production migration or B3 admission is permitted from this note.",
]:
    req(needle in recon, "GHG01 reconstruction missing: " + needle)

p = load(POLICY)
req(p["target"] == "TCD-033" and p["b3_class"] == "B_LOCAL_SCIENTIFIC_IDENTITY", "policy identity")
req(p["review_risk_tier"] == "C_SCIENTIFIC_MASS_TRANSFER_PARTITION_IDENTITY", "risk tier")
req(p["source_identity"]["member_sha256"] == "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98", "policy source hash")
req(p["semantic_contract"]["parent_daughter_identity"] == "sum_i(Q_i)=Q", "parent daughter identity")
qp = p["qualified_policy"]
req(qp["positive_substrate"] == "Q_i=Q*S_i/S", "qualified positive-substrate expression")
req(qp["equivalent_form"] == "Q_i=E*A*S_i", "equivalent expression")
req(qp["zero_substrate"] == "if S=0 then Q=0 and all Q_i=0", "zero substrate policy")
req(qp["anaerobic_early_return"] == "if A < 1.0e-8 then Q=0 and all Q_i=0", "existing cutoff preservation")
req(qp["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty")
req(p["evidence"]["exact_historical_component_equation"] == "UNAVAILABLE" and p["evidence"]["historical_active_GHG_reference"] == "UNAVAILABLE", "historical evidence boundary")
req(p["b3_admission_performed"] is False and p["production_authorized"] is False, "no admission or production")
req(all(v is False for v in p["hard_boundaries"].values()), "policy boundaries")

with MATRIX.open(newline="") as f:
    rows = list(csv.DictReader(f))
req(len(rows) == 8, "oracle matrix row count")
roles = {r["case_id"]: r for r in rows}
for cid in ["full_anaerobic", "partial_anaerobic", "cutoff_exact", "below_cutoff", "zero_substrate", "single_source", "zero_environment", "mixed_four_pool"]:
    req(cid in roles, "missing matrix case " + cid)
req(roles["partial_anaerobic"]["expected_legacy_control"] == "legacy_sum_equals_total_div_A", "partial negative control")
req(roles["zero_substrate"]["expected_legacy_control"] == "legacy_component_expression_undefined", "zero substrate negative control")
req(ORACLE.exists(), "oracle missing")
oracle_out = run("python", str(ORACLE.relative_to(ROOT)))
req("TCD033 partition oracle PASS" in oracle_out and "historical_behavior UNKNOWN_WITHOUT_B2" in oracle_out, "oracle result")

fr = load(FREEZE)
req(fr["target"] == "TCD-033" and fr["base_head"] == BASE, "freeze base")
req(fr["review_must_pin_exact_green_authoring_head"] is True and fr["substantive_change_resets_GOV05_review"] is True, "freeze review contract")

st = load(STATUS)
req(st["target"] == "TCD-033" and st["base_authority"] == "ANIMO-B3Q05@" + BASE, "status identity")
req(st["aggregate_authority"] == "ANIMO-RG05N@" + RG05N, "status aggregate")
req(st["historical_behavior"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty")
req(st["b3_admission_performed"] is False and st["production_authorized"] is False, "status no admission/production")
req(st["tcd032_modified_or_admitted"] is False and st["tcd034_modified_or_admitted"] is False, "sibling separation")
req(all(v is False for v in st["hard_boundaries"].values()), "status boundaries")

if REVIEW.exists():
    rv = load(REVIEW)
    head = rv.get("reviewed_head")
    req(rv.get("target") == "TCD-033", "review target")
    req(rv.get("model") == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW", "review model")
    req(rv.get("same_agent") is True and rv.get("genuinely_independent") is False and rv.get("independence_claimed") is False, "review independence semantics")
    req(rv.get("assurance") == ASSURANCE, "review assurance")
    req(bool(head) and rv.get("reviewed_head_ci_run") and rv.get("reviewed_head_ci_job") and rv.get("reviewed_head_ci_conclusion") == "success", "reviewed head CI")
    req(rv.get("outcome") == "SELF_REVIEW_PASS_TCD033_SCIENTIFIC_PARTITION_POLICY_WITH_HISTORICAL_UNCERTAINTY", "review outcome")
    post = {x for x in run("git", "diff", "--name-only", head + "..HEAD").splitlines() if x}
    req(post <= {"integration/animo-ghg/ANIMO-GHG02_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-ghg/ANIMO-GHG02_STATUS.json"}, "post-review substantive change")
    req(st["phase"] == "CLOSED_QUALIFIED_SCIENTIFIC_POLICY" and st["state"] == "QUALIFIED_TCD033_SCIENTIFIC_PARTITION_POLICY_NO_B3_ADMISSION", "final state")
    req(st["decision"] == st["candidate_decision"], "final decision")
    req(st["qualified"] is True and st["review"]["completed"] is True and st["review"]["genuinely_independent"] is False, "final qualification/review")
    req(st["work_status"] == {"realized": True, "persisted": True, "tested": True, "reviewed": True, "qualified": True, "workunit_complete": True}, "final work status")
    print("ANIMO-GHG02 PASS final qualified TCD033 partition policy; B3 admission remains separate")
else:
    req(st["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW", "candidate phase")
    req(st["qualified"] is False and st["review"]["completed"] is False and st["work_status"]["tested"] is False, "candidate not prematurely qualified")
    print("ANIMO-GHG02 PASS frozen TCD033 candidate pending GOV05 Tier-C adversarial review")
