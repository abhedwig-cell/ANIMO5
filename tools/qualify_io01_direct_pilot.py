#!/usr/bin/env python3
"""Reproduce ANIMO-IO01 Pilot A against frozen B0 steering files.

The runner requires user-supplied frozen archives. It never downloads TTUTIL.
It verifies the SWAP 4.3.1 and ANIMO testbank identities, materializes the exact
embedded TTUTIL 4.27 source, builds it with GNU Fortran, and compares the
normalized DIRECT routing object produced by the revision-53 compatibility
parser with a separate TTUTILNativeTextAdapter/v1 representation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


direct = _load("io01_direct_pilot", TOOLS / "io01_direct_pilot.py")
materializer = _load("materialize_ttutil427", TOOLS / "materialize_ttutil427.py")

TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
EXPECTED_CASES = (
    "ANIMO_testbank/CranGrass/animo.ini",
    "ANIMO_testbank/CranMais/animo.ini",
    "ANIMO_testbank/GHGMais/animo.ini",
    "ANIMO_testbank/GrassPeat/animo.ini",
    "ANIMO_testbank/LWKM_gras_1040.2021.2045/animo.ini",
    "ANIMO_testbank/Puitmijn_Cranendonck_60/animo.ini",
    "ANIMO_testbank/Puitmijn_Cranendonck_60/input/animo.ini",
    "ANIMO_testbank/RuurloGrass/animo.ini",
    "ANIMO_testbank/STONE_akk_0006.2001.2015/animo.ini",
    "ANIMO_testbank/Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA/animo.ini",
)
PERMUTED_NATIVE_FIELDS = (
    "MAT", "GEN", "SOI", "PLA", "INI", "BOU", "MAN", "SWU",
    "WAI", "WAU", "CHE", "INO", "CRU", "STE",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _quote_ttutil(value: str) -> str:
    if "'" in value or "\n" in value or "\r" in value:
        raise ValueError(
            "TTUTIL DIRECT-v1 string escaping is not qualified for quote/newline characters"
        )
    return "'" + value + "'"


def render_native_direct_v1(legacy: dict[str, object]) -> str:
    lines = [f"SchemaVersion = '{direct.NATIVE_SCHEMA_VERSION}'"]
    bindings = legacy["bindings"]
    assert isinstance(bindings, dict)
    for field in PERMUTED_NATIVE_FIELDS:
        item = bindings[field]
        if item["presence"] == "EXPLICIT":
            value = item["value"]
            if not isinstance(value, str):
                raise ValueError(f"unexpected non-string binding {field}")
            lines.append(f"{field} = {_quote_ttutil(value)}")
    lines.insert(2 if len(lines) > 1 else 1, f"AnimoVersion = {legacy['animo_version']}")
    message = legacy["message_output"]
    if message["presence"] == "EXPLICIT":
        lines.append(f"MES = {_quote_ttutil(str(message['value']))}")
    return "\n".join(lines) + "\n"


def _fortran_order(swap_zip: Path) -> list[str]:
    with zipfile.ZipFile(swap_zip, "r") as outer:
        inner_bytes = outer.read(materializer.EMBEDDED_PATH)
    order: list[str] = []
    with zipfile.ZipFile(io.BytesIO(inner_bytes), "r") as inner:
        for zi in inner.infolist():
            if zi.is_dir():
                continue
            p = PurePosixPath(zi.filename)
            if p.suffix.lower() in (".for", ".f90"):
                order.append(p.name)
    return order


def _run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def build_ttutil_and_probe(
    swap_zip: Path,
    source: Path,
    build: Path,
    probe_source: Path,
) -> tuple[Path, str, int]:
    compiler = shutil.which("gfortran")
    if compiler is None:
        raise RuntimeError("gfortran is required for the TTUTIL runtime qualification")
    version = _run([compiler, "--version"]).stdout.splitlines()[0]
    build.mkdir(parents=True, exist_ok=True)
    flags = [
        "-c",
        "-O0",
        "-std=legacy",
        "-fallow-argument-mismatch",
        f"-I{source}",
        f"-J{build}",
    ]
    order = _fortran_order(swap_zip)
    if "ttutilprefs.f90" not in order:
        raise RuntimeError("official TTUTIL source lacks ttutilprefs.f90")
    compile_order = ["ttutilprefs.f90", *[f for f in order if f != "ttutilprefs.f90"]]
    for name in compile_order:
        _run([compiler, *flags, str(source / name)], cwd=build)
    objects = sorted(build.glob("*.o"))
    if len(objects) != 153:
        raise RuntimeError(f"expected 153 TTUTIL objects, got {len(objects)}")
    library = build / "libttutil427.a"
    ar = shutil.which("ar")
    if ar is None:
        raise RuntimeError("ar is required")
    _run([ar, "rcs", str(library), *[str(p) for p in objects]], cwd=build)
    probe = build / "ttutil_direct_probe"
    _run(
        [
            compiler,
            "-O0",
            "-std=legacy",
            "-fallow-argument-mismatch",
            f"-I{source}",
            f"-I{build}",
            str(probe_source),
            str(library),
            "-o",
            str(probe),
        ],
        cwd=build,
    )
    return probe, version, len(objects)


def _read_cases(testbank_zip: Path) -> dict[str, str]:
    digest = sha256_file(testbank_zip)
    if digest != TESTBANK_SHA256:
        raise ValueError(f"ANIMO testbank SHA-256 mismatch: {digest}")
    with zipfile.ZipFile(testbank_zip, "r") as z:
        names = {n for n in z.namelist() if n.lower().endswith("animo.ini")}
        if names != set(EXPECTED_CASES):
            raise ValueError(
                "unexpected natural DIRECT case set: "
                f"missing={sorted(set(EXPECTED_CASES)-names)}, "
                f"extra={sorted(names-set(EXPECTED_CASES))}"
            )
        return {name: z.read(name).decode("latin-1") for name in EXPECTED_CASES}


def qualify(
    swap_zip: Path,
    testbank_zip: Path,
    manifest: Path,
    probe_source: Path,
    work_dir: Path,
) -> dict[str, object]:
    source = work_dir / "TTUTIL"
    build = work_dir / "build"
    mat = materializer.materialize(swap_zip, source, manifest)
    probe, compiler_version, object_count = build_ttutil_and_probe(
        swap_zip, source, build, probe_source
    )
    cases = _read_cases(testbank_zip)
    details: list[dict[str, object]] = []
    pass_count = 0
    for index, (case, text) in enumerate(cases.items(), start=1):
        legacy = direct.parse_legacy_direct_text(text, case)
        native_text = render_native_direct_v1(legacy)
        direct.validate_native_direct_schema(native_text)
        case_dir = work_dir / f"case-{index:02d}"
        case_dir.mkdir()
        native_file = case_dir / "direct-v1.inp"
        native_file.write_text(native_text, encoding="utf-8")
        cp = _run([str(probe), str(native_file)], cwd=case_dir)
        native = direct.parse_native_probe_output(cp.stdout, case + "#TTUTIL-v1")
        equivalent = direct.semantic_projection(legacy) == direct.semantic_projection(native)
        if equivalent:
            pass_count += 1
        details.append(
            {
                "case": case,
                "field_exact_equivalent": equivalent,
                "legacy_adapter": direct.LEGACY_ADAPTER_ID,
                "native_adapter": direct.NATIVE_ADAPTER_ID,
            }
        )
    result = "PASS" if pass_count == len(details) else "FAIL"
    return {
        "schema": "ANIMO-IO01/DIRECTPilotQualification/v2",
        "result": result,
        "field_exact_equivalence_pass": pass_count,
        "cases": len(details),
        "details": details,
        "source_identity": {
            "swap_4_3_1_sha256": mat["source_package_sha256"],
            "embedded_ttutil_zip_sha256": mat["embedded_archive_sha256"],
            "ttutil_version": mat["ttutil_version"],
            "ttutil_files_verified": mat["files_verified"],
            "ttutil_fortran_objects_built": object_count,
            "animo_testbank_sha256": TESTBANK_SHA256,
        },
        "compiler": compiler_version,
        "qualification_scope": (
            "LegacyInputBinding routing semantics only; no model physics and no GHG schema admission"
        ),
        "legacy_undefined_behavior_exclusion": {
            "revision53_strip_empty_or_whitespace_only_quoted_payload": "FAIL_CLOSED_NOT_NORMALIZED",
            "reason": (
                "Istart can remain 0 while Ilast>0, causing Fname(0:Ilast) "
                "out-of-bounds substring semantics"
            ),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--swap-zip", type=Path, required=True)
    ap.add_argument("--testbank-zip", type=Path, required=True)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "integration" / "animo-io" / "TTUTIL-4.27-SHA256SUMS.txt",
    )
    ap.add_argument(
        "--probe-source",
        type=Path,
        default=TOOLS / "ttutil_direct_probe.f90",
    )
    ap.add_argument("--output", type=Path)
    ap.add_argument("--work-dir", type=Path)
    args = ap.parse_args()
    if args.work_dir is None:
        with tempfile.TemporaryDirectory(prefix="animo-io01-direct-") as tmp:
            result = qualify(
                args.swap_zip,
                args.testbank_zip,
                args.manifest,
                args.probe_source,
                Path(tmp),
            )
    else:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        result = qualify(
            args.swap_zip,
            args.testbank_zip,
            args.manifest,
            args.probe_source,
            args.work_dir,
        )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
