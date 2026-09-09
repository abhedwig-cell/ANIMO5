# ANIMO-TIME01 — Generic Time, Transaction, Retry & Scheduler Contract Qualification

Status: `ACTIVE_CANDIDATE_ARCHITECTURE_WORKUNIT`.

## Purpose

TIME01 converts the source-bound temporal constraints from ANIMO-TS01 and the candidate transaction/state/exchange assumptions from ARCH01, ARCH02 and ARCH07 into one explicit candidate generic time and transaction contract.

TIME01 is architecture qualification work only. It does not implement a production scheduler, modify revision-53 source, modify the historical testcase corpus, define scientific corrections, or admit canonical TIME.

## Repository and branch

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-time01-generic-time-transaction-contract`

Starting head: `ed12a678cfba19ce851eb2f380e6da3f49203fe4`

Starting workunit: `ANIMO-TS01`

## Authoritative inputs checked at start

- TS01 continuation head: `ed12a678cfba19ce851eb2f380e6da3f49203fe4`
- ARCH01 head: `24f57d8daab828f88446a79bd6a276f2925c828b`
- ARCH02 head: `a079d93c965f6073586c55ee4b3544dd8873b723`
- ARCH07 qualification commit: `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`
- ARCHG01 head observed by TS01: `92812896b6a91b422fcbd9bf5e843da5cfc0f278`

No existing branch containing `time` or `transaction` was found when TIME01 was opened. TIME01 therefore starts as a new workunit rather than replacing another candidate.

## Evidence boundary

TIME01 must preserve the distinction between:

- `SOURCE_EQUIVALENCE_CONSTRAINT`: revision-53 ordering/dataflow facts reconstructed by TS01;
- `FUTURE_TRANSACTION_POLICY`: new architecture policy needed for deterministic trial, accept, reject, retry and coupled ownership;
- `REFERENCE_BEHAVIOR_REQUIRED`: claims that need independent B2/reference execution;
- `SCIENTIFIC_ADMISSION_REQUIRED`: intentional behaviour changes that require B3/theory qualification.

Candidate architecture coherence is not historical behavioural qualification.

## Hard constraints

TIME01 SHALL NOT:

1. alter revision-53 source;
2. alter supplied historical testcases;
3. implement a production scheduler, adapter or process kernel;
4. claim that legacy has an explicit atomic commit/reject mechanism;
5. normalize management and harvest endpoint semantics into one rule without admitted evidence;
6. remove `Sqnu` order or mixed-generation reads by architectural assumption;
7. commit provisional/potential-pass physical transfers;
8. use report reset as physical acceptance;
9. define numerical comparison tolerances outside qualified numerical policy;
10. claim split-run, replay or restart equivalence without independent reference evidence;
11. admit canonical `TIME`, `MASS`, `EX` or production migration.

## Candidate questions

TIME01 must define, at specification level:

- canonical interval identity and calendar coordinates;
- accepted generation and trial identity;
- trial lifecycle state machine;
- immutable versus mutable state and frame bindings;
- source-compatible state-generation views;
- event selection semantics and event identity;
- process partial-order constraints;
- same-step versus previous-step dependency declarations;
- retry semantics and whether `t1` or external frames may change;
- coupled accept/reject barrier requirements;
- checkpointable boundaries;
- reporting/diagnostic boundaries separate from physical commit;
- fail-closed topology/configuration transition policy;
- minimum trace required to qualify implementations later.

## Required deliverables

- `docs/time01/CANDIDATE_TIME_TRANSACTION_MODEL.md`
- `docs/time01/INTERVAL_FRAME_IDENTITY_CONTRACT.md`
- `docs/time01/SCHEDULER_PARTIAL_ORDER_CONTRACT.md`
- `docs/time01/RETRY_REJECT_CHECKPOINT_POLICY.md`
- `integration/animo-time/TIME01_REQUIREMENT_COVERAGE.csv`
- `tools/audit_time01_candidate_contract.py`
- `integration/animo-time/TIME01_STRUCTURAL_AUDIT.json`
- `integration/animo-time/ANIMO-TIME01_STATUS.json`

## Qualification target

The strongest admissible result for this workunit without new B2 evidence is:

`QUALIFIED_CANDIDATE_GENERIC_TIME_TRANSACTION_AND_SCHEDULER_CONTRACT`

This means the specification is internally coherent, explicitly covers the TS01 source constraints and reconciles the current candidate architecture inputs. It does NOT mean canonical TIME is admitted.

The required closeout flags remain:

- `candidate_contract_only = true`
- `historical_reference_qualified = false`
- `canonical_time_admitted = false`
- `production_implemented = false`
- `production_migration_admitted = false`

## Work method

Follow `persist early, test second`:

1. persist the workunit boundary and candidate contracts;
2. persist a machine-readable requirement matrix;
3. add a fail-closed structural audit;
4. run only specification/static consistency checks available in this workunit;
5. close with unresolved behavioural and scientific gates still visible.
