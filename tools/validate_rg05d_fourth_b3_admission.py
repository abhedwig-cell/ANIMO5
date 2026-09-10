#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
status = json.loads((ROOT/'integration/animo-reg/ANIMO-RG05D_STATUS.json').read_text())
inv = json.loads((ROOT/'integration/animo-reg/RG05D_B3_ADMISSION_INVENTORY.json').read_text())
queue = json.loads((ROOT/'integration/animo-reg/RG05D_B3_QUEUE_DELTA.json').read_text())
doc = (ROOT/'docs/governance/ANIMO_RG05D_FOURTH_B3_ADMISSION_REGIE.md').read_text()
errors=[]
def req(c,m):
    if not c: errors.append(m)

req(status['work_unit']=='ANIMO-RG05D','wrong work unit')
req(status['base']['head']=='cc280b630d6dc0d6bc1b8b0783ccfa4f91e15624','wrong B3D08 base')
req(status['authority']['RG05C']=='2d3cc363599ed32b6537f318462c27db5ffaa7c2','wrong RG05C authority')
req(status['admission_state']['scientific_admissions']==4,'wrong admission count')
req(status['admission_state']['admitted_tcds']==['TCD-017','TCD-018','TCD-024','TCD-026'],'wrong admitted list')
req(status['admission_state']['b3_whole_model_baseline_complete'] is False,'B3 must remain incomplete')
req(status['admission_state']['b4_baseline_admitted'] is False,'B4 must remain closed')
req(status['admission_state']['production_migration_admitted'] is False,'production must remain closed')

req(inv['new_admission']['admission_authority']=='ANIMO-B3D08@cc280b630d6dc0d6bc1b8b0783ccfa4f91e15624','wrong TCD026 authority')
req(inv['new_admission']['historical_behaviour']=='UNKNOWN','historical behaviour changed')
req(inv['counts']['scientific_admissions']==4,'inventory count wrong')
req(inv['project_boundary']['B3_complete'] is False and inv['project_boundary']['B4_open'] is False and inv['project_boundary']['production_open'] is False,'project boundary opened')

q=queue['post_delta_counts']
req(q['canonical_tcd_entries']==25,'canonical count wrong')
req(q['active_queue_entries']==21,'active count wrong')
req(q['scientific_admissions']==4,'queue admission count wrong')
req(q['active_queue_entries']+q['scientific_admissions']==q['canonical_tcd_entries'],'queue arithmetic mismatch')
req(q['WAITING_ON_ROUTE_AND_REVIEW']==3,'route/review count wrong')
req(queue['unchanged_high_level_boundaries']['canonical_tcd_register_tail']=='TCD-042','register tail changed')
req(queue['unchanged_high_level_boundaries']['TCD043_reserved'] is False,'TCD043 reserved')

for token in ['TCD-026','21 + 4 = 25','WAITING_ON_ROUTE_AND_REVIEW','TCD-042']:
    req(token in doc,f'doc missing {token}')

if status['state'].startswith('QUALIFIED_'):
    req(status['decision']=='QUALIFIED_POST_RG05C_FOURTH_ATOMIC_B3_ADMISSION_INTEGRATION_NO_PRODUCTION_MIGRATION','wrong qualified decision')
    req(status['work_status']['tested'] and status['work_status']['qualified'] and status['work_status']['work_unit_complete'],'qualified work status incomplete')
    req(status['validation']['github_actions_conclusion']=='success','qualified status missing green run')
    req(status['validation']['validator_result']=='PASS_RG05D_FOURTH_B3_ADMISSION_INTEGRATION','wrong validator result')
    req(status['validation']['scope_guard']=='PASS_RG05D_SCOPE_GUARD','wrong scope guard')
else:
    req(status['state']=='IN_PROGRESS_PERSISTED_FOURTH_B3_ADMISSION_INTEGRATION_VALIDATION_PENDING','unexpected pending state')
    req(status['decision']=='PENDING_FAIL_CLOSED_VALIDATION','unexpected pending decision')

if errors:
    print('FAIL_RG05D_FOURTH_B3_ADMISSION_INTEGRATION')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('PASS_RG05D_FOURTH_B3_ADMISSION_INTEGRATION')
