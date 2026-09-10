#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "eed822037ed8d906a2ab424220597cffac9cca73"
GOV04 = "ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc"
B3D13 = "ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4"
B3D14 = "ANIMO-B3D14@d672992bbc32d40d7e0fbdf03f3fa9bc4cd5a522"
B3B07R = "ANIMO-B3B07R@3587c7a94a992f3779034c4c1e5f4134192d54f3"
ADMITTED = ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015", "TCD-027", "TCD-041"]
ALLOWED = {
    ".github/workflows/animo-rg05f-first-gov04-batch.yml",
    "docs/governance/ANIMO_RG05F_FIRST_GOV04_BATCHED_ADMISSION_REGIE.md",
    "integration/animo-reg/ANIMO-RG05F_STATUS.json",
    "integration/animo-reg/RG05F_B3_ADMISSION_INVENTORY.json",
    "integration/animo-reg/RG05F_B3_QUEUE_DELTA.json",
    "tools/validate_rg05f_first_gov04_batch.py",
}


def fail(message: str) -> None:
    print(f"FAIL_RG05F: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: str):
    p = ROOT / path
    if not p.is_file():
        fail(f"missing required file {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path}: {exc}")


def expect(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


inv = load("integration/animo-reg/RG05F_B3_ADMISSION_INVENTORY.json")
delta = load("integration/animo-reg/RG05F_B3_QUEUE_DELTA.json")
status = load("integration/animo-reg/ANIMO-RG05F_STATUS.json")

expect(inv.get("work_unit") == "ANIMO-RG05F", "inventory work_unit mismatch")
expect(inv.get("source_aggregate", {}).get("head") == BASE, "inventory RG05E base mismatch")
expect(inv.get("governance_authority") == GOV04, "inventory GOV04 pin mismatch")
expect(inv.get("admitted_tcds") == ADMITTED, "aggregate admitted_tcd list mismatch")
expect(inv.get("counts", {}).get("scientific_admissions") == 7, "scientific admission count must be 7")
expect(inv.get("counts", {}).get("atomic_admissions") == 7, "atomic admission count must be 7")
expect(inv.get("counts", {}).get("historical_uncertainty_admissions") == 7, "historical-uncertainty count must be 7")
expect(inv.get("counts", {}).get("b4_admissions") == 0, "B4 must remain closed")
expect(inv.get("counts", {}).get("production_migrations") == 0, "production migration must remain closed")

batch = inv.get("batch_policy", {})
expect(batch.get("normal_new_admission_min") == 3, "GOV04 normal batch minimum must be 3")
expect(batch.get("normal_new_admission_max") == 5, "GOV04 normal batch maximum must be 5")
expect(batch.get("new_admissions_in_this_batch") == 2, "RG05F must integrate exactly two new admissions")
expect(batch.get("normal_threshold_reached") is False, "two-admission batch must not claim normal threshold reached")
expect(batch.get("early_batch") is True, "RG05F must explicitly identify the early batch")
expect(bool(batch.get("early_batch_basis")), "early batch requires explicit ambiguity-reduction basis")

new = inv.get("new_admissions", [])
expect(len(new) == 2, "inventory must contain exactly two new admissions")
by_tcd = {x.get("tcd"): x for x in new}
expect(set(by_tcd) == {"TCD-027", "TCD-041"}, "new admission set must be exactly TCD-027 and TCD-041")
expect(by_tcd["TCD-027"].get("admission_authority") == B3D13, "TCD-027 B3D13 pin mismatch")
expect(by_tcd["TCD-027"].get("risk_tier") == "A", "TCD-027 must remain Tier A")
expect(by_tcd["TCD-027"].get("gov04_tier_a_waiver") == "PASS_ALL_CONDITIONS", "TCD-027 Tier-A waiver must remain explicit")
expect(by_tcd["TCD-027"].get("historical_behaviour") == "UNKNOWN", "TCD-027 historical behaviour must remain UNKNOWN")
expect(by_tcd["TCD-041"].get("admission_authority") == B3D14, "TCD-041 B3D14 pin mismatch")
expect(by_tcd["TCD-041"].get("review_authority") == B3B07R, "TCD-041 independent review pin mismatch")
expect(by_tcd["TCD-041"].get("risk_tier") == "B", "TCD-041 must remain Tier B")
expect(by_tcd["TCD-041"].get("historical_behaviour") == "UNKNOWN_WITHOUT_B2", "TCD-041 historical behaviour must remain UNKNOWN_WITHOUT_B2")
expect(by_tcd["TCD-041"].get("tcd032_037_dependency") is False, "TCD-041 must not gain TCD-032..037 dependency")

expect(delta.get("work_unit") == "ANIMO-RG05F", "queue delta work_unit mismatch")
expect(delta.get("base_aggregate") == f"ANIMO-RG05E@{BASE}", "queue delta RG05E pin mismatch")
expect(delta.get("governance_authority") == GOV04, "queue delta GOV04 pin mismatch")
expect(delta.get("admitted_tcds") == ADMITTED, "queue delta admitted list mismatch")
expect(len(delta.get("tcd_deltas", [])) == 2, "queue delta must contain exactly two TCD changes")
pre = delta.get("pre_delta_counts", {})
post = delta.get("post_delta_counts", {})
expected_pre = {
    "canonical_tcd_entries": 25,
    "active_queue_entries": 20,
    "READY_FOR_ADMISSION_READINESS": 4,
    "IN_PROGRESS_ADMISSION_READINESS": 0,
    "WAITING_ON_ROUTE_AND_REVIEW": 2,
    "WAITING_ON_THEORY": 4,
    "WAITING_ON_NUMERICS": 2,
    "WAITING_ON_STATE": 5,
    "WAITING_ON_RUNTIME": 2,
    "WAITING_ON_CHILDREN": 1,
    "NOT_READY": 0,
    "scientific_admissions": 5,
}
expected_post = dict(expected_pre)
expected_post.update({
    "active_queue_entries": 18,
    "READY_FOR_ADMISSION_READINESS": 3,
    "WAITING_ON_ROUTE_AND_REVIEW": 1,
    "scientific_admissions": 7,
})
expect(pre == expected_pre, "pre-delta count vector does not match RG05E")
expect(post == expected_post, "post-delta count vector is not the exact two-admission delta")
expect(post["active_queue_entries"] == post["canonical_tcd_entries"] - post["scientific_admissions"], "active queue count must equal canonical entries minus admissions")

expect(status.get("work_unit") == "ANIMO-RG05F", "status work_unit mismatch")
expect(status.get("authoring_base") == f"ANIMO-RG05E@{BASE}", "status authoring base mismatch")
expect(status.get("governance_authority") == GOV04, "status GOV04 pin mismatch")
expect(status.get("aggregate_state", {}).get("scientific_admissions") == 7, "status scientific admission count must be 7")
expect(status.get("aggregate_state", {}).get("admitted_tcds") == ADMITTED, "status admitted list mismatch")
expect(status.get("aggregate_state", {}).get("active_queue_entries") == 18, "status active queue must be 18")
expect(status.get("aggregate_state", {}).get("B3_complete") is False, "B3 must remain incomplete")
expect(status.get("aggregate_state", {}).get("B4_admitted") is False, "B4 must remain closed")
expect(status.get("aggregate_state", {}).get("production_migration_admitted") is False, "production migration must remain closed")
expect(status.get("state") in {"PERSISTED_PENDING_MACHINE_VALIDATION", "QUALIFIED_FIRST_GOV04_BATCHED_POST_RG05E_AGGREGATE_NO_PRODUCTION_MIGRATION"}, "unexpected RG05F status state")

hard = status.get("hard_boundaries", {})
for key in [
    "production_source_modified",
    "legacy_source_modified",
    "frozen_testcase_modified",
    "canonical_tcd_register_modified",
    "evidence_strength_promoted",
    "scientific_review_performed",
    "new_scientific_admission_created",
    "composition_admitted",
    "b4_opened",
    "production_migration_opened",
]:
    expect(hard.get(key) is False, f"hard boundary {key} must remain false")

try:
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
except subprocess.CalledProcessError:
    fail("RG05E base is not an ancestor of HEAD")

changed = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], cwd=ROOT, text=True).splitlines()
changed_set = set(changed)
expect(changed_set == ALLOWED, f"scope guard expected exactly six RG05F files; got {sorted(changed_set)}")
for path in changed:
    lower = path.lower()
    expect(not lower.endswith((".for", ".f90", ".f", ".fortran")), f"production/legacy Fortran path modified: {path}")
    expect(not path.startswith("src/"), f"source path modified: {path}")
    expect("CANONICAL_TCD" not in path.upper(), f"canonical TCD register path modified: {path}")

if status.get("state") == "QUALIFIED_FIRST_GOV04_BATCHED_POST_RG05E_AGGREGATE_NO_PRODUCTION_MIGRATION":
    val = status.get("validation") or {}
    expect(status.get("work_status", {}).get("tested") is True, "qualified status must be tested")
    expect(status.get("work_status", {}).get("qualified") is True, "qualified status must mark qualified")
    expect(status.get("work_status", {}).get("work_unit_complete") is True, "qualified status must be complete")
    expect(val.get("conclusion") == "success", "qualified status must pin a successful validation run")
    expect(isinstance(val.get("github_actions_run_id"), int), "qualified status must pin validation run id")

print("PASS_RG05F_FIRST_GOV04_BATCHED_ADMISSION_INTEGRATION")
print("PASS_RG05F_SCOPE_GUARD")
