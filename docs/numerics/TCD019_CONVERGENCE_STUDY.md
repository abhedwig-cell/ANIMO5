# ANIMO-NQ02 — TCD-019 convergence study

Status: `QUALIFIED_CAUSALITY_AND_ROUTE_LEVEL_CONVERGENCE_CANDIDATE_NO_TOLERANCE_OR_ADMISSION`.

This document records B1 diagnostic qualification only. It does not establish B2, does not choose a production tolerance, and does not admit corrected legacy or production migration.

## Evidence scope

Primary historical B0 testcase: `LWKM_gras_1040.2021.2045`.

Its active sorption configuration is fast Langmuir with one site and slow Freundlich with three sites. The TCD-019 fast-Langmuir path is active. The TCD-024 slow-Langmuir wrong-index path is not active in this historical case.

Frozen identities were rechecked before execution:

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Canonical B1 compiler path: GNU Fortran 14.2.0 with `-ffree-form -ffree-line-length-none -fallow-argument-mismatch -std=legacy -fdefault-real-8 -fdefault-double-8 -fno-automatic` and linker build-id disabled. Every scientific diagnostic source descendant and executable used in the primary matrix is SHA-256 registered in `TCD019_NUMERICAL_MATRIX.json`.

The observer instrumentation writes unrounded scientific records for accepted nonlinear state, path, residuals and P stores. An observer/non-observer control on the same B1 source logic found no ordinary scientific-output difference after normalizing only run timestamps and elapsed-time fields. Observer output is therefore treated as diagnostic observation, not as an altered physical model route.

## Residuals

Three residuals are kept separate:

- `R_eq`: independent evaluation of the accepted `C_unl` equation residual, with both components and their L1 sum recorded;
- `R_cons = Bapd - Batr`: the unfiltered layer P conservation identity reconstructed by `Transgen` from actual start/end aqueous, fast-sorbed, slow-sorbed and precipitated stores plus transfers;
- `R_constitutive = Rhbd * (Avadco*(Rsc-Con) - (fast_end-fast_start))`: the difference between fast-storage change represented in the solve and the actual fast-sorption state change.

No legacy warning limit is used as an acceptance criterion.

## Baseline reproduction

The instrumented baseline reproduces the existing PREP01 B1 result over 27,000 layer/timestep records:

| quantity | baseline |
| --- | ---: |
| cumulative `R_cons`, kg/ha P | `-2.7254515116348993e-1` |
| sum of absolute `R_cons`, kg/ha P | `2.7285079493861103e-1` |
| maximum local `|R_cons|`, kg/ha P | `5.011328758918021e-4` |
| negative / positive local residuals | `24379 / 2621` |
| maximum `R_eq` L1 | `1.045143528519657e-9` |
| maximum `|R_constitutive|`, source concentration units | `1.0022657517523265e-6` |
| mean accepted Newton iterations | `1.2423333333333333` |
| bisection fallbacks | `0` |

The systematic conservation drift therefore coexists with a small residual of the equation that the legacy solver actually solves. Legacy equation convergence does not imply exact P storage conservation because the equation contains an approximate constitutive storage representation.

## Small-delta switch refinement

Only the fast-sorption `abs(Ct-Ct0)` switch was changed. `Small` remained at the legacy value `1e-4`.

| switch | cumulative `R_cons`, kg/ha P | sum `|R_cons|`, kg/ha P | max `|R_constitutive|` |
| ---: | ---: | ---: | ---: |
| `1e-5` | `-3.157359197709864` | `3.157664841156121` | `5.066223554886949e-5` |
| `1e-6` legacy | `-2.725451511634899e-1` | `2.728507949386110e-1` | `1.0022657517523265e-6` |
| `1e-7` | `-1.962823676380751e-2` | `1.993388137502906e-2` | `8.75729495425123e-8` |
| `1e-8` | `-1.797424729186776e-2` | `1.823801424333675e-2` | see matrix |
| `1e-10` | `-1.797396283764501e-2` | `1.823774276106648e-2` | `1.0573307961296064e-9` |
| `1e-12` | `-1.797396283764501e-2` | `1.823774276106648e-2` | `1.8911533618753806e-17` |

The direction is not monotone over the whole range: making the switch looser to `1e-5` worsens drift by more than an order of magnitude. Below roughly `1e-8` the cumulative result reaches the legacy-`Small` floor. This confirms switch sensitivity but does not justify choosing a smaller arbitrary switch. A threshold-free exact formulation is tested separately.

## `Small` refinement with legacy constitutive policy

Only Newton `Small` was changed. The legacy small-delta tangent remained.

| `Small` | cumulative `R_cons`, kg/ha P | max `R_eq` L1 | mean iterations | bisections |
| ---: | ---: | ---: | ---: | ---: |
| `1e-3` | `-3.478294752327902e-1` | `1.720923802778525e-8` | `1.158` | `0` |
| `1e-4` legacy | `-2.725451511634899e-1` | `1.045143528519657e-9` | `1.24233` | `0` |
| `1e-5` | `-2.579234612601354e-1` | `1.068159443826233e-10` | `1.6449` | `0` |
| `1e-6` | `-2.550706253814267e-1` | `5.016556208492752e-12` | `1.92485` | `0` |
| `1e-8` | `-2.548942332279020e-1` | `3.696272612771589e-12` | `2.0740` | `0` |
| `1e-10` | `-2.548966453723643e-1` | `9.924877063174776e-12` | `2.25956` | `5` |

The equation residual refines strongly, then reaches a floor. The conservation drift remains about `-0.255 kg/ha P` because the constitutive tangent bias remains. At `1e-10`, tightening the Newton threshold starts to activate the separate fallback policy and no longer improves the global equation metric monotonically. A tighter `Small` alone is therefore not a defensible TCD-019 correction.

## Threshold-free exact storage representation

For a Langmuir site on the constitutive relation,

```text
S(C) = a*C/(1+b*C)
```

the cancellation-free secant is

```text
[S(C)-S(C0)]/(C-C0) = a / ((1+b*C)*(1+b*C0)).
```

The diagnostic exact-storage descendant retains any material off-relation start-state inconsistency rather than using TCD-019 to normalize it away. Significant off-relation initialization remains a separate TCD-014 concern.

With legacy `Small=1e-4`, the exact storage representation gives cumulative `R_cons = -1.7973962838665782e-2 kg/ha P` and reduces maximum `|R_constitutive|` to `1.2177894326628747e-16`. Its LWKM trajectory is nearly identical to the `delta_switch=1e-12` diagnostic: maximum `Rsc` difference `7.77e-15`, maximum fast-store difference `4.39e-12`. This confirms that the earlier threshold-lowering probe was approximating the exact-storage route, rather than identifying `1e-12` as a meaningful threshold.

## Exact storage plus nonlinear refinement

| `Small` | cumulative `R_cons`, kg/ha P | sum `|R_cons|`, kg/ha P | max local `|R_cons|`, kg/ha P | max `R_eq` L1 | mean iterations | bisections |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1e-4` | `-1.797396283866578e-2` | `1.823774273675467e-2` | `2.569152032477612e-4` | `1.045647190582601e-9` | `1.24230` | `0` |
| `1e-5` | `-3.243949600646231e-3` | `3.445873519008029e-3` | `1.936652296331442e-4` | `1.457085439751143e-10` | `1.64811` | `0` |
| `1e-6` | `-1.693466732349684e-4` | `2.683874998059811e-4` | `1.043319476092089e-5` | `7.853462972615223e-12` | `1.98096` | `0` |
| `1e-7` | `-4.566927694353575e-7` | `8.052162897499051e-5` | `5.184177847484498e-7` | `4.617731256360741e-12` | `2.16870` | `0` |
| `1e-8` | `-5.071063764773603e-7` | `7.958530117516555e-5` | `2.428799021558898e-7` | `2.638177326253712e-12` | `2.21193` | `0` |
| `1e-9` | `8.791209410558785e-6` | `9.058543114419888e-5` | `1.014888896290749e-5` | `5.515097073579880e-11` | `2.29611` | `2` |
| `1e-10` | `3.066615331962126e-6` | `8.315892595562731e-5` | `1.530710211463175e-6` | `7.878809408256549e-12` | `2.51415` | `4` |

There is a clear stable region before fallback activation in LWKM. `1e-7` and `1e-8` give almost the same cumulative conservation result and closely aligned trajectories. From exact `1e-6` to exact `1e-8`, the maximum `Rsc` change is `1.89e-11`, maximum fast-store change `9.86e-9`, maximum slow-store change `6.97e-9`, and maximum changes in the captured transport terms are of order `2e-13`.

This does not qualify `1e-7` or `1e-8` as a production threshold. It establishes a convergence envelope and exposes a second policy boundary: once the Newton threshold is tighter than the fallback's own acceptance/control semantics, the fallback begins to govern rare steps and monotone refinement breaks.

## Signed residual stopping test

Replacing the source's one-sided `Vec < ...` residual checks by magnitude checks, while keeping legacy `Small`, produced the same recorded LWKM aggregates as the baseline. The same was true for exact storage plus `Small=1e-8`.

The signed test remains a source-bound numerical risk, but it is not materially activated in this primary case under the tested paths. It should not be folded into a TCD-019 correction merely because the source form looks asymmetric.

## Precision sensitivity

The canonical B1 path uses promoted binary64 defaults because the reconstructed legacy source has implicit-interface dependencies. A default four-byte REAL build is already known to produce unstable interface behaviour and NaNs, so it is not a clean precision-only experiment and is excluded from numerical-policy inference.

An independent 100-decimal-digit evaluation used an actually observed very small concentration increment:

```text
C0 = 2.1813092841667838e-5
C1 = 2.1813092840919100e-5
Delta C = -7.487398559231223e-16
```

For source-bound Langmuir parameters `a = 0.8400301920000034`, `b = 1129.000000000013`:

- high-precision exact secant: `0.8001350946256463946801469...`;
- binary64 subtractive quotient: `0.800130323228758`, relative error about `-5.96e-6`;
- binary64 cancellation-free exact secant: `0.8001350946256465`, relative error about `9.44e-17`;
- binary64 tangent: `0.8001350946263066`, close numerically but not exactly conservative for the finite storage change.

A naive `always use the direct exact quotient` formulation would therefore trade the legacy constitutive bias for cancellation error at observed tiny increments. The cancellation-free exact expression avoids both failure modes for Langmuir.

## Synthetic time-step refinement

A source-bound one-layer fast-Langmuir-only probe applied the same integrated source over total time 1 using 1 to 128 equal substeps. It is synthetic B1, not historical evidence.

With the legacy stopping policy, the mass residual after 2, 4, 8, ..., 128 substeps approximately halves from `6.66e-10` to `1.04e-11`, showing time-splitting dependence from the loose nonlinear acceptance. Exact storage with the same legacy `Small` follows essentially the same pattern, so exact constitutive storage alone is not enough.

With exact storage plus `Small=1e-8`, final concentration is stable to roughly the last binary64 digits across all refinements and the mass residual stays at about `1e-16` to `1.6e-15`. This supports, but does not by itself admit, the combined route.

## Natural multi-case coverage

Five additional supplied natural cases with the same fast-Langmuir/slow-Freundlich option family were executed under the same frozen B0 hash controls: CranGrass, GrassPeat, STONE, Puitmijn and Zuiderzeeland.

All five reproduce a negative legacy cumulative P drift. The exact-storage plus refined-solver route strongly reduces post-initial-step drift across the set. CranGrass is especially diagnostic: a first-step residual of about `-0.72357 kg/ha` remains almost unchanged, but excluding that step the cumulative residual changes from `-0.04231 kg/ha` in the baseline to approximately `+1.3e-7 kg/ha` at exact storage plus `Small=1e-7`. NQ02 therefore keeps the first-step term separate rather than tuning TCD-019 against it.

The extension also shows that fallback is naturally active outside LWKM. Puitmijn uses 6 bisection fallbacks in the unchanged baseline and Zuiderzeeland uses 2. At the common diagnostic `Small=1e-7`, the counts increase to 12 and 15. At `1e-8`, they rise to 23 and 48. Whole-run absolute conservation does not improve monotonically with this tightening in every case even though the Newton equation residual becomes smaller.

This is evidence against any policy rule based only on `Small`. Newton and fallback acceptance must be qualified as one route.

Detailed values and descendant hashes are in `docs/numerics/TCD019_MULTICASE_NATURAL_COVERAGE.md` and `integration/animo-numerics/TCD019_MULTICASE_EXTENSION.json`.

## Qualification finding

The evidence supports two separate conclusions.

1. Legacy TCD-019 is `LEGACY_NUMERICAL_POLICY_NONCONVERGENT_OR_BIASED`, specifically because the small-delta constitutive representation is biased with respect to exact storage conservation, while nonlinear/fallback acceptance determines how much residual remains after that formulation bias is removed.
2. A route consisting of threshold-free, cancellation-safe exact storage representation plus a jointly qualified nonlinear/fallback convergence policy is a `CONVERGENT_POLICY_CANDIDATE`.

The second statement is route-level, not a tolerance choice. Natural multi-case support is now established for the supplied fast-Langmuir family, but the work still does not establish a production `Small`, a new fallback threshold, a global comparison tolerance, or integrated fast-Freundlich qualification. Independent B2 evidence where obtainable and independent numerical review remain open before B3 admission.

`TOLERANCE_NOT_YET_QUALIFIED`.
