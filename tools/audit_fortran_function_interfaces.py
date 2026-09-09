#!/usr/bin/env python3
"""Source-bound static audit of legacy Fortran external function result declarations.

This is qualification tooling, not a Fortran compiler/parser. It reports only explicit
textual evidence and labels possible calls conservatively. The input source archive is
verified by SHA-256 before analysis.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
SOURCE_SUFFIXES = {".for", ".f90", ".inc"}

FUNCTION_DEF = re.compile(
    r"^\s*(?:(real(?:\s*\([^)]*\)|\s*\*\s*\d+)?|"
    r"integer(?:\s*\([^)]*\)|\s*\*\s*\d+)?|logical|"
    r"character(?:\s*\([^)]*\)|\s*\*\s*\d+)?)\s+)?"
    r"function\s+([a-z_]\w*)\s*\(",
    re.IGNORECASE,
)
TYPE_DECL = re.compile(
    r"^\s*(real(?:\s*\([^)]*\)|\s*\*\s*\d+)?|"
    r"integer(?:\s*\([^)]*\)|\s*\*\s*\d+)?|logical|"
    r"character(?:\s*\([^)]*\)|\s*\*\s*\d+)?)"
    r"(?:\s*::)?\s*(.*)$",
    re.IGNORECASE,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_type(value: str) -> str:
    return re.sub(r"\s+", "", value.lower())


def split_decl_names(text: str) -> list[str]:
    text = text.split("!", 1)[0]
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current).strip())
    names: list[str] = []
    for item in parts:
        m = re.match(r"([a-z_]\w*)", item, re.IGNORECASE)
        if m:
            names.append(m.group(1).lower())
    return names


def source_files(root: Path) -> list[Path]:
    return sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SOURCE_SUFFIXES
    )


def find_result_type(lines: list[str], start: int, name: str, prefix_type: str | None) -> str:
    if prefix_type:
        return normalize_type(prefix_type)
    for line in lines[start + 1 : min(len(lines), start + 180)]:
        if re.match(r"^\s*end\b", line, re.IGNORECASE):
            break
        m = TYPE_DECL.match(line)
        if m and name in split_decl_names(m.group(2)):
            return normalize_type(m.group(1))
    return "unknown"


def is_comment(line: str) -> bool:
    s = line.lstrip()
    return not s or s.startswith("!") or (line and line[0] in "cC*")


def analyze(root: Path) -> dict:
    files = source_files(root)
    definitions: dict[str, dict] = {}
    contents: dict[Path, list[str]] = {}

    for path in files:
        lines = path.read_text("latin-1", errors="replace").splitlines()
        contents[path] = lines
        for i, line in enumerate(lines):
            if is_comment(line):
                continue
            m = FUNCTION_DEF.match(line)
            if not m:
                continue
            name = m.group(2).lower()
            definitions[name] = {
                "function": name,
                "definition_file": path.name,
                "definition_line": i + 1,
                "definition_result_type": find_result_type(lines, i, name, m.group(1)),
            }

    declarations: dict[str, list[dict]] = defaultdict(list)
    possible_calls: dict[str, list[dict]] = defaultdict(list)

    for path, lines in contents.items():
        for i, line in enumerate(lines, start=1):
            if is_comment(line):
                continue
            decl = TYPE_DECL.match(line)
            if decl:
                dtype = normalize_type(decl.group(1))
                for name in split_decl_names(decl.group(2)):
                    if name in definitions:
                        declarations[name].append(
                            {"file": path.name, "line": i, "type": dtype, "text": line.strip()}
                        )
            low = line.lower()
            for name in definitions:
                if re.search(rf"\b{name}\s*\(", low):
                    if FUNCTION_DEF.match(line):
                        continue
                    possible_calls[name].append({"file": path.name, "line": i, "text": line.strip()})

    rows = []
    for name in sorted(definitions):
        d = definitions[name]
        decls = declarations.get(name, [])
        observed_types = sorted({x["type"] for x in decls})
        result_type = d["definition_result_type"]
        differing = sorted(t for t in observed_types if t != result_type)
        rows.append(
            {
                **d,
                "observed_declaration_types": observed_types,
                "differing_declaration_types": differing,
                "declaration_count": len(decls),
                "possible_call_count": len(possible_calls.get(name, [])),
                "classification": (
                    "MIXED_EXPLICIT_RESULT_DECLARATION"
                    if differing
                    else "EXPLICIT_DECLARATIONS_CONSISTENT_WITH_DEFINITION"
                ),
                "declarations": decls,
                "possible_calls": possible_calls.get(name, []),
            }
        )

    return {
        "evidence_class": "STATIC_SOURCE_TEXT_AUDIT_NOT_FULL_FORTRAN_SEMANTIC_PARSE",
        "source_file_count_scanned": len(files),
        "function_definition_count": len(rows),
        "mixed_result_declaration_functions": [
            r["function"] for r in rows if r["classification"] == "MIXED_EXPLICIT_RESULT_DECLARATION"
        ],
        "functions": rows,
    }


def write_csv(path: Path, result: dict) -> None:
    fields = [
        "function",
        "definition_file",
        "definition_line",
        "definition_result_type",
        "observed_declaration_types",
        "differing_declaration_types",
        "declaration_count",
        "possible_call_count",
        "classification",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in result["functions"]:
            out = {k: row[k] for k in fields}
            out["observed_declaration_types"] = ";".join(row["observed_declaration_types"])
            out["differing_declaration_types"] = ";".join(row["differing_declaration_types"])
            w.writerow(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archive", type=Path)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--allow-unpinned-source", action="store_true")
    args = ap.parse_args()

    digest = sha256_file(args.archive)
    if digest != EXPECTED_SOURCE_SHA256 and not args.allow_unpinned_source:
        raise SystemExit(
            f"source SHA-256 mismatch: expected {EXPECTED_SOURCE_SHA256}, got {digest}"
        )

    with tempfile.TemporaryDirectory(prefix="animo_function_audit_") as td:
        with zipfile.ZipFile(args.archive) as zf:
            zf.extractall(td)
        result = analyze(Path(td))
    result["source_archive"] = args.archive.name
    result["source_sha256"] = digest

    text = json.dumps(result, indent=2) + "\n"
    if args.json:
        args.json.write_text(text, encoding="utf-8")
    if args.csv:
        write_csv(args.csv, result)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
