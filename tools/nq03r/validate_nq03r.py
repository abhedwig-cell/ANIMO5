#!/usr/bin/env python3
"""Fail-closed independent numerical review validator for ANIMO-NQ03R.

This reconstruction intentionally does not call the NQ03 oracle or validator.
It derives the finite-positive reservoir coefficients from the persisted
mathematical contract and checks the NQ03 claims with an independent 120-digit
Decimal reference.
"""
from __future__ import annotations

import json
import math
import struct
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 120

ROOT = Path(__file__).resolve().parents[2]
NQ03_BASE = "7fa0162415e02a6f0167e71b48ae38177a9e06e0"
NQ03_HEAD = "8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6"
POLICY = ROOT / "integration/animo-science/NQ03_TCD042_E1_POLICY.json"
REVIEW = ROOT / "integration/animo-science/NQ03R_INDEPENDENT_REVIEW.json"
STATUS = ROOT / "integration/animo-science/ANIMO-NQ03R_STATUS.json"
B3I05 = ROOT / "integration/animo-b3/ANIMO-B3I05_STATUS.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def D(value: float | str | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def exact_decimal(p: float) -> tuple[Decimal, Decimal, Decimal]:
    x = D(p)
    require(x > 0, "review oracle is finite-positive only")
    a1 = (-x).exp()
    f = (D(1) - a1) / x
    g = (x - D(1) + a1) / (x * x)
    return a1, f, g


def series_horner64(p: float, degree: int) -> tuple[float, float]:
    f = 0.0
    g = 0.0
    for k in range(degree, -1, -1):
        f = f * p + ((-1.0) ** k) / math.factorial(k + 1)
        g = g * p + ((-1.0) ** k) / math.factorial(k + 2)
    return f, g


def direct_polynomial64(p: float) -> tuple[float, float]:
    return 1.0 - p / 2.0 + p * p / 6.0, 0.5 - p / 6.0 + p * p / 24.0


def dense_grid(pmin: float, pmax: float, n: int = 2001) -> list[float]:
    lo = math.log(pmin)
    hi = math.log(pmax)
    return [math.exp(lo + i * (hi - lo) / (n - 1)) for i in range(n)]


def relerr(value: float, reference: float) -> float:
    return abs(value - reference) / abs(reference)


def f32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", float(value)))[0]


def add32(a: float, b: float) -> float:
    return f32(f32(a) + f32(b))


def mul32(a: float, b: float) -> float:
    return f32(f32(a) * f32(b))


def candidate32(p: float) -> tuple[float, float, float]:
    x = f32(p)
    f = add32(mul32(f32(1.0 / 6.0), x), f32(-0.5))
    f = add32(mul32(f, x), f32(1.0))
    g = add32(mul32(f32(1.0 / 24.0), x), f32(-1.0 / 6.0))
    g = add32(mul32(g, x), f32(0.5))
    a1 = f32(math.exp(-x))
    return a1, f, g


def apply_candidate(c0: float, lbar: float, p: float) -> tuple[float, float]:
    f, g = series_horner64(p, 2)
    a1 = math.exp(-p)
    return c0 * a1 + lbar * f, c0 * f + lbar * g


def split_candidate(c0: float, lbar: float, p: float, n: int) -> tuple[float, float]:
    c = c0
    averages: list[float] = []
    for _ in range(n):
        c, avg = apply_candidate(c, lbar / n, p / n)
        averages.append(avg)
    return c, sum(averages) / n


def changed_paths(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def validate_scope() -> None:
    nq03_allowed = (
        ".github/workflows/animo-nq03-",
        "docs/numerics/TCD042_E1_",
        "integration/animo-science/ANIMO-NQ03_STATUS.json",
        "integration/animo-science/NQ03_",
        "tools/nq03/",
    )
    nq03_changed = changed_paths(NQ03_BASE, NQ03_HEAD)
    require(len(nq03_changed) == 11, f"unexpected NQ03 changed-file count: {len(nq03_changed)}")
    for path in nq03_changed:
        require(path.startswith(nq03_allowed), f"NQ03 scope widened by {path}")
        require(not path.startswith("src/"), "NQ03 modified production source")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "NQ03 modified canonical TCD register")
        require("TCD042_ZERO" not in path, "NQ03 modified TCD-042-B1 artifact")

    review_allowed = (
        ".github/workflows/animo-nq03r-",
        "docs/numerics/TCD042_E1_INDEPENDENT_NUMERICAL_REVIEW.md",
        "integration/animo-science/ANIMO-NQ03R_STATUS.json",
        "integration/animo-science/NQ03R_",
        "tools/nq03r/",
    )
    review_changed = changed_paths(NQ03_HEAD, "HEAD")
    require(review_changed, "review branch contains no review artifacts")
    for path in review_changed:
        require(path.startswith(review_allowed), f"NQ03R scope widened by {path}")
        require(not path.startswith("src/"), "NQ03R modified production source")


def main() -> None:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    b3i05 = json.loads(B3I05.read_text(encoding="utf-8"))

    require(policy["target"] == "TCD-042-E1", "wrong policy target")
    require(policy["selected_candidate_policy"]["name"] == "NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY", "wrong policy identity")
    require(review["work_unit"] == "ANIMO-NQ03R", "wrong review workunit")
    require(review["reviewed_head"] == NQ03_HEAD, "review head drift")
    require(review["outcome"] == "INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY", "review outcome changed")
    require(review["independence"]["methodological"] is True, "methodological independence missing")
    require(review["independence"]["organizational"] is False, "organizational independence incorrectly claimed")
    require(b3i05["status"] == "QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS", "B3I05 route no longer qualified in reviewed tree")

    pinfo = policy["natural_P_envelope"]
    require(pinfo["records"] == 1238 and pinfo["cases"] == 6, "natural envelope count drift")
    pmin = float(pinfo["min"])
    pmax = float(pinfo["max"])
    natural = [float(pinfo[k]) for k in ("min", "p01", "p25", "median", "p75", "p99", "max")]
    dense = dense_grid(pmin, pmax)
    probes = list(dict.fromkeys(dense + natural))
    require(len(dense) == 2001, "wrong dense grid count")
    require(len(probes) == 2008, f"wrong unique review probe count: {len(probes)}")

    max_direct_f = 0.0
    max_direct_g = 0.0
    max_expm1_f = 0.0
    max_expm1_g = 0.0
    max_f32_a1 = 0.0
    max_f32_f = 0.0
    max_f32_g = 0.0
    horner_f_mismatch = 0
    horner_g_mismatch = 0
    literal_f_mismatch = 0
    literal_g_mismatch = 0
    literal_any_mismatch = 0
    max_literal_f = 0.0
    max_literal_g = 0.0

    for p in probes:
        a1d, fd, gd = exact_decimal(p)
        a1r = float(a1d)
        fr = float(fd)
        gr = float(gd)

        a1 = math.exp(-p)
        direct_f = (1.0 - a1) / p
        direct_g = (1.0 - direct_f) / p
        max_direct_f = max(max_direct_f, relerr(direct_f, fr))
        max_direct_g = max(max_direct_g, relerr(direct_g, gr))

        em = math.expm1(-p)
        expm1_f = -em / p
        expm1_g = (1.0 - expm1_f) / p
        max_expm1_f = max(max_expm1_f, relerr(expm1_f, fr))
        max_expm1_g = max(max_expm1_g, relerr(expm1_g, gr))

        fh, gh = series_horner64(p, 2)
        horner_f_mismatch += fh != fr
        horner_g_mismatch += gh != gr

        fl, gl = direct_polynomial64(p)
        fm = fl != fr
        gm = gl != gr
        literal_f_mismatch += fm
        literal_g_mismatch += gm
        literal_any_mismatch += fm or gm
        max_literal_f = max(max_literal_f, relerr(fl, fr))
        max_literal_g = max(max_literal_g, relerr(gl, gr))

        a32, f_32, g_32 = candidate32(p)
        max_f32_a1 = max(max_f32_a1, relerr(a32, a1r))
        max_f32_f = max(max_f32_f, relerr(f_32, fr))
        max_f32_g = max(max_f32_g, relerr(g_32, gr))

    require(max_direct_f == 1.0, "direct f failure not reproduced")
    require(max_direct_g > 4.7e19, "direct g failure not reproduced")
    require(max_expm1_f <= 2.0 ** -52, "expm1 f unexpectedly inaccurate")
    require(max_expm1_g == 1.0, "expm1-only g failure not reproduced")
    require(horner_f_mismatch == 0 and horner_g_mismatch == 0, "Horner degree-2 policy does not round to independent oracle")
    require(literal_f_mismatch == 67, f"literal-order f mismatch count changed: {literal_f_mismatch}")
    require(literal_g_mismatch == 73, f"literal-order g mismatch count changed: {literal_g_mismatch}")
    require(literal_any_mismatch == 129, f"literal-order combined mismatch count changed: {literal_any_mismatch}")
    require(max_literal_f <= 2.0 ** -52 and max_literal_g <= 2.0 ** -52, "literal-order variation exceeds one-ulp-scale review envelope")

    require(abs(max_f32_a1 - review["precision_review"]["binary32_max_relative_error_A1"]) < 1e-20, "binary32 A1 review mismatch")
    require(abs(max_f32_f - review["precision_review"]["binary32_max_relative_error_f"]) < 1e-20, "binary32 f review mismatch")
    require(abs(max_f32_g - review["precision_review"]["binary32_max_relative_error_g"]) < 1e-20, "binary32 g review mismatch")

    # Independent alternating-series order check at the upper envelope.
    x = D(pmax)
    f1 = D(1) - x / D(2)
    g1 = D(1) / D(2) - x / D(6)
    f2 = f1 + x * x / D(6)
    g2 = g1 + x * x / D(24)
    _, fexact, gexact = exact_decimal(pmax)
    f1err = abs(f1 - fexact)
    g1err = abs(g1 - gexact)
    f2err = abs(f2 - fexact)
    g2err = abs(g2 - gexact)
    half_ulp_f = D(math.ulp(1.0) / 2.0)
    half_ulp_g = D(math.ulp(0.5) / 2.0)
    require(f1err > half_ulp_f and g1err > half_ulp_g, "degree 1 unexpectedly satisfies representation-scale criterion")
    require(f2err < half_ulp_f and g2err < half_ulp_g, "degree 2 does not satisfy representation-scale criterion")

    # Conservation and equal-subinterval composition.
    state_probes = ((0.37, 0.0), (0.37, 0.23), (0.0, 0.23))
    max_balance = 0.0
    split = {n: [0.0, 0.0] for n in (2, 4, 8, 16, 32)}
    for p in dense:
        for c0, lbar in state_probes:
            c1, cavg = apply_candidate(c0, lbar, p)
            max_balance = max(max_balance, abs((c1 - c0) - (lbar - p * cavg)))
            for n in split:
                cs, avs = split_candidate(c0, lbar, p, n)
                split[n][0] = max(split[n][0], abs(cs - c1))
                split[n][1] = max(split[n][1], abs(avs - cavg))
    require(max_balance == 1.1102230246251565e-16, f"conservation review changed: {max_balance}")
    require(split[32][0] == 1.887379141862766e-15, f"32-step end-state review changed: {split[32][0]}")
    require(split[32][1] == 8.326672684688674e-16, f"32-step average review changed: {split[32][1]}")

    zero = policy["exact_zero_continuity"]
    require(zero["matches_UBQ01_exact_zero_limit"] is True, "UBQ01 continuity lost")
    require(zero["TCD042_B1_redefined"] is False, "TCD-042-B1 redefined")
    require(zero["P_equals_zero_inside_NQ03_scope"] is False, "exact zero leaked into E1")

    finding = review["implementation_order_review_finding"]
    require(finding["severity"] == "NON_BLOCKING_FOR_RESTRICTED_POLICY_BLOCKING_BEFORE_BITWISE_PRODUCTION_BINDING", "evaluation-order finding severity changed")
    require("freeze" in finding["required_downstream_constraint"].lower(), "downstream evaluation-order constraint lost")

    for key, value in review["review_nonclaims"].items():
        require(value is False, f"unexpected review admission/nonclaim flip: {key}")

    validate_scope()

    require(status["work_unit"] == "ANIMO-NQ03R", "wrong status workunit")
    require(status["work_status"]["persisted"] is True, "review checkpoint not persisted")

    print("NQ03R PASS: restricted TCD-042-E1 policy independently reproduced; Horner-specific exact-rounding finding carried forward; no admission or production change")


if __name__ == "__main__":
    main()
