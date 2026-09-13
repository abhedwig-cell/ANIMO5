#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

BASE='063627cddd478904c437c9c47f02513ef0d9326b'
GUIDE='ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301'
ALLOWED=(
 '.github/workflows/animo-sq05-tcd016-c1.yml',
 'docs/science/TCD016_B0_USER_GUIDE_RECONCILIATION.md',
 'integration/animo-science/SQ05_TCD016_B0_USER_GUIDE_RECONCILIATION.json',
 'integration/animo-science/ANIMO-SQ05_AUTHORING_FREEZE.json',
 'integration/animo-science/ANIMO-SQ05_INTERNAL_ADVERSARIAL_REVIEW.json',
 'integration/animo-science/ANIMO-SQ05_STATUS.json',
 'tools/sq05/'
)

def load(p): return json.loads(Path(p).read_text())
def changed():
    out=subprocess.check_output(['git','diff','--name-only',f'{BASE}..HEAD'],text=True)
    return [x for x in out.splitlines() if x]
def allowed(p): return any(p==a or (a.endswith('/') and p.startswith(a)) for a in ALLOWED)

def main():
    ev=load('integration/animo-science/SQ05_TCD016_B0_USER_GUIDE_RECONCILIATION.json')
    st=load('integration/animo-science/ANIMO-SQ05_STATUS.json')
    reg=load('integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json')
    assert ev['work_unit']==st['work_unit']=='ANIMO-SQ05'
    assert ev['target']==st['target']=='TCD-016-C1'
    assert ev['base_authority']==st['base_authority']==f'ANIMO-SQ04@{BASE}'
    docs=[x for x in reg['artifacts'] if x['evidence_id']=='ANIMO-B0-DOC-UG40-2005']
    assert len(docs)==1
    doc=docs[0]
    assert doc['sha256']==GUIDE==st['b0_document_sha256']==ev['b0_document']['sha256']
    assert doc['identity_basis']['documented_model_version']=='ANIMO 4.0'
    assert ev['b0_document']['controlled_immutable_storage_proven'] is False
    pages={x['page'] for x in ev['page_claims']}
    assert {17,18,21,46,49,50}.issubset(pages)
    assert ev['bounded_negative_search']['qualified_result']=='NO_EXPLICIT_ANIMO4_0_USER_GUIDE_CONTRACT_FOUND_FOR_TCD016_C1_CONTINUATION_STATE_OR_REWETTING_PROCESS'
    assert ev['bounded_negative_search']['absence_not_promoted_to_proof_of_PHYSICAL_IMPOSSIBILITY'] is True
    assert ev['reconciliation']['SQ04_Frvo_not_reusable_unchanged']=='CORROBORATED_BY_ADDITION_EVENT_PROVENANCE'
    assert ev['reconciliation']['SQ04_Conhtop_not_generic_continuation_owner']=='CORROBORATED_BY_VIRTUAL_ADDITIONS_LAYER_IDENTITY'
    assert ev['reconciliation']['specific_new_dry_process_law']=='NOT_QUALIFIED'
    assert ev['reconciliation']['specific_rewetting_receiver_or_kinetics']=='NOT_QUALIFIED'
    assert ev['historical_behavior']==st['historical_behavior']=='UNKNOWN_WITHOUT_B2'
    assert ev['b3_disposition']==st['c1_b3_disposition']=='UNRESOLVED_NOT_ADMITTED'
    assert st['hard_boundaries']['production_source_modified'] is False
    assert st['hard_boundaries']['frozen_b0_modified'] is False
    assert st['hard_boundaries']['raw_pdf_republished'] is False
    assert st['hard_boundaries']['central_queue_modified'] is False
    bad=[p for p in changed() if not allowed(p)]
    assert not bad, bad
    rp=Path('integration/animo-science/ANIMO-SQ05_INTERNAL_ADVERSARIAL_REVIEW.json')
    if rp.exists():
        rv=load(rp)
        assert rv['work_unit']=='ANIMO-SQ05'
        assert rv['same_agent'] is True and rv['genuinely_independent'] is False and rv['independence_claimed'] is False
        assert rv['outcome']=='SELF_REVIEW_PASS'
        assert rv['decision']=='PASS_TCD016_C1_B0_GUIDE_RECONCILIATION_NO_PROCESS_LAW_ADMISSION'
        assert st['review']['completed'] is True
        assert st['qualified'] is True
    print('SQ05 TCD016-C1 B0 user-guide reconciliation PASS')

if __name__=='__main__': main()
