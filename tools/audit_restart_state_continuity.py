#!/usr/bin/env python3
"""Audit restart/state-continuity contracts in frozen ANIMO revision-53 source.

Evidence tooling only. The frozen source archive is read-only and hash-pinned.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sources(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.lower().endswith(".for"):
                result[Path(name).name.lower()] = archive.read(name).decode("latin1")
    return result


def active_lines(text: str) -> list[str]:
    result: list[str] = []
    for raw in text.splitlines():
        stripped = raw.lstrip()
        if not stripped or stripped.startswith("!"):
            continue
        code = raw.split("!", 1)[0].strip()
        if code:
            result.append(re.sub(r"\s+", " ", code))
    return result


def active_has(text: str, pattern: str) -> bool:
    return any(re.search(pattern, line, re.IGNORECASE) for line in active_lines(text))


def audit(source_zip: Path) -> dict:
    if sha256(source_zip) != SOURCE_SHA256:
        raise ValueError("source archive SHA-256 mismatch")

    source = sources(source_zip)
    input1 = source["input1.for"]
    output_init = source["output_init.for"]
    init = source["init.for"]
    inicalc = source["inicalc.for"]
    mapoinput = source["mapoinput.for"]
    uptpar_plant = source["uptpar_plant.for"]

    checks = {
        "input_reads_orgpla_actual_n": active_has(
            input1,
            r"Read\s*\([^)]*\)\s*Rsamplro\s*,\s*Rsamplsh\s*,\s*Rsamplni_act",
        ),
        "output_writes_orgpla_actual_n": active_has(
            output_init,
            r"Write\s*\([^)]*\).*Rsamplro\s*,\s*Rsamplsh\s*,\s*Rsamplni_act",
        ),
        "input_has_no_potential_plant_restart_field": not active_has(
            input1, r"Rsamplni_pot|Rsamplpo_pot|Amplni_pot|Amplpo_pot"
        ),
        "output_has_no_potential_plant_restart_field": not active_has(
            output_init, r"Rsamplni_pot|Rsamplpo_pot|Amplni_pot|Amplpo_pot"
        ),
        "init_carries_potential_n": active_has(
            init, r"Amplni_pot\s*=\s*Rsamplni_pot"
        ),
        "init_carries_potential_p": active_has(
            init, r"Amplpo_pot\s*=\s*Rsamplpo_pot"
        ),
        "uptake_future_logic_uses_potential_minus_actual": active_has(
            uptpar_plant, r"Demnide\s*=\s*Amplni_pot\s*-\s*Amplni_act"
        ),
        "inicalc_resets_potential_n": active_has(
            inicalc, r"Amplni_pot\s*=\s*0\.0"
        ),
        "inicalc_resets_potential_p": active_has(
            inicalc, r"Amplpo_pot\s*=\s*0\.0"
        ),
        "macropore_restart_reader_active": re.search(
            r"Mapoinput[\s&]*\(\s*4\s*,", input1, re.IGNORECASE
        ) is not None,
        "mapoinput_reads_mpnitr": active_has(
            mapoinput,
            r"Read\s*\([^)]*\)\s*CoMpnh\(1\)\s*,\s*CoMpnh\(2\)\s*,\s*CoMpni\(1\)\s*,\s*CoMpni\(2\)",
        ),
        "mapoinput_reads_mporgs": active_has(
            mapoinput,
            r"Read\s*\([^)]*\)\s*CoMpDiorma\(1\)\s*,\s*CoMpDiorma\(2\)",
        ),
        "mapoinput_reads_mpphos": active_has(
            mapoinput,
            r"Read\s*\([^)]*\)\s*CoMpPo\(1\)\s*,\s*CoMpPo\(2\)",
        ),
        "init_commits_macropore_nitrate": active_has(
            init, r"CoMpNi\(Dn\)\s*=\s*RsCoMpNi\(Dn\)"
        ),
        "init_commits_macropore_organics": active_has(
            init, r"CoMpDiorMa\(Dn\)\s*=\s*RsCoMpDiorMa\(Dn\)"
        ),
        "init_commits_macropore_p": active_has(
            init, r"CoMpPo\(Dn\)\s*=\s*RsCoMpPo\(Dn\)"
        ),
        "output_has_no_active_mpnitr_writer": not active_has(
            output_init, r"Label\s*=\s*'>mpnitr:'"
        ),
        "output_has_no_active_mporgs_writer": not active_has(
            output_init, r"Label\s*=\s*'>mporgs:'"
        ),
        "output_has_no_active_mpphos_writer": not active_has(
            output_init, r"Label\s*=\s*'>mpphos:'"
        ),
        "output_source_contains_commented_mpnitr_marker": re.search(
            r"(?im)^\s*!\s*.*'>mpnitr:'", output_init
        ) is not None,
        "output_source_contains_commented_mporgs_marker": re.search(
            r"(?im)^\s*!\s*.*'>mporgs:'", output_init
        ) is not None,
        "output_source_contains_commented_mpphos_marker": re.search(
            r"(?im)^\s*!\s*.*'>mpphos:'", output_init
        ) is not None,
        "mapoinput_nitrate_check_uses_wrong_ammonium_value_1": active_has(
            mapoinput,
            r"Checkrea\([^)]*'CoMpni\(1\)'\s*,\s*CoMpnh\(1\)",
        ),
        "mapoinput_nitrate_check_uses_wrong_ammonium_value_2": active_has(
            mapoinput,
            r"Checkrea\([^)]*'CoMpni\(2\)'\s*,\s*CoMpnh\(2\)",
        ),
        "output_canonicalizes_p_restart_to_inpo1": active_has(
            output_init, r"Inpo\s*=\s*1"
        ),
    }

    return {
        "evidence_class": "SOURCE_BOUND_RESTART_STATE_AUDIT_NOT_REFERENCE",
        "source_sha256": SOURCE_SHA256,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_checks_pass": all(checks.values()),
        "findings": {
            "macropore_restart_writer": (
                "SOURCE_CONFIRMED_PERSISTENT_STATE_WRITER_OMISSION_"
                "TESTBANK_UNEXERCISED"
            ),
            "macropore_nitrate_validation": (
                "SOURCE_CONFIRMED_WRONG_VARIABLE_VALIDATED_UNEXERCISED"
            ),
            "plant_potential_restart": (
                "CANDIDATE_INFORMATION_LOSS_CAUSAL_PROBE_REQUIRED"
            ),
            "p_restart_mode": "CANONICALIZED_TO_INPO1_SPLIT_RUN_CHECK_REQUIRED",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence = audit(args.source_zip)
    encoded = json.dumps(evidence, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if evidence["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
