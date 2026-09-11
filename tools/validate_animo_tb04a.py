#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
frag = json.loads((ROOT / 'integration/animo-testbank/fragments/ANIMO-TB04A_STATE_RESTART_FRAGMENT.json').read_text())
status = json.loads((ROOT / 'integration/animo-testbank/ANIMO-TB04A_STATUS.json').read_text())

assert frag['schema_version'] == '1.0'
assert frag['fragment_id'] == 'ANIMO-TB04A-STATE-RESTART'
assert frag['producer_workunit'] == 'ANIMO-TB04A'
assert frag['base_authority'] == 'ANIMO-TB02@54a565c2f7f2a29817ae027cc18bee1613ce568d'
assert frag['central_registry_write'] == 'FORBIDDEN_BY_FRAGMENT_PRODUCER'
assert frag['registry_integration'] == 'SEPARATE_SERIAL_CONSOLIDATION_WORKUNIT_ONLY'

entries = frag['entries']
ids = [e['test_id'] for e in entries]
assert len(ids) == len(set(ids))
assert ids == ['ATB-STATE-003','ATB-STATE-004','ATB-STATE-005','ATB-STATE-006','ATB-STATE-007']
for e in entries:
    for field in ['test_id','layer','owner','status','source_identity','expected_value_provenance','comparison_policy','claim','applicability_pins','failure_semantics','permanence']:
        assert field in e
    assert e['layer'] == 'TB-L5'
    assert e['status'] in {'QUALIFIED_FRAGMENT_ENTRY','GAP'}

byid = {e['test_id']: e for e in entries}
assert byid['ATB-STATE-003']['applicability_pins']['legacy_Output_Init_purity_claim'] is False
assert byid['ATB-STATE-004']['applicability_pins']['whole_model_state_claim'] is False
assert byid['ATB-STATE-004']['comparison_policy'] == 'EXACT_BITWISE_NO_TOLERANCE'
assert byid['ATB-STATE-005']['applicability_pins']['canonical_time_admission'] is False
assert byid['ATB-STATE-006']['applicability_pins']['whole_model_active_split'] is False
assert byid['ATB-STATE-006']['applicability_pins']['canonical_state_admission'] is False
assert byid['ATB-STATE-007']['status'] == 'GAP'
assert byid['ATB-STATE-007']['expected_value_provenance'] == 'UNKNOWN'

assert all(v is False for v in frag['hard_boundaries'].values())
assert status['work_unit'] == 'ANIMO-TB04A'
assert status['gov05_adversarial_self_review']['assurance'] == 'PROCESS_SELF_REVIEWED_NOT_INDEPENDENT'
assert status['qualification']['exact_final_head_ci_required'] is True
assert all(v is False for v in status['hard_boundaries'].values())
print('ANIMO-TB04A bounded state/restart fragment validation: PASS')
