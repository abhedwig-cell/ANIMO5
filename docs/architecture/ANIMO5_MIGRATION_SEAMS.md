# ANIMO5 Candidate Migration Seams

Work unit: `ANIMO-ARCHG01`

Status: `CANDIDATE_MIGRATION_SEAMS_NOT_PRODUCTION_IMPLEMENTATION_PLAN`

A migration seam is the smallest boundary at which legacy behaviour can later be replaced behind already-qualified state, transfer, configuration and exchange contracts. A seam is not permission to migrate the process now.

## General seam contract

Every process seam must declare:

- ANIMO-owned input state;
- external-owner observations/forcing;
- trial state it may mutate;
- typed transfer events it may emit;
- derived/scratch outputs;
- required feature and configuration identities;
- B3 discrepancy/admission dependencies;
- NQ comparison/capture requirements;
- TQ coverage evidence;
- TS01 ordering/accepted-versus-trial dependencies;
- expected-difference policy;
- rollback and restart relevance.

A seam must not accept a legacy routine merely because its argument list has been wrapped.

## Hydrology exchange

**State owner:** external hydrology owner.

**ANIMO reads:** accepted/start and proposed/end water coordinates, interval water transfers, geometry and exchange identity.

**ANIMO emits:** solute/carrier `TransferEvent` records driven by the admitted transport contract. Water events may be observed from the external frame where needed for the water ledger.

**Migration boundary:** replace SWATRE/WATBAL/file-global access with one qualified immutable hydrology exchange adapter.

**Open gates:** TS01 coupled interval semantics; concrete adapter qualification; restart synchronization; active macropore extension if used.

**Readiness:** candidate seam defined, production implementation not admitted.

## Mineral nitrogen

**State owner:** `MineralNitrogenState`.

**Core state:** aqueous NH4, adsorbed NH4, aqueous NO3.

**Transfers:** sorption/desorption, nitrification, denitrification, crop uptake, deposition/addition, leaching/drainage/runoff, DOM/mineral exchange as qualified.

**Migration boundary:** process routines receive typed state views and emit events into the trial journal.

**Open gates:** TCD-015 negative-concentration handling and TCD-016 dry-down continuation require B3 qualification; TS01 ordering is required; NQ applies to numerical behaviour.

**Readiness:** candidate seam coherent, not production-ready.

## Phosphorus

**State owner:** `MineralPhosphorusState` plus P composition in organic/dissolved owners.

**Core state:** aqueous PO4, site-resolved fast sorption, site-resolved slow sorption, precipitated P.

**Transfers:** sorption/desorption, precipitation/dissolution, organic/mineral exchange, crop uptake, management, hydrological export/import.

**Migration boundary:** keep site identity explicit across initialization, management and runtime mutation.

**Open gates:** TCD-014 initialization projection, TCD-019 nonlinear numerical policy, TCD-024 slow-site parameter indexing, TCD-029 multi-site management semantics. Class E work must remain separate from architecture.

**Readiness:** not production-ready.

## Organic matter

**State owner:** `OrganicMatterState`.

**Core state:** fresh organic fractions, original humus, exudate-derived humus, root exudate organic matter.

**Transfers:** decomposition/assimilation, residue and manure additions, dissolved transfer, crop root/shoot returns, external export where physically defined.

**Migration boundary:** one source-of-truth owner model with typed reaction bundles. Beginning and end storage use the same state projection.

**Open gates:** GHG elemental-C reconciliation for any whole C ledger; discrepancy-specific B3 admissions. TCD-026 is accounting evidence, not automatic production correction.

**Readiness:** candidate seam defined, production correction/admission still separate.

## Crop

**State owner:** either ANIMO or external owner, never both.

**ANIMO mode:** `CropState` stores shoot/root dry matter and actual N/P state.

**External mode:** ANIMO consumes immutable crop observations/demand and returns realized uptake/events; residues/exudates/harvest/grazing use explicit transfer bundles.

**Migration boundary:** crop owner mode is fixed by normalized configuration and physical layout.

**Open gates:** TS01 coupled acceptance/rollback; concrete external crop adapter qualification; B3 qualification for process-specific discrepancies; split-run restart evidence.

**Readiness:** architecture-ready, implementation not admitted.

## Management

**State owner:** no persistent "management state" unless continuation evidence requires a scheduled-event cursor. Applied material becomes typed transfers into physical stores.

**Inputs:** immutable management-event frame bound by configuration and trial interval.

**Transfers:** additions, volatilization, redistribution/ploughing, harvest/grazing/export where the management contract owns the action.

**Migration boundary:** parser/schedule representation is separated from physical event emission.

**Open gates:** TS01 event ordering; P multi-site management semantics; B3 discrepancy classification; legacy parser compatibility.

**Readiness:** not production-ready.

## Dissolved organic matter

**State owner:** `DissolvedOrganicState` plus optional `SurfaceReservoirState`.

**Core state:** labile dissolved OM/N/P and later-admitted stable dissolved state.

**Transfers:** dissolution, decomposition, sorption/retardation where source-defined, hydrological transport, surface-reservoir exchange, cross-pool reactions.

**Migration boundary:** keep quantity/species explicit so P transfers cannot consume N amounts.

**Open gates:** stable-DOM provenance/theory, TCD-023, dormant surface stable DOM unsupported status, B3 admission.

**Readiness:** labile candidate seam coherent; stable-DOM production scope not admitted.

## GHG

**State owner:** candidate `GasState` only when an admitted GHG feature identity exists.

**Core state:** candidate system CH4-C and N2O-N stores; aqueous phase views are derived.

**Transfers:** only after theory-to-ledger reaction/conversion contracts define how organic matter, mineral N and gas quantities reconcile.

**Migration boundary:** no legacy GHG routine may be migrated merely by exposing its arrays.

**Open gates:** revision-53 theory/provenance, B3/scientific admission, compatible testcase lineage, TQ coverage, NQ where numerical choices matter.

**Readiness:** `NOT_PRODUCTION_READY`, theory-blocked.

## Macropores

**State owner:** candidate `MacroporeState` when feature is admitted.

**Core state:** macropore water and dissolved solute stores by qualified domain/layer structure.

**Transfers:** matrix/macropore exchange is internal to combined volume; direct macropore drainage is external; surface entry is explicit.

**Migration boundary:** full state plus transfer plus hydrology-exchange extension must be migrated as one qualified seam, not as an optional array tail.

**Open gates:** TCD-025, no supplied active historical case, B3 feature admission, external hydrology contract extension, restart and ledger qualification.

**Readiness:** `NOT_PRODUCTION_READY`.

## Sequencing boundary

ARCHG01 recommends no production migration before the shared candidate architecture is admitted through the project serial gates. Future process work may prepare fixtures, adapters, unit-level kernels, state mappings and comparison harnesses behind these seams, but integration into a canonical ANIMO5 runtime remains blocked until the relevant B3, STATE, TS01/TIME, MASS and EX gates are satisfied.
