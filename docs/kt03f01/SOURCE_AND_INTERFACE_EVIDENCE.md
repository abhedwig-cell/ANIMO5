# ANIMO-KT03F01 Source and Interface Evidence

## 1. Interface asymmetry is explicit in revision-53 source

For `Iopthyvs=1`, the static hydrology read in `input1.for` reads:

- Hlpimp=11: `SWale, sSic, SPn`;
- otherwise: `SWale, SPn`.

The source then executes `Sic = Dble_trunc(sSic)` unconditionally.

The dynamic read in `Input_hydro.for` similarly reads:

- Hlpimp=11: 19 surface values including `sSict`;
- otherwise: 18 values with no `sSict`.

It then executes `Sict = Dble_trunc(sSict)` unconditionally.

`Init.for` strengthens the distinction: previous interception storage is promoted with `Sic = Sict` only when `Iopthyvs=1 .and. Hlpimp==11`. Therefore the source itself contains an explicit lifecycle for interception storage only on the Hlpimp=11 path.

This does not establish the value of the undefined Hlpimp=1 locals. TCD-010 and TCD-011 already show that default-real and local-storage behaviour depend on the historical build contract. KT03F01 therefore treats those local values as scientifically undefined, not as zero and not as a stable historical carry value.

## 2. The consequence is not accounting-only

`Hydro_detailed.for` uses `Sict-Sic` in two places relevant here.

First, the Hlpimp-independent `Iopthyvs=1` top-boundary correction includes `-(Sict-Sic)/St` inside `Dif`. `Dif` then changes `Evso` through `Evso = Max(0, Evso-Dif)`, after which `Flab(1)` is recomputed. `Hydro_detailed` immediately calls `Modflux`, which converts `Flab` into non-negative transport-facing inflow/outflow terms. Elsewhere, `Flab(1)` is also consumed by uptake parameter calculations.

The causal chain is therefore:

`undefined Hlpimp=1 Sic/Sict -> Dif -> Evso -> Flab(1) -> Modflux / transport-facing water fluxes`

Second, the whole-profile water-balance deviation subtracts `Sict-Sic` directly.

Consequently KT03-F01 is not merely another form of TCD-018 output accounting. An undefined interception delta can alter the hydrological transformation presented to solute transport.

## 3. Supplied 4.0 documentation supports an absent-state older interface

The supplied ANIMO 4.0 user guide describes SWATRE.UNF in Table 10. Its initial-condition fields include groundwater level, ponding storage and snow storage, but no interception-storage state. Its dynamic fields include precipitation, interception-evaporation fluxes, soil evaporation, ponded-water evaporation, transpiration terms, runoff, groundwater level, ponding, snow storage, a water-balance error and profile flux/state arrays, again without `Sic` or `Sict`.

The same guide describes `Hydro_detailed` as taking detailed water-model fluxes/moisture as input and modifying flux terms for use in the transport equation. The guide is version-limited evidence for ANIMO 4.0, not exact revision-53 authority, but it agrees with the observed Hlpimp=1 file grammar.

## 4. Frozen testbank lineages separate the two layouts

The supplied textual-header SWAP files inspected for this workunit show:

- CranMais: Hlpimp=1, SWAP3.0beta;
- CranGrass: Hlpimp=1, swap_3_0_2;
- GrassPeat: Hlpimp=1, Swap 3.2.26;
- STONE: Hlpimp=1, Swap 3.2.36;
- LWKM: Hlpimp=11, V7.3.3.3.

All four Hlpimp=1 files omit initial and dynamic interception storage. LWKM Hlpimp=11 supplies initial `Sic` and dynamic `Sict` explicitly.

## 5. Whole-profile balance probe

`tools/kt03f01/analyze_interception_balance.py` evaluates the revision-53 whole-profile water-balance identity directly from frozen SWATRE logical records after the same diagnostic `Dble_trunc` normalization used by KT03. The tool does not execute production source and does not reconstruct historical compiler behaviour.

For Hlpimp=1, the probe evaluates the balance without an interception-storage term because no such state exists in the record. Mean absolute residuals are:

- CranMais: `4.812e-08 m` over 3287 timesteps, max `3.716e-06 m`;
- CranGrass: `5.609e-08 m` over 2922 timesteps, max `9.480e-06 m`;
- GrassPeat: `3.579e-08 m` over 540 timesteps, max `2.751e-07 m`;
- STONE: `4.787e-08 m` over 540 timesteps, max `6.598e-07 m`.

For Hlpimp=11 LWKM, omitting the explicit interception-storage change gives mean absolute residual `4.124e-05 m`; including the supplied `Sict-Sic` reduces it to `2.284e-06 m`, an approximately `18.06x` reduction. The maximum explicit interception-storage change in the file is `2.0e-04 m`.

These results are derived B1 diagnostic evidence. They do not establish historical executable behaviour. They do establish a strong interface distinction: the older Hlpimp=1 hydrology payloads are internally close to the revision-53 whole-profile identity without interception storage, whereas the Hlpimp=11 payload materially requires the explicitly supplied storage term.

## 6. Qualification implication

The evidence currently supports H0 more strongly than H1:

- no Hlpimp=1 producer state exists in the documented or observed grammar;
- no Hlpimp=1 lifecycle promotion exists in `Init`;
- four independent frozen Hlpimp=1 payload lineages close their whole-profile hydrological balance without an interception-storage term;
- the later Hlpimp=11 layout explicitly adds the state and materially improves closure when the term is used.

The candidate bounded scientific disposition is therefore:

`HLPIMP1_INTERCEPTION_STORAGE_NOT_PART_OF_PRODUCER_STATE_CONTRACT`

with the candidate corrected source semantics:

- for Hlpimp=1, do not read or propagate undefined `Sic/Sict`, and omit the interception-storage delta from both the `Dif` top-boundary term and whole-profile `Badev` term;
- for Hlpimp=11, retain the explicit `Sic/Sict` state and current delta terms.

This is a qualification candidate only. It requires adversarial review before close and does not authorize a production patch.
