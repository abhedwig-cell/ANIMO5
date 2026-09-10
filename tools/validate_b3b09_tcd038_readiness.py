#!/usr/bin/env python3
import csv
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B3 = ROOT / "integration" / "animo-b3"

RG05F = "7c61a5031f41d602e996310df6f3958cbd1b511e"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I03 = "814ea660d367494432beb63ea78298d1f6cd73d7"
B3I04 = "400b7cd79f89043e091751707dfa96537587dcf6"
STATEQ01 = "4adae99576eb56978da71f7c8a250e4445fd3bc4"
PREP12 = "3d86de057247adcfeefb82c11d7cf7d5b2cbdf73"
B3B08_TCD028 = "215f3800df5afa5811c1105cec2fb4f77a5548c2"
B3D15 = "22e48f7e2c1eaa1245f034de2d909191d9cfa227"
B3D16 = "8650ea9e716336520d8d7df5f9ea2b393d17ab98"
EXPECTED_DECISION = "QUALIFIED_CLASS_B_ADMISSION_READINESS_GOV04_TIER_C_RESTART_SEMANTICS_INDEPENDENT_REVIEW_REQUIRED"


def req(cond, msg):
    if not cond:
        raise SystemExit("B3B09 FAIL_CLOSED: " + msg)


def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def git_show_json(ref, path):
    return json.loads(git_show(ref, path))


def load_local(name):
    return json.loads((B3 / name).read_text(encoding="utf-8"))


e = load_local("TCD038_READINESS_EVIDENCE.json")
s = load_local("ANIMO-B3B09_STATUS.json")

# Workunit collision resolution and authority basis.
req(e["work_unit"] == "ANIMO-B3B09" and e["target"] == "TCD-038", "wrong workunit or target")
req(e["requested_work_unit"] == "ANIMO-B3B08", "requested alias not preserved")
req(e["requested_id_collision"]["detected"] is True, "B3B08 collision not recorded")
old = git_show_json(B3B08_TCD028, "integration/animo-b3/ANIMO-B3B08_STATUS.json")
req(old["work_unit"] == "ANIMO-B3B08" and old["target"] == "TCD-028", "B3B08 collision evidence drift")
req(e["authoring_base"] == f"ANIMO-RG05F@{RG05F}", "authoring base drift")
req(e["authority_snapshot"]["post_rg05f_atomic_admissions_observed"] == [
    f"ANIMO-B3D15@{B3D15}:TCD-030",
    f"ANIMO-B3D16@{B3D16}:TCD-023",
], "post-RG05F authority snapshot drift")
req(e["authority_snapshot"]["GOV04"] == f"ANIMO-GOV04@{GOV04}", "GOV04 pin drift")
req(e["authority_snapshot"]["GOV03"] == f"ANIMO-GOV03@{GOV03}", "GOV03 pin drift")
req(e["authority_snapshot"]["B3Q01"] == f"ANIMO-B3Q01@{B3Q01}", "B3Q01 pin drift")
req(e["authority_snapshot"]["B3I03_canonical_register"] == f"ANIMO-B3I03@{B3I03}", "B3I03 pin drift")
req(e["authority_snapshot"]["B3I04_incremental_state_intake"] == f"ANIMO-B3I04@{B3I04}", "B3I04 pin drift")
req(e["authority_snapshot"]["STATEQ01"] == f"ANIMO-STATEQ01@{STATEQ01}", "STATEQ01 pin drift")
req(e["authority_snapshot"]["PREP12"] == f"ANIMO-PREP12@{PREP12}", "PREP12 pin drift")

# B0 identity and exact relevant member identities.
source_hash = git_show(RG05F, "reference/source/ANIMO_4.1.5.53.zip.sha256")
test_hash = git_show(RG05F, "reference/testcases/ANIMO_testbank.zip.sha256")
req(e["frozen_identity"]["source_archive_sha256"] in source_hash, "source archive hash not pinned in B0")
req(e["frozen_identity"]["testbank_archive_sha256"] in test_hash, "testbank hash not pinned in B0")
manifest = list(csv.DictReader(io.StringIO(git_show(RG05F, "reference/source/source_manifest.csv"))))
by_path = {r["path"]: r for r in manifest}
for member, spec in e["frozen_identity"]["source_members"].items():
    path = "ANIMO_4.1.5.53/" + member
    req(path in by_path, f"source member missing from frozen manifest: {member}")
    req(by_path[path]["sha256"] == spec["sha256"], f"source member hash drift: {member}")
    req(int(by_path[path]["size_bytes"]) == spec["size_bytes"], f"source member size drift: {member}")

# Canonical identity remains exactly TCD-038 and OPEN at pinned later register authority.
reg = list(csv.DictReader(io.StringIO(git_show(B3I03, "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"))))
r38s = [r for r in reg if r.get("ID") == "TCD-038"]
req(len(r38s) == 1, "canonical register does not contain exactly one TCD-038")
r38 = r38s[0]
req(r38.get("process") == "crop actual uptake restart initialization", "canonical process drift")
req(r38.get("classification") == "RESERVED_POST_G5_LOCAL_RESTART_INITIALIZATION_DIRECTION_DEFECT", "canonical classification drift")
req(r38.get("status") == "OPEN", "pinned TCD-038 is not OPEN")
req(e["canonical_register_state"]["status"] == "OPEN", "local evidence overstates canonical status")

# PREP12/PREP10 B1 evidence is reused without evidence-strength promotion.
p12 = git_show_json(PREP12, "integration/animo-prep12/source/PREP10_PLANT_UPTAKE_RESTART_CONTINUITY.json")
req(p12["evidence_class"] == "DIAGNOSTIC_NOT_REFERENCE_PLUS_SOURCE_BOUND", "PREP12 evidence class drift")
req(p12["source_archive_sha256"] == e["frozen_identity"]["source_archive_sha256"], "PREP12 source identity drift")
req(p12["testbank_sha256"] == e["frozen_identity"]["testbank_archive_sha256"], "PREP12 testbank identity drift")
a = p12["TCD_033"]
req(a["classification"] == "CONFIRMED_LEGACY_PLANT_ACTUAL_UPTAKE_RESTART_INITIALIZATION_DIRECTION_DEFECT", "source-local actual uptake classification drift")
req(len(a["natural_case_replication"]) == 4, "natural actual-uptake replication count drift")
req(all(x["post_Inicalc_Amplni_act"] == 0.0 for x in a["natural_case_replication"]), "legacy N loss not replicated in all pinned natural cases")
req(all(x["post_Inicalc_Amplpo_act"] == 0.0 for x in a["natural_case_replication"]), "legacy P loss not replicated in all pinned natural cases")
req(a["minimal_probe"].startswith("assign Amplni_act=Rsamplni_act"), "minimal direction probe drift")
req(a["LWKM_post_Inicalc_probe"]["Amplni_act_kg_m2_N"] == 0.0666813, "LWKM corrected N handoff drift")
req(a["LWKM_post_Inicalc_probe"]["Amplpo_act_kg_m2_P"] == 0.0088759, "LWKM corrected P handoff drift")
req(a["production_correction_admitted"] is False, "PREP12 unexpectedly admits production correction")
req(e["b1_causal_evidence"]["b2_strength_claimed"] is False, "B1 evidence promoted to B2")

# STATEQ01 and later STATEQ02 intake may not be promoted beyond their qualified scopes.
recon = git_show(STATEQ01, "docs/state/PREP12_RESTART_EVIDENCE_RECONCILIATION.md")
req("QUALIFIED_RECONCILIATION_NO_EVIDENCE_STRENGTH_UPGRADE" in recon, "STATEQ01 reconciliation strength boundary drift")
req("CORE_CNP_WITH_CROP`" in recon and "blocked by explicit crop restart-continuity findings" in recon, "STATEQ01 crop blocker boundary drift")
state2intake = git_show(B3I04, "docs/b3/POST_STATEQ02_INCREMENTAL_STATE_INTAKE.md")
req("explicitly excludes GHG, macropores" in state2intake and "unresolved internal-crop restart state" in state2intake, "STATEQ02 exclusion boundary drift")
req(e["split_run_evidence"]["stateq01_used_as_tcd038_admission_proof"] is False, "STATEQ01 improperly promoted")
req(e["split_run_evidence"]["stateq02_used_to_retire_or_admit_tcd038"] is False, "STATEQ02 improperly promoted")
req(e["split_run_evidence"]["tcd038_specific_split_run_discriminator"] == "NOT_CAUSALLY_ISOLATED", "split-run uncertainty hidden")

# GOV03 allows historical-uncertainty route but creates no B2.
g3 = git_show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
req(g3["work_status"]["qualified"] is True, "GOV03 not qualified")
req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 closure drift")
req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 route drift")
req(g3["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 unexpectedly recovered B2")
req(e["historical_route"]["historical_revision53_native_behaviour"] == "UNKNOWN_WITHOUT_B2", "historical uncertainty overclaimed")

# B3 Class B is retained, but GOV04 strictest trigger forces risk Tier C.
g4 = git_show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
req(g4["governance_semantics"]["qualification_class_is_not_risk_tier"] is True, "GOV04 class/tier separation missing")
req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "GOV04 strictest-trigger principle missing")
forced = set(g4["risk_tiers"]["C"]["forced_tier_triggers"])
for trigger in ("RESTART_OR_COLD_START_DISCRIMINATION", "INITIALIZATION_SEMANTICS", "CHECKPOINT_SEMANTICS"):
    req(trigger in forced, f"required GOV04 Tier-C trigger absent: {trigger}")
    req(e["gov04_risk"]["forced_tier_c_triggers"][trigger] is True, f"TCD-038 did not apply Tier-C trigger: {trigger}")
req(e["b3_qualification"]["class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "B3 qualification class drift")
req(e["gov04_risk"]["selected_tier"] == "C", "TCD-038 risk tier is not C")
req(e["gov04_risk"]["tier_b_permitted"] is False, "Tier B incorrectly permitted")
req(e["gov04_risk"]["forced_tier_c_triggers"]["SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY"] is False, "resolved ownership incorrectly left ambiguous")
req(e["gov04_risk"]["required_independent_review_count"] == 1, "independent review count is not exactly one")

# Claim-scoped restart/state contract and candidate boundaries.
c = e["restart_state_contract"]
req(c["contract_state"] == "QUALIFIED_CLAIM_SCOPED_TIER_C_RESTART_HANDOFF_CONTRACT", "restart contract not qualified")
req(c["ownership_ambiguity_remaining"] is False, "ownership ambiguity remains")
req(c["input_read_direction"] == "serialized Rsampl*_act -> accepted Ampl*_act", "restore direction drift")
req(c["checkpoint_representation_changed_by_candidate"] is False, "checkpoint representation widened")
req(c["checkpoint_restore_semantics_changed_by_candidate"] is True, "restart semantics change hidden")
req(c["separate_restart_discriminator_present_on_orgpla_initialization_path"] is False, "invented restart discriminator")
req(c["potential_uptake_in_scope"] is False, "TCD-039 leaked into TCD-038 contract")
ci = e["candidate_identity"]
req(ci["production_candidate_applied"] is False, "production candidate applied")
req(len(ci["conceptual_insertions_only"]) == 2, "candidate is not exactly two guarded direction assignments")
req(ci["existing_trigger_retained"] is True and ci["existing_threshold_retained"] is True and ci["existing_p_guard_retained"] is True, "legacy guards/policy not retained")
req(ci["serialization_layout_changed"] is False and ci["new_state_introduced"] is False, "candidate changes representation/state model")
req(ci["numerical_policy_changed"] is False and ci["solver_changed"] is False and ci["tolerance_changed"] is False, "numerical scope creep")
req(ci["tcd039_composed"] is False, "TCD-039 composition detected")

# Tier-C pre-review gates must be explicitly closed without hiding non-applicability or uncertainty.
gates = e["tier_c_pre_review_gates"]
required_pass_prefix = [
    "B0_IDENTITY", "B1_CAUSAL_EVIDENCE_WHERE_APPLICABLE", "B2_ROUTE_OR_GOV03_HISTORICAL_UNCERTAINTY_ROUTE",
    "AUTHORITATIVE_THEORY_OR_EXACT_DOMAIN_CONTRACT", "STATE_OWNERSHIP_AND_UNITS_WHERE_APPLICABLE",
    "INITIALIZATION_AND_RESTART_SEMANTICS_WHERE_APPLICABLE", "FAILURE_AND_FALLBACK_BEHAVIOUR_WHERE_APPLICABLE",
    "EXPECTED_DIFFERENCE_PREDECLARED", "CONSERVATION", "NON_INTERFERENCE", "EDGE_AND_BOUNDARY_CASE_COVERAGE",
    "RESIDUAL_UNCERTAINTY_EXPLICIT", "HISTORICAL_UNKNOWN_PRESERVED_WITHOUT_B2", "NO_PRODUCTION_AUTHORIZATION"
]
for key in required_pass_prefix:
    req(str(gates[key]).startswith("PASS"), f"Tier-C pre-review gate not passed: {key}")
req(gates["NUMERICAL_POLICY_AND_CONVERGENCE_EVIDENCE_WHERE_APPLICABLE"] == "NOT_APPLICABLE_NO_NUMERICAL_CHANGE", "numerical non-applicability not explicit")

# Status and hard boundaries. Review may be prepared later, but never performed here.
req(s["work_unit"] == "ANIMO-B3B09" and s["target"] == "TCD-038", "status identity drift")
req(s["decision"] == EXPECTED_DECISION, "status decision drift")
req(s["b3_qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "status B3 class drift")
req(s["gov04_risk_tier"] == "C", "status GOV04 tier drift")
req(s["historical_revision53_behaviour"] == "UNKNOWN_WITHOUT_B2", "status historical uncertainty drift")
req(s["independent_review"]["required"] is True and s["independent_review"]["required_count"] == 1, "status independent review requirement drift")
req(s["independent_review"]["status"] == "PENDING_NOT_EXECUTED", "independent review improperly completed in authoring context")
req(s["b3_admitted"] is False and s["production_authorized"] is False, "readiness workunit over-admitted")
for key, value in s["hard_boundaries"].items():
    req(value is False, f"forbidden side effect recorded: {key}")

handoff = B3 / "TCD038_INDEPENDENT_REVIEW_HANDOFF.json"
if handoff.exists():
    h = json.loads(handoff.read_text(encoding="utf-8"))
    req(h["work_unit"] == "ANIMO-B3B09" and h["target"] == "TCD-038", "handoff identity drift")
    req(h["review_required_count"] == 1 and h["review_tier"] == "C", "handoff does not define exactly one Tier-C review")
    req(h["review_performed"] is False, "review performed in authoring context")
    req(h["source_readiness_decision"] == EXPECTED_DECISION, "handoff readiness decision drift")

print("B3B09 PASS: TCD-038 is a bounded B3 Class-B direction correction escalated by GOV04 to Tier C for restart/initialization/checkpoint semantics; the claim-scoped restore contract is pinned, historical behaviour remains unknown without B2, TCD-039 is excluded, and production/review gates remain closed.")
