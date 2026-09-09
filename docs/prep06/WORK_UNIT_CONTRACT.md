# ANIMO-PREP06 — Conserved State and Transfer-Ledger Audit

Status: `WORK_UNIT_RESERVED_SOURCE_BOUND_AUDIT_ONLY`.

## Purpose

Build an explicit conserved-state and transfer-ledger inventory for the frozen ANIMO 4.1.5 revision-53 source before any production migration. The audit will separate physical storage, inter-pool transfers, external boundary fluxes, management events and reporting-only accumulators for C, N, P and water.

## Scope

- source and documentation analysis;
- machine-readable ownership inventory;
- local conservation identities and cross-checks;
- identification of missing, duplicated or cross-species ledger terms when source evidence supports them.

No frozen source or testcase change is permitted in this workunit.

Physics change: no.

Numerical-policy change: no.

Production migration: not admitted.

## Verification contract

Every state/transfer claim must be traceable to the frozen source or supplied ANIMO 4.0 documentation. Potential defects are not promoted from static suspicion to confirmed defect without a reachable or otherwise causally sufficient source-bound argument.

## Checkpoint boundary

This file reserves PREP06 before deeper analysis, following `persist early, test second`.
