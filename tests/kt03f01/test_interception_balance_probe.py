from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.kt03f01.analyze_interception_balance import analyze_records  # noqa: E402


def rf(*values: float) -> bytes:
    return struct.pack("<" + "f" * len(values), *values)


def ri(*values: int) -> bytes:
    return struct.pack("<" + "i" * len(values), *values)


def records(hlpimp: int) -> list[bytes]:
    nl = 1
    nh = 1
    result = [
        b"* Project: synthetic",
        b"* File content: unformatted hydrological data",
        b"* File name: synthetic",
        b"* Model version: synthetic",
        b"* Generated at: synthetic",
        ri(hlpimp),
        struct.pack("<iiff", 2000, 2000, 0.0, 1.0),
        ri(nl, nh, 0),
        ri(1),
        rf(0.5),
        rf(0.3),
        rf(0.1),
        rf(1.0),
        rf(0.3),
        rf(1.0, 0.0001, 0.0) if hlpimp == 11 else rf(1.0, 0.0),
        rf(0.0),
        rf(-99.9),
    ]
    if hlpimp == 11:
        surface = rf(
            1.0, 1.0, 0.001, 0.0, 0.0, 0.0002, 0.0, 0.0,
            0.0007, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
            0.0002, 0.0, 0.0, 0.0,
        )
    else:
        surface = rf(
            1.0, 1.0, 0.001, 0.0, 0.0, 0.0002, 0.0, 0.0,
            0.0008, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
            0.0, 0.0, 0.0,
        )
    result.extend(
        [
            surface,
            rf(0.0),
            rf(0.3),
            rf(0.0),
            rf(0.0, 0.0),
            rf(0.0, 0.0, 0.0, 0.0),
            rf(0.0),
            rf(0.0),
        ]
    )
    return result


def main() -> int:
    h1 = analyze_records(records(1))
    assert h1["whole_profile_residual_with_explicit_interception_storage"] == "NOT_AVAILABLE_IN_LAYOUT"
    assert h1["whole_profile_residual_without_interception_storage"]["max_abs_m"] < 1.0e-10

    h11 = analyze_records(records(11))
    no_storage = h11["whole_profile_residual_without_interception_storage"]["max_abs_m"]
    with_storage = h11["whole_profile_residual_with_explicit_interception_storage"]["max_abs_m"]
    assert no_storage > 9.9e-5
    assert with_storage < 1.0e-10
    assert h11["mean_abs_improvement_factor"] > 1.0e5

    malformed = records(1)
    malformed[7] = ri(0, 1, 0)
    try:
        analyze_records(malformed)
    except ValueError as exc:
        assert "invalid dimensions" in str(exc)
    else:
        raise AssertionError("invalid dimensions must fail closed")

    print("KT03-F01 interception balance probe tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
