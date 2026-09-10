#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISP = ROOT / "integration/animo-b3/TCD015_B3_DISPOSITION_GOV03.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3D09_STATUS.json"
DOC = ROOT / "docs/b3/TCD015_GOV03_FORMAL_DISPOSITION.md"

RG05D = "f3d6b9780631bd627f8bca0658a8e3878746e666"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3B01 = "b982242949aecab32b9067cf7910ad75abfc2b19"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
TRANS_SHA = "c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552"
LEGACY = "Reko = (Mt*rsc-Mto*Co)/St - (-Avc*Hv1 + Flo*Con/ld + Flb*Cb/ld + Fid*Coid/ld)"
CANDIDATE = "Reko = (Mt*rsc-Mto*Co)/St - (-Avc*(Hv1-Hv) + Flo*Con/ld + Flb*Cb/ld + Fid*Coid/ld)"
DECISION = "UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03"
ROUTE = "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY"
REVIEW_BRANCH = "review/animo-b3b01r-tcd015-independent-second-line"


def load(path):
    if not path.exists():
        raise SystemExit(f"FAIL missing {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL " + msg)


d = load(DISP)
s = load(STATUS)
doc = DOC.read_text(encoding="utf-8") if DOC.exists() else ""

require(d["record_id"] == "B3D09-TCD015-GOV03-DISPOSITION", "record id")
require(d["tcd_ids"] == ["TCD-015"], "atomic TCD binding")
require(d["atomicity"] == "ATOMIC", "atomicity")
require(d["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "Class-B identity")
require(d["admission_route"] == ROUTE, "route selection")
require(d["disposition"] == "UNRESOLVED_NOT_ADMITTED", "disposition must remain unresolved/not admitted")

require(d["authorities"]["RG05D"] == RG05D, "RG05D authority")
require(d["authorities"]["GOV03"] == GOV03, "GOV03 authority")
require(d["authorities"]["B3B01"] == B3B01, "B3B01 authority")
require(d["authorities"]["B3Q01"] == B3Q01, "B3Q01 authority")
require(d["authorities"]["SYNQ01"] == SYNQ01, "SYNQ01 authority")

b0 = d["identities"]["b0"]
require(b0["source_sha256"] == SOURCE_SHA, "B0 source SHA")
require(b0["testbank_sha256"] == TESTBANK_SHA, "B0 testbank SHA")
require(b0["source_member"] == "ANIMO_4.1.5.53/Transsub.for", "Transsub source member")
require(b0["source_member_sha256"] == TRANS_SHA, "Transsub SHA")
require(b0["authoring_environment_raw_archive_hash_recheck"] == "PASS_2026_09_10", "raw B0 hash recheck")
require(b0["authoring_environment_source_member_hash_recheck"] == "PASS_2026_09_10", "Transsub hash recheck")

scope = d["scope"]
require(scope["legacy_expression"] == LEGACY, "exact legacy expression")
require(scope["Hv"] == "(Mt-Mto)/st", "Hv definition")
require(scope["Hv1"] == "Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv", "Hv1 definition")
require(scope["candidate_nitrate_expression"] == CANDIDATE, "exact candidate expression")
require(scope["candidate_delta_reko"] == "-Avc*Hv", "candidate delta")
require(scope["species_scope"] == "NITRATE_ONLY", "nitrate-only scope")
require(scope["feature_scope"] == "CORE_NITRATE_TRANSPORT_GREENHOUSEGASOPTION_0", "GHG=0 scope")
require("non-NITRATE" in scope["implementation_boundary"], "generic shared-substance exclusion")

source = d["source_recheck"]
require(source["raw_source_rechecked_directly"] is True, "direct raw source recheck")
require(source["Transsub_Hv_line"] == "Hv = (Mt-Mto)/st", "direct Hv source line")
require(source["Transsub_Hv1_line"] == "Hv1 = Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv", "direct Hv1 source line")
require(source["target_reconstruction_line"] == LEGACY, "direct target source line")
require(source["generic_shared_routine_confirmed"] is True, "generic Transsub source status")
require("NITRATE" in source["nitrate_call_binding"], "nitrate call binding")

route = d["historical_route"]
require(route["pre_GOV03_state_superseded_for_route_eligibility"] is True, "pre-GOV03 route supersession")
require(route["B2_available"] is False, "B2 must remain unavailable")
require(route["GOV03_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT", "GOV03 closure state")
require(route["G6U"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "G6U state")
require(route["b2_route_gate"] == "PASS", "route gate")
require(route["historical_behaviour"] == "UNKNOWN", "historical behaviour")
require(route["historical_fidelity_claimed"] is False, "historical fidelity must remain false")

causal = d["causal_reconciliation"]
e = causal["dominant_event"]
require(causal["case"] == "LWKM_gras_1040.2021.2045", "LWKM case")
require(e["TITO"] == 2312 and e["layer"] == 1 and e["substance"] == "NITRATE" and e["Iflsol"] == 1, "natural activation coordinates")
require(abs(e["BAPD_minus_BATR_kg_m2"] - 5.7871190198869e-5) < 1e-18, "local residual value")
require(causal["duplicate_mass_identity"] == "Avc*Hv*St*Ld", "duplicate mass identity")
require(causal["duplicate_mass_matches_local_residual"] == "PASS_TO_FLOATING_POINT_ROUNDOFF", "causal mass reconciliation")
require(causal["tolerance_used_for_claim"] is False, "no tolerance in causal claim")

syn = d["SYNQ_O001"]
require(syn["oracle_id"] == "SYNQ-O001", "SYNQ-O001 identity")
require(syn["independence"] == "STRONGLY_INDEPENDENT", "SYNQ-O001 independence")
require(abs(syn["expected_duplicated_Hv_residual_kg_m2"] - 0.004) < 1e-15, "SYNQ-O001 exact discriminator")
require(syn["pass"] is True and syn["B2_created"] is False and syn["historical_behaviour_claimed"] is False, "SYNQ-O001 scope")

b1 = d["additional_B1_non_interference"]
require(b1["matrix_cases"] == 8 and b1["all_cases_completed"] is True, "eight-case B1 matrix")
require(b1["total_compared_files_excluding_stdout"] == 550, "550-file comparison")
require(b1["equal_raw"] == 430 and b1["equal_after_declared_volatile_metadata_normalization"] == 99 and b1["scientifically_different"] == 21, "B1 file counts")
require(b1["all_scientific_differences_within_predeclared_surface"] is True, "expected-difference surface")
require(b1["numerical_tolerance"] is None, "no B1 numerical tolerance")
require(b1["generic_probe_policy_consequence"].startswith("NONE"), "generic probe must not authorize generic correction")

cov = d["branch_coverage"]
require(cov["natural_target_reconstruction_entries"] == 508, "natural reconstruction count")
require(cov["natural_non_nitrate_entries"] == 0, "natural non-nitrate target count")
require(cov["Iflsol_1_natural"] == 486 and cov["Iflsol_3_natural"] == 22, "IFLSOL natural counts")
require(cov["reachable_target_modes_covered"] == [1, 3, 4], "reachable IFLSOL coverage")
require("STRUCTURALLY_UNREACHABLE" in cov["Iflsol_2_target_reconstruction"], "IFLSOL2 structural-unreachability proof")
require("STRUCTURALLY_UNREACHABLE" in cov["Iflsol_5_target_reconstruction"], "IFLSOL5 structural-unreachability proof")
require(cov["coverage_gate"] == "PASS", "coverage gate")

rr = d["readiness_reconciliation"]
for key in [
    "frozen_B0_identity", "canonical_TCD015_binding", "exact_source_seam",
    "exact_Hv_Hv1_storage_decomposition", "natural_LWKM_activation",
    "local_conservation", "SYNQ_O001_scope", "predeclared_expected_difference",
    "additional_B1_non_interference", "IFLSOL_branch_coverage", "nitrate_only_scope",
    "GHG0_qualified_boundary", "generic_shared_substance_correction",
    "clipping_policy_redesign", "tolerance_change", "solver_change",
    "production_source_unchanged"
]:
    require(str(rr[key]).startswith("PASS"), f"readiness gate {key}")

required_unchanged = set(d["expected_difference"]["required_unchanged"])
for text in [
    "negative-concentration trigger and Optneg policy",
    "Vsmall and all clipping constants",
    "all solver and convergence tolerances",
    "all non-NITRATE Transsub paths under the species-scoped candidate",
    "GreenHouseGasOption-enabled behaviour is not claimed"
]:
    require(text in required_unchanged, f"required unchanged surface: {text}")

g = d["gates"]
require(g["b2_route"] == "PASS_GOV03_HISTORICAL_UNCERTAINTY_ROUTE", "GOV03 route gate")
for key in ["b0_identity", "b1_evidence", "theory_or_exact_identity", "causal", "conservation", "expected_difference", "non_interference", "coverage", "class_specific", "residual_uncertainty", "composition_if_applicable"]:
    require(str(g[key]).startswith("PASS"), f"gate {key}")
require(g["independent_review"] == "FAIL_PENDING_NOT_COMPLETED", "independent review must remain blocking")

review = d["independent_review"]
require(review["same_authoring_context_may_count"] is False, "same authoring context independence boundary")
require(review["existing_PR21_same_account_COMMENTED_handoff_is_independent"] is False, "PR21 comment cannot count as independent review")
require(review["review_status_at_reconciliation"] == "PENDING_INDEPENDENT_REVIEW", "review pending")
require(review["planned_handoff_branch"] == REVIEW_BRANCH, "review branch")
require(review["gate"] == "BLOCKING", "review gate blocking")

ad = d["admission_decision"]
require(ad["admitted"] is False, "TCD015 not admitted")
require(ad["decision"] == DECISION, "formal decision")
for key in ["historical_fidelity_claimed", "production_patch_authorized", "production_migration_admitted", "B4_admitted", "composition_admitted"]:
    require(ad[key] is False, f"non-admission {key}")

require(s["work_unit"] == "ANIMO-B3D09", "status workunit")
require(s["branch"] == "work/animo-b3d09-tcd015-gov03-disposition", "status branch")
require(s["base"]["head"] == RG05D, "status RG05D base")
require(s["authorities"]["readiness"] == f"ANIMO-B3B01@{B3B01}", "status readiness authority")
require(s["authorities"]["B3_framework"] == f"ANIMO-B3Q01@{B3Q01}", "status framework authority")
require(s["authorities"]["historical_route"] == f"ANIMO-GOV03@{GOV03}", "status GOV03 authority")
require(s["route"]["route_gate"] == "PASS" and s["route"]["historical_behaviour"] == "UNKNOWN", "status route and historical uncertainty")
require(s["scientific_gate_summary"]["independent_second_line_review"] == "FAIL_PENDING_NOT_COMPLETED", "status review blocker")
require(s["review_handoff"]["planned_branch"] == REVIEW_BRANCH, "status review handoff branch")
for key, value in s["admission"].items():
    require(value is False, f"status admission boundary {key}")
for key in ["shared_Transsub_generic_correction_authorized", "GreenHouseGasOption_enabled_qualified", "clipping_policy_changed", "numerical_tolerance_changed", "solver_changed", "production_source_modified", "legacy_source_modified", "testcase_modified", "independent_review_executed_in_this_context"]:
    require(s["hard_boundaries"][key] is False, f"status hard boundary {key}")

allowed_states = {
    "IN_PROGRESS_PERSISTED_TCD015_FORMAL_DISPOSITION_VALIDATION_PENDING",
    "QUALIFIED_TCD015_FORMAL_DISPOSITION_ROUTE_OPEN_INDEPENDENT_REVIEW_PENDING_NO_ADMISSION"
}
require(s["state"] in allowed_states, "allowed workunit state")
if s["state"].startswith("QUALIFIED_"):
    require(s["decision"] == DECISION, "qualified status decision")
    require(s["work_status"] == {"realized": True, "persisted": True, "tested": True, "qualified": True, "work_unit_complete": True}, "qualified work status")
    require(s["validation"]["tested_head"], "qualified tested head")
    require(s["validation"]["github_actions_run_id"], "qualified workflow run")
    require(s["validation"]["github_actions_conclusion"] == "success", "qualified workflow conclusion")
    require(s["validation"]["validator_result"] == "PASS", "qualified validator result")
    require(s["validation"]["scope_guard"] == "PASS_B3D09_SCOPE_GUARD", "qualified scope guard")
else:
    require(s["decision"] == "PENDING_FAIL_CLOSED_VALIDATION", "pending status decision")
    require(s["work_status"]["tested"] is False and s["work_status"]["qualified"] is False, "pending work status")

for phrase in [
    "Historical behaviour remains `UNKNOWN`",
    "No historical fidelity is claimed",
    "No generic shared-substance correction is authorized",
    "GreenHouseGasOption=0",
    "genuinely independent second-line review",
    "TCD-015 therefore remains **NOT ADMITTED**",
    "no production patch",
    "no B4 step",
    "no central RG05 update",
    "no composition"
]:
    require(phrase in doc, f"documentation phrase: {phrase}")

print("PASS_B3D09_TCD015_GOV03_DISPOSITION")
