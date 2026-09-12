#!/usr/bin/env python3
import math
from decimal import Decimal, getcontext

getcontext().prec = 90


def d(x):
    return Decimal.from_float(float(x))


def secant_float(a, b, c, c0):
    den1 = 1.0 + b * c
    den0 = 1.0 + b * c0
    assert math.isfinite(den1) and math.isfinite(den0)
    assert den1 > 0.0 and den0 > 0.0
    v = a / (den1 * den0)
    assert math.isfinite(v)
    return v


def secant_decimal(a, b, c, c0):
    A, B, C, C0 = map(d, (a, b, c, c0))
    return A / ((Decimal(1) + B * C) * (Decimal(1) + B * C0))


def storage_decimal(a, b, c):
    A, B, C = map(d, (a, b, c))
    return A * C / (Decimal(1) + B * C)


def ulp_error(v, ref):
    rf = float(ref)
    if v == rf:
        return 0.0
    u = math.ulp(rf if rf != 0.0 else 0.0)
    if u == 0.0:
        return 0.0 if v == rf else math.inf
    return abs(v - rf) / u


def neighbour_points(x, y):
    xs = [math.nextafter(x, -math.inf), x, math.nextafter(x, math.inf)]
    ys = [math.nextafter(y, -math.inf), y, math.nextafter(y, math.inf)]
    for xx in xs:
        for yy in ys:
            if xx == x and yy == y:
                continue
            if math.isfinite(xx) and math.isfinite(yy) and xx >= 0.0 and yy >= 0.0:
                yield xx, yy


def toy_residual(x, y, rx, ry):
    return (x - rx, y - ry)


def toy_correction(x, y, rx, ry):
    # J = identity, so Newton correction equals F.
    return toy_residual(x, y, rx, ry)


def representation_stable(x, y, rx, ry):
    f1, f2 = toy_residual(x, y, rx, ry)
    dr, da = toy_correction(x, y, rx, ry)
    if not all(math.isfinite(v) for v in (x, y, f1, f2, dr, da)):
        return False
    if x < 0.0 or y < 0.0:
        return False
    if (x - dr) != x or (y - da) != y:
        return False
    r0 = abs(f1) + abs(f2)
    for xx, yy in neighbour_points(x, y):
        q1, q2 = toy_residual(xx, yy, rx, ry)
        if abs(q1) + abs(q2) < r0:
            return False
    return True


def main():
    a_values = [0.0, 1e-14, 1e-8, 1e-3, 0.5, 10.0, 999.0]
    b_values = [0.0, 1e-12, 1e-6, 0.1, 1.0, 10.0, 999.0]
    c_values = [0.0, 1e-18, 1e-12, 1e-8, 1e-5, 1e-2, 1.0, 100.0]
    max_ulp = 0.0
    cases = 0
    for a in a_values:
        for b in b_values:
            for c in c_values:
                for c0 in c_values:
                    v = secant_float(a, b, c, c0)
                    ref = secant_decimal(a, b, c, c0)
                    max_ulp = max(max_ulp, ulp_error(v, ref))
                    # The closed form is also the exact analytic zero-delta limit.
                    if c == c0:
                        A, B, C = map(d, (a, b, c))
                        tangent_ref = A / (Decimal(1) + B * C) ** 2
                        assert ref == tangent_ref
                    # For finite deltas, D*(C-C0) equals the exact storage change
                    # in real arithmetic. Check this with high precision.
                    if c != c0:
                        lhs = ref * (d(c) - d(c0))
                        rhs = storage_decimal(a, b, c) - storage_decimal(a, b, c0)
                        scale = max(Decimal(1), abs(rhs))
                        assert abs(lhs - rhs) <= Decimal('1e-75') * scale
                    cases += 1

    # Binary64 evaluation of this cancellation-free form should remain within
    # a small rounding envelope. This is arithmetic verification, not a model tolerance.
    assert max_ulp <= 4.0, max_ulp

    # Active negative control: endpoint tangent is not the finite secant away from zero delta.
    a, b, c0, c = 0.8400301920000034, 1129.000000000013, 2.1813092841667838e-5, 2.2313092841667838e-5
    sec = secant_decimal(a, b, c, c0)
    A, B, C = map(d, (a, b, c))
    tangent = A / (Decimal(1) + B * C) ** 2
    assert sec != tangent
    finite_change = storage_decimal(a, b, c) - storage_decimal(a, b, c0)
    tangent_change = tangent * (d(c) - d(c0))
    assert finite_change != tangent_change

    # Tolerance-free discrete-root acceptance predicate controls.
    rx = float.fromhex('0x1.23456789abcdep-10')
    ry = float.fromhex('0x1.3456789abcde0p-11')
    assert representation_stable(rx, ry, rx, ry)
    rx_up = math.nextafter(rx, math.inf)
    assert not representation_stable(rx_up, ry, rx, ry)
    ry_down = math.nextafter(ry, -math.inf)
    assert not representation_stable(rx, ry_down, rx, ry)

    print('TCD019 restricted policy oracle PASS')
    print('langmuir_cases', cases)
    print('max_secant_binary64_error_ulp', max_ulp)
    print('finite_delta_tangent_negative_control PASS')
    print('representation_stable_root_control PASS')
    print('one_ulp_displaceable_negative_controls PASS')
    print('model_tolerance NONE')
    print('legacy_fallback_admitted false')
    print('historical_behavior UNKNOWN_WITHOUT_B2')


if __name__ == '__main__':
    main()
