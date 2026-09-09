# TCD-016-C1 proposed non-aqueous surface continuation-state contract

Work unit: `ANIMO-SQ01`

Child qualification record: `TCD-016-C1`

Status: `REVIEW_READY_MODEL_EXTENSION_HYPOTHESIS_NOT_SCIENTIFICALLY_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Purpose

This document defines the minimum conservative state contract that would be needed if ANIMO5 evolves beyond the incomplete revision-53 wet/dry representation.

It is deliberately **not** an implementation specification and deliberately **not** a claim about corrected historical ANIMO physics.

The contract separates what follows from conservation and state ownership from what remains scientifically unresolved.

## 2. Provisional state

Provisional identifier:

`M_surface_NH4_non_aqueous_continuation`

Unit:

`kg N m-2`

Control-volume owner:

`surface chemistry / ponding control volume`

State type:

persistent areic mass, independent of aqueous volume.

The name is intentionally chemically noncommittal. It does not assert that the mass is crystallized salt, adsorbed residue, precipitate, a microscopic water film, or another specific phase.

A more specific name may only replace it after theory establishes the phase identity.

## 3. Conservation identity

For the surface NH4 control volume over one accepted transition:

```text
M_aq,beg + M_cont,beg
+ M_external_in
- M_external_out
+ M_internal_in
- M_internal_out
- M_reaction_loss
+ M_reaction_gain
=
M_aq,end + M_cont,end
```

Every nonzero term must have a declared physical source and destination.

Evaporation of water is not an NH4 mass sink by itself.

A numerical threshold may choose representation, but may not remove or create mass.

## 4. Wet to non-aqueous transition

### 4.1 Trigger semantics

The physical trigger is **not yet qualified**.

A future admitted formulation must distinguish:

- hydrological disappearance of representable ponding water;
- any numerical conditioning threshold used before exact zero water;
- any true chemical phase transition, if theory defines one.

The existing revision-53 `Factor=100` and `Fu > 1e-6 m d-1` thresholds are not admitted as physical transition parameters.

### 4.2 Transfer amount

If the accepted state transition removes the aqueous representation while finite NH4 remains inside the surface control volume, the residual conservative mass must have a destination.

The conservation-defined residual is:

```text
Delta_M_to_cont =
  M_aq,beg
+ legitimate aqueous inputs
- legitimate aqueous boundary outputs
- legitimate reactions
- M_aq,end
```

subject to:

```text
Delta_M_to_cont >= 0
```

for a pure aqueous to continuation transfer.

The transfer is internal to the surface control volume and must not be recorded as runoff, drainage or leaching.

## 5. Dry/non-aqueous hold

With no separately admitted process acting on the continuation state:

```text
M_cont,end = M_cont,beg
```

The continuation mass has no water-driven transport while it is non-aqueous/unrepresented as mobile solution.

No volatilization, adsorption, nitrification, precipitation, dissolution or surface-soil exchange is implied by storage in this state.

Any such process requires its own theory-supported transfer law.

This fail-closed rule prevents conservation repair from silently inventing dry chemistry.

## 6. Rewetting/remobilization contract

A future admitted model requires an explicit transfer operator:

`J_remobilize`

from:

`M_surface_NH4_non_aqueous_continuation`

to a declared receiving state, most naturally surface aqueous NH4 if theory supports redissolution there.

For an accepted timestep:

```text
0 <= Delta_M_remobilize <= M_cont,beg + valid_continuation_inputs
```

and:

```text
M_cont,end = M_cont,beg + inputs - Delta_M_remobilize - other_admitted_outputs
```

The receiving aqueous concentration may only be formed when its aqueous volume is positive and representable:

```text
C_aq = M_aq / V_aq
```

The kinetics of `J_remobilize` are **not qualified by SQ01**.

Instantaneous dissolution was used only as a diagnostic conservation experiment. It is not part of this proposed scientific contract.

## 7. Interaction with existing ANIMO phases

### Soil NH4 sorption

No automatic transfer to `Cxnh/Rscxnh` or first-layer sorption is permitted merely because ponding water disappears.

Existing ANIMO theory assigns NH4 adsorption to the soil complex. Transfer to that state requires actual surface-to-soil delivery plus the existing or separately admitted sorption process.

### Artificial additions reservoir

No automatic transfer to `Conhtop/Rsconhtop` is permitted.

That state has management-addition provenance and rainfall-controlled release semantics. Reusing it would alias two different physical meanings.

### Boundary fluxes

Continuation mass may leave through a boundary only through a declared physical carrier or process.

A tiny positive water flux does not justify exporting arbitrarily large solute concentration solely to make accounting close.

### Reactions

The continuation store is not automatically available to aqueous transformations. Availability must be defined process by process after phase theory is established.

## 8. Initialization

A future model using this state must define an initial value explicitly.

For migration of an ordinary historical initial condition with no evidence of pre-existing dry surface residue, the conservative default may be zero only if the initial-state contract explicitly states that no unrepresented continuation mass is being inferred.

Restart is different from cold initialization and may not reset a nonzero continuation store to zero.

## 9. Restart/checkpoint

If admitted, `M_surface_NH4_non_aqueous_continuation` becomes mandatory restart/checkpoint state.

Required properties:

- persisted in physical units `kg N m-2`;
- exact owner and spatial index persisted;
- accepted/start value reconstructed without using concentration or arbitrary water volume;
- restart during a dry interval conserves total surface NH4;
- restart immediately before and after rewetting produces trajectory-equivalent results to uninterrupted execution within the later qualified numerical precision.

A checkpoint that stores only aqueous `Rsconh(0)` is incomplete once this state exists.

## 10. Architecture implications

If admitted after scientific review, ANIMO5 should represent at least these typed internal transfers:

```text
surface_aqueous_NH4 -> surface_non_aqueous_continuation_NH4
surface_non_aqueous_continuation_NH4 -> surface_aqueous_NH4
```

or to another explicitly justified receiving phase.

The MassLedger observes these transfers. It must not own or reconstruct the continuation mass itself.

Accepted/result state semantics are required, consistent with PREP06 and the candidate ANIMO5 architecture.

## 11. Numerical-policy boundary

This contract intentionally does not specify:

- water-volume threshold;
- concentration threshold;
- `Factor` equivalent;
- `Fu` threshold;
- solver tolerance;
- clipping or limiting policy.

Those belong to `TCD-016-E1` after the physical phase semantics are admitted.

The numerical layer may decide when two mathematically equivalent representations are switched, but it may not decide the physical destination of mass.

## 12. Required scientific decisions before admission

The following remain unresolved:

1. physical identity of the continuation phase;
2. whether it is surface-specific or should be generalized to other compartments/species;
3. remobilization law and characteristic timescale;
4. availability to volatilization or biochemical transformations during dry hold;
5. whether any transfer to soil solids can occur without re-entry to aqueous transport;
6. dependency on surface material, temperature, pH or ionic composition;
7. calibration/parameter implications if kinetics are non-instantaneous;
8. independent scientific review.

Until these are resolved, this contract is an explicit model-evolution hypothesis.

## 13. Current disposition

`CORRECTED_LEGACY_CANDIDATE = NOT_ESTABLISHED`

`MODEL_EXTENSION_HYPOTHESIS = REVIEW_READY`

`TCD-016-C1 = BLOCKED_INSUFFICIENT_ANIMO_SPECIFIC_PHASE_THEORY`

`TCD-016-E1 = BLOCKED_DEPENDS_ON_TCD016_C1`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
