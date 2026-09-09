# ANIMO-TIME01 retry, reject and checkpoint policy

Status: `CANDIDATE_CONTRACT_ONLY`.

## 1. Scope

This document defines candidate transaction semantics for failed trials, retries and checkpoint boundaries. Revision 53 does not implement a generic retry/rollback controller, so these rules are future architecture policy constrained by TS01, ARCH01, ARCH02 and ARCH07.

## 2. Reject invariant

Rejecting a trial SHALL leave all accepted physical owner generations unchanged.

For ANIMO this means:

- accepted physical state at `t0` is unchanged;
- no trial-local physical transfer event becomes committed;
- trial scratch and provisional results are discarded;
- trial-local mutated event state is discarded;
- diagnostic records may survive only when explicitly tagged nonphysical and rejected.

For external owners the same logical rule applies: a rejected ANIMO/coupled trial cannot force hydrology or external crop accepted state to advance.

## 3. Retry identity

Every retry receives a new `trial_id`.

### Retry with unchanged interval

If `t0`, `t1`, accepted generation, configuration/layout and all required immutable input frames remain unchanged, the same `interval_id` may be reused with a new trial attempt.

This supports replay from an unchanged accepted snapshot.

### Retry with changed external frame

A changed hydrology/crop payload requires a new frame identity. The new trial explicitly binds that frame before execution.

The old frame remains immutable and auditable.

### Retry with changed `t1`

A shorter/longer proposed interval is a new interval, not merely another attempt. It requires:

- new `interval_id`;
- newly valid interval-scoped forcing/exchange frames;
- re-evaluation of event membership under the relevant endpoint class;
- a fresh `trial_id`.

Event membership MUST NOT be carried forward from the rejected longer/shorter interval without reclassification.

## 4. Retry causes

TIME01 does not prescribe which numerical/scientific conditions trigger retry. A future implementation may request retry because of:

- solver nonconvergence;
- conservation acceptance failure;
- invalid/stale external frame;
- coupled participant failure;
- explicit orchestrator policy.

The acceptance criterion itself belongs to the relevant numerical, conservation, exchange or scientific gate.

## 5. Process-local iteration versus interval retry

Internal loops such as the source-observed `Resp_miner` recalculation are process-local algorithm steps. They do not create new `trial_id`s and do not reset the whole interval.

A generic interval retry restarts from accepted state and creates a new `trial_id`.

A future substep solver must likewise distinguish:

- algorithmic substeps internal to one trial;
- model intervals that have accepted-state meaning.

No internal substep may independently commit physical state unless a later canonical TIME contract explicitly promotes substeps to accepted intervals.

## 6. Coupled acceptance barrier

A coupled interval reaches local `TRIAL_READY` independently for each participant, but no participant may irreversibly publish its next accepted generation until the group acceptance condition is satisfied.

The candidate contract requires the following observable properties without prescribing a particular distributed commit algorithm:

1. all participants refer to the same admitted `t0 -> t1` interval;
2. all required trial results are ready;
3. any required conservation/numerical/coupling checks have passed;
4. no accepted owner generation has advanced early;
5. group accept advances mutually corresponding owner generations;
6. group reject leaves all accepted generations unchanged.

TIME01 does not require database-style two-phase commit. It requires equivalent atomic semantics at the model contract boundary.

## 7. Checkpointable boundary

A portable physical checkpoint may be created only while the model is in accepted-idle state, after a completed accepted transaction.

TIME01 therefore forbids ordinary portable checkpoints from:

- `TRIAL_BOUND`;
- `TRIAL_EXECUTING`;
- `TRIAL_READY` before accept;
- rejected trial scratch;
- provisional/potential-pass state.

This is consistent with ARCH02's accepted-state-only checkpoint model.

## 8. Checkpoint payload classes

TIME01 recognizes two different continuation promises.

### Physical continuation checkpoint

Contains accepted ANIMO-owned physical continuation state and the identities/metadata required to restore and bind external owners.

It excludes report accumulators as physical state.

### Diagnostic continuation payload

Optional and separate. Required if a restart promises identical mid-report-period cumulative outputs/diagnostics.

If diagnostic continuation is omitted, the checkpoint contract must explicitly limit the output-equivalence promise or restrict checkpoint placement to an admitted report boundary.

## 9. Restore protocol temporal requirements

Before the next trial after restore:

1. validate checkpoint identity/schema/configuration/layout;
2. establish the restored accepted generation at the checkpoint time;
3. restore or bind external owner accepted generations at that same time;
4. restore diagnostic continuation when required;
5. reconstruct derived views;
6. establish event schedule identity and continuation semantics;
7. create a fresh interval/trial binding for the next step.

No restored trial scratch or stale trial journal is reused.

## 10. Event continuation across restart

Revision-53 `INITIAL.OUT` does not by itself prove exact management cursor continuation. TIME01 therefore requires one of two future mechanisms:

- serialize explicit event schedule/cursor continuation state; or
- deterministically reconstruct selection from immutable absolute event schedule plus accepted time and prove equivalence.

Until independent B2 split-run tests pass, neither mechanism is declared historically equivalent.

Required behavioural sentinels remain:

- clean non-event split;
- split immediately before/after management event;
- split around crop/harvest transition;
- split at year boundary;
- split inside a reporting period with physical and diagnostic equivalence tested separately.

## 11. Final-state serialization

For source compatibility, a legacy-style final export must derive from the completed actual result generation, not a stale start snapshot.

A future canonical checkpoint writer SHALL be side-effect free with respect to accepted physical state. If exact legacy restart material requires reproducing a serializer transformation such as the observed crop-P clamp, it must be represented as an explicit compatibility export transformation and not hidden mutation of accepted state.

## 12. Reporting after rejected attempts

A rejected attempt may emit diagnostic trace records, solver statistics or rejection reasons. These records must carry `trial_id` and rejected status.

They must not:

- alter committed mass ledgers;
- be counted as accepted physical process outputs;
- advance report-period physical begin/end storage;
- overwrite accepted-run outputs without explicit diagnostic labeling.

## 13. Runtime topology transitions

Feature topology, geometry, site cardinality and ownership mode are immutable within a trial.

A topology transition may occur only at an accepted boundary under a separately admitted transition/migration contract. If no such contract exists, the transition request is rejected before beginning the next trial.

## 14. Qualification evidence required later

Static coherence of this policy is not sufficient. Later admission requires at least:

- runtime reject-atomicity evidence;
- retry/replay evidence;
- coupled group accept/reject evidence;
- checkpoint/restore owner-binding evidence;
- independent reference split-run evidence where historical equivalence is claimed;
- numerical comparison policy from the relevant NQ gate;
- scientific admission for intentional legacy behaviour changes.

## 15. Qualification boundary

TIME01 does not execute these behavioural tests and does not admit canonical restart or TIME semantics. It defines the candidate rules against which future runtime implementations can be qualified.
