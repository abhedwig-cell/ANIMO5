#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / 'integration/animo-testbank/fragments/ANIMO-TB04B_BOUNDARY_INITIALIZATION_FRAGMENT.json'
STATUS = ROOT / 'integration/animo-testbank/ANIMO-TB04B_STATUS.json'
RECEIPT = ROOT / 'integration/animo-testbank/receipts/ANIMO-TB04B_QUALIFICATION_RECEIPT.json'
WORKFLOW = ROOT / '.github/workflows/animo-tb04b-boundary-initialization.yml'


def load(path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def require(cond, msg):
    if not cond:
        raise SystemExit(f'ANIMO-TB04B validation FAIL: {msg}')


fragment = load(FRAGMENT)
status = load(STATUS)
receipt = load(RECEIPT)

require(fragment['producer_workunit'] == 'ANIMO-TB04B', 'wrong producer workunit')
require(fragment['central_registry_write'] == 'FORBIDDEN_BY_FRAGMENT_PRODUCER', 'central registry write not forbidden')
require(fragment['registry_integration'] == 'SEPARATE_SERIAL_CONSOLIDATION_WORKUNIT_ONLY', 'registry integration not serial-only')
require(fragment['base_authority'] == 'ANIMO-TB04A@ad9683716e1a41a6f6b3d32ff1012bfa215c27db', 'wrong TB04A base')

entries = fragment['entries']
ids = [e['test_id'] for e in entries]
require(len(ids) == len(set(ids)), 'duplicate test IDs')
require(ids == ['ATB-BND-002','ATB-BND-003','ATB-BND-004','ATB-BND-005','ATB-BND-006'], 'unexpected bounded ID set')
required = {'test_id','layer','owner','status','source_identity','expected_value_provenance','comparison_policy','claim','failure_semantics','permanence'}
for e in entries:
    require(required.issubset(e), f'missing required field in {e.get("test_id")}')
    require(e['layer'] == 'TB-L6', f'wrong layer for {e["test_id"]}')
    if e['status'] == 'GAP':
        require(e['expected_value_provenance'] == 'UNKNOWN', f'gap provenance must be UNKNOWN for {e["test_id"]}')
        require(e['comparison_policy'] == 'NOT_YET_QUALIFIED', f'gap comparison policy must remain unqualified for {e["test_id"]}')

b2 = next(e for e in entries if e['test_id'] == 'ATB-BND-002')
require(b2['applicability_pins']['flux_domain'] == 'Flux=0 EXACTLY', 'BND-002 widened beyond exact zero')
require(b2['applicability_pins']['Hetop_domain'] == 'Hetop>0', 'BND-002 HETOP domain widened')
require(b2['applicability_pins']['finite_positive_subthreshold_included'] is False, 'BND-002 silently includes subthreshold flux')

b3 = next(e for e in entries if e['test_id'] == 'ATB-BND-003')
require(b3['applicability_pins']['numerical_policy_selected'] is False, 'subthreshold numerical policy selected')
require(b3['applicability_pins']['tolerance_admitted'] is False, 'subthreshold tolerance admitted')

b4 = next(e for e in entries if e['test_id'] == 'ATB-BND-004')
require(b4['applicability_pins']['zero_thickness_policy_selected'] is False, 'HETOP=0 policy selected')
require(b4['applicability_pins']['global_semantics_unique'] is False, 'HETOP=0 semantic nonuniqueness erased')

b5 = next(e for e in entries if e['test_id'] == 'ATB-BND-005')
require(b5['applicability_pins']['qualified_boundary_value'] == 0.0, 'GHG lower boundary is not exact zero')
require(b5['applicability_pins']['production_patch_admitted'] is False, 'BUILDQ04 contract promoted to production patch')
require(b5['applicability_pins']['b3_scientific_admitted'] is False, 'BUILDQ04 contract promoted to admission')

require(all(v is False for v in fragment['hard_boundaries'].values()), 'fragment hard boundary violated')
require(status['gov05_adversarial_self_review']['assurance'] == 'PROCESS_SELF_REVIEWED_NOT_INDEPENDENT', 'wrong GOV05 assurance')
require(all(v is False for v in status['hard_boundaries'].values()), 'status hard boundary violated')
require(status['existing_registry_handling'].startswith('ATB-BND-001 is not modified'), 'existing BND-001 handling missing')
require(receipt['work_unit'] == 'ANIMO-TB04B', 'wrong receipt workunit')
require(receipt['exact_head'] == 'ESTABLISHED_BY_EXACT_HEAD_CI', 'receipt exact-head sentinel missing')
require(receipt['scientific_admission'] is False, 'receipt implies admission')
require(receipt['registry_integration_performed'] is False, 'receipt implies central registry integration')
require(WORKFLOW.exists(), 'workflow missing')

print('ANIMO-TB04B bounded boundary and initialization fragment validation: PASS')
