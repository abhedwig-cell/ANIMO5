# ANIMO-STATEQ01 surface-state scope correction

Status: `QUALIFIED_SCOPE_CORRECTION_NO_PHYSICS_CHANGE`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Correction

The first STATEQ01 matrix conflated two distinct revision-53 state families:

1. the virtual management/addition reservoirs `Conhtop`, `Conitop`, `Codiormatop`, `Codiornitop`, `Copotop`, `Codiorpotop` identified by PREP06 as `TOP-*` state;
2. the actual layer-0 aqueous transport coordinates `Conh(0)`, `Coni(0)`, `Codiorma(0)`, `Codiorni(0)`, `Copo(0)`, `Codiorpo(0)` that are part of the normal dissolved-state arrays when the surface compartment is active.

That conflation incorrectly attached TCD-016 to the management/addition reservoir profile.

SQ01 explicitly distinguishes the TCD-016 missing owner from the artificial additions reservoir. The natural NH4 failure is a wet-to-low-storage transition of the layer-0 aqueous representation. `Conhtop/Rsconhtop` cannot be reused as the missing continuation owner because it has different management-addition provenance and release semantics.

## 2. Correct topology

STATEQ01 therefore separates three state families.

### Soil dissolved state

Layers `1..Nl` remain ordinary core dissolved-state coordinates for labile DOM/DON/DOP, NH4, NO3 and PO4.

### Layer-0 aqueous state

Index `0` is a dynamically activated surface aqueous compartment controlled by hydrological surface-state semantics. It can be present even though the artificial management-addition reservoir is conceptually distinct.

For NH4 this state is not scientifically complete across deactivation because TCD-016-C1 has no admitted dry/non-aqueous continuation owner. The proposed SQ01 continuation mass remains `UNRESOLVED_SCIENTIFIC_STATE` and is not canonicalized.

SQ01 establishes shared low-storage reachability for several other solutes but only NH4 has the qualified natural mass-deletion finding. Their layer-0 coordinates are therefore separated from the soil core and retained as shared-hazard candidates rather than silently declared defective.

### Management/addition reservoir state

The `TOP-*` `Con*top/Rscon*top` family remains its own conditional physical state. PREP06 and PREP12 support structural persistence/read-write representation for the active species. This family is not the TCD-016 continuation phase and must not absorb residual layer-0 mass by convenience.

## 3. Profile consequence

A generic core profile that allows layer-0 aqueous NH4 activation cannot be called state-complete while TCD-016-C1 is unresolved.

To preserve feature-scoped progress without hiding that fact STATEQ01 now distinguishes:

- `CORE_CNP_SUBSURFACE_ONLY`: readiness candidate only under an explicit application-envelope invariant that layer-0 aqueous solute state cannot activate. If that invariant is violated the run/profile fails closed;
- `CORE_CNP`: general core with layer-0 aqueous activation in scope and therefore blocked on TCD-016-C1;
- `CORE_CNP_WITH_ADDITION_RESERVOIRS`: adds the separate `TOP-*` management/addition state but does not solve the layer-0 TCD-016 gap.

This is a readiness/profile distinction only. It does not claim a new legacy feature switch exists and does not alter hydrology or transport physics.

## 4. Admission consequence

The corrected matrix no longer obtains a nominally ready core by misclassifying the TCD-016 compartment as an optional additions feature.

The narrower `CORE_CNP_SUBSURFACE_ONLY` candidate can proceed to split-run qualification if its no-layer0-activation envelope can itself be specified and enforced fail-closed. General `CORE_CNP` remains blocked on the explicit scientific state gap.

No TCD identity is changed and no new TCD is allocated.