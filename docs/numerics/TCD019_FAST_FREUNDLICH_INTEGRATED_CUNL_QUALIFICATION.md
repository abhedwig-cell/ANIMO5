# ANIMO-NQ02 — integrated fast-Freundlich `C_unl` qualification

Status: `INTEGRATED_SYNTHETIC_C_UNL_CONVERGENCE_SUPPORTED_NATURAL_COVERAGE_UNAVAILABLE`.

This is B1 synthetic evidence. It closes the specific gap between the isolated fast-Freundlich `Sorpfast` constitutive probe and the coupled `C_unl` Newton solve. It does not create historical B2 evidence and it does not qualify a production tolerance or implementation.

## Evidence boundary

The supplied P-active natural cases inspected by NQ02 use fast Langmuir, not fast Freundlich. Natural fast-Freundlich coverage is therefore unavailable in the frozen testbank.

The synthetic integrated probe uses the revision-53 `C_unl`, `Coefdc` and `Detcoef` route directly with:

- one fast Freundlich site;
- no slow sorption, so TCD-024 and fallback `Recfso` policy are absent;
- no precipitation;
- constant water content, `Iflsol=5`, avoiding the separately registered `Iflsol=4` coefficient-cancellation dependency;
- a constitutively consistent start store;
- positive concentrations throughout.

This makes the probe deliberately narrow: it tests whether the fast-Freundlich constitutive representation integrates coherently into the nonlinear solver without confounding the already identified fallback, initialization, TCD-024 or `Iflsol=4` seams.

Frozen identities:

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Compiler path: GNU Fortran 14.2.0 with the NQ01 promoted-binary64/static-local diagnostic flags. All source descendants and executables are recorded in `integration/animo-numerics/TCD019_FAST_FREUNDLICH_INTEGRATED_CUNL.json`.

## Synthetic state

The constitutive parameters are the same source-scale Freundlich pair used in the isolated probe:

```text
C0       = 2.1813092841667838e-5
Parcxfa4 = 11.870e-6
Parcxfa5 = 0.5357
Rhbd     = 1650
Mto      = 0.300
St       = 1
Iflsol   = 5
```

The initial fast store is placed exactly on

```text
S(C0) = Parcxfa4*C0^Parcxfa5/Rhbd.
```

Source strengths are chosen to generate concentration changes spanning approximately `+5e-7` through `+1e-12` and corresponding negative changes. These are activation probes, not tolerance candidates.

## Mathematical reference residual

With constant water content, no slow sorption and no external loss, exact finite storage conservation is

```text
R_cons = Mto*(C1-C0)
       + Parcxfa4*(C1^n-C0^n)
       - Hv2*St.
```

An independent 80-digit root solve of this equation supplies a solver-independent mathematical reference for the synthetic probe.

The `C_unl` equation residual is also re-evaluated at the accepted state using `Sorpfast` plus `Detcoef`. This keeps represented-equation convergence separate from exact finite-storage conservation.

## Legacy integrated behavior

For a target change of approximately `+5e-7`, the legacy fast-Freundlich small-delta tangent gives, already at `Small=1e-4`:

```text
accepted Rsc  = 2.2313108984470250e-5
R_cons        = +2.4154771048324987e-12
|R_eq|_1      = 3.39e-21
Newton steps  = 2
```

Tightening `Small` through `1e-10` changes the iteration count from 2 to 3 at the tightest settings but leaves the accepted concentration and conservation residual unchanged. The represented equation is solved essentially to floating-point zero while the finite-storage balance remains biased.

The accepted concentration differs from the high-precision conservation root by about `8.03e-12` for this activation point.

For a target change near `1e-7`, the same pattern remains:

```text
R_cons ≈ 9.83e-14
R_eq   ≈ 0
```

and `Small` refinement does not remove it. This is integrated confirmation that the legacy fast-Freundlich issue is formulation bias, not insufficient Newton convergence.

## Stable exact-secant integrated behavior

The candidate diagnostic uses the previously qualified stable exact finite secant and its consistent derivative for the fast-Freundlich small-delta branch. Its numerical-method crossover remains derived from binary64 machine precision and is not a scientific acceptance tolerance.

Across `Small = 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-10` and all nine positive/negative source probes:

- every run accepts through Newton;
- no fallback is used;
- accepted states require only 1 to 3 Newton iterations;
- accepted `Rsc` agrees with the independent high-precision conservation root to the captured binary64 value;
- `R_cons` is at approximately `1e-22` to `1e-21` in the harness units;
- `R_eq` is at or near binary64 zero.

For the `+5e-7` activation point:

```text
accepted Rsc  = 2.2313100957453506e-5
R_cons        = 5.29e-23
|R_eq|_1      = 3.39e-21 at Small=1e-4, zero after an additional Newton step at the tightest settings
```

This is not merely a smaller mass balance. The accepted state coincides with the independently solved finite-storage conservation root while also solving the represented `C_unl` equations.

An observer/non-observer control at candidate `Small=1e-7` produced byte-identical scientific harness output, supporting non-interference of the path instrumentation.

## Time-step refinement

A second synthetic integrated probe applies the same total source over total time 1 using 1, 2, 4, ..., 128 equal substeps, with legacy `Small=1e-4` fixed.

For the legacy fast-Freundlich tangent route, the total conservation residual approximately halves with each doubling of substeps:

| substeps | `R_cons` |
| ---: | ---: |
| 1 | `2.4154771048324987e-12` |
| 2 | `1.2110777159070968e-12` |
| 4 | `6.063736884647552e-13` |
| 8 | `3.033955499742075e-13` |
| 16 | `1.517499515813799e-13` |
| 32 | `7.588802095834551e-14` |
| 64 | `3.794727154278479e-14` |
| 128 | `1.897445093472501e-14` |

The final concentration approaches the exact-storage result under time-step refinement. This is expected for a finite-step tangent approximation and is evidence of discretization/formulation dependence, not a reason to select a timestep as a correction.

For the stable exact-secant route, the final concentration is invariant to approximately binary64 rounding across all refinements and `R_cons` remains around `1e-22` to a few `1e-21`. All 255 substep solves in each route use Newton with two iterations and no fallback in this test.

## Qualification result

The combined isolated and integrated evidence now supports:

`FAST_FREUNDLICH_EXACT_CONSERVATIVE_CONSTITUTIVE_FORMULATION_INTEGRATED_C_UNL_SYNTHETIC_CONVERGENCE_SUPPORTED`

This strengthens the TCD-019 route-level candidate across both nonlinear fast-sorption families present in source:

- fast Langmuir: natural multi-case support plus precision and nonlinear convergence studies;
- fast Freundlich: isolated constitutive support plus integrated synthetic `C_unl` and time-step convergence support.

The remaining limitation is evidence provenance, not an observed failure of the integrated fast-Freundlich candidate: no supplied natural P-active testcase activates fast Freundlich, so natural or B2 validation is unavailable from the frozen testbank.

No specific `Small`, evaluation crossover, fallback threshold or global numerical tolerance is admitted.

`TOLERANCE_NOT_YET_QUALIFIED`.

`corrected_legacy_admitted=false`

`B3_admitted=false`

`production_migration_admitted=false`
