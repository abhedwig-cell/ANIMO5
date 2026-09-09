#!/usr/bin/env python3
"""Source-bound PREP09 audit for element-transfer sequencing and slow P tillage seams.

This tool only reads the supplied frozen ANIMO source and testbank ZIPs. It does
not run or alter the model and therefore does not turn diagnostic evidence into
reference evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_member(archive: zipfile.ZipFile, suffix: str) -> str:
    matches = [name for name in archive.namelist() if name.lower().endswith(suffix.lower())]
    if len(matches) != 1:
        raise SystemExit(f"expected one member ending {suffix!r}, found {matches}")
    return archive.read(matches[0]).decode("latin1")


def check(name: str, condition: bool, detail: str, checks: list[dict]) -> None:
    checks.append({"check": name, "pass": bool(condition), "detail": detail})
    if not condition:
        raise SystemExit(f"FAIL {name}: {detail}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("testbank_zip", type=Path)
    args = parser.parse_args()
    checks: list[dict] = []

    source_hash = sha256(args.source_zip)
    testbank_hash = sha256(args.testbank_zip)
    check("source_sha256", source_hash == SOURCE_SHA, source_hash, checks)
    check("testbank_sha256", testbank_hash == TESTBANK_SHA, testbank_hash, checks)

    with zipfile.ZipFile(args.source_zip) as archive:
        addit = read_member(archive, "/Addit.for")
        outbal = read_member(archive, "/Outbal_calc.for")
        init = read_member(archive, "/Init.for")

    old_n = "Adhuexnipl(I,Ln) = Adhuexnipl(I,Ln) - Huex(Ln)*Nifrhu(Ln)"
    old_p = "Adhuexpopl(I,Ln) = Adhuexpopl(I,Ln) - Huex(Ln)*Pofrhu(Ln)"
    new_n = "Adhuexnipl(I,Ln) = Adhuexnipl(I,Ln) + huex(Ln)*Nifrhu(Ln)"
    new_p = "Adhuexpopl(I,Ln) = Adhuexpopl(I,Ln) + huex(Ln)*Pofrhu(Ln)"
    rec_n = "Nifrhu(Ln) = Huosni(ln) / Huos(Ln)"
    rec_p = "if(Ipo==1) Pofrhu(Ln) = Huospo(ln) / Huos(Ln)"

    for name, source in [
        ("old_n", old_n),
        ("old_p", old_p),
        ("new_n", new_n),
        ("new_p", new_p),
        ("recalc_n", rec_n),
        ("recalc_p", rec_p),
    ]:
        check(f"tcd030_{name}_present", source in addit, source, checks)

    check(
        "tcd030_n_add_precedes_fraction_recalc",
        addit.index(new_n) < addit.index(rec_n),
        f"{addit.index(new_n)} < {addit.index(rec_n)}",
        checks,
    )
    check(
        "tcd030_p_add_precedes_fraction_recalc",
        addit.index(new_p) < addit.index(rec_p),
        f"{addit.index(new_p)} < {addit.index(rec_p)}",
        checks,
    )

    slow_patterns = [
        "!-19-10-2010                     Supocxsl(J) = Supocxsl(J) + Amcxsl(J,Ln)*He(Ln)",
        "!-19-10-2010                     Adpocxslpl(I,Ln,J) = Adpocxslpl(I,Ln,J) -",
        "!-19-10-2010                     Amcxsl(J,Ln) = Supocxsl(J) / Bo(Pl(I))",
        "!-19-10-2010                     Adpocxslpl(I,Ln,J) = Adpocxslpl(I,Ln,J) +",
    ]
    for number, source in enumerate(slow_patterns, 1):
        check(f"slow_plough_block_{number}_commented", source in addit, source, checks)

    check(
        "slow_commented_site_loop_starts_at_management_index",
        "!-19-10-2010                  Do J = I,Ncxsl" in addit,
        "Do J = I,Ncxsl",
        checks,
    )
    check(
        "slow_ledger_consumer_active",
        "Adpocxslpl(I,Ln,J)*Z" in outbal,
        "Outbal_calc consumes Adpocxslpl",
        checks,
    )
    check(
        "slow_ledger_reset_active",
        "Adpocxslpl(I,Ln,J) = 0.0" in init,
        "Init resets Adpocxslpl",
        checks,
    )

    with zipfile.ZipFile(args.testbank_zip) as archive:
        chem = read_member(archive, "/LWKM_gras_1040.2021.2045/input/CHEMPAR.INP")
        management = read_member(archive, "/LWKM_gras_1040.2021.2045/input/Management.inp")

    optcxsl = re.search(r"(?im)^\s*([0-9]+)\s*!\s*optcxsl\s*:", chem)
    ncxsl = re.search(r"(?im)^\s*([0-9]+)\s*!\s*ncxsl\s*:", chem)
    check(
        "lwkm_optcxsl_3",
        bool(optcxsl and int(optcxsl.group(1)) == 3),
        optcxsl.group(0) if optcxsl else "missing",
        checks,
    )
    check(
        "lwkm_ncxsl_3",
        bool(ncxsl and int(ncxsl.group(1)) == 3),
        ncxsl.group(0) if ncxsl else "missing",
        checks,
    )
    check(
        "lwkm_management_present",
        ">lmanag:" in management and ">matvar:" in management,
        "management sections present",
        checks,
    )

    result = {
        "work_unit": "ANIMO-PREP09",
        "evidence_class": "SOURCE_BOUND_STATIC_AUDIT",
        "source_sha256": SOURCE_SHA,
        "testbank_sha256": TESTBANK_SHA,
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "reference_qualified": False,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
