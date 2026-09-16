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

The explicit KT01 representation envelope is:

- all integer coordinate fields use signed Fortran `int64` storage;
- `day_index` may occupy the `int64` range, subject to fail-closed whole-day carry during arithmetic;
- `subday_denominator` is an `int64` value greater than zero;
- constructor and arithmetic numerators are nonnegative `int64` values and normalize to `0 <= numerator < denominator` with `gcd=1`;
- arithmetic exposed by KT01 is forward nonnegative rational addition only; any intermediate multiply, add, denominator construction or whole-day carry that is not representable in `int64` fails closed;
- exact ratio comparison does not multiply denominators and is defined for every valid coordinate inside this bounded envelope;
- `calendar_contract_id` is an opaque nonempty identifier of at most 48 characters; the prototype serialization delimiter `|` is excluded so serialization cannot become ambiguous;
- cross-calendar ordering/equality fails closed rather than converting calendars implicitly.

TIME02 defines mathematical-integer semantics beyond this bounded storage backend. KT01 does not claim arbitrary-precision realization. Values outside the envelope are rejected rather than rounded, truncated or projected through REAL.

The prototype pipe-delimited serializer is a bounded executable round-trip harness for the four TIME02 identity fields. It is deliberately **not** claimed to be the TIME02 canonical JSON interchange form. A later admitted implementation must either implement the TIME02 canonical serialization contract or qualify an explicit adapter. This distinction does not change time identity or ordering semantics.

This is not canonical TIME admission.

## Transaction model

`AcceptedState` is authoritative physical state. It contains lineage, generation, exact accepted time and the synthetic physical payload only. It does not contain committed transfer/event history.

A `TrialState` is created from one exact accepted origin and is private until commit. Its `TransferJournal` is attempt-local. A `TrialResult` carries the candidate endpoint, trial-local transfer journal, supplied conservation assessments, diagnostics and explicit provenance.

`CommittedEventLedger` is a separate publication product. It is not physical accepted state and is not restart continuation state. Transfer direction is represented by `source_id -> sink_id`; event amounts are therefore non-negative, and a negative directed amount is rejected before journal mutation.

Commit checks a valid accepted origin, nonempty trial provenance, exact lineage, generation and origin-time identity, forward endpoint progress, supplied acceptance and event-ledger capacity/validity. It first constructs candidate physical and ledger postimages. Only after all checks succeed are both outputs assigned. Rejection leaves accepted physical state and the external committed event ledger unchanged.

No scientific process ordering or process equations exist in KT01.

## Conservation acceptance boundary

The runtime accepts a collection of typed `ConservationAssessment` values with explicit quantity and control-volume identity. A commit requires every supplied assessment to be complete and admissible. The substrate does not calculate or choose a scientific tolerance. It does not create balancing mass, balancing flux or corrective events.

The synthetic tests use exact Boolean pass/fail assessments only. They do not define the future ANIMO scientific quantity registry.

## Persistence and restart

`AcceptedCheckpoint` is constructed through the KT01 checkpoint constructor from `AcceptedState`. Its components are private outside the persistence module. It contains accepted physical continuation state plus checkpoint schema, state layout, configuration, feature layout, lineage, generation and exact accepted time. It contains no trial state, transfer journal, committed event ledger, worker/process scratch or diagnostics.

Fixed-width compatibility identifiers supplied to the constructor or restore boundary must be nonempty and at most 48 characters; overlength identities fail closed rather than truncate. Restore fails closed on schema, state-layout, configuration or feature-layout mismatch and on invalid accepted provenance or time.

The executable restart control compares an uninterrupted two-segment synthetic continuation with a run split at an accepted checkpoint. Final exact time, lineage/generation and synthetic physical storage must match exactly. The separately published event ledger is deliberately retained outside the physical checkpoint and compared separately after continuation. This demonstrates restart mechanics only. It is not a historical ANIMO restart equivalence claim and creates no B2 evidence.

## Worker context

The minimal worker context holds only worker/job ownership, logical-model/attempt binding, synthetic scratch and attempt-local diagnostic counters. Preparing an attempt resets scratch and attempt diagnostics. External identity arguments are nonempty and at most 48 characters so worker/model/attempt identifiers cannot silently truncate. No worker payload can become accepted physical state or checkpoint state.

## Interval runtime

The interval runtime clones the externally accepted physical origin and the external committed event ledger into private working values. Internal accepted substeps update only those private values. Accepted substep events accumulate in the private event ledger. The runtime publishes both physical accepted state and the separately owned event ledger only after the exact requested target coordinate is reached.

If a later attempt fails, the attempt budget is exhausted, progress is invalid, or the requested interval otherwise remains incomplete, neither the privately advanced physical state nor accepted-event progress is externally published.

The runtime fails closed on invalid interval ordering, zero or backward progress, endpoint beyond target, failed acceptance when retry is not permitted, attempt exhaustion, trace exhaustion, unrepresentable synthetic state arithmetic, invalid event construction and incomplete interval completion. Retry policy is supplied by the synthetic test plan. No scientific timestep, subdivision, step-doubling or solver fallback policy is defined.

## Explicit non-authority

A passing KT01 test demonstrates only the bounded mechanics above. It does not transfer SWAP5 Status-A authority, does not qualify ANIMO process semantics, does not change B3, does not open B4 or production, and does not make Status A or Status AA claims for ANIMO5.
