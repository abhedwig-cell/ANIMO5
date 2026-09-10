#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[2]
status_path = root / "integration/animo-b3/ANIMO-B3B04E2_STATUS.json"
doc_path = root / "docs/b3/TCD040_REPLAY_RECONSTRUCTION_GOVERNANCE.md"

status = json.loads(status_path.read_text(encoding="utf-8"))
doc = doc_path.read_text(encoding="utf-8")
errors = []

def req(cond, msg):
    if not cond:
        errors.append(msg)

req(status["workunit"] == "ANIMO-B3B04E2", "wrong workunit")
req(status["target"] == "TCD-040", "wrong target")
req(status["scope"] == "GOVERNANCE_ONLY_REPLAY_RECONSTRUCTION_AUTHORIZATION", "wrong scope")
req(status["decision"] == "AUTHORIZED_DISTINCT_PROVENANCE_PINNED_REPLAY_RECONSTRUCTION", "wrong decision")
req(status["canonical_tcd_status"] == "UNRESOLVED_NOT_ADMITTED", "TCD-040 status widened")

refs = status["authorities"]
expected_refs = {
    "B3B04": "19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865",
    "B3D11": "4cc782986faf3d3af829f2e16142dd7f8622c6ac",
    "B3B04R": "bb001129578457ca8435e39deb2b8586e7ebc6a2",
    "B3B04E1": "9f3e1e9b583d540e5d7048de31e62701747ab69d",
    "EG01": "a818b5a37b80ed92aded0b9c404990d356eb2300",
    "RG05D": "f3d6b9780631bd627f8bca0658a8e3878746e666",
}
for key, value in expected_refs.items():
    req(refs.get(key) == value, f"authority mismatch: {key}")

b0 = status["frozen_b0"]
req(b0["source_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "wrong source hash")
req(b0["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "wrong testbank hash")
req(b0["user_guide_sha256"] == "ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301", "wrong guide hash")
req(b0["controlled_immutable_storage_proven"] is False, "EG01 storage proof silently claimed")

auth = status["authorization"]
req(auth["reconstruction_allowed"] is True, "reconstruction not authorized")
req(auth["reconstruction_is_distinct_remediation_artifact"] is True, "reconstruction not distinct")
req(auth["reconstruction_is_original_B3B04_harness"] is False, "reconstruction misrepresented as original")
req(auth["retroactive_original_evidence_claim_allowed"] is False, "retroactive evidence claim allowed")
req(auth["expected_B3B04_results_are_comparison_targets_only"] is True, "expected results not quarantined")
req(auth["expected_results_may_be_generator_inputs"] is False, "circular generator inputs allowed")
req(auth["hidden_chat_state_allowed"] is False, "hidden chat dependency allowed")
req(auth["unversioned_scripts_allowed"] is False, "unversioned scripts allowed")
req(auth["manual_output_editing_allowed"] is False, "manual output editing allowed")
req(auth["public_republication_of_raw_B0_authorized"] is False, "raw B0 republication authorized")

topo = status["required_replay_topology"]
for key in [
    "continuous_path",
    "stageA_atomic_checkpoint",
    "stageB_corrected_restore",
    "stageB_defective_five_coordinate_erasure",
    "split67_exact_zero_negative_control",
    "separate_process_boundary_required",
    "Copo0_excluded_control",
]:
    req(topo.get(key) is True, f"missing replay topology requirement: {key}")

resume = status["b3b04e1_resume_effect"]
req(resume["explicit_governance_reconstruction_authorization_satisfied"] is True, "reconstruction authorization not satisfied")
req(resume["controlled_immutable_B0_acquisition_satisfied"] is False, "B0 custody falsely satisfied")
req(resume["ordinary_B3B04E1_evidence_gate_open"] is False, "B3B04E1 gate opened too early")
req(resume["independent_second_line_reconsideration_allowed"] is False, "reconsideration opened too early")

for key, value in status["hard_boundaries"].items():
    req(value is False, f"hard boundary violated: {key}")

required_doc_phrases = [
    "AUTHORIZED_DISTINCT_PROVENANCE_PINNED_REPLAY_RECONSTRUCTION",
    "comparison targets, not generator inputs",
    "This workunit does **not** waive ANIMO-EG01",
    "UNRESOLVED_NOT_ADMITTED",
    "No heuristic restart discriminator is authorized",
    "No second-line reconsideration branch may be created",
]
for phrase in required_doc_phrases:
    req(phrase in doc, f"missing governance guard phrase: {phrase}")

if errors:
    print("B3B04E2 validation FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("PASS_B3B04E2_PROVENANCE_PINNED_RECONSTRUCTION_AUTHORIZATION")
