#!/usr/bin/env python3
import csv, io, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "94afe7d649a8c60758a41996f0059de0acddd2fc"
EXPECTED = {
    "ANIMO-GOV05":"f65a47724e4a4fca7f2d8b8d6de9eeee51867904",
    "ANIMO-GOV04":"1bbe4c211197590f346803106e45dca5faae79fc",
    "ANIMO-GOV03":"cbd262bdabe92923113b7326f2f42822ce9a971c",
    "ANIMO-B3Q01":"846e0f4d02a38b9e02cc1419b1ca87e63aaedb54",
    "ANIMO-MP01":"7b5979dd6301b9d55d23e8c22948a0dba24b229b",
    "ANIMO-MP02":"6b0f2e7470f13baeb6612b0bddb662a497dea528",
    "ANIMO-STATEQ01":"4adae99576eb56978da71f7c8a250e4445fd3bc4",
    "ANIMO-MASSQ02":"56a11b524d03c33ee4ab9b1cd13b2cd523d543fc",
    "ANIMO-B3D23":"6c9ab83952b53566b878b533c08e3cb10074f399",
}
EXPECTED_SOURCE = {"Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7", "Animo.inc": "0f8b58e522ac2cdae95e8ae727dbf3ecea942e39c4d117b6bcae955d80fb69a2", "Init.for": "287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058", "MAPOHYDRO.FOR": "86659aaac3e48439252c37490d44f214945dfe8f1d49d14876a40abc03e3722a", "MAPOTRANSPORT.FOR": "735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da", "Outbal_Init.for": "95c0d7aad6cb863fcbb5dd41563674af3ab0819387212d27d5f6f04b4a788cc8", "Outbal_calc.for": "4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981", "Outbal_write.for": "cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea", "mapoinput.for": "081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065"}

def fail(msg):
    print("B3A08 FAIL_CLOSED:", msg)
    raise SystemExit(1)

def load(path):
    p = ROOT / path
    if not p.exists():
        fail(f"missing {path}")
    return json.loads(p.read_text(encoding="utf-8"))

readiness = load("integration/animo-b3/TCD025_MACROPORE_MAIN_LEDGER_READINESS.json")
waiver = load("integration/animo-b3/TCD025_TIER_A_WAIVER_AUDIT.json")
status = load("integration/animo-b3/ANIMO-B3A08_STATUS.json")
freeze = load("integration/animo-b3/ANIMO-B3A08_AUTHORING_FREEZE.json")

if readiness.get("work_unit") != "ANIMO-B3A08" or readiness.get("target") != "TCD-025":
    fail("wrong readiness identity")
if readiness.get("base_authority",{}).get("head") != BASE:
    fail("wrong RG05I base")
if readiness.get("upstream_pins") != EXPECTED:
    fail("authority pin mismatch")
if readiness.get("frozen_identity",{}).get("selected_member_sha256") != EXPECTED_SOURCE:
    fail("source member pin mismatch")
if readiness.get("risk_assessment",{}).get("candidate_review_risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS":
    fail("risk tier is not fail-closed Tier C")
if readiness.get("risk_assessment",{}).get("tier_a_waiver_available") is not False:
    fail("Tier-A waiver must be unavailable")
if readiness.get("admission_readiness",{}).get("ready_for_tier_a_admission") is not False:
    fail("Tier-A admission incorrectly marked ready")
if readiness.get("admission_readiness",{}).get("ready_for_tier_c_admission") is not False:
    fail("Tier-C admission incorrectly marked ready")
if readiness.get("hard_boundaries",{}).get("b3_admission") is not False:
    fail("B3 admission boundary violated")
if readiness.get("hard_boundaries",{}).get("production_patch") is not False:
    fail("production boundary violated")
if waiver.get("result") != "TIER_A_WAIVER_UNAVAILABLE":
    fail("waiver result mismatch")
if waiver.get("decision") != "FAIL_CLOSED_ESCALATE_TO_TIER_C_QUALIFICATION":
    fail("waiver decision mismatch")
for gate in ("physical_and_accounting_ownership_unambiguous", "no_unresolved_scientific_or_source_meaning_ambiguity"):
    if waiver.get("gates",{}).get(gate,{}).get("result") != "FAIL":
        fail(f"required fail-closed gate {gate} did not fail")

manifest = (ROOT / "reference/source/source_manifest.csv").read_text(encoding="utf-8")
rows = list(csv.DictReader(io.StringIO(manifest)))
by_name = {pathlib.PurePosixPath(r["path"]).name: r["sha256"] for r in rows}
for name, sha in EXPECTED_SOURCE.items():
    if by_name.get(name) != sha:
        fail(f"frozen source manifest mismatch for {name}")

for label, sha in EXPECTED.items():
    rc = subprocess.run(["git","cat-file","-e",sha+"^{commit}"], cwd=ROOT).returncode
    if rc != 0:
        fail(f"missing pinned commit {label}@{sha}")

allowed = {
 ".github/workflows/animo-b3a08-tcd025.yml",
 "docs/b3a08/WORK_UNIT_CONTRACT.md",
 "docs/b3a08/TCD025_MACROPORE_MAIN_LEDGER_READINESS.md",
 "integration/animo-b3/TCD025_MACROPORE_MAIN_LEDGER_READINESS.json",
 "integration/animo-b3/TCD025_TIER_A_WAIVER_AUDIT.json",
 "integration/animo-b3/ANIMO-B3A08_STATUS.json",
 "integration/animo-b3/ANIMO-B3A08_AUTHORING_FREEZE.json",
 "integration/animo-b3/ANIMO-B3A08_INTERNAL_ADVERSARIAL_REVIEW.json",
 "tools/validate_b3a08_tcd025.py",
}
changed = subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"], cwd=ROOT, text=True).splitlines()
extra = sorted(set(changed) - allowed)
if extra:
    fail("scope escape: " + ", ".join(extra))

if freeze.get("authoring_complete") is not True:
    fail("authoring freeze not declared")
if status.get("b3_admitted") is not False or status.get("production_authorized") is not False:
    fail("forbidden admission/production state")

review_path = ROOT / "integration/animo-b3/ANIMO-B3A08_INTERNAL_ADVERSARIAL_REVIEW.json"
if review_path.exists():
    review = json.loads(review_path.read_text(encoding="utf-8"))
    reviewed_head = review.get("reviewed_head")
    if not reviewed_head:
        fail("review has no exact reviewed head")
    if review.get("model") != "MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW":
        fail("wrong GOV05 review model")
    if review.get("genuinely_independent") is not False:
        fail("same-agent review mislabelled independent")
    if review.get("outcome") != "SELF_REVIEW_PASS_FAIL_CLOSED_TIER_C_ESCALATION":
        fail("review outcome mismatch")
    post = subprocess.check_output(["git","diff","--name-only",reviewed_head+"..HEAD"], cwd=ROOT, text=True).splitlines()
    post_allowed = {
      "integration/animo-b3/ANIMO-B3A08_INTERNAL_ADVERSARIAL_REVIEW.json",
      "integration/animo-b3/ANIMO-B3A08_STATUS.json",
    }
    bad = sorted(set(post)-post_allowed)
    if bad:
        fail("substantive files changed after reviewed freeze: " + ", ".join(bad))
    if status.get("phase") != "CLOSED_QUALIFIED_READINESS_BLOCKED":
        fail("review exists but status is not final closeout")
    if status.get("qualified") is not True:
        fail("final classification not qualified")
    if status.get("decision") != "QUALIFIED_TCD025_TIER_A_WAIVER_UNAVAILABLE_ESCALATE_TIER_C_SELECTED_PROFILE_CONTROL_VOLUME_QUALIFICATION":
        fail("final decision mismatch")
    if status.get("review_governance",{}).get("reviewed_head") != reviewed_head:
        fail("status/review head mismatch")
    print("B3A08 PASS final fail-closed readiness classification", reviewed_head)
else:
    if status.get("phase") != "AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW":
        fail("missing review outside authoring-frozen phase")
    if status.get("qualified") is not False:
        fail("pre-review status cannot be qualified")
    print("B3A08 PASS authoring frozen; GOV05 adversarial review still required")
