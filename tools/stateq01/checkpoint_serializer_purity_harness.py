"""Qualification-only RC-R8 checkpoint serializer purity harness.

This is not a production checkpoint format. It exists only to make the
STATEQ01 observational-purity contract executable: projecting an already
accepted state into a deterministic diagnostic byte representation must not
mutate physical or continuation state.

The representation used here is intentionally a test representation. Numeric
serialization policy for a production canonical checkpoint remains outside
this harness.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import math
from typing import Any, Mapping


class SerializerPurityError(ValueError):
    """Raised when the qualification projection cannot serialize safely."""


@dataclass(frozen=True)
class SerializerProjection:
    payload_bytes: bytes
    physical_state_before: object
    continuation_before: object
    diagnostics_before: object


def _validate_json_scalar_tree(value: Any, path: str = "root") -> None:
    if value is None or isinstance(value, (bool, int, str)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SerializerPurityError(f"{path}: non-finite float is not serializable")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_scalar_tree(item, f"{path}[{index}]")
        return
    if isinstance(value, tuple):
        for index, item in enumerate(value):
            _validate_json_scalar_tree(item, f"{path}[{index}]")
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise SerializerPurityError(f"{path}: mapping keys must be strings")
            _validate_json_scalar_tree(item, f"{path}.{key}")
        return
    raise SerializerPurityError(f"{path}: unsupported type {type(value).__name__}")


def qualification_serialize_accepted_state(
    *,
    identity_header: Mapping[str, Any],
    physical_state: Mapping[str, Any],
    continuation_state: Mapping[str, Any],
    diagnostic_state: Mapping[str, Any] | None = None,
    include_diagnostics: bool = False,
) -> SerializerProjection:
    """Project accepted state without mutation, clipping or process execution.

    The returned bytes are only a deterministic qualification representation.
    They are not a proposed production checkpoint wire format.
    """

    before_identity = deepcopy(identity_header)
    before_physical = deepcopy(physical_state)
    before_continuation = deepcopy(continuation_state)
    before_diagnostics = deepcopy(diagnostic_state)

    document: dict[str, Any] = {
        "identity": deepcopy(identity_header),
        "physical_state": deepcopy(physical_state),
        "continuation_state": deepcopy(continuation_state),
    }
    if include_diagnostics:
        if diagnostic_state is None:
            raise SerializerPurityError("diagnostic continuation requested but not supplied")
        document["diagnostic_observer_state"] = deepcopy(diagnostic_state)

    _validate_json_scalar_tree(document)
    try:
        payload = json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SerializerPurityError(str(exc)) from exc

    if identity_header != before_identity:
        raise AssertionError("serializer mutated identity header")
    if physical_state != before_physical:
        raise AssertionError("serializer mutated accepted physical state")
    if continuation_state != before_continuation:
        raise AssertionError("serializer mutated continuation state")
    if diagnostic_state != before_diagnostics:
        raise AssertionError("serializer mutated diagnostic observer state")

    return SerializerProjection(
        payload_bytes=payload,
        physical_state_before=before_physical,
        continuation_before=before_continuation,
        diagnostics_before=before_diagnostics,
    )
