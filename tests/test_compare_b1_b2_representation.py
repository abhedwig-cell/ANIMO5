import copy
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).parents[1] / "tools" / "compare_b1_b2_representation.py"
spec = importlib.util.spec_from_file_location("compare_b1_b2_representation", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

HASH = "a" * 64


def observation(domain="formatting", subject="report_line_endings", classification="CRLF", text="CRLF"):
    return {
        "domain": domain,
        "subject": subject,
        "classification": classification,
        "reference_text": text,
        "notes": None,
    }


def capture(role, observations):
    return {
        "schema_version": "1.1.0",
        "evidence_role": role,
        "run_identity": {
            "run_id": role.lower(),
            "testcase_id": "RuurloGrass",
            "executable_sha256": HASH,
            "source_sha256": HASH,
            "testcase_archive_sha256": HASH,
            "input_tree_sha256_or_manifest": "ruurlo-manifest",
            "environment_id": "env",
            "input_content_transformed": False,
        },
        "capture_contract": {
            "observer_only": True,
            "ordinary_output_reproduced_before_observer_trust": True,
            "rounded_report_only": False,
            "precision_capture_method": "ROUND_TRIP_DECIMAL",
        },
        "representation_observations": observations,
        "records": [],
    }


class RepresentationComparatorTests(unittest.TestCase):
    def test_exact_representation_observation_match(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [observation()])
        b1 = capture("B1_DIAGNOSTIC", [observation()])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "MATCH_EXACT_REPRESENTATION_OBSERVATIONS")
        self.assertFalse(report["normalization_applied"])
        self.assertFalse(report["numerical_equivalence_qualified_by_this_tool"])

    def test_formatting_difference_fails_closed(self):
        b2_obs = observation(classification="CRLF", text="CRLF")
        b1_obs = observation(classification="LF", text="LF")
        report = mod.compare_captures(
            capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [b2_obs]),
            capture("B1_DIAGNOSTIC", [b1_obs]),
        )
        self.assertEqual(report["decision"], "DIFFERENT_REPRESENTATION_FAIL_CLOSED")
        self.assertEqual(report["comparisons"][0]["classification"], "FORMATTING_DIFFERENCE")

    def test_precision_representation_difference_fails_closed(self):
        b2_obs = observation(
            domain="precision_representation",
            subject="internal_real_kind",
            classification="REAL64",
            text="8-byte default REAL",
        )
        b1_obs = copy.deepcopy(b2_obs)
        b1_obs["classification"] = "REAL32"
        b1_obs["reference_text"] = "4-byte default REAL"
        report = mod.compare_captures(
            capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [b2_obs]),
            capture("B1_DIAGNOSTIC", [b1_obs]),
        )
        self.assertEqual(report["decision"], "DIFFERENT_REPRESENTATION_FAIL_CLOSED")
        self.assertEqual(
            report["comparisons"][0]["classification"],
            "PRECISION_REPRESENTATION_DIFFERENCE",
        )

    def test_missing_representation_observation_fails_closed(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [observation()])
        b1 = capture("B1_DIAGNOSTIC", [])
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "DIFFERENT_REPRESENTATION_FAIL_CLOSED")
        self.assertEqual(len(report["observation_set"]["missing_in_b1"]), 1)

    def test_b2_cannot_use_b1_role(self):
        report = mod.compare_captures(
            capture("B1_DIAGNOSTIC", [observation()]),
            capture("B1_DIAGNOSTIC", [observation()]),
        )
        self.assertEqual(report["decision"], "SCHEMA_OR_PROVENANCE_FAILURE")
        self.assertTrue(report["b2_validation_errors"])

    def test_input_manifest_mismatch_is_provenance_failure(self):
        b2 = capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [observation()])
        b1 = capture("B1_DIAGNOSTIC", [observation()])
        b1["run_identity"]["input_tree_sha256_or_manifest"] = "different-manifest"
        report = mod.compare_captures(b2, b1)
        self.assertEqual(report["decision"], "SCHEMA_OR_PROVENANCE_FAILURE")
        self.assertTrue(report["provenance_errors"])

    def test_missing_observation_text_is_schema_failure(self):
        bad = observation()
        bad["reference_text"] = ""
        report = mod.compare_captures(
            capture("B2_HISTORICAL_REFERENCE_QUALIFIED", [bad]),
            capture("B1_DIAGNOSTIC", [observation()]),
        )
        self.assertEqual(report["decision"], "SCHEMA_OR_PROVENANCE_FAILURE")
        self.assertTrue(report["b2_validation_errors"])


if __name__ == "__main__":
    unittest.main()
