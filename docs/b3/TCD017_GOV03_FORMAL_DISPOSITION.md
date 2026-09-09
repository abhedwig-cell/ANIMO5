# ANIMO-B3D01 — TCD-017 formal B3 disposition under GOV03

## Purpose

B3D01 is the first formal TCD disposition attempt after `ANIMO-GOV03` qualified bounded historical-reference acquisition closure and opened the strict historical-uncertainty route.

Target: `TCD-017`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Atomic claim: the already-existing top-reservoir dissolved-organic-P ploughing loss `Addiorpotoppl(I)` is omitted from the `Bapo(Redi,Ly)` redistribution ledger, while the corresponding layer redistribution is already represented and the encompassing physical redistribution is conservative.

Candidate reporting-only statement:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

No physical state, ploughing physics, transport, reaction or numerical-policy change is part of this disposition.

## Authorities

- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- B3A02 current readiness authority: `1a714eb144e43420ef5b176727e496ff9c46bc6d`
- frozen B3A02 second-line review object: `3ff8f4bda77c631b82110b83317c6a9b42b867ad`
- independent-review request: GitHub issue `#25`
- clean review branch: `review/animo-b3a02r-tcd017-second-line`

Frozen B0 source and testbank hashes remain unchanged.

## GOV03 route effect

Before GOV03, TCD-017 was blocked because no qualified B2 reference existed and the historical-uncertainty route was not eligible.

GOV03 now qualifies:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

and:

`G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`

Therefore the B3D01 `b2_route` gate is now `PASS` for the strict historical-uncertainty route.

This does not create B2 and does not establish historical fidelity. Historical revision-53 behaviour remains `UNKNOWN` where B2 is absent.

## Gate reconciliation

B3D01 records PASS for the already-qualified B0 identity, B1 causal evidence, theory/accounting identity, conservation, expected-difference whitelist, non-interference, natural/synthetic coverage, Class-A evidence and explicit residual historical uncertainty.

The single blocking gate is:

`independent_review = FAIL_PENDING_NOT_COMPLETED`

The existing B3A02 authoring context cannot review itself into admission. The clean review branch and issue #25 are only handoff infrastructure, not reviewer evidence.

## Current formal disposition

The machine disposition therefore remains:

`UNRESOLVED_NOT_ADMITTED`

with decision:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03`

This is a materially different state from the pre-GOV03 dossier: the route gate is no longer blocking. Independent second-line review is now the only identified admission gate still failing for this atomic record.

## Next transition

A separate genuinely independent reviewer must review the frozen B3A02 object without inheriting the authoring conclusion. If that review fails, TCD-017 remains not admitted. If it passes, a separate B3 admission-closeout step may evaluate whether all B3Q01 gates are then PASS and whether the appropriate historical-uncertainty scientific disposition can be admitted.

B3D01 does not modify production source, authorize a patch, claim historical equivalence, compose TCD-017 with another TCD, or establish B4.
