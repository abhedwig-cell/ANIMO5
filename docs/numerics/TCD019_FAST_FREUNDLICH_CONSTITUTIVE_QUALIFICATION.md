# ANIMO-NQ02 — TCD-019 fast Freundlich constitutive qualification

Status: `ISOLATED_CONSTITUTIVE_MECHANISM_QUALIFIED_INTEGRATED_SOLVER_QUALIFICATION_PENDING`.

This is B1 synthetic numerical evidence only. The supplied P-active historical cases inspected for NQ02 use fast Langmuir, not fast Freundlich. No result below is B2, no production implementation is admitted, and no numerical switch or tolerance is selected.

## Why this extension is needed

`Sorpfast` applies the same small-delta policy family to fast Freundlich sorption that produced the confirmed Langmuir TCD-019 conservation bias. For Freundlich,

```text
S(C) = K C^n,
K = Parcxfa(4)/Rhbd,
n = Parcxfa(5).
```

When `abs(Ct-Ct0) < 1e-6`, revision 53 replaces the finite storage secant by the tangent at `Ct`:

```text
Avadco = S'(Ct) = n K Ct^(n-1)
```

and uses

```text
Avadcodc = S''(Ct) = n(n-1) K Ct^(n-2).
```

This requires separate qualification because there is no supplied natural fast-Freundlich case on which the integrated route can be observed directly.

## Exact finite-storage residual

For an on-relation start state, the exact storage coefficient is

```text
Q(C,C0) = [S(C)-S(C0)]/(C-C0).
```

The derivative needed by the nonlinear Jacobian is

```text
dQ/dC = [S'(C)-Q]/(C-C0).
```

At the equal-state limit,

```text
Q(C0,C0) = S'(C0)
```

but

```text
dQ/dC | C=C0 = 0.5 S''(C0).
```

The legacy small-delta branch therefore has two distinct properties:

1. for finite `Ct-Ct0`, the tangent does not equal the finite conserved storage change;
2. even at the exact `Ct=Ct0` limit, the legacy Jacobian derivative is `S''`, whereas the derivative of the exact secant is `0.5 S''`.

The second point is not a rounding effect. It is a factor-of-two analytical mismatch in the limiting Jacobian of the finite-storage formulation.

## Diagnostic probe

An isolated `Sorpfast` source probe was compiled from the frozen revision-53 `Transorp.for`. The harness calls the actual routine with a constitutively consistent start store and no transport, slow sorption or other process coupling.

Synthetic parameter point:

```text
C0          = 2.1813092841667838e-5
Parcxfa(4)  = 11.870e-6
Parcxfa(5)  = 0.5357
Rhbd        = 1650
```

The Freundlich parameter pair is on the scale of parameters present in the supplied LWKM input, but activation as fast Freundlich is synthetic. It is used to test the source equation, not to represent a historical testcase.

The exact candidate descendant evaluates the finite secant directly away from equality and uses a relative-change binomial expansion near equality to avoid cancellation. The probe's series crossover is derived from binary64 machine epsilon, not from a legacy mass residual. It is a diagnostic implementation detail, not an admitted production switch.

All source, harness, executable and output hashes are registered in `integration/animo-numerics/TCD019_FAST_FREUNDLICH_PROBE.json`.

## Results

For `Delta C = +5e-7`, still inside the legacy `1e-6` small-delta branch:

| quantity | legacy tangent | stable exact secant |
| --- | ---: | ---: |
| relative error in `Avadco` | `-5.2323e-3` | `1.52e-15` |
| relative error in `Avadcodc` | `+9.7806e-1` | `3.00e-13` |
| `R_constitutive` | `-2.4153e-12` | `1.67e-25` |

At `Delta C = +1e-7`, the storage-coefficient error remains about `-1.06e-3`, and the legacy Jacobian derivative remains almost a factor two away from the exact secant derivative. The stable secant closes the finite storage change to numerical floor.

At `Delta C = 0`, the difference is especially clear. `Avadco` itself has the correct limiting tangent value in both routes, but the legacy `Avadcodc` is almost exactly twice the correct derivative of the finite secant. The stable exact route agrees with the analytical `0.5 S''` limit to binary64 precision.

The sign of the storage bias changes with the sign of `Delta C`, as expected from using a tangent at one end of a nonlinear secant. For `Delta C = -5e-7`, the legacy relative `Avadco` error is about `+5.41e-3`; the stable route remains at numerical floor.

## Cancellation check

Simply replacing the tangent by the direct quotient is not robust enough. At an observed concentration increment magnitude used elsewhere in NQ02,

```text
|Delta C| = 7.487398559231223e-16,
```

a binary64 subtractive evaluation of

```text
[S(C)-S(C0)]/(C-C0)
```

has relative error about `3.52e-6` for this Freundlich parameter point. The stable relative-change representation remains at roughly binary64 precision.

Thus the same distinction found for Langmuir applies here:

- tangent substitution is not exactly conservative for finite storage change;
- naïve direct subtraction can lose precision near equality;
- a cancellation-safe exact finite-storage representation avoids both failure modes.

## Qualification finding

The fast Freundlich small-delta policy is classified at isolated constitutive-routine level as:

`LEGACY_FAST_FREUNDLICH_SMALL_DELTA_CONSTITUTIVE_POLICY_BIASED_AND_JACOBIAN_INCONSISTENT`.

A stable exact finite-storage representation is supported as:

`CONVERGENT_CONSTITUTIVE_FORMULATION_CANDIDATE_INTEGRATED_SOLVER_QUALIFICATION_PENDING`.

This does not complete TCD-019 admission. Two limitations remain.

First, there is no natural fast-Freundlich activation in the supplied P-active historical cases inspected by NQ02. Historical prevalence and integrated natural trajectory effects are therefore unsupported by the testbank.

Second, the isolated constitutive result does not prove convergence of the full `C_unl` route with Freundlich under the Newton, late-iteration and fallback policies. That integrated solver qualification remains open.

Any materially off-relation start state belongs to the separate TCD-014 state-consistency boundary and must not be normalized away by an exact secant formula.

No production tolerance or switching value is qualified.

`TOLERANCE_NOT_YET_QUALIFIED`.
