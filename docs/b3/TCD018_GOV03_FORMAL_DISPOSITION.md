# ANIMO-B3D05 — TCD-018 Formal B3 Disposition Under GOV03

## Decision

TCD-018 remains **not admitted** at this step.

The historical-evidence route is no longer the blocking gate. ANIMO-GOV03 qualifies `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and opens `G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

The remaining blocking gate is a genuinely independent second-line review.

Formal disposition:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03`

## Atomic claim

TCD-018 is restricted to the interception-storage water-ledger interface.

The existing physical states are:

- begin interception storage: `Sic`;
- end interception storage: `Sict`.

The accounting relation is:

`Bawa_Ddev_corrected = Bawa_Ddev_legacy - sum((Sict-Sic)*1000)`

for the active reporting period/control volume.

This is an accounting/reporting claim only. No interception physics, hydrology state, flux, forcing, testcase input or state-promotion semantics may change.

## Reconciled evidence

Authority is pinned to:

- `ANIMO-RG05B@c353c3179f213c1bf24c48b3c06f8065c760d3e2`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3A03@8eaaca34e4f0d906c2d8245f0df232586efe8ff3`;
- `ANIMO-B3A03R@0876e6e1b6ce33ee5e7b812ab4107f54760d6b27` as same-context technical evidence only;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`, oracle `SYNQ-O003`.

The readiness dossier establishes Sic/Sict ownership, the begin/end storage identity, the omission from the Bawa interface, natural LWKM activation and the water-only expected-difference surface.

The B3A03R technical continuation additionally executed an isolated eight-case non-interference run: 376 outputs compared, 370 equal after declared volatile normalization, six whitelisted differences, zero unexpected differences. This strengthens the technical evidence but does **not** satisfy reviewer independence because it was produced in the same authoring context.

## Expected difference

Only the six water-ledger outputs may differ when the relevant reporting control volume is active and net interception storage changes:

- `bawaGP.Out`
- `bawaRP.Out`
- `bawaTP.Out`
- `ani_waGP.Bal`
- `ani_waRP.Bal`
- `ani_waTP.Bal`

Physical trajectories, non-water reporting and unrelated residual classifications must remain unchanged.

## Residual uncertainty

Historical revision-53 behaviour remains `UNKNOWN` because no qualified B2 behavioural reference exists.

The MASSQ01 CranGrass TITO=724 residual of `-0.0030198960466805147 mm` remains unexplained and outside the atomic TCD-018 claim. It is not corrected, masked or used as a tolerance.

The observed approximately `0.0601 mm` legacy LWKM balance difference is evidence for the omitted storage term, not an acceptance epsilon.

## Independent-review boundary

A fresh second-line review must execute in a separate ChatGPT context. The same-context B3A03R technical review cannot count.

Clean review branch:

`review/animo-b3a03r-tcd018-independent-second-line`

A PASS there is review evidence only. A separate admission-closeout remains required.

## Production boundary

This workunit does not modify production source and does not authorize B4, production migration, hydrology changes or global water-closure claims.
