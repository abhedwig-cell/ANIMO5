import copy
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).parents[1] / "tools" / "compare_b1_b2_reference.py"
spec = importlib.util.spec_from_file_location("compare_b1_b2_reference", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64


def record(variable_class="PHYSICAL_STORAGE_STATE", text="1.25", quantity="NO3"):
    return {
        "record_id": f"r-{variable_class}-{quantity}",
        "variable_class": variable_class,
        "quantity_name": quantity,
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
            "state_id": "aqueous_no3",
            "transfer_id": None,
            "ledger_id": None,
            "cumulative": False,
            "boundary": None,
        },
        "execution_context": {
            "source_routine": "Transgen",
            "call_context": "accepted",
            "accepted_state": True,
            "trial_state": False,
            "iteration_index": None,
            "branch_id": None,
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


def capture(role, records):
    return {
        "schema_version": "1.0.0",
        "evidence_role": role,
        "run_identity": {
            "run_id": role.lower(),
            "testcase_id": "RuurloGrass",
            "executable_sha256": HASH_A if role.startswith("B2") else HASH_B,
            "source_sha256": HASH_C,
            "testcase_archive_sha256": HASH_C,
            "input_tree_sha256_or_manifest": "manifest-ruurlo",
            "environment_id": "env",
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
        "representation_observations": [],
        "records": records,
    }


class ComparatorTests(unittest.TestCase):
    def test_exact_scientific_match_with_qualified_b2_is_comparison_evidence(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [record()])
        b1 = capture("B1_DIAGNOSTIC", [record()])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "MATCH_EXACT_COMPARISON_EVIDENCE")
        self.assertFalse(report["numerical_equivalence_qualified_by_this_tool"])
        self.assertFalse(report["global_numeric_tolerance_applied"])

    def test_nonexact_float_fails_closed_without_tolerance(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [record(text="1.000000")])
        b1 = capture("B1_DIAGNOSTIC", [record(text="1.000001")])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
        comparison = report["comparisons"][0]
        self.assertEqual(comparison["classification"], "UNQUALIFIED_NUMERICAL_DIFFERENCE")
        self.assertEqual(comparison["numeric_difference"]["absolute_difference"], "0.000001")
        self.assertFalse(report["non_exact_scientific_values_are_accepted"])

    def test_control_flow_difference_is_exact_failure(self):
        b2_record = record(variable_class="DISCRETE_CONTROL_FLOW", text="LANGMUIR", quantity="branch")
        b1_record = copy.deepcopy(b2_record)
        b1_record["record_id"] = "b1-branch"
        b1_record["value"]["text"] = "FREUNDLICH"
        b1_record["value"]["decimal_text"] = None
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [b2_record])
        b1 = capture("B1_DIAGNOSTIC", [b1_record])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
        self.assertEqual(report["comparisons"][0]["classification"], "CONTROL_FLOW_DIFFERENCE")

    def test_non_scientific_metadata_difference_is_nonfatal(self):
        b2_record = record(variable_class="TIMING_OR_NONSCIENTIFIC_METADATA", text="1.2", quantity="cpu")
        b1_record = copy.deepcopy(b2_record)
        b1_record["record_id"] = "b1-cpu"
        b1_record["value"]["text"] = "2.4"
        b1_record["value"]["decimal_text"] = "2.4"
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [b2_record])
        b1 = capture("B1_DIAGNOSTIC", [b1_record])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "MATCH_SCIENTIFIC_RECORDS_REPRESENTATION_DIFFERS")
        self.assertEqual(report["comparisons"][0]["classification"], "REPRESENTATION_ONLY_DIFFERENCE")

    def test_b2_must_not_be_b1_role(self):
        b2 = capture("B1_DIAGNOSTIC", [record()])
        b1 = capture("B1_DIAGNOSTIC", [record()])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "SCHEMA_OR_PROVENANCE_FAILURE")
        self.assertTrue(report["b2_validation_errors"])

    def test_missing_record_fails_closed(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [record()])
        b1 = capture("B1_DIAGNOSTIC", [])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
        self.assertEqual(len(report["record_set"]["missing_in_b1"]), 1)

    def test_exact_match_to_b2_candidate_does_not_upgrade_reference(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_CANDIDATE", [record()])
        b1 = capture("B1_DIAGNOSTIC", [record()])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "MATCH_EXACT_B2_CANDIDATE_NOT_QUALIFIED")
        self.assertFalse(report["b2_reference_qualified_by_this_tool"])


if __name__ == "__main__":
    unittest.main()
