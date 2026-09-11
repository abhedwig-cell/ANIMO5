# ANIMO-NQ04 - TCD-029 Iflsol=4 Detcoef/Coefdc numerical qualification

## Decision surface

This workunit qualifies only the numerical evaluation semantics of canonical `TCD-029`, the `Iflsol=4` cancellation in `Transsub.for:Detcoef` and `Transorp.for:Coefdc`. It does not modify production source and it does not perform B3 admission.

B3I01 allocated this finding as TCD-029. The original proposed owner name `ANIMO-NQ03` is not reused because NQ03 is now the qualified TCD-042-E1 numerical-policy workunit. The workunit label changes to NQ04; the canonical TCD identity does not change.

## Pinned evidence

The frozen revision-53 source archive is `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. The frozen testbank is `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`. Relevant frozen members are:

- `Transsub.for` SHA-256 `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`;
- `Transorp.for` SHA-256 `65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`.

NQ02@`40a41089020f78ee1d5181b8afc7bdb511af3193` is reused only for the source-bound cancellation diagnosis, naturally activated state, trajectory sensitivity and conservation/fallback observations. Its diagnostic series switch is not adopted as policy. Canonical allocation to TCD-029 comes from B3I01 and remains unchanged.

## Existing equations

For Detcoef let `D=Mto+Rhbd*Avsocf`; for Coefdc use `D=Mto+Rhbd*Avadco`. Let `x=Hv*T/D` and, for Coefdc, `q=Rhbd*Avadcodc`.

Revision-53 evaluates the Iflsol=4 coefficients through expressions that are exact in real arithmetic but poorly conditioned as `x` approaches zero. The same equations can be written as:

```text
F(x) = log1p(x)/x                              F(0)=1
G(x) = ((1+x)*log1p(x)-x)/x^2                 G(0)=1/2
H(x) = (x-log1p(x))/x^2                       H(0)=1/2

A2   = T/D * F(x)
B2   = T/D * G(x)
A2dc = -T/D^2 * q/(1+x)
B2dc = -T/D^2 * H(x) * q
```

The qualified mathematical domain is finite binary64 input with `D>0`, `T>0`, and `x>-1`. No new physical state, constitutive relation, solver stopping rule or acceptance tolerance is introduced.

## Selected binary64 evaluation

At exactly `x=0`, use the analytic limits. For `abs(x)<=1/4`, evaluate degree-24 Taylor polynomials by Horner:

```text
F(x) = sum(k=0..24) (-1)^k x^k/(k+1)
G(x) = sum(k=0..24) (-1)^k x^k/((k+1)(k+2))
H(x) = sum(k=0..24) (-1)^k x^k/(k+2)
```

The crossover `1/4` is exactly representable in binary64 and is only an evaluation-method crossover. It is not a scientific threshold, solver tolerance, convergence criterion or hidden epsilon.

For `1/4<abs(x)<=1`, evaluate with `log1p` and the dimensionless quotients. For `abs(x)>1`, use the algebraically equivalent overflow-resistant forms

```text
G(x) = ((1+1/x)*log1p(x)-1)/x
H(x) = (1-log1p(x)/x)/x
```

while `F(x)=log1p(x)/x`. `A2dc` uses the cancellation-free rational form directly.

The degree-24 truncation bounds at `abs(x)=1/4`, expressed in binary64 unit roundoff `u=2^-53`, are below `0.411u` for F, `0.016u` for G and `0.396u` for H. The CI oracle compares 4756 deterministic finite points against high-precision Decimal evaluation. Observed maximum relative errors are below `1.73u` for F, `19.45u` for G and `7.96u` for H. The declared verification envelope is `128u` relative for F, G and H. This is an equation-evaluation verification bound, not a model acceptance tolerance.

## Natural active control and negative control

At the naturally activated NQ02 Zuiderzeeland state, `x` is approximately `-4.358493040215e-10`. High precision gives `B2=0.00043584930412067741147...`; the selected binary64 policy rounds to `0.0004358493041206774`. The revision-53 direct expression gives approximately `0.2685923078097403`.

For B2dc the high-precision reference is approximately `+0.47279499321842785`, while the direct revision-53 binary64 expression gives approximately `-290.4145135735744`. This sign and magnitude failure is the negative control demonstrating material cancellation.

NQ02 also showed that replacing the coefficient evaluation changes ordinary scientific trajectories and fallback activation in natural cases but does not uniformly improve the TCD-019 mass residual. Therefore conservation improvement is explicitly not an acceptance criterion for NQ04.

## Class-E qualification

The qualified correction mechanism is numerical evaluation of the same closed analytical coefficient functions. The evidence package requires:

1. exact frozen B0 and source-member identity;
2. algebraic equivalence to the revision-53 real-arithmetic equations;
3. analytic zero limits;
4. 100-plus-digit reference evaluation with dense edge coverage;
5. the naturally activated NQ02 control point;
6. explicit failure of the legacy direct binary64 form as a negative control;
7. no residual-derived tolerance;
8. no solver, state, restart or constitutive change;
9. historical behavior preserved as `UNKNOWN_WITHOUT_B2`;
10. fail-closed behavior outside the declared mathematical domain.

The workunit is GOV05 Tier C because it qualifies a numerical policy. Same-agent adversarial review may close the workunit only with assurance `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT`.

## Nonclaims

NQ04 does not qualify TCD-019 solver or fallback semantics. It does not include `Coefdt`, other Iflsol branches, broad solver replacement, residual-derived tolerances, historical equivalence, production binding or B4. It does not modify the canonical TCD register. It does not perform B3 admission.

Historical revision-53 corrected behavior remains `UNKNOWN_WITHOUT_B2`. Bitwise production binding is not established because future production implementation must still freeze or independently qualify compiler-level reassociation, contraction and intrinsic semantics.

Only after exact-final NQ04 qualification may a separate GOV05 Tier-C B3 admission decision for TCD-029 be opened.
