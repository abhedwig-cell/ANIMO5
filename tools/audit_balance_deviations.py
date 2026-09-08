#!/usr/bin/env python3
"""Measure legacy balance-residual envelopes from ANIMO balance output files.

The result is diagnostic evidence only. This tool deliberately does not define or
apply an acceptance tolerance.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

SPECS = {
    "water": {"glob": "bawa*.Out", "period": -2, "cumulative": -1, "units": "mm"},
    "fresh_organic_matter": {"glob": "baom*.Out", "period": -6, "cumulative": -5, "units": "kg/ha organic matter"},
    "humus": {"glob": "baom*.Out", "period": -4, "cumulative": -3, "units": "kg/ha organic matter"},
    "dissolved_organic_matter": {"glob": "baom*.Out", "period": -2, "cumulative": -1, "units": "kg/ha organic matter"},
    "nh4_n": {"glob": "banh*.Out", "period": -2, "cumulative": -1, "units": "kg/ha N"},
    "no3_n": {"glob": "bani*.Out", "period": -2, "cumulative": -1, "units": "kg/ha N"},
    "organic_n": {"glob": "bano*.Out", "period": -2, "cumulative": -1, "units": "kg/ha N"},
    "po4_p": {"glob": "bapp*.Out", "period": -2, "cumulative": -1, "units": "kg/ha P"},
    "organic_p": {"glob": "bapo*.Out", "period": -2, "cumulative": -1, "units": "kg/ha P"},
}

RECORD1 = re.compile(r"^\s*1\s+\d{4}\s+")


def parse_file(path: Path, period_index: int, cumulative_index: int) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if not RECORD1.match(line):
            continue
        try:
            values = [float(token) for token in line.split()]
        except ValueError:
            continue
        need = max(abs(period_index), abs(cumulative_index))
        if len(values) < need:
            continue
        records.append(
            {
                "line": line_number,
                "year": int(values[1]),
                "tito": int(values[2]),
                "tiyr": int(values[3]),
                "period_deviation": values[period_index],
                "cumulative_deviation": values[cumulative_index],
            }
        )
    return records


def audit(root: Path, cases: list[str] | None = None) -> dict:
    if cases is None:
        cases = sorted(path.name for path in root.iterdir() if path.is_dir())

    result = {
        "evidence_class": "DIAGNOSTIC_OUTPUT_RESIDUAL_ENVELOPE_NOT_ACCEPTANCE_THRESHOLD",
        "root": str(root),
        "cases": cases,
        "balances": {},
    }

    for name, spec in SPECS.items():
        records = []
        file_count = 0
        for case in cases:
            case_dir = root / case
            for path in sorted(case_dir.glob(spec["glob"])):
                file_count += 1
                for record in parse_file(path, spec["period"], spec["cumulative"]):
                    record.update({"case": case, "file": path.name})
                    records.append(record)

        entry = {
            "units": spec["units"],
            "file_count": file_count,
            "record_count": len(records),
        }
        if records:
            max_period = max(records, key=lambda row: abs(row["period_deviation"]))
            max_cumulative = max(records, key=lambda row: abs(row["cumulative_deviation"]))
            entry.update(
                {
                    "nonfinite_record_count": sum(
                        not math.isfinite(row["period_deviation"])
                        or not math.isfinite(row["cumulative_deviation"])
                        for row in records
                    ),
                    "max_abs_period_deviation": abs(max_period["period_deviation"]),
                    "max_abs_cumulative_deviation": abs(max_cumulative["cumulative_deviation"]),
                    "max_period_location": max_period,
                    "max_cumulative_location": max_cumulative,
                }
            )
        result["balances"][name] = entry

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--cases", nargs="*")
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    result = audit(args.root, args.cases)
    text = json.dumps(result, indent=2) + "\n"
    if args.json:
        args.json.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
