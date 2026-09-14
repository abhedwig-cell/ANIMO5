import csv
import json
from pathlib import Path

DECISION = 'QUALIFIED_TCD034_CLASS_F_READINESS_REASSESSMENT_NOT_READY_THREE_MATERIAL_GATES_REMAIN_V1'
MATERIAL = {
    'PROCESS_RESOLVED_EMPIRICAL_VALIDATION_WITH_ANTI_COMPENSATION_DESIGN',
    'INTENDED_APPLICATION_ENVELOPE_EXPECTED_CHANGE_EVIDENCE',
    'GENUINELY_INDEPENDENT_CLASS_F_SCIENTIFIC_REVIEW',
}

def load(path):
    return json.loads(Path(path).read_text())

def main():
    a = load('integration/animo-ghg/GHG14_TCD034_CLASS_F_READINESS_ASSESSMENT.json')
    f = load('integration/animo-ghg/ANIMO-GHG14_AUTHORING_FREEZE.json')
    s = load('integration/animo-ghg/ANIMO-GHG14_STATUS.json')
    predecessors = [load(f'integration/animo-ghg/ANIMO-GHG{i:02d}_STATUS.json') for i in range(8, 14)]
    with open('integration/animo-ghg/GHG14_TCD034_CLASS_F_GATE_MATRIX.csv', newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert a['work_unit'] == f['work_unit'] == s['work_unit'] == 'ANIMO-GHG14'
    assert a['target'] == f['target'] == s['target'] == 'TCD-034'
    assert a['decision'] == s['primary_disposition'] == DECISION
    assert all(item['work_status']['qualified'] and item['work_status']['reviewed'] for item in predecessors)
    gates = a['class_f_gate_assessment']
    assert gates['scientific_rationale_and_authoritative_theory'] == 'PASS_STRENGTHENED'
    assert gates['calibration_and_parameter_implications'] == 'PASS_BOUNDED_NONTRANSFERABILITY_DEFINED'
    assert gates['conservation_implications'] == 'PASS_BOUNDED_SOURCE_LEDGER_COMPATIBILITY'
    assert gates['validation_evidence_appropriate_to_process'] == 'FAIL_MATERIAL'
    assert gates['expected_changes_across_application_envelope'] == 'PARTIAL_MATERIAL_GAP'
    assert gates['independent_scientific_review'] == 'FAIL_MATERIAL'
    assert set(a['material_remaining_gates']) == MATERIAL
    assert s['remaining_material_gate_count'] == 3
    assert set(s['remaining_material_gates']) == MATERIAL
    assert a['admission']['class_f_ready'] is False
    assert a['admission']['class_f_admitted'] is False
    assert a['admission']['b3_admitted'] is False
    assert a['admission']['production_authorized'] is False
    assert len(rows) == 7
    review = Path('integration/animo-ghg/ANIMO-GHG14_INTERNAL_ADVERSARIAL_REVIEW.json')
    if review.exists():
        r = load(review)
        assert r['same_agent'] is True
        assert r['genuinely_independent'] is False
        assert r['independence_claimed'] is False
        assert s['review']['completed'] is True
        assert s['work_status']['qualified'] is True
        assert s['work_status']['workunit_complete'] is True
    print('GHG14 TCD034 Class-F readiness reassessment PASS')

if __name__ == '__main__':
    main()
