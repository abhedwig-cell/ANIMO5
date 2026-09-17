# ANIMO-KT03 Legacy Hydrology-Step Boundary

## Boundary decision

The candidate adapter boundary is the normalized output responsibility of `Input_hydro`, immediately before `Hydro_detailed` consumes those values.

This is intentionally not the raw byte layout of `SWATRE.UNF` and not the later fully transformed ANIMO water state.

The distinction is important:

`SWATRE.UNF bytes -> legacy file adapter / Input_hydro normalization -> typed hydrology step -> Hydro_detailed -> ANIMO internal hydrology/process inputs`

A future in-memory SWAP5 provider would replace only the left-hand file-adapter path. It would have to produce the same typed hydrology-step contract. `Hydro_detailed` remains ANIMO-owned until a separate scientific workunit says otherwise.

## Evidence from revision-53 source

The main loop calls `Input_hydro` before `Hydro_detailed` on every detailed-hydrology timestep. The file reader therefore already forms a natural anti-corruption layer between an external hydrology producer and the ANIMO scientific calculation.

For SWAP-style detailed hydrology, `Input_hydro` reads and normalizes several record groups. The exact active layout depends on the legacy SWAP version and options. For the `Iopthyvs=1` branch, the first timestep record includes time/step information and atmospheric/surface/bottom quantities such as precipitation components, interception and soil evaporation components, runoff, groundwater level and related values. It then reads per-layer storage/moisture/flux arrays, one drainage array per configured drainage system, and additional crop/weather/temperature records. Optional macropore input is delegated to `Mapoinput`.

The reader converts single-precision file values through `Dble_trunc` into ANIMO working values and also applies at least one semantic normalization: a groundwater-level sentinel below approximately `-9.98` is mapped to the bottom of the model profile with a diagnostic transition flag.

Those behaviours are part of the legacy adapter contract. They must not disappear merely because the file is replaced by typed in-memory input.

## Candidate typed responsibility groups

The first specification should group fields by responsibility rather than preserve the legacy subroutine argument order:

### Interval identity

- producer timestep time coordinate (`Tiwa` lineage);
- timestep duration (`St`) when present in the selected legacy layout;
- source layout/version identity;
- layer and drainage dimensions.

### Surface and atmospheric water terms

- rainfall/snow/irrigation precipitation components where present;
- interception evaporation components;
- snow/soil/potential and maximum evaporation/transpiration terms where present;
- runon and runoff;
- ponding/surface storage terms carried by the selected layout.

### Profile hydrology

- groundwater level;
- per-layer storage `Sc`;
- end-of-step moisture fraction `Mofrt`;
- lateral/exchange flux `Flev`;
- vertical boundary/interface flux array `Flab` with its `Nl+1` extent;
- drainage flux matrix `Fldr(1:Nudr,1:Nl)`.

### Auxiliary producer fields

- producer crop/weather fields read by the legacy SWAP branch, including the values represented by `Soco`, `Lai`, `Dpro`, `Hecr` and `Avdate`;
- per-layer producer temperature record as required by the active option/layout.

### Optional extensions

Macropore records are not part of the first CranMais carrier because `MacroPoreOption=0`. They require an explicit later extension rather than nullable fields whose semantics are guessed now.

## What the typed carrier must not contain

It must not contain:

- ANIMO concentrations, pools, reaction rates or crop nutrient state;
- outputs of `Hydro_detailed` that are derived from the hydrology packet plus ANIMO geometry/state;
- SWAP solver convergence state or retry policy;
- file handles, record positions or parser scratch;
- implicit sentinel values as a substitute for explicit validity/availability.

## First qualification envelope

The first executable probe is intentionally bounded to the frozen CranMais files:

- `Swatre.unf` SHA-256 `538827d517f7be4c060e2d62131e1942f8e0e76fdeae49dc0268486984cc9eaf`;
- `GENERAL.INP` SHA-256 `e514e50020f7d73d2695b359c4b956117b0161d862c375f03a3ae8b95ca43029`;
- `animo.ini` SHA-256 `5d1f62faf62747b7d91d3e9199e33954e3038ddd005259f32a8bca95f0c82bb8`.

The probe must first establish the exact record/layout identity actually used by CranMais. The field list above is a source-derived candidate responsibility map, not yet a claim that every listed field is active in that case.

## Design consequence for future SWAP5 coupling

The future coupling API should target the normalized typed hydrology-step contract, not `SWATRE.UNF` bytes and not the internal `Hydro_detailed` working arrays.

That gives three useful properties:

1. legacy ANIMO can remain runnable from frozen files through an adapter;
2. SWAP5 can later provide the same information in memory after an accepted hydrological interval;
3. the model-neutral transient runtime remains ignorant of both the SWAP file grammar and ANIMO nutrient science.

KT03 has not yet proven those properties executable. This document only fixes the candidate boundary and the evidence needed for the next phase.
