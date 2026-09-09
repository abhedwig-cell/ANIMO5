# ANIMO-PREP11 work-unit contract

Work unit: `ANIMO-PREP11 — Parser-Exposed Option Contract Evidence Rehome`

Branch: `work/animo-prep11-option-contract-rehome`

Base: governance-converged ANIMO-RG02 head `67104b7253d5ebc963ee2a801f4e07a23552572a`.

Source evidence lineage: `work/animo-prep09-option-contract-audit` at `0ae0e2180cf0569f8ea22319aa9ccb54ebca3210`.

## Purpose

Rehome already persisted option-contract evidence from a duplicate PREP09 lineage into a non-colliding work-unit identity. This work unit performs evidence preservation and governance reconciliation only. It does not reinterpret or requalify the scientific findings.

## Hard boundaries

- no legacy source modification;
- no testcase modification;
- no physics change;
- no numerical-policy change;
- no corrected-legacy admission;
- no B3 or B4 admission;
- no production migration;
- no import of the source branch's `ANIMO-PREP09_STATUS.json`;
- no import of the source branch's `THEORY_CODE_DISCREPANCY_REGISTER.csv`;
- branch-local `TCD-030` is retained only as historical source text and maps in governance metadata to `RG02-LCL-AERATION-OPTION2-ALIAS` until B3 governance allocates a canonical ID.

## Verification contract

The rehome is qualified only as provenance-preserving evidence movement when:

1. every selected source evidence file is copied byte-for-byte or its source blob identity is explicitly recorded;
2. source branch and head are recorded;
3. no excluded status/register path enters PREP11;
4. tools/tests copied from the source retain exact blob identity;
5. no claim is made that rehome itself adds reference, scientific or production qualification.

## Status vocabulary

Initial status: `IN_PROGRESS_EVIDENCE_REHOME_NO_REQUALIFICATION`.

Permitted closeout status: `QUALIFIED_PROVENANCE_PRESERVING_OPTION_CONTRACT_EVIDENCE_REHOME`.
