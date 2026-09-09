import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]
HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64
FROZEN_TESTBANK = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
PINNED_B1 = "0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e"


def scientific_record(text="1.25"):
    return {
        "record_id": "state-no3-1",
        "variable_class": "PHYSICAL_STORAGE_STATE",
        "quantity_name": "NO3",
        "units": "kg m-3",
        "temporal": {
            "checkpoint": "ACCEPTED_END_OF_STEP_STATE",
            "simulation_year": 1980,
            "simulation_time_day": 1.0,
            "step_index": 1,
            "period_id": None,
        },
        "location": {
            "layer": 1,
            "compartment": 1,
            "species": "NO3-N",
            "site_or_fraction": None,
        },
        "scientific_context": {
            "state_id": "N-NO3",
            "transfer_id": None,
            "ledger_id": None,
            "cumulative": False,
            "boundary": None,
            "ledger_member_id": None,
            "ledger_sign": None,
            "index_mapping_id": None,
        },
        "execution_context": {
            "source_routine": "Transgen",
            "call_context": "accepted",
            "accepted_state": True,
            "trial_state": False,
            "iteration_index": None,
            "branch_id": "ordinary",
            "fallback_id": None,
        },
        "precision": {
            "storage_kind": "REAL64",
            "bits": 64,
            "decimal_digits_emitted": 17,
            "capture_is_round_trip": True,
            "compiler_default_kind_dependency": False,
        },
        "value": {
            "encoding": "decimal_text",
            "text": text,
            "decimal_text": text,
            "binary_hex": None,
            "formatted_source_text": None,
        },
        "notes": None,
    }


def representation_observation(text="LF"):
    return {
        "domain": "formatting",
        "subject": "line_ending_convention",
        "classification": text,
        "reference_text": text,
        "notes": None,
    }


def capture(role, *, scientific_text="1.25", representation_text="LF"):
    return {
        "schema_version": "1.1.0",
        "evidence_role": role,
        "run_identity": {
            "run_id": role.lower(),
            "testcase_id": "RuurloGrass",
            "executable_sha256": HASH_A if role.startswith("B2") else PINNED_B1,
            "source_sha256": HASH_C,
            "testcase_archive_sha256": FROZEN_TESTBANK,
            "input_tree_sha256_or_manifest": "ruurlo-manifest",
            "environment_id": "synthetic-env",
            "compiler_or_runtime_identity": None,
            "command_line": None,
            "working_directory_layout_id": None,
            "input_content_transformed": False,
        },
        "capture_contract": {
            "observer_only": True,
            "ordinary_output_reproduced_before_observer_trust": True,
            "rounded_report_only": False,
            "precision_capture_method": "ROUND_TRIP_DECIMAL",
            "observer_patch_sha256": None,
            "ordinary_output_tree_manifest": None,
            "observer_output_tree_manifest": None,
        },
        "representation_observations": [representation_observation(representation_text)],
        "records": [scientific_record(scientific_text)],
    }


def representation_registry_keys():
    registry = json.loads(
        (ROOT / "integration/animo-numerics/FIRST_REFERENCE_REPRESENTATION_SURFACE.json").read_text(
            encoding="utf-8"
        )
    )
    return sorted((item["domain"], item["subject"]) for item in registry["subjects"])


def packet():
    keys = representation_registry_keys()
    observed_key = ("formatting", "line_ending_convention")
    omitted = [
        {
            "domain": domain,
            "subject": subject,
            "reason_class": "NOT_JOINTLY_OBSERVABLE",
            "rationale": "synthetic CLI integration packet",
        }
        for domain, subject in keys
        if (domain, subject) != observed_key
    ]
    return {
        "packet_schema_version": "1.2.0",
        "work_unit": "ANIMO-NQ01",
        "testcase_id": "RuurloGrass",
        "inputs": {
            "testbank_archive_sha256": FROZEN_TESTBANK,
            "input_tree_manifest": "ruurlo-manifest",
            "hydrology_identity_or_manifest": "hydrology-manifest",
            "input_content_transformed": False,
        },
        "b2": {
            "evidence_role": "B2_HISTORICAL_REFERENCE_CANDIDATE",
            "artifact_sha256": HASH_A,
            "receipt_manifest": "receipt.json",
            "lineage_classification": "SYNTHETIC_TEST_ONLY",
            "execution_attempt_permitted_by_prep02r": True,
            "ordinary_run_manifest": "b2-run.json",
            "raw_output_tree_manifest": "b2-tree.json",
            "repeat_determinism": "NOT_RUN_WITH_RATIONALE",
            "repeat_rationale": "synthetic CLI integration test",
        },
        "b1": {
            "evidence_role": "B1_DIAGNOSTIC",
            "executable_sha256": PINNED_B1,
            "run_manifest": "b1-run.json",
            "raw_output_tree_manifest": "b1-tree.json",
        },
        "formatted_tree_comparison": {
            "result_artifact": "tree-comparison.json",
            "decision": "DIFFERENT_FAIL_CLOSED",
        },
        "observer": {
            "used": False,
            "ordinary_output_non_interference_passed": None,
            "observer_patch_sha256": None,
            "b2_structured_capture": None,
            "b1_structured_capture": None,
        },
        "representation_scope": {
            "registry": "integration/animo-numerics/FIRST_REFERENCE_REPRESENTATION_SURFACE.json",
            "jointly_observed_subjects": [
                {"domain": observed_key[0], "subject": observed_key[1]}
            ],
            "omitted_subjects": omitted,
        },
        "representation_comparison": {
            "result_artifact": "representation-comparison.json",
            "decision": "MATCH_EXACT_REPRESENTATION_OBSERVATIONS",
        },
        "structured_comparison": {
            "result_artifact": None,
            "decision": "NOT_RUN_NO_UNROUNDED_CAPTURE",
        },
        "policy_assertions": {
            "global_numeric_tolerance_applied": False,
            "legacy_residual_used_as_tolerance": False,
            "rounded_report_treated_as_unrounded_oracle": False,
            "representation_difference_auto_accepted": False,
            "b1_classified_as_independent_reference": False,
            "numerical_equivalence_qualified_by_packet": False,
            "production_migration_admitted": False,
        },
        "disposition": {
            "b2_reference_status": "CANDIDATE_NOT_QUALIFIED",
            "next_action": "synthetic test only",
        },
    }


class CliIntegrationTests(unittest.TestCase):
    def run_cli(self, script, *paths):
        return subprocess.run(
            [sys.executable, str(ROOT / script), *(str(path) for path in paths)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_json(self, root, name, value):
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_scientific_cli_exact_candidate_match_returns_zero_without_qualification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            b2 = self.write_json(root, "b2.json", capture("B2_HISTORICAL_REFERENCE_CANDIDATE"))
            b1 = self.write_json(root, "b1.json", capture("B1_DIAGNOSTIC"))
            result = self.run_cli("tools/compare_b1_b2_reference.py", b2, b1)
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["decision"], "MATCH_EXACT_B2_CANDIDATE_NOT_QUALIFIED")
            self.assertFalse(report["numerical_equivalence_qualified_by_this_tool"])

    def test_scientific_cli_difference_returns_two(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            b2 = self.write_json(root, "b2.json", capture("B2_HISTORICAL_REFERENCE_QUALIFIED"))
            b1 = self.write_json(
                root,
                "b1.json",
                capture("B1_DIAGNOSTIC", scientific_text="1.250000000000001"),
            )
            result = self.run_cli("tools/compare_b1_b2_reference.py", b2, b1)
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")

    def test_representation_cli_exact_match_returns_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            b2 = self.write_json(root, "b2.json", capture("B2_HISTORICAL_REFERENCE_QUALIFIED"))
            b1 = self.write_json(root, "b1.json", capture("B1_DIAGNOSTIC"))
            result = self.run_cli("tools/compare_b1_b2_representation.py", b2, b1)
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["decision"], "MATCH_EXACT_REPRESENTATION_OBSERVATIONS")
            self.assertFalse(report["numerical_equivalence_qualified_by_this_tool"])

    def test_representation_cli_difference_returns_two(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            b2 = self.write_json(root, "b2.json", capture("B2_HISTORICAL_REFERENCE_QUALIFIED"))
            b1 = self.write_json(
                root,
                "b1.json",
                capture("B1_DIAGNOSTIC", representation_text="CRLF"),
            )
            result = self.run_cli("tools/compare_b1_b2_representation.py", b2, b1)
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(report["decision"], "DIFFERENT_REPRESENTATION_FAIL_CLOSED")

    def test_packet_validator_cli_accepts_complete_evidence_packet_without_admission(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet_path = self.write_json(root, "packet.json", packet())
            result = self.run_cli("tools/validate_first_reference_packet.py", packet_path)
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["decision"], "PACKET_COMPLETE")
            self.assertFalse(report["numerical_equivalence_qualified_by_this_tool"])
            self.assertFalse(report["production_migration_admitted"])


if __name__ == "__main__":
    unittest.main()
