#!/usr/bin/env python3
"""Materialize the exact TTUTIL 4.27 source from a user-supplied SWAP 4.3.1 ZIP.

No network access, registration, or license acceptance is performed by this tool.
It fails closed on outer package identity, embedded TTUTIL archive identity, file
set, and per-file SHA-256 values recorded by ANIMO-IO01.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

SWAP431_SHA256 = "2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360"
EMBEDDED_PATH = "SWAP_4.3.1/tools/SWAP/source/TTUTIL.ZIP"
TTUTIL427_ZIP_SHA256 = "ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193"
EXPECTED_VERSION = "4.27"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_manifest(path: Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            digest, name = raw.split(None, 1)
        except ValueError as exc:
            raise ValueError(f"malformed manifest line {lineno}: {raw!r}") from exc
        name = name.strip()
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError(f"invalid SHA-256 at manifest line {lineno}")
        if name in expected:
            raise ValueError(f"duplicate manifest path {name!r}")
        expected[name] = digest
    if not expected:
        raise ValueError("empty TTUTIL manifest")
    return expected


def safe_member_name(name: str) -> str:
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or len(p.parts) != 2 or p.parts[0] != "TTUTIL":
        raise ValueError(f"unsafe or unexpected TTUTIL member path {name!r}")
    return p.name


def materialize(swap_zip: Path, target: Path, manifest: Path, force: bool = False) -> dict[str, object]:
    outer_sha = sha256_file(swap_zip)
    if outer_sha != SWAP431_SHA256:
        raise ValueError(f"SWAP package SHA-256 mismatch: {outer_sha}")

    with zipfile.ZipFile(swap_zip, "r") as outer:
        try:
            ttutil_zip = outer.read(EMBEDDED_PATH)
        except KeyError as exc:
            raise ValueError(f"missing embedded {EMBEDDED_PATH}") from exc

    inner_sha = sha256_bytes(ttutil_zip)
    if inner_sha != TTUTIL427_ZIP_SHA256:
        raise ValueError(f"embedded TTUTIL.ZIP SHA-256 mismatch: {inner_sha}")

    expected = read_manifest(manifest)
    with zipfile.ZipFile(io.BytesIO(ttutil_zip), "r") as inner:
        files = [zi for zi in inner.infolist() if not zi.is_dir()]
        names = [safe_member_name(zi.filename) for zi in files]
        if len(names) != len(set(names)):
            raise ValueError("duplicate file name in embedded TTUTIL.ZIP")
        actual_set = set(names)
        expected_set = set(expected)
        if actual_set != expected_set:
            missing = sorted(expected_set - actual_set)
            extra = sorted(actual_set - expected_set)
            raise ValueError(f"TTUTIL file-set mismatch: missing={missing}, extra={extra}")
        verified: dict[str, bytes] = {}
        for zi in files:
            bare = safe_member_name(zi.filename)
            data = inner.read(zi)
            digest = sha256_bytes(data)
            if digest != expected[bare]:
                raise ValueError(f"TTUTIL member SHA-256 mismatch for {bare}: {digest}")
            verified[bare] = data

    ttuver = verified.get("ttuver.for", b"").decode("latin-1")
    if "CUR_V=4.27" not in ttuver.replace(" ", ""):
        raise ValueError("ttuver.for does not declare CUR_V=4.27")

    if target.exists():
        if not force:
            raise FileExistsError(f"target already exists: {target}")
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ttutil427-", dir=target.parent) as tmp:
        stage = Path(tmp) / "TTUTIL"
        stage.mkdir()
        for name, data in verified.items():
            (stage / name).write_bytes(data)
        shutil.move(str(stage), str(target))

    suffixes: dict[str, int] = {}
    for name in expected:
        suffix = Path(name).suffix.lower() or "<none>"
        suffixes[suffix] = suffixes.get(suffix, 0) + 1
    fortran_units = suffixes.get(".for", 0) + suffixes.get(".f90", 0)

    return {
        "schema": "ANIMO-IO01/TTUTILMaterialization/v1",
        "source_package": str(swap_zip),
        "source_package_sha256": outer_sha,
        "embedded_archive_path": EMBEDDED_PATH,
        "embedded_archive_sha256": inner_sha,
        "ttutil_version": EXPECTED_VERSION,
        "target": str(target),
        "files_verified": len(expected),
        "fortran_compilation_units": fortran_units,
        "suffix_counts": dict(sorted(suffixes.items())),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("swap_zip", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path("integration/animo-io/TTUTIL-4.27-SHA256SUMS.txt"),
    )
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    result = materialize(args.swap_zip, args.target, args.manifest, args.force)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
