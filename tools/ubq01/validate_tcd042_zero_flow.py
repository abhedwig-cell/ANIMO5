#!/usr/bin/env python3
"""Fail-closed validation for ANIMO-UBQ01 / TCD-042 exact-zero atom.

The validator is deliberately restricted to the exact Flux == 0 Class-B atom.
Finite positive sub-threshold reachability is checked only to prove that it must
remain separate numerical-policy work. No tolerance, threshold change,
production correction or scientific admission is created here.
"""
from __future__ import annotations

import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 50

ROOT = Path(__file__).resolve().parents[2]
SCI = ROOT / "integration" / "animo-science"
ATOM = SCI / "TCD042_ZERO_FLOW_ATOMIZATION.json"
NATURAL = SCI / "TCD042_NATURAL_EXACT_ZERO_PROBE.json"
REACH = SCI / "TCD042_SUBTHRESHOLD_REACHABILITY.json"
STATUS = SCI / "ANIMO-UBQ01_STATUS.json"

DIRECT = {"Rsconhtop", "Rsconitop", "Avconhtop", "Avconitop"}


def D(value) -> Decimal:
    return Decimal(str(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    data = load(ATOM)
    natural = load(NATURAL)
    reach = load(REACH)
    status = load(STATUS)

    require(data["target"] == "TCD-042", "wrong atom target")
    require(data["scope"] == "EXACT_ZERO_THROUGHFLOW_ATOM_ONLY", "atom scope widened")
    require(data["classification"]["selected_candidate"] == "B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT", "unexpected exact-zero class")
    require(data["classification"]["class_A_accounting_only"].startswith("REJECTED"), "Class A must remain rejected for exact zero")
    require(data["classification"]["class_C_missing_state"].startswith("REJECTED"), "Class C must remain rejected for exact zero")
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
    require(load_nh4 * D(10000) * st == D(w["booked_NH4_kg_ha"]), "NH4 booked load mismatch")
    require(load_no3 * D(10000) * st == D(w["booked_NO3_kg_ha"]), "NO3 booked load mismatch")
    require((load_nh4 + load_no3) * D(10000) * st == D(w["booked_total_N_kg_ha"]), "total N booked load mismatch")

    A1 = D(1)
    A2 = st / h
    B1 = D(1)
    B2 = st / (D(2) * h)
    require(A1 == D(data["exact_zero_limit"]["A1"]), "A1 zero limit mismatch")
    require(B1 == D(data["exact_zero_limit"]["B1"]), "B1 zero limit mismatch")

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
    require(h * c1_nh4 == h * c0_nh4 + st * load_nh4, "NH4 zero-flow storage identity failed")
    require(h * c1_no3 == h * c0_no3 + st * load_no3, "NO3 zero-flow storage identity failed")

    legacy_residual_nh4 = h * c0_nh4 + st * load_nh4 - h * c0_nh4
    legacy_residual_no3 = h * c0_no3 + st * load_no3 - h * c0_no3
    require(legacy_residual_nh4 == st * load_nh4, "NH4 legacy residual is not exactly the input load")
    require(legacy_residual_no3 == st * load_no3, "NO3 legacy residual is not exactly the input load")
    require(c0_no3 + D(0) * A2 == c0_no3, "zero-load synthetic non-interference failed")

    require(natural["target"] == "TCD-042", "natural probe target mismatch")
    require(natural["scope"] == "EXACT_ZERO_THROUGHFLOW_MINERAL_N_ATOM_NATURAL_ISOLATED_PROBE", "natural probe scope widened")
    require(natural["case"]["name"] == "RuurloGrass", "unexpected natural case")
    require(natural["case"]["records_before_first_difference"] == 1914, "natural pre-difference horizon mismatch")
    require(natural["case"]["first_difference_TITO"] == 1915.0, "natural first difference is not TITO 1915")
    require(natural["case"]["all_prior_trace_records_bitwise_equal"] is True, "pre-witness records are not bitwise equal")
    first = natural["first_difference"]
    require(set(first["actual_different_coordinates"]) == DIRECT, "unexpected direct coordinates differ at first witness")
    require(first["only_predeclared_direct_surfaces_differ"] is True, "first difference escaped predeclared direct surfaces")
    require(first["forcing_and_hydrology_trace_coordinates_equal"] is True, "forcing/hydrology changed at first witness")
    require(first["preexisting_top_state_equal"] is True, "beginning top state differs before correction")
    require(first["layer1_state_equal_at_immediate_post_UBoundconc_trace"] is True, "layer1 changed before causal propagation")
    require(first["all_formula_predictions_bitwise_equal"] is True, "natural corrected values do not equal formula bitwise")
    require(all(first["formula_prediction_bitwise_equal"].values()), "one natural formula prediction is not bitwise equal")
    require(natural["negative_controls"]["exact_zero_zero_load"]["trace_record_bitwise_equal"] is True, "natural zero-load control changed")
    require(natural["negative_controls"]["ordinary_positive_flow"]["trace_record_bitwise_equal"] is True, "natural positive-flow control changed")
    require(natural["comparison_policy"] == "EXACT_BITWISE_NO_TOLERANCE", "natural comparison policy weakened")
    require(natural["admission"]["b3_admitted"] is False, "natural probe may not admit B3")
    require(natural["build"]["production_source_modified"] is False, "natural probe may not modify production source")

    require(reach["target"] == "TCD-042", "reachability target mismatch")
    require(reach["range"] == "0<Flux<1.0d-8", "reachability range mismatch")
    summary = reach["summary"]
    require(summary["executed_cases_with_trace"] == 8, "unexpected executed reachability case count")
    require(summary["blocked_cases_without_trace"] == 1, "unexpected blocked reachability case count")
    require(summary["no_ponding_records_scanned"] == 15043, "reachability scan record count mismatch")
    require(summary["exact_zero_records"] == 5370, "exact-zero reachability count mismatch")
    require(summary["finite_positive_subthreshold_records"] == 1238, "finite-positive subthreshold count mismatch")
    require(summary["cases_with_finite_positive_subthreshold"] == 6, "finite-positive case count mismatch")
    require(reach["classification"]["reachable"] is True, "finite-positive subthreshold seam must remain recorded reachable")
    require(reach["classification"]["provisional_class"] == "E_NUMERICAL_POLICY", "reachable finite-positive seam must remain numerical-policy work")
    require(reach["classification"]["included_in_exact_zero_class_B_atom"] is False, "numerical seam silently composed into exact-zero atom")
    require(reach["classification"]["new_tcd_reserved"] is False, "validator may not reserve a new TCD")
    require(reach["classification"]["canonical_child_created"] is False, "validator may not create a canonical child")

    require(status["scope"]["finite_positive_subthreshold_flux_included"] is False, "status silently includes finite-positive seam")
    require(status["admission"]["b3_admitted"] is False, "status may not admit B3")
    require(status["admission"]["corrected_legacy_admitted"] is False, "status may not admit corrected legacy")
    require(status["admission"]["production_migration_admitted"] is False, "status may not admit production migration")

    print("UBQ01 validation PASS: exact-zero Class-B atom exact; natural first difference isolated; finite-positive seam reachable and separate")


if __name__ == "__main__":
    main()
