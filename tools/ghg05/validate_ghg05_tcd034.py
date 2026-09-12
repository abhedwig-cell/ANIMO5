#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

BASE = "11e9bcdc6654e63f84875bf1f28dc54abe725700"
ALLOWED_PREFIXES = (
    ".github/workflows/animo-ghg05-tcd034.yml",
    "docs/ghg/TCD034_PLANT_GROWTH_TEMPERATURE_SELECTOR_REQUALIFICATION.md",
    "integration/animo-ghg/GHG05_TCD034_SOURCE_RECONSTRUCTION.json",
    "integration/animo-ghg/ANIMO-GHG05_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG05_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG05_STATUS.json",
    "tools/ghg05/",
)

EXPECTED_SOURCE = {
    "ANIMO_4.1.5.53/ghg_ch4.for": "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
    "ANIMO_4.1.5.53/input1.for": "041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95",
    "ANIMO_4.1.5.53/Param.inc": "20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475",
    "ANIMO_4.1.5.53/Temper.for": "643e4460a897ec629068dc97ab4589a745304b8fa7adb7597dfadc1a9a9d41e5",
    "ANIMO_4.1.5.53/Input_hydro.for": "5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64",
    "ANIMO_4.1.5.53/root_plant.for": "07adda92e78a21bde08e137d1cb09bb40d9c63c4f19dcdeeef0d3e263b107816",
    "ANIMO_4.1.5.53/root_grass.for": "cad5cc713e72b7fac01cbba63caa25560fcabd243c73d9fc06ab7130de4d0661",
    "ANIMO_4.1.5.53/root_extern.for": "063a754fac2fe1b1c4b60fab1e395b8b65a9a03a5d89ace03e08868e1774f0e9",
    "ANIMO_4.1.5.53/Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
}
EXPECTED_TESTCASE = {
    "ANIMO_testbank/GHGMais/Input/soil.inp": "6a07157f64c0913f977487c1719794c1126416646b0b329ce39940935601f760",
}


def read_json(path):
    return json.loads(Path(path).read_text())


def manifest_map(path, key="path", hash_key="sha256"):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {row[key]: row[hash_key] for row in csv.DictReader(f)}


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return [x.strip() for x in out.splitlines() if x.strip()]


def allowed(path):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in ALLOWED_PREFIXES)


def main():
    recon = read_json("integration/animo-ghg/GHG05_TCD034_SOURCE_RECONSTRUCTION.json")
    freeze = read_json("integration/animo-ghg/ANIMO-GHG05_AUTHORING_FREEZE.json")
    status = read_json("integration/animo-ghg/ANIMO-GHG05_STATUS.json")

    assert recon["work_unit"] == freeze["work_unit"] == status["work_unit"] == "ANIMO-GHG05"
    assert recon["target"] == freeze["target"] == status["target"] == "TCD-034"
    assert freeze["base_head"] == BASE
    assert status["base_authority"] == f"ANIMO-B3Q06@{BASE}"
    assert recon["historical_behavior"] == status["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
    assert recon["b3_disposition"] == status["candidate_disposition"] == "UNRESOLVED_NOT_ADMITTED"

    src = manifest_map("reference/source/source_manifest.csv")
    for path, sha in EXPECTED_SOURCE.items():
        assert src.get(path) == sha, (path, src.get(path), sha)
        assert recon["source_files"].get(path) == sha

    tb = manifest_map("reference/testcases/testbank_manifest.csv")
    for path, sha in EXPECTED_TESTCASE.items():
        assert tb.get(path) == sha, (path, tb.get(path), sha)
        assert recon["testbank_activation"]["only_case_sha256"] == sha

    s = recon["source_reconstruction"]
    assert s["input_time_bounds"] == "1<=Nuroup<=Nl<=Manl"
    assert s["runtime_bounds"] == "0<=Nuroup<=Nl"
    assert s["Manl"] == 50
    assert "reset Nuroup=0" in s["dynamic_root_update"]
    assert "Flev(Ln)>=1e-7" in s["dynamic_root_update"]
    assert s["positive_trip_post_loop_control_variable"] == "LnRoot+1"
    assert s["zero_trip_current_standard_semantics"] == "Ln=1 when LnRoot=0"
    assert s["resolved_selector_current_standard_semantics"] == "Te(Nuroup+1)"
    assert "K1plant zero" in s["zero_root_path_effect"]
    assert s["old_use_before_definition_premise"] == "REJECTED"
    assert s["intended_scientific_selector"] == "UNQUALIFIED"

    p = recon["temperature_population"]
    assert "K1plant zero" in p["when_Nuroup_eq_0"]
    assert "first compartment below root zone" in p["when_0_lt_Nuroup_lt_Nl"]
    assert "outside demonstrated current-step producer range" in p["when_Nuroup_eq_Nl_lt_Manl"]
    assert "outside declared bound" in p["when_Nuroup_eq_Nl_eq_Manl"]

    a = recon["testbank_activation"]
    assert a["ghg_ch4_blocks_found"] == 1
    assert a["FvegCH4"] == 0.0
    assert a["plant_mediated_positive_control"] is False
    assert a["natural_testbank_activates_selector_effect"] is False

    assert status["source_premise"]["old_use_before_definition_premise"] == "REJECTED_BY_SOURCE_ORDER"
    assert status["source_premise"]["intended_scientific_selector"] == "UNQUALIFIED"
    assert status["hard_boundaries"]["production_source_modified"] is False
    assert status["hard_boundaries"]["canonical_register_modified"] is False
    assert status["hard_boundaries"]["central_queue_modified"] is False
    assert status["hard_boundaries"]["TCD034_admitted"] is False
    assert status["hard_boundaries"]["replacement_temperature_index_invented"] is False
    assert status["hard_boundaries"]["current_gnu_promoted_to_b2"] is False

    bad = [p for p in changed_files() if not allowed(p)]
    assert not bad, f"scope guard failed, unexpected changed files: {bad}"

    review_path = Path("integration/animo-ghg/ANIMO-GHG05_INTERNAL_ADVERSARIAL_REVIEW.json")
    if review_path.exists():
        review = read_json(review_path)
        assert review["work_unit"] == "ANIMO-GHG05"
        assert review["target"] == "TCD-034"
        assert review["same_agent"] is True
        assert review["genuinely_independent"] is False
        assert review["independence_claimed"] is False
        assert review["decision"] == "PASS_FAIL_CLOSED_TCD034_RECONSTRUCTION_UNRESOLVED_NOT_ADMITTED"
        assert review["gates"]["dynamic_Nuroup_ownership"] == "PASS"
        assert review["gates"]["post_do_zero_trip_control"] == "PASS"
        assert review["gates"]["theory_selector_identity"] == "FAIL_CLOSED_UNQUALIFIED"
        assert status["review"]["completed"] is True
        assert status["qualified"] is True
        assert status["b3_admission_performed"] is False
        assert status["state"] == "QUALIFIED_TCD034_SOURCE_RECONSTRUCTION_BLOCKED_INTENDED_SELECTOR_UNQUALIFIED_NO_ADMISSION"

    print("GHG05 TCD034 package validation PASS")


if __name__ == "__main__":
    main()
