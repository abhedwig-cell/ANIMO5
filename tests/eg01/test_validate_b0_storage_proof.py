import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_b0_storage_proof",
    ROOT / "tools" / "validate_b0_storage_proof.py",
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)

REGISTER = json.loads(
    (ROOT / "integration" / "evidence" / "ANIMO_B0_EVIDENCE_REGISTER.json").read_text(encoding="utf-8")
)

HASHES = {
    item["evidence_id"]: item["sha256"]
    for item in REGISTER["artifacts"]
    if item.get("evidence_class") == "B0_RAW_IMMUTABLE"
}


def valid_proof():
    objects = []
    for evidence_id, digest in HASHES.items():
        objects.append(
            {
                "evidence_id": evidence_id,
                "expected_sha256": digest,
                "primary_storage_record_id": f"primary:{evidence_id}",
                "secondary_storage_record_id": f"secondary:{evidence_id}",
                "immutability_proof_reference": f"immutable:{evidence_id}",
                "ingest_timestamp": "2026-09-09T00:00:00Z",
                "post_ingest_sha256": digest,
                "post_ingest_sha256_match": True,
                "secondary_sha256": digest,
                "secondary_sha256_match": True,
                "restore_test": {
                    "performed": True,
                    "timestamp": "2026-09-09T00:30:00Z",
                    "restored_sha256": digest,
                    "sha256_match": True,
                    "proof_reference": f"restore:{evidence_id}",
                },
                "retention_status": "PROVEN_CONTROLLED_IMMUTABLE",
            }
        )
    return {
        "schema_version": "1.0",
        "work_unit": "ANIMO-EG01",
        "proof_status": "PROVEN_CONTROLLED_IMMUTABLE",
        "storage_authority": {
            "organization_or_authority": "TEST_AUTHORITY_NOT_REAL_PROOF",
            "custodian_role": "B0 Evidence Custodian",
            "primary_storage_control": "TEST_WORM_CONTROL_NOT_REAL_PROOF",
            "secondary_failure_domain_independent": True,
            "least_privilege_access": True,
            "auditability_statement": "TEST_AUDITABLE_NOT_REAL_PROOF",
            "retention_policy_reference": "TEST_POLICY_NOT_REAL_PROOF",
        },
        "evidence_objects": objects,
        "custodian_approval": {
            "approved": True,
            "approval_reference": "TEST_APPROVAL_NOT_REAL_PROOF",
            "approval_timestamp": "2026-09-09T01:00:00Z",
            "notes": ["Synthetic unit-test record. It is not evidence of real storage."],
        },
    }


class StorageProofGateTests(unittest.TestCase):
    def test_synthetic_complete_record_passes_metadata_gate(self):
        result = mod.evaluate(valid_proof(), REGISTER)
        self.assertTrue(result["admission_ready"])
        self.assertEqual(result["failures"], [])

    def test_pending_status_fails_closed(self):
        proof = valid_proof()
        proof["proof_status"] = "INCOMPLETE"
        result = mod.evaluate(proof, REGISTER)
        self.assertFalse(result["admission_ready"])

    def test_wrong_hash_fails(self):
        proof = valid_proof()
        proof["evidence_objects"][0]["post_ingest_sha256"] = "0" * 64
        result = mod.evaluate(proof, REGISTER)
        self.assertFalse(result["admission_ready"])
        self.assertTrue(any("primary retained-byte SHA-256" in x for x in result["failures"]))

    def test_duplicate_id_fails(self):
        proof = valid_proof()
        proof["evidence_objects"][1]["evidence_id"] = proof["evidence_objects"][0]["evidence_id"]
        result = mod.evaluate(proof(), REGISTER)
        self.assertFalse(result["admission_ready"])
        self.assertTrue(any("duplicate evidence_id" in x for x in result["failures"]))

    def test_false_restore_flag_fails(self):
        proof = valid_proof()
        proof["evidence_objects"][0]["restore_test"]["performed"] = False
        result = mod.evaluate(proof, REGISTER)
        self.assertFalse(result["admission_ready"])
        self.assertTrue(any("restore test was not performed" in x for x in result["failures"]))

    def test_placeholder_reference_fails(self):
        proof = valid_proof()
        proof["custodian_approval"]["approval_reference"] = "PENDING"
        result = mod.evaluate(proof, REGISTER)
        self.assertFalse(result["admission_ready"])
        self.assertTrue(any("approval_reference" in x for x in result["failures"]))


if __name__ == "__main__":
    unittest.main()
