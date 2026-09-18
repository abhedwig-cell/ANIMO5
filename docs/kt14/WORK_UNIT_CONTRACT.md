# ANIMO-KT14 Boundary-Frame TCD-042 Composition Qualification

## Purpose

KT14 closes the chemistry-time binding gap left explicit by KT13A.

KT13A accepts a typed chemistry forcing object, but that object is not itself bound to an exact interval. BOUNDQ02 now supplies a self-validating interval frame with exact TIME02 origin/endpoint identity, source-year cursor provenance and UBFORCE02 chemistry.

KT14 requires that exact frame before invoking the already-qualified KT13A one-interval science composition.

## Authorities

Program:
`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Remediated one-interval composition:
`ANIMO-KT13A@df2310cc69e3fe16187ba2235843222f8acfb726`

Static boundary year binding:
`ANIMO-BOUNDQ02@fb0c0c842aed9a90378aca613279e09a856ad09b`

BOUNDQ02 exact-final workflow:
`35373354465 = success`

The imported implementation blobs are:

- BOUNDQ01 adapter: `6b381ec9b37528b0decee8a2fa484e8124fc767d`
- BOUNDQ02 frame binding: `2b7441c9909022dcb16b3ca2f35ee08d079269b8`
- KT13A composition: `6e2e4c73e9b43f5d1bda58dc9387a56be8b2e2b1`

## Composition order

KT14 performs:

1. validate the BOUNDQ02 frame against the exact requested `t0` and `t1`;
2. verify runtime calendar identity matches the interval calendar;
3. expose selected source year/slot and separate dry-deposition values as trace only;
4. pass only `boundary_frame%chemistry` to KT13A;
5. let KT13A perform KT06 binding, KT05 projection, HYDROEXEC01, UBFORCE02, KT12 and KT02 atomic accepted-state publication.

No chemistry is used before frame validation.

## Dry deposition

BOUNDQ02 carries dry NH and NI deposition because they are part of the BOUNDARY source family.

KT14 does not pass those values into KT13A.

They remain separate from the wet/advective `Load1...Load6` path.

An adversarial test changes only finite dry-deposition values and verifies that the TCD-042 accepted concentration and selected wet/advective load rate are bit-identical.

This does not qualify the dry-deposition process itself.

## Rejection and accepted-state safety

A stale frame, a frame for a different endpoint, or mutated forcing provenance fails before KT13A science execution.

Therefore those failures cannot change the accepted TCD-042 store.

Once KT13A invokes KT02, KT02 remains the sole owner of accepted-state publication.

## What KT14 does not solve

KT14 consumes an already-created BOUNDQ02 frame.

It does not atomically commit the BOUNDQ02 year cursor together with the TCD-042 accepted state.

It does not provide multi-interval hydrology/state continuation.

It does not resolve the first-call `Runinu` uncertainty.

Those are separate continuation/composite-state work.

## Governance

KT14 is cross-module scientific composition and is GOV04 Tier D.

Same-agent qualification may establish a bounded nonproduction candidate only.

Genuine independent Tier D review remains required before composition admission.

## Hard boundaries

No BOUNDARY parser change.
No dynamic boundary forcing.
No dry-deposition process migration.
No chemistry-frame fabrication inside KT13A.
No year-cursor canonical state admission.
No multi-interval state claim.
No TCD-042 scope widening.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.
