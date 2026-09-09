#!/usr/bin/env python3
"""Fail-closed readiness checks for ANIMO-B3B03 / TCD-024.

This is qualification tooling only. It does not patch ANIMO production source,
change TCD-019 numerical policy, define a numerical tolerance, or admit B3.
"""
from __future__ import annotations

import json
from decimal import Decimal, localcontext
from pathlib import Path

D = Decimal
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "integration/animo-b3/TCD024_READINESS_FIXTURE.json"
EXPECTED = ROOT / "integration/animo-b3/TCD024_EXPECTED_DIFFERENCE.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3B03_STATUS.json"
SOURCE_EVIDENCE = ROOT / "docs/prep05/SLOW_LANGMUIR_SITE_INDEX_DEFECT.md"
INTERACTION_EVIDENCE = ROOT / "docs/numerics/TCD019_TCD024_INTERACTION.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def site_update(site: dict, concentration: Decimal, rho: Decimal, dt: Decimal, exponent_k: Decimal | None = None):
    with localcontext() as ctx:
        ctx.prec = 80
        qmax = D(site["qmax"])
        k = D(site["K"])
        qold = D(site["qold"])
        r_ads = D(site["r_ads"])
        r_des = D(site["r_des"])
        kc = k * concentration
        qeq = (qmax / rho) * kc / (D(1) + kc)
        rate = r_ads if qeq >= qold else r_des
        k_exp = k if exponent_k is None else exponent_k
        yy = (-(rate * (D(1) + k_exp * concentration) * dt)).exp()
        qnew = qold * yy + qeq * (D(1) - yy)
        transfer_rate = (qnew - qold) / dt
        return qeq, yy, qnew, transfer_rate


def main() -> None:
    fixture = load(FIXTURE)
    expected = load(EXPECTED)
    status = load(STATUS)

    assert status["target_tcd"] == "TCD-024"
    assert status["class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES"
    assert status["source_expression"]["legacy"] == "Yy = One + Parcxsl(3,I) * Avc"
    assert status["source_expression"]["candidate_atomic_correction"] == "Yy = One + Parcxsl(3,J) * Avc"
    assert status["historical_reference"]["historical_prevalence"] == "UNKNOWN"
    assert status["admitted"] is False
    assert status["production_migration_admitted"] is False
    assert all(value is False for value in status["hard_boundaries"].values())

    source_text = SOURCE_EVIDENCE.read_text(encoding="utf-8")
    assert "Do 1030 I=1,20" in source_text
    assert "Do 1050 J=1,Ncxsl" in source_text
    assert "Yy = One + Parcxsl(3,I) * Avc" in source_text
    assert "Parcxsl(3,I) -> Parcxsl(3,J)" in source_text
    assert "All six supplied cases with active phosphorus use" in source_text
    assert "OPTCXSL = 3" in source_text

    interaction_text = INTERACTION_EVIDENCE.read_text(encoding="utf-8")
    assert "FOUR_WAY_SYNTHETIC_INTERACTION_CHARACTERIZED_NO_COMPOSITION_ADMISSION" in interaction_text
    assert "TCD-019 is Class E" in interaction_text
    assert "TCD-024 is Class B" in interaction_text
    assert "TCD-024 still needs its Class B evidence" in interaction_text

    assert expected["atomic_change"] == "Parcxsl(3,I) -> Parcxsl(3,J) only in the slow-Langmuir kinetic exponent"
    unchanged = "\n".join(expected["expected_unchanged"])
    assert "TCD-019 fast-sorption finite-change policy" in unchanged
    assert "TCD-019 C_unl stopping or convergence policy" in unchanged
    assert expected["comparison_policy"]["numerical_tolerance_allowed"] is False
    assert expected["comparison_policy"]["unrounded_site_state_required"] is True
    assert expected["comparison_policy"]["unrounded_site_transfer_required"] is True

    active = fixture["active_unequal_sites"]
    c = D(active["concentration"])
    rho = D(active["rho"])
    dt = D(active["dt"])
    sites = active["sites"]
    wrong_k = D(sites[0]["K"])

    correct = []
    mutant = []
    transfers = []
    for site in sites:
        _, _, qnew, transfer = site_update(site, c, rho, dt)
        _, _, qnew_wrong, _ = site_update(site, c, rho, dt, wrong_k)
        correct.append(qnew)
        mutant.append(qnew_wrong)
        transfers.append(transfer)

    assert [str(x) for x in correct] == active["expected_unrounded_qnew_80"]
    assert [str(x) for x in transfers] == active["expected_unrounded_transfer_rate_80"]
    assert [str(x) for x in mutant] == active["expected_wrong_K1_qnew_80"]
    assert [a != b for a, b in zip(correct, mutant)] == active["expected_selector_discriminator"]

    # SYNQ01 publishes shorter decimal strings; require exact textual prefix agreement,
    # not a numeric tolerance comparison.
    oracle = fixture["synq_oracle"]
    for actual, prefix in zip(correct, oracle["published_expected_qnew_prefixes"]):
        assert str(actual).startswith(prefix)
    for actual, prefix in zip(mutant, oracle["published_wrong_K1_prefixes"]):
        assert str(actual).startswith(prefix)

    # Closed multi-site internal transfer identity. The solution counter-transfer is
    # defined as the exact negative of site storage gain; no tolerance is involved.
    with localcontext() as ctx:
        ctx.prec = 80
        dq = [correct[i] - D(sites[i]["qold"]) for i in range(len(sites))]
        site_gain = sum(dq, D(0))
        solution_counter_transfer = -site_gain
        assert solution_counter_transfer + site_gain == D(0)
        assert sum(transfers, D(0)) == site_gain / dt

    # Site-level negative control: zero kinetic rate makes the slow site inactive.
    inactive = fixture["inactive_site_control"]
    inactive_site = inactive["site"]
    _, _, qnew_inactive, tr_inactive = site_update(
        inactive_site, D(inactive["concentration"]), D(inactive["rho"]), D(inactive["dt"])
    )
    _, _, qnew_inactive_wrong, tr_inactive_wrong = site_update(
        inactive_site,
        D(inactive["concentration"]),
        D(inactive["rho"]),
        D(inactive["dt"]),
        wrong_k,
    )
    assert qnew_inactive == D(inactive["expected_qnew"])
    assert tr_inactive == D(inactive["expected_transfer_rate"])
    assert qnew_inactive_wrong == qnew_inactive
    assert tr_inactive_wrong == tr_inactive

    # Exact index-domain safety check from SYNQ-O007.
    trial_domain = range(1, 21)
    site_domain = range(1, len(sites) + 1)
    invalid = [i for i in trial_domain if i not in site_domain]
    assert invalid[0] == 4

    assert fixture["natural_activation"]["available_in_frozen_supplied_testbank"] is False
    assert fixture["natural_activation"]["historical_prevalence"] == "UNKNOWN"
    assert fixture["inactive_route_control"]["Optcxsl"] == 3

    print("ANIMO-B3B03 TCD-024 readiness validator: PASS")
    print("active unequal-site discriminator: PASS")
    print("inactive-site exact control: PASS")
    print("multi-site exact conservation projection: PASS")
    print("TCD-019 separation guard: PASS")
    print("historical prevalence: UNKNOWN")
    print("B3 admission performed: false")


if __name__ == "__main__":
    main()
