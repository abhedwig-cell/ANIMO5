# TCD-042 finite-positive subthreshold numerical seam

Work unit: `ANIMO-UBQ02`

Parent: `TCD-042`

Base: qualified UBQ01 head `6895b67799f26888025eced7188e7190b2a0d07d`

Scope: only `Flpn=0` and `0 < Flux < 1.0d-8`.

Status: `CHARACTERIZED_CLASS_E_ROUTE_NOT_ADMITTED`.

## Boundary inherited from UBQ01

UBQ01 qualified the exact `Flux=0` atom as `B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`. UBQ02 does not reopen that result. The finite-positive interval is separate because the legacy source applies the same fallback coefficients to positive flow:

`A1=1, A2=0, B1=1, B2=0`.

For positive flow the already represented reservoir equation is

`Hetop*dC/dt = Load - Flux*C`,

with

`P = St*Flux/Hetop`,

`A1 = exp(-P)`,

`A2 = (1-exp(-P))/Flux`,

`B1 = (1-exp(-P))/P`,

`B2 = (1-B1)/Flux`.

Therefore the finite-positive fallback is not the exact solution. It is a small-delta numerical approximation selected by the hard-coded `1.0d-8` flow threshold.

## Frozen execution evidence

The source and testbank were rechecked before execution:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

A qualification-only GNU Fortran 14.2 build used the PREP01 diagnostic compile contract. Instrumentation added only a trace at the `UBoundconc` finite-positive subthreshold branch and passed `Tito` into that trace. No production source was changed. The instrumented executable SHA-256 is `7241a72edd5f253539575bb64deab3e1a2860cf7aa1aa06cf32f7cb9d3793d82`.

Eight testbank cases reached `Successful completion of simulation`. `GHGMais` remained blocked at its already known `>outGHG:` input/output contract and produces no absence claim.

A harness correction is worth recording. An earlier failed local attempt was caused by invoking the executable without the required direct-file argument. The correct invocation is `animo_trace Animo.ini`. The failure was not evidence of a missing `general.Inp` alias and is not used in the characterization.

The six cases with finite-positive subthreshold records produced:

- CranGrass: 188;
- CranMais: 299;
- LWKM_gras_1040.2021.2045: 12;
- Puitmijn_Cranendonck_60: 490;
- RuurloGrass: 191;
- Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA: 58.

Total: 1,238 records. Trace hashes are persisted in `integration/animo-science/TCD042_SUBTHRESHOLD_NUMERICAL_CHARACTERIZATION.json`.

## Dimensionless numerical envelope

For each natural record, `P=St*Flux/Hetop` was evaluated. The observed range is:

- minimum `4.2351647362715017e-20`;
- median `2.7105054312137607e-18`;
- 99th percentile `1.5098499996065392e-7`;
- maximum `3.8510200002999744e-7`.

The important point is that the legacy flow threshold maps to an extremely small dimensionless residence-time argument for these cases. Most reachable events are many orders of magnitude below the largest observed P.

## Removing the fallback naively is numerically invalid

UBQ02 explicitly tested the raw positive-flow formulas in binary64. This is not a proposed correction. It is a failure probe.

For 1,189 of the 1,238 natural records, direct binary64 evaluation makes `1-exp(-P)` round to exactly zero. Consequently the direct evaluation of

`f(P)=(1-exp(-P))/P`

has 100 percent relative error for those records. The median relative error over all 1,238 records is 1.0.

The time-average factor is still more sensitive. Define

`g(P)=(P-1+exp(-P))/P^2`,

so `B2=(St/Hetop)*g(P)`. The raw nested binary64 form has median relative error about `7.38e17`; 1,206 of 1,238 records exceed one percent relative error.

Therefore deleting the `Flux < 1.0d-8` branch and evaluating the existing expressions literally is fail-closed. It would replace one approximation problem with catastrophic cancellation.

## Cancellation-safe comparison candidate

To determine whether the discontinuity is numerically unavoidable, UBQ02 compared the exact exponential expressions against the local series

`f(P) = 1 - P/2 + P^2/6 - P^3/24 + P^4/120`

and

`g(P) = 1/2 - P/6 + P^2/24 - P^3/120 + P^4/720`.

This is a comparison method only, not a selected implementation or threshold policy.

Against an 80-decimal-digit reference over the complete observed UBQ02 P envelope, binary64 evaluation of these series had maximum relative errors of approximately:

- `1.1102231667e-16` for `f`;
- `1.1102231194e-16` for `g`.

The same calculation in binary32 reaches about `2.9e-8` maximum relative error. This supplies a precision-sensitivity axis and confirms that the result depends on numerical representation, as expected for Class E work.

Using the binary64 comparison series in the recovered reservoir equation left at most `4.34e-15 kg/ha` coordinate-level conservation roundoff in the evaluated natural records. That number is diagnostic roundoff, not an acceptance tolerance.

The only claim from this exercise is that a cancellation-safe evaluation route exists inside the observed finite-positive envelope. UBQ02 does not select the series order, a switching point, an `expm1` implementation, a new threshold, or a production algorithm.

## Natural materiality

For the legacy fallback, the local signed transaction residual for one represented solute coordinate is

`St*(Load - Flux*C0)`.

Across all 1,238 finite-positive records, the summed mineral-N local residual is `0.01686637146830565 kg/ha`; the sum of absolute local residuals is `0.01687197932049386 kg/ha`.

This result is strongly concentrated. Only four subthreshold records contain nonzero mineral-N load, all in RuurloGrass at `Tito=527, 533, 595, 847`. RuurloGrass contributes a signed `0.016866741552807048 kg N/ha`, and the largest single record contributes about `0.006747669348 kg N/ha`.

In the other cases the observed local N effects are mainly the opposite mechanism: with zero new load, the fallback holds the beginning reservoir concentration fixed and therefore omits the small positive-flow depletion. Those effects are much smaller for the sampled records, but they prove that the finite-positive branch is not equivalent to exact zero even when `Load=0`.

For the 748 subthreshold records in which phosphorus is active, no nonzero P load occurs in this trace. No nonzero DOM or DON load occurs either. UBQ02 therefore does not infer loaded-event materiality for those coordinates from this testbank.

The DOM values are not converted into whole-system carbon claims.

## Classification

The finite-positive seam remains provisionally

`E_NUMERICAL_POLICY`.

This follows B3Q01 directly: the hard-coded small-delta approximation and threshold change how an existing mathematical model is numerically solved. The fact that a stable evaluation can reduce the local residual does not by itself qualify a replacement policy.

UBQ02 has now established the inputs needed for a dedicated Class-E qualification:

- governing equation and exact legacy policy;
- natural reachability;
- natural dimensionless envelope;
- materiality;
- direct-form cancellation failure;
- a high-precision comparison axis;
- a binary32/binary64 precision axis;
- conservation behaviour for a cancellation-safe comparison method.

Still required before any Class-E admission are a selected numerical policy, its full-domain envelope, boundary/continuity behaviour, fallback behaviour, independent numerical review and the applicable B2/G6U route.

Because TCD-042 now contains a qualified exact-zero Class-B atom plus a separate reachable finite-positive Class-E mechanism, canonical incremental intake should decide the child record or TCD representation. UBQ02 does not allocate that identifier itself.

## Nonclaims

UBQ02 does not:

- admit a numerical policy;
- change the `1.0d-8` threshold;
- introduce a tolerance;
- modify production source;
- admit corrected legacy behaviour;
- admit B3 or B4;
- classify the synthetic/high-precision calculation as B2;
- claim absence for GHGMais;
- mark parent TCD-042 fully qualified.
