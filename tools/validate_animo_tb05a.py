#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / 'integration/animo-testbank/fragments/ANIMO-TB05A_MACROPORE_SUBSYSTEM_FRAGMENT.json'
STATUS = ROOT / 'integration/animo-testbank/ANIMO-TB05A_STATUS.json'
RECEIPT = ROOT / 'integration/animo-testbank/receipts/ANIMO-TB05A_QUALIFICATION_RECEIPT.json'
WORKFLOW = ROOT / '.github/workflows/animo-tb05a-macropore-subsystem.yml'


def load(path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def require(cond, msg):
    if not cond:
        raise SystemExit(f'ANIMO-TB05A validation FAIL: {msg}')


fragment = load(FRAGMENT)
status = load(STATUS)
receipt = load(RECEIPT)

require(fragment['producer_workunit'] == 'ANIMO-TB05A', 'wrong producer workunit')
require(fragment['base_authority'] == 'ANIMO-TB04B@82213ad143bd5f0fa5c500303a8a4f1d35dd3f0c', 'wrong TB04B base')
require(fragment['central_registry_write'] == 'FORBIDDEN_BY_FRAGMENT_PRODUCER', 'central registry write not forbidden')
require(fragment['registry_integration'] == 'SEPARATE_SERIAL_CONSOLIDATION_WORKUNIT_ONLY', 'registry integration not serial-only')
entries = fragment['entries']
ids = [e['test_id'] for e in entries]
require(ids == ['ATB-SUB-003','ATB-SUB-004','ATB-SUB-005','ATB-SUB-006','ATB-SUB-007'], 'unexpected bounded ID set')
require(len(ids) == len(set(ids)), 'duplicate test IDs')
required = {'test_id','layer','owner','status','source_identity','expected_value_provenance','comparison_policy','claim','failure_semantics','permanence'}
for e in entries:
    require(required.issubset(e), f'missing required field in {e.get("test_id")}')
    require(e['layer'] == 'TB-L7', f'wrong layer for {e["test_id"]}')
    if e['status'] == 'GAP':
        require(e['expected_value_provenance'] == 'UNKNOWN', f'gap provenance must be UNKNOWN for {e["test_id"]}')
        require(e['comparison_policy'] == 'NOT_YET_QUALIFIED', f'gap comparison policy must remain unqualified for {e["test_id"]}')

sub3 = next(e for e in entries if e['test_id'] == 'ATB-SUB-003')
require(sub3['applicability_pins']['configuration_gate'] == 'Ioptmp=1', 'activation gate drift')
require(sub3['applicability_pins']['hydrology_gate'] == 'Hlpimp=2', 'hydrology gate drift')
require(sub3['applicability_pins']['historical_reference_qualified'] is False, 'MP01 promoted to historical reference')
require(sub3['applicability_pins']['b3_ready'] is False, 'MP01 promoted to B3-ready')

sub4 = next(e for e in entries if e['test_id'] == 'ATB-SUB-004')
require(sub4['applicability_pins']['evidence_class'] == 'B1_COMPLETE_CASE_SYNTHETIC_DIAGNOSTIC_ONLY', 'MP02 evidence class widened')
require(sub4['applicability_pins']['historical_B2'] is False, 'MP02 promoted to historical B2')
require(sub4['applicability_pins']['behavioural_golden_reference'] is False, 'MP02 promoted to golden reference')

sub5 = next(e for e in entries if e['test_id'] == 'ATB-SUB-005')
require(sub5['applicability_pins']['whole_model_active_split'] is False, 'narrow restart promoted to whole-model split')
require(sub5['applicability_pins']['production_checkpoint_implementation'] is False, 'restart dependency promoted to production implementation')

sub6 = next(e for e in entries if e['test_id'] == 'ATB-SUB-006')
require(sub6['applicability_pins']['TCD025_correction_implemented'] is False, 'TCD-025 correction implemented')
require(sub6['applicability_pins']['TCD025_correction_admitted'] is False, 'TCD-025 correction admitted')

require(all(v is False for v in fragment['hard_boundaries'].values()), 'fragment hard boundary violated')
require(status['gov05_adversarial_self_review']['assurance'] == 'PROCESS_SELF_REVIEWED_NOT_INDEPENDENT', 'wrong GOV05 assurance')
require(all(v is False for v in status['hard_boundaries'].values()), 'status hard boundary violated')
require(status['existing_registry_handling'].startswith('ATB-SUB-001 is not modified'), 'existing SUB-001 handling missing')
require(receipt['work_unit'] == 'ANIMO-TB05A', 'wrong receipt workunit')
require(receipt['exact_head'] == 'ESTABLISHED_BY_EXACT_HEAD_CI', 'receipt exact-head sentinel missing')
require(receipt['scientific_admission'] is False, 'receipt implies admission')
require(receipt['registry_integration_performed'] is False, 'receipt implies registry integration')
require(WORKFLOW.exists(), 'workflow missing')

print('ANIMO-TB05A bounded macropore subsystem fragment validation: PASS')
