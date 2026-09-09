# ANIMO-ARCH01 transaction state model

Status: `CANDIDATE_DESIGN_ONLY`.

This document connects PREP06's accepted/start versus result/end evidence to the existing ANIMO5 architecture invariants for checkpoint, trial, commit and rollback. It does not define time integration policy. Generic time semantics remain a later serial gate.

## Transaction objects

A future ANIMO5 step is modeled conceptually with four separate objects:

1. `AcceptedState`: continuation-critical state at the beginning of the proposed interval;
2. `TrialState`: mutable candidate post-state for that interval;
3. `TrialScratch`: rates, averages, solver work and other nonpersistent intermediates;
4. `TransferJournal`: typed physical transfer events and diagnostic constraint observations produced by that trial.

Configuration, parameters, forcing and exchange data are separate read-only inputs to the trial.

## Begin trial

Beginning a trial creates a candidate state from the accepted state under explicit copy/share semantics and binds the forcing/exchange frame for `[t0,t1]`.

The operation must not change accepted state. Optional component state exists only when its feature is active and qualified.

Hydrological coordinates are supplied through the explicit hydrology exchange contract rather than by reading internal SWAP state or files from inside the kernel.

## Process execution

Processes may:

- read accepted state when old-state values are scientifically required;
- read and mutate trial state according to the process schedule;
- allocate/write trial scratch;
- append typed transfer events to the trial journal;
- append diagnostic nonclosure/constraint observations.

Processes may not:

- mutate accepted state;
- mutate reporting accumulators as a substitute for physical state;
- commit their own partial state independently;
- write directly into another model's internal state;
- turn a diagnostic correction into an external flux without an admitted contract.

## Derived views

Derived values are associated with a specific snapshot. A derived concentration, site total or demand value must declare whether it was computed from accepted or trial state. This prevents stale or mixed-generation values from becoming implicit continuation state.

## Commit

Commit is atomic at the column/model-instance level:

- `TrialState` becomes the next `AcceptedState`;
- the trial transfer journal becomes the committed journal for the interval;
- commit metadata identifies the exact interval and transaction;
- trial scratch is discarded;
- reporting may consume the committed state and journal.

There is no separate process-level commit.

## Reject / rollback

Reject discards `TrialState`, `TrialScratch` and the trial transfer journal. `AcceptedState` is unchanged bit-for-bit under the eventual implementation contract, except for diagnostics stored outside physical state.

A rejected trial cannot contribute mass to cumulative physical ledgers. Diagnostic counters may record that a rejected attempt occurred, but these counters remain outside conserved state.

## Initialization transaction

Initialization is treated separately from normal stepping:

1. parse/construct the initial physical specification;
2. perform any qualified state partition/projection as an initialization transaction;
3. produce an initialization transfer/adjustment journal where needed;
4. only then freeze the first `AcceptedState` and derive beginning-storage diagnostics.

This ordering is required by the TCD-014 class of initialization seam. It prevents a hidden state projection from appearing later as an unexplained first-step residual.

## Restart/checkpoint contract

A checkpoint contains only continuation-critical accepted state plus the configuration/identity information required to interpret it. It must not require serialized reporting accumulators or reconstructable derived views unless later evidence proves they affect continuation.

The candidate ownership registry therefore distinguishes persistent state from derived views and diagnostics. A later restart-continuity qualification workunit must still verify exact sufficiency against source/reference behaviour before this becomes canonical.

## Coupled execution boundary

The transaction contract is intended to support standalone, SWAP-coupled and later multi-column execution through the same kernel:

- external models exchange typed forcing/state frames;
- no model accesses another model's internal data structures;
- accepted ANIMO state remains ANIMO-owned except for explicitly exchange-owned hydrological coordinates;
- coupling orchestration decides when a trial is accepted or rejected under the later admitted time/transaction policy.

ARCH01 does not choose that orchestration policy.

## Evidence-driven constraints

- TCD-015: a numerical state constraint must not create unexplained accepted-state mass loss/gain.
- TCD-016: a state becoming numerically unrepresentable requires an explicit continuation representation or qualified external path, not silent zeroing.
- TCD-017/TCD-018/TCD-026/TCD-027/TCD-028: observers are not state and cannot be independently committed.
- TCD-023: transfer-journal species and conserved quantity must be explicit.
- TCD-024/TCD-029: site-indexed state identity must remain stable through initialization, management and trial mutation.

## Qualification boundary

This model satisfies an architecture-design need only. It does not pass the canonical `STATE` or `TIME` gates, does not prove restart sufficiency, and does not qualify any timestep acceptance/rejection algorithm.
