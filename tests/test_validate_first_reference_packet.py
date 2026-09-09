import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).parents[1] / "tools" / "validate_first_reference_packet.py"
spec = importlib.util.spec_from_file_location("validate_first_reference_packet", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

HASH_D = "d" * 64


def representation_scope(observed_count=0):
    keys = sorted(mod._load_representation_registry_keys())
    observed = [
        {"domain": domain, "subject": subject}
        for domain, subject in keys[:observed_count]
    ]
    omitted = [
        {
            "domain": domain,
            "subject": subject,
            "reason_class": "NOT_JOINTLY_OBSERVABLE",
            "rationale": "synthetic test packet marks this predefined subject as not jointly observable",
        }
        for domain, subject in keys[observed_count:]
    ]
    return {
        "registry": mod.REPRESENTATION_REGISTRY,
        "jointly_observed_subjects": observed,
        "omitted_subjects": omitted,
    }


def packet():
    return {
        "packet_schema_version": "1.2.0",
        "work_unit": "ANIMO-NQ01",
        "testcase_id": "RuurloGrass",
        "inputs": {
            "testbank_archive_sha256": mod.FROZEN_TESTBANK_SHA256,
            "input_tree_manifest": "ruurlo-input-manifest.json",
            "hydrology_identity_or_manifest": "ruurlo-hydrology-manifest.json",
            "input_content_transformed": False,
        },
        "b2": {
            "evidence_role": "B2_HISTORICAL_REFERENCE_CANDIDATE",
            "artifact_sha256": HASH_D,
            "receipt_manifest": "prep02r-receipt.json",
            "lineage_classification": "NEARBY_4_1_X_EXPLICIT_NONIDENTICAL_LINEAGE",
            "execution_attempt_permitted_by_prep02r": True,
            "ordinary_run_manifest": "b2-run.json",
            "raw_output_tree_manifest": "b2-tree.json",
            "repeat_determinism": "NOT_RUN_WITH_RATIONALE",
            "repeat_rationale": "historical runtime available for a single controlled execution only",
        },
        "b1": {
            "evidence_role": "B1_DIAGNOSTIC",
            "executable_sha256": mod.PINNED_B1_EXECUTABLE_SHA256,
            "run_manifest": "b1-run.json",
            "raw_output_tree_manifest": "b1-tree.json",
        },
        "formatted_tree_comparison": {
            "result_artifact": "formatted-comparison.json",
            "decision": "DIFFERENT_FAIL_CLOSED",
        },
        "observer": {
            "used": False,
            "ordinary_output_non_interference_passed": None,
            "observer_patch_sha256": None,
            "b2_structured_capture": None,
            "b1_structured_capture": None,
        },
        "representation_scope": representation_scope(0),
        "representation_comparison": {
            "result_artifact": None,
            "decision": "NOT_RUN_NO_STRUCTURED_REPRESENTATION_CAPTURE",
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
            "next_action": "classify formatted differences before any numerical admission",
        },
    }


def enable_observer(p):
    p["observer"].update(
        {
            "used": True,
            "ordinary_output_non_interference_passed": True,
            "observer_patch_sha256": "f" * 64,
            "b2_structured_capture": "b2-capture.json",
            "b1_structured_capture": "b1-capture.json",
        }
    )
    p["representation_scope"] = representation_scope(1)
    p["representation_comparison"].update(
        {
            "result_artifact": "representation-comparison.json",
            "decision": "MATCH_EXACT_REPRESENTATION_OBSERVATIONS",
        }
    )
    p["structured_comparison"].update(
        {
            "result_artifact": "structured-comparison.json",
            "decision": "DIFFERENT_FAIL_CLOSED",
        }
    )


class FirstReferencePacketTests(unittest.TestCase):
    def test_complete_packet_can_contain_fail_closed_comparison(self):
        report = mod.validate_packet(packet())
        self.assertEqual(report["decision"], "PACKET_COMPLETE")
        self.assertTrue(report["packet_complete"])
        self.assertTrue(report["comparison_may_still_be_fail_closed"])
        self.assertFalse(report["numerical_equivalence_qualified_by_this_tool"])
        self.assertEqual(
            report["representation_registry_subjects"],
            report["representation_omitted_subjects"],
        )

    def test_wrong_b1_executable_fails_closed(self):
        p = packet()
        p["b1"]["executable_sha256"] = "e" * 64
        report = mod.validate_packet(p)
        self.assertEqual(report["decision"], "PACKET_INCOMPLETE_FAIL_CLOSED")
        self.assertTrue(any("pinned diagnostic executable" in error for error in report["errors"]))

    def test_transformed_frozen_input_fails_closed(self):
        p = packet()
        p["inputs"]["input_content_transformed"] = True
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("input_content_transformed" in error for error in report["errors"]))

    def test_b2_cannot_be_relabelled_b1(self):
        p = packet()
        p["b2"]["evidence_role"] = "B1_DIAGNOSTIC"
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("explicit B2" in error for error in report["errors"]))

    def test_incomplete_representation_scope_fails_closed(self):
        p = packet()
        p["representation_scope"]["omitted_subjects"].pop()
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("does not disposition all predefined subjects" in error for error in report["errors"]))

    def test_unknown_representation_subject_fails_closed(self):
        p = packet()
        p["representation_scope"]["jointly_observed_subjects"].append(
            {"domain": "formatting", "subject": "invented_after_seeing_b2"}
        )
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("outside the predefined registry" in error for error in report["errors"]))

    def test_representation_subject_cannot_be_observed_and_omitted(self):
        p = packet()
        first = p["representation_scope"]["omitted_subjects"][0]
        p["representation_scope"]["jointly_observed_subjects"].append(
            {"domain": first["domain"], "subject": first["subject"]}
        )
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("both observed and omitted" in error for error in report["errors"]))

    def test_observed_representation_subject_requires_comparison(self):
        p = packet()
        p["representation_scope"] = representation_scope(1)
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("jointly observed representation subjects exist" in error for error in report["errors"]))

    def test_observer_requires_non_interference_and_captures(self):
        p = packet()
        p["observer"]["used"] = True
        p["representation_scope"] = representation_scope(1)
        p["representation_comparison"].update(
            {
                "result_artifact": "representation-comparison.json",
                "decision": "DIFFERENT_REPRESENTATION_FAIL_CLOSED",
            }
        )
        p["structured_comparison"]["decision"] = "DIFFERENT_FAIL_CLOSED"
        p["structured_comparison"]["result_artifact"] = "structured-comparison.json"
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("non-interference" in error for error in report["errors"]))

    def test_observer_requires_representation_comparison(self):
        p = packet()
        enable_observer(p)
        p["representation_comparison"].update(
            {
                "result_artifact": None,
                "decision": "NOT_RUN_NO_STRUCTURED_REPRESENTATION_CAPTURE",
            }
        )
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("representation comparison must be run" in error for error in report["errors"]))

    def test_observer_packet_may_be_complete_even_when_structured_comparison_fails(self):
        p = packet()
        enable_observer(p)
        report = mod.validate_packet(p)
        self.assertTrue(report["packet_complete"])
        self.assertEqual(report["decision"], "PACKET_COMPLETE")
        self.assertEqual(report["representation_jointly_observed_subjects"], 1)

    def test_representation_difference_can_be_retained_in_complete_packet(self):
        p = packet()
        p["representation_scope"] = representation_scope(1)
        p["representation_comparison"].update(
            {
                "result_artifact": "representation-comparison.json",
                "decision": "DIFFERENT_REPRESENTATION_FAIL_CLOSED",
            }
        )
        report = mod.validate_packet(p)
        self.assertTrue(report["packet_complete"])
        self.assertFalse(report["representation_difference_auto_accepted"])

    def test_representation_auto_acceptance_invalidates_packet(self):
        p = packet()
        p["policy_assertions"]["representation_difference_auto_accepted"] = True
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("representation_difference_auto_accepted" in error for error in report["errors"]))

    def test_any_global_tolerance_claim_invalidates_packet(self):
        p = packet()
        p["policy_assertions"]["global_numeric_tolerance_applied"] = True
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("global_numeric_tolerance_applied" in error for error in report["errors"]))

    def test_repeat_not_run_requires_rationale(self):
        p = packet()
        p["b2"]["repeat_rationale"] = None
        report = mod.validate_packet(p)
        self.assertFalse(report["packet_complete"])
        self.assertTrue(any("repeat_rationale" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
