# ANIMO-MASSQ02 residual causality reconciliation

Status: `QUALIFIED_RESIDUAL_CAUSAL_RECONCILIATION_NO_UNEXPLAINED_MASS_ADMISSION_PENDING`.

## Scope and evidence identity

MASSQ02 follows ANIMO-MASSQ01 and preserves its observer-only boundary. This workunit does not alter physical state, correct residuals, introduce a mass-balance tolerance, mask a known TCD, allocate a new TCD identifier, or infer whole-system elemental-carbon closure from `Cfracom`.

Frozen evidence identity:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- deterministic B1 diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

The authoritative machine-readable residual register is `integration/animo-mass/MASSQ02_RESIDUAL_CLASSIFICATION.csv`.

## Final classification

All 23 non-zero MASSQ01/MASSQ02 residual records now have a causal or governed semantic classification. No residual is accepted by magnitude and no epsilon is used.

| class | count | interpretation |
| --- | ---: | --- |
| `KNOWN_TCD` | 6 | cause is already governed by an existing TCD |
| `REPORTING_SEMANTIC_DIFFERENCE` | 2 | legacy report and physical control-volume semantics differ without a missing physical boundary transfer |
| `CONTROL_VOLUME_MISMATCH` | 0 | none required in the final register |
| `TRANSACTION_BOUNDARY_MISMATCH` | 0 | rejected observer-boundary artifacts remain tooling archaeology, not physical residuals |
| `NEW_CAUSAL_FINDING` | 15 | a source/process-local causal seam is demonstrated; canonical allocation is deferred to governed incremental B3 intake |
| `UNEXPLAINED` | 0 | no remaining residual lacks causal localization |

This is residual reconciliation, not MASS admission. A causal explanation can identify a legacy nonclosure or reporting seam without making that behaviour acceptable.

## Existing governed discrepancies

MASSQ02 preserves the already qualified associations:

- TCD-014: CranGrass TITO 1 P initialization/first-`Transgen` seam, observer residual `-0.723582514679947 kg/ha P`;
- TCD-015: LWKM TITO 2312 N negative-concentration `Reko` algebra defect, observer residual `+0.5787119019951206 kg/ha N`;
- TCD-016: Puitmijn TITO 1490 NH4 dry-down state loss, `0.13880242022597072 kg/ha N`;
- TCD-019: LWKM run-scale recurring PO4 numerical-conservation drift, cumulative observer residual `-0.2725459891917126 kg/ha P`;
- TCD-025: MP02 synthetic matrix/macropore ledger integration gap for water and solute.

TCD-017 and TCD-018 remain `REPORTING_SEMANTIC_DIFFERENCE`, not physical balancing fluxes. Ploughing redistribution is physically internal even where `Bapo(Redi)` omits a reporting leg. Interception `Sic/Sict` is physical water state even though the public `Bawa` interface omits its storage change.

## Localized N and P findings

The residual reconciliation reproduces multiple N residuals directly in local process equations rather than only in whole-profile reporting. CranGrass TITO 726, CranMais TITO 1036, GrassPeat TITO 5224, LWKM TITO 8531, STONE TITO 2382 and Zuiderzeeland TITO 637 reproduce in `TRANSPORT.FOR:251-270`, often nitrate-dominated. These events are not automatically relabelled TCD-015 because a common local surface does not prove an identical branch mechanism.

Puitmijn TITO 1490 is explicitly composite. The total N observer residual `0.2240510811934655 kg/ha N` contains the known TCD-016 NH4 component `0.13880242022597072 kg/ha N` plus an independently localized layer-0 NO3 component of approximately `0.08524873053248594 kg/ha N`. The additional NO3 component is retained as a `NEW_CAUSAL_FINDING`.

For P, GrassPeat TITO 10, STONE TITO 10 and Zuiderzeeland TITO 1 reproduce in the first-step/`Transgen` initialization surface and are related to the TCD-014 family without assuming canonical identity. LWKM TITO 4503 and Puitmijn TITO 1490 reproduce in the local PO4 `Transgen` equation. The documented TCD-019 correction probe does not explain the LWKM target event, so MASSQ02 does not fold it into TCD-019.

The bounded LWKM TITO 3073 soil-organic-C residual is causally localized to dissolved-organic-matter transport and its source-defined `Cfracom=0.58` projection. This remains a soil-organic-C claim only. Crop dry matter, CO2 and CH4 are not silently merged into one elemental-C ledger.

## Final resolution of the two formerly unexplained records

### CranGrass TITO 724 water

MASSQ01 observer residual:

`-0.0030198960466805147 mm`.

An execution-only source-bound probe of the exact detailed hydrology balance at `Hydro_detailed.for:235-247` computes:

`Badev = -3.0198960463157789e-6 m`

or:

`-0.003019896046315779 mm`.

This directly reproduces the observer residual. The causal coordinate is therefore the ANIMO detailed whole-profile hydrology balance itself, using matrix water `Mofro/Mofrt`, ponding `Pn/Pnt`, snow `Snla/Snt`, interception `Sic/Sict`, and the accepted hydrologic boundary fluxes.

The separately observed input-hydrology `Wabaer` value of approximately `-0.01026848 mm` is not the coordinate that causes the MassLedger residual and is not used as a balancing term.

Classification changes from `UNEXPLAINED` to `NEW_CAUSAL_FINDING`. No new TCD is allocated here.

### RuurloGrass TITO 1915 N

MASSQ01 observer residual:

`+0.0067493732130969875 kg/ha N`.

The local dissolved-solute `TRANSPORT` mismatch is only about `-1.9e-14 kg/ha N`, so `TRANSPORT` is excluded as the material cause. The source-bound upper-boundary probe instead isolates `UBoundconc.for:110-132`.

At this interval:

- `Iopthyvs = 0`;
- `Flib(1) = 0` and `Rurv = 0`;
- therefore `Flux = Max(0, Flib(1)+Rurv) = 0`;
- the zero-throughflow branch selects `A1=1`, `A2=0`;
- `Rsconhtop` and `Rsconitop` retain the previous top-reservoir concentrations and the incoming `Load1/Load2` contribution is multiplied by zero.

At the same accepted interval `Outbal_calc.for:766-784` books precipitation/deposition N input from `Pr*Coprnhyn` and `Pr*Coprniyn`:

- NH4-N: `0.005069031338 kg/ha`;
- NO3-N: `0.00168034188 kg/ha`;
- sum: `0.006749373218 kg/ha N`.

That sum matches the observer residual to about `5e-12 kg/ha N`. The residual is therefore causally localized to a zero-top-throughflow upper-boundary concentration-reservoir seam: precipitation/deposition N is booked as system input but is not transferred into the represented top-reservoir concentration state on that branch.

Classification changes from `UNEXPLAINED` to `NEW_CAUSAL_FINDING`. MASSQ02 does not decide the scientific correction and allocates no new TCD.

## Observer independence from legacy balance accumulators

The observer equation remains:

`begin storage + external inputs + source terms - external outputs - end storage`.

Beginning/end storage are read from physical owner state. Transfer terms originate from source process coordinates. `Bawa`, `Banh`, `Bani`, `Bano`, `Bapp`, `Bapo`, `Bfom`, `Bahu`, `Bdom` and related arrays are comparison/report evidence only.

This independence is now stronger than in MASSQ01. Most N/P causal residuals reproduce locally in `TRANSPORT` or `Transgen`, the CranGrass water residual reproduces in `Hydro_detailed`, and the Ruurlo N residual reconstructs from `UBoundconc` state handling plus explicit precipitation/deposition input. None requires a legacy whole-profile balance accumulator as authoritative physical state or event owner.

## Natural coverage and feature limits

The natural evidence set remains the eight compatible B1 cases:

`CranGrass`, `CranMais`, `GrassPeat`, `LWKM_gras_1040.2021.2045`, `Puitmijn_Cranendonck_60`, `RuurloGrass`, `STONE_akk_0006.2001.2015`, and `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

MP02 is synthetic feature coverage only. The frozen natural testbank has no active macropore case.

GHG remains fail-closed incomplete because there is no compatible natural active-GHG B1 case with a complete qualified C/N owner-and-event topology.

Whole-system elemental-carbon closure remains unqualified.

## B3 intake boundary

The 15 `NEW_CAUSAL_FINDING` records require governed incremental B3 intake. MASSQ02 records exact evidence coordinates and candidate family relationships where justified, but it does not reopen a completed B3I02 register and does not allocate new canonical identifiers.

This is important for causality discipline. Similar symptoms are not silently merged into an existing TCD. The incremental intake must decide whether each finding is an existing TCD instance, child atom, new TCD, runtime hazard, observer artifact, or insufficient evidence.

## MASS gate readiness

Residual causality is now reconciled for the current MASSQ01 natural/synthetic evidence set: `UNEXPLAINED = 0`.

Canonical MASS nevertheless remains pending because:

1. 15 newly causal findings require governed incremental B3 intake;
2. existing governed TCDs that expose physical or ledger nonclosure remain unresolved for admission purposes;
3. the typed-event projection is a qualified candidate, not an implemented/admitted canonical runtime journal;
4. full executable soil+crop nested state-plus-event closure remains unqualified across all continuation/management transitions;
5. natural macropore feature coverage is absent;
6. GHG completeness is fail-closed;
7. whole-system elemental-carbon closure is not qualified.

MASSQ02 therefore supports the target status `QUALIFIED_TYPED_MASS_EVENT_PROJECTION_AND_RESIDUAL_RECONCILIATION_MASS_ADMISSION_PENDING` but does not admit canonical MASS, B3 corrections, or production migration.
