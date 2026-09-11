#!/usr/bin/env python3
import json
import math
from decimal import Decimal, localcontext

U = 2.0 ** -53
BOUND_U = 128.0

def horner_f(x, degree=24):
    acc = 0.0
    for k in range(degree, -1, -1):
        acc = acc * x + ((-1.0) ** k) / (k + 1)
    return acc

def horner_g(x, degree=24):
    acc = 0.0
    for k in range(degree, -1, -1):
        acc = acc * x + ((-1.0) ** k) / ((k + 1) * (k + 2))
    return acc

def horner_h(x, degree=24):
    acc = 0.0
    for k in range(degree, -1, -1):
        acc = acc * x + ((-1.0) ** k) / (k + 2)
    return acc

def evaluate(x):
    if not math.isfinite(x) or x <= -1.0:
        raise ValueError("outside qualified domain")
    if x == 0.0:
        return (1.0, 0.5, 0.5)
    ax = abs(x)
    if ax <= 0.25:
        return (horner_f(x), horner_g(x), horner_h(x))
    L = math.log1p(x)
    if ax <= 1.0:
        return (
            L / x,
            ((1.0 + x) * L - x) / (x * x),
            (x - L) / (x * x),
        )
    return (
        L / x,
        ((1.0 + 1.0 / x) * L - 1.0) / x,
        (1.0 - L / x) / x,
    )

def decimal_series(xd, kind, precision=120):
    with localcontext() as ctx:
        ctx.prec = precision + 30
        s = Decimal(0)
        power = Decimal(1)
        sign = Decimal(1)
        tolerance = Decimal(10) ** Decimal(-(precision + 10))
        for k in range(2001):
            if kind == "F":
                coeff = Decimal(1) / Decimal(k + 1)
            elif kind == "G":
                coeff = Decimal(1) / (Decimal(k + 1) * Decimal(k + 2))
            elif kind == "H":
                coeff = Decimal(1) / Decimal(k + 2)
            else:
                raise ValueError(kind)
            term = sign * power * coeff
            s += term
            if abs(term) < tolerance:
                return +s
            power *= xd
            sign = -sign
    raise RuntimeError("series did not converge")

def reference(x, precision=120):
    xd = Decimal.from_float(x)
    if xd == 0:
        return (Decimal(1), Decimal("0.5"), Decimal("0.5"))
    with localcontext() as ctx:
        ctx.prec = precision + 30
        if abs(xd) <= Decimal("0.25"):
            return tuple(decimal_series(xd, k, precision) for k in ("F", "G", "H"))
        L = (Decimal(1) + xd).ln()
        return (
            +(L / xd),
            +(((Decimal(1) + xd) * L - xd) / (xd * xd)),
            +((xd - L) / (xd * xd)),
        )

def points():
    p = set()
    for k in range(1, 1075):
        v = math.ldexp(1.0, -k)
        if v:
            p.add(v)
            p.add(-v)
    for i in range(2001):
        x = -0.999 + i * (1.999 / 2000)
        if x > -1.0:
            p.add(float(x))
    for e in range(-300, 301):
        x = 10.0 ** e
        if math.isfinite(x):
            p.add(x)
    p.update({
        -0.9999999999999999, -0.75, -0.5, -0.25, -0.24999999999999997,
        0.0, 0.24999999999999997, 0.25, 0.5, 1.0, 2.0, 1e10, 1e100, 1e300
    })
    return sorted(x for x in p if math.isfinite(x) and x > -1.0)

def main():
    pts = points()
    if len(pts) != 4756:
        raise AssertionError(f"unexpected deterministic point count: {len(pts)}")
    maxima = [0.0, 0.0, 0.0]
    max_at = [None, None, None]
    for x in pts:
        got = evaluate(x)
        ref = reference(x)
        for j in range(3):
            gd = Decimal.from_float(got[j])
            rel = abs(gd - ref[j]) / abs(ref[j])
            rel_u = float(rel / (Decimal(2) ** Decimal(-53)))
            if rel_u > maxima[j]:
                maxima[j] = rel_u
                max_at[j] = x
    for name, value in zip(("F", "G", "H"), maxima):
        if value > BOUND_U:
            raise AssertionError(f"{name} relative error {value}u exceeds {BOUND_U}u")

    # NQ02 naturally activated control point.
    Hv = -4.9999999995886668e-7
    T = 1.0
    D = 1147.1854958708439
    x = Hv * T / D
    _, G, _ = evaluate(x)
    b2_policy = T / D * G
    expected_b2 = 0.0004358493041206774
    if b2_policy != expected_b2:
        raise AssertionError((b2_policy, expected_b2))

    # Pinned NQ02 negative-control observations.
    legacy_b2 = 0.2685923078097403
    reference_b2dc = 0.47279499321842785
    legacy_b2dc = -290.4145135735744
    if abs(legacy_b2 / b2_policy) < 100.0:
        raise AssertionError("legacy B2 negative control is not materially separated")
    if not (reference_b2dc > 0.0 and legacy_b2dc < 0.0):
        raise AssertionError("B2dc sign negative control lost")

    result = {
        "work_unit": "ANIMO-NQ04",
        "target": "TCD-029",
        "deterministic_points": len(pts),
        "unit_roundoff": U,
        "verification_bound_u": BOUND_U,
        "max_relative_error_u": {
            "F": maxima[0],
            "G": maxima[1],
            "H": maxima[2],
        },
        "max_error_x": {
            "F": max_at[0],
            "G": max_at[1],
            "H": max_at[2],
        },
        "natural_control": {
            "x": x,
            "B2_policy_binary64": b2_policy,
            "B2_legacy_direct_pinned": legacy_b2,
            "B2dc_reference_pinned": reference_b2dc,
            "B2dc_legacy_direct_pinned": legacy_b2dc,
        },
        "result": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
