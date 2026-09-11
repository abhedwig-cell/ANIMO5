#!/usr/bin/env python3


def restart_layer0(cs0, ponding_active, pn, new_event_value=None):
    if not ponding_active:
        return {"owner": 0.0, "co0": 0.0, "mode": "NO_PONDING"}
    if pn < 1.0e-4:
        if new_event_value is None:
            raise ValueError("new ponding event requires source inflow initialization value")
        return {"owner": cs0, "co0": new_event_value, "mode": "NEW_PONDING_SOURCE_INITIALIZATION"}
    return {"owner": cs0, "co0": cs0, "mode": "PRE_EXISTING_PONDING_RESTART_IDENTITY"}


def zero_reset_legacy_view(cs0, ponding_active, pn, new_event_value=None):
    if not ponding_active:
        return 0.0
    if pn < 1.0e-4:
        if new_event_value is None:
            raise ValueError("new ponding event requires source inflow initialization value")
        return new_event_value
    return 0.0


def generated_cases():
    cases = []
    for gas in ("CH4", "N2O"):
        for cs0 in (0.0, 1.0e-8, 2.5e-4, 0.2):
            for pn in (0.0, 5.0e-5, 1.0e-4, 1.0e-3):
                new_value = 7.0e-5 if pn < 1.0e-4 else None
                q = restart_layer0(cs0, True, pn, new_value)
                legacy = zero_reset_legacy_view(cs0, True, pn, new_value)
                cases.append({"gas": gas, "cs0": cs0, "pn": pn, "qualified": q, "legacy": legacy})
        cases.append({"gas": gas, "cs0": 0.0, "pn": 0.0, "qualified": restart_layer0(9.0, False, 0.0), "legacy": zero_reset_legacy_view(9.0, False, 0.0)})
    return cases


def validate_cases():
    cases = generated_cases()
    pre_existing_nonzero = 0
    new_event_controls = 0
    absent_controls = 0
    zero_controls = 0
    for c in cases:
        q = c["qualified"]
        if q["mode"] == "PRE_EXISTING_PONDING_RESTART_IDENTITY":
            if q["co0"] != c["cs0"]:
                raise AssertionError(f"identity reconstruction failed: {c}")
            if c["cs0"] == 0.0:
                zero_controls += 1
                if c["legacy"] != q["co0"]:
                    raise AssertionError(f"zero control mismatch: {c}")
            else:
                pre_existing_nonzero += 1
                if c["legacy"] == q["co0"]:
                    raise AssertionError(f"zero-reset negative control not discriminating: {c}")
        elif q["mode"] == "NEW_PONDING_SOURCE_INITIALIZATION":
            new_event_controls += 1
            if q["co0"] != c["legacy"]:
                raise AssertionError(f"new-event source rule must be preserved: {c}")
        elif q["mode"] == "NO_PONDING":
            absent_controls += 1
            if q["co0"] != 0.0 or q["owner"] != 0.0:
                raise AssertionError(f"absent ponding must not create dormant state: {c}")
        else:
            raise AssertionError(f"unknown mode: {c}")
    if not pre_existing_nonzero or not new_event_controls or not absent_controls or not zero_controls:
        raise AssertionError("oracle control bank incomplete")
    # Species are intentionally carried independently through the same physical identity.
    gas_set = {c["gas"] for c in cases}
    if gas_set != {"CH4", "N2O"}:
        raise AssertionError("species coverage incomplete")
    return {
        "cases": len(cases),
        "pre_existing_nonzero_divergence_cases": pre_existing_nonzero,
        "new_event_controls": new_event_controls,
        "absent_ponding_controls": absent_controls,
        "zero_gas_controls": zero_controls,
    }


if __name__ == "__main__":
    print(validate_cases())
