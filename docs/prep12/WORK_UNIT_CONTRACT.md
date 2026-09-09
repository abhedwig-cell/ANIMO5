# ANIMO-PREP12 work-unit contract

Work unit: `ANIMO-PREP12 — Restart-State Continuity Evidence Rehome`

Branch: `work/animo-prep12-restart-state-continuity-rehome`

Base: governance-converged ANIMO-RG02 head `67104b7253d5ebc963ee2a801f4e07a23552572a`.

Source evidence lineage: `work/animo-prep10-restart-state-continuity` at `761db23269b45ba79df3be97ea85289682e57106`.

## Purpose

Rehome already persisted restart/state-continuity evidence from a duplicate PREP10 lineage into a non-colliding work-unit identity. This is evidence preservation and governance reconciliation only. It does not reinterpret or requalify the source findings.

## Hard boundaries

- no legacy source modification;
- no testcase modification;
- no physics change;
- no numerical-policy change;
- no corrected-legacy admission;
- no B3 or B4 admission;
- no production migration;
- no import of the source PREP10 work-unit contract;
- no import of `PREP10_DISCREPANCY_RESERVATIONS.json`;
- no import of the source branch's `THEORY_CODE_DISCREPANCY_REGISTER.csv`;
- historical local `TCD-032`, `TCD-033` and `TCD-034` remain provenance labels only and map to RG02 local identity keys until B3 governance allocates canonical IDs.

## Local identity mapping

- source local `TCD-032` -> `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`;
- source local `TCD-033` -> `RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`;
- source local `TCD-034` -> `RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`.

TCD-025 remains separate. The source evidence itself treats the macropore restart writer omission as distinct from the main-ledger macropore gap.

## Verification contract

The rehome is qualified only as provenance-preserving evidence movement when:

1. every selected evidence file is copied by exact blob identity or explicitly bound to its source blob;
2. source branch, head and tree are recorded;
3. excluded source status, contract, reservation and discrepancy-register paths do not enter PREP12;
4. the copied audit tool retains exact source blob identity;
5. no claim is made that rehome adds reference, scientific or production qualification.

## Status vocabulary

Initial status: `IN_PROGRESS_EVIDENCE_REHOME_NO_REQUALIFICATION`.

Permitted closeout status: `QUALIFIED_PROVENANCE_PRESERVING_RESTART_CONTINUITY_EVIDENCE_REHOME`.
