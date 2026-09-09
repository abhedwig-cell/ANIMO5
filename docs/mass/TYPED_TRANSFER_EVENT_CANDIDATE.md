# ANIMO-MASSQ02 candidate typed transfer event contract

Status: `QUALIFIED_CANDIDATE_TYPED_EVENT_PROJECTION_NOT_CANONICAL_RUNTIME_JOURNAL`.

The machine-readable candidate is `integration/animo-mass/TYPED_EVENT_PROJECTION.json`.

## Purpose

PREP06 showed that conserved state ownership and process transfers are distributed through the legacy ANIMO source, while public balance arrays are reporting surfaces rather than physical state owners. MASSQ01 qualified an observer projection above that source/runtime surface. MASSQ02 turns the source-bound transfer map into a candidate typed-event model without changing physical state or introducing a second hidden state machine.

The candidate is a projection contract. It is not yet the ANIMO5 production event bus and is not a MASS admission.

## Required event fields

Every candidate event has these fields:

| field | contract |
| --- | --- |
| `time_interval` | exact accepted interval identity; no hidden epsilon is introduced |
| `element` | conserved quantity, normally water, N, P, or explicitly qualified C |
| `species_pool` | physical species or pool carrying the quantity |
| `amount` | non-negative scalar magnitude |
| `unit` | explicit quantity unit |
| `source_owner` | physical source owner or external-boundary sentinel |
| `destination_owner` | physical destination owner or external-boundary sentinel |
| `internal_external` | derived from owner membership in the declared system boundary |
| `process` | process that generated the transfer |
| `evidence_coordinate` | source routine/state/transfer coordinate or qualified synthetic coordinate |

Direction is represented only by source and destination ownership. A negative `amount` is invalid.

The owner namespace used by the candidate treats `animo.*` as internal and `external.*` as outside the ANIMO system boundary. Source and destination may not be identical.

## Single-edge conservation rule

For a transfer amount `q >= 0`, the owner deltas are defined as:

`delta(source) = -q`

`delta(destination) = +q`

If source and destination both belong to a combined control volume, then:

`-q + q = 0`

exactly. This is an algebraic identity, not a numerical pass criterion, so no tolerance is involved.

This rule is especially important for layer interfaces. One physical interface crossing creates one typed event edge. Emitting one independently signed record for each adjacent layer is forbidden because that can double count or allow the two sides to diverge.

## External-boundary rule

A system-external event is valid only when exactly one endpoint is internal:

`XOR(internal(source_owner), internal(destination_owner)) = true`.

Therefore every external event has exactly one system-boundary crossing. An event with both endpoints external is not an ANIMO system transfer and is invalid in this journal.

The same physical event can have different observer semantics under a narrower control volume. For example, soil-to-crop N uptake is internal for a soil+crop volume but appears as a sink for a soil-only projection. The physical event itself is not duplicated or retyped.

## Candidate event families

The projection covers the source-bound transfer families needed for the restricted non-GHG core.

### Water

- atmospheric/management input into surface or profile water;
- evaporation/transpiration/sublimation to atmosphere;
- runoff, drainage and lower-boundary export;
- layer-to-layer matrix water transfer;
- matrix-to-macropore exchange and macropore direct drainage for synthetic MP02 coverage.

Water storage change is not emitted as a transfer. Stores remain state-owner coordinates. Interception `Sic/Sict` therefore stays physical state, which prevents TCD-018 from being disguised as an invented flux.

### Dissolved solute transport

- one layer-interface event for DON, DOP, DOM, NH4, NO3 or PO4 movement;
- explicit upper/lower/lateral boundary inputs;
- runoff, drainage and leaching outputs;
- surface/top-reservoir release to soil or, where physically routed, to an external runoff boundary.

A local transport nonclosure such as TCD-015 or TCD-016 remains a residual. The event projection does not create a compensating edge.

### Material additions and management

A material addition is decomposed into species/pool-specific transfers from `external.management_material` into the receiving ANIMO stores. Composition is taken from the source process coordinates rather than legacy balance accumulators.

NH4 volatilization at addition is a separate external atmospheric loss event where the source defines it. This keeps the material identity explicit:

`material element amount = retained additions + explicit external loss`.

### Crop ownership

Realized N and P uptake are represented as soil-to-crop internal transfers when crop state is included in the system owner set.

MASSQ02 distinguishes requested/potential uptake from realized transfer. For the external crop-forcing route, an external request is not itself a mass crossing. Only realized `Upintg_Extern` uptake becomes a physical soil-to-crop event.

Natural B1 coverage exists for both crop routes:

- `CropUptakeModel=0`: CranGrass, CranMais, Puitmijn, RuurloGrass and Zuiderzeeland;
- `CropUptakeModel=1`: GrassPeat, LWKM and STONE.

Crop residue return is crop-to-soil internal when both owners are included. Harvest and grazing removal are external exports for the non-returned fraction. A later management return, if present, is a separate event re-entering the system.

This qualifies the candidate owner/event topology and natural path activation. It does not yet prove complete executable soil+crop nested closure across growth, reset, harvest and continuation state.

### Redistribution

Ploughing and mixing are represented as owner-to-owner internal transfers. Summing the same transfer over an encompassing profile gives exact net zero. This representation captures the physical redistribution directly and does not inherit the TCD-017 `Bapo(Redi)` reporting omission.

### Organic-pool transformations

Decomposition, assimilation, mineralization and immobilization are represented by species-specific owner-to-owner transfers. Internal N/P transfers cancel over an encompassing control volume; only source-explicit gaseous or other external products cross the boundary.

For C, an event is admitted only when the participating pool has an explicit qualified carbon conversion. MASSQ02 natural evidence only supports the bounded soil-organic-C projection through source-defined `Cfracom`. Crop dry matter and GHG carbon are not silently merged into it.

### Nitrogen transformations

For the non-GHG core, nitrification is an internal NH4-N to NO3-N event.

Denitrification is represented as NO3-N leaving the soil N owner set toward an atmospheric boundary where the source process treats gaseous N as exported. If active GHG state retains N2O before emission, that topology requires a separate qualified internal gas owner and is outside current MASSQ02 admission.

### Mineral phosphorus phase transfers

Fast/slow sorption, desorption and precipitation/dissolution are internal P phase transfers. The phase-transfer event must correspond to one physical amount between state owners.

A numerical constitutive inconsistency, such as TCD-019, remains visible as nonclosure between state change and process transfers. It is not repaired by adjusting event amounts.

### Macropores

The candidate contains matrix-to-macropore internal exchange and macropore direct drainage events. Storage owners include the source-explicit `SrWaMp` and macropore solute state.

Qualification is synthetic MP02 only. The frozen natural testbank contains no active macropore case. Therefore the event topology is a source/synthetic candidate and not a natural feature admission.

## Representative projections from MASSQ01 evidence

MASSQ01 observer records can be mapped into the typed model without making legacy balance arrays authoritative.

For CranGrass TITO 1, for example, beginning/end storage remains state projection. Aggregate external water, N, P and OM transfers can be decomposed by their source process coordinates into typed boundary events. The current MASSQ01 sidecars aggregate some transfer classes and therefore do not themselves constitute the canonical event journal.

MP02 provides two explicit synthetic examples:

- matrix-to-macropore water exchange is internal over the combined matrix+macropore control volume and contributes `-q/+q`, net zero;
- direct macropore drainage has one internal macropore owner and one external drainage owner, so it has exactly one system-boundary crossing.

## Legacy balance accumulator independence

`Bawa`, `Banh`, `Bani`, `Bano`, `Bapp`, `Bapo`, `Bfom`, `Bahu`, `Bdom` and similar arrays are forbidden as physical event amount or storage owners.

Event amounts must come from process transfer/state coordinates. Legacy balances can be compared as report evidence, especially for discrepancy archaeology, but they do not define the candidate physical journal.

This follows PREP06 ownership and is supported at runtime by MASSQ01/MASSQ02: known and newly localized residuals are reconstructed from physical state plus process transfers, with many N/P causal mismatches reproduced directly in `TRANSPORT` or `Transgen` before public balance reporting.

## Feature readiness

Current candidate readiness is deliberately feature-scoped:

| feature | MASSQ02 result |
| --- | --- |
| core water/N/P | source-qualified candidate projection plus natural B1 observer coverage |
| crop nested owner topology | source-qualified candidate; both crop uptake routes naturally exercised |
| macropore | MP02 synthetic only; no natural admission; TCD-025 remains visible |
| GHG | fail-closed incomplete; no compatible natural active B1 case and no MASSQ02 GHG event admission |
| carbon | bounded soil-organic-C only where conversion is explicit; no whole-system C claim |

## Validation result

The machine-readable projection records these qualification checks:

- candidate field completeness: `PASS_CANDIDATE_SCHEMA`;
- internal-event combined-volume net zero: `PASS_BY_SINGLE_EDGE_OWNER_ALGEBRA_NO_TOLERANCE`;
- external event exactly one system crossing: `PASS_BY_OWNER_XOR_RULE`;
- legacy balance accumulator as storage/amount owner: forbidden and not used;
- canonical runtime typed-event journal: `NOT_IMPLEMENTED_OR_ADMITTED`.

The first three results qualify the candidate semantics. They do not prove that every production process has already been instrumented to emit the canonical events.

## Admission boundary

MASSQ02 qualifies the typed-event projection as a candidate architecture/evidence contract. Canonical MASS remains pending because:

1. two natural residuals still lack causal isolation;
2. newly localized causal findings still require governed B3 intake;
3. full executable soil+crop nested closure remains open;
4. macropore natural coverage is absent;
5. GHG event/state completeness is fail-closed;
6. whole-system elemental C remains unqualified;
7. the candidate has not yet been implemented and qualified as the canonical runtime event journal.

The candidate therefore supports subsequent MASS admission work without itself performing that admission.
