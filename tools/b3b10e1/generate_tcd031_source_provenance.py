#!/usr/bin/env python3
import argparse, hashlib, json, re, sys, zipfile
from pathlib import Path

ARCHIVE_SHA="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
PREFIX="ANIMO_4.1.5.53/"
EVD=Path("integration/animo-b3/tcd031-source-provenance")

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(",",":"))+"\n"
def norm(b): return b.decode("latin-1").replace("\r\n","\n").replace("\r","\n")
def nlines(b): return [x.rstrip() for x in norm(b).split("\n")]
def slice_bytes(ls,a,b): return ("\n".join(ls[a-1:b])+"\n").encode()
def fail(msg): raise AssertionError(msg)

def active_lines(ls,a,b):
    return [x for x in ls[a-1:b] if x.strip() and not x.lstrip().startswith("!")]
def inactive_lines(ls,a,b):
    return [x for x in ls[a-1:b] if x.lstrip().startswith("!")]
def has_all(text,*tokens):
    low=text.lower()
    return all(t.lower() in low for t in tokens)

def check_probe(p, members, all_source_names, z):
    member=p["source_member"]
    if member not in z.namelist(): fail(f"missing probe member {member}")
    data=z.read(member)
    if sha(data)!=p["member_sha256"]: fail(f"member hash mismatch for {p['probe_id']}")
    ls=nlines(data); a,b=p["line_range"]
    if sha(slice_bytes(ls,a,b))!=p["normalized_slice_sha256"]: fail(f"slice hash mismatch for {p['probe_id']}")
    text="\n".join(ls[a-1:b]); pid=p["probe_id"]
    if pid=="SRC-MAPO-001" and not has_all(text,">mpnitr:","compnh(1)","compnh(2)","compni(1)","compni(2)"): fail(pid)
    if pid=="SRC-MAPO-002" and not has_all(text,">mporgs:","compdiorma(1)","compdiorma(2)","compdiorni(1)","compdiorni(2)"): fail(pid)
    if pid=="SRC-MAPO-003" and not has_all(text,">mpphos:","comppo(1)","comppo(2)","compdiorpo(1)","compdiorpo(2)"): fail(pid)
    if pid=="SRC-MAPO-004" and not has_all(text,"if (ipo.eq.1) then",">mpphos:"): fail(pid)
    if pid=="SRC-OUTINIT-001":
        if active_lines(ls,a,b) or not has_all(text,"ioptmp","compdiorma","compdiorni","compdiorpo","compnh","compni","comppo"): fail(pid)
    if pid=="SRC-OUTINIT-002":
        if active_lines(ls,a,b) or not has_all(text,">mpnitr:",">mporgs:",">mpphos:"): fail(pid)
    if pid=="SRC-ANIMO-001":
        if not any(re.search(r"^\s*Call\s+Output_Init\b",x,re.I) for x in active_lines(ls,a,b)): fail(pid)
        if not has_all("\n".join(inactive_lines(ls,a,b)),"compdiorma","compdiorni","compdiorpo","compnh","compni","comppo"): fail(pid)
    if pid=="SRC-INIT-001" and not has_all(text,"if (yr.eq.yrmi .and. stnu.eq.1)","if (ioptmp.eq.1) then"): fail(pid)
    if pid=="SRC-INIT-002":
        for q in p["pairs"]:
            pat=re.escape(q["destination"])+r"\s*=\s*"+re.escape(q["source"])
            if not re.search(pat,text,re.I): fail(f"{pid}:{q['destination']}")
    if pid=="SRC-RSCOMP-001":
        rx=re.compile(r"^\s*RsCoMp(?:DiorMa|DiorNi|DiorPo|Nh|Ni|Po)\s*\([^)]*\)\s*=",re.I)
        writes=[]
        for full in all_source_names:
            for i,line in enumerate(nlines(z.read(full)),1):
                if not line.lstrip().startswith("!") and rx.search(line): writes.append((full,i))
        if writes or p["family_specific_direct_write_count"]!=0: fail(f"{pid}: direct writes {writes}")
        an=z.read(PREFIX+"Animo.for"); als=nlines(an)
        init=[i for i,x in enumerate(als,1) if re.search(r"^\s*Call\s+Init\b",x,re.I) and not x.lstrip().startswith("!")]
        tc=[i for i,x in enumerate(als,1) if re.search(r"^\s*Call\s+Transca\b",x,re.I) and not x.lstrip().startswith("!")]
        tg=[i for i,x in enumerate(als,1) if re.search(r"^\s*Call\s+Transgen\b",x,re.I) and not x.lstrip().startswith("!")]
        if not(init and tc and tg and init[0]<min(tc+tg)): fail(f"{pid}: call order")
    if pid=="SRC-RSCOMP-002":
        for n in (PREFIX+"input1.for",PREFIX+"mapoinput.for"):
            for i,x in enumerate(nlines(z.read(n)),1):
                if "rscomp" in x.lower() and not x.lstrip().startswith("!"): fail(f"{pid}: active RsCoMp input reference {n}:{i}")
        if not has_all(text,"call mapoinput","(4","ipo"): fail(pid)
    if pid=="SRC-HYDRO-001" and not has_all(text,"nupa.eq.2","srwamp(1)","srwamp(2)","srwampcp(1","srwampcp(2"): fail(pid)
    if pid=="SRC-HYDRO-002" and not has_all(text,"nupa.eq.5","srwamp(1)","srwamp(2)","srwampcp(1","srwampcp(2"): fail(pid)
    if pid=="SRC-HYDRO-003" and not has_all(text,"srwampold","srwampcpold"): fail(pid)
    if pid=="SRC-ITREC-001" and not re.search(r"ItRec\s*\([^)]*\)\s*=\s*0",text,re.I): fail(pid)
    if pid=="SRC-ITREC-002" and not has_all(text,"itrec(1,iter)","+ 1"): fail(pid)

def main():
    ap=argparse.ArgumentParser(description="Replay license-safe TCD-031 frozen-source provenance evidence without redistributing source text.")
    ap.add_argument("archive"); ap.add_argument("--output-dir",required=True); ap.add_argument("--repo-root")
    a=ap.parse_args(); archive=Path(a.archive); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    root=Path(a.repo_root) if a.repo_root else Path(__file__).resolve().parents[2]
    if sha(archive.read_bytes())!=ARCHIVE_SHA: fail("frozen archive SHA-256 mismatch")
    spec_probe=json.loads((root/EVD/"PROBE_OUTPUT.json").read_text())
    spec_own=json.loads((root/EVD/"OWNERSHIP_MAP.json").read_text())
    if spec_probe["scope"]!="SOURCE_PROVENANCE_REMEDIATION": fail("scope")
    if spec_probe["persistent_state"]!={"domains":[1,2],"p_off_scalar_count":8,"p_on_scalar_count":12,"phosphorus_condition":"Ipo.EQ.1"}: fail("persistent-state contract")
    required={"CoMpDiorMa","CoMpDiorNi","CoMpNh","CoMpNi","CoMpDiorPo","CoMpPo","RsCoMp*","AvCoMp*","AvCoML*","MpReKo*","ItRec","SrWaMpOld","SrWaMp","SrWaMpCp","SrWaMpCpOld"}
    if {x["family"] for x in spec_own["families"]}!=required: fail("ownership map incomplete")
    with zipfile.ZipFile(archive) as z:
        source=[n for n in z.namelist() if n.startswith(PREFIX) and n.lower().endswith((".for",".inc")) and not n.endswith("/")]
        idx=[{"source_member":n,"member_sha256":sha(z.read(n)),"byte_count":len(z.read(n))} for n in sorted(source,key=str.lower)]
        idx_hash=sha(canon(idx).encode())
        if spec_probe["source_scan"]!={"index_sha256":idx_hash,"member_count":len(idx)}: fail("full source index mismatch")
        for p in spec_probe["probes"]: check_probe(p,None,source,z)
        for f in spec_own["families"]:
            d=f["declared_in"]; dat=z.read(d["member"])
            if sha(dat)!=d["member_sha256"]: fail(f"ownership member hash: {f['family']}")
            ln=d.get("line") or d.get("line_range",[None])[0]
            if ln and f["family"].rstrip("*").lower() not in nlines(dat)[ln-1].lower() and f["family"] not in ("MpReKo*",): fail(f"ownership declaration line: {f['family']}")
        files={"SOURCE_MEMBER_INDEX.json":idx,"PROBE_OUTPUT.json":spec_probe,"OWNERSHIP_MAP.json":spec_own}
        hashes={}
        for name,obj in files.items():
            b=canon(obj).encode(); (out/name).write_bytes(b); hashes[name]=sha(b)
        replay={"archive_sha256":ARCHIVE_SHA,"command":"python tools/b3b10e1/generate_tcd031_source_provenance.py /path/to/ANIMO_4.1.5.53(3).zip --output-dir /tmp/b3b10e1","comparison":"Compare SHA-256 of all three generated JSON files with the committed manifest. Any mismatch is FAIL_CLOSED.","outputs":hashes,"source_exposure":"No frozen source text is emitted or required to be committed.","workunit":"ANIMO-B3B10E1"}
        (out/"REPLAY_INSTRUCTIONS.json").write_text(canon(replay))
        print(json.dumps({"archive_sha256":ARCHIVE_SHA,"member_count":len(idx),"probe_count":len(spec_probe["probes"]),"outputs":hashes},indent=2))

if __name__=="__main__":
    try: main()
    except (AssertionError,KeyError,ValueError,zipfile.BadZipFile) as e:
        print(f"FAIL_CLOSED: {e}",file=sys.stderr); sys.exit(2)
