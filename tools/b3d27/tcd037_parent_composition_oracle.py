#!/usr/bin/env python3
"""Independent parent-level composition oracle for ANIMO-B3D27.

This is a bounded exact-rational accounting oracle. It does not execute ANIMO,
does not emulate GHG physics, and does not create historical B2 evidence. The
source-owned semantic contract comes from the pinned RUNTIMEQ03 authority; this
oracle tests only the new parent-level composition rules and noninterference.
"""

from fractions import Fraction as F

Z = F(10000)
CFRACOM = F(1, 2)


def compose(*, st, ch4_form_rates, ch4_emit_rates, n2o_deni_rates, n2o_emit_rates,
            n2o_nitr_sentinel=F(17), n2o_reduction_sentinel=F(19), d_om=F(16)):
    ch4_layers = tuple(q * st for q in ch4_form_rates)
    ch4_form_total = sum(ch4_layers, F(0))
    ch4_emit_total = sum(ch4_emit_rates, F(0)) * st
    n2o_deni_layers = tuple(Z * q * st for q in n2o_deni_rates)
    n2o_emit_total = Z * sum(n2o_emit_rates, F(0)) * st
    return {
        "ch4_layer_formation": ch4_layers,
        "Btom_CH4e": Z * ch4_emit_total / CFRACOM,
        "Btom_CO2e": d_om - Z * ch4_form_total / CFRACOM,
        "Bani_N2Od": n2o_deni_layers,
        "Bani_N2Oe": n2o_emit_total,
        "n2o_nitr_sentinel": n2o_nitr_sentinel,
        "n2o_reduction_sentinel": n2o_reduction_sentinel,
    }


def main():
    st = F(1, 4)
    base = compose(
        st=st,
        ch4_form_rates=(F(1, 16384), F(1, 8192), F(3, 16384)),
        ch4_emit_rates=(F(1, 32768), F(1, 16384), F(1, 32768), F(0)),
        n2o_deni_rates=(F(1, 4096), F(3, 8192), F(1, 8192)),
        n2o_emit_rates=(F(1, 16384), F(-1, 32768)),
    )

    # Formation and atmosphere exchange are deliberately independent.
    emit_flip = compose(
        st=st,
        ch4_form_rates=(F(1, 16384), F(1, 8192), F(3, 16384)),
        ch4_emit_rates=(F(-1, 32768), F(-1, 16384), F(-1, 32768), F(0)),
        n2o_deni_rates=(F(1, 4096), F(3, 8192), F(1, 8192)),
        n2o_emit_rates=(F(1, 16384), F(-1, 32768)),
    )
    assert emit_flip["ch4_layer_formation"] == base["ch4_layer_formation"]
    assert emit_flip["Btom_CO2e"] == base["Btom_CO2e"]
    assert emit_flip["Btom_CH4e"] == -base["Btom_CH4e"]

    form_change = compose(
        st=st,
        ch4_form_rates=(F(2, 16384), F(2, 8192), F(6, 16384)),
        ch4_emit_rates=(F(1, 32768), F(1, 16384), F(1, 32768), F(0)),
        n2o_deni_rates=(F(1, 4096), F(3, 8192), F(1, 8192)),
        n2o_emit_rates=(F(1, 16384), F(-1, 32768)),
    )
    assert form_change["Btom_CH4e"] == base["Btom_CH4e"]
    assert form_change["Btom_CO2e"] != base["Btom_CO2e"]

    # Signed N2O atmosphere exchange is independent from denitrification formation.
    n2o_emit_flip = compose(
        st=st,
        ch4_form_rates=(F(1, 16384), F(1, 8192), F(3, 16384)),
        ch4_emit_rates=(F(1, 32768), F(1, 16384), F(1, 32768), F(0)),
        n2o_deni_rates=(F(1, 4096), F(3, 8192), F(1, 8192)),
        n2o_emit_rates=(F(-1, 16384), F(1, 32768)),
    )
    assert n2o_emit_flip["Bani_N2Od"] == base["Bani_N2Od"]
    assert n2o_emit_flip["Bani_N2Oe"] == -base["Bani_N2Oe"]

    n2o_deni_change = compose(
        st=st,
        ch4_form_rates=(F(1, 16384), F(1, 8192), F(3, 16384)),
        ch4_emit_rates=(F(1, 32768), F(1, 16384), F(1, 32768), F(0)),
        n2o_deni_rates=(F(1, 2048), F(3, 4096), F(1, 4096)),
        n2o_emit_rates=(F(1, 16384), F(-1, 32768)),
    )
    assert n2o_deni_change["Bani_N2Oe"] == base["Bani_N2Oe"]
    assert n2o_deni_change["Bani_N2Od"] != base["Bani_N2Od"]

    # Parent composition must not consume or mutate nitrification/reduction context.
    for result in (base, emit_flip, form_change, n2o_emit_flip, n2o_deni_change):
        assert result["n2o_nitr_sentinel"] == F(17)
        assert result["n2o_reduction_sentinel"] == F(19)

    # Rate-time equivalence: halve all rates and double timestep.
    rate_time = compose(
        st=2 * st,
        ch4_form_rates=tuple(q / 2 for q in (F(1, 16384), F(1, 8192), F(3, 16384))),
        ch4_emit_rates=tuple(q / 2 for q in (F(1, 32768), F(1, 16384), F(1, 32768), F(0))),
        n2o_deni_rates=tuple(q / 2 for q in (F(1, 4096), F(3, 8192), F(1, 8192))),
        n2o_emit_rates=tuple(q / 2 for q in (F(1, 16384), F(-1, 32768))),
    )
    assert rate_time == base

    # No cross-element aggregate is defined by the parent contract.
    assert "ghg_total" not in base
    assert "climate_CO2e" not in base

    print("ANIMO-B3D27 parent composition oracle: PASS")


if __name__ == "__main__":
    main()
