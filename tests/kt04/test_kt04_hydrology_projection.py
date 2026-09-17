from __future__ import annotations

import math
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
    EXPLICIT_INTERCEPTION_AUTHORITY,
    HLPIMP1_CANDIDATE,
    HydroDetailedProjection,
    ProjectionAuthority,
    TopBoundaryContext,
    authority_from_legacy_provenance,
    evaluate_swap3_top_boundary,
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
        b"* Project: synthetic", b"* File content: test", b"* File name: x",
        b"* Model version: SWAP3", b"* Generated at: now", ri(1),
        struct.pack("<iiff", 2000, 2000, 0.0, 1.0), ri(1, 1, 0), ri(1),
        rf(0.4), rf(0.3), rf(0.1), rf(0.1), rf(0.25), rf(1.0, 0.0),
        rf(0.0), rf(-99.9),
        rf(1.0, 1.0, 0.001, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0008,
           0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
        rf(0.1), rf(0.25), rf(0.0001), rf(0.0002, 0.0003),
        rf(0.0, 0.0, 0.0, 0.0), rf(0.0), rf(0.0),
    ]


def records_h11() -> list[bytes]:
    return [
        b"* Project: synthetic h11", b"* File content: test", b"* File name: x",
        b"* Model version: SWAP3", b"* Generated at: now", ri(11),
        struct.pack("<iiff", 2000, 2000, 0.0, 1.0), ri(1, 1, 0), ri(1),
        rf(0.4), rf(0.3), rf(0.1), rf(0.1), rf(0.25), rf(1.0, 0.0001, 0.0),
        rf(0.0), rf(-99.9),
        rf(1.0, 1.0, 0.001, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0007,
           0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0002, 0.0, 0.0, 0.0),
        rf(0.1), rf(0.25), rf(0.0001), rf(0.0002, 0.0003),
        rf(0.0, 0.0, 0.0, 0.0), rf(0.0), rf(0.0),
    ]


def expect_error(fragment: str, fn) -> None:
    try:
        fn()
    except HydrologyAdapterError as exc:
        assert fragment in str(exc), (fragment, str(exc))
    else:
        raise AssertionError(f"expected error containing {fragment!r}")


def main() -> int:
    # Fail closed on the unresolved Tier-C Hlpimp=1 semantics.
    h1_records = records_h1()
    h1_static = parse_swap3_static(h1_records)
    h1_step = parse_dynamic_step(h1_records, 0, h1_static)
    h1_prov = legacy_step_provenance(h1_records, 0, h1_static)

    expect_error(
        "blocked pending GOV04 Tier C independent review",
        lambda: authority_from_legacy_provenance(h1_step, h1_prov),
    )
    expect_error(
        "blocked pending GOV04 Tier C independent review",
        lambda: project_legacy_step(h1_step, h1_prov),
    )
    expect_error(
        "blocked pending GOV04 Tier C independent review",
        lambda: project_typed_step(
            HydrologyStep(**h1_step.__dict__), authority=HLPIMP1_CANDIDATE
        ),
    )

    # The explicit Hlpimp=11 state is already part of the frozen KT03 contract.
    h11_records = records_h11()
    h11_static = parse_swap3_static(h11_records)
    h11_step = parse_dynamic_step(h11_records, 0, h11_static)
    h11_prov = legacy_step_provenance(h11_records, 0, h11_static)
    assert authority_from_legacy_provenance(h11_step, h11_prov) == EXPLICIT_INTERCEPTION_AUTHORITY

    file_projection = project_legacy_step(h11_step, h11_prov)
    typed_projection = project_typed_step(
        HydrologyStep(**h11_step.__dict__),
        authority=EXPLICIT_INTERCEPTION_AUTHORITY,
    )
    assert file_projection == typed_projection
    assert projection_digest(file_projection) == projection_digest(typed_projection)
    assert file_projection.as_dict()["Sict"] == 0.0002
    assert isinstance(file_projection.external_inputs, tuple)

    context = TopBoundaryContext(
        ruso=0.0,
        moisture_storage_rate_layer1=0.0,
        runinu=0.0,
        rupr=0.0,
        rurv=0.0,
        ponding_start=0.0,
        snow_storage_start=0.0,
        interception_storage_start=0.0001,
    )
    result = evaluate_swap3_top_boundary(file_projection, context)
    assert abs(result.interception_delta - 0.0001) < 1.0e-12
    assert result == evaluate_swap3_top_boundary(typed_projection, context)
    assert math.isfinite(result.preliminary_flab1)
    assert math.isfinite(result.dif)
    assert math.isfinite(result.flab1_after_correction)

    expect_error(
        "requires interception payload",
        lambda: project_typed_step(h1_step, authority=EXPLICIT_INTERCEPTION_AUTHORITY),
    )
    expect_error(
        "unqualified hydrology projection authority",
        lambda: project_typed_step(
            h11_step,
            authority=ProjectionAuthority(
                "UNQUALIFIED", EXPLICIT_INTERCEPTION_AUTHORITY.interception_policy_id
            ),
        ),
    )

    missing_field = HydroDetailedProjection(
        authority=EXPLICIT_INTERCEPTION_AUTHORITY,
        interception_storage_end=file_projection.interception_storage_end,
        external_inputs=tuple(
            item for item in file_projection.external_inputs if item[0] != "Prr"
        ),
    )
    expect_error("external projection field set mismatch", missing_field.validate)

    bad_shape = HydroDetailedProjection(
        authority=EXPLICIT_INTERCEPTION_AUTHORITY,
        interception_storage_end=file_projection.interception_storage_end,
        external_inputs=tuple(
            (key, tuple()) if key == "Flev" else (key, value)
            for key, value in file_projection.external_inputs
        ),
    )
    expect_error("projection Flev layer dimension mismatch", bad_shape.validate)

    bad_context = TopBoundaryContext(
        **{**context.__dict__, "moisture_storage_rate_layer1": math.nan}
    )
    expect_error(
        "context.moisture_storage_rate_layer1: non-finite value",
        lambda: evaluate_swap3_top_boundary(file_projection, bad_context),
    )

    bad_runoff_context = TopBoundaryContext(**{**context.__dict__, "ruso": 0.001})
    expect_error(
        "runoff split closure mismatch",
        lambda: evaluate_swap3_top_boundary(file_projection, bad_runoff_context),
    )

    print("KT04 hydrology projection tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
