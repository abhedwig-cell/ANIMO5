#!/usr/bin/env python3
"""Analyze ANIMO-MASSQ01 observer sidecars without applying a closure tolerance.

Qualification tooling only. Sidecars are observer evidence, not physical state.
For the first simulated interval, beginning storage comes from the initialized
accepted-state snapshot. For subsequent chemical intervals (N, P and organic
matter), beginning storage comes from the previous result-state projection
captured immediately before Init. This avoids treating Init/hydrology staging as
physical creation or loss. Water continues to use the explicit persisted start
snapshot.

The recomputed beginning-storage and residual columns in massq01_step.dat are
instrumentation archaeology only and are deliberately not authoritative here.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

START_FILE = "massq01_start.dat"
RESULT_BEGIN_FILE = "massq01_init_pre.dat"
STEP_FILE = "massq01_step.dat"
ELEMENT_UNITS = {
    "W": "mm water",
    "N": "kg/ha N",
    "P": "kg/ha P",
    "O": "kg/ha organic_matter_mass",
}
CHEMICAL_ELEMENTS = {"N", "P", "O"}


def _key(value: float) -> str:
    rounded = round(value)
    if abs(value - rounded) == 0.0:
        return str(int(rounded))
    return format(value, ".17g")


def parse_start(path: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split()
        if len(parts) != 8:
            raise ValueError(f"{path}:{lineno}: expected 8 columns, got {len(parts)}")
        tito, st, water, nitrogen, phosphorus, organic_matter, ghg, mp = parts
        key = _key(float(tito))
        if key in result:
            raise ValueError(f"{path}:{lineno}: duplicate TITO {key}")
        result[key] = {
            "tito": float(tito),
            "st": float(st),
            "W": float(water),
            "N": float(nitrogen),
            "P": float(phosphorus),
            "O": float(organic_matter),
            "IoptGHG": int(ghg),
            "IoptMp": int(mp),
        }
    if not result:
        raise ValueError(f"{path}: no start snapshots")
    return result


def parse_result_begin(path: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split()
        if len(parts) != 5:
            raise ValueError(f"{path}:{lineno}: expected 5 columns, got {len(parts)}")
        tito, st, nitrogen, phosphorus, organic_matter = parts
        key = _key(float(tito))
        if key in result:
            raise ValueError(f"{path}:{lineno}: duplicate TITO {key}")
        result[key] = {
            "tito": float(tito),
            "st": float(st),
            "N": float(nitrogen),
            "P": float(phosphorus),
            "O": float(organic_matter),
        }
    if not result:
        raise ValueError(f"{path}: no previous-result snapshots")
    return result


def parse_steps(path: Path) -> list[dict]:
    rows: list[dict] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split()
        if len(parts) != 13:
            raise ValueError(f"{path}:{lineno}: expected 13 columns, got {len(parts)}")
        element = parts[0]
        if element not in ELEMENT_UNITS:
            raise ValueError(f"{path}:{lineno}: unknown element code {element}")
        nums = list(map(float, parts[1:11]))
        ghg = int(parts[11])
        mp = int(parts[12])
        rows.append({
            "element": element,
            "tito": nums[0],
            "st": nums[1],
            "instrumented_recomputed_begin": nums[2],
            "external_inputs": nums[3],
            "external_outputs": nums[4],
            "source_terms": nums[5],
            "end_storage": nums[6],
            "instrumented_recomputed_residual": nums[7],
            "aux1": nums[8],
            "aux2": nums[9],
            "IoptGHG": ghg,
            "IoptMp": mp,
        })
    if not rows:
        raise ValueError(f"{path}: no step records")
    return rows


def analyze_case(case_dir: Path) -> dict:
    starts = parse_start(case_dir / START_FILE)
    result_begins = parse_result_begin(case_dir / RESULT_BEGIN_FILE)
    steps = parse_steps(case_dir / STEP_FILE)
    first_tito_key = _key(steps[0]["tito"])
    by_element: dict[str, list[dict]] = defaultdict(list)
    seen_pairs: set[tuple[str, str]] = set()

    for row in steps:
        tito_key = _key(row["tito"])
        if tito_key not in starts:
            raise ValueError(f"{case_dir}: missing persisted start snapshot for TITO {tito_key}")
        pair = (row["element"], tito_key)
        if pair in seen_pairs:
            raise ValueError(f"{case_dir}: duplicate step record {pair}")
        seen_pairs.add(pair)

        start = starts[tito_key]
        if start["IoptGHG"] != row["IoptGHG"] or start["IoptMp"] != row["IoptMp"]:
            raise ValueError(f"{case_dir}: feature flag mismatch at TITO {tito_key}")

        if row["element"] in CHEMICAL_ELEMENTS and tito_key != first_tito_key:
            if tito_key not in result_begins:
                raise ValueError(
                    f"{case_dir}: missing previous-result begin snapshot for TITO {tito_key}"
                )
            result_begin = result_begins[tito_key]
            if result_begin["st"] != row["st"]:
                raise ValueError(f"{case_dir}: result-begin timestep mismatch at TITO {tito_key}")
            begin_storage = result_begin[row["element"]]
            begin_source = RESULT_BEGIN_FILE
        else:
            begin_storage = start[row["element"]]
            begin_source = START_FILE

        residual = (
            begin_storage
            + row["external_inputs"]
            + row["source_terms"]
            - row["external_outputs"]
            - row["end_storage"]
        )
        by_element[row["element"]].append({
            "tito": row["tito"],
            "st": row["st"],
            "begin_storage": begin_storage,
            "begin_storage_source": begin_source,
            "external_inputs": row["external_inputs"],
            "external_outputs": row["external_outputs"],
            "source_terms": row["source_terms"],
            "end_storage": row["end_storage"],
            "residual": residual,
        })

    summaries = {}
    for element, rows in sorted(by_element.items()):
        max_row = max(rows, key=lambda item: abs(item["residual"]))
        summaries[element] = {
            "unit": ELEMENT_UNITS[element],
            "records": len(rows),
            "max_abs_residual": abs(max_row["residual"]),
            "signed_residual_at_max": max_row["residual"],
            "tito_at_max": max_row["tito"],
            "begin_storage_source_at_max": max_row["begin_storage_source"],
            "cumulative_signed_residual": sum(item["residual"] for item in rows),
            "acceptance_tolerance_applied": False,
        }

    return {
        "case": case_dir.name,
        "evidence_class": "B1_DIAGNOSTIC_OBSERVER_SIDECAR_NOT_REFERENCE",
        "first_interval_begin_storage_source": START_FILE,
        "subsequent_chemical_begin_storage_source": RESULT_BEGIN_FILE,
        "water_begin_storage_source": START_FILE,
        "step_transfer_and_end_storage_source": STEP_FILE,
        "legacy_balance_accumulator_used_as_storage_owner": False,
        "acceptance_tolerance_applied": False,
        "elements": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dirs", nargs="+", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    report = {
        "tool": "analyze_massledger_b1_sidecars.py",
        "qualification_boundary": "B1_DIAGNOSTIC_OBSERVER_NOT_REFERENCE_NO_TOLERANCE",
        "cases": [analyze_case(path.resolve()) for path in args.case_dirs],
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
