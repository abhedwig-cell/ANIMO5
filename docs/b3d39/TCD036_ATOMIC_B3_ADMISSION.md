# ANIMO-B3D39 — TCD-036 bounded GHG pre-existing ponding layer0 restart atomic B3 admission

## Decision

Admit the exact bounded identity qualified by STATEQ07 and B3B13:

`TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_GHG_RESTART_IDENTITY_FROM_SERIALIZED_TOTAL_SYSTEM_OWNER`

with historical uncertainty.

## Admitted scientific scope

For frozen ANIMO 4.1.5 revision 53 with GHG active, layer 0 and gases CH4/N2O independently:

- gas-specific total gas-water system concentration `Cs(0)` / accepted `RsCs(0)` is the serialized checkpoint owner;
- aqueous `Co(0)` / `RsCo(0)` is a deterministic derived view, not an independent checkpoint owner;
- for active pre-existing ponding, the source identity `Cs(0)=Co(0)` permits restart reconstruction as `Co(0)=Cs(0)`;
- CH4 and N2O remain separate identities and may not be cross-mapped;
- a new ponding event remains governed by the source-defined inflow initialization and is not replaced by this identity reconstruction;
- when ponding is absent, no dormant layer0 GHG state is introduced.

The scientific B3 class is `B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER`. GOV05 review remains Tier C because restart/checkpoint semantics can alter future trajectories.

## Evidence and uncertainty

The decision consumes exact-final `ANIMO-STATEQ07@26f6e61da328a5578b9c4b332de04eb99a3ac04f` and `ANIMO-B3B13@202a2983d1cce07682eaa95825891fc33e4f6398`, together with their pinned GHG01/ARCH02/source evidence and source-shaped layer0 oracle.

The executable oracle is B1 source-derived synthetic causality evidence, not historical B2. Historical revision-53 runtime behavior therefore remains `UNKNOWN_WITHOUT_B2`; this admission carries historical uncertainty and makes no historical-fidelity claim.

## Excluded scope

This admission does not admit or modify:

- TCD-035 soil-layer `1..Nl` restart reconstruction;
- TCD-032, TCD-033 or TCD-034;
- new-ponding initialization semantics;
- a dormant layer0 GHG store in no-ponding conditions;
- BUILDQ03 hidden within-timestep GHG solver/context state;
- canonical STATE as a whole;
- checkpoint serialization format redesign;
- whole-model GHG split-run equivalence;
- production source, B4 or production operation.

## Aggregate cadence

B3D37/TCD-039 and B3D38/TCD-035 are the first two exact-final admissions after RG05M. If B3D39 reaches exact-final green, TCD-036 is the third post-RG05M admission. The normal three-admission aggregation threshold is then reached, so RG05N must be opened before any fourth scientific admission.
