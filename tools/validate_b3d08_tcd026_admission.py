#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
status = json.loads((ROOT / 'integration/animo-b3/ANIMO-B3D08_STATUS.json').read_text())
closeout = json.loads((ROOT / 'integration/animo-b3/TCD026_B3_ADMISSION_CLOSEOUT.json').read_text())
doc = (ROOT / 'docs/b3/TCD026_B3_ADMISSION_CLOSEOUT.md').read_text()

errors = []
def req(cond, msg):
    if not cond:
        errors.append(msg)

req(status['work_unit'] == 'ANIMO-B3D08', 'wrong work unit')
req(status['target_tcd'] == 'TCD-026', 'wrong target')
req(status['qualification_class'] == 'A_ACCOUNTING_REPORTING_ONLY', 'wrong class')
req(status['base']['head'] == '21766eaf3443bcf432f05fbf6ba89d365bc70988', 'wrong B3D07 base')
req(status['review_authority']['head'] == '767779127d092c54a298e2f76a21d544e9af9895', 'wrong independent review head')
req(status['review_authority']['result'] == 'PASS', 'review not PASS')
req(status['review_authority']['workflow_run'] == 34446939959, 'wrong review run')
req(status['admission_route'] == 'INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY', 'wrong route')
req(status['intended_final_disposition'] == 'HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY', 'wrong disposition')

req(closeout['atomic_claim']['candidate'] == 'Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P', 'wrong atomic candidate')
req(closeout['historical_route']['qualified_B2_exists'] is False, 'B2 must remain unavailable')
req(closeout['historical_route']['historical_behaviour'] == 'UNKNOWN', 'historical behaviour must remain UNKNOWN')
req(closeout['historical_route']['historical_fidelity_claimed'] is False, 'historical fidelity must not be claimed')
req(closeout['admission']['decision'] == 'ADMIT_TCD026_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY', 'wrong admission decision')
req(closeout['admission']['scientific_b3_admission'] is True, 'scientific admission must be true in closeout record')
req(closeout['admission']['whole_model_b3_complete'] is False, 'whole-model B3 must remain incomplete')
req(closeout['admission']['b4_admitted'] is False, 'B4 must remain closed')
req(closeout['admission']['production_patch_authorized'] is False, 'production patch must remain unauthorized')
req(closeout['admission']['production_migration_admitted'] is False, 'production migration must remain closed')

for key, value in closeout['hard_boundaries'].items():
    if key in {
        'legacy_source_modified','frozen_testbank_modified','canonical_tcd_register_modified',
        'physical_state_patch','initialization_physics_change','process_flux_change',
        'restart_state_change','numerical_tolerance_added','whole_model_formatted_restart_identity_claimed',
        'SYNQ01_promoted_to_TCD026_oracle','STATEQ02_promoted_to_ledger_or_B2_oracle',
        'composition_with_other_organic_matter_TCDs','production_code_modified'
    }:
        req(value is False, f'hard boundary violated: {key}')

for token in [
    'ANIMO-B3D07@21766eaf3443bcf432f05fbf6ba89d365bc70988',
    'ANIMO-B3A04R2@767779127d092c54a298e2f76a21d544e9af9895',
    'ADMIT_TCD026_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY',
    'HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY',
    'No qualified B2 exists'
]:
    req(token in doc, f'document missing token: {token}')

if status['state'].startswith('QUALIFIED_'):
    req(status['decision'] == 'ADMIT_TCD026_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY', 'qualified status has wrong decision')
    req(status['admission']['scientific_b3_admission_qualified'] is True, 'qualified status missing admission qualification')
    req(status['work_status']['tested'] is True and status['work_status']['qualified'] is True and status['work_status']['work_unit_complete'] is True, 'qualified work status incomplete')
    req(status['validation']['github_actions_conclusion'] == 'success', 'qualified status must record green validation')
    req(status['validation']['validator_result'] == 'PASS_B3D08_TCD026_ADMISSION', 'wrong validator result')
    req(status['validation']['scope_guard'] == 'PASS_B3D08_ADMISSION_SCOPE_GUARD', 'wrong scope guard result')
else:
    req(status['state'] == 'IN_PROGRESS_PERSISTED_TCD026_ADMISSION_CLOSEOUT_VALIDATION_PENDING', 'unexpected pre-closeout state')
    req(status['decision'] == 'PENDING_FAIL_CLOSED_VALIDATION', 'unexpected pre-closeout decision')

if errors:
    print('FAIL_B3D08_TCD026_ADMISSION')
    for e in errors:
        print('-', e)
    raise SystemExit(1)
print('PASS_B3D08_TCD026_ADMISSION')
