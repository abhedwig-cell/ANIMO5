#!/usr/bin/env python3
import hashlib, pathlib, re, sys
p=pathlib.Path(sys.argv[1])
raw=p.read_bytes()
expected="f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a"
if hashlib.sha256(raw).hexdigest()!=expected:
    raise SystemExit("FAIL: vfproj SHA-256 mismatch")
text=raw.decode(errors="replace")
configs=re.findall(r'<Configuration Name="([^"]+)"[\s\S]*?<Tool Name="VFFortranCompilerTool"([^>]*)/>',text)
if len(configs)!=4:
    raise SystemExit(f"FAIL: expected 4 configurations, got {len(configs)}")
for name,attrs in configs:
    d=dict(re.findall(r'(\w+)="([^"]*)"',attrs))
    if d.get("RealKIND")!="realKIND8":
        raise SystemExit(f"FAIL: {name} RealKIND={d.get('RealKIND')}")
    if d.get("FloatingPointModel")!="source":
        raise SystemExit(f"FAIL: {name} FloatingPointModel={d.get('FloatingPointModel')}")
print("PASS_NQ06_SUPPLIED_VFPROJ_REAL_KIND_8_ALL_CONFIGURATIONS")
