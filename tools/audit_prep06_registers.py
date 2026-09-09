#!/usr/bin/env python3
"""Fail-closed schema/coverage audit for ANIMO-PREP06 machine registers.

This tool checks the preparatory evidence artifacts only. It does not execute or
modify frozen ANIMO source/testcases and cannot qualify behavioural reference.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

STATE_COLUMNS = [
    'state_id','symbol','species','phase','spatial_owner','routine_owner','unit',
    'storage_nonstorage','conserved_quantity','initialization_path',
    'mutation_routines','output_balance_exposure','evidence_path'
]
TRANSFER_COLUMNS = [
    'transfer_id','source_state','sink_state','external_internal','species',
    'sign_convention','routine','rate_state_variable','corresponding_balance_term',
    'conservation_identity','known_discrepancy_id','evidence'
]
REQUIRED_TCD = {'TCD-014','TCD-015','TCD-016','TCD-017','TCD-018','TCD-019','TCD-023','TCD-024'}
REQUIRED_STATE_IDS = {
    'W-INTERCEPTION','W-MATRIX','W-MACROPORE','OM-FOM','OM-HUMUS','OM-EXUDATE',
    'DOM-L-C','DOM-L-N','DOM-L-P','DOM-S-C','DOM-S-N','DOM-S-P',
    'N-NH4-AQ','N-NH4-ADS','N-NO3','P-PO4-AQ','P-FAST','P-SLOW','P-PRECIP',
    'TOP-NH4','TOP-NO3','TOP-DOM-C','TOP-DON','TOP-PO4','TOP-DOP',
    'CROP-SHOOT-DM','CROP-ROOT-DM','CROP-N-ACT','CROP-P-ACT',
    'GHG-CH4-SYS','GHG-N2O-SYS','MP-NH4','MP-NO3','MP-PO4'
}
REQUIRED_TRANSFER_MARKERS = {
    'vertical transport':'-VERTICAL', 'lateral drainage':'-DRAIN',
    'top/bottom boundary':'BOTTOM-', 'runoff/runon':'-RUNOFF',
    'irrigation':'IRRIGATION', 'precipitation/deposition':'DEPOSITION',
    'fertilization/manure':'FERT-', 'crop uptake':'CROP-N-UPTAKE',
    'harvest':'HARVEST-', 'grazing':'GRAZING-', 'root death':'ROOT-DEATH',
    'mineralization':'MINERALIZATION', 'immobilization':'IMMOBILIZATION',
    'nitrification':'N-NITRIFICATION', 'denitrification':'N-DENITRIFICATION',
    'sorption/desorption':'SORPTION', 'precipitation/dissolution':'P-PRECIPITATION',
    'DOM production/decay':'DOM-', 'ploughing/redistribution':'PLOUGH-',
    'phase transfer':'internal_phase', 'reporting-only':'reporting_only',
}

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        return reader.fieldnames or [], list(reader)

def audit(root: Path) -> dict:
    sp=root/'integration/animo-prep/PREP06_CONSERVED_STATE_INVENTORY.csv'
    tp=root/'integration/animo-prep/PREP06_TRANSFER_LEDGER.csv'
    sf, states=read_csv(sp); tf, transfers=read_csv(tp)
    errors=[]
    if sf != STATE_COLUMNS: errors.append('state columns do not match required schema/order')
    if tf != TRANSFER_COLUMNS: errors.append('transfer columns do not match required schema/order')
    state_ids=[r.get('state_id','') for r in states]; transfer_ids=[r.get('transfer_id','') for r in transfers]
    if len(state_ids)!=len(set(state_ids)): errors.append('duplicate state_id')
    if len(transfer_ids)!=len(set(transfer_ids)): errors.append('duplicate transfer_id')
    missing_states=sorted(REQUIRED_STATE_IDS-set(state_ids))
    if missing_states: errors.append('missing required state families: '+','.join(missing_states))
    tcd=set()
    transfer_text='\n'.join('|'.join(r.values()) for r in transfers)
    for r in transfers:
        tcd.update(x.strip() for x in r.get('known_discrepancy_id','').split(';') if x.strip())
    missing_tcd=sorted(REQUIRED_TCD-tcd)
    if missing_tcd: errors.append('missing required TCD mapping: '+','.join(missing_tcd))
    marker_coverage={name:(marker.lower() in transfer_text.lower()) for name,marker in REQUIRED_TRANSFER_MARKERS.items()}
    missing_markers=[name for name,ok in marker_coverage.items() if not ok]
    if missing_markers: errors.append('missing transfer classes: '+','.join(missing_markers))
    storage_classes=sorted(set(r['storage_nonstorage'] for r in states))
    if 'REPORTING_ACCUMULATOR' not in storage_classes: errors.append('reporting accumulator class absent')
    result={
        'evidence_class':'PREP06_REGISTER_SCHEMA_COVERAGE_TEST_NOT_REFERENCE',
        'state_rows':len(states),'transfer_rows':len(transfers),
        'state_columns_ok':sf==STATE_COLUMNS,'transfer_columns_ok':tf==TRANSFER_COLUMNS,
        'unique_state_ids':len(state_ids)==len(set(state_ids)),
        'unique_transfer_ids':len(transfer_ids)==len(set(transfer_ids)),
        'missing_required_state_ids':missing_states,
        'missing_required_tcd_mapping':missing_tcd,
        'transfer_class_coverage':marker_coverage,
        'storage_classes':storage_classes,
        'errors':errors,'passed':not errors,
        'reference_qualified':False,'production_migration_admitted':False,
    }
    return result

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('root',type=Path,nargs='?',default=Path('.')); p.add_argument('--json',type=Path)
    a=p.parse_args(); result=audit(a.root.resolve()); payload=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.json: a.json.write_text(payload,encoding='utf-8')
    print(payload,end='')
    return 0 if result['passed'] else 2
if __name__=='__main__': raise SystemExit(main())
