# ANIMO-KT03F01 Qualification Status

## Corrected governance disposition

The scientific/source evidence for KT03-F01 is strong enough to support a **candidate positive disposition**, but it is not yet a completed qualification.

Current status:

`CANDIDATE_POSITIVE_HLPIMP1_INTERCEPTION_EXCHANGE_STATE_DISPOSITION_PENDING_GOV04_TIER_C_INDEPENDENT_REVIEW`

The earlier same-agent closeout remains useful authoring and adversarial evidence, but it does not satisfy the governing independent-review gate. GOV06 explicitly preserves genuinely independent review wherever another authority requires it. GOV04 places this work in Tier C because it concerns missing physical state, initialization/state semantics and source/state ownership ambiguity with scientific consequences.

## Candidate scientific statement

For revision-53 detailed hydrology with `Iopthyvs=1, Hlpimp=1`, the available evidence supports the interpretation that interception storage is **not part of the producer exchange-state contract**. The unconditional legacy use of `Sic/Sict` therefore cannot be treated as scientifically defined input.

The candidate corrected transformation is:

- Hlpimp=1: do not reconstruct, fabricate or default `Sic/Sict`; omit the interception-storage delta from the affected `Hydro_detailed` identities.
- Hlpimp=11: retain the explicit initial `Sic`, dynamic `Sict`, lifecycle promotion and delta terms.

At equation level, omission of a non-existent exchange term contributes zero. Semantically this is not the creation of a zero-valued interception-storage state.

## Evidence already complete

The candidate is supported by converging B1 evidence:

1. revision-53 Hlpimp=1 static and dynamic records omit `sSic/sSict`;
2. revision-53 nevertheless normalizes those unread locals unconditionally;
3. `Init` promotes `Sic=Sict` only for Hlpimp=11;
4. the supplied ANIMO 4.0 SWATRE exchange table contains no interception-storage state;
5. four frozen Hlpimp=1 producer lineages close the revision-53 whole-profile identity without a separate interception term at mean absolute residuals of order `10^-8 m` per timestep;
6. LWKM Hlpimp=11 explicitly supplies interception state and inclusion of its storage delta improves mean absolute closure by about `18.06x`;
7. `Sict-Sic` participates in the `Dif -> Evso -> Flab(1) -> Modflux` chain, so the ambiguity can affect transport-facing hydrology and is not accounting-only.

The same-agent adversarial review found no material scientific contradiction in this bounded candidate, but its assurance remains `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Newly recovered historical build evidence

The supplied Visual Studio / Intel Fortran project materially narrows the historical build contract:

- `animo41.vfproj` SHA-256: `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`;
- `animo41.sln` SHA-256: `206dd6cc23b7d53c117131e16f15a22c4c97afc1c81febb3c73d789cdb9551f2`;
- `animo41.exe` SHA-256: `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`.

The project specifies `RealKIND=realKIND8` and `LocalVariableStorage=localStorageSave` for the inspected configurations. Debug x64 additionally has `LocalSavedScalarsZero=true`; Release x64 does not expose that explicit zero-initialization setting.

This evidence resolves part of the previously missing compiler contract, but it does **not** establish a portable or scientifically defined value for unread `sSic/sSict` in release execution. Therefore no B2 historical-behaviour claim follows from it.

## Governance classification

KT03-F01 is Tier C under GOV04. The triggers are:

- missing or redefined physical state;
- initialization/state semantics;
- state/source ownership ambiguity with scientific consequences.

A genuinely independent second-line review is therefore mandatory before this candidate can be called qualified or used as an admitted scientific rule.

## Current authority boundary

No production source is changed. The canonical TCD register is unchanged. No B3/B4, Status A or production claim is made.

The architecture line may continue in parallel only on surfaces that do not consume the unresolved Hlpimp=1 candidate as qualified authority, for example the explicit-state Hlpimp=11 path.

## Next action

Run a genuinely independent second-line review against the frozen authoring evidence and candidate claim. If that review passes without changing claim, scope or semantics, perform formal disposition closeout. If it changes the scientific claim, reopen qualification before any adapter implementation consumes it.
