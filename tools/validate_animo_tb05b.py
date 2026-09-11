#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
F = ROOT/'integration/animo-testbank/fragments/ANIMO-TB05B_GHG_SUBSYSTEM_FRAGMENT.json'
S = ROOT/'integration/animo-testbank/ANIMO-TB05B_STATUS.json'
R = ROOT/'integration/animo-testbank/receipts/ANIMO-TB05B_QUALIFICATION_RECEIPT.json'
W = ROOT/'.github/workflows/animo-tb05b-ghg-subsystem.yml'
def load(p):
    with p.open(encoding='utf-8') as f: return json.load(f)
def req(c,m):
    if not c: raise SystemExit('ANIMO-TB05B validation FAIL: '+m)
f,s,r=load(F),load(S),load(R)
req(f['producer_workunit']=='ANIMO-TB05B','producer')
req(f['base_authority']=='ANIMO-TB05A@e3d537935104b4a7253a5287f8fbf7df7e7459e2','base')
req(f['central_registry_write']=='FORBIDDEN_BY_FRAGMENT_PRODUCER','registry write')
ids=[e['test_id'] for e in f['entries']]
req(ids==['ATB-SUB-008','ATB-SUB-009','ATB-SUB-010','ATB-SUB-011','ATB-SUB-012'],'IDs')
req(len(ids)==len(set(ids)),'duplicate IDs')
required={'test_id','layer','owner','status','source_identity','expected_value_provenance','comparison_policy','claim','failure_semantics','permanence'}
for e in f['entries']:
    req(required.issubset(e), 'fields '+e.get('test_id','?'))
    req(e['layer']=='TB-L7','layer '+e['test_id'])
    if e['status']=='GAP':
        req(e['expected_value_provenance']=='UNKNOWN','gap provenance')
        req(e['comparison_policy']=='NOT_YET_QUALIFIED','gap policy')
e8=next(e for e in f['entries'] if e['test_id']=='ATB-SUB-008')
req(e8['applicability_pins']['supplied_historical_case_reaches_GHG_branch'] is False,'historical reachability overclaim')
req(e8['applicability_pins']['b3_admitted'] is False,'B3 overclaim')
e9=next(e for e in f['entries'] if e['test_id']=='ATB-SUB-009')
req(e9['applicability_pins']['parent_atomic'] is False,'parent atomized silently')
req(e9['applicability_pins']['parent_atomization_required'] is True,'atomization requirement lost')
req(e9['applicability_pins']['scientific_admission'] is False,'runtime semantics promoted to admission')
e10=next(e for e in f['entries'] if e['test_id']=='ATB-SUB-010')
req(e10['applicability_pins']['boundary_value']==0.0,'boundary value drift')
req(e10['applicability_pins']['production_patch_admitted'] is False,'boundary promoted to patch')
e11=next(e for e in f['entries'] if e['test_id']=='ATB-SUB-011')
req(e11['applicability_pins']['full_model_C_ledger_closed'] is False,'C ledger overclaim')
req(e11['applicability_pins']['full_model_N_ledger_closed'] is False,'N ledger overclaim')
req(e11['applicability_pins']['canonical_GHG_restart_qualified'] is False,'restart overclaim')
req(all(v is False for v in f['hard_boundaries'].values()),'fragment hard boundary')
req(s['gov05_adversarial_self_review']['assurance']=='PROCESS_SELF_REVIEWED_NOT_INDEPENDENT','GOV05 assurance')
req(all(v is False for v in s['hard_boundaries'].values()),'status hard boundary')
req(s['existing_registry_handling'].startswith('ATB-SUB-002 is not modified'),'SUB-002 handling')
req(r['exact_head']=='ESTABLISHED_BY_EXACT_HEAD_CI','receipt exact head')
req(r['scientific_admission'] is False and r['registry_integration_performed'] is False,'receipt scope')
req(W.exists(),'workflow')
print('ANIMO-TB05B bounded GHG subsystem fragment validation: PASS')
