#!/usr/bin/env python3
import argparse, hashlib, json, os, re, zipfile
from decimal import Decimal

def tokens(line):
    return line.split("!",1)[0].replace(","," ").split()

def d(token):
    return Decimal(token.replace("D","E").replace("d","e"))

def find_label(lines,label):
    for i,line in enumerate(lines):
        if line[:8] == label:
            return i+1
    raise ValueError(f"missing label {label}")

def read_array(lines,idx,count):
    values=[]
    while len(values)<count:
        if idx>=len(lines): raise ValueError("unexpected EOF")
        row=tokens(lines[idx]); idx+=1
        if not row: continue
        values.extend(row)
    if len(values)!=count:
        raise ValueError("legacy array READ has extra tokens in final consumed record")
    return [d(x) for x in values],idx

def read_record(lines,idx,count):
    while idx<len(lines):
        row=tokens(lines[idx]); idx+=1
        if not row: continue
        if len(row)<count: raise ValueError("short record")
        return [d(x) for x in row[:count]],idx
    raise ValueError("unexpected EOF")

def check(vals,lo,hi):
    lo,hi=Decimal(lo),Decimal(hi)
    return all(lo<=x<=hi for x in vals)

def general_meta(z,case):
    candidates=[n for n in z.namelist() if len(n.split("/"))>2 and n.split("/")[1]==case and os.path.basename(n).lower()=="general.inp"]
    if len(candidates)!=1: raise ValueError(f"{case}: GENERAL.INP cardinality {len(candidates)}")
    text=z.read(candidates[0]).decode("latin1")
    ipo=re.search(r"(?mi)^PhosphorusCycle\s*=\s*([01])",text)
    start=re.search(r"(?mi)^StartDate\s*=\s*(\d{4})-",text)
    end=re.search(r"(?mi)^EndDate\s*=\s*(\d{4})-",text)
    if not (ipo and start and end): raise ValueError(f"{case}: required GENERAL metadata missing")
    sy,ey=int(start.group(1)),int(end.group(1))
    return int(ipo.group(1)),ey-sy+1,sy,ey

def scan_case(z,path):
    raw=z.read(path); lines=raw.decode("latin1").splitlines(); case=path.split("/")[1]
    ipo,nuyr,sy,ey=general_meta(z,case)
    oi=find_label(lines,">optibc:")
    opts,oi=read_record(lines,oi,2); opts=[int(x) for x in opts]
    ti=find_label(lines,">topbou:")
    nh,ti=read_array(lines,ti,nuyr); ni,ti=read_array(lines,ti,nuyr)
    po=[]
    if ipo: po,ti=read_array(lines,ti,nuyr)
    ddnh,ti=read_array(lines,ti,nuyr); ddni,ti=read_array(lines,ti,nuyr)
    run_m,ti=read_record(lines,ti,2); run_po=[]
    if ipo: run_po,ti=read_record(lines,ti,1)
    run_org,ti=read_record(lines,ti,2); run_dop=[]
    if ipo: run_dop,ti=read_record(lines,ti,1)
    irr_m,ti=read_record(lines,ti,2); irr_po=[]
    if ipo: irr_po,ti=read_record(lines,ti,1)
    irr_org,ti=read_record(lines,ti,2); irr_dop=[]
    if ipo: irr_dop,ti=read_record(lines,ti,1)
    li=find_label(lines,">latbou:")
    lat_m,li=read_record(lines,li,2); lat_po=[]
    if ipo: lat_po,li=read_record(lines,li,1)
    lat_org,li=read_record(lines,li,2); lat_dop=[]
    if ipo: lat_dop,li=read_record(lines,li,1)

    checks={
      "precip_nh":check(nh,"0","1"),"precip_ni":check(ni,"0","1"),
      "dry_nh":check(ddnh,"0","100"),"dry_ni":check(ddni,"0","100"),
      "runon_mineral":check(run_m,"0","999"),"runon_org":check(run_org,"0","10"),
      "irrigation_mineral":check(irr_m,"0","999"),"irrigation_org":check(irr_org,"0","10"),
      "lateral_mineral":check(lat_m,"0","1"),"lateral_doma":check([lat_org[0]],"0","10"),
      "lateral_don":check([lat_org[1]],"0","1")
    }
    if ipo:
      checks.update({
        "precip_po":check(po,"0","1"),"runon_po":check(run_po,"0","999"),
        "runon_dop":check(run_dop,"0","10"),"irrigation_po":check(irr_po,"0","999"),
        "irrigation_dop":check(irr_dop,"0","10"),"lateral_po":check(lat_po,"0","1"),
        "lateral_dop":check(lat_dop,"0","0.1")
      })
    labels=[line[:8] for line in lines if len(line)>=8 and line.startswith(">")]
    return {
      "case":case,"path":path,"sha256":hashlib.sha256(raw).hexdigest(),
      "ipo":ipo,"nuyr":nuyr,"start_year":sy,"end_year":ey,
      "ioptidti":opts[0],"ioptirti":opts[1],"labels":labels,
      "all_source_ranges_pass":all(checks.values()),"range_checks":checks
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("testbank_zip")
    ap.add_argument("--output")
    args=ap.parse_args()
    raw=open(args.testbank_zip,"rb").read()
    with zipfile.ZipFile(args.testbank_zip) as z:
      paths=[n for n in z.namelist() if os.path.basename(n).lower()=="boundary.inp"]
      cases=[scan_case(z,n) for n in paths]
    result={
      "schema":"ANIMO-BOUNDQ01/NaturalStaticBoundaryAudit/v1",
      "testbank_sha256":hashlib.sha256(raw).hexdigest(),
      "case_count":len(cases),
      "all_static_options":all(c["ioptidti"]==0 and c["ioptirti"]==0 for c in cases),
      "all_source_ranges_pass":all(c["all_source_ranges_pass"] for c in cases),
      "phosphorus_modes":sorted(set(c["ipo"] for c in cases)),
      "cases":cases,
      "numeric_evidence":"DECIMAL_LEXICAL_RANGE_AUDIT_NOT_BINARY64_RUNTIME_EQUIVALENCE",
      "historical_b2":False
    }
    text=json.dumps(result,indent=2)+"\n"
    if args.output: open(args.output,"w",encoding="utf-8").write(text)
    else: print(text,end="")

if __name__=="__main__":
    main()
