# ANIMO-STATEQ01 restricted-core application-envelope qualification specification

Status: `SOURCE_GUARD_QUALIFIED_TEST_SPEC_NOT_B3_ADMISSION`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Purpose

This specification defines what must be proven before `CORE_CNP_SUBSURFACE_ONLY` can be used as the first executable checkpoint-admission candidate. It does not create a production feature switch and does not change revision-53 physics.

The restricted profile exists only to isolate a state-complete application envelope that excludes layer-0 surface transport and the unresolved general-core surface continuation seams.

## Source-qualified envelope invariant

The central legacy transport gate is `Flpn`. `MODFLUX` and the standard transport routines start at compartment `1-Flpn`; therefore layer 0 participates when `Flpn=1`.

The restricted profile is deliberately stricter than merely requiring `Flpn=0`, because revision 53 permits physically positive surface storage below its `1.0d-4` activation threshold.

At every accepted start boundary and every candidate hydrology end frame:

### Aggregated hydrology

```text
Pn  == 0
Pnt == 0
```

### Detailed hydrology

```text
Pn + Snla == 0
Pnt + Snt  == 0
```

In addition, every layer-0 restart/input solute coordinate in scope must be exactly zero before restore is admitted.

These equalities define an application envelope. They do not replace the legacy `1.0d-4` process threshold.

## Upper-boundary reservoirs remain core

`Conhtop`, `Conitop`, `Codiormatop`, `Codiornitop`, and P-active `Copotop/Codiorpotop` are not an optional add-on to the restricted profile.

`UBoundconc` evolves these reservoirs when `Flpn=0`, and the standard transport path uses their average concentration as the upper boundary for soil layer 1. They therefore remain continuation-critical core state even when layer 0 is excluded.

The former `CORE_CNP_WITH_ADDITION_RESERVOIRS` distinction is withdrawn.

## Restore zero-state requirement

The restricted profile must reject, not normalize, a checkpoint/input containing nonzero layer-0 dissolved state.

This is necessary because revision 53 explicitly reads layer-0 NH4/NO3/DOM/DON and related coordinates but `Inicalc` unconditionally zeroes several of them before the first timestep. That local finding is tracked as:

`RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`

A restricted-profile restore can avoid that defect only by proving that the incoming layer-0 state is exactly zero.

## Fail-before-mutate contract

The restricted profile may be entered only after configuration normalization and exact external hydrology binding establish all envelope predicates.

Hard failures include:

- unsupported or unknown hydrology mode;
- missing accepted/candidate surface-storage coordinates needed by the guard;
- nonzero `Pn`, `Pnt`, or detailed-hydrology `Pn+Snla` / `Pnt+Snt`;
- nonzero layer-0 restart/input C/N/P state;
- a candidate hydrology frame that would create positive layer-0 storage;
- any attempt to continue by discarding, clipping, projecting or remapping layer-0 mass;
- any attempt to use the unadmitted SQ01 dry-continuation proposal as an implicit restore field.

The guard is evaluated before chemistry or management mutation. A violating candidate interval can never become accepted state under this profile.

## Restricted-core split-run qualification matrix

Required test classes:

| ID | Boundary | Required assertion |
|---|---|---|
| RC-R1 | clean non-event accepted boundary | uninterrupted and split trajectories have equivalent continuation-critical core state and event sequence |
| RC-R2 | immediately before/after management event within the zero-surface envelope | event is neither replayed nor skipped; upper-boundary reservoir state round-trips |
| RC-R3 | year boundary | scheduler/year continuation and state remain equivalent |
| RC-R4 | P-active explicit `Inpo=1` case | site-resolved P state and site cardinality restore exactly |
| RC-R5 | NH4 sorption-active case | deterministic adsorbed-N reconstruction matches uninterrupted continuation under admitted policy |
| RC-R6 | external hydrology frame rebind | exact frame is accepted; incompatible frame rejected before mutation |
| RC-R7 | geometry/site-cardinality mismatch | restore fails before mutation |
| RC-R8 | final interval checkpoint serialization | serializer is observationally pure |
| RC-R9 | report-period split when physical-only continuation is promised | physical continuation does not depend on report accumulators |
| RC-R10 | deliberate positive-surface-storage sentinel | candidate interval fails before chemistry mutation and is never accepted |
| RC-R11 | deliberate nonzero layer-0 restart-state sentinel | restore fails before accepted-state construction; no zeroing normalization is allowed |
| RC-R12 | nonzero `Con*top` with `Flpn=0` | upper-boundary reservoir continuity is preserved and feeds layer 1 identically after split |

No local tolerance policy is invented here. Comparison policy must come from the admitted numerical and B2/B3 qualification framework.

## Management continuation dependency

The restricted profile remains blocked until management progression is either serialized as exact next-event identity/cursor state or reconstructed under a separately qualified deterministic rule. RC-R2 must make replay/skip observable.

## P initialization-origin boundary

The first campaign should use `Inpo=1` unless `Inpo=2/3` origin to explicit-state restart has already been independently qualified.

## NH4 adsorbed reconstruction boundary

Adsorbed NH4 may remain outside the serialized independent owner payload only if RC-R5 proves deterministic reconstruction from the complete accepted input set. Failure requires reconsidering checkpoint representation, not silently creating duplicate mutable ownership.

## Admission result categories

The campaign reports one of:

- `GUARD_SOURCE_QUALIFIED_EXECUTABLE_SENTINEL_NOT_RUN`;
- `SPLIT_RUN_EXECUTED_DISCREPANCY_OPEN`;
- `RESTRICTED_CORE_CHECKPOINT_EVIDENCE_READY_FOR_B3_REVIEW`.

None of these labels grants canonical STATE admission by itself.
