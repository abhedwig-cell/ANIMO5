#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('source_zip',type=Path)
ap.add_argument('output_dir',type=Path)
ap.add_argument('--compiler',default='gfortran')
args=ap.parse_args()
SRCZIP=args.source_zip.resolve(); OUT=args.output_dir.resolve(); COMPILER=args.compiler
EXPECTED='183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566'
FLAGS=['-ffree-form','-ffree-line-length-none','-fallow-argument-mismatch','-std=legacy','-fdefault-real-8','-fdefault-double-8','-fno-automatic']
LINK=['-Wl,--build-id=none']
EX={'input1_1.for','Outselorg.for'}
OUTSEL_PATTERN=re.compile(r"\(\(\s*([A-Za-z0-9_]+\(Drn\),Comma)\s*\),\s*Drn=1,Nudr\)")
DFPORT='''module dfport\n  implicit none\ncontains\n  real(4) function secnds(x)\n    real(4), intent(in) :: x\n    real(4) :: t\n    call cpu_time(t)\n    secnds = t - x\n  end function secnds\nend module dfport\n'''
INTR='''integer(8) function kint(x)\n  real(4), intent(in) :: x\n  kint = int(x, kind=8)\nend function kint\ninteger(8) function kidnnt(x)\n  real(8), intent(in) :: x\n  kidnnt = nint(x, kind=8)\nend function kidnnt\n'''

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def run(cmd,cwd,log):
    r=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Path(log).write_text(r.stdout)
    if r.returncode: raise SystemExit(f'FAIL {cmd}\n{r.stdout[-5000:]}')

if sha(SRCZIP)!=EXPECTED: raise SystemExit('source archive SHA mismatch')
if OUT.exists(): shutil.rmtree(OUT)
src=OUT/'src'; obj=OUT/'obj'; logs=OUT/'logs'; src.mkdir(parents=True); obj.mkdir(); logs.mkdir()
with zipfile.ZipFile(SRCZIP) as z:
    for m in z.infolist():
        if m.is_dir(): continue
        rel=Path(*Path(m.filename).parts[1:])
        if not rel.parts: continue
        t=src/rel; t.parent.mkdir(parents=True,exist_ok=True); t.write_bytes(z.read(m))
for a,o in [('param.inc','Param.inc'),('Param.Inc','Param.inc'),('animo.inc','Animo.inc'),('Animo.Inc','Animo.inc')]:
    (src/a).write_bytes((src/o).read_bytes())

# TCD-018 execution-copy patch. This is qualification tooling only, not a production patch.
p=src/'Animo.for'; s=p.read_text(encoding='latin1')
old='''     &       Corurvnh,Corurvni,CorurvDOM,CorurvDON,Corurvpo,CorurvDOP,  &\n     &        Snla)    '''
new='''     &       Corurvnh,Corurvni,CorurvDOM,CorurvDON,Corurvpo,CorurvDOP,  &\n     &        Sic,Sict,Snla)    '''
if s.count(old)!=1: raise SystemExit('Animo call patch seam count !=1')
p.write_text(s.replace(old,new),encoding='latin1',newline='')

p=src/'Outbal_calc.for'; s=p.read_text(encoding='latin1')
if s.count(old)!=1: raise SystemExit('Outbal signature seam count !=1')
s=s.replace(old,new)
old_decl='''      Real :: Snla\n'''; new_decl='''      Real :: Sic,Sict,Snla\n'''
if s.count(old_decl)!=1: raise SystemExit('declaration seam !=1')
s=s.replace(old_decl,new_decl)
old_local='''      Real :: BtomDissi,Btot,CumAmN2Onitr,Dum,Dumi,Fahu,Fdom,Ffom,FHlp, & \n     &        Latist,NhNitr,Nudayr,OmCH4,T,Z , sum1, sum2                 ! GHG  \n'''
new_local='''      Real :: BtomDissi,Btot,CumAmN2Onitr,Dum,Dumi,Fahu,Fdom,Ffom,FHlp, & \n     &        Latist,NhNitr,Nudayr,OmCH4,T,Z , sum1, sum2                 ! GHG  \n      Real, Save :: Tcd018IcCu(Maba) = 0.0d0\n'''
if s.count(old_local)!=1: raise SystemExit('local seam !=1')
s=s.replace(old_local,new_local)
old_acc='''        Ln1 = Balnmi(Ly)\n        Ln2 = Balnma(Ly)\n\n!.....                Water (balance terms in mm)                 ......\n'''
new_acc='''        Ln1 = Balnmi(Ly)\n        Ln2 = Balnma(Ly)\n\n        If (Ln1 .Eq. 0) Tcd018IcCu(Ly) = Tcd018IcCu(Ly) + (Sict-Sic)*1.d3\n\n!.....                Water (balance terms in mm)                 ......\n'''
if s.count(old_acc)!=1: raise SystemExit('accumulation seam !=1')
s=s.replace(old_acc,new_acc)
old_fin='''          Bawadvcu(Ly) = Bawadvcu(Ly) + Bawa(Ddev,Ly)\n        End If\n'''
new_fin='''          If (Ln1 .Eq. 0) Bawa(Ddev,Ly) = Bawa(Ddev,Ly) - Tcd018IcCu(Ly)\n          Bawadvcu(Ly) = Bawadvcu(Ly) + Bawa(Ddev,Ly)\n          If (Ln1 .Eq. 0) Tcd018IcCu(Ly) = 0.0d0\n        End If\n'''
if s.count(old_fin)!=1: raise SystemExit('finalization seam !=1')
p.write_text(s.replace(old_fin,new_fin),encoding='latin1',newline='')

# Same frozen GNU portability contract as tools/build_gnu_diagnostic.py.
text=(src/'Outsel.for').read_text(encoding='latin1')
patch,n=OUTSEL_PATTERN.subn(r'(\1,Drn=1,Nudr)',text)
if n!=14: raise SystemExit(f'expected 14 Outsel substitutions, got {n}')
(src/'Outsel_gnu.for').write_text(patch,encoding='latin1',newline='')
(src/'dfport_shim.f90').write_text(DFPORT)
(src/'intel_intrinsics_shim.f90').write_text(INTR)
base=[COMPILER,*FLAGS,'-I','.','-I','../obj','-J','../obj']; objs=[]
for shim in ['dfport_shim.f90','intel_intrinsics_shim.f90']:
    o=f'../obj/{Path(shim).stem}.o'; run([*base,'-c',shim,'-o',o],src,logs/f'{shim}.log'); objs.append(f'obj/{Path(shim).stem}.o')
names=sorted([p.name for p in src.iterdir() if p.suffix.lower() in {'.for','.f90'} and p.name not in EX and p.name not in {'Outsel_gnu.for','dfport_shim.f90','intel_intrinsics_shim.f90'}],key=str.lower)
if len(names)!=58: raise SystemExit(f'expected 58 compilation units, got {len(names)}')
for name in names:
    cn='Outsel_gnu.for' if name=='Outsel.for' else name; o=f'../obj/{Path(name).stem}.o'
    run([*base,'-c',cn,'-o',o],src,logs/f'{name}.log'); objs.append(f'obj/{Path(name).stem}.o')
run([COMPILER,*objs,*LINK,'-o','animo_tcd018'],OUT,logs/'link.log')
actual=sha(OUT/'animo_tcd018')
expected_candidate='c1e281d5ceaa45952dc7ee21041454fbfab5bee34aa8aee09d59604b75826bbe'
if actual!=expected_candidate: raise SystemExit('candidate executable SHA mismatch: '+actual)
print('candidate',actual)
