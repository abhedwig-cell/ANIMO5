# TCD-019 and TCD-024 interaction

Status: `B1_SYNTHETIC_INTERACTION_CHARACTERIZED_NO_COMPOSITION_ADMISSION`.

TCD-019 and TCD-024 remain separate discrepancies.

- TCD-019 is a Class E nonlinear numerical-policy claim around fast nonlinear sorption and nonlinear convergence.
- TCD-024 is a Class B wrong-index defect in the slow-Langmuir update path.

The natural LWKM TCD-019 case does not activate TCD-024 because its slow sorption option is Freundlich. This interaction study therefore uses an explicitly transformed B1 synthetic input. It is not historical evidence and cannot establish prevalence or B2 behavior.

## Source separation

### TCD-019

`Sorpfast` in frozen revision-53 `Transorp.for` uses a tangent in the fast-Langmuir branch when `abs(Ct-Ct0) < 1e-6`. This substitutes a local derivative for a finite nonlinear storage change. `C_unl` additionally applies the legacy nonlinear stopping and fallback policy.

### TCD-024

In `Conc_unl`, the time-subdivision trial loop uses `I` as the trial counter and `J` as the slow-sorption site index. In the slow-Langmuir branch the source calculates:

```text
Yy = 1 + Parcxsl(3,I) * Avc
```

inside the loop over `J`.

The site parameter is therefore indexed by the trial counter instead of the slow-sorption site. The TCD-024-only diagnostic changes this one index from `I` to `J` and makes no TCD-019 policy change.

## Synthetic interaction input

Starting point: frozen `LWKM_gras_1040.2021.2045`.

The transformed input changes only the slow-sorption relation from the original three Freundlich sites to three unequal Langmuir sites. The transformation is designed for local comparability rather than historical realism.

Reference concentration is the median unrounded natural-case `Con` captured from the TCD-019 baseline:

`Cref = 0.0001432479464174597`

For each original Freundlich site

```text
S_F(C) = K * C^n
```

a synthetic Langmuir relation

```text
S_L(C) = M*b*C/(1+b*C)
```

was chosen to match both `S_F(Cref)` and its first derivative at `Cref`:

```text
b = (1/n - 1) / Cref
M = S_F(Cref) * (1+b*Cref) / (b*Cref)
```

Resulting sites:

| site | M | b | original K | original n |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 2.2308408768e-7 | 6050.46332215 | 1.187e-5 | 0.5357 |
| 2 | 9.9727768490e-7 | 28011.09145835 | 4.667e-6 | 0.1995 |
| 3 | 1.3101242103e-6 | 19827.47988200 | 9.711e-6 | 0.2604 |

Synthetic input manifest SHA-256:

`bbacab1a4761ff286778533dc46ac09ce41bcc54390a45698d6c9a937eb1d45e`

Synthetic `CHEMPAR.INP` SHA-256:

`884bad9603b5c511dd438ca3a7f468a7d1d5582ab240bffbd8e73754bf17dc60`

Transformation metadata SHA-256:

`a1d478a0a0f74c2de0d989979a71ca396aba136f3a6f28fb4077f2130fa28d54`

Evidence role:

`B1_SYNTHETIC_INTERACTION_ONLY`

## Four-way diagnostic composition matrix

The TCD-019 numerical-policy diagnostic in this matrix uses the threshold-free fast-Langmuir constitutive secant and `Small=1e-7`. That value is a diagnostic point inside the observed natural-case convergence envelope. It is not a qualified tolerance.

| variant | TCD-024 index | TCD-019 fast policy | cumulative P residual kg/ha | max local kg/ha | solver paths |
| --- | --- | --- | ---: | ---: | --- |
| legacy | legacy wrong index | legacy tangent + legacy Small | -25607.38038 | 116.25623 | 26,644 Newton, 65 retry-return observations |
| TCD-024 only | corrected `I` to `J` | legacy tangent + legacy Small | -2.493197716 | 0.00136324 | 27,000 Newton |
| TCD-019 policy only | legacy wrong index | threshold-free fast secant, diagnostic Small=1e-7 | -27138.53641 | 140.59194 | 26,531 Newton, 23 bisection, 2 retry-return observations |
| combined | corrected `I` to `J` | threshold-free fast secant, diagnostic Small=1e-7 | +19.05595682 | 1.46215732 | 26,978 Newton, 22 bisection |

Derived `Transorp.for` SHA-256 values:

- legacy observer descendant: `6ffe89a48e32fd527b915fefa90ab5b6e291194d8802b4853bf6823e2383335e`;
- TCD-024-only: `9b21544b5b8c91939c594885c1403c0fd79c49d690a79917e134cdeed4970ee3`;
- TCD-019-policy-only: `3cdcd2c20cfeb25968e009fadebbbf15abe253e3b237541994077daa8ecab11d`;
- combined: `4553191fc34b0422c9107decc8cd72cfd40cfc0a89fded74c90d89fea0fb58b6`.

Derived executable SHA-256 values:

- legacy: `2b646b1c6b49f236ed498fd48aee66d110467dd3bacceae51bc6523df26d090d`;
- TCD-024-only: `a3a5dd9deed62ce2dfabee127b7a26be0d12193155ce47a3cf1c708aeaaa8fa5`;
- TCD-019-policy-only: `cbb74b3b32244e6c1c3d0a47bd105cd10f2483e9eb164ff2e852ecf6e6509eee`;
- combined: `06337ebe65d86c2a4788c6c64e421e1326f64920a40cce0937d0bbbdfccd1cdd`.

## What the matrix proves

The TCD-024 index defect dominates the synthetic slow-Langmuir case. Correcting only that index reduces a catastrophic multi-order-of-magnitude conservation failure to a much smaller, but still nontrivial, residual.

The TCD-019 fast-policy change does not repair TCD-024 and must not be presented as doing so.

More importantly, the combined diagnostic is not additive. After correcting the TCD-024 index, adding the natural-case TCD-019 candidate produces a much larger residual and triggers bisection. This is not evidence that the fast-Langmuir constitutive secant is invalid in the natural TCD-019 scope. It is evidence that the slow-Langmuir path contains additional numerical seams that confound a two-defect composition test.

## Additional slow-Langmuir seams exposed

NQ02 identified two source-bound interaction risks. They are recorded here as risks, not admitted corrections and not silently folded into TCD-024.

### 1. `Sorpslow` Langmuir derivative is not the derivative of its own stored equation

The source computes, for `OPTCXSL=2`:

```text
Dum = b*Avc
Dum = (M/rhbd) * Dum/(1+Dum)
Eqcxsl = Dum
Eqcxsldc = (M/rhbd)*b / (1+Dum)^2
```

After the second assignment, `Dum` contains the sorbed amount, not `b*Avc`. The derivative of the stated Langmuir relation is instead proportional to

```text
(M/rhbd)*b / (1+b*Avc)^2
```

The Jacobian therefore appears algebraically inconsistent with the state equation on this branch. NQ02 does not assign a new TCD identifier or correct it here because that would exceed the workunit boundary.

### 2. Newton and bisection use different slow-Langmuir kinetic factors

In the Newton path, slow Langmuir uses:

```text
Y = exp[-k*(1+b*Avc)*St]
```

The `C_unl` bisection fallback uses slow storage terms with:

```text
Y = exp(-k*St)
```

without the `1+b*Avc` multiplier. A solver fallback can therefore change the represented slow-Langmuir kinetic equation rather than merely solve the same equation by another method.

This explains why a composition experiment that begins to activate bisection is not a clean test of only TCD-019 plus TCD-024.

## Composition decision

The interaction outcome is:

`INTERACTION_NONADDITIVE_ADDITIONAL_SLOW_LANGMUIR_NUMERICAL_SEAMS_DETECTED_NO_COMPOSITION_ADMISSION`

Consequences:

- TCD-019 remains separate from TCD-024;
- the natural LWKM TCD-019 convergence result remains valid only in its fast-Langmuir plus slow-Freundlich scope;
- TCD-024-only correction is not admitted by this workunit;
- no combined correction is admitted;
- the additional slow-Langmuir Jacobian and fallback-equation seams require separate atomization/qualification before any slow-Langmuir composition admission;
- the synthetic case remains B1 and cannot be treated as historical B2 evidence.

`corrected_legacy_admitted=false`

`B3_admitted=false`

`production_migration_admitted=false`
