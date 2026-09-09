# ANIMO-TIMEQ01 work unit contract

Status: `RESERVED_AND_STARTED`.

## Work unit

`ANIMO-TIMEQ01 — Candidate Runtime Transaction, Retry, Coupled Barrier & Scheduler Trace Qualification`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-timeq01-runtime-transaction-qualification`

Starting head: `db8183802631902f41aa5bec518a3c2e63e03ab7` from qualified `ANIMO-ARCHG02`.

## Purpose

Execute a non-production synthetic runtime fixture for the candidate TIME01/ARCHG02 transaction contract. The fixture must test state-machine and trace semantics only. It must not implement ANIMO chemistry, hydrology, crop science, numerical solvers, legacy process equations, or production adapters.

This workunit is intended to move selected TIME01/ARCHG02 claims from specification-only to **candidate runtime contract evidence** while keeping historical/reference/scientific evidence classes separate.

## Authoritative contract inputs

- ARCHG02: `work/animo-archg02-temporal-revalidation@db8183802631902f41aa5bec518a3c2e63e03ab7`
- TIME01: `work/animo-time01-generic-time-transaction-contract@246128dd14732173a6f27c15c923970d50c14e2a`
- TS01: `work/animo-ts01-temporal-semantics@ed12a678cfba19ce851eb2f380e6da3f49203fe4`
- ARCH07 adapter qualification specification: qualification commit `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`
- RG02 post-G5 architecture revalidation attachment remains governance context only.

## Runtime fixture scope

The fixture may model only abstract identities, small synthetic owner-state values, event records and trace entries needed to test:

1. begin-trial identity binding;
2. accepted-state immutability;
3. same-interval reject atomicity;
4. fresh `trial_id` on retry;
5. changed `t1` requiring new `interval_id` and frame rebinding;
6. immutable external-frame identity;
7. stale accepted-generation/frame rejection;
8. same-step management generation visibility;
9. explicit previous-step-neighbour read generation;
10. provisional potential events excluded from committed physical events;
11. report-only observations excluded from physical commit;
12. accepted-boundary checkpoint restriction;
13. coupled logical acceptance barrier with no partial accepted-owner advance;
14. rollback/replay determinism of the **synthetic transaction fixture only**;
15. mid-trial topology/configuration change rejection;
16. management `(t0,t1]` and harvest `[t0,t1)` event classification;
17. one physical crop-uptake transfer identity;
18. `Sqnu` trace ordering representation;
19. per-layer P transport/phase coupling trace representation.

Items 8, 9, 16, 18 and 19 verify that the candidate runtime trace can represent TS01 constraints. They do not execute the scientific processes themselves.

## Evidence classes

- `ARCH_RUNTIME_SYNTHETIC`: executable evidence that the abstract candidate transaction fixture obeys its own contract.
- `SOURCE_CONSTRAINT_TRACEABILITY`: trace mapping to already-qualified TS01 source-bound constraints.
- `REFERENCE_BEHAVIOR`: reserved and blocked until independently trustworthy B2 exists.
- `SCIENTIFIC_ADMISSION`: outside TIMEQ01.

Synthetic replay equality is not historical restart equivalence and must never be reported as B2.

## Required deliverables

- `docs/timeq01/RUNTIME_TRANSACTION_FIXTURE_MODEL.md`
- `integration/animo-time/TIMEQ01_TEST_CASES.csv`
- `tools/timeq01_runtime_fixture.py`
- `tools/test_timeq01_runtime_fixture.py`
- `integration/animo-time/TIMEQ01_RUNTIME_RESULT.json`
- `integration/animo-time/ANIMO-TIMEQ01_STATUS.json`

A GitHub Actions workflow must execute the fixture tests from a repository checkout.

## Hard boundaries

- no legacy source modification;
- no historical testcase modification;
- no production implementation;
- no real SWAP/WOFOST adapter implementation;
- no ANIMO process-kernel implementation;
- no physical/numerical tolerance invention;
- no claim of scientific correctness from synthetic state-machine tests;
- no B2, B3, canonical STATE, canonical TIME, MASS, EX, B4 or production admission;
- no process-order change relative to TS01 source-equivalence constraints.

## Qualification target

`QUALIFIED_CANDIDATE_RUNTIME_TRANSACTION_AND_SCHEDULER_TRACE_FIXTURE_NON_B2_NONPRODUCTION`

A qualification may assert that the synthetic runtime fixture executes the candidate transaction contract correctly. It may not assert legacy behavioural equivalence or canonical TIME admission.
