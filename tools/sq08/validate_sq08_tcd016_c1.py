#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
q = json.loads((ROOT / "integration/animo-science/SQ08_TCD016_C1_IDENTITY_SPECIATION_QUALIFICATION.json").read_text())
s = json.loads((ROOT / "integration/animo-science/ANIMO-SQ08_STATUS.json").read_text())
f = json.loads((ROOT / "integration/animo-testbank/fragments/ANIMO-SQ08_TCD016_C1_IDENTITY_FRAGMENT.json").read_text())

assert q["work_unit"] == "ANIMO-SQ08"
assert q["target"] == "TCD-016-C1"
assert q["base_head"] == "ANIMO-SQ07@2076c0def17c504a3ba29db02d964d4a6238d2cf"
assert q["inherited_state"]["owner"] == "M_surface_NH4_non_aqueous_continuation"
assert q["inherited_state"]["unit"] == "kg N m-2"
assert q["inherited_state"]["chemically_noncommittal"] is True
assert q["qualified_identity_envelope"]["current_phase"] == "UNRESOLVED"
assert q["qualified_identity_envelope"]["current_molecular_speciation"] == "UNRESOLVED"
assert q["hypotheses"]["I6_noncommittal_identity_envelope"] == "SELECTED"
assert q["decision"] == "QUALIFY_ONLY_BOUNDED_NONCOMMITTAL_IDENTITY_ENVELOPE_NO_SPECIFIC_PHASE_OR_SPECIATION_CURRENTLY_DEFENSIBLE"
assert q["parameters"] == []
assert q["historical_behavior"] == "UNKNOWN_WITHOUT_B2"
assert q["disposition"]["tcd016_c1_b3"] == "UNRESOLVED_NOT_ADMITTED"
assert q["disposition"]["parent_tcd016_b3"] == "UNRESOLVED_NOT_ADMITTED"
assert q["disposition"]["production_authorized"] is False
assert f["central_registry_write"] == "FORBIDDEN"
assert f["whole_model_golden_created"] is False
assert f["admission_effect"] == "NONE"
assert len(f["entries"]) == 3
assert s["hard_boundaries"]["production_source_modified"] is False
assert s["hard_boundaries"]["central_queue_modified"] is False
assert s["hard_boundaries"]["central_testbank_registry_modified"] is False
print("SQ08_VALIDATION_PASS")
