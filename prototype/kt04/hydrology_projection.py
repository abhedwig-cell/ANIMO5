from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Optional

from prototype.kt03.hydrology_step import (
    HydrologyAdapterError,
    HydrologyStep,
    LegacyStepProvenance,
)

HLPIMP1_ABSENT_INTERCEPTION_POLICY = "ANIMO_KT03F01_HLPIMP1_ABSENT_INTERCEPTION_V1"
EXPLICIT_INTERCEPTION_POLICY = "ANIMO_EXPLICIT_INTERCEPTION_STORAGE_V1"

KT03F01_HLPIMP1_AUTHORITY_ID = (
    "ANIMO-KT03F01@0bd8e3f2fe84837e85c45c44ec2e8201f81cef12"
)
KT03_EXPLICIT_INTERCEPTION_AUTHORITY_ID = (
    "ANIMO-KT03@e844c7658a95819fc0463c55737f9bd41b29a6da"
)

BASE_EXTERNAL_FIELDS = frozenset(
    {
        "Evicirr",
        "Evicpr",
        "Evpn",
        "Evsn",
        "Evso",
        "Evsoma",
        "Evtrma",
        "Flab",
        "Fldr",
        "Flev",
        "Mofrt",
        "Pnt",
        "Prirr",
        "Prr",
        "Prsn",
        "Ru",
        "Runon",
        "Snt",
        "St",
    }
)


@dataclass(frozen=True)
class ProjectionAuthority:
    authority_id: str
    interception_policy_id: str

    def validate(self) -> None:
        allowed = {
            (
                KT03F01_HLPIMP1_AUTHORITY_ID,
                HLPIMP1_ABSENT_INTERCEPTION_POLICY,
            ),
            (
                KT03_EXPLICIT_INTERCEPTION_AUTHORITY_ID,
                EXPLICIT_INTERCEPTION_POLICY,
            ),
        }
        if (self.authority_id, self.interception_policy_id) not in allowed:
            raise HydrologyAdapterError("unqualified hydrology projection authority")


HLPIMP1_AUTHORITY = ProjectionAuthority(
    KT03F01_HLPIMP1_AUTHORITY_ID,
    HLPIMP1_ABSENT_INTERCEPTION_POLICY,
)
EXPLICIT_INTERCEPTION_AUTHORITY = ProjectionAuthority(
    KT03_EXPLICIT_INTERCEPTION_AUTHORITY_ID,
    EXPLICIT_INTERCEPTION_POLICY,
)


def _validate_numeric_value(value: object, label: str) -> None:
    if isinstance(value, bool):
        raise HydrologyAdapterError(f"{label}: boolean is not a hydrology number")
    if isinstance(value, (int, float)):
        if not math.isfinite(float(value)):
            raise HydrologyAdapterError(f"{label}: non-finite value")
        return
    if isinstance(value, tuple):
        for index, item in enumerate(value):
            _validate_numeric_value(item, f"{label}[{index}]")
        return
    raise HydrologyAdapterError(f"{label}: unsupported projection value type")


def _validate_projection_shapes(values: dict) -> None:
    mofrt = values["Mofrt"]
    flev = values["Flev"]
    flab = values["Flab"]
    fldr = values["Fldr"]
    if not all(isinstance(value, tuple) for value in (mofrt, flev, flab, fldr)):
        raise HydrologyAdapterError("projection profile fields must be immutable tuples")
    layer_count = len(mofrt)
    if layer_count <= 0:
        raise HydrologyAdapterError("projection has no soil layers")
    if len(flev) != layer_count:
        raise HydrologyAdapterError("projection Flev layer dimension mismatch")
    if len(flab) != layer_count + 1:
        raise HydrologyAdapterError("projection Flab interface dimension mismatch")
    if any(not isinstance(row, tuple) or len(row) != layer_count for row in fldr):
        raise HydrologyAdapterError("projection Fldr layer dimension mismatch")


@dataclass(frozen=True)
class HydroDetailedProjection:
    authority: ProjectionAuthority
    interception_storage_end: Optional[float]
    external_inputs: tuple[tuple[str, object], ...]

    def as_dict(self) -> dict:
        return dict(self.external_inputs)

    def validate(self) -> None:
        self.authority.validate()
        values = self.as_dict()
        if len(values) != len(self.external_inputs):
            raise HydrologyAdapterError("duplicate external projection field")

        expected_fields = set(BASE_EXTERNAL_FIELDS)
        if self.authority.interception_policy_id == HLPIMP1_ABSENT_INTERCEPTION_POLICY:
            if self.interception_storage_end is not None:
                raise HydrologyAdapterError(
                    "absent-interception projection must not carry Sict"
                )
            if "Sict" in values:
                raise HydrologyAdapterError(
                    "absent-interception projection must not expose Sict"
                )
        elif self.authority.interception_policy_id == EXPLICIT_INTERCEPTION_POLICY:
            expected_fields.add("Sict")
            if self.interception_storage_end is None:
                raise HydrologyAdapterError(
                    "explicit-interception projection requires Sict"
                )
            if values.get("Sict") != self.interception_storage_end:
                raise HydrologyAdapterError(
                    "explicit-interception projection Sict mismatch"
                )
        else:
            raise HydrologyAdapterError("unknown interception projection policy")

        if set(values) != expected_fields:
            missing = sorted(expected_fields - set(values))
            extra = sorted(set(values) - expected_fields)
            raise HydrologyAdapterError(
                f"external projection field set mismatch: missing={missing}, extra={extra}"
            )
        for key, value in values.items():
            _validate_numeric_value(value, key)
        _validate_projection_shapes(values)


@dataclass(frozen=True)
class TopBoundaryContext:
    ruso: float
    moisture_storage_rate_layer1: float
    runinu: float
    rupr: float
    rurv: float
    ponding_start: float
    snow_storage_start: float
    flmp_hlp0: float = 0.0
    flmp_hlp1: float = 0.0
    interception_storage_start: Optional[float] = None

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if value is None:
                continue
            _validate_numeric_value(value, f"context.{name}")


@dataclass(frozen=True)
class TopBoundaryResult:
    interception_delta: Optional[float]
    interception_rate: float
    preliminary_flab1: float
    drainage_total_layer1: float
    dif: float
    evso_adjusted: float
    flab1_after_correction: float


def _base_external_inputs(step: HydrologyStep) -> dict:
    return {
        "Evicirr": step.evicirr,
        "Evicpr": step.evicpr,
        "Evpn": step.evpn,
        "Evsn": step.evsn,
        "Evso": step.evso,
        "Evsoma": step.evsoma,
        "Evtrma": step.evtrma,
        "Flab": step.flab,
        "Fldr": step.fldr,
        "Flev": step.flev,
        "Mofrt": step.mofrt,
        "Pnt": step.ponding_end,
        "Prirr": step.prirr,
        "Prr": step.prr,
        "Prsn": step.prsn,
        "Ru": step.runoff,
        "Runon": step.runon,
        "Snt": step.snow_storage_end,
        "St": step.producer_step_days,
    }


def _freeze_external_inputs(values: dict) -> tuple[tuple[str, object], ...]:
    return tuple(sorted(values.items(), key=lambda item: item[0]))


def project_typed_step(
    step: HydrologyStep, *, authority: ProjectionAuthority
) -> HydroDetailedProjection:
    step.validate()
    authority.validate()
    external = _base_external_inputs(step)

    if authority.interception_policy_id == HLPIMP1_ABSENT_INTERCEPTION_POLICY:
        if step.has_interception_storage_end or step.interception_storage_end is not None:
            raise HydrologyAdapterError(
                "Hlpimp=1 absent-state policy conflicts with explicit interception payload"
            )
        projection = HydroDetailedProjection(
            authority=authority,
            interception_storage_end=None,
            external_inputs=_freeze_external_inputs(external),
        )
    elif authority.interception_policy_id == EXPLICIT_INTERCEPTION_POLICY:
        if not step.has_interception_storage_end or step.interception_storage_end is None:
            raise HydrologyAdapterError(
                "explicit interception policy requires interception payload"
            )
        external = {**external, "Sict": step.interception_storage_end}
        projection = HydroDetailedProjection(
            authority=authority,
            interception_storage_end=step.interception_storage_end,
            external_inputs=_freeze_external_inputs(external),
        )
    else:
        raise HydrologyAdapterError("unknown interception projection policy")

    projection.validate()
    return projection


def authority_from_legacy_provenance(
    step: HydrologyStep, provenance: LegacyStepProvenance
) -> ProjectionAuthority:
    step.validate()
    provenance.validate()
    if provenance.hlpimp == 1:
        if step.has_interception_storage_end:
            raise HydrologyAdapterError(
                "Hlpimp=1 provenance conflicts with explicit interception payload"
            )
        return HLPIMP1_AUTHORITY
    if provenance.hlpimp == 11:
        if not step.has_interception_storage_end:
            raise HydrologyAdapterError(
                "Hlpimp=11 provenance requires explicit interception payload"
            )
        return EXPLICIT_INTERCEPTION_AUTHORITY
    raise HydrologyAdapterError("unsupported legacy interception provenance")


def project_legacy_step(
    step: HydrologyStep, provenance: LegacyStepProvenance
) -> HydroDetailedProjection:
    return project_typed_step(
        step,
        authority=authority_from_legacy_provenance(step, provenance),
    )


def _validate_runoff_split(values: dict, context: TopBoundaryContext) -> None:
    runoff = values["Ru"]
    tolerance = 1.0e-12 * max(1.0, abs(runoff))
    if runoff < 0.0:
        if abs(context.runinu + runoff) > tolerance:
            raise HydrologyAdapterError("negative-runoff Runinu closure mismatch")
        if max(abs(context.rupr), abs(context.rurv), abs(context.ruso)) > tolerance:
            raise HydrologyAdapterError("negative-runoff split must be zero")
    else:
        if abs(context.runinu) > tolerance:
            raise HydrologyAdapterError("nonnegative-runoff Runinu must be zero")
        if abs((context.rupr + context.rurv + context.ruso) - runoff) > tolerance:
            raise HydrologyAdapterError("runoff split closure mismatch")


def evaluate_swap3_top_boundary(
    projection: HydroDetailedProjection, context: TopBoundaryContext
) -> TopBoundaryResult:
    projection.validate()
    context.validate()
    values = projection.as_dict()
    st = values["St"]
    if st <= 0.0:
        raise HydrologyAdapterError("non-positive timestep in projection")
    _validate_runoff_split(values, context)

    if projection.authority.interception_policy_id == HLPIMP1_ABSENT_INTERCEPTION_POLICY:
        if context.interception_storage_start is not None:
            raise HydrologyAdapterError(
                "absent-state policy must not receive an interception start state"
            )
        interception_delta = None
        interception_rate = 0.0
    else:
        if context.interception_storage_start is None:
            raise HydrologyAdapterError(
                "explicit interception policy requires interception start state"
            )
        interception_delta = (
            projection.interception_storage_end - context.interception_storage_start
        )
        interception_rate = interception_delta / st

    drainage_total_layer1 = sum(row[0] for row in values["Fldr"])
    flab2 = values["Flab"][1]
    preliminary_flab1 = (
        flab2
        + context.ruso
        + values["Evso"]
        + context.moisture_storage_rate_layer1
        + drainage_total_layer1
        + values["Flev"][0]
        + context.flmp_hlp1
    )

    source_term = (
        values["Prr"]
        - values["Evicpr"]
        + values["Prirr"]
        - values["Evicirr"]
        - interception_rate
        + values["Prsn"]
        - values["Evsn"]
        - (values["Snt"] - context.snow_storage_start) / st
        - values["Evpn"]
        - (values["Pnt"] - context.ponding_start) / st
        + values["Runon"]
        + context.runinu
        - context.rupr
        - context.rurv
    )
    dif = preliminary_flab1 - source_term + context.flmp_hlp0
    evso_adjusted = max(0.0, values["Evso"] - dif)
    flab1_after = (
        flab2
        + context.ruso
        + evso_adjusted
        + drainage_total_layer1
        + values["Flev"][0]
        + context.moisture_storage_rate_layer1
        + context.flmp_hlp1
    )
    return TopBoundaryResult(
        interception_delta=interception_delta,
        interception_rate=interception_rate,
        preliminary_flab1=preliminary_flab1,
        drainage_total_layer1=drainage_total_layer1,
        dif=dif,
        evso_adjusted=evso_adjusted,
        flab1_after_correction=flab1_after,
    )


def projection_digest(projection: HydroDetailedProjection) -> str:
    projection.validate()
    payload = {
        "authority_id": projection.authority.authority_id,
        "interception_policy_id": projection.authority.interception_policy_id,
        "interception_storage_end": projection.interception_storage_end,
        "external_inputs": projection.as_dict(),
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
