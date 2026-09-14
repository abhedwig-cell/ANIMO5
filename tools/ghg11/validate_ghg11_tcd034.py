import csv
import json
from pathlib import Path

ECLASS = 'NEW_MODEL_EVOLUTION_SCIENTIFIC_EVIDENCE_NOT_HISTORICAL_ANIMO_AUTHORITY'
DECISION = 'QUALIFIED_TCD034_EXTERNAL_MODEL_EVOLUTION_EVIDENCE_PARTIAL_EMPIRICAL_SUPPORT_CLASS_F_VALIDATION_GAP_REMAINS_V1'

def load(path):
    return json.loads(Path(path).read_text())

def main():
    assessment = load('integration/animo-ghg/GHG11_TCD034_EXTERNAL_EVIDENCE_ASSESSMENT.json')
    freeze = load('integration/animo-ghg/ANIMO-GHG11_AUTHORING_FREEZE.json')
    status = load('integration/animo-ghg/ANIMO-GHG11_STATUS.json')
    predecessor = load('integration/animo-ghg/ANIMO-GHG10_STATUS.json')
    with open('integration/animo-ghg/GHG11_TCD034_EXTERNAL_EVIDENCE_MATRIX.csv', newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert assessment['work_unit'] == freeze['work_unit'] == status['work_unit'] == 'ANIMO-GHG11'
    assert assessment['target'] == freeze['target'] == status['target'] == 'TCD-034'
    assert assessment['evidence_class'] == ECLASS
    assert assessment['decision'] == status['primary_disposition'] == DECISION
    assert predecessor['work_status']['qualified'] is True
    assert predecessor['work_status']['reviewed'] is True
    assert len(rows) == 9
    assert all(row['evidence_class'] == ECLASS for row in rows)
    assert all(row['historical_animo_authority'] == 'NO' for row in rows)
    gates = assessment['class_f_gate_assessment']
    assert gates['scientific_rationale_and_authoritative_theory'] == 'PASS_STRENGTHENED'
    assert gates['validation_evidence_appropriate_to_process'].startswith('FAIL_MATERIAL')
    assert gates['independent_scientific_review'].startswith('FAIL_NOT_PERFORMED')
    assert assessment['admission']['class_f_ready'] is False
    assert assessment['admission']['class_f_admitted'] is False
    assert assessment['admission']['b3_admitted'] is False
    assert assessment['admission']['production_authorized'] is False
    review_path = Path('integration/animo-ghg/ANIMO-GHG11_INTERNAL_ADVERSARIAL_REVIEW.json')
    if review_path.exists():
        review = load(review_path)
        assert review['same_agent'] is True
        assert review['genuinely_independent'] is False
        assert review['independence_claimed'] is False
        assert status['review']['completed'] is True
        assert status['work_status']['qualified'] is True
        assert status['work_status']['workunit_complete'] is True
    print('GHG11 TCD034 external validation evidence qualification PASS')

if __name__ == '__main__':
    main()
