#!/usr/bin/env python3
"""Analyze ANIMO-MASSQ01 observer sidecars without a closure tolerance.

Qualification tooling only. Sidecars are observer evidence, not physical state.
Water beginning storage comes from the persisted hydrological start snapshot.
Chemical beginning storage (N, P and organic-matter mass) comes from the
read-only process-start snapshot captured after hydrology/crop preparation and
before Addit. This split is required by the revision-53 orchestration: Init
promotes layer-0 solute result concentrations but not Mofro(0), so reconstructing
chemical mass immediately after Init can create a representational jump that is
not a physical transfer.

A source-defined soil-organic-carbon view is derived as Cfracom times the
organic-matter ledger. This is deliberately narrower than whole-system carbon:
crop dry matter and CH4-C are not silently folded into this projection.

The recomputed beginning-storage and residual columns in massq01_step.dat are
instrumentation archaeology only and are deliberately not authoritative here.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

START_FILE = "massq01_start.dat"
CHEM_START_FILE = "massq01_chem_start.dat"
STEP_FILE = "massq01_step.dat"
DIRECT_FILE = "animo.ini"
ELEMENT_UNITS = {
    "W": "mm water",
    "N": "kg/ha N",
    "P": "kg/ha P",
    "O": "kg/ha organic_matter_mass",
    "C": "kg/ha C",
}
CHEMICAL_ELEMENTS = {"N", "P", "O"}
PATH_LINE = re.compile(r'^\s*([A-Za-z]{3})\s*=\s*"([^"]+)"')
ORGCOM_LABEL = re.compile(r"^\s*>orgcom\s*:", re.IGNORECASE)


def _key(value: float) -> str:
    rounded = round(value)
    if abs(value - rounded) == 0.0:
        return str(int(rounded))
    return format(value, ".17g")


def _find_case_insensitive(root: Path, relative: Path) -> Path | None:
    current = root
    for part in relative.parts:
        exact = current / part
        if exact.exists():
            current = exact
            continue
        if not current.is_dir():
            return None
        matches = [p for p in current.iterdir() if p.name.casefold() == part.casefold()]
        if len(matches) != 1:
            return None
        current = matches[0]
    return current


def parse_cfracom(case_dir: Path) -> tuple[float, str]:
    direct_path = case_dir / DIRECT_FILE
    text = direct_path.read_text(encoding="latin1")
    material_ref = None
    for raw in text.splitlines():
        match = PATH_LINE.match(raw)
        if match and match.group(1).upper() == "MAT":
            material_ref = match.group(2).replace("\\", "/")
            break
    if material_ref is None:
        raise ValueError(f"{direct_path}: MAT entry not found")

    material_path = _find_case_insensitive(case_dir, Path(material_ref))
    if material_path is None or not material_path.is_file():
        raise ValueError(f"{case_dir}: material file not found: {material_ref}")

    lines = material_path.read_text(encoding="latin1").splitlines()
    for index, raw in enumerate(lines):
        if not ORGCOM_LABEL.match(raw):
            continue
        for next_raw in lines[index + 1:]:
            payload = next_raw.split("!", 1)[0].strip()
            if not payload:
                continue
            if payload.startswith(">"):
                break
            token = payload.split()[0]
            try:
                value = float(token.replace("D", "E").replace("d", "e"))
            except ValueError as exc:
                raise ValueError(
                    f"{material_path}:{index + 2}: invalid Cfracom value {token!r}"
                ) from exc
            if not (0.0 < value <= 1.0):
                raise ValueError(f"{material_path}: Cfracom outside (0,1]: {value}")
            return value, material_path.relative_to(case_dir).as_posix()
        raise ValueError(f"{material_path}: >orgcom label has no numeric value")
    raise ValueError(f"{material_path}: >orgcom label not found")


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


def parse_chem_start(path: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split()
        if len(parts) != 7:
            raise ValueError(f"{path}:{lineno}: expected 7 columns, got {len(parts)}")
        tito, st, nitrogen, phosphorus, organic_matter, ghg, mp = parts
        key = _key(float(tito))
        if key in result:
            raise ValueError(f"{path}:{lineno}: duplicate TITO {key}")
        result[key] = {
            "tito": float(tito),
            "st": float(st),
            "N": float(nitrogen),
            "P": float(phosphorus),
            "O": float(organic_matter),
            "IoptGHG": int(ghg),
            "IoptMp": int(mp),
        }
    if not result:
        raise ValueError(f"{path}: no chemical start snapshots")
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
        if element not in {"W", "N", "P", "O"}:
            raise ValueError(f"{path}:{lineno}: unknown element code {element}")
        nums = list(map(float, parts[1:11]))
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
            "IoptGHG": int(parts[11]),
            "IoptMp": int(parts[12]),
        })
    if not rows:
        raise ValueError(f"{path}: no step records")
    return rows


def _summarize(rows: list[dict], unit: str) -> dict:
    max_row = max(rows, key=lambda item: abs(item["residual"]))
    return {
        "unit": unit,
        "records": len(rows),
        "max_abs_residual": abs(max_row["residual"]),
        "signed_residual_at_max": max_row["residual"],
        "tito_at_max": max_row["tito"],
        "begin_storage_source_at_max": max_row["begin_storage_source"],
        "cumulative_signed_residual": sum(item["residual"] for item in rows),
        "acceptance_tolerance_applied": False,
    }


def analyze_case(case_dir: Path) -> dict:
    starts = parse_start(case_dir / START_FILE)
    chem_starts = parse_chem_start(case_dir / CHEM_START_FILE)
    steps = parse_steps(case_dir / STEP_FILE)
    cfracom, cfracom_source = parse_cfracom(case_dir)
    by_element: dict[str, list[dict]] = defaultdict(list)
    seen_pairs: set[tuple[str, str]] = set()

    for row in steps:
        tito_key = _key(row["tito"])
        if tito_key not in starts:
            raise ValueError(f"{case_dir}: missing persisted water/start snapshot for TITO {tito_key}")
        pair = (row["element"], tito_key)
        if pair in seen_pairs:
            raise ValueError(f"{case_dir}: duplicate step record {pair}")
        seen_pairs.add(pair)

        start = starts[tito_key]
        if start["IoptGHG"] != row["IoptGHG"] or start["IoptMp"] != row["IoptMp"]:
            raise ValueError(f"{case_dir}: feature flag mismatch at TITO {tito_key}")
        if start["st"] != row["st"]:
            raise ValueError(f"{case_dir}: start timestep mismatch at TITO {tito_key}")

        if row["element"] in CHEMICAL_ELEMENTS:
            if tito_key not in chem_starts:
                raise ValueError(f"{case_dir}: missing chemical start snapshot for TITO {tito_key}")
            chem = chem_starts[tito_key]
            if chem["st"] != row["st"]:
                raise ValueError(f"{case_dir}: chemical-start timestep mismatch at TITO {tito_key}")
            if chem["IoptGHG"] != row["IoptGHG"] or chem["IoptMp"] != row["IoptMp"]:
                raise ValueError(f"{case_dir}: chemical-start feature flag mismatch at TITO {tito_key}")
            begin_storage = chem[row["element"]]
            begin_source = CHEM_START_FILE
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

    summaries = {
        element: _summarize(rows, ELEMENT_UNITS[element])
        for element, rows in sorted(by_element.items())
    }

    if "O" in by_element:
        c_rows = []
        for row in by_element["O"]:
            c_rows.append({
                **row,
                "begin_storage": row["begin_storage"] * cfracom,
                "external_inputs": row["external_inputs"] * cfracom,
                "external_outputs": row["external_outputs"] * cfracom,
                "source_terms": row["source_terms"] * cfracom,
                "end_storage": row["end_storage"] * cfracom,
                "residual": row["residual"] * cfracom,
            })
        summaries["C"] = _summarize(c_rows, ELEMENT_UNITS["C"])
        summaries["C"]["projection"] = "Cfracom * CV-SOIL-OM"
        summaries["C"]["Cfracom"] = cfracom
        summaries["C"]["Cfracom_source"] = cfracom_source
        summaries["C"]["whole_system_elemental_carbon_claim"] = False

    return {
        "case": case_dir.name,
        "evidence_class": "B1_DIAGNOSTIC_OBSERVER_SIDECAR_NOT_REFERENCE",
        "water_begin_storage_source": START_FILE,
        "chemical_begin_storage_source": CHEM_START_FILE,
        "chemical_begin_boundary": "after hydrology/crop preparation and before Addit",
        "step_transfer_and_end_storage_source": STEP_FILE,
        "soil_organic_carbon_projection": {
            "enabled": "C" in summaries,
            "formula": "C = Cfracom * organic_matter_mass",
            "Cfracom": cfracom,
            "source": cfracom_source,
            "scope": "soil organic C only; excludes crop dry matter and GHG carbon state",
        },
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
