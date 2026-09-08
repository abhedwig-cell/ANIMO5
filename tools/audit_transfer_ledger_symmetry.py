#!/usr/bin/env python3
"""Source-bound transfer-ledger symmetry audit for frozen ANIMO revision-53.

Qualification/audit tooling only. The tool never edits the source archive and
never promotes a syntactic asymmetry to a scientific defect by itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = (
    "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
)

ASSIGNMENT = re.compile(
    r"\b(?P<family>Bafom|Bafon|Bafop)\s*\(\s*(?P<lhs>\d+)\s*,[^=]*\)\s*=\s*(?P<rhs>.*)",
    re.IGNORECASE,
)
SAME_FAMILY_REF = re.compile(
    r"\b(?P<family>Bafom|Bafon|Bafop)\s*\(\s*(?P<slot>\d+)\s*,",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def uncommented_fortran_statements(text: str) -> list[tuple[int, str]]:
    """Return approximate logical statements while preserving first line number.

    The supplied source is free-form-style legacy Fortran. This helper is not a
    complete parser; it only joins ampersand continuations needed by the ledger
    expressions audited here and removes full-line/comment tails.
    """
    statements: list[tuple[int, str]] = []
    current = ""
    first_line = 0
    continuing = False

    for line_number, raw in enumerate(text.splitlines(), 1):
        stripped = raw.lstrip()
        if not stripped or stripped.startswith("!"):
            continue
        code = raw.split("!", 1)[0].strip()
        if not code:
            continue

        begins_continuation = code.startswith("&")
        if begins_continuation:
            code = code[1:].lstrip()

        ends_continuation = code.endswith("&")
        if ends_continuation:
            code = code[:-1].rstrip()

        if current and (continuing or begins_continuation):
            current += " " + code
        else:
            if current:
                statements.append((first_line, current))
            current = code
            first_line = line_number

        continuing = ends_continuation
        if not continuing:
            statements.append((first_line, current))
            current = ""
            first_line = 0

    if current:
        statements.append((first_line, current))
    return statements


def detailed_accumulator_audit(text: str) -> dict:
    assignments: list[dict] = []
    cross_slot_self_references: list[dict] = []
    slots_by_family: dict[str, set[int]] = {"bafom": set(), "bafon": set(), "bafop": set()}

    for line_number, statement in uncommented_fortran_statements(text):
        match = ASSIGNMENT.search(statement)
        if not match:
            continue
        family = match.group("family").lower()
        lhs = int(match.group("lhs"))
        rhs = match.group("rhs")
        slots_by_family[family].add(lhs)

        refs = [
            int(ref.group("slot"))
            for ref in SAME_FAMILY_REF.finditer(rhs)
            if ref.group("family").lower() == family
        ]
        row = {
            "line": line_number,
            "family": family,
            "lhs_slot": lhs,
            "same_family_rhs_slots": refs,
            "statement": " ".join(statement.split()),
        }
        assignments.append(row)
        wrong = sorted({slot for slot in refs if slot != lhs})
        if wrong:
            row = dict(row)
            row["cross_slot_rhs_slots"] = wrong
            cross_slot_self_references.append(row)

    normalized_slots = {name: sorted(values) for name, values in slots_by_family.items()}
    union = sorted(set().union(*slots_by_family.values()))
    slot_coverage = {
        name: {
            "slots": normalized_slots[name],
            "missing_from_union": sorted(set(union) - values),
        }
        for name, values in slots_by_family.items()
    }
    return {
        "assignment_count": len(assignments),
        "slot_union": union,
        "slot_coverage": slot_coverage,
        "cross_slot_self_reference_count": len(cross_slot_self_references),
        "cross_slot_self_references": cross_slot_self_references,
    }


def _contains(text: str, fragments: list[str]) -> bool:
    normalized = " ".join(text.replace("&", " ").lower().split())
    return all(fragment.lower() in normalized for fragment in fragments)


def initial_final_state_audit(outbal_init: str, outbal_calc: str) -> dict:
    checks = {
        "fresh_om_initial_exudate": {
            "initial_has_ex": _contains(outbal_init, ["bfom(inip_x", "ex(ln)"]),
            "final_has_rsex": _contains(outbal_calc, ["bfom(finp_x", "rsex(ln)"]),
        },
        "organic_n_initial_exudate": {
            "initial_has_ex_n": _contains(outbal_init, ["bano(inip_x", "ex(ln)*nifrex"]),
        },
        "organic_p_initial_exudate": {
            "initial_has_ex_p": _contains(outbal_init, ["bapo(inip_x", "ex(ln)*pofrex"]),
        },
    }
    checks["fresh_om_initial_exudate"]["asymmetric"] = (
        checks["fresh_om_initial_exudate"]["final_has_rsex"]
        and not checks["fresh_om_initial_exudate"]["initial_has_ex"]
    )
    return checks


def stable_surface_reachability_audit(input1: str, resp_miner: str, init: str) -> dict:
    return {
        "parser_exposes_layer_zero_stable_dom": _contains(
            input1, ["costdiorma(ln)", "costdiorni(ln)"]
        ),
        "resp_miner_explicitly_skips_layer_zero": _contains(
            resp_miner, ["if(ln.eq.0)goto 1000"]
        ) or _contains(resp_miner, ["if(ln .eq. 0) goto 1000"]),
        "init_zeroes_result_stable_dom": _contains(
            init, ["rscostdiorma(ln)", "0.0"]
        ),
        "interpretation": "source signals only; reachability classification remains a reviewed evidence decision",
    }


def audit_archive(source_zip: Path) -> dict:
    actual_sha = sha256(source_zip)
    if actual_sha != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source SHA-256 mismatch: {actual_sha}")

    with zipfile.ZipFile(source_zip) as archive:
        members = {
            Path(name).name.lower(): name
            for name in archive.namelist()
            if not name.endswith("/")
        }

        def read(name: str) -> str:
            key = name.lower()
            if key not in members:
                raise ValueError(f"missing frozen source member: {name}")
            return archive.read(members[key]).decode("latin1")

        outbal_calc = read("Outbal_calc.for")
        result = {
            "evidence_class": "SOURCE_BOUND_TRANSFER_LEDGER_AUDIT_NOT_DEFECT_ADMISSION",
            "source_sha256": actual_sha,
            "detailed_accumulators": detailed_accumulator_audit(outbal_calc),
            "initial_final_state": initial_final_state_audit(
                read("Outbal_Init.for"), outbal_calc
            ),
            "stable_surface_reachability": stable_surface_reachability_audit(
                read("input1.for"), read("Resp_miner.for"), read("Init.for")
            ),
            "automatic_defect_admission": False,
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    try:
        result = audit_archive(args.source_zip)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise SystemExit(str(exc)) from exc

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
