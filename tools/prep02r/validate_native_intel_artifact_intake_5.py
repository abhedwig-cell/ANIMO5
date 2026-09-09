#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I = ROOT / "integration" / "animo-prep"

project = json.loads((I / "PREP02R_INTAKE5_PROJECT_RECEIPT.json").read_text())
exe = json.loads((I / "PREP02R_INTAKE5_EXE_RECEIPT.json").read_text())
ev = json.loads((I / "PREP02R_INTAKE5_LINEAGE_EVIDENCE.json").read_text())
status = json.loads((I / "PREP02R_NATIVE_INTEL_ARTIFACT_INTAKE_5_STATUS.json").read_text())
prep = json.loads((I / "PREP02R_STATUS.json").read_text())
registry = json.loads((I / "PREP02R_REFERENCE_CANDIDATES.json").read_text())

assert project["evidence_class"] == "RECEIPT_MANIFEST_NOT_REFERENCE_ADMISSION"
assert exe["evidence_class"] == "RECEIPT_MANIFEST_NOT_REFERENCE_ADMISSION"
assert project["reference_admitted"] is False
assert exe["reference_admitted"] is False
assert project["native_execution_admitted"] is False
assert exe["native_execution_admitted"] is False
assert project["receipt_checks"]["bytes_hashed_before_execution"] is True
assert exe["receipt_checks"]["bytes_hashed_before_execution"] is True
assert project["receipt_checks"]["artifact_executed_by_this_tool"] is False
assert exe["receipt_checks"]["artifact_executed_by_this_tool"] is False

assert project["artifact"]["content_set_sha256"] == "3dc760141d9047d86e07f9490c5e591ac1d6298b3c47882177d8ed9dec53e2b6"
assert exe["artifact"]["sha256"] == "40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d"

p = ev["project_observations"]
assert p["project_creator"] == "Intel Fortran"
assert p["all_configurations"]["RealKIND"] == "realKIND8"
assert p["all_configurations"]["LocalVariableStorage"] == "localStorageSave"
assert p["project_files_not_in_frozen_source"] == []
assert sorted(x.lower() for x in p["frozen_source_files_not_in_project"]) == ["input1_1.for", "outselorg.for"]

x = ev["executable_observations"]
assert x["architecture"] == "x86-64"
assert x["pe_timestamp_utc_interpretation"] == "2026-05-27T13:41:28Z"
assert x["linker_version"] == "14.35"
assert "src_develop_for_20260519" in x["embedded_source_root"]
assert x["static_version_inc_compiler_claim_matches_observed_actual_linker_runtime_lineage"] is False

la = ev["lineage_assessment"]
assert la["received_executable_classification"] == "RECENT_2026_NATIVE_REBUILD_CANDIDATE_NOT_HISTORICAL_REFERENCE"
assert la["historical_revision_53_reference_admitted"] is False
assert la["historical_fidelity_claim"] is False
assert la["exact_project_to_executable_identity_proven"] is False
assert la["exact_frozen_source_bytes_to_executable_identity_proven"] is False

for key in ["TCD_004_build_environment", "TCD_010_default_real_kind", "TCD_011_local_storage_duration"]:
    assert ev["build_contract_impact"][key]["historical_B2_closed"] is False

assert status["scope"]["historical_reference_admission"] is False
assert status["scope"]["native_execution_admission"] is False
assert status["scope"]["B2_admission"] is False
assert status["scope"]["production_migration"] is False

assert prep["status"] == "BLOCKED_HISTORICAL_REFERENCE_PROVENANCE_NOT_ESTABLISHED_RECEIVED_2026_REBUILD_CANDIDATE"
assert prep["state_dimensions"]["received_project_metadata_artifact"] is True
assert prep["state_dimensions"]["received_executable_artifact"] is True
assert prep["state_dimensions"]["native_reconstruction_candidate_obtained"] is True
assert prep["state_dimensions"]["historical_reference_artifact_obtained"] is False
assert prep["supplied_artifact_scan"]["received_animo_executable_sha256"] == exe["artifact"]["sha256"]
assert prep["supplied_artifact_scan"]["received_animo_executable_classification"] == la["received_executable_classification"]
assert prep["supplied_artifact_scan"]["received_project_build_contract"]["RealKIND_all_configs"] == "realKIND8"
assert prep["supplied_artifact_scan"]["received_project_build_contract"]["LocalVariableStorage_all_configs"] == "localStorageSave"
assert prep["native_admission"]["received_2026_executable_historical_reference"] is False
assert prep["native_admission"]["received_2026_executable_native_reconstruction_candidate"] is True

by_id = {c["id"]: c for c in registry["candidates"]}
assert by_id["PREP02R-C02"]["sha256"] == exe["artifact"]["sha256"]
assert by_id["PREP02R-C02"]["bytes_available"] is True
assert by_id["PREP02R-C02"]["trust_classification"] == "RECENT_2026_NATIVE_REBUILD_CANDIDATE_NOT_HISTORICAL_REFERENCE"
assert by_id["PREP02R-C02"]["reference_admitted"] is False
assert by_id["PREP02R-C10"]["content_set_sha256"] == project["artifact"]["content_set_sha256"]
assert by_id["PREP02R-C10"]["trust_classification"] == "DIRECT_BUILD_CONFIGURATION_EVIDENCE_WITH_UNVERIFIED_ORIGINAL_PROVENANCE"
assert by_id["PREP02R-C10"]["reference_admitted"] is False
assert registry["qualifying_reference_artifact_obtained"] is False
assert registry["native_reconstruction_candidate_obtained"] is True
assert registry["native_reference_run_completed"] is False

print("PASS PREP02R-I5 receipt, lineage, canonical reconciliation and admission guards")
