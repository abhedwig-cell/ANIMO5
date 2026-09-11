#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "0bec1968adbf77fd04c6f46819d704b86482d8b2"
RG05K = "e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"
B3D32 = "4d7c42bb749ed5fbf1c884fba4a26a1a5b898505"
B3I10 = "942f26fe32eaf91679e59a1968ae173a3703e22d"
B3D33_SEED = "942f26fe32eaf91679e59a1968ae173a3703e22d"
TB07A = "6d77e92f5beb2a30deb7411d93890aa7a5559685"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"

ALLOWED = {
    ".github/workflows/animo-b3comp01-composition-completeness.yml",
    "docs/b3comp01/B3_COMPOSITION_COMPLETENESS_AUTHORITY.md",
    "integration/animo-b3/ANIMO-B3COMP01_SOURCE_PINS.json",
    "integration/animo-b3/ANIMO-B3COMP01_COMPLETENESS_AUDIT.json",
    "integration/animo-b3/ANIMO-B3COMP01_AUTHORING_FREEZE.json",
    "integration/animo-b3/ANIMO-B3COMP01_STATUS.json",
    "integration/animo-b3/ANIMO-B3COMP01_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/validate_b3comp01_composition_completeness.py",
}


def sh(*args, check=True):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if check and p.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
    return p


def text(*args):
    return sh(*args).stdout.strip()


def load(path):
    return json.loads((ROOT / path).read_text())


def show_json(commit, path):
    return json.loads(text("git", "show", f"{commit}:{path}"))


def assert_eq(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def remote_heads():
    out = text("git", "ls-remote", "--heads", "origin")
    result = {}
    for line in out.splitlines():
        if line.strip():
            sha, ref = line.split("\t", 1)
            result[ref] = sha
    return result


pins = load("integration/animo-b3/ANIMO-B3COMP01_SOURCE_PINS.json")
audit = load("integration/animo-b3/ANIMO-B3COMP01_COMPLETENESS_AUDIT.json")
status = load("integration/animo-b3/ANIMO-B3COMP01_STATUS.json")
freeze = load("integration/animo-b3/ANIMO-B3COMP01_AUTHORING_FREEZE.json")

assert_eq(pins["work_unit"], "ANIMO-B3COMP01R", "pins work unit")
assert_eq(pins["current_aggregate"]["head"], RG05K, "aggregate pin")
assert_eq(pins["tcd025_parent_composition"]["head"], B3D32, "B3D32 pin")
assert_eq(pins["tcd042_routing"]["head"], B3I10, "B3I10 pin")
assert_eq(pins["concurrent_tcd042_b1_admission_workstream"]["observed_head"], B3D33_SEED, "B3D33 observed pin")
assert_eq(pins["testbank_prerequisite_gate"]["head"], TB07A, "TB07A pin")
assert_eq(pins["governance"]["gov05"], f"ANIMO-GOV05@{GOV05}", "GOV05 pin")
assert_eq(pins["governance"]["b3q01"], f"ANIMO-B3Q01@{B3Q01}", "B3Q01 pin")

changed = set(filter(None, text("git", "diff", "--name-only", f"{BASE}..HEAD").splitlines()))
extra = changed - ALLOWED
if extra:
    raise AssertionError(f"out-of-scope changed paths: {sorted(extra)}")
if any(p.startswith("src/") or p.startswith("reference/source/") or p.startswith("reference/testcases/") for p in changed):
    raise AssertionError("production or frozen reference source changed")

heads = remote_heads()
expected_heads = {
    "refs/heads/work/animo-rg05k-fifth-batched-admission-integration": RG05K,
    "refs/heads/work/animo-b3d32-tcd025-restricted-parent-composition-gov05-tier-d-admission": B3D32,
    "refs/heads/work/animo-b3i10-tcd042-positive-hetop-child-scope-routing": B3I10,
    "refs/heads/work/animo-b3d33-tcd042-b1-positive-hetop-gov05-tier-c-admission": B3D33_SEED,
}
for ref, expected in expected_heads.items():
    assert_eq(heads.get(ref), expected, f"live head drift for {ref}")

later_aggregate = []
later_b3d = []
later_b3i = []
for ref in heads:
    ma = re.search(r"refs/heads/work/animo-rg05([a-z])-", ref)
    if ma and ma.group(1) > "k":
        later_aggregate.append(ref)
    md = re.search(r"refs/heads/work/animo-b3d(\d+)-", ref)
    if md and int(md.group(1)) > 33:
        later_b3d.append(ref)
    mi = re.search(r"refs/heads/work/animo-b3i(\d+)-", ref)
    if mi and int(mi.group(1)) > 10:
        later_b3i.append(ref)
if later_aggregate:
    raise AssertionError(f"newer aggregate branch detected: {later_aggregate}")
if later_b3d:
    raise AssertionError(f"newer B3 admission branch detected: {later_b3d}")
if later_b3i:
    raise AssertionError(f"newer B3 routing branch detected: {later_b3i}")

rg = show_json(RG05K, "integration/animo-reg/ANIMO-RG05K_STATUS.json")
rg_inv = show_json(RG05K, "integration/animo-reg/RG05K_B3_ADMISSION_INVENTORY.json")
b3d32 = show_json(B3D32, "integration/animo-b3/ANIMO-B3D32_STATUS.json")
b3i10 = show_json(B3I10, "integration/animo-b3/ANIMO-B3I10_STATUS.json")
tb07a = show_json(TB07A, "integration/animo-testbank/ANIMO-TB07A_STATUS.json")
gov05 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
b3q01 = show_json(B3Q01, "integration/animo-b3/ANIMO-B3Q01_STATUS.json")

assert_eq(rg["b3_complete"], False, "RG05K B3 completeness")
assert_eq(rg["global_canonical_queue_count_recomputed"], False, "RG05K queue recomputation")
assert_eq(rg_inv["project_boundary"]["B3_complete"], False, "RG05K inventory completeness")
assert_eq(b3d32["admitted"], True, "B3D32 admitted")
assert_eq(b3d32["parent_tcd_admitted"], True, "B3D32 parent admission")
assert_eq(b3d32["admission_effect"]["A5_b3_admitted"], False, "B3D32 A5 remains unadmitted")
assert_eq(b3d32["admission_effect"]["A5_revision53_scope_exclusion_preserved"], True, "B3D32 A5 exclusion preserved")
assert_eq(b3i10["qualified"], True, "B3I10 qualified")
assert_eq(b3i10["routing_effect"]["TCD042_B1_ready_for_separate_bounded_admission"], True, "B3I10 B1 readiness")
assert_eq(b3i10["child_admitted_here"], False, "B3I10 no child admission")
assert_eq(b3i10["parent_tcd_admitted"], False, "B3I10 no parent admission")
assert_eq(tb07a["composition_readiness"]["TB7_baseline_authorized"], False, "TB07A authorization")
assert_eq(gov05["assurance_change"]["same_agent_assurance"], "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "GOV05 assurance")
assert_eq(b3q01["fail_closed_contract"]["composition_requires_separate_record_and_qualification"], True, "B3Q01 separate composition record")

# B3D33 is a separate concurrent workstream. At the observed pin it is only a seed branch.
probe = sh("git", "cat-file", "-e", f"{B3D33_SEED}:integration/animo-b3/ANIMO-B3D33_STATUS.json", check=False)
if probe.returncode == 0:
    raise AssertionError("B3D33 status unexpectedly exists at observed seed head; re-audit required")

assert_eq(audit["result"], "B3_COMPOSITION_COMPLETENESS_NOT_ESTABLISHED", "audit result")
assert_eq(audit["tb7_effect"], "BLOCKED", "audit TB7 effect")
assert_eq(audit["observations"]["tcd025_restricted_parent_admitted"], True, "audit TCD025 closure")
assert_eq(audit["observations"]["tcd042_B1_admitted"], False, "audit TCD042 B1 admission")
assert_eq(audit["observations"]["whole_b3_composition_exact_final_authority_found"], False, "audit whole-B3 authority")
assert_eq(status["b3_composition_complete"], False, "status B3 completeness")
assert_eq(status["tb7_authorized"], False, "status TB7 authorization")
assert_eq(status["whole_model_golden_baseline_authorized"], False, "status whole-model golden authorization")
assert_eq(status["review_assurance"], "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "status assurance")
assert_eq(freeze["concurrent_workstream_policy"], "OBSERVE_AND_FAIL_CLOSED_ON_ADVANCE_DO_NOT_MUTATE", "concurrency policy")
for key, value in status["hard_boundaries"].items():
    if value is not False:
        raise AssertionError(f"hard boundary {key} must remain false")

if status["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW":
    assert_eq(status["state"], "NOT_YET_QUALIFIED", "authoring state")
    assert_eq(status["review"]["completed"], False, "authoring review completion")
    assert_eq(status["work_status"]["qualified"], False, "authoring qualified flag")
    print("PASS_B3COMP01R_AUTHORING_FROZEN_NEGATIVE_COMPLETENESS_REAUDIT")
elif status["phase"] == "QUALIFIED_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
    assert_eq(status["state"], "QUALIFIED_B3_COMPOSITION_COMPLETENESS_AUTHORITY_NEGATIVE_TB7_BLOCKED", "final state")
    assert_eq(status["decision"], "B3_COMPOSITION_COMPLETENESS_NOT_ESTABLISHED_TB7_REMAINS_BLOCKED", "final decision")
    review = load("integration/animo-b3/ANIMO-B3COMP01_INTERNAL_ADVERSARIAL_REVIEW.json")
    assert_eq(review["work_unit"], "ANIMO-B3COMP01R", "review work unit")
    assert_eq(review["outcome"], "SELF_REVIEW_PASS_NEGATIVE_COMPLETENESS_AUTHORITY", "review outcome")
    assert_eq(review["assurance"], "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance")
    assert_eq(review["genuinely_independent"], False, "review independence")
    authoring_head = status["validation"]["authoring_head"]
    assert_eq(review["reviewed_head"], authoring_head, "reviewed authoring head")
    post_review_changed = set(filter(None, text("git", "diff", "--name-only", f"{authoring_head}..HEAD").splitlines()))
    permitted = {
        "integration/animo-b3/ANIMO-B3COMP01_INTERNAL_ADVERSARIAL_REVIEW.json",
        "integration/animo-b3/ANIMO-B3COMP01_STATUS.json",
    }
    if post_review_changed - permitted:
        raise AssertionError(f"substantive files changed after reviewed checkpoint: {sorted(post_review_changed - permitted)}")
    assert_eq(status["work_status"]["qualified"], True, "final qualified flag")
    assert_eq(status["work_status"]["workunit_complete"], True, "final complete flag")
    print("PASS_B3COMP01R_NEGATIVE_COMPOSITION_COMPLETENESS_AUTHORITY")
else:
    raise AssertionError(f"unexpected phase: {status['phase']}")
