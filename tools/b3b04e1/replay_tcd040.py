#!/usr/bin/env python3
"""Reconstruct and replay the existing TCD-040 split evidence from frozen B0.

Evidence-remediation harness only. This script does not modify frozen B0 bytes,
does not patch production source, and does not create a new scientific claim.
It creates execution-only instrumented descendants of the exact revision-53
source and regenerates the bounded split-282 and split-67 observations that
B3B04 reported.

The checked-in script is intentionally usable only with caller-supplied frozen
B0 archives. It never downloads or republishes those archives.
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

SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_COMPILER = "GNU Fortran (Debian 14.2.0-19) 14.2.0"
CASE = "LWKM_gras_1040.2021.2045"
NORMAL_EXIT = 100
STAGE_A_EXIT = 94
EXPECTED_STEPS = 900
EXPECTED_RECORDS_PER_STEP = 2
EXPECTED_NL = 30

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

TRACE_SCALARS = ["Pn", "Pnt", "Snla", "Snt", "Wale", "Walet"]
TRACE_ARRAYS = [
    "Conh",
    "Coni",
    "Codiorma",
    "Codiorni",
    "Codiorpo",
    "Copo",
    "Rsconh",
    "Rsconi",
    "Rscodiorma",
    "Rscodiorni",
    "Rscodiorpo",
    "Rscopo",
]
TARGET_LAYER0 = ["Conh(0)", "Coni(0)", "Codiorma(0)", "Codiorni(0)", "Codiorpo(0)"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str], *, cwd: Path | None = None, expected: int = 0) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != expected:
        raise RuntimeError(
            f"command returned {result.returncode}, expected {expected}: {command}\n{result.stdout}"
        )
    return result.stdout


def require_hash(path: Path, expected: str, role: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise RuntimeError(f"{role} SHA-256 mismatch: {actual}")


def compiler_identity(compiler: str) -> str:
    return run([compiler, "--version"]).splitlines()[0]


def trace_record_size(nl: int) -> int:
    # 3 little-endian int32 headers, six binary64 scalars, twelve arrays 0:Nl.
    return 3 * 4 + len(TRACE_SCALARS) * 8 + len(TRACE_ARRAYS) * (nl + 1) * 8


def patch_animo(source: str, mode: str, split: int, trace_name: str, checkpoint_name: str) -> str:
    if mode not in {"continuous", "stageA", "restore", "legacy"}:
        raise ValueError(mode)

    declaration = "      character :: chelp*16,Rcsrev*80\n"
    if source.count(declaration) != 1:
        raise RuntimeError("Animo.for declaration seam not unique")
    source = source.replace(declaration, declaration + "      Real(8) :: B3Ck(5)\n")

    loop_setup = "      Juda=Judami\n"
    if source.count(loop_setup) != 1:
        raise RuntimeError("Animo.for Juda loop seam not unique")
    source = source.replace(
        loop_setup,
        loop_setup
        + f"      Open(Unit=991,File='{trace_name}',Access='stream',Form='unformatted',Status='replace',Convert='little_endian')\n",
    )

    init_end = "     &       IoptPCl,PClYrSw,Uipc,Yearcor,Pwplln)\n"
    if source.count(init_end) != 1:
        raise RuntimeError("Animo.for post-Init seam not unique")

    after_init = ""
    if mode in {"restore", "legacy"}:
        after_init += f"            If(Sttot.Eq.{split + 1}) Then\n"
        after_init += (
            f"              Open(Unit=992,File='{checkpoint_name}',Status='old',Form='unformatted',"
            "Access='sequential',Convert='little_endian')\n"
        )
        after_init += "              Read(992) B3Ck\n              Close(992)\n"
        if mode == "restore":
            after_init += (
                "              Conh(0)=B3Ck(1)\n"
                "              Coni(0)=B3Ck(2)\n"
                "              Codiorma(0)=B3Ck(3)\n"
                "              Codiorni(0)=B3Ck(4)\n"
                "              Codiorpo(0)=B3Ck(5)\n"
            )
        else:
            after_init += (
                "              Conh(0)=0.0\n"
                "              Coni(0)=0.0\n"
                "              Codiorma(0)=0.0\n"
                "              Codiorni(0)=0.0\n"
                "              Codiorpo(0)=0.0\n"
            )
        after_init += "            End If\n"

    after_init += (
        "            Write(991) Sttot,0,Nl,Pn,Pnt,Snla,Snt,Wale,Walet, &\n"
        "     &      Conh(0:Nl),Coni(0:Nl),Codiorma(0:Nl),Codiorni(0:Nl),Codiorpo(0:Nl),Copo(0:Nl), &\n"
        "     &      Rsconh(0:Nl),Rsconi(0:Nl),Rscodiorma(0:Nl),Rscodiorni(0:Nl),Rscodiorpo(0:Nl),Rscopo(0:Nl)\n"
    )
    source = source.replace(init_end, init_end + after_init)

    outsel_end = "     &       Respex, Respos, Resphuex, Resphuos, PotDeni,Ioptae,Wfps)\n"
    if source.count(outsel_end) != 1:
        raise RuntimeError("Animo.for post-Outsel seam not unique")
    after_step = (
        "            Write(991) Sttot,1,Nl,Pn,Pnt,Snla,Snt,Wale,Walet, &\n"
        "     &      Conh(0:Nl),Coni(0:Nl),Codiorma(0:Nl),Codiorni(0:Nl),Codiorpo(0:Nl),Copo(0:Nl), &\n"
        "     &      Rsconh(0:Nl),Rsconi(0:Nl),Rscodiorma(0:Nl),Rscodiorni(0:Nl),Rscodiorpo(0:Nl),Rscopo(0:Nl)\n"
    )
    if mode == "stageA":
        after_step += (
            f"            If(Sttot.Eq.{split}) Then\n"
            f"              Open(Unit=992,File='{checkpoint_name}',Status='replace',Form='unformatted',"
            "Access='sequential',Convert='little_endian')\n"
            "              Write(992) Rsconh(0),Rsconi(0),Rscodiorma(0),Rscodiorni(0),Rscodiorpo(0)\n"
            "              Close(992)\n"
            "              Close(991)\n"
            f"              Stop {STAGE_A_EXIT}\n"
            "            End If\n"
        )
    source = source.replace(outsel_end, outsel_end + after_step)

    loop_end = "      End do\n!\n!.... Final results"
    if loop_end not in source:
        raise RuntimeError("Animo.for loop-end seam absent")
    source = source.replace(loop_end, "      End do\n      Close(991)\n!\n!.... Final results")
    return source


def compile_variant(
    build_root: Path,
    work_root: Path,
    compiler: str,
    mode: str,
    split: int,
) -> tuple[Path, str, str]:
    name = f"{mode}{split}"
    trace_name = f"trace_{name}.bin"
    checkpoint_name = f"checkpoint_{split}.bin"
    original = (build_root / "src" / "Animo.for").read_bytes().decode("latin1")
    patched = patch_animo(original, mode, split, trace_name, checkpoint_name)
    source_path = work_root / f"Animo_{name}.for"
    object_path = work_root / f"Animo_{name}.o"
    executable = work_root / f"animo_{name}"
    source_path.write_text(patched, encoding="latin1", newline="")

    run(
        [
            compiler,
            *COMPILE_FLAGS,
            "-I",
            str(build_root / "src"),
            "-I",
            str(build_root / "obj"),
            "-J",
            str(build_root / "obj"),
            "-c",
            str(source_path),
            "-o",
            str(object_path),
        ]
    )
    other_objects = sorted(
        str(path)
        for path in (build_root / "obj").glob("*.o")
        if path.name.casefold() != "animo.o"
    )
    run([compiler, str(object_path), *other_objects, *LINK_FLAGS, "-o", str(executable)])
    return executable, trace_name, checkpoint_name


def fresh_run_dir(case_root: Path, work_root: Path, name: str) -> Path:
    target = work_root / f"run_{name}"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(case_root, target)
    return target


def execute_variant(
    executable: Path,
    case_root: Path,
    work_root: Path,
    name: str,
    expected_exit: int,
    checkpoint_source: Path | None = None,
) -> Path:
    run_dir = fresh_run_dir(case_root, work_root, name)
    if checkpoint_source is not None:
        shutil.copy2(checkpoint_source, run_dir / checkpoint_source.name)
    stdout = run([str(executable), "animo.ini"], cwd=run_dir, expected=expected_exit)
    (run_dir / "run_stdout.txt").write_text(stdout, encoding="utf-8")
    return run_dir


def parse_checkpoint(path: Path) -> tuple[list[float], list[str]]:
    data = path.read_bytes()
    if len(data) != 48:
        raise RuntimeError(f"checkpoint size is {len(data)}, expected 48")
    lead = struct.unpack_from("<i", data, 0)[0]
    trail = struct.unpack_from("<i", data, 44)[0]
    if lead != 40 or trail != 40:
        raise RuntimeError(f"checkpoint record markers are {lead}/{trail}, expected 40/40")
    values = list(struct.unpack_from("<5d", data, 4))
    raw_hex = [data[4 + index * 8 : 12 + index * 8].hex() for index in range(5)]
    return values, raw_hex


def inspect_trace(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 12:
        raise RuntimeError(f"trace too short: {path}")
    first_step, first_phase, nl = struct.unpack_from("<iii", data, 0)
    if nl != EXPECTED_NL:
        raise RuntimeError(f"trace Nl={nl}, expected {EXPECTED_NL}")
    record_size = trace_record_size(nl)
    if len(data) % record_size:
        raise RuntimeError(f"trace byte count not divisible by record size: {path}")
    count = len(data) // record_size
    if first_step != 1 or first_phase != 0:
        raise RuntimeError(f"unexpected first trace header: {(first_step, first_phase, nl)}")
    for index in range(count):
        step, phase, record_nl = struct.unpack_from("<iii", data, index * record_size)
        expected_step = index // EXPECTED_RECORDS_PER_STEP + 1
        expected_phase = index % EXPECTED_RECORDS_PER_STEP
        if (step, phase, record_nl) != (expected_step, expected_phase, nl):
            raise RuntimeError(
                f"trace header mismatch at record {index}: {(step, phase, record_nl)}"
            )
    return {
        "sha256": sha256_file(path),
        "size_bytes": len(data),
        "record_size_bytes": record_size,
        "record_count": count,
        "nl": nl,
    }


def decode_record(data: bytes, record_index: int, nl: int) -> dict:
    size = trace_record_size(nl)
    record = data[record_index * size : (record_index + 1) * size]
    step, phase, record_nl = struct.unpack_from("<iii", record, 0)
    if record_nl != nl:
        raise RuntimeError("record Nl mismatch")
    offset = 12
    scalars = dict(zip(TRACE_SCALARS, struct.unpack_from(f"<{len(TRACE_SCALARS)}d", record, offset)))
    offset += len(TRACE_SCALARS) * 8
    arrays: dict[str, tuple[float, ...]] = {}
    for name in TRACE_ARRAYS:
        arrays[name] = struct.unpack_from(f"<{nl + 1}d", record, offset)
        offset += (nl + 1) * 8
    return {"step": step, "phase": phase, "nl": nl, "scalars": scalars, "arrays": arrays}


def first_trace_difference(reference: Path, candidate: Path) -> dict | None:
    left = reference.read_bytes()
    right = candidate.read_bytes()
    if len(left) != len(right):
        raise RuntimeError("cannot localize traces with unequal byte lengths")
    nl = struct.unpack_from("<i", left, 8)[0]
    size = trace_record_size(nl)
    for record_index in range(len(left) // size):
        lrec = left[record_index * size : (record_index + 1) * size]
        rrec = right[record_index * size : (record_index + 1) * size]
        if lrec == rrec:
            continue
        a = decode_record(left, record_index, nl)
        b = decode_record(right, record_index, nl)
        differences: list[dict] = []
        for name in TRACE_SCALARS:
            av = a["scalars"][name]
            bv = b["scalars"][name]
            if struct.pack("<d", av) != struct.pack("<d", bv):
                differences.append({"coordinate": name, "reference": av, "candidate": bv})
        for name in TRACE_ARRAYS:
            for layer, (av, bv) in enumerate(zip(a["arrays"][name], b["arrays"][name])):
                araw = struct.pack("<d", av)
                braw = struct.pack("<d", bv)
                if araw != braw:
                    differences.append(
                        {
                            "coordinate": f"{name}({layer})",
                            "reference": av,
                            "candidate": bv,
                            "reference_raw_hex": araw.hex(),
                            "candidate_raw_hex": braw.hex(),
                        }
                    )
        return {
            "record_index_zero_based": record_index,
            "step": a["step"],
            "phase": a["phase"],
            "differences": differences,
        }
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("testbank_zip", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--compiler", default="gfortran")
    parser.add_argument(
        "--allow-compiler-identity-mismatch",
        action="store_true",
        help="diagnostic only; a mismatched compiler identity is never qualification evidence",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    source_zip = args.source_zip.resolve()
    testbank_zip = args.testbank_zip.resolve()
    output_dir = args.output_dir.resolve()
    require_hash(source_zip, SOURCE_SHA, "source archive")
    require_hash(testbank_zip, TESTBANK_SHA, "testbank archive")

    compiler = compiler_identity(args.compiler)
    compiler_match = compiler == EXPECTED_COMPILER
    if not compiler_match and not args.allow_compiler_identity_mismatch:
        raise SystemExit(f"compiler identity mismatch: {compiler!r}; expected {EXPECTED_COMPILER!r}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    build_root = output_dir / "base_build"
    case_root = output_dir / "case"
    run(
        [
            sys.executable,
            str(repo_root / "tools/build_gnu_diagnostic.py"),
            str(source_zip),
            str(build_root),
            "--compiler",
            args.compiler,
        ]
    )
    run(
        [
            sys.executable,
            str(repo_root / "tools/prepare_gnu_case.py"),
            str(testbank_zip),
            CASE,
            str(case_root),
        ]
    )

    expectations = json.loads(
        (repo_root / "integration/animo-b3/b3b04e1/TCD040_REPLAY_EXPECTATIONS.json").read_text(
            encoding="utf-8"
        )
    )

    variants: dict[str, dict] = {}
    executables: dict[str, tuple[Path, str, str]] = {}
    for mode, split in [
        ("continuous", 282),
        ("stageA", 282),
        ("restore", 282),
        ("legacy", 282),
        ("stageA", 67),
        ("legacy", 67),
    ]:
        name = f"{mode}{split}"
        executable, trace_name, checkpoint_name = compile_variant(
            build_root, output_dir, args.compiler, mode, split
        )
        executables[name] = (executable, trace_name, checkpoint_name)
        variants[name] = {
            "mode": mode,
            "split": split,
            "executable_sha256": sha256_file(executable),
            "trace_filename": trace_name,
            "checkpoint_filename": checkpoint_name,
        }

    # Continuous reference generated from the same frozen B0 execution descendant.
    continuous_exe, continuous_trace_name, _ = executables["continuous282"]
    continuous_dir = execute_variant(
        continuous_exe, case_root, output_dir, "continuous282", NORMAL_EXIT
    )
    continuous_trace = continuous_dir / continuous_trace_name
    variants["continuous282"]["exit_code"] = NORMAL_EXIT
    variants["continuous282"]["trace"] = inspect_trace(continuous_trace)
    if variants["continuous282"]["trace"]["record_count"] != 1800:
        raise RuntimeError("continuous trace does not contain 1800 records")

    stage_a_282_exe, stage_a_282_trace_name, checkpoint_282_name = executables["stageA282"]
    stage_a_282_dir = execute_variant(
        stage_a_282_exe, case_root, output_dir, "stageA282", STAGE_A_EXIT
    )
    stage_a_282_trace = stage_a_282_dir / stage_a_282_trace_name
    checkpoint_282 = stage_a_282_dir / checkpoint_282_name
    variants["stageA282"]["exit_code"] = STAGE_A_EXIT
    variants["stageA282"]["trace"] = inspect_trace(stage_a_282_trace)
    variants["stageA282"]["checkpoint_sha256"] = sha256_file(checkpoint_282)
    variants["stageA282"]["checkpoint_size_bytes"] = checkpoint_282.stat().st_size

    if variants["stageA282"]["trace"]["record_count"] != 564:
        raise RuntimeError("split-282 Stage A trace does not contain 564 records")
    if stage_a_282_trace.read_bytes() != continuous_trace.read_bytes()[: stage_a_282_trace.stat().st_size]:
        raise RuntimeError("split-282 Stage A trace is not an exact continuous prefix")

    checkpoint_values, checkpoint_raw = parse_checkpoint(checkpoint_282)
    expected_split = expectations["split_282"]
    expected_raw = expected_split["checkpoint_binary64_little_endian_hex"]
    for index, name in enumerate(["NH4", "NO3", "DOM", "DON", "DOP"]):
        if checkpoint_raw[index] != expected_raw[name]:
            raise RuntimeError(
                f"split-282 checkpoint {name} raw mismatch: {checkpoint_raw[index]}"
            )
    if sha256_file(checkpoint_282) != expected_split["checkpoint_file_sha256"]:
        raise RuntimeError("split-282 checkpoint file hash does not reproduce B3B04 target")

    restored_exe, restored_trace_name, _ = executables["restore282"]
    restored_dir = execute_variant(
        restored_exe,
        case_root,
        output_dir,
        "restore282",
        NORMAL_EXIT,
        checkpoint_282,
    )
    restored_trace = restored_dir / restored_trace_name
    variants["restore282"]["exit_code"] = NORMAL_EXIT
    variants["restore282"]["trace"] = inspect_trace(restored_trace)
    if restored_trace.read_bytes() != continuous_trace.read_bytes():
        raise RuntimeError("corrected split-282 restore is not full-trace exact")

    legacy_exe, legacy_trace_name, _ = executables["legacy282"]
    legacy_dir = execute_variant(
        legacy_exe,
        case_root,
        output_dir,
        "legacy282",
        NORMAL_EXIT,
        checkpoint_282,
    )
    legacy_trace = legacy_dir / legacy_trace_name
    variants["legacy282"]["exit_code"] = NORMAL_EXIT
    variants["legacy282"]["trace"] = inspect_trace(legacy_trace)
    divergence = first_trace_difference(continuous_trace, legacy_trace)
    if divergence is None:
        raise RuntimeError("defective split-282 replay did not diverge")
    if (
        divergence["record_index_zero_based"] != 564
        or divergence["step"] != 283
        or divergence["phase"] != 0
        or [item["coordinate"] for item in divergence["differences"]] != TARGET_LAYER0
    ):
        raise RuntimeError(f"unexpected first split-282 divergence: {divergence}")
    if any(item["candidate_raw_hex"] != "0000000000000000" for item in divergence["differences"]):
        raise RuntimeError("defective split-282 first divergence is not exact positive zero")

    stage_a_67_exe, stage_a_67_trace_name, checkpoint_67_name = executables["stageA67"]
    stage_a_67_dir = execute_variant(
        stage_a_67_exe, case_root, output_dir, "stageA67", STAGE_A_EXIT
    )
    stage_a_67_trace = stage_a_67_dir / stage_a_67_trace_name
    checkpoint_67 = stage_a_67_dir / checkpoint_67_name
    variants["stageA67"]["exit_code"] = STAGE_A_EXIT
    variants["stageA67"]["trace"] = inspect_trace(stage_a_67_trace)
    variants["stageA67"]["checkpoint_sha256"] = sha256_file(checkpoint_67)
    variants["stageA67"]["checkpoint_size_bytes"] = checkpoint_67.stat().st_size
    if variants["stageA67"]["trace"]["record_count"] != 134:
        raise RuntimeError("split-67 Stage A trace does not contain 134 records")
    if stage_a_67_trace.read_bytes() != continuous_trace.read_bytes()[: stage_a_67_trace.stat().st_size]:
        raise RuntimeError("split-67 Stage A trace is not an exact continuous prefix")
    _, checkpoint_67_raw = parse_checkpoint(checkpoint_67)
    if any(raw != "0000000000000000" for raw in checkpoint_67_raw):
        raise RuntimeError(f"split-67 checkpoint target is not exact positive zero: {checkpoint_67_raw}")

    legacy_67_exe, legacy_67_trace_name, _ = executables["legacy67"]
    legacy_67_dir = execute_variant(
        legacy_67_exe,
        case_root,
        output_dir,
        "legacy67",
        NORMAL_EXIT,
        checkpoint_67,
    )
    legacy_67_trace = legacy_67_dir / legacy_67_trace_name
    variants["legacy67"]["exit_code"] = NORMAL_EXIT
    variants["legacy67"]["trace"] = inspect_trace(legacy_67_trace)
    if legacy_67_trace.read_bytes() != continuous_trace.read_bytes():
        raise RuntimeError("split-67 exact-zero negative control is not full-trace exact")

    result = {
        "workunit": "ANIMO-B3B04E1",
        "target": "TCD-040",
        "evidence_class": "RECONSTRUCTED_REPLAY_HARNESS_FOR_EXISTING_CLAIM",
        "new_scientific_claim_created": False,
        "production_source_modified": False,
        "frozen_b0_modified": False,
        "source_archive_sha256": SOURCE_SHA,
        "testbank_archive_sha256": TESTBANK_SHA,
        "case": CASE,
        "compiler": compiler,
        "compiler_identity_matches_pinned_authoring_toolchain": compiler_match,
        "compile_flags": COMPILE_FLAGS,
        "link_flags": LINK_FLAGS,
        "trace_contract": {
            "byte_order": "little-endian",
            "record_layout": [
                "int32 Sttot",
                "int32 phase (0=post-Init/pre-process; 1=post-process/post-Outsel)",
                "int32 Nl",
                *[f"binary64 {name}" for name in TRACE_SCALARS],
                *[f"binary64 {name}(0:Nl)" for name in TRACE_ARRAYS],
            ],
            "record_size_bytes_for_Nl30": trace_record_size(30),
            "comparison": "EXACT_BYTES_NO_TOLERANCE",
        },
        "split_282": {
            "checkpoint_values": checkpoint_values,
            "checkpoint_raw_little_endian_hex": checkpoint_raw,
            "checkpoint_sha256": sha256_file(checkpoint_282),
            "checkpoint_reproduces_prior_B3B04_hash": True,
            "stage_a_records": 564,
            "stage_a_exact_continuous_prefix": True,
            "continuous_records": 1800,
            "corrected_restore_full_trace_exact": True,
            "first_defective_divergence": divergence,
        },
        "split_67": {
            "checkpoint_raw_little_endian_hex": checkpoint_67_raw,
            "checkpoint_all_five_targets_exact_positive_zero": True,
            "stage_a_records": 134,
            "stage_a_exact_continuous_prefix": True,
            "legacy_zeroing_full_trace_exact": True,
        },
        "variants": variants,
        "gate_note": (
            "This executable reconstruction removes the missing-harness blocker only. "
            "It is not independently provenance-qualified until the exact B0 artifacts "
            "are obtainable through the controlled immutable acquisition route required by EG01."
        ),
    }
    result_path = output_dir / "TCD040_RECONSTRUCTED_REPLAY_RESULT.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
