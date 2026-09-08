#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, re, zipfile
from pathlib import Path, PurePosixPath

INPUT_KEYS = {"GEN","MAT","PLA","SOI","BOU","INI","MAN","SWU","WAI","WAU","CHE","CRU"}
OUTPUT_KEYS = {"INO","MES"}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def decode_text(data: bytes):
    for enc in ("utf-8-sig", "cp1252", "latin1"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            pass
    return None, None

def parse_ini(data: bytes):
    text, enc = decode_text(data)
    if text is None:
        return {}, None, None
    version = None
    kv = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if version is None and "=" not in line:
            version = line
            continue
        m = re.match(r'([A-Za-z]{3})\s*=\s*"([^"]*)"', line)
        if m:
            kv[m.group(1).upper()] = m.group(2)
    return kv, version, enc

def find_member_casefold(names, target):
    t = target.replace("\\", "/").lstrip("./").lower()
    matches = [n for n in names if n.lower() == t]
    return matches

def parse_general(data: bytes):
    text, enc = decode_text(data)
    if text is None:
        return {}, None
    out = {}
    for key in ["HydrologicInput","PhosphorusCycle","SulphateSimulation","AerationModel","CropUptakeModel","MacroPoreOption","GreenHouseGasOption","SoilTempFile","StartDate","EndDate"]:
        m = re.search(rf'\b{re.escape(key)}\s*=\s*([^!\r\n]+)', text, re.I)
        if m:
            out[key] = m.group(1).strip().strip("'\"")
    comments = [ln.strip() for ln in text.splitlines()[:20] if ln.strip().startswith(("!","File","Content","Filename"))]
    if comments:
        out["header_evidence"] = " | ".join(comments[:4])
    return out, enc

def classify_case(case, general):
    h=(general.get("header_evidence") or "").lower()
    if "example" in h:
        return "documented_example"
    n=case.lower()
    if n.startswith("lwkm_"):
        return "production_or_reference_named_case_unverified"
    if n.startswith("stone_"):
        return "historical_regression_or_reference_named_case_unverified"
    if "zuiderzeeland" in n or "puitmijn" in n:
        return "project_case_unverified"
    if "ghg" in n:
        return "feature_case_unverified"
    if "peat" in n:
        return "feature_case_unverified"
    return "unknown_provenance"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("zip_path", type=Path)
    ap.add_argument("--json", type=Path, required=True)
    ap.add_argument("--manifest-csv", type=Path, required=True)
    ap.add_argument("--cases-csv", type=Path, required=True)
    args=ap.parse_args()
    raw=args.zip_path.read_bytes()
    with zipfile.ZipFile(args.zip_path) as z:
        infos=z.infolist()
        files=[i for i in infos if not i.is_dir()]
        names=[i.filename for i in files]
        root_prefix="ANIMO_testbank/"
        cases=sorted({PurePosixPath(n).parts[1] for n in names if n.startswith(root_prefix) and len(PurePosixPath(n).parts)>2})
        manifest=[]
        for i in files:
            b=z.read(i.filename)
            txt, enc=decode_text(b)
            manifest.append({
                "path": i.filename,
                "size": i.file_size,
                "crc32": f"{i.CRC:08x}",
                "sha256": sha256_bytes(b),
                "zip_datetime": "%04d-%02d-%02dT%02d:%02d:%02d" % i.date_time,
                "encoding_observed": enc if txt is not None and b.count(b"\x00") < 2 else "binary_or_unknown",
            })
        case_rows=[]
        for case in cases:
            prefix=f"{root_prefix}{case}/"
            cnames=[n for n in names if n.startswith(prefix)]
            ini_names=[n for n in cnames if PurePosixPath(n).name.lower()=="animo.ini" and len(PurePosixPath(n).parts)==3]
            ini=ini_names[0] if ini_names else None
            kv={}; version=None; ini_enc=None
            if ini:
                kv,version,ini_enc=parse_ini(z.read(ini))
            general_name=None
            for n in cnames:
                if PurePosixPath(n).name.lower()=="general.inp" and "/input/" in n.lower():
                    general_name=n; break
            general={}; gen_enc=None
            if general_name:
                general,gen_enc=parse_general(z.read(general_name))
            missing=[]; ambiguous=[]; resolved={}
            for key,val in kv.items():
                if key not in INPUT_KEYS or val.strip()=="-":
                    continue
                target=f"{prefix}{val}".replace("\\","/")
                ms=find_member_casefold(names,target)
                if len(ms)==1: resolved[key]=ms[0]
                elif len(ms)==0: missing.append(f"{key}:{val}")
                else: ambiguous.append(f"{key}:{val}")
            output_files=[n for n in cnames if "/output/" in n.lower() and not n.endswith("/")]
            historical_outputs=[n for n in cnames if PurePosixPath(n).name.lower() in {"initial.out","message.out"} or PurePosixPath(n).suffix.lower() in {".bal",".csv"}]
            runner=[n for n in cnames if PurePosixPath(n).suffix.lower() in {".bat",".cmd"}]
            case_rows.append({
                "testcase_id":case,
                "origin":"ANIMO_testbank.zip",
                "animo_version_evidence":version or "UNKNOWN",
                "classification":classify_case(case,general),
                "start_date":general.get("StartDate","UNKNOWN"),
                "end_date":general.get("EndDate","UNKNOWN"),
                "hydrologic_input":general.get("HydrologicInput","UNKNOWN"),
                "phosphorus_cycle":general.get("PhosphorusCycle","UNKNOWN"),
                "sulphate_simulation":general.get("SulphateSimulation","UNKNOWN"),
                "aeration_model":general.get("AerationModel","UNKNOWN"),
                "crop_uptake_model":general.get("CropUptakeModel","UNKNOWN"),
                "macropore_option":general.get("MacroPoreOption","UNKNOWN"),
                "greenhouse_gas_option":general.get("GreenHouseGasOption","UNKNOWN"),
                "soil_temp_file":general.get("SoilTempFile","UNKNOWN"),
                "input_file_count":sum(1 for n in cnames if "/input/" in n.lower()),
                "available_output_file_count":len(output_files),
                "historical_output_like_files":historical_outputs,
                "runner_files":runner,
                "missing_ini_references":missing,
                "ambiguous_ini_references":ambiguous,
                "current_executability":"BLOCKED_EXECUTABLE_MISSING" if not missing else "BLOCKED_EXECUTABLE_MISSING_INPUT_REQUIREMENT_UNASSESSED",
                "scientific_provenance":"NOT_ASSESSED",
                "status":"INVENTORIED_NOT_QUALIFIED",
                "general_header_evidence":general.get("header_evidence",""),
            })
    args.json.parent.mkdir(parents=True,exist_ok=True)
    out={
        "archive":{"path":args.zip_path.name,"size":len(raw),"sha256":sha256_bytes(raw),"file_count":len(files),"case_count":len(cases)},
        "cases":case_rows,
        "summary":{
            "cases":len(case_rows),
            "cases_with_no_output_directory_files":sum(1 for r in case_rows if r["available_output_file_count"]==0),
            "cases_with_missing_ini_inputs":sum(1 for r in case_rows if r["missing_ini_references"]),
            "all_cases_blocked_without_animo_executable":all(r["current_executability"].startswith("BLOCKED_EXECUTABLE") for r in case_rows),
        }
    }
    args.json.write_text(json.dumps(out,indent=2),encoding="utf-8")
    with args.manifest_csv.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(manifest[0]))
        w.writeheader(); w.writerows(manifest)
    fields=[k for k in case_rows[0] if k not in {"historical_output_like_files","runner_files","missing_ini_references","ambiguous_ini_references"}]
    with args.cases_csv.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields+["historical_output_like_files","runner_files","missing_ini_references","ambiguous_ini_references"])
        w.writeheader()
        for r in case_rows:
            rr=dict(r)
            for k in ("historical_output_like_files","runner_files","missing_ini_references","ambiguous_ini_references"):
                rr[k]=";".join(rr[k])
            w.writerow(rr)
    print(json.dumps(out["archive"],indent=2))
    print(json.dumps(out["summary"],indent=2))

if __name__=="__main__":
    main()
