#!/usr/bin/env python3
"""Source-bound C/N/P species-identity audit for frozen ANIMO revision-53.

This audit is intentionally conservative. It reports only strong species identity
signals and separates known intentional stoichiometric conversions, already
confirmed discrepancies, latent/dormant bindings, and unresolved candidates.
It does not infer scientific correctness from naming alone.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
SOURCE_SUFFIXES = {".for", ".f90"}
IDENT = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*\b")
SUBROUTINE = re.compile(r"^\s*subroutine\s+([A-Za-z][A-Za-z0-9_]*)\s*\((.*)\)\s*$", re.I)
CALL = re.compile(r"^\s*call\s+([A-Za-z][A-Za-z0-9_]*)\s*\((.*)\)\s*$", re.I)

SPECIES_PATTERNS: dict[str, tuple[str, ...]] = {
    "P": (
        "transfop", "bapp", "bapo", "bafop", "pofr", "stdiorpo", "diorpo",
        "rekopo", "orgp", "phosph", "rudop",
    ),
    "N": (
        "transfon", "bani", "banh", "bano", "bafon", "nifr", "stdiorni",
        "diorni", "rekoni", "orgn", "nitrat", "ammon", "rudon",
    ),
    "C": (
        "transfom", "bafom", "bfom", "bhum", "bdom", "stdiorma", "diorma",
    ),
}

INTENTIONAL_RULES = (
    ("Grassprd.for", "pofrsh", "INTENTIONAL_STOICHIOMETRIC_P_FROM_N_CONTENT_RATIO"),
    ("Grassprd.for", "pofrro", "INTENTIONAL_STOICHIOMETRIC_P_FROM_N_CONTENT_RATIO"),
    ("Uptpar_Grass.for", "orgpsh", "INTENTIONAL_STOICHIOMETRIC_P_FROM_N_CONTENT_RATIO"),
    ("Uptpar_Grass.for", "orgpro", "INTENTIONAL_STOICHIOMETRIC_P_FROM_N_CONTENT_RATIO"),
    ("Inicalc.for", "pofrhu", "INTENTIONAL_STOICHIOMETRIC_P_FROM_N_HUMUS_RATIO"),
    ("Rates.for", "nifrdo", "INTENTIONAL_DON_TO_DOC_RATIO"),
    ("Rates.for", "pofrdo", "INTENTIONAL_DOP_TO_DOC_RATIO"),
    ("ghgasses.for", "grminch4don", "INTENTIONAL_DON_TO_DOC_RATIO_FOR_CH4_DOM_SINK"),
)

CONFIRMED_RULES = (
    ("resp_miner.for", "transfop", "transfon", "TCD-023"),
)

LATENT_RULES = (
    ("Outsel.for", "rudon", "avcostdiorma", "LATENT_DORMANT_STABLE_SURFACE_DON_BINDING"),
    ("Outsel.for", "rudop", "avcostdiorma", "LATENT_DORMANT_STABLE_SURFACE_DOP_BINDING"),
    ("Outselorg.for", "rudon", "avcostdiorma", "LATENT_DORMANT_STABLE_SURFACE_DON_BINDING"),
    ("Outselorg.for", "rudop", "avcostdiorma", "LATENT_DORMANT_STABLE_SURFACE_DOP_BINDING"),
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def species_of(name: str) -> str | None:
    lower = name.lower()
    found = [species for species, pats in SPECIES_PATTERNS.items() if any(p in lower for p in pats)]
    return found[0] if len(found) == 1 else None


def _is_fixed_comment(line: str) -> bool:
    return bool(line) and line[0] in "cC*!"


def logical_statements(text: str) -> list[tuple[int, str]]:
    """Join ampersand continuations and split semicolon statements."""
    result: list[tuple[int, str]] = []
    buf = ""
    start: int | None = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        if _is_fixed_comment(raw):
            continue
        code = raw.split("!", 1)[0].rstrip()
        if not code.strip():
            continue
        trailing = code.endswith("&")
        if trailing:
            code = code[:-1]
        part = code.lstrip()
        if part.startswith("&"):
            part = part[1:].lstrip()
        if not buf:
            start = lineno
            buf = part
        else:
            buf += " " + part
        if trailing:
            continue
        assert start is not None
        for sub in buf.split(";"):
            if sub.strip():
                result.append((start, sub.strip()))
        buf = ""
        start = None
    if buf and start is not None:
        for sub in buf.split(";"):
            if sub.strip():
                result.append((start, sub.strip()))
    return result


def _lhs_identifier(statement: str) -> str | None:
    if "=" not in statement or "==" in statement:
        return None
    lower = statement.lstrip().lower()
    if lower.startswith(("if ", "if(", "do ", "where", "write", "read", "select ")):
        return None
    lhs = statement.split("=", 1)[0]
    match = IDENT.search(lhs)
    return match.group(0) if match else None


def classify_cross_assignment(filename: str, lineno: int, statement: str) -> dict | None:
    lhs_name = _lhs_identifier(statement)
    if not lhs_name:
        return None
    lhs_species = species_of(lhs_name)
    if not lhs_species:
        return None
    rhs = statement.split("=", 1)[1]
    rhs_names = list(dict.fromkeys(IDENT.findall(rhs)))
    foreign = [
        {"name": name, "species": species_of(name)}
        for name in rhs_names
        if species_of(name) and species_of(name) != lhs_species
    ]
    if not foreign:
        return None

    file_key = filename.lower()
    lhs_key = lhs_name.lower()
    classification = "UNRESOLVED_CROSS_SPECIES_CANDIDATE"
    evidence_id = None

    for rule_file, rule_lhs, label in INTENTIONAL_RULES:
        if file_key == rule_file.lower() and lhs_key == rule_lhs.lower():
            classification = label
            break

    for rule_file, rule_lhs, foreign_name, tcd in CONFIRMED_RULES:
        if (
            file_key == rule_file.lower()
            and lhs_key == rule_lhs.lower()
            and any(item["name"].lower() == foreign_name.lower() for item in foreign)
        ):
            classification = "CONFIRMED_EXISTING_DISCREPANCY"
            evidence_id = tcd
            break

    for rule_file, rule_lhs, foreign_name, label in LATENT_RULES:
        if (
            file_key == rule_file.lower()
            and lhs_key == rule_lhs.lower()
            and any(item["name"].lower() == foreign_name.lower() for item in foreign)
        ):
            classification = label
            break

    return {
        "file": filename,
        "line": lineno,
        "lhs": lhs_name,
        "lhs_species": lhs_species,
        "foreign_rhs": foreign,
        "classification": classification,
        "existing_discrepancy": evidence_id,
        "statement": statement,
    }


def _split_args(arg_text: str) -> list[str]:
    args: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in arg_text:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current or arg_text.strip():
        args.append("".join(current).strip())
    return args


def parse_local_subroutines(source: dict[str, str]) -> dict[str, dict]:
    definitions: dict[str, dict] = {}
    for filename, text in source.items():
        for lineno, stmt in logical_statements(text):
            match = SUBROUTINE.match(stmt)
            if not match:
                continue
            definitions[match.group(1).lower()] = {
                "name": match.group(1),
                "file": filename,
                "line": lineno,
                "formals": _split_args(match.group(2)),
            }
    return definitions


def audit_calls(source: dict[str, str], definitions: dict[str, dict]) -> dict:
    calls = 0
    aligned_local_calls = 0
    strong_pairs = 0
    mismatches: list[dict] = []
    for filename, text in source.items():
        for lineno, stmt in logical_statements(text):
            match = CALL.match(stmt)
            if not match:
                continue
            calls += 1
            definition = definitions.get(match.group(1).lower())
            if not definition:
                continue
            actuals = _split_args(match.group(2))
            formals = definition["formals"]
            if len(actuals) != len(formals):
                continue
            aligned_local_calls += 1
            for position, (formal, actual) in enumerate(zip(formals, actuals), 1):
                f_id = IDENT.search(formal)
                a_id = IDENT.search(actual)
                if not (f_id and a_id):
                    continue
                formal_species = species_of(f_id.group(0))
                actual_species = species_of(a_id.group(0))
                if formal_species and actual_species:
                    strong_pairs += 1
                    if formal_species != actual_species:
                        mismatches.append({
                            "caller_file": filename,
                            "caller_line": lineno,
                            "subroutine": definition["name"],
                            "definition_file": definition["file"],
                            "position": position,
                            "formal": formal,
                            "formal_species": formal_species,
                            "actual": actual,
                            "actual_species": actual_species,
                        })
    return {
        "call_statements": calls,
        "local_subroutine_definitions": len(definitions),
        "aligned_local_calls": aligned_local_calls,
        "strong_species_formal_actual_pairs": strong_pairs,
        "strong_species_mismatch_count": len(mismatches),
        "strong_species_mismatches": mismatches,
    }


def load_source_from_zip(zip_path: Path) -> dict[str, str]:
    actual_hash = sha256_file(zip_path)
    if actual_hash != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source ZIP hash mismatch: {actual_hash}")
    source: dict[str, str] = {}
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            name = Path(info.filename).name
            if Path(name).suffix.lower() not in SOURCE_SUFFIXES:
                continue
            source[name] = zf.read(info).decode("latin1")
    if not source:
        raise ValueError("no Fortran source members found")
    return source


def audit_source(source: dict[str, str]) -> dict:
    assignments: list[dict] = []
    assignment_statement_count = 0
    for filename in sorted(source):
        for lineno, stmt in logical_statements(source[filename]):
            if _lhs_identifier(stmt):
                assignment_statement_count += 1
            finding = classify_cross_assignment(filename, lineno, stmt)
            if finding:
                assignments.append(finding)

    definitions = parse_local_subroutines(source)
    call_audit = audit_calls(source, definitions)
    by_class: dict[str, int] = {}
    for item in assignments:
        by_class[item["classification"]] = by_class.get(item["classification"], 0) + 1

    unresolved = [x for x in assignments if x["classification"] == "UNRESOLVED_CROSS_SPECIES_CANDIDATE"]
    confirmed = [x for x in assignments if x["classification"] == "CONFIRMED_EXISTING_DISCREPANCY"]
    latent = [x for x in assignments if x["classification"].startswith("LATENT_DORMANT")]
    intentional = [x for x in assignments if x["classification"].startswith("INTENTIONAL_")]

    return {
        "evidence_class": "SOURCE_BOUND_HEURISTIC_AUDIT_NOT_SCIENTIFIC_REFERENCE",
        "source_sha256_required": EXPECTED_SOURCE_SHA256,
        "fortran_source_members": len(source),
        "assignment_statements_scanned": assignment_statement_count,
        "cross_species_assignment_findings": len(assignments),
        "assignment_class_counts": dict(sorted(by_class.items())),
        "confirmed_existing_discrepancies": confirmed,
        "intentional_stoichiometric_or_ratio_bindings": intentional,
        "latent_dormant_bindings": latent,
        "unresolved_cross_species_candidates": unresolved,
        "call_interface_audit": call_audit,
        "decision": (
            "UNRESOLVED_CANDIDATES_REQUIRE_REVIEW"
            if unresolved or call_audit["strong_species_mismatch_count"]
            else "NO_NEW_ACTIVE_DIRECT_CROSS_SPECIES_DEFECT_FROM_STRONG_IDENTITY_SCAN"
        ),
        "production_migration_admitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = audit_source(load_source_from_zip(args.source_zip))
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 2 if report["decision"] == "UNRESOLVED_CANDIDATES_REQUIRE_REVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
