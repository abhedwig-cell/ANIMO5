#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

BASE = "8758bd30e302b75dd7854ac00fd2e29473669a13"
PREV = "dcc0885f73de6241d5efa9324ddb9f41784f6f2d"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I10 = "942f26fe32eaf91679e59a1968ae173a3703e22d"
ROOT = Path(__file__).resolve().parents[1]
RECOMP = ROOT / "integration/animo-b3/ANIMO-B3Q05_GLOBAL_QUEUE_RECOMPUTE.json"
PINS = ROOT / "integration/animo-b3/ANIMO-B3Q05_SOURCE_PINS.json"
FREEZE = ROOT / "integration/animo-b3/ANIMO-B3Q05_AUTHORING_FREEZE.json"
REVIEW = ROOT / "integration/animo-b3/ANIMO-B3Q05_INTERNAL_ADVERSARIAL_REVIEW.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3Q05_STATUS.json"
ASSURANCE = "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
ALLOWED = {
    ".github/workflows/animo-b3q05-global-queue-recompute.yml",
    "integration/animo-b3/ANIMO-B3Q05_GLOBAL_QUEUE_RECOMPUTE.json",
    "integration/animo-b3/ANIMO-B3Q05_SOURCE_PINS.json",
    "integration/animo-b3/ANIMO-B3Q05_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3Q05_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3Q05_STATUS.json",
    "tools/validate_animo_b3q05.py",
}


def fail(message):
    raise SystemExit("ANIMO-B3Q05 validation failed: " + message)


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout


def load(path):
    return json.loads(path.read_text())


def gj(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def gt(commit, path):
    return run("git", "show", f"{commit}:{path}")


def req(condition, message):
    if not condition:
        fail(message)


for commit in (BASE, PREV, B3Q01, B3I10):
    subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT, check=True)

changed = {p for p in run("git", "diff", "--name-only", BASE + "..HEAD").splitlines() if p}
req(changed <= ALLOWED, "scope escape " + str(sorted(changed - ALLOWED)))
req(not any(p.startswith("src/") or p.startswith("reference/") for p in changed), "source/reference modified")
req("integration/animo-reg/RG05_B3_QUEUE.json" not in changed, "canonical queue source modified")
req("docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" not in changed, "canonical TCD register modified")

pins = load(PINS)
rec = load(RECOMP)
fr = load(FREEZE)
st = load(STATUS)

req(pins["base_authority"]["head"] == BASE, "RG05N head pin")
req(pins["base_authority"]["exact_final_ci_run"] == 34646787915, "RG05N exact-final CI pin")
req(pins["base_authority"]["exact_final_ci_conclusion"] == "success", "RG05N exact-final conclusion")
req(pins["previous_queue_authority"]["head"] == PREV, "B3Q04 head pin")
req(pins["previous_queue_authority"]["exact_final_ci_run"] == 34610684987, "B3Q04 exact-final CI pin")
req(pins["previous_queue_authority"]["exact_final_ci_conclusion"] == "success", "B3Q04 exact-final conclusion")
req(pins["assurance"] == ASSURANCE, "pin assurance")
live = pins["live_recheck"]
req(live["rg05n_b3_complete"] is False and live["rg05n_b4_open"] is False and live["rg05n_production_open"] is False, "live project gate")
req(live["rg05n_scientific_admissions"] == 29 and live["rg05n_top_level_admitted"] == 19 and live["rg05n_admitted_child_atoms"] == 10, "live RG05N counts")
req(live["newer_top_level_tcd_reservation_found"] is False and live["later_aggregate_found"] is False, "unexpected newer authority")
req(fr["base_head"] == BASE and fr["review_must_pin_exact_commit"] is True and fr["substantive_change_resets_GOV05_review"] is True, "freeze contract")

rg = gj(BASE, "integration/animo-reg/ANIMO-RG05N_STATUS.json")
req(rg["state"] == "QUALIFIED_EIGHTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD039_TCD035_TCD036_NO_PRODUCTION", "RG05N state")
req(rg["scientific_admission_count"] == 29 and rg["historical_uncertainty_admission_count"] == 29 and rg["top_level_admitted_tcd_count"] == 19 and rg["admitted_child_atom_count"] == 10, "RG05N counts")
req(rg["current_queue_authority"] == "ANIMO-B3Q04@" + PREV, "RG05N prior queue pin")
req(rg["tcd039_state"]["top_level_admitted"] is True and rg["tcd039_state"]["canonical_state_admitted"] is False and rg["tcd039_state"]["production_authorized"] is False, "RG05N TCD039")
req(rg["tcd035_state"]["top_level_admitted"] is True and rg["tcd035_state"]["tcd036_admitted_by_tcd035"] is False and rg["tcd035_state"]["production_authorized"] is False, "RG05N TCD035")
req(rg["tcd036_state"]["top_level_admitted"] is True and rg["tcd036_state"]["ponding_scope"] == "ACTIVE_PRE_EXISTING_PONDING_ONLY" and rg["tcd036_state"]["dormant_layer0_state_created"] is False and rg["tcd036_state"]["production_authorized"] is False, "RG05N TCD036")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False, "RG05N downstream gate")

prev = gj(PREV, "integration/animo-b3/ANIMO-B3Q04_GLOBAL_QUEUE_RECOMPUTE.json")
req(prev["counts"] == {"canonical_top_level_queue": 25, "admitted_top_level": 16, "unadmitted_top_level": 9, "admitted_child_atoms": 10, "scientific_admission_objects": 26}, "B3Q04 counts")
req(prev["closure_result"]["global_canonical_b3_queue_closed"] is False, "B3Q04 closure state")

queue = gj(BASE, "integration/animo-reg/RG05_B3_QUEUE.json")
ids = [x["tcd"] for x in queue["entries"]]
req(len(ids) == 25 and len(set(ids)) == 25, "canonical queue membership")
req(queue["canonical_register"]["tail"] == "TCD-042" and queue["canonical_register"]["tcd_043_reserved"] is False, "canonical queue tail")
expected_admitted = set(prev["admitted_top_level_at_RG05M"]) | {"TCD-035", "TCD-036", "TCD-039"}
expected_unadmitted = set(ids) - expected_admitted
req(len(expected_admitted) == 19 and len(expected_unadmitted) == 6, "derived queue counts")
req(expected_unadmitted == {"TCD-016", "TCD-019", "TCD-032", "TCD-033", "TCD-034", "TCD-040"}, "derived remaining set")
req(set(rec["canonical_top_level_queue"]) == set(ids), "recomputed canonical membership")
req(set(rec["admitted_top_level_at_RG05N"]) == expected_admitted, "admitted set")
req({x["tcd"] for x in rec["unadmitted_top_level_at_RG05N"]} == expected_unadmitted, "unadmitted set")
req(set(rec["newly_admitted_top_level_since_B3Q04"]) == {"TCD-035", "TCD-036", "TCD-039"}, "new top-level delta")
req(rec["newly_admitted_child_atoms_since_B3Q04"] == [], "unexpected child delta")
req(rec["counts"] == {"canonical_top_level_queue": 25, "admitted_top_level": 19, "unadmitted_top_level": 6, "admitted_child_atoms": 10, "scientific_admission_objects": 29}, "recompute counts")
req(all(x["last_queue_state_revalidated_here"] is False for x in rec["unadmitted_top_level_at_RG05N"]), "remaining queue states must not be requalified here")

rules = gt(B3Q01, "docs/governance/B3_COMPOSITION_RULES.md")
req("If one required component is not admitted, the composition is not admitted." in rules, "B3Q01 component rule")
req("all component records are admitted and immutable by identity" in rules, "B3Q01 composition rule")
route = gj(B3I10, "integration/animo-b3/ANIMO-B3I10_STATUS.json")
req(route.get("qualified") is True and route.get("scientific_admission") is False, "B3I10 state")

cl = rec["closure_result"]
req(cl["global_canonical_b3_queue_closed"] is False and cl["whole_b3_composition_precondition_met"] is False and cl["positive_b3_composition_completeness_authority_allowed"] is False, "negative closure")
req(cl["tb7_allowed"] is False and cl["b4_allowed"] is False and cl["production_allowed"] is False, "downstream forbidden")
req(cl["blocker"] == "SIX_CANONICAL_TOP_LEVEL_B3_QUEUE_OBJECTS_REMAIN_UNADMITTED_AT_RG05N", "blocker")
req(all(v is False for v in rec["hard_boundaries"].values()), "recompute hard boundary")

req(st["current_aggregate_authority"] == "ANIMO-RG05N@" + BASE, "status aggregate")
req(st["canonical_queue"]["top_level_objects"] == 25 and st["canonical_queue"]["admitted_top_level"] == 19 and st["canonical_queue"]["unadmitted_top_level"] == 6 and st["canonical_queue"]["admitted_child_atoms"] == 10 and st["canonical_queue"]["scientific_admission_objects"] == 29, "status counts")
req(set(st["unadmitted_top_level"]) == expected_unadmitted, "status unadmitted")
req(st["global_canonical_b3_queue_closed"] is False and st["whole_b3_composition_complete"] is False and st["tb7_allowed"] is False and st["b4_allowed"] is False and st["production_allowed"] is False, "status negative gate")
req(st["registry_or_queue_modified"] is False and all(v is False for v in st["hard_boundaries"].values()), "status boundaries")
req(st["assurance"] == ASSURANCE and st["review"]["assurance"] == ASSURANCE, "status assurance")

if REVIEW.exists():
    rv = load(REVIEW)
    reviewed_head = rv.get("reviewed_head")
    req(rv.get("model") == "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" and rv.get("same_agent") is True and rv.get("genuinely_independent") is False and rv.get("independence_claimed") is False, "review model")
    req(rv.get("assurance") == ASSURANCE and rv.get("outcome") == "SELF_REVIEW_PASS_NEGATIVE_B3_CLOSURE_GATE_SIX_TOP_LEVEL_UNADMITTED", "review outcome")
    req(bool(reviewed_head) and rv.get("reviewed_head_ci_conclusion") == "success" and rv.get("reviewed_head_ci_run") and rv.get("reviewed_head_ci_job"), "reviewed-head CI")
    post = run("git", "diff", "--name-only", reviewed_head + "..HEAD").splitlines()
    req(not (set(post) - {"integration/animo-b3/ANIMO-B3Q05_INTERNAL_ADVERSARIAL_REVIEW.json", "integration/animo-b3/ANIMO-B3Q05_STATUS.json"}), "post-review substantive change")
    req(st["state"] == "QUALIFIED_ANIMO_B3Q05_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_SIX_TOP_LEVEL_UNADMITTED", "final state")
    req(st["decision"] == "B3_COMPOSITION_INCOMPLETE_DO_NOT_OPEN_TB7_B4_OR_PRODUCTION", "final decision")
    req(st["work_status"]["tested"] is True and st["work_status"]["reviewed"] is True and st["work_status"]["qualified"] is True and st["work_status"]["work_unit_complete"] is True, "final work status")
    req(st["review"]["completed"] is True and st["review"]["genuinely_independent"] is False, "final review status")
    print("ANIMO-B3Q05 PASS final negative closure gate; six top-level objects remain")
else:
    req(st["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" and st["state"] == "CANDIDATE_NEGATIVE_CLOSURE_GATE_PENDING_REVIEW", "candidate state")
    req(st["work_status"]["qualified"] is False and st["review"]["completed"] is False, "candidate not prematurely qualified")
    print("ANIMO-B3Q05 PASS frozen candidate pending GOV05 adversarial review")
