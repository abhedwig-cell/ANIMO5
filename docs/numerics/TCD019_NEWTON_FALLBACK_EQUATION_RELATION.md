# ANIMO-NQ02 — Newton versus fallback equation relation for TCD-019

Status: `DISTINCT_FALLBACK_CLOSURE_AND_NATURAL_PATH_DEPENDENCE_CONFIRMED_POLICY_NOT_QUALIFIED`.

This document is B1 diagnostic numerical evidence. It does not admit a fallback algorithm, root-selection rule or numerical tolerance.

## Question

The fallback sensitivity study showed that a smaller scalar `Df` does not necessarily give a scientifically preferable accepted P state. The remaining source question was whether fallback is merely a robust scalar solver for the same nonlinear equations used by Newton, or whether it changes the discrete equation being solved.

The source reconstruction shows the latter.

## Newton system

For fixed nonlinear coefficients in one Newton evaluation, `Detcoef` gives the analytical solution of the concentration equation. `C_unl` solves for both

- `Rsc`, the end-of-step concentration;
- `Avc`, the time-average concentration.

The two residual equations are

```text
F1 = Con*A1 + A2*q - Rsc
F2 = Con*B1 + B2*q - Avc
```

with

```text
q = Hv2 + sum(Fact_i*(Amp_i-Eq_i(Avc))).
```

For linear or Freundlich slow sorption, `Fact_i = Rhbd*(1-exp(-Recfso_i*St))/St`. Fast storage enters through `Avadco` in `Detcoef`.

When fast storage is represented by the exact finite secant, the analytical ODE implies the integrated conservation identity

```text
(Mto + Hv*St)*Rsc - Mto*Con
+ Rhbd*(Sfast(Rsc)-Sfast_start)
+ (Hv1-Hv)*St*Avc
- Hv2*St
- sum[Rhbd*(1-exp(-Recfso_i*St))*(Amp_i-Eq_i(Avc))]
= 0.
```

The two-variable Newton solution therefore supplies both conservation and the analytical time-average closure represented by `B1,B2`.

## What fallback changes

The fallback source imposes

```text
Rsc = 2*Avc - Con.
```

This is the trapezoidal midpoint relation

```text
Avc = 0.5*(Con+Rsc),
```

not the general analytical-average relation from `Detcoef`.

Substituting this midpoint constraint into the integrated conservation identity gives the scalar equation coded as `Df = Lhs-Rhs`:

```text
Lhs = (2*Mto + Hv1*St + Hv*St)*Avc
     + fast_end(Rsc)
     + slow_equilibrium_terms(Avc)

Rhs = (2*Mto + Hv*St)*Con
     + Hv2*St
     + fast_start
     + slow_start_terms.
```

The algebra matches the revision-53 fallback source term by term for the natural NQ02 slow-Freundlich cases.

Therefore fallback is not bisection applied to a scalarized form of the original two-equation Newton system. It replaces the analytical average-concentration closure by a different time closure and then solves conservation on that restricted line.

For slow Langmuir there is an additional difference. Newton uses the concentration-dependent kinetic exponential

```text
exp[-Recfso*(1+Parcxsl(3)*Avc)*St],
```

whereas the fallback slow-Langmuir term uses

```text
exp[-Recfso*St].
```

Thus `Optcxsl=2` changes more than the average-concentration closure. This interaction remains separate from TCD-024's wrong index.

## Observer test on accepted fallback states

A hash-controlled observer was added to descendants that otherwise retain the exact-fast-storage, `Small=1e-7` diagnostic policy. It does not change the accepted state. At every fallback acceptance it records:

- scalar fallback `Df`;
- the two Newton residual components evaluated at the accepted fallback `Rsc,Avc`;
- the same residual after recomputing the adsorption/desorption branch from the accepted `Avc`;
- inherited and state-local `Recfso` values per slow-sorption site.

The machine-readable identities and results are in `integration/animo-numerics/TCD019_NEWTON_FALLBACK_RELATION.json`.

### Puitmijn

No inherited-versus-state-local `Recfso` mismatch occurs in the observed fallback events. Nevertheless, fallback states do not generally solve the two-variable Newton equations. The maximum Newton-residual L1 at fallback states is about `2.87e-5` with the legacy `Df=1e-6` acceptance and about `1.01e-5` with the `Df=1e-8` diagnostic acceptance.

This is direct numerical confirmation of the closure difference. Tightening `Df` reduces the scalar fallback residual but does not turn the fallback state into the solution of the analytical two-variable system.

### Zuiderzeeland

Here the second source property is naturally active: fallback inherits `Recfso` values that can disagree with the adsorption/desorption branch implied by the state it eventually accepts.

With the legacy `Df=1e-6` acceptance, 3 of 15 fallback events contain at least one branch mismatch. At the first timestep in layer 6, two slow sites differ:

| site | inherited `Recfso` | state-local `Recfso` |
| ---: | ---: | ---: |
| 1 | `3.0e-4` | `1.1755` |
| 2 | `6.0e-5` | `3.34e-2` |

The accepted scalar residual is `Df=-3.03e-7`, but the two-variable Newton residual L1 is about `1.45e-7` using the inherited rate branch and `4.50e-7` using the branch implied by the accepted state.

With `Df=1e-8`, 3 of 13 fallback events again contain branch mismatches. At first-step layer 6, `Df` is reduced to about `-8.26e-10`, yet the Newton residual remains about `1.75e-7` with inherited rates and `5.48e-7` with state-local rates. At first-step layer 5, site 1 has the opposite branch mismatch, inherited `1.1755` versus state-local `3.0e-4`, and the Newton residual is of order `1e-7` even though `Df` is `6.14e-9`.

A smaller `Df` therefore does not imply convergence to the Newton equations or even remove path dependence in the slow-sorption kinetic branch.

## Interpretation

Three numerical-policy facts are now source-bound and behaviorally supported.

First, Newton and fallback do not share one discrete root definition. Newton uses the analytical average-concentration relation; fallback imposes the trapezoidal midpoint relation.

Second, the fallback scalar function can depend on the failed Newton history because `Recfso` is inherited. Zuiderzeeland demonstrates that this is not only a theoretical code-path concern. The inherited branch can be inconsistent with the fallback state that is accepted.

Third, tightening the scalar residual cannot by itself qualify fallback. It can reduce `Df` while leaving a materially different two-variable equation residual and a stale kinetic branch.

This explains the non-monotone behavior seen when `Small` becomes tight enough to hand control to fallback. The issue is not merely that the fallback tolerance is looser. The fallback owns a different closure and can own path-dependent kinetic choices.

## Qualification consequence

A future policy cannot be justified as “Newton with bisection backup” unless one of two things is established:

1. both paths are reformulated to solve the same explicit governing residual and use a safeguarded root-selection method; or
2. the fallback's different discrete model is scientifically justified as an intentional alternate formulation, including its time-average, kinetic-branch and bracketing semantics.

NQ02 supplies no evidence for the second interpretation.

The current fallback classification is strengthened to:

`DISTINCT_FALLBACK_DISCRETE_CLOSURE_WITH_NATURALLY_ACTIVATED_HISTORY_DEPENDENT_RATE_BRANCH_POLICY_NOT_QUALIFIED`.

The TCD-019 route-level candidate remains an exact conservative constitutive representation plus a jointly qualified nonlinear and fallback policy. A specific implementation or tolerance is still not qualified.

`TOLERANCE_NOT_YET_QUALIFIED`.
