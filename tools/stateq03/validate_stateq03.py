#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE="4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
OWN=ROOT/"integration/animo-state/STATEQ03_MACROPORE_SOLUTE_OWNERSHIP.json"
SPLIT=ROOT/"integration/animo-state/STATEQ03_SPLIT_RUN_EVIDENCE.json"
STATUS=ROOT/"integration/animo-state/ANIMO-STATEQ03_STATUS.json"
DOC=ROOT/"docs/state/ANIMO_STATEQ03_TCD031_MACROPORE_RESTART_QUALIFICATION.md"
ALLOWED={
 "docs/state/ANIMO_STATEQ03_TCD031_MACROPORE_RESTART_QUALIFICATION.md",
 "integration/animo-state/STATEQ03_MACROPORE_SOLUTE_OWNERSHIP.json",
 "integration/animo-state/STATEQ03_SPLIT_RUN_EVIDENCE.json",
 "integration/animo-state/ANIMO-STATEQ03_STATUS.json",
 "tools/stateq03/validate_stateq03.py",
 ".github/workflows/animo-stateq03-tcd031.yml",
}

def load(p): return json.loads(p.read_text())
def require(c,m):
    if not c: raise SystemExit("FAIL: "+m)

for p in [OWN,SPLIT,STATUS,DOC]: require(p.exists(),f"missing {p.relative_to(ROOT)}")
o,s,st=load(OWN),load(SPLIT),load(STATUS)
for obj,name in [(o,'ownership'),(s,'split'),(st,'status')]:
    require(obj['workunit']=='ANIMO-STATEQ03',f"{name} workunit")
    require(obj['base_head']==BASE,f"{name} base head")
require(o['tcd']=='TCD-031' and s['tcd']=='TCD-031','TCD identity')
require(o['risk_tier']=='GOV04_TIER_C','risk tier')
require(o['b3_class']=='CLASS_C_STATE_RESTART_SEMANTICS','B3 class')
require(o['active_profile']['p_off_persistent_solute_scalars']==8,'P-off scalar inventory')
require(o['active_profile']['p_on_persistent_solute_scalars']==12,'P-on scalar inventory')
require(o['active_profile']['independent_layer_resolved_solute_coordinates']==0,'layer-resolved owner count')
require(o['deterministic_reconstruction_contracts']==[],'no invented reconstruction contract')

families=o['solute_families']
require(len(families)==6,'six solute families')
required_co={'CoMpDiorMa','CoMpDiorNi','CoMpNh','CoMpNi','CoMpDiorPo','CoMpPo'}
required_rs={'RsCoMpDiorMa','RsCoMpDiorNi','RsCoMpNh','RsCoMpNi','RsCoMpDiorPo','RsCoMpPo'}
require({f['variables']['accepted_start'] for f in families}==required_co,'accepted variable families')
require({f['variables']['result_end'] for f in families}==required_rs,'result variable families')
require(o['role_contracts']['accepted_start']['classification']=='PERSISTENT_STATE','accepted state class')
require(o['role_contracts']['accepted_start']['deterministic_reconstructibility']=='NO','persistent owners not reconstructed')
require(o['shared_scientific_contract']['owner']=='ANIMO_MACROPORE_SOLUTE','owner contract')

require(s['natural_active_case_search']['frozen_testbank_cases_scanned']==9,'testbank scan count')
require(s['natural_active_case_search']['natural_active_case_available'] is False,'no natural active case')
require(set(s['natural_active_case_search']['MacroPoreOption_values'])=={0},'all natural MacroPoreOption values are zero')
require(s['independent_local_reproduction']['matches_MP02_executable_sha256'] is True,'MP02 executable reproduction')
inv=s['native_checkpoint_inventory']
require(inv['revision53_native_Output_Init_serialized_scalars']==0,'native serialized scalar count')
require(inv['missing_p_off_scalars']==8 and inv['missing_p_on_scalars']==12,'missing inventory')
require(s['restore_direction_precondition']['result']=='FAIL_BEFORE_FIRST_POST_RESTORE_COMPARISON','restore-direction fail')
cr=s['continuous_vs_split']
require(cr['status']=='NOT_EXECUTABLE_AS_NATIVE_EQUIVALENCE_QUALIFICATION','split status')
require(cr['first_post_restore_comparison']=='NOT_REACHED','no fabricated first comparison')
require(cr['bounded_trajectory_comparison']=='NOT_REACHED','no fabricated trajectory')
require(cr['tolerance_introduced'] is False,'no tolerance')
require(cr['qualification_only_source_patch_created'] is False,'no hidden qualification source patch')

require(st['status']=='FAIL_CLOSED_TCD031_NATIVE_ACTIVE_MACROPORE_RESTART_STATE_INCOMPLETE','final status')
require(st['tcd031_atomic_tier_c_b3_readiness']=='NOT_READY','B3 readiness closed')
require(st['tcd025_dependency_decision']['current_TCD025_class_A_ledger_readiness'].startswith('NOT_OPENED'),'TCD025 readiness closed')
for key in ['production_patch','canonical_STATE_admission','TCD025_composition','B4','central_regie_update','new_tolerance']:
    require(st['scope_guards'][key] is False,f"scope guard {key}")

text=DOC.read_text()
for token in ['0/8','0/12','FAIL_CLOSED_TCD031_NATIVE_ACTIVE_MACROPORE_RESTART_STATE_INCOMPLETE','TCD-025 Class-A ledger readiness = NOT_OPENED']:
    require(token in text,f"documentation token {token}")

try:
    changed=subprocess.check_output(['git','diff','--name-only',BASE+'..HEAD'],cwd=ROOT,text=True).splitlines()
except Exception as exc:
    raise SystemExit(f'FAIL: cannot evaluate git scope guard: {exc}')
unexpected=sorted(set(changed)-ALLOWED)
require(not unexpected,'unexpected changed paths: '+', '.join(unexpected))
require(not any(p.startswith(('reference/','src/')) for p in changed),'production/reference source path changed')
print('PASS: ANIMO-STATEQ03 persisted evidence, fail-closed decision, and scope guards are internally consistent')
