# ANIMO-NQ04 - TCD-029 Iflsol=4 Detcoef/Coefdc numerical qualification

## Decision surface

This workunit qualifies only the numerical evaluation semantics of canonical `TCD-029`, the `Iflsol=4` cancellation in `Transsub.for:Detcoef` and `Transorp.for:Coefdc`. It does not modify production source and it does not perform B3 admission.

B3I01 allocated this finding as TCD-029. The original proposed owner name `ANIMO-NQ03` is not reused because NQ03 is now the qualified TCD-042-E1 numerical policy workunit. The workunit label changes to NQ04; the canonical TCD identity does not change.

## Pinned evidence

The frozen revision-53 source archive is `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. The relevant frozen members are:

- `Transsub.for` SHA-256 `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`;
- `Transorp.for` SHA-256 `65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`.

NQ02@`40a41089020f78ee1d5181b8afc7bdb511af3193` is reused only for the source-bound cancellation diagnosis, naturally activated state, trajectory sensitivity and conservation/fallback observations. Its diagnostic series switch is not adopted as policy.

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

The qualified mathematical domain is finite binary64 input with `D>0`, `T>0`, and `x>-1`. No new physical state or constitutive relation is introduced.

## Selected binary64 evaluation

At exactly `x=0`, use the analytic limits. For `abs(x)<=1/4`, evaluate degree-24 Taylor polynomials by Horner. The crossover `1/4` is exactly representable in binary64 and is only an evaluation-method crossover. It is not a scientific threshold, solver tolerance, convergence criterion or hidden epsilon.

For `1/4<abs(x)<=1`, evaluate with `log1p` and the direct dimensionless quotients. For `abs(x)>1`, use algebraically equivalent overflow-resistant quotient forms. `A2dc` uses its cancellation-free rational form directly.

The degree-24 truncation bounds at `abs(x)=1/4`, expressed in binary64 unit roundoff `u=2^-53`, are below `0.411u` for F, `0.016u` for G and `0.396u` for H. The CI oracle compares 4289 deterministic points against 100-digit Decimal evaluation. The verification bound is `128u` relative for F, G and H. This is an equation-evaluation verification bound, not a model acceptance tolerance. It sits above the combined degree-24 Horner rounding envelope and the condition-amplified direct-quotient region beginning at `abs(x)>1/4`.

## Natural active control and negative control

At the naturally activated NQ02 Zuiderzeeland state, `x` is approximately `-4.358493040215e-10`. High precision gives `B2=0.00043584930412067741147...`; the selected binary64 policy rounds to `0.0004358493041206774`. The revision-53 direct expression gives approximately `0.2685923078097403`.

For B2dc the high-precision reference is approximately `+0.47279499321842785`, while the direct revision-53 binary64 expression gives approximately `-290.4145135735744`. This sign and magnitude failure is the negative control demonstrating material cancellation.

## Class-E evidence and nonclaims

NQ02 showed that changing this coefficient layer changes ordinary trajectories and solver/fallback activation in natural cases, but it does not uniformly improve mass conservation. That is important: NQ04 qualifies the coefficient evaluation against the existing equations, not against smaller balance residuals.

NQ04 does not qualify TCD-019 solver or fallback semantics. It does not include `Coefdt`, other Iflsol branches, a broad solver replacement, a residual-derived tolerance, historical equivalence, production binding or B4. Historical revision-53 corrected behavior remains `UNKNOWN_WITHOUT_B2`.

The next scientific step, only after exact-final NQ04 qualification, is a separate GOV05 Tier-C B3 admission decision for TCD-029.
