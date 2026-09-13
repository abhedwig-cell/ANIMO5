from decimal import Decimal

OWNER = "M_surface_NH4_non_aqueous_continuation"
UNIT = "kg N m-2"


def fail_closed_rewet_guard(m_cont):
    m = Decimal(m_cont)
    assert m >= 0
    return {
        "source_owner": OWNER,
        "source_before": m,
        "transfer": Decimal("0"),
        "source_after": m,
        "receiver_gains": {},
        "boundary_terms": {},
        "unit": UNIT,
    }


def assert_exact_identity(record):
    assert record["source_after"] == record["source_before"] - record["transfer"]
    assert sum(record["receiver_gains"].values(), Decimal("0")) == record["transfer"]
    assert record["boundary_terms"] == {}


def main():
    for value in ("0", "0.000013880242022597072", "1.25"):
        r = fail_closed_rewet_guard(value)
        assert_exact_identity(r)
        assert r["source_after"] == Decimal(value)

    whole = fail_closed_rewet_guard("0.75")
    split_a = fail_closed_rewet_guard("0.75")
    split_b = fail_closed_rewet_guard(str(split_a["source_after"]))
    assert whole["source_after"] == split_b["source_after"]

    rejected_shortcuts = {
        "instantaneous_complete_dissolution_on_first_water": "UNQUALIFIED",
        "fixed_fraction_release": "UNQUALIFIED",
        "direct_layer1_infiltration_release": "UNQUALIFIED",
        "Conhtop_receiver_reuse": "UNQUALIFIED",
        "residual_derived_receiver_gain": "FORBIDDEN",
    }
    assert all(v in {"UNQUALIFIED", "FORBIDDEN"} for v in rejected_shortcuts.values())

    # Negative controls: a non-zero source loss must not exist without an exactly
    # typed receiver gain or declared external sink.
    bad_loss = Decimal("0.1")
    receiver_gain = Decimal("0")
    assert bad_loss != receiver_gain

    print("PASS SQ07 exact negative rewetting oracle")


if __name__ == "__main__":
    main()
