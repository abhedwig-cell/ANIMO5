#!/usr/bin/env python3
import csv,json,subprocess
from pathlib import Path
BASE="cf235fbc93fdb77d93aa260c8ede8fcdbbdbc5d3"
EXPECTED_DISPOSITION="QUALIFIED_TCD034_SELECTOR_IDENTITY_UNRESOLVED_MATERIAL_THEORY_OR_DESIGN_EVIDENCE_REQUIRED"
ALLOWED=(".github/workflows/animo-ghg06-tcd034.yml","docs/ghg/TCD034_SELECTOR_THEORY_PROVENANCE.md","integration/animo-ghg/GHG06_TCD034_","integration/animo-ghg/ANIMO-GHG06_","tools/ghg06/")
EXPECTED_SOURCE={
  "ANIMO_4.1.5.53/ghg_ch4.for": "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
  "ANIMO_4.1.5.53/input1.for": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95",
  "ANIMO_4.1.5.53/Param.inc": "20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475",
  "ANIMO_4.1.5.53/Temper.for": "643e4460a897ec629068dc97ab4589a745304b8fa7adb7597dfadc1a9a9d41e5",
  "ANIMO_4.1.5.53/Input_hydro.for": "5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64",
  "ANIMO_4.1.5.53/root_plant.for": "07adda92e78a21bde08e137d1cb09bb40d9c63c4f19dcdeeef0d3e263b107816",
  "ANIMO_4.1.5.53/root_grass.for": "cad5cc713e72b7fac01cbba63caa25560fcabd243c73d9fc06ab7130de4d0661",
  "ANIMO_4.1.5.53/root_extern.for": "063a754fac2fe1b1c4b60fab1e395b8b65a9a03a5d89ace03e08868e1774f0e9",
  "ANIMO_4.1.5.53/Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7"
}

def readj(p): return json.loads(Path(p).read_text())
def csvrows(p):
    with open(p,newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def changed(): return [x for x in subprocess.check_output(['git','diff','--name-only',f'{BASE}..HEAD'],text=True).splitlines() if x]
def allowed(p): return any(p==x or p.startswith(x) for x in ALLOWED)
def manifest_map(path):
    with open(path,newline='',encoding='utf-8-sig') as f: return {r['path']:r['sha256'] for r in csv.DictReader(f)}

def main():
    prov=readj('integration/animo-ghg/GHG06_TCD034_SELECTOR_PROVENANCE.json')
    var=readj('integration/animo-ghg/GHG06_TCD034_VARIABLE_INDEX_MAP.json')
    dec=readj('integration/animo-ghg/GHG06_TCD034_DECISION.json')
    frag=readj('integration/animo-ghg/GHG06_TCD034_PROVENANCE_FRAGMENT.json')
    freeze=readj('integration/animo-ghg/ANIMO-GHG06_AUTHORING_FREEZE.json')
    status=readj('integration/animo-ghg/ANIMO-GHG06_STATUS.json')
    assert all(x['work_unit']=='ANIMO-GHG06' for x in [prov,var,dec,freeze,status])
    assert all(x['target']=='TCD-034' for x in [prov,var,dec,freeze,status])
    assert freeze['base_head']==BASE and prov['base_predecessor']==f'ANIMO-GHG05@{BASE}'
    assert prov['semantic_contract']=='TCD034_PLANT_GROWTH_TEMPERATURE_SELECTOR_IDENTITY'
    assert prov['parallelism']=='PARALLEL_AFTER_PINNING'
    assert dec['primary_disposition']==status['primary_disposition']==EXPECTED_DISPOSITION
    assert dec['historical_selector_conclusion']=='NOT_QUALIFIED'
    assert dec['model_evolution_selector_conclusion']=='NOT_QUALIFIED'
    assert dec['positive_gate']['3_exact_mathematical_selector'].startswith('FAIL_')
    assert dec['positive_gate']['9_multi_layer_behavior'].startswith('FAIL_')
    assert dec['FVEGCH4_positive_control_status'].startswith('OPEN_UNCHANGED')
    assert status['b3_admission_performed'] is False and status['production_authorized'] is False
    assert frag['registry_mutated'] is False and frag['production_behavior_claimed'] is False
    assert 'Te(Nuroup+1)' in prov['current_source_reconstruction']['current_standard_fortran_selector']
    assert prov['current_source_reconstruction']['Kpl']=='0.24 d-1'
    assert prov['provenance_fingerprint']['assessment']=='STRONGLY_SUPPORTED_NOT_HISTORICAL_AUTHORITY'
    assert '0.50 m' in prov['provenance_fingerprint']['inference']
    assert var['geometry_gap'].startswith('No reviewed ANIMO authority')
    hyps={r['hypothesis']:r for r in csvrows('integration/animo-ghg/GHG06_TCD034_HYPOTHESIS_MATRIX.csv')}
    assert hyps['H6']['historical_status']=='STRONGLY_SUPPORTED_CONCEPTUAL_IDENTITY_NOT_EXACT_SELECTOR'
    assert hyps['H7']['decision']=='SELECTED'
    trace={r['link']:r for r in csvrows('integration/animo-ghg/GHG06_TCD034_THEORY_CODE_TRACE.csv')}
    assert trace['6']['status']=='ABSENT' and trace['7']['status']=='CONTRADICTED'
    ev={r['id']:r for r in csvrows('integration/animo-ghg/GHG06_TCD034_EVIDENCE_MATRIX.csv')}
    assert ev['EXT-WH2000']['role']=='NEW_MODEL_EVOLUTION_SCIENTIFIC_EVIDENCE only'
    src=manifest_map('reference/source/source_manifest.csv')
    for p,h in EXPECTED_SOURCE.items(): assert src.get(p)==h,(p,src.get(p),h)
    bad=[p for p in changed() if not allowed(p)]
    assert not bad, f'scope guard failed: {bad}'
    rp=Path('integration/animo-ghg/ANIMO-GHG06_INTERNAL_ADVERSARIAL_REVIEW.json')
    if rp.exists():
        rev=readj(rp)
        assert rev['work_unit']=='ANIMO-GHG06' and rev['target']=='TCD-034'
        assert rev['same_agent'] is True and rev['genuinely_independent'] is False and rev['independence_claimed'] is False
        assert rev['assurance']=='PROCESS_SELF_REVIEWED_NOT_INDEPENDENT'
        assert rev['primary_disposition']==EXPECTED_DISPOSITION
        assert rev['outcome']=='PASS_NEGATIVE_SELECTOR_DISPOSITION_WITH_NO_SUBSTANTIVE_REMEDIATION'
        assert status['review']['completed'] is True
        assert status['work_status']['reviewed'] is True and status['work_status']['qualified'] is True
        assert status['work_status']['workunit_complete'] is True
        assert status['phase']=='COMPLETE_SUBJECT_TO_EXACT_FINAL_HEAD_CI'
    print('GHG06 TCD034 theory/provenance validation PASS')
if __name__=='__main__': main()
