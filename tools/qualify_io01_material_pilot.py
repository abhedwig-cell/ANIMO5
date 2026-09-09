#!/usr/bin/env python3
"""Reproduce ANIMO-IO01 bounded MATERIAL Pilot B from frozen user-supplied archives.

The runner:
1. verifies the frozen ANIMO testbank and SWAP 4.3.1 package;
2. materializes exact embedded TTUTIL 4.27 against the committed manifest;
3. builds all 153 TTUTIL units and both MATERIAL probes;
4. verifies Python normalization of every numeric lexeme in the natural Ruurlo
   MATERIAL file against GNU Fortran external list-directed REAL(8) conversion;
5. proves the CHARACTER-token TTUTIL adapter is field-exact;
6. records the bounded 1-ULP failure of direct TTUTIL DOUBLE conversion.

No model physics is executed.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, io, json, re, shutil, struct, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/"tools"

def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(f"cannot load {path}")
    mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod); return mod

material=_load("io01_material_pilot",TOOLS/"io01_material_pilot.py")
materializer=_load("materialize_ttutil427",TOOLS/"materialize_ttutil427.py")

TESTBANK_SHA256="44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
RUURLO_MATERIAL="ANIMO_testbank/RuurloGrass/Input/MATERIAL.INP"
RUURLO_MATERIAL_SHA256="03857e4681cc83fe84c054ac1b1e1cd3df91c9b5204f7f8bc70962d14033c507"
NUMERIC_TOKEN_RE=re.compile(r"(?<![\w.])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?")

def sha256_file(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def run(cmd,*,cwd=None):
    cp=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if cp.returncode: raise RuntimeError(f"command failed {cp.returncode}: {cmd}\n{cp.stdout}\n{cp.stderr}")
    return cp

def fortran_order(swap_zip):
    with zipfile.ZipFile(swap_zip,"r") as outer: inner=outer.read(materializer.EMBEDDED_PATH)
    with zipfile.ZipFile(io.BytesIO(inner),"r") as z:
        return [PurePosixPath(x.filename).name for x in z.infolist() if not x.is_dir() and PurePosixPath(x.filename).suffix.lower() in (".for",".f90")]

def build_ttutil_and_probes(swap_zip,source,build,exact_src,typed_src):
    compiler=shutil.which("gfortran")
    if compiler is None: raise RuntimeError("gfortran required")
    ar=shutil.which("ar")
    if ar is None: raise RuntimeError("ar required")
    compiler_version=run([compiler,"--version"]).stdout.splitlines()[0]
    build.mkdir(parents=True,exist_ok=True)
    order=fortran_order(swap_zip)
    if "ttutilprefs.f90" not in order: raise RuntimeError("official TTUTIL lacks ttutilprefs.f90")
    order=["ttutilprefs.f90",*[x for x in order if x!="ttutilprefs.f90"]]
    flags=["-c","-O0","-std=legacy","-fallow-argument-mismatch",f"-I{source}",f"-J{build}"]
    for name in order: run([compiler,*flags,str(source/name)],cwd=build)
    objects=sorted(build.glob("*.o"))
    if len(objects)!=153: raise RuntimeError(f"expected 153 TTUTIL objects, got {len(objects)}")
    lib=build/"libttutil427.a"; run([ar,"rcs",str(lib),*[str(x) for x in objects]],cwd=build)
    out={}
    for tag,src in (("exact",exact_src),("typed",typed_src)):
        exe=build/f"ttutil_material_probe_{tag}"
        run([compiler,"-O0","-std=legacy","-fallow-argument-mismatch",f"-I{source}",f"-I{build}",str(src),str(lib),"-o",str(exe)],cwd=build)
        out[tag]=exe
    return out,compiler_version,len(objects),sha256_file(lib)

def verify_numeric_lexemes(material_bytes,work,compiler):
    # External formatted list-directed READ matches the numeric conversion family
    # exercised by revision-53 text input. Compare every natural file lexeme bitwise.
    text=material_bytes.decode("latin-1")
    tokens=NUMERIC_TOKEN_RE.findall(text)
    token_file=work/"numeric-lexemes.txt"; token_file.write_text("\n".join(tokens)+"\n",encoding="ascii")
    src=work/"numeric_lexeme_probe.f90"
    src.write_text("""program numeric_lexeme_probe
use iso_fortran_env, only: int64, real64
implicit none
real(real64) :: x
integer(int64) :: bits
integer :: u,ios
open(newunit=u,file='numeric-lexemes.txt',status='old',action='read')
do
  read(u,*,iostat=ios) x
  if (ios /= 0) exit
  bits=transfer(x,bits)
  write(*,'(Z16.16)') bits
end do
end program
""",encoding="utf-8")
    exe=work/"numeric_lexeme_probe"; run([compiler,str(src),"-o",str(exe)],cwd=work)
    lines=run([str(exe)],cwd=work).stdout.splitlines()
    if len(lines)!=len(tokens): raise RuntimeError(f"numeric probe count {len(lines)} != {len(tokens)}")
    mismatch=[]
    for i,(tok,hx) in enumerate(zip(tokens,lines)):
        py=struct.unpack(">Q",struct.pack(">d",float(tok.replace("D","E").replace("d","e"))))[0]
        ft=int(hx,16)
        if py!=ft: mismatch.append({"index":i,"token":tok,"python_bits":f"{py:016X}","fortran_bits":f"{ft:016X}"})
    return {"numeric_lexemes_checked":len(tokens),"bit_exact_matches":len(tokens)-len(mismatch),"mismatches":mismatch}

def run_probe(exe,fixture,work,name):
    p=work/f"{name}.inp"; p.write_text(fixture,encoding="utf-8")
    return run([str(exe.resolve()),p.name],cwd=work).stdout

def ulp_distance(a,b):
    ia=struct.unpack(">q",struct.pack(">d",a))[0]; ib=struct.unpack(">q",struct.pack(">d",b))[0]
    if ia<0: ia=0x8000000000000000-ia
    if ib<0: ib=0x8000000000000000-ib
    return abs(ia-ib)
def numeric_mismatches(a,b,path=""):
    out=[]
    if isinstance(a,dict):
        for k in a:
            if k in b: out.extend(numeric_mismatches(a[k],b[k],path+"/"+str(k)))
    elif isinstance(a,list):
        for i,(x,y) in enumerate(zip(a,b)): out.extend(numeric_mismatches(x,y,path+f"/{i}"))
    elif isinstance(a,float) and isinstance(b,float) and a!=b:
        out.append({"path":path,"legacy":a,"native":b,"ulp_distance":ulp_distance(a,b),"absolute_difference":abs(a-b)})
    return out

def qualify(swap_zip,testbank_zip,manifest,exact_src,typed_src,work):
    th=sha256_file(testbank_zip)
    if th!=TESTBANK_SHA256: raise ValueError(f"testbank hash mismatch {th}")
    source=work/"TTUTIL"; build=work/"build"
    mat=materializer.materialize(swap_zip,source,manifest)
    probes,compiler_version,object_count,libhash=build_ttutil_and_probes(swap_zip,source,build,exact_src,typed_src)
    with zipfile.ZipFile(testbank_zip,"r") as z: raw=z.read(RUURLO_MATERIAL)
    if sha256_bytes(raw)!=RUURLO_MATERIAL_SHA256: raise ValueError("Ruurlo MATERIAL hash mismatch")
    legacy=material.parse_legacy_material_text(raw.decode("latin-1"),source_file=RUURLO_MATERIAL,ipo=0,ioptae=0,ioptghg=0)
    exact_fixture=material.dense_native_fixture(legacy); material.validate_native_material_schema(exact_fixture)
    exact=material.parse_native_material_probe_output(run_probe(probes["exact"],exact_fixture,work,"exact"),RUURLO_MATERIAL+"#TTUTIL-char")
    exact_equal=material.semantic_projection(legacy)==material.semantic_projection(exact)
    typed_fixture=material.dense_native_typed_double_fixture(legacy); material.validate_native_material_schema(typed_fixture)
    typed=material.parse_native_material_probe_output(run_probe(probes["typed"],typed_fixture,work,"typed"),RUURLO_MATERIAL+"#TTUTIL-double")
    mism=numeric_mismatches(material.semantic_projection(legacy),material.semantic_projection(typed))
    lexical=verify_numeric_lexemes(raw,work,shutil.which("gfortran"))
    maxulp=max((x["ulp_distance"] for x in mism),default=0)
    maxabs=max((x["absolute_difference"] for x in mism),default=0.0)
    passed=exact_equal and not lexical["mismatches"] and len(mism)==26 and maxulp==1
    return {
      "schema":"ANIMO-IO01/MATERIALPilotQualification/v2",
      "result":"PASS" if passed else "FAIL",
      "decision":"QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS" if passed else "NOT_QUALIFIED",
      "scope":"RuurloGrass non-GHG MATERIAL only; IPO=0, Ioptae=0, IoptGHG=0; parser/normalization semantics only",
      "source_identity":{"testbank_sha256":th,"ruurlo_material_sha256":sha256_bytes(raw),"swap_4_3_1_sha256":mat["source_package_sha256"],"embedded_ttutil_zip_sha256":mat["embedded_archive_sha256"],"ttutil_version":mat["ttutil_version"],"ttutil_files_verified":mat["files_verified"],"ttutil_fortran_objects_built":object_count},
      "compiler":compiler_version,
      "ttutil_local_build":{"static_library_sha256_local_build_only":libhash,"exact_probe_sha256":sha256_file(probes["exact"]),"typed_probe_sha256":sha256_file(probes["typed"])},
      "legacy_numeric_conversion_oracle":{"method":"GNU Fortran external list-directed REAL(8) conversion of every numeric lexeme in natural Ruurlo MATERIAL compared bitwise to normalization oracle",**lexical},
      "exact_character_transport":{"field_exact_equivalent":exact_equal,"numeric_tolerance_used":False,"transport":"TTUTIL CHARACTER scalar/array token lookup followed by explicit Fortran list-directed REAL(8) conversion"},
      "typed_double_comparison":{"field_exact_equivalent":len(mism)==0,"decision":"REJECT_TYPED_DOUBLE_FOR_FIELD_EXACT_REPRESENTATION","numeric_mismatch_count":len(mism),"maximum_ulp_distance":maxulp,"maximum_absolute_difference":maxabs,"mismatches":mism},
      "sparse_zero_semantics":{"status":"QUALIFIED_BY_SEPARATE_NATURAL_OLD_VS_REV53_LINEAGE_EVIDENCE","evidence":"integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json"},
      "runtime_hazard_exclusions":[
        "revision-53 omitted FR/FRca storage initialization mechanism remains unqualified even though intended omitted-cell zero semantics are lineage-qualified",
        "revision-53 IPO=0 Pofr(Frno) range check can read a runtime value not defined by active input"
      ],
      "non_admissions":{"production_migration_admitted":False,"GHG_schema_admitted":False,"binary_hydrology_converted":False,"model_output_equivalence_claimed":False,"B4_admitted":False}
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--swap-zip",type=Path,required=True); ap.add_argument("--testbank-zip",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,default=ROOT/"integration/animo-io/TTUTIL-4.27-SHA256SUMS.txt")
    ap.add_argument("--exact-probe-source",type=Path,default=TOOLS/"ttutil_material_probe.f90")
    ap.add_argument("--typed-probe-source",type=Path,default=TOOLS/"ttutil_material_probe_typed_double.f90")
    ap.add_argument("--output",type=Path); ap.add_argument("--work-dir",type=Path)
    a=ap.parse_args()
    if a.work_dir is None:
        with tempfile.TemporaryDirectory(prefix="animo-io01-material-") as t:
            r=qualify(a.swap_zip,a.testbank_zip,a.manifest,a.exact_probe_source,a.typed_probe_source,Path(t))
    else:
        a.work_dir.mkdir(parents=True,exist_ok=True); r=qualify(a.swap_zip,a.testbank_zip,a.manifest,a.exact_probe_source,a.typed_probe_source,a.work_dir)
    s=json.dumps(r,indent=2,sort_keys=True)+"\n"
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(s,encoding="utf-8")
    print(s,end=""); return 0 if r["result"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
