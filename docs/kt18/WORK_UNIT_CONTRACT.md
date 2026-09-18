# ANIMO-KT18 Work Unit Contract

Workunit: `ANIMO-KT18 - Multi-Packet Hydrology Provider to Accepted Application Composition Qualification`.

Execution discipline: `RECONCILE -> ARCHITECTURE BINDING -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT18 closes the application-composition gap left by KT16/RG07: the bounded accepted application no longer receives a hydrology packet selected manually by the caller.

KT18 composes the admitted KT11 multi-packet provider with the qualified KT15A accepted application runtime.

The bounded path is:

`KT11 immutable packet collection -> exact interval-key selection -> selected packet copy -> KT15A/KT15 application interval -> KT14B/KT13A science composition -> atomic accepted publication`.

## Authorities

Current program authority:

`ANIMO-RG07@c60dd36a38a2030e4f4ac1925f95b2966a6d1c87`.

Central admitted provider authority:

`ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480`.

Accepted application candidate:

`ANIMO-KT15A@2279a961459211e03550dfda4af09ab4f7f6b9a3`.

Checkpoint/integrity work is ownership-disjoint. KT18 does not depend on KT17 semantics even though the branch inherits the post-RG07 repository state.

## Read-only KT11 selection seam

The admitted KT11 implementation keeps provider packet storage private. Its existing transaction-client API proves interval-key selection by delegating into KT06, but it does not return the selected complete `hydrology_step_t` to an application orchestrator.

KT18 adds:

`select_multi_packet_hydrology_step_copy`.

This procedure uses the same bounded provider identity:

- runtime calendar must match;
- whole-day origin and endpoint only;
- endpoint must be after origin;
- exact producer-day offset;
- exact integer runtime duration;
- exact pair `(producer endpoint day, producer step duration)`;
- zero matches fail closed;
- ambiguity fails closed.

The returned packet is a copy. Mutation of that returned copy cannot mutate provider-owned forcing.

This is an introspection/composition extension on the KT18 branch only. It does not mutate the centrally admitted KT11-A1 authority.

KT11 regression tests are rerun.

## Application composition

`execute_provider_backed_application_interval`:

1. validates the current accepted KT15A application state;
2. obtains its accepted origin time;
3. asks KT11 for the exact selected packet copy for `[origin, endpoint]`;
4. passes only that packet to `execute_kt15_atomic_interval`;
5. publishes success only if the KT15 application interval commits.

KT15 remains the owner of science plus continuation atomicity.

KT06 remains nested in the downstream science path and revalidates producer/runtime identity against the immutable application configuration. Therefore a provider with a different day offset may select a packet under its own configuration but the application still rejects that packet before publication.

## Atomicity

Provider selection is read-only.

If selection fails, the accepted application state is unchanged.

If provider selection succeeds but downstream application binding or science fails, KT15 atomicity leaves the external accepted application state unchanged.

## Qualification cases

The executable harness covers:

- two provider-backed accepted intervals;
- provider packets stored out of chronological order;
- missing packet failure before application execution;
- provider/application day-offset disagreement rejected downstream without publication;
- repeated selection after mutating an earlier returned packet copy, proving the provider owns immutable forcing.

KT11 and KT15 regression harnesses are rerun.

## Scope

KT18 is bounded to the already qualified whole-day KT11/KT15A envelope.

It does not add:

- fractional/subday provider selection;
- runtime SWATRE.UNF decoding;
- packet generation;
- packet prefetch/cache policy;
- retry/timestep policy;
- full 1800-packet production execution;
- canonical external forcing admission;
- canonical application admission.

## Governance

This is a cross-module provider/application composition and is conservatively GOV04 Tier D.

Same-agent review is process assurance only:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Genuine independent Tier D review remains required before admission.

## Hard boundaries

No production source.
No central KT11-A1 mutation/promotion.
No KT15A central admission.
No science change.
No B3 mutation.
No canonical forcing/application state.
No TB7.
No B4.
No production.
No Status A or AA.
