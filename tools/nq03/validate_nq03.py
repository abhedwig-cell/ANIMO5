#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-NQ03 / TCD-042-E1.

The validator independently reproduces the key numerical claims with only the
Python standard library. It validates qualification artifacts and scope. It
cannot admit B3, TCD-042, a production patch, or a new TCD.
"""
from __future__ import annotations

import csv
import json
import math
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 100
ROOT = Path(__file__).resolve().parents[2]
BASE = "7fa0162415e02a6f0167e71b48ae38177a9e06e0"
STATUS = ROOT / "integration/animo-science/ANIMO-NQ03_STATUS.json"
EVIDENCE = ROOT / "integration/animo-science/NQ03_TCD042_E1_POLICY.json"
NATURAL = ROOT / "integration/animo-science/NQ03_NATURAL_ENVELOPE_MATRIX.csv"
TRUNC = ROOT / "integration/animo-science/NQ03_SERIES_TRUNCATION_MATRIX.csv"
PRECISION = ROOT / "integration/animo-science/NQ03_PRECISION_MATRIX.csv"
B3I05 = ROOT / "integration/animo-b3/ANIMO-B3I05_STATUS.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def D(x: float | str) -> Decimal:
    return Decimal(str(x))


def exact_decimal(p: float) -> tuple[Decimal, Decimal]:
    x = D(p)
    e = (-x).exp()
    return (D(1) - e) / x, (x - D(1) + e) / (x * x)


def series64(p: float, degree: int) -> tuple[float, float]:
    f = 0.0
    g = 0.0
    for k in range(degree, -1, -1):
        f = f * p + ((-1.0) ** k) / math.factorial(k + 1)
        g = g * p + ((-1.0) ** k) / math.factorial(k + 2)
    return f, g


def apply_candidate(c0: float, lbar: float, p: float) -> tuple[float, float]:
    f, g = series64(p, 2)
    a1 = math.exp(-p)
    return c0 * a1 + lbar * f, c0 * f + lbar * g


def split_candidate(c0: float, lbar: float, p: float, n: int) -> tuple[float, float]:
    c = c0
    avgs = []
    for _ in range(n):
        c, avg = apply_candidate(c, lbar / n, p / n)
        avgs.append(avg)
    return c, sum(avgs) / n


def dense_grid(pmin: float, pmax: float, n: int = 2001) -> list[float]:
    lo = math.log(pmin)
    hi = math.log(pmax)
    return [math.exp(lo + i * (hi - lo) / (n - 1)) for i in range(n)]


def scope_guard() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", BASE, "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    changed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    allowed_prefixes = (
        ".github/workflows/animo-nq03-",
        "docs/numerics/TCD042_E1_",
        "integration/animo-science/ANIMO-NQ03_STATUS.json",
        "integration/animo-science/NQ03_",
        "tools/nq03/",
    )
    require(changed, "NQ03 branch has no persisted changes")
    for path in changed:
        require(path.startswith(allowed_prefixes), f"scope widened by {path}")
        require(not path.startswith("src/"), "production source modified")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")
        require("TCD042_ZERO" not in path, "TCD-042-B1 artifact modified")


def main() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    b3i05 = json.loads(B3I05.read_text(encoding="utf-8"))

    require(status["work_unit"] == "ANIMO-NQ03", "wrong status workunit")
    require(status["target"] == "TCD-042-E1", "wrong status target")
    require(status["class"] == "E_NUMERICAL_POLICY", "wrong status class")
    require(status["work_status"]["persisted"] is True, "persist-early checkpoint lost")
    require(b3i05["status"] == "QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS", "B3I05 qualification prerequisite not present in branch")
    require(b3i05["child_state"]["TCD-042-E1"] == "ATOM_CHARACTERIZED_NUMERICAL_POLICY_QUALIFICATION_REQUIRED", "E1 child route changed")

    require(evidence["target"] == "TCD-042-E1", "wrong evidence target")
    require(evidence["scope"] == "Flpn=0 AND 0<Flux<1.0d-8", "scope widened")
    require(evidence["conditioning_coordinate"] == "P=St*Flux/Hetop", "conditioning coordinate changed")
    require(evidence["upstream"]["UBQ02_head"] == "bb572bb5d431f91d780018a1acbb345fbcfced37", "UBQ02 pin changed")
    require(evidence["frozen_identity"]["source_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "source hash changed")
    require(evidence["frozen_identity"]["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "testbank hash changed")

    policy = evidence["selected_candidate_policy"]
    require(policy["name"] == "NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY", "candidate identity changed")
    require(policy["evaluation_precision"] == "binary64", "canonical precision changed")
    require(policy["switch_inside_qualified_envelope"] is False, "unexpected switch introduced")
    require(policy["raw_Flux_threshold_selected_by_NQ03"] is False, "raw Flux threshold promoted to policy")
    require(policy["hidden_epsilon"] is False, "hidden epsilon introduced")
    require(policy["outside_applicability"] == "NOT_QUALIFIED_FAIL_CLOSED", "outside-envelope fail-closed guard lost")

    p = evidence["natural_P_envelope"]
    pmin = float(p["min"])
    pmax = float(p["max"])
    require(0.0 < pmin < pmax < 1.0e-6, "unexpected natural P envelope")
    require(p["records"] == 1238 and p["cases"] == 6, "natural reachability pin changed")

    u = 2.0 ** -53
    pD = D(pmax)
    f_degree1_bound = pD**2 / D(math.factorial(3))
    g_degree1_bound = pD**2 / D(math.factorial(4))
    f_degree2_bound = pD**3 / D(math.factorial(4))
    g_degree2_bound = pD**3 / D(math.factorial(5))
    require(f_degree1_bound > D(u), "degree 1 unexpectedly meets binary64 truncation criterion")
    require(g_degree1_bound > D(u), "degree 1 g unexpectedly meets binary64 truncation criterion")
    require(f_degree2_bound < D(u), "degree 2 f does not meet binary64 truncation criterion")
    require(g_degree2_bound < D(u), "degree 2 g does not meet binary64 truncation criterion")

    # Natural quantile matrix and independent high-precision reproduction.
    rows = list(csv.DictReader(NATURAL.open(encoding="utf-8")))
    require([r["point"] for r in rows] == ["min", "p01", "p25", "median", "p75", "p99", "max"], "natural matrix points changed")
    for row in rows:
        x = float(row["P"])
        f_ref_d, g_ref_d = exact_decimal(x)
        f_ref = float(f_ref_d)
        g_ref = float(g_ref_d)
        f, g = series64(x, 2)
        require(f == f_ref, f"series2 f does not round to oracle at {row['point']}")
        require(g == g_ref, f"series2 g does not round to oracle at {row['point']}")

    # Dense full-envelope reproduction. No fitted tolerance is used: selected
    # binary64 series must equal the rounded 100-digit oracle at every probe.
    for x in dense_grid(pmin, pmax):
        f_ref_d, g_ref_d = exact_decimal(x)
        f, g = series64(x, 2)
        require(f == float(f_ref_d), f"dense f mismatch at P={x}")
        require(g == float(g_ref_d), f"dense g mismatch at P={x}")

    pmed = float(p["median"])
    a1 = math.exp(-pmed)
    require(1.0 - a1 == 0.0, "raw binary64 cancellation at median no longer reproduces")
    f_direct = (1.0 - a1) / pmed
    g_direct = (1.0 - f_direct) / pmed
    require(f_direct == 0.0 and g_direct > 1.0e17, "legacy nested failure mode not reproduced")
    f_expm1 = -math.expm1(-pmed) / pmed
    g_expm1_nested = (1.0 - f_expm1) / pmed
    require(f_expm1 == 1.0, "expm1 f should recover the median-P rounded limit")
    require(g_expm1_nested == 0.0, "expm1 alone should expose unresolved second cancellation at median P")

    # Conservation and semigroup checks use bounds derived from binary64 unit
    # roundoff, never from legacy or balance residual envelopes.
    probes = ((0.37, 0.0), (0.37, 0.23), (0.0, 0.23))
    max_balance = 0.0
    max_split = 0.0
    for x in dense_grid(pmin, pmax):
        for c0, lbar in probes:
            c1, cavg = apply_candidate(c0, lbar, x)
            max_balance = max(max_balance, abs((c1 - c0) - (lbar - x * cavg)))
            for n in (2, 4, 8, 16, 32):
                cs, avs = split_candidate(c0, lbar, x, n)
                max_split = max(max_split, abs(cs - c1), abs(avs - cavg))
    require(max_balance <= 8.0 * u, f"conservation exceeds binary64 roundoff-derived guard: {max_balance}")
    require(max_split <= 32.0 * u, f"subdivision sensitivity exceeds operation-count roundoff guard: {max_split}")

    cont = evidence["exact_zero_continuity"]
    require(cont["matches_UBQ01_exact_zero_limit"] is True, "zero-limit continuity lost")
    require(cont["TCD042_B1_redefined"] is False, "B1 was redefined")
    require(cont["P_equals_zero_inside_NQ03_scope"] is False, "exact zero leaked into E1 scope")

    for key, value in evidence["nonclaims"].items():
        require(value is False, f"unexpected admission or widened claim: {key}")
    for key, value in status["scope_guards"].items():
        if key.endswith("allowed"):
            require(value is False, f"forbidden policy enabled: {key}")
        else:
            require(value is False, f"forbidden mutation/admission claimed: {key}")

    trunc_rows = list(csv.DictReader(TRUNC.open(encoding="utf-8")))
    require(trunc_rows[2]["disposition_binary64_natural_envelope"] == "SELECT_MINIMAL_ORDER", "degree-2 selection record changed")
    precision_rows = list(csv.DictReader(PRECISION.open(encoding="utf-8")))
    require(any(r["method"] == "series_degree2" and r["precision"] == "binary64" and r["disposition"] == "SELECT" for r in precision_rows), "binary64 selected precision row missing")
    require(any(r["precision"] == "emulated_binary32" and r["disposition"] == "SENSITIVITY_ONLY_NOT_CANONICAL" for r in precision_rows), "binary32 noncanonical sensitivity row missing")

    scope_guard()
    print("NQ03 PASS: restricted TCD-042-E1 quadratic P-policy is numerically qualified for the observed natural envelope; no admission or production change")


if __name__ == "__main__":
    main()
