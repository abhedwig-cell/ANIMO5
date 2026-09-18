from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
from typing import Iterable

from tools.convert_legacy_unformatted import parse_powerstation_records
from prototype.kt03.hydrology_step import (
    HydrologyAdapterError,
    HydrologyStep,
    legacy_step_provenance,
    parse_dynamic_step,
    parse_swap3_static,
    typed_step_digest,
)

EXPECTED_SOURCE_SHA256 = "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c"
EXPECTED_PACKET_COUNT = 1800
EXPECTED_TYPED_SEQUENCE_SHA256 = "c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4"
EXPECTED_GROUP_SEQUENCE_SHA256 = "40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34"
EXPECTED_RECORD_SEQUENCE_SHA256 = "eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1"
MAX_EXACT_REAL64_INTEGER = 9007199254740991


class PinnedProviderError(ValueError):
    pass


def _sequence_sha256(values: Iterable[str]) -> str:
    payload = "\n".join(values) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def _exact_nonnegative_integer(value: float, label: str) -> int:
    if not math.isfinite(value):
        raise PinnedProviderError(f"{label}: non-finite value")
    if value < 0.0 or value > float(MAX_EXACT_REAL64_INTEGER):
        raise PinnedProviderError(f"{label}: outside exact integer envelope")
    integer = round(value)
    if float(integer) != value:
        raise PinnedProviderError(f"{label}: non-integer producer coordinate")
    return int(integer)


@dataclass(frozen=True)
class ProviderIdentity:
    source_sha256: str
    packet_count: int
    logical_record_count: int
    physical_block_count: int
    typed_step_digest_sequence_sha256: str
    dynamic_group_digest_sequence_sha256: str
    temporal_and_digest_record_sequence_sha256: str


class ImmutableHydrologyPacketProvider:
    """Read-only exact whole-day packet selection.

    This is an adapter/provider responsibility only. It owns no accepted ANIMO
    state, retry policy or scientific process semantics.
    """

    def __init__(
        self,
        packets: Iterable[HydrologyStep],
        runtime_calendar_contract_id: str,
        producer_day_offset: int = 0,
    ) -> None:
        if not runtime_calendar_contract_id.strip():
            raise PinnedProviderError("missing runtime calendar contract id")
        if producer_day_offset < 0:
            raise PinnedProviderError("negative producer day offset")

        materialized = tuple(packets)
        if not materialized:
            raise PinnedProviderError("empty hydrology packet provider")

        index: dict[tuple[int, int], int] = {}
        previous_endpoint: int | None = None
        for i, packet in enumerate(materialized):
            packet.validate()
            packet.require_hydro_detailed_projection()
            endpoint = _exact_nonnegative_integer(
                packet.producer_endpoint_day, f"packet[{i}].endpoint"
            )
            step = _exact_nonnegative_integer(
                packet.producer_step_days, f"packet[{i}].step"
            )
            if step <= 0:
                raise PinnedProviderError(f"packet[{i}]: non-positive producer step")
            origin = endpoint - step
            if origin < 0:
                raise PinnedProviderError(f"packet[{i}]: negative producer origin")
            if previous_endpoint is not None and origin != previous_endpoint:
                raise PinnedProviderError(
                    f"packet[{i}]: producer chain discontinuity "
                    f"{origin} != {previous_endpoint}"
                )
            previous_endpoint = endpoint
            key = (endpoint, step)
            if key in index:
                raise PinnedProviderError(f"duplicate producer interval key {key}")
            index[key] = i

        self._packets = materialized
        self._index = index
        self._runtime_calendar_contract_id = runtime_calendar_contract_id.strip()
        self._producer_day_offset = producer_day_offset

    @property
    def packet_count(self) -> int:
        return len(self._packets)

    @property
    def runtime_calendar_contract_id(self) -> str:
        return self._runtime_calendar_contract_id

    @property
    def producer_day_offset(self) -> int:
        return self._producer_day_offset

    def select(
        self,
        origin_day: int,
        endpoint_day: int,
        runtime_calendar_contract_id: str,
    ) -> HydrologyStep:
        if runtime_calendar_contract_id != self._runtime_calendar_contract_id:
            raise PinnedProviderError("runtime calendar binding mismatch")
        if isinstance(origin_day, bool) or isinstance(endpoint_day, bool):
            raise PinnedProviderError("boolean runtime coordinate is invalid")
        if not isinstance(origin_day, int) or not isinstance(endpoint_day, int):
            raise PinnedProviderError("runtime coordinates must be exact integers")
        if origin_day < 0 or endpoint_day <= origin_day:
            raise PinnedProviderError("invalid runtime interval")

        step = endpoint_day - origin_day
        expected_endpoint = endpoint_day + self._producer_day_offset
        if expected_endpoint > MAX_EXACT_REAL64_INTEGER:
            raise PinnedProviderError("producer time mapping overflow")

        index = self._index.get((expected_endpoint, step))
        if index is None:
            raise PinnedProviderError("hydrology packet not found")
        return self._packets[index]


def decode_unpinned_powerstation_hydrology(raw: bytes) -> tuple[dict, tuple[HydrologyStep, ...], int]:
    """Decode a bounded SWAP3 PowerStation byte stream through the frozen KT03 adapter.

    This helper is intentionally unpinned. Callers that need the qualified LWKM
    source identity must use PinnedLWKMFileHydrologyProvider.
    """
    try:
        records, physical_blocks = parse_powerstation_records(raw)
        static = parse_swap3_static(records)
    except (ValueError, HydrologyAdapterError) as exc:
        raise PinnedProviderError(str(exc)) from exc

    records_per_step = 8 + static["nudr"]
    dynamic_count = len(records) - static["dynamic_start"]
    if dynamic_count < 0 or dynamic_count % records_per_step != 0:
        raise PinnedProviderError("dynamic logical-record count is not step-aligned")
    packet_count = dynamic_count // records_per_step
    if packet_count <= 0:
        raise PinnedProviderError("no dynamic hydrology packets")

    packets: list[HydrologyStep] = []
    for index in range(packet_count):
        try:
            step = parse_dynamic_step(records, index, static)
            step.validate()
            step.require_hydro_detailed_projection()
        except (ValueError, HydrologyAdapterError) as exc:
            raise PinnedProviderError(f"packet[{index}]: {exc}") from exc
        packets.append(step)
    return static, tuple(packets), physical_blocks


class PinnedLWKMFileHydrologyProvider(ImmutableHydrologyPacketProvider):
    """Pinned nonproduction adapter for the supplied LWKM SWATRE.UNF source."""

    def __init__(
        self,
        packets: Iterable[HydrologyStep],
        runtime_calendar_contract_id: str,
        producer_day_offset: int,
        identity: ProviderIdentity,
        static: dict,
    ) -> None:
        super().__init__(packets, runtime_calendar_contract_id, producer_day_offset)
        self._identity = identity
        self._static = dict(static)

    @property
    def identity(self) -> ProviderIdentity:
        return self._identity

    @property
    def static_metadata(self) -> dict:
        return dict(self._static)

    @classmethod
    def from_path(
        cls,
        path: Path | str,
        runtime_calendar_contract_id: str,
        producer_day_offset: int = 0,
    ) -> "PinnedLWKMFileHydrologyProvider":
        return cls.from_bytes(
            Path(path).read_bytes(),
            runtime_calendar_contract_id,
            producer_day_offset,
        )

    @classmethod
    def from_bytes(
        cls,
        raw: bytes,
        runtime_calendar_contract_id: str,
        producer_day_offset: int = 0,
    ) -> "PinnedLWKMFileHydrologyProvider":
        source_sha = hashlib.sha256(raw).hexdigest()
        if source_sha != EXPECTED_SOURCE_SHA256:
            raise PinnedProviderError(
                f"unexpected LWKM source SHA-256: {source_sha}"
            )

        try:
            records, physical_blocks = parse_powerstation_records(raw)
            static = parse_swap3_static(records)
        except (ValueError, HydrologyAdapterError) as exc:
            raise PinnedProviderError(str(exc)) from exc

        expected_static = {
            "hlpimp": 11,
            "nl": 30,
            "nh": 30,
            "nudr": 5,
            "ioptte": True,
        }
        for key, expected in expected_static.items():
            if static.get(key) != expected:
                raise PinnedProviderError(
                    f"unexpected pinned LWKM static {key}: {static.get(key)!r}"
                )
        if "V7.3.3.3" not in static["headers"][3]:
            raise PinnedProviderError("unexpected pinned LWKM producer model header")

        records_per_step = 8 + static["nudr"]
        dynamic_count = len(records) - static["dynamic_start"]
        if dynamic_count < 0 or dynamic_count % records_per_step != 0:
            raise PinnedProviderError("pinned LWKM dynamic records are not step-aligned")
        packet_count = dynamic_count // records_per_step
        if packet_count != EXPECTED_PACKET_COUNT:
            raise PinnedProviderError(
                f"unexpected pinned LWKM packet count: {packet_count}"
            )

        packets: list[HydrologyStep] = []
        typed_digests: list[str] = []
        group_digests: list[str] = []
        record_lines: list[str] = []
        previous_endpoint: float | None = None

        for index in range(packet_count):
            try:
                step = parse_dynamic_step(records, index, static)
                step.validate()
                step.require_hydro_detailed_projection()
                provenance = legacy_step_provenance(records, index, static)
            except (ValueError, HydrologyAdapterError) as exc:
                raise PinnedProviderError(f"packet[{index}]: {exc}") from exc

            endpoint = step.producer_endpoint_day
            duration = step.producer_step_days
            origin = endpoint - duration
            if index > 0 and origin != previous_endpoint:
                raise PinnedProviderError(
                    f"producer chain discontinuity at {index}: "
                    f"{origin} != {previous_endpoint}"
                )
            previous_endpoint = endpoint

            typed = typed_step_digest(step)
            group = provenance.source_record_sha256
            typed_digests.append(typed)
            group_digests.append(group)
            record_lines.append(
                f"{index}|{endpoint:.17g}|{duration:.17g}|{group}|{typed}"
            )
            packets.append(step)

        typed_sequence = _sequence_sha256(typed_digests)
        group_sequence = _sequence_sha256(group_digests)
        record_sequence = _sequence_sha256(record_lines)

        expected_identity = {
            "typed step sequence": (
                typed_sequence,
                EXPECTED_TYPED_SEQUENCE_SHA256,
            ),
            "dynamic group sequence": (
                group_sequence,
                EXPECTED_GROUP_SEQUENCE_SHA256,
            ),
            "temporal/digest sequence": (
                record_sequence,
                EXPECTED_RECORD_SEQUENCE_SHA256,
            ),
        }
        for label, (actual, expected) in expected_identity.items():
            if actual != expected:
                raise PinnedProviderError(
                    f"{label} mismatch: {actual} != {expected}"
                )

        identity = ProviderIdentity(
            source_sha256=source_sha,
            packet_count=packet_count,
            logical_record_count=len(records),
            physical_block_count=physical_blocks,
            typed_step_digest_sequence_sha256=typed_sequence,
            dynamic_group_digest_sequence_sha256=group_sequence,
            temporal_and_digest_record_sequence_sha256=record_sequence,
        )
        return cls(
            packets,
            runtime_calendar_contract_id,
            producer_day_offset,
            identity,
            static,
        )
