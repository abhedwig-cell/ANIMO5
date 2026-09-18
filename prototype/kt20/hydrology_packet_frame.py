from __future__ import annotations

from dataclasses import dataclass
import argparse
import hashlib
from pathlib import Path
import struct

from prototype.kt03.hydrology_step import (
    HydrologyStep,
    SCHEMA_ID,
    UNIT_CONTRACT_ID,
    typed_step_digest,
)
from prototype.kt19.pinned_lwkm_file_provider import (
    PinnedLWKMFileHydrologyProvider,
    decode_unpinned_powerstation_hydrology,
)

FRAME_SCHEMA = "ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1"
FRAME_ROLE = "NONPRODUCTION_ADAPTER_INTERCHANGE_NOT_CANONICAL_FORCING_ABI"

_SCALARS = (
    "producer_endpoint_day",
    "producer_step_days",
    "prr",
    "prsn",
    "prirr",
    "evicpr",
    "evicirr",
    "evsn",
    "evso",
    "evpn",
    "evsoma",
    "evtrma",
    "runon",
    "runoff",
    "groundwater_level",
    "ponding_end",
    "snow_storage_end",
    "water_balance_aeration",
)


class PacketFrameError(ValueError):
    pass


def _bits(value: float) -> str:
    return struct.pack(">d", value).hex()


def _from_bits(text: str) -> float:
    if len(text) != 16 or any(ch not in "0123456789abcdef" for ch in text):
        raise PacketFrameError(f"invalid binary64 hex identity: {text!r}")
    return struct.unpack(">d", bytes.fromhex(text))[0]


def _canonical_digest(text: str) -> bool:
    return len(text) == 64 and all(ch in "0123456789abcdef" for ch in text)


def export_hydrology_packet_frame(packet: HydrologyStep) -> str:
    """Materialize one validated immutable packet as exact binary64 identities.

    This is an adapter/test interchange only. It is deliberately not a
    production or canonical forcing ABI.
    """
    packet.validate()
    packet.require_hydro_detailed_projection()
    digest = typed_step_digest(packet)

    lines = [
        FRAME_SCHEMA,
        FRAME_ROLE,
        digest,
        packet.schema_id,
        packet.unit_contract_id,
        str(packet.layer_count),
        str(packet.drainage_count),
    ]
    lines.extend(_bits(getattr(packet, name)) for name in _SCALARS)
    lines.append("1" if packet.has_interception_storage_end else "0")
    lines.append(_bits(packet.interception_storage_end or 0.0))
    lines.append("1" if packet.has_soil_temperature else "0")

    lines.extend(_bits(value) for value in packet.sc)
    lines.extend(_bits(value) for value in packet.mofrt)
    lines.extend(_bits(value) for value in packet.flev)
    lines.extend(_bits(value) for value in packet.flab)
    for row in packet.fldr:
        lines.extend(_bits(value) for value in row)
    lines.extend(_bits(value) for value in packet.soil_temperature)
    lines.append("END_ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1")
    return "\n".join(lines) + "\n"


def parse_hydrology_packet_frame(text: str) -> HydrologyStep:
    lines = text.splitlines()
    if len(lines) < 29:
        raise PacketFrameError("truncated KT20 packet frame")
    pos = 0

    def take() -> str:
        nonlocal pos
        if pos >= len(lines):
            raise PacketFrameError("unexpected end of KT20 packet frame")
        value = lines[pos]
        pos += 1
        return value

    if take() != FRAME_SCHEMA:
        raise PacketFrameError("KT20 packet frame schema mismatch")
    if take() != FRAME_ROLE:
        raise PacketFrameError("KT20 packet frame role mismatch")
    declared_digest = take()
    if not _canonical_digest(declared_digest):
        raise PacketFrameError("invalid declared typed-step SHA-256")
    schema_id = take()
    unit_contract_id = take()
    try:
        layer_count = int(take())
        drainage_count = int(take())
    except ValueError as exc:
        raise PacketFrameError("invalid frame dimensions") from exc
    if layer_count <= 0 or drainage_count < 0:
        raise PacketFrameError("invalid frame dimensions")

    scalars = {name: _from_bits(take()) for name in _SCALARS}

    interception_flag = take()
    if interception_flag not in ("0", "1"):
        raise PacketFrameError("invalid interception availability flag")
    interception_value = _from_bits(take())

    temperature_flag = take()
    if temperature_flag not in ("0", "1"):
        raise PacketFrameError("invalid temperature availability flag")

    sc = tuple(_from_bits(take()) for _ in range(layer_count))
    mofrt = tuple(_from_bits(take()) for _ in range(layer_count))
    flev = tuple(_from_bits(take()) for _ in range(layer_count))
    flab = tuple(_from_bits(take()) for _ in range(layer_count + 1))
    fldr = tuple(
        tuple(_from_bits(take()) for _ in range(layer_count))
        for _ in range(drainage_count)
    )
    soil_temperature = (
        tuple(_from_bits(take()) for _ in range(layer_count))
        if temperature_flag == "1"
        else tuple()
    )
    if take() != "END_ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1":
        raise PacketFrameError("KT20 packet frame footer mismatch")
    if pos != len(lines):
        raise PacketFrameError("trailing KT20 packet frame content")

    packet = HydrologyStep(
        schema_id=schema_id,
        unit_contract_id=unit_contract_id,
        layer_count=layer_count,
        drainage_count=drainage_count,
        has_interception_storage_end=interception_flag == "1",
        interception_storage_end=(
            interception_value if interception_flag == "1" else None
        ),
        has_soil_temperature=temperature_flag == "1",
        sc=sc,
        mofrt=mofrt,
        flev=flev,
        flab=flab,
        fldr=fldr,
        soil_temperature=soil_temperature,
        **scalars,
    )
    packet.validate()
    packet.require_hydro_detailed_projection()
    actual_digest = typed_step_digest(packet)
    if actual_digest != declared_digest:
        raise PacketFrameError(
            f"typed-step digest mismatch: {actual_digest} != {declared_digest}"
        )
    return packet


def synthetic_commit_control_packet() -> HydrologyStep:
    n = 30
    nd = 5
    return HydrologyStep(
        schema_id=SCHEMA_ID,
        unit_contract_id=UNIT_CONTRACT_ID,
        layer_count=n,
        drainage_count=nd,
        producer_endpoint_day=1.0,
        producer_step_days=1.0,
        prr=2.0 ** -30,
        prsn=0.0,
        prirr=0.0,
        evicpr=0.0,
        evicirr=0.0,
        evsn=0.0,
        evso=0.0,
        evpn=0.0,
        evsoma=0.0,
        evtrma=0.0,
        runon=0.0,
        runoff=0.0,
        groundwater_level=1.0,
        ponding_end=0.0,
        snow_storage_end=0.0,
        water_balance_aeration=0.0,
        sc=tuple(-1.0 for _ in range(n)),
        mofrt=tuple(0.5 for _ in range(n)),
        flev=tuple(0.0 for _ in range(n)),
        flab=tuple(0.0 for _ in range(n + 1)),
        fldr=tuple(tuple(0.0 for _ in range(n)) for _ in range(nd)),
        has_interception_storage_end=True,
        interception_storage_end=0.0,
        has_soil_temperature=True,
        soil_temperature=tuple(10.0 for _ in range(n)),
    )


def write_ci_frames(real_fixture: Path, target_dir: Path) -> None:
    raw = real_fixture.read_bytes()
    _, packets, _ = decode_unpinned_powerstation_hydrology(raw)
    if len(packets) != 1:
        raise PacketFrameError("KT20 CI source fixture must contain one packet")
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "real_first_packet.frame").write_text(
        export_hydrology_packet_frame(packets[0]), encoding="ascii"
    )
    (target_dir / "synthetic_commit_control.frame").write_text(
        export_hydrology_packet_frame(synthetic_commit_control_packet()),
        encoding="ascii",
    )


def export_from_pinned_source(
    source: Path,
    target: Path,
    *,
    origin_day: int,
    endpoint_day: int,
    calendar_id: str,
    producer_day_offset: int = 0,
) -> None:
    provider = PinnedLWKMFileHydrologyProvider.from_path(
        source, calendar_id, producer_day_offset
    )
    packet = provider.select(origin_day, endpoint_day, calendar_id)
    target.write_text(export_hydrology_packet_frame(packet), encoding="ascii")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    ci = sub.add_parser("ci-frames")
    ci.add_argument("real_fixture", type=Path)
    ci.add_argument("target_dir", type=Path)

    pinned = sub.add_parser("pinned-select")
    pinned.add_argument("source", type=Path)
    pinned.add_argument("target", type=Path)
    pinned.add_argument("--origin-day", type=int, required=True)
    pinned.add_argument("--endpoint-day", type=int, required=True)
    pinned.add_argument("--calendar-id", required=True)
    pinned.add_argument("--producer-day-offset", type=int, default=0)

    args = parser.parse_args()
    if args.command == "ci-frames":
        write_ci_frames(args.real_fixture, args.target_dir)
    else:
        export_from_pinned_source(
            args.source,
            args.target,
            origin_day=args.origin_day,
            endpoint_day=args.endpoint_day,
            calendar_id=args.calendar_id,
            producer_day_offset=args.producer_day_offset,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
