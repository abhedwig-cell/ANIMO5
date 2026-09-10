#!/usr/bin/env python3
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path

BASE="36aad892cac546105dfec0fe43aa34a18e23bcad"
ARCHIVE_SHA="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
DISPOSITION="QUALIFIED_SOURCE_PROVENANCE_REMEDIATION_READY_FOR_TARGETED_INDEPENDENT_REREVIEW"
REQ_PROBES={"SRC-MAPO-001","SRC-MAPO-002","SRC-MAPO-003","SRC-MAPO-004","SRC-OUTINIT-001","SRC-OUTINIT-002","SRC-ANIMO-001","SRC-INIT-001","SRC-INIT-002","SRC-RSCOMP-001","SRC-RSCOMP-002","SRC-HYDRO-001","SRC-HYDRO-002","SRC-HYDRO-003","SRC-ITREC-001","SRC-ITREC-002"}
FAILED_GATES={"complete_source_level_ownership","native_mapoinput_loader","native_Output_Init_serialization_omission","native_Animo_Output_Init_call_surface","native_Init_restore_direction_and_timing","native_RsCoMp_pre_promotion_initialization"}
REQ_FAMILIES={"CoMpDiorMa","CoMpDiorNi","CoMpNh","CoMpNi","CoMpDiorPo","CoMpPo","RsCoMp*","AvCoMp*","AvCoML*","MpReKo*","ItRec","SrWaMpOld","SrWaMp","SrWaMpCp","SrWaMpCpOld"}
ALLOWED={
 ".github/workflows/animo-b3b10e1-tcd031-source-provenance.yml",
 "docs/b3/ANIMO_B3B10E1_TCD031_SOURCE_PROVENANCE_REMEDIATION.md",
 "integration/animo-b3/ANIMO-B3B10E1_CHECKPOINT.json",
 "integration/animo-b3/ANIMO-B3B10E1_MANIFEST.json",
 "integration/animo-b3/ANIMO-B3B10E1_STATUS.json",
 "integration/animo-b3/tcd031-source-provenance/SOURCE_MEMBER_INDEX.json",
 "integration/animo-b3/tcd031-source-provenance/PROBE_OUTPUT.json",
 "integration/animo-b3/tcd031-source-provenance/OWNERSHIP_MAP.json",
 "integration/animo-b3/tcd031-source-provenance/REPLAY_INSTRUCTIONS.json",
 "tools/b3b10e1/generate_tcd031_source_provenance.py",
 "tools/b3b10e1/validate_b3b10e1.py",
}
def fail(msg): raise AssertionError(msg)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--archive'); ap.add_argument('--skip-git-diff',action='store_true'); a=ap.parse_args()
 r=Path(a.repo_root).resolve(); ip=r/'integration/animo-b3'; ev=ip/'tcd031-source-provenance'
 manifest=load(ip/'ANIMO-B3B10E1_MANIFEST.json'); status=load(ip/'ANIMO-B3B10E1_STATUS.json'); probe=load(ev/'PROBE_OUTPUT.json'); own=load(ev/'OWNERSHIP_MAP.json')
 if manifest['workunit']!='ANIMO-B3B10E1' or status['disposition']!=DISPOSITION: fail('workunit/disposition mismatch')
 if manifest['exact_starting_head']!=BASE: fail('starting head mismatch')
 if manifest['frozen_source_archive']['sha256']!=ARCHIVE_SHA or probe['archive']['sha256']!=ARCHIVE_SHA: fail('archive SHA binding missing/mismatch')
 for fn,want in manifest['generated_artifacts'].items():
  if sha(ev/fn)!=want: fail(f'generated artifact hash mismatch: {fn}')
 ids={x['probe_id'] for x in probe['probes']}
 if ids!=REQ_PROBES: fail(f'probe set mismatch: missing={REQ_PROBES-ids}, extra={ids-REQ_PROBES}')
 byid={x['probe_id']:x for x in probe['probes']}
 for x in probe['probes']:
  if not x.get('source_member') or not x.get('member_sha256'): fail(f'unbound evidence record {x.get("probe_id")}')
  leaf=x['source_member'].split('/')[-1]
  if leaf in manifest['member_sha256_bindings'] and manifest['member_sha256_bindings'][leaf]!=x['member_sha256']: fail(f'member binding mismatch {leaf}')
 if set(manifest['failed_gate_evidence'])!=FAILED_GATES: fail('failed gate coverage set mismatch')
 for g,records in manifest['failed_gate_evidence'].items():
  if not records: fail(f'failed gate has no evidence: {g}')
  for rec in records:
   if rec.endswith('.json'): continue
   if rec not in ids: fail(f'failed gate {g} references unknown probe {rec}')
 c=manifest['structural_contract']; pc=probe['persistent_state']
 if (c['persistent_state_scalar_count_p_off'],c['persistent_state_scalar_count_p_on'])!=(8,12) or (pc['p_off_scalar_count'],pc['p_on_scalar_count'])!=(8,12): fail('persistent scalar counts mismatch')
 if c['domains']!=[1,2] or pc['domains']!=[1,2]: fail('both domains not explicit')
 if c['phosphorus_condition']!='Ipo.EQ.1' or byid['SRC-MAPO-004']['condition']!='Ipo.EQ.1': fail('phosphorus condition missing')
 if byid['SRC-OUTINIT-002']['active'] is not False: fail('native serialization omission not established as inactive')
 if byid['SRC-INIT-002']['direction']!='CoMp <- RsCoMp' or byid['SRC-INIT-001']['includes_first_active_timestep'] is not True: fail('native restore direction/timing incomplete')
 if byid['SRC-RSCOMP-001']['family_specific_direct_write_count']!=0 or byid['SRC-RSCOMP-002']['native_input_path_rscomp_reference_count']!=0: fail('native RsCoMp pre-promotion initialization evidence incomplete')
 fams={x['family'] for x in own['families']}
 if fams!=REQ_FAMILIES: fail(f'ownership incomplete: {REQ_FAMILIES-fams}')
 for x in own['families']:
  for k in ['producer_routines','consumer_routines','timestep_role','checkpoint_relevance','classification','evidence','declared_in']:
   if k not in x or x[k] in (None,[],{}): fail(f'ownership field missing {x["family"]}:{k}')
 guards=manifest['scope_guards']
 if any(guards.values()) or any(status['scope_guards'].values()): fail('scope guard violation')
 if status['scientific_admission'] or not status['atomic_b3_admission_blocked']: fail('scientific-admission boundary violated')
 if status['stateq04_reopen_required']: fail('STATEQ04 unexpectedly reopened')
 if status['tcd025']!='BLOCKED_PENDING_TCD031_INDEPENDENT_TIER_C_REVIEW_PASS': fail('TCD-025 guard changed')
 if not a.skip_git_diff:
  changed=subprocess.check_output(['git','diff','--name-only',BASE+'..HEAD'],cwd=r,text=True).splitlines()
  extra=set(changed)-ALLOWED
  if extra: fail('out-of-scope changed paths: '+', '.join(sorted(extra)))
  if not changed: fail('no remediation changes detected')
 if a.archive:
  apath=Path(a.archive)
  if sha(apath)!=ARCHIVE_SHA: fail('local replay archive SHA mismatch')
  with tempfile.TemporaryDirectory() as td:
   subprocess.run([sys.executable,str(r/'tools/b3b10e1/generate_tcd031_source_provenance.py'),str(apath),'--output-dir',td],check=True,stdout=subprocess.DEVNULL)
   for fn,want in manifest['generated_artifacts'].items():
    if fn=='REPLAY_INSTRUCTIONS.json': continue
    if sha(Path(td)/fn)!=want: fail(f'independent local replay output mismatch: {fn}')
 print('ANIMO-B3B10E1 package validation: PASS')
 print('Interpretation: source-provenance remediation package integrity only; NOT a scientific review PASS.')
 return 0
if __name__=='__main__':
 try: sys.exit(main())
 except Exception as e:
  print('FAIL_CLOSED:',e,file=sys.stderr); sys.exit(2)
