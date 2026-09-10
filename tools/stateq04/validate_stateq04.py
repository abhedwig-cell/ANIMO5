#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
STATUS=ROOT/'integration/animo-state/ANIMO-STATEQ04_STATUS.json'
CONTRACT=ROOT/'integration/animo-state/STATEQ04_REMEDIATION_CONTRACT.json'
RESULT=ROOT/'integration/animo-state/STATEQ04_KERNEL_SPLIT_RESULT.json'
DOC=ROOT/'docs/state/ANIMO_STATEQ04_TCD031_REMEDIATION_QUALIFICATION.md'
DRIVER=ROOT/'tools/stateq04/stateq04_mptransp_driver.f90'
RUNNER=ROOT/'tools/stateq04/run_stateq04_kernel.py'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
    if not c: raise SystemExit(m)

for p in (STATUS,CONTRACT,RESULT,DOC,DRIVER,RUNNER): require(p.exists(),f'missing {p}')
s=json.loads(STATUS.read_text()); c=json.loads(CONTRACT.read_text()); r=json.loads(RESULT.read_text())
require(s['status']=='QUALIFIED_CANDIDATE_RESTORE_CONTRACT_READY_FOR_TIER_C_READINESS_NOT_ADMITTED','bad status')
require(s['risk_tier']=='GOV04_TIER_C' and s['b3_class'].startswith('CLASS_C'),'risk/class drift')
require(c['persistent_coordinates']['p_off_scalar_count']==8 and c['persistent_coordinates']['p_on_scalar_count']==12,'inventory drift')
require(c['deterministic_reconstruction']['RsCoMp_runtime_alias_at_accepted_restore']=='QUALIFIED_CANDIDATE_FROM_CoMp','alias rule missing')
require(c['deterministic_reconstruction']['CoMp_persistent_owner']=='NOT_RECONSTRUCTIBLE_GLOBALLY','owner reconstruction weakened')
require(r['comparison_policy']=='EXACT_BYTEWISE_NO_TOLERANCE','tolerance introduced')
require(r['all_species_exact'] and r['all_native_bad_controls_diverge'] and r['all_domain_drop_controls_diverge'],'discriminator failure')
require(set(r['species'])=={'DOM','DON','NH4','NO3','DOP','PO4'},'species coverage drift')
for sp,v in r['species'].items():
    require(v['stageA_prefix_exact'] and v['stageB_good_suffix_exact'] and v['native_bad_suffix_diverges'],f'{sp} primary result failed')
    require(v['first_post_restore_good_abs_diff']==[0.0,0.0],f'{sp} nonzero first restore diff')
    require(v['domain_drop_controls']['domain_1']['diverges'] and v['domain_drop_controls']['domain_2']['diverges'],f'{sp} domain-drop control failed')
    require(all(n==0 for n in v['warning_bytes'].values()),f'{sp} warning bytes present')
require(sha(DRIVER)==r['driver_sha256'],'driver hash mismatch')
for k in ('production_patch','canonical_STATE_admission','TCD025_composition','B4','central_regie_update','new_tolerance'):
    require(s['scope_guards'][k] is False,f'scope guard violated: {k}')
require(s['tcd031_atomic_tier_c_readiness']=='MAY_OPEN_SEPARATE_WORKUNIT','TCD031 downstream drift')
require(s['tcd025_class_a_ledger_readiness']=='MAY_OPEN_SEPARATE_WORKUNIT','TCD025 downstream drift')
print('ANIMO-STATEQ04 validation PASS')
