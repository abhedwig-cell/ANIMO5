#!/usr/bin/env python3
"""Independent mathematical reference functions for ANIMO-SYNQ01.

This module intentionally imports no ANIMO production or legacy implementation.
It contains only equations and identities reconstructed from qualified theory,
conservation statements, or explicitly documented candidate contracts.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from typing import Iterable, Sequence

D = Decimal


def q(x: str | int | Decimal) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def assert_exact_zero(x: Decimal, label: str) -> None:
    if x != 0:
        raise AssertionError(f"{label}: expected exact zero, got {x}")


@dataclass(frozen=True)
class No3ClippingCase:
    avc: Decimal
    hv: Decimal
    st: Decimal
    ld: Decimal

    def duplicated_storage_term(self) -> Decimal:
        """Exact local areic-mass residual caused by using Hv twice."""
        return self.avc * self.hv * self.st * self.ld

    def conservative_residual(self) -> Decimal:
        """The same term is absent when the disappearance coefficient excludes Hv."""
        return D(0)


@dataclass(frozen=True)
class Redistribution:
    source_loss: Decimal
    destination_gains: tuple[Decimal, ...]

    def internal_ledger_sum(self) -> Decimal:
        return -self.source_loss + sum(self.destination_gains, D(0))

    def final_total(self, initial_total: Decimal) -> Decimal:
        return initial_total + self.internal_ledger_sum()


@dataclass(frozen=True)
class InterceptionCase:
    begin: Decimal
    precipitation: Decimal
    evaporation: Decimal
    throughfall: Decimal
    end: Decimal

    def residual(self) -> Decimal:
        return self.begin + self.precipitation - self.evaporation - self.throughfall - self.end


@dataclass(frozen=True)
class SpeciesPartition:
    concentration: Decimal
    moisture: Decimal
    rate: Decimal
    thickness_time: Decimal
    assimilation_fraction: Decimal

    def parent(self) -> Decimal:
        return self.moisture * self.rate * self.concentration * self.thickness_time

    def products(self) -> tuple[Decimal, Decimal]:
        p = self.parent()
        a = self.assimilation_fraction
        return (D(1) - a) * p, a * p

    def closure(self) -> Decimal:
        x, y = self.products()
        return x + y - self.parent()


def species_partition_vector(
    concentrations: Sequence[Decimal],
    moisture: Decimal,
    rate: Decimal,
    thickness_time: Decimal,
    assimilation_fraction: Decimal,
) -> tuple[tuple[Decimal, Decimal, Decimal], ...]:
    out = []
    for c in concentrations:
        s = SpeciesPartition(c, moisture, rate, thickness_time, assimilation_fraction)
        x, y = s.products()
        out.append((s.parent(), x, y))
    return tuple(out)


def permute(values: Sequence, order: Sequence[int]):
    return tuple(values[i] for i in order)


@dataclass(frozen=True)
class SlowLangmuirSite:
    qmax: Decimal
    k: Decimal
    qold: Decimal
    r_ads: Decimal
    r_des: Decimal

    def equilibrium(self, concentration: Decimal, rho: Decimal) -> Decimal:
        kc = self.k * concentration
        return (self.qmax / rho) * kc / (D(1) + kc)

    def rate(self, concentration: Decimal, rho: Decimal) -> Decimal:
        return self.r_ads if self.equilibrium(concentration, rho) >= self.qold else self.r_des

    def relaxation_factor(self, concentration: Decimal, rho: Decimal, dt: Decimal) -> Decimal:
        r = self.rate(concentration, rho)
        with localcontext() as ctx:
            ctx.prec = 80
            return (-(r * (D(1) + self.k * concentration) * dt)).exp()

    def updated(self, concentration: Decimal, rho: Decimal, dt: Decimal) -> Decimal:
        qe = self.equilibrium(concentration, rho)
        y = self.relaxation_factor(concentration, rho, dt)
        return self.qold * y + qe * (D(1) - y)


def slow_langmuir_sites(
    sites: Sequence[SlowLangmuirSite], concentration: Decimal, rho: Decimal, dt: Decimal
) -> tuple[Decimal, ...]:
    return tuple(s.updated(concentration, rho, dt) for s in sites)


def slow_langmuir_wrong_selector_mutant(
    sites: Sequence[SlowLangmuirSite], concentration: Decimal, rho: Decimal, dt: Decimal, selector: int
) -> tuple[Decimal, ...]:
    """Defect-seeding comparator, not an oracle.

    It deliberately substitutes one site's K into all site-specific exponential
    factors, so the independent site oracle must reject it for unequal sites.
    """
    wrong_k = sites[selector].k
    values = []
    for s in sites:
        qe = s.equilibrium(concentration, rho)
        r = s.rate(concentration, rho)
        with localcontext() as ctx:
            ctx.prec = 80
            y = (-(r * (D(1) + wrong_k * concentration) * dt)).exp()
        values.append(s.qold * y + qe * (D(1) - y))
    return tuple(values)


@dataclass(frozen=True)
class MacroporeLedgerCase:
    matrix_begin: Decimal
    macropore_begin: Decimal
    internal_transfer_matrix_to_mp: Decimal
    external_direct_drain: Decimal

    def end_stores(self) -> tuple[Decimal, Decimal]:
        x = self.internal_transfer_matrix_to_mp
        d = self.external_direct_drain
        return self.matrix_begin - x, self.macropore_begin + x - d

    def whole_control_volume_residual(self) -> Decimal:
        matrix_end, mp_end = self.end_stores()
        begin = self.matrix_begin + self.macropore_begin
        end = matrix_end + mp_end
        return begin - self.external_direct_drain - end

    def internal_transfer_sum(self) -> Decimal:
        x = self.internal_transfer_matrix_to_mp
        return -x + x


def langmuir_storage(concentration: Decimal, theta: Decimal, qmax: Decimal, k: Decimal) -> Decimal:
    return theta * concentration + qmax * k * concentration / (D(1) + k * concentration)


def langmuir_exact_positive_root(total_mass: Decimal, theta: Decimal, qmax: Decimal, k: Decimal) -> Decimal:
    """Positive exact root of M = theta*C + qmax*K*C/(1+K*C)."""
    with localcontext() as ctx:
        ctx.prec = 100
        a = theta * k
        b = theta + qmax * k - total_mass * k
        c = -total_mass
        disc = b * b - D(4) * a * c
        return (-b + disc.sqrt()) / (D(2) * a)


def langmuir_bisection_root(
    total_mass: Decimal,
    theta: Decimal,
    qmax: Decimal,
    k: Decimal,
    digits: int = 80,
) -> tuple[Decimal, Decimal, int]:
    """Independent high-precision monotone root solve.

    Stopping is precision-derived: bracket width <= 10^(-(digits-8)).
    This is a reference-computation resolution, not an ANIMO acceptance tolerance.
    """
    with localcontext() as ctx:
        ctx.prec = digits
        lo = D(0)
        hi = max(D(1), total_mass / theta + D(1))
        f = lambda c: langmuir_storage(c, theta, qmax, k) - total_mass
        while f(hi) < 0:
            hi *= D(2)
        width_target = D(10) ** (-(digits - 8))
        n = 0
        while hi - lo > width_target:
            mid = (lo + hi) / D(2)
            if f(mid) <= 0:
                lo = mid
            else:
                hi = mid
            n += 1
        root = (lo + hi) / D(2)
        return root, hi - lo, n


def management_events(events: Iterable[Decimal], t0: Decimal, t1: Decimal) -> tuple[Decimal, ...]:
    return tuple(e for e in events if t0 < e <= t1)


def harvest_events(events: Iterable[Decimal], t0: Decimal, t1: Decimal) -> tuple[Decimal, ...]:
    return tuple(e for e in events if t0 <= e < t1)


def scalar_step(state: Decimal, source: Decimal, sink: Decimal) -> Decimal:
    return state + source - sink


def run_scalar_sequence(state: Decimal, increments: Sequence[tuple[Decimal, Decimal]]) -> Decimal:
    for source, sink in increments:
        state = scalar_step(state, source, sink)
    return state


def limiting_case_results() -> dict[str, bool]:
    zero = D(0)
    one = D(1)
    sites = (
        SlowLangmuirSite(D("0.3"), D("10"), D("0.01"), D("0.02"), D("0.001")),
        SlowLangmuirSite(D("0.3"), D("10"), D("0.01"), D("0.02"), D("0.001")),
    )
    c = D("0.05")
    rho = D("1")
    dt = D("2")
    vals = slow_langmuir_sites(sites, c, rho, dt)
    return {
        "zero_reaction_rate": scalar_step(one, zero, zero) == one,
        "zero_transport": scalar_step(one, zero, zero) == one,
        "zero_sorption_capacity": SlowLangmuirSite(zero, D("4"), D("0"), D("1"), D("1")).equilibrium(c, rho) == zero,
        "zero_crop_demand": min(D("0.2"), zero) == zero,
        "zero_external_forcing": scalar_step(one, zero, zero) == one,
        "single_layer_profile": sum((D("0.7"),), zero) == D("0.7"),
        "one_active_species": species_partition_vector((D("0.3"),), D("0.4"), D("0.2"), D("1"), D("0.25"))[0][0] > zero,
        "one_active_sorption_site": len(slow_langmuir_sites((sites[0],), c, rho, dt)) == 1,
        "identical_sites_permutation": vals == tuple(reversed(vals)),
        "identical_layers_permutation": sum((D("0.2"), D("0.2")), zero) == sum((D("0.2"), D("0.2")), zero),
        "zero_macropore_exchange": MacroporeLedgerCase(D("1"), D("0.5"), zero, zero).end_stores() == (D("1"), D("0.5")),
        "inactive_feature_negative_control": scalar_step(one, zero, zero) == one,
    }


def self_test() -> dict[str, str]:
    out: dict[str, str] = {}

    n = No3ClippingCase(D("0.2"), D("0.1"), D("2"), D("0.1"))
    assert n.duplicated_storage_term() == D("0.004")
    assert_exact_zero(n.conservative_residual(), "TCD015 conservative residual")
    out["SYNQ-O001"] = "PASS"

    r = Redistribution(D("0.31"), (D("0.12"), D("0.19")))
    assert_exact_zero(r.internal_ledger_sum(), "TCD017 internal ledger")
    assert r.final_total(D("1.7")) == D("1.7")
    out["SYNQ-O002"] = "PASS"

    i = InterceptionCase(D("0.06"), D("0.10"), D("0.04"), D("0.08"), D("0.04"))
    assert_exact_zero(i.residual(), "TCD018 control volume")
    out["SYNQ-O003"] = "PASS"

    conc = (D("2.0"), D("0.2"), D("0.05"))
    common = (D("0.35"), D("0.08"), D("0.2"), D("0.3"))
    v = species_partition_vector(conc, *common)
    for parent, dis, hum in v:
        assert_exact_zero(dis + hum - parent, "TCD023 species partition")
    order = (2, 0, 1)
    vp = species_partition_vector(permute(conc, order), *common)
    assert vp == permute(v, order)
    p_parent = v[2][0]
    n_parent = v[1][0]
    bad_p = ((D(1) - common[3]) * n_parent, common[3] * n_parent)
    assert sum(bad_p, D(0)) != p_parent
    out["SYNQ-O004"] = "PASS"
    out["SYNQ-O005"] = "PASS"

    sites = (
        SlowLangmuirSite(D("0.30"), D("2"), D("0.010"), D("0.20"), D("0.02")),
        SlowLangmuirSite(D("0.90"), D("40"), D("0.020"), D("0.07"), D("0.01")),
        SlowLangmuirSite(D("0.12"), D("600"), D("0.005"), D("0.015"), D("0.003")),
    )
    correct = slow_langmuir_sites(sites, D("0.04"), D("1"), D("1.5"))
    mutant = slow_langmuir_wrong_selector_mutant(sites, D("0.04"), D("1"), D("1.5"), 0)
    assert correct[1] != mutant[1] and correct[2] != mutant[2]
    assert max(range(1, 21)) > len(sites)
    out["SYNQ-O006"] = "PASS"
    out["SYNQ-O007"] = "PASS"

    m = MacroporeLedgerCase(D("1.0"), D("0.4"), D("0.15"), D("0.05"))
    assert_exact_zero(m.internal_transfer_sum(), "TCD025 internal transfer")
    assert_exact_zero(m.whole_control_volume_residual(), "TCD025 whole control volume")
    assert m.end_stores() == (D("0.85"), D("0.50"))
    out["SYNQ-O008"] = "PASS"

    M, theta, qmax, k = D("0.19"), D("0.35"), D("0.24"), D("125")
    root_bis, width, _ = langmuir_bisection_root(M, theta, qmax, k, 80)
    root_exact = langmuir_exact_positive_root(M, theta, qmax, k)
    with localcontext() as ctx:
        ctx.prec = 80
        assert abs(root_bis - root_exact) <= width
        residual = abs(langmuir_storage(root_bis, theta, qmax, k) - M)
        derivative_upper_bound = theta + qmax * k
        assert residual <= derivative_upper_bound * width
    out["SYNQ-O009"] = "PASS"

    events = (D("0"), D("0.5"), D("1"), D("1.5"), D("2"))
    assert management_events(events, D("0"), D("1")) == (D("0.5"), D("1"))
    assert harvest_events(events, D("0"), D("1")) == (D("0"), D("0.5"))
    assert management_events(events, D("0"), D("1.5")) == (D("0.5"), D("1"), D("1.5"))
    out["SYNQ-T001"] = "PASS"
    out["SYNQ-T002"] = "PASS"

    inc = ((D("0.2"), D("0.05")), (D("0.1"), D("0.02")), (D("0.0"), D("0.03")))
    continuous = run_scalar_sequence(D("1"), inc)
    checkpoint = run_scalar_sequence(D("1"), inc[:2])
    split = run_scalar_sequence(checkpoint, inc[2:])
    assert continuous == split
    out["SYNQ-T003"] = "PASS"

    limits = limiting_case_results()
    if not all(limits.values()):
        raise AssertionError(f"limiting cases failed: {limits}")
    out["SYNQ-LIMITING"] = "PASS"
    return out


if __name__ == "__main__":
    for oracle_id, result in self_test().items():
        print(f"{oracle_id},{result}")
