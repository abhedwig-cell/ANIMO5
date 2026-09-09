# ANIMO-ARCH01 candidate state ownership model

Status: `CANDIDATE_ARCHITECTURE_DESIGN_NOT_CANONICAL_STATE_ADMISSION`.

This design is derived from the qualified source-bound PREP06 state register. It deliberately stops before implementation. The programme migration DAG still requires a qualified migration baseline before canonical STATE admission.

## Core ownership rule

Every continuation-critical physical quantity has exactly one runtime owner. Derived values, rates, scratch and reporting accumulators do not become co-owners merely because the legacy implementation stores them in arrays.

The machine-readable mapping is `integration/animo-architecture/ARCH01_STATE_OWNERSHIP.csv`. It covers all 53 PREP06 state/non-state families exactly once.

## Candidate runtime components

### `HydrologyExchangeState`

Owns the hydrological coordinates ANIMO needs to compute aqueous storage and transport but does not make ANIMO the physical hydrology solver. The same explicit exchange contract can be populated by standalone hydrology input or by a coupled hydrological kernel.

Candidate coordinates include matrix water and, for detailed hydrology, interception, snow and ponding. `W-SURFACE-AGG` remains a derived representation rather than an independent store. This preserves PREP06's finding that water is supplied by hydrology while still making storage coordinates explicit.

TCD-018 remains an open evidence seam: interception is real storage even though the legacy public water ledger does not observe its storage change.

### `SurfaceReservoirState`

Owns the conditional top/addition reservoir for NH4, NO3, labile DOM/DON/DOP and PO4. These values are physical only when the configured route allows mass to reside in the virtual surface reservoir.

The stable DOM/DON/DOP layer-0 parser surface is not promoted. PREP06 found it parser-representable but dynamically dormant in revision 53. ARCH01 marks it `NOT_SUPPORTED_UNTIL_QUALIFIED`.

### `OrganicMatterState`

Owns fresh organic fractions, original humus, exudate-derived humus and root-exudate organic matter. N and P composition are properties of these stores, not separate independently mutable copies of the same organic material.

This component must not reconstruct beginning storage from a different formula than end storage. TCD-026 is the concrete reason: initial exudate OM is physical state even though the legacy fresh-OM initial ledger omits it.

### `DissolvedOrganicState`

Owns labile and stable dissolved organic C/OM, N and P state coordinates. A concentration coordinate can be persistent state even when conserved storage is calculated using water volume plus the source-defined sorption contribution.

Stable DOM remains a candidate with documentation limitations. Stable-DOM P additionally carries TCD-023 and must not be considered scientifically admitted until its source-to-theory discrepancy is qualified.

### `MineralNitrogenState`

Owns aqueous NH4, adsorbed NH4 and aqueous NO3. NH4 aqueous and adsorbed stores are separate state coordinates within one elemental-N control volume.

TCD-015 and TCD-016 remain architecture constraints, not accepted behaviours: a negative-concentration constraint may not create a hidden ledger residual, and dry-down may not erase dissolved mass simply because the aqueous coordinate ceases to be representable.

### `MineralPhosphorusState`

Owns aqueous PO4, fast sorption sites, slow sorption sites and precipitated P. Site-indexed stores remain site-indexed state rather than being flattened into totals.

`Toamcxfa` and `Toamcxsl` become derived views only. TCD-014, TCD-019, TCD-024 and the later TCD-029 evidence remain separate qualification seams: initialization projection, finite-change numerical closure, slow-site parameter indexing and multi-site management handling are different problems.

### `CropState`

Owns shoot/root dry matter and actual crop N and P when the crop option is active. Potential N/P quantities remain derived demand/reference state.

This makes soil-to-crop uptake an internal transfer for a combined soil+crop control volume while still allowing a soil-only ledger to view uptake as an outward boundary flux. Crop dry matter is not silently reinterpreted as elemental carbon.

### `GasState`

Owns the system CH4-C and N2O-N stores only when the GHG option is active. Water-phase concentrations remain derived phase views.

This is a candidate boundary only. Revision-53 GHG theory-to-ledger reconciliation is still incomplete, so ARCH01 does not define a qualified global elemental-C ledger from these fields.

### `MacroporeState`

Owns macropore water and dissolved solutes when macropores are active. Matrix/macropore exchange must be internal to a combined control volume and direct macropore drainage external.

The entire component remains feature-blocked for canonical admission because PREP06/TCD-025 found that the main legacy ledger does not expose the complete specialized control volume and the supplied testbank has no active macropore case.

### `DerivedViews`, `ProcessScratch`, `DiagnosticsLedger`

These are explicitly not physical state owners.

`DerivedViews` contains quantities such as site totals, phase concentrations, average concentrations and crop demand. They are recomputed from state and configuration.

`ProcessScratch` contains step-local rates and intermediate calculations. It is trial-local and discarded after the step.

`DiagnosticsLedger` observes state and typed transfer events. It cannot mutate physical state and cannot become a second source or sink. This removes the architectural failure mode behind TCD-017, TCD-018, TCD-026, TCD-027 and TCD-028, where legacy reporting structures can omit, duplicate or misbind real transfers without changing the underlying physical state.

## Accepted/trial separation

Every candidate persistent model state uses explicit accepted and trial/result semantics:

1. accepted state is read-only during a trial;
2. a trial state is initialized from accepted state plus the explicit forcing/exchange frame;
3. process routines mutate trial state only;
4. typed transfer events are written to the same trial transaction;
5. derived views are computed from the relevant accepted or trial snapshot;
6. rejection discards trial state, scratch and trial transfer journal;
7. commit atomically promotes the trial state and its transfer journal.

This preserves the revision-53 start/result seam identified by PREP06 without preserving legacy global-array ownership.

## Layout boundary

ARCH01 does not prescribe array-of-structures versus structure-of-arrays, a programming language, SIMD strategy or GPU layout. It only requires that component ownership and optional-feature activation be compatible with many independent columns and that inactive optional features do not require full persistent-state allocation where this can be avoided safely.

## Qualification boundary

This model is not the canonical `STATE` gate from `MIGRATION_DAG.md`. It is a prepared candidate for later qualification after `QM` exists. Open reference, GHG, macropore, corrected-legacy and B0-retention blockers remain unchanged.
