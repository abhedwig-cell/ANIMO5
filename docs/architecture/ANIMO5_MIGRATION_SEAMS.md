# ANIMO5 Candidate Migration Seams

Work unit: `ANIMO-ARCHG01`

Status: `CANDIDATE_MIGRATION_SEAMS_POST_TS01_REVALIDATED_NOT_PRODUCTION_IMPLEMENTATION_PLAN`

A migration seam is the smallest boundary at which legacy behaviour can later be replaced behind qualified state, transfer, configuration, exchange and temporal-preservation contracts. A seam is not permission to migrate the process now.

## General seam contract

Every process seam must declare:

- ANIMO-owned input state;
- external-owner observations/forcing;
- exact read generation for temporally sensitive inputs;
- trial state it may mutate;
- typed transfer events it may emit;
- provisional versus actual outputs;
- derived/scratch outputs;
- required feature/configuration identities;
- event endpoint and ordering semantics where applicable;
- `Sqnu` or other source-observable traversal dependencies where applicable;
- B3 discrepancy/admission dependencies;
- NQ comparison/capture requirements;
- TQ coverage evidence;
- expected-difference policy;
- rollback/restart relevance.

A seam must not accept a legacy routine merely because its argument list has been wrapped.

## Hydrology exchange

**State owner:** external hydrology owner.

**ANIMO reads:** accepted/start and proposed/end water coordinates, interval water transfers, geometry and exchange identity.

**ANIMO emits:** solute/carrier `TransferEvent` records driven by the admitted transport contract. Water events may be observed from the external frame where needed for the water ledger.

**Migration boundary:** replace SWATRE/WATBAL/file-global access with one qualified immutable hydrology exchange adapter.

**TS01 constraint:** hydrology records are consumed sequentially and source audit found no explicit per-record equality assertion between the hydrology timestamp and already advanced ANIMO interval time. A modern adapter must validate interval/time identity explicitly.

**Open gates:** concrete adapter qualification, canonical coupled TIME/retry semantics, restart synchronization, active macropore extension if used.

**Readiness:** candidate seam defined, production implementation not admitted.

## Mineral nitrogen

**State owner:** `MineralNitrogenState`.

**Core state:** aqueous NH4, adsorbed NH4, aqueous NO3.

**Transfers:** sorption/desorption, nitrification, denitrification, crop uptake, deposition/addition, leaching/drainage/runoff, DOM/mineral exchange as qualified.

**Migration boundary:** process routines receive explicit state-generation views and emit events into the trial journal.

**TS01 constraints:** same-step management is visible before process rates; potential NH4 transport precedes aeration; actual NH4 transport precedes NO3 source construction; `Resp_miner` may read previous-step neighbour NH4; generic transport follows `Sqnu` order.

**Open gates:** TCD-015 negative-concentration handling, TCD-016 dry-solute continuation, discrepancy-specific B3 qualification and NQ for changed numerical behaviour.

**Readiness:** candidate seam coherent, not production-ready.

## Phosphorus

**State owner:** `MineralPhosphorusState` plus P composition in organic/dissolved owners.

**Core state:** aqueous PO4, site-resolved fast sorption, site-resolved slow sorption, precipitated P.

**Transfers:** sorption/desorption, precipitation/dissolution, organic/mineral exchange, crop uptake, management, hydrological export/import.

**Migration boundary:** keep site identity explicit across initialization, management and runtime mutation.

**TS01 constraints:** P transport, fast/slow sorption and precipitation/dissolution are coupled per layer through `Transgen/Transorp`; same-step average P can propagate in `Sqnu` order; previous-step neighbour P can be used by `Resp_miner` availability logic. No global reorderable all-transport/all-sorption split is source-equivalent by assumption.

**Open gates:** TCD-014 initialization projection, TCD-019 nonlinear numerical policy, TCD-024 slow-site parameter indexing, TCD-029 multi-site management semantics, and `Output_Init` phosphorus clamp compatibility.

**Readiness:** not production-ready.

## Organic matter

**State owner:** `OrganicMatterState`.

**Core state:** fresh organic fractions, original humus, exudate-derived humus, root exudate organic matter.

**Transfers:** decomposition/assimilation, residue and manure additions, dissolved transfer, crop root/shoot returns, external export where physically defined.

**Migration boundary:** one source-of-truth owner model with typed reaction bundles. Beginning and end storage use the same state projection.

**TS01 constraints:** distinguish potential versus actual `Transca/Resp_miner`; potential results remain provisional; same-step residue/management mutation precedes later process calculations.

**Open gates:** GHG elemental-C reconciliation for whole C ledger and discrepancy-specific B3 admissions. TCD-026 remains accounting evidence, not automatic production correction.

**Readiness:** candidate seam defined, production correction/admission separate.

## Crop

**State owner:** either ANIMO or external owner, never both.

**ANIMO mode:** `CropState` stores shoot/root dry matter and actual N/P state.

**External mode:** ANIMO consumes immutable crop observations/demand and returns realized uptake/events; residues/exudates/harvest/grazing use explicit transfer bundles.

**Migration boundary:** crop owner mode is fixed by normalized configuration and physical layout.

**TS01 constraints:** crop demand/selectivity occurs before transport; soil-side uptake sink occurs inside transport; plant-side `Upintg_*` later integrates the same realized transfer. Annual harvest/root-residue uses `[t0,t1)` and crop identity can differ at `t0` and `t1`.

**Open gates:** canonical coupled acceptance/rollback, concrete external crop adapter qualification, B3 qualification for process-specific discrepancies, split-run reference evidence.

**Readiness:** architecture-ready, implementation not admitted.

## Management

**State owner:** no persistent generic management physical state. Continuation may require an event/schedule cursor in orchestration metadata.

**Inputs:** immutable management-event frame bound by configuration and interval.

**Transfers:** additions, volatilization, redistribution/ploughing, harvest/grazing/export where the management contract owns the action.

**Migration boundary:** parser/schedule representation is separated from physical event emission.

**TS01 constraints:** management packets use `(t0,t1]`; same-row material addition precedes ploughing; same-step applied material is visible to downstream chemistry; event cursor continuation matters for restart equivalence.

**Open gates:** canonical TIME/event scheduler, P multi-site management semantics, B3 discrepancy classification, legacy parser compatibility, split-run reference evidence.

**Readiness:** not production-ready.

## Dissolved organic matter

**State owner:** `DissolvedOrganicState` plus optional `SurfaceReservoirState`.

**Core state:** labile dissolved OM/N/P and later-admitted stable dissolved state.

**Transfers:** dissolution, decomposition, sorption/retardation where source-defined, hydrological transport, surface-reservoir exchange, cross-pool reactions.

**Migration boundary:** keep quantity/species explicit so P transfers cannot consume N amounts.

**TS01 constraints:** top-reservoir additions can be visible to same-interval `UBoundconc`; transport order and same-step propagation remain source-observable.

**Open gates:** stable-DOM provenance/theory, TCD-023, dormant surface stable DOM unsupported status, B3 admission.

**Readiness:** labile candidate seam coherent; stable-DOM production scope not admitted.

## GHG

**State owner:** candidate `GasState` only when an admitted GHG feature identity exists.

**Core state:** candidate system CH4-C and N2O-N stores; aqueous phase views are derived.

**Transfers:** only after theory-to-ledger reaction/conversion contracts define how organic matter, mineral N and gas quantities reconcile.

**TS01 constraint:** preliminary and final GHG calls occupy different points around potential/actual processing. Reachable source ordering is evidence, not sufficient scientific admission.

**Open gates:** revision-53 theory/provenance, B3 scientific admission, compatible testcase lineage, TQ coverage and NQ where numerical choices matter.

**Readiness:** `NOT_PRODUCTION_READY`, theory-blocked.

## Macropores

**State owner:** candidate `MacroporeState` when feature is admitted.

**Core state:** macropore water and dissolved solute stores by qualified domain/layer structure.

**Transfers:** matrix/macropore exchange is internal to combined volume; direct macropore drainage is external; surface entry is explicit.

**Migration boundary:** full state plus transfer plus hydrology-exchange extension must be migrated as one qualified seam, not as an optional array tail.

**TS01 constraint:** source temporal reconstruction covers reachable macropore branches but no supplied historical case naturally exercises active macropore behaviour; `Output_Init` macropore serialization is commented out.

**Open gates:** TCD-025, active-path scientific/theory qualification, external hydrology contract extension, restart and ledger qualification, reference evidence.

**Readiness:** `NOT_PRODUCTION_READY`.

## Sequencing boundary

TS01 now reconstructs legacy source order, but that does not admit a production scheduler. Future work may prepare fixtures, adapters, typed state views, event producers and comparison harnesses behind these seams. Integration into a canonical ANIMO5 runtime remains blocked until relevant B3, STATE, TIME, MASS, EX, numerical and reference gates are satisfied.
