# ANIMO-TIMEQ01 synthetic runtime transaction fixture

Status: `NONPRODUCTION_ARCHITECTURE_RUNTIME_FIXTURE`.

## 1. What this fixture is

TIMEQ01 is a small executable model of the TIME01/ARCHG02 transaction contract. It exists to test whether the candidate lifecycle and trace rules can be represented and enforced at runtime without implementing any ANIMO scientific process.

The fixture carries only:

- synthetic accepted owner values;
- accepted generation identity;
- interval and trial identity;
- immutable external-frame metadata and small synthetic payloads;
- synthetic trial-local mutations;
- typed event records classified as physical, provisional or report-only;
- scheduler trace records with explicit generation labels;
- synthetic coupled-owner generation tokens.

It does **not** calculate nutrient transformations, sorption, transport, crop demand, hydrology, GHG, macropore physics or numerical convergence.

## 2. Lifecycle

The fixture implements the candidate lifecycle:

```text
ACCEPTED_IDLE
    |
    | begin_trial(interval_id, trial_id, t0, t1, frames)
    v
TRIAL_EXECUTING
    |       |
    |       +--> reject --> ACCEPTED_IDLE, same accepted generation
    |
    +--> ready --> TRIAL_READY
                    |
                    +--> accept if all coupled participants ready
                              |
                              v
                         ACCEPTED_IDLE
                         new accepted generation
```

`AcceptedState` is immutable. Trial mutation happens on a copied trial-local value map. This is intentionally a modern abstraction. TS01 already established that revision 53 does not literally keep its current/start arrays immutable throughout a timestep.

## 3. Identity contract

A trial binds:

- `interval_id`;
- `trial_id`;
- `t0` and `t1`;
- starting accepted generation;
- topology/configuration identity;
- zero or more external frame IDs.

Every retry requires a fresh `trial_id`.

If `t1` changes, the fixture requires a new `interval_id`. Reusing the old interval identity with changed endpoints fails closed.

An external `frame_id` is content-addressed by contract semantics: once observed, the same ID cannot denote different interval, generation, geometry, configuration, endpoint or payload metadata.

## 4. Generation labels

Trace records may use the TIME01/ARCHG02 generation roles:

- `G_ACCEPTED_START`;
- `G_MUTATED_EVENT`;
- `G_PROVISIONAL`;
- `G_ACTUAL_RESULT`;
- `G_PREVIOUS_NEIGHBOR`;
- `G_SAME_STEP_DERIVED`;
- `G_REPORT_ONLY`.

TIMEQ01 does not claim that these are literal revision-53 objects. It tests whether a modern runtime can make the distinctions explicit.

## 5. Event journal

Each event is classified as exactly one of:

- `PHYSICAL`;
- `PROVISIONAL`;
- `REPORT_ONLY`.

Only `PHYSICAL` events can become committed events on accept. Rejection discards all trial events. Provisional and report-only records may remain in diagnostic trace but never enter the committed physical journal.

Crop uptake is represented by one directed physical event identity from soil to crop. The fixture deliberately does not model a second physical event for the later crop-state bookkeeping step.

## 6. Same-step and previous-step views

Two trace sentinels intentionally distinguish opposite generation requirements from TS01:

- same-step management mutation is written as `G_MUTATED_EVENT` and can be read by later synthetic process probes in the same trial;
- a previous-neighbour probe explicitly reads `G_PREVIOUS_NEIGHBOR` from the immutable accepted snapshot rather than the trial's latest value.

The fixture therefore rejects the idea that one generic `latest_state` API is sufficient for source-equivalent migration.

## 7. Event boundary classifier

The fixture contains exact source-compatibility predicates only as event-selection sentinels:

- management event: `t0 < event_time <= t1`;
- annual harvest/root-residue event: `t0 <= event_time < t1`.

This does not claim that the asymmetry is scientifically optimal. It only proves that the candidate scheduler can represent the source-bound distinction.

## 8. Layer-order trace

TIMEQ01 does not solve transport. It can record and verify scheduler traces for:

- generic `Sqnu` traversal with `G_SAME_STEP_DERIVED` propagation semantics;
- phosphorus per-layer `transport+phase` coupling in the same `Sqnu` order.

The trace fixture must reject an order that differs from the bound expected order when operating in source-equivalence mode.

## 9. Coupled acceptance barrier

The synthetic engine holds accepted generation tokens for ANIMO and external owners. A coupled accept succeeds only when every required participant provides the expected next-generation token and is marked ready.

A failed barrier leaves every accepted token unchanged. This tests no-partial-commit semantics without implementing any distributed commit protocol.

## 10. Checkpoint rule

A synthetic checkpoint can be requested only in `ACCEPTED_IDLE`. It contains accepted state identity and owner-generation metadata only. Trial-local values, trial events and scratch/trace are excluded.

This is contract evidence only. It is not a claim that the historical `INITIAL.OUT` payload is restart-sufficient.

## 11. Synthetic rollback/replay

TIMEQ01 may reject one synthetic trial and rerun the same interval from the unchanged accepted state under a fresh `trial_id`. If identical deterministic synthetic operations are applied, the accepted values and committed physical event signature must match a clean execution.

This is **not** B2 restart or rollback equivalence. It verifies only the internal determinism and rollback semantics of the fixture.

## 12. Qualification boundary

A passing fixture can support only:

`QUALIFIED_CANDIDATE_RUNTIME_TRANSACTION_AND_SCHEDULER_TRACE_FIXTURE_NON_B2_NONPRODUCTION`.

It cannot establish scientific process correctness, numerical equivalence, historical behaviour, canonical TIME, MASS/EX admission, B3/B4 or production readiness.
