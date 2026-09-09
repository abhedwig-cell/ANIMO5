# ANIMO-MASSQ02 candidate typed transfer event contract

Status: `QUALIFIED_CANDIDATE_TYPED_EVENT_PROJECTION_NOT_CANONICAL_RUNTIME_JOURNAL`.

The machine-readable candidate is `integration/animo-mass/TYPED_EVENT_PROJECTION.json`.

## Purpose

PREP06 establishes that conserved-state ownership and process transfers are distributed through legacy ANIMO, while public balance arrays are reporting surfaces rather than physical state owners. MASSQ01 qualified a non-interfering B1 observer above that surface. MASSQ02 projects those source-bound transfers into a candidate typed-event model without changing physical state or introducing a second hidden state machine.

The candidate is a qualification contract. It is not yet the ANIMO5 production event bus and is not a MASS admission.

## Required event fields

Every candidate event has:

| field | contract |
| --- | --- |
| `time_interval` | exact accepted interval identity; no hidden epsilon |
| `element` | conserved quantity, normally water, N, P, or explicitly qualified C |
| `species_pool` | physical species or pool carrying the quantity |
| `amount` | non-negative scalar transfer magnitude |
| `unit` | explicit conserved-quantity unit |
| `source_owner` | physical source owner or external boundary owner |
| `destination_owner` | physical destination owner or external boundary owner |
| `internal_external` | derived from owner membership in the declared system boundary |
| `process` | process causing the transfer |
| `evidence_coordinate` | source routine/state/transfer coordinate or qualified synthetic coordinate |

Direction is encoded only by `source_owner -> destination_owner`; negative `amount` is invalid. Candidate owner names use `animo.*` for internal owners and `external.*` for external boundaries.

## Exact conservation rules

For a transfer amount `q >= 0`:

`delta(source_owner) = -q`

`delta(destination_owner) = +q`.

If both owners belong to the selected combined control volume, the event contribution is exactly:

`-q + q = 0`.

No tolerance is part of this identity.

A system-external event is valid only when exactly one endpoint is internal:

`XOR(internal(source_owner), internal(destination_owner)) = true`.

Therefore one external event represents exactly one system-boundary crossing. Events with two external endpoints, equal source/destination, negative amount, or missing evidence coordinates are invalid.

A physical interface transfer is emitted once. Two independently signed layer records are forbidden because they can double count one internal edge or allow the two sides to diverge.

## Projection to narrower control volumes

The same physical event can have different observer semantics without being duplicated. Soil-to-crop N uptake, for example, is internal for a soil+crop control volume but a sink for a soil-only observer. The physical event remains one `soil -> crop` edge.

This distinction is required for nested control volumes and keeps reporting perspective separate from physical ownership.

## Candidate event families

The qualified candidate projection covers the source-bound families required by the restricted non-GHG core:

- precipitation, irrigation, runon and other water input;
- evaporation, transpiration and sublimation output;
- runoff, drainage and bottom-boundary water export;
- matrix layer-to-layer water transfer;
- dissolved-solute layer interfaces and external boundary input/output;
- material/fertilizer/manure additions expanded by species composition;
- NH4 volatilization where explicitly defined by the addition process;
- upper-boundary and surface-reservoir release;
- realized crop N/P uptake;
- crop residue return, harvest export and grazing export;
- ploughing/mixing redistribution;
- organic-pool transformation, mineralization and immobilization;
- nitrification and non-GHG denitrification export topology;
- mineral-P aqueous/sorbed/precipitated phase transfers;
- matrix/macropore exchange and direct drainage in synthetic MP02 coverage.

Storage change itself is not emitted as a transfer. State owners remain state coordinates. This prevents physical state changes such as `Sic -> Sict` from being reinterpreted as invented fluxes merely to repair a reporting residual.

## Crop ownership

Realized N and P uptake are physical soil-to-crop transfers. Potential/requested uptake is not itself a mass crossing. The candidate records the realized process amount at the uptake coordinate.

Natural B1 path evidence includes both uptake routes used by the eight qualified MASSQ01 cases. Crop residue return is internal when both crop and soil owners are included. Harvest and the non-returned grazing fraction are external exports. Any later material return is a separate re-entry event.

This qualifies the owner/event topology. It does not yet prove a complete executable soil+crop state-plus-event closure across all growth, reset, harvest, grazing and continuation transitions.

## Reporting-only discrepancies

TCD-017 and TCD-018 demonstrate why reporting and physical transfers must remain separate.

For TCD-017, ploughing redistribution is an internal owner-to-owner event and nets exactly zero over the encompassing control volume. An omitted `Bapo(Redi)` reporting leg does not create an external transfer.

For TCD-018, interception is physical water storage. The public `Bawa` omission is not repaired by synthesizing a hydrologic event.

## Physical nonclosures are not balancing events

Known TCD-014, TCD-015, TCD-016, TCD-019 and TCD-025 residuals remain visible. The event projection does not create compensating edges.

The same rule applies to all 15 MASSQ02 `NEW_CAUSAL_FINDING` records, including the now-localized CranGrass detailed-hydrology residual and RuurloGrass upper-boundary N seam. Causal localization does not imply an admitted physical transfer and does not authorize a new TCD in this workunit. Those findings are routed to governed incremental B3 intake.

## Carbon boundary

MASSQ01/MASSQ02 support only the bounded soil-organic-C projection where the source-defined `Cfracom` conversion applies to the participating organic-matter quantity. The schema can represent C, but does not thereby establish one elemental-C ledger spanning crop dry matter, CO2 and CH4.

Whole-system elemental-carbon closure remains unqualified.

## Natural and feature coverage

The natural evidence set is the same eight compatible B1 cases:

`CranGrass`, `CranMais`, `GrassPeat`, `LWKM_gras_1040.2021.2045`, `Puitmijn_Cranendonck_60`, `RuurloGrass`, `STONE_akk_0006.2001.2015`, and `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

MP02 remains synthetic B1 macropore evidence only. The frozen natural testbank has no active macropore case, so no natural macropore admission follows.

GHG remains fail-closed incomplete because compatible natural active-GHG B1 runtime coverage and a complete qualified N2O/CH4 owner-and-event topology are absent.

## Legacy accumulator independence

`Bawa`, `Banh`, `Bani`, `Bano`, `Bapp`, `Bapo`, `Bfom`, `Bahu`, `Bdom` and related arrays are forbidden as physical storage or event amount owners.

Event amounts must originate from process state/transfer coordinates. Legacy balances may be compared as reporting evidence, but do not define the candidate physical journal.

MASSQ02 strengthens this at runtime: N/P residuals reproduce locally in `TRANSPORT`/`Transgen`, CranGrass TITO 724 water reproduces directly in `Hydro_detailed`, and RuurloGrass TITO 1915 N reconstructs from `UBoundconc` state handling plus the explicitly booked precipitation/deposition input. The whole-profile legacy accumulator is not needed as the causal owner.

## Validation result

The machine-readable projection qualifies:

- required candidate fields: `PASS_CANDIDATE_SCHEMA`;
- internal-event combined-volume cancellation: `PASS_BY_SINGLE_EDGE_OWNER_ALGEBRA_NO_TOLERANCE`;
- external event exactly one system crossing: `PASS_BY_OWNER_XOR_RULE`;
- legacy balance accumulator dependency: `NONE`;
- canonical runtime typed-event journal: `NOT_IMPLEMENTED_OR_ADMITTED`.

These results qualify the candidate semantics, not complete runtime instrumentation of every production process.

## Admission boundary

Together with the completed residual causality reconciliation (`UNEXPLAINED = 0`), this candidate supports the MASSQ02 target status:

`QUALIFIED_TYPED_MASS_EVENT_PROJECTION_AND_RESIDUAL_RECONCILIATION_MASS_ADMISSION_PENDING`.

Canonical MASS remains pending because:

1. 15 newly causal findings require governed incremental B3 intake;
2. existing governed TCDs remain admission constraints where they expose physical or ledger nonclosure;
3. the candidate is not yet implemented and qualified as the canonical runtime event journal;
4. full executable soil+crop nested state-plus-event closure remains open;
5. natural macropore coverage is absent;
6. GHG state/event completeness remains fail-closed;
7. whole-system elemental C remains unqualified.

No B3 correction or production migration is admitted by MASSQ02.
