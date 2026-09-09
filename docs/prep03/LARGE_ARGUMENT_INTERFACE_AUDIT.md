# ANIMO-PREP03 — Semantic audit of large legacy argument interfaces

Status: `SOURCE_BOUND_INTERFACE_DECOMPOSITION_EVIDENCE`.

## Purpose

PREP01 established that the supplied legacy source contains very long Fortran argument lists. PREP03 classifies what those lists mean architecturally.

The objective is not to reduce argument counts cosmetically. The objective is to identify ownership boundaries so later ANIMO5 interfaces can be smaller because state, parameters, forcing, diagnostics and process responsibilities are actually separated.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Alternate compilation units `input1_1.for` and `Outselorg.for` are excluded from the primary count because the current diagnostic build selects `input1.for` and `Outsel.for`.

## Inventory result

A source-signature scan found 137 routines/functions in the selected source units.

- 86 have at least 10 formal arguments;
- 61 have at least 20;
- 26 have at least 50;
- 10 have at least 100;
- 5 have at least 150;
- 2 have at least 200;
- maximum: 352;
- median: 16;
- mean: 33.54.

Largest interfaces:

| rank | routine | arguments |
| ---: | --- | ---: |
| 1 | `Input1` | 352 |
| 2 | `Outbal_calc` | 246 |
| 3 | `Inicalc` | 198 |
| 4 | `Init` | 194 |
| 5 | `Input_Echo` | 155 |
| 6 | `Outsel` | 143 |
| 7 | `Addit` | 140 |
| 8 | `Resp_miner` | 133 |
| 9 | `Aeration_original` | 105 |
| 10 | `GHGasses` | 102 |
| 11 | `Grassprd` | 94 |
| 12 | `Transca` | 91 |
| 13 | `GHG_Miner` | 84 |
| 14 | `Transgen` | 79 |
| 15 | `Hydro_detailed` | 78 |
| 16 | `GHG_Methane` | 72 |
| 17 | `UBoundconc` | 72 |
| 18 | `Input_hydro` | 69 |
| 19 | `Transport` | 69 |
| 20 | `Hydro_Aggregated` | 67 |

This is not concentrated in one parser. Large interfaces occur in input, initialization, transport, balances, mineralisation, aeration, crop growth and GHG physics.

## What the large lists represent

Inspection of the signatures shows repeated mixing of several distinct semantic families.

### Geometry and discretisation

Examples:

`Nl`, `He`, `Lnhn`, horizon mappings, root-zone bounds, macropore geometry.

Ownership implication: one immutable profile/discretisation description should be passed by reference, not repeated as loose scalars and arrays.

### Time and execution state

Examples:

`St`, `Tito`, `Tima`, year/day variables, period boundaries and reset state.

Ownership implication: time belongs in an explicit time-step context. Balance-period clocks and calendar policy should not be implicit side channels in unrelated process interfaces.

### Hydrology forcing and hydrologic state

Examples:

`Mofr`, `Mofro`, `Mofrt`, `Flib`, `Flio`, `Flou`, `Flev`, groundwater level and drainage terms.

Ownership implication: ANIMO5 should consume a typed hydrology exchange state/flux object. Hydrology input must remain physically separate from chemical state.

### Chemical state

Examples:

NH4, NO3, PO4, dissolved organic matter/N/P, sorbed stores, precipitated P and stable-DOM states.

Ownership implication: state should be organized by conserved species/pool and phase, with explicit units and storage ownership. One generic flat `model state` object would merely move the legacy coupling into a derived type.

### Organic matter/material parameters

Examples:

fractions, decomposition rates, assimilation factors, humus/exudate properties and C/N/P composition.

Ownership implication: immutable material/process parameters should not travel with mutable state unless the process genuinely needs both.

### Crop and management

Examples:

crop identifiers, root/shoot state, uptake demand, additions, tillage, P-class policy.

Ownership implication: management events and crop state need distinct owners. `Addit` is an event application seam, not the owner of every state array it can mutate.

### GHG extension state and parameters

Examples:

`IoptGHG`, `Cfracom`, CH4/N2O states, production/reduction rates, gas transport parameters and atmospheric boundary values.

Ownership implication: GHG is a separate process/state domain. Its later addition is one reason inherited core routines became wider.

### Macropore extension state and parameters

Examples:

`Srwamp`, `Vlmp`, `Flmp...`, wall-contact fractions and matrix exchange.

Ownership implication: matrix and macropore domains should have explicit exchange contracts instead of sharing one flat interface.

### Diagnostics, balance and I/O control

Examples:

`Outse`, `Outba`, units, file handles, error codes and balance accumulators.

Ownership implication: diagnostic/reporting state must not be required to compute physical process rates. Ledger accumulation should observe committed process fluxes rather than force physics routines to know output formatting.

## High-frequency cross-interface arguments

Across selected routines with at least 10 formal arguments, the most recurrent argument names include:

- `St` in 54 routines;
- `Nl` in 52;
- `He` in 48;
- `Mofr` in 34;
- `Tito` in 31;
- `Ipo` in 28;
- `Rhbd` in 23;
- `Tiyr` in 23;
- `Nuroup` in 22;
- `Flpn` and `Mofro` in 21;
- `Flev` in 21;
- `Mofrt` in 20.

This pattern is evidence of repeated transport of global model context through procedure boundaries. It does not mean those variables should be made global in ANIMO5.

## Routine-specific interpretation

### `Input1`, 352 arguments

This routine is effectively a parser plus whole-model construction interface. It mixes file/IO configuration, numerical switches, geometry, chemical parameters, initial states, crop/management parameters, GHG, macropores, P classes and stable DOM.

ANIMO5 migration rule: never reproduce this as one constructor with a derived-type argument for each old array. Split parsing from validated configuration construction, and split configuration by owner.

### `Outbal_calc`, 246 arguments

The balance calculator sees hydrology, chemistry, transformations, crop/addition terms, GHG terms and ledger arrays at once. PREP01 defects TCD-017 and TCD-018 already demonstrate why this is dangerous: balance completeness depends on whether every relevant process/store happened to be threaded into this interface.

ANIMO5 migration rule: the mass ledger should receive typed storage snapshots and typed committed flux/event ledgers from process owners. Adding a new physical store should not require editing a 246-argument call to remember it manually.

### `Inicalc` and `Init`, 198 and 194 arguments

Initialization mixes static parameter expansion, dynamic state initialization, calendar/crop policy, GHG state, stable DOM and P-class choices.

ANIMO5 migration rule: distinguish model construction, initial-condition projection/reconciliation and per-period reset. These are different semantic operations and should have different contracts.

### `Addit`, 140 arguments

The routine applies additions, residues and tillage across many state families. The organic-P bookkeeping defect TCD-017 shows that state mutation and diagnostic bookkeeping are intertwined but incompletely mirrored.

ANIMO5 migration rule: represent management operations as explicit conservative events that return a mass-transfer ledger. State mutation and balance evidence then derive from the same event object.

### `Aeration_original`, 105 arguments

The inherited aeration routine now also carries GHG-specific N2O controls. This is a concrete example of later feature growth widening an inherited scientific interface.

ANIMO5 migration rule: preserve the aeration/redox scientific contract, but use a narrow exchange object for rates needed by N transformations and GHG rather than coupling all GHG state directly into the aeration owner.

### `GHGasses`, 102 arguments

This is a later subsystem with its own large cross-domain context, including DOM/N state, hydrology, temperature, atmosphere, CH4/N2O process state and transport.

ANIMO5 migration rule: GHG should be decomposed internally into gas state, production/reduction, transport and boundary exchange, with explicit coupling to the C/N transformation owners.

## Candidate ANIMO5 ownership seams

The source evidence supports the following candidate interfaces. These are architecture hypotheses, not yet production code:

1. `ProfileGeometry`
2. `TimeStepContext`
3. `HydrologyExchange`
4. `CarbonPools`
5. `MineralNitrogenState`
6. `PhosphorusState`
7. `DissolvedOrganicState`, explicitly including labile/stable forms
8. `CropState` and `CropDemand`
9. `ManagementEvent`
10. `AerationRedoxState`
11. `GHGState` / `GHGFluxes`
12. `MacroporeState` / matrix-macropore exchange
13. `MassLedger`
14. `DiagnosticsView`

A single `AnimoState` may still exist as an owning aggregate, but process routines should receive only the subviews they own or consume.

## Anti-patterns to avoid

The audit specifically argues against three superficially easy migrations:

- replacing 352 scalar/array arguments with one unstructured mega-derived-type;
- moving the same data into module globals;
- mechanically shortening every interface before establishing which routine owns each mutation and conservation term.

All three would reduce line length without reducing semantic coupling.

## Qualification implications

For each future interface reduction, qualification must demonstrate:

- the same owned state is read and written;
- no previously implicit mutation is dropped;
- balance/event terms follow the same physical transfer;
- parameter versus state versus forcing ownership is explicit;
- unrelated process families are not pulled into the new interface merely for convenience;
- reference comparison is performed after each semantic seam, not after a broad rewrite.

## Gate

`SEMANTIC_INTERFACE_DECOMPOSITION_MAP_ESTABLISHED_NO_PRODUCTION_REFACTOR_ADMITTED`

This audit is architecture evidence only. No legacy source is changed and no ANIMO5 process migration is admitted.