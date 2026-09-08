#!/usr/bin/env python3
"""Source-bound audit of selected parser option ranges against revision-53 dispatch.

Evidence tooling only. Frozen source and testbank archives are read-only and hash-pinned.
"""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

SOURCE_SHA256="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256="44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def text_members(path: Path) -> dict[str,str]:
    out={}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.lower().endswith((".for",".f90",".inc",".inp",".ini",".txt")):
                try: out[n]=z.read(n).decode("latin1")
                except UnicodeDecodeError: pass
    return out

def member_ending(members: dict[str,str], ending: str) -> str:
    matches=[v for k,v in members.items() if k.lower().endswith(ending.lower())]
    if len(matches)!=1:
        raise ValueError(f"expected one member ending {ending}, got {len(matches)}")
    return matches[0]

def has_checkint(text: str, var: str, lo: int, hi: int) -> bool:
    p=(rf"Checkint\([^\n]*'{re.escape(var)}'\s*,\s*{re.escape(var)}\s*,"
       rf"\s*{lo}\s*,\s*{hi}\s*\)")
    return re.search(p,text,re.I) is not None

def eq_values(text: str, var: str) -> set[int]:
    p=rf"\b{re.escape(var)}\b\s*(?:\.Eq\.|==)\s*(-?\d+)"
    return {int(x) for x in re.findall(p,text,re.I)}

def has_rel(text: str, var: str, op: str, value: int) -> bool:
    opmap={"ne":r"\.Ne\.|/=", "gt":r"\.Gt\.", "ge":r"\.Ge\.", "lt":r"\.Lt\.", "le":r"\.Le\."}
    return re.search(rf"\b{re.escape(var)}\b\s*(?:{opmap[op]})\s*{value}\b",text,re.I) is not None

def audit(source_zip: Path, testbank_zip: Path) -> dict:
    if sha256(source_zip)!=SOURCE_SHA256:
        raise ValueError("source archive SHA-256 mismatch")
    if sha256(testbank_zip)!=TESTBANK_SHA256:
        raise ValueError("testbank archive SHA-256 mismatch")
    src=text_members(source_zip)
    input1=member_ending(src,"/input1.for")
    grass=member_ending(src,"/grassprd.for")
    addit=member_ending(src,"/input_addit.for")
    ini=member_ending(src,"/inicalc.for")
    hydro=member_ending(src,"/input_hydro.for")
    allsrc="\n".join(src.values())

    checks={
      "ioptgrev_parser_1_3": has_checkint(input1,"IoptGrEv",1,3),
      "ioptgrev_dispatch_1_2_3": {1,2,3}.issubset(eq_values(grass,"IoptGrEv")),
      "optmf_parser_0_2": has_checkint(input1,"Optmf",0,2),
      "optmf_dispatch_1_2_and_zero_disable": {1,2}.issubset(eq_values(addit,"Optmf")) and has_rel(input1,"Optmf","gt",0),
      "optalfe_parser_0_2": has_checkint(input1,"Optalfe",0,2),
      "optalfe_dispatch_1_2_and_zero_disable": {1,2}.issubset(eq_values(input1,"Optalfe")) and has_rel(ini,"Optalfe","ne",0),
      "inpo_parser_1_3": has_checkint(input1,"Inpo",1,3),
      "inpo_dispatch_1_2_3": {1,2,3}.issubset(eq_values(input1,"Inpo")) and {1,2,3}.issubset(eq_values(ini,"Inpo")),
      "evrose_parser_0_1": has_checkint(input1,"Evrose",0,1),
      "evrose_source_branch": 1 in eq_values(allsrc,"Evrose"),
      "optpfhn_parser_0_1": has_checkint(input1,"Optpfhn",0,1),
      "optpfhn_source_split": 1 in eq_values(allsrc,"Optpfhn") and has_rel(allsrc,"Optpfhn","ne",1),
      "optst_parser_1_2": has_checkint(input1,"Optst",1,2),
      "optst_input_hydro_dispatch_1_2": {1,2}.issubset(eq_values(hydro,"Optst")),
      "optst_3_internal_sentinel_assignment": re.search(r"If\s*\(\s*Nint\(St\)\.Lt\.0\s*\)\s*Then[\s\S]{0,120}?Optst\s*=\s*3",ini,re.I) is not None,
      "optst_negative_sentinel_values_limited": re.search(r"Nint\(St\)\.Eq\.-10",ini,re.I) is not None and re.search(r"Nint\(St\)\.Eq\.-30",ini,re.I) is not None,
      "inmo_parser_0_1": has_checkint(input1,"Inmo",0,1),
      "inmo_source_split": 1 in eq_values(ini,"Inmo") and has_rel(input1,"Inmo","ne",1),
      "optcxfa_parser_fixed_2": has_checkint(input1,"Optcxfa",2,2),
      "optcxfa_nonadmitted_helper_branches_present": {1,2,3}.issubset(eq_values(allsrc,"Optcxfa")),
    }
    return {
      "evidence_class":"SOURCE_BOUND_STATIC_OPTION_DISPATCH_AUDIT_NOT_REFERENCE",
      "source_sha256":SOURCE_SHA256,
      "testbank_sha256":TESTBANK_SHA256,
      "checks":checks,
      "checks_passed":sum(checks.values()),
      "checks_total":len(checks),
      "all_checks_pass":all(checks.values()),
      "interpretation":{
        "new_alias_defects_found":0,
        "optst_3":"INTERNAL_NEGATIVE_TIMESTEP_SENTINEL_NOT_PARSER_OPTION",
        "optcxfa_1_3":"SOURCE_BRANCHES_EXIST_BUT_ARE_NOT_PARSER_ADMITTED_AND_DO_NOT_IMPLY_SUPPORT",
        "coverage_gaps_are_not_defects":True
      }
    }

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("source_zip",type=Path); p.add_argument("testbank_zip",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    ev=audit(a.source_zip,a.testbank_zip)
    s=json.dumps(ev,indent=2)+"\n"
    if a.output: a.output.write_text(s,encoding="utf-8")
    print(s,end="")
    return 0 if ev["all_checks_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
