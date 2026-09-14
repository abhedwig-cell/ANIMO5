#!/usr/bin/env python3
import csv
import json
import math
import subprocess
from pathlib import Path

BASE = "730f09f1567461a45bff4566368db05963b200fa"
TARGET_DEPTH_M = 0.5
ALLOWED_PREFIXES = (
    ".github/workflows/animo-ghg06a-tcd034.yml",
    "docs/ghg/TCD034_T50_DEPTH_OPERATOR_MODEL_EVOLUTION.md",
    "integration/animo-ghg/GHG06A_TCD034_T50_OPERATOR_CONTRACT.json",
    "integration/animo-ghg/GHG06A_TCD034_T50_OPERATOR_ORACLES.json",
    "integration/animo-ghg/ANIMO-GHG06A_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG06A_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG06A_STATUS.json",
    "tools/ghg06a/",
)
EXPECTED_SOURCE = {
    "ANIMO_4.1.5.53/ghg_ch4.for": "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
    "ANIMO_4.1.5.53/Temper.for": "643e4460a897ec629068dc97ab4589a745304b8fa7adb7597dfadc1a9a9d41e5",
    "ANIMO_4.1.5.53/Inicalc.for": "306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1",
    "ANIMO_4.1.5.53/Input_hydro.for": "5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64",
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


def evaluate_t50(he, te, target=TARGET_DEPTH_M):
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
            return {"status": "AVAILABLE", "T50_degC": te[i], "mode": "EXACT_NODE", "centers_m": centers}

    for i in range(len(centers) - 1):
        z0, z1 = centers[i], centers[i + 1]
        if z0 < target < z1:
            w = (target - z0) / (z1 - z0)
            value = (1.0 - w) * te[i] + w * te[i + 1]
            return {
                "status": "AVAILABLE",
                "T50_degC": value,
                "mode": "LINEAR_INTERPOLATION",
                "bracket": [i + 1, i + 2],
                "weight_upper": w,
                "centers_m": centers,
            }

    raise AssertionError("target passed bracket precondition but no bracket was found")


def main():
    contract = read_json("integration/animo-ghg/GHG06A_TCD034_T50_OPERATOR_CONTRACT.json")
    oracles = read_json("integration/animo-ghg/GHG06A_TCD034_T50_OPERATOR_ORACLES.json")
    freeze = read_json("integration/animo-ghg/ANIMO-GHG06A_AUTHORING_FREEZE.json")
    status = read_json("integration/animo-ghg/ANIMO-GHG06A_STATUS.json")

    assert contract["work_unit"] == oracles["work_unit"] == freeze["work_unit"] == status["work_unit"] == "ANIMO-GHG06A"
    assert contract["target"] == oracles["target"] == freeze["target"] == status["target"] == "TCD-034"
    assert freeze["base_head"] == BASE
    assert contract["predecessor"] == status["base_predecessor"] == f"ANIMO-GHG06@{BASE}"
    assert contract["semantic_target"]["depth_m"] == TARGET_DEPTH_M
    assert contract["contract_id"] == status["scientific_contract"] == "TCD034_T50_0P50M_DEPTH_OPERATOR_V1"
    assert contract["decision"] == "QUALIFIED_BOUNDED_MODEL_EVOLUTION_T50_DEPTH_OPERATOR_V1"
    assert contract["historical_claims"]["historical_revision53_selector_qualified"] is False
    assert contract["historical_claims"]["historical_interpolation_claimed"] is False
    assert contract["historical_claims"]["walter_heimann_promoted_to_ANIMO_authority"] is False
    assert contract["b3_admission_performed"] is False
    assert contract["production_authorized"] is False

    src = manifest_map("reference/source/source_manifest.csv")
    for path, sha in EXPECTED_SOURCE.items():
        assert src.get(path) == sha, (path, src.get(path), sha)
        assert contract["source_manifest_evidence"].get(path) == sha

    assert oracles["evidence_class"] == "SYNTHETIC_MODEL_EVOLUTION_ORACLE_NOT_B2"
    assert oracles["historical_behavior_claimed"] is False
    assert oracles["whole_model_golden_baseline"] is False

    seen = set()
    for case in oracles["cases"]:
        assert case["id"] not in seen
        seen.add(case["id"])
        got = evaluate_t50(case["He_m"], case["Te_degC"])
        assert got["status"] == case["expected_status"], (case["id"], got, case)
        if got["status"] == "AVAILABLE":
            assert math.isclose(got["T50_degC"], case["expected_T50_degC"], rel_tol=0.0, abs_tol=1e-12), (case["id"], got)
            if "irrelevant_Nuroup_values" in case:
                baseline = got["T50_degC"]
                for _nuroup in case["irrelevant_Nuroup_values"]:
                    repeated = evaluate_t50(case["He_m"], case["Te_degC"])
                    assert repeated["T50_degC"] == baseline
        else:
            assert got["reason"] == case["expected_reason"], (case["id"], got)

    assert {c["id"] for c in oracles["cases"]} == {
        "GHG06A-O01-EXACT-NODE",
        "GHG06A-O02-NONUNIFORM-INTERPOLATION",
        "GHG06A-O03-AFFINE-COARSE",
        "GHG06A-O04-AFFINE-REFINED",
        "GHG06A-O05-ROOT-INDEPENDENCE",
        "GHG06A-O06-SINGLE-LAYER-EXACT-CENTRE",
        "GHG06A-O07-TOP-HALF-CELL-UNBRACKETED",
        "GHG06A-O08-BOTTOM-HALF-CELL-UNBRACKETED",
        "GHG06A-O09-NONPOSITIVE-THICKNESS",
    }

    assert status["model_evolution_selector_qualified"] is True
    assert status["historical_revision53_selector_qualified"] is False
    assert status["selector_domain"] == "LAYER_CENTER_BRACKETED_0P50M_ONLY"
    assert status["boundary_extrapolation"] == "FORBIDDEN_FAIL_CLOSED"
    assert status["FVEGCH4_positive_control"] == "OPEN_UNCHANGED_GHG07_NOT_STARTED"
    assert status["b3_admission_performed"] is False
    assert status["production_authorized"] is False
    assert all(v is False for v in status["hard_boundaries"].values())

    bad = [p for p in changed_files() if not allowed(p)]
    assert not bad, f"scope guard failed, unexpected changed files: {bad}"

    review_path = Path("integration/animo-ghg/ANIMO-GHG06A_INTERNAL_ADVERSARIAL_REVIEW.json")
    if review_path.exists():
        review = read_json(review_path)
        assert review["work_unit"] == "ANIMO-GHG06A"
        assert review["target"] == "TCD-034"
        assert review["same_agent"] is True
        assert review["genuinely_independent"] is False
        assert review["independence_claimed"] is False
        assert review["decision"] == "PASS_BOUNDED_MODEL_EVOLUTION_T50_OPERATOR_V1"
        assert review["gates"]["fixed_depth_identity"] == "PASS_MODEL_EVOLUTION_ONLY"
        assert review["gates"]["operator_mathematics"] == "PASS"
        assert review["gates"]["root_independence"] == "PASS"
        assert review["gates"]["no_extrapolation"] == "PASS_FAIL_CLOSED"
        assert review["gates"]["historical_claim_separation"] == "PASS"
        assert status["review"]["completed"] is True
        assert status["work_status"]["qualified"] is True
        assert status["work_status"]["workunit_complete"] is True
        assert status["b3_admission_performed"] is False
        assert status["state"] == "QUALIFIED_BOUNDED_MODEL_EVOLUTION_T50_OPERATOR_NO_B3_ADMISSION"

    print("GHG06A TCD034 bounded T50 operator package validation PASS")


if __name__ == "__main__":
    main()
