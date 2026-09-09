# TCD-016 atomization and qualification-gate plan

Work unit: `ANIMO-SQ01`

Status: `ATOMIZATION_REFINED_BY_HISTORICAL_THEORY_AND_SHARED_SURFACE_ACTIVATION_NO_CHILD_ADMITTED`

Production migration: `NOT_ADMITTED`

## Why atomization is required

B3Q01 classifies TCD-016 primarily as Class C with a secondary Class E aspect and marks the parent `REQUIRES_ATOMIZATION_BEFORE_ADMISSION`.

The observed legacy branch combines two different questions:

1. what physical state owns NH4 mass when the layer-0 aqueous phase is deactivated;
2. how the low-storage transport algorithm and its outflow threshold should behave numerically once that physical state model is defined.

Historical ANIMO 3.5 theory strengthens this separation. Report 144 defines conservation over liquid plus named solid phases and gives the semi-analytical concentration formulation recognizable in revision-53 `Transsub/Detcoef`.

A further frozen-source reconstruction shows that the effective layer-0 `0.1 mm` low-storage boundary in `Transsub` is aligned with the `Flpn` ponding activation boundary in both `Hydro_detailed.for` and `Hydro_aggregated.for`.

Therefore the parent discrepancy is best interpreted as a missing conserved owner across a source-defined surface-state deactivation seam, plus a separate numerical/export-policy problem around that seam.

The two questions cannot be admitted as one correction.

## Proposed child qualification records

### TCD-016-C1: surface NH4 continuation-state ownership

Provisional class:

`C = MISSING_PHYSICAL_STATE_OR_INCOMPLETE_STATE_MODEL`

Question:

When the source deactivates the mobile ponding representation while finite NH4 mass remains inside the surface control volume, which physical state owns that mass and how does it later leave that state?

Historical theory supports two points independently of the defect code:

- matter must be conserved;
- dissolved storage is represented through liquid water and concentration, while NH4 sorption belongs to the soil complex.

Source reconstruction now also identifies the legacy representation seam:

- hydrology sets `Flpn` from a `1.0d-4 m = 0.1 mm` surface-water threshold;
- `Transsub` uses the same effective `0.1 mm` threshold for layer 0 through `1.0d-6*Factor` with `Factor=100`.

This establishes a historical **surface activation boundary**. It does not establish a physical dry chemical phase or remobilization law.

Required evidence:

- authoritative ANIMO-specific phase theory or explicit model-evolution authority;
- state definition and unit;
- spatial/control-volume ownership;
- relationship between the legacy `0.1 mm` representation boundary and the physical state transition;
- wet-to-continuation transfer condition;
- dry/non-aqueous hold semantics;
- continuation-to-wet or other release transition;
- interaction with volatilization, adsorption, transport and boundary fluxes;
- initialization and restart semantics;
- conservation closure for all connected transfers;
- expected trajectory differences from frozen legacy behaviour;
- independent scientific review.

Current status:

`BLOCKED_INSUFFICIENT_ANIMO_SPECIFIC_PHASE_THEORY`

Preferred extension hypothesis:

`M_surface_NH4_non_aqueous_continuation [kg N m-2]`

A review-ready fail-closed state contract is recorded in `TCD016_C1_PROPOSED_NONAQUEOUS_STATE_CONTRACT.md`. It defines conservation and ownership constraints but deliberately leaves chemistry and remobilization kinetics unresolved.

This is not yet a corrected-legacy state.

### TCD-016-E1: low-storage transport threshold and numerical transition policy

Provisional class:

`E = NUMERICAL_POLICY_CHANGE`

Question:

Given an admitted physical continuation state, what numerical policy governs concentration-based transport approaching and crossing the source-defined surface activation seam?

The legacy policy surfaces must be separated:

- `0.1 mm` layer-0 storage boundary: shared by hydrological ponding activation and the effective `Transsub` low-storage test;
- `Fu > 1e-6 m d-1 = 0.001 mm d-1`: `Transsub`-local export condition for residual mass;
- `Small`, `Vsmall`, `Vvsmall`: local numerical branch-selection constants.

Historical Report 144 theory defines the semi-analytical concentration equation in terms of moisture storage and sorption. No recovered theory identifies the `0.1 mm` or `0.001 mm d-1` values as physical chemical constants.

Required evidence after C1 is defined:

- exact governing mass equations on both sides of the admitted state transition;
- dimensional meaning and role of every threshold;
- separation of representation activation, numerical conditioning and physical transition semantics;
- convergence/sensitivity around the transition;
- no concentration singularity;
- no mass deletion or creation;
- continuity or explicitly justified discontinuity of state/flux trajectories;
- timestep and precision sensitivity;
- failure/fallback behaviour;
- restart equivalence across the transition;
- independent numerical review.

Current status:

`BLOCKED_DEPENDS_ON_TCD016_C1`

The existing tiny-outflow counterfactual is not an E1 candidate because it closes mass by generating a pathological concentration and does not define state ownership.

## Ancillary surface-routing seam

`UBoundconc.for` uses a separate `1.0d-3 m = 1 mm` threshold for routing dry NH4/NO3 deposition between layer 0 and the first soil compartment.

The canonical TCD-016 event starts at about `0.109 mm`, so it is above the `Flpn` activation boundary but below this dry-deposition routing boundary.

This is recorded as an additional source semantic seam. SQ01 has not established causal relevance to the TCD-016 mass-loss event and does not open another TCD solely from this observation.

## No standalone Class-B child at this stage

The immediate branch that zeroes `Rsc` and, for the observed `Iflsol=2` route, `Avc` is source-localized. But the mathematically correct replacement cannot be specified without answering C1.

Therefore SQ01 does not create a Class-B child merely because the deletion occurs in one local branch.

If later authoritative theory proves that the intended continuation state already exists and only one local assignment is wrong, that conclusion may justify reclassification. Current evidence does not.

## Dependency order

Qualification order is strict:

`TCD-016-C1 -> TCD-016-E1 -> parent TCD-016 disposition`

E1 cannot define the missing phase by numerical convention.

The parent remains unadmitted until both children are separately qualified or until C1 establishes that no E1 policy change is required.

## Class-C gates for C1

C1 may only move to B3 admission review when all gates below are independently satisfied:

| gate | requirement | current state |
| --- | --- | --- |
| C1-G1 | authoritative phase/state theory | **FAIL**: conservation and activation seam reconstructed, phase identity still missing |
| C1-G2 | state variable definition and units | `M_surface_NH4_non_aqueous_continuation`, `kg N m-2`, **PROPOSED** |
| C1-G3 | single physical owner/control volume | surface control volume, **PROPOSED** |
| C1-G4 | activation/deactivation semantics | legacy `0.1 mm` representation seam source-bound, **PHYSICAL MEANING NOT QUALIFIED** |
| C1-G5 | initialization semantics | fail-closed contract drafted, **NOT SCIENTIFICALLY QUALIFIED** |
| C1-G6 | restart/checkpoint completeness | mandatory persistent mass if admitted, **CONTRACT DEFINED NOT QUALIFIED** |
| C1-G7 | wet-to-continuation transfer rule | conservation residual rule defined, **PHYSICAL TRIGGER NOT QUALIFIED** |
| C1-G8 | dry/non-aqueous hold processes | fail-closed no-process default proposed, **CHEMISTRY NOT QUALIFIED** |
| C1-G9 | rewetting/release rule | bounded transfer operator defined, **KINETICS NOT QUALIFIED** |
| C1-G10 | connected-process conservation | local wet/dry synthetic closure demonstrated, **FULL PROCESS SET NOT QUALIFIED** |
| C1-G11 | edge-case tests | wet -> dry -> hold -> wet topology demonstrated, **APPLICATION ENVELOPE NOT RUN** |
| C1-G12 | expected legacy divergence | deterministic loss event and state deactivation characterized, **PARTIAL** |
| C1-G13 | independent scientific review | **NOT DONE** |

Because C1-G1 and C1-G13 fail, and multiple transition/chemistry gates remain provisional, no Class-C B3 admission is permitted.

## Historical-theory and source-seam effect on the blocker

The blocker is now narrower than at SQ01 start.

It is no longer uncertain whether conservation requires a destination for residual mass. Historical ANIMO theory explicitly requires conservation.

It is also no longer uncertain where the problematic representation transition occurs. The frozen source aligns hydrology and transport at a `0.1 mm` surface activation boundary, and the canonical event crosses that boundary.

What remains uncertain is the **physical identity and release law** of the destination, and how the numerical transport solution should cross that boundary once the state model is admitted.

Therefore the current scientific statement is:

`THEORY_SUPPORTED_CONSERVATION_REQUIREMENT_AND_SOURCE_BOUND_SURFACE_ACTIVATION_GAP`

but not:

`THEORY_QUALIFIED_DRY_PHASE`.

## Parent disposition

Current parent route remains:

`PHYSICS_MODEL_EXTENSION_REQUIRED`

unless stronger ANIMO-specific theory establishes C1 as intended legacy physics.

Current work-unit status remains:

`BLOCKED_TCD016_INSUFFICIENT_THEORY_FOR_CORRECTED_LEGACY_ADMISSION`

Production migration remains `NOT_ADMITTED`.
