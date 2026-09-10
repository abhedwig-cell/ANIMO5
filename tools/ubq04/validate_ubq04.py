#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-UBQ04 HETOP zero-semantics qualification."""
from __future__ import annotations

import json
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "8f01f0cb366dfa8cc63a184d6f885100899a8cd9"
EVIDENCE = ROOT / "integration/animo-science/UBQ04_HETOP_ZERO_SEMANTICS.json"
STATUS = ROOT / "integration/animo-science/ANIMO-UBQ04_STATUS.json"
DOC = ROOT / "docs/numerics/HETOP_ZERO_MODEL_SEMANTICS_QUALIFICATION.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def changed_paths() -> list[str]:
    p = subprocess.run(
        ["git", "diff", "--name-only", BASE, "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def main() -> None:
    e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    d = DOC.read_text(encoding="utf-8")

    require(e["work_unit"] == "ANIMO-UBQ04", "wrong evidence owner")
    eb = e["evidence_boundary"]
    require(eb["source_sha256"] == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "source identity drift")
    require(eb["testbank_sha256"] == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "testbank identity drift")
    require(eb["process_reference_full_text_available_in_controlled_evidence"] is False, "uncontrolled process report silently promoted")

    doc = e["documentation_findings"]
    require(doc["table_6_range"] == "[0.0 ... 0.2]", "documented endpoint changed")
    require(doc["zero_value_semantics_explicitly_defined"] is False, "zero semantics invented from documentation")
    require(doc["zero_value_declared_as_disable_switch"] is False, "disable sentinel invented")
    require(doc["zero_value_declared_as_instantaneous_passthrough"] is False, "passthrough sentinel invented")
    require(doc["zero_value_declared_invalid"] is False, "invalid endpoint invented")
    require(doc["example_input_order_conflict"]["internal_documentation_consistency"] == "CONFLICTING", "guide conflict lost")

    src = e["revision53_source_findings"]
    require(src["parser"]["read_order"] == "Hetop, He(0)", "parser order changed")
    require(src["parser"]["zero_accepted"] is True, "zero no longer parser-admissible")
    require(src["explicit_Hetop_value_branch_found"] is False, "zero branch invented")
    require(src["zero_sentinel_implementation_found"] is False, "zero sentinel invented")
    files = {x["file"] for x in src["sites"]}
    require(files == {"Addit.for", "UBoundconc.for", "Uptpar_Grass.for", "Uptpar_Plant.for"}, "source surface changed")

    recon = e["mathematical_reconstruction"]
    require(recon["positive_Hetop_no_ponding_equation"] == "HETOP*dC/dt = Load - Flux*C", "reservoir equation changed")
    require(recon["positive_flux_zero_capacity_limit"]["unique_for_this_restricted_condition"] is True, "restricted positive-flow limit lost")
    require(recon["zero_flux_limit"]["finite_global_concentration_semantics_unique"] is False, "global zero-flow uniqueness incorrectly claimed")
    require(recon["relation_to_TCD042_E1"]["NQ03_small_P_policy_extendable_to_Hetop_zero"] is False, "NQ03 scope silently widened")

    # Equation-derived sanity check only: at zero throughflow with positive load,
    # Delta C = Load*St/H. Reducing H by a decade must increase Delta C by a decade.
    getcontext().prec = 50
    load = Decimal("0.23")
    st = Decimal("1")
    h1 = Decimal("1e-3")
    h2 = Decimal("1e-4")
    dc1 = load * st / h1
    dc2 = load * st / h2
    require(dc2 == Decimal(10) * dc1, "zero-flow divergence reconstruction failed")

    candidates = e["candidate_interpretations"]
    require(len(candidates) == 3, "candidate interpretation inventory changed")
    require(all(x["qualified"] is False for x in candidates), "a zero policy was silently selected")
    names = {x["candidate"] for x in candidates}
    require(names == {"INPUT_ENDPOINT_INVALID", "ZERO_CAPACITY_INSTANTANEOUS_PASSTHROUGH", "CONDITIONALLY_ADMISSIBLE_ZERO"}, "candidate set changed")

    q = e["qualification_result"]
    require(q["semantic_nonuniqueness_proven"] is True, "nonuniqueness result lost")
    for key in (
        "zero_thickness_policy_selected",
        "input_rejection_authorized",
        "instantaneous_passthrough_authorized",
        "conditional_zero_domain_authorized",
        "positive_Hetop_B1_or_E1_invalidated",
        "new_TCD_reserved",
        "scientific_admission",
        "production_change",
    ):
        require(q[key] is False, f"forbidden qualification effect: {key}")
    require(q["decision"] == "QUALIFIED_HETOP_ZERO_SEMANTIC_NONUNIQUENESS_NO_MODEL_POLICY_SELECTED", "wrong decision")

    require("The answer is no." in d, "document does not state fail-closed answer")
    require("cannot simply be promoted to a universal `HETOP=0` policy" in d, "positive-flow limit overgeneralized")
    require("cannot be extended toward `HETOP=0`" in d, "NQ03 non-extension missing")

    require(s["work_unit"] == "ANIMO-UBQ04", "wrong status owner")
    for key, value in s["scope_guards"].items():
        require(value is False, f"scope guard violated: {key}")

    allowed = (
        ".github/workflows/animo-ubq04-",
        "docs/numerics/HETOP_ZERO_MODEL_SEMANTICS_QUALIFICATION.md",
        "integration/animo-science/UBQ04_HETOP_ZERO_SEMANTICS.json",
        "integration/animo-science/ANIMO-UBQ04_STATUS.json",
        "tools/ubq04/",
    )
    changed = changed_paths()
    require(changed, "no UBQ04 artifacts")
    for path in changed:
        require(path.startswith(allowed), f"scope widened by {path}")
        require(not path.startswith("src/"), "production source modified")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")

    print("UBQ04 PASS: HETOP=0 semantics are demonstrably non-unique in the controlled evidence; no zero policy, TCD, admission or production change selected")


if __name__ == "__main__":
    main()
