#!/usr/bin/env python3
"""Run the qualification-only ANIMO-STATEQ01 RC-R5 source-component probe.

The probe compiles the repository fixture against the original hash-pinned
revision-53 TRANSPORT.FOR and Transsub.for. It does not modify ANIMO source and
does not claim full-model restart equivalence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE_ARCHIVE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED = {
    "TRANSPORT.FOR": "3f597b896ab5514e0b836f5547b342e317b03c8e3e58e053e113bd1c17e2f998",
    "Transsub.for": "c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552",
    "Param.inc": "20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475",
}

DIAGNOSTIC_FLAGS = [
    "-O0",
    "-ffree-form",
    "-ffree-line-length-none",
    "-fallow-argument-mismatch",
    "-std=legacy",
    "-fdefault-real-8",
    "-fdefault-double-8",
    "-fno-automatic",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_vector(line: str) -> list[float]:
    return [float(x) for x in line.split()[1:]]


def parse_bool(line: str) -> bool:
    return line.split()[-1].upper() == "T"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path, help="Extracted ANIMO_4.1.5.53 source directory")
    parser.add_argument(
        "--driver",
        type=Path,
        default=Path("tests/stateq01/fixtures/stateq01_rc5_nh4_adsorption_probe.f90"),
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    driver = args.driver.resolve()

    mismatches: dict[str, dict[str, str]] = {}
    for name, expected in EXPECTED.items():
        actual = sha256(source_dir / name)
        if actual != expected:
            mismatches[name] = {"expected": expected, "actual": actual}
    if mismatches:
        raise SystemExit(f"Frozen-source hash mismatch: {mismatches}")

    compiler = subprocess.run(
        ["gfortran", "--version"], check=True, text=True, capture_output=True
    ).stdout.splitlines()[0]

    with tempfile.TemporaryDirectory(prefix="stateq01_rc5_") as td:
        td_path = Path(td)
        shutil.copy2(source_dir / "TRANSPORT.FOR", td_path / "TRANSPORT.FOR")
        shutil.copy2(source_dir / "Transsub.for", td_path / "Transsub.for")
        # Revision 53 includes lowercase 'param.inc' while the archive stores Param.inc.
        # This is a build-environment compatibility copy only.
        shutil.copy2(source_dir / "Param.inc", td_path / "param.inc")

        exe = td_path / "probe.exe"
        cmd = [
            "gfortran",
            *DIAGNOSTIC_FLAGS,
            "-I",
            str(td_path),
            str(td_path / "TRANSPORT.FOR"),
            str(td_path / "Transsub.for"),
            str(driver),
            "-o",
            str(exe),
        ]
        compile_proc = subprocess.run(
            cmd, check=True, cwd=td_path, text=True, capture_output=True
        )
        run_proc = subprocess.run(
            [str(exe)], check=True, cwd=td_path, text=True, capture_output=True
        )

        lines = [line.strip() for line in run_proc.stdout.splitlines() if line.strip()]
        parsed: dict[str, object] = {}
        for line in lines:
            if line.startswith("CHECKPOINT_RSCO "):
                parsed["checkpoint_rsco"] = parse_vector(line)[0]
            elif line.startswith("CHECKPOINT_RSCX "):
                parsed["checkpoint_rscx"] = parse_vector(line)[0]
            elif line.startswith("RECONSTRUCTED_CX "):
                parsed["reconstructed_cx"] = parse_vector(line)[0]
            elif line.startswith("CHECKPOINT_EQ_RECONSTRUCTED_CX "):
                parsed["checkpoint_equals_reconstructed_cx_exact"] = parse_bool(line)
            elif line.startswith("CONT_FINAL "):
                parsed["continuous_final"] = parse_vector(line)
            elif line.startswith("RECON_FINAL "):
                parsed["reconstructed_final"] = parse_vector(line)
            elif line.startswith("OMIT_FINAL "):
                parsed["omitted_final"] = parse_vector(line)
            elif line.startswith("CONT_EQ_RECON "):
                parsed["continuous_equals_reconstructed_exact"] = parse_bool(line)
            elif line.startswith("CONT_EQ_OMIT_PHYSICAL "):
                parsed["continuous_equals_omitted_physical_exact"] = parse_bool(line)

        logs = {
            name: (td_path / name).read_text(encoding="utf-8", errors="replace")
            for name in ["step1.log", "continuous.log", "reconstructed.log", "omitted.log"]
        }
        warning_token = "deviation in massbalance"
        clean_logs = {
            name: warning_token not in text.lower()
            for name, text in logs.items()
            if name != "omitted.log"
        }
        omitted_warning = warning_token in logs["omitted.log"].lower()

        if not parsed.get("checkpoint_equals_reconstructed_cx_exact"):
            raise SystemExit("RC-R5 probe failed: reconstructed adsorbed NH4 differs from accepted Rscx")
        if not parsed.get("continuous_equals_reconstructed_exact"):
            raise SystemExit("RC-R5 probe failed: reconstructed path differs from uninterrupted source component")
        if not all(clean_logs.values()):
            raise SystemExit(f"RC-R5 probe failed: unexpected balance warning in control path: {clean_logs}")
        if not omitted_warning:
            raise SystemExit("RC-R5 probe failed: omission sentinel did not expose missing adsorbed storage in TRANSPORT balance check")
        if not parsed.get("continuous_equals_omitted_physical_exact"):
            raise SystemExit(
                "RC-R5 probe assumption changed: Cx omission now affects component physical outputs; reassess owner classification"
            )
        if parsed.get("checkpoint_rsco") == 0.010:
            raise SystemExit("RC-R5 probe failed: step-1 transport did not create a nontrivial accepted concentration")

        result = {
            "workunit": "ANIMO-STATEQ01",
            "test_id": "RC-R5-source-component",
            "status": "PASS_FROZEN_SOURCE_COMPONENT_RECONSTRUCTION_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN",
            "evidence_class": "B0_HASH_PINNED_SOURCE_COMPONENT_EXECUTION_NOT_B2",
            "canonical_state_admission": "NOT_ADMITTED",
            "canonical_time_admission": "NOT_ADMITTED",
            "production_code": False,
            "physics_change": False,
            "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
            "source_file_hashes": EXPECTED,
            "driver_sha256": sha256(driver),
            "compiler": compiler,
            "compiler_flags": DIAGNOSTIC_FLAGS,
            "compile_stderr": compile_proc.stderr.splitlines(),
            "stdout": lines,
            "executable_sha256": sha256(exe),
            "results": parsed,
            "balance_logs": {
                "control_paths_warning_free": all(clean_logs.values()),
                "omitted_adsorbed_storage_warning": omitted_warning,
                "omitted_log": logs["omitted.log"].splitlines(),
            },
            "interpretation": {
                "accepted_rscx_equals_candidate_reconstruction_exact_within_build": True,
                "next_component_outputs_equal_uninterrupted_vs_reconstructed_exact_within_build": True,
                "omitting_cx_changes_component_physical_outputs": False,
                "omitting_cx_breaks_original_transport_storage_ledger_check": True,
                "independent_mutable_adsorbed_nh4_owner_supported": False,
                "physical_adsorbed_nh4_storage_can_be_dropped_from_control_volume": False,
            },
            "qualification_boundary": "original frozen TRANSPORT.FOR plus Transsub.for component only under deterministic GNU diagnostic build contract; no full revision-53 profile-clean split, no historical B2 oracle and no canonical numerical policy admission",
        }

    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
