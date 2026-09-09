# ANIMO-ARCHG02 work unit contract

Status: `RESERVED_AND_STARTED`.

## Work unit

`ANIMO-ARCHG02 — Consolidated Candidate Architecture Temporal Revalidation after TS01/TIME01`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-archg02-temporal-revalidation`

Base architecture branch: `work/animo-archg01-candidate-architecture-consolidation`

Base architecture head: `5cef7969ee921acd2044521cc7636d388aa02efe`.

## Purpose

Revalidate the consolidated ARCHG01 candidate architecture against the completed source-bound temporal audit TS01 and the completed candidate TIME01 contract, using RG02 G5 authority/provenance attachment as governance context.

This is an architecture-governance revalidation, not a production implementation and not canonical TIME admission.

## Authoritative inputs at start

- ARCHG01: `work/animo-archg01-candidate-architecture-consolidation@5cef7969ee921acd2044521cc7636d388aa02efe`
- TS01: `work/animo-ts01-temporal-semantics@ed12a678cfba19ce851eb2f380e6da3f49203fe4`
- TIME01: `work/animo-time01-generic-time-transaction-contract@246128dd14732173a6f27c15c923970d50c14e2a`
- RG02 G5: `work/animo-rg02-g5-independent-stream-attachment@b289174f4378dcbfcfea9c0d77d0665b3b6c2603`
- B3Q01 remains the canonical scientific admission framework owner.

All heads must be treated as explicit evidence pins. No branch-name inference may promote parallel refs.

## Questions

1. Which ARCHG01 temporal deferrals are now source-bound resolved by TS01?
2. Which are candidate-contract resolved by TIME01 but still noncanonical?
3. Which remain unresolved because they require B2, runtime transaction evidence, canonical STATE/TIME admission, numerical policy or scientific admission?
4. Does TS01 contradict any literal interpretation of ARCHG01 lifecycle semantics, especially immutable accepted state and atomic end-of-step commit?
5. Can the accepted/trial candidate model remain coherent if legacy same-step management visibility, mixed-generation reads and `Sqnu` dependencies are represented explicitly?
6. Do ARCH02 restart semantics remain coherent after TS01's final-result serialization and management/report continuation findings?
7. Do ARCH05/07 external-frame and coupled accept/reject contracts remain compatible with TIME01?
8. Which migration seams change readiness classification after final temporal revalidation?

## Required disposition classes

- `CONFIRMED_UNCHANGED`
- `CONFIRMED_WITH_TEMPORAL_REFINEMENT`
- `SOURCE_CONSTRAINT_NOW_RESOLVED`
- `CANDIDATE_POLICY_NOW_SPECIFIED_NONCANONICAL`
- `CONTRADICTED_AS_LITERAL_LEGACY_BUT_VALID_CANDIDATE_ABSTRACTION`
- `REMAINS_BLOCKED_B2`
- `REMAINS_BLOCKED_CANONICAL_STATE_TIME`
- `REMAINS_BLOCKED_SCIENTIFIC_OR_NUMERICAL`
- `OUTSIDE_ARCHG02_SCOPE`

## Required deliverables

- `docs/architecture/ANIMO5_FINAL_TEMPORAL_REVALIDATION.md`
- `integration/animo-architecture/ARCHG02_TEMPORAL_REVALIDATION_MATRIX.csv`
- `integration/animo-architecture/ARCHG02_MIGRATION_SEAM_READINESS.csv`
- `integration/animo-architecture/ANIMO-ARCHG02_STATUS.json`

A fail-closed structural checker and CI workflow should be added after the evidence surfaces are persisted.

## Hard boundaries

- no frozen legacy source modification;
- no historical testcase modification;
- no process reorder implementation;
- no runtime scheduler implementation;
- no canonical STATE or TIME admission;
- no B2 promotion from source/static/synthetic evidence;
- no B3/B4 admission;
- no production migration admission;
- no silent rewrite of ARCHG01 historical artifacts: ARCHG02 records a revalidation overlay.

## Qualification target

`QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED_AGAINST_FINAL_TS01_TIME01_PRODUCTION_NOT_ADMITTED`

The target can be reached only if every ARCHG01 temporal deferral is explicitly dispositioned and no unresolved item is accidentally promoted to canonical or production status.
