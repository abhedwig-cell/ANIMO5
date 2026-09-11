#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "integration/animo-testbank/fragments/ANIMO-TB03C_CONVERGENCE_HANDOFF.json"
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
TB02 = ROOT / "integration/animo-testbank/ANIMO-TB02_RUNNER_CONTRACT.json"

A_HEAD = "a37f07b15ae50d6fbb526cef3215fb58702e85aa"
B_HEAD = "48a3036501e9e871608ab920f46dde5570ebf369"
A_PATH = "integration/animo-testbank/fragments/ANIMO-TB03A_CNP_SPECIES_ORACLE_FRAGMENT.json"
B_PATH = "integration/animo-testbank/fragments/ANIMO-TB03B_FRAGMENT.json"
B_STATUS_PATH = "integration/animo-testbank/ANIMO-TB03B_STATUS.json"
REGISTRY_PATH = "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"


def git_text(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True)


def git_json(commit, path):
    return json.loads(git_text(commit, path))


def git_blob(commit, path):
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


handoff = json.loads(HANDOFF.read_text())
registry = json.loads(REGISTRY.read_text())
tb02 = json.loads(TB02.read_text())
a = git_json(A_HEAD, A_PATH)
b = git_json(B_HEAD, B_PATH)
b_status = git_json(B_HEAD, B_STATUS_PATH)

assert handoff["schema_version"] == "1.0"
assert handoff["fragment_id"] == "ANIMO-TB03C-TB3-FRAGMENT-CONVERGENCE-HANDOFF-v1"
assert handoff["producer_workunit"] == "ANIMO-TB03C"
assert handoff["base_authority"] == "ANIMO-TB02@54a565c2f7f2a29817ae027cc18bee1613ce568d:CI_34557165449_SUCCESS"
assert handoff["entries"] == [], "TB03C must not create scientific test entries"
assert tb02["fragment_contract"]["central_registry_write"] == "FORBIDDEN_BY_FRAGMENT_PRODUCER"
assert tb02["fragment_contract"]["registry_integration"] == "SEPARATE_SERIAL_CONSOLIDATION_WORKUNIT_ONLY"
assert handoff["central_registry_baseline"]["write_policy"] == "FORBIDDEN_IN_TB03C"
assert handoff["central_registry_baseline"]["future_write_owner"] == "SEPARATE_SERIAL_CONSOLIDATION_WORKUNIT_ONLY"

source_by_workunit = {x["work_unit"]: x for x in handoff["source_fragments"]}
assert set(source_by_workunit) == {"ANIMO-TB03A", "ANIMO-TB03B"}
sa = source_by_workunit["ANIMO-TB03A"]
sb = source_by_workunit["ANIMO-TB03B"]
assert sa["exact_head"] == A_HEAD
assert sb["exact_head"] == B_HEAD
assert sa["exact_head_ci_run"] == 34557800712 and sa["exact_head_ci_conclusion"] == "success"
assert sb["exact_head_ci_run"] == 34557679150 and sb["exact_head_ci_conclusion"] == "success"
assert git_blob(A_HEAD, A_PATH) == sa["git_blob_sha1"] == "aa11d224964bdc5f1d529d823f774afc18994bbd"
assert git_blob(B_HEAD, B_PATH) == sb["git_blob_sha1"] == "4b1f1a0ef11a02a76dbb33f9168dbb1f552ade7e"
assert git_blob("HEAD", REGISTRY_PATH) == handoff["central_registry_baseline"]["git_blob_sha1"] == "a5f279cfa334dc63d3e4e8759370279736d874a0"

assert a["producer_workunit"] == "ANIMO-TB03A"
assert a["package_state_rule"].startswith("QUALIFIED_ANIMO_TB03A_BOUNDED_FRAGMENT_PACKAGE")
assert a["qualification"]["exact_final_head_ci_required"] is True
assert a["qualification"]["receipt_is_not_scientific_admission"] is True
assert b["producer_workunit"] == "ANIMO-TB03B"
assert b_status["state"] == "QUALIFIED_TB03B_BOUNDED_TRANSACTION_AND_CONSERVATION_FRAGMENT_PACKAGE"
assert b_status["work_status"]["qualified"] is True
assert b_status["work_status"]["work_unit_complete"] is True
assert b_status["qualification"]["exact_final_head_ci_required"] is True

central_ids = {x["test_id"] for x in registry["test_registry"]}
a_entries = {x["test_id"]: x for x in a["entries"]}
b_entries = {x["test_id"]: x for x in b["entries"]}
a_ids = set(a_entries)
b_ids = set(b_entries)
assert len(a_ids) == len(a["entries"])
assert len(b_ids) == len(b["entries"])
assert not (a_ids & b_ids), f"cross-fragment ID collision: {sorted(a_ids & b_ids)}"
assert not (a_ids & central_ids), f"TB03A collision with central registry: {sorted(a_ids & central_ids)}"
assert not (b_ids & central_ids), f"TB03B collision with central registry: {sorted(b_ids & central_ids)}"

expected_a_qualified = {"ATB-ORACLE-002", "ATB-ORACLE-003", "ATB-SPC-003"}
expected_a_candidate = {"ATB-SPC-004", "ATB-SPC-005", "ATB-SPC-006"}
expected_a_gap = {"ATB-SPC-007"}
expected_b_qualified = {"ATB-TRN-002", "ATB-CONS-002", "ATB-CONS-003", "ATB-CONS-004", "ATB-CONS-005"}

assert {k for k, v in a_entries.items() if v["status"] == "QUALIFIED_FRAGMENT_ENTRY"} == expected_a_qualified
assert {k for k, v in a_entries.items() if v["status"] == "CANDIDATE"} == expected_a_candidate
assert {k for k, v in a_entries.items() if v["status"] == "GAP"} == expected_a_gap
assert set(b_entries) == expected_b_qualified
assert all(v["status"] == "QUALIFIED_FRAGMENT_ENTRY" for v in b_entries.values())
assert set(sa["qualified_entry_ids"]) == expected_a_qualified
assert set(sa["status_preserved_nonqualified_entry_ids"]) == expected_a_candidate | expected_a_gap
assert set(sb["qualified_entry_ids"]) == expected_b_qualified
assert sb["status_preserved_nonqualified_entry_ids"] == []

union_ids = central_ids | a_ids | b_ids
for origin, entries in (("TB03A", a_entries), ("TB03B", b_entries)):
    for test_id, entry in entries.items():
        missing = [d for d in entry.get("dependencies", []) if d not in union_ids]
        assert not missing, f"{origin} {test_id} missing dependencies: {missing}"

# No sibling fragment currently relies on the other sibling. This keeps the convergence
# mechanically additive and prevents an accidental hidden qualification dependency.
assert not any(d in b_ids for e in a_entries.values() for d in e.get("dependencies", []))
assert not any(d in a_ids for e in b_entries.values() for d in e.get("dependencies", []))

qualified_handoff = expected_a_qualified | expected_b_qualified
preserved_nonqualified = expected_a_candidate | expected_a_gap
assert set(handoff["convergence_result"]["qualified_handoff_entry_ids"]) == qualified_handoff
assert set(handoff["convergence_result"]["status_preserved_nonqualified_entry_ids"]) == preserved_nonqualified
assert handoff["convergence_result"]["new_test_ids_created_by_tb03c"] == []
assert handoff["convergence_result"]["inter_fragment_id_collision"] is False
assert handoff["convergence_result"]["central_registry_id_collision"] is False
assert handoff["convergence_result"]["dependency_closure"] == "PASS_AGAINST_CENTRAL_REGISTRY_PLUS_BOUNDED_FRAGMENT_IDS"
assert handoff["convergence_result"]["cross_fragment_dependency_required"] is False
assert handoff["convergence_result"]["central_registry_modified"] is False

# Adversarial semantic guard: TB03B's elemental-N aggregation contract does not close
# TB03A's still-missing executable NH4/NO3 ownership adapter.
spc004 = a_entries["ATB-SPC-004"]
cons004 = b_entries["ATB-CONS-004"]
assert spc004["status"] == "CANDIDATE"
assert "executable" in spc004["permanence_blocker"].lower()
assert cons004["status"] == "QUALIFIED_FRAGMENT_ENTRY"
assert cons004["species"] == "NH4-N and NO3-N separate"
assert "species-resolved ledgers" in cons004["residual_equation"]
assert handoff["semantic_reconciliation"]["nh4_no3"]["decision"].startswith("NO_CONTRADICTION_AND_NO_AUTOMATIC_PROMOTION")

assert handoff["gov05_adversarial_self_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
assert handoff["gov05_adversarial_self_review"]["result"] == "PASS_BOUNDED_CONVERGENCE_READINESS_SCOPE"
assert all(v is False for v in handoff["hard_boundaries"].values())
assert handoff["qualification"]["exact_final_head_ci_required"] is True
assert handoff["qualification"]["receipt_is_not_scientific_admission"] is True
assert handoff["qualification"]["qualified_state_after_success"] == "QUALIFIED_ANIMO_TB03C_FRAGMENT_CONVERGENCE_HANDOFF_READY_FOR_SEPARATE_SERIAL_REGISTRY_CONSOLIDATION"

print("ANIMO-TB03C fragment convergence readiness validation: PASS")
print(f"central={len(central_ids)} tb03a={len(a_ids)} tb03b={len(b_ids)} qualified_handoff={len(qualified_handoff)} preserved_nonqualified={len(preserved_nonqualified)}")
