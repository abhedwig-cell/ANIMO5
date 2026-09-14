#!/usr/bin/env python3
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "bc9e6ed997a078336645210ebb4d99ae976893fe"
REQUIRED = [
    "docs/governance/ANIMO_GOV06_UNIFIED_PROGRAM_REGIE.md",
    "integration/animo-governance/ANIMO_GOV06_WORKUNIT_RESUMPTION_SCHEMA.json",
    "integration/animo-governance/ANIMO_GOV06_SEMANTIC_CONTRACT_OWNERSHIP_SCHEMA.json",
    "integration/animo-governance/ANIMO_GOV06_MODULE_CONTRACT_SCHEMA.json",
    "integration/animo-governance/ANIMO_GOV06_MODULE_REGISTRY.json",
    "integration/animo-governance/ANIMO_GOV06_CAPABILITY_SCOPE_MAP.json",
    "integration/animo-governance/ANIMO_GOV06_DEPENDENCY_WAVE_MAP.json",
    "integration/animo-governance/ANIMO_GOV06_REBASELINE_SNAPSHOT.json",
    "integration/animo-governance/ANIMO-GOV06_STATUS.json",
    "tools/validate_gov06_unified_regie.py",
    ".github/workflows/animo-gov06-unified-regie.yml",
]
OPTIONAL_FINAL = ["integration/animo-governance/ANIMO_GOV06_ADVERSARIAL_REVIEW.json"]
ALLOWED = set(REQUIRED + OPTIONAL_FINAL)

def fail(msg):
    print("GOV06 FAIL:", msg)
    raise SystemExit(1)

def load(path):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path}: {exc}")

def main():
    for p in REQUIRED:
        if not (ROOT / p).exists():
            fail(f"missing required artifact {p}")

    status = load("integration/animo-governance/ANIMO-GOV06_STATUS.json")
    scope = load("integration/animo-governance/ANIMO_GOV06_CAPABILITY_SCOPE_MAP.json")
    waves = load("integration/animo-governance/ANIMO_GOV06_DEPENDENCY_WAVE_MAP.json")
    resume = load("integration/animo-governance/ANIMO_GOV06_WORKUNIT_RESUMPTION_SCHEMA.json")
    own = load("integration/animo-governance/ANIMO_GOV06_SEMANTIC_CONTRACT_OWNERSHIP_SCHEMA.json")
    module_schema = load("integration/animo-governance/ANIMO_GOV06_MODULE_CONTRACT_SCHEMA.json")
    registry = load("integration/animo-governance/ANIMO_GOV06_MODULE_REGISTRY.json")
    snapshot = load("integration/animo-governance/ANIMO_GOV06_REBASELINE_SNAPSHOT.json")

    if status.get("scope") != "GOVERNANCE_ONLY": fail("scope is not governance only")
    if status.get("denominator_status") != "DENOMINATOR_NOT_YET_QUALIFIED": fail("denominator overclaimed")
    if scope.get("denominator_status") != "DENOMINATOR_NOT_YET_QUALIFIED" or scope.get("numeric_completion_authorized") is not False: fail("numeric completion must be disallowed")
    if snapshot.get("b4") != "NOT_OPEN" or snapshot.get("production") != "NOT_OPEN": fail("B4 or production advanced")
    hb = status.get("hard_boundaries", {})
    if not hb or any(v is not False for v in hb.values()): fail("a hard boundary is not explicitly false")

    raw_scope = (ROOT / "integration/animo-governance/ANIMO_GOV06_CAPABILITY_SCOPE_MAP.json").read_text()
    if re.search(r"\b\d+(?:\.\d+)?%", raw_scope) or "completion_percentage" in raw_scope: fail("arbitrary completion percentage found")

    if resume.get("$id") != "ANIMO_GOV06_WORKUNIT_RESUMPTION_SCHEMA_v1": fail("resumption schema identity")
    if own.get("$id") != "ANIMO_GOV06_SEMANTIC_CONTRACT_OWNERSHIP_SCHEMA_v1": fail("ownership schema identity")
    if module_schema.get("$id") != "ANIMO_GOV06_MODULE_CONTRACT_SCHEMA_v1": fail("module schema identity")
    if registry.get("role") != "PROSPECTIVE_GOVERNANCE_INDEX_NOT_SCIENTIFIC_SOURCE_OF_TRUTH": fail("module registry truth-source guard")
    if registry.get("retroactive_invalidation") is not False: fail("retroactive science invalidation")

    allowed_parallel = {"SAFE_PARALLEL","PARALLEL_AFTER_PINNING","SERIAL_REQUIRED"}
    for w in waves.get("waves", []):
        if w.get("parallelism") not in allowed_parallel: fail(f"bad parallel class in {w.get('stream')}")
        for k in ("owner","consumed_contracts","moving_contracts","frozen_dependencies","blocker","next_closure_action"):
            if k not in w: fail(f"wave missing {k}: {w.get('stream')}")
    if not any(w.get("parallelism") == "SERIAL_REQUIRED" for w in waves.get("waves", [])): fail("no serialized shared-authority lane")

    doc = (ROOT / "docs/governance/ANIMO_GOV06_UNIFIED_PROGRAM_REGIE.md").read_text(encoding="utf-8")
    must = ["qualification and admission","child admission and parent admission","PROCESS_SELF_REVIEWED_NOT_INDEPENDENT","synthetic or reconstructed evidence","DENOMINATOR_NOT_YET_QUALIFIED","Branch separation and disjoint filenames are insufficient","Existing qualified B3 science is not invalidated retroactively"]
    for phrase in must:
        if phrase not in doc: fail(f"policy phrase missing: {phrase}")

    try:
        out = subprocess.check_output(["git","diff","--name-only",f"{BASE}...HEAD"], cwd=ROOT, text=True)
        changed = {x.strip() for x in out.splitlines() if x.strip()}
    except Exception as exc:
        fail(f"scope guard cannot inspect git diff: {exc}")
    extra = changed - ALLOWED
    if extra: fail("out-of-scope files changed: " + ", ".join(sorted(extra)))
    forbidden_prefixes = ("src/","reference/","integration/evidence/","integration/animo-b3/","integration/animo-reg/")
    if any(p.startswith(forbidden_prefixes) for p in changed): fail("forbidden scientific/evidence/central authority path changed")

    review_path = ROOT / OPTIONAL_FINAL[0]
    if review_path.exists():
        review = load(OPTIONAL_FINAL[0])
        if review.get("same_agent") is not True or review.get("independence_claimed") is not False or review.get("assurance") != "PROCESS_SELF_REVIEWED_NOT_INDEPENDENT": fail("review assurance mislabeled")
        if review.get("outcome") not in {"SELF_REVIEW_PASS","SELF_REVIEW_PASS_WITH_NON_SUBSTANTIVE_CLARIFICATIONS"}: fail("review not passing")
        challenges = review.get("challenges", {})
        required_challenges = ["swap_assumption_transfer","scope_gaming","branch_count_as_progress","tcd_count_as_program_completion","research_as_production","evidence_as_authority","child_to_parent_promotion","same_agent_as_independent","runtime_interruption_as_invalidity","parallel_moving_contract_coownership","module_registry_second_truth","retroactive_science_invalidation"]
        for c in required_challenges:
            if challenges.get(c) != "PASS": fail(f"adversarial challenge failed or missing: {c}")
        if status.get("review",{}).get("completed") is not True: fail("review artifact exists but status not closed")
        if status.get("decision") != "QUALIFIED_UNIFIED_PROGRAM_GOVERNANCE_DENOMINATOR_NOT_YET_QUALIFIED_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE": fail("final disposition mismatch")
        print("GOV06 PASS: final governance package including adversarial review")
    else:
        if status.get("review",{}).get("completed") is not False: fail("review status inconsistent before review")
        print("GOV06 PASS: immutable authoring package valid; adversarial review still required")

if __name__ == "__main__":
    main()
