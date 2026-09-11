#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
contract_path = ROOT / "integration/animo-testbank/ANIMO-TB02_RUNNER_CONTRACT.json"
status_path = ROOT / "integration/animo-testbank/ANIMO-TB02_STATUS.json"
workflow_path = ROOT / ".github/workflows/animo-tb02-testbank-infrastructure.yml"

c = json.loads(contract_path.read_text())
assert c["work_unit"] == "ANIMO-TB02"
assert c["base"].startswith("ANIMO-TB01@")
assert c["fragment_contract"]["central_registry_write"] == "FORBIDDEN_BY_FRAGMENT_PRODUCER"
assert c["fragment_contract"]["id_collision_policy"] == "FAIL_CLOSED"
assert c["runner_contract"]["missing_dependency"] == "FAIL_CLOSED"
assert c["runner_contract"]["runner_may_create_scientific_expected_values"] is False
assert c["runner_contract"]["runner_may_promote_empirical_tolerance"] is False
assert c["runner_contract"]["runner_may_create_whole_model_golden_baseline"] is False
assert c["receipt_contract"]["receipt_is_not_scientific_admission"] is True
assert all(v is False for v in c["hard_boundaries"].values())
assert status_path.exists()
s = json.loads(status_path.read_text())
assert s["work_unit"] == "ANIMO-TB02"
assert s["gov05_adversarial_self_review"]["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
assert s["qualification"]["exact_final_head_ci_required"] is True
assert workflow_path.exists()
print("ANIMO-TB02 infrastructure contract validation: PASS")
