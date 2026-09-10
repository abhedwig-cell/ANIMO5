#!/usr/bin/env python3
"""Reconstruct and execute the bounded TCD-040 Stage-A/Stage-B replay.

This is ANIMO-B3B04E3 remediation tooling. It patches only an extracted
execution copy of frozen B0 source. It does not load B3B04 expected scientific
results. Those are consulted only by the separate comparison script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
CASE = "LWKM_gras_1040.2021.2045"
SPLIT_NONZERO = 282
SPLIT_ZERO = 67
TARGET_NAMES = ["NH4", "NO3", "DOM", "DON", "DOP"]
ARRAY_NAMES = ["NH4", "NO3", "DOM", "DON", "DOP", "PO4", "MOFRT"]
SCALAR_NAMES = ["Wale", "Snla", "Pn"]
COMPILE_FLAGS = [
    "-ffree-form",
    "-ffree-line-length-none",
    "-fallow-argument-mismatch",
    "-std=legacy",
    "-fdefault-real-8",
    "-fdefault-double-8",
    "-fno-automatic",
]
LINK_FLAGS = ["-Wl,--build-id=none"]
SOURCE_MEMBER_PATHS = {
    "Inicalc.for": "Inicalc.for",
    "input1.for": "input1.for",
    "Init.for": "Init.for",
    "Output_Init.for": "Output_Init.for",
    "Animo.for": "Animo.for",
}

DECL_ANCHOR = "      character :: chelp*16,Rcsrev*80\n"
INIT_ANCHOR = "      include 'Version.inc'\n"
PHASE0_ANCHOR = "     &       IoptPCl,PClYrSw,Uipc,Yearcor,Pwplln)\n"
PHASE1_ANCHOR = "     &       Respex, Respos, Resphuex, Resphuos, PotDeni,Ioptae,Wfps)\n"

DECL_INSERT = """      Character*16 B3Mode,B3SplitText
      Integer B3Split,B3TraceUnit,B3CkptUnit,B3Phase
      Real B3C1,B3C2,B3C3,B3C4,B3C5
      Logical B3Active
"""

INIT_INSERT = """      B3Mode='NONE'
      B3SplitText='0'
      B3Split=0
      B3TraceUnit=991
      B3CkptUnit=992
      B3Active=.false.
      Call Getarg(2,B3Mode)
      Call Getarg(3,B3SplitText)
      If(Len_trim(B3SplitText).Gt.0) Read(B3SplitText,*) B3Split
      If(Trim(B3Mode).Ne.'NONE' .And. Len_trim(B3Mode).Gt.0) Then
        B3Active=.true.
        Open(Unit=B3TraceUnit,File='b3trace.bin',Form='unformatted',Status='replace',Action='write')
      End If
"""

PHASE0_INSERT = """
! B3B04E3 qualification-only instrumentation: phase 0 after accepted-owner restore
            If(B3Active) Then
              If((Trim(B3Mode).Eq.'RESTORE' .Or. Trim(B3Mode).Eq.'DEFECT') .And. Sttot.Eq.B3Split+1) Then
                Open(Unit=B3CkptUnit,File='b3checkpoint.bin',Form='unformatted',Status='old',Action='read')
                Read(B3CkptUnit) B3C1,B3C2,B3C3,B3C4,B3C5
                Close(B3CkptUnit)
                If(Conh(0).Ne.B3C1 .Or. Coni(0).Ne.B3C2 .Or. Codiorma(0).Ne.B3C3 .Or. Codiorni(0).Ne.B3C4 .Or. Codiorpo(0).Ne.B3C5) Stop 95
                If(Trim(B3Mode).Eq.'RESTORE') Then
                  Conh(0)=B3C1
                  Coni(0)=B3C2
                  Codiorma(0)=B3C3
                  Codiorni(0)=B3C4
                  Codiorpo(0)=B3C5
                Else
                  Conh(0)=0.0
                  Coni(0)=0.0
                  Codiorma(0)=0.0
                  Codiorni(0)=0.0
                  Codiorpo(0)=0.0
                End If
              End If
              B3Phase=0
              Write(B3TraceUnit) Sttot,B3Phase,Nl,Conh(0:Nl),Coni(0:Nl),Codiorma(0:Nl),Codiorni(0:Nl),Codiorpo(0:Nl),Copo(0:Nl),Mofrt(0:Nl),Wale,Snla,Pn
            End If
"""

PHASE1_INSERT = """
! B3B04E3 qualification-only instrumentation: phase 1 accepted end-of-step state
            If(B3Active) Then
              B3Phase=1
              Write(B3TraceUnit) Sttot,B3Phase,Nl,Rsconh(0:Nl),Rsconi(0:Nl),Rscodiorma(0:Nl),Rscodiorni(0:Nl),Rscodiorpo(0:Nl),Rscopo(0:Nl),Mofrt(0:Nl),Wale,Snla,Pn
              If(Trim(B3Mode).Eq.'STAGEA' .And. Sttot.Eq.B3Split) Then
                Open(Unit=B3CkptUnit,File='b3checkpoint.bin',Form='unformatted',Status='replace',Action='write')
                Write(B3CkptUnit) Rsconh(0),Rsconi(0),Rscodiorma(0),Rscodiorni(0),Rscodiorpo(0)
                Close(B3CkptUnit)
                Close(B3TraceUnit)
                Stop 94
              End If
            End If
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run_checked(cmd: list[str], cwd: Path, log: Path, allowed: set[int] = {0}) -> int:
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode not in allowed:
        raise RuntimeError(f"command returned {result.returncode}, allowed={sorted(allowed)}: {cmd}; see {log}")
    return result.returncode


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def invoke_helper(helper: Path, args: list[str], log: Path) -> None:
    run_checked([sys.executable, str(helper), *args], cwd=repo_root(), log=log)


def hash_selected_source_members(source_dir: Path) -> dict[str, str]:
    return {name: sha256_file(source_dir / rel) for name, rel in SOURCE_MEMBER_PATHS.items()}


def patch_animo_for(source_dir: Path) -> dict[str, object]:
    path = source_dir / "Animo.for"
    before_bytes = path.read_bytes()
    text = before_bytes.decode("latin1")
    counts = {
        "declaration_anchor": text.count(DECL_ANCHOR),
        "initialization_anchor": text.count(INIT_ANCHOR),
        "phase0_anchor": text.count(PHASE0_ANCHOR),
        "phase1_anchor": text.count(PHASE1_ANCHOR),
    }
    if any(v != 1 for v in counts.values()):
        raise RuntimeError(f"instrumentation anchor multiplicity changed: {counts}")
    text = text.replace(DECL_ANCHOR, DECL_ANCHOR + DECL_INSERT, 1)
    text = text.replace(INIT_ANCHOR, INIT_ANCHOR + INIT_INSERT, 1)
    text = text.replace(PHASE0_ANCHOR, PHASE0_ANCHOR + PHASE0_INSERT, 1)
    text = text.replace(PHASE1_ANCHOR, PHASE1_ANCHOR + PHASE1_INSERT, 1)
    path.write_text(text, encoding="latin1", newline="")
    return {
        "execution_copy_only": True,
        "before_sha256": hashlib.sha256(before_bytes).hexdigest(),
        "after_sha256": sha256_file(path),
        "anchor_counts": counts,
        "production_source_modified": False,
    }


def relink_instrumented(build_dir: Path, compiler: str, log_dir: Path) -> str:
    source_dir = build_dir / "src"
    object_dir = build_dir / "obj"
    compile_cmd = [
        compiler, *COMPILE_FLAGS, "-I", ".", "-I", "../obj", "-J", "../obj",
        "-c", "Animo.for", "-o", "../obj/Animo.o",
    ]
    run_checked(compile_cmd, source_dir, log_dir / "instrumented_Animo_compile.log")

    excluded = {"input1_1.for", "Outselorg.for"}
    selected = sorted(
        [
            p.name for p in source_dir.iterdir()
            if p.suffix.lower() in {".for", ".f90"}
            and p.name not in excluded
            and p.name not in {"Outsel_gnu.for", "dfport_shim.f90", "intel_intrinsics_shim.f90"}
        ],
        key=str.lower,
    )
    if len(selected) != 58:
        raise RuntimeError(f"expected 58 selected legacy units, got {len(selected)}")
    objects = [object_dir / "dfport_shim.o", object_dir / "intel_intrinsics_shim.o"]
    objects.extend(object_dir / f"{Path(name).stem}.o" for name in selected)
    exe = build_dir / "animo_b3b04e3_recon"
    run_checked([compiler, *map(str, objects), *LINK_FLAGS, "-o", str(exe)], build_dir, log_dir / "instrumented_link.log")
    return sha256_file(exe)


def parse_fortran_records(path: Path) -> list[bytes]:
    data = path.read_bytes()
    records: list[bytes] = []
    pos = 0
    while pos < len(data):
        if pos + 4 > len(data):
            raise ValueError(f"truncated leading marker: {path}")
        n = struct.unpack_from("<i", data, pos)[0]
        pos += 4
        if n < 0 or pos + n + 4 > len(data):
            raise ValueError(f"invalid record length {n}: {path}")
        payload = data[pos:pos+n]
        pos += n
        n2 = struct.unpack_from("<i", data, pos)[0]
        pos += 4
        if n2 != n:
            raise ValueError(f"record marker mismatch {n}/{n2}: {path}")
        records.append(payload)
    return records


def parse_trace(path: Path) -> list[dict[str, object]]:
    out = []
    for payload in parse_fortran_records(path):
        if len(payload) < 12:
            raise ValueError("trace payload too short")
        step, phase, nl = struct.unpack_from("<iii", payload, 0)
        count = nl + 1
        expected = 12 + (7 * count + 3) * 8
        if len(payload) != expected:
            raise ValueError(f"unexpected trace payload bytes: got {len(payload)}, expected {expected}, nl={nl}")
        offset = 12
        arrays = {}
        for name in ARRAY_NAMES:
            arrays[name] = list(struct.unpack_from(f"<{count}d", payload, offset))
            offset += count * 8
        scalars = {}
        for name in SCALAR_NAMES:
            scalars[name] = struct.unpack_from("<d", payload, offset)[0]
            offset += 8
        out.append({"step": step, "phase": phase, "nl": nl, "arrays": arrays, "scalars": scalars})
    return out


def parse_checkpoint(path: Path) -> dict[str, object]:
    records = parse_fortran_records(path)
    if len(records) != 1 or len(records[0]) != 40:
        raise ValueError(f"checkpoint must contain one 40-byte logical record, got {[len(x) for x in records]}")
    payload = records[0]
    values = struct.unpack("<5d", payload)
    return {
        "file_size_bytes": path.stat().st_size,
        "file_sha256": sha256_file(path),
        "logical_records": 1,
        "payload_size_bytes": 40,
        "serialization": "GNU_FORTRAN_SEQUENTIAL_UNFORMATTED_ONE_RECORD_5_BINARY64_LITTLE_ENDIAN",
        "order": TARGET_NAMES,
        "values": dict(zip(TARGET_NAMES, values)),
        "binary64_little_endian_hex": {
            name: struct.pack("<d", value).hex() for name, value in zip(TARGET_NAMES, values)
        },
        "all_exact_positive_zero": all(struct.pack("<d", v) == b"\x00" * 8 for v in values),
    }


def copy_case(prepared_case: Path, run_dir: Path) -> None:
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(prepared_case, run_dir)
    for stale in ["b3trace.bin", "b3checkpoint.bin"]:
        p = run_dir / stale
        if p.exists():
            p.unlink()


def execute_model(exe: Path, run_dir: Path, mode: str, split: int, allowed: set[int]) -> int:
    result = subprocess.run(
        [str(exe), "animo.ini", mode, str(split)],
        cwd=run_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    (run_dir / "run.stdout").write_text(result.stdout, encoding="utf-8")
    (run_dir / "run.stderr").write_text(result.stderr, encoding="utf-8")
    if result.returncode not in allowed:
        raise RuntimeError(f"{mode}/{split} returned {result.returncode}, expected {sorted(allowed)}")
    return result.returncode


def validate_trace_topology(trace: list[dict[str, object]]) -> None:
    if len(trace) % 2:
        raise ValueError("trace record count must be even")
    for i, record in enumerate(trace):
        expected_step = i // 2 + 1
        expected_phase = i % 2
        if record["step"] != expected_step or record["phase"] != expected_phase:
            raise ValueError(f"trace topology mismatch at record {i}: {record}")
        if record["nl"] < 0:
            raise ValueError("negative Nl")


def compare_trace_records(ref: list[dict[str, object]], other: list[dict[str, object]]) -> dict[str, object]:
    if len(ref) != len(other):
        raise ValueError(f"trace length mismatch {len(ref)} != {len(other)}")
    first = None
    changed_records = 0
    changed_layers = {name: set() for name in ARRAY_NAMES}
    max_abs = {name: 0.0 for name in ARRAY_NAMES}
    scalar_max_abs = {name: 0.0 for name in SCALAR_NAMES}
    for idx, (a, b) in enumerate(zip(ref, other)):
        if (a["step"], a["phase"], a["nl"]) != (b["step"], b["phase"], b["nl"]):
            raise ValueError(f"trace metadata mismatch at record {idx}")
        rec_changed = False
        coords = []
        for name in ARRAY_NAMES:
            aa = a["arrays"][name]
            bb = b["arrays"][name]
            if len(aa) != len(bb):
                raise ValueError(f"array length mismatch {name} at record {idx}")
            for layer, (x, y) in enumerate(zip(aa, bb)):
                if struct.pack("<d", x) != struct.pack("<d", y):
                    rec_changed = True
                    changed_layers[name].add(layer)
                    max_abs[name] = max(max_abs[name], abs(x-y))
                    coords.append([name, layer, x, y])
        for name in SCALAR_NAMES:
            x = a["scalars"][name]
            y = b["scalars"][name]
            if struct.pack("<d", x) != struct.pack("<d", y):
                rec_changed = True
                scalar_max_abs[name] = max(scalar_max_abs[name], abs(x-y))
                coords.append([name, None, x, y])
        if rec_changed:
            changed_records += 1
            if first is None:
                first = {
                    "record_index": idx,
                    "step": a["step"],
                    "phase": a["phase"],
                    "coordinates": coords,
                }
    def envelope(values: set[int]) -> str | None:
        if not values:
            return None
        ordered = sorted(values)
        return f"{ordered[0]}:{ordered[-1]}" if len(ordered) > 1 else str(ordered[0])
    return {
        "changed_records": changed_records,
        "first_divergence": first,
        "changed_layers": {k: envelope(v) for k, v in changed_layers.items()},
        "max_abs_difference": max_abs,
        "scalar_max_abs_difference": scalar_max_abs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("testbank_zip", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--compiler", default="gfortran")
    args = parser.parse_args()

    source_zip = args.source_zip.resolve()
    testbank_zip = args.testbank_zip.resolve()
    output_dir = args.output_dir.resolve()
    if sha256_file(source_zip) != SOURCE_SHA256:
        raise SystemExit("frozen source SHA-256 mismatch")
    if sha256_file(testbank_zip) != TESTBANK_SHA256:
        raise SystemExit("frozen testbank SHA-256 mismatch")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    logs = output_dir / "logs"
    logs.mkdir()

    root = repo_root()
    build_helper = root / "tools/build_gnu_diagnostic.py"
    case_helper = root / "tools/prepare_gnu_case.py"
    if not build_helper.is_file() or not case_helper.is_file():
        raise SystemExit("required repository build/case helpers are missing")

    build_dir = output_dir / "build"
    case_dir = output_dir / "prepared_case"
    invoke_helper(build_helper, [str(source_zip), str(build_dir), "--compiler", args.compiler], logs / "build_helper.log")
    invoke_helper(case_helper, [str(testbank_zip), CASE, str(case_dir)], logs / "case_helper.log")

    build_meta = json.loads((build_dir / "build_metadata.json").read_text(encoding="utf-8"))
    case_meta = json.loads((case_dir / "PREP02_case_adapter.json").read_text(encoding="utf-8"))
    if build_meta.get("source_zip_sha256") != SOURCE_SHA256:
        raise RuntimeError("build helper source pin mismatch")
    if case_meta.get("testbank_sha256") != TESTBANK_SHA256 or case_meta.get("case") != CASE:
        raise RuntimeError("case helper provenance mismatch")
    if build_meta.get("compile_flags") != COMPILE_FLAGS:
        raise RuntimeError("compiler flag contract changed")

    source_dir = build_dir / "src"
    original_member_hashes = hash_selected_source_members(source_dir)
    instrumentation = patch_animo_for(source_dir)
    instrumented_exe_sha = relink_instrumented(build_dir, args.compiler, logs)
    exe = build_dir / "animo_b3b04e3_recon"

    runs_dir = output_dir / "runs"
    run_defs = [
        ("continuous", "CONT", 0, {100}),
        ("stageA282", "STAGEA", SPLIT_NONZERO, {94}),
        ("restore282", "RESTORE", SPLIT_NONZERO, {100}),
        ("defect282", "DEFECT", SPLIT_NONZERO, {100}),
        ("stageA67", "STAGEA", SPLIT_ZERO, {94}),
        ("defect67", "DEFECT", SPLIT_ZERO, {100}),
    ]
    rc = {}
    for name, mode, split, allowed in run_defs:
        run_dir = runs_dir / name
        copy_case(case_dir, run_dir)
        if name in {"restore282", "defect282"}:
            source_ckpt = runs_dir / "stageA282" / "b3checkpoint.bin"
            if not source_ckpt.is_file():
                raise RuntimeError("Stage-A 282 checkpoint not available before Stage-B")
            shutil.copy2(source_ckpt, run_dir / "b3checkpoint.bin")
        if name == "defect67":
            source_ckpt = runs_dir / "stageA67" / "b3checkpoint.bin"
            if not source_ckpt.is_file():
                raise RuntimeError("Stage-A 67 checkpoint not available before Stage-B")
            shutil.copy2(source_ckpt, run_dir / "b3checkpoint.bin")
        rc[name] = execute_model(exe, run_dir, mode, split, allowed)

    traces = {name: parse_trace(runs_dir / name / "b3trace.bin") for name in rc}
    for trace in traces.values():
        validate_trace_topology(trace)
    raw_trace_paths = {name: runs_dir / name / "b3trace.bin" for name in rc}

    continuous = traces["continuous"]
    stage282 = traces["stageA282"]
    restored = traces["restore282"]
    defective = traces["defect282"]
    stage67 = traces["stageA67"]
    defect67 = traces["defect67"]

    if len(stage282) != SPLIT_NONZERO * 2 or len(stage67) != SPLIT_ZERO * 2:
        raise RuntimeError("Stage-A record count does not follow two-record-per-step topology")
    if stage282 != continuous[:len(stage282)] or stage67 != continuous[:len(stage67)]:
        raise RuntimeError("Stage-A trace is not an exact prefix of continuous trace")
    if restored != continuous:
        raise RuntimeError("corrected restore trace is not exact to continuous trace")

    ckpt282 = parse_checkpoint(runs_dir / "stageA282" / "b3checkpoint.bin")
    ckpt67 = parse_checkpoint(runs_dir / "stageA67" / "b3checkpoint.bin")
    last282 = stage282[-1]
    last67 = stage67[-1]
    if last282["phase"] != 1 or last67["phase"] != 1:
        raise RuntimeError("Stage-A checkpoint not written after accepted phase-1 record")
    stage282_values = [last282["arrays"][name][0] for name in TARGET_NAMES]
    stage67_values = [last67["arrays"][name][0] for name in TARGET_NAMES]
    if [ckpt282["values"][name] for name in TARGET_NAMES] != stage282_values:
        raise RuntimeError("split-282 checkpoint does not equal accepted layer-0 owners")
    if [ckpt67["values"][name] for name in TARGET_NAMES] != stage67_values:
        raise RuntimeError("split-67 checkpoint does not equal accepted layer-0 owners")
    if not ckpt67["all_exact_positive_zero"]:
        raise RuntimeError("split-67 checkpoint is not exact positive zero")
    if defect67 != continuous:
        raise RuntimeError("split-67 defective zero application is not exact identity")

    diff282 = compare_trace_records(continuous, defective)
    expected_first_index = len(stage282)
    first = diff282["first_divergence"]
    if first is None or first["record_index"] != expected_first_index or first["step"] != SPLIT_NONZERO + 1 or first["phase"] != 0:
        raise RuntimeError(f"unexpected first divergence topology: {first}")
    first_coords = {(x[0], x[1]) for x in first["coordinates"]}
    required_coords = {(name, 0) for name in TARGET_NAMES}
    if first_coords != required_coords:
        raise RuntimeError(f"first divergence is not exactly five target layer-0 coordinates: {first_coords}")

    generated_artifacts = {}
    for name in rc:
        p = raw_trace_paths[name]
        generated_artifacts[f"{name}/b3trace.bin"] = {"sha256": sha256_file(p), "size_bytes": p.stat().st_size}
    for name in ["stageA282", "stageA67"]:
        p = runs_dir / name / "b3checkpoint.bin"
        generated_artifacts[f"{name}/b3checkpoint.bin"] = {"sha256": sha256_file(p), "size_bytes": p.stat().st_size}

    report = {
        "schema_version": "1.0",
        "workunit": "ANIMO-B3B04E3",
        "target": "TCD-040",
        "evidence_role": "E2_AUTHORIZED_DISTINCT_RECONSTRUCTED_REPLAY_GENERATED_WITHOUT_B3B04_EXPECTED_RESULT_INPUTS",
        "case": CASE,
        "execution_context": {
            "controlled_immutable_B0_storage_proven": False,
            "independent_replay_qualified": False,
            "reason": "local/session B0 bytes are hash-verified but EG01 controlled-custody proof is not yet available",
        },
        "frozen_b0": {
            "source_sha256": sha256_file(source_zip),
            "testbank_sha256": sha256_file(testbank_zip),
        },
        "source_member_identity_before_instrumentation": original_member_hashes,
        "build": {
            "base_helper_metadata": build_meta,
            "case_helper_metadata": case_meta,
            "instrumentation": instrumentation,
            "instrumented_executable_sha256": instrumented_exe_sha,
            "compile_flags": COMPILE_FLAGS,
            "link_flags": LINK_FLAGS,
        },
        "trace_schema": {
            "serialization": "GNU_FORTRAN_SEQUENTIAL_UNFORMATTED",
            "record_header": ["int32 step", "int32 phase", "int32 Nl"],
            "arrays": [f"binary64 {name}(0:Nl)" for name in ARRAY_NAMES],
            "scalars": [f"binary64 {name}" for name in SCALAR_NAMES],
            "phase_0": "current owners immediately after Init and optional atomic restore/defect action",
            "phase_1": "accepted Rs* owners after Outsel at end of timestep",
            "records_per_step": 2,
        },
        "run_exit_codes": rc,
        "continuous": {
            "records": len(continuous),
            "trace_sha256_reconstructed_schema": sha256_file(raw_trace_paths["continuous"]),
            "trace_size_bytes": raw_trace_paths["continuous"].stat().st_size,
        },
        "split282": {
            "split_step": SPLIT_NONZERO,
            "stageA_records": len(stage282),
            "stageA_exact_continuous_prefix": True,
            "checkpoint": ckpt282,
            "checkpoint_matches_stageA_accepted_owner_bytes": True,
            "corrected_restore_full_trace_exact": True,
            "corrected_restore_trace_sha256_reconstructed_schema": sha256_file(raw_trace_paths["restore282"]),
            "defective_trace_sha256_reconstructed_schema": sha256_file(raw_trace_paths["defect282"]),
            "defective_comparison": diff282,
            "Copo0_modified_at_boundary": False,
        },
        "split67_zero_control": {
            "split_step": SPLIT_ZERO,
            "stageA_records": len(stage67),
            "stageA_exact_continuous_prefix": True,
            "checkpoint": ckpt67,
            "defective_zero_application_full_trace_exact": True,
            "defective_trace_sha256_reconstructed_schema": sha256_file(raw_trace_paths["defect67"]),
        },
        "generated_artifacts": generated_artifacts,
        "generator_expected_scientific_results_loaded": False,
        "production_source_modified": False,
        "whole_model_checkpoint_qualified": False,
    }
    report_path = output_dir / "TCD040_RECONSTRUCTED_REPLAY_RESULT.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "result": "PASS_B3B04E3_RECONSTRUCTED_REPLAY_GENERATION",
        "report": str(report_path),
        "continuous_records": len(continuous),
        "split282_checkpoint_sha256": ckpt282["file_sha256"],
        "first_divergence": first,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
