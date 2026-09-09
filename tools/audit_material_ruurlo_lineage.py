#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, zipfile
from decimal import Decimal
from pathlib import Path

TESTBANK_SHA256='44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84'
OLD='ANIMO_testbank/RuurloGrass/Input/MATERIAL_oud.INP'
NEW='ANIMO_testbank/RuurloGrass/Input/MATERIAL.INP'


def sha256_file(p: Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def sha256_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def d(tok:str)->Decimal:return Decimal(tok.replace('D','E').replace('d','e'))
def c(x:Decimal)->str:
    if x==0:return '0'
    return format(x.normalize(),'f')

def section_lines(text:str,label:str)->list[str]:
    lines=text.splitlines(); idx=None
    for i,line in enumerate(lines):
        if line[:8].lower()==label.lower(): idx=i+1;break
    if idx is None: raise ValueError(f'missing {label}')
    out=[]
    for line in lines[idx:]:
        if line.startswith('>'): break
        st=line.strip()
        if not st or st.startswith('-') or st.startswith('!'): continue
        if st[0] not in '+-.0123456789': continue
        out.append(st)
    return out

def parse_old(text:str):
    ls=section_lines(text,'>defmat:'); nm=int(ls[0].split()[0])
    vals=[d(t) for line in ls[1:4] for t in line.split()]
    if len(vals)!=3*nm: raise ValueError(('old defmat',len(vals),nm))
    fror=vals[:nm]; frnh=vals[nm:2*nm]; frni=vals[2*nm:]
    ls=section_lines(text,'>orgmat:'); nf=int(ls[0].split()[0])
    data=[[d(t) for t in line.split()] for line in ls[1:1+2*nm]]
    if len(data)!=2*nm or any(len(row)!=nf for row in data): raise ValueError('old orgmat dimensions')
    fr=data[:nm]; frca=data[nm:]; hufros=d(ls[1+2*nm].split()[0])
    ls=section_lines(text,'>orgdec:')
    asfa=[d(t) for t in ls[0].split()]; trio=[d(t) for t in ls[1].split()]
    frhetero=d(ls[2].split()[0]); recfav=[d(t) for t in ls[3].split()]
    rates=[d(t) for t in ls[4].split()]; recfdeav=d(ls[5].split()[0])
    if len(asfa)!=nf or len(trio)!=3 or len(recfav)!=nf or len(rates)!=4: raise ValueError('old orgdec dimensions')
    asfaca,asfahu,asfaex=trio; recfcaav,recfhuav,recfexav,recfntav=rates
    ls=section_lines(text,'>orgnit:')
    nifr=[d(t) for t in ls[0].split()]; n_tail=[d(t) for t in ls[1].split()]
    if len(nifr)!=nf or len(n_tail)!=2: raise ValueError('old orgnit dimensions')
    nifrhuma,nifrex=n_tail
    return locals()

def parse_new(text:str):
    ls=section_lines(text,'>defmat:'); nm=int(ls[0].split()[0]); rows=[]
    for line in ls[1:1+nm]:
        t=line.split()
        if len(t)<5: raise ValueError('new defmat row short')
        rows.append((int(t[0]),int(t[1]),d(t[2]),d(t[3]),d(t[4]),[d(x) for x in t[5:]]))
    fror=[r[2] for r in rows]; frnh=[r[3] for r in rows]; frni=[r[4] for r in rows]
    defmat_residues=[r[5] for r in rows]
    cfracom=d(section_lines(text,'>orgcom:')[0].split()[0])
    ls=section_lines(text,'>deffra:'); nf=int(ls[0].split()[0]); frows=[]
    for line in ls[1:1+nf]:
        t=line.split()
        if len(t)<6: raise ValueError('new deffra row short')
        frows.append((int(t[0]),d(t[1]),d(t[2]),d(t[3]),d(t[4]),d(t[5]),[d(x) for x in t[6:]]))
    recfav=[r[1] for r in frows]; hufros=[r[2] for r in frows]; ratio_rd_st=[r[3] for r in frows]
    asfa=[r[4] for r in frows]; nifr=[r[5] for r in frows]; deffra_residues=[r[6] for r in frows]
    recfexav,hufrosex,asfaex,nifrex,pofrex=[d(t) for t in section_lines(text,'>defexu:')[0].split()]
    recfcaav,sdofr,asfaca=[d(t) for t in section_lines(text,'>defdom:')[0].split()]
    recfsdoav,asfasdo=[d(t) for t in section_lines(text,'>defsdo:')[0].split()]
    recfhuav,recfhusdoav,asfahu,nifrhuma,pofrhuma=[d(t) for t in section_lines(text,'>defhum:')[0].split()]
    recfntav=d(section_lines(text,'>defntr:')[0].split()[0])
    recfdeav,frhetero=[d(t) for t in section_lines(text,'>defden:')[0].split()]
    ls=section_lines(text,'>matfra:'); tokens=[]
    for line in ls: tokens.extend(line.split())
    pos=0; fr=[[Decimal(0) for _ in range(nf)] for _ in range(nm)]
    frca=[[Decimal(0) for _ in range(nf)] for _ in range(nm)]; sparse=[]
    for expected_mn in range(1,nm+1):
        mn=int(tokens[pos]); nufr=int(tokens[pos+1]); pos+=2
        triples=[]
        if mn!=expected_mn: raise ValueError(f'new matfra material order/index {mn}!={expected_mn}')
        seen=set()
        for _ in range(nufr):
            fn=int(tokens[pos]); fv=d(tokens[pos+1]); cv=d(tokens[pos+2]); pos+=3
            if fn in seen: raise ValueError('duplicate sparse fraction')
            seen.add(fn)
            if not 1<=fn<=nf: raise ValueError('fraction out of range')
            fr[mn-1][fn-1]=fv; frca[mn-1][fn-1]=cv; triples.append([fn,c(fv),c(cv)])
        sparse.append({'material':mn,'NuFR':nufr,'triples':triples})
    if pos!=len(tokens): raise ValueError(f'unconsumed matfra tokens {len(tokens)-pos}')
    return locals()

def eq_seq(a,b): return len(a)==len(b) and all(x==y for x,y in zip(a,b))
def eq_matrix(a,b): return len(a)==len(b) and all(eq_seq(x,y) for x,y in zip(a,b))

def audit(zpath:Path):
    actual=sha256_file(zpath)
    if actual!=TESTBANK_SHA256: raise ValueError(f'testbank hash mismatch {actual}')
    with zipfile.ZipFile(zpath) as z:
        oldb=z.read(OLD); newb=z.read(NEW)
    old=parse_old(oldb.decode('latin-1')); new=parse_new(newb.decode('latin-1'))
    checks={
      'Nm':old['nm']==new['nm'], 'Nf':old['nf']==new['nf'],
      'Fror':eq_seq(old['fror'],new['fror']), 'Frnh':eq_seq(old['frnh'],new['frnh']), 'Frni':eq_seq(old['frni'],new['frni']),
      'FR_full_matrix_after_sparse_zero_fill':eq_matrix(old['fr'],new['fr']),
      'FRca_full_matrix_after_sparse_zero_fill':eq_matrix(old['frca'],new['frca']),
      'Hufros_old_scalar_expands_to_all_new_fractions':all(v==old['hufros'] for v in new['hufros']),
      'Asfa':eq_seq(old['asfa'],new['asfa']), 'Asfaca':old['asfaca']==new['asfaca'], 'Asfahu':old['asfahu']==new['asfahu'], 'Asfaex':old['asfaex']==new['asfaex'],
      'Frhetero':old['frhetero']==new['frhetero'], 'Recfav':eq_seq(old['recfav'],new['recfav']), 'Recfcaav':old['recfcaav']==new['recfcaav'], 'Recfhuav':old['recfhuav']==new['recfhuav'], 'Recfexav':old['recfexav']==new['recfexav'], 'Recfntav':old['recfntav']==new['recfntav'], 'Recfdeav':old['recfdeav']==new['recfdeav'],
      'Nifr':eq_seq(old['nifr'],new['nifr']), 'Nifrhuma':old['nifrhuma']==new['nifrhuma'], 'Nifrex':old['nifrex']==new['nifrex'],
    }
    sparse_count=sum(item['NuFR'] for item in new['sparse'])
    return {
      'schema':'ANIMO-IO01/RuurloMaterialLineageAudit/v1', 'result':'PASS' if all(checks.values()) else 'FAIL',
      'evidence_class':'CROSS_VERSION_NATURAL_CASE_LINEAGE_EVIDENCE_NOT_RUNTIME_REFERENCE',
      'testbank_sha256':actual,
      'files':{'old':{'path':OLD,'sha256':sha256_bytes(oldb)},'revision53':{'path':NEW,'sha256':sha256_bytes(newb)}},
      'dimensions':{'Nm':new['nm'],'Nf':new['nf'],'full_matrix_cells_each':new['nm']*new['nf'],'sparse_explicit_triplets':sparse_count,'sparse_omitted_cells_each':new['nm']*new['nf']-sparse_count},
      'checks':checks,
      'sparse_zero_rule':{
        'status':'SUPPORTED_BY_EXACT_NATURAL_CASE_LINEAGE_EQUIVALENCE',
        'old_full_FR_equals_new_sparse_FR_zero_filled':checks['FR_full_matrix_after_sparse_zero_fill'],
        'old_full_FRca_equals_new_sparse_FRca_zero_filled':checks['FRca_full_matrix_after_sparse_zero_fill'],
        'normalization_candidate':'omitted (material,fraction) sparse entries normalize to numeric zero',
        'runtime_implementation_dependency_separate':True,
      },
      'ipo0_lexical_residue':{
        'new_defmat_rows_with_trailing_values':sum(bool(x) for x in new['defmat_residues']),
        'new_deffra_rows_with_trailing_values':sum(bool(x) for x in new['deffra_residues']),
        'interpretation':'revision-53 implied-DO consumes zero P elements when IPO=0; trailing lexical columns are not active Frpo/Pofr input values',
      },
      'revision53_only_or_restructured_fields':{
        'Cfracom':c(new['cfracom']),'Ratio_rd_st_unique':sorted({c(v) for v in new['ratio_rd_st']}), 'Hufrosex':c(new['hufrosex']), 'SDOfr':c(new['sdofr']), 'RecfSDOav':c(new['recfsdoav']), 'AsfaSDO':c(new['asfasdo']), 'RecfHUSDOav':c(new['recfhusdoav']), 'Pofrex':c(new['pofrex']), 'Pofrhuma':c(new['pofrhuma'])
      }
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('testbank_zip',type=Path); ap.add_argument('--output',type=Path)
    a=ap.parse_args(); r=audit(a.testbank_zip); s=json.dumps(r,indent=2,sort_keys=True)+'\n'; print(s,end='')
    if a.output: a.output.write_text(s,encoding='utf-8')
    return 0 if r['result']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
