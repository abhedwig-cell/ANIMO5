# TCD-042-E1 finite-positive upper-reservoir numerical policy qualification

Work unit: `ANIMO-NQ03`

Target: `TCD-042-E1`

Class: `E_NUMERICAL_POLICY`

Scope: only `Flpn=0` and `0 < Flux < 1.0d-8`.

This workunit selects a restricted numerical evaluation policy. It does not patch production source, admit B3, admit parent TCD-042, reserve another TCD, or modify the already qualified TCD-042-B1 exact-zero atom.

## Upstream and provenance

NQ03 was started only after live verification that no NQ03 branch existed and after live verification of the B3I05 qualified child routing. The work branch was created from B3I05 head `7fa0162415e02a6f0167e71b48ae38177a9e06e0`.

Authoritative numerical evidence is pinned to UBQ02 head `bb572bb5d431f91d780018a1acbb345fbcfced37`. The frozen B0 identities remain:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

UBQ01 head `6895b67799f26888025eced7188e7190b2a0d07d` is used only as the exact-zero boundary reference.

## Numerical reconstruction

The represented upper-reservoir equation for constant forcing over one hydrological interval is

`Hetop*dC/dt = Load - Flux*C`.

Define the dimensionless conditioning coordinate

`P = St*Flux/Hetop`.

For positive flow the exact coefficients can be written as

`A1 = exp(-P)`

`A2 = (St/Hetop)*f(P)`

`B1 = f(P)`

`B2 = (St/Hetop)*g(P)`

where

`f(P) = (1-exp(-P))/P`

and

`g(P) = (P-1+exp(-P))/P^2`.

Then

`C1 = C0*A1 + Load*A2`

and

`Cavg = C0*B1 + Load*B2`.

The conservation identity is

`Hetop*(C1-C0) = St*Load - St*Flux*Cavg`.

This reconstruction is the basis for policy selection. No threshold is inferred from a legacy output residual.

## Why the legacy direct evaluation is not a candidate

UBQ02 already established natural reachability of 1,238 finite-positive subthreshold records in six executed cases. Their observed dimensionless envelope is

`4.2351647362715017e-20 <= P <= 3.8510200002999744e-7`.

The median is `2.7105054312137607e-18` and the 99th percentile is `1.5098499996065392e-7`.

On the legacy nested binary64 expression, `1-exp(-P)` becomes exactly zero in 1,189 of the 1,238 natural UBQ02 records. The consequence is not merely a small rounding error. `f` can have 100 percent relative error and the nested `g=(1-f)/P` error reaches the order of `1/P`. On the dense NQ03 envelope probe the maximum relative error in `g` is `4.722366482869656e19`.

Deleting the small-flow branch and evaluating the legacy formulas literally therefore remains rejected.

## expm1 study

The cancellation-safe first-order expression

`f(P) = -expm1(-P)/P`

works well in binary64. Across the dense natural envelope its maximum relative error against the rounded 100-decimal-digit reference is about `1.11e-16`.

That does not solve `g`. If `g` is reconstructed as `(1-f)/P`, the subtraction of two quantities close to one introduces a second cancellation. At the lower natural P values the relative error is again 100 percent. The algebraically equivalent `P+expm1(-P)` numerator has the same second-order conditioning problem for sufficiently small P.

Thus `expm1` is a valid component for `f`, but is not by itself a complete upper-reservoir policy.

## Series study and order selection

For positive P the two analytic series are

`f(P) = 1 - P/2 + P^2/6 - P^3/24 + ...`

`g(P) = 1/2 - P/6 + P^2/24 - P^3/120 + ...`.

Because the natural P envelope is far below one, the alternating terms decrease monotonically. The first omitted term therefore bounds the absolute truncation error.

At the observed maximum `P=3.8510200002999744e-7`:

- degree 1 gives an `f` truncation error about `2.47e-14` and `g` about `6.18e-15`; this is larger than binary64 unit roundoff and is rejected;
- degree 2 gives an `f` error `2.3796662284e-21` and `g` error `4.7593325179e-22`;
- the corresponding alternating remainder bounds are `2.3796664117e-21` and `4.7593328234e-22`.

Binary64 unit roundoff is `1.1102230246251565e-16`. Degree 2 is therefore the lowest tested polynomial order whose analytic truncation is already far below the representation limit over the complete natural envelope. Degrees 3 and 4 are numerically valid there but add no qualified accuracy at binary64 resolution.

On 2,008 unique envelope probes, the binary64 degree-2 values for both `f` and `g` round to exactly the same binary64 values as the 100-decimal-digit oracle.

## Precision sensitivity

The project precision baseline already treats explicit real64 as the conservative scientific/reference computation, while FP32 or mixed precision requires separate qualification. NQ03 follows that boundary and does not create a broader precision admission.

With stepwise binary32 emulation, the same degree-2 representation remains cancellation-safe but has expected representation-level sensitivity. Across the dense natural envelope the maximum relative differences to the high-precision reference are approximately:

- `A1`: `2.9644e-8`;
- `f`: `2.9776e-8`;
- `g`: `2.9749e-8`.

These results are recorded only as a precision sensitivity axis. Binary32 is not selected as the canonical NQ03 policy.

## Conservation evidence

Use `Lbar=(St/Hetop)*Load`. The dimensional balance can be divided by `Hetop` to obtain the normalized identity

`C1-C0 = Lbar - P*Cavg`.

NQ03 evaluates three nondegenerate probes across the dense P envelope: decay-only, loaded beginning state, and source-only. With the selected binary64 degree-2 coefficients, the largest observed absolute floating-point identity remainder is `1.1102230246251565e-16` in normalized concentration coordinates.

This is reported as roundoff evidence only. It is not used to define a tolerance and no acceptance threshold is derived from it.

## Interval subdivision sensitivity

For constant `Flux` and `Load`, the exact affine reservoir solution has the semigroup property. One full interval and repeated equal subintervals should therefore represent the same physical solution.

NQ03 compares one interval with 2, 4, 8, 16 and 32 equal substeps over the dense natural P envelope. The largest full-versus-split end-state difference grows from about `1.11e-16` at two substeps to `1.89e-15` at 32 substeps. The largest time-average difference grows from about `1.11e-16` to `8.33e-16`.

The growth is consistent with accumulation of binary64 operations, not a timestep-dependent change of the represented reservoir equation. NQ03 derives no timestep tolerance from these numbers.

## Continuity to the exact-zero boundary

As `P -> 0+`:

`A1 -> 1`

`f(P) -> 1`

`g(P) -> 1/2`.

Therefore

`A2 -> St/Hetop`

`B1 -> 1`

`B2 -> St/(2*Hetop)`.

These are exactly the unique zero-flow coefficients already qualified by UBQ01 for TCD-042-B1. NQ03 does not apply its finite-positive evaluation at `P=0` and does not reopen or redefine B1. It only demonstrates one-sided continuity of E1 to that existing boundary.

## Selected restricted policy

The selected candidate is

`NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY`.

Applicability is restricted to all of the following:

- `Flpn=0`;
- `0 < Flux < 1.0d-8`;
- `Hetop > 0`;
- `0 < P <= 3.8510200002999744e-7`;
- canonical evaluation in binary64.

Within that envelope evaluate

`A1 = exp(-P)`

`f = 1 - P/2 + P^2/6`

`g = 1/2 - P/6 + P^2/24`

`A2 = (St/Hetop)*f`

`B1 = f`

`B2 = (St/Hetop)*g`.

There is no switching threshold inside the qualified P envelope. The `1.0d-8` Flux value remains only the legacy trigger defining the TCD-042-E1 investigation scope. NQ03 does not select it as a new numerical threshold.

The upper P bound is an applicability boundary from the complete observed UBQ02 natural envelope, not a claim that values above it are physically invalid. Any finite-positive event above that P value remains numerically unqualified by NQ03 and must fail closed at the qualification level until a broader Class-E policy is studied.

## Qualification disposition

The policy is sufficiently supported for restricted Class-E qualification because:

- the governing equation and conserved quantity are explicit;
- the legacy policy and its cancellation failure are reconstructed;
- a 100-digit independent oracle is defined;
- direct binary64, expm1, series order and binary32 sensitivity axes are compared;
- degree 2 is selected from an analytic truncation criterion rather than legacy matching;
- the complete observed natural P envelope is covered;
- conservation and interval subdivision behave at binary64 roundoff scale without deriving a tolerance from those residuals;
- the finite-positive limit is continuous with, but does not redefine, the UBQ01 exact-zero atom;
- the scope outside the observed P envelope remains explicitly unqualified.

Final NQ03 closeout still requires the live B3I05 qualified status to be rechecked and the branch validator/CI to pass. Independent numerical review remains a separate downstream gate before any admission or production implementation.
