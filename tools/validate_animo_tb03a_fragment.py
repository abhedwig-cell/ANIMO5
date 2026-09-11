#!/usr/bin/env python3
import json
import re
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / "integration/animo-testbank/fragments/ANIMO-TB03A_CNP_SPECIES_ORACLE_FRAGMENT.json"
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
TB02_CONTRACT = ROOT / "integration/animo-testbank/ANIMO-TB02_RUNNER_CONTRACT.json"

f = json.loads(FRAGMENT.read_text())
r = json.loads(REGISTRY.read_text())
tb02 = json.loads(TB02_CONTRACT.read_text())

assert f["schema_version"] == "1.0"
assert f["fragment_id"] == "ANIMO-TB03A-CNP-SPECIES-ORACLE-FRAGMENT-v1"
assert f["producer_workunit"] == "ANIMO-TB03A"
assert f["base_authority"] == "ANIMO-TB02@54a565c2f7f2a29817ae027cc18bee1613ce568d:CI_34557165449_SUCCESS"
assert f["tb01_authority"] == "ANIMO-TB01@15a17bfa2c321d08f3ac89f334986c0ae8429045"
assert f["gov05_authority"] == "ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
assert f["synq01_authority"] == "ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121"
assert f["central_registry_write"] == "FORBIDDEN_BY_FRAGMENT_PRODUCER"
assert f["registry_integration"] == "SEPARATE_SERIAL_CONSOLIDATION_WORKUNIT_ONLY"
assert f["gov05_adversarial_self_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
assert f["gov05_adversarial_self_review"]["result"] == "PASS_BOUNDED_TB03A_FRAGMENT_SCOPE"
assert all(v is False for v in f["hard_boundaries"].values())
assert f["qualification"]["exact_final_head_ci_required"] is True
assert f["qualification"]["receipt_is_not_scientific_admission"] is True

required = set(tb02["fragment_contract"]["required_fields"])
assert required.issubset(f)
entry_required = set(tb02["fragment_contract"]["entry_required_fields"])
allowed_status = set(tb02["fragment_contract"]["allowed_status"])
comparison_policies = set(r["controlled_vocabularies"]["comparison_policy"])
id_pattern = re.compile(r["id_scheme"]["pattern"])
central_ids = {x["test_id"] for x in r["test_registry"]}
fragment_ids = [x["test_id"] for x in f["entries"]]
assert len(fragment_ids) == len(set(fragment_ids))
assert not (set(fragment_ids) & central_ids), "TB03A fragment collides with central registry"

all_dependency_ids = central_ids | set(fragment_ids)
for entry in f["entries"]:
    assert entry_required.issubset(entry)
    assert id_pattern.fullmatch(entry["test_id"])
    assert entry["status"] in allowed_status
    assert entry["expected_value_provenance"] != "UNKNOWN"
    assert entry["comparison_policy"] in comparison_policies
    assert entry.get("admission_effect") == "NONE"
    assert all(dep in all_dependency_ids for dep in entry.get("dependencies", []))
    if entry["status"] == "QUALIFIED_FRAGMENT_ENTRY":
        p = entry["permanence_review"]
        assert len(p) == 10 and all(p.values()), entry["test_id"]
        assert entry["cost_class"] in r["legacy_taxonomy"]["cost_classes"]
        assert entry["execution_profile"]
    elif entry["status"] == "CANDIDATE":
        assert entry.get("permanence_blocker")
    elif entry["status"] == "GAP":
        assert entry.get("gap_reason")

assert set(f["qualification"]["qualified_entry_ids"]) == {
    "ATB-ORACLE-002", "ATB-ORACLE-003", "ATB-SPC-003"
}
assert set(f["qualification"]["candidate_entry_ids"]) == {
    "ATB-SPC-004", "ATB-SPC-005", "ATB-SPC-006"
}
assert set(f["qualification"]["gap_entry_ids"]) == {"ATB-SPC-007"}

by_id = {x["test_id"]: x for x in f["entries"]}
assert "SYNQ-O004" in by_id["ATB-ORACLE-002"]["source_identity"]
assert "SYNQ-O005" in by_id["ATB-ORACLE-003"]["source_identity"]
assert "5ce33964c2b3d93ee7038984f1e22c12668fb7f8" in by_id["ATB-SPC-003"]["source_identity"]
assert "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566" in by_id["ATB-SPC-003"]["source_identity"]

# Independently re-evaluate the bounded SYNQ-O004 analytical relation.
m, k, h, a = D("0.35"), D("0.08"), D("0.2"), D("0.3")
def partition(c):
    parent = m * k * D(c) * h
    return parent, (D(1) - a) * parent, a * parent
expected = by_id["ATB-ORACLE-002"]["expected_relation"]
for species, c in (("C", "2.0"), ("N", "0.2"), ("P", "0.05")):
    got = partition(c)
    declared = tuple(D(x) for x in expected[f"{species}_parent_d19_d20"])
    assert got == declared
    assert got[1] + got[2] == got[0]

# Independently re-evaluate the bounded SYNQ-O005 permutation relation.
concentrations = (D("2.0"), D("0.2"), D("0.05"))
order = (2, 0, 1)
base = tuple(partition(x) for x in concentrations)
permuted_input = tuple(concentrations[i] for i in order)
permuted_output = tuple(partition(x) for x in permuted_input)
assert permuted_output == tuple(base[i] for i in order)

# Explicit non-generalization guards.
assert by_id["ATB-SPC-004"]["status"] == "CANDIDATE"
assert by_id["ATB-SPC-005"]["status"] == "CANDIDATE"
assert by_id["ATB-SPC-006"]["status"] == "CANDIDATE"
assert by_id["ATB-SPC-007"]["status"] == "GAP"
assert "no universal C/N/P ratio is inferred by this fragment" in by_id["ATB-SPC-006"]["scientific_claims"]
assert "full reaction-wide species ownership is not qualified by the three promoted TB03A entries" in by_id["ATB-SPC-007"]["scientific_claims"]

print("ANIMO-TB03A bounded fragment validation: PASS")
