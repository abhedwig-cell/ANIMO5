#!/usr/bin/env python3
"""Fail-closed static validator for ANIMO-UBQ03."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3"
EVIDENCE = ROOT / "integration/animo-science/UBQ03_HETOP_ZERO_DOMAIN.json"
STATUS = ROOT / "integration/animo-science/ANIMO-UBQ03_STATUS.json"
DOC = ROOT / "docs/numerics/HETOP_ZERO_THICKNESS_SEMANTICS.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def changed_paths() -> list[str]:
    p = subprocess.run(["git", "diff", "--name-only", BASE, "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def main() -> None:
    e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    d = DOC.read_text(encoding="utf-8")

    require(e["work_unit"] == "ANIMO-UBQ03", "wrong evidence owner")
    require(e["frozen_identity"]["source_archive_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "source identity drift")
    require(e["frozen_identity"]["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "testbank identity drift")
    require(e["documentation_contract"]["declared_range"] == "[0.0 ... 0.2]", "documentation range changed")
    require(e["parser_contract"]["hetop_zero_accepted"] is True, "zero no longer parser-admissible")
    require(e["parser_contract"]["lower_rejection_condition"] == "Value.Lt.Low", "lower-bound semantics changed")

    sites = e["direct_division_sites"]
    require(len(sites) == 9 and e["direct_division_site_count"] == 9, "division inventory count mismatch")
    by_file = {}
    for x in sites:
        by_file.setdefault(x["file"], []).append(x["line"])
    require(by_file == {
        "Addit.for": [361, 363, 365, 367],
        "UBoundconc.for": [114],
        "Uptpar_Grass.for": [92, 194],
        "Uptpar_Plant.for": [110, 283],
    }, "division inventory changed")
    require(e["explicit_zero_thickness_guard_for_division_sites_found"] is False, "unexpected zero-thickness guard claimed")

    matrix = {x["condition"]: x for x in e["upper_boundary_path_matrix"]}
    require(matrix["Flpn=0 AND Flux>=1.0d-8 AND Hetop=0"]["legacy_UBoundconc_direct_division"] is True, "ordinary positive-flow singularity lost")
    require(matrix["Flpn=0 AND 0<Flux<1.0d-8 AND Hetop=0"]["legacy_UBoundconc_direct_division"] is False, "E1 fallback incorrectly called a legacy division")
    require(matrix["Flpn=0 AND Flux=0 AND Hetop=0"]["legacy_UBoundconc_direct_division"] is False, "B1 fallback incorrectly called a legacy division")

    tb = e["testbank_domain"]
    require(tb["soil_input_files_checked"] == 9, "testbank case count changed")
    require(tb["observed_Hetop_values_m"] == [0.02], "testbank HETOP surface changed")
    require(tb["Hetop_zero_case_present"] is False, "unexpected zero HETOP natural fixture claimed")

    eff = e["tcd042_effect"]
    require(eff["B1_positive_Hetop_limit_invalidated"] is False, "B1 positive-Hetop result invalidated")
    require(eff["E1_positive_Hetop_policy_invalidated"] is False, "E1 positive-Hetop result invalidated")
    require(eff["full_raw_child_trigger_domain_covered"] is False, "raw child domain silently widened")
    require(eff["silent_Hetop_positive_guard_authorized"] is False, "silent guard authorized")
    require(eff["input_lower_bound_change_authorized"] is False, "input behavior change authorized")

    rb = e["runtime_claim_boundary"]
    require(rb["historical_B2_execution_at_Hetop_zero_available"] is False, "historical B2 invented")
    require(rb["exact_historical_exception_or_nan_behavior_claimed"] is False, "exact historical FPE behavior invented")
    require(rb["global_claim_that_every_Hetop_zero_run_fails"] is False, "overbroad failure claim")

    cd = e["canonical_disposition"]
    require(cd["new_top_level_tcd_reserved"] is False and cd["tcd_043_reserved"] is False, "new TCD allocated")
    require(cd["scientific_admission"] is False and cd["production_change"] is False, "UBQ03 performed forbidden admission/change")

    require("fallback itself is not the source of a division" in d, "document lacks E1/B1 distinction")
    require("does not prove that every possible `Hetop=0` execution fails" in d, "document lacks conditional-runtime claim boundary")

    require(s["work_unit"] == "ANIMO-UBQ03", "wrong status owner")
    for key, value in s["scope_guards"].items():
        require(value is False, f"scope guard violated: {key}")

    allowed = (
        ".github/workflows/animo-ubq03-",
        "docs/numerics/HETOP_ZERO_THICKNESS_SEMANTICS.md",
        "integration/animo-science/UBQ03_HETOP_ZERO_DOMAIN.json",
        "integration/animo-science/ANIMO-UBQ03_STATUS.json",
        "tools/ubq03/",
    )
    changed = changed_paths()
    require(changed, "no UBQ03 artifacts")
    for path in changed:
        require(path.startswith(allowed), f"scope widened by {path}")
        require(not path.startswith("src/"), "production source modified")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")

    print("UBQ03 PASS: HETOP=0 input-domain hazard characterized without widening B1/E1 or admitting production change")


if __name__ == "__main__":
    main()
