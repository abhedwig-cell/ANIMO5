from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from prototype.kt03.hydrology_step import (  # noqa: E402
    HydrologyAdapterError,
    HydrologyStep,
    parse_dynamic_step,
    parse_swap3_static,
)


def rec_f(*values: float) -> bytes:
    return struct.pack("<" + "f" * len(values), *values)


def rec_i(*values: int) -> bytes:
    return struct.pack("<" + "i" * len(values), *values)


def synthetic_records() -> list[bytes]:
    nl = 2
    nh = 1
    nudr = 0
    records = [
        b"* Project: synthetic",
        b"* File content: test",
        b"* File name: x",
        b"* Model version: SWAP3",
        b"* Generated at: now",
        rec_i(1),
        struct.pack("<iiff", 1974, 1974, 0.0, 1.0),
        rec_i(nl, nh, nudr),
        rec_i(2),
        rec_f(0.4),
        rec_f(0.3),
        rec_f(0.1),
        rec_f(0.1, 0.2),
        rec_f(0.25, 0.26),
        rec_f(0.0, 0.0),
        rec_f(0.0),
        rec_f(-99.9, -99.9),
    ]
    records += [
        rec_f(
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            0.1,
            0.0,
            0.0,
            0.2,
            0.3,
            0.4,
            0.5,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
        ),
        rec_f(0.1, 0.2),
        rec_f(0.2, 0.3),
        rec_f(0.0, 0.0),
        rec_f(0.0, 0.0, 0.0),
        rec_f(0.0, 0.0, 0.0, 0.0),
        rec_f(12.0),
        rec_f(99.0, 98.0),
    ]
    return records


def assert_raises(fragment: str, fn) -> None:
    try:
        fn()
    except HydrologyAdapterError as exc:
        assert fragment in str(exc), (fragment, str(exc))
    else:
        raise AssertionError(f"expected HydrologyAdapterError containing {fragment!r}")


def main() -> int:
    records = synthetic_records()
    static = parse_swap3_static(records)
    step = parse_dynamic_step(records, 0, static)

    assert step.layer_count == 2
    assert step.drainage_count == 0
    assert step.tiwa == 1.0
    assert step.step_days == 1.0
    assert not step.has_soil_temperature
    assert step.soil_temperature == ()
    assert not step.has_interception_storage_end
    assert step.interception_storage_end is None

    assert_raises("Sict unavailable", step.require_hydro_detailed_compatibility)

    independent = HydrologyStep(**step.__dict__)
    independent.validate()
    assert independent == step

    assert_raises(
        "layout identity mismatch",
        lambda: HydrologyStep(**{**step.__dict__, "layout_id": "WRONG"}).validate(),
    )
    assert_raises(
        "layer-vector dimension mismatch",
        lambda: HydrologyStep(**{**step.__dict__, "sc": (1.0,)}).validate(),
    )

    sentinel_records = synthetic_records()
    first = list(struct.unpack("<18f", sentinel_records[17]))
    first[14] = -9.99
    sentinel_records[17] = rec_f(*first)
    sentinel_static = parse_swap3_static(sentinel_records)

    assert_raises(
        "profile_bottom",
        lambda: parse_dynamic_step(sentinel_records, 0, sentinel_static),
    )
    normalized = parse_dynamic_step(
        sentinel_records, 0, sentinel_static, profile_bottom=2.5
    )
    assert normalized.groundwater_level == 2.5

    malformed = synthetic_records()
    malformed[18] = rec_f(0.1)
    assert_raises(
        "Sc: expected 8 bytes",
        lambda: parse_dynamic_step(malformed, 0, parse_swap3_static(malformed)),
    )

    print("KT03 hydrology adapter tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
