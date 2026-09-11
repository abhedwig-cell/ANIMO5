#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "integration/animo-testbank/fragments/ANIMO-TB03B_FRAGMENT.json"
registry_path = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
status_path = ROOT / "integration/animo-testbank/ANIMO-TB03B_STATUS.json"

m = json.loads(manifest_path.read_text())
r = json.loads(registry_path.read_text())
s = json.loads(status_path.read_text())

assert m["fragment_id"] == "ANIMO-TB03B"
assert m["base_authority"] == "ANIMO-TB02@54a565c2f7f2a29817ae027cc18bee1613ce568d"
assert m["supporting_authorities"]["MASSQ02"] == "ANIMO-MASSQ02@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc"
assert "scientific residual tolerance" in m["excluded"]
assert m["sign_contract"]["amount_rule"].startswith("q >= 0")
assert "cannot convert a non-zero physical residual" in m["sign_contract"]["tolerance_policy"]

required = {
    "test_id", "layer", "owner", "status", "source_identity",
    "expected_value_provenance", "comparison_policy", "element", "species",
    "storage", "inputs", "outputs", "internal_transfers", "boundary_signs",
    "residual_equation", "assertions", "dependencies", "qualification_strength"
}
entries = m["entries"]
ids = [e["test_id"] for e in entries]
assert len(ids) == len(set(ids)), "fragment test-id collision"
assert all(e["status"] == "QUALIFIED_FRAGMENT_ENTRY" for e in entries)
for e in entries:
    missing = required - set(e)
    assert not missing, f"{e.get('test_id')} missing {sorted(missing)}"
    assert e["element"]
    assert e["species"]
    assert e["residual_equation"]
    assert e["boundary_signs"]

central_ids = {e["test_id"] for e in r.get("test_registry", [])}
fragment_ids = set(ids)
assert not (central_ids & fragment_ids), "TB03B must not duplicate a central-registry test id"
for e in entries:
    for dep in e["dependencies"]:
        assert dep in central_ids or dep in fragment_ids, f"unresolved dependency {dep}"

# Exact algebraic contract checks. These are identities, not empirical tolerances.
for q in (0, 1, 7, 1000000):
    assert (-q) + q == 0

# Local layer residual example: storage and signed boundary/interface terms.
S0, ext_in, int_in, internal_net, ext_out, int_out = 10, 3, 2, 0, 4, 1
S1 = S0 + ext_in + int_in + internal_net - ext_out - int_out
R_layer = S0 + ext_in + int_in + internal_net - ext_out - int_out - S1
assert R_layer == 0

# Whole profile: internal interfaces cancel from the combined profile equation.
S0_profile, external_in, external_out = 20, 5, 8
S1_profile = S0_profile + external_in - external_out
R_profile = S0_profile + external_in - external_out - S1_profile
assert R_profile == 0

# Species preservation: nitrification moves N internally without changing total N.
nh4_delta, no3_delta = -6, 6
assert nh4_delta + no3_delta == 0
assert nh4_delta != 0 and no3_delta != 0

assert s["work_unit"] == "ANIMO-TB03B"
assert s["gov05_adversarial_self_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
assert s["qualification"]["exact_final_head_ci_required"] is True
assert s["hard_boundaries"]["central_registry_modified"] is False
assert s["hard_boundaries"]["production_source_modified"] is False
print("ANIMO-TB03B bounded transaction/conservation fragment validation: PASS")
