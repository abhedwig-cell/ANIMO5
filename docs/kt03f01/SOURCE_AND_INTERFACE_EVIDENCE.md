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

## 2. The consequence is not accounting-only

`Hydro_detailed.for` uses `Sict-Sic` inside the top-boundary `Dif` identity and the whole-profile `Badev` identity. The `Dif` path can change `Evso`, then `Flab(1)`, after which `Modflux` derives transport-facing water fluxes.

Causal chain:

`undefined Hlpimp=1 Sic/Sict -> Dif -> Evso -> Flab(1) -> Modflux / transport-facing water fluxes`

This makes KT03-F01 distinct from TCD-018, which concerns reporting-ledger coverage for an interception state that actually exists.

## 3. Supplied 4.0 documentation supports an absent-state older interface

The supplied ANIMO 4.0 user guide Table 10 documents the SWATRE.UNF exchange. It contains interception-evaporation fluxes but no initial or dynamic interception-storage state. This is version-limited evidence for ANIMO 4.0, but it agrees with the observed Hlpimp=1 file grammar.

## 4. Frozen producer lineages separate the layouts

Observed bounded files:

- CranMais: Hlpimp=1, SWAP3.0beta;
- CranGrass: Hlpimp=1, swap_3_0_2;
- GrassPeat: Hlpimp=1, Swap 3.2.26;
- STONE: Hlpimp=1, Swap 3.2.36;
- LWKM: Hlpimp=11, V7.3.3.3.

All four Hlpimp=1 files omit initial and dynamic interception storage. LWKM Hlpimp=11 supplies initial `Sic` and dynamic `Sict` explicitly.

## 5. Whole-profile balance probe

The bounded B1 probe evaluates the revision-53 whole-profile identity directly from the frozen producer records after diagnostic `Dble_trunc` normalization.

Mean absolute residual without a separate interception-storage term:

- CranMais: `4.812e-08 m`;
- CranGrass: `5.609e-08 m`;
- GrassPeat: `3.579e-08 m`;
- STONE: `4.787e-08 m`.

LWKM Hlpimp=11:

- without explicit interception delta: `4.124e-05 m`;
- with supplied `Sict-Sic`: `2.284e-06 m`;
- improvement factor: about `18.06x`.

This is B1 diagnostic evidence, not historical executable truth.

## 6. Historical build artifacts recovered

The user-supplied original project artifacts provide new B0/build-contract evidence:

- `animo41.vfproj` SHA-256 `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`;
- `animo41.sln` SHA-256 `206dd6cc23b7d53c117131e16f15a22c4c97afc1c81febb3c73d789cdb9551f2`;
- `animo41.exe` SHA-256 `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`.

The Visual Studio 2010 Intel Fortran project specifies `RealKIND=realKIND8` and `LocalVariableStorage=localStorageSave`. Debug x64 additionally sets `LocalSavedScalarsZero=true`; Release x64 does not contain an explicit equivalent zero-initialization setting.

This materially narrows TCD-010/TCD-011 historical build uncertainty, but it does not turn unread `sSic/sSict` into scientifically defined state and does not establish their exact release-executable value.

## 7. Candidate implication

The evidence supports the candidate:

`HLPIMP1_INTERCEPTION_STORAGE_NOT_PART_OF_PRODUCER_EXCHANGE_STATE_CONTRACT`

Candidate corrected semantics:

- Hlpimp=1: do not read, expose or reconstruct undefined `Sic/Sict`; omit the absent interception-storage delta from the affected transformation identities.
- Hlpimp=11: retain explicit `Sic/Sict` state and delta terms.

Because this is a Tier C state/initialization/source-ownership decision, the candidate requires genuinely independent second-line review before qualification.
