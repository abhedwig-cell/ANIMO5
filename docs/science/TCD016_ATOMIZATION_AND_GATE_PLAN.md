# TCD-016 atomization and qualification-gate plan

Work unit: `ANIMO-SQ01`

Status: `ATOMIZATION_PLAN_DEFINED_NO_CHILD_ADMITTED`

Production migration: `NOT_ADMITTED`

## Why atomization is required

B3Q01 classifies TCD-016 primarily as Class C with a secondary Class E aspect and marks the parent `REQUIRES_ATOMIZATION_BEFORE_ADMISSION`.

The observed legacy branch combines two different questions:

1. what physical state owns NH4 mass when the layer-0 aqueous phase disappears;
2. how the low-storage transport algorithm and its `Fu > 1e-6` threshold should behave numerically once that physical state model is defined.

They cannot be admitted as one correction.

## Proposed child qualification records

### TCD-016-C1: surface NH4 continuation-state ownership

Provisional class:

`C = MISSING_PHYSICAL_STATE_OR_INCOMPLETE_STATE_MODEL`

Question:

When ponding water vanishes while finite NH4 mass remains inside the surface control volume, which physical state owns that mass and how does it later leave that state?

Required evidence:

- authoritative ANIMO-specific phase theory or explicit model-evolution authority;
- state definition and unit;
- spatial/control-volume ownership;
- wet -> dry transfer condition;
- dry hold semantics;
- dry -> wet or other release transition;
- interaction with volatilization, adsorption, transport and boundary fluxes;
- initialization and restart semantics;
- conservation closure for all connected transfers;
- expected trajectory differences from frozen legacy behaviour;
- independent scientific review.

Current status:

`BLOCKED_INSUFFICIENT_ANIMO_SPECIFIC_PHASE_THEORY`

Preferred extension hypothesis:

`M_surface_NH4_non_aqueous_continuation [kg N m-2]`

This is not yet a corrected-legacy state.

### TCD-016-E1: low-storage transport threshold and numerical transition policy

Provisional class:

`E = NUMERICAL_POLICY_CHANGE`

Question:

Given an admitted physical continuation state, what numerical policy governs the transition between ordinary aqueous transport and the dry/continuation-state route?

The legacy trigger includes the `Factor=100` low-storage criterion and the layer-0 export condition `Fu > 1e-6 m d-1`.

Required evidence after C1 is defined:

- exact governing mass equations on both sides of the transition;
- dimensional meaning of every threshold;
- proof that a threshold is numerical rather than a hidden physical parameter;
- convergence/sensitivity around the transition;
- no concentration singularity;
- no mass deletion or creation;
- continuity or explicitly justified discontinuity of state/flux trajectories;
- precision sensitivity;
- failure/fallback behaviour;
- independent numerical review.

Current status:

`BLOCKED_DEPENDS_ON_TCD016_C1`

The existing tiny-outflow counterfactual is not an E1 candidate because it closes mass by generating a pathological concentration and does not define state ownership.

## No standalone Class-B child at this stage

The immediate branch that zeroes `Rsc` and `Avc` is source-localized, but the mathematically correct replacement cannot be specified without answering C1. Therefore SQ01 does not create a Class-B child merely because the deletion occurs in one local branch.

If later authoritative theory proves that the intended state already exists and only one local assignment is wrong, that conclusion may justify reclassification. Current evidence does not.

## Dependency order

Qualification order is strict:

`TCD-016-C1 -> TCD-016-E1 -> parent TCD-016 disposition`

E1 cannot define the missing phase by numerical convention.

The parent remains unadmitted until both children are separately qualified or until C1 establishes that no E1 policy change is required.

## Class-C gates for C1

C1 may only move to B3 admission review when all gates below are independently satisfied:

| gate | requirement | current state |
| --- | --- | --- |
| C1-G1 | authoritative phase/state theory | FAIL / missing |
| C1-G2 | state variable definition and units | PROVISIONAL only |
| C1-G3 | single physical owner/control volume | PROVISIONAL only |
| C1-G4 | initialization semantics | NOT QUALIFIED |
| C1-G5 | restart/checkpoint completeness | DESIGNABLE, NOT QUALIFIED |
| C1-G6 | wet -> dry transfer rule | CONSERVATION FORM DEFINED, PHYSICS NOT QUALIFIED |
| C1-G7 | dry hold processes | NOT QUALIFIED |
| C1-G8 | rewetting/release rule | NOT QUALIFIED |
| C1-G9 | connected-process conservation | PARTIAL diagnostic only |
| C1-G10 | edge-case tests | DIAGNOSTIC TOPOLOGY ONLY |
| C1-G11 | expected legacy divergence | PARTIALLY CHARACTERIZED |
| C1-G12 | independent scientific review | NOT DONE |

Because C1-G1 fails, no Class-C B3 admission is permitted.

## Parent disposition

Current parent route remains:

`PHYSICS_MODEL_EXTENSION_REQUIRED`

unless stronger ANIMO-specific theory establishes C1 as intended legacy physics.

Current work-unit status remains:

`BLOCKED_TCD016_INSUFFICIENT_THEORY_FOR_CORRECTED_LEGACY_ADMISSION`

Production migration remains `NOT_ADMITTED`.
