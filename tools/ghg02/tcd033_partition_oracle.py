#!/usr/bin/env python3
"""Equation oracle for TCD-033. Verification bounds are not model tolerances."""
from decimal import Decimal, getcontext
import math

getcontext().prec = 100
CUTOFF = 1.0e-8
VERIFY_ULP_BOUND = 64.0


def policy(a, e, substrates):
    s = sum(substrates)
    if a < CUTOFF or s == 0.0:
        return 0.0, [0.0 for _ in substrates]
    q = e * a * s
    return q, [q * si / s for si in substrates]


def legacy(a, e, substrates):
    s = sum(substrates)
    if a < CUTOFF:
        return 0.0, [0.0 for _ in substrates]
    q = e * a * s
    if s == 0.0:
        return q, None
    den = a * s
    return q, [q * si / den for si in substrates]


def d(x):
    return Decimal.from_float(float(x))


def reference(a, e, substrates):
    ad, ed = d(a), d(e)
    sd = sum((d(x) for x in substrates), Decimal(0))
    if float(a) < CUTOFF or sd == 0:
        return Decimal(0), [Decimal(0) for _ in substrates]
    q = ed * ad * sd
    return q, [q * d(si) / sd for si in substrates]


def ulp_error(value, reference_decimal):
    ref_float = float(reference_decimal)
    if value == ref_float:
        return 0.0
    scale = math.ulp(ref_float) if ref_float != 0.0 else math.ulp(0.0)
    return abs(value - ref_float) / scale


def check_case(a, e, substrates):
    q, parts = policy(a, e, substrates)
    qr, pr = reference(a, e, substrates)
    max_u = ulp_error(q, qr)
    for value, ref in zip(parts, pr):
        max_u = max(max_u, ulp_error(value, ref))
    if q == 0.0:
        assert all(x == 0.0 for x in parts)
    else:
        closure_u = abs(sum(parts) - q) / math.ulp(q)
        max_u = max(max_u, closure_u)
        assert closure_u <= VERIFY_ULP_BOUND, (a, e, substrates, closure_u)
        s = sum(substrates)
        for si, pi in zip(substrates, parts):
            expected = q * si / s
            assert pi == expected
    assert max_u <= VERIFY_ULP_BOUND, (a, e, substrates, max_u)
    return max_u


def main():
    anaerobic = [1.0, 0.9, 0.67, 0.4, 0.25, 1.0e-3, 1.0e-6, 1.0e-8, 9.999999e-9]
    env = [0.0, 1.0e-9, 0.123, 0.5, 2.0]
    vectors = [
        [2.0, 3.0],
        [4.0],
        [0.2, 1.7, 3.1, 5.0],
        [1.0e-12, 2.0e-12, 3.0e-12],
        [1.0e6, 2.0e6, 7.0e6],
        [0.0, 0.0],
    ]
    max_u = 0.0
    count = 0
    for a in anaerobic:
        for e in env:
            for ss in vectors:
                max_u = max(max_u, check_case(a, e, ss))
                count += 1

    # Full-anaerobic compatibility: policy and revision-53 component algebra coincide.
    q, p = policy(1.0, 0.5, [2.0, 3.0])
    ql, pl = legacy(1.0, 0.5, [2.0, 3.0])
    assert q == ql and p == pl

    # Partial-anaerobic negative control: revision-53 components sum to Q/A.
    a = 0.4
    q, p = policy(a, 0.5, [2.0, 3.0])
    ql, pl = legacy(a, 0.5, [2.0, 3.0])
    assert q == ql and pl is not None
    assert abs(sum(p) - q) <= VERIFY_ULP_BOUND * math.ulp(q)
    assert abs(sum(pl) - q / a) <= VERIFY_ULP_BOUND * math.ulp(q / a)
    assert sum(pl) > q

    # Existing source cutoff is strict LT. At exactly 1e-8 the branch remains active.
    q_cut, p_cut = policy(1.0e-8, 0.5, [2.0, 3.0])
    assert q_cut > 0.0 and sum(p_cut) > 0.0
    q_below, p_below = policy(9.999999e-9, 0.5, [2.0, 3.0])
    assert q_below == 0.0 and all(x == 0.0 for x in p_below)

    # Zero-substrate negative-domain control: legacy component division is undefined;
    # qualified policy defines the physically empty partition as all zero.
    q_zero, p_zero = policy(0.4, 0.5, [0.0, 0.0])
    ql_zero, pl_zero = legacy(0.4, 0.5, [0.0, 0.0])
    assert q_zero == ql_zero == 0.0 and all(x == 0.0 for x in p_zero) and pl_zero is None

    print("TCD033 partition oracle PASS")
    print("cases", count)
    print("max_equation_ulp", max_u)
    print("verification_bound_ulp", VERIFY_ULP_BOUND)
    print("historical_behavior UNKNOWN_WITHOUT_B2")


if __name__ == "__main__":
    main()
