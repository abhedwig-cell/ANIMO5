from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from prototype.kt03.hydrology_step import (  # noqa: E402
    HydrologyAdapterError,
    HydrologyStep,
    legacy_step_provenance,
    parse_dynamic_step,
    parse_swap3_static,
)
from prototype.kt04.hydrology_projection import (  # noqa: E402
    EXPLICIT_INTERCEPTION_POLICY,
    HLPIMP1_ABSENT_INTERCEPTION_POLICY,
    TopBoundaryContext,
    evaluate_swap3_top_boundary,
    policy_from_legacy_provenance,
    project_legacy_step,
    project_typed_step,
    projection_digest,
)


def rf(*values: float) -> bytes:
    return struct.pack("<" + "f" * len(values), *values)


def ri(*values: int) -> bytes:
    return struct.pack("<" + "i" * len(values), *values)


def records_h1() -> list[bytes]:
    return [
        b"* Project: synthetic",
        b"* File content: test",
        b"* File name: x",
        b"* Model version: SWAP3",
        b"* Generated at: now",
        ri(1),
        struct.pack("<iiff", 2000, 2000, 0.0, 1.0),
        ri(1, 1, 0),
        ri(1),
        rf(0.4),
        rf(0.3),
        rf(0.1),
        rf(0.1),
        rf(0.25),
        rf(1.0, 0.0),
        rf(0.0),
        rf(-99.9),
        rf(
            1.0, 1.0, 0.001, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0008,
            0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
        ),
        rf(0.1),
        rf(0.25),
        rf(0.0001),
        rf(0.0002, 0.0003),
        rf(0.0, 0.0, 0.0, 0.0),
        rf(0.0),
        rf(0.0),
    ]


def records_h11() -> list[bytes]:
    return [
        b"* Project: synthetic h11",
        b"* File content: test",
        b"* File name: x",
        b"* Model version: SWAP3",
        b"* Generated at: now",
        ri(11),
        struct.pack("<iiff", 2000, 2000, 0.0, 1.0),
        ri(1, 1, 0),
        ri(1),
        rf(0.4),
        rf(0.3),
        rf(0.1),
        rf(0.1),
        rf(0.25),
        rf(1.0, 0.0001, 0.0),
        rf(0.0),
        rf(-99.9),
        rf(
            1.0, 1.0, 0.001, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0007,
            0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0002, 0.0, 0.0, 0.0,
        ),
        rf(0.1),
        rf(0.25),
        rf(0.0001),
        rf(0.0002, 0.0003),
        rf(0.0, 0.0, 0.0, 0.0),
        rf(0.0),
        rf(0.0),
    ]


def expect_error(fragment: str, fn) -> None:
    try:
        fn()
    except HydrologyAdapterError as exc:
        assert fragment in str(exc), (fragment, str(exc))
    else:
        raise AssertionError(f"expected error containing {fragment!r}")


def main() -> int:
    h1_records = records_h1()
    h1_static = parse_swap3_static(h1_records)
    h1_step = parse_dynamic_step(h1_records, 0, h1_static)
    h1_prov = legacy_step_provenance(h1_records, 0, h1_static)

    assert policy_from_legacy_provenance(h1_step, h1_prov) == HLPIMP1_ABSENT_INTERCEPTION_POLICY
    file_projection = project_legacy_step(h1_step, h1_prov)
    typed_projection = project_typed_step(
        HydrologyStep(**h1_step.__dict__),
        interception_policy_id=HLPIMP1_ABSENT_INTERCEPTION_POLICY,
    )
    assert file_projection == typed_projection
    assert projection_digest(file_projection) == projection_digest(typed_projection)
    assert "Sict" not in file_projection.external_inputs

    context_h1 = TopBoundaryContext(
        flab1_before_correction=0.0002,
        flab2=0.0001,
        ruso=0.0,
        moisture_storage_rate_layer1=0.0,
        drainage_total_layer1=0.0,
        runinu=0.0,
        rupr=0.0,
        rurv=0.0,
        ponding_start=0.0,
        snow_storage_start=0.0,
    )
    assert (
        evaluate_swap3_top_boundary(file_projection, context_h1)
        == evaluate_swap3_top_boundary(typed_projection, context_h1)
    )

    expect_error(
        "must not receive an interception start state",
        lambda: evaluate_swap3_top_boundary(
            file_projection,
            TopBoundaryContext(**{**context_h1.__dict__, "interception_storage_start": 0.0}),
        ),
    )
    expect_error(
        "requires interception payload",
        lambda: project_typed_step(
            h1_step, interception_policy_id=EXPLICIT_INTERCEPTION_POLICY
        ),
    )

    h11_records = records_h11()
    h11_static = parse_swap3_static(h11_records)
    h11_step = parse_dynamic_step(h11_records, 0, h11_static)
    h11_prov = legacy_step_provenance(h11_records, 0, h11_static)
    assert policy_from_legacy_provenance(h11_step, h11_prov) == EXPLICIT_INTERCEPTION_POLICY

    h11_file_projection = project_legacy_step(h11_step, h11_prov)
    h11_typed_projection = project_typed_step(
        HydrologyStep(**h11_step.__dict__),
        interception_policy_id=EXPLICIT_INTERCEPTION_POLICY,
    )
    assert h11_file_projection == h11_typed_projection
    assert h11_file_projection.external_inputs["Sict"] == 0.0002

    context_h11 = TopBoundaryContext(
        flab1_before_correction=0.0002,
        flab2=0.0001,
        ruso=0.0,
        moisture_storage_rate_layer1=0.0,
        drainage_total_layer1=0.0,
        runinu=0.0,
        rupr=0.0,
        rurv=0.0,
        ponding_start=0.0,
        snow_storage_start=0.0,
        interception_storage_start=0.0001,
    )
    result_h11 = evaluate_swap3_top_boundary(h11_file_projection, context_h11)
    assert abs(result_h11.interception_delta - 0.0001) < 1.0e-12
    assert (
        result_h11
        == evaluate_swap3_top_boundary(h11_typed_projection, context_h11)
    )

    expect_error(
        "conflicts with explicit interception payload",
        lambda: project_typed_step(
            h11_step,
            interception_policy_id=HLPIMP1_ABSENT_INTERCEPTION_POLICY,
        ),
    )

    print("KT04 hydrology projection tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
