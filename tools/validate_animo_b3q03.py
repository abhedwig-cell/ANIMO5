#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

BASE = "214062fe773618ea77c7c74867cc8d9a2a4eef6d"
RG05J = "624bbad35add93de29ac89649155d9fa086a73af"
RG05K = "e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I10 = "942f26fe32eaf91679e59a1968ae173a3703e22d"

ROOT = Path(__file__).resolve().parents[1]
RECOMP = ROOT / "integration/animo-b3/ANIMO-B3Q03_GLOBAL_QUEUE_RECOMPUTE.json"
PINS = ROOT / "integration/animo-b3/ANIMO-B3Q03_SOURCE_PINS.json"
REVIEW = ROOT / "integration/animo-b3/ANIMO-B3Q03_INTERNAL_ADVERSARIAL_REVIEW.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3Q03_STATUS.json"

ALLOWED = {
    ".github/workflows/animo-b3q03-global-queue-recompute.yml",
    "integration/animo-b3/ANIMO-B3Q03_GLOBAL_QUEUE_RECOMPUTE.json",
    "integration/animo-b3/ANIMO-B3Q03_SOURCE_PINS.json",
    "integration/animo-b3/ANIMO-B3Q03_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-b3/ANIMO-B3Q03_STATUS.json",
    "tools/validate_animo_b3q03.py",
}


def fail(msg):
    raise SystemExit(f"ANIMO-B3Q03 validation failed: {msg}")


def run(*args):
    p = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return p.stdout


def jload(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def git_json(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def git_text(commit, path):
    return run("git", "show", f"{commit}:{path}")


def require(cond, msg):
    if not cond:
        fail(msg)


for commit in (BASE, RG05J, RG05K, B3Q01, B3I10):
    subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT, check=True)

changed = {p for p in run("git", "diff", "--name-only", f"{BASE}..HEAD").splitlines() if p}
require(changed <= ALLOWED, f"scope guard found non-allowlisted paths: {sorted(changed - ALLOWED)}")
require(not any(p.startswith("src/") for p in changed), "production source changed")
require("integration/animo-reg/RG05_B3_QUEUE.json" not in changed, "canonical queue source was modified")
require("docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" not in changed, "canonical TCD register was modified")

pins = jload(PINS)
recomp = jload(RECOMP)
review = jload(REVIEW)

require(pins["base_authority"]["head"] == BASE, "base authority head mismatch")
require(pins["base_authority"]["exact_final_ci_run"] == 34588681709, "RG05L exact-head CI pin mismatch")
require(pins["base_authority"]["exact_final_ci_conclusion"] == "success", "RG05L exact-head CI not pinned successful")
require(pins["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "assurance wording mismatch")
require(pins["live_recheck"]["rg05l_b3_complete"] is False, "pins unexpectedly claim B3 complete")
require(pins["live_recheck"]["newer_top_level_tcd_reservation_found"] is False, "unexpected later top-level reservation")

rg05l = git_json(BASE, "integration/animo-reg/ANIMO-RG05L_STATUS.json")
rg05k = git_json(RG05K, "integration/animo-reg/RG05K_B3_ADMISSION_INVENTORY.json")
rg05j = git_json(RG05J, "integration/animo-reg/RG05J_B3_ADMISSION_INVENTORY.json")
queue = git_json(BASE, "integration/animo-reg/RG05_B3_QUEUE.json")
routing = git_json(B3I10, "integration/animo-b3/B3I10_TCD042_CHILD_SCOPE_ROUTING.json")
rules = git_text(B3Q01, "docs/governance/B3_COMPOSITION_RULES.md")

require(rg05l["state"] == "QUALIFIED_SIXTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD025_A4_PARENT_AND_TCD042_B1_NO_PRODUCTION", "unexpected RG05L state")
require(rg05l["b3_complete"] is False, "RG05L unexpectedly claims B3 complete")
require(rg05l["b4_open"] is False and rg05l["production_open"] is False, "RG05L opened B4 or production")
require(rg05l["top_level_admitted_tcd_count"] == 14, "RG05L top-level admitted count mismatch")
require(rg05l["admitted_child_atom_count"] == 9, "RG05L child atom count mismatch")
require(rg05l["scientific_admission_count"] == 23, "RG05L scientific admission count mismatch")
require(rg05l["tcd025_state"]["parent_admitted"] is True, "TCD-025 parent is not admitted at RG05L")
require(rg05l["tcd042_state"]["parent_admitted"] is False, "TCD-042 parent unexpectedly admitted")
require(rg05l["tcd042_state"]["E1_admitted"] is False, "TCD-042-E1 unexpectedly admitted")
require(rg05l["hard_boundaries"]["automatic_parent_admission_performed"] is False, "automatic parent admission was performed")
require(rg05l["hard_boundaries"]["historical_fidelity_claimed"] is False, "historical fidelity unexpectedly claimed")

require(rg05k["post_state"]["top_level_admitted_tcd_count"] == 13, "RG05K top-level count mismatch")
require(all(x["object_kind"] == "BOUNDED_CHILD_ATOM" for x in rg05k["new_admissions"]), "RG05K contained an unexpected non-child admission")
require(rg05j["post_state"]["tcd037_parent_admitted"] is True, "RG05J TCD-037 parent state mismatch")

queue_ids = [x["tcd"] for x in queue["entries"]]
require(len(queue_ids) == 25 and len(set(queue_ids)) == 25, "canonical queue must contain 25 unique top-level objects")
require(queue["canonical_register"]["tail"] == "TCD-042", "canonical queue tail is not TCD-042")
require(queue["canonical_register"]["tcd_043_reserved"] is False, "TCD-043 unexpectedly reserved")

rg05j_top = list(rg05j["post_state"]["top_level_admitted_tcds"])
expected_admitted = set(rg05j_top) | {"TCD-025"}
require(len(expected_admitted) == 14, "derived RG05L top-level admitted set does not contain 14 objects")
require(set(recomp["admitted_top_level_at_RG05L"]) == expected_admitted, "recomputed admitted top-level set mismatch")
require(set(recomp["canonical_top_level_queue"]) == set(queue_ids), "recomputed canonical queue membership mismatch")

unadmitted = set(queue_ids) - expected_admitted
reported_unadmitted = {x["tcd"] for x in recomp["unadmitted_top_level_at_RG05L"]}
require(reported_unadmitted == unadmitted, "recomputed unadmitted top-level set mismatch")
require(len(unadmitted) == 11, "expected exactly eleven unadmitted top-level objects")
require(recomp["counts"] == {"canonical_top_level_queue":25,"admitted_top_level":14,"unadmitted_top_level":11,"admitted_child_atoms":9,"scientific_admission_objects":23}, "recompute counts mismatch")

require(routing["parent"]["admitted"] is False, "B3I10 parent TCD-042 unexpectedly admitted")
require(routing["children"]["TCD-042-B1"]["ready_for_separate_bounded_admission_decision"] is True, "B3I10 B1 routing state mismatch")
require(routing["children"]["TCD-042-E1"]["ready_for_admission_here"] is False, "B3I10 E1 unexpectedly ready for admission here")
require(routing["Hetop_zero_disposition"]["state"] == "EXCLUDED_FROM_SUPPORTED_B3_B4_CHILD_SCOPE_FOR_FROZEN_REVISION53", "Hetop=0 disposition mismatch")

require("If one required component is not admitted, the composition is not admitted." in rules, "B3Q01 component-admission composition rule missing")
require("all component records are admitted and immutable by identity" in rules, "B3Q01 composition admission rule missing")

closure = recomp["closure_result"]
require(closure["global_canonical_b3_queue_closed"] is False, "queue incorrectly marked closed")
require(closure["whole_b3_composition_precondition_met"] is False, "whole-B3 composition precondition incorrectly met")
require(closure["positive_b3_composition_completeness_authority_allowed"] is False, "positive completeness authority incorrectly allowed")
require(closure["tb7_allowed"] is False, "TB7 incorrectly allowed")
require(closure["blocker"] == "ELEVEN_CANONICAL_TOP_LEVEL_B3_QUEUE_OBJECTS_REMAIN_UNADMITTED_AT_RG05L", "unexpected closure blocker")
require(all(v is False for v in recomp["hard_boundaries"].values()), "a recompute hard boundary was crossed")

require(review["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance mismatch")
require(review["review_conclusion"] == "PASS_FOR_NEGATIVE_CLOSURE_GATE_ONLY", "adversarial review did not pass negative gate")
require(review["positive_composition_completeness_authority_created"] is False, "review claims positive completeness authority")

if STATUS.exists():
    status = jload(STATUS)
    require(status["state"] == "QUALIFIED_ANIMO_B3Q03_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_ELEVEN_TOP_LEVEL_UNADMITTED", "status state mismatch")
    require(status["decision"] == "B3_COMPOSITION_INCOMPLETE_DO_NOT_OPEN_TB7_B4_OR_PRODUCTION", "status decision mismatch")
    require(status["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "status assurance mismatch")
    require(status["current_aggregate_authority"] == f"ANIMO-RG05L@{BASE}", "status aggregate authority mismatch")
    require(status["global_canonical_b3_queue_closed"] is False, "status incorrectly closes queue")
    require(status["whole_b3_composition_complete"] is False, "status incorrectly claims composition complete")
    require(status["tb7_allowed"] is False, "status incorrectly allows TB7")
    require(status["registry_or_queue_modified"] is False, "status claims queue/registry modification")
    require(all(v is False for v in status["hard_boundaries"].values()), "a status hard boundary was crossed")

print("ANIMO-B3Q03 validation PASS")
