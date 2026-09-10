#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "integration/animo-b3/TCD018_INDEPENDENT_R2_REVIEW_RESULT.json"
REPORT = ROOT / "docs/b3/TCD018_INDEPENDENT_SECOND_LINE_R2_REVIEW.md"
PERIOD = ROOT / "integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv"
RUNS = ROOT / "integration/animo-b3/TCD018_EIGHT_CASE_RUN_LEDGER.json"
LEDGER_DIR = ROOT / "integration/animo-b3/tcd018_output_digest_ledger"
BUILDER = ROOT / "tools/build_tcd018_reporting_candidate.py"
COMPARATOR = ROOT / "tools/compare_legacy_output_trees.py"

PASS_TOKEN = "PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_READINESS_REVIEW"
BASE = "4c92b27ed5bbcaadb0e703e622e8c3f690458fa8"
ACTIVE = "LWKM_gras_1040.2021.2045"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

HEADS = {
    "ANIMO-B3A03": "8eaaca34e4f0d906c2d8245f0df232586efe8ff3",
    "ANIMO-B3A03R_same_context_evidence_only": "0876e6e1b6ce33ee5e7b812ab4107f54760d6b27",
    "ANIMO-B3D05": "2f06cc86225637f8dadfdd969fe48dcf851b9ee2",
    "previous_independent_review": "57cfdfb3a7fb982f6692b0b32f8c8aa044c57fd7",
    "ANIMO-B3A03E": BASE,
    "ANIMO-GOV03": "cbd262bdabe92923113b7326f2f42822ce9a971c",
    "ANIMO-RG05B": "c353c3179f213c1bf24c48b3c06f8065c760d3e2",
    "ANIMO-PREP06": "9b1f1ea51c24fb82823290193651830dc61ea3c8",
    "ANIMO-SYNQ01": "842f72300fd03ede0b9024537a7ee6126722a121",
    "ANIMO-MASSQ01": "6ccddd631a8dcc21f06b1384baf2561e81179e75",
}

EXPECTED_CASE_COUNTS = {
    "CranGrass": 31,
    "CranMais": 23,
    "GrassPeat": 60,
    ACTIVE: 53,
    "Puitmijn_Cranendonck_60": 77,
    "RuurloGrass": 72,
    "STONE_akk_0006.2001.2015": 44,
    "Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA": 16,
}
EXPECTED_WHITELIST = {
    "ani_waGP.Bal",
    "ani_waRP.Bal",
    "ani_waTP.Bal",
    "bawaGP.Out",
    "bawaRP.Out",
    "bawaTP.Out",
}
EXPECTED_LEDGER_FILES = {"CranGrass.csv", "part2.csv", "part3.csv", "part4.csv"}

PINNED_BLOBS = {
    (BASE, "integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv"): "a8513296e856c716ee1c53d839920d089f92492f",
    (BASE, "integration/animo-b3/TCD018_EIGHT_CASE_RUN_LEDGER.json"): "49e0fb498a1e6324290c533aad20485be07d27d5",
    (BASE, "integration/animo-b3/tcd018_output_digest_ledger/CranGrass.csv"): "52b99da183c20b517a26bd9059da8bc4bc10bd5a",
    (BASE, "integration/animo-b3/tcd018_output_digest_ledger/part2.csv"): "bd238a6c8c3d20c607535d959be4849d860bcfa3",
    (BASE, "integration/animo-b3/tcd018_output_digest_ledger/part3.csv"): "749c9a2ad62325702a1578da1db602cf2e554a2a",
    (BASE, "integration/animo-b3/tcd018_output_digest_ledger/part4.csv"): "59450584b6339c4c001f6d39f98f6f2a7fa3604d",
    (BASE, "integration/animo-b3/TCD018_EVIDENCE_REMEDIATION_MANIFEST.json"): "e2500475578f6bbd6034c268774ac5f606a91bbd",
    (BASE, "integration/animo-b3/ANIMO-B3A03E_STATUS.json"): "e931dacc6d22c4dc2eb3478f739b92a041c8b81a",
    (BASE, "tools/build_tcd018_reporting_candidate.py"): "e52cb88299236aa06ba4b7fd7d8f20705cf7ec14",
    (HEADS["ANIMO-B3A03"], "integration/animo-b3/TCD018_SOURCE_SEAM_PIN.json"): "cbc68024db6b649370ffe55a55b2a2de346ac2d2",
    (HEADS["ANIMO-PREP06"], "docs/prep06/CONSERVED_STATE_INVENTORY.csv"): "838f224fc67a72371437c6d5b6e75cd03f5c8d51",
    (HEADS["ANIMO-PREP06"], "docs/prep06/PROCESS_CONSERVATION_IDENTITIES.md"): "f0e9bfe0432cc7651f3421eccaef472111f36721",
    (HEADS["ANIMO-SYNQ01"], "integration/animo-synthetic/SYNTHETIC_ORACLE_REGISTER.json"): "4c215d19844614de8868380fb03f93268ea4c5d8",
    (HEADS["ANIMO-MASSQ01"], "integration/animo-mass/MASSLEDGER_RESIDUAL_REGISTER.csv"): "356cea3db7818905a8fb173af7df6fb0d42fa494",
    (HEADS["ANIMO-MASSQ01"], "tools/compare_legacy_output_trees.py"): "0b5928184ffef38caf1f8040f47fa4ea5366c62f",
    (HEADS["previous_independent_review"], "integration/animo-b3/TCD018_INDEPENDENT_REVIEW_RESULT.json"): "a98b2d094890f9f88587b0b6c196d850ed5fe88f",
}


def fail(message: str) -> None:
    raise SystemExit("FAIL_B3A03R2: " + message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def read_at(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True)


def valid_sha(value: str) -> bool:
    return bool(HEX64.fullmatch(value or ""))


def validate_result_contract() -> dict:
    require(RESULT.is_file(), "missing R2 result")
    require(REPORT.is_file(), "missing R2 report")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    report = REPORT.read_text(encoding="utf-8")

    require(data["overall_result"] == PASS_TOKEN, "exact PASS result token")
    require(PASS_TOKEN in report, "report/result token mismatch")
    require(data["classification"] == "A_ACCOUNTING_REPORTING_ONLY", "Class-A classification")
    require(data["review_start_head"] == BASE, "clean review start head")
    require(data["reviewed_heads"] == HEADS, "reviewed heads must be exact")
    require(data["separate_chatgpt_context_from_B3A03_B3A03E_B3D05_authoring"] is True, "separate ChatGPT context")
    require(data["organizational_or_human_independence_claimed"] is False, "no organizational/human independence claim")
    require(data["review_evidence_only"] is True, "PASS must be review evidence only")
    require(data["B3_admission_performed"] is False, "R2 must not admit TCD-018")
    require(data["previous_review_history"]["result"] == "FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW", "preserve R1 FAIL")
    require(data["previous_review_history"]["historically_valid_for_previous_packet"] is True, "R1 history retained")
    require(data["previous_review_history"]["overwritten_by_R2"] is False, "R1 not overwritten")
    require(len(data["gates"]) == 19, "all 19 R2 gates recorded")
    require(all(v == "PASS" for v in data["gates"].values()), "every mandatory R2 gate PASS")
    require(set(data["independent_eight_case_audit"]["exact_whitelist"]) == EXPECTED_WHITELIST, "exact six-file whitelist")
    require(len(data["independent_eight_case_audit"]["exact_whitelist"]) == 6, "whitelist cardinality")
    require(data["noninterference_basis"]["not_inferred_from_output_equality_alone"] is True, "state/flux claim must not be inferred from output equality alone")
    require(data["residual_boundaries"]["LWKM_approximately_0_0601_mm"] == "CAUSAL_EVIDENCE_NOT_TOLERANCE", "0.0601 mm boundary")
    require(data["residual_boundaries"]["MASSQ01_CranGrass_TITO724_mm"] == -0.0030198960466805147, "CranGrass residual exact")
    require(data["residual_boundaries"]["MASSQ01_CranGrass_TITO724_class"] == "UNEXPLAINED_RESIDUAL", "CranGrass residual class")
    require(data["residual_boundaries"]["global_water_closure_claimed"] is False, "no global water closure")
    require(data["historical_route"]["qualified_B2_exists"] is False, "no qualified B2")
    require(data["historical_route"]["historical_revision53_behaviour"] == "UNKNOWN", "historical behaviour UNKNOWN")
    require(data["historical_route"]["TCD018_admitted"] is False, "TCD-018 not admitted")
    require(all(v is False for v in data["hard_boundaries"].values()), "all hard boundaries false")
    return data


def validate_artifact_pins(data: dict) -> None:
    reported = data["artifact_blob_shas"]
    expected_reported = {path: blob for (_, path), blob in PINNED_BLOBS.items()}
    require(reported == expected_reported, "machine-readable artifact pin set differs")
    for (commit, path), expected in PINNED_BLOBS.items():
        actual = git("rev-parse", f"{commit}:{path}")
        require(actual == expected, f"blob pin mismatch {commit}:{path}")


def validate_frozen_and_scientific_boundaries(data: dict) -> None:
    source_pin = (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text().split()[0]
    testbank_pin = (ROOT / "reference/testcases/ANIMO_testbank.zip.sha256").read_text().split()[0]
    require(source_pin == "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566", "frozen source pin")
    require(testbank_pin == "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84", "frozen testbank pin")
    require(data["frozen_B0"]["source_sha256"] == source_pin, "result source pin")
    require(data["frozen_B0"]["testbank_sha256"] == testbank_pin, "result testbank pin")

    seam = json.loads(read_at(HEADS["ANIMO-B3A03"], "integration/animo-b3/TCD018_SOURCE_SEAM_PIN.json"))
    require(seam["source_files"]["Hydro_detailed.for"]["sha256"] == "f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d", "Hydro_detailed source identity")
    require("(Sict-Sic)" in seam["source_files"]["Hydro_detailed.for"]["exact_storage_observation"], "Hydro_detailed interception storage term")
    outbal = seam["source_files"]["Outbal_calc.for"]
    require(outbal["sic_sict_token_count"] == 0 and outbal["interception_storage_term_present"] is False, "Outbal_calc omission")
    require("Bawa(Eint)" in outbal["interception_flux_present"], "Outbal_calc observes interception evaporation")
    require(seam["source_files"]["Init.for"]["exact_interception_promotion"] == "If(Iopthyvs .Eq. 1 .and. Hlpimp==11) Sic = Sict", "state promotion exact")

    inventory = read_at(HEADS["ANIMO-PREP06"], "docs/prep06/CONSERVED_STATE_INVENTORY.csv")
    require("Sic,Sict" in inventory and "canopy interception" in inventory.lower(), "PREP06 Sic/Sict ownership")
    require("Init: Sic=Sict" in inventory, "PREP06 Sic/Sict lifecycle")
    conservation = read_at(HEADS["ANIMO-PREP06"], "docs/prep06/PROCESS_CONSERVATION_IDENTITIES.md")
    require("matrix water + snow + ponding + interception" in conservation, "PREP06 water conservation control volume")

    synq = json.loads(read_at(HEADS["ANIMO-SYNQ01"], "integration/animo-synthetic/SYNTHETIC_ORACLE_REGISTER.json"))
    o003 = next(x for x in synq["oracles"] if x["oracle_id"] == "SYNQ-O003")
    require(o003["target_tcd"] == "TCD-018" and o003["evidence_class"] == "CONSERVATION_ORACLE", "SYNQ-O003 type")
    require(o003["mathematical_formulation"] == "Interception CV: S0 + precipitation - evaporation - throughfall - S1 = 0.", "SYNQ-O003 identity")
    require(synq["evidence_boundary"]["B2_reference_created"] is False, "SYNQ01 never B2")
    require(synq["evidence_boundary"]["historical_behaviour_claimed"] is False, "SYNQ01 no historical claim")

    residual_rows = list(csv.DictReader(read_at(HEADS["ANIMO-MASSQ01"], "integration/animo-mass/MASSLEDGER_RESIDUAL_REGISTER.csv").splitlines()))
    r010 = next(r for r in residual_rows if r["record_id"] == "MASSQ01-R010")
    require(r010["case"] == "CranGrass" and r010["interval"] == "TITO=724", "MASSQ01 discriminator identity")
    require(float(r010["observed_value"]) == -0.0030198960466805147, "MASSQ01 discriminator value")
    require(r010["residual_class"] == "UNEXPLAINED_RESIDUAL", "MASSQ01 discriminator class")
    r008 = next(r for r in residual_rows if r["record_id"] == "MASSQ01-R008")
    require(r008["canonical_tcd"] == "TCD-018" and "not a tolerance" in r008["interpretation"], "0.0601 mm is causal evidence only")

    gov = json.loads(read_at(HEADS["ANIMO-GOV03"], "integration/animo-governance/ANIMO-GOV03_STATUS.json"))
    require(gov["qualified_G6U_state"] == "ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS", "GOV03 G6U route")
    require(gov["hard_boundaries"]["historical_B2_recovered"] is False, "GOV03 no B2")
    require(gov["route_effect"]["historical_behaviour_without_B2"] == "UNKNOWN", "GOV03 historical unknown")
    b3d05 = json.loads(read_at(HEADS["ANIMO-B3D05"], "integration/animo-b3/ANIMO-B3D05_STATUS.json"))
    require(b3d05["admission_route"] == "INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY", "B3D05 route")
    require(b3d05["route_reconciliation"]["historical_behaviour"] == "UNKNOWN", "B3D05 historical unknown")
    require(b3d05["admission"]["admitted"] is False, "B3D05 no admission")


def validate_period_rows(data: dict) -> None:
    rows = list(csv.DictReader(PERIOD.open(newline="", encoding="utf-8")))
    require(len(rows) == 25, "period row count != 25")
    require([int(r["year"]) for r in rows] == list(range(1991, 2016)), "years not exactly 1991..2015")
    previous_end = 0
    total_records = 0
    for row in rows:
        start = int(row["period_start_tito_exclusive"])
        end = int(row["period_end_tito"])
        days = int(row["period_days_reported"])
        probes = int(row["hydro_probe_records"])
        require(start == previous_end, f"non-contiguous period before {row['year']}")
        require(end - start == days, f"period-day identity {row['year']}")
        require(probes == 36, f"probe count {row['year']}")
        total_records += probes
        previous_end = end

        legacy = float(row["legacy_bawadv_formatted_mm"])
        hydro = float(row["hydro_badev_sum_raw_mm"])
        interception = float(row["interception_storage_change_sum_raw_mm"])
        reconstructed = float(row["reconstructed_legacy_raw_mm"])
        recon_minus_formatted = float(row["reconstruction_minus_legacy_formatted_mm"])
        candidate = float(row["fresh_candidate_bawadv_formatted_mm"])
        candidate_minus_hydro = float(row["fresh_candidate_minus_hydro_badev_raw_mm"])

        # Exact binary64 serialization consistency only. No scientific epsilon is used.
        require(reconstructed == hydro + interception, f"raw reconstruction arithmetic {row['year']}")
        require(recon_minus_formatted == reconstructed - legacy, f"reconstruction-minus-formatted arithmetic {row['year']}")
        require(candidate_minus_hydro == candidate - hydro, f"candidate-minus-hydro arithmetic {row['year']}")

    require(total_records == 900, "fresh probe total != 900")
    require(previous_end == 9131, "final TITO != 9131")
    r2008 = next(r for r in rows if r["year"] == "2008")
    require((int(r2008["period_start_tito_exclusive"]), int(r2008["period_end_tito"])) == (6209, 6575), "2008 period")
    require(float(r2008["legacy_bawadv_formatted_mm"]) == -0.0601, "2008 legacy discriminator")
    require(float(r2008["hydro_badev_sum_raw_mm"]) == -5.2640587582358024e-05, "2008 Hydro Badev")
    require(float(r2008["interception_storage_change_sum_raw_mm"]) == -0.059999999999999984, "2008 interception change")
    require(float(r2008["fresh_candidate_bawadv_formatted_mm"]) == -5.26e-05, "2008 candidate Bawa")
    audit = data["independent_period_audit"]
    require(audit["rows"] == 25 and audit["total_hydrology_probe_records"] == 900 and audit["final_tito"] == 9131, "result period audit mismatch")
    require(audit["scientific_acceptance_tolerance_used"] is False, "period audit must use no scientific tolerance")


def validate_run_and_output_ledgers(data: dict) -> None:
    runs = json.loads(RUNS.read_text(encoding="utf-8"))
    require(len(runs) == 16, "run record count != 16")
    grouped = defaultdict(dict)
    for run in runs:
        case = run["case"]
        variant = run["variant"]
        require(case in EXPECTED_CASE_COUNTS, f"unexpected run case {case}")
        require(variant in {"baseline", "candidate"}, f"unexpected run variant {variant}")
        require(variant not in grouped[case], f"duplicate run {case}/{variant}")
        require(run["success_message_present"] is True, f"unsuccessful run {case}/{variant}")
        require(run["success_message_paths"], f"missing completion path {case}/{variant}")
        require(valid_sha(run["runner_stdout_sha256"]), f"invalid runner stdout digest {case}/{variant}")
        grouped[case][variant] = run
    require(set(grouped) == set(EXPECTED_CASE_COUNTS), "run case set")
    for case, pair in grouped.items():
        require(set(pair) == {"baseline", "candidate"}, f"missing baseline/candidate {case}")
        require(pair["baseline"]["runner_stdout_sha256"] == pair["candidate"]["runner_stdout_sha256"], f"runner stdout differs {case}")

    files = {p.name for p in LEDGER_DIR.iterdir() if p.is_file()}
    require(files == EXPECTED_LEDGER_FILES, "digest ledger file set must be exact")
    rows = []
    for name in sorted(EXPECTED_LEDGER_FILES):
        rows.extend(csv.DictReader((LEDGER_DIR / name).open(newline="", encoding="utf-8")))
    require(len(rows) == 376, "output ledger rows != 376")
    pairs = [(r["case"], r["path"]) for r in rows]
    require(len(set(pairs)) == 376, "duplicate case/path output records")
    require(set(r["case"] for r in rows) == set(EXPECTED_CASE_COUNTS), "output ledger case set")

    case_counts = Counter(r["case"] for r in rows)
    require(dict(case_counts) == EXPECTED_CASE_COUNTS, f"per-case counts differ: {dict(case_counts)}")
    classes = Counter(r["classification"] for r in rows)
    expected_classes = Counter({
        "EQUAL_RAW": 270,
        "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY": 100,
        "DIFFERENT_WHITELISTED": 6,
    })
    require(classes == expected_classes, f"classification totals differ: {dict(classes)}")

    for r in rows:
        cls = r["classification"]
        if cls == "EQUAL_RAW":
            require(r["digest_basis"] == "RAW_BYTES", f"raw digest basis {r['case']}/{r['path']}")
            require(valid_sha(r["common_sha256"]), f"raw common digest {r['case']}/{r['path']}")
            require(not r["reference_sha256"] and not r["candidate_sha256"], f"raw row must use common digest {r['case']}/{r['path']}")
        elif cls == "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY":
            require(r["digest_basis"] == "DECLARED_VOLATILE_NORMALIZED_BYTES", f"normalized digest basis {r['case']}/{r['path']}")
            require(valid_sha(r["common_sha256"]), f"normalized common digest {r['case']}/{r['path']}")
            require(not r["reference_sha256"] and not r["candidate_sha256"], f"normalized row must use common digest {r['case']}/{r['path']}")
        elif cls == "DIFFERENT_WHITELISTED":
            require(r["digest_basis"] == "DECLARED_VOLATILE_NORMALIZED_BYTES", f"different digest basis {r['case']}/{r['path']}")
            require(not r["common_sha256"], f"different row must not have common digest {r['case']}/{r['path']}")
            require(valid_sha(r["reference_sha256"]) and valid_sha(r["candidate_sha256"]), f"different row digests {r['case']}/{r['path']}")
            require(r["reference_sha256"] != r["candidate_sha256"], f"different row digests equal {r['case']}/{r['path']}")
        else:
            fail(f"unexpected classification {cls}")

    diff_rows = [r for r in rows if r["classification"] == "DIFFERENT_WHITELISTED"]
    require({r["case"] for r in diff_rows} == {ACTIVE}, "all six differences must be LWKM only")
    require({r["path"] for r in diff_rows} == EXPECTED_WHITELIST, "exact six-file difference surface")

    audit = data["independent_eight_case_audit"]
    require(audit["cases"] == 8 and audit["run_records"] == 16 and audit["unique_case_path_rows"] == 376, "result run totals")
    require(audit["classification_totals"] == {"EQUAL_RAW": 270, "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY": 100, "DIFFERENT_WHITELISTED": 6, "unexpected": 0}, "result classification totals")
    require(audit["case_output_counts"] == EXPECTED_CASE_COUNTS, "result per-case counts")
    require(set(audit["exact_whitelist"]) == EXPECTED_WHITELIST and len(audit["exact_whitelist"]) == 6, "result whitelist")
    require(audit["scientific_numeric_tolerance_applied"] is False, "no scientific numeric tolerance")


def validate_comparator_and_builder() -> None:
    comparator = COMPARATOR.read_text(encoding="utf-8")
    required_rules = {
        "file_creation_timestamp",
        "output_run_start_timestamp",
        "message_run_start_timestamp",
        "message_run_end_timestamp",
        "elapsed_cpu_seconds",
    }
    for rule in required_rules:
        require(f'"{rule}"' in comparator, f"missing volatile normalization rule {rule}")
    require("if left_raw == right_raw:" in comparator, "raw-byte equality classification missing")
    require("if left == right:" in comparator, "normalized-byte equality classification missing")
    require("math.isclose" not in comparator and "numpy.isclose" not in comparator, "numeric tolerance used in comparator classification")
    require("Scientific\nnumbers are never tolerance-filtered" in comparator, "comparator numeric boundary statement")

    builder = BUILDER.read_text(encoding="utf-8")
    require("if sha(SRCZIP)!=EXPECTED: raise SystemExit('source archive SHA mismatch')" in builder, "builder frozen-source fail-closed pin")
    require("if s.count(old)!=1: raise SystemExit('Animo call patch seam count !=1')" in builder, "builder Animo seam cardinality")
    require("if s.count(old)!=1: raise SystemExit('Outbal signature seam count !=1')" in builder, "builder Outbal seam cardinality")
    require("Tcd018IcCu(Ly) = Tcd018IcCu(Ly) + (Sict-Sic)*1.d3" in builder, "builder interception accumulator")
    require("Bawa(Ddev,Ly) = Bawa(Ddev,Ly) - Tcd018IcCu(Ly)" in builder, "builder Bawa correction")
    require("Tcd018IcCu(Ly) = 0.0d0" in builder, "builder reporting accumulator reset")
    require("Sic =" not in builder and "Sict =" not in builder, "builder must not assign Sic/Sict")
    require("expected_candidate='c1e281d5ceaa45952dc7ee21041454fbfab5bee34aa8aee09d59604b75826bbe'" in builder, "candidate executable exact pin")
    require("candidate executable SHA mismatch" in builder, "candidate SHA fail-closed enforcement")


def validate_remediation_scope() -> None:
    previous = HEADS["previous_independent_review"]
    changed = set(git("diff", "--name-only", f"{previous}..{BASE}").splitlines())
    allowed = {
        ".github/workflows/animo-b3a03e-tcd018-evidence-remediation.yml",
        "docs/b3/TCD018_EVIDENCE_REMEDIATION.md",
        "integration/animo-b3/ANIMO-B3A03E_STATUS.json",
        "integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv",
        "integration/animo-b3/TCD018_EIGHT_CASE_RUN_LEDGER.json",
        "integration/animo-b3/TCD018_EVIDENCE_REMEDIATION_MANIFEST.json",
        "integration/animo-b3/tcd018_output_digest_ledger/CranGrass.csv",
        "integration/animo-b3/tcd018_output_digest_ledger/part2.csv",
        "integration/animo-b3/tcd018_output_digest_ledger/part3.csv",
        "integration/animo-b3/tcd018_output_digest_ledger/part4.csv",
        "tools/build_tcd018_reporting_candidate.py",
        "tools/validate_b3a03e_tcd018_evidence.py",
    }
    require(changed <= allowed, f"B3A03E changed paths outside evidence-remediation scope: {sorted(changed - allowed)}")
    forbidden = [p for p in changed if p.startswith(("src/", "source/", "production/")) or "TCD_REGISTER" in p.upper()]
    require(not forbidden, f"B3A03E production/canonical mutation: {forbidden}")


def main() -> int:
    data = validate_result_contract()
    validate_artifact_pins(data)
    validate_frozen_and_scientific_boundaries(data)
    validate_period_rows(data)
    validate_run_and_output_ledgers(data)
    validate_comparator_and_builder()
    validate_remediation_scope()
    print("PASS_TCD018_INDEPENDENT_SECOND_LINE_R2_RECORD_VALIDATOR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
