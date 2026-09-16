# ANIMO-KT01 Nonproduction Runtime Substrate Contract

## Status boundary

This contract applies only to `prototype/kt01/`. It is a nonproduction research prototype and does not open B4, does not modify the ANIMO production tree, does not admit canonical TIME, and does not admit any ANIMO scientific process.

The prototype is ANIMO-native source. It has no runtime dependency on the SWAP5 repository and creates no shared cross-model library.

## Reused mechanics

The prototype materializes only the reuse classes allowed by `SWAP5_RUNTIME_REUSE_MATRIX.csv`:

- `PORT_WITH_ANIMO_ADAPTATION`: atomic accepted-state publication with lineage and generation checks; committed-only checkpoint mechanics; private interval working state with final publication only after exact completion.
- `DESIGN_ONLY`: neutral runtime contract separation; clone/retry isolation pattern; worker-owned scratch reset/isolation.
- `DIRECT_PORT`: none.
- `REJECT`: floating time identity/progress, SWAP retry and step-doubling policy, single-water acceptance, hydraulic/solver payload, SWAP calendar/file/state layout assumptions.

## Time

`TimeCoordinate` is a bounded prototype realization of the TIME02 candidate fields `calendar_contract_id`, `day_index`, `subday_numerator`, and `subday_denominator`. Fractions are normalized exactly. Equality and ordering use integer-only exact comparison. Ratio comparison uses Euclidean continued-fraction comparison and does not use unchecked cross products. Arithmetic detects overflow and fails closed. No fixed global timestep quantum is introduced.

This is not canonical TIME admission.

## Transaction model

`AcceptedState` is authoritative physical state. A `TrialState` is created from one exact accepted origin and is private until commit. A `TrialResult` carries the candidate endpoint, trial-local transfer journal, supplied conservation assessments, diagnostics and provenance.

Commit checks exact lineage, generation and origin-time identity, forward endpoint progress, and supplied acceptance. Publication is built in a temporary next state and assigned to accepted state only after all checks pass. Rejection leaves accepted state unchanged and trial events remain uncommitted.

No scientific process ordering or process equations exist in KT01.

## Conservation acceptance boundary

The runtime accepts a collection of typed `ConservationAssessment` values with explicit quantity and control-volume identity. A commit requires every supplied assessment to be complete and admissible. The substrate does not calculate or choose a scientific tolerance. It does not create balancing mass, balancing flux or corrective events.

The synthetic tests use exact Boolean pass/fail assessments only. They do not define the future ANIMO scientific quantity registry.

## Persistence and restart

`AcceptedCheckpoint` can be constructed only from `AcceptedState`. It contains accepted continuation state plus checkpoint schema, state layout, configuration, feature layout, lineage, generation and exact accepted time. It excludes trial state, uncommitted journal events, worker/process scratch and diagnostics.

Restore fails closed on schema, state-layout, configuration or feature-layout mismatch. This demonstrates the ARCH02/04/06 mechanics only. It is not a historical ANIMO restart equivalence claim and creates no B2 evidence.

## Worker context

The minimal worker context holds only worker/job ownership, logical-model/attempt binding, synthetic scratch and attempt-local diagnostic counters. Preparing an attempt resets scratch and attempt diagnostics. No worker payload can become accepted physical state or checkpoint state.

## Interval runtime

The interval runtime clones the externally accepted origin into a private working accepted state. It consumes caller-supplied synthetic attempt plans, performs transaction checks against the private working origin, and publishes externally only after the exact requested target coordinate is reached.

It fails closed on invalid interval ordering, zero or backward progress, endpoint beyond target, failed acceptance when retry is not permitted, attempt exhaustion, trace exhaustion, unrepresentable synthetic state arithmetic and incomplete interval completion. Retry policy is supplied by the synthetic test plan. No scientific timestep, subdivision, step-doubling or solver fallback policy is defined.

## Explicit non-authority

A passing KT01 test demonstrates only the bounded mechanics above. It does not transfer SWAP5 Status-A authority, does not qualify ANIMO process semantics, does not change B3, does not open B4 or production, and does not make Status A or Status AA claims for ANIMO5.
