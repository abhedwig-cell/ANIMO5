# ANIMO-B3D17 — TCD-028 GOV04 Tier-C Formal Disposition

## Decision

`QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION`

Formal B3 disposition for `TCD-028`:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

This is a disposition only. `TCD-028` is **not admitted** by ANIMO-B3D17.

## Live authority recheck

Before creating this workunit, the repository was rechecked live. No pre-existing `ANIMO-B3D17`, no later TCD-028 formal-disposition/admission branch, and no aggregate branch later than RG05F were present. The current aggregate authority remained:

`ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`

Two post-RG05F atomic admissions were observed but are not merged or composed here:

- `ANIMO-B3D15@22e48f7e2c1eaa1245f034de2d909191d9cfa227` — TCD-030;
- `ANIMO-B3D16@8650ea9e716336520d8d7df5f9ea2b393d17ab98` — TCD-023.

The independent review handoff issue #46 is closed as completed with one result comment. The final review authority is:

`ANIMO-B3B08R@3281f98feef7af4822e85a0f011ede0b779de07b`

Its validated semantic result is `PASS`, with Actions run `34523750753`, job `103027480186`.

## Scientific disposition

The independently reviewed scientific ownership statement is accepted for disposition: `SuStdiorma`, `SuStdiorni`, and conditional `SuStdiorpo` are current-plough-event transaction accumulators. At every active `Pl(I) > 0` event they must start from the additive identity before current-event accumulation. A surviving prior-event scalar has no separate physical owner because the previous redistribution has already been written into `CoStdiorma`, `CoStdiorni`, and conditional `CoStdiorpo` state.

The bounded candidate remains exactly:

```fortran
SuStdiorma = 0.0
SuStdiorni = 0.0
If (Ipo.Eq.1) SuStdiorpo = 0.0
```

inserted at the beginning of each active plough event before the existing stable-pool accumulation loop. No other `Addit.for` change is part of the disposition.

The B3 qualification class remains `B_LOCAL_ALGEBRA_INDEX_SPECIES`. GOV04 risk remains Tier C because the scientific interpretation depends on initialization/lifecycle semantics and state/source ownership. The review found no Tier-D trigger: there is no composition, B4 scope, production-bound change, multi-TCD change, or whole-model baseline claim.

## Historical route

GOV03 remains authoritative at `cbd262bdabe92923113b7326f2f42822ce9a971c` and records:

- `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`;
- `ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

Therefore the formal disposition uses `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`. Historical revision-53 Intel/native manifestation remains `UNKNOWN_WITHOUT_B2`. Current-GNU `-fno-automatic` persistence is diagnostic B1 evidence, not historical B2 evidence and not a historical-fidelity claim.

## Expected-difference boundary

Only repeated active plough events with nonzero affected stable pools may change. Allowed consequences are stable DOM/DON/conditional-DOP redistribution, causally downstream physical state and fluxes, dependent balances/reports, and restart output only as a downstream image of already changed state.

The disposition does not authorize changes to management timing, plough trigger semantics, restart serialization/checkpoint representation, solver/tolerance policy, numerical precision policy, unrelated process ordering, unrelated ledgers, frozen B0 identities, or non-plough source semantics.

The eight completing frozen testbank cases remain supporting non-interference evidence only; the four plough-active cases are non-discriminating because the observed accumulators remain zero across the 31 observed events.

## Explicit non-actions

ANIMO-B3D17 does not:

- admit TCD-028 into B3;
- modify production or corrected-legacy source;
- modify frozen B0;
- modify the canonical TCD register;
- compose TCD-028 with any other discrepancy;
- open B4 or production migration;
- update aggregate central regie;
- convert historical uncertainty into a fidelity claim.

The next allowed workunit after validated closeout is a **separate Tier-C B3 admission-decision workunit** that consumes this disposition and the independent review by exact immutable pins.
