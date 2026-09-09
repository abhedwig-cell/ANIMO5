#!/usr/bin/env python3
"""ANIMO-IO01 bounded MATERIAL Pilot B.

Scope is deliberately narrow: revision-53 MATERIAL input as exercised by the
natural non-GHG RuurloGrass case with IPO=0, Ioptae=0 and IoptGHG=0.

The legacy parser surface and the TTUTIL native v1 representation are separate.
This module provides the legacy normalization oracle, the native schema surface
validator, and semantic projection used for representation-only comparison.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

LEGACY_ADAPTER_ID = "LegacyRevision53MaterialAdapter/Ruurlo-v1"
NATIVE_ADAPTER_ID = "TTUTILNativeMaterialAdapter/v1"
NORMALIZED_SCHEMA = "MaterialParameterSet/v1"
NATIVE_SCHEMA_VERSION = "ANIMO5_TTUTIL_MATERIAL_V1"

ACTIVE_LABELS = (
    ">defmat:", ">orgcom:", ">deffra:", ">defexu:", ">defdom:",
    ">defsdo:", ">defhum:", ">defntr:", ">defden:", ">matfra:",
)

NATIVE_KEYS = frozenset({
    "SchemaVersion", "IPO", "Nm", "Nf",
    "Fror", "Frnh", "Frni", "Cfracom",
    "Recfav", "Hufros", "RatioRdSt", "Asfa", "Nifr",
    "Recfexav", "Hufrosex", "Asfaex", "Nifrex", "Pofrex",
    "Recfcaav", "SDOfr", "Asfaca",
    "RecfSDOav", "AsfaSDO",
    "RecfHUav", "RecfHUSDOav", "AsfaHU", "Nifrhuma", "Pofrhuma",
    "Recfntav", "Recfdeav", "Frhetero",
    "FR", "FRca",
})


@dataclass(frozen=True)
class LegacyMaterialParseError(ValueError):
    message: str
    section: str | None = None
    record: int | None = None

    def __str__(self) -> str:
        where = ""
        if self.section:
            where += f" section {self.section}"
        if self.record is not None:
            where += f" record {self.record}"
        return f"legacy MATERIAL parse error{where}: {self.message}"


@dataclass(frozen=True)
class NativeMaterialSchemaError(ValueError):
    message: str
    line: int | None = None

    def __str__(self) -> str:
        where = f" line {self.line}" if self.line is not None else ""
        return f"TTUTIL native MATERIAL v1 schema error{where}: {self.message}"


def _d(token: str) -> Decimal:
    try:
        value = Decimal(token.replace("D", "E").replace("d", "e"))
    except InvalidOperation as exc:
        raise LegacyMaterialParseError(f"malformed numeric token {token!r}") from exc
    if not value.is_finite():
        raise LegacyMaterialParseError(f"non-finite numeric token {token!r}")
    return value


def _as_float(value: Decimal) -> float:
    return float(value)


def _record_tokens(record: str) -> list[str]:
    if "/" in record or "*" in record:
        raise LegacyMaterialParseError(
            "list-directed repetition or slash termination is outside bounded Pilot B"
        )
    return [t for t in re.split(r"[\s,]+", record.strip()) if t]


def _find_label_line(lines: list[str], label: str) -> int:
    for idx, line in enumerate(lines):
        if (line[:8]).ljust(8) == label:
            return idx
    raise LegacyMaterialParseError("required label not found", label)


def _records_after_label(text: str, label: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    start = _find_label_line(lines, label)
    out: list[tuple[int, str]] = []
    for idx in range(start + 1, len(lines)):
        raw = lines[idx]
        if raw.startswith(">"):
            break
        if not raw.strip():
            continue
        out.append((idx + 1, raw))
    return out


def _one_record(records, pos, section):
    if pos >= len(records):
        raise LegacyMaterialParseError("unexpected end of section", section)
    lineno, raw = records[pos]
    return lineno, _record_tokens(raw), pos + 1


def _check_range(name: str, value: Decimal, low: float, high: float, section: str) -> None:
    fv = float(value)
    if fv < low or fv > high:
        raise LegacyMaterialParseError(
            f"{name}={value} outside revision-53 range [{low},{high}]", section
        )


def parse_legacy_material_text(
    text: str,
    *,
    source_file: str = "<memory>",
    ipo: int = 0,
    ioptae: int = 0,
    ioptghg: int = 0,
) -> dict[str, object]:
    """Normalize the bounded revision-53 Ruurlo MATERIAL representation."""
    if ipo != 0 or ioptae != 0 or ioptghg != 0:
        raise LegacyMaterialParseError(
            "Pilot B v1 is admitted only for IPO=0, Ioptae=0, IoptGHG=0"
        )

    lexical_residue: dict[str, list[dict[str, object]]] = {"defmat": [], "deffra": []}
    parsed_unused: dict[str, list[dict[str, object]]] = {"material_type_tokens": []}

    sec = ">defmat:"
    recs = _records_after_label(text, sec); pos = 0
    lineno, tok, pos = _one_record(recs, pos, sec)
    if len(tok) != 1:
        raise LegacyMaterialParseError("Nm record must contain exactly one value", sec, lineno)
    try: nm = int(tok[0])
    except ValueError as exc: raise LegacyMaterialParseError("invalid Nm", sec, lineno) from exc
    if nm < 1:
        raise LegacyMaterialParseError("Nm must be positive", sec, lineno)

    materials: list[dict[str, object] | None] = [None] * nm
    for _ in range(nm):
        lineno, tok, pos = _one_record(recs, pos, sec)
        if len(tok) < 5:
            raise LegacyMaterialParseError("short defmat row", sec, lineno)
        try:
            mty, mn = int(tok[0]), int(tok[1])
        except ValueError as exc:
            raise LegacyMaterialParseError("invalid Mty/Mn", sec, lineno) from exc
        if not 1 <= mn <= nm:
            raise LegacyMaterialParseError("Mn outside 1..Nm", sec, lineno)
        if materials[mn - 1] is not None:
            raise LegacyMaterialParseError(
                "duplicate material index would leave another material undefined", sec, lineno
            )
        fror, frnh, frni = map(_d, tok[2:5])
        for name, val in (("Fror", fror), ("Frnh", frnh), ("Frni", frni)):
            _check_range(name, val, 0.0, 1.0, sec)
        residues = tok[5:]
        lexical_residue["defmat"].append(
            {"line": lineno, "mn": mn, "tokens": residues, "reason": "IPO=0 implied-DO consumes no Frpo"}
        )
        parsed_unused["material_type_tokens"].append({"line": lineno, "mn": mn, "Mty": mty})
        materials[mn - 1] = {
            "mn": mn,
            "fror": _as_float(fror),
            "frnh": _as_float(frnh),
            "frni": _as_float(frni),
            "frpo": None,
            "frpo_presence": "FEATURE_INACTIVE_NULL",
        }
    if any(x is None for x in materials):
        raise LegacyMaterialParseError("incomplete material index coverage", sec)

    sec = ">orgcom:"; recs = _records_after_label(text, sec)
    lineno, tok, _ = _one_record(recs, 0, sec)
    if len(tok) < 1: raise LegacyMaterialParseError("missing Cfracom", sec, lineno)
    cfracom = _d(tok[0]); _check_range("Cfracom", cfracom, 0.1, 1.0, sec)

    sec = ">deffra:"; recs = _records_after_label(text, sec); pos = 0
    lineno, tok, pos = _one_record(recs, pos, sec)
    if len(tok) != 1: raise LegacyMaterialParseError("Nf record must contain exactly one value", sec, lineno)
    try: nf = int(tok[0])
    except ValueError as exc: raise LegacyMaterialParseError("invalid Nf", sec, lineno) from exc
    if nf < 1: raise LegacyMaterialParseError("Nf must be positive", sec, lineno)
    fractions: list[dict[str, object] | None] = [None] * nf
    for _ in range(nf):
        lineno, tok, pos = _one_record(recs, pos, sec)
        if len(tok) < 6: raise LegacyMaterialParseError("short deffra row", sec, lineno)
        try: frno = int(tok[0])
        except ValueError as exc: raise LegacyMaterialParseError("invalid Frno", sec, lineno) from exc
        if not 1 <= frno <= nf: raise LegacyMaterialParseError("Frno outside 1..Nf", sec, lineno)
        if fractions[frno - 1] is not None:
            raise LegacyMaterialParseError("duplicate fraction index", sec, lineno)
        recfav, hufros, ratio, asfa, nifr = map(_d, tok[1:6])
        _check_range("Recfav", recfav, 0.0, 365.0, sec)
        for name, val in (("Hufros", hufros), ("Ratio_rd_st", ratio), ("Asfa", asfa), ("Nifr", nifr)):
            _check_range(name, val, 0.0, 1.0, sec)
        lexical_residue["deffra"].append(
            {"line": lineno, "frno": frno, "tokens": tok[6:], "reason": "IPO=0 implied-DO consumes no Pofr"}
        )
        fractions[frno - 1] = {
            "frno": frno, "recfav": _as_float(recfav), "hufros": _as_float(hufros),
            "ratio_rd_st": _as_float(ratio), "asfa": _as_float(asfa), "nifr": _as_float(nifr),
            "pofr": None, "pofr_presence": "FEATURE_INACTIVE_NULL",
        }
    if any(x is None for x in fractions):
        raise LegacyMaterialParseError("incomplete fraction index coverage", sec)

    def one_vals(label: str, count: int) -> tuple[list[Decimal], int]:
        recs = _records_after_label(text, label)
        lineno, tok, _ = _one_record(recs, 0, label)
        if len(tok) < count:
            raise LegacyMaterialParseError(f"expected {count} values", label, lineno)
        return [_d(x) for x in tok[:count]], lineno

    vals, _ = one_vals(">defexu:", 5)
    recfexav,hufrosex,asfaex,nifrex,pofrex = vals
    _check_range("Recfexav", recfexav,0,365,">defexu:")
    for n,v in (("Hufrosex",hufrosex),("Asfaex",asfaex),("Nifrex",nifrex),("Pofrex",pofrex)):
        _check_range(n,v,0,1,">defexu:")

    vals,_=one_vals(">defdom:",3); recfcaav,sdofr,asfaca=vals
    _check_range("Recfcaav",recfcaav,0,100,">defdom:")
    _check_range("SDOfr",sdofr,0,1,">defdom:"); _check_range("Asfaca",asfaca,0,1,">defdom:")

    vals,_=one_vals(">defsdo:",2); recfsdoav,asfasdo=vals
    _check_range("RecfSDOav",recfsdoav,0,999,">defsdo:"); _check_range("AsfaSDO",asfasdo,0,1,">defsdo:")

    vals,_=one_vals(">defhum:",5); recfhuav,recfhusdoav,asfahu,nifrhuma,pofrhuma=vals
    _check_range("RecfHUav",recfhuav,0,0.1,">defhum:")
    _check_range("RecfHUSDOav",recfhusdoav,0,999,">defhum:")
    for n,v in (("AsfaHU",asfahu),("Nifrhuma",nifrhuma),("Pofrhuma",pofrhuma)):
        _check_range(n,v,0,1,">defhum:")

    vals,_=one_vals(">defntr:",1); recfntav=vals[0]
    _check_range("Recfntav",recfntav,0,500,">defntr:")
    vals,_=one_vals(">defden:",2); recfdeav,frhetero=vals
    _check_range("Recfdeav",recfdeav,0,1,">defden:"); _check_range("Frhetero",frhetero,0,1,">defden:")

    sec = ">matfra:"; recs = _records_after_label(text, sec); pos = 0
    fr = [[0.0 for _ in range(nf)] for _ in range(nm)]
    frca = [[0.0 for _ in range(nf)] for _ in range(nm)]
    sparse_rows=[]; seen_materials=set()
    for _ in range(nm):
        if pos >= len(recs): raise LegacyMaterialParseError("missing matfra material row",sec)
        start_line, raw = recs[pos]; pos += 1
        tokens = _record_tokens(raw)
        while len(tokens) < 2:
            if pos >= len(recs): raise LegacyMaterialParseError("short matfra header",sec,start_line)
            tokens.extend(_record_tokens(recs[pos][1])); pos += 1
        try: mn=int(tokens[0]); nufr=int(tokens[1])
        except ValueError as exc: raise LegacyMaterialParseError("invalid Mn/NuFR",sec,start_line) from exc
        if not 1<=mn<=nm: raise LegacyMaterialParseError("matfra Mn outside 1..Nm",sec,start_line)
        if mn in seen_materials: raise LegacyMaterialParseError("duplicate matfra material index",sec,start_line)
        if nufr<0 or nufr>nf: raise LegacyMaterialParseError("NuFR outside 0..Nf",sec,start_line)
        needed=2+3*nufr
        while len(tokens) < needed:
            if pos>=len(recs): raise LegacyMaterialParseError("matfra continuation truncated",sec,start_line)
            tokens.extend(_record_tokens(recs[pos][1])); pos+=1
        consumed=tokens[:needed]
        ignored_final_record_residue=tokens[needed:]
        explicit=[]
        for j in range(nufr):
            base=2+3*j
            try: fn=int(consumed[base])
            except ValueError as exc: raise LegacyMaterialParseError("invalid matfra frno",sec,start_line) from exc
            if not 1<=fn<=nf: raise LegacyMaterialParseError("matfra frno outside 1..Nf",sec,start_line)
            fv=_d(consumed[base+1]); cv=_d(consumed[base+2])
            _check_range("FR",fv,0,1,sec)
            if float(cv)<0 or float(cv)>float(fv):
                raise LegacyMaterialParseError("FRca outside 0..FR",sec,start_line)
            fr[mn-1][fn-1]=_as_float(fv); frca[mn-1][fn-1]=_as_float(cv)
            explicit.append({"frno":fn,"fr":_as_float(fv),"frca":_as_float(cv)})
        if sum(fr[mn-1]) > 1.000001 + 1e-15:
            raise LegacyMaterialParseError("sum FR exceeds 1.000001",sec,start_line)
        sparse_rows.append({
            "mn":mn,"nufr":nufr,"explicit":explicit,
            "ignored_final_record_residue":ignored_final_record_residue,
        })
        seen_materials.add(mn)
    if seen_materials != set(range(1,nm+1)):
        raise LegacyMaterialParseError("incomplete matfra material coverage",sec)

    return {
        "schema": NORMALIZED_SCHEMA,
        "adapter_id": LEGACY_ADAPTER_ID,
        "source_family": "MAT",
        "source_file": source_file,
        "feature_context": {"IPO": ipo, "Ioptae": ioptae, "IoptGHG": ioptghg},
        "dimensions": {"Nm": nm, "Nf": nf},
        "materials": materials,
        "fractions": fractions,
        "cfracom": _as_float(cfracom),
        "exudate": {"recfexav":_as_float(recfexav),"hufrosex":_as_float(hufrosex),"asfaex":_as_float(asfaex),"nifrex":_as_float(nifrex),"pofrex":_as_float(pofrex)},
        "dom": {"recfcaav":_as_float(recfcaav),"sdofr":_as_float(sdofr),"asfaca":_as_float(asfaca)},
        "sdo": {"recfsdoav":_as_float(recfsdoav),"asfasdo":_as_float(asfasdo)},
        "humus": {"recfhuav":_as_float(recfhuav),"recfhusdoav":_as_float(recfhusdoav),"asfahu":_as_float(asfahu),"nifrhuma":_as_float(nifrhuma),"pofrhuma":_as_float(pofrhuma)},
        "nitrification": {"recfntav":_as_float(recfntav)},
        "denitrification": {"recfdeav":_as_float(recfdeav),"frhetero":_as_float(frhetero)},
        "allocation": {"fr":fr,"frca":frca,"sparse_source_rows":sparse_rows,"omitted_sparse_rule":"ZERO_BY_RUURLO_NATURAL_LINEAGE_EQUIVALENCE"},
        "conditional_inactive": {"sonicg":None,"sonic2":None,"ghg_material_extension":None},
        "legacy_lexical_residue": lexical_residue,
        "parsed_but_unused_legacy_metadata": parsed_unused,
        "legacy_runtime_hazards": [
            "IPO0_Pofr_is_range_checked_after_zero-element_implied-DO_read",
            "sparse_FR_FRca_unassigned_cells_are_read_without_explicit_source_initialization",
        ],
    }


def parse_legacy_material_file(path: Path, **kwargs) -> dict[str, object]:
    return parse_legacy_material_text(path.read_bytes().decode("latin-1"), source_file=str(path), **kwargs)


def validate_native_material_schema(text: str) -> list[str]:
    seen: dict[str,int]={}; ordered=[]; previous_key: str | None = None
    for lineno, raw in enumerate(text.splitlines(),1):
        s=raw.strip()
        if not s or s.startswith("!") or s.startswith("*"): continue
        if "=" not in s:
            if raw[:1].isspace() and previous_key is not None:
                continue
            raise NativeMaterialSchemaError("expected assignment containing '='",lineno)
        key=s.split("=",1)[0].strip()
        if key not in NATIVE_KEYS: raise NativeMaterialSchemaError(f"unknown key {key!r}",lineno)
        if key in seen: raise NativeMaterialSchemaError(f"duplicate key {key!r}; first line {seen[key]}",lineno)
        seen[key]=lineno; ordered.append(key); previous_key=key
    for key in NATIVE_KEYS:
        if key not in seen: raise NativeMaterialSchemaError(f"missing mandatory key {key!r}")
    return ordered


def dense_native_typed_double_fixture(obj: dict[str, object]) -> str:
    """Comparison-only TTUTIL DOUBLE representation; not the admitted exact path."""
    def fmt(x):
        if isinstance(x,int): return str(x)
        return repr(float(x))
    def arr_lines(name, values, per_line=8):
        vals=[fmt(v) for v in values]; out=[]
        for i in range(0,len(vals),per_line):
            prefix=f"{name} = " if i==0 else "  "
            out.append(prefix+" ".join(vals[i:i+per_line]))
        return out
    mats=obj['materials']; fracs=obj['fractions']; alloc=obj['allocation']
    ex=obj['exudate']; dom=obj['dom']; sdo=obj['sdo']; hu=obj['humus']; ni=obj['nitrification']; de=obj['denitrification']
    nm=obj['dimensions']['Nm']; nf=obj['dimensions']['Nf']
    lines=[
        f"SchemaVersion = '{NATIVE_SCHEMA_VERSION}'",
        "IPO = 0", f"Nm = {nm}", f"Nf = {nf}",
        *arr_lines("Fror",(m['fror'] for m in mats)), *arr_lines("Frnh",(m['frnh'] for m in mats)), *arr_lines("Frni",(m['frni'] for m in mats)),
        f"Cfracom = {fmt(obj['cfracom'])}",
        *arr_lines("Recfav",(f['recfav'] for f in fracs)), *arr_lines("Hufros",(f['hufros'] for f in fracs)),
        *arr_lines("RatioRdSt",(f['ratio_rd_st'] for f in fracs)), *arr_lines("Asfa",(f['asfa'] for f in fracs)), *arr_lines("Nifr",(f['nifr'] for f in fracs)),
        f"Recfexav = {fmt(ex['recfexav'])}", f"Hufrosex = {fmt(ex['hufrosex'])}", f"Asfaex = {fmt(ex['asfaex'])}", f"Nifrex = {fmt(ex['nifrex'])}", f"Pofrex = {fmt(ex['pofrex'])}",
        f"Recfcaav = {fmt(dom['recfcaav'])}", f"SDOfr = {fmt(dom['sdofr'])}", f"Asfaca = {fmt(dom['asfaca'])}",
        f"RecfSDOav = {fmt(sdo['recfsdoav'])}", f"AsfaSDO = {fmt(sdo['asfasdo'])}",
        f"RecfHUav = {fmt(hu['recfhuav'])}", f"RecfHUSDOav = {fmt(hu['recfhusdoav'])}", f"AsfaHU = {fmt(hu['asfahu'])}", f"Nifrhuma = {fmt(hu['nifrhuma'])}", f"Pofrhuma = {fmt(hu['pofrhuma'])}",
        f"Recfntav = {fmt(ni['recfntav'])}", f"Recfdeav = {fmt(de['recfdeav'])}", f"Frhetero = {fmt(de['frhetero'])}",
        *arr_lines("FR",(x for row in alloc['fr'] for x in row)), *arr_lines("FRca",(x for row in alloc['frca'] for x in row)),
    ]
    return "\n".join(lines)+"\n"


def dense_native_fixture(obj: dict[str, object]) -> str:
    """Render exact-numeric TTUTIL MATERIAL v1.

    Integer dimensions remain TTUTIL INTEGER. Real-valued leaves are transported
    as TTUTIL CHARACTER tokens and converted by the ANIMO adapter's explicit
    numeric decoder. This avoids TTUTIL 4.27 VFLOAT decimal conversion, which
    can differ by one binary64 ULP from compiler list-directed REAL(8) input.
    """
    def fmt(x): return repr(float(x))
    def q(x): return "'"+fmt(x)+"'"
    def arr_lines(name, values, per_line=6):
        vals=[q(v) for v in values]; out=[]
        for i in range(0,len(vals),per_line):
            prefix=f"{name} = " if i==0 else "  "
            out.append(prefix+" ".join(vals[i:i+per_line]))
        return out
    mats=obj['materials']; fracs=obj['fractions']; alloc=obj['allocation']
    ex=obj['exudate']; dom=obj['dom']; sdo=obj['sdo']; hu=obj['humus']; ni=obj['nitrification']; de=obj['denitrification']
    nm=obj['dimensions']['Nm']; nf=obj['dimensions']['Nf']
    lines=[
        f"SchemaVersion = '{NATIVE_SCHEMA_VERSION}'", "IPO = 0", f"Nm = {nm}", f"Nf = {nf}",
        *arr_lines("Fror",(m['fror'] for m in mats)), *arr_lines("Frnh",(m['frnh'] for m in mats)), *arr_lines("Frni",(m['frni'] for m in mats)),
        f"Cfracom = {q(obj['cfracom'])}",
        *arr_lines("Recfav",(f['recfav'] for f in fracs)), *arr_lines("Hufros",(f['hufros'] for f in fracs)),
        *arr_lines("RatioRdSt",(f['ratio_rd_st'] for f in fracs)), *arr_lines("Asfa",(f['asfa'] for f in fracs)), *arr_lines("Nifr",(f['nifr'] for f in fracs)),
        f"Recfexav = {q(ex['recfexav'])}", f"Hufrosex = {q(ex['hufrosex'])}", f"Asfaex = {q(ex['asfaex'])}", f"Nifrex = {q(ex['nifrex'])}", f"Pofrex = {q(ex['pofrex'])}",
        f"Recfcaav = {q(dom['recfcaav'])}", f"SDOfr = {q(dom['sdofr'])}", f"Asfaca = {q(dom['asfaca'])}",
        f"RecfSDOav = {q(sdo['recfsdoav'])}", f"AsfaSDO = {q(sdo['asfasdo'])}",
        f"RecfHUav = {q(hu['recfhuav'])}", f"RecfHUSDOav = {q(hu['recfhusdoav'])}", f"AsfaHU = {q(hu['asfahu'])}", f"Nifrhuma = {q(hu['nifrhuma'])}", f"Pofrhuma = {q(hu['pofrhuma'])}",
        f"Recfntav = {q(ni['recfntav'])}", f"Recfdeav = {q(de['recfdeav'])}", f"Frhetero = {q(de['frhetero'])}",
        *arr_lines("FR",(x for row in alloc['fr'] for x in row)), *arr_lines("FRca",(x for row in alloc['frca'] for x in row)),
    ]
    return "\n".join(lines)+"\n"


def parse_native_material_probe_output(text: str, source_file: str = "<native-probe>") -> dict[str, object]:
    scalars: dict[str,str] = {}; arrays: dict[str,list[float]] = {}
    for lineno, raw in enumerate(text.splitlines(),1):
        if not raw.strip(): continue
        if raw.startswith("ERROR="): raise NativeMaterialSchemaError(raw.split("=",1)[1],lineno)
        if "=" not in raw: raise NativeMaterialSchemaError(f"malformed probe output {raw!r}",lineno)
        key,val=raw.split("=",1)
        if key in scalars or key in arrays: raise NativeMaterialSchemaError(f"duplicate probe output key {key!r}",lineno)
        if key.startswith("array."):
            try: arrays[key[6:]]=[float(x) for x in val.split()]
            except ValueError as exc: raise NativeMaterialSchemaError(f"invalid numeric array {key}",lineno) from exc
        else: scalars[key]=val.strip()
    if scalars.get("schema") != NORMALIZED_SCHEMA: raise NativeMaterialSchemaError("probe schema mismatch")
    if scalars.get("adapter_id") != NATIVE_ADAPTER_ID: raise NativeMaterialSchemaError("probe adapter mismatch")
    try: ipo=int(scalars["IPO"]); nm=int(scalars["Nm"]); nf=int(scalars["Nf"])
    except (KeyError,ValueError) as exc: raise NativeMaterialSchemaError("invalid probe dimensions") from exc
    if ipo != 0: raise NativeMaterialSchemaError("Pilot B native probe returned IPO != 0")
    def arr(name,n):
        a=arrays.get(name)
        if a is None or len(a)!=n: raise NativeMaterialSchemaError(f"probe array {name} count mismatch")
        return a
    def scalar(name):
        try: return float(scalars[name])
        except (KeyError,ValueError) as exc: raise NativeMaterialSchemaError(f"invalid probe scalar {name}") from exc
    fror=arr("Fror",nm); frnh=arr("Frnh",nm); frni=arr("Frni",nm)
    recfav=arr("Recfav",nf); hufros=arr("Hufros",nf); ratio=arr("RatioRdSt",nf); asfa=arr("Asfa",nf); nifr=arr("Nifr",nf)
    flat_fr=arr("FR",nm*nf); flat_frca=arr("FRca",nm*nf)
    materials=[{"mn":i+1,"fror":fror[i],"frnh":frnh[i],"frni":frni[i],"frpo":None,"frpo_presence":"FEATURE_INACTIVE_NULL"} for i in range(nm)]
    fractions=[{"frno":i+1,"recfav":recfav[i],"hufros":hufros[i],"ratio_rd_st":ratio[i],"asfa":asfa[i],"nifr":nifr[i],"pofr":None,"pofr_presence":"FEATURE_INACTIVE_NULL"} for i in range(nf)]
    fr=[flat_fr[i*nf:(i+1)*nf] for i in range(nm)]; frca=[flat_frca[i*nf:(i+1)*nf] for i in range(nm)]
    return {
        "schema": NORMALIZED_SCHEMA, "adapter_id": NATIVE_ADAPTER_ID, "source_family":"MAT", "source_file":source_file,
        "feature_context":{"IPO":ipo,"Ioptae":0,"IoptGHG":0}, "dimensions":{"Nm":nm,"Nf":nf},
        "materials":materials, "fractions":fractions, "cfracom":scalar("Cfracom"),
        "exudate":{"recfexav":scalar("Recfexav"),"hufrosex":scalar("Hufrosex"),"asfaex":scalar("Asfaex"),"nifrex":scalar("Nifrex"),"pofrex":scalar("Pofrex")},
        "dom":{"recfcaav":scalar("Recfcaav"),"sdofr":scalar("SDOfr"),"asfaca":scalar("Asfaca")},
        "sdo":{"recfsdoav":scalar("RecfSDOav"),"asfasdo":scalar("AsfaSDO")},
        "humus":{"recfhuav":scalar("RecfHUav"),"recfhusdoav":scalar("RecfHUSDOav"),"asfahu":scalar("AsfaHU"),"nifrhuma":scalar("Nifrhuma"),"pofrhuma":scalar("Pofrhuma")},
        "nitrification":{"recfntav":scalar("Recfntav")}, "denitrification":{"recfdeav":scalar("Recfdeav"),"frhetero":scalar("Frhetero")},
        "allocation":{"fr":fr,"frca":frca,"sparse_source_rows":[],"omitted_sparse_rule":"DENSE_NATIVE_EXPLICIT"},
        "conditional_inactive":{"sonicg":None,"sonic2":None,"ghg_material_extension":None},
        "legacy_lexical_residue":{},"parsed_but_unused_legacy_metadata":{},"legacy_runtime_hazards":[],
    }


def semantic_projection(obj: dict[str, object]) -> dict[str, object]:
    return {
        "schema": NORMALIZED_SCHEMA, "feature_context": obj["feature_context"], "dimensions": obj["dimensions"],
        "materials": [{k:m[k] for k in ("mn","fror","frnh","frni","frpo","frpo_presence")} for m in obj["materials"]],
        "fractions": [{k:f[k] for k in ("frno","recfav","hufros","ratio_rd_st","asfa","nifr","pofr","pofr_presence")} for f in obj["fractions"]],
        "cfracom":obj["cfracom"], "exudate":obj["exudate"], "dom":obj["dom"], "sdo":obj["sdo"],
        "humus":obj["humus"], "nitrification":obj["nitrification"], "denitrification":obj["denitrification"],
        "fr":obj["allocation"]["fr"], "frca":obj["allocation"]["frca"], "conditional_inactive":obj["conditional_inactive"],
    }


def _main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('path',type=Path); ap.add_argument('--emit-native',action='store_true')
    a=ap.parse_args(); obj=parse_legacy_material_file(a.path)
    if a.emit_native: print(dense_native_fixture(obj),end='')
    else: print(json.dumps(obj,indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(_main())
