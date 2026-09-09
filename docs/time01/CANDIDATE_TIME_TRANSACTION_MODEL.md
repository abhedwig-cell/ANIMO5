# ANIMO-TIME01 candidate time and transaction model

Status: `CANDIDATE_CONTRACT_ONLY`.

This document defines a future-facing transaction model constrained by TS01 source evidence. It is not a claim that revision 53 implements transactions literally and it does not admit canonical TIME.

## 1. Core semantic objects

A runtime interval is described by immutable identities:

- `interval_id`: identity of one proposed model interval and its exact `t0`/`t1` coordinates;
- `accepted_generation_id`: identity of the ANIMO state accepted at `t0`;
- `trial_id`: identity of one execution attempt for that interval;
- `configuration_identity` and `physical_layout_id` from the admitted configuration/state architecture;
- `hydrology_frame_id` and, when applicable, `crop_frame_id`;
- `calendar_contract_id`: identity of calendar/time-coordinate interpretation;
- `event_schedule_identity`: identity of the event schedule/configuration used to classify events.

`interval_id` and `trial_id` are deliberately different. A retry of the same `t0 -> t1` interval receives a new `trial_id`. A retry with a different `t1` is a different interval and therefore receives a new `interval_id` and newly bound interval frames.

## 2. Time coordinates

TIME01 requires time coordinates to be:

- totally ordered under one explicit calendar contract;
- losslessly serializable within the chosen representation;
- comparable without hidden tolerance;
- able to represent every admitted forcing, event and checkpoint boundary;
- independent of report-period semantics.

TIME01 does not select a binary encoding, tick quantum or floating-point representation. That choice must be verified against the admitted input/calendar range before canonical TIME admission.

The semantic interval is an ordered pair `(t0,t1)` with `t1 > t0`. Endpoint membership for events is defined by the event class, not by a universal interval convention.

## 3. Transaction state machine

The candidate lifecycle is:

`ACCEPTED_IDLE -> TRIAL_BOUND -> TRIAL_EXECUTING -> TRIAL_READY -> ACCEPTED_IDLE`

or:

`ACCEPTED_IDLE -> TRIAL_BOUND -> TRIAL_EXECUTING -> TRIAL_READY/FAILED -> REJECTED -> ACCEPTED_IDLE`

A retry starts again from the unchanged accepted generation with a new `trial_id`.

### ACCEPTED_IDLE

- one accepted state exists at `t0`;
- no trial-local physical journal is committed;
- checkpoints may be created if the restart contract is otherwise satisfied.

### TRIAL_BOUND

Before process execution, the trial binds:

- exact `interval_id`, `t0`, `t1` and calendar contract;
- accepted ANIMO generation;
- configuration/layout identities;
- all required immutable external frames;
- event schedule identity;
- active feature topology.

A stale or mismatched frame fails before process mutation.

### TRIAL_EXECUTING

The accepted state remains immutable. The trial may contain mutable state, scratch and a trial-local transfer journal. Process execution follows the admitted partial order and explicit state-generation read rules.

### TRIAL_READY

All required physical processes have completed, candidate end state exists, trial-local journal is complete, and structural/conservation/numerical acceptance checks required by later gates have either passed or returned a decision to reject. Reporting is not the mechanism that creates this state.

### ACCEPT

Acceptance is one logical transaction boundary:

- candidate end state becomes the next accepted ANIMO generation at `t1`;
- trial physical journal becomes committed for the interval;
- accepted metadata records interval/trial identity;
- trial scratch is discarded;
- observers may consume committed state/journal.

In coupled execution, local readiness is insufficient. The logical group barrier must prevent one participant from irreversibly advancing before all required participants can accept the same interval.

### REJECT

Rejection:

- discards trial state, trial scratch and uncommitted physical journal;
- leaves accepted ANIMO state unchanged;
- leaves external accepted owner generations unchanged;
- may append nonphysical diagnostic information about the failed attempt.

Rejected physical events never contribute to committed conservation ledgers.

## 4. Legacy-compatible state-generation views

ARCH01's immutable future `AcceptedState` can reproduce revision-53 semantics only if trial reads distinguish the following views:

- `G_ACCEPTED_START`: immutable accepted snapshot at `t0`;
- `G_MUTATED_EVENT`: trial state after same-step residue/management mutation;
- `G_PROVISIONAL`: potential-pass result/scratch that is not a physical committed outcome;
- `G_ACTUAL_RESULT`: completed candidate end state for the interval;
- `G_PREVIOUS_NEIGHBOR`: explicit reads from the accepted/start neighbour where source requires previous-step values;
- `G_SAME_STEP_DERIVED`: explicit same-step upstream averages/results propagated in scheduler order;
- `G_REPORT_ONLY`: diagnostics/reporting state outside physical ownership.

No process API may silently substitute a generic `latest state` view when source-equivalence requires one of these identities.

This is the key reconciliation with TS01: legacy current/start arrays are mutated by `Addit`, but the future architecture may keep `AcceptedState` immutable by applying management to `TrialState` and routing later reads to `G_MUTATED_EVENT`.

## 5. Event semantics

Event identity contains at least:

- event class;
- source/schedule row identity;
- event time;
- event ordering key within the same source row/packet;
- interval that selected it;
- trial identity during execution;
- physical or diagnostic classification.

For source-equivalence mode:

- management packets use `t0 < E <= t1`;
- annual harvest/root-residue uses `t0 <= H < t1`;
- same-row material addition occurs before ploughing;
- year-boundary start and closeout hooks remain on their source-observed sides of the boundary;
- balance-period closure remains diagnostic, not a physical event boundary.

A future scientific correction may replace these rules only through an admitted discrepancy/theory decision.

## 6. Process scheduling rule

TIME01 does not require one monolithic routine order. It requires a partial order whose edges preserve all source-observed data dependencies relevant to source-equivalence.

A process declaration must state:

- required predecessor boundary or data dependency;
- state-generation views read;
- state-generation view written;
- whether the output is provisional, physical candidate state, transfer event or diagnostic;
- layer traversal constraint if any;
- feature activation condition;
- whether it is retry-safe under immutable input frames.

Specific edges are defined in `SCHEDULER_PARTIAL_ORDER_CONTRACT.md`.

## 7. Potential versus actual execution

Potential/process-provisional calculation is explicitly noncommitting. It may write `G_PROVISIONAL` and diagnostic scratch but cannot append committed physical transfers.

The actual pass consumes required provisional/aeration information and produces `G_ACTUAL_RESULT` plus trial-local physical events. This prevents the source-observed potential results from being double-counted in a typed future MassLedger.

## 8. Layer order and mixed-generation reads

Two noninterchangeable dependency types are explicit:

- `PREVIOUS_ACCEPTED_NEIGHBOR`: read neighbour from `G_ACCEPTED_START`, required by the identified `Resp_miner` availability path;
- `SAME_TRIAL_UPSTREAM`: read same-step upstream derived result, required by generic transport and P `Sqnu` traversal.

These dependency labels are scheduler constraints. Parallel execution is admissible only after a separate reformulation qualification proves equivalent dependency satisfaction.

## 9. External frame binding

A coupled trial cannot read hydrology/crop data by implicit record position alone. Every external frame must bind to:

- the exact interval coordinates it describes;
- producer accepted generation at `t0`;
- required end/proposed coordinates at `t1`;
- geometry/layout/configuration/schema identities;
- immutable frame content identity.

Changed frame content requires a new frame identity. Changed `t1` requires interval rebind and newly valid frames.

## 10. Reporting boundary

Physical acceptance and reporting are separate.

- `Outbal_calc`-equivalent observation occurs only after the physical candidate interval is complete.
- report rollover/reset changes diagnostic continuation state only;
- a report boundary neither accepts nor rejects a physical trial;
- diagnostic continuation may be checkpointed separately when output continuity is promised.

## 11. Initialization

Initialization is not the first normal trial. It constructs the first accepted generation through a separately qualified initialization transaction. Any initialization projection or correction must be explicit before beginning-storage diagnostics are established.

TS01 first-step semantics therefore cannot be used as evidence for ordinary accept/retry behaviour.

## 12. Topology and configuration transitions

Within `TRIAL_BOUND`, configuration, feature topology, geometry, site cardinality and ownership mode are immutable.

A requested topology/configuration transition is allowed only at an accepted boundary and only under a separately admitted state-migration/transition contract. Otherwise the scheduler fails closed.

## 13. Qualification boundary

TIME01 specifies an internally coherent candidate contract only. Runtime implementation, independent B2 replay/split-run evidence, numerical acceptance tolerances, GHG/macropore positive-path temporal qualification and scientific corrections remain outside this workunit.
