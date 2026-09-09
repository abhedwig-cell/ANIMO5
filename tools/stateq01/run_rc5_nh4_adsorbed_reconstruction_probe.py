#!/usr/bin/env python3
"""Run the ANIMO-STATEQ01 RC-R5 frozen Transport reconstruction probe.

The probe verifies only revision-53 TRANSPORT.FOR's adsorbed-NH4 result
construction and its balance-diagnostic dependence on the beginning adsorbed
amount. The concentration solver is deliberately stubbed by the persisted
fixture so this does not claim a full transport or ANIMO split-run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

SOURCE_ARCHIVE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED = {
    "TRANSPORT.FOR": "3f597b896ab5514e0b836f5547b342e317b03c8e3e58e053e113bd1c17e2f998",
    "Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058",
    "Param.inc": "20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_source_dir(root: Path) -> Path:
    matches = [p.parent for p in root.rglob("TRANSPORT.FOR") if (p.parent / "Init.for").exists()]
    if len(matches) != 1:
        raise SystemExit(f"Expected one extracted revision-53 source directory, found {len(matches)}")
    return matches[0]


def parse_bool(lines: list[str], key: str) -> bool:
    prefix = key + "="
    matches = [line for line in lines if line.startswith(prefix)]
    if len(matches) != 1:
        raise SystemExit(f"Missing or duplicate probe marker {key}")
    return matches[0][len(prefix):].strip() == "T"


def run_build(source_dir: Path, driver: Path, flags: list[str]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="stateq01_rc5_") as td:
        td_path = Path(td)
        shutil.copy2(source_dir / "TRANSPORT.FOR", td_path / "TRANSPORT.FOR")
        # Revision 53 includes lowercase 'param.inc' while the archive stores Param.inc.
        shutil.copy2(source_dir / "Param.inc", td_path / "param.inc")
        exe = td_path / "probe.exe"
        compile_cmd = [
            "gfortran", "-ffree-form", *flags,
            str(td_path / "TRANSPORT.FOR"), str(driver), "-o", str(exe),
        ]
        compile_proc = subprocess.run(compile_cmd, check=True, text=True, capture_output=True, cwd=td_path)
        run_proc = subprocess.run([str(exe)], check=True, text=True, capture_output=True, cwd=td_path)
        lines = [line.strip() for line in run_proc.stdout.splitlines() if line.strip()]
        checks = {
            "exact_reconstruction": parse_bool(lines, "EXACT_RECONSTRUCTION"),
            "uninterrupted_diagnostic_empty": parse_bool(lines, "UNINTERRUPTED_DIAGNOSTIC_EMPTY"),
            "split_diagnostic_empty": parse_bool(lines, "SPLIT_DIAGNOSTIC_EMPTY"),
            "omitted_cx_diagnostic_present": parse_bool(lines, "OMITTED_CX_DIAGNOSTIC_PRESENT"),
        }
        if not all(checks.values()):
            raise SystemExit(f"RC-R5 source probe failed: {checks}")
        return {
            "flags": flags,
            "compiler_command": compile_cmd,
            "compiler_stderr": [line for line in compile_proc.stderr.splitlines() if line.strip()],
            "stdout": lines,
            "checks": checks,
            "executable_sha256": sha256(exe),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_archive", type=Path)
    parser.add_argument(
        "--driver",
        type=Path,
        default=Path("tests/stateq01/fixtures/stateq01_rc5_nh4_adsorbed_reconstruction_probe.f90"),
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    archive = args.source_archive.resolve()
    driver = args.driver.resolve()
    actual_archive_hash = sha256(archive)
    if actual_archive_hash != SOURCE_ARCHIVE_SHA256:
        raise SystemExit(f"Frozen-source archive hash mismatch: {actual_archive_hash}")

    with tempfile.TemporaryDirectory(prefix="stateq01_rc5_src_") as td:
        root = Path(td)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(root)
        source_dir = find_source_dir(root)
        mismatches = {}
        for name, expected in EXPECTED.items():
            actual = sha256(source_dir / name)
            if actual != expected:
                mismatches[name] = {"expected": expected, "actual": actual}
        if mismatches:
            raise SystemExit(f"Frozen-source file hash mismatch: {mismatches}")

        compiler = subprocess.run(["gfortran", "--version"], check=True, text=True, capture_output=True).stdout.splitlines()[0]
        builds = [
            {"id": "GNU_DEFAULT_REAL", **run_build(source_dir, driver, ["-O0"])},
            {
                "id": "GNU_DEFAULT_REAL_8_DOUBLE_8_COMPAT",
                **run_build(
                    source_dir,
                    driver,
                    ["-O0", "-fdefault-real-8", "-fdefault-double-8"],
                ),
            },
        ]

    result = {
        "workunit": "ANIMO-STATEQ01",
        "test_id": "RC-R5-source-component",
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_file_hashes": EXPECTED,
        "driver_sha256": sha256(driver),
        "compiler": compiler,
        "builds": builds,
        "result": "PASS_FROZEN_SOURCE_COMPONENT_RECONSTRUCTION_DIAGNOSTIC_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN",
        "claims": {
            "rscx_exactly_reconstructed_from_rsco_he_rhbd_socf_with_same_source_expression": True,
            "reconstructed_split_preserves_transport_balance_diagnostic_for_probe": True,
            "omitting_reconstruction_changes_transport_balance_diagnostic": True,
            "physical_trajectory_split_run_qualified": False,
            "canonical_state_admitted": False,
            "b2_historical_reference": False,
        },
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
