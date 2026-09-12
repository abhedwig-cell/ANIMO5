#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE='62080a8e731681407e2e7e759decc49c1a47fa7b'
B3Q05='997d867a2b107ec8e28efce530c82a204719de46'; RG05N='8758bd30e302b75dd7854ac00fd2e29473669a13'
B3D40='83fedc7323cea6da696a81bc64e4e3b13d794880'; B3D41='3ac98899dd4e6b7a5133cbecd758fab0b81e945d'
DEC='ADMIT_TCD019_RESTRICTED_FAST_LANGMUIR_EXACT_STORAGE_REPRESENTATION_STABLE_NO_LEGACY_FALLBACK_POLICY_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_C'
IDENT='TCD019_FAST_LANGMUIR_EXACT_STORAGE_REPRESENTATION_STABLE_TWO_VARIABLE_ROOT_NO_LEGACY_FALLBACK_BINARY64_POLICY'
ASSURANCE='PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT'
C=R/'integration/animo-b3/B3D42_TCD019_ADMISSION_CONTRACT.json'; S=R/'integration/animo-b3/ANIMO-B3D42_STATUS.json'; F=R/'integration/animo-b3/ANIMO-B3D42_AUTHORING_FREEZE.json'; V=R/'integration/animo-b3/ANIMO-B3D42_INTERNAL_ADVERSARIAL_REVIEW.json'
ALLOWED={'.github/workflows/animo-b3d42-tcd019.yml','docs/b3d42/WORK_UNIT_CONTRACT.md','integration/animo-b3/B3D42_TCD019_ADMISSION_CONTRACT.json','integration/animo-b3/ANIMO-B3D42_AUTHORING_FREEZE.json','integration/animo-b3/ANIMO-B3D42_INTERNAL_ADVERSARIAL_REVIEW.json','integration/animo-b3/ANIMO-B3D42_STATUS.json','tools/validate_b3d42_tcd019.py'}
def run(*a): return subprocess.run(a,cwd=R,check=True,text=True,capture_output=True).stdout
def gj(h,p): return json.loads(run('git','show',f'{h}:{p}'))
def load(p): return json.loads(p.read_text())
def req(x,m):
    if not x: raise SystemExit('ANIMO-B3D42 FAIL_CLOSED: '+m)
changed={p for p in run('git','diff','--name-only',BASE+'..HEAD').splitlines() if p}
req(changed<=ALLOWED,'scope escape '+str(sorted(changed-ALLOWED)))
req(not any(p.startswith(('src/','reference/','integration/animo-reg/')) for p in changed),'protected surface modified')
req('docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv' not in changed,'canonical register modified')
n5=gj(BASE,'integration/animo-numerics/ANIMO-NQ05_STATUS.json')
req(n5['qualified'] is True and n5['b3_admission_performed'] is False,'NQ05 boundary')
req(n5['qualified_candidate_identity']==IDENT and n5['historical_behavior']=='UNKNOWN_WITHOUT_B2','NQ05 identity/history')
req(n5['review']['completed'] is True and n5['review']['genuinely_independent'] is False,'NQ05 review')
p=gj(BASE,'integration/animo-numerics/NQ05_TCD019_RESTRICTED_POLICY.json')
req(p['qualified_scope']['fast_sorption']=='LANGMUIR_ONLY_Optcxfa_EQ_2','fast scope')
req(p['qualified_scope']['slow_sorption']==['LINEAR_Optcxsl_EQ_1','FREUNDLICH_Optcxsl_EQ_3'],'slow scope')
req(p['qualified_scope']['legacy_fallback_allowed'] is False and p['acceptance_contract']['model_tolerance']=='NONE','fallback/tolerance boundary')
req(p['acceptance_contract']['failure_to_satisfy']=='FAIL_CLOSED_NO_ACCEPTED_STATE','fail closed')
q=gj(B3Q05,'integration/animo-b3/ANIMO-B3Q05_STATUS.json'); req('TCD-019' in q['unadmitted_top_level'],'queue identity')
d40=gj(B3D40,'integration/animo-b3/ANIMO-B3D40_STATUS.json'); d41=gj(B3D41,'integration/animo-b3/ANIMO-B3D41_STATUS.json')
req(d40['admitted'] is True and d41['admitted'] is True,'prior post-RG05N admissions')
req(d41['aggregate_policy']['post_RG05N_new_admissions_if_exact_final_green']==2,'post-RG05N count')
rg=gj(RG05N,'integration/animo-reg/ANIMO-RG05N_STATUS.json'); req(rg['b4_open'] is False and rg['production_open'] is False,'RG05N gates')
c=load(C); req(c['candidate_decision']==DEC and c['admitted_identity']==IDENT,'contract decision')
req(c['aggregate_policy']['post_RG05N_exact_final_admissions_if_candidate_green']==3 and c['aggregate_policy']['required_next_aggregate']=='ANIMO-RG05O','aggregate handoff')
f=load(F); req(f['base_head']==BASE and f['review_must_pin_exact_green_authoring_head'] is True and f['substantive_change_resets_GOV05_review'] is True,'freeze')
s=load(S); req(s['candidate_decision']==DEC and all(x is False for x in s['hard_boundaries'].values()),'status/boundaries')
if V.exists():
    v=load(V); h=v.get('reviewed_head')
    req(v.get('target')=='TCD-019' and v.get('risk_tier')=='C','review target/tier')
    req(v.get('same_agent') is True and v.get('genuinely_independent') is False and v.get('independence_claimed') is False,'review independence')
    req(v.get('assurance')==ASSURANCE and v.get('reviewed_head_ci_conclusion')=='success','review assurance/CI')
    req(v.get('outcome')=='SELF_REVIEW_PASS_ADMIT_TCD019_RESTRICTED_NUMERICAL_POLICY_WITH_HISTORICAL_UNCERTAINTY','review outcome')
    post={p for p in run('git','diff','--name-only',h+'..HEAD').splitlines() if p}; req(post<={'integration/animo-b3/ANIMO-B3D42_INTERNAL_ADVERSARIAL_REVIEW.json','integration/animo-b3/ANIMO-B3D42_STATUS.json'},'post-review substantive change')
    req(s['state']=='ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY' and s['decision']==DEC and s['admitted'] is True and s['qualified'] is True,'final state')
    req(s['admitted_atomic_identity']==IDENT and s['work_status']=={'realized':True,'persisted':True,'tested':True,'reviewed':True,'qualified':True,'workunit_complete':True},'final identity/status')
    print('ANIMO-B3D42 PASS admitted bounded TCD019 policy; RG05O required before fourth post-RG05N admission')
else:
    req(s['state']=='CANDIDATE_NOT_ADMITTED_PENDING_REVIEW' and s['admitted'] is False and s['qualified'] is False,'candidate state')
    print('ANIMO-B3D42 PASS frozen candidate pending GOV05 Tier-C adversarial review')
