#!/usr/bin/env python3
from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[2]
status = json.loads((root / 'integration/animo-b3/ANIMO-B3B04_STATUS.json').read_text())
e = json.loads((root / 'integration/animo-b3/B3B04_TCD040_RESTART_IDENTITY_EVIDENCE.json').read_text())
errors = []

def req(condition, message):
    if not condition:
        errors.append(message)

req(status['workunit'] == 'ANIMO-B3B04', 'wrong workunit')
req(status['target'] == 'TCD-040', 'wrong target')
req(status['class'] == 'B_LOCAL_RESTORE_INITIALIZATION_IDENTITY', 'wrong class')
req(e['frozen_b0']['source_archive_sha256'] == '183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566', 'wrong B0 source hash')
req(e['frozen_b0']['testbank_archive_sha256'] == '44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84', 'wrong B0 testbank hash')
req(e['cold_start_restart']['explicit_discriminator_at_zeroing'] is False, 'source discriminator claim changed')
req(e['cold_start_restart']['unconditional_line_deletion_qualified'] is False, 'unsafe unconditional edit admitted')
req(e['natural_GrassPeat']['five_targets_exact_positive_zero_after'] is True, 'natural activation failed')
req(e['natural_GrassPeat']['PO4_raw_unchanged'] is True, 'PO4 mechanism control failed')

s = e['split282']
req(s['stageA_exact_continuous_prefix'] is True, 'Stage A prefix failed')
req(s['checkpoint_matches_pre_owner_bytes'] is True, 'checkpoint identity failed')
req(s['checkpoint_write_noninterference'] is True, 'checkpoint write changed target')
req(s['restore_pre_checkpoint_exact'] and s['restore_post_checkpoint_exact'] and s['restore_pre_post_exact'], 'restore identity failed')
req(s['continuous_trace_sha256'] == s['restored_trace_sha256'], 'restored trace hash differs')
req(s['restored_full_1800_records_exact'] is True, 'restored full trace not exact')
req(s['legacy_post_targets_exact_positive_zero'] is True, 'legacy erasure not exact positive zero')
req(s['PO4_layer0_boundary_unchanged'] is True, 'PO4 boundary control changed')
f = s['first_divergence']
req(f['step'] == 283 and f['phase'] == 0, 'wrong first divergence step/phase')
req({tuple(x) for x in f['coordinates']} == {('NH4', 0), ('NO3', 0), ('DOM', 0), ('DON', 0), ('DOP', 0)}, 'wrong first divergence coordinates')

z = e['split67_zero_control']
req(z['checkpoint_all_targets_exact_positive_zero'] is True, 'zero checkpoint control failed')
req(z['continuous_trace_sha256'] == z['legacy_trace_sha256'], 'zero-state trace hash differs')
req(z['full_1800_records_exact'] is True, 'zero-state full trace not exact')
req(e['comparison_policy'] == 'EXACT_RAW_IEEE754_BYTES_NO_TOLERANCE', 'comparison policy changed')

a = e['atomic_correction']
req(a['restart_only'] and a['preserve_or_restore_exact_accepted_owners'] and a['retain_cold_start_semantics'], 'atomic correction widened')
req(a['modify_PO4'] is False and a['new_state'] is False and a['tolerance'] is False, 'atomic correction surface widened')
req(a['TCD016_composition'] is False and a['internal_crop_composition'] is False and a['broad_restart_redesign'] is False and a['production_patch'] is False, 'composition/production guard failed')

d = e['decision']
req(d['status'] == 'QUALIFIED_ATOMIC_CLASS_B_RESTART_IDENTITY_READINESS_ONLY', 'wrong decision')
req(d['canonical_STATE_admission'] is False and d['B3_admission'] is False and d['production_patch'] is False, 'admission overclaim')

for key, value in status['scope_guards'].items():
    if key != 'fail_closed_on_owner_ambiguity':
        req(value is False, f'status scope guard widened: {key}')
req(status['scope_guards']['fail_closed_on_owner_ambiguity'] is True, 'fail-closed guard removed')
req(status['stateq02_guard_282_is_tcd040_qualification'] is False, 'STATEQ02 sentinel mis-promoted')

if errors:
    print('B3B04 validation FAIL')
    for error in errors:
        print('-', error)
    sys.exit(1)

print('B3B04 validation PASS')
