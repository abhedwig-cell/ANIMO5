# ANIMO-GHG13 — TCD-034 Plant-Transfer Transport-Sink / Reported-Flux Carbon-Ledger Composition

## Scope

GHG13 starts from the exact green GHG12 authority `ANIMO-GHG12@b4a3c603743a2e3ba62fdf69f0879975a3b4f14a` and closes only the bounded carbon-ledger compatibility question left open in the TCD-034 model-evolution path.

It does not change production source. It does not claim that the evolved T50 selector was historical ANIMO behavior. It does not qualify the whole methane balance, empirical flux magnitude, B3 admission, Class-F admission or production migration.

## Source identity

The frozen revision-53 source manifest pins:

- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`;
- `ghgtransport.for`: `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`;
- `ghgtranssub.for`: `48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c`.

The scientific selector remains the separately qualified model-evolution contract `TCD034_T50_0P50M_DEPTH_OPERATOR_V1` from GHG06A.

## Ledger identity reconstructed from source

After the raw plant coefficient is formed, revision-53 adapts `K1plant` to the soil-system concentration basis using the local water/gas phase-storage factor. The adapted `K1plant` is passed into `GHGtransport`.

Within `GHGtranssub`, `K1plant` enters the dynamic analytical transport coefficient. Within `GHGtransport`, the process-side mass-balance expression contains the plant sink contribution

`Mplant_sink_i = AvCo_i * K1plant_i * He_i * St`.

Here `AvCo_i` is the average concentration over the time step, `He_i` is layer thickness and `St` is step duration in days.

After the converged transport calculation, `ghg_ch4.for` reports plant oxidation and atmospheric plant emission from the same adapted coefficient and the same average methane concentration:

`Qox_i = PvCH4Ox * K1plant_i * AvCoCH4_i * He_i`

`Qem_i = (1-PvCH4Ox) * K1plant_i * AvCoCH4_i * He_i`.

The time-integrated reported mass therefore satisfies

`St * (Qox_i + Qem_i) = Mplant_sink_i`

for every rooted layer. Summing over rooted layers preserves the identity exactly.

This is stronger than the GHG07 partition identity alone because it connects the externally reported plant oxidation/emission terms to the plant-removal term that participates in the frozen transport solver's process balance.

## Composition with the evolved selector

GHG13 does not wire GHG06A into production. It builds a bounded research composition:

1. obtain `T50` from the qualified GHG06A fixed-depth operator;
2. compute `fGrow` with the frozen source response;
3. compute root-normalized `Kraw` and the phase-adapted `K1plant` using the GHG07 contract;
4. evaluate the source-identical plant sink mass over `St`;
5. partition the same transfer into plant oxidation and atmospheric emission;
6. assert layerwise and profile ledger closure.

If the selector is unavailable, no plant-transfer ledger result is published. There is no fallback temperature.

## Qualification boundary

The qualified identity is an atomic plant-transfer carbon ledger. It does not assert that all CH4 production, soil oxidation, diffusion, ebullition, air/water advection and storage close in a full run with the evolved selector. It also does not demonstrate a production executable connection.

The result may therefore close the specific Class-F evidence sub-gap `INTEGRATED_CH4_OR_CARBON_CONSERVATION_AFTER_EXECUTABLE_SELECTOR_CONNECTION` only to the narrower status `PASS_BOUNDED_SOURCE_LEDGER_COMPATIBILITY`; whole-model executable conservation remains a later production-migration qualification if the model evolution is scientifically admitted.

## Decision

`QUALIFIED_TCD034_MODEL_EVOLUTION_PLANT_TRANSFER_SOURCE_LEDGER_COMPATIBILITY_V1`

Evidence class: `BOUNDED_SOURCE_LEDGER_COMPATIBILITY_MODEL_EVOLUTION_NOT_B2`.
