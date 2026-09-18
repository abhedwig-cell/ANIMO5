from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
from typing import Iterable

from prototype.kt03.hydrology_step import (
    HydrologyStep,
    legacy_dble_trunc_diagnostic,
    typed_step_digest,
)
from prototype.kt19.pinned_lwkm_file_provider import PinnedLWKMFileHydrologyProvider

REV53_PONDING_THRESHOLD = 1.0e-4
REV53_RUNOFF_NEAR_ZERO = 1.0e-8
TCD042_FLUX_THRESHOLD = 1.0e-8
TCD042_P_MAX = 3.8510200002999744e-7

CLASS_BLOCKED_RUNINU = "BLOCKED_FIRST_CALL_RUNINU"
CLASS_PONDING = "PONDING_OUTSIDE_TCD042"
CLASS_EXACT_ZERO = "TCD042_B1_EXACT_ZERO_HYDROLOGY"
CLASS_E1 = "TCD042_E1_HYDROLOGY_ENVELOPE"
CLASS_OUTSIDE = "TCD042_HYDROLOGY_OUTSIDE_ADMITTED_SCOPE"
CLASS_SINGULAR = "REV53_RUNOFF_PARTITION_SINGULARITY"


@dataclass(frozen=True)
class EnvelopeConfig:
    he_top: float
    lefrrv: float
    lefrso: float


@dataclass(frozen=True)
class PacketEnvelopeResult:
    index: int
    endpoint_day: float
    step_days: float
    typed_step_sha256: str
    classification: str
    runinu_known: bool
    runinu: float | None
    flpn: int | None
    flux: float | None
    p: float | None


@dataclass(frozen=True)
class EnvelopeSummary:
    packet_count: int
    blocked_first_call_runinu: int
    deterministic_packet_count: int
    ponding_count: int
    exact_zero_count: int
    e1_count: int
    outside_count: int
    singular_count: int
    first_runinu_reset_index: int | None
    first_runinu_reset_endpoint_day: float | None
    first_exact_zero_index: int | None
    first_e1_index: int | None


def _validate_config(config: EnvelopeConfig) -> None:
    if config.he_top <= 0.0:
        raise ValueError("he_top must be positive")
    if not (0.0 <= config.lefrrv <= 1.0):
        raise ValueError("lefrrv outside bounded fraction range")
    if not (0.0 <= config.lefrso <= 1.0):
        raise ValueError("lefrso outside bounded fraction range")


def characterize_packets(
    packets: Iterable[HydrologyStep],
    *,
    initial_pn: float,
    initial_sic: float,
    initial_snla: float,
    initial_mofro: tuple[float, ...],
    config: EnvelopeConfig,
) -> tuple[EnvelopeSummary, tuple[PacketEnvelopeResult, ...]]:
    """Diagnostic B1 characterization of the frozen bounded hydrology algebra.

    The function intentionally starts with Runinu unknown. The revision-53
    near-zero runoff branch preserves call-entry Runinu and therefore cannot be
    classified deterministically until a later source branch assigns Runinu.
    """
    _validate_config(config)
    materialized = tuple(packets)
    if not materialized:
        raise ValueError("empty packet sequence")
    if len(initial_mofro) != materialized[0].layer_count:
        raise ValueError("initial Mofro extent mismatch")

    pn = initial_pn
    sic = initial_sic
    snla = initial_snla
    mofro = tuple(initial_mofro)
    runinu_known = False
    runinu = None
    first_reset_index = None
    first_reset_endpoint = None

    out: list[PacketEnvelopeResult] = []

    for index, packet in enumerate(materialized):
        packet.validate()
        packet.require_hydro_detailed_projection()
        if packet.layer_count != len(mofro):
            raise ValueError(f"packet[{index}] layer count changed")
        if packet.interception_storage_end is None:
            raise ValueError(f"packet[{index}] missing Sict")

        ru = packet.runoff
        rupr = 0.0
        rurv = 0.0
        ruso = 0.0
        singular = False

        if ru < 0.0:
            runinu = -ru
            runinu_known = True
            if first_reset_index is None:
                first_reset_index = index
                first_reset_endpoint = packet.producer_endpoint_day
        elif -REV53_RUNOFF_NEAR_ZERO < ru < REV53_RUNOFF_NEAR_ZERO:
            pass
        else:
            runinu = 0.0
            runinu_known = True
            if first_reset_index is None:
                first_reset_index = index
                first_reset_endpoint = packet.producer_endpoint_day
            rupr = (1.0 - config.lefrrv) * ru
            rurv = (1.0 - config.lefrso) * config.lefrrv * ru
            ruso = config.lefrso * config.lefrrv * ru
            denom = rupr + ruso
            if denom == 0.0:
                singular = True
            else:
                rupr = min(rupr + rurv * rupr / denom, packet.prr)
                rurv = 0.0
                ruso = ru - rupr

        flpn = (
            0
            if (
                packet.ponding_end + packet.snow_storage_end <= REV53_PONDING_THRESHOLD
                and pn + snla <= REV53_PONDING_THRESHOLD
            )
            else 1
        )

        flux = None
        p = None
        if singular:
            classification = CLASS_SINGULAR
        elif not runinu_known:
            classification = CLASS_BLOCKED_RUNINU
        elif flpn != 0:
            classification = CLASS_PONDING
        else:
            st = packet.producer_step_days
            fl_dr_to1 = sum(row[0] for row in packet.fldr)
            provisional_flab_top = (
                packet.flab[1]
                + ruso
                + packet.evso
                + (packet.mofrt[0] - mofro[0]) * config.he_top / st
                + fl_dr_to1
                + packet.flev[0]
            )
            dif = provisional_flab_top - (
                packet.prr
                - packet.evicpr
                + packet.prirr
                - packet.evicirr
                - (packet.interception_storage_end - sic) / st
                + packet.prsn
                - packet.evsn
                - (packet.snow_storage_end - snla) / st
                - packet.evpn
                - (packet.ponding_end - pn) / st
                + packet.runon
                + float(runinu)
                - rupr
                - rurv
            )
            evso_resolved = max(0.0, packet.evso - dif)
            flab_top = (
                packet.flab[1]
                + ruso
                + evso_resolved
                + fl_dr_to1
                + packet.flev[0]
                + (packet.mofrt[0] - mofro[0]) * config.he_top / st
            )
            flux = max(0.0, flab_top)
            p = st * flux / config.he_top
            if flux == 0.0:
                classification = CLASS_EXACT_ZERO
            elif flux < TCD042_FLUX_THRESHOLD and p <= TCD042_P_MAX:
                classification = CLASS_E1
            else:
                classification = CLASS_OUTSIDE

        out.append(
            PacketEnvelopeResult(
                index=index,
                endpoint_day=packet.producer_endpoint_day,
                step_days=packet.producer_step_days,
                typed_step_sha256=typed_step_digest(packet),
                classification=classification,
                runinu_known=runinu_known,
                runinu=runinu if runinu_known else None,
                flpn=flpn if runinu_known else None,
                flux=flux,
                p=p,
            )
        )

        # Exact revision-53 accepted endpoint -> next-origin transfer used by
        # the bounded characterization. Runinu remains separately persistent.
        pn = packet.ponding_end
        sic = packet.interception_storage_end
        snla = packet.snow_storage_end
        mofro = packet.mofrt

    def count(label: str) -> int:
        return sum(item.classification == label for item in out)

    deterministic = len(out) - count(CLASS_BLOCKED_RUNINU)
    first_zero = next((x.index for x in out if x.classification == CLASS_EXACT_ZERO), None)
    first_e1 = next((x.index for x in out if x.classification == CLASS_E1), None)

    summary = EnvelopeSummary(
        packet_count=len(out),
        blocked_first_call_runinu=count(CLASS_BLOCKED_RUNINU),
        deterministic_packet_count=deterministic,
        ponding_count=count(CLASS_PONDING),
        exact_zero_count=count(CLASS_EXACT_ZERO),
        e1_count=count(CLASS_E1),
        outside_count=count(CLASS_OUTSIDE),
        singular_count=count(CLASS_SINGULAR),
        first_runinu_reset_index=first_reset_index,
        first_runinu_reset_endpoint_day=first_reset_endpoint,
        first_exact_zero_index=first_zero,
        first_e1_index=first_e1,
    )
    return summary, tuple(out)


def characterize_pinned_lwkm(
    source: Path,
    *,
    he_top: float,
    lefrrv: float,
    lefrso: float,
    initial_snla: float = 0.0,
) -> tuple[EnvelopeSummary, tuple[PacketEnvelopeResult, ...]]:
    provider = PinnedLWKMFileHydrologyProvider.from_path(
        source, "ANIMO_PG_86400_NOLEAPSECONDS_V1", 0
    )
    static = provider.static_metadata
    initial_surface = static["initial_surface_record"]
    initial_mofro = tuple(
        legacy_dble_trunc_diagnostic(value) for value in static["initial_moisture"]
    )
    initial_pn = legacy_dble_trunc_diagnostic(initial_surface[2])
    initial_sic = legacy_dble_trunc_diagnostic(initial_surface[1])
    packets = tuple(provider._packets)  # bounded diagnostic on already-validated immutable tuple
    return characterize_packets(
        packets,
        initial_pn=initial_pn,
        initial_sic=initial_sic,
        initial_snla=legacy_dble_trunc_diagnostic(initial_snla),
        initial_mofro=initial_mofro,
        config=EnvelopeConfig(he_top=he_top, lefrrv=lefrrv, lefrso=lefrso),
    )


def summary_json(summary: EnvelopeSummary, results: tuple[PacketEnvelopeResult, ...]) -> dict:
    anchors = {}
    for label in (CLASS_BLOCKED_RUNINU, CLASS_OUTSIDE, CLASS_EXACT_ZERO, CLASS_E1, CLASS_PONDING):
        item = next((x for x in results if x.classification == label), None)
        if item is not None:
            anchors[label] = item.__dict__
    return {"summary": summary.__dict__, "first_classification_anchors": anchors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--he-top", type=float, required=True)
    parser.add_argument("--lefrrv", type=float, required=True)
    parser.add_argument("--lefrso", type=float, required=True)
    parser.add_argument("--initial-snla", type=float, default=0.0)
    args = parser.parse_args()

    summary, results = characterize_pinned_lwkm(
        args.source,
        he_top=args.he_top,
        lefrrv=args.lefrrv,
        lefrso=args.lefrso,
        initial_snla=args.initial_snla,
    )
    args.target.write_text(
        json.dumps(summary_json(summary, results), indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
