#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print("KT22 FAIL_CLOSED:", message)
    raise SystemExit(1)


evidence = json.loads(
    (R / "integration/animo-kt22/KT22_LWKM_EXCLUSION_ROUTING.json").read_text()
)
status = json.loads(
    (R / "integration/animo-kt22/ANIMO-KT22_STATUS.json").read_text()
)
review_path = R / "integration/animo-kt22/ANIMO-KT22_ADVERSARIAL_REVIEW.json"

if evidence["authorities"]["predecessor"] != "ANIMO-KT21@e591344d9a2fd03b92fd56af1b9b555099edc340":
    fail("wrong KT21 predecessor")
if evidence["authorities"]["tcd042_parent"] != "ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367":
    fail("wrong TCD042 parent authority")
if evidence["source"]["hydrology_sha256"] != "b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c":
    fail("wrong hydrology source identity")

p = evidence["kt21_partition"]
if p["packet_count"] != 1800:
    fail("packet count")
if p["blocked_first_call_runinu"] + p["deterministic_packet_count"] != p["packet_count"]:
    fail("blocked/deterministic partition")
if (
    p["tcd042_b1_exact_zero"]
    + p["tcd042_e1"]
    + p["tcd042_hydrology_outside_admitted_scope"]
    + p["ponding"]
    != p["deterministic_packet_count"]
):
    fail("deterministic partition does not close")

d = evidence["outside_remainder_decomposition"]
if d["examined_count"] != p["tcd042_hydrology_outside_admitted_scope"]:
    fail("outside count drift")
if (
    d["ordinary_positive_flow_flux_ge_threshold"]
    + d["subthreshold_positive_flux_p_above_nq03_envelope"]
    + d["other"]
    != d["examined_count"]
):
    fail("outside route partition does not close")
if d["ordinary_positive_flow_flux_ge_threshold"] != 1401:
    fail("ordinary positive-flow count")
if d["subthreshold_positive_flux_p_above_nq03_envelope"] != 0:
    fail("unexpected P-only numerical-envelope remainder")
if d["other"] != 0:
    fail("unclassified outside remainder")
if not d["min_flux_m_per_d"] >= 1.0e-8:
    fail("minimum outside flux is not on main positive-flow branch")
if d["min_flux_over_tcd042_threshold"] <= 1.0:
    fail("outside remainder not separated from threshold")
if sum(d["step_days_counts"].values()) != d["examined_count"]:
    fail("step-day partition does not close")

c = evidence["conclusion"]
if c["tcd042_scope_extension_supported_by_this_evidence"] is not False:
    fail("TCD042 widening overclaim")
if c["p_envelope_extension_supported_by_this_evidence"] is not False:
    fail("NQ03 envelope widening overclaim")
if c["entire_1401_remainder_is_ordinary_positive_flow_branch"] is not True:
    fail("routing conclusion")

for key, value in status["hard_boundaries"].items():
    if value is not False:
        fail("hard-boundary overclaim: " + key)
if status["tcd042_scope_widened"] is not False:
    fail("status widens TCD042")
if status["ordinary_positive_flow_implemented"] is not False:
    fail("status claims ordinary-flow implementation")
if status["ponding_implemented"] is not False:
    fail("status claims ponding implementation")
if status["first_call_runinu_resolved"] is not False:
    fail("status claims Runinu resolution")
if status["production_authorized"] is not False:
    fail("status claims production")

if status["review"]["completed"]:
    if not review_path.exists():
        fail("completed review missing artifact")
    review = json.loads(review_path.read_text())
    if review.get("genuinely_independent") is not False:
        fail("same-agent review misrepresented as independent")
    if review.get("outcome") != "SELF_REVIEW_PASS":
        fail("unexpected same-agent review outcome")
    if any(v != "PASS" for v in review.get("review_axes", {}).values()):
        fail("same-agent review has non-PASS axis")
    if review.get("admission_performed") is not False:
        fail("review attempted admission")
    if review.get("production_authorized") is not False:
        fail("review attempted production authorization")

print("PASS_KT22_LWKM_TCD042_EXCLUSION_ROUTING")
