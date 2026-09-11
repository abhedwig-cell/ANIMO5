#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "0bec1968adbf77fd04c6f46819d704b86482d8b2"
RG05K = "e5ccad78d7c85aaf2c68d844c5a496edf6d73db5"
B3I08 = "f4a3056087e5f7bac41b243be1f404739cde52b0"
B3I09 = "fcce3e5d3c465dbd618f1e36e1d5f259f74b2d2a"
B3D27 = "cb881d0cd3e3c50455614a93b562b32354f0f1a8"
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


def sh(*args):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()


def load(path):
    return json.loads((ROOT / path).read_text())


def show_json(commit, path):
    return json.loads(sh("git", "show", f"{commit}:{path}"))


def assert_eq(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def remote_heads():
    out = sh("git", "ls-remote", "--heads", "origin")
    result = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        sha, ref = line.split("\t", 1)
        result[ref] = sha
    return result


pins = load("integration/animo-b3/ANIMO-B3COMP01_SOURCE_PINS.json")
audit = load("integration/animo-b3/ANIMO-B3COMP01_COMPLETENESS_AUDIT.json")
freeze = load("integration/animo-b3/ANIMO-B3COMP01_AUTHORING_FREEZE.json")
status = load("integration/animo-b3/ANIMO-B3COMP01_STATUS.json")

assert_eq(pins["authoring_base"]["head"], BASE, "base pin")
assert_eq(pins["current_aggregate"]["head"], RG05K, "aggregate pin")
assert_eq(pins["current_qualified_tcd025_routing"]["head"], B3I08, "B3I08 pin")
assert_eq(pins["concurrent_tcd025_scope_workstream"]["observed_head"], B3I09, "B3I09 observed pin")
assert_eq(pins["bounded_existing_parent_composition"]["head"], B3D27, "B3D27 pin")
assert_eq(pins["testbank_prerequisite_gate"]["head"], TB07A, "TB07A pin")
assert_eq(pins["governance"]["gov05"], f"ANIMO-GOV05@{GOV05}", "GOV05 pin")
assert_eq(pins["governance"]["b3q01"], f"ANIMO-B3Q01@{B3Q01}", "B3Q01 pin")

changed = set(filter(None, sh("git", "diff", "--name-only", f"{BASE}..HEAD").splitlines()))
extra = changed - ALLOWED
if extra:
    raise AssertionError(f"out-of-scope changed paths: {sorted(extra)}")
if any(p.startswith("src/") for p in changed):
    raise AssertionError("production source changed")

heads = remote_heads()
b3i09_ref = "refs/heads/work/animo-b3i09-tcd025-a5-exclusion-parent-scope-routing"
assert_eq(heads.get(b3i09_ref), B3I09, "concurrent B3I09 live head advanced; re-audit required")
rg05k_ref = "refs/heads/work/animo-rg05k-fifth-batched-admission-integration"
assert_eq(heads.get(rg05k_ref), RG05K, "RG05K live head drift")

higher_aggregate = []
for ref in heads:
    m = re.search(r"refs/heads/work/animo-rg05([a-z])-", ref)
    if m and m.group(1) > "k":
        higher_aggregate.append(ref)
if higher_aggregate:
    raise AssertionError(f"newer RG05 aggregate branch detected: {higher_aggregate}")

higher_b3d = []
higher_b3i = []
for ref in heads:
    md = re.search(r"refs/heads/work/animo-b3d(\d+)-", ref)
    if md and int(md.group(1)) > 31:
        higher_b3d.append(ref)
    mi = re.search(r"refs/heads/work/animo-b3i(\d+)-", ref)
    if mi and int(mi.group(1)) > 9:
        higher_b3i.append(ref)
if higher_b3d:
    raise AssertionError(f"newer B3 admission branch detected: {higher_b3d}")
if higher_b3i:
    raise AssertionError(f"newer B3 routing branch detected: {higher_b3i}")

rg = show_json(RG05K, "integration/animo-reg/ANIMO-RG05K_STATUS.json")
rg_inv = show_json(RG05K, "integration/animo-reg/RG05K_B3_ADMISSION_INVENTORY.json")
b3d31 = show_json(BASE, "integration/animo-b3/ANIMO-B3D31_STATUS.json")
b3i08 = show_json(B3I08, "integration/animo-b3/ANIMO-B3I08_STATUS.json")
b3i09 = show_json(B3I09, "integration/animo-b3/ANIMO-B3I09_STATUS.json")
b3i09_route = show_json(B3I09, "integration/animo-b3/B3I09_TCD025_PARENT_SCOPE_ROUTING.json")
b3d27 = show_json(B3D27, "integration/animo-b3/ANIMO-B3D27_STATUS.json")
tb07a = show_json(TB07A, "integration/animo-testbank/ANIMO-TB07A_STATUS.json")
gov05 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
b3q01 = show_json(B3Q01, "integration/animo-b3/ANIMO-B3Q01_STATUS.json")

assert_eq(rg["b3_complete"], False, "RG05K B3 completeness")
assert_eq(rg["global_canonical_queue_count_recomputed"], False, "RG05K queue recomputation")
assert_eq(rg_inv["project_boundary"]["B3_complete"], False, "RG05K inventory completeness")
assert_eq(b3d31["admitted"], True, "B3D31 admitted")
assert_eq(b3d31["admission_effect"]["parent_tcd_admitted"], False, "B3D31 parent non-admission")
assert_eq(b3d31["admission_effect"]["A5_blocker_disposed"], False, "B3D31 A5 non-disposition")
assert_eq(b3i08["status"], "QUALIFIED_TCD025_CHILD_SCOPE_PARTITION_A1_A4_BOUNDED_A5_BLOCKED_NO_ADMISSION", "B3I08 state")
assert_eq(b3i09["state"], "NOT_YET_QUALIFIED", "B3I09 qualification state")
assert_eq(b3i09_route["parent"]["admitted"], False, "B3I09 candidate parent admission")
assert_eq(b3i09_route["parent"]["ready_for_separate_restricted_parent_composition_decision"], True, "B3I09 candidate separate parent decision")
assert_eq(b3d27["parent_scientific_claim"]["kind"], "BOUNDED_COMPOSED_GHG_OBSERVER_ACCOUNTING_CONTRACT", "B3D27 bounded composition kind")
assert_eq(b3d27["parent_scientific_claim"]["complete_ghg_carbon_ledger"], False, "B3D27 no complete GHG carbon ledger")
assert_eq(tb07a["composition_readiness"]["TB7_baseline_authorized"], False, "TB07A authorization")
assert_eq(tb07a["unblock_condition"].startswith("A separate exact-head-qualified scientific authority"), True, "TB07A unblock contract")
assert_eq(gov05["assurance_change"]["same_agent_assurance"], "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "GOV05 assurance")
assert_eq(b3q01["fail_closed_contract"]["composition_requires_separate_record_and_qualification"], True, "B3Q01 composition separate record")

assert_eq(audit["result"], "B3_COMPOSITION_COMPLETENESS_NOT_ESTABLISHED", "audit result")
assert_eq(audit["tb7_effect"], "BLOCKED", "audit TB7 effect")
assert_eq(audit["observations"]["aggregate_b3_complete"], False, "audit aggregate observation")
assert_eq(audit["observations"]["whole_b3_composition_exact_final_authority_found"], False, "audit whole-B3 authority observation")
assert_eq(status["b3_composition_complete"], False, "status B3 composition complete")
assert_eq(status["tb7_authorized"], False, "status TB7 authorization")
assert_eq(status["whole_model_golden_baseline_authorized"], False, "status whole-model golden authorization")
assert_eq(status["review_assurance"], "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "status assurance")
for key, value in status["hard_boundaries"].items():
    if value is not False:
        raise AssertionError(f"hard boundary {key} must remain false")

review_path = ROOT / "integration/animo-b3/ANIMO-B3COMP01_INTERNAL_ADVERSARIAL_REVIEW.json"
if status["phase"] == "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW":
    assert_eq(status["state"], "NOT_YET_QUALIFIED", "authoring state")
    assert_eq(status["review"]["completed"], False, "authoring review completion")
    if review_path.exists():
        raise AssertionError("review artifact present before status enters reviewed phase")
    print("PASS_B3COMP01_AUTHORING_FROZEN_NEGATIVE_COMPLETENESS_AUDIT")
elif status["phase"] == "QUALIFIED_SUBJECT_TO_EXACT_FINAL_HEAD_CI":
    assert_eq(status["state"], "QUALIFIED_B3_COMPOSITION_COMPLETENESS_AUTHORITY_NEGATIVE_TB7_BLOCKED", "final state")
    assert_eq(status["decision"], "B3_COMPOSITION_COMPLETENESS_NOT_ESTABLISHED_TB7_REMAINS_BLOCKED", "final decision")
    assert_eq(status["review"]["completed"], True, "final review completion")
    review = load("integration/animo-b3/ANIMO-B3COMP01_INTERNAL_ADVERSARIAL_REVIEW.json")
    assert_eq(review["outcome"], "SELF_REVIEW_PASS_NEGATIVE_COMPLETENESS_AUTHORITY", "review outcome")
    assert_eq(review["assurance"], "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT", "review assurance")
    assert_eq(review["genuinely_independent"], False, "review independence")
    authoring_head = status["validation"]["authoring_head"]
    assert_eq(review["reviewed_head"], authoring_head, "reviewed authoring head")
    post_review_changed = set(filter(None, sh("git", "diff", "--name-only", f"{authoring_head}..HEAD").splitlines()))
    permitted = {
        "integration/animo-b3/ANIMO-B3COMP01_INTERNAL_ADVERSARIAL_REVIEW.json",
        "integration/animo-b3/ANIMO-B3COMP01_STATUS.json",
    }
    if post_review_changed - permitted:
        raise AssertionError(f"substantive files changed after reviewed checkpoint: {sorted(post_review_changed - permitted)}")
    assert_eq(status["work_status"]["qualified"], True, "final qualified flag")
    assert_eq(status["work_status"]["workunit_complete"], True, "final workunit complete")
    print("PASS_B3COMP01_NEGATIVE_COMPOSITION_COMPLETENESS_AUTHORITY")
else:
    raise AssertionError(f"unexpected phase: {status['phase']}")
