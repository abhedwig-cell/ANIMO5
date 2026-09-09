#!/usr/bin/env python3
"""Validate the TCD-028 fail-closed intake reservation across register phases.

The reservation itself is an immutable pre-append evidence snapshot bound to the
qualified TCD-001..027 register. Later integration branches may register TCD-028
and subsequent IDs only through explicit append reconciliations that preserve
non-admission.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv"
CLASSIFICATION = ROOT / "integration/animo-b3/B3_EXISTING_TCD_CLASSIFICATION.csv"
B3_STATUS = ROOT / "integration/animo-b3/ANIMO-B3Q01_STATUS.json"
RESERVATION = ROOT / "integration/animo-b3/TCD-028_RESERVATION.json"
APPEND_RECON = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_RECONCILIATION.json"
APPEND_RECON_SUPP1 = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_SUPPLEMENT_01_RECONCILIATION.json"
APPEND_RECON_SUPP2 = ROOT / "integration/animo-b3/CANONICAL_TCD_REGISTER_APPEND_SUPPLEMENT_02_RECONCILIATION.json"

EXPECTED_GOVERNANCE_HEAD = "846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_REGISTER_SHA = "224acc350fde69d3c4aebed8628c0f945e0b3367"
EXPECTED_PREP10_HEAD = "65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab"


def ids(path: Path, column: str) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row[column] for row in csv.DictReader(handle)]


def assert_recon_non_admission(recon: dict, label: str) -> None:
    admission = recon.get("admission_state", {})
    if any(admission.get(key) is not False for key in [
        "new_corrections_admitted",
        "b3_baseline_established",
        "production_migration_admitted",
        "evidence_strength_increased_by_register_append",
    ]):
        raise AssertionError(f"{label} improperly increases admission or evidence strength")


def validate_first_append() -> dict:
    if not APPEND_RECON.is_file():
        raise AssertionError("TCD-028 is registered but initial append reconciliation is missing")
    recon = json.loads(APPEND_RECON.read_text(encoding="utf-8"))
    canonical = recon.get("canonical_register", {})
    if canonical.get("tail_before") != "TCD-027" or canonical.get("tail_after") != "TCD-037":
        raise AssertionError("initial append reconciliation has unexpected register tails")
    if canonical.get("append_only") is not True or canonical.get("existing_rows_changed") is not False:
        raise AssertionError("initial TCD registration is not proven append-only")
    if "TCD-028" not in recon.get("registered_not_admitted", []):
        raise AssertionError("initial append reconciliation does not preserve TCD-028 as registered-not-admitted")
    assert_recon_non_admission(recon, "initial append reconciliation")
    return recon


def validate_supplement(path: Path, tail_before: str, tail_after: str, ids_expected: list[str], label: str) -> None:
    if not path.is_file():
        raise AssertionError(f"{label} registered IDs but append reconciliation is missing")
    recon = json.loads(path.read_text(encoding="utf-8"))
    canonical = recon.get("canonical_register", {})
    if canonical.get("tail_before") != tail_before or canonical.get("tail_after") != tail_after:
        raise AssertionError(f"{label} append reconciliation has unexpected register tails")
    if canonical.get("append_only") is not True or canonical.get("existing_rows_changed") is not False:
        raise AssertionError(f"{label} TCD registration is not proven append-only")
    if recon.get("registered_not_admitted") != ids_expected:
        raise AssertionError(f"{label} append reconciliation has unexpected registered IDs")
    assert_recon_non_admission(recon, f"{label} append reconciliation")


def validate_register_phase(register_ids: list[str]) -> str:
    pre_append_ids = [f"TCD-{i:03d}" for i in range(1, 28)]
    first_append_ids = [f"TCD-{i:03d}" for i in range(1, 38)]
    supplement_1_ids = [f"TCD-{i:03d}" for i in range(1, 40)]
    supplement_2_ids = [f"TCD-{i:03d}" for i in range(1, 41)]

    if register_ids == pre_append_ids:
        return "PRE_APPEND_RESERVATION_PHASE"

    if register_ids == first_append_ids:
        validate_first_append()
        return "POST_APPEND_REGISTERED_NOT_ADMITTED_PHASE_TCD037"

    if register_ids == supplement_1_ids:
        validate_first_append()
        validate_supplement(APPEND_RECON_SUPP1, "TCD-037", "TCD-039", ["TCD-038", "TCD-039"], "supplement-01")
        return "POST_APPEND_REGISTERED_NOT_ADMITTED_PHASE_TCD039"

    if register_ids == supplement_2_ids:
        validate_first_append()
        validate_supplement(APPEND_RECON_SUPP1, "TCD-037", "TCD-039", ["TCD-038", "TCD-039"], "supplement-01")
        validate_supplement(APPEND_RECON_SUPP2, "TCD-039", "TCD-040", ["TCD-040"], "supplement-02")
        return "POST_APPEND_REGISTERED_NOT_ADMITTED_PHASE_TCD040"

    raise AssertionError(f"unexpected canonical register sequence for TCD-028 intake: {register_ids}")


def main() -> None:
    register_ids = ids(REGISTER, "ID")
    register_phase = validate_register_phase(register_ids)

    classification_ids = ids(CLASSIFICATION, "tcd_id")
    if "TCD-028" in classification_ids:
        raise AssertionError("TCD-028 unexpectedly exists in qualified B3Q01 classification snapshot")

    status = json.loads(B3_STATUS.read_text(encoding="utf-8"))
    if status.get("qualified") is not True:
        raise AssertionError("B3Q01 governance is not qualified")
    if status.get("decision") != "QUALIFIED_B3_SCIENTIFIC_ADMISSION_FRAMEWORK_NO_LEGACY_CORRECTIONS_ADMITTED":
        raise AssertionError("unexpected B3Q01 decision")
    if status.get("corrected_legacy_admitted") is not False:
        raise AssertionError("B3Q01 must not already admit corrected legacy")
    if status.get("source_evidence", {}).get("canonical_tcd_register_blob_sha") != EXPECTED_REGISTER_SHA:
        raise AssertionError("reservation is not bound to the expected qualified canonical TCD snapshot")

    reservation = json.loads(RESERVATION.read_text(encoding="utf-8"))
    if reservation.get("record_type") != "TCD_RESERVATION_NOT_B3_DISPOSITION":
        raise AssertionError("reservation record type is not fail-closed")
    if reservation.get("tcd_id") != "TCD-028":
        raise AssertionError("wrong reserved TCD id")
    governance = reservation.get("governance_base", {})
    if governance.get("head") != EXPECTED_GOVERNANCE_HEAD:
        raise AssertionError("reservation governance head mismatch")
    if governance.get("canonical_tcd_register_sha") != EXPECTED_REGISTER_SHA:
        raise AssertionError("reservation canonical register SHA mismatch")
    if governance.get("canonical_register_tail_at_reservation") != "TCD-027":
        raise AssertionError("reservation did not observe TCD-027 as prior tail")

    prep10 = reservation.get("prep10_binding", {})
    if prep10.get("head") != EXPECTED_PREP10_HEAD:
        raise AssertionError("reservation PREP10 evidence head mismatch")
    if prep10.get("draft_pr") != 9 or prep10.get("intake_issue") != 8:
        raise AssertionError("reservation review surfaces mismatch")

    if reservation.get("provisional_class") != "B":
        raise AssertionError("TCD-028 intake must remain provisional Class B")
    if reservation.get("provisional_disposition") != "UNRESOLVED_NOT_ADMITTED":
        raise AssertionError("TCD-028 must remain unresolved/not admitted")

    b2 = reservation.get("b2", {})
    if b2.get("status") != "NOT_ESTABLISHED":
        raise AssertionError("B2 must remain not established at intake")
    if b2.get("historical_reference_recovery_still_open") is not True:
        raise AssertionError("historical reference recovery must still be open")
    if b2.get("documented_acquisition_route_formally_exhausted") is not False:
        raise AssertionError("intake must not claim B2 acquisition exhaustion")
    if b2.get("normal_b2_route_eligible_now") is not False:
        raise AssertionError("normal B2 route cannot be eligible without B2")
    if b2.get("historical_uncertainty_route_eligible_now") is not False:
        raise AssertionError("historical-uncertainty route cannot be eligible before exhaustion")

    disposition = reservation.get("b3_disposition_record", {})
    if disposition.get("instantiated") is not False:
        raise AssertionError("B3 disposition record must not be fabricated at intake")
    if disposition.get("fail_closed_state") != "B3_DISPOSITION_RECORD_DEFERRED_UNTIL_ADMISSION_ROUTE_ELIGIBLE":
        raise AssertionError("unexpected disposition deferral state")

    canonical = reservation.get("canonical_register", {})
    if canonical.get("tcd_028_row_present") is not False:
        raise AssertionError("reservation snapshot must record TCD-028 as absent at reservation time")
    if canonical.get("append_pending_review") is not True:
        raise AssertionError("reservation snapshot must preserve append-pending-review state")
    if canonical.get("b3q01_existing_classification_snapshot_modified") is not False:
        raise AssertionError("qualified B3Q01 snapshot must remain unchanged")

    admissions = reservation.get("admissions", {})
    if any(admissions.get(key) is not False for key in [
        "b3_admitted", "corrected_legacy_admitted", "reference_output_admitted", "production_migration_admitted"
    ]):
        raise AssertionError("TCD-028 reservation must admit nothing")

    print(f"TCD-028 B3 intake reservation validation: PASS ({register_phase})")


if __name__ == "__main__":
    main()
