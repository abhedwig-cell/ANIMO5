# TCD-019 convergence study

Status: `B1_CONVERGENCE_AND_CAUSALITY_QUALIFIED_POLICY_CANDIDATE_NOT_ADMITTED`.

All numerical values in this document are B1 diagnostic observations. None is a B2 reference and none defines a production tolerance. The frozen source and frozen LWKM testcase are unchanged. Each modified diagnostic `Transorp.for` descendant and executable is hash-registered in `integration/animo-numerics/TCD019_NUMERICAL_MATRIX.json`.

## Diagnostic build and observer contract

The canonical B1 build uses GNU Fortran 14.2.0 with the already qualified diagnostic build semantics:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

The uninstrumented deterministic executable SHA-256 is:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Observer instrumentation records unrounded local solver state, path, iteration count, exact-equation residual and local conservation terms. On the natural LWKM baseline, scientific outputs and balances were bitwise identical to the uninstrumented diagnostic run; PW/PAL files differed only in the legacy run-start timestamp header. After the known timestamp field is excluded from the representation comparison, observer non-interference is `PASS` for this study.

## Baseline

Natural case: `LWKM_gras_1040.2021.2045`.

Activation:

- fast sorption: Langmuir;
- slow sorption: Freundlich;
- TCD-024 slow-Langmuir wrong-index path: inactive.

Baseline over 27,000 layer/timestep solver calls:

| Metric | Baseline |
| --- | ---: |
| Newton accepted | 27,000 |
| bisection accepted | 0 |
| mean iterations | 1.2423333333 |
| maximum iterations | 3 |
| max absolute exact-equation residual | 1.0007604588e-6 |
| mean absolute exact-equation residual | 1.9857497039e-8 |
| cumulative P conservation residual | -0.2725451512 kg/ha |
| max local absolute P residual | 5.0113287589e-4 kg/ha |
| negative local residuals | 24,379 |
| positive local residuals | 2,621 |

The strong sign asymmetry is the important feature. This is not random-looking accumulation around zero.

## Experiment family A: fast-Langmuir small-delta switch

Only the `abs(C-C0)` threshold that selects tangent versus exact stored-state secant was changed. Legacy `Small=1e-4` was held fixed.

| tangent switch | cumulative P residual kg/ha | max exact-equation residual | mean iterations | solver path |
| ---: | ---: | ---: | ---: | --- |
| 1e-6 | -0.2725451512 | 1.00076046e-6 | 1.242333 | 27,000 Newton |
| 1e-7 | -0.01962823676 | 4.72667370e-7 | 1.242296 | 27,000 Newton |
| 1e-8 | -0.01797424729 | 4.72671148e-7 | 1.242296 | 27,000 Newton |
| 1e-9 | -0.01797396284 | 4.72671148e-7 | 1.242296 | 27,000 Newton |
| 1e-10 | -0.01797396284 | 4.72671148e-7 | 1.242296 | 27,000 Newton |
| 1e-12 | -0.01797396284 | 4.72671148e-7 | 1.242296 | 27,000 Newton |

Trajectory refinement also reaches a clear plateau in this case:

- 1e-7 to 1e-8: max `|delta Rsc| = 7.0525360e-10`, max `|delta Avc| = 7.0520484e-10`;
- 1e-8 to 1e-9: max `|delta Rsc| = 2.0550656e-13`, max `|delta Avc| = 1.3683711e-11`;
- 1e-9 to 1e-10: both captured trajectories identical;
- 1e-10 to 1e-12: both captured trajectories identical.

This proves a causal point, not a tolerance. Once the tangent branch is effectively removed from ordinary small changes, further threshold reduction has no effect on the captured LWKM trajectory. The remaining approximately `-0.017974 kg/ha` residual therefore comes from other numerical-policy terms, primarily nonlinear stopping and the initialization seam, not from unresolved threshold placement.

## Independent tangent error decomposition

At 80 decimal digits, using accepted unrounded states and effective layer-specific source parameters, the exact finite Langmuir storage change minus the storage represented by the legacy tangent branch sums to:

`+0.2546290594721548 kg/ha`

The observed baseline-to-refined change between 1e-6 and the 1e-9 plateau is approximately:

`+0.2545711883 kg/ha`

The agreement is sufficiently close to identify the tangent substitution as the dominant systematic cause. The independent high-precision calculation differs from its binary64 counterpart by only about `4.07e-14 kg/ha`, so the result is not a binary64 precision artifact.

## Experiment family B: Newton `Small` with legacy tangent retained

Only `C_unl` `Small` was refined while the legacy tangent threshold remained 1e-6.

| Small | cumulative P residual kg/ha | max exact-equation residual | mean iterations | path change |
| ---: | ---: | ---: | ---: | --- |
| 1e-4 | -0.2725451512 | 1.00076046e-6 | 1.2423 | none |
| 1e-5 | -0.2579234613 | 1.00076048e-6 | 1.6449 | none |
| 1e-6 | -0.2550706254 | 1.00076048e-6 | 1.9249 | none |
| 1e-7 | -0.2548945926 | 1.00076048e-6 | 2.0503 | none |
| 1e-8 | -0.2548942332 | 1.00076048e-6 | 2.0740 | none |
| 1e-10 | -0.2548966454 | 1.00076049e-6 | 2.2596 | 5 bisection fallbacks |

Tightening `Small` alone leaves almost all of the systematic drift. The exact-equation residual ceiling remains controlled by the tangent mismatch. At 1e-10 the solver path changes and the result is not monotonic. This is direct evidence against the rule "use the tightest available tolerance".

## Experiment family C: tangent effectively removed plus Newton refinement

The tangent switch was fixed at 1e-12 only as a diagnostic way to keep ordinary calls on the stored-state secant path. `Small` was then refined.

| Small | cumulative P residual kg/ha | max exact-equation residual | mean iterations | path |
| ---: | ---: | ---: | ---: | --- |
| 1e-5 | -0.003243949605 | 9.68458022e-8 | 1.6481 | all Newton |
| 1e-6 | -0.000169346655 | 3.33934990e-8 | 1.9810 | all Newton |
| 1e-7 | -4.56708061e-7 | 3.33934992e-8 | 2.1687 | all Newton |
| 1e-8 | +9.63374343e-6 | 3.33934990e-8 | 2.2119 | 1 bisection |
| 1e-10 | +6.40682910e-6 | 3.33934991e-8 | 2.5159 | 5 bisections |

State trajectories have already become very close by this point. For 1e-6 to 1e-7, maximum differences are approximately `1.88e-11` in `Rsc` and `1.84e-11` in `Avc`. Refinement below 1e-7 does not produce monotonic conservation improvement and starts to alter fallback behavior.

The relevant conclusion is a convergence envelope, not a chosen tolerance: once the constitutive tangent error is removed, accepted trajectories stabilize to roughly 1e-11 scale in this case while conservation becomes micro-kg/ha-scale after excluding the separate first-step initialization seam. The onset of bisection fallback at stricter `Small` values shows that the legacy solver has a practical path/precision floor.

`TOLERANCE_NOT_YET_QUALIFIED` remains mandatory.

## TCD-014 initialization partition

The first timestep is separated from the remainder of the run because the supplied initial fast store is not exactly on the fast Langmuir constitutive relation.

| route | first timestep kg/ha | remainder kg/ha |
| --- | ---: | ---: |
| legacy baseline | -5.2930848005e-4 | -0.2720158427 |
| tangent 1e-12 + Small 1e-7 | +8.0826700325e-7 | -1.2649750647e-6 |
| threshold-free constitutive secant + Small 1e-7 | -2.6434521232e-4 | -1.2649377437e-6 |

The threshold-free constitutive formulation makes the initialization inconsistency visible instead of incorporating the represented initial store into a singular near-zero secant. NQ02 therefore treats its full-run first-step residual as a TCD-014 boundary, not a failure of the TCD-019 constitutive identity after the state has become consistent.

## Alternative formulation 1: exact represented-store secant

A diagnostic formulation used

```text
[S(C)-A0]/(C-C0)
```

in algebraically decomposed form, including the explicit start-store offset `S(C0)-A0`.

This is mathematically exact for the represented initial store but numerically unsuitable when `A0-S(C0)` is tiny and `C-C0` is also tiny. Across diagnostic `Small` values 1e-4 through 1e-10:

- every one of 27,000 calls went to bisection;
- cumulative P residual remained about `-37.4963681231 kg/ha`;
- max local residual was about `0.2217114393 kg/ha`;
- max exact-equation residual was about `4.4342287866e-4`;
- mean bisection iterations were about 16.47.

This counterexample is useful because it shows that "exact secant" is not enough as a slogan. State consistency and numerical conditioning matter. This route is rejected as a TCD-019 policy candidate in its tested form.

## Alternative formulation 2: threshold-free constitutive Langmuir secant

For a constitutively consistent start state, NQ02 evaluated the stable identity

```text
Avadco = (M/rhbd)*b / [(1+b*C)(1+b*C0)]
```

with the corresponding analytic derivative. This removes the arbitrary small-delta threshold while preserving the Langmuir constitutive relation.

| Small | cumulative P residual kg/ha | max exact-equation residual | path |
| ---: | ---: | ---: | --- |
| 1e-4 | -0.01789074428 | 4.72489145e-7 | all Newton |
| 1e-5 | -0.003294471702 | 9.68450533e-8 | all Newton |
| 1e-6 | -0.000441642155 | 8.75722931e-8 | all Newton |
| 1e-7 | -0.000265610150 | 8.75722931e-8 | all Newton |
| 1e-8 | -0.000265250728 | 8.75722931e-8 | all Newton |
| 1e-10 | -0.000266844200 | 8.75722931e-8 | 3 bisections |

The residual floor is dominated by the first-step TCD-014 offset. At `Small=1e-7`, the remainder after the first timestep is `-1.2649377437e-6 kg/ha`. The 1e-7 to 1e-8 state refinement is tiny: max `|delta Rsc| = 1.6833923e-13`, max `|delta Avc| = 5.6528690e-12`.

This formulation is classified:

`CONVERGENT_POLICY_CANDIDATE_WITH_TCD014_INITIALIZATION_BOUNDARY`

That classification does not choose `Small=1e-7` as a future production setting. A future numerical-policy design should first replace the sign-asymmetric and multi-threshold legacy stopping contract by an equation-derived norm and then qualify the resulting criterion. The current study only shows where the legacy refinement envelope stabilizes.

## Precision sensitivity

The source is materially dependent on default `REAL` kind. The canonical r8 diagnostic build works and is the basis for the matrix.

A full default-real-4 diagnostic build was also attempted. It failed in the input/binary interface before the TCD-019 solver capture, so it is not a valid process-level precision comparison. Its executable SHA-256 is:

`a20680a80a5d4328bebbc38cad370582e10cc025bfce1b783e2a6d3da0207b65`

This confirms the already known source-bound kind sensitivity, but no r4 TCD-019 trajectory is claimed.

The independent 80-digit constitutive calculation agrees with the binary64 aggregate tangent mismatch to about `4e-14 kg/ha`. Within the valid r8 diagnostic contract, the dominant drift is therefore formulation and solver policy, not simple floating-point roundoff.

## Time-step refinement

Status:

`NOT_EXECUTED_NO_QUALIFIED_FORCING_SUBDIVISION_CONTRACT`

The frozen LWKM hydrology supplies external 10-day records. Splitting those records would require a new interpolation and forcing-transformation contract. That would change more than one numerical factor and would create synthetic forcing evidence that has not been qualified. NQ02 therefore does not manufacture a time-step refinement series.

This remains a limitation for a future B3 admission if the eventual numerical policy is shown to interact materially with timestep length.

## Initial-guess sensitivity

Status:

`NOT_EXECUTED_NO_SOURCE_BOUND_ALTERNATIVE_INITIAL_GUESS_POLICY`

Revision 53 hardcodes `Rsc=Con` and `Avc=Con`. No alternative initial-guess contract is established by current evidence. NQ02 captures path and convergence from that source-bound starting point rather than introducing an arbitrary guess strategy.

## Outcome

The study supports four separate conclusions:

1. The small-delta fast-Langmuir tangent substitution is the dominant cause of the systematic LWKM P drift.
2. Legacy `Small` contributes additional residual, but tightening it alone cannot repair the constitutive mismatch and eventually changes fallback behavior.
3. A threshold-free constitutive Langmuir secant has a stable convergence envelope in the natural TCD-019 case after the separate TCD-014 initialization seam.
4. No numerical tolerance has been scientifically qualified and no corrected-legacy route is admitted.

Qualification labels:

- legacy policy: `LEGACY_NUMERICAL_POLICY_NONCONVERGENT_OR_BIASED`;
- candidate: `CONVERGENT_POLICY_CANDIDATE_WITH_TCD014_INITIALIZATION_BOUNDARY`;
- tolerance: `TOLERANCE_NOT_YET_QUALIFIED`;
- B3 admission: `false`;
- corrected legacy admission: `false`;
- production migration: `false`.
