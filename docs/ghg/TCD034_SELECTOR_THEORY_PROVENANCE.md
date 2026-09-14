# ANIMO-GHG06: TCD-034 selector scientific identity, theory provenance and bounded design qualification

## Scope and governance

This workunit owns exactly `TCD034_PLANT_GROWTH_TEMPERATURE_SELECTOR_IDENTITY`. It starts from `ANIMO-GHG05@cf235fbc93fdb77d93aa260c8ede8fcdbbdbc5d3` and consumes, without mutating, `ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`, `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`, `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`, `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`, `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700` and routing authority `ANIMO-B3I10@942f26fe32eaf91679e59a1968ae173a3703e22d`. Parallelism is `PARALLEL_AFTER_PINNING`. No production source, TCD register, B3 queue, aggregate, routing, canonical testbank registry or B4 authority is changed. GHG06 does not close the separate `FvegCH4>0` positive-control blocker.

## Reconstructed source semantics

The GHG05 reconstruction survives recheck. In frozen revision 53, `Nuroup` is updated by the root routines before `GHGasses`. For detailed SWATRE hydrology those routines reset `Nuroup=0` and retain the deepest compartment with `Flev(Ln)>=1e-7`, so runtime ownership is `0<=Nuroup<=Nl`. `GHG_Methane` then sets `LnRoot=Nuroup`, traverses the rooted domain, and after the root loops executes `Te50=Te(Ln)`. Under current standard Fortran loop termination this is `Te(Nuroup+1)` for a positive-trip loop and `Te(1)` for the zero-trip case. The zero-root temperature evaluation is not observable in plant transport because `K1plant` is zero for every compartment.

`Te` is not an air-temperature proxy. The frozen internal temperature routine computes layer temperature at the compartment midpoint, while hydrological input supplies `Te(1:Nl)` and separately assigns `Te(0)=Avdate`. The ANIMO 4.0 User's Guide likewise defines `TE(NL)` as average daily soil temperature of layers 1 to NL in degrees Celsius. That guide predates the GHG extension and does not define `Te50` or a CH4 plant-growth selector.

The plant and soil methane temperature concepts are distinct in the code. `CH4produc` consumes local `Te(Ln)` for soil methanogenesis. The disputed `Te50` is used only to calculate `fGrow`, which multiplies plant-mediated transport: `K1plant = Kpl * FvegCH4 * fRoot * fGrow`. Treating the two temperature roles as one concept would therefore be a category error.

## New provenance result: the Walter-Heimann fingerprint

GHG06 found a much stronger provenance fingerprint than GHG05 had available, but it still does not complete the selector gate. Walter and Heimann (2000, Global Biogeochemical Cycles, DOI `10.1029/1999GB001204`) describe plant-mediated wetland CH4 transport as a product of a rate constant, vegetation factor, root-distribution factor, vegetation-growth factor and methane concentration. Their rate constant is `0.01 h-1`, exactly `0.24 d-1`, matching ANIMO `Kpl=0.24`. Their growth multiplier runs from 0 to 4, uses the same quadratic form, and sets `Tmat=Tgr+10 C`. Most importantly, their growth-state temperature is daily mean soil temperature at 50 cm depth, named `T50`.

The ANIMO implementation contains the same multi-feature structure: `Kpl=0.24 d-1`, `FvegCH4`, `fRoot`, the same `fGrow` envelope and `Tmat=Tegr+10`, plus the local variable name `Te50`. Later Wageningen GHG context also links the SWAP-ANIMO methane model to Walter-Heimann lineage. This makes the conceptual interpretation **daily mean soil temperature at 0.50 m depth** substantially more than a naming guess. It is `STRONGLY_SUPPORTED` as a source-model provenance fingerprint.

It is not promoted to historical ANIMO authority. Under this workunit's evidence hierarchy Walter-Heimann and later literature remain `NEW_MODEL_EVOLUTION_SCIENTIFIC_EVIDENCE`, not a revision-53 ANIMO specification. The accessible 2007 SWAP-ANIMO publication confirms the GHG lineage but does not specify the disputed selector. The detailed Hendriks et al. ANIMO GHG report cited in later literature remains a provenance lead rather than a frozen reviewed selector authority here.

## Why the stronger T50 evidence still does not qualify a positive selector

The decisive missing link is not now primarily the physical concept. It is the exact ANIMO discretization operator. ANIMO represents temperature on arbitrary model compartments. No reviewed ANIMO authority states whether physical `T(z=0.50 m)` must be taken from the containing compartment, the nearest layer midpoint, an interpolation between layer-centred temperatures, or another scheme. Those choices are not mathematically equivalent when layer geometry changes.

The current expression `Te(Nuroup+1)` cannot supply that missing rule. `Nuroup` is a dynamic root/transpiration state, not a fixed-depth coordinate. Its physical depth can change with crop state and hydrology. At `Nuroup=Nl` the current selector can leave the demonstrated producer range, and at `Nl=Manl` it leaves the declared array bound. Therefore the observed post-DO selector cannot be silently reinterpreted as a robust 50 cm lookup.

This fails the positive gate for exact mathematical selector, indexing semantics of a replacement T50 operator, multi-layer behavior, and proof of no contradiction with frozen ANIMO evidence. A root-weighted temperature is also not adopted. It may be scientifically plausible, but neither ANIMO evidence nor the Walter-Heimann formulation authorizes it for this term.

## Competing hypotheses

H1 and H2 describe aspects of current source behavior, not established scientific identity. H3, H4 and H5 lack authority. H6, fixed-depth daily mean soil temperature at 0.50 m, is the strongest conceptual candidate by a wide margin because of the exact provenance fingerprint, but no exact ANIMO layer-selection rule is qualified. H7 therefore remains the only defensible exact-selector disposition: no unique implementable selector can yet be scientifically qualified. The detailed machine-readable assessment is in `GHG06_TCD034_HYPOTHESIS_MATRIX.csv`.

## Decision

The historical-selector result is `NOT_QUALIFIED`. The bounded model-evolution selector result is also `NOT_QUALIFIED`. The primary disposition is:

`QUALIFIED_TCD034_SELECTOR_IDENTITY_UNRESOLVED_MATERIAL_THEORY_OR_DESIGN_EVIDENCE_REQUIRED`

This is not an empirical-discrimination disposition. Dedicated experiments are not needed to establish the current gap. The next missing evidence is a theory/design rule that turns the strongly supported physical T50 concept into one exact operator over arbitrary ANIMO layer geometry, or an ANIMO-specific historical source that proves a different selector. Empirical data may later test a chosen model-evolution operator, but that is downstream of the present missing-definition problem.

## FVEGCH4 boundary and next handoff

The frozen natural GHG testcase still has `FvegCH4=0.0`; GHG06 does not claim positive activation or reachability closure. If a later workunit positively qualifies one exact selector, the normal next step remains a separate `ANIMO-GHG07` for active `FvegCH4>0` positive-control and selector-reachability qualification. GHG06 does not start it.

## Falsification and minimal evidence

This negative qualification is falsifiable. It should be superseded if a source-specific ANIMO GHG theory/design authority explicitly defines the plant-growth temperature and its layer mapping, or if a separately governed model-evolution workunit explicitly defines and scientifically qualifies a 0.50 m temperature operator with arbitrary-layer, boundary, restart and observation semantics. A historical document that explicitly supports `Te(Nuroup+1)` would also override the present interpretation, but none was found in the reviewed evidence.

## Testbank posture

No production or central testbank mutation is made. `GHG06_TCD034_PROVENANCE_FRAGMENT.json` is a bounded provenance fragment only. It preserves source hashes, the negative selector result and the separation from `FvegCH4` positive-control work without claiming a new behavioral oracle or whole-model golden baseline.
