# ANIMO-TS01 source-bound inputs to the future TIME gate

Status: `HANDOFF_REQUIREMENTS_NOT_TIME_ADMISSION`.

The ANIMO5 migration DAG places the generic time and transaction contract after canonical state ownership and before mass accounting, exchange admission and process migration. TS01 does not admit that TIME gate. This document states only what the qualified revision-53 temporal audit requires a future TIME workunit to preserve, distinguish or explicitly requalify.

## 1. Evidence boundary

TS01 contributes source-bound B0 implementation evidence and structural/synthetic qualification specifications. It does not contribute independent B2 historical behaviour and does not define a corrected B3 reference.

A future TIME design must therefore keep three categories separate:

1. `SOURCE_EQUIVALENCE_CONSTRAINT`: directly reconstructed from revision-53 ordering/dataflow;
2. `FUTURE_TRANSACTION_POLICY`: required by the candidate architecture but not a literal legacy mechanism;
3. `OPEN_ADMISSION_QUESTION`: cannot be resolved from source order alone.

## 2. Source-equivalence constraints

The following belong in the TIME input contract unless a later admitted difference supersedes them.

### Interval and state generations

- The main interval clock is advanced before ordinary `Init` staging.
- Ordinary continuation stages previous final `Rs*` results into current/start arrays at the beginning of the next interval.
- Current/start state is then mutable by same-step residue/management logic before later chemistry reads it.
- Potential-pass result/rate values are provisional.
- Actual-pass final result is the end generation for the interval.
- Final-run serialization reads final result generation because no following `Init` exists.

A modern transaction model need not copy this storage mechanism literally, but it must expose equivalent read generations at the points where legacy uses them.

### Event boundaries

- Management packet selection uses `(t0,t1]`.
- Annual harvest/root-residue selection uses `[t0,t1)`.
- Same-row material addition precedes ploughing.
- Crop start and end identity may differ within one interval.
- A step ending on the year boundary closes prior-year output before the following step performs new-year start logic.
- Report-period crossing has its own half-step rule and is not a physical state boundary.

### Process partial order

The source-equivalence baseline includes:

`management/residues -> demand -> potential process pass -> aeration -> actual process pass -> actual NH4 transport -> denitrification/NO3 source construction -> NO3 transport -> P solve -> crop integration -> balance observation -> reporting`.

The exact detailed call graph is in `PROCESS_ORDER_GRAPH.md`. A future TIME scheduler may encode a partial order rather than one monolithic sequence only if all source-observed dependencies remain satisfied.

### Mixed-generation and layer dependencies

- `Resp_miner` availability logic can read previous-step neighbour `Conh/Copo` values.
- Generic solute transport propagates same-step `Av*` values in `Sqnu` order.
- P processing also follows `Sqnu` and couples transport with phase processes per layer.

There is no valid global rule that every process reads either only accepted state or only the latest trial state.

### Observation boundaries

- `Outbal_calc` observes a completed physical interval.
- `Outbal_write` report reset/rollover is diagnostic continuation, not physical commit.
- Potential-pass observations must not become committed physical transfers.

## 3. Future transaction policy not defined by legacy

The following are architecture decisions that the future TIME gate must make explicitly. TS01 provides constraints but not answers.

### Explicit accept/reject

Revision 53 has no generic transaction object or rollback protocol. A future TIME contract must define:

- when a trial starts;
- what state snapshot is immutable;
- what trial-local state may change;
- what constitutes acceptance;
- what is discarded on rejection;
- how transfer journals and diagnostics behave on reject.

### Retry and substep policy

Legacy source contains local process iterations and sequential layer traversal, but no generic retry controller. TIME must define whether a rejected interval is retried at the same `t1`, a shorter interval, revised external frames or another policy. This cannot be inferred from TS01.

### Coupled acceptance barrier

ARCH07 requires mutually corresponding accepted generations for ANIMO and external owners. TIME must define the logical barrier/protocol without allowing an external participant to advance irreversibly before the group is accepted.

### Canonical time identity

Revision 53 uses `Juda`, `Juda-St`, `Tiyr`, `Tito` and calendar conversion routines with process-specific predicates. TIME must define a canonical representation for interval endpoints, calendar identity and comparison semantics. It must be able to reproduce legacy event classification exactly where compatibility is required.

### Checkpoint timing

Legacy restart-style output is end-of-run only. TIME must define which accepted boundaries are checkpointable and whether mid-trial checkpointing is prohibited or separately specified.

### Runtime topology transition

TS01 does not qualify changing active feature topology, layer geometry, crop ownership mode or site cardinality during a trial. TIME must fail closed unless another admitted transition contract exists.

## 4. Open admission questions

These remain outside TS01 source authority:

- whether any legacy event endpoint asymmetry is scientifically intentional or should be corrected;
- whether process-order changes are scientifically/numerically equivalent;
- whether `Sqnu`-ordered algorithms may be safely parallelized after reformulation;
- whether exact legacy `Output_Init` compatibility requires reproducing the crop-P clamp;
- whether omitted restart cursors can always be reconstructed exactly from input and time;
- numerical tolerances for state/output/restart comparison;
- corrected behaviour for TCD-014, TCD-015, TCD-016, TCD-019, TCD-023, TCD-024, TCD-025 and TCD-029;
- full GHG and macropore temporal contracts where feature qualification remains incomplete.

## 5. Minimum TIME-gate acceptance evidence

TS01 recommends that a future TIME workunit fail closed unless it can point to all applicable evidence classes below:

- canonical state ownership admitted or explicitly identified as still candidate;
- exact source-order/generation coverage against `TS01_SCHEDULER_SENTINELS.csv`;
- explicit event-class endpoint policy with compatibility disposition;
- explicit accepted/trial/reject/retry contract;
- explicit external-frame generation/interval binding;
- explicit reporting versus physical-commit boundary;
- split-run and event-boundary behavioural tests once independent B2/reference evidence exists;
- NQ-controlled comparison policy for any non-bitwise numerical comparisons;
- B3/scientific admission for intentional source-observed behavioural differences.

Absence of B2 evidence must remain visible. Passing static/synthetic sentinels does not by itself admit TIME.

## 6. Minimum scheduler trace for qualification

A diagnostic scheduler trace should be able to record, for each interval and relevant layer/process:

- `interval_id`, `t0`, `t1`, calendar identity;
- accepted generation ID and trial ID;
- event IDs selected and the predicate that selected them;
- process boundary ID;
- state generation read;
- state generation written;
- `Sqnu` traversal index where relevant;
- provisional versus physical event classification;
- external hydrology/crop frame IDs;
- result/accept/reject outcome;
- report-period close/reset separately from physical acceptance.

The trace is diagnostic evidence, not physical continuation state.

## 7. Required negative cases

A future TIME candidate must reject or flag at least:

- a management event classified by the harvest endpoint rule or vice versa;
- ploughing scheduled before the same-row addition;
- downstream chemistry reading pre-management state when legacy sees post-management state;
- `Resp_miner` receiving same-step neighbour values where previous-step values are required;
- layer solver execution in an order inconsistent with `Sqnu` for source-equivalence mode;
- committed physical event emission from the potential pass;
- report reset being interpreted as physical acceptance;
- stale/mismatched external interval frame;
- replay or omission of an event across restart;
- final serialization from stale start/current state;
- rejected trial events appearing in committed physical ledgers.

## 8. Handoff to architecture governance

ARCHG01 explicitly deferred process order, accepted-versus-mutated reads, substep/retry and time representation to TS01. Those source-bound parts are now reconstructed and machine-readable through the scheduler sentinel matrix.

A future architecture-governance consolidation should therefore treat TS01 as an input constraint on the TIME design, not as permission to claim that ARCH01's atomic transaction model already matches legacy literally.

## 9. Qualification boundary

This handoff adds no canonical TIME decision. Production migration remains `NOT_ADMITTED`. No source, testcase or production code is changed.
