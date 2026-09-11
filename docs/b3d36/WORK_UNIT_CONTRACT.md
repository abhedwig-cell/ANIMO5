# ANIMO-B3D36 - TCD-029 cancellation-safe coefficient numerical policy atomic B3 admission

## Decision surface

This workunit makes one atomic B3 admission decision for canonical `TCD-029`, using exact-final ANIMO-NQ04 as its numerical-policy qualification authority. It does not implement the policy in production source.

The admitted correction is restricted to the NQ04-qualified binary64 evaluation of the existing revision-53 `Iflsol=4` `Detcoef` and `Coefdc` coefficient functions. No TCD-019 solver or fallback behavior is composed into this decision.

## Authorities

- current aggregate: `ANIMO-RG05L@214062fe773618ea77c7c74867cc8d9a2a4eef6d`;
- global negative queue authority: `ANIMO-B3Q03@67a87c6a650d503c1b0968ada2cc5eaa5155aa42`, which lists TCD-029 as top-level unadmitted;
- canonical allocation: `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`;
- numerical qualification: `ANIMO-NQ04@bfd736b88b6fc4f2a66970b812172729c1923562`;
- NQ04 exact-final CI: run `34600616004`, job `103266708308`, success;
- governance: GOV05 `f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, GOV04 `1bbe4c211197590f346803106e45dca5faae79fc`, GOV03 `cbd262bdabe92923113b7326f2f42822ce9a971c`, B3Q01 `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

## Admitted identity and scope

Candidate identity:

`IFLSOL4_DETCOEF_COEFDC_CANCELLATION_SAFE_BINARY64_EVALUATION_ON_NQ04_QUALIFIED_DOMAIN`

Supported domain is exactly NQ04:

- finite binary64 inputs;
- `D>0`;
- `T>0`;
- `x=Hv*T/D>-1`;
- `x=0` uses the analytic limits `F=1`, `G=H=1/2`;
- `abs(x)<=0.25` uses the degree-24 Horner series qualified by NQ04;
- `0.25<abs(x)<=1` uses the dimensionless `log1p` quotient forms;
- `abs(x)>1` uses the algebraically equivalent large-x forms qualified by NQ04;
- outside that domain remains fail-closed and unqualified.

The `128u` NQ04 bound is an equation-evaluation oracle bound. It is not a model acceptance tolerance, solver threshold or residual criterion.

## Evidence and historical uncertainty

NQ04 established algebraic identity with the revision-53 real-arithmetic coefficient equations, analytic zero limits, a 4756-point high-precision deterministic oracle, and the naturally activated NQ02 control where direct binary64 evaluation catastrophically loses significance. Its exact-final validator, oracle and scope guard are green.

No qualified B2 exists. Therefore the formal disposition is scientific admission with historical uncertainty. Historical behavior remains exactly `UNKNOWN_WITHOUT_B2`. The high-precision oracle, NQ02 diagnostic descendants and natural controls are not promoted to B2.

The change is scientifically admitted because it is a bounded numerical evaluation policy for the same analytical functions, with equation-derived high-precision evidence and explicit scope. It is not admitted because a mass residual gets smaller. NQ02 in fact showed non-uniform residual response, which is retained as a negative control against conservation masking.

## Expected difference

If later implemented in a separately authorized production migration, coefficient values and downstream trajectories may differ when the direct revision-53 binary64 formulas suffer cancellation. The expected direction and magnitude are input dependent. No claim is made that all model balances improve or that legacy trajectories are reproduced.

Unaffected by this admission are TCD-019 nonlinear solver/fallback semantics, `Coefdt`, all non-`Iflsol=4` branches, persistent state, restart semantics, global tolerances, input validation, frozen B0 and production source.

## GOV05 Tier C review

Numerical-policy admission forces Tier C. Substantive authoring freezes before review. The same-agent adversarial pass must bind the immutable authoring head and must use the assurance label `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT`. A same-agent pass is never genuinely independent.

## Nonclaims

This workunit does not modify production source, frozen B0, the canonical TCD register or the current aggregate. It does not admit TCD-019. It does not qualify or admit `Coefdt` or other Iflsol branches. It does not open B4, authorize production or establish historical fidelity.
