from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from prototype.kt03.hydrology_step import (  # noqa: E402
    HYDROLOGY_UNITS,
    LEGACY_LAYOUT_ID,
    SCHEMA_ID,
    UNIT_CONTRACT_ID,
    HydrologyAdapterError,
    HydrologyStep,
    LegacyStepProvenance,
    legacy_step_provenance,
    parse_dynamic_step,
    parse_swap3_static,
)


def rec_f(*values: float) -> bytes:
    return struct.pack("<" + "f" * len(values), *values)


def rec_i(*values: int) -> bytes:
    return struct.pack("<" + "i" * len(values), *values)


def synthetic_records() -> list[bytes]:
    nl = 2
    records = [
        b"* Project: synthetic",
        b"* File content: test",
        b"* File name: x",
        b"* Model version: SWAP3",
        b"* Generated at: now",
        rec_i(1),
        struct.pack("<iiff", 1974, 1974, 0.0, 1.0),
        rec_i(nl, 1, 0),
        rec_i(2),
        rec_f(0.4),
        rec_f(0.3),
        rec_f(0.1),
        rec_f(0.1, 0.2),
        rec_f(0.25, 0.26),
        rec_f(0.0, 0.0),
        rec_f(0.0),
        rec_f(-99.9, -99.9),
        rec_f(
            1.0, 1.0, 1.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.2,
            0.3, 0.4, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
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


def synthetic_hlpimp11_records() -> list[bytes]:
    nl = 3
    records = [
        b"* Project: synthetic Hlpimp11",
        b"* File content: test",
        b"* File name: x",
        b"* Model version: SWAP3",
        b"* Generated at: now",
        rec_i(11),
        struct.pack("<iiff", 1991, 1991, 0.0, 10.0),
        rec_i(nl, 1, 1),
        rec_i(3),
        rec_f(0.45),
        rec_f(0.32),
        rec_f(0.12),
        rec_f(0.10, 0.10, 0.20),
        rec_f(0.25, 0.26, 0.27),
        rec_f(1.5, 0.01, 0.0),
        rec_f(0.0),
        rec_f(8.0, 8.5, 9.0),
        rec_f(
            10.0, 10.0, 2.0, 0.0, 0.1, 0.2, 0.05, 0.0, 0.3, 0.4,
            0.5, 0.6, 0.1, 0.2, 1.4, 0.015, 0.02, 0.0, 0.001,
        ),
        rec_f(0.11, 0.12, 0.13),
        rec_f(0.21, 0.22, 0.23),
        rec_f(0.01, 0.02, 0.03),
        rec_f(0.001, 0.002, 0.003, 0.004),
        rec_f(0.0001, 0.0002, 0.0003),
        rec_f(0.0, 2.5, 0.4, 0.3),
        rec_f(5.0),
        rec_f(9.0, 9.5, 10.0),
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
    assert HYDROLOGY_UNITS["prr"] == "m d-1"
    assert HYDROLOGY_UNITS["sc"] == "cm pressure head"

    records = synthetic_records()
    static = parse_swap3_static(records)
    step = parse_dynamic_step(records, 0, static)
    provenance = legacy_step_provenance(records, 0, static)

    assert step.schema_id == SCHEMA_ID
    assert step.unit_contract_id == UNIT_CONTRACT_ID
    assert step.layer_count == 2
    assert step.drainage_count == 0
    assert step.producer_endpoint_day == 1.0
    assert step.producer_step_days == 1.0
    assert not step.has_soil_temperature
    assert step.soil_temperature == ()
    assert not step.has_interception_storage_end
    assert step.interception_storage_end is None
    assert not hasattr(step, "hlpimp")
    assert not hasattr(step, "source_record_sha256")
    assert provenance.legacy_layout_id == LEGACY_LAYOUT_ID
    assert provenance.hlpimp == 1
    provenance.validate()

    assert_raises("Sict unavailable", step.require_hydro_detailed_projection)

    independent = HydrologyStep(**step.__dict__)
    independent.validate()
    assert independent == step

    assert_raises(
        "schema identity mismatch",
        lambda: HydrologyStep(**{**step.__dict__, "schema_id": "WRONG"}).validate(),
    )
    assert_raises(
        "unit contract mismatch",
        lambda: HydrologyStep(
            **{**step.__dict__, "unit_contract_id": "WRONG"}
        ).validate(),
    )
    assert_raises(
        "layer-vector dimension mismatch",
        lambda: HydrologyStep(**{**step.__dict__, "sc": (1.0,)}).validate(),
    )
    assert_raises(
        "malformed source record SHA-256",
        lambda: LegacyStepProvenance(
            LEGACY_LAYOUT_ID, 1, "z" * 64
        ).validate(),
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

    h11_records = synthetic_hlpimp11_records()
    h11_static = parse_swap3_static(h11_records)
    h11 = parse_dynamic_step(h11_records, 0, h11_static)
    h11_provenance = legacy_step_provenance(h11_records, 0, h11_static)

    assert h11_provenance.hlpimp == 11
    assert h11_static["initial_interception_storage_present"]
    assert h11_static["ioptte"]
    assert h11.has_interception_storage_end
    assert h11.interception_storage_end == 0.015
    assert h11.has_soil_temperature
    assert h11.soil_temperature == (9.0, 9.5, 10.0)
    assert h11.fldr == ((0.0001, 0.0002, 0.0003),)

    h11.require_hydro_detailed_projection()
    downstream = h11.hydro_detailed_boundary()
    assert downstream["Sict"] == 0.015
    assert downstream["St"] == 10.0
    assert downstream["Fldr"] == h11.fldr
    assert downstream["Flab"] == h11.flab
    assert "groundwater_level" not in downstream
    assert "soil_temperature" not in downstream

    h11_independent = HydrologyStep(**h11.__dict__)
    h11_independent.validate()
    assert h11_independent.hydro_detailed_boundary() == downstream

    malformed_h11 = synthetic_hlpimp11_records()
    malformed_h11[14] = rec_f(1.5, 0.0)
    assert_raises(
        "initial groundwater/interception/ponding",
        lambda: parse_swap3_static(malformed_h11),
    )

    print("KT03 hydrology adapter tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
