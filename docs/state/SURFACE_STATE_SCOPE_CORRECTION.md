# ANIMO-STATEQ01 surface-state scope correction

Status: `QUALIFIED_SCOPE_CORRECTION_SUPERSEDED_AND_REFINED_BY_SOURCE_PREDICATE_AUDIT`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Original correction retained

STATEQ01 originally conflated two revision-53 state families:

1. `Con*top/Rscon*top` upper-boundary reservoir coordinates;
2. layer-0 dissolved transport coordinates `Con*(0)` and related arrays.

That conflation was incorrect. TCD-016 concerns layer-0 NH4 low-storage continuation and cannot be repaired by reusing the upper-boundary reservoir as a dry continuation owner.

## 2. Refinement after source qualification

A subsequent source audit adds an important correction to the first scope note: the `Con*top/Rscon*top` family is not an optional management-only feature.

`UBoundconc` evolves these reservoirs even when `Flpn=0`, and standard transport uses their average concentration as the upper boundary for soil layer 1. They therefore belong to the core continuation set, including `CORE_CNP_SUBSURFACE_ONLY`.

The previously proposed profile `CORE_CNP_WITH_ADDITION_RESERVOIRS` is withdrawn.

## 3. Current topology

STATEQ01 now distinguishes:

- core soil dissolved state in layers `1..Nl`;
- core upper-boundary reservoir state `Con*top/Rscon*top`;
- layer-0 surface transport state, active in the standard transport domain when `Flpn=1`;
- the unadmitted proposed non-aqueous NH4 continuation state from SQ01.

The restricted core excludes layer-0 state by requiring zero surface storage and zero layer-0 restart state, not by dropping upper-boundary reservoirs.

## 4. General core blockers

General surface-capable `CORE_CNP` remains blocked by:

- TCD-016-C1, unresolved low-storage NH4 continuation science;
- `RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`, a separate source-confirmed restart initialization finding.

No new physics or canonical TCD allocation is made here.
