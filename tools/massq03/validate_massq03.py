#!/usr/bin/env python3
import csv
import io
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "624bbad35add93de29ac89649155d9fa086a73af"
B3A08 = "7a7309e913e8216a20ac134539470e3e5eb4302f"
DECISION = "QUALIFIED_TCD025_SELECTED_PROFILE_MACROPORE_BOUNDARY_ADMISSIBILITY_PARTIAL_SATURATED_RESERVOIR_CUTS_NOT_SOURCE_CLOSED_NO_ADMISSION"
EXPECTED = {
    "ANIMO-GOV05": "f65a47724e4a4fca7f2d8b8d6de9eeee51867904",
    "ANIMO-GOV04": "1bbe4c211197590f346803106e45dca5faae79fc",
    "ANIMO-GOV03": "cbd262bdabe92923113b7326f2f42822ce9a971c",
    "ANIMO-MASSQ02": "56a11b524d03c33ee4ab9b1cd13b2cd523d543fc",
    "ANIMO-MP01": "7b5979dd6301b9d55d23e8c22948a0dba24b229b",
    "ANIMO-MP02": "6b0f2e7470f13baeb6612b0bddb662a497dea528",
    "ANIMO-B3D23": "6c9ab83952b53566b878b533c08e3cb10074f399",
    "ANIMO-B3A08": B3A08,
}
EXPECTED_SOURCE = {
    "Outbal_calc.for": "4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981",
    "MAPOHYDRO.FOR": "86659aaac3e48439252c37490d44f214945dfe8f1d49d14876a40abc03e3722a",
    "MAPOTRANSPORT.FOR": "735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da",
    "Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058",
    "Animo.inc": "0f8b58e522ac2cdae95e8ae727dbf3ecea942e39c4d117b6bcae955d80fb69a2",
}


def fail(msg):
    print("MASSQ03 FAIL_CLOSED:", msg)
    raise SystemExit(1)


def load(path):
    p = ROOT / path
    if not p.exists():
        fail(f"missing {path}")
    return json.loads(p.read_text(encoding="utf-8"))


contract = load("integration/animo-mass/MASSQ03_TCD025_CONTROL_VOLUME_CONTRACT.json")
evidence = load("integration/animo-mass/MASSQ03_SOURCE_SEAM_EVIDENCE.json")
status = load("integration/animo-mass/ANIMO-MASSQ03_STATUS.json")
freeze = load("integration/animo-mass/ANIMO-MASSQ03_AUTHORING_FREEZE.json")

if contract.get("work_unit") != "ANIMO-MASSQ03" or contract.get("target") != "TCD-025":
    fail("wrong work-unit or target identity")
if contract.get("base_authority") != f"ANIMO-RG05J@{BASE}":
    fail("wrong aggregate base authority")
if contract.get("consumed_readiness_authority") != f"ANIMO-B3A08@{B3A08}":
    fail("wrong B3A08 readiness authority")
if contract.get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS":
    fail("risk tier must remain Tier C")
qp = contract.get("qualified_predicate", {})
if qp.get("necessary_for_exact_selected_profile_species_observer") is not True:
    fail("boundary predicate must be a necessary condition")
if qp.get("sufficient_for_complete_TCD025_observer") is not False:
    fail("boundary predicate must not be promoted to sufficient TCD025 closure")
if qp.get("partial_saturated_reservoir_cut") != "NOT_SOURCE_CLOSED":
    fail("partial saturated reservoir cut must fail closed")
forbidden = contract.get("forbidden_inference", {})
if forbidden.get("residual_derived_missing_boundary_flux") is not False:
    fail("residual-derived self-closure forbidden")
if forbidden.get("geometric_mass_allocation_implies_transport_owner") is not False:
    fail("geometric mass allocation cannot imply transport ownership")
if contract.get("b3_admitted") is not False or contract.get("production_authorized") is not False:
    fail("admission or production boundary violated")
if contract.get("decision") != DECISION:
    fail("decision string mismatch")

if evidence.get("frozen_source_archive_sha256") != "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566":
    fail("source archive identity mismatch")
if evidence.get("frozen_testbank_archive_sha256") != "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84":
    fail("testbank identity mismatch")
if evidence.get("member_hashes") != EXPECTED_SOURCE:
    fail("source member hashes mismatch")
if evidence.get("raw_source_redistributed") is not False:
    fail("raw source redistribution forbidden")

manifest = (ROOT / "reference/source/source_manifest.csv").read_text(encoding="utf-8")
rows = list(csv.DictReader(io.StringIO(manifest)))
by_name = {pathlib.PurePosixPath(r["path"]).name: r["sha256"] for r in rows}
for name, sha in EXPECTED_SOURCE.items():
    if by_name.get(name) != sha:
        fail(f"frozen source manifest mismatch for {name}")

if status.get("base_authority") != f"ANIMO-RG05J@{BASE}":
    fail("status base mismatch")
if status.get("consumed_readiness_authority") != f"ANIMO-B3A08@{B3A08}":
    fail("status B3A08 pin mismatch")
if status.get("upstream_pins") != EXPECTED:
    fail("status authority pin mismatch")
if status.get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS":
    fail("status risk tier mismatch")
if status.get("b3_admitted") is not False or status.get("production_authorized") is not False:
    fail("status illegally opens admission/production")
if status.get("hard_boundaries", {}).get("persistent_state_added") is not False:
    fail("new persistent state is out of scope")
if status.get("hard_boundaries", {}).get("canonical_tcd_register_changed") is not False:
    fail("canonical TCD register change forbidden")
if status.get("hard_boundaries", {}).get("historical_b2_claim") is not False:
    fail("historical B2 claim forbidden")

matrix_path = ROOT / "integration/animo-mass/MASSQ03_BOUNDARY_ADMISSIBILITY_MATRIX.csv"
rows = list(csv.DictReader(matrix_path.read_text(encoding="utf-8").splitlines()))
by_case = {r["case_id"]: r for r in rows}
for cid in ("CV05", "CV06", "CV07"):
    if by_case.get(cid, {}).get("qualified_result") != "NOT_SOURCE_CLOSED":
        fail(f"{cid} must fail closed")
for cid in ("CV01", "CV02", "CV03", "CV04", "CV08"):
    if by_case.get(cid, {}).get("qualified_result") != "PASSES_THIS_BOUNDARY_GATE_ONLY":
        fail(f"{cid} must remain necessary-gate-only")
if by_case.get("CV09", {}).get("qualified_result") != "NOT_APPLICABLE":
    fail("inactive-domain control must be NOT_APPLICABLE")

for label, sha in EXPECTED.items():
    rc = subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"], cwd=ROOT).returncode
    if rc != 0:
        fail(f"missing pinned commit {label}@{sha}")

allowed = {
    ".github/workflows/animo-massq03-tcd025-control-volume.yml",
    "docs/massq03/TCD025_SELECTED_PROFILE_CONTROL_VOLUME_QUALIFICATION.md",
    "integration/animo-mass/MASSQ03_TCD025_CONTROL_VOLUME_CONTRACT.json",
    "integration/animo-mass/MASSQ03_SOURCE_SEAM_EVIDENCE.json",
    "integration/animo-mass/MASSQ03_BOUNDARY_ADMISSIBILITY_MATRIX.csv",
    "integration/animo-mass/ANIMO-MASSQ03_STATUS.json",
    "integration/animo-mass/ANIMO-MASSQ03_AUTHORING_FREEZE.json",
    "integration/animo-mass/ANIMO-MASSQ03_INTERNAL_ADVERSARIAL_REVIEW.json",
    "tools/massq03/validate_massq03.py",
}
changed = subprocess.check_output(["git", "diff", "--name-only", BASE + "..HEAD"], cwd=ROOT, text=True).splitlines()
extra = sorted(set(changed) - allowed)
if extra:
    fail("scope escape: " + ", ".join(extra))
for p in changed:
    if p.startswith("src/") or p.startswith("reference/"):
        fail("production or frozen-reference path changed: " + p)
if freeze.get("authoring_complete") is not True:
    fail("authoring freeze not declared")

review_path = ROOT / "integration/animo-mass/ANIMO-MASSQ03_INTERNAL_ADVERSARIAL_REVIEW.json"
if review_path.exists():
    review = json.loads(review_path.read_text(encoding="utf-8"))
    reviewed_head = review.get("reviewed_head")
    if not reviewed_head:
        fail("review missing exact reviewed head")
    if review.get("model") != "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW":
        fail("wrong GOV05 review model")
    if review.get("genuinely_independent") is not False or review.get("independence_claimed") is not False:
        fail("same-agent review mislabelled independent")
    if review.get("outcome") != "SELF_REVIEW_PASS_QUALIFIED_BOUNDARY_PREDICATE_NO_ADMISSION":
        fail("review outcome mismatch")
    post = subprocess.check_output(["git", "diff", "--name-only", reviewed_head + "..HEAD"], cwd=ROOT, text=True).splitlines()
    post_allowed = {
        "integration/animo-mass/ANIMO-MASSQ03_INTERNAL_ADVERSARIAL_REVIEW.json",
        "integration/animo-mass/ANIMO-MASSQ03_STATUS.json",
    }
    bad = sorted(set(post) - post_allowed)
    if bad:
        fail("substantive files changed after reviewed freeze: " + ", ".join(bad))
    if status.get("phase") != "CLOSED_QUALIFIED_CONTROL_VOLUME_SEMANTICS":
        fail("review exists but status is not final closeout")
    if status.get("qualified") is not True:
        fail("reviewed qualification not marked qualified")
    if status.get("decision") != DECISION:
        fail("final decision mismatch")
    if status.get("review_governance", {}).get("reviewed_head") != reviewed_head:
        fail("status/review head mismatch")
    print("MASSQ03 PASS final qualified selected-profile boundary semantics", reviewed_head)
else:
    if status.get("phase") != "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW":
        fail("missing review outside authoring-frozen phase")
    if status.get("qualified") is not False:
        fail("pre-review status cannot be qualified")
    print("MASSQ03 PASS authoring frozen; GOV05 adversarial review still required")
