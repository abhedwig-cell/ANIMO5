# ANIMO-KT04 Work Unit Contract

Workunit: `ANIMO-KT04 — Hlpimp=1 Legacy Projection and File/Typed Equivalence`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE`.

## Governance correction

KT04 was started from a same-agent KT03F01 closeout that labelled the Hlpimp=1 absent-interception rule as qualified. Current GOV04/GOV06 reconciliation shows that label was too strong. The underlying decision is Tier C because it concerns missing physical state, initialization/state semantics and state/source ownership ambiguity with scientific consequences.

The corrected KT03F01 checkpoint is:

`ANIMO-KT03F01@36024e5b8cd62203b03b9b72c0d08e4c797612bb`

Its Hlpimp=1 claim is a candidate pending genuinely independent second-line review. Therefore KT04 must fail closed for Hlpimp=1 and cannot complete qualification or closeout on that semantic until the review is complete.

## Frozen authority that remains usable

The explicit interception path remains supported by frozen KT03 evidence:

- KT03 closeout: `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- frozen KT03 contract implementation: `e844c7658a95819fc0463c55737f9bd41b29a6da`;
- typed payload: `ANIMO_HYDROLOGY_STEP_V1`;
- unit contract: `ANIMO_HYDROLOGY_UNITS_V1`.

For the bounded Hlpimp=11 layout, interception storage is explicitly supplied. The nonproduction projection may require its endpoint and accepted-start values.

## Owned surface

KT04 owns a nonproduction projection prototype between a validated `HydrologyStep` and external hydrology terms used by the detailed ANIMO transformation.

The KT03 payload stays frozen. File provenance is not physical forcing. Projection data are immutable and fail closed on field-set, shape, authority, runoff-split and finite-value mismatch.

## Current required behavior

1. Hlpimp=1 legacy provenance fails closed with an explicit Tier-C-review-pending error.
2. Typed Hlpimp=1 candidate projection fails closed for the same reason.
3. Hlpimp=11 legacy provenance may select only the frozen KT03 explicit-interception rule.
4. An independently constructed explicit-state typed packet may use the same frozen explicit projection contract without file identity.
5. File-backed and typed-provider Hlpimp=11 paths produce identical projection digests and source-ordered top-boundary results under the same ANIMO-owned context.
6. No KT04 result is called a completed Hlpimp=1 qualification before KT03F01 independent review.

## Exclusions

No Hlpimp=2 claim, no production source change, no full `Hydro_detailed`/Modflux/transport equivalence, no B2 historical claim, no B3/B4 admission, no canonical TCD mutation, no production shared runtime and no Status A/AA claim.
