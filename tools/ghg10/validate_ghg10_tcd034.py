#!/usr/bin/env python3
import csv
import json
import math
import subprocess
from pathlib import Path

BASE = "31c8ba9a53cb602c7a4a71f501384058ef7be7b2"
EXPECTED_TESTBANK = {
    "ANIMO_testbank/GHGMais/Input/result.bun": "cd4202745ee8a9ccd890e6aa6d3f551ff3bb80041efd178aedb3f5f4bbe002e2",
    "ANIMO_testbank/GHGMais/Input/result_crop_ext.inp": "075a3a612df2b8745d3eda65eac7c56d6c37eb2beea5b91e4cb6dc1edb526679",
    "ANIMO_testbank/GHGMais/Input/soil.inp": "6a07157f64c0913f977487c1719794c1126416646b0b329ce39940935601f760",
}
EXPECTED_SOURCE = {
    "ANIMO_4.1.5.53/Input_hydro.for": "5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64",
    "ANIMO_4.1.5.53/root_extern.for": "063a754fac2fe1b1c4b60fab1e395b8b65a9a03a5d89ace03e08868e1774f0e9",
    "ANIMO_4.1.5.53/ghg_ch4.for": "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
}
ALLOWED = (
    ".github/workflows/animo-ghg10-tcd034.yml",
    "docs/ghg/TCD034_FROZEN_DRIVER_SELECTOR_REPLAY.md",
    "integration/animo-ghg/GHG10_TCD034_FROZEN_DRIVER_REPLAY_SUMMARY.json",
    "integration/animo-ghg/GHG10_TCD034_FROZEN_DRIVER_YEARLY_SUMMARY.csv",
    "integration/animo-ghg/GHG10_TCD034_GROWTH_REGIME_TRANSITIONS.csv",
    "integration/animo-ghg/GHG10_TCD034_REPRESENTATIVE_REPLAY_ROWS.csv",
    "integration/animo-ghg/ANIMO-GHG10_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG10_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG10_STATUS.json",
    "tools/ghg10/",
)


def read_json(path):
    return json.loads(Path(path).read_text())


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def manifest_map(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {row["path"]: row["sha256"] for row in csv.DictReader(f)}


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return [x.strip() for x in out.splitlines() if x.strip()]


def allowed(path):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in ALLOWED)


def close(a, b, tol=2e-8):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


def main():
    summary = read_json("integration/animo-ghg/GHG10_TCD034_FROZEN_DRIVER_REPLAY_SUMMARY.json")
    freeze = read_json("integration/animo-ghg/ANIMO-GHG10_AUTHORING_FREEZE.json")
    status = read_json("integration/animo-ghg/ANIMO-GHG10_STATUS.json")
    predecessor = read_json("integration/animo-ghg/ANIMO-GHG09_STATUS.json")
    yearly = read_csv("integration/animo-ghg/GHG10_TCD034_FROZEN_DRIVER_YEARLY_SUMMARY.csv")
    transitions = read_csv("integration/animo-ghg/GHG10_TCD034_GROWTH_REGIME_TRANSITIONS.csv")
    samples = read_csv("integration/animo-ghg/GHG10_TCD034_REPRESENTATIVE_REPLAY_ROWS.csv")

    assert summary["work_unit"] == freeze["work_unit"] == status["work_unit"] == "ANIMO-GHG10"
    assert summary["target"] == freeze["target"] == status["target"] == "TCD-034"
    assert freeze["base_head"] == BASE
    assert summary["predecessor"] == status["base_predecessor"] == f"ANIMO-GHG09@{BASE}"
    assert predecessor["primary_disposition"] == "QUALIFIED_TCD034_SELECTOR_SENSITIVITY_AND_PARAMETER_NONTRANSFERABILITY_RISK_V1"
    assert predecessor["work_status"]["qualified"] is True
    assert predecessor["work_status"]["reviewed"] is True

    testbank = manifest_map("reference/testcases/testbank_manifest.csv")
    for path, sha in EXPECTED_TESTBANK.items():
        assert testbank.get(path) == sha, (path, testbank.get(path), sha)
    assert summary["testbank"]["result_bun"]["sha256"] == EXPECTED_TESTBANK["ANIMO_testbank/GHGMais/Input/result.bun"]
    assert summary["testbank"]["crop_driver"]["sha256"] == EXPECTED_TESTBANK["ANIMO_testbank/GHGMais/Input/result_crop_ext.inp"]
    assert summary["testbank"]["soil_input"]["sha256"] == EXPECTED_TESTBANK["ANIMO_testbank/GHGMais/Input/soil.inp"]
    assert summary["testbank"]["archive_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
    assert summary["testbank"]["soil_input"]["FvegCH4"] == 0.0
    assert summary["testbank"]["b2_claimed"] is False

    source = manifest_map("reference/source/source_manifest.csv")
    for path, sha in EXPECTED_SOURCE.items():
        assert source.get(path) == sha, (path, source.get(path), sha)
        assert summary["source_evidence"].get(path) == sha

    prep = Path("docs/prep01/GHG_TESTCASE_PROVENANCE.md").read_text()
    assert "BLOCKED_SOURCE_TESTCASE_CONTRACT_LINEAGE_MISMATCH" in prep
    assert "SOURCE_TESTCASE_PROVENANCE_MISMATCH" in prep
    assert summary["testbank"]["lineage_status"] == "BLOCKED_SOURCE_TESTCASE_CONTRACT_LINEAGE_MISMATCH"
    assert summary["testbank"]["allowed_use"] == "ENVIRONMENTAL_DRIVER_TRACE_ONLY"

    driver = summary["driver"]
    assert driver["daily_records"] == 3652
    assert driver["soil_compartments"] == 32
    assert driver["start_date"] == "2010-01-01" and driver["end_date"] == "2019-12-31"
    assert driver["active_root_days"] == 1604
    assert driver["tiwa_start_d"] == 1.0 and driver["tiwa_end_d"] == 3652.0 and driver["tiwa_step_d"] == 1.0
    assert summary["replay_artifact"]["rows"] == 1604
    assert summary["replay_artifact"]["sha256"] == "970bdc7b8666ddc30df5427310799efab77239d6cd02d11d92d977a54b45783e"

    assert len(yearly) == 10
    assert [int(r["year"]) for r in yearly] == list(range(2010, 2020))
    active_days = sum(int(r["active_days"]) for r in yearly)
    regime_changes = sum(int(r["regime_changes"]) for r in yearly)
    legacy_sum = sum(float(r["legacy_fGrow_sum"]) for r in yearly)
    t50_sum = sum(float(r["t50_fGrow_sum"]) for r in yearly)
    weighted_temp_mae = sum(int(r["active_days"]) * float(r["mean_abs_delta_C"]) for r in yearly) / active_days
    weighted_fgrow_mae = sum(int(r["active_days"]) * float(r["mean_abs_delta_fGrow"]) for r in yearly) / active_days
    max_temp = max(float(r["max_abs_delta_C"]) for r in yearly)
    assert active_days == 1604
    assert regime_changes == 231
    assert close(weighted_temp_mae, summary["temperature_difference"]["mean_absolute_degC"])
    assert close(weighted_fgrow_mae, summary["growth_response_difference"]["mean_absolute_fGrow_difference"])
    assert close(max_temp, summary["temperature_difference"]["maximum_absolute_degC"])
    assert close(legacy_sum, summary["growth_response_difference"]["legacy_fGrow_unweighted_sum"])
    assert close(t50_sum, summary["growth_response_difference"]["t50_fGrow_unweighted_sum"])
    assert close(100.0 * (t50_sum / legacy_sum - 1.0), summary["growth_response_difference"]["t50_vs_legacy_unweighted_sum_change_percent"])
    assert all(int(r["regime_changes"]) > 0 for r in yearly)

    transition_map = {(r["legacy_growth_branch"], r["t50_growth_branch"]): int(r["count"]) for r in transitions}
    assert transition_map == {
        ("MATURE", "MATURE"): 114,
        ("MATURE", "TRANSITION"): 196,
        ("OFF", "TRANSITION"): 34,
        ("TRANSITION", "OFF"): 1,
        ("TRANSITION", "TRANSITION"): 1259,
    }
    assert sum(transition_map.values()) == 1604
    assert transition_map[("MATURE", "TRANSITION")] + transition_map[("OFF", "TRANSITION")] + transition_map[("TRANSITION", "OFF")] == 231

    assert len(samples) >= 10
    assert any(close(abs(float(r["legacy_minus_t50_C"])), 5.384873259) for r in samples)
    assert any(close(abs(float(r["legacy_minus_t50_fGrow"])), 2.487223461) for r in samples)
    assert any(r["legacy_growth_branch"] == "OFF" and r["t50_growth_branch"] == "TRANSITION" for r in samples)
    assert any(r["legacy_growth_branch"] == "MATURE" and r["t50_growth_branch"] == "TRANSITION" for r in samples)
    assert any(r["legacy_growth_branch"] == "TRANSITION" and r["t50_growth_branch"] == "OFF" for r in samples)

    td = summary["temperature_difference"]
    assert td["count_abs_ge_0p5_degC"] == 1210
    assert td["count_abs_ge_1_degC"] == 767
    assert td["count_abs_ge_2_degC"] == 246
    assert td["count_abs_ge_3_degC"] == 76
    assert td["count_abs_ge_4_degC"] == 17
    assert td["count_abs_ge_5_degC"] == 5
    gd = summary["growth_response_difference"]
    assert gd["regime_change_days"] == 231
    assert close(gd["regime_change_percent"], 14.40149625935162)

    interp = summary["interpretation"]
    assert interp["selector_difference_material_on_case"] is True
    assert interp["representation_only_supported"] is False
    assert interp["numerically_negligible_supported"] is False
    assert interp["parameter_transfer_can_be_assumed"] is False
    assert interp["methane_flux_change_claimed"] is False
    assert interp["empirical_validation_claimed"] is False
    assert interp["full_application_envelope_closed"] is False
    assert interp["class_f_admission_supported"] is False
    assert summary["decision"] == "QUALIFIED_TCD034_FROZEN_GHGMAIS_DRIVER_DUAL_SELECTOR_REPLAY_CASE_EVIDENCE_V1"

    assert status["evidence_class"] == summary["evidence_class"]
    assert status["interpretation"]["material_selector_divergence_demonstrated"] is True
    assert status["interpretation"]["full_application_envelope_closed"] is False
    assert status["interpretation"]["class_f_admission_ready"] is False
    assert status["b3_admission_performed"] is False
    assert status["class_f_admission_performed"] is False
    assert status["production_authorized"] is False
    assert all(v is False for v in status["hard_boundaries"].values())

    bad = [p for p in changed_files() if not allowed(p)]
    assert not bad, f"scope guard failed: {bad}"

    review_path = Path("integration/animo-ghg/ANIMO-GHG10_INTERNAL_ADVERSARIAL_REVIEW.json")
    if review_path.exists():
        review = read_json(review_path)
        assert review["work_unit"] == "ANIMO-GHG10"
        assert review["target"] == "TCD-034"
        assert review["same_agent"] is True
        assert review["genuinely_independent"] is False
        assert review["independence_claimed"] is False
        assert review["decision"] == "PASS_TCD034_FROZEN_DRIVER_DUAL_SELECTOR_REPLAY_CASE_EVIDENCE_V1"
        assert review["gates"]["driver_provenance"] == "PASS_PINNED_WITH_LINEAGE_LIMIT_PRESERVED"
        assert review["gates"]["material_selector_divergence"] == "PASS_CASE_BOUND"
        assert review["gates"]["growth_regime_divergence"] == "PASS_CASE_BOUND"
        assert review["gates"]["no_flux_overclaim"] == "PASS"
        assert review["gates"]["no_b2_overclaim"] == "PASS"
        assert review["gates"]["class_f_boundary"] == "PASS_NOT_READY"
        assert status["review"]["completed"] is True
        assert status["work_status"]["qualified"] is True
        assert status["work_status"]["workunit_complete"] is True
        assert status["state"] == "QUALIFIED_FROZEN_DRIVER_SELECTOR_REPLAY_CASE_EVIDENCE_NO_ADMISSION"

    print("GHG10 TCD034 frozen-driver dual-selector replay validation PASS")


if __name__ == "__main__":
    main()
