# ANIMO-STATEQ01 restricted-core application-envelope qualification specification

Status: `CANDIDATE_TEST_SPEC_NOT_B3_ADMISSION`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Purpose

This specification defines what must be proven before `CORE_CNP_SUBSURFACE_ONLY` may be used as the first executable checkpoint-admission candidate. It does not create a production feature switch and does not change revision-53 physics.

The restricted profile exists only to isolate a state-complete application envelope that excludes the unresolved layer-0 aqueous continuation seam. It is valid only if that exclusion is explicit, machine-checkable and fail-closed.

## Envelope invariant

For every accepted interval and every trial that could be committed under `CORE_CNP_SUBSURFACE_ONLY`:

```text
no layer-0 aqueous C/N/P solute coordinate may become physically active
```

This is stronger than checking that the initial layer-0 concentration is zero. It requires proving that the hydrology/event/configuration combination cannot activate layer-0 aqueous storage or route solute mass through that compartment.

The profile must fail before physical mutation if the invariant cannot be established.

## Evidence needed to define the guard

The eventual guard must be source-bound to the exact conditions that activate layer-0 aqueous transport/storage in revision 53. STATEQ01 does not guess those predicates.

Qualification must determine at minimum:

1. which hydrology state variables make layer 0 physically present;
2. whether ponding, surface water depth, management addition water or boundary routing can activate it;
3. whether `Con*top` addition reservoirs can feed layer 0 even when initial layer-0 storage is absent;
4. whether rainfall/infiltration or same-step management can create a transient layer-0 aqueous state inside an otherwise dry accepted boundary;
5. whether P, DOM/DON/DOP and mineral N use identical activation predicates;
6. whether any option combination bypasses the ordinary layer-0 activation path.

Until these predicates are source-qualified, `CORE_CNP_SUBSURFACE_ONLY` is a readiness candidate only, not an executable admitted profile.

## Fail-closed contract

An implementation candidate may enter the restricted profile only after configuration normalization and external hydrology binding establish the envelope invariant.

The following are hard failures:

- unknown or unsupported surface-hydrology option;
- missing external hydrology fields needed to determine layer-0 activation;
- accepted ponding/surface-water state inconsistent with the restricted envelope;
- a management event capable of creating an aqueous surface compartment under the admitted legacy schedule;
- a trial-time transition into layer-0 aqueous activation;
- an attempt to continue by discarding or synthesizing layer-0 mass.

A trial that would violate the envelope is rejected before it can become the next accepted generation. The run must then either terminate or move through a separately admitted profile-transition contract. STATEQ01 defines no such transition contract.

## Restricted-core split-run qualification matrix

The first split-run qualification should use only cases proven to remain inside the envelope.

Required test classes:

| ID | Boundary | Required assertion |
|---|---|---|
| RC-R1 | clean non-event accepted boundary | uninterrupted and split trajectories have equivalent continuation-critical state and event sequence |
| RC-R2 | immediately before and after management event that does not activate layer 0 | event is neither replayed nor skipped; state round-trip remains equivalent |
| RC-R3 | year boundary | scheduler/year continuation and state remain equivalent |
| RC-R4 | P-active explicit `Inpo=1` case | site-resolved P state and site cardinality restore exactly |
| RC-R5 | NH4 sorption-active case | deterministic adsorbed-N reconstruction matches uninterrupted continuation under the admitted numerical policy |
| RC-R6 | external hydrology frame rebind | exact frame identity is accepted; incompatible frame is rejected before mutation |
| RC-R7 | geometry/site-cardinality mismatch | restore fails before mutation |
| RC-R8 | final interval checkpoint serialization | serializer is observationally pure |
| RC-R9 | report-period split when physical-only continuation is promised | physical state equivalence does not depend on report accumulators |
| RC-R10 | deliberate envelope-violation sentinel | any layer-0 activation attempt fails closed and never becomes accepted state |

No tolerance policy is defined here. Exact/semantic comparison rules must come from the admitted numerical and B2/B3 qualification policy rather than being invented locally.

## Management continuation dependency

The restricted profile remains blocked until management schedule continuation is either:

- serialized explicitly as next-event identity/cursor state; or
- deterministically reconstructed from accepted time plus immutable schedule identity under a separately qualified rule.

The split-run suite must include a boundary where a nearby event makes replay/skip observable.

## P initialization-origin boundary

The first restricted-core admission campaign should use `Inpo=1` only unless the 2/3-to-explicit restart conversion has already been independently qualified.

If `Inpo=2/3` origins are later admitted, add a dedicated test proving that conversion to explicit site-resolved restart state preserves the promised trajectory semantics.

## NH4 adsorbed reconstruction boundary

Adsorbed NH4 may remain outside the serialized owner payload only if RC-R5 proves deterministic reconstruction from the complete accepted input set. Failure of that proof means the checkpoint representation must be reconsidered. It does not justify silently adding duplicate mutable ownership.

## Admission result categories

The qualification campaign must report one of:

- `ENVELOPE_NOT_SOURCE_QUALIFIED`;
- `ENVELOPE_SOURCE_QUALIFIED_SPLIT_RUN_NOT_EXECUTED`;
- `SPLIT_RUN_EXECUTED_DISCREPANCY_OPEN`;
- `RESTRICTED_CORE_CHECKPOINT_EVIDENCE_READY_FOR_B3_REVIEW`.

None of these labels by itself grants canonical STATE admission. Final admission remains a governance decision after evidence review.
