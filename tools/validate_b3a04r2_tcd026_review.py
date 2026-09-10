#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

BASE = "bd19ee247ba910eee234c67ec74def28d376c779"
REPORT = Path("docs/b3/TCD026_INDEPENDENT_SECOND_LINE_REVIEW.md")
MACHINE = Path("integration/animo-b3/TCD026_INDEPENDENT_SECOND_LINE_REVIEW.json")
ALLOWED_CHANGED_PATHS = {
    ".github/workflows/animo-b3a04r2-tcd026-independent-second-line.yml",
    "docs/b3/TCD026_INDEPENDENT_SECOND_LINE_REVIEW.md",
    "integration/animo-b3/TCD026_INDEPENDENT_SECOND_LINE_REVIEW.json",
    "tools/validate_b3a04r2_tcd026_review.py",
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def main():
    require(REPORT.is_file(), f"missing {REPORT}")
    require(MACHINE.is_file(), f"missing {MACHINE}")

    report = REPORT.read_text(encoding="utf-8")
    data = json.loads(MACHINE.read_text(encoding="utf-8"))

    require(data["work_unit"] == "ANIMO-B3A04R2", "wrong work unit")
    require(data["target_tcd"] == "TCD-026", "wrong target TCD")
    require(data["reviewed_handoff_head"] == BASE, "wrong reviewed handoff head")
    require(data["result"] in {"PASS", "FAIL", "INCOMPLETE"}, "invalid semantic result")
    require(data["result"] == "PASS", "review result is not PASS")
    require("Result: `PASS`" in report and "## Decision" in report, "human report PASS missing")

    independence = data["independence"]
    require(independence["separate_chatgpt_context_from_b3a04_b3a04r_b3d07_authoring"] is True,
            "separate ChatGPT context not asserted")
    require(independence["organizational_or_human_independence_claimed"] is False,
            "organizational/human independence must not be claimed")

    authorities = data["reviewed_authorities"]
    expected_authorities = {
        "readiness": "ANIMO-B3A04@5eaf02298603b85f802d8e35d6a63941d0878879",
        "same_context_technical_review_evidence_only": "ANIMO-B3A04R@27b1700a330959d1b5eae23a2094cad579630f14",
        "formal_route_reconciliation": "ANIMO-B3D07@21766eaf3443bcf432f05fbf6ba89d365bc70988",
        "historical_route": "ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c",
        "b3_framework": "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
        "stateq02_support_boundary": "ANIMO-STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6",
        "synq01": "ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121",
    }
    for key, value in expected_authorities.items():
        require(authorities[key] == value, f"wrong authority {key}")

    b0 = data["frozen_B0"]
    require(b0["source_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566",
            "wrong frozen source identity")
    require(b0["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84",
            "wrong frozen testbank identity")

    claim = data["atomic_claim"]
    require(claim["candidate"] == "Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P",
            "wrong atomic candidate")
    require(data["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", "wrong qualification class")

    checks = data["independent_checks"]
    require(len(checks) == 19, "must contain exactly 19 independent checks")
    require([c["id"] for c in checks] == list(range(1, 20)), "check ids must be 1..19")
    require(all(c["status"] == "PASS" for c in checks), "every required check must PASS")

    synq = data["source_bound_evidence"]["synq01_oracle_register"]
    require(synq["blob"] == "4c215d19844614de8868380fb03f93268ea4c5d8", "wrong SYNQ01 register blob")
    require(synq["oracle_count"] == 12, "wrong SYNQ01 oracle count")
    require(synq["tcd026_matches"] == 0, "TCD-026-specific SYNQ01 oracle must remain absent")

    live = data["live_head_checks_before_write"]
    require(live["review_branch"] == BASE, "review branch was not clean at pre-write check")
    require(live["b3d07_branch"] == "21766eaf3443bcf432f05fbf6ba89d365bc70988", "wrong live B3D07 head")
    require(live["gov03_branch"] == "cbd262bdabe92923113b7326f2f42822ce9a971c", "wrong live GOV03 head")

    hist = data["historical_uncertainty"]
    require(hist["qualified_B2_exists"] is False, "qualified B2 must remain absent")
    require(hist["historical_revision53_behaviour"] == "UNKNOWN", "historical behaviour must remain UNKNOWN")
    require(hist["historical_fidelity_claimed"] is False, "historical fidelity must not be claimed")
    require(hist["synthetic_or_diagnostic_evidence_promoted_to_B2"] is False,
            "synthetic/diagnostic evidence must not be promoted to B2")

    expected = data["expected_difference"]
    require(expected["global_synthetic_allowed_changed_outputs"] == [
        "ani_omGP.Bal", "ani_omRP.Bal", "ani_omTP.Bal",
        "baomGP.Out", "baomRP.Out", "baomTP.Out"
    ], "wrong global expected-difference whitelist")
    require(expected["restart_activation_allowed_changed_subset"] == [
        "ani_omMP.Bal", "ani_omTP.Bal", "baomMP.Out", "baomTP.Out"
    ], "wrong restart expected-difference subset")
    require(expected["unexpected_difference_policy"] == "FAIL_CLOSED", "unexpected differences must fail closed")
    require(expected["tolerance_used_for_scope_or_non_interference"] is False, "scope tolerance must remain false")

    bounds = data["boundaries"]
    for key in (
        "initialization_physics_changed",
        "physical_state_changed",
        "process_flux_changed",
        "restart_state_changed_by_candidate",
        "forcing_changed",
        "numerical_policy_changed",
        "other_organic_matter_tcds_composed",
        "whole_model_continuous_vs_formatted_restart_identity_claimed",
        "production_source_modified",
        "production_patch_authorized",
        "B3_admission_performed",
        "B4_admission_performed",
        "production_migration_performed",
    ):
        require(bounds[key] is False, f"boundary {key} must remain false")

    decision = data["review_decision"]
    require(decision["review_passed"] is True, "review pass flag missing")
    require(decision["review_evidence_only"] is True, "review evidence-only boundary missing")
    require(decision["B3_admitted"] is False, "review must not admit B3")

    lower_report = report.lower()
    require("raw-byte parse" in lower_report, "raw-source limitation not documented")
    require("historical revision-53 behaviour remains `unknown`" in lower_report,
            "historical UNKNOWN boundary not explicit")
    require("not converted into a tolerance" in lower_report, "restart negative boundary not explicit")
    require("no tcd-026-specific synq01 oracle" in lower_report, "SYNQ01 absence not explicit")
    require("no admission" in lower_report, "non-admission boundary not explicit")

    changed = {p for p in git("diff", "--name-only", f"{BASE}..HEAD").splitlines() if p}
    require(changed == ALLOWED_CHANGED_PATHS,
            f"scope guard failed; changed paths={sorted(changed)}")

    for path in changed:
        require(not path.startswith("src/"), f"production source changed: {path}")
        require(not path.startswith("reference/"), f"frozen reference changed: {path}")
        require(not path.startswith("test"), f"testcase surface changed: {path}")

    print("PASS")


if __name__ == "__main__":
    main()
