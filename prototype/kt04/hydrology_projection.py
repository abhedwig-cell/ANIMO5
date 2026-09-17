from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Optional

from prototype.kt03.hydrology_step import (
    HydrologyAdapterError,
    HydrologyStep,
    LegacyStepProvenance,
)

HLPIMP1_ABSENT_INTERCEPTION_POLICY = "ANIMO_KT03F01_HLPIMP1_ABSENT_INTERCEPTION_V1"
EXPLICIT_INTERCEPTION_POLICY = "ANIMO_EXPLICIT_INTERCEPTION_STORAGE_V1"


@dataclass(frozen=True)
class HydroDetailedProjection:
    interception_policy_id: str
    interception_storage_end: Optional[float]
    external_inputs: dict

    def validate(self) -> None:
        if self.interception_policy_id == HLPIMP1_ABSENT_INTERCEPTION_POLICY:
            if self.interception_storage_end is not None:
                raise HydrologyAdapterError(
                    "absent-interception projection must not carry Sict"
                )
            if "Sict" in self.external_inputs:
                raise HydrologyAdapterError(
                    "absent-interception projection must not expose Sict"
                )
        elif self.interception_policy_id == EXPLICIT_INTERCEPTION_POLICY:
            if self.interception_storage_end is None:
                raise HydrologyAdapterError(
                    "explicit-interception projection requires Sict"
                )
            if self.external_inputs.get("Sict") != self.interception_storage_end:
                raise HydrologyAdapterError(
                    "explicit-interception projection Sict mismatch"
                )
        else:
            raise HydrologyAdapterError("unknown interception projection policy")


@dataclass(frozen=True)
class TopBoundaryContext:
    flab1_before_correction: float
    flab2: float
    ruso: float
    moisture_storage_rate_layer1: float
    drainage_total_layer1: float
    runinu: float
    rupr: float
    rurv: float
    ponding_start: float
    snow_storage_start: float
    flmp_hlp0: float = 0.0
    flmp_hlp1: float = 0.0
    interception_storage_start: Optional[float] = None


@dataclass(frozen=True)
class TopBoundaryResult:
    interception_delta: Optional[float]
    interception_rate: float
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


def project_typed_step(
    step: HydrologyStep, *, interception_policy_id: str
) -> HydroDetailedProjection:
    step.validate()
    external = _base_external_inputs(step)

    if interception_policy_id == HLPIMP1_ABSENT_INTERCEPTION_POLICY:
        if step.has_interception_storage_end or step.interception_storage_end is not None:
            raise HydrologyAdapterError(
                "Hlpimp=1 absent-state policy conflicts with explicit interception payload"
            )
        projection = HydroDetailedProjection(
            interception_policy_id=interception_policy_id,
            interception_storage_end=None,
            external_inputs=external,
        )
    elif interception_policy_id == EXPLICIT_INTERCEPTION_POLICY:
        if not step.has_interception_storage_end or step.interception_storage_end is None:
            raise HydrologyAdapterError(
                "explicit interception policy requires interception payload"
            )
        external = {**external, "Sict": step.interception_storage_end}
        projection = HydroDetailedProjection(
            interception_policy_id=interception_policy_id,
            interception_storage_end=step.interception_storage_end,
            external_inputs=external,
        )
    else:
        raise HydrologyAdapterError("unknown interception projection policy")

    projection.validate()
    return projection


def policy_from_legacy_provenance(
    step: HydrologyStep, provenance: LegacyStepProvenance
) -> str:
    step.validate()
    provenance.validate()
    if provenance.hlpimp == 1:
        if step.has_interception_storage_end:
            raise HydrologyAdapterError(
                "Hlpimp=1 provenance conflicts with explicit interception payload"
            )
        return HLPIMP1_ABSENT_INTERCEPTION_POLICY
    if provenance.hlpimp == 11:
        if not step.has_interception_storage_end:
            raise HydrologyAdapterError(
                "Hlpimp=11 provenance requires explicit interception payload"
            )
        return EXPLICIT_INTERCEPTION_POLICY
    raise HydrologyAdapterError("unsupported legacy interception provenance")


def project_legacy_step(
    step: HydrologyStep, provenance: LegacyStepProvenance
) -> HydroDetailedProjection:
    return project_typed_step(
        step,
        interception_policy_id=policy_from_legacy_provenance(step, provenance),
    )


def evaluate_swap3_top_boundary(
    projection: HydroDetailedProjection, context: TopBoundaryContext
) -> TopBoundaryResult:
    projection.validate()
    values = projection.external_inputs
    st = values["St"]
    if st <= 0.0:
        raise HydrologyAdapterError("non-positive timestep in projection")

    if projection.interception_policy_id == HLPIMP1_ABSENT_INTERCEPTION_POLICY:
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
    dif = context.flab1_before_correction - source_term + context.flmp_hlp0
    evso_adjusted = max(0.0, values["Evso"] - dif)
    flab1_after = (
        context.flab2
        + context.ruso
        + evso_adjusted
        + context.drainage_total_layer1
        + values["Flev"][0]
        + context.moisture_storage_rate_layer1
        + context.flmp_hlp1
    )
    return TopBoundaryResult(
        interception_delta=interception_delta,
        interception_rate=interception_rate,
        dif=dif,
        evso_adjusted=evso_adjusted,
        flab1_after_correction=flab1_after,
    )


def projection_digest(projection: HydroDetailedProjection) -> str:
    projection.validate()
    payload = {
        "interception_policy_id": projection.interception_policy_id,
        "interception_storage_end": projection.interception_storage_end,
        "external_inputs": projection.external_inputs,
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
