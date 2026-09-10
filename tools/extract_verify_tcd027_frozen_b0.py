#!/usr/bin/env python3
"""Verify/rebind exact frozen-B0 source neighbourhood evidence for ANIMO-B3A01E."""
from __future__ import annotations
import argparse, base64, hashlib, json, re, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"integration/animo-b3/TCD027_FROZEN_B0_SOURCE_EVIDENCE_MANIFEST.json"
EXPECTED_ARCHIVE_SHA="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_MEMBER_SHA={
 "ANIMO_4.1.5.53/Outbal_calc.for":"4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981",
 "ANIMO_4.1.5.53/Outbal_write.for":"cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea",
}
def sha(b): return hashlib.sha256(b).hexdigest()
def lineslice(b,start,end): return b"".join(b.splitlines(keepends=True)[start-1:end])
def decode(rec): return base64.b64decode(rec["exact_bytes_base64"],validate=True)
def verify_committed(m):
 if m["frozen_b0"]["source_archive_sha256"]!=EXPECTED_ARCHIVE_SHA: raise AssertionError("manifest archive SHA drift")
 byid={}
 for rec in m["source_neighbourhoods"]:
  b=decode(rec)
  if sha(b)!=rec["sha256_exact_bytes"] or len(b)!=rec["size_bytes"]: raise AssertionError(f"neighbourhood identity mismatch: {rec['id']}")
  if b.count(b"\r\n") != rec["line_end_1"]-rec["line_start_1"]+1 or not b.endswith(b"\r\n"): raise AssertionError(f"CRLF identity mismatch: {rec['id']}")
  byid[rec["id"]]=b
 # Exact statements from the retained review's three missing source surfaces.
 p=byid["P_REDISTRIBUTION_TCD027_SEAM"].decode("ascii")
 for needle in ["Dum = Adexpl(I,Ln)*Pofrex*Z","Bafop(24,Ly)=bafop(25,Ly) + Dum","Bafop(26,Ly)=bafop(26,Ly)+ Addiorpopl(I,Ln) * Z","Bafop(27,Ly)=bafop(27,Ly) + Dum","Bafop(25,Ly)=bafop(25,Ly) + Dum"]:
  if needle not in p: raise AssertionError(f"P seam statement missing: {needle}")
 h=byid["ORGANIC_P_DETAILED_HEADER"].decode("ascii"); w=byid["ORGANIC_P_DETAILED_WRITE_RESET"].decode("ascii")
 if "'transfop'//chba(Ly)//'.Out'" not in h or "(Bafop(I,Ly),I=1,30)" not in w: raise AssertionError("detailed output binding missing")
 literals=re.findall(r"'([^']*)'",h)
 joined="".join(literals); marker=" yr      tito tiyr  "
 if marker not in joined: raise AssertionError("header marker missing")
 labels=joined.split(marker,1)[1].split()
 if len(labels)!=30: raise AssertionError("expected 30 detailed organic-P labels")
 for i,l in {24:"redis_EXP",25:"redis_OP",26:"redis_DOP",27:"redis_HUP"}.items():
  if labels[i-1]!=l: raise AssertionError(f"slot {i} mapping mismatch")
 return byid
def verify_archive(path,m):
 raw=path.read_bytes()
 if sha(raw)!=EXPECTED_ARCHIVE_SHA: raise AssertionError("FAIL_CLOSED_FROZEN_ARCHIVE_SHA_MISMATCH")
 with zipfile.ZipFile(path) as z:
  member_bytes={}
  for member,expected in EXPECTED_MEMBER_SHA.items():
   b=z.read(member); member_bytes[member]=b
   if sha(b)!=expected: raise AssertionError(f"FAIL_CLOSED_ARCHIVE_MEMBER_SHA_MISMATCH: {member}")
  for rec in m["source_neighbourhoods"]:
   actual=lineslice(member_bytes[rec["archive_member"]],rec["line_start_1"],rec["line_end_1"])
   if actual!=decode(rec): raise AssertionError(f"FAIL_CLOSED_ARCHIVE_NEIGHBOURHOOD_NOT_BYTE_IDENTICAL: {rec['id']}")
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--archive",type=Path); a=ap.parse_args()
 m=json.loads(MANIFEST.read_text()); verify_committed(m)
 if a.archive:
  verify_archive(a.archive,m); print("PASS_B3A01E_FROZEN_ARCHIVE_NEIGHBOURHOOD_REEXTRACTION")
 else: print("PASS_B3A01E_COMMITTED_FROZEN_SOURCE_NEIGHBOURHOOD_BYTES")
if __name__=="__main__":
 try: main()
 except Exception as e: print(f"FAIL_B3A01E_SOURCE_EVIDENCE: {e}",file=sys.stderr); raise SystemExit(1)
