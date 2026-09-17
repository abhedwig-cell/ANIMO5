# ANIMO-KT06 Work Unit Contract

Workunit: `ANIMO-KT06 — Explicit Hydrology Runtime Interval Binding`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE`.

## Reconciliation

A parallel workstream completed the compiled explicit-state ANIMO hydrology
adapter as **ANIMO-KT05** before this runtime-binding workunit was persisted.

Canonical KT05 authority consumed here:

- KT05 closeout head:
  `3319e57adbf6036a86684f8e26d9559454c07b82`;
- frozen KT05 implementation:
  `69dd607ba1efa28de3f83cc963526021352b3311`;
- exact-head KT05 CI:
  `35285836540 -> SUCCESS`;
- verdict:
  `QUALIFIED_NONPRODUCTION_EXPLICIT_STATE_FORTRAN_HYDROLOGY_CALL_BOUNDARY_ADAPTER_NO_HYDRO_DETAILED_EXECUTION_OR_RUNTIME_INTEGRATION`.

KT06 therefore owns the next layer only. It does not duplicate KT05.

## Purpose

Combine the frozen KT02 model-neutral interval runtime with the qualified
nonproduction KT05 explicit-state `hydrology_step_t` carrier and projection
boundary.

The bounded question is:

> Can a complete KT05 explicit-state hydrology packet be bound to a KT02
> requested interval while KT02 remains the sole accepted-time/publication
> authority and hydrology forcing remains outside accepted continuation state?

## Time ownership

KT03/KT05 producer endpoint and duration fields remain producer metadata.

For this first proof, KT06 deliberately supports only:

- one pinned runtime calendar contract;
- exact whole-day KT02 time coordinates;
- producer endpoint and duration metadata that are exact nonnegative integers
  in REAL64;
- one configured nonnegative day-index offset between runtime and producer
  coordinates.

The adapter validates exact endpoint and duration agreement. It does not let
producer metadata advance runtime time.

Fractional producer coordinates, subday runtime mapping and calendar
conversion are separate future qualification surfaces.

## Scientific ownership

The KT06 client validates the complete KT05 `hydrology_step_t` and calls the
qualified KT05 producer-to-`Hydro_detailed` external projection.

It does **not** execute `Hydro_detailed`, `Modflux`, reactions, transport or
ANIMO conservation/admissibility. The accepted payload in this proof is only a
synthetic state token.

Returning an admissible no-op candidate therefore proves runtime binding
mechanics only, not scientific acceptance.

## Hlpimp=1 isolation

KT06 requires the KT05 explicit-interception path. It does not consume
KT03F01, KT04 Hlpimp=1 semantics or any fabricated interception state.

## Governance

Runtime interval mapping can alter model behaviour if wrong, so KT06 is a
GOV04 Tier C candidate. Same-agent review can find/remediate defects but cannot
satisfy the genuinely independent second-line review gate.

## Exclusions

No Hlpimp=1 or Hlpimp=2 semantics, no `Hydro_detailed` execution, no ANIMO
scientific admissibility, no full real-LWKM payload equivalence, no retry or
timestep-selection policy, no fractional/subday mapping, no production
migration, no B3/B4 admission and no Status A/AA claim.
