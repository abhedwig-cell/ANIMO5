#!/usr/bin/env python3
"""ANIMO-STATEQ01 qualification-only external-crop split-window scan.

Builds the hash-pinned revision-53 GNU diagnostic executable in an execution
copy, adds read-only surface and management-event observers, prepares the three
known successful external-crop testbank cases without changing scientific input
values, executes them, and finds exact-zero-surface candidate checkpoint
boundaries.

This tool produces diagnostic readiness evidence only. It does not admit
canonical STATE/TIME and it does not modify frozen source or testbank bytes.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, struct, subprocess, zipfile
from datetime import date, timedelta
from pathlib import Path

SOURCE_SHA256="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256="44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
CASES=["GrassPeat","LWKM_gras_1040.2021.2045","STONE_akk_0006.2001.2015"]
FLAGS=["-ffree-form","-ffree-line-length-none","-fallow-argument-mismatch","-std=legacy","-fdefault-real-8","-fdefault-double-8","-fno-automatic"]
LINK=["-Wl,--build-id=none"]
EXCLUDE={"input1_1.for","Outselorg.for"}
OUTSEL_PATTERN=re.compile(r"\(\(\s*([A-Za-z0-9_]+\(Drn\),Comma)\s*\),\s*Drn=1,Nudr\)")
DFPORT="""module dfport
  implicit none
contains
  real(4) function secnds(x)
    real(4), intent(in) :: x
    real(4) :: t
    call cpu_time(t)
    secnds=t-x
  end function secnds
end module dfport
"""
INTEL="""integer(8) function kint(x)
  real(4), intent(in) :: x
  kint=int(x,kind=8)
end function kint
integer(8) function kidnnt(x)
  real(8), intent(in) :: x
  kidnnt=nint(x,kind=8)
end function kidnnt
"""
PATH_LINE=re.compile(r'^\s*([A-Za-z]{3})\s*=\s*"([^"]+)"')
PRINT_BAL_LABEL=re.compile(r"(?im)^(\s*PrintBalLabel\s*=\s*)'([^'\r\n]{1,2})'")
INPUT_KEYS={"GEN","MAT","PLA","SOI","BOU","INI","MAN","SWU","WAI","WAU","CHE","CRU"}
HEADER=0x4B; TRAILER=0x82; CONT=0x81

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):h.update(c)
    return h.hexdigest()

def run(cmd,cwd,timeout=240):
    return subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)

def extract_single_root(z:Path,out:Path):
    with zipfile.ZipFile(z) as a:
        members=[m for m in a.infolist() if not m.is_dir()]
        roots={Path(m.filename).parts[0] for m in members}
        if len(roots)!=1: raise SystemExit(f"unexpected archive root layout: {roots}")
        root=next(iter(roots))
        for m in members:
            rel=Path(*Path(m.filename).parts[1:])
            if rel.parts:
                p=out/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(a.read(m))
        return root

def find_ci(root:Path,rel:Path):
    cur=root
    for part in rel.parts:
        exact=cur/part
        if exact.exists():cur=exact;continue
        ms=[p for p in cur.iterdir() if p.name.casefold()==part.casefold()]
        if len(ms)!=1:return None
        cur=ms[0]
    return cur

def parse_ps(data:bytes):
    if not data or data[0]!=HEADER or data[-1]!=TRAILER: raise ValueError('not PowerStation framing')
    pos=1; records=[]; cur=bytearray()
    while pos<len(data):
        m=data[pos]; pos+=1
        if m==TRAILER:
            if cur or pos!=len(data): raise ValueError('bad trailer')
            return records
        ln=128 if m==CONT else m
        cur.extend(data[pos:pos+ln]); pos+=ln
        if data[pos]!=m: raise ValueError('block marker mismatch')
        pos+=1
        if m!=CONT: records.append(bytes(cur));cur.clear()
    raise ValueError('missing trailer')

def enc_gnu(records):
    out=bytearray()
    for r in records: out+=struct.pack('<i',len(r))+r+struct.pack('<i',len(r))
    return bytes(out)

def prepare_case(testbank_dir:Path,case:str,out:Path):
    src=testbank_dir/case
    if not src.is_dir(): raise SystemExit(f'missing case {case}')
    shutil.copytree(src,out)
    ini=next((p for p in out.iterdir() if p.is_file() and p.name.casefold()=='animo.ini'),None)
    if ini is None: raise SystemExit(f'{case}: no animo.ini')
    t=ini.read_text(encoding='latin1').replace('\\','/')
    ini.write_text(t,encoding='latin1')
    entries={}
    for ln in t.splitlines():
        m=PATH_LINE.match(ln)
        if m:entries[m.group(1).upper()]=m.group(2)
    for k,v in entries.items():
        target=out/Path(v)
        if k in INPUT_KEYS:
            source=find_ci(out,Path(v))
            if source is None or not source.is_file():
                if k not in {'WAI','WAU'}: raise SystemExit(f'{case}: unresolved {k}={v}')
                continue
            if source!=target:
                target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        else: target.parent.mkdir(parents=True,exist_ok=True)
    gp=out/Path(entries['GEN'])
    g=gp.read_text(encoding='latin1'); g,n=PRINT_BAL_LABEL.subn(r'\1\2',g); gp.write_text(g,encoding='latin1')
    hyd=out/Path(entries['SWU']); b=hyd.read_bytes()
    if b and b[0]==HEADER and b[-1]==TRAILER:hyd.write_bytes(enc_gnu(parse_ps(b)))
    return ini,entries

def stlen(tiyr:float,yr:int)->float:
    # Exact branch transcription of revision-53 Function.for:Stlen.
    for b,v in [(364,10),(353,11),(343,10),(333,10),(323,10),(313,10),(303,10),(292,11),(282,10),(272,10),(262,10),(252,10),(242,10),(231,11),(221,10),(211,10),(200,11),(190,10),(180,10),(170,10),(160,10),(150,10),(139,11),(129,10),(119,10),(109,10),(99,10),(89,10),(78,11),(68,10),(58,10)]:
        if tiyr>b:return float(v)
    if tiyr>49:
        leap=yr%4==0 and (yr%100!=0 or yr%400==0)
        return 9.0 if leap else 8.0
    if tiyr>40:return 10.0
    if tiyr>30:return 10.0
    if tiyr>20:return 11.0
    return 10.0

def parse_trace(path:Path):
    return [[float(x) for x in ln.split()] for ln in path.read_text().splitlines() if ln.strip()]

def analyze(case_dir:Path,entries):
    g=(case_dir/Path(entries['GEN'])).read_text(encoding='latin1')
    sd=date.fromisoformat(re.search(r'(?m)^StartDate\s*=\s*(\d{4}-\d{2}-\d{2})',g).group(1))
    ed=date.fromisoformat(re.search(r'(?m)^EndDate\s*=\s*(\d{4}-\d{2}-\d{2})',g).group(1))
    crop=int(re.search(r'(?m)^CropUptakeModel\s*=\s*(\d+)',g).group(1))
    if crop!=1: raise SystemExit(f'{case_dir.name}: not external crop')
    surf=parse_trace(case_dir/'stateq01_surface_trace.csv')
    mg=parse_trace(case_dir/'stateq01_management_trace.csv')
    events={r[0] for r in mg}
    def zero(r):return r[1]+r[2]==0.0 and r[3]+r[4]==0.0
    def dt(t):return sd+timedelta(days=int(round(t))-1)
    runs=[]; start=None
    for i in range(len(surf)+1):
        q=i<len(surf) and zero(surf[i])
        if q and start is None:start=i
        if not q and start is not None:runs.append((start,i-1));start=None
    eligible=[]; crop_compatible=[]
    for i in range(1,len(surf)-1):
        trip=surf[i-1:i+2]
        if not all(zero(r) for r in trip):continue
        if any(r[0] in events for r in trip):continue
        dates=[dt(r[0]) for r in trip]
        if len({d.year for d in dates})!=1:continue
        eligible.append(i)
        next_d=dates[2]; delta=trip[2][0]-trip[1][0]
        if delta==stlen(next_d.timetuple().tm_yday-1,next_d.year):crop_compatible.append(i)
    return {
      'start_date':sd.isoformat(),'end_date':ed.isoformat(),'surface_records':len(surf),
      'strict_zero_records':sum(zero(r) for r in surf),'management_events':len(mg),
      'zero_runs':[{'records':b-a+1,'tito_start':surf[a][0],'tito_end':surf[b][0],'date_start':dt(surf[a][0]).isoformat(),'date_end':dt(surf[b][0]).isoformat()} for a,b in sorted(runs,key=lambda x:x[1]-x[0],reverse=True)],
      'strict_neighbor_non_event_same_year_candidates':len(eligible),
      'external_crop_start_compatible_candidates':len(crop_compatible),
      '_candidate_indices':crop_compatible,'_surf':surf,'_dt':dt
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source_zip',type=Path);ap.add_argument('testbank_zip',type=Path);ap.add_argument('output_dir',type=Path);ap.add_argument('--output-json',type=Path)
    a=ap.parse_args(); source=a.source_zip.resolve(); testbank=a.testbank_zip.resolve(); out=a.output_dir.resolve()
    if sha(source)!=SOURCE_SHA256:raise SystemExit('source hash mismatch')
    if sha(testbank)!=TESTBANK_SHA256:raise SystemExit('testbank hash mismatch')
    if out.exists():shutil.rmtree(out)
    src=out/'src';obj=out/'obj';cases=out/'cases';src.mkdir(parents=True);obj.mkdir();cases.mkdir()
    extract_single_root(source,src)
    for alias,orig in [('param.inc','Param.inc'),('Param.Inc','Param.inc'),('animo.inc','Animo.inc'),('Animo.Inc','Animo.inc')]:shutil.copy2(src/orig,src/alias)
    text=(src/'Outsel.for').read_bytes().decode('latin1'); patched,n=OUTSEL_PATTERN.subn(r'(\1,Drn=1,Nudr)',text)
    if n!=14:raise SystemExit(f'Outsel substitutions {n}')
    (src/'Outsel_gnu.for').write_text(patched,encoding='latin1',newline='')
    (src/'dfport_shim.f90').write_text(DFPORT);(src/'intel_intrinsics_shim.f90').write_text(INTEL)
    # Exact observer injection counts fail closed.
    hp=src/'Hydro_detailed.for'; h=hp.read_text(encoding='latin1')
    needle='      End If\n      Mofro(0) = Amax1(0.0,(Pn+Snla)  / He(0))'
    if h.count(needle)!=1:raise SystemExit('surface observer seam changed')
    h=h.replace(needle,"      End If\n! STATEQ01 execution-copy observer: no model-state assignment.\n      Open(Unit=98,File='stateq01_surface_trace.csv',Status='Unknown',Position='Append')\n      Write(98,'(F24.12,1X,5(ES24.16,1X),I2)') Tito,Pn,Snla,Pnt,Snt,St,Flpn\n      Close(98)\n      Mofro(0) = Amax1(0.0,(Pn+Snla)  / He(0))")
    hp.write_text(h,encoding='latin1',newline='')
    an=src/'Animo.for'; s=an.read_text(encoding='latin1')
    needle='            If(Juda.ge.Tinead .and. (Juda-St).lt.Tinead) Then\n              Call Input_addit'
    if s.count(needle)!=1:raise SystemExit('management observer seam changed')
    s=s.replace(needle,"            If(Juda.ge.Tinead .and. (Juda-St).lt.Tinead) Then\n! STATEQ01 execution-copy management-event observer: no model-state assignment.\n              Open(Unit=97,File='stateq01_management_trace.csv',Status='Unknown',Position='Append')\n              Write(97,'(4(ES24.16,1X))') Tito,St,Juda,Tinead\n              Close(97)\n              Call Input_addit")
    an.write_text(s,encoding='latin1',newline='')
    compiler=subprocess.run(['gfortran','--version'],text=True,stdout=subprocess.PIPE,check=True).stdout.splitlines()[0]
    base=['gfortran',*FLAGS,'-I','.', '-I','../obj','-J','../obj']; objects=[]
    for shim in ['dfport_shim.f90','intel_intrinsics_shim.f90']:
        on=f'../obj/{Path(shim).stem}.o';p=run([*base,'-c',shim,'-o',on],src); 
        if p.returncode:
            raise SystemExit(p.stdout)
        objects.append('obj/'+Path(shim).stem+'.o')
    names=sorted([p.name for p in src.iterdir() if p.suffix.lower() in {'.for','.f90'} and p.name not in EXCLUDE and p.name not in {'Outsel_gnu.for','dfport_shim.f90','intel_intrinsics_shim.f90'}],key=str.lower)
    if len(names)!=58:raise SystemExit(f'legacy units {len(names)}')
    for nm in names:
        cn='Outsel_gnu.for' if nm=='Outsel.for' else nm; on=f'../obj/{Path(nm).stem}.o';p=run([*base,'-c',cn,'-o',on],src)
        if p.returncode:
            raise SystemExit(p.stdout)
        objects.append('obj/'+Path(nm).stem+'.o')
    exe=out/'animo_external_crop_window';p=run(['gfortran',*objects,*LINK,'-o',str(exe)],out)
    if p.returncode:raise SystemExit(p.stdout)
    # extract testbank under normalized root for case copies
    tb=out/'testbank';tb.mkdir();root=extract_single_root(testbank,tb)
    result={'workunit':'ANIMO-STATEQ01','status':'PASS_EXTERNAL_CROP_EXACT_ZERO_SUBWINDOW_SCAN_SPLIT_BEHAVIOUR_NOT_QUALIFIED','evidence_class':'B0_HASH_PINNED_DIAGNOSTIC_OBSERVER_EXECUTION_NOT_B2','canonical_state_admission':'NOT_ADMITTED','canonical_time_admission':'NOT_ADMITTED','production_code':False,'physics_change':False,'source_archive_sha256':SOURCE_SHA256,'testbank_sha256':TESTBANK_SHA256,'compiler':compiler,'compiler_flags':FLAGS,'observer_executable_sha256':sha(exe),'cases':{}}
    analyses={}
    for case in CASES:
        cd=cases/case;ini,entries=prepare_case(tb,case,cd)
        for t in ['stateq01_surface_trace.csv','stateq01_management_trace.csv']:
            q=cd/t
            if q.exists():q.unlink()
        p=run([str(exe),ini.name],cd,timeout=240)
        if 'Successful completion of simulation' not in p.stdout:raise SystemExit(f'{case} failed: {p.stdout[-2000:]}')
        z=analyze(cd,entries);analyses[case]=z
        result['cases'][case]={k:v for k,v in z.items() if not k.startswith('_')}
    # deterministic selection: highest strict-zero fraction, then longest zero run; first crop-compatible candidate in midpoint year.
    def score(c):
        z=analyses[c];return (z['strict_zero_records']/z['surface_records'],z['zero_runs'][0]['records'])
    chosen=max(CASES,key=score);z=analyses[chosen];mid=(int(z['start_date'][:4])+int(z['end_date'][:4]))//2
    indices=[i for i in z['_candidate_indices'] if z['_dt'](z['_surf'][i][0]).year==mid]
    if not indices:raise SystemExit('no midpoint-year crop-compatible candidate')
    i=indices[0];r=z['_surf'][i];prev=z['_surf'][i-1];nxt=z['_surf'][i+1]
    result['selected_candidate']={'case':chosen,'selection_rule':'highest strict-zero fraction; then longest zero run; earliest external-crop-start-compatible strict non-event candidate in midpoint calendar year','midpoint_year':mid,'row_index_zero_based':i,'checkpoint_tito':r[0],'checkpoint_end_date':z['_dt'](r[0]).isoformat(),'restart_start_date':(z['_dt'](r[0])+timedelta(days=1)).isoformat(),'previous_tito':prev[0],'next_tito':nxt[0],'next_step_length':nxt[0]-r[0],'surface_storage_exact_zero':True,'neighbor_surface_storage_exact_zero':True,'management_event_at_previous_current_next':False,'same_calendar_year_previous_current_next':True,'external_crop_input_start_check_compatible':True,'hidden_epsilon_used':False}
    text=json.dumps(result,indent=2)+'\n';target=a.output_json or out/'EXTERNAL_CROP_WINDOW_SCAN.json';target.write_text(text);print(text,end='')
if __name__=='__main__':main()
