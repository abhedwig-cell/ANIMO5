#!/usr/bin/env python3
"""ANIMO-IO01 bounded DIRECT/animo.ini parser-normalization pilot.

This module intentionally separates the revision-53 legacy grammar from the
new TTUTIL native representation. It contains the exact defined legacy DIRECT
text normalizer and a schema-surface validator for TTUTILNativeTextAdapter/v1.
Actual TTUTIL typed decoding is exercised by tools/ttutil_direct_probe.f90.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

LEGACY_ADAPTER_ID = "LegacyRevision53TextAdapter"
NATIVE_ADAPTER_ID = "TTUTILNativeTextAdapter/v1"
NORMALIZED_SCHEMA = "LegacyInputBinding/v1"
NATIVE_SCHEMA_VERSION = "ANIMO5_TTUTIL_DIRECT_V1"
MESSAGE_DEFAULT_RULE = "IO01-DIRECT-MES-DEFAULT-message.Out"

SELECTOR_TO_FIELD = {
    "GEN=": "GEN",
    "MAT=": "MAT",
    "PLA=": "PLA",
    "SOI=": "SOI",
    "BOU=": "BOU",
    "INI=": "INI",
    "MAN=": "MAN",
    "SWU=": "SWU",
    "WAI=": "WAI",
    "WAU=": "WAU",
    "CHE=": "CHE",
    "INO=": "INO",
    "CRU=": "CRU",
    "STE=": "STE",
}
BINDING_FIELDS = tuple(SELECTOR_TO_FIELD.values())
NATIVE_KEYS = frozenset({"SchemaVersion", "AnimoVersion", *BINDING_FIELDS, "MES"})


@dataclass(frozen=True)
class LegacyDirectParseError(ValueError):
    code: int
    message: str
    line: int | None = None

    def __str__(self) -> str:
        where = f" line {self.line}" if self.line is not None else ""
        return f"ANIMO legacy DIRECT error {self.code}{where}: {self.message}"


class LegacyDirectUndefinedBehavior(RuntimeError):
    """A revision-53 parser edge whose Fortran behavior is runtime-dependent."""

    def __init__(self, message: str):
        super().__init__(message)


@dataclass(frozen=True)
class NativeDirectSchemaError(ValueError):
    message: str
    line: int | None = None

    def __str__(self) -> str:
        where = f" line {self.line}" if self.line is not None else ""
        return f"TTUTILNativeTextAdapter/v1 schema error{where}: {self.message}"


def _fortran_a_field(text: str, width: int) -> str:
    """Model a Fortran A<w> input field: truncate or blank-pad to width."""
    return (text[:width]).ljust(width)


def legacy_strip(payload: str) -> str:
    """Semantic transcription of revision-53 Subroutine Strip where defined.

    The input is the A80 payload after the A4 selector. The first nonblank,
    nontab, non-double-quote character becomes Istart. The last subsequent
    double quote determines Ilast. If no such quote exists, the result is
    blank. If Istart remains zero while Ilast becomes positive, the original
    routine forms Fname(0:Ilast), outside the declared CHARACTER(80) bounds;
    that runtime-dependent edge is explicitly excluded rather than normalized.
    """
    fname = _fortran_a_field(payload, 80)
    istart = 0
    ilast = 0
    for i, ch in enumerate(fname, start=1):
        if ch not in (" ", "\t", '"') and istart == 0:
            istart = i
    for i in range(istart + 1, 81):
        if fname[i - 1] == '"':
            ilast = i - 1
    if ilast == 0:
        return ""
    if istart == 0:
        raise LegacyDirectUndefinedBehavior(
            "revision-53 Strip would form an out-of-bounds substring Fname(0:Ilast)"
        )
    return fname[istart - 1 : ilast].rstrip()


def _empty_binding_state() -> dict[str, dict[str, object]]:
    return {
        field: {"value": None, "presence": "INACTIVE_NULL", "source_line": None}
        for field in BINDING_FIELDS
    }


def parse_legacy_direct_text(text: str, source_file: str = "<memory>") -> dict[str, object]:
    """Parse revision-53 DIRECT text and return deterministic normalized state."""
    lines = text.splitlines()
    header_record = lines[0] if lines else ""
    header = _fortran_a_field(header_record, 7)
    if header == "Animo40":
        version = 40
    elif header == "Animo41":
        version = 41
    else:
        raise LegacyDirectParseError(
            12345,
            f"{source_file} does not start with Animo40 or Animo41",
            1,
        )

    bindings = _empty_binding_state()
    seen: dict[str, int] = {}
    unknown: list[dict[str, object]] = []
    duplicates: list[dict[str, object]] = []
    provenance: list[dict[str, object]] = []
    message = {
        "value": "message.Out",
        "presence": "DEFAULTED",
        "default_rule_id": MESSAGE_DEFAULT_RULE,
        "source_line": None,
    }
    chempar_selector_present = False
    soil_temperature_selector_present = False
    terminated_by = "EOF"

    for lineno, raw in enumerate(lines[1:], start=2):
        record = _fortran_a_field(raw, 84)
        selector = record[:4]
        payload = record[4:84]
        value = legacy_strip(payload)

        if selector == "END ":
            terminated_by = "END"
            break

        if selector == "MES=":
            if "MES" in seen:
                duplicates.append(
                    {
                        "field": "MES",
                        "previous_line": seen["MES"],
                        "replacement_line": lineno,
                        "rule": "LAST_ASSIGNMENT_WINS",
                    }
                )
            seen["MES"] = lineno
            if len(value.rstrip()) == 0:
                raise LegacyDirectParseError(
                    1016,
                    f"Input File Label MES= Not Defined In {source_file}",
                    lineno,
                )
            message = {
                "value": value,
                "presence": "EXPLICIT",
                "default_rule_id": None,
                "source_line": lineno,
            }
            provenance.append(
                {
                    "field": "MES",
                    "selector": selector,
                    "source_line": lineno,
                    "lexical_payload": payload.rstrip(),
                    "normalized_value": value,
                }
            )
            continue

        field = SELECTOR_TO_FIELD.get(selector)
        if field is not None:
            if field in seen:
                duplicates.append(
                    {
                        "field": field,
                        "previous_line": seen[field],
                        "replacement_line": lineno,
                        "rule": "LAST_ASSIGNMENT_WINS",
                    }
                )
            seen[field] = lineno
            bindings[field] = {
                "value": value,
                "presence": "EXPLICIT",
                "source_line": lineno,
            }
            if field == "CHE":
                chempar_selector_present = True
            if field == "STE":
                soil_temperature_selector_present = True
            provenance.append(
                {
                    "field": field,
                    "selector": selector,
                    "source_line": lineno,
                    "lexical_payload": payload.rstrip(),
                    "normalized_value": value,
                }
            )
            continue

        if selector.strip():
            unknown.append(
                {
                    "selector": selector,
                    "source_line": lineno,
                    "rule": "LEGACY_IGNORE_UNKNOWN_SELECTOR",
                }
            )

    gen_value = bindings["GEN"]["value"]
    if gen_value is None or len(str(gen_value).rstrip()) == 0:
        raise LegacyDirectParseError(
            1001,
            f"Input file label GEN= not defined in {source_file}",
            seen.get("GEN"),
        )

    return {
        "schema": NORMALIZED_SCHEMA,
        "adapter_id": LEGACY_ADAPTER_ID,
        "source_family": "DIRECT",
        "source_file": source_file,
        "animo_version": version,
        "bindings": bindings,
        "message_output": message,
        "flags": {
            "chempar_selector_present": chempar_selector_present,
            "soil_temperature_selector_present": soil_temperature_selector_present,
        },
        "diagnostics": {
            "unknown_selectors": unknown,
            "duplicate_selectors": duplicates,
            "terminated_by": terminated_by,
        },
        "provenance": provenance,
    }


def parse_legacy_direct_file(path: Path) -> dict[str, object]:
    text = path.read_bytes().decode("latin-1")
    return parse_legacy_direct_text(text, str(path))


def _native_assignment_key(line: str) -> str | None:
    """Return the TTUTIL assignment key for DIRECT-v1 schema prevalidation."""
    stripped = line.strip()
    if not stripped or stripped.startswith("*") or stripped.startswith("!"):
        return None
    if "=" not in stripped:
        raise NativeDirectSchemaError("expected scalar assignment containing '='")
    key = stripped.split("=", 1)[0].strip()
    if not key:
        raise NativeDirectSchemaError("empty variable name")
    return key


def validate_native_direct_schema(text: str) -> list[str]:
    """Fail closed on unknown/duplicate TTUTILNativeTextAdapter/v1 keys."""
    seen: dict[str, int] = {}
    ordered: list[str] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        try:
            key = _native_assignment_key(raw)
        except NativeDirectSchemaError as exc:
            raise NativeDirectSchemaError(exc.message, lineno) from None
        if key is None:
            continue
        if key not in NATIVE_KEYS:
            raise NativeDirectSchemaError(f"unknown key {key!r}", lineno)
        if key in seen:
            raise NativeDirectSchemaError(
                f"duplicate key {key!r}; first occurrence was line {seen[key]}",
                lineno,
            )
        seen[key] = lineno
        ordered.append(key)
    for required in ("SchemaVersion", "AnimoVersion", "GEN"):
        if required not in seen:
            raise NativeDirectSchemaError(f"missing mandatory key {required!r}")
    return ordered


def parse_native_probe_output(text: str, source_file: str = "<native-probe>") -> dict[str, object]:
    """Convert deterministic ttutil_direct_probe output into the normalized object."""
    values: dict[str, str] = {}
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        if raw.startswith("ERROR="):
            raise NativeDirectSchemaError(raw.split("=", 1)[1], lineno)
        if "=" not in raw:
            raise NativeDirectSchemaError(f"malformed probe output {raw!r}", lineno)
        key, value = raw.split("=", 1)
        if key in values:
            raise NativeDirectSchemaError(f"duplicate probe output key {key!r}", lineno)
        values[key] = value

    if values.get("schema") != NORMALIZED_SCHEMA:
        raise NativeDirectSchemaError("probe did not emit LegacyInputBinding/v1")
    if values.get("adapter_id") != NATIVE_ADAPTER_ID:
        raise NativeDirectSchemaError("probe adapter id mismatch")
    try:
        animo_version = int(values["animo_version"])
    except (KeyError, ValueError) as exc:
        raise NativeDirectSchemaError("invalid probe AnimoVersion") from exc

    bindings = _empty_binding_state()
    for field in BINDING_FIELDS:
        presence = values.get(f"binding.{field}.presence")
        value = values.get(f"binding.{field}.value")
        if presence not in ("EXPLICIT", "INACTIVE_NULL") or value is None:
            raise NativeDirectSchemaError(f"incomplete probe binding output for {field}")
        bindings[field] = {
            "value": value if presence == "EXPLICIT" else None,
            "presence": presence,
            "source_line": None,
        }

    message_presence = values.get("message_output.presence")
    message_value = values.get("message_output.value")
    if message_presence not in ("EXPLICIT", "DEFAULTED") or message_value is None:
        raise NativeDirectSchemaError("incomplete probe message output")

    def flag(name: str) -> bool:
        raw = values.get(f"flag.{name}")
        if raw == "true":
            return True
        if raw == "false":
            return False
        raise NativeDirectSchemaError(f"invalid probe flag {name}")

    return {
        "schema": NORMALIZED_SCHEMA,
        "adapter_id": NATIVE_ADAPTER_ID,
        "source_family": "DIRECT",
        "source_file": source_file,
        "animo_version": animo_version,
        "bindings": bindings,
        "message_output": {
            "value": message_value,
            "presence": message_presence,
            "default_rule_id": MESSAGE_DEFAULT_RULE if message_presence == "DEFAULTED" else None,
            "source_line": None,
        },
        "flags": {
            "chempar_selector_present": flag("chempar_selector_present"),
            "soil_temperature_selector_present": flag("soil_temperature_selector_present"),
        },
        "diagnostics": {
            "unknown_selectors": [],
            "duplicate_selectors": [],
            "terminated_by": "TTUTIL",
        },
        "provenance": [],
    }


def semantic_projection(obj: dict[str, object]) -> dict[str, object]:
    """Projection used for representation-only DIRECT equivalence."""
    bindings = obj["bindings"]
    assert isinstance(bindings, dict)
    message = obj["message_output"]
    assert isinstance(message, dict)
    return {
        "schema": obj["schema"],
        "animo_version": obj["animo_version"],
        "bindings": {
            field: {
                "value": bindings[field]["value"],
                "presence": bindings[field]["presence"],
            }
            for field in BINDING_FIELDS
        },
        "message_output": {
            "value": message["value"],
            "presence": message["presence"],
        },
        "flags": obj["flags"],
    }


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--validate-native-schema", action="store_true")
    args = parser.parse_args()
    if args.validate_native_schema:
        keys = validate_native_direct_schema(args.path.read_text(encoding="utf-8"))
        print(json.dumps({"adapter_id": NATIVE_ADAPTER_ID, "keys": keys}, indent=2))
    else:
        print(json.dumps(parse_legacy_direct_file(args.path), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
