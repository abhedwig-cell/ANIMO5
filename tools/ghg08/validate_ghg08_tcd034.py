#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

BASE = "f8969334f648ca28ceb93a2a55bb4eedd478e1dc"
EXPECTED_PRIMARY = "QUALIFIED_TCD034_PARENT_DUAL_TRACK_CLOSURE_LEGACY_UNRESOLVED_MODEL_EVOLUTION_NOT_READY_FOR_SEPARATE_CLASS_F_ADMISSION"
ALLOWED_PREFIXES = (
    ".github/workflows/animo-ghg08-tcd034.yml",
    "docs/ghg/TCD034_PARENT_SCIENTIFIC_CLOSURE_READINESS.md",
    "integration/animo-ghg/GHG08_TCD034_PARENT_CLOSURE_DECISION.json",
    "integration/animo-ghg/GHG08_TCD034_CLASS_F_GATE_MATRIX.csv",
    "integration/animo-ghg/ANIMO-GHG08_AUTHORING_FREEZE.json",
    "integration/animo-ghg/ANIMO-GHG08_INTERNAL_ADVERSARIAL_REVIEW.json",
    "integration/animo-ghg/ANIMO-GHG08_STATUS.json",
    "tools/ghg08/",
)


def read_json(path):
    return json.loads(Path(path).read_text())


def changed_files():
    out = subprocess.check_output(["git", "diff", "--name-only", f"{BASE}..HEAD"], text=True)
    return [x.strip() for x in out.splitlines() if x.strip()]


def allowed(path):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in ALLOWED_PREFIXES)


def gate_matrix():
    with open("integration/animo-ghg/GHG08_TCD034_CLASS_F_GATE_MATRIX.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {row["gate_id"]: row for row in rows}


def main():
    decision = read_json("integration/animo-ghg/GHG08_TCD034_PARENT_CLOSURE_DECISION.json")
    freeze = read_json("integration/animo-ghg/ANIMO-GHG08_AUTHORING_FREEZE.json")
    status = read_json("integration/animo-ghg/ANIMO-GHG08_STATUS.json")
    ghg05 = read_json("integration/animo-ghg/ANIMO-GHG05_STATUS.json")
    ghg06 = read_json("integration/animo-ghg/ANIMO-GHG06_STATUS.json")
    ghg06a = read_json("integration/animo-ghg/ANIMO-GHG06A_STATUS.json")
    ghg07 = read_json("integration/animo-ghg/ANIMO-GHG07_STATUS.json")
    b3q06 = read_json("integration/animo-b3/ANIMO-B3Q06_STATUS.json")

    assert decision["work_unit"] == freeze["work_unit"] == status["work_unit"] == "ANIMO-GHG08"
    assert decision["target"] == freeze["target"] == status["target"] == "TCD-034"
    assert freeze["base_head"] == BASE
    assert decision["predecessor"] == status["base_predecessor"] == f"ANIMO-GHG07@{BASE}"

    assert ghg05["target"] == ghg06["target"] == ghg06a["target"] == ghg07["target"] == "TCD-034"
    assert ghg05["b3_admission_performed"] is False
    assert ghg06["historical_selector_qualified"] is False
    assert ghg06a["historical_revision53_selector_qualified"] is False
    assert ghg06a["model_evolution_selector_qualified"] is True
    assert ghg07["model_evolution_active_path_qualified"] is True
    assert ghg07["historical_revision53_selector_qualified"] is False
    assert ghg07["b3_admission_performed"] is False
    assert b3q06["global_canonical_b3_queue_closed"] is False
    assert "TCD-034" in b3q06["unadmitted_top_level"]

    legacy = decision["parent_tracks"]["historical_corrected_legacy"]
    evolution = decision["parent_tracks"]["explicit_model_evolution"]
    assert legacy["status"] == "UNRESOLVED_NOT_ADMITTED"
    assert legacy["historical_selector_identity"] == "UNRESOLVED"
    assert legacy["active_historical_B2_reference"] == "ABSENT"
    assert legacy["model_evolution_evidence_may_substitute_for_historical_authority"] is False
    assert legacy["ready_for_B3_corrected_legacy_admission"] is False
    assert evolution["qualification_class"] == "F_PHYSICS_OR_MODEL_EVOLUTION"
    assert evolution["bounded_selector_qualified"] is True
    assert evolution["synthetic_active_reachability_qualified"] is True
    assert evolution["ready_for_separate_class_f_scientific_admission"] is False

    gates = gate_matrix()
    assert set(gates) == {"F01", "F02", "F03", "F04", "F05", "F06", "F07", "L01", "L02", "P01", "P02"}
    assert gates["F01"]["status"] == "PASS_BOUNDED"
    assert gates["F02"]["status"] == "PARTIAL"
    assert gates["F03"]["status"] == "MATERIAL_GAP"
    assert gates["F04"]["status"] == "PASS_BOUNDED_ONLY"
    assert gates["F05"]["status"] == "MATERIAL_GAP"
    assert gates["F06"]["status"] == "MATERIAL_GAP"
    assert gates["F07"]["status"] == "MATERIAL_GAP"
    assert gates["L01"]["status"] == "MATERIAL_GAP"
    assert gates["L02"]["status"] == "MATERIAL_GAP"
    assert gates["P01"]["status"] == "FAIL_CLOSED"
    assert gates["P02"]["status"] == "NOT_READY"

    expected_gaps = {
        "APPLICATION_ENVELOPE_SELECTOR_SENSITIVITY_AND_EXPECTED_DIFFERENCE",
        "CALIBRATION_AND_PARAMETER_TRANSFER_IMPLICATIONS",
        "PROCESS_APPROPRIATE_ACTIVE_PLANT_CH4_VALIDATION",
        "INTEGRATED_CH4_OR_CARBON_CONSERVATION_AFTER_EXECUTABLE_SELECTOR_CONNECTION",
        "GENUINELY_INDEPENDENT_CLASS_F_SCIENTIFIC_REVIEW",
    }
    assert set(decision["material_gaps"]) == expected_gaps
    assert decision["primary_disposition"] == EXPECTED_PRIMARY
    assert decision["b3_admission_performed"] is False
    assert decision["class_f_admission_performed"] is False
    assert decision["production_authorized"] is False
    assert decision["global_b3_queue_recomputed"] is False

    assert status["legacy_track"]["disposition"] == "UNRESOLVED_NOT_ADMITTED"
    assert status["model_evolution_track"]["class"] == "F_PHYSICS_OR_MODEL_EVOLUTION"
    assert status["model_evolution_track"]["separate_class_f_admission_ready"] is False
    assert set(status["material_gaps"]) == expected_gaps
    assert status["b3_admission_performed"] is False
    assert status["class_f_admission_performed"] is False
    assert status["production_authorized"] is False
    assert status["global_b3_queue_recomputed"] is False
    assert all(v is False for v in status["hard_boundaries"].values())

    bad = [p for p in changed_files() if not allowed(p)]
    assert not bad, f"scope guard failed, unexpected changed files: {bad}"

    review_path = Path("integration/animo-ghg/ANIMO-GHG08_INTERNAL_ADVERSARIAL_REVIEW.json")
    if review_path.exists():
        review = read_json(review_path)
        assert review["work_unit"] == "ANIMO-GHG08"
        assert review["target"] == "TCD-034"
        assert review["same_agent"] is True
        assert review["genuinely_independent"] is False
        assert review["independence_claimed"] is False
        assert review["decision"] == "PASS_NEGATIVE_TCD034_PARENT_READINESS_SYNTHESIS"
        assert review["gates"]["legacy_track_not_admitted"] == "PASS"
        assert review["gates"]["class_f_not_prematurely_admitted"] == "PASS"
        assert review["gates"]["qualified_child_evidence_preserved"] == "PASS"
        assert review["gates"]["independence_requirement_not_waived"] == "PASS"
        assert status["review"]["completed"] is True
        assert status["work_status"]["qualified"] is True
        assert status["work_status"]["workunit_complete"] is True
        assert status["state"] == "QUALIFIED_NEGATIVE_TCD034_PARENT_READINESS_NO_ADMISSION"
        assert status["primary_disposition"] == EXPECTED_PRIMARY

    print("GHG08 TCD034 parent closure/readiness synthesis validation PASS")


if __name__ == "__main__":
    main()
