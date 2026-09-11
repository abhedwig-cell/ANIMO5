#!/usr/bin/env python3
import math

PARAMS = {
    "CH4": (0.00134, 1750.0),
    "N2O": (0.0245, 2600.0),
}


def alpha_bunsen(gas, temp_c):
    kh0, esdvr = PARAMS[gas]
    tk = max(273.15, temp_c + 273.15)
    return kh0 * math.exp(esdvr * (1.0 / tk - 1.0 / 298.15)) * tk / 12.2


def reciprocal_bunsen(gas, temp_c):
    return 1.0 / alpha_bunsen(gas, temp_c)


def aqueous_from_total(gas, cs, theta, theta_sat, temp_c):
    if theta < 0.0 or theta_sat < theta:
        raise ValueError("invalid hydrology coordinate")
    denom = theta + reciprocal_bunsen(gas, temp_c) * (theta_sat - theta)
    if denom <= 0.0:
        raise ValueError("non-positive phase denominator")
    return cs / denom


def witness(gas, cs, theta, theta_sat, checkpoint_temp_c, terf_c):
    continuous = aqueous_from_total(gas, cs, theta, theta_sat, checkpoint_temp_c)
    qualified_restart = aqueous_from_total(gas, cs, theta, theta_sat, checkpoint_temp_c)
    legacy_restart = aqueous_from_total(gas, cs, theta, theta_sat, terf_c)
    return {
        "gas": gas,
        "cs": cs,
        "theta": theta,
        "theta_sat": theta_sat,
        "checkpoint_temp_c": checkpoint_temp_c,
        "terf_c": terf_c,
        "continuous": continuous,
        "qualified_restart": qualified_restart,
        "legacy_restart": legacy_restart,
        "qualified_error": qualified_restart - continuous,
        "legacy_error": legacy_restart - continuous,
    }


def generated_cases():
    cases = []
    for gas in ("CH4", "N2O"):
        for cs in (0.0, 1.0e-8, 2.5e-4):
            for theta, theta_sat in ((0.12, 0.45), (0.30, 0.45), (0.45, 0.45)):
                for checkpoint_temp_c, terf_c in ((5.0, 10.0), (25.0, 10.0), (10.0, 10.0), (-5.0, 10.0)):
                    cases.append(witness(gas, cs, theta, theta_sat, checkpoint_temp_c, terf_c))
    return cases


def validate_cases():
    cases = generated_cases()
    nontrivial = 0
    equality_controls = 0
    for c in cases:
        if c["qualified_error"] != 0.0:
            raise AssertionError(f"qualified reconstruction mismatch: {c}")
        rb_cp = reciprocal_bunsen(c["gas"], c["checkpoint_temp_c"])
        rb_ref = reciprocal_bunsen(c["gas"], c["terf_c"])
        equality_expected = (
            c["cs"] == 0.0
            or c["theta_sat"] == c["theta"]
            or rb_cp == rb_ref
        )
        equal_observed = c["legacy_restart"] == c["continuous"]
        if equality_expected:
            equality_controls += 1
            if not equal_observed:
                raise AssertionError(f"exact continuity control failed: {c}")
        else:
            nontrivial += 1
            if equal_observed:
                raise AssertionError(f"Terf unexpectedly equivalent outside continuity controls: {c}")
    if nontrivial == 0 or equality_controls == 0:
        raise AssertionError("oracle lacks positive or negative controls")
    if reciprocal_bunsen("CH4", 25.0) == reciprocal_bunsen("N2O", 25.0):
        raise AssertionError("species-specific Bunsen contracts collapsed")
    return {"cases": len(cases), "nontrivial_divergence_cases": nontrivial, "equality_controls": equality_controls}


if __name__ == "__main__":
    print(validate_cases())
