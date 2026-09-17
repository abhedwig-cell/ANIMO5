from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import struct
from typing import Optional

LAYOUT_ID = "ANIMO41_SWAP3_HYDROLOGY_STEP_V1"


class HydrologyAdapterError(ValueError):
    pass


def _f32s(record: bytes, expected: int, label: str) -> tuple[float, ...]:
    if len(record) != expected * 4:
        raise HydrologyAdapterError(
            f"{label}: expected {expected * 4} bytes, got {len(record)}"
        )
    values = struct.unpack("<" + "f" * expected, record)
    if not all(math.isfinite(value) for value in values):
        raise HydrologyAdapterError(f"{label}: non-finite value")
    return values


def _i32s(record: bytes, expected: int, label: str) -> tuple[int, ...]:
    if len(record) != expected * 4:
        raise HydrologyAdapterError(
            f"{label}: expected {expected * 4} bytes, got {len(record)}"
        )
    return struct.unpack("<" + "i" * expected, record)


def legacy_dble_trunc_diagnostic(value: float) -> float:
    """Diagnostic emulation of revision-53 REAL(4)->REAL(8) normalization.

    This isolates the legacy decimal-normalization intent for adapter testing.
    It is not an independently qualified Intel/B2 compiler authority.
    """
    r4 = struct.unpack("<f", struct.pack("<f", value))[0]
    integer = math.trunc(r4)
    remainder = struct.unpack("<f", struct.pack("<f", math.fmod(r4, 1.0)))[0]
    if remainder == 0.0:
        exponent = 0
    else:
        helper = struct.unpack(
            "<f", struct.pack("<f", -math.log10(abs(remainder)))
        )[0]
        exponent = (
            math.trunc(helper - 0.9999999) if helper < 0.0 else math.trunc(helper)
        )
    scale = 10.0 ** (exponent + 7)
    return round(scale * remainder) / scale + integer


@dataclass(frozen=True)
class HydrologyStep:
    layout_id: str
    hlpimp: int
    layer_count: int
    drainage_count: int

    tiwa: float
    step_days: float

    prr: float
    prsn: float
    prirr: float
    evicpr: float
    evicirr: float
    evsn: float
    evso: float
    evpn: float
    evsoma: float
    evtrma: float
    runon: float
    runoff: float
    groundwater_level: float
    ponding_end: float
    snow_storage_end: float
    water_balance_aeration: float

    sc: tuple[float, ...]
    mofrt: tuple[float, ...]
    flev: tuple[float, ...]
    flab: tuple[float, ...]
    fldr: tuple[tuple[float, ...], ...]

    has_interception_storage_end: bool
    interception_storage_end: Optional[float]
    has_soil_temperature: bool
    soil_temperature: tuple[float, ...]

    source_record_sha256: str

    def validate(self) -> None:
        if self.layout_id != LAYOUT_ID:
            raise HydrologyAdapterError("layout identity mismatch")
        if self.hlpimp not in (1, 11):
            raise HydrologyAdapterError("unsupported hlpimp for KT03 prototype")
        if self.layer_count <= 0 or self.drainage_count < 0:
            raise HydrologyAdapterError("invalid dimensions")
        if (
            len(self.sc) != self.layer_count
            or len(self.mofrt) != self.layer_count
            or len(self.flev) != self.layer_count
        ):
            raise HydrologyAdapterError("layer-vector dimension mismatch")
        if len(self.flab) != self.layer_count + 1:
            raise HydrologyAdapterError("flab dimension mismatch")
        if len(self.fldr) != self.drainage_count or any(
            len(row) != self.layer_count for row in self.fldr
        ):
            raise HydrologyAdapterError("drainage dimension mismatch")
        if self.has_soil_temperature and len(self.soil_temperature) != self.layer_count:
            raise HydrologyAdapterError("temperature dimension mismatch")
        if not self.has_soil_temperature and self.soil_temperature:
            raise HydrologyAdapterError(
                "temperature payload present while temperature is unavailable"
            )
        if self.has_interception_storage_end != (
            self.interception_storage_end is not None
        ):
            raise HydrologyAdapterError("interception availability mismatch")

        scalars = [
            self.tiwa,
            self.step_days,
            self.prr,
            self.prsn,
            self.prirr,
            self.evicpr,
            self.evicirr,
            self.evsn,
            self.evso,
            self.evpn,
            self.evsoma,
            self.evtrma,
            self.runon,
            self.runoff,
            self.groundwater_level,
            self.ponding_end,
            self.snow_storage_end,
            self.water_balance_aeration,
        ]
        if self.interception_storage_end is not None:
            scalars.append(self.interception_storage_end)
        all_values = (
            scalars
            + list(self.sc)
            + list(self.mofrt)
            + list(self.flev)
            + list(self.flab)
            + [value for row in self.fldr for value in row]
            + list(self.soil_temperature)
        )
        if not all(math.isfinite(value) for value in all_values):
            raise HydrologyAdapterError("non-finite typed hydrology value")
        if self.step_days <= 0.0:
            raise HydrologyAdapterError("non-positive timestep")
        if len(self.source_record_sha256) != 64:
            raise HydrologyAdapterError("missing or malformed source record identity")

    def require_hydro_detailed_compatibility(self) -> None:
        """Fail closed unless every file-derived Hydro_detailed input is defined."""
        self.validate()
        if not self.has_interception_storage_end:
            raise HydrologyAdapterError(
                "Sict unavailable from this legacy layout; Hydro_detailed call must "
                "fail closed pending scientific disposition"
            )

    def hydro_detailed_boundary(self) -> dict:
        """Project the typed packet onto the file-derived Hydro_detailed seam."""
        self.require_hydro_detailed_compatibility()
        return {
            "Evicirr": self.evicirr,
            "Evicpr": self.evicpr,
            "Evpn": self.evpn,
            "Evsn": self.evsn,
            "Evso": self.evso,
            "Evsoma": self.evsoma,
            "Evtrma": self.evtrma,
            "Flab": self.flab,
            "Fldr": self.fldr,
            "Flev": self.flev,
            "Mofrt": self.mofrt,
            "Pnt": self.ponding_end,
            "Prirr": self.prirr,
            "Prr": self.prr,
            "Prsn": self.prsn,
            "Ru": self.runoff,
            "Runon": self.runon,
            "Sict": self.interception_storage_end,
            "Snt": self.snow_storage_end,
            "St": self.step_days,
        }


def parse_swap3_static(records: list[bytes]) -> dict:
    if len(records) < 17:
        raise HydrologyAdapterError("insufficient SWAP3 records")

    headers = [record.decode("ascii", errors="strict") for record in records[:5]]
    if not all(header.startswith("*") for header in headers):
        raise HydrologyAdapterError("unexpected SWAP3 textual header")

    (hlpimp,) = _i32s(records[5], 1, "hlpimp")
    if len(records[6]) != 16:
        raise HydrologyAdapterError("hydrology period record has wrong size")
    start_year, end_year = struct.unpack("<ii", records[6][:8])
    start_time, end_time = _f32s(records[6][8:], 2, "hydrology period")
    layer_count, horizon_count, drainage_count = _i32s(
        records[7], 3, "dimensions"
    )

    if hlpimp not in (1, 11):
        raise HydrologyAdapterError(
            "KT03 parser currently supports only the observed Hlpimp=1/11 SWAP3 layouts"
        )
    if layer_count <= 0 or horizon_count <= 0 or drainage_count < 0:
        raise HydrologyAdapterError("invalid static dimensions")

    _i32s(records[8], horizon_count, "horizon lower-layer map")
    _f32s(records[9], horizon_count, "saturation moisture")
    _f32s(records[10], horizon_count, "field-capacity moisture")
    _f32s(records[11], horizon_count, "wilting moisture")
    layer_thickness = _f32s(records[12], layer_count, "layer thickness")
    initial_moisture = _f32s(records[13], layer_count, "initial moisture")
    initial_surface = _f32s(
        records[14],
        3 if hlpimp == 11 else 2,
        "initial groundwater/interception/ponding",
    )
    _f32s(records[15], 1, "initial snow storage")
    initial_temperature = _f32s(
        records[16], layer_count, "initial producer temperature"
    )
    has_soil_temperature = abs(initial_temperature[0] - (-99.9)) > 1.0e-4

    return {
        "headers": headers,
        "hlpimp": hlpimp,
        "start_year": start_year,
        "end_year": end_year,
        "start_time": start_time,
        "end_time": end_time,
        "nl": layer_count,
        "nh": horizon_count,
        "nudr": drainage_count,
        "layer_thickness": layer_thickness,
        "initial_moisture": initial_moisture,
        "initial_interception_storage_present": hlpimp == 11,
        "initial_surface_record": initial_surface,
        "ioptte": has_soil_temperature,
        "dynamic_start": 17,
    }


def parse_dynamic_step(
    records: list[bytes],
    index: int,
    static: dict,
    *,
    expected_layout_id: str = LAYOUT_ID,
    profile_bottom: float | None = None,
) -> HydrologyStep:
    layer_count = static["nl"]
    drainage_count = static["nudr"]
    hlpimp = static["hlpimp"]
    records_per_step = 8 + drainage_count
    start = static["dynamic_start"] + index * records_per_step
    end = start + records_per_step
    if end > len(records):
        raise HydrologyAdapterError("incomplete dynamic timestep record group")

    group = records[start:end]
    first = _f32s(
        group[0], 19 if hlpimp == 11 else 18, "dynamic surface record"
    )
    if hlpimp == 11:
        (
            tiwa,
            step_days,
            prr,
            prsn,
            prirr,
            evicpr,
            evicirr,
            evsn,
            evso,
            evpn,
            evsoma,
            evtrma,
            runon,
            runoff,
            groundwater_level,
            interception_storage_end,
            ponding_end,
            snow_storage_end,
            water_balance_aeration,
        ) = first
        has_interception_storage_end = True
    else:
        (
            tiwa,
            step_days,
            prr,
            prsn,
            prirr,
            evicpr,
            evicirr,
            evsn,
            evso,
            evpn,
            evsoma,
            evtrma,
            runon,
            runoff,
            groundwater_level,
            ponding_end,
            snow_storage_end,
            water_balance_aeration,
        ) = first
        interception_storage_end = None
        has_interception_storage_end = False

    sc = _f32s(group[1], layer_count, "Sc")
    mofrt = _f32s(group[2], layer_count, "Mofrt")
    flev = _f32s(group[3], layer_count, "Flev")
    flab = _f32s(group[4], layer_count + 1, "Flab")

    drainage_rows = []
    position = 5
    for drainage_index in range(drainage_count):
        drainage_rows.append(
            _f32s(
                group[position],
                layer_count,
                f"Fldr[{drainage_index + 1}]",
            )
        )
        position += 1

    # These two records are read by Input_hydro but only populate local variables.
    # They are validated for framing/completeness but are not part of the typed
    # output contract delivered to Hydro_detailed.
    _f32s(group[position], 4, "local producer crop/weather")
    position += 1
    _f32s(group[position], 1, "local average date")
    position += 1

    temperature_record = _f32s(
        group[position], layer_count, "producer temperature/dummy"
    )
    position += 1
    if position != len(group):
        raise HydrologyAdapterError("unexpected dynamic record count")

    if groundwater_level < -9.98:
        if profile_bottom is None or not math.isfinite(profile_bottom):
            raise HydrologyAdapterError(
                "groundwater sentinel requires explicit profile_bottom normalization input"
            )
        groundwater_level = profile_bottom

    normalize = legacy_dble_trunc_diagnostic
    step = HydrologyStep(
        layout_id=expected_layout_id,
        hlpimp=hlpimp,
        layer_count=layer_count,
        drainage_count=drainage_count,
        tiwa=normalize(tiwa),
        step_days=normalize(step_days),
        prr=normalize(prr),
        prsn=normalize(prsn),
        prirr=normalize(prirr),
        evicpr=normalize(evicpr),
        evicirr=normalize(evicirr),
        evsn=normalize(evsn),
        evso=normalize(evso),
        evpn=normalize(evpn),
        evsoma=normalize(evsoma),
        evtrma=normalize(evtrma),
        runon=normalize(runon),
        runoff=normalize(runoff),
        groundwater_level=normalize(groundwater_level),
        ponding_end=normalize(ponding_end),
        snow_storage_end=normalize(snow_storage_end),
        water_balance_aeration=normalize(water_balance_aeration),
        sc=tuple(map(normalize, sc)),
        mofrt=tuple(map(normalize, mofrt)),
        flev=tuple(map(normalize, flev)),
        flab=tuple(map(normalize, flab)),
        fldr=tuple(tuple(map(normalize, row)) for row in drainage_rows),
        has_interception_storage_end=has_interception_storage_end,
        interception_storage_end=(
            normalize(interception_storage_end)
            if interception_storage_end is not None
            else None
        ),
        has_soil_temperature=bool(static["ioptte"]),
        soil_temperature=(
            tuple(map(normalize, temperature_record)) if static["ioptte"] else tuple()
        ),
        source_record_sha256=hashlib.sha256(b"".join(group)).hexdigest(),
    )
    step.validate()
    return step


def typed_step_digest(step: HydrologyStep) -> str:
    payload = json.dumps(
        step.__dict__, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
