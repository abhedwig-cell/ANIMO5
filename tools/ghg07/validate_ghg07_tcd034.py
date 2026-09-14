#!/usr/bin/env python3
import csv
import json
import math
import subprocess
from pathlib import Path

BASE = "2573686af69a8d68a94010bb663272b35871a6e1"
TARGET_DEPTH_M = 0.5
KPL = 0.24
ALLOWED_PREFIXES = (
    ".github/workflows/animo-ghg07-tcd034.yml",
    "docs/ghg/TCD034_ACTIVE_PLANT_CH4_REACHABILITY.md",
    "integration/animo-ghg/GHG07_TCD034_ACTIVE_PLANT_CH4_CONTRACT.json",
    "integration/animo-ghg/GHG07_TCD034_ACTIVE_PLANT_CH4_ORACLES.json",
    "integration/animo-ghg/ANIMO-GHG07_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG07_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG07_STATUS.json",
    "tools/ghg07/",
)
EXPECTED_SOURCE = {
    "ANIMO_4.1.5.53/ghg_ch4.for": "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
    "ANIMO_4.1.5.53/input1.for": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95",
}


def read_json(path):
    return json.loads(Path(path).read_text())


def manifest_map(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {row["path"]: row["sha256"] for row in csv.DictReader(f)}


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return [x.strip() for x in out.splitlines() if x.strip()]


def allowed(path):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in ALLOWED_PREFIXES)


def close(a, b, tol=1e-12):
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tol)


def t50_operator(he, te, target=TARGET_DEPTH_M):
    if len(he) < 1 or len(he) != len(te):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "INVALID_GEOMETRY"}
    if any((not math.isfinite(x)) or x <= 0.0 for x in he):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "INVALID_GEOMETRY"}
    if any(not math.isfinite(x) for x in te):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "INVALID_TEMPERATURE"}
    centers = []
    bottom = 0.0
    for h in he:
        bottom += h
        centers.append(bottom - 0.5 * h)
    if any(not centers[i] < centers[i + 1] for i in range(len(centers) - 1)):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "INVALID_GEOMETRY"}
    if target < centers[0] or target > centers[-1]:
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "TARGET_OUTSIDE_LAYER_CENTER_BRACKET"}
    for i, z in enumerate(centers):
        if target == z:
            return {"status": "AVAILABLE", "T50": te[i]}
    for i in range(len(centers) - 1):
        if centers[i] < target < centers[i + 1]:
            w = (target - centers[i]) / (centers[i + 1] - centers[i])
            return {"status": "AVAILABLE", "T50": (1.0 - w) * te[i] + w * te[i + 1]}
    raise AssertionError("selector bracket logic inconsistent")


def growth_factor(t50, tegr):
    temat = tegr + 10.0
    if t50 < temat:
        if t50 > tegr:
            return 4.0 * (1.0 - ((temat - t50) / (temat - tegr)) ** 2.0)
        return 0.0
    return 4.0


def active_path(case):
    he = case["He_m"]
    te = case["Te_degC"]
    selector = t50_operator(he, te)
    if selector["status"] != "AVAILABLE":
        return selector

    t50 = selector["T50"]
    tegr = case["Tegr_degC"]
    f_grow = growth_factor(t50, tegr)
    nuroup = case["Nuroup"]
    fveg = case["FvegCH4"]
    pv = case["PvCH4Ox"]

    if not (0.0 <= fveg <= 100.0):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "FVEG_OUT_OF_RANGE"}
    if not (0.0 <= pv <= 1.0):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "PV_OUT_OF_RANGE"}
    if not (0 <= nuroup <= len(he)):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "ROOT_ZONE_OUT_OF_RANGE"}

    if nuroup == 0:
        return {
            "status": "AVAILABLE",
            "T50": t50,
            "fGrow": f_grow,
            "fRoot": [],
            "fallback_used": False,
            "root_depth_integral": 0.0,
            "Kraw": [],
            "Kplant": [],
            "Qplant": [],
            "Qox": [],
            "Qem": [],
            "Qplant_total": 0.0,
            "Qox_total": 0.0,
            "Qem_total": 0.0,
        }

    ro = case["Ro"]
    mofr = case["Mofr"]
    mofrsa = case["Mofrsa"]
    rebu = case["ReBu"]
    avco = case["AvCoCH4"]
    for arr, name in [(ro, "Ro"), (mofr, "Mofr"), (mofrsa, "Mofrsa"), (rebu, "ReBu"), (avco, "AvCoCH4")]:
        if len(arr) != nuroup:
            return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": f"{name}_LENGTH_MISMATCH"}
    if any(not math.isfinite(x) for arr in (ro, mofr, mofrsa, rebu, avco) for x in arr):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "NONFINITE_ACTIVE_PATH_INPUT"}
    if any(x < 0.0 for x in ro) or any(x < 0.0 for x in avco):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "NEGATIVE_ACTIVE_PATH_INPUT"}

    to_zr = sum(he[:nuroup])
    am_ro = list(ro)
    to_ro = sum(am_ro)
    fallback = to_ro < 1.0e-4
    if fallback:
        am_ro = list(he[:nuroup])
        to_ro = sum(am_ro)
    assert to_ro > 0.0 and to_zr > 0.0

    f_root = [am_ro[i] / to_ro * to_zr / he[i] for i in range(nuroup)]
    root_integral = sum(f_root[i] * he[i] for i in range(nuroup))
    k_raw = [KPL * fveg * f_root[i] * f_grow for i in range(nuroup)]
    phase = [mofr[i] + rebu[i] * (mofrsa[i] - mofr[i]) for i in range(nuroup)]
    if any((not math.isfinite(x)) or x < 0.0 for x in phase):
        return {"status": "UNAVAILABLE_FAIL_CLOSED", "reason": "INVALID_PHASE_STORAGE_FACTOR"}
    k_plant = [k_raw[i] * phase[i] for i in range(nuroup)]
    q_plant = [k_plant[i] * avco[i] * he[i] for i in range(nuroup)]
    q_ox = [pv * q for q in q_plant]
    q_em = [(1.0 - pv) * q for q in q_plant]

    return {
        "status": "AVAILABLE",
        "T50": t50,
        "fGrow": f_grow,
        "fRoot": f_root,
        "fallback_used": fallback,
        "root_depth_integral": root_integral,
        "Kraw": k_raw,
        "Kplant": k_plant,
        "Qplant": q_plant,
        "Qox": q_ox,
        "Qem": q_em,
        "Qplant_total": sum(q_plant),
        "Qox_total": sum(q_ox),
        "Qem_total": sum(q_em),
    }


def check_expected(case, got):
    expected = case["expected"]
    assert got["status"] == expected["status"], (case["id"], got, expected)
    if got["status"] != "AVAILABLE":
        assert got["reason"] == expected["reason"], (case["id"], got)
        return
    scalar_map = {
        "T50_degC": "T50",
        "fGrow": "fGrow",
        "root_depth_integral": "root_depth_integral",
        "Qplant_total": "Qplant_total",
        "Qox_total": "Qox_total",
        "Qem_total": "Qem_total",
    }
    for ek, gk in scalar_map.items():
        if ek in expected:
            assert close(got[gk], expected[ek]), (case["id"], ek, got[gk], expected[ek])
    for key in ("fRoot", "Kraw", "Kplant"):
        if key in expected:
            assert len(got[key]) == len(expected[key])
            for a, b in zip(got[key], expected[key]):
                assert close(a, b), (case["id"], key, got[key], expected[key])
    if "fallback_used" in expected:
        assert got["fallback_used"] is expected["fallback_used"]


def main():
    contract = read_json("integration/animo-ghg/GHG07_TCD034_ACTIVE_PLANT_CH4_CONTRACT.json")
    oracles = read_json("integration/animo-ghg/GHG07_TCD034_ACTIVE_PLANT_CH4_ORACLES.json")
    freeze = read_json("integration/animo-ghg/ANIMO-GHG07_AUTHORING_FREEZE.json")
    status = read_json("integration/animo-ghg/ANIMO-GHG07_STATUS.json")
    selector_contract = read_json("integration/animo-ghg/GHG06A_TCD034_T50_OPERATOR_CONTRACT.json")

    assert contract["work_unit"] == oracles["work_unit"] == freeze["work_unit"] == status["work_unit"] == "ANIMO-GHG07"
    assert contract["target"] == oracles["target"] == freeze["target"] == status["target"] == "TCD-034"
    assert freeze["base_head"] == BASE
    assert contract["predecessor"] == status["base_predecessor"] == f"ANIMO-GHG06A@{BASE}"
    assert selector_contract["contract_id"] == contract["selector_contract"]["id"] == "TCD034_T50_0P50M_DEPTH_OPERATOR_V1"
    assert selector_contract["decision"] == "QUALIFIED_BOUNDED_MODEL_EVOLUTION_T50_DEPTH_OPERATOR_V1"
    assert contract["decision"] == "QUALIFIED_TCD034_MODEL_EVOLUTION_ACTIVE_PLANT_CH4_REACHABILITY_AND_PARTITION_V1"
    assert contract["evidence_class"] == oracles["evidence_class"] == "SYNTHETIC_MODEL_EVOLUTION_POSITIVE_CONTROL_NOT_B2"
    assert contract["historical_claims"]["historical_revision53_selector_qualified"] is False
    assert contract["historical_claims"]["historical_positive_control_claimed"] is False
    assert contract["historical_claims"]["synthetic_oracles_promoted_to_B2"] is False
    assert contract["b3_admission_performed"] is False
    assert contract["production_authorized"] is False

    src = manifest_map("reference/source/source_manifest.csv")
    for path, sha in EXPECTED_SOURCE.items():
        assert src.get(path) == sha, (path, src.get(path), sha)
        assert contract["source_manifest_evidence"].get(path) == sha

    ids = set()
    results = {}
    for case in oracles["cases"]:
        assert case["id"] not in ids
        ids.add(case["id"])
        got = active_path(case)
        check_expected(case, got)
        results[case["id"]] = got
        if got["status"] == "AVAILABLE":
            assert close(got["Qox_total"] + got["Qem_total"], got["Qplant_total"]), (case["id"], got)
            for q, qo, qe in zip(got["Qplant"], got["Qox"], got["Qem"]):
                assert close(qo + qe, q), (case["id"], q, qo, qe)
            if case["Nuroup"] > 0:
                assert close(got["root_depth_integral"], sum(case["He_m"][:case["Nuroup"]]))

    assert ids == {
        "GHG07-O01-ACTIVE-POSITIVE-CONTROL",
        "GHG07-O02-VEGETATION-SWITCH-OFF",
        "GHG07-O03-GROWTH-SWITCH-COLD",
        "GHG07-O04-GROWTH-MATURE",
        "GHG07-O05-NO-ROOTS",
        "GHG07-O06-SELECTOR-UNAVAILABLE-FAIL-CLOSED",
        "GHG07-O07-PARTITION-ALL-EMISSION",
        "GHG07-O08-PARTITION-ALL-OXIDATION",
        "GHG07-O09-UNEQUAL-ROOT-NORMALIZATION",
        "GHG07-O10-ZERO-ROOT-MASS-FALLBACK",
    }

    active = results["GHG07-O01-ACTIVE-POSITIVE-CONTROL"]
    assert active["Qplant_total"] > 0.0 and active["Qox_total"] > 0.0 and active["Qem_total"] > 0.0
    assert results["GHG07-O02-VEGETATION-SWITCH-OFF"]["Qplant_total"] == 0.0
    assert results["GHG07-O03-GROWTH-SWITCH-COLD"]["fGrow"] == 0.0
    assert results["GHG07-O04-GROWTH-MATURE"]["fGrow"] == 4.0
    assert results["GHG07-O05-NO-ROOTS"]["Qplant_total"] == 0.0
    assert results["GHG07-O06-SELECTOR-UNAVAILABLE-FAIL-CLOSED"]["status"] == "UNAVAILABLE_FAIL_CLOSED"
    assert results["GHG07-O07-PARTITION-ALL-EMISSION"]["Qox_total"] == 0.0
    assert results["GHG07-O08-PARTITION-ALL-OXIDATION"]["Qem_total"] == 0.0
    assert results["GHG07-O10-ZERO-ROOT-MASS-FALLBACK"]["fallback_used"] is True

    assert oracles["historical_behavior_claimed"] is False
    assert oracles["whole_model_golden_baseline"] is False
    assert oracles["central_testbank_registry_modified"] is False
    assert status["historical_revision53_selector_qualified"] is False
    assert status["model_evolution_active_path_qualified"] is True
    assert status["b3_admission_performed"] is False
    assert status["production_authorized"] is False
    assert all(v is False for v in status["hard_boundaries"].values())

    bad = [p for p in changed_files() if not allowed(p)]
    assert not bad, f"scope guard failed, unexpected changed files: {bad}"

    review_path = Path("integration/animo-ghg/ANIMO-GHG07_INTERNAL_ADVERSARIAL_REVIEW.json")
    if review_path.exists():
        review = read_json(review_path)
        assert review["work_unit"] == "ANIMO-GHG07"
        assert review["target"] == "TCD-034"
        assert review["same_agent"] is True
        assert review["genuinely_independent"] is False
        assert review["independence_claimed"] is False
        assert review["decision"] == "PASS_TCD034_MODEL_EVOLUTION_ACTIVE_PLANT_CH4_REACHABILITY_AND_PARTITION_V1"
        assert review["gates"]["active_positive_control"] == "PASS"
        assert review["gates"]["partition_conservation"] == "PASS"
        assert review["gates"]["selector_fail_closed"] == "PASS"
        assert review["gates"]["historical_claim_separation"] == "PASS"
        assert status["review"]["completed"] is True
        assert status["work_status"]["qualified"] is True
        assert status["work_status"]["workunit_complete"] is True
        assert status["state"] == "QUALIFIED_MODEL_EVOLUTION_ACTIVE_PLANT_CH4_REACHABILITY_NO_B3_ADMISSION"

    print("GHG07 TCD034 active plant-mediated CH4 reachability package validation PASS")


if __name__ == "__main__":
    main()
