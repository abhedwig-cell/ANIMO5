# ANIMO-BUILDQ04 — B3 governance handoff

Status: `NEW_LOCAL_B3_CLASS_B_CANDIDATE_ZERO_BOTTOM_AIR_BOUNDARY_NO_ADMISSION`

## Source local finding

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

BUILDQ04 strengthens and refines the BUILDQ03 intake. The source defect is not merely topology-conditional. For every normal profile with `Nl >= 1`, the `La=Max(0,La-1)` update guarantees `La <= Nl-1`, so the Task-1 fill never assigns `Flair(Nl+1)` before the bottom-layer transformation reads it.

Qualified first-read scope:

`UNCONDITIONAL_TASK1_FIRST_READ_WITHOUT_SOURCE_ASSIGNMENT_FOR_NL_GE_1`

## Qualified boundary identity

`Flair(Nl+1)` is the advective air flux through the lower external face of the modeled soil column.

The connected revision-53 source establishes a closed lower GHG air boundary:

- `GHGasses` anchors air flow to zero at the first saturated interface and states that below the first saturated zone there is no air flow;
- `GHGtransport` has no bottom-neighbour air concentration or bottom diffusion term;
- `GHGtranssub` forces bottom inflow/diffusion coupling to zero;
- the GHG interface has an atmospheric gas boundary but no bottom-air reservoir input;
- CH4 and N2O advective emissions are defined at the atmosphere-soil boundary only.

Qualified local identity:

`Flair(Nl+1) = 0.0`

This is a boundary value already implied by the revision-53 connected source contract. It is not a new physical state and not a new numerical policy.

The peer-reviewed ANIMO N2O formulation of Stolk et al. (2011, Biogeosciences 8, 2649-2663, DOI 10.5194/bg-8-2649-2011) independently supports vertical air advection and atmosphere-soil emission, but does not itself specify the exact revision-53 discrete lower-boundary assignment. The exact zero identity therefore remains primarily source-internal evidence.

## Controlled materiality

Two persisted GNU B1 probes support causal materiality.

The uninitialized first-read probe shows compiler-sensitive first-use values, including NaN propagation at O0 with signalling-NaN initialization and nonzero stack values in ordinary O2 automatic-local execution.

The 60-row boundary-sensitivity matrix varies `Nl`, topology and a controlled lower-interface value. O0 and O2 are byte-identical after the value is made explicit. A positive artificial lower-boundary flux produces bottom gas outflow and changes both the bottom advection balance and disappearance coefficient. In the controlled identity:

`Delta ToFl = -AvCa(Nl) * q_b * St`

and

`Delta Y3 = ReBuAv(Nl) * q_b / He(Nl)`.

Thus the finding is `FLUX_MATERIAL` and `STATE_MATERIAL`. Historical Intel magnitude remains unknown.

## B3 classification request

Provisional class:

`B — LOCAL_ALGEBRA_INDEX_OR_SPECIES_CORRECTION`

More specific subtype:

`LOCAL_BOUNDARY_INDEX_INITIALIZATION_OMISSION`

This is distinct from:

- `TCD-011`, cross-call storage duration;
- `TCD-032`, methanogenesis source-pool transfers;
- `TCD-033`, CH4 component partition;
- `TCD-034`, CH4 plant-growth temperature indexing;
- `TCD-035` and `TCD-036`, GHG restart state;
- `TCD-037`, GHG balance observer interface.

Requested canonical action:

`NEW_CANONICAL_TCD_CANDIDATE_PENDING_COLLISION_CHECK_AND_FAIL_CLOSED_RESERVATION`

BUILDQ04 does not allocate the canonical ID itself.

## Correction boundary

The smallest candidate correction is to establish the closed lower-interface value explicitly before the transformation, or make the existing zeroing range include the lower external face. No production correction has been made.

A future nonzero deep-gas boundary condition would be model evolution, not this local correction, and would require separate qualification.

## Admission state

`new_canonical_tcd_allocated=false`

`corrected_legacy_admitted=false`

`b3_scientific_admitted=false`

`production_migration_admitted=false`

Gate:

`QUALIFIED_ZERO_BOTTOM_AIR_ADVECTIVE_BOUNDARY_CONTRACT_LOCAL_INITIALIZATION_DEFECT_CANDIDATE_HISTORICAL_INTEL_OPEN`
