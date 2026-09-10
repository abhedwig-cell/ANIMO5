#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "integration" / "animo-reg"

RG05F = "7c61a5031f41d602e996310df6f3958cbd1b511e"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3D15 = "22e48f7e2c1eaa1245f034de2d909191d9cfa227"
B3D16 = "8650ea9e716336520d8d7df5f9ea2b393d17ab98"
B3D18 = "796c6f78ff863a2237e163d00cf4b5d15c04fc17"
B3I03 = "814ea660d367494432beb63ea78298d1f6cd73d7"
B3I04 = "400b7cd79f89043e091751707dfa96537587dcf6"
B3I05 = "7fa0162415e02a6f0167e71b48ae38177a9e06e0"
B3I06 = "8f01f0cb366dfa8cc63a184d6f885100899a8cd9"
EXPECTED_DECISION = "QUALIFIED_SECOND_GOV04_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05F_ADMISSIONS_NO_PRODUCTION"
EXPECTED_PRE = ["TCD-017", "TCD-018", "TCD-024", "TCD-026", "TCD-015", "TCD-027", "TCD-041"]
EXPECTED_NEW = ["TCD-030", "TCD-023", "TCD-028"]
EXPECTED_POST = EXPECTED_PRE + EXPECTED_NEW
ALLOWED = {
    ".github/workflows/animo-rg05g-second-gov04-batch.yml",
    "docs/governance/ANIMO_RG05G_SECOND_GOV04_BATCHED_ADMISSION_REGIE.md",
    "integration/animo-reg/ANIMO-RG05G_STATUS.json",
    "integration/animo-reg/RG05G_B3_ADMISSION_INVENTORY.json",
    "integration/animo-reg/RG05G_B3_QUEUE_DELTA.json",
    "tools/validate_rg05g_second_gov04_batch.py",
}


def req(cond, msg):
    if not cond:
        raise SystemExit("RG05G FAIL_CLOSED: " + msg)


def load_local(name):
    return json.loads((REG / name).read_text(encoding="utf-8"))


def git_show_json(ref, path):
    return json.loads(subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True))


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


inv = load_local("RG05G_B3_ADMISSION_INVENTORY.json")
delta = load_local("RG05G_B3_QUEUE_DELTA.json")
status = load_local("ANIMO-RG05G_STATUS.json")

# Aggregate lineage and governance policy.
req(inv["work_unit"] == "ANIMO-RG05G", "wrong inventory workunit")
req(inv["source_aggregate"]["head"] == RG05F, "source aggregate drift")
req(inv["source_aggregate"]["scientific_admissions"] == 7, "source aggregate count drift")
req(inv["source_aggregate"]["admitted_tcds"] == EXPECTED_PRE, "source aggregate admitted list drift")
req(inv["governance_authority"] == f"ANIMO-GOV04@{GOV04}", "GOV04 authority drift")
req(inv["historical_uncertainty_authority"] == f"ANIMO-GOV03@{GOV03}", "GOV03 authority drift")
req(subprocess.run(["git", "merge-base", "--is-ancestor", RG05F, "HEAD"]).returncode == 0, "RG05F is not ancestor")

rg05f = git_show_json(RG05F, "integration/animo-reg/RG05F_B3_ADMISSION_INVENTORY.json")
req(rg05f["admitted_tcds"] == EXPECTED_PRE, "live RG05F admitted list differs from pinned pre-state")
req(rg05f["counts"]["scientific_admissions"] == 7, "live RG05F count differs from pinned pre-state")

g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
central = g4["central_regie_integration"]
req(central["mode"] == "AGGREGATED_ATOMIC_ADMISSION_INTEGRATION", "GOV04 aggregate mode drift")
req(central["normal_batch_min"] == 3 and central["normal_batch_max"] == 5, "GOV04 normal batch cadence drift")
req(inv["batch_policy"]["new_admissions_in_this_batch"] == 3, "batch is not exactly three admissions")
req(inv["batch_policy"]["normal_threshold_reached"] is True, "normal batch threshold not reached")
req(inv["batch_policy"]["early_batch"] is False, "RG05G incorrectly marked early batch")

# Three lateral atomic admission authorities are consumed exactly at their recorded strength.
a15 = git_show_json(B3D15, "integration/animo-b3/TCD030_B3_ADMISSION_CLOSEOUT.json")
a16 = git_show_json(B3D16, "integration/animo-b3/TCD023_B3_ADMISSION_CLOSEOUT.json")
a18 = git_show_json(B3D18, "integration/animo-b3/TCD028_B3_ADMISSION_CLOSEOUT.json")
s18 = git_show_json(B3D18, "integration/animo-b3/ANIMO-B3D18_STATUS.json")

req(a15["target"] == "TCD-030" and a15["admitted"] is True, "TCD-030 admission authority invalid")
req(a15["risk"]["tier"] == "B", "TCD-030 risk tier drift")
req(a15["historical_uncertainty"]["route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "TCD-030 route drift")
req(a15["historical_uncertainty"]["historical_fidelity_claimed"] is False, "TCD-030 fidelity overclaimed")

req(a16["target"] == "TCD-023" and a16["admitted"] is True, "TCD-023 admission authority invalid")
req(a16["risk"]["tier"] == "B", "TCD-023 risk tier drift")
req(a16["historical_uncertainty"]["route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "TCD-023 route drift")
req(a16["historical_uncertainty"]["historical_fidelity_claimed"] is False, "TCD-023 fidelity overclaimed")

req(a18["target"] == "TCD-028" and a18["admitted"] is True, "TCD-028 admission authority invalid")
req(a18["gov04_risk_tier"] == "C", "TCD-028 Tier-C authority drift")
req(a18["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "TCD-028 B3 class drift")
req(a18["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "TCD-028 route drift")
req(a18["historical_uncertainty"]["historical_revision53_manifestation"] == "UNKNOWN_WITHOUT_B2", "TCD-028 historical uncertainty drift")
req(a18["historical_uncertainty"]["historical_fidelity_claimed"] is False, "TCD-028 fidelity overclaimed")
req(s18["validation"]["machine_validated"] is True and s18["validation"]["conclusion"] == "success", "B3D18 final admission status not green")
req(s18["validation"]["validator"] == "PASS" and s18["validation"]["scope_guard"] == "PASS", "B3D18 final gates not PASS")

new = inv["new_admissions"]
req([x["tcd"] for x in new] == EXPECTED_NEW, "new admission order/identity drift")
req([x["admission_authority"] for x in new] == [f"ANIMO-B3D15@{B3D15}", f"ANIMO-B3D16@{B3D16}", f"ANIMO-B3D18@{B3D18}"], "new admission authority pins drift")
req(inv["admitted_tcds"] == EXPECTED_POST, "post-aggregate admitted list drift")
req(inv["counts"] == {
    "scientific_admissions": 10,
    "atomic_admissions": 10,
    "historical_uncertainty_admissions": 10,
    "normal_b2_route_admissions": 0,
    "b4_admissions": 0,
    "production_migrations": 0,
}, "aggregate admission counts drift")

# Do not fabricate a stale global queue count after later routing work.
req(delta["admission_counts"] == {
    "pre_delta_scientific_admissions": 7,
    "new_atomic_admissions": 3,
    "post_delta_scientific_admissions": 10,
}, "admission-count delta drift")
qc = delta["canonical_queue_cardinality"]
req(qc["global_canonical_queue_count_recomputed"] is False, "RG05G fabricated a global queue count")
req(qc["canonical_register_or_routing_files_modified_here"] is False, "RG05G claims routing/register mutation")
req(qc["observed_later_routing_authorities"] == [
    f"ANIMO-B3I03@{B3I03}", f"ANIMO-B3I04@{B3I04}", f"ANIMO-B3I05@{B3I05}", f"ANIMO-B3I06@{B3I06}"
], "routing authority observation drift")
req(qc["observed_canonical_tail"] == "TCD-042", "observed canonical tail drift")
for sha in (B3I03, B3I04, B3I05, B3I06):
    req(subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0, f"routing authority {sha} unavailable")
# B3I06 explicitly carries no new TCD or register append; use it as latest observed no-append sentinel.
i06 = git_show_json(B3I06, "integration/animo-b3/ANIMO-B3I06_STATUS.json")
req(i06["intake"]["new_top_level_tcd_count"] == 0, "B3I06 unexpectedly adds a top-level TCD")
req(i06["intake"]["canonical_register_append_performed"] is False, "B3I06 unexpectedly changes canonical register")
req(i06["canonical_authority"]["canonical_tail"] == "TCD-042", "B3I06 canonical tail drift")

# Aggregate boundaries and status.
req(inv["project_boundary"]["B3_complete"] is False, "RG05G overclaims B3 completion")
req(inv["project_boundary"]["B4_open"] is False and inv["project_boundary"]["production_open"] is False, "B4/production opened")
req(inv["project_boundary"]["canonical_tcd_register_modified"] is False, "canonical register modified")
req(inv["project_boundary"]["routing_register_modified"] is False, "routing register modified")
req(inv["project_boundary"]["composition_admitted"] is False, "composition admitted")

req(status["decision"] == EXPECTED_DECISION, "status decision drift")
req(status["source_aggregate"] == f"ANIMO-RG05F@{RG05F}", "status source aggregate drift")
req(status["new_atomic_admissions"] == [
    f"ANIMO-B3D15@{B3D15}:TCD-030",
    f"ANIMO-B3D16@{B3D16}:TCD-023",
    f"ANIMO-B3D18@{B3D18}:TCD-028",
], "status admission pins drift")
req(status["scientific_admission_count"] == 10 and status["historical_uncertainty_admission_count"] == 10, "status counts drift")
req(status["b3_complete"] is False and status["b4_open"] is False and status["production_open"] is False, "status opens downstream scope")
req(status["global_canonical_queue_count_recomputed"] is False, "status fabricates global queue count")
for key, value in status["hard_boundaries"].items():
    req(value is False, f"forbidden aggregate side effect recorded: {key}")
if status["validation"]["machine_validated"]:
    req(status["validation"]["conclusion"] == "success", "validated status lacks success")
    req(status["validation"]["validator"] == "PASS" and status["validation"]["scope_guard"] == "PASS", "validated status lacks PASS gates")
    req(isinstance(status["validation"]["run_id"], int) and isinstance(status["validation"]["job_id"], int), "validated status lacks CI ids")

# Exact governance-only scope from immutable RG05F aggregate base.
changed = subprocess.check_output(["git", "diff", "--name-only", f"{RG05F}...HEAD"], text=True).splitlines()
req(set(changed) == ALLOWED, "scope differs from exact six-file RG05G governance package: " + repr(sorted(changed)))
for path in changed:
    req(not path.startswith(("src/", "production/", "reference/", "ANIMO_4.1.5.53/")), "protected source/B0 path changed: " + path)
req("docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" not in changed, "canonical TCD register changed")

print("RG05G PASS: exactly three post-RG05F atomic B3 admissions are aggregated; admission count is 10; B3/B4/production remain closed and no stale global queue count is fabricated.")
