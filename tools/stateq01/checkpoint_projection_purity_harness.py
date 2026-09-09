"""Qualification-only checkpoint projection purity harness for RC-R8/RC-R9.

This is not a production serializer and contains no ANIMO physics. It tests the
candidate contract that a checkpoint is an observational projection of an
already accepted boundary. Diagnostic/report accumulators are not physical
owners and therefore cannot alter the physical+continuation checkpoint view.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping


class CheckpointProjectionError(ValueError):
    """Raised when candidate checkpoint projection inputs are malformed."""


def _identity(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckpointProjectionError(f"{label}: non-empty identity required")
    return value


def _generation(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CheckpointProjectionError("accepted_generation: non-negative integer required")
    return value


def _copy_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise CheckpointProjectionError(f"{label}: mapping required")
    return deepcopy(dict(value))


@dataclass(frozen=True)
class CheckpointMetadata:
    accepted_time_id: str
    accepted_generation: int
    physical_layout_id: str
    configuration_id: str

    @classmethod
    def build(
        cls,
        *,
        accepted_time_id: object,
        accepted_generation: object,
        physical_layout_id: object,
        configuration_id: object,
    ) -> "CheckpointMetadata":
        return cls(
            accepted_time_id=_identity(accepted_time_id, "accepted_time_id"),
            accepted_generation=_generation(accepted_generation),
            physical_layout_id=_identity(physical_layout_id, "physical_layout_id"),
            configuration_id=_identity(configuration_id, "configuration_id"),
        )


@dataclass(frozen=True)
class CheckpointProjection:
    metadata: CheckpointMetadata
    physical_state: dict[str, object]
    continuation_state: dict[str, object]


def project_checkpoint(
    *,
    metadata: CheckpointMetadata,
    physical_state: Mapping[str, object],
    continuation_state: Mapping[str, object],
    report_accumulators: Mapping[str, object],
    final_result_generation: bool,
) -> CheckpointProjection:
    """Project accepted state without mutating inputs or serializing reports.

    `final_result_generation` is intentionally accepted as context and then
    ignored. TS01 final-result generation must not mutate or redefine the
    already accepted physical checkpoint boundary.
    """

    if not isinstance(metadata, CheckpointMetadata):
        raise CheckpointProjectionError("metadata: CheckpointMetadata required")
    if not isinstance(final_result_generation, bool):
        raise CheckpointProjectionError("final_result_generation: bool required")

    physical_copy = _copy_mapping(physical_state, "physical_state")
    continuation_copy = _copy_mapping(continuation_state, "continuation_state")
    _copy_mapping(report_accumulators, "report_accumulators")

    return CheckpointProjection(
        metadata=metadata,
        physical_state=physical_copy,
        continuation_state=continuation_copy,
    )


def projection_payload(projection: CheckpointProjection) -> dict[str, object]:
    """Return the candidate serialized view used only by synthetic tests."""

    if not isinstance(projection, CheckpointProjection):
        raise CheckpointProjectionError("projection: CheckpointProjection required")
    return {
        "metadata": {
            "accepted_time_id": projection.metadata.accepted_time_id,
            "accepted_generation": projection.metadata.accepted_generation,
            "physical_layout_id": projection.metadata.physical_layout_id,
            "configuration_id": projection.metadata.configuration_id,
        },
        "physical_state": deepcopy(projection.physical_state),
        "continuation_state": deepcopy(projection.continuation_state),
    }
