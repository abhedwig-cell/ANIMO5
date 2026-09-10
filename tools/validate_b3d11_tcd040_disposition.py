#!/usr/bin/env python3
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISP = ROOT / "integration/animo-b3/TCD040_B3_DISPOSITION_GOV03.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D11_STATUS.json"
DOC = ROOT / "docs/b3/TCD040_GOV03_RESTORE_DISCRIMINATOR_DISPOSITION.md"


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_B3D11: " + message)


d = json.loads(DISP.read_text(encoding="utf-8"))
s = json.loads(STATUS.read_text(encoding="utf-8"))
doc = DOC.read_text(encoding="utf-8")

require(d["workunit"] == "ANIMO-B3D11", "wrong workunit")
require(d["target"] == "TCD-040", "wrong target")
require(d["canonical_disposition"] == "UNRESOLVED_NOT_ADMITTED", "canonical disposition must fail closed")
require(d["admitted"] is False, "TCD-040 must not be admitted")
require(d["historical_behaviour"] if "historical_behaviour" in d else d["GOV03_route"]["historical_behaviour"] == "UNKNOWN", "historical behaviour must remain UNKNOWN")

require(
    d["frozen_b0"]["source_archive_sha256"]
    == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
    "wrong frozen source hash",
)
require(
    d["frozen_b0"]["testbank_archive_sha256"]
    == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
    "wrong frozen testbank hash",
)
require(d["frozen_b0"]["rehash_confirmed_in_B3D11"] is True, "B3D11 rehash not recorded")

expected_owners = [
    ("NH4", "Conh(0)", "Rsconh(0)"),
    ("NO3", "Coni(0)", "Rsconi(0)"),
    ("DOM", "Codiorma(0)", "Rscodiorma(0)"),
    ("DON", "Codiorni(0)", "Rscodiorni(0)"),
    ("DOP", "Codiorpo(0)", "Rscodiorpo(0)"),
]
actual_owners = [
    (x["species"], x["current_owner"], x["accepted_owner"])
    for x in d["atomic_scope"]["coordinates"]
]
require(actual_owners == expected_owners, "atomic owner surface changed")
require(d["atomic_scope"]["PO4_control_excluded"] is True, "PO4 control must remain excluded")
require(d["atomic_scope"]["TCD016_composition"] is False, "TCD-016 composition forbidden")
require(d["atomic_scope"]["whole_model_checkpoint_qualification"] is False, "whole-model checkpoint claim forbidden")
require(d["atomic_scope"]["canonical_STATE_admission"] is False, "canonical STATE admission forbidden")

src = d["source_recheck"]
require(src["destructive_block"] == "Inicalc.for:125-129", "wrong destructive source seam")
require(src["destructive_assignments_unconditional"] is True, "legacy zeroing must be recorded unconditional")
require(src["legacy_explicit_restart_discriminator_present"] is False, "must not invent a legacy restart discriminator")
require(src["first_timestep_result_zeroing_erases_current_target_owners"] is False, "first Init current-owner boundary misstated")

nat = d["natural_GrassPeat_recheck"]
for k in ("NH4_layer0", "NO3_layer0", "DOM_layer0", "DON_layer0", "DOP_layer0"):
    require(nat[k] != 0.0, f"GrassPeat {k} must activate nonzero path")
require(nat["natural_nonzero_activation_confirmed"] is True, "natural activation not confirmed")

b = d["B3B04_evidence_recheck"]
require(b["split"] == 282, "wrong split")
require(b["records_total"] == 1800, "wrong trace length")
require(b["accepted_prefix_records"] + b["changed_records_defective"] == b["records_total"], "trace arithmetic inconsistent")
require(b["arithmetic_564_plus_1236_equals_1800"] is True, "trace arithmetic flag missing")
require(b["continuous_trace_sha256"] == b["corrected_restore_trace_sha256"], "corrected restore trace must be exact")
require(b["defective_trace_sha256"] != b["continuous_trace_sha256"], "defective trace must diverge")
require(b["split67_zero_control_trace_sha256"] == b["continuous_trace_sha256"], "zero control must remain exact")
require(b["B3B04_validation_run_rechecked_success"] is True, "B3B04 CI recheck missing")
require(b["full_1800_record_harness_reexecuted_in_B3D11"] is False, "B3D11 must not pretend to re-execute B3B04 harness")
for species, value in b["accepted_values"].items():
    raw = struct.pack("<d", value).hex()
    require(raw == b["raw_little_endian_ieee754_hex"][species], f"raw IEEE-754 mismatch for {species}")
require(b["raw_hex_independently_reproduced"] is True, "raw byte recheck flag missing")

fmt = d["formatted_restart_boundary"]
require(fmt["INITIAL_OUT_can_feed_initialization"] is True, "restart-style formatted surface not recorded")
require(fmt["INITIAL_OUT_is_raw_byte_checkpoint"] is False, "must not promote formatted INITIAL.OUT to raw checkpoint")
require(fmt["formatted_roundtrip_exact_whole_model_identity_claimed"] is False, "formatted whole-model identity forbidden")

r = d["restore_discriminator"]
require(r["qualified"] is True, "restore discriminator must be qualified")
require(r["kind"] == "EXPLICIT_CONTROL_PLANE_INITIALIZATION_INTENT", "wrong discriminator kind")
require(r["allowed_values"] == ["COLD_START", "RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE"], "discriminator must be exactly two-state")
require(r["inferred_from_state_or_filename"] is False, "state or filename inference forbidden")
require(r["legacy_entrypoint_without_restore_capability"] == "COLD_START", "legacy cold-start semantics must be retained")
require(r["restore_capable_entrypoint_requires_explicit_recognized_value"] is True, "restore entrypoint must require explicit intent")
require(r["serialized_as_canonical_physical_state"] is False, "control discriminator must not become canonical physical state")

seam = d["atomic_implementation_seam"]
require("Inicalc.for:125-129" in seam["qualified_semantic_seam"], "wrong implementation seam")
require("existing five zero assignments unchanged" in seam["COLD_START"], "cold-start zeroing not retained")
require("do not apply the five zero assignments" in seam["RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE"], "restore semantics not explicit")
for field in ("other_Inicalc_initialization_changed", "Copo_changed", "new_physical_state", "restart_architecture_redesign", "production_source_syntax_selected", "unconditional_deletion_qualified"):
    require(seam[field] is False, f"forbidden seam broadening: {field}")

route = d["GOV03_route"]
require(route["route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "wrong GOV03 route")
require(route["B2_status"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "wrong B2 closure state")
require(route["historical_behaviour"] == "UNKNOWN", "historical behaviour must remain UNKNOWN")
require(route["historical_fidelity_claimed"] is False, "historical fidelity forbidden")
require(route["route_open_for_independent_second_line"] is True, "route must be open for second line")
require(route["independent_second_line_complete"] is False, "B3D11 must not perform second line")

for key, value in d["hard_boundaries"].items():
    require(value is False, f"hard boundary must remain false: {key}")

require(s["workunit"] == "ANIMO-B3D11", "status workunit mismatch")
require(s["target"] == "TCD-040", "status target mismatch")
require(s["admitted"] is False, "status must not admit TCD-040")
require(s["historical_behaviour"] == "UNKNOWN", "status historical behaviour must be UNKNOWN")
require(s["restore_discriminator"]["legacy_discriminator_present"] is False, "status invents legacy discriminator")
require(s["restore_discriminator"]["cold_start_zeroing_retained"] is True, "status does not retain cold start")
require(s["restore_discriminator"]["unconditional_Inicalc_zero_deletion_qualified"] is False, "status qualifies unconditional deletion")
require(s["atomic_scope"]["TCD016_composed"] is False, "status composes TCD-016")
require(s["atomic_scope"]["whole_model_checkpoint_qualified"] is False, "status overclaims checkpoint scope")
require(s["atomic_scope"]["restart_architecture_redesigned"] is False, "status overclaims restart redesign")

allowed_states = {
    "IN_PROGRESS_PERSISTED_TCD040_ROUTE_AND_DISCRIMINATOR_VALIDATION_PENDING",
    "QUALIFIED_TCD040_FORMAL_DISPOSITION_ROUTE_OPEN_RESTORE_DISCRIMINATOR_QUALIFIED_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION",
}
require(s["state"] in allowed_states, "unexpected status state")
if s["state"].startswith("QUALIFIED_"):
    require(s["work_status"]["tested"] is True, "qualified status must be tested")
    require(s["work_status"]["qualified"] is True, "qualified status must be qualified")
    require(s["work_status"]["workunit_complete"] is True, "qualified status must be complete")
    require(s["decision"] == d["decision"], "qualified status decision must match disposition")

required_doc_phrases = [
    "Simply deleting `Inicalc.for:125-129` is specifically not qualified",
    "Historical revision-53 behaviour for the missing B2 reference remains `UNKNOWN`",
    "`UNRESOLVED_NOT_ADMITTED`",
    "no production patch",
    "no canonical STATE admission",
]
for phrase in required_doc_phrases:
    require(phrase in doc, "missing document guard: " + phrase)

print("PASS_B3D11_TCD040_GOV03_RESTORE_DISCRIMINATOR_DISPOSITION")
