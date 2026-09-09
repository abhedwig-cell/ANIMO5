#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

DIAGNOSTIC_FLAGS = [
    "-ffree-form",
    "-ffree-line-length-none",
    "-fallow-argument-mismatch",
    "-std=legacy",
    "-fdefault-real-8",
    "-fdefault-double-8",
    "-fno-automatic",
]

PROGRAM = r"""program prep10_storage_probe
  implicit none
  integer :: i
  do i = 1, 3
    call acc(i)
  end do
contains
  subroutine acc(i)
    integer, intent(in) :: i
    real :: x
    x = x + 1.0
    write(*,'(I0,1X,ES24.16)') i, x
  end subroutine acc
end program prep10_storage_probe
"""


def run_mode(compiler: str, work: Path, name: str, flags: list[str]) -> dict:
    src = work / f"{name}.f90"
    exe = work / name
    src.write_text(PROGRAM, encoding="utf-8")
    compile_cmd = [compiler, *flags, str(src), "-o", str(exe)]
    cp = subprocess.run(compile_cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if cp.returncode:
        return {
            "name": name,
            "flags": flags,
            "compile_returncode": cp.returncode,
            "compile_output": cp.stdout,
            "run_returncode": None,
            "stdout": None,
            "values": [],
        }
    rp = subprocess.run([str(exe)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    values = []
    for line in rp.stdout.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            try:
                values.append(float(parts[1]))
            except ValueError:
                pass
    return {
        "name": name,
        "flags": flags,
        "compile_returncode": cp.returncode,
        "compile_output": cp.stdout,
        "run_returncode": rp.returncode,
        "stdout": rp.stdout,
        "values": [("NaN" if math.isnan(v) else v) for v in values],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Probe local-storage behavior relevant to the PREP10 GNU diagnostic build contract.")
    ap.add_argument("--compiler", default="gfortran")
    ap.add_argument("--json", type=Path, dest="json_path")
    ns = ap.parse_args()

    version = subprocess.run(
        [ns.compiler, "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    ).stdout.splitlines()[0]

    with tempfile.TemporaryDirectory(prefix="prep10-storage-probe-") as td:
        work = Path(td)
        diagnostic = run_mode(ns.compiler, work, "diagnostic_contract", DIAGNOSTIC_FLAGS)
        snan = run_mode(ns.compiler, work, "snan_observer", [*DIAGNOSTIC_FLAGS, "-finit-real=snan"])
        automatic = run_mode(
            ns.compiler,
            work,
            "automatic_control",
            [f for f in DIAGNOSTIC_FLAGS if f != "-fno-automatic"],
        )

    diagnostic_persists = diagnostic["values"] == [1.0, 2.0, 3.0]
    snan_exposes = snan["values"] == ["NaN", "NaN", "NaN"]
    result = {
        "classification": (
            "CURRENT_GNU_DIAGNOSTIC_CONTRACT_LOCAL_STATE_PERSISTENCE_CONFIRMED_BY_SYNTHETIC_PROBE"
            if diagnostic_persists
            else "GNU_DIAGNOSTIC_CONTRACT_LOCAL_STATE_PERSISTENCE_NOT_CONFIRMED"
        ),
        "compiler": version,
        "diagnostic_contract_flags": DIAGNOSTIC_FLAGS,
        "diagnostic_contract_probe": diagnostic,
        "snan_observer_probe": snan,
        "automatic_control_probe": automatic,
        "diagnostic_contract_local_state_persists_across_calls": diagnostic_persists,
        "snan_observer_exposes_undefined_first_read": snan_exposes,
        "scope_note": (
            "Synthetic compiler-semantics probe only. It demonstrates behavior of the current GNU diagnostic "
            "flag contract for this local self-read pattern, not the numerical magnitude of ANIMO Addit.for "
            "and not the historical Intel reference behavior."
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if ns.json_path:
        ns.json_path.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if diagnostic_persists and snan_exposes else 2


if __name__ == "__main__":
    raise SystemExit(main())
