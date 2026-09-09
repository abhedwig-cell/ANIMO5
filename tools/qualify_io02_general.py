from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from io02_general_contract import General41Parser, LegacyGrammarError, TOP_LEVEL_LABEL_CALL_ORDER

SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
VFPROJ_SHA256 = "f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a"
SOURCE_MEMBER = "ANIMO_4.1.5.53/input1.for"

GENERAL_MEMBERS = [
    "ANIMO_testbank/CranGrass/Input/GENERAL.INP",
    "ANIMO_testbank/CranMais/Input/GENERAL.INP",
    "ANIMO_testbank/GHGMais/Input/general.inp",
    "ANIMO_testbank/GrassPeat/Input/GENERAL.INP",
    "ANIMO_testbank/LWKM_gras_1040.2021.2045/input/GENERAL.INP",
    "ANIMO_testbank/Puitmijn_Cranendonck_60/input/GENERAL.INP",
    "ANIMO_testbank/RuurloGrass/Input/GENERAL.INP",
    "ANIMO_testbank/STONE_akk_0006.2001.2015/input/GENERAL.INP",
    "ANIMO_testbank/Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA/Input/GENERAL.INP",
]

QUALIFIED_NATURAL = {
    "ANIMO_testbank/CranGrass/Input/GENERAL.INP",
    "ANIMO_testbank/CranMais/Input/GENERAL.INP",
    "ANIMO_testbank/LWKM_gras_1040.2021.2045/input/GENERAL.INP",
    "ANIMO_testbank/Puitmijn_Cranendonck_60/input/GENERAL.INP",
    "ANIMO_testbank/RuurloGrass/Input/GENERAL.INP",
    "ANIMO_testbank/STONE_akk_0006.2001.2015/input/GENERAL.INP",
    "ANIMO_testbank/Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA/Input/GENERAL.INP",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ghg_option(text: str) -> int | None:
    for line in text.splitlines():
        if line.startswith("GreenHouseGasOption="):
            match = re.search(r"=\s*([+-]?\d+)", line)
            return int(match.group(1)) if match else None
    return None


def projection(text: str) -> dict:
    return General41Parser(text).parse()["projection"]


def get_record(parsed: dict, field_id: str) -> dict:
    matches = [r for r in parsed["records"] if r["field_id"] == field_id]
    if not matches:
        raise AssertionError(f"record not found: {field_id}")
    return matches[0]


def mutate_swap_complete_sections(text: str, a: str, b: str) -> str:
    lines = text.splitlines()
    starts = []
    for i, line in enumerate(lines):
        if line[:8] in TOP_LEVEL_LABEL_CALL_ORDER:
            starts.append((i, line[:8]))
    if set(label for _, label in starts) != set(TOP_LEVEL_LABEL_CALL_ORDER):
        raise AssertionError("fixture does not have exactly the six non-GHG top-level labels")
    prefix = lines[: starts[0][0]]
    blocks = {}
    order = []
    for j, (start, label) in enumerate(starts):
        end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        blocks[label] = lines[start:end]
        order.append(label)
    ia, ib = order.index(a), order.index(b)
    order[ia], order[ib] = order[ib], order[ia]
    out = prefix[:]
    for label in order:
        out.extend(blocks[label])
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def replace_first_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            lines[i] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    raise AssertionError(f"prefix not found: {prefix}")


def remove_first_line(text: str, prefix: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            del lines[i]
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    raise AssertionError(f"prefix not found: {prefix}")


def expect_error(text: str, expected: str) -> dict:
    try:
        General41Parser(text).parse()
    except LegacyGrammarError as exc:
        if exc.code != expected:
            raise AssertionError(f"expected {expected}, got {exc.code}: {exc}") from exc
        return {
            "status": "PASS",
            "observed_error": exc.code,
            "line": exc.line,
            "message": str(exc),
        }
    raise AssertionError(f"expected parser error {expected}, parser accepted mutation")


def source_contract_checks(source: str, vfproj_text: str) -> dict:
    checks = {}
    checks["revision_53_id"] = "$Id: input1.for 53 " in source
    checks["compiled_member_named_input1"] = 'RelativePath=".\\input1.for"' in vfproj_text
    checks["real_kind_8"] = 'RealKIND="realKIND8"' in vfproj_text
    checks["findadr_rewinds"] = "Rewind (Unit=unit)" in source
    checks["findadr_exact_a8"] = (
        "Read (Unit,'(A8)',Iostat=Ios) Text" in source
        and "If (Text.Eq.Label) Return" in source
    )
    checks["readop_bang_delimited"] = (
        "L2 = INDEX(text,'!')" in source
        and "Read(text(L1+1:L2-1),*) jout" in source
    )
    checks["readts_digit_scan"] = (
        "Do i=L1+1,132" in source and "if(text(i:i).eq.'3')then" in source
    )
    checks["optional_readts_defaults"] = (
        "AnnDOMNtotNO3_1mGWL=" in source
        and "DOMNtotNO3_1mGWL=" in source
        and "jout = 0" in source
    )
    checks["pclass_default_path"] = "IoptPCl=0" in source and "Error=0" in source
    checks["hydro_year_default_path"] = "HydrYrSw=0" in source
    compact = "".join(source.split())
    checks["hydro_year_wrong_range_check_preserved"] = (
        "CallCheckint(Uoer,Error,Label,'IoptPCl',IoptPCl,0,1)" in compact
    )
    checks["balance_sort"] = (
        "call sort(Tiba(Ibs,1:Nubati(Ibs)),Nubati(Ibs))" in source
    )
    checks["printbal_silent_return"] = (
        "if(Str256(1:idum).ne.'PrintBalLabel=') return" in source
    )
    checks["ghg_feature_gate"] = (
        "If (IoptGHG.Ge.1) Then" in source and "Label = '>outGHG:'" in source
    )

    positions = []
    for label in TOP_LEVEL_LABEL_CALL_ORDER:
        needle = f"Label = '{label}'"
        pos = source.find(needle)
        checks[f"label_call_{label}"] = pos >= 0
        positions.append(pos)
    checks["top_level_parser_call_order"] = all(
        a < b for a, b in zip(positions, positions[1:])
    )

    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise AssertionError(f"source contract anchors failed: {failed}")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", required=True, type=Path)
    parser.add_argument("--testbank-zip", required=True, type=Path)
    parser.add_argument("--vfproj", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    identities = {
        "source_zip_sha256": sha256(args.source_zip),
        "testbank_zip_sha256": sha256(args.testbank_zip),
        "vfproj_sha256": sha256(args.vfproj),
    }
    expected = {
        "source_zip_sha256": SOURCE_SHA256,
        "testbank_zip_sha256": TESTBANK_SHA256,
        "vfproj_sha256": VFPROJ_SHA256,
    }
    if identities != expected:
        raise SystemExit(f"frozen identity mismatch: {identities} != {expected}")

    with zipfile.ZipFile(args.source_zip) as source_zip:
        source = source_zip.read(SOURCE_MEMBER).decode("latin1")
    vfproj_text = args.vfproj.read_text(encoding="utf-8-sig")
    source_checks = source_contract_checks(source, vfproj_text)

    with zipfile.ZipFile(args.testbank_zip) as testbank:
        missing = [name for name in GENERAL_MEMBERS if name not in testbank.namelist()]
        if missing:
            raise AssertionError(f"expected GENERAL members missing: {missing}")
        natural = {}
        texts = {
            name: testbank.read(name).decode("latin1") for name in GENERAL_MEMBERS
        }
        for name, text in texts.items():
            option = ghg_option(text)
            if option is not None and option >= 1:
                natural[name] = {
                    "status": "EXCLUDED_GHG_SCHEMA_NOT_ADMITTED",
                    "GreenHouseGasOption": option,
                }
                continue
            try:
                parsed = General41Parser(text).parse()
                natural[name] = {
                    "status": "PASS_SOURCE_COMPATIBLE_BOUNDED_REPRESENTATION",
                    "record_count": len(parsed["records"]),
                    "source_defaults": parsed["meta"]["source_defaults"],
                    "legacy_storage_hazards": parsed["meta"]["legacy_storage_hazards"],
                }
            except LegacyGrammarError as exc:
                natural[name] = {
                    "status": "REJECTED_BY_REV53_SEQUENCE_CONTRACT",
                    "error": exc.code,
                    "line": exc.line,
                    "message": str(exc),
                }

    observed_pass = {
        name
        for name, result in natural.items()
        if result["status"] == "PASS_SOURCE_COMPATIBLE_BOUNDED_REPRESENTATION"
    }
    if observed_pass != QUALIFIED_NATURAL:
        raise AssertionError(f"unexpected natural pass set: {sorted(observed_pass)}")
    grass = natural["ANIMO_testbank/GrassPeat/Input/GENERAL.INP"]
    if grass.get("error") != "9871" or "WFPS=" not in grass.get("message", ""):
        raise AssertionError(f"GrassPeat negative evidence changed: {grass}")

    ruurlo = texts["ANIMO_testbank/RuurloGrass/Input/GENERAL.INP"]
    cran = texts["ANIMO_testbank/CranGrass/Input/GENERAL.INP"]
    lwkm = texts[
        "ANIMO_testbank/LWKM_gras_1040.2021.2045/input/GENERAL.INP"
    ]

    probes = {}

    reordered = mutate_swap_complete_sections(ruurlo, ">simtim:", ">outscr:")
    if projection(reordered) != projection(ruurlo):
        raise AssertionError(
            "complete top-level section reordering changed semantic projection"
        )
    probes["top_level_section_physical_reorder"] = {
        "status": "PASS",
        "finding": "Findadr rewind makes complete block physical order non-authoritative",
    }

    lines = ruurlo.splitlines()
    first = next(i for i, line in enumerate(lines) if line.startswith("HydrologicInput="))
    lines[first], lines[first + 1] = lines[first + 1], lines[first]
    probes["intra_simopt_key_reorder"] = expect_error(
        "\n".join(lines) + "\n", "9870"
    )

    probes["missing_label"] = expect_error(
        ruurlo.replace(">outscr:", ">outsXX:", 1), "1995"
    )
    probes["leading_space_in_ordered_key"] = expect_error(
        replace_first_line(
            ruurlo,
            "ProgressToScreen=",
            " ProgressToScreen= 1! shifted key",
        ),
        "9870",
    )

    pclass_omitted = remove_first_line(ruurlo, "PClassOption=")
    parsed_default = General41Parser(pclass_omitted).parse()
    pclass_record = get_record(parsed_default, "PClassOption=")
    if pclass_record["value"] != 0 or pclass_record["presence"] != "DEFAULTED":
        raise AssertionError(f"PClass default not explicit: {pclass_record}")
    probes["pclass_compatibility_default"] = {
        "status": "PASS",
        "value": 0,
        "presence": "DEFAULTED",
        "rule": pclass_record["default_rule_id"],
    }

    parsed_lwkm = General41Parser(lwkm).parse()
    hydro = get_record(parsed_lwkm, "HydroYearSwitch=")
    if hydro["value"] != -30:
        raise AssertionError(f"expected natural HydroYearSwitch=-30, got {hydro}")
    probes["hydro_year_negative_natural"] = {
        "status": "PASS",
        "value": -30,
        "finding": "revision-53 parses it and accidentally range-checks IoptPCl instead",
    }

    comment_digit = replace_first_line(
        ruurlo, "Nitrate=", "Nitrate= nonsense! comment supplies selector 3"
    )
    parsed_comment = General41Parser(comment_digit).parse()
    nitrate = get_record(parsed_comment, "Nitrate=")
    if nitrate["value"] != {
        "file_output": 1,
        "selected_compartment_output": 1,
    }:
        raise AssertionError(f"ReadTs digit-scan semantics changed: {nitrate}")
    probes["readts_scans_comment_for_first_0_to_3_digit"] = {
        "status": "PASS",
        "normalized": nitrate["value"],
    }

    date_renamed = replace_first_line(
        ruurlo,
        "StartDate=",
        "NotAStart=          1980-01-01! same fixed date columns",
    )
    if projection(date_renamed) != projection(ruurlo):
        raise AssertionError("source-compatible date key rename changed projection")
    probes["simtim_date_key_name_not_validated"] = {
        "status": "PASS",
        "finding": "date record identity is positional in revision-53, not key-validated",
    }

    balance_lines = ruurlo.splitlines()
    count_i = next(
        i
        for i, line in enumerate(balance_lines)
        if line.startswith("PrintBalNoUpd=") and re.search(r"=\s*1!", line)
    )
    balance_lines[count_i] = "PrintBalNoUpd=         2! synthetic two-date probe"
    if not balance_lines[count_i + 1].startswith("PrintBalUpdDate="):
        raise AssertionError("unexpected Ruurlo balance layout")
    balance_lines[count_i + 1] = (
        "PrintBalUpdDate= 300.0 100.0! synthetic unsorted"
    )
    parsed_sort = General41Parser("\n".join(balance_lines) + "\n").parse()
    dates = [
        record
        for record in parsed_sort["records"]
        if record["field_id"] == "PrintBalUpdDate="
    ][0]["value"]
    if dates != [100.0, 300.0]:
        raise AssertionError(
            f"balance date normalization does not reflect source sort: {dates}"
        )
    probes["repeated_balance_update_dates_source_sort"] = {
        "status": "PASS",
        "post_parser_value": dates,
        "lexical_order_preserved_separately": True,
    }

    cran_parsed = General41Parser(cran).parse()
    for key in ("AnnDOMNtotNO3_1mGWL=", "DOMNtotNO3_1mGWL="):
        record = get_record(cran_parsed, key)
        if (
            record["value"]["file_output"] != 0
            or record["value"]["selected_compartment_output"]
            != "LEGACY_UNDEFINED_IF_OMITTED"
        ):
            raise AssertionError(
                f"optional ReadTs hazard not preserved for {key}: {record}"
            )
    probes["optional_last_outputs_omission"] = {
        "status": "PASS_WITH_EXPLICIT_HAZARD",
        "file_output": 0,
        "selected_compartment_output": "LEGACY_UNDEFINED_IF_OMITTED",
    }

    probes["printbal_label_mismatch"] = expect_error(
        replace_first_line(
            ruurlo,
            "PrintBalLabel=",
            "WrongBalLabel= 'RP'! synthetic",
        ),
        "RETURN_WITHOUT_ERROR",
    )

    out_index = next(
        i for i, line in enumerate(ruurlo.splitlines()) if line[:8] == ">outscr:"
    )
    truncated = "\n".join(ruurlo.splitlines()[: out_index + 1]) + "\n"
    probes["eof_at_required_readop"] = expect_error(truncated, "9870")

    if (
        natural["ANIMO_testbank/GHGMais/Input/general.inp"]["status"]
        != "EXCLUDED_GHG_SCHEMA_NOT_ADMITTED"
    ):
        raise AssertionError("GHGMais routing boundary changed")
    probes["ghg_schema_boundary"] = {
        "status": "PASS",
        "finding": "GreenHouseGasOption>=1 routed, >outGHG payload not normalized",
    }

    result = {
        "workunit": "ANIMO-IO02",
        "schema": "ANIMO-IO02-Qualification/v1",
        "decision": "QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS",
        "production_migration_admitted": False,
        "grammar_redesign_admitted": False,
        "ghg_schema_admitted": False,
        "initial_restart_admitted": False,
        "binary_hydrology_admitted": False,
        "frozen_identities": identities,
        "source_contract_checks": source_checks,
        "natural_testbank": natural,
        "mutation_probes": probes,
        "qualified_natural_count": len(observed_pass),
        "non_ghg_natural_count": 8,
        "ghg_natural_count_excluded": 1,
        "explicit_exclusions": [
            "GrassPeat GENERAL with inserted WFPS= outsel field is not revision-53 sequence compatible",
            "GHGMais GENERAL schema is not admitted",
            "optional OutseLn(77:78) storage state when lines are omitted is not normalized to a fabricated zero",
            "whole-profile OutseLn(37,43,48,54) storage state is not input-defined by the ReadTs calls that use idum",
            "malformed ReadTs records without '=' are outside the bounded admitted grammar",
            "negative PrintBalNoUpd values below -1 are not assigned normalized repeat semantics",
            "uncontrolled runtime/EOF paths without explicit source error codes are not converted into scientific defaults",
        ],
        "equivalence_claim": (
            "For admitted revision-53-compatible non-GHG GENERAL files, the representation preserves "
            "typed ModelConfiguration, SimulationWindow and DiagnosticsConfiguration parser semantics, "
            "source-observed defaults, ordered repeated structures, lexical provenance and feature conditions. "
            "It does not claim byte round-trip identity and does not normalize undefined legacy storage artifacts."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "decision": result["decision"],
                "qualified_natural_count": result["qualified_natural_count"],
                "natural_files": len(natural),
                "probes": len(probes),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
