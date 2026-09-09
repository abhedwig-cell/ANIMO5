# ANIMO-MASSQ02 residual causality reconciliation

Status: `QUALIFIED_RESIDUAL_CLASSIFICATION_WITH_TWO_UNEXPLAINED_CASES_MASS_ADMISSION_PENDING`.

## Scope

This workunit follows ANIMO-MASSQ01. It does not alter physical state, correct residuals, introduce a mass-balance tolerance, mask known discrepancies, allocate new TCD identifiers, or infer whole-system elemental-carbon closure from `Cfracom`.

Frozen evidence identity remains:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- reproduced deterministic B1 diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

The authoritative machine-readable classification is `integration/animo-mass/MASSQ02_RESIDUAL_CLASSIFICATION.csv`.

## Classification result

MASSQ02 re-evaluates the nonzero MASSQ01 residual evidence under the required classes:

| class | count | interpretation |
| --- | ---: | --- |
| `KNOWN_TCD` | 6 | cause is already governed by an existing TCD |
| `REPORTING_SEMANTIC_DIFFERENCE` | 2 | legacy report and physical control-volume semantics differ without requiring a physical balancing flux |
| `NEW_CAUSAL_FINDING` | 13 | a source/process-local causal seam is now demonstrated, but no new TCD is allocated here |
| `UNEXPLAINED` | 2 | deterministic residual remains without sufficiently isolated cause |

No residual is accepted by magnitude. No epsilon or tolerance is introduced.

## Existing TCD reconciliation

### TCD-014

CranGrass TITO 1 P remains the qualified initialization/first-Transgen seam at `-0.723582514679947 kg/ha P`. The state coordinates are the supplied `INPO=1` coupled P stores and their first-step projection through `Inicalc` and `Transgen`.

### TCD-015

LWKM TITO 2312 N remains the exact negative-concentration `Reko` algebra defect. The independent causal identity is the duplicated `Avc*Hv` contribution, matching the observer residual of `+0.5787119019951206 kg/ha N`.

### TCD-016

Puitmijn TITO 1490 contains the already qualified NH4 dry-down loss of `0.13880242022597072 kg/ha N`. MASSQ02 does not turn this into an export or retained state.

### TCD-019

The LWKM run-scale P drift remains associated with the qualified nonlinear PO4 conservation-policy seam. The observed cumulative residual is `-0.2725459891917126 kg/ha P`. That value is evidence, not a tolerance.

### TCD-025

MP02 remains synthetic B1 evidence only. It confirms that the combined matrix/macropore water and solute control volumes require macropore storage and direct drainage. No natural macropore feature admission follows.

## Reporting semantic differences

TCD-018 and TCD-017 are retained separately from physical nonclosure.

For TCD-018, `Sic/Sict` is physical interception storage and belongs in the detailed water control volume, while the public `Bawa` interface omits the storage change. The observer must therefore retain interception state without inventing a hydrological flux.

For TCD-017, ploughing redistribution is a physical internal transfer. `Addit` exposes both source loss and destination gain, whereas the legacy organic-P reporting path omits the top-reservoir leg. The physical event remains net zero over the encompassing control volume.

## Newly localized N findings

Several MASSQ01 N residuals now reproduce directly in the local dissolved-solute transport mass equation rather than only in whole-profile reporting.

- CranGrass TITO 726: observer `+0.0038163099216035334 kg/ha N`; independent local `TRANSPORT` sum `+0.0038163099170967787`, with layer-0 DON, NH4 and NO3 components.
- CranMais TITO 1036: observer `-3.2822208595462143e-6 kg/ha N`; local transport `-3.2822245765048552e-6`, dominated by layer-6 nitrate.
- GrassPeat TITO 5224: observer `+0.29986345767974854 kg/ha N`; local transport `+0.2998634577479425`, concentrated in nitrate layers 1 and 2 and coincident with the source zero-order adjustment path.
- LWKM TITO 8531: observer `+0.5842666837997967 kg/ha N`; local transport `+0.5842666837650191`, dominated by layer-1 nitrate.
- STONE TITO 2382: observer `+0.023667581954214256 kg/ha N`; local transport `+0.023667581953343442`, dominated by layer-6 nitrate.
- Zuiderzeeland TITO 637: observer `+7.479684427380562e-8 kg/ha N`; local transport approximately `+7.484243194963797e-8`, again nitrate-dominated.

These findings demonstrate a local causal surface. They do not by themselves prove that every event is the same TCD-015 mechanism. MASSQ02 therefore records candidate relations where appropriate but leaves canonical allocation to the B3 intake process.

Puitmijn TITO 1490 is explicitly composite. The total N observer residual is `0.2240510811934655 kg/ha N`. The known TCD-016 NH4 component is `0.13880242022597072`; an additional layer-0 NO3 contribution of approximately `0.08524873053248594 kg/ha N` is independently localized. That NO3 component is a new causal finding and is not silently folded into TCD-016.

## Newly localized P findings

MASSQ02 also reproduces four previously unassigned P residuals in the local `Transgen` mass equation.

GrassPeat TITO 10, STONE TITO 10 and Zuiderzeeland TITO 1 are first-step/initialization-associated cases. In each case `INPO=1` exposes coupled solution and sorption state, and the source reports supplied slow-site values inconsistent with `Copo`. They are related to the TCD-014 initialization family, but case-specific canonical identity is not assumed without B3 intake.

LWKM TITO 4503 and Puitmijn TITO 1490 reproduce in the local PO4 `Transgen` equation. The documented TCD-019 tangent/Newton correction probe does not explain the LWKM target event, so MASSQ02 deliberately does not relabel it as TCD-019. Puitmijn is likewise retained as a new causal P finding rather than being inferred from the same-step N dry-down event.

## Bounded organic-C finding

LWKM TITO 3073 has a bounded soil-organic-C observer residual of `-2.8300704434514044e-5 kg/ha C`. An independent dissolved-organic-matter transport mismatch is approximately `-4.8794859983485134e-5 kg/ha OM`. Multiplication by the source-defined `Cfracom=0.58` gives approximately `-2.8301018790421378e-5 kg/ha C`, reproducing the scale and sign of the bounded observer residual.

This establishes a causal transport surface for the bounded soil-organic-C projection only. It does not establish one elemental-C ledger spanning crop dry matter, CO2 and CH4.

## Residuals still unexplained

Two records remain `UNEXPLAINED`.

### CranGrass TITO 724 water

Observer residual: `-0.0030198960466805147 mm`.

The owner coordinates are matrix water `Mofro/Mofrt`, ponding `Pn/Pnt`, snow `Snla/Snt`, interception `Sic/Sict`, and the source-bound hydrology transfers in `Input_hydro/Hydro_detailed`. The independent detailed-water diagnostic `Wabaer` at the same interval is approximately `-0.01026848 mm`, so it does not directly explain the observer residual. A unique omitted state or transfer coordinate has not yet been isolated.

### RuurloGrass TITO 1915 N

Observer residual: `+0.0067493732130969875 kg/ha N`.

The local `TRANSPORT` mass-equation mismatch is only about `-1.9e-14 kg/ha N`, excluding the dissolved-solute transport equation as the material cause. The residual therefore lies in another process transfer, transaction boundary, or observer projection seam. The legacy NH4/NO3 whole-profile reports reproduce approximately the same total nonclosure, so the residual is not dismissed as a MassLedger-only artifact.

Both findings remain admission blockers. No balancing event is synthesized.

## Relation to B3I02

The completed ANIMO-B3I02 intake was based on MASSQ01 and explicitly classified MASSQ01-R010 through MASSQ01-R024 as local observer findings pending causality. It also explicitly excluded then-in-progress MASSQ02 from its completed intake scope.

MASSQ02 now supplies new causal evidence for 13 of those records. Because B3I02 is already closed and this workunit is forbidden to allocate new TCD identifiers, these 13 findings are routed to the next governed incremental B3 intake. MASSQ02 does not reopen or mutate the canonical register itself.

## Observer independence from legacy balance accumulators

The closure equation remains:

`begin storage + external inputs + source terms - external outputs - end storage`.

Beginning and ending storage come from physical owner state. Boundary/process transfers come from source variables and local process coordinates. `Bawa`, `Banh`, `Bani`, `Bano`, `Bapp`, `Bapo`, `Bfom`, `Bahu`, `Bdom` and related arrays are comparison/report evidence only.

This independence is strengthened by the MASSQ02 causal traces. Most newly localized N and P residuals reproduce inside `TRANSPORT` or `Transgen` before whole-profile public balance accumulation. The legacy balance accumulators are therefore neither required state owners nor required causal oracles for the observer closure.

## Natural coverage and feature limits

All eight compatible natural B1 cases from MASSQ01 remain the natural evidence set:

`CranGrass`, `CranMais`, `GrassPeat`, `LWKM_gras_1040.2021.2045`, `Puitmijn_Cranendonck_60`, `RuurloGrass`, `STONE_akk_0006.2001.2015`, and `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

MP02 is used only for synthetic macropore feature coverage. GHG remains fail-closed incomplete because there is no compatible natural active-GHG B1 case and no complete qualified GHG C/N event topology. Whole-system elemental C remains unqualified.

## MASS gate readiness

The residual observer and causal-reconciliation machinery are sufficiently qualified to support a candidate typed event projection and further MASS admission work. They are not sufficient to admit canonical MASS.

Current blockers are:

1. CranGrass TITO 724 water remains unexplained;
2. RuurloGrass TITO 1915 N remains unexplained;
3. 13 newly causal findings require governed B3 intake before any new canonical discrepancy relation is asserted;
4. full executable nested soil+crop closure is not yet qualified as one complete state-plus-event balance;
5. natural macropore feature coverage is absent;
6. GHG completeness is fail-closed;
7. whole-system elemental-carbon closure is not qualified;
8. the candidate typed-event model is not yet a canonical runtime event journal.

Therefore no MASS admission is made by MASSQ02.
