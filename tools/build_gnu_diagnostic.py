#!/usr/bin/env python3
"""Build a reproducible GNU Fortran diagnostic ANIMO executable from the
supplied frozen source archive.

Qualification tooling only. The produced executable is DIAGNOSTIC_NOT_REFERENCE.
The script never edits the supplied archive. It extracts an execution copy,
applies only explicitly documented portability adaptations there, and fails
closed if source identity or expected adaptation counts differ.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = (
    "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
)

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
EXCLUDED_ALTERNATE_UNITS = {"input1_1.for", "Outselorg.for"}

OUTSEL_PATTERN = re.compile(
    r"\(\(\s*([A-Za-z0-9_]+\(Drn\),Comma)\s*\),\s*Drn=1,Nudr\)"
)

DFPORT_SHIM = """module dfport
  implicit none
contains
  real(4) function secnds(x)
    real(4), intent(in) :: x
    real(4) :: t
    call cpu_time(t)
    secnds = t - x
  end function secnds
end module dfport
"""

INTEL_INTRINSICS_SHIM = """integer(8) function kint(x)
  real(4), intent(in) :: x
  kint = int(x, kind=8)
end function kint
integer(8) function kidnnt(x)
  real(8), intent(in) :: x
  kidnnt = nint(x, kind=8)
end function kidnnt
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str], log_path: Path, cwd: Path) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log_path.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(
            f"command failed with status {result.returncode}: {command}; "
            f"see {log_path}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--compiler", default="gfortran")
    args = parser.parse_args()

    source_zip = args.source_zip.resolve()
    output_dir = args.output_dir.resolve()

    actual_sha = sha256(source_zip)
    if actual_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"source archive SHA-256 mismatch: {actual_sha}")

    if output_dir.exists():
        shutil.rmtree(output_dir)

    source_dir = output_dir / "src"
    object_dir = output_dir / "obj"
    log_dir = output_dir / "logs"
    source_dir.mkdir(parents=True)
    object_dir.mkdir()
    log_dir.mkdir()

    with zipfile.ZipFile(source_zip) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        roots = {Path(member.filename).parts[0] for member in members}
        if len(roots) != 1:
            raise SystemExit("unexpected archive root layout")

        for member in members:
            relative = Path(*Path(member.filename).parts[1:])
            if not relative.parts:
                continue
            target = source_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))

    # The supplied source assumes case-insensitive include-name resolution.
    for alias, original in [
        ("param.inc", "Param.inc"),
        ("Param.Inc", "Param.inc"),
        ("animo.inc", "Animo.inc"),
        ("Animo.Inc", "Animo.inc"),
    ]:
        (source_dir / alias).write_bytes((source_dir / original).read_bytes())

    # GNU rejects one nested implied-do output-list construct in Outsel.for.
    # Create an execution-only syntax-equivalent copy and fail closed if the
    # expected source pattern count changes.
    outsel_text = (source_dir / "Outsel.for").read_bytes().decode("latin1")
    patched_outsel, substitutions = OUTSEL_PATTERN.subn(
        r"(\1,Drn=1,Nudr)", outsel_text
    )
    if substitutions != 14:
        raise SystemExit(
            f"expected 14 Outsel compatibility substitutions, got {substitutions}"
        )
    (source_dir / "Outsel_gnu.for").write_text(
        patched_outsel, encoding="latin1", newline=""
    )

    (source_dir / "dfport_shim.f90").write_text(DFPORT_SHIM, encoding="utf-8")
    (source_dir / "intel_intrinsics_shim.f90").write_text(
        INTEL_INTRINSICS_SHIM, encoding="utf-8"
    )

    compiler_version = subprocess.run(
        [args.compiler, "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    ).stdout.splitlines()[0]

    compile_base = [
        args.compiler,
        *COMPILE_FLAGS,
        "-I",
        ".",
        "-I",
        "../obj",
        "-J",
        "../obj",
    ]

    objects: list[str] = []

    for shim in ["dfport_shim.f90", "intel_intrinsics_shim.f90"]:
        object_name = f"../obj/{Path(shim).stem}.o"
        run(
            [*compile_base, "-c", shim, "-o", object_name],
            log_dir / f"{shim}.log",
            source_dir,
        )
        objects.append(f"obj/{Path(shim).stem}.o")

    source_names = sorted(
        [
            path.name
            for path in source_dir.iterdir()
            if path.suffix.lower() in {".for", ".f90"}
            and path.name not in EXCLUDED_ALTERNATE_UNITS
            and path.name
            not in {
                "Outsel_gnu.for",
                "dfport_shim.f90",
                "intel_intrinsics_shim.f90",
            }
        ],
        key=str.lower,
    )

    if len(source_names) != 58:
        raise SystemExit(
            f"expected 58 selected legacy compilation units, got {len(source_names)}"
        )

    for source_name in source_names:
        compile_name = "Outsel_gnu.for" if source_name == "Outsel.for" else source_name
        object_name = f"../obj/{Path(source_name).stem}.o"
        run(
            [*compile_base, "-c", compile_name, "-o", object_name],
            log_dir / f"{source_name}.log",
            source_dir,
        )
        objects.append(f"obj/{Path(source_name).stem}.o")

    run(
        [args.compiler, *objects, *LINK_FLAGS, "-o", "animo_diag"],
        log_dir / "link.log",
        output_dir,
    )

    executable = output_dir / "animo_diag"
    metadata = {
        "evidence_class": "DIAGNOSTIC_NOT_REFERENCE",
        "source_zip_sha256": EXPECTED_SOURCE_SHA256,
        "compiler": compiler_version,
        "compile_flags": COMPILE_FLAGS,
        "link_flags": LINK_FLAGS,
        "selected_legacy_units": len(source_names),
        "excluded_alternate_units": sorted(EXCLUDED_ALTERNATE_UNITS),
        "outsel_compatibility_substitutions": substitutions,
        "executable_sha256": sha256(executable),
        "frozen_source_modified": False,
    }
    (output_dir / "build_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
