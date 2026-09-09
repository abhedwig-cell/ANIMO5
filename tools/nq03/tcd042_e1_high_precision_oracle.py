#!/usr/bin/env python3
"""Independent high-precision oracle for ANIMO-NQ03 / TCD-042-E1.

Standard-library only. The Decimal path is the authority for the mathematical
reference; binary64 and emulated binary32 paths are comparison axes only.
No production source is read or modified.
"""
from __future__ import annotations

import json
import math
import struct
from decimal import Decimal, getcontext

getcontext().prec = 100

NATURAL_P = {
    "min": 4.2351647362715017e-20,
    "p01": 8.470329472543003e-20,
    "p25": 1.3552527156068803e-18,
    "median": 2.7105054312137607e-18,
    "p75": 5.421010862427522e-18,
    "p99": 1.5098499996065392e-7,
    "max": 3.8510200002999744e-7,
}


def D(value: float | str | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def exact_decimal(p: float | str | Decimal) -> tuple[Decimal, Decimal, Decimal]:
    x = D(p)
    if x <= 0:
        raise ValueError("oracle is finite-positive only")
    e = (-x).exp()
    f = (D(1) - e) / x
    g = (x - D(1) + e) / (x * x)
    return e, f, g


def series_decimal(p: float | str | Decimal, degree: int) -> tuple[Decimal, Decimal]:
    x = D(p)
    f = D(0)
    g = D(0)
    for k in range(degree + 1):
        sign = D(-1) if k % 2 else D(1)
        f += sign * x**k / D(math.factorial(k + 1))
        g += sign * x**k / D(math.factorial(k + 2))
    return f, g


def series_binary64(p: float, degree: int = 2) -> tuple[float, float, float]:
    f = 0.0
    g = 0.0
    for k in range(degree, -1, -1):
        f = f * p + ((-1.0) ** k) / math.factorial(k + 1)
        g = g * p + ((-1.0) ** k) / math.factorial(k + 2)
    return math.exp(-p), f, g


def direct_binary64(p: float) -> tuple[float, float, float]:
    a1 = math.exp(-p)
    f = (1.0 - a1) / p
    g = (1.0 - f) / p
    return a1, f, g


def expm1_binary64(p: float) -> tuple[float, float, float]:
    em1 = math.expm1(-p)
    a1 = 1.0 + em1
    f = -em1 / p
    g = (1.0 - f) / p
    return a1, f, g


def f32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", float(value)))[0]


def add32(a: float, b: float) -> float:
    return f32(f32(a) + f32(b))


def mul32(a: float, b: float) -> float:
    return f32(f32(a) * f32(b))


def series_binary32_emulated(p: float, degree: int = 2) -> tuple[float, float, float]:
    x = f32(p)
    f = f32(0.0)
    g = f32(0.0)
    for k in range(degree, -1, -1):
        cf = f32(((-1.0) ** k) / math.factorial(k + 1))
        cg = f32(((-1.0) ** k) / math.factorial(k + 2))
        f = add32(mul32(f, x), cf)
        g = add32(mul32(g, x), cg)
    a1 = f32(math.exp(-x))
    return a1, f, g


def relerr(value: float, reference: float) -> float:
    return abs(value - reference) / abs(reference)


def main() -> None:
    rows = []
    for name, p in NATURAL_P.items():
        e_d, f_d, g_d = exact_decimal(p)
        e = float(e_d)
        f = float(f_d)
        g = float(g_d)
        direct = direct_binary64(p)
        expm1 = expm1_binary64(p)
        series = series_binary64(p, 2)
        single = series_binary32_emulated(p, 2)
        rows.append(
            {
                "point": name,
                "P": p,
                "reference_f": str(f_d),
                "reference_g": str(g_d),
                "direct64_f_relerr": relerr(direct[1], f),
                "direct64_nested_g_relerr": relerr(direct[2], g),
                "expm1_f_relerr": relerr(expm1[1], f),
                "expm1_nested_g_relerr": relerr(expm1[2], g),
                "series2_64_f_relerr_to_rounded_reference": relerr(series[1], f),
                "series2_64_g_relerr_to_rounded_reference": relerr(series[2], g),
                "series2_32_f_relerr": relerr(single[1], f),
                "series2_32_g_relerr": relerr(single[2], g),
            }
        )
    print(json.dumps({"decimal_digits": getcontext().prec, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
