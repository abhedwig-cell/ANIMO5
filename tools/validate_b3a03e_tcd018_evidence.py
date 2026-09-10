#!/usr/bin/env python3
"""Fail-closed structural validator for ANIMO-B3A03E.

This validator qualifies persistence and internal consistency of the remediated
TCD-018 evidence packet. It does not perform an independent scientific review,
create B2 evidence, or admit TCD-018.
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_REVIEW = "57cfdfb3a7fb982f6692b0b32f8c8aa044c57fd7"
B3D05 = "2f06cc86225637f8dadfdd969fe48dcf851b9ee2"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
BASE_EXE = "0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e"
CAND_EXE = "c1e281d5ceaa45952dc7ee21041454fbfab5bee34aa8aee09d59604b75826bbe"
HEX64 = re.compile(r"[0-9a-f]{64}")

MANIFEST_PATH = ROOT / "integration/animo-b3/TCD018_EVIDENCE_REMEDIATION_MANIFEST.json"
PERIOD_PATH = ROOT / "integration/animo-b3/TCD018_25_PERIOD_RECONCILIATION.csv"
RUN_PATH = ROOT / "integration/animo-b3/TCD018_EIGHT_CASE_RUN_LEDGER.json"
LEDGER_DIR = ROOT / "integration/animo-b3/tcd018_output_digest_ledger"
BUILDER_PATH = ROOT / "tools/build_tcd018_reporting_candidate.py"
STATUS_PATH = ROOT / "integration/animo-b3/ANIMO-B3A03E_STATUS.json"
DOC_PATH = ROOT / "docs/b3/TCD018_EVIDENCE_REMEDIATION.md"

EXPECTED_CASE_COUNTS = {
    "CranGrass": 31,
    "CranMais": 23,
    "GrassPeat": 60,
    "LWKM_gras_1040.2021.2045": 53,
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
EXPECTED_CLASSES = Counter({
    "EQUAL_RAW": 270,
    "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY": 100,
    "DIFFERENT_WHITELISTED": 6,
})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL_B3A03E: " + message)


def close(a: float, b: float, atol: float = 1.0e-12) -> bool:
    # Serialization-consistency check only; never a scientific acceptance epsilon.
    return math.isclose(a, b, rel_tol=0.0, abs_tol=atol)


def main() -> int:
    for path in [MANIFEST_PATH, PERIOD_PATH, RUN_PATH, BUILDER_PATH, DOC_PATH]:
        require(path.is_file(), f"missing required artifact {path.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    require(manifest["work_unit"] == "ANIMO-B3A03E", "wrong work unit")
    require(manifest["target"] == "TCD-018", "wrong target")
    require(manifest["class"] == "A_ACCOUNTING_REPORTING_ONLY", "wrong class")
    require(manifest["base_review"]["head"] == BASE_REVIEW, "wrong failed-review base")
    require(
        manifest["base_review"]["result"] == "FAIL_TCD018_INDEPENDENT_SECOND_LINE_READINESS_REVIEW",
        "failed review must remain explicit",
    )
    require(manifest["formal_route_authority"]["head"] == B3D05, "wrong B3D05 authority")
    require(manifest["formal_route_authority"]["historical_behaviour"] == "UNKNOWN", "historical behaviour must remain UNKNOWN")
    require(manifest["frozen_identity"]["source_zip_sha256"] == SOURCE_SHA, "source identity drift")
    require(manifest["frozen_identity"]["testbank_zip_sha256"] == TESTBANK_SHA, "testbank identity drift")
    require(manifest["execution_environment"]["baseline_executable_sha256"] == BASE_EXE, "baseline executable drift")
    require(manifest["execution_environment"]["fresh_candidate_executable_sha256"] == CAND_EXE, "candidate executable drift")
    require(manifest["period_reconciliation"]["acceptance_tolerance_defined"] is False, "scientific tolerance must not be defined")
    require(manifest["period_reconciliation"]["raw_0_0601_mm_used_as_tolerance"] is False, "0.0601 mm must not be a tolerance")
    require(manifest["eight_case_noninterference"]["scientific_numeric_tolerance_applied"] is False, "numeric tolerance must remain false")

    # Complete 25-period record.
    with PERIOD_PATH.open(newline="", encoding="utf-8") as stream:
        periods = list(csv.DictReader(stream))
    require(len(periods) == 25, "period ledger must contain exactly 25 rows")
    require([int(r["year"]) for r in periods] == list(range(1991, 2016)), "period years must be exactly 1991..2015")
    previous = 0
    probe_records = 0
    for row in periods:
        start = int(row["period_start_tito_exclusive"])
        end = int(row["period_end_tito"])
        days = int(row["period_days_reported"])
        records = int(row["hydro_probe_records"])
        require(start == previous, f"non-contiguous period start in {row['year']}")
        require(end - start == days, f"Tito duration mismatch in {row['year']}")
        require(records == 36, f"expected 36 fresh hydro probe records in {row['year']}")
        hb = float(row["hydro_badev_sum_raw_mm"])
        ic = float(row["interception_storage_change_sum_raw_mm"])
        recon = float(row["reconstructed_legacy_raw_mm"])
        legacy = float(row["legacy_bawadv_formatted_mm"])
        cdelta = float(row["reconstruction_minus_legacy_formatted_mm"])
        cand = float(row["fresh_candidate_bawadv_formatted_mm"])
        cand_delta = float(row["fresh_candidate_minus_hydro_badev_raw_mm"])
        require(close(hb + ic, recon, 1.0e-14), f"reconstruction arithmetic mismatch in {row['year']}")
        require(close(recon - legacy, cdelta, 1.0e-14), f"legacy delta arithmetic mismatch in {row['year']}")
        require(close(cand - hb, cand_delta, 1.0e-14), f"candidate delta arithmetic mismatch in {row['year']}")
        previous = end
        probe_records += records
    require(previous == 9131, "final period Tito must be 9131")
    require(probe_records == 900, "period ledger must account for 900 fresh hydro probe records")

    y2008 = next(r for r in periods if r["year"] == "2008")
    require(close(float(y2008["legacy_bawadv_formatted_mm"]), -0.0601), "2008 legacy value drift")
    require(close(float(y2008["interception_storage_change_sum_raw_mm"]), -0.06), "2008 interception storage drift")
    require(close(float(y2008["hydro_badev_sum_raw_mm"]), -5.2640587582358e-5), "2008 Hydro_detailed sum drift")

    # Per-output digest evidence.
    ledger_files = [ROOT / p for p in manifest["eight_case_noninterference"]["output_digest_ledger_parts"]]
    require(len(ledger_files) == 4, "expected exactly four digest-ledger partitions")
    rows = []
    for path in ledger_files:
        require(path.is_file(), f"missing digest partition {path.relative_to(ROOT)}")
        with path.open(newline="", encoding="utf-8") as stream:
            rows.extend(csv.DictReader(stream))
    require(len(rows) == 376, "digest ledger must contain exactly 376 output rows")
    keys = [(r["case"], r["path"]) for r in rows]
    require(len(set(keys)) == 376, "digest ledger case/path keys must be unique")
    require(Counter(r["case"] for r in rows) == Counter(EXPECTED_CASE_COUNTS), "per-case output counts drift")
    require(Counter(r["classification"] for r in rows) == EXPECTED_CLASSES, "output classification totals drift")

    diffs = [r for r in rows if r["classification"] == "DIFFERENT_WHITELISTED"]
    require({r["case"] for r in diffs} == {"LWKM_gras_1040.2021.2045"}, "whitelisted differences must occur only in LWKM")
    require({Path(r["path"]).name for r in diffs} == EXPECTED_WHITELIST, "whitelisted difference surface drift")

    for row in rows:
        cls = row["classification"]
        common = row["common_sha256"]
        ref = row["reference_sha256"]
        cand = row["candidate_sha256"]
        if cls in {"EQUAL_RAW", "EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY"}:
            require(bool(HEX64.fullmatch(common)), f"missing common digest for {row['case']}:{row['path']}")
            require(ref == "" and cand == "", f"equal row must use common digest only for {row['case']}:{row['path']}")
        elif cls == "DIFFERENT_WHITELISTED":
            require(common == "", f"different row must not have common digest for {row['case']}:{row['path']}")
            require(bool(HEX64.fullmatch(ref)) and bool(HEX64.fullmatch(cand)), f"different row missing side digests for {row['case']}:{row['path']}")
            require(ref != cand, f"different row side digests unexpectedly equal for {row['case']}:{row['path']}")
        else:
            raise SystemExit(f"FAIL_B3A03E: unexpected classification {cls}")

    # Separate run completion evidence.
    run_records = json.loads(RUN_PATH.read_text(encoding="utf-8"))
    require(len(run_records) == 16, "run ledger must contain 16 records")
    expected_pairs = {(case, variant) for case in EXPECTED_CASE_COUNTS for variant in ("baseline", "candidate")}
    actual_pairs = {(r["case"], r["variant"]) for r in run_records}
    require(actual_pairs == expected_pairs, "run ledger case/variant coverage drift")
    require(all(r["success_message_present"] is True for r in run_records), "all 16 runs must have successful-completion evidence")
    require(all(bool(HEX64.fullmatch(r["runner_stdout_sha256"])) for r in run_records), "runner stdout digests must be SHA-256")

    # Pinned candidate builder must remain explicitly bounded.
    builder = BUILDER_PATH.read_text(encoding="utf-8")
    for token in [SOURCE_SHA, CAND_EXE, "Sic,Sict", "(Sict-Sic)*1.d3", "qualification tooling only"]:
        require(token in builder, f"candidate builder missing required token: {token}")

    boundaries = manifest["hard_boundaries"]
    require(all(value is False for value in boundaries.values()), "all hard-boundary admission/promotion flags must remain false")
    require(manifest["residual_boundaries"]["global_water_closure_claimed"] is False, "global water closure must not be claimed")
    require(
        manifest["residual_boundaries"]["MASSQ01_CranGrass_TITO724_class"] == "UNEXPLAINED_RESIDUAL_RETAINED_OUTSIDE_TCD018",
        "unrelated CranGrass residual must remain visible",
    )

    # If a status record is present, it must remain bounded to remediation only.
    if STATUS_PATH.exists():
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        require(status["work_unit"] == "ANIMO-B3A03E", "status work unit drift")
        require(status["target"] == "TCD-018", "status target drift")
        require(status["independent_second_line_pass"] is False, "remediation may not self-certify independent PASS")
        require(status["tcd018_admitted"] is False, "remediation may not admit TCD-018")
        require(status["production_migration_admitted"] is False, "remediation may not admit production migration")
        require(status["historical_behaviour"] == "UNKNOWN", "status historical behaviour must remain UNKNOWN")

    print("PASS_B3A03E_TCD018_EVIDENCE_REMEDIATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
