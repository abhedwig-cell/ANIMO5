#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, shutil, struct, subprocess, zipfile
from pathlib import Path

EXPECTED_SOURCE_ZIP_SHA256='183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566'
EXPECTED_MEMBER_HASHES={
 'MAPOTRANSPORT.FOR':'735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da',
 'Transsub.for':'c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552',
 'Param.inc':'20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475',
}
SPECIES=['DOM','DON','NH4','NO3','DOP','PO4']
FLAGS=['-ffree-form','-ffree-line-length-none','-fallow-argument-mismatch','-std=legacy','-fdefault-real-8','-fdefault-double-8','-fno-automatic']


def sha256_bytes(data: bytes)->str: return hashlib.sha256(data).hexdigest()
def sha256(path: Path)->str: return sha256_bytes(path.read_bytes())
def run(cmd, cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if p.returncode:
        raise SystemExit(f'command failed {p.returncode}: {cmd}\n{p.stdout}')
    return p.stdout

def parse_trace(path:Path):
    data=path.read_bytes()
    if len(data)%100: raise SystemExit(f'bad trace length {path}: {len(data)}')
    recs=[]
    for off in range(0,len(data),100):
        step=struct.unpack_from('<i',data,off)[0]
        vals=struct.unpack_from('<12d',data,off+4)
        recs.append({'step':step,'accepted':vals[0:2],'result':vals[2:4],'water':vals[4:6],
                     'average':vals[6:8],'mpreko':vals[8:10],'toin':vals[10:12]})
    return recs

def mutate_checkpoint_drop_domain(src:Path,dst:Path,domain:int):
    b=bytearray(src.read_bytes())
    # magic 8, version 4, split step 4, then two REAL(8) accepted concentrations.
    off=16+(domain-1)*8
    b[off:off+8]=struct.pack('<d',0.0)
    dst.write_bytes(b)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source_zip',type=Path)
    ap.add_argument('driver_source',type=Path)
    ap.add_argument('workdir',type=Path)
    ap.add_argument('--compiler',default='gfortran')
    args=ap.parse_args()
    source_zip=args.source_zip.resolve(); driver=args.driver_source.resolve(); wd=args.workdir.resolve()
    if sha256(source_zip)!=EXPECTED_SOURCE_ZIP_SHA256: raise SystemExit('source zip hash mismatch')
    if wd.exists(): shutil.rmtree(wd)
    src=wd/'src'; runs=wd/'runs'; src.mkdir(parents=True); runs.mkdir()
    with zipfile.ZipFile(source_zip) as z:
        roots={Path(n).parts[0] for n in z.namelist() if n and not n.endswith('/')}
        if len(roots)!=1: raise SystemExit('unexpected source root')
        root=next(iter(roots))
        for name in EXPECTED_MEMBER_HASHES:
            data=z.read(f'{root}/{name}')
            (src/name).write_bytes(data)
            if sha256_bytes(data)!=EXPECTED_MEMBER_HASHES[name]: raise SystemExit(f'member hash mismatch: {name}')
    # Compile a qualification copy under stable relative filenames. Frozen bytes are verified above and not modified.
    for name in ('MAPOTRANSPORT.FOR','Transsub.for','Param.inc'):
        shutil.copy2(src/name, wd/name)
    # Revision 53 assumes case-insensitive include lookup. Add only a build-copy alias.
    shutil.copy2(wd/'Param.inc', wd/'param.inc')
    shutil.copy2(driver,wd/'stateq04_mptransp_driver.f90')
    compiler_version=run([args.compiler,'--version'],wd).splitlines()[0]
    common=[args.compiler,*FLAGS,'-I','.']
    run([*common,'-c','MAPOTRANSPORT.FOR','-o','MAPOTRANSPORT.o'],wd)
    run([*common,'-c','Transsub.for','-o','Transsub.o'],wd)
    run([*common,'-c','stateq04_mptransp_driver.f90','-o','driver.o'],wd)
    run([args.compiler,'MAPOTRANSPORT.o','Transsub.o','driver.o','-Wl,--build-id=none','-o','stateq04_driver'],wd)
    exe=wd/'stateq04_driver'
    result={'workunit':'ANIMO-STATEQ04','tcd':'TCD-031','evidence_class':'FROZEN_SOURCE_KERNEL_REMEDIATION_QUALIFICATION_NOT_WHOLE_MODEL',
            'source_zip_sha256':EXPECTED_SOURCE_ZIP_SHA256,'source_member_sha256':EXPECTED_MEMBER_HASHES,
            'driver_sha256':sha256(driver),'compiler':compiler_version,'compile_flags':FLAGS,
            'executable_sha256':sha256(exe),'split_after_accepted_step':5,'post_restore_steps_compared':5,
            'comparison_policy':'EXACT_BYTEWISE_NO_TOLERANCE','species':{},'all_species_exact':True,
            'all_native_bad_controls_diverge':True,'all_domain_drop_controls_diverge':True}
    for sp in SPECIES:
        cp=runs/f'{sp}.chk'; cont=runs/f'{sp}_continuous.bin'; a=runs/f'{sp}_stageA.bin'; good=runs/f'{sp}_stageB_good.bin'; bad=runs/f'{sp}_stageB_bad.bin'
        for mode,tr in [('continuous',cont),('stageA',a),('stageB-good',good),('stageB-nativebad',bad)]:
            run([str(exe),mode,sp,str(cp),str(tr)],wd)
            warn=wd/'stateq04_mptransp_warnings.log'
            shutil.copy2(warn,runs/f'{sp}_{mode}.warn')
        cb=cont.read_bytes(); ab=a.read_bytes(); gb=good.read_bytes(); bb=bad.read_bytes()
        prefix=(ab==cb[:len(ab)]); exact=(gb==cb[len(ab):]); bad_div=(bb!=cb[len(ab):])
        if not(prefix and exact and bad_div): raise SystemExit(f'primary discriminator failed for {sp}')
        c_recs=parse_trace(cont); g_recs=parse_trace(good); b_recs=parse_trace(bad)
        drop={}
        for d in (1,2):
            dcp=runs/f'{sp}_drop_d{d}.chk'; dout=runs/f'{sp}_drop_d{d}.bin'
            mutate_checkpoint_drop_domain(cp,dcp,d)
            run([str(exe),'stageB-good',sp,str(dcp),str(dout)],wd)
            diverges=dout.read_bytes()!=cb[len(ab):]
            if not diverges: raise SystemExit(f'domain-drop control did not diverge: {sp} d{d}')
            drop[f'domain_{d}']={'diverges':True,'suffix_sha256':sha256(dout),'checkpoint_sha256':sha256(dcp)}
        warns={p.name:p.stat().st_size for p in runs.glob(f'{sp}_*.warn')}
        if any(warns.values()): raise SystemExit(f'unexpected kernel warning bytes for {sp}: {warns}')
        result['species'][sp]={
            'stageA_prefix_exact':prefix,'stageB_good_suffix_exact':exact,'native_bad_suffix_diverges':bad_div,
            'accepted_at_split':c_recs[4]['accepted'],'first_post_restore_step':g_recs[0]['step'],
            'first_post_restore_good_abs_diff':[abs(x-y) for x,y in zip(c_recs[5]['accepted'],g_recs[0]['accepted'])],
            'first_post_restore_native_bad_abs_diff':[abs(x-y) for x,y in zip(c_recs[5]['accepted'],b_recs[0]['accepted'])],
            'continuous_suffix_sha256':sha256_bytes(cb[len(ab):]),'good_suffix_sha256':sha256(good),
            'native_bad_suffix_sha256':sha256(bad),'checkpoint_sha256':sha256(cp),'warning_bytes':warns,
            'domain_drop_controls':drop}
    out=wd/'STATEQ04_KERNEL_SPLIT_RESULT.json'
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
