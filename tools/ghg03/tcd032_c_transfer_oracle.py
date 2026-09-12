#!/usr/bin/env python3
from fractions import Fraction

FAMILIES = ("DOM", "EXUDATE", "HUMUS_BIOMASS", "FRESH_OM_1", "FRESH_OM_2")


def transfer(q, dt, fc, a):
    assert q >= 0
    assert dt > 0
    assert fc > 0
    assert 0 <= a < 1
    if q == 0:
        return Fraction(0), Fraction(0)
    gross = q * dt / (fc * (1 - a))
    incorp = a * gross
    return gross, incorp


def family_identity(q, dt, fc, a):
    g, i = transfer(q, dt, fc, a)
    return fc * (g - i) == q * dt


def run_case(qs, dt, fc, aa):
    assert set(qs) == set(FAMILIES)
    assert set(aa) == set(FAMILIES)
    assert aa["HUMUS_BIOMASS"] == 0
    total_q = sum(qs.values(), Fraction(0))
    net_c = Fraction(0)
    for fam in FAMILIES:
        q = qs[fam]
        a = aa[fam]
        assert family_identity(q, dt, fc, a), fam
        g, i = transfer(q, dt, fc, a)
        net_c += fc * (g - i)
    assert net_c == total_q * dt
    return total_q, net_c


def main():
    dts = [Fraction(1, 24), Fraction(1, 1), Fraction(7, 3)]
    fcs = [Fraction(2, 5), Fraction(1, 2), Fraction(3, 5)]
    qsets = [
        {f: Fraction(0) for f in FAMILIES},
        {"DOM": Fraction(1, 100), "EXUDATE": Fraction(0), "HUMUS_BIOMASS": Fraction(0), "FRESH_OM_1": Fraction(0), "FRESH_OM_2": Fraction(0)},
        {"DOM": Fraction(1, 100), "EXUDATE": Fraction(3, 200), "HUMUS_BIOMASS": Fraction(1, 250), "FRESH_OM_1": Fraction(7, 500), "FRESH_OM_2": Fraction(11, 1000)},
        {"DOM": Fraction(13, 1000), "EXUDATE": Fraction(17, 1000), "HUMUS_BIOMASS": Fraction(19, 1000), "FRESH_OM_1": Fraction(23, 1000), "FRESH_OM_2": Fraction(29, 1000)},
    ]
    aset = [
        {"DOM": Fraction(0), "EXUDATE": Fraction(0), "HUMUS_BIOMASS": Fraction(0), "FRESH_OM_1": Fraction(0), "FRESH_OM_2": Fraction(0)},
        {"DOM": Fraction(1, 10), "EXUDATE": Fraction(1, 4), "HUMUS_BIOMASS": Fraction(0), "FRESH_OM_1": Fraction(2, 5), "FRESH_OM_2": Fraction(3, 5)},
        {"DOM": Fraction(19, 20), "EXUDATE": Fraction(9, 10), "HUMUS_BIOMASS": Fraction(0), "FRESH_OM_1": Fraction(7, 8), "FRESH_OM_2": Fraction(1, 3)},
    ]
    cases = 0
    for dt in dts:
        for fc in fcs:
            for qs in qsets:
                for aa in aset:
                    run_case(qs, dt, fc, aa)
                    cases += 1

    # Active negative control 1: duplicating the DOM debit must break the ledger.
    q = Fraction(1, 100)
    dt = Fraction(1)
    fc = Fraction(1, 2)
    a = Fraction(1, 4)
    g, i = transfer(q, dt, fc, a)
    correct = fc * (g - i)
    duplicated_dom_debit = fc * ((g + g) - i)
    assert correct == q * dt
    assert duplicated_dom_debit != q * dt

    # Active negative control 2: dropping the matching internal credit must over-debit C.
    missing_credit = fc * g
    assert missing_credit != q * dt

    # Domain guards.
    bad = [
        (Fraction(-1, 10), dt, fc, a),
        (q, Fraction(0), fc, a),
        (q, dt, Fraction(0), a),
        (q, dt, fc, Fraction(-1, 10)),
        (q, dt, fc, Fraction(1)),
    ]
    for args in bad:
        try:
            transfer(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError("domain guard failed: %r" % (args,))

    print("TCD032 carbon-transfer ownership oracle PASS")
    print("cases", cases)
    print("arithmetic EXACT_RATIONAL_NO_TOLERANCE")
    print("negative_control_double_DOM_debit PASS")
    print("negative_control_missing_internal_credit PASS")
    print("historical_behavior UNKNOWN_WITHOUT_B2")


if __name__ == "__main__":
    main()
