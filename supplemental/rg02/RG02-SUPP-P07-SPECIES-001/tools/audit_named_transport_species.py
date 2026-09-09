#!/usr/bin/env python3
"""Check generic transport calls against their explicit substance label.

Uses the strong variable-species classifier from audit_species_identity.py, but
infers the expected species from literal substance names passed to Transport,
Transsub and Transgen. Calls using a runtime variable as substance label are
left unclassified rather than guessed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

BASE_TOOL = Path(__file__).with_name("audit_species_identity.py")
spec = importlib.util.spec_from_file_location("audit_species_identity", BASE_TOOL)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)


def expected_species(argument: str) -> str | None:
    label = argument.strip().strip("\"'").lower()
    if "org.mat" in label:
        return "C"
    if any(token in label for token in ("org.nit", "ammon", "nitrat")):
        return "N"
    if any(token in label for token in ("org.pho", "phosph")):
        return "P"
    return None


def audit_source(source: dict[str, str]) -> dict:
    audited_calls = 0
    strong_actuals = 0
    mismatches: list[dict] = []
    for filename, text in source.items():
        for line_no, statement in base.logical_statements(text):
            match = base.CALL.match(statement)
            if not match or match.group(1).lower() not in {"transport", "transsub", "transgen"}:
                continue
            actuals = base._split_args(match.group(2))
            if not actuals:
                continue
            target = expected_species(actuals[0])
            if not target:
                continue
            audited_calls += 1
            for position, actual in enumerate(actuals, 1):
                identifier = base.IDENT.search(actual)
                if not identifier:
                    continue
                actual_species = base.species_of(identifier.group(0))
                if not actual_species:
                    continue
                strong_actuals += 1
                if actual_species != target:
                    mismatches.append({
                        "caller_file": filename,
                        "caller_line": line_no,
                        "routine": match.group(1),
                        "substance_argument": actuals[0],
                        "expected_species": target,
                        "position": position,
                        "actual": actual,
                        "actual_species": actual_species,
                    })
    return {
        "evidence_class": "SOURCE_BOUND_NAMED_GENERIC_TRANSPORT_BINDING_AUDIT_NOT_REFERENCE",
        "source_sha256_required": base.EXPECTED_SOURCE_SHA256,
        "named_transport_calls_audited": audited_calls,
        "strong_species_actuals_checked": strong_actuals,
        "species_mismatch_count": len(mismatches),
        "species_mismatches": mismatches,
        "decision": (
            "NAMED_TRANSPORT_SPECIES_MISMATCH_REQUIRES_REVIEW"
            if mismatches
            else "NO_STRONG_SPECIES_MISMATCH_IN_NAMED_GENERIC_TRANSPORT_CALLS"
        ),
        "production_migration_admitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = audit_source(base.load_source_from_zip(args.source_zip))
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 2 if report["species_mismatch_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
