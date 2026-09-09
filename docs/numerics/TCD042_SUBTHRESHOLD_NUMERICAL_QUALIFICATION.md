# TCD-042 finite-positive subthreshold numerical seam qualification

Work unit: `ANIMO-UBQ02`

Branch: `work/animo-ubq02-tcd042-subthreshold-numerical-seam`

Parent: `TCD-042`

Scope: `0 < Flux < 1.0d-8` with `Flpn=0` only.

## Decision boundary

UBQ01 qualified only the exact `Flux=0` atom as `B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`. It deliberately left the finite-positive interval open because the same legacy fallback is also used for small but nonzero throughflow.

UBQ02 qualifies that remaining interval as a distinct Class-E numerical seam. It does not admit a numerical policy, a threshold, a tolerance, a source correction, corrected legacy, B3, B4 or production migration.

Frozen identities remain:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Source equation

For the no-ponding upper reservoir the revision-53 source defines

`P = St*Flux/Hetop`

and, for the ordinary positive-flow branch,

`A1 = exp(-P)`

`A2 = (1-A1)/Flux`

`B1 = (1-A1)/P`

`B2 = (1-B1)/Flux`.

The end and interval-average concentration are then

`C1 = C0*A1 + Load*A2`

and

`Cavg = C0*B1 + Load*B2`.

For `Flux < 1.0d-8`, however, the legacy source replaces these coefficients by

`A1=1, A2=0, B1=1, B2=0`.

That fallback is not the positive-flow equation evaluated accurately. It freezes the existing reservoir concentration and removes the same-step load contribution from both end and average state.

## Dimensionless conditioning

The numerically relevant small parameter is not `Flux` by itself but

`P = St*Flux/Hetop`.

Define

`phi1(P) = (1-exp(-P))/P`

and

`phi2(P) = (P-1+exp(-P))/P^2`.

Then

`A2 = (St/Hetop)*phi1`

`B1 = phi1`

`B2 = (St/Hetop)*phi2`.

This separates the physical time/geometry scale from the cancellation-prone dimensionless functions.

For small positive `P`,

`phi1 = 1 - P/2 + P^2/6 - ...`

and

`phi2 = 1/2 - P/6 + P^2/24 - ...`.

Thus neither `A2` nor `B2` tends to zero as positive throughflow becomes tiny. The legacy fallback therefore cannot be justified as the positive-flow limiting coefficients.

## Natural reachability and P range

The B0-hash-pinned testbank scan inherited from UBQ01 found 1,238 finite-positive subthreshold records across six of eight executable cases. UBQ02 independently reconstructed the same 1,238 branch activations with qualification-only tracing.

Across those records the observed dimensionless range is

`4.2351647362715017e-20 <= P <= 3.8510200002999744e-7`.

The detailed case summary is in `integration/animo-numerics/UBQ02_NATURAL_SUBTHRESHOLD_SUMMARY.csv`.

This is an important numerical result: one fixed dimensional `Flux` threshold spans many orders of magnitude in the actual conditioning variable `P`. Therefore the historical threshold value cannot itself be treated as a general binary64 conditioning criterion.

## Natural nonzero-load materiality

Most finite-positive subthreshold records in the frozen testbank have zero same-step upper-reservoir load. `RuurloGrass` nevertheless contains four naturally activated records with nonzero NH4 and NO3 precipitation loads at qualification-trace call ordinals 527, 533, 595 and 847.

For those four records:

- `St=1 d`;
- `Hetop=0.02 m`;
- `P` is between `6.776263578034403e-19` and `2.710505431213761e-18`;
- the positive-flow load-response coefficient is therefore effectively the same physical scale as the exact-zero limit, `St/Hetop=50`, not zero.

At call ordinal 527 the legacy fallback suppresses approximately

- `0.005067751667999977 kg ha-1` NH4-N end-storage response;
- `0.0016799176799999793 kg ha-1` NO3-N end-storage response;
- total mineral N `0.006747669347999956 kg ha-1`.

The other three nonzero-load witnesses each suppress about `0.0033738353488 kg ha-1` total mineral-N end-storage response. Full captured values are in `integration/animo-numerics/UBQ02_RUURLO_LOAD_WITNESSES.csv`.

This proves natural materiality of the finite-positive branch without using a tolerance. The issue is not merely theoretical reachability.

## Why the direct positive-flow formulas cannot simply be switched back on

The ordinary source formulas are themselves badly conditioned at small `P` if evaluated literally in binary64.

Over the 1,238 natural subthreshold `P` values, a direct binary64 evaluation of

`(1-exp(-P))/P`

collapses to exactly zero in 1,189 records because `exp(-P)` rounds to one before the subtraction. The derived direct `phi2` evaluation can then become enormous or even negative. The largest absolute direct `phi2` value observed in this diagnostic was about `2.36e19`, while the mathematical small-P value is near `0.5`.

Therefore replacing the legacy fallback by the original literal formula is not a qualified solution.

## Cancellation-safe comparison candidate

For analysis and future numerical-policy work, UBQ02 qualifies the following as a comparison candidate only:

`phi1 = -expm1(-P)/P`

with

`phi2 = 1/2 - P/6 + P^2/24 - P^3/120 + P^4/720 - ...`

for small `P`.

Then

`A2 = (St/Hetop)*phi1`, `B1=phi1`, and `B2=(St/Hetop)*phi2`.

Against a 100-decimal-digit analytic reference over all 1,238 natural `P` values, the binary64 diagnostic error magnitude of this comparison candidate remained at approximately one binary64 rounding unit: maximum absolute differences were `1.1102230246251565e-16` for `phi1` and `5.551115123125783e-17` for `phi2`.

These magnitudes are diagnostics only. They are not a tolerance and do not constitute a numerical acceptance policy.

## Classification

The finite-positive seam is qualified as

`E_NUMERICAL_POLICY`.

It is not Class A because the fallback changes persistent reservoir state and therefore future trajectory. It is not Class C because UBQ01 already proved that the persistent upper-reservoir owner exists. It is not merely the exact-zero Class-B atom because, for `Flux>0`, the governing positive-flow equation already exists and the unresolved question is how that equation should be evaluated robustly in finite precision.

The parent TCD-042 is therefore still not fully qualified for admission. The recommended routing is a child atom such as `TCD-042-E1`, but UBQ02 does not create or canonically allocate that child itself. That routing belongs to canonical incremental intake.

## Numerical policy still open

UBQ02 does not select:

- the historical `Flux=1.0d-8` threshold as an admitted conditioning threshold;
- any replacement threshold;
- a `P` switch value;
- a truncation order for production series evaluation;
- a global absolute or relative tolerance;
- a production `expm1`/series implementation.

A future numerical-policy workunit must derive those choices from conditioning, convergence, representation and scientific sensitivity evidence, not from a threshold chosen to make B1 comparisons pass.

The NQ01 rule remains controlling: a small floating difference is not automatically acceptable, and no tolerance may be reverse-engineered from observed legacy residuals.

## Qualification result

UBQ02 establishes all of the following:

1. the finite-positive subthreshold branch is naturally reachable;
2. it is naturally material under nonzero load;
3. the legacy zero-like fallback is not the positive-flow equation;
4. the literal positive-flow formulas are numerically unsafe at naturally reached `P`;
5. a cancellation-safe analytic reformulation exists for comparison and probing;
6. production numerical policy remains unadmitted;
7. no new physical state is required;
8. no production source is changed.

Target closeout status:

`QUALIFIED_TCD042_FINITE_POSITIVE_SUBTHRESHOLD_CLASS_E_SEAM_NUMERICAL_POLICY_PENDING`
