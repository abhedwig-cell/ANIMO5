#!/usr/bin/env python3
"""Run the qualification-only ANIMO-STATEQ01 RC-R12 source component probe.

This tool does not modify ANIMO source. It expects an extracted copy of the
hash-pinned revision-53 source archive and compiles the repository probe driver
against the original UBoundconc.for.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE_ARCHIVE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED = {
    "UBoundconc.for": "b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7",
    "Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058",
    "Output_Init.for": "6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f",
    "Transgen.for": "cd5efa76c1a4840b50901ee5015940b74c5fe4df79aca43d53a4a4cb77b9fecb",
    "Transca.for": "7f31150050bd41aef203587818cde94cf689e6288094b2ad84aea34732b07ff9",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_vector(line: str) -> list[float]:
    return [float(x) for x in line.split()[1:]]


def run_build(source_dir: Path, driver: Path, flags: list[str]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="stateq01_rc12_") as td:
        td_path = Path(td)
        # Revision-53 includes lowercase 'param.inc' while the archive stores
        # Param.inc. Provide a build-environment compatibility copy only.
        shutil.copy2(source_dir / "Param.inc", td_path / "param.inc")
        shutil.copy2(source_dir / "UBoundconc.for", td_path / "UBoundconc.for")
        shutil.copy2(source_dir / "Param.inc", td_path / "Param.inc")
        exe = td_path / "probe.exe"
        cmd = ["gfortran", *flags, "-I", str(td_path), str(td_path / "UBoundconc.for"), str(driver), "-o", str(exe)]
        subprocess.run(cmd, check=True, cwd=td_path)
        proc = subprocess.run([str(exe)], check=True, text=True, capture_output=True, cwd=td_path)
        lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        values: dict[str, object] = {"compiler_command": cmd, "stdout": lines, "executable_sha256": sha256(exe)}
        for line in lines:
            if line.startswith("CONT_FINAL "):
                values["continuous_final"] = parse_vector(line)
            elif line.startswith("SPLIT_FINAL "):
                values["split_final"] = parse_vector(line)
            elif line.startswith("OMITTED_FINAL "):
                values["omitted_checkpoint_final"] = parse_vector(line)
            elif line.startswith("CONT_EQ_SPLIT "):
                values["continuous_equals_split_exact_within_build"] = line.endswith("T")
            elif line.startswith("OMITTED_DIFFERS "):
                values["omitted_checkpoint_differs"] = line.endswith("T")
        if not values.get("continuous_equals_split_exact_within_build"):
            raise SystemExit("RC-R12 probe failed: split path differs from uninterrupted component path")
        if not values.get("omitted_checkpoint_differs"):
            raise SystemExit("RC-R12 probe failed: omission sentinel did not change result")
        return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path, help="Extracted ANIMO_4.1.5.53 source directory")
    parser.add_argument(
        "--driver",
        type=Path,
        default=Path("tests/stateq01/fixtures/stateq01_rc12_upper_boundary_probe.f90"),
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    driver = args.driver.resolve()
    mismatches = {}
    for name, expected in EXPECTED.items():
        actual = sha256(source_dir / name)
        if actual != expected:
            mismatches[name] = {"expected": expected, "actual": actual}
    if mismatches:
        raise SystemExit(f"Frozen-source hash mismatch: {mismatches}")

    compiler = subprocess.run(["gfortran", "--version"], check=True, text=True, capture_output=True).stdout.splitlines()[0]
    result = {
        "workunit": "ANIMO-STATEQ01",
        "test_id": "RC-R12-source-component",
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_file_hashes": EXPECTED,
        "driver_sha256": sha256(driver),
        "compiler": compiler,
        "builds": [
            {"id": "GNU_DEFAULT_REAL", "flags": ["-O0"], **run_build(source_dir, driver, ["-O0"])},
            {
                "id": "GNU_DEFAULT_REAL_8_QUALIFICATION_VARIANT",
                "flags": ["-O0", "-fdefault-real-8"],
                **run_build(source_dir, driver, ["-O0", "-fdefault-real-8"]),
            },
        ],
        "result": "PASS_FROZEN_SOURCE_COMPONENT_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN",
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
