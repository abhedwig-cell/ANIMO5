# ANIMO-B3D38 — TCD-035 bounded GHG soil-layer restart reconstruction atomic B3 admission

## Decision

Admit the exact bounded identity qualified by STATEQ06 and B3B12:

`TCD035_GHG_SOIL_LAYER_PHASE_VIEW_RECONSTRUCT_FROM_ACCEPTED_CS_HYDROLOGY_AND_CHECKPOINT_TEMPERATURE`

with historical uncertainty.

## Admitted scientific scope

For frozen ANIMO 4.1.5 revision 53 with `IoptGHG >= 1`, soil layers `1..Nl` and gases CH4/N2O:

- gas-specific total gas-water system concentration `Cs/RsCs` is the accepted checkpoint owner;
- aqueous `Co` is a derived phase view, not an independent checkpoint owner;
- restart reconstruction uses accepted checkpoint `theta`, `theta_sat` and checkpoint soil temperature with the unchanged source Bunsen relation;
- revision-53 `Terf` substitution is not admitted as a generally equivalent reconstruction;
- source-derived exact equality controls remain valid: equal reciprocal Bunsen ratio, zero gas-filled pore volume, or zero total gas state.

The admission is a bounded Class-B local restart reconstruction of an existing owner. GOV05 review risk remains Tier C because restart reconstruction affects future trajectories.

## Evidence and uncertainty

The decision consumes exact-final STATEQ06 and B3B12 authorities, plus their pinned GHG01/STATEQ01/ARCH02 evidence and 72-case source-shaped reconstruction oracle. The executable oracle is B1 causality evidence and is not historical B2.

Historical revision-53 behavior remains `UNKNOWN_WITHOUT_B2`; this admission therefore carries historical uncertainty and makes no historical-fidelity claim.

## Excluded scope

This admission does not admit or modify:

- TCD-036 layer0/ponding GHG restart continuity;
- TCD-032, TCD-033 or TCD-034;
- BUILDQ03 hidden within-timestep GHG solver/context state;
- continuous-run Bunsen update policy;
- canonical STATE as a whole;
- a checkpoint file format or production migration;
- full-model GHG split-run equivalence;
- production source, B4 or production operation.

## Aggregate cadence

B3D37/TCD-039 is the first exact-final admission after RG05M. If B3D38 reaches exact-final green, TCD-035 becomes the second post-RG05M admission. The normal three-admission aggregation threshold is therefore not yet reached and RG05N must not be opened solely by this admission.
