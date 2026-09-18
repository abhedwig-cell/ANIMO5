# ANIMO-KT11 Same-Agent Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Frozen KT11 candidate reviewed:

`843ac357f8b86f84131ddc08bf2097bb5af4e080`

Frozen provider implementation blob:

`prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90`
= `a41d0f61da6dd30a18dbfadbe4b29b00259fa41e`

Exact-head qualification run:

`35351056242 -> SUCCESS`

The workflow also reran frozen KT02, KT05 and KT06 qualification tests before
executing the KT11 harness.

## Candidate claim

> An immutable collection of complete KT05 explicit hydrology packets can
> deterministically select exactly one packet from a bounded whole-day KT02
> requested interval, remain stateless across repeated requests, fail closed on
> missing or duplicate interval keys, and delegate the selected packet through
> admitted KT06 without changing KT02 time, accepted-state or publication
> ownership.

This review addresses only that runtime/provider claim.

## Adversarial questions

### 1. Is the lookup key explicit and deterministic?

**PASS.**

Selection is keyed by the pair `(producer_endpoint_day, producer_step_days)`,
after both REAL64 values have been converted under the same bounded exact
integer policy used by KT06.

Duplicate exact pairs fail during provider initialization. Storage order is not
consulted for semantics. A dedicated test proves that the same producer endpoint
with two different durations remains two distinct keys selected by the
corresponding KT02 origin/end interval.

### 2. Can caller-owned packet mutation change provider behaviour after initialization?

**PASS.**

The provider performs intrinsic derived-type assignment into a private internal
packet array. For allocatable components this creates provider-owned copies.
The harness now mutates schema, endpoint, duration, scalar forcing and an
allocated vector in the caller-owned source after initialization. The original
runtime interval still binds successfully through the provider.

The provider type exposes no public component through which those internal
packets or keys can subsequently be mutated.

### 3. Is packet selection stateful or consumptive?

**PASS.**

There is no selection cursor, consumed flag or mutable packet index. Every
attempt derives its lookup key only from the current KT02 origin/end interval
plus the configured producer-day offset.

Repeated execution of the same interval returns a valid candidate twice. No
forcing packet is consumed by selection.

Here, "forcing lifecycle" is deliberately bounded to immutable availability and
repeatable interval-key selection. Dynamic loading, cache eviction, streaming
or mutable provider lifecycle is not claimed.

### 4. Does a missing packet leak a partially completed multi-step interval?

**PASS.**

The missing-middle-packet test reaches one successful private KT02 working
commit, then fails on the second provider lookup. The externally accepted
generation, time and payload remain at the original interval origin.

Atomic external publication therefore remains KT02-owned.

### 5. Does KT11 bypass or duplicate KT06 binding semantics?

**PASS.**

After exact packet lookup, KT11 constructs a local frozen KT06 probe client with
the selected complete packet, the same calendar binding and the same
producer-day offset, then delegates the attempt.

KT11 does not create its own accepted payload semantics, publication path or
scientific admissibility rule.

### 6. Does forcing enter accepted continuation state?

**PASS.**

The selected packet remains inside the client/provider side. Frozen KT06 returns
the unchanged synthetic probe-state token. The multi-step tests confirm the
accepted payload token remains unchanged while accepted time advances only
through KT02 commits.

### 7. Are sparse collections being mistaken for complete producer-sequence coverage?

**PASS, with an explicit boundary.**

The provider contract intentionally allows sparse and unordered immutable
collections. Missing coverage is observable and fails closed.

KT08 proves the pinned LWKM file has a gap-free 1800-packet temporal sequence,
but KT11 does not materialize all 1800 complete payloads. KT09 contributes eight
representative complete real-derived packets only. No full-sequence runtime
payload claim is made.

### 8. Do KT08 or KT09 become runtime authority?

**PASS.**

Their exact evidence blobs are transplanted and machine-pinned. They remain B1
supplemental producer/contact evidence. The runtime authority is KT06-A1 plus
the new KT11 provider candidate.

### 9. Does calendar or time ownership drift from KT06?

**PASS within the inherited bounded envelope.**

KT11 requires the configured runtime calendar id, exact whole-day KT02
coordinates, a nonnegative integer producer-day offset and exact bounded
producer metadata. It performs no generic calendar conversion.

The calendar relation remains a composition assertion, not producer-carried
calendar semantics.

### 10. Are retry or timestep-selection semantics introduced?

**PASS as an exclusion.**

KT11 chooses forcing for the interval presented by KT02. It does not decide the
interval, retry budget, retry endpoint or timestep policy. Because lookup is
stateless, a repeated request can recover the same forcing, but KT11 does not
qualify the policy that causes such a request.

### 11. Are invalid providers observably safe?

**PASS.**

Failed initialization never sets `configured`. The readiness query therefore
fails closed, and the public packet-count helper now returns zero for a provider
that failed initialization rather than exposing a partially allocated internal
array as a usable count.

## Evidence execution

Exact-head run `35351056242` succeeded with:

- frozen KT02 qualification tests;
- frozen KT05 compiled adapter tests;
- frozen KT06 runtime-binding tests;
- KT11 upstream evidence identity checks;
- KT11 compiled provider/lifecycle tests;
- KT11 checkpoint JSON validation.

The earlier run `35350489308` failed only because the Python evidence test
incorrectly compared a raw-file SHA1 with a Git blob SHA. That test defect was
removed. Subsequent runs `35350629856`, `35350953259` and the final hardened
run `35351056242` passed. The original failure did not reveal a runtime
semantic defect.

## Findings

No open material finding was identified against the bounded KT11 claim.

Non-material retained limitations:

1. complete 1800-packet runtime payload coverage is not demonstrated;
2. provider completeness is not required, by design; absent intervals fail closed;
3. the configured calendar relation is not producer-carried provenance;
4. detailed provider failure reasons are collapsed by KT02 to
   `CLIENT_ATTEMPT_FAILED` at the public interval boundary;
5. no retry/timestep policy, scientific execution or production composition is
   admitted by this workunit.

## Same-agent verdict

`PASS_BOUNDED_MULTI_PACKET_PROVIDER_CANDIDATE_INDEPENDENT_TIER_C_REVIEW_REQUIRED`

This is **not** a GOV04 Tier C independent-review result and does not admit
KT11. A genuinely separate second-line review remains required.
