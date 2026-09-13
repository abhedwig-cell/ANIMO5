#!/usr/bin/env python3
import csv, json, subprocess
from pathlib import Path

BASE='897ba742630f06381a2b89290db80d5f405ab51d'
MASSQ03='68a8c202bd01bf55b31b7c944884fb2f78a6a8e8'
EXPECTED_SOURCE={
 'ANIMO_4.1.5.53/Outbal_Init.for':'95c0d7aad6cb863fcbb5dd41563674af3ab0819387212d27d5f6f04b4a788cc8',
 'ANIMO_4.1.5.53/Outbal_calc.for':'4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981',
 'ANIMO_4.1.5.53/Outbal_write.for':'cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea',
}
ALLOWED=(
 '.github/workflows/animo-massq04-tcd016-c1.yml',
 'docs/mass/TCD016_C1_CONTINUATION_BALANCE_ONTOLOGY.md',
 'integration/animo-mass/MASSQ04_TCD016_C1_BALANCE_ONTOLOGY.json',
 'integration/animo-mass/ANIMO-MASSQ04_AUTHORING_FREEZE.json',
 'integration/animo-mass/ANIMO-MASSQ04_INTERNAL_ADVERSARIAL_REVIEW.json',
 'integration/animo-mass/ANIMO-MASSQ04_STATUS.json',
 'tools/massq04/'
)

def load(p): return json.loads(Path(p).read_text())
def manifest():
    with open('reference/source/source_manifest.csv',newline='',encoding='utf-8-sig') as f:
        return {r['path']:r['sha256'] for r in csv.DictReader(f)}
def changed():
    out=subprocess.check_output(['git','diff','--name-only',f'{BASE}..HEAD'],text=True)
    return [x for x in out.splitlines() if x]
def allowed(p): return any(p==x or (x.endswith('/') and p.startswith(x)) for x in ALLOWED)

def main():
    ev=load('integration/animo-mass/MASSQ04_TCD016_C1_BALANCE_ONTOLOGY.json')
    st=load('integration/animo-mass/ANIMO-MASSQ04_STATUS.json')
    fr=load('integration/animo-mass/ANIMO-MASSQ04_AUTHORING_FREEZE.json')
    assert ev['work_unit']==st['work_unit']==fr['work_unit']=='ANIMO-MASSQ04'
    assert ev['target']==st['target']==fr['target']=='TCD-016-C1'
    assert ev['base_science_authority']==st['base_science_authority']==f'ANIMO-SQ05@{BASE}'
    assert ev['mass_predecessor']==st['mass_predecessor']==f'ANIMO-MASSQ03@{MASSQ03}'
    m=manifest()
    for p,h in EXPECTED_SOURCE.items():
        assert m.get(p)==h, (p,m.get(p),h)
        assert ev['source_files'][p]==h
    legacy=ev['legacy_balance_ontology']
    assert legacy['solution_storage_begin']=='BANHST'
    assert legacy['solution_storage_end']=='BANHSTT'
    assert legacy['soil_complex_storage_begin']=='BANHCX'
    assert legacy['soil_complex_storage_end']=='BANHCXT'
    assert legacy['explicit_continuation_storage_term_present'] is False
    rr=ev['revision53_storage_reconstruction']
    assert rr['continuation_state_in_legacy_deviation_equation'] is False
    q=ev['qualified_model_evolution_contract']
    assert q['total_storage_identity']=='S_NH4=S_aq+S_complex+S_cont'
    assert q['S_cont_owner']=='M_surface_NH4_non_aqueous_continuation'
    assert q['wet_to_continuation_transfer']=='INTERNAL_NOT_EXTERNAL'
    assert q['continuation_to_receiver_transfer']=='INTERNAL_NOT_EXTERNAL'
    assert q['observer_may_reconstruct_state_from_residual'] is False
    assert q['observer_may_own_physical_state'] is False
    assert q['new_process_loss_must_be_named_once'] is True
    assert q['legacy_public_field_meaning_may_change_silently'] is False
    assert q['specific_public_output_name_qualified'] is False
    assert ev['historical_behavior']==st['historical_behavior']=='UNKNOWN_WITHOUT_B2'
    assert ev['b3_disposition']==st['c1_b3_disposition']=='UNRESOLVED_NOT_ADMITTED'
    hb=st['hard_boundaries']
    for k in ('production_source_modified','persistent_state_added','canonical_register_modified','central_queue_modified','TCD016_C1_admitted','specific_process_law_qualified','legacy_balance_field_redefined','historical_fidelity_claimed','production_migration_authorized'):
        assert hb[k] is False, k
    bad=[p for p in changed() if not allowed(p)]
    assert not bad, bad
    rp=Path('integration/animo-mass/ANIMO-MASSQ04_INTERNAL_ADVERSARIAL_REVIEW.json')
    if rp.exists():
        r=load(rp)
        assert r['same_agent'] is True and r['genuinely_independent'] is False and r['independence_claimed'] is False
        assert r['outcome']=='SELF_REVIEW_PASS'
        assert r['decision']=='PASS_TCD016_C1_BALANCE_ONTOLOGY_NO_PROCESS_OR_B3_ADMISSION'
        assert st['review']['completed'] is True and st['qualified'] is True
    print('MASSQ04 TCD016-C1 balance ontology validation PASS')

if __name__=='__main__': main()
