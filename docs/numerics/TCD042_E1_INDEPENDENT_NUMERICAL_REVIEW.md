# TCD-042-E1 independent numerical review

Work unit: `ANIMO-NQ03R`

Reviewed work unit: `ANIMO-NQ03`

Reviewed head: `8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6`

Outcome: `INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY`.

This is a methodologically independent second-line reconstruction. It is not an organizational-independence claim. The review authorizes no production patch, B3 admission, parent TCD-042 admission, new TCD reservation, or change to TCD-042-B1.

## Independent reconstruction

Starting from the reservoir balance rather than the NQ03 implementation, the finite-positive no-ponding reservoir satisfies

`Hetop*dC/dt = Load - Flux*C`.

With constant forcing over interval `St`, define

`P = St*Flux/Hetop`.

The exact end-state and interval-average coefficients are

`A1 = exp(-P)`

`A2 = (St/Hetop)*f(P)`

`B1 = f(P)`

`B2 = (St/Hetop)*g(P)`

with

`f(P)=(1-exp(-P))/P`

and

`g(P)=(P-1+exp(-P))/P^2`.

The associated conservation identity is

`Hetop*(C1-C0)=St*Load-St*Flux*Cavg`.

This independently confirms that `P`, not raw `Flux`, is the conditioning coordinate. A raw-flow threshold alone cannot express the numerical conditioning because the same Flux maps to different P when `St/Hetop` changes.

## Natural envelope and reference

UBQ02 pins 1,238 finite-positive records across six traced cases, with

`4.2351647362715017e-20 <= P <= 3.8510200002999744e-7`.

The review used a fresh 120-decimal-digit `Decimal.exp` reference and did not use the candidate polynomial as the mathematical oracle. The probe set contains 2,001 logarithmic points plus the seven persisted natural quantile points. With the exact binary64 values produced by the logarithmic construction, these are 2,008 unique probe values.

Direct nested binary64 evaluation reproduces the NQ03 failure characterization: maximum relative error is 1.0 for `f` and approximately `4.722366482869656e19` for `g`. `expm1` reduces the maximum `f` relative error to approximately `1.11e-16`, but `g=(1-f)/P` still reaches 100 percent relative error. Therefore neither direct nested evaluation nor `expm1` alone is a complete policy.

## Series order

Independent expansion gives

`f(P)=1-P/2+P^2/6-P^3/24+...`

`g(P)=1/2-P/6+P^2/24-P^3/120+...`.

At the natural maximum P, the absolute degree-1 truncation errors are approximately `2.4717256025e-14` for `f` and `6.1793141252e-15` for `g`. Those exceed binary64 half-ulp scales near the represented values. Degree 2 reduces the errors to approximately `2.3796662284e-21` and `4.7593325179e-22`, far below the corresponding representation scale.

Thus degree 2 is the lowest polynomial order satisfying the declared truncation criterion over the restricted natural envelope. Degrees 3 and above are valid but add no justified accuracy for this binary64 policy.

Using the Horner order employed by the NQ03 validator, the degree-2 `f` and `g` values equal the rounded 120-digit reference at all 2,008 probes.

## Precision, conservation and subdivision

The independent binary32 emulation reproduces maximum relative sensitivities of approximately `2.96435e-8` for `A1`, `2.97765e-8` for `f`, and `2.97494e-8` for `g`. This supports the NQ03 decision to keep binary32 as a sensitivity axis only.

Across the same dense envelope and the three declared state/load probes, the largest normalized conservation remainder is `1.1102230246251565e-16`. The review treats this only as observed floating-point roundoff and does not derive an acceptance tolerance from it.

The equal-subinterval check for 2, 4, 8, 16 and 32 subdivisions reproduces the persisted NQ03 values. At 32 substeps the largest end-state difference is `1.887379141862766e-15` and the largest interval-average difference is `8.326672684688674e-16`. The pattern is consistent with accumulation of binary64 operations rather than a changed physical interval model.

## Exact-zero boundary

The one-sided finite-positive limit is

`A1 -> 1`

`A2 -> St/Hetop`

`B1 -> 1`

`B2 -> St/(2*Hetop)`.

That is the UBQ01 exact-zero boundary. The review therefore confirms continuity without reopening or redefining TCD-042-B1.

## Review finding: evaluation-order contract

The review found one implementation-level issue that should remain visible downstream. The exact-rounded dense claim depends on the Horner evaluation order used by the NQ03 validator. If the mathematically equivalent polynomial is evaluated literally as

`1 - P/2 + P^2/6`

and

`1/2 - P/6 + P^2/24`,

ordinary binary64 operation ordering differs from the rounded high-precision reference by one ulp on some probes. In the 2,008-point review set, 67 `f` values and 73 `g` values differ; 129 unique probe points have at least one such difference. The maximum relative difference remains approximately one binary64 unit roundoff.

This does not overturn the restricted policy because NQ03 explicitly selected no production implementation and the mathematical degree-2 approximation remains inside its analytic envelope. It does mean that a later production-binding workunit must freeze the evaluation order and FP-contraction/reassociation contract if it wants to preserve the exact-rounded claim. Alternatively it must define an equation-derived ulp bound and qualify the chosen implementation against that bound.

This finding is deliberately not converted into a hidden epsilon or residual-derived tolerance.

## Scope review

A live compare from B3I05 head `7fa0162415e02a6f0167e71b48ae38177a9e06e0` to NQ03 head `8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6` shows 11 changed files. They are confined to the NQ03 workflow, numerical documentation, machine-readable evidence and `tools/nq03` validation/oracle files. No `src/` file, canonical TCD register, TCD-042-B1 artifact or B3 admission record was modified.

## Disposition

The restricted policy is independently supported for the declared envelope:

`Flpn=0`, `0<Flux<1.0d-8`, `Hetop>0`, `0<P<=3.8510200002999744e-7`, binary64.

Review disposition:

`INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY`.

The pass does not admit corrected legacy behaviour and does not authorize production binding. A downstream admission-readiness or production-binding workunit must carry the evaluation-order finding explicitly.
