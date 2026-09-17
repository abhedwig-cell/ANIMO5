# ANIMO-KT03-F01 — Undefined SWAP3 interception-storage input for Hlpimp=1

Status: `ADJACENT_SOURCE_FINDING_REQUIRES_SCIENTIFIC_DISPOSITION`.

This is not assigned a canonical TCD number by KT03. Canonical TCD allocation and B3 disposition remain under their governing scientific authority.

## Observation

For `Iopthyvs=1`, revision-53 `Input_hydro` has two dynamic first-record layouts:

- `Hlpimp==11`: the record includes `sSict`;
- other values, including CranMais `Hlpimp=1`: the record does not include `sSict`.

After that branch, the routine unconditionally executes the equivalent of `Sict = Dble_trunc(sSict)`.

The frozen CranMais hydrology header contains `Hlpimp=1`, and its dynamic first record is exactly 18 REAL(4) values, matching the source branch without `sSict`.

## Downstream relevance

`Hydro_detailed` uses `Sict` for the `Iopthyvs=1` route in at least:

- the top-boundary water-balance expression through `(Sict-Sic)/St`;
- the whole-profile water-balance expression through `(Sict-Sic)`.

`Init` only advances `Sic = Sict` when `Iopthyvs==1 .and. Hlpimp==11`. This does not define the current-step `Sict` value for the `Hlpimp=1` route.

## Why KT03 does not repair it

The frozen file provides no current-step interception-storage value in this layout. Choosing zero, carrying a previous value, reconstructing it from precipitation/evaporation or changing the downstream balance would introduce scientific semantics not present in the bounded adapter authority.

The typed adapter therefore records:

`has_interception_storage_end = false`

and fails closed when asked to produce a fully defined `Hydro_detailed` call surface.

## Current evidence classification

The finding is source- and frozen-byte-based. It is stronger than a speculative architecture concern, but KT03 has not yet established the historical Intel runtime value actually observed for the uninitialized local `sSict` or the intended scientific meaning for this legacy layout.

Therefore KT03 does not classify this as a confirmed scientific code defect or select a correction.

## Required next scientific question

A separate bounded disposition should establish one of the following with evidence:

1. `Sict` is scientifically inapplicable for `Hlpimp=1` and `Hydro_detailed` should not consume it on that route;
2. the producer layout is missing an intended interception-storage field and a recoverable historical contract exists;
3. another explicit state/flux relation supplies the intended interception term;
4. the historical implementation intentionally relied on a documented compiler/storage convention, in which case that behaviour must be qualified rather than guessed.

Until then, KT03 can qualify only the defined file-to-typed hydrology fields, not full downstream compatibility for CranMais.
