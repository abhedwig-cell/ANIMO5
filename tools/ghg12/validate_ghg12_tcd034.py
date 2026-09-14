import csv
import json
from pathlib import Path

ECLASS = 'NEW_MODEL_EVOLUTION_SCIENTIFIC_EVIDENCE_NOT_HISTORICAL_ANIMO_AUTHORITY'
DECISION = 'QUALIFIED_TCD034_PUBLIC_VALIDATION_DATASET_CANDIDATE_STACK_IDENTIFIED_DETAILED_JOINABILITY_EXTRACTION_REQUIRED_V1'

def load(path):
    return json.loads(Path(path).read_text())

def main():
    assessment = load('integration/animo-ghg/GHG12_TCD034_VALIDATION_DATASET_ASSESSMENT.json')
    freeze = load('integration/animo-ghg/ANIMO-GHG12_AUTHORING_FREEZE.json')
    status = load('integration/animo-ghg/ANIMO-GHG12_STATUS.json')
    predecessor = load('integration/animo-ghg/ANIMO-GHG11_STATUS.json')
    with open('integration/animo-ghg/GHG12_TCD034_VALIDATION_DATASET_CANDIDATES.csv', newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert assessment['work_unit'] == freeze['work_unit'] == status['work_unit'] == 'ANIMO-GHG12'
    assert assessment['target'] == freeze['target'] == status['target'] == 'TCD-034'
    assert assessment['evidence_class'] == status['evidence_class'] == ECLASS
    assert assessment['decision'] == status['primary_disposition'] == DECISION
    assert predecessor['primary_disposition'] == 'QUALIFIED_TCD034_EXTERNAL_MODEL_EVOLUTION_EVIDENCE_PARTIAL_EMPIRICAL_SUPPORT_CLASS_F_VALIDATION_GAP_REMAINS_V1'
    assert predecessor['work_status']['qualified'] is True
    assert predecessor['work_status']['reviewed'] is True
    assert len(rows) == 6
    assert rows[0]['candidate_id'] == 'GHG12-C01'
    assert rows[0]['readiness'] == 'PRIMARY_CANDIDATE_READY_FOR_FILE_LEVEL_EXTRACTION'
    assert assessment['candidate_stack']['primary_dataset'] == 'spruce.200'
    gates = assessment['joinability_gates']
    assert all(value is False for value in gates.values())
    sci = assessment['scientific_interpretation']
    assert sci['process_resolved_public_candidate_exists'] is True
    assert sci['candidate_materially_stronger_than_system_flux_only'] is True
    assert sci['empirical_validation_performed'] is False
    assert sci['class_f_admission_ready'] is False
    assert assessment['class_f_admitted'] is False
    assert assessment['b3_admitted'] is False
    assert assessment['production_authorized'] is False
    review_path = Path('integration/animo-ghg/ANIMO-GHG12_INTERNAL_ADVERSARIAL_REVIEW.json')
    if review_path.exists():
        review = load(review_path)
        assert review['same_agent'] is True
        assert review['genuinely_independent'] is False
        assert review['independence_claimed'] is False
        assert status['review']['completed'] is True
        assert status['work_status']['qualified'] is True
        assert status['work_status']['workunit_complete'] is True
    print('GHG12 TCD034 validation dataset acquisition qualification PASS')

if __name__ == '__main__':
    main()
