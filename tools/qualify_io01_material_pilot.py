#!/usr/bin/env python3
"""Execute bounded ANIMO-IO01 MATERIAL Pilot B qualification.

Requires the frozen ANIMO testbank plus locally built probes linked against the
exact official TTUTIL 4.27 source. No model physics is executed.
"""
from __future__ import annotations
import argparse, hashlib, json, struct, subprocess, tempfile, zipfile
from pathlib import Path

from io01_material_pilot import (
    dense_native_fixture,
    dense_native_typed_double_fixture,
    parse_legacy_material_text,
    parse_native_material_probe_output,
    semantic_projection,
    validate_native_material_schema,
)

TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
TTUTIL_ZIP_SHA256 = "ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193"
RUURLO_MATERIAL = "ANIMO_testbank/RuurloGrass/Input/MATERIAL.INP"
RUURLO_MATERIAL_SHA256 = "03857e4681cc83fe84c054ac1b1e1cd3df91c9b5204f7f8bc70962d14033c507"


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def sha256_bytes(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def run_probe(exe:Path, fixture:str, work:Path, name:str):
    inp=work/f"{name}.inp"; inp.write_text(fixture,encoding='utf-8')
    result=subprocess.run([str(exe.resolve()),inp.name],cwd=work,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if result.returncode!=0:
        raise RuntimeError(f"{name} probe failed rc={result.returncode}: {result.stderr}\n{result.stdout}")
    if not result.stdout.strip():
        raise RuntimeError(f"{name} probe produced no output")
    return result.stdout

def ulp_distance(a:float,b:float)->int:
    ia=struct.unpack('>q',struct.pack('>d',a))[0]; ib=struct.unpack('>q',struct.pack('>d',b))[0]
    if ia<0: ia=0x8000000000000000-ia
    if ib<0: ib=0x8000000000000000-ib
    return abs(ia-ib)

def numeric_mismatches(a,b,path=''):
    out=[]
    if isinstance(a,dict):
        for k in a: out.extend(numeric_mismatches(a[k],b[k],path+'/'+str(k)))
    elif isinstance(a,list):
        for i,(x,y) in enumerate(zip(a,b)): out.extend(numeric_mismatches(x,y,path+f'/{i}'))
    elif isinstance(a,float) and isinstance(b,float) and a!=b:
        out.append({'path':path,'legacy':a,'native':b,'ulp_distance':ulp_distance(a,b),'absolute_difference':abs(a-b)})
    return out

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('testbank_zip',type=Path); ap.add_argument('ttutil_zip',type=Path); ap.add_argument('exact_probe',type=Path)
    ap.add_argument('--typed-probe',type=Path); ap.add_argument('--output',type=Path)
    a=ap.parse_args()

    test_hash=sha256_file(a.testbank_zip)
    if test_hash!=TESTBANK_SHA256: raise SystemExit(f'testbank hash mismatch {test_hash}')
    tt_hash=sha256_file(a.ttutil_zip)
    if tt_hash!=TTUTIL_ZIP_SHA256: raise SystemExit(f'TTUTIL ZIP hash mismatch {tt_hash}')
    with zipfile.ZipFile(a.testbank_zip) as z: material_bytes=z.read(RUURLO_MATERIAL)
    if sha256_bytes(material_bytes)!=RUURLO_MATERIAL_SHA256: raise SystemExit('Ruurlo MATERIAL member hash mismatch')

    legacy_obj=parse_legacy_material_text(material_bytes.decode('latin-1'),source_file=RUURLO_MATERIAL)
    exact_fixture=dense_native_fixture(legacy_obj); validate_native_material_schema(exact_fixture)

    with tempfile.TemporaryDirectory(prefix='animo_io01_mat_') as td:
        work=Path(td)
        exact_out=run_probe(a.exact_probe,exact_fixture,work,'material_exact')
        exact_obj=parse_native_material_probe_output(exact_out,'TTUTILNativeMaterialAdapter/v1 exact-numeric probe')
        exact_equal=semantic_projection(legacy_obj)==semantic_projection(exact_obj)

        typed_result=None
        if a.typed_probe:
            typed_fixture=dense_native_typed_double_fixture(legacy_obj); validate_native_material_schema(typed_fixture)
            typed_out=run_probe(a.typed_probe,typed_fixture,work,'material_typed_double')
            typed_obj=parse_native_material_probe_output(typed_out,'TTUTIL 4.27 typed DOUBLE probe')
            lp=semantic_projection(legacy_obj); tp=semantic_projection(typed_obj); mm=numeric_mismatches(lp,tp)
            typed_result={
                'field_exact_equivalent':lp==tp,'numeric_mismatch_count':len(mm),
                'max_ulp_distance':max((x['ulp_distance'] for x in mm),default=0),
                'max_absolute_difference':max((x['absolute_difference'] for x in mm),default=0.0),
                'mismatches':mm,
                'decision':'REJECT_TYPED_DOUBLE_FOR_FIELD_EXACT_REPRESENTATION' if mm else 'NO_MISMATCH_OBSERVED',
            }

    result={
      'schema':'ANIMO-IO01/MATERIALPilotQualification/v1',
      'result':'PASS' if exact_equal else 'FAIL',
      'decision':'QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS' if exact_equal else 'NOT_QUALIFIED',
      'scope':{'case':'RuurloGrass','family':'MATERIAL','IPO':0,'Ioptae':0,'IoptGHG':0,'normalized_schema':'MaterialParameterSet/v1','physics_executed':False,'GHG_admitted':False},
      'source_identity':{
        'testbank_sha256':test_hash,'ruurlo_material_member_sha256':sha256_bytes(material_bytes),'ttutil_zip_sha256':tt_hash,'ttutil_version':'4.27',
        'exact_probe_sha256':sha256_file(a.exact_probe),'typed_probe_sha256':sha256_file(a.typed_probe) if a.typed_probe else None,
      },
      'exact_numeric_native_adapter':{
        'adapter_id':'TTUTILNativeMaterialAdapter/v1','transport':'TTUTIL CHARACTER scalar/array tokens plus explicit REAL(8) numeric conversion',
        'field_exact_equivalent':exact_equal,'native_key_count':len(validate_native_material_schema(exact_fixture)),'numeric_tolerance_used':False,
      },
      'typed_ttutil_double_comparison':typed_result,
      'legacy_contract_evidence':{
        'sparse_omitted_FR_FRca_normalization':'ZERO_BY_EXACT_RUURLO_OLD_NEW_LINEAGE_EQUIVALENCE',
        'ipo0_Frpo_Pofr_input_presence':'FEATURE_INACTIVE_NULL','ipo0_trailing_defmat_deffra_columns':'LEXICAL_RESIDUE_NOT_ACTIVE_P_FIELDS',
      },
      'runtime_hazard_exclusions':[
        'revision-53 sparse FR/FRca omitted cells are read without explicit source initialization; intended zero semantics are lineage-qualified but legacy storage mechanism is not',
        'revision-53 Pofr(Frno) is range-checked when IPO=0 after a zero-element implied-DO input, so the checked runtime value is not input-defined',
      ],
      'non_admissions':{'production_migration':False,'GHG_schema':False,'binary_hydrology':False,'model_output_equivalence':False,'B4':False},
    }
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'; print(text,end='')
    if a.output: a.output.write_text(text,encoding='utf-8')
    return 0 if result['result']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
