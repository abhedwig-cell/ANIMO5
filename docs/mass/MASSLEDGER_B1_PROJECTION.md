# ANIMO-MASSQ01 B1 MassLedger projection

Decision: `QUALIFIED_MASSLEDGER_OBSERVER_PROJECTION_B1_NONREFERENCE_MASS_GATE_NOT_ADMITTED`.

Evidence class: `B1_DIAGNOSTIC_OBSERVER_NOT_REFERENCE`.

This workunit qualifies an observer-only MassLedger projection over the existing revision-53 diagnostic execution surface. It does not repair the legacy model, does not define a mass-balance tolerance, does not turn a B1 diagnostic into B2 reference evidence, and does not admit canonical MASS, B3 or production migration.

## 1. Evidence identity

The workunit is based on the RG02-G5 attached evidence lineage and the frozen ANIMO artifacts:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- reproduced baseline GNU diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

The physical source/testbank artifacts were not modified. Observer instrumentation was applied only to execution copies and writes sidecar diagnostics.

Pinned design/evidence inputs are PREP06 conserved-state and transfer identities, ARCH03 control-volume/MassLedger semantics, ARCHG01/02 architecture reconciliation, TQ01 B1 execution qualification, MP02 synthetic macropore evidence and GHG01 source/runtime qualification limits.

## 2. Observer equation and ownership rule

For each selected control volume and conserved quantity MASSQ01 records:

`begin storage + external inputs + source terms - external outputs - end storage`.

Storage is reconstructed from source-bound owner state. `Bawa`, `Banh`, `Bani`, `Bano`, `Bapp`, `Bapo`, `Bfom`, `Bahu`, `Bdom` and related reporting arrays are not used as authoritative physical storage.

Internal transfers cancel when both endpoints belong to the selected control volume. Crop uptake is external for soil-only views and would become internal in a soil+crop view. Matrix/macropore exchange is external to a matrix-only view and internal to the combined matrix+macropore view.

The observer never creates a compensating flux for a residual. Constraint/state-model losses such as TCD-015 and TCD-016 remain visible as nonclosure.

## 3. Transaction-boundary qualification

A key result of MASSQ01 is that one universal post-`Init` beginning-state snapshot is not valid for every conserved quantity.

`Init.for` promotes matrix moisture only for layers `1:Nl`, but promotes NH4, NO3 and dissolved-organic concentrations for layers `0:Nl`. Consequently a chemical storage reconstruction immediately after `Init` can combine new layer-0 concentrations with stale `Mofro(0)`. Wet/dry surface transitions then appear as large fictitious mass creation or loss.

The first observer version exposed exactly this problem. Apparent residual clusters included:

- GrassPeat TITO 1704: N `-8.276164955692366 kg/ha`;
- STONE TITO 1530: N `-4.90885883878218 kg/ha`;
- Zuiderzeeland TITO 473: N `-2.3146104119950905 kg/ha`.

A layer-0 diagnostic predicted these jumps from the moisture-coordinate mismatch alone as respectively `-8.27616495572782`, `-4.908858838774846` and `-2.314610412007279 kg/ha N`. P and organic-matter jumps reconcile in the same way.

These were observer-boundary artefacts, not new physical defects. They were removed from the residual register and were not assigned canonical TCD identifiers.

The qualified B1 observer therefore uses:

- `massq01_start.dat` for hydrological beginning storage;
- `massq01_chem_start.dat`, captured after hydrology/crop preparation and before `Addit`, for N, P and organic-matter beginning storage;
- `massq01_step.dat` for external/source terms and end-state projection.

`tools/analyze_massledger_b1_sidecars.py` fails closed when these snapshots are missing or timestep/feature flags disagree. The analyzer has six focused tests covering split-boundary use, preservation of nonclosure, missing-snapshot failure and the C projection.

## 4. Control-volume coverage

The qualified observer projection covers the following B1 views.

### Water

`CV-HYDRO-PROFILE` includes matrix water in layers `1:Nl` plus the route-specific ponding/surface-water, snow and interception stores. Boundary inputs/outputs include precipitation, irrigation, runon/inundation, evaporation, runoff, drainage and lower-boundary exchange.

TCD-018 remains a reporting-only difference: the public ANIMO water ledger omits interception storage while the physical detailed-hydrology state contains it.

### Nitrogen

`CV-SOIL-N` includes aqueous and adsorbed NH4, NO3, labile/stable DON, N in solid organic stores and source-defined surface/top reservoirs. External boundaries include deposition/material input, external crop return, runoff/leaching/drainage, volatilization, crop uptake and denitrification when gas state is not inside the selected view.

### Phosphorus

`CV-SOIL-P` includes aqueous PO4, fast/slow sorbed P, precipitated P, dissolved organic P and P carried by solid organic stores. Sorption and precipitation are internal phase transfers. TCD-014, TCD-017, TCD-019 and TCD-024 remain separate mechanisms.

### Organic matter and soil organic C

`CV-SOIL-OM` observes explicit organic-matter storage and OM boundary/reaction losses.

Revision 53 reads `Cfracom` under `>orgcom:` as the organic C content. MASSQ01 therefore defines a bounded `CV-SOIL-ORGANIC-C` view as:

`soil organic C quantity = Cfracom * corresponding OM quantity`.

All eight compatible natural B1 cases resolve `Cfracom = 0.58` from their active material input. The analyzer reads this value rather than hard-coding it.

This is not a whole-system elemental-C ledger. Crop dry matter and CH4-C remain separate quantity contracts. GHG-linked whole-system C closure is not claimed.

### Crop/external-owner boundaries

Crop-to-soil residue return and soil-to-crop nutrient uptake are observed as external boundaries for soil-only views. A sensitivity probe showed that direct crop state delta is not universally equivalent to the interval uptake transfer because crop routines reset/partition state around growth and harvest logic. Soil+crop nested closure is therefore mapped but not claimed as runtime-qualified.

### Surface reservoirs

Ponding/surface water, snow, interception, chemical layer 0 and top dissolved reservoirs are kept as distinct owner coordinates. They are not collapsed into a reporting-only surface bucket.

## 5. Eight natural B1 cases

All eight compatible natural cases completed with the corrected observer projection. No acceptance tolerance is applied to the residuals.

| case | water max abs mm | N max abs kg/ha | P max abs kg/ha | soil organic C max abs kg/ha |
| --- | ---: | ---: | ---: | ---: |
| CranGrass | 0.00301989604668 | 0.00381630992160 | 0.723582514680 | 2.57063831668e-5 |
| CranMais | 5.92584128754e-5 | 3.28222085955e-6 | inactive | 2.02562659979e-10 |
| GrassPeat | 7.45869256207e-5 | 0.299863457680 | 0.00171616832813 | 1.08033418655e-8 |
| LWKM_gras_1040.2021.2045 | 0.000235163600337 | 0.584266683800 | 0.00134024659565 | 2.83007044345e-5 |
| Puitmijn_Cranendonck_60 | 6.56995316604e-5 | 0.224051081193 | 0.0133329241853 | 1.49457482621e-7 |
| RuurloGrass | 7.13157496648e-5 | 0.00674937321310 | inactive | 1.08033418655e-9 |
| STONE_akk_0006.2001.2015 | 8.39964932311e-5 | 0.0236675819542 | 0.00243889995181 | 5.40167093277e-10 |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 7.40847108318e-5 | 7.47968442738e-8 | 0.0259910714594 | 5.40167093277e-9 |

These maxima are evidence, not acceptance limits. A nonzero value remains nonzero unless independently classified.

## 6. Known-discrepancy visibility

The observer reproduces known discrepancies without correcting them.

### TCD-014

CranGrass TITO 1 independently reconstructs:

`-0.723582514679947 kg/ha P`.

The projection uses owner state plus transfers, not public P balance storage.

### TCD-015

LWKM TITO 2312 reconstructs:

`+0.5787119019951206 kg/ha N`.

This matches the previously source-localized negative-concentration `Reko` nonclosure to floating-point arithmetic noise.

### TCD-016

At Puitmijn TITO 1490 the known NH4 dry-down loss of `0.13880242022597 kg/ha N` remains an explicit TCD-associated component. The corrected total-N observer residual for that interval is `0.2240510811934655 kg/ha N`; the remainder is not explained away and remains local/unassigned.

### TCD-017 and TCD-018

These remain `LEGACY_REPORTING_ONLY_DIFFERENCE`: the physical control-volume interpretation differs from incomplete/misaccumulated public reporting, without changing physical state.

### TCD-019

LWKM cumulative observed P residual is `-0.2725459891917126 kg/ha P`, consistent with the independently qualified recurring nonlinear-sorption conservation seam. This is not used as a tolerance.

## 7. Local unexplained residuals

MASSQ01 deliberately retains unassigned residuals. Examples include:

- GrassPeat TITO 5224 N `+0.29986345767974854 kg/ha`;
- STONE TITO 2382 N `+0.023667581954214256 kg/ha`;
- RuurloGrass TITO 1915 N `+0.0067493732130969875 kg/ha`;
- Zuiderzeeland TITO 1 P `-0.025991071459429804 kg/ha`.

Independent per-step legacy diagnostics reproduce several of these values. For example GrassPeat Bani at TITO 5224 is `+0.2998634577478822 kg/ha`, and STONE Bani at TITO 2382 is `+0.023667581953337291 kg/ha`. Therefore those residuals are not artefacts introduced by the MassLedger mapping. Their exact canonical cause was not independently qualified in this workunit.

They remain `UNEXPLAINED_RESIDUAL` with MASSQ01-local finding identifiers. No new canonical TCD is allocated.

## 8. Observer non-interference

Observer-on and observer-off output trees were compared for all eight natural B1 cases.

- cases compared: `8`;
- physical output files compared: `379`;
- raw byte-equal: `279`;
- equal after declared volatile metadata normalization: `100`;
- scientific/output differences: `0`;
- missing/extra physical outputs: `0`.

The only permitted normalization is the already governed legacy timestamp/elapsed-CPU normalization. Scientific numeric values are not tolerance-filtered.

Decision:

`PASS_NO_PHYSICAL_OUTPUT_DIFFERENCE_AFTER_DECLARED_VOLATILE_NORMALIZATION`.

This establishes observer non-interference for the exercised B1 diagnostic scope.

## 9. Macropore synthetic B1

Natural testbank coverage remains zero for active macropores. MASSQ01 therefore uses MP02 only as explicitly synthetic B1 evidence.

MP02 shows that:

- matrix-to-macropore exchange plus matching macropore storage can occur while the public water balance remains unchanged;
- direct macropore drainage can be hidden when both omitted storage change and omitted drainage cancel in the public view;
- public N/P/DOM residuals can shift when matrix storage changes but macropore solute storage is absent from the public ledger;
- the specialized macropore balance itself can close.

The combined observer control volume must therefore include `SrWaMp` and `SrWaMp * CoMp/RsCoMp` storage plus direct drainage. This remains TCD-025 synthetic B1 evidence. It is not B2 and does not admit a production macropore ledger.

## 10. GHG coverage

GHG coverage remains explicitly incomplete.

The supplied `GHGMais` case is not compatible with the revision-53 parser/input contract, so there is no compatible natural active-GHG B1 execution in the supplied bank. GHG01 also identifies hidden task/restart state and incomplete model-wide C/N ledger coupling.

MASSQ01 therefore maps CH4/N2O ownership but does not claim full GHG C/N closure. This limitation is compatible with the workunit contract and is not converted into a pass or failure residual.

## 11. Observer record contract

`integration/animo-mass/MASSLEDGER_OBSERVER_RECORDS.csv` persists normalized representative runtime records with:

- interval;
- control volume;
- element/quantity;
- store;
- transfer identity;
- source owner;
- destination owner;
- sign;
- quantity;
- units;
- evidence source.

The current B1 execution-copy sidecar aggregates some physical boundary terms by interval. It therefore qualifies the observer projection, not the future canonical typed-event journal.

## 12. Qualification decision

The evidence is sufficient to qualify the **B1 nonreference observer projection** because:

1. beginning/end storage is reconstructed from physical owner state rather than legacy balance arrays;
2. the quantity-specific transaction boundary is source- and runtime-qualified;
3. all eight compatible natural B1 cases execute with the observer;
4. observer-on/off non-interference is demonstrated over 379 physical outputs;
5. known TCD residuals remain visible rather than being repaired or hidden;
6. unexplained residuals are retained without invented tolerance or new canonical TCD allocation;
7. soil organic C is explicitly bounded through source-defined `Cfracom`, without silently absorbing crop/CH4 carbon;
8. surface, crop boundary and synthetic macropore ownership are explicitly represented;
9. GHG limits are explicit rather than overstated.

Therefore the workunit status is:

`QUALIFIED_MASSLEDGER_OBSERVER_PROJECTION_B1_NONREFERENCE_MASS_GATE_NOT_ADMITTED`.

This status does **not** mean that every revision-53 conservation residual is explained or acceptable. It means the observer projection is qualified to expose B1 conservation evidence without interfering with the model and without becoming a reference or production ledger.

Canonical MASS remains `NOT_ADMITTED`. B2 reference qualification remains absent. B3 and production migration remain closed.
