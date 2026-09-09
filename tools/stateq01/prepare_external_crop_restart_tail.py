#!/usr/bin/env python3
"""Prepare a qualification-only external-crop restart input tail for STATEQ01.

The adapter is intentionally explicit. It does not modify frozen testbank bytes.
It rebases the selected management continuation, yearly top-boundary vectors and
runtime start date around a supplied accepted-boundary checkpoint. External crop
and hydrology payloads remain byte-identical to the already prepared diagnostic
case copy.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil
from datetime import date
from pathlib import Path

def sha(p:Path):return hashlib.sha256(p.read_bytes()).hexdigest()

def parse_date(text,key):
 m=re.search(rf'(?m)^{re.escape(key)}\s*=\s*(\d{{4}}-\d{{2}}-\d{{2}})',text)
 if not m:raise SystemExit(f'missing {key}')
 return date.fromisoformat(m.group(1))

def update_aliases(root:Path,names:list[str],transform):
 seen=set()
 for p in root.rglob('*'):
  if p.is_file() and p.name.casefold() in {n.casefold() for n in names} and p.resolve() not in seen:
   seen.add(p.resolve()); transform(p)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('prepared_case',type=Path);ap.add_argument('checkpoint',type=Path);ap.add_argument('output_dir',type=Path)
 ap.add_argument('--checkpoint-tito',type=float,required=True);ap.add_argument('--restart-start-date',required=True);ap.add_argument('--next-add-number',type=int,required=True)
 a=ap.parse_args();base=a.prepared_case.resolve();cp=a.checkpoint.resolve();out=a.output_dir.resolve();restart=date.fromisoformat(a.restart_start_date)
 if out.exists():shutil.rmtree(out)
 shutil.copytree(base,out)
 # Remove generated root outputs but keep the direct file and input tree.
 for p in list(out.iterdir()):
  if p.is_file() and p.name.casefold()!='animo.ini':p.unlink()
 ini=next(p for p in out.iterdir() if p.is_file() and p.name.casefold()=='animo.ini')
 direct=ini.read_text(encoding='latin1')
 entries={m.group(1).upper():m.group(2) for m in re.finditer(r'(?m)^\s*([A-Za-z]{3})\s*=\s*"([^"]+)"',direct)}
 for key in ['GEN','MAN','BOU','INI','CRU','SWU']:
  if key not in entries:raise SystemExit(f'missing direct-file key {key}')
 restart_rel=Path(entries['INI']).parent/'stateq01_restart_initial.inp'
 direct=re.sub(r'(?m)^INI\s*=.*$',f'INI="{restart_rel.as_posix()}"',direct)
 ini.write_text(direct,encoding='latin1')
 restart_path=out/restart_rel;restart_path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(cp,restart_path)
 # General start date and original simulation years.
 gp=out/Path(entries['GEN']);g=gp.read_text(encoding='latin1');old_start=parse_date(g,'StartDate');old_end=parse_date(g,'EndDate')
 g=re.sub(r'(?m)^(StartDate\s*=\s*)\d{4}-\d{2}-\d{2}',rf'\g<1>{restart.isoformat()}',g);gp.write_text(g,encoding='latin1')
 # update any case-insensitive runtime alias of general file
 for p in gp.parent.iterdir():
  if p.is_file() and p.name.casefold()==gp.name.casefold() and p!=gp:p.write_text(g,encoding='latin1')
 old_nuyr=old_end.year-old_start.year+1;new_nuyr=old_end.year-restart.year+1;annual_offset=restart.year-old_start.year
 if annual_offset<0 or new_nuyr<=0:raise SystemExit('restart outside original period')
 # Checkpoint P activity. Output_Init restart is explicit Inpo=1 for this qualified route.
 cptext=cp.read_text(encoding='latin1')
 mi=re.search(r'(?ms)^>inipho:\s*\n\s*(\d+)',cptext);ipo=1 if mi and int(mi.group(1))==1 else 0
 if ipo!=1:raise SystemExit('adapter currently qualified only for explicit P-active Inpo=1 checkpoint')
 # Management tail.
 mp=out/Path(entries['MAN']);mtext=mp.read_text(encoding='latin1')
 lm=re.search(r'>lmanag:\s*\n\s*(\d+)\s*\n(?P<rows>.*?)(?=^>matvar:)',mtext,re.M|re.S)
 if not lm:raise SystemExit('lmanag not found')
 rows=[ln for ln in lm.group('rows').splitlines() if ln.strip()]
 retained=[]
 for ln in rows:
  parts=ln.split();yr=int(parts[2][:4])
  if yr>=restart.year:
   parts[0]=str(len(retained)+1)
   if yr==restart.year:parts[2]=restart.isoformat()
   retained.append(' '.join(parts))
 matvar=re.search(r'(?ms)^>matvar:.*?(?=^>add001:)',mtext)
 if not matvar:raise SystemExit('matvar not found')
 labels=list(re.finditer(r'(?m)^>add(\d+):\s*$',mtext));blocks={}
 for i,m in enumerate(labels):
  n=int(m.group(1));st=m.end();en=labels[i+1].start() if i+1<len(labels) else len(mtext);blocks[n]=mtext[st:en].strip('\n')
 n0=a.next_add_number
 if n0<=1 or n0 not in blocks or n0-1 not in blocks:raise SystemExit('next-add cursor unavailable')
 def blines(n):return [x for x in blocks[n].splitlines()]
 def trailer(n):
  xs=[x for x in blines(n) if x.strip()];return float(xs[-1].split()[0])
 outm=['>lmanag:',f'{len(retained):12d}',*retained,matvar.group(0).rstrip()]
 kept=sorted(n for n in blocks if n>=n0)
 for j,n in enumerate(kept,1):
  ls=blines(n);payload=ls[:-1]
  outm.append(f'>add{j:03d}:')
  if j==1:outm.append(f'{trailer(n-1)-a.checkpoint_tito:10.1f}')
  outm.extend(payload);outm.append(f'{trailer(n)-a.checkpoint_tito:10.1f}')
 new_m='\n'.join(outm)+'\n';mp.write_text(new_m,encoding='latin1')
 for p in mp.parent.iterdir():
  if p.is_file() and p.name.casefold()==mp.name.casefold() and p!=mp:p.write_text(new_m,encoding='latin1')
 # Yearly top-boundary vectors. Current qualified case has Ioptidti=Ioptirti=0 and P active.
 bp=out/Path(entries['BOU']);bt=bp.read_text(encoding='latin1');pre,rest=bt.split('>topbou:',1);block,post=rest.split('>latbou:',1)
 vals=[float(x) for x in block.split()]
 arrays=5 # Coprnh, Coprni, Coprpo, Drdepnh, Drdepni for P-active Inpo=1.
 expected=arrays*old_nuyr+12 # runoff and irrigation scalar records: 2,1,2,1 twice.
 if len(vals)!=expected:raise SystemExit(f'unexpected topbou token count {len(vals)} != {expected}')
 annual=[vals[i*old_nuyr:(i+1)*old_nuyr] for i in range(arrays)];scalars=vals[arrays*old_nuyr:]
 sel=[v[annual_offset:annual_offset+new_nuyr] for v in annual]
 lines=[]
 for v in sel:
  for i in range(0,len(v),4):lines.append(' '.join(f'{x:16.8E}' for x in v[i:i+4]))
 k=0
 for n in (2,1,2,1,2,1,2,1):
  row=scalars[k:k+n];k+=n;lines.append(' '.join(f'{x:16.8E}' for x in row))
 bp.write_text(pre+'>topbou:\n'+'\n'.join(lines)+'\n>latbou:'+post,encoding='latin1')
 # Hydrology and crop files are not altered by this tail adapter.
 manifest={
  'workunit':'ANIMO-STATEQ01','status':'QUALIFICATION_ONLY_EXTERNAL_CROP_RESTART_TAIL_PREPARED',
  'checkpoint_tito':a.checkpoint_tito,'restart_start_date':restart.isoformat(),'next_original_add_number':n0,
  'retained_management_periods':len(retained),'retained_add_blocks':len(kept),'first_rebased_event_coordinate':trailer(n0-1)-a.checkpoint_tito,
  'annual_boundary_offset_years':annual_offset,'annual_boundary_years':new_nuyr,'p_active_inpo1':True,
  'checkpoint_sha256':sha(cp),'restart_input_sha256':sha(restart_path),'management_sha256':sha(mp),'boundary_sha256':sha(bp),
  'hydrology_payload_modified_by_this_adapter':False,'external_crop_payload_modified_by_this_adapter':False,
  'canonical_state_admission':'NOT_ADMITTED','production_code':False,'physics_change':False,
  'qualification_boundary':'legacy input-tail adapter only; exact split behaviour must be tested independently'
 }
 (out/'STATEQ01_EXTERNAL_CROP_RESTART_TAIL.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
