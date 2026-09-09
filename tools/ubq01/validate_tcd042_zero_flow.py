#!/usr/bin/env python3
"""Fail-closed exact-zero oracle for ANIMO-UBQ01 / TCD-042.

This validator is deliberately restricted to Flux == 0. It introduces no tolerance,
no positive-subthreshold policy, and no production correction.
"""
from __future__ import annotations

import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 50

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "integration" / "animo-science" / "TCD042_ZERO_FLOW_ATOMIZATION.json"


def D(value) -> Decimal:
    return Decimal(str(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    require(data["target"] == "TCD-042", "wrong target")
    require(data["scope"] == "EXACT_ZERO_THROUGHFLOW_ATOM_ONLY", "scope widened")
    require(data["classification"]["selected_candidate"] == "B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT", "unexpected class")
    require(data["classification"]["class_A_accounting_only"].startswith("REJECTED"), "Class A must remain rejected")
    require(data["classification"]["class_C_missing_state"].startswith("REJECTED"), "Class C must remain rejected")
    require(data["existing_owner"]["present"] is True, "existing upper-reservoir owner missing")
    require(data["finite_positive_subthreshold"]["included_in_exact_zero_atom"] is False, "positive sub-threshold seam silently included")
    require(data["finite_positive_subthreshold"]["tolerance_or_threshold_change_admitted"] is False, "threshold/tolerance change admitted")
    require(data["admission"]["b3_admitted"] is False, "validator may not admit B3")
    require(data["admission"]["source_correction_implemented"] is False, "validator may not claim source correction")

    w = data["natural_witness"]
    require(D(w["Flux"]) == 0, "natural witness must be exact zero throughflow")

    pr = D(w["Pr_m_d"])
    c_nh4 = D(w["Coprnhyn_kg_m3"])
    c_no3 = D(w["Coprniyn_kg_m3"])
    st = D(w["St_d"])
    h = D(w["Hetop_m"])
    require(h > 0 and st > 0, "invalid reservoir geometry or timestep")

    load_nh4 = pr * c_nh4
    load_no3 = pr * c_no3
    require(load_nh4 == D("5.069031338e-7"), "NH4 load does not reproduce exactly")
    require(load_no3 == D("1.68034188e-7"), "NO3 load does not reproduce exactly")
    require(load_nh4 == D(w["NH4_load_kg_m2_d"]), "persisted NH4 load mismatch")
    require(load_no3 == D(w["NO3_load_kg_m2_d"]), "persisted NO3 load mismatch")

    # Unit conversion only, exactly 1 kg/m2 = 10000 kg/ha.
    require(load_nh4 * D(10000) * st == D(w["booked_NH4_kg_ha"]), "NH4 booked load mismatch")
    require(load_no3 * D(10000) * st == D(w["booked_NO3_kg_ha"]), "NO3 booked load mismatch")
    require((load_nh4 + load_no3) * D(10000) * st == D(w["booked_total_N_kg_ha"]), "total N booked load mismatch")

    # Exact mathematical zero-flow coefficients recovered as limits.
    A1 = D(1)
    A2 = st / h
    B1 = D(1)
    B2 = st / (D(2) * h)
    require(A1 == D(data["exact_zero_limit"]["A1"]), "A1 zero limit mismatch")
    require(B1 == D(data["exact_zero_limit"]["B1"]), "B1 zero limit mismatch")

    # Use arbitrary beginning concentrations so the oracle cannot pass only at C0=0.
    c0_nh4 = D("0.003141592653589793")
    c0_no3 = D("0.001414213562373095")

    c1_nh4 = c0_nh4 * A1 + load_nh4 * A2
    c1_no3 = c0_no3 * A1 + load_no3 * A2
    cavg_nh4 = c0_nh4 * B1 + load_nh4 * B2
    cavg_no3 = c0_no3 * B1 + load_no3 * B2

    require(c1_nh4 - c0_nh4 == D(w["zero_limit_NH4_end_increment_kg_m3"]), "NH4 end increment mismatch")
    require(c1_no3 - c0_no3 == D(w["zero_limit_NO3_end_increment_kg_m3"]), "NO3 end increment mismatch")
    require(cavg_nh4 - c0_nh4 == D(w["zero_limit_NH4_average_increment_kg_m3"]), "NH4 average increment mismatch")
    require(cavg_no3 - c0_no3 == D(w["zero_limit_NO3_average_increment_kg_m3"]), "NO3 average increment mismatch")

    # Exact storage identity at Flux=0. No epsilon is allowed.
    require(h * c1_nh4 == h * c0_nh4 + st * load_nh4, "NH4 zero-flow storage identity failed")
    require(h * c1_no3 == h * c0_no3 + st * load_no3, "NO3 zero-flow storage identity failed")

    # Legacy fallback A2=B2=0 leaves precisely the source load outside represented end storage.
    legacy_c1_nh4 = c0_nh4
    legacy_c1_no3 = c0_no3
    legacy_residual_nh4 = h * c0_nh4 + st * load_nh4 - h * legacy_c1_nh4
    legacy_residual_no3 = h * c0_no3 + st * load_no3 - h * legacy_c1_no3
    require(legacy_residual_nh4 == st * load_nh4, "NH4 legacy residual is not exactly the input load")
    require(legacy_residual_no3 == st * load_no3, "NO3 legacy residual is not exactly the input load")

    # Zero-load negative control: corrected and legacy exact-zero states coincide.
    zero = D(0)
    corrected_zero_load = c0_no3 + zero * A2
    legacy_zero_load = c0_no3
    require(corrected_zero_load == legacy_zero_load, "zero-load non-interference control failed")

    print("UBQ01 exact-zero oracle PASS: existing owner + unique zero-flow limit + exact conservation; no tolerance")


if __name__ == "__main__":
    main()
