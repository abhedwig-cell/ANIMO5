#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3A09 / TCD-037-A4 Tier-A readiness."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "ca3b6fba99ddc70e1f063ac98088f8825f467c1a"
B3D25 = "4da2dd067069944a5e3eeb5f532566a23402bd68"
RG05I = "94afe7d649a8c60758a41996f0059de0acddd2fc"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
B3Q01 = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
READINESS = ROOT / "integration/animo-b3/TCD037_A4_TIER_A_READINESS.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3A09_STATUS.json"
ALLOWED = {
    ".github/workflows/animo-b3a09-tcd037-a4.yml",
    "docs/b3a09/WORK_UNIT_CONTRACT.md",
    "docs/b3a09/TCD037_A4_TIER_A_READINESS.md",
    "integration/animo-b3/TCD037_A4_TIER_A_READINESS.json",
    "integration/animo-b3/ANIMO-B3A09_STATUS.json",
    "tools/validate_b3a09_tcd037_a4.py",
}


def req(cond, msg):
    if not cond:
        raise SystemExit("B3A09 FAIL_CLOSED: " + msg)


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def show_json(ref, path):
    return json.loads(run("git", "show", f"{ref}:{path}"))


def main():
    rd = json.loads(READINESS.read_text())
    st = json.loads(STATUS.read_text())

    req(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT).returncode == 0,
        "SYNQ05 base is not ancestor")

    syn = show_json(BASE, "integration/animo-synthetic/ANIMO-SYNQ05_STATUS.json")
    oracle = show_json(BASE, "integration/animo-synthetic/SYNQ05_TCD037_A4_ORACLE.json")
    req(syn["state"] == "QUALIFIED_TCD037_A4_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2",
        "SYNQ05 not qualified")
    req(syn["target"] == "TCD-037-A4" and syn["evidence_strength"] == "B1_SYNTHETIC_NOT_B2",
        "wrong SYNQ05 target or strength")
    req(syn["scientific_admission"] is False and syn["tier_a_waiver_granted"] is False,
        "SYNQ05 overclaims admission or waiver")
    req(syn["historical_behavior"] == "UNKNOWN" and syn["historical_fidelity_claimed"] is False,
        "SYNQ05 history promoted")
    req(syn["testcase_translation_performed"] is False and syn["global_Ly_equals_Ln_theorem_claimed"] is False,
        "SYNQ05 testcase or index boundary violated")
    req(oracle["accounting_contract"]["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St",
        "SYNQ05 source owner drift")
    req(oracle["accounting_contract"]["observer_increment"] == "10000*(QEmN2ODif+QEmN2OFlw)*St",
        "SYNQ05 observer identity drift")
    req(oracle["allowed_difference_surface"] == ["Bani(N2Oe)"], "SYNQ05 scope widened")
    req(oracle["frozen_source_provenance"]["raw_source_redistributed"] is False,
        "SYNQ05 source redistribution boundary violated")
    req(set(oracle["cases"]) == {
        "EMISSION_NONZERO_PRODUCTION_ZERO", "PRODUCTION_NONZERO_EMISSION_ZERO", "COMPONENT_PERMUTED",
        "RATE_TIME_EQUIVALENT", "SIGNED_UPTAKE", "INACTIVE"
    }, "SYNQ05 coverage drift")

    latest = show_json(B3D25, "integration/animo-b3/ANIMO-B3D25_STATUS.json")
    req(latest["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY" and
        latest["target_child_atom"] == "TCD-037-A3", "B3D25 latest admission drift")
    req(latest["candidate_admission_effect"]["a4_admitted"] is False and
        latest["candidate_admission_effect"]["parent_tcd_admitted"] is False, "A4 or parent already admitted")
    req(latest["aggregate_policy"]["pending_atomic_admissions_after_rg05i_if_qualified"] == 1 and
        latest["aggregate_policy"]["normal_batch_threshold_reached"] is False, "aggregate cadence drift")

    rg = show_json(RG05I, "integration/animo-reg/ANIMO-RG05I_STATUS.json")
    req(rg["state"] == "QUALIFIED_THIRD_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05H_ADMISSIONS_NO_PRODUCTION",
        "RG05I not qualified")
    req(rg["scientific_admission_count"] == 14 and rg["tcd037_state"]["parent_admitted"] is False,
        "RG05I aggregate state drift")
    req(rg["b4_open"] is False and rg["production_open"] is False, "RG05I downstream gate opened")

    b3i = show_json(B3I07, "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms = {x["atom_id"]: x for x in b3i["atoms"]}
    a4 = atoms["TCD-037-A4"]
    req(a4["class"] == "A_ACCOUNTING_REPORTING_ONLY" and
        a4["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St", "B3I07 A4 identity drift")
    req(a4["allowed_observer_fields"] == ["Bani(N2Oe)"], "B3I07 A4 surface drift")
    req(a4["historical_behavior"] == "UNKNOWN" and
        a4["natural_activation"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "B3I07 evidence boundary drift")
    req(a4["next_work_unit"] == "ANIMO-B3A08 — TCD-037-A4 N2O Atmosphere Emission Observer Tier-A Readiness",
        "historical B3I07 route unexpectedly rewritten")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    req(rq["semantic_qualification"]["n2o_atmosphere_emission_owner"] == "(QEmN2ODif+QEmN2OFlw)*St",
        "RUNTIMEQ03 A4 owner drift")
    req(rq["semantic_qualification"]["n2o_index0_consumer_mismatch"] is True,
        "RUNTIMEQ03 A4 mismatch no longer established")
    req(rq["semantic_qualification"]["n2o_reduction_role"] == "SEPARATE_N2O_REDUCTION_SINK_NOT_TCD037_OBSERVER_PRODUCER",
        "RUNTIMEQ03 N2O reduction role drift")
    for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy"):
        req(rq["expected_difference"][key] == "NONE", "RUNTIMEQ03 non-interference drift: " + key)
    req(rq["historical_intel_behavior"] == "UNKNOWN", "RUNTIMEQ03 historical behavior promoted")

    s1 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    req(s1["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM",
        "SYNQ01 policy drift")

    g5 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
    req(g5["work_status"]["qualified"] is True and g5["assurance_change"]["scientific_gate_reduction"] is False,
        "GOV05 invalid or weakened")
    g4 = show_json(GOV04, "integration/animo-governance/GOV04_REVIEW_INTENSITY_MATRIX.json")
    req(g4["tier_a_independent_review_waiver_conditions"]["logic"] == "ALL_MUST_PASS", "Tier-A waiver logic drift")
    req(g4["governance_semantics"]["strictest_applicable_risk_trigger_wins"] is True, "strictest trigger rule lost")
    g3 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    req(g3["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT",
        "GOV03 B2 closure drift")
    req(g3["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS",
        "GOV03 G6U drift")
    schema = run("git", "show", f"{B3Q01}:integration/animo-b3/B3_DISPOSITION_SCHEMA.json")
    req("^TCD-[0-9]{3}$" in schema, "B3Q01 lineage schema drift")

    req(rd["work_unit"] == "ANIMO-B3A09" and rd["target_child_atom"] == "TCD-037-A4",
        "wrong readiness identity")
    req(rd["target_parent_tcd"] == "TCD-037" and rd["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY" and
        rd["risk_tier_at_readiness"] == "A", "wrong parent/class/tier")
    ident = rd["identifier_reconciliation"]
    req(ident["historical_b3i07_route"] == "ANIMO-B3A08" and ident["historical_route_rewritten"] is False,
        "historical route reconciliation invalid")
    req(ident["collision"] == "ANIMO-B3A08_ALREADY_ALLOCATED_TO_TCD025_MACROPORE_MAIN_LEDGER_READINESS" and
        ident["live_free_identifier_selected"] == "ANIMO-B3A09", "identifier collision not resolved fail-closed")
    req(ident["canonical_atom_identity_changed"] is False and ident["canonical_atom_identity"] == "TCD-037-A4",
        "canonical atom identity changed during identifier allocation")

    claim = rd["atomic_claim"]
    req(claim["atomic"] is True and claim["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St", "atomic owner invalid")
    req(claim["local_observer_increment"] == "10000*(QEmN2ODif+QEmN2OFlw)*St" and
        claim["allowed_observer_fields"] == ["Bani(N2Oe)"], "accounting surface invalid")
    req(claim["global_Ly_equals_Ln_theorem_claimed"] is False, "unsupported global index theorem claimed")
    req(claim["denitrification_observer_in_scope"] is False and claim["nitrification_observer_in_scope"] is False and
        claim["reduction_sink_in_scope"] is False, "A4 scope widened")

    acct = rd["accounting_identity"]
    req(acct["observer_increment"] == "Delta Bani(N2Oe)=10000*(QEmN2ODif+QEmN2OFlw)*St",
        "readiness observer identity drift")
    req(acct["strongest_alternative_rejected"] == "N2O production totals are not the atmosphere-emission owner",
        "alternative ownership discriminator missing")
    req(acct["signed_exchange_semantics"] == "negative atmosphere emission is soil uptake and decreases the observer amount",
        "signed exchange semantics missing")
    req(acct["numerical_acceptance"] == "EXACT_BINARY64_FOR_CHOSEN_DYADIC_SYNTHETIC_VALUES_NO_EMPIRICAL_TOLERANCE",
        "numerical acceptance drift")

    diff = rd["expected_difference"]
    req(diff["allowed_observer_fields"] == ["Bani(N2Oe)"] and diff["predeclared_before_b3a09"] is True,
        "expected difference invalid")
    for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy", "Banh_N2On",
                "Bani_N2Od", "QRdN2O", "unrelated_observer_fields", "sibling_atoms", "tcd032_036"):
        req(diff[key] == "NONE", "unexpected difference " + key)

    cov = rd["coverage"]
    req(cov["synthetic_activation_predicate"] == "PASS" and cov["synthetic_evidence_strength"] == "B1_SYNTHETIC_NOT_B2",
        "coverage predicate invalid")
    req(cov["natural_active_ghg"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH" and
        cov["natural_case_translation_performed"] is False and cov["historical_behavior"] == "UNKNOWN",
        "coverage or history boundary invalid")
    req("NOT_REVIEW_INDEPENDENCE" in cov["synthetic_independence"], "synthetic independence wording can be mistaken for review independence")

    waiver = rd["gov04_tier_a_waiver_predicate"]
    for key, value in waiver.items():
        if key in {"readiness_result", "final_waiver_granted", "final_waiver_grant_deferred_to_admission_workunit"}:
            continue
        req(value in {"PASS", "PASS_IF_EXACT_B3A09_CI_GREEN"}, f"Tier-A predicate not PASS: {key}={value}")
    req(waiver["readiness_result"] == "TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS" and
        waiver["final_waiver_granted"] is False and waiver["final_waiver_grant_deferred_to_admission_workunit"] is True,
        "waiver lifecycle invalid")

    agg = rd["aggregate_context"]
    req(agg["rg05i_snapshot_scientific_admission_count"] == 14 and
        agg["effective_scientific_admission_count_in_lineage"] == 15 and
        agg["effective_post_rg05i_new_admissions"] == ["ANIMO-B3D25:TCD-037-A3"], "aggregate context invalid")
    req(agg["normal_batch_threshold"] == 3 and agg["normal_batch_threshold_reached"] is False and
        agg["aggregate_update_performed_here"] is False, "premature aggregate update")
    req(agg["admitted_children"] == ["TCD-037-A1", "TCD-037-A2", "TCD-037-A3"] and
        agg["unadmitted_children"] == ["TCD-037-A4"] and agg["tcd037_parent_admitted"] is False,
        "TCD-037 child state invalid")

    req(rd["b3q01_child_schema_binding"]["later_disposition_tcd_ids"] == ["TCD-037"] and
        rd["b3q01_child_schema_binding"]["canonical_atomic_child_identity"] == "TCD-037-A4",
        "child binding invalid")
    req(rd["source_provenance"]["raw_source_redistributed"] is False and
        rd["source_provenance"]["frozen_archive_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
        "source provenance boundary invalid")

    req(st["state"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_TCD037_A4_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION"},
        "status lifecycle invalid")
    req(st["target_child_atom"] == "TCD-037-A4" and st["tier_a_waiver"]["final_waiver_granted"] is False,
        "status target or waiver invalid")
    req(st["identifier_reconciliation"]["selected_free_readiness_identifier"] == "ANIMO-B3A09" and
        st["identifier_reconciliation"]["historical_route_rewritten"] is False,
        "status identifier reconciliation invalid")
    req(st["aggregate_context"]["effective_lineage_scientific_admission_count"] == 15 and
        st["aggregate_context"]["aggregate_update_required_now"] is False, "status aggregate cadence invalid")
    for key, value in st["scope_guards"].items():
        req(value is False, "scope guard violated: " + key)

    changed = {x.strip() for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x.strip()}
    req(changed == ALLOWED, "scope differs from exact six-file B3A09 package: " + repr(sorted(changed)))
    for path in changed:
        req(not path.startswith(("src/", "reference/", "production/")), "protected source/B0 modified: " + path)
        req("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")

    print("B3A09 PASS: TCD-037-A4 satisfies retained Tier-A readiness predicate with signed atmosphere-emission ownership; no admission or final waiver performed")


if __name__ == "__main__":
    main()