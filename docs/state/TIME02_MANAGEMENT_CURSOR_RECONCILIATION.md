# ANIMO-STATEQ01 TIME02 management-cursor reconciliation

Status: `CANDIDATE_CROSS_STREAM_RECONCILIATION_SYNTHETIC_RC_R2_EXECUTION_PENDING`

Canonical STATE admission: `NOT_ADMITTED`

Canonical TIME admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Purpose

This note reconciles STATEQ01 management continuation with the concrete TIME02 candidate without promoting either stream beyond its admitted evidence level.

Pinned TIME02 input:

- branch: `work/animo-time02-concrete-time-coordinate`;
- head: `b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8`;
- decision: `QUALIFIED_CONCRETE_TIME_REPRESENTATION_CANDIDATE_CANONICAL_TIME_ADMISSION_PENDING`;
- calendar contract: `ANIMO_PG_86400_NOLEAPSECONDS_V1`;
- canonical comparison candidate: normalized exact rational civil-day coordinate;
- floating tolerance in event identity: forbidden.

This reconciliation consumes TIME02 as candidate contract evidence only. It does not claim canonical TIME is admitted.

## Management continuation contract

STATEQ01 has already source-qualified that source-equivalent checkpoint continuation cannot generally be reconstructed from accepted time plus schedule identity alone. The candidate checkpoint therefore retains:

```text
management_schedule_identity
next_management_event_id
accepted_time
```

The next event boundary is not a second mutable checkpoint owner. It is resolved from the exact normalized schedule record identified by `next_management_event_id` under the pinned TIME02 calendar/time contract.

A raw legacy file position remains adapter implementation state and is not canonical continuation.

## Exact endpoint rule

For management additions, source-equivalent interval membership remains:

```text
t0 < E <= t1
```

All comparisons in the qualification harness use exact rational arithmetic. No epsilon, ULP window or floating tolerance is allowed.

At an exact split boundary `S`:

- a management event with `E=S` belongs to the interval ending at `S`;
- after that interval is accepted, the checkpoint cursor must already identify the following management record;
- restore at `S` must restore that explicit following event identity;
- the event at `S` must not be replayed in the interval starting at `S`.

This is exactly the restart consequence already stated by TIME02 and is now made executable inside STATEQ01.

## Qualification-only executable harness

`tools/stateq01/management_cursor_exact_time_harness.py` encodes only the continuation contract required for RC-R2. It is deliberately not a scheduler implementation and contains no ANIMO process physics.

The harness enforces:

- exact TIME02 rational coordinate normalization;
- exact `t0 < E <= t1` management membership;
- explicit immutable schedule identity;
- explicit next-event identity in every restart payload;
- next-event boundary derived from the bound schedule, not serialized as an independent owner;
- fail-closed restore on missing cursor identity, schedule mismatch or unknown event identity;
- no float coordinate as canonical time identity;
- no reconstruction of the cursor by searching for the first event after accepted time.

The source-style harness considers the explicit current management cursor once per accepted interval. It does not broaden revision-53 behaviour into a general multi-event queue semantics.

## RC-R2 synthetic vector

The primary vector places `ADD-001` exactly at split boundary `S` and `ADD-002` strictly after `S`.

Uninterrupted path:

```text
[t0,S]  -> consume ADD-001
[S,t2]  -> consume ADD-002
```

Split path:

```text
[t0,S]  -> consume ADD-001
checkpoint at S with next_event_id=ADD-002
restore at S
[S,t2]  -> consume ADD-002
```

Pass requires identical event sequence and explicit proof that `ADD-001` is absent from the post-restore interval.

Additional sentinels exercise exact just-before/just-after coordinates, schedule mismatch, missing cursor identity, unknown cursor identity, absence of duplicated next-event time in the checkpoint, non-reduced rational input and attempted floating canonical identity.

## Evidence boundary

A passing harness establishes only:

`RC_R2_CANDIDATE_CONTRACT_SYNTHETIC_NO_REPLAY_NO_SKIP`

It does not establish:

- historical B2 split-run equivalence;
- revision-53 executable restart equivalence;
- canonical TIME admission;
- canonical STATE admission;
- full `CORE_CNP_SUBSURFACE_ONLY` admission;
- production scheduler or checkpoint implementation.

The natural supplied testbank still lacks a profile-clean `CORE_CNP_SUBSURFACE_ONLY` case suitable for the full RC-R1 through RC-R12 campaign. `RuurloGrass` satisfies the strict zero-surface envelope but uses the internal crop ownership route, so using it as a no-crop core case would contaminate the qualification scope.

## Consequence for STATEQ01

Once the synthetic RC-R2 harness passes, the management cursor blocker can be narrowed from "canonical TIME integration not yet represented" to two distinct remaining items:

1. canonical TIME admission remains external to STATEQ01;
2. behavioural split-run qualification on an admitted/profile-clean executable case remains open.

The explicit cursor requirement itself remains unchanged.
