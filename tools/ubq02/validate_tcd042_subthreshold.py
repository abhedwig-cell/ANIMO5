#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-UBQ02.

This validates the persisted finite-positive subthreshold characterization and a
small independent numerical reproduction of the cancellation claims. It does
not regenerate the B0 execution traces and it cannot admit numerical policy.
"""
from __future__ import annotations

import json
import math
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 80

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "integration" / "animo-science" / "TCD042_SUBTHRESHOLD_NUMERICAL_CHARACTERIZATION.json"
STATUS = ROOT / "integration" / "animo-science" / "ANIMO-UBQ02_STATUS.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def D(value) -> Decimal:
    return Decimal(str(value))


def f_series_float(p: float) -> float:
    return 1.0 - p / 2.0 + p * p / 6.0 - p**3 / 24.0 + p**4 / 120.0


def g_series_float(p: float) -> float:
    return 0.5 - p / 6.0 + p * p / 24.0 - p**3 / 120.0 + p**4 / 720.0


def exact_decimal(p: float) -> tuple[Decimal, Decimal]:
    x = D(p)
    e = (-x).exp()
    f = (D(1) - e) / x
    g = (x - D(1) + e) / (x * x)
    return f, g


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    require(data["work_unit"] == "ANIMO-UBQ02", "wrong workunit")
    require(data["target_parent"] == "TCD-042", "wrong parent")
    require(data["scope"] == "0<Flux<1.0d-8, Flpn=0", "scope widened")
    require(data["evidence_class"].endswith("NOT_B2"), "diagnostic evidence promoted to B2")
    require(data["base"]["exact_zero_atom_qualified"] is True, "UBQ01 exact-zero prerequisite lost")

    execution = data["execution"]
    require(execution["instrumentation_only"] is True, "execution must remain instrumentation-only")
    require(execution["production_source_modified"] is False, "production source mutation claimed")
    require(execution["invocation_contract"] == "animo_trace Animo.ini", "direct-file invocation contract changed")
    require(execution["cases_total"] == 9, "wrong testbank case count")
    require(execution["successful_cases"] == 8, "wrong successful case count")
    require(execution["blocked_cases"] == 1, "wrong blocked case count")
    counts = execution["case_counts"]
    require(sum(counts.values()) == 1238, "subthreshold per-case counts do not sum to 1238")
    require(sum(value > 0 for value in counts.values()) == 6, "wrong number of cases with subthreshold reachability")
    require(counts["RuurloGrass"] == 191, "Ruurlo subthreshold count changed")
    require(counts["GHGMais"] == 0, "GHGMais must not acquire an absence-bearing trace")
    require("NO_ABSENCE_CLAIM" in execution["GHGMais"], "GHGMais fail-closed note missing")

    reach = data["reachability"]
    require(reach["records"] == 1238 and reach["cases"] == 6, "reachability summary mismatch")
    p = reach["P_distribution"]
    require(0.0 < p["min"] <= p["median"] <= p["max"] < 1.0e-6, "unexpected P envelope")

    legacy = data["legacy_fallback"]
    require(legacy["trigger"] == "Flux<1.0d-8", "legacy trigger changed")
    require([legacy[k] for k in ("A1", "A2", "B1", "B2")] == [1, 0, 1, 0], "legacy fallback coefficients changed")
    require(legacy["local_signed_residual"] == "St*(Load-Flux*C0)", "legacy local residual identity changed")

    direct = data["binary64_direct_formula"]
    require(direct["records"] == 1238, "direct-form test count mismatch")
    require(direct["one_minus_exp_zero"] == 1189, "binary64 cancellation count changed")
    require(direct["f_records_gt_1pct"] == 1189, "f error-count changed")
    require(direct["g_records_gt_1pct"] == 1206, "g error-count changed")

    # Independent cancellation reproduction at the persisted median P.
    pmid = float(p["median"])
    require(1.0 - math.exp(-pmid) == 0.0, "median-P raw binary64 cancellation no longer reproduces")

    # Independent high-precision check at the largest observed P. The local
    # fourth-order series is only a comparison method inside this envelope.
    pmax = float(p["max"])
    f_ref_d, g_ref_d = exact_decimal(pmax)
    f_ref = float(f_ref_d)
    g_ref = float(g_ref_d)
    f_rel = abs(f_series_float(pmax) - f_ref) / abs(f_ref)
    g_rel = abs(g_series_float(pmax) - g_ref) / abs(g_ref)
    require(f_rel <= 2.0e-16, f"f series exceeds binary64 comparison envelope: {f_rel}")
    require(g_rel <= 2.0e-16, f"g series exceeds binary64 comparison envelope: {g_rel}")

    stable = data["stable_comparison_candidate"]
    require(stable["selected_policy"] is False, "comparison method promoted to selected policy")
    require(stable["envelope"] == "observed P range only", "comparison envelope widened")
    require(stable["binary64_max_relative_error_f"] <= 2.0e-16, "persisted f comparison error too large")
    require(stable["binary64_max_relative_error_g"] <= 2.0e-16, "persisted g comparison error too large")
    require(stable["binary32_max_relative_error_f"] > 1.0e-9, "precision sensitivity axis disappeared")
    require(stable["max_abs_conservation_roundoff_kg_ha"] < 1.0e-12, "comparison conservation roundoff unexpectedly large")

    material = data["natural_materiality"]
    require(material["nonzero_mineral_N_load_records"] == 4, "wrong loaded N record count")
    require(material["nonzero_load_TITO"] == [527, 533, 595, 847], "loaded-event identity changed")
    require(material["mineral_N_signed_local_residual_sum_kg_ha"] > 0.0168, "natural N materiality lost")
    require(material["RuurloGrass_max_abs_single_record_N_residual_kg_ha"] > 0.0067, "Ruurlo witness materiality lost")
    require(material["P_load_nonzero_records"] == 0, "unexpected P loaded-event claim")
    require(material["DOM_load_nonzero_records"] == 0, "unexpected DOM loaded-event claim")
    require(material["DON_load_nonzero_records"] == 0, "unexpected DON loaded-event claim")

    classification = data["classification"]
    require(classification["provisional_class"] == "E_NUMERICAL_POLICY", "finite-positive seam class changed")
    require(classification["exact_zero_Class_B_reopened"] is False, "UBQ01 exact-zero atom reopened")
    require(classification["parent_tcd_fully_qualified"] is False, "parent TCD-042 incorrectly closed")
    require(classification["canonical_incremental_intake_recommended"] is True, "canonical intake recommendation lost")
    require(classification["new_tcd_reserved"] is False, "UBQ02 may not reserve a TCD")
    require(classification["canonical_child_created"] is False, "UBQ02 may not create a canonical child")

    for key, value in data["admission"].items():
        require(value is False, f"unexpected admission: {key}")
    for key, value in status["admission"].items():
        require(value is False, f"status unexpectedly admits {key}")

    print("UBQ02 PASS: finite-positive seam is natural, material and numerically cancellation-sensitive; Class-E route remains unadmitted")


if __name__ == "__main__":
    main()
