#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integration/animo-testbank/ANIMO_TESTBANK_REGISTRY.json"
HANDOFF = ROOT / "integration/animo-testbank/fragments/ANIMO-TB05C_CONVERGENCE_HANDOFF.json"
STATUS = ROOT / "integration/animo-testbank/ANIMO-TB05C_STATUS.json"

BASE_REGISTRY_BLOB = "4c78cdb542c5ff4ce898c033eb99dd7b2daa7c2c"
TB03D_IDS = {
    "ATB-ORACLE-002", "ATB-ORACLE-003", "ATB-SPC-003", "ATB-TRN-002",
    "ATB-CONS-002", "ATB-CONS-003", "ATB-CONS-004", "ATB-CONS-005",
}
SOURCE_EXPECTED = {
    "ANIMO-TB04A": {
        "qualified": {"ATB-STATE-003", "ATB-STATE-004", "ATB-STATE-005", "ATB-STATE-006"},
        "gaps": {"ATB-STATE-007"},
    },
    "ANIMO-TB04B": {
        "qualified": {"ATB-BND-002", "ATB-BND-005"},
        "gaps": {"ATB-BND-003", "ATB-BND-004", "ATB-BND-006"},
    },
    "ANIMO-TB05A": {
        "qualified": {"ATB-SUB-003", "ATB-SUB-004", "ATB-SUB-005"},
        "gaps": {"ATB-SUB-006", "ATB-SUB-007"},
    },
    "ANIMO-TB05B": {
        "qualified": {"ATB-SUB-008", "ATB-SUB-009", "ATB-SUB-010"},
        "gaps": {"ATB-SUB-011", "ATB-SUB-012"},
    },
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_text(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)


def git_blob_at(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{ref}:{path}"], cwd=ROOT, text=True).strip()


def require_false(mapping: dict, key: str) -> None:
    assert mapping.get(key) is False, f"expected {key}=false, got {mapping.get(key)!r}"


def main() -> int:
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    assert handoff["work_unit"] == "ANIMO-TB05C"
    assert handoff["base_registry_authority"] == "ANIMO-TB03D@abcfc9daeacbba4c7d56339fdeedae8f422288c5"
    assert handoff["base_registry_blob"] == BASE_REGISTRY_BLOB
    assert handoff["registry_write"] == "FORBIDDEN_IN_TB05C"
    assert handoff["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"

    raw_registry = REGISTRY.read_bytes()
    assert git_blob_sha(raw_registry) == BASE_REGISTRY_BLOB, "TB05C must not mutate the TB03D central registry"
    registry = json.loads(raw_registry)
    registry_ids = [e["test_id"] for e in registry["test_registry"]]
    assert len(registry_ids) == len(set(registry_ids)), "central registry contains duplicate IDs"
    registry_id_set = set(registry_ids)
    assert TB03D_IDS <= registry_id_set, "TB03D consolidated entries missing from serial base"

    qualified = set(handoff["qualified_for_serial_consolidation"])
    gaps = set(handoff["preserve_without_promotion"])
    assert len(qualified) == 12
    assert len(gaps) == 8
    assert qualified.isdisjoint(gaps)
    assert qualified.isdisjoint(registry_id_set), f"qualified target collision with central registry: {sorted(qualified & registry_id_set)}"
    assert gaps.isdisjoint(registry_id_set), f"GAP entry accidentally centralized: {sorted(gaps & registry_id_set)}"

    collected: dict[str, dict] = {}
    seen_source_ids: set[str] = set()
    for work_unit, pin in handoff["fragment_pins"].items():
        expected = SOURCE_EXPECTED[work_unit]
        assert pin["ci_conclusion"] == "success"
        assert git_blob_at(pin["head"], pin["fragment_path"]) == pin["fragment_blob"]
        assert git_blob_at(pin["head"], pin["status_path"]) == pin["status_blob"]
        fragment = json.loads(git_text(pin["head"], pin["fragment_path"]))
        status = json.loads(git_text(pin["head"], pin["status_path"]))
        assert fragment["producer_workunit"] == work_unit
        assert status["work_unit"] == work_unit
        assert status["work_status"]["qualified"] is True
        assert status["work_status"]["complete"] is True
        assert set(status["qualified_entries"]) == expected["qualified"]
        assert set(status["gap_entries"]) == expected["gaps"]
        require_false(fragment["hard_boundaries"], "production_source_modified")
        require_false(fragment["hard_boundaries"], "scientific_admission_performed")
        require_false(fragment["hard_boundaries"], "central_registry_modified")
        require_false(fragment["hard_boundaries"], "whole_model_golden_baseline_created")

        for entry in fragment["entries"]:
            test_id = entry["test_id"]
            assert test_id not in seen_source_ids, f"duplicate ID across source fragments: {test_id}"
            seen_source_ids.add(test_id)
            collected[test_id] = entry
            if test_id in expected["qualified"]:
                assert entry["status"] == "QUALIFIED_FRAGMENT_ENTRY"
                assert entry["expected_value_provenance"] != "UNKNOWN"
                assert entry["comparison_policy"] != "NOT_YET_QUALIFIED"
                assert entry.get("source_identity")
                assert entry.get("failure_semantics")
                assert entry.get("permanence")
                assert isinstance(entry.get("applicability_pins"), dict)
            elif test_id in expected["gaps"]:
                assert entry["status"] == "GAP"
                assert entry["expected_value_provenance"] == "UNKNOWN"
                assert entry["comparison_policy"] == "NOT_YET_QUALIFIED"
            else:
                raise AssertionError(f"unexpected source fragment ID {test_id} in {work_unit}")

    assert set(collected) == qualified | gaps
    assert qualified == set().union(*(v["qualified"] for v in SOURCE_EXPECTED.values()))
    assert gaps == set().union(*(v["gaps"] for v in SOURCE_EXPECTED.values()))

    dependency_plan = handoff["dependency_plan"]
    assert set(dependency_plan) == qualified
    closure = registry_id_set | qualified
    for test_id, deps in dependency_plan.items():
        assert len(deps) == len(set(deps)), f"duplicate dependency for {test_id}"
        missing = set(deps) - closure
        assert not missing, f"unclosed dependencies for {test_id}: {sorted(missing)}"
        assert not (set(deps) & gaps), f"qualified entry {test_id} depends on GAP entry"

    normalization = handoff["registry_metadata_normalization"]
    assert set(normalization) == qualified
    allowed_levels = set(registry["legacy_taxonomy"]["test_levels"])
    allowed_costs = set(registry["legacy_taxonomy"]["cost_classes"])
    allowed_failures = set(registry["controlled_vocabularies"]["failure_class"])
    profiles_doc = json.loads((ROOT / "integration/animo-testbank/ANIMO_TESTBANK_EXECUTION_PROFILES.json").read_text(encoding="utf-8"))
    allowed_profiles = {p["profile"] for p in profiles_doc["profiles"]}
    for test_id, meta in normalization.items():
        assert meta["level"] in allowed_levels
        assert meta["cost_class"] in allowed_costs
        assert set(meta["execution_profile"]) <= allowed_profiles
        assert meta["failure_class"] in allowed_failures
        assert meta["subsystem"], f"empty subsystem normalization for {test_id}"

    # Adversarial fail-closed assertions on the highest-risk scope boundaries.
    require_false(collected["ATB-STATE-004"]["applicability_pins"], "whole_model_state_claim")
    require_false(collected["ATB-STATE-006"]["applicability_pins"], "whole_model_active_split")
    require_false(collected["ATB-BND-002"]["applicability_pins"], "finite_positive_subthreshold_included")
    require_false(collected["ATB-BND-005"]["applicability_pins"], "production_patch_admitted")
    require_false(collected["ATB-SUB-004"]["applicability_pins"], "historical_B2")
    require_false(collected["ATB-SUB-004"]["applicability_pins"], "behavioural_golden_reference")
    require_false(collected["ATB-SUB-005"]["applicability_pins"], "whole_model_active_split")
    require_false(collected["ATB-SUB-008"]["applicability_pins"], "b3_admitted")
    require_false(collected["ATB-SUB-008"]["applicability_pins"], "production_ready")
    require_false(collected["ATB-SUB-009"]["applicability_pins"], "scientific_admission")
    require_false(collected["ATB-SUB-010"]["applicability_pins"], "production_patch_admitted")

    boundaries = handoff["hard_boundaries"]
    for key in (
        "production_source_modified", "scientific_admission_performed", "central_registry_modified",
        "gap_promoted", "historical_B2_fabricated", "whole_model_golden_baseline_created",
        "whole_model_restart_qualified", "whole_model_boundary_initialization_qualified",
        "whole_model_conservation_qualified", "subsystem_release_qualified",
    ):
        require_false(boundaries, key)

    if STATUS.exists():
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        assert status["work_unit"] == "ANIMO-TB05C"
        assert status["state"] == "QUALIFIED_ANIMO_TB05C_TB4_TB5_FRAGMENT_CONVERGENCE_READINESS"
        assert status["assurance"] == "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT"
        assert status["qualified_for_serial_consolidation"] == handoff["qualified_for_serial_consolidation"]
        assert status["preserved_gaps"] == handoff["preserve_without_promotion"]
        assert status["work_status"] == {"realized": True, "persisted": True, "tested": True, "qualified": True, "complete": True}

    print("QUALIFIED_ANIMO_TB05C_TB4_TB5_FRAGMENT_CONVERGENCE_READINESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
