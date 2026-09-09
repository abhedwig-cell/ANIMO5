# ANIMO-NQ02 — `Iflsol=4` Detcoef/Coefdc cancellation dependency

Status: `NEW_DISCREPANCY_CANDIDATE_PENDING_REGISTRY_AUTHORITY_ASSIGNMENT`.

This is a cross-cutting B1 numerical dependency discovered while qualifying TCD-019. It is **not** assigned a new canonical TCD number here and it is **not** folded into TCD-019.

RG02 explicitly records that the qualified central B3 discrepancy register ends at `TCD-027` and that later numbers on preparatory branches are local/collision-prone. Canonical allocation belongs to the B3 governance line. NQ02 therefore preserves this finding under a descriptive local identity only.

## Scope

The affected source is the analytical concentration-coefficient layer used by nonlinear transport/sorption:

- `Transsub.for:Detcoef`, `Iflsol=4`;
- `Transorp.for:Coefdc`, `Iflsol=4`.

This layer is upstream of the TCD-019 Newton residual and is not specific to phosphate sorption. A numerically different evaluation can therefore change TCD-019 trajectories without being a TCD-019 constitutive correction.

## Frozen identity and diagnostic descendant

- frozen source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- B0 hashes matched before the diagnostic run;
- diagnostic driver SHA-256: `778bbe8e54420a7fbbce01134fa51bfefb4381fdfbec737c90aaa23203060c0c`;
- scientific `Transsub` descendant SHA-256: `4bcc5afbb6013ea80491668e421996fc8c3f31b0494d75daf17ab0a845b53470`;
- scientific `Transorp` descendant SHA-256: `3db1c7c7bfb7e5aace7b848e32ee3b9ae2475a326583105ffec930f617ef49ef`;
- observer `Transorp` SHA-256: `b14c2a39f0a7316e5e647910af223c7e4fc0cc0290dad49a8d0bba1db523ff9a`;
- observer `Transgen` SHA-256: `28a223e5f9007bb52bcb5e97871f1c952b4d61146fea5ff5ea2d32b2e6557ab1`;
- executable SHA-256: `7cac3cb74a695baf527cb45d8f30f1e66b626c307301d29fa246ae4185d40844`.

The diagnostic uses exact fast-Langmuir storage and `Small=1e-7` as a fixed TCD-019 observation point. It changes only the numerical evaluation of the `Iflsol=4` analytical coefficients and derivatives.

## Source-bound cancellation

Define

```text
D = Mto + Rhbd*Avsocf
x = Hv*T/D.
```

Revision-53 `Detcoef` evaluates

```text
A2 = log((D+Hv*T)/D)/Hv
B2 = A2*(D+Hv*T)/(Hv*T) - 1/Hv.
```

For small `|x|`, `B2` is obtained by subtracting two terms of order `1/Hv` whose difference is finite. Algebraically,

```text
B2 = T/D * ((1+x)*log(1+x)-x)/x^2,
```

with finite limit

```text
B2 -> 0.5*T/D  as x -> 0.
```

`Coefdc` contains the analogous derivative cancellation:

```text
B2dc = 1/(Hv^2*T)
       * (log(1+x)-x)
       * Rhbd*Avadcodc.
```

The mathematical limit is finite, but direct binary64 subtraction is poorly conditioned when `x` is very small.

## Stable diagnostic evaluation

For the B1 sensitivity descendant, the small-`x` evaluation was replaced only when

```text
abs(x) < sqrt(epsilon(1.0d0)).
```

This switch is derived from machine precision as an evaluation-method crossover, not from a legacy residual and not as a scientific acceptance tolerance.

The series used were

```text
A2 = T/D * (1 - x/2 + x^2/3 - x^3/4 + x^4/5)

B2 = T/D * (1/2 - x/6 + x^2/12 - x^3/20 + x^4/30)
```

and for the adsorption-coefficient derivatives

```text
A2dc = -T/D^2
       * (1 - x + x^2 - x^3 + x^4)
       * Rhbd*Avadcodc

B2dc = -T/D^2
       * (1/2 - x/3 + x^2/4 - x^3/5 + x^4/6)
       * Rhbd*Avadcodc.
```

These are algebraic series for the existing analytical coefficient functions. Their use here is diagnostic only and does not admit an implementation policy.

## Observed natural state

The first naturally observed Zuiderzeeland fallback input includes:

```text
Tito   = 1
layer  = 6
Iflsol = 4
Con    = 3.5693099999999999e-5
Hv     = -4.9999999995886668e-7
Hv1    = 0
Hv2    = 5.2106985615000466e-7
Mto    = 0.5278366
Rhbd   = 1244
T      = 1
```

with the fast Langmuir start state on its constitutive relation. At this state:

```text
Avadco = 0.9217505299604854...
D      = 1147.1854958708439...
x      = -4.35849304021500015e-10.
```

Independent high-precision evaluation gives

```text
B2   = 0.00043584930412067741147...
B2dc = 0.47279499321842785163...
```

whereas the direct revision-53 expressions evaluated in binary64 give approximately

```text
B2   = 0.2685923078097403
B2dc = -290.4145135735744.
```

The sign and magnitude error in `B2dc`, and the roughly three-orders-of-magnitude error in `B2`, cannot be interpreted as a tolerance issue. They arise from cancellation in coefficient evaluation.

## Natural-case sensitivity

The stable-evaluation descendant was run on the existing NQ02 natural-case set with all other TCD-019 diagnostic settings fixed.

| case | cumulative `R_cons`, kg/ha | sum `|R_cons|`, kg/ha | bisections |
| --- | ---: | ---: | ---: |
| LWKM | `-2.656101995167309e-4` | `6.046022485115978e-4` | `0` |
| CranGrass | `-7.235682812602482e-1` | `7.91746913677539e-1` | `0` |
| GrassPeat | `-1.9335112473253208e-3` | `4.47036998414209e-3` | `2` |
| STONE | `+2.840419209292865e-3` | `3.6875836315779908e-3` | `1` |
| Puitmijn | `+1.2179585372876845e-3` | `5.178546894290078e-3` | `13` |
| Zuiderzeeland | `+5.572450840979992e-3` | `1.024818835468299e-2` | `16` |

The response is not a uniform TCD-019 improvement. For example, LWKM's previously qualified exact-storage plus `Small=1e-7` TCD-019 diagnostic had cumulative `R_cons` around `-4.57e-7 kg/ha`, while stable `Iflsol=4` coefficient evaluation moves that result to about `-2.66e-4 kg/ha`. Conversely, the first-step Zuiderzeeland residual changes from about `-1.47e-3` to `+1.25e-4 kg/ha`.

Ordinary scientific output trajectories also change in naturally activated cases. This demonstrates numerical materiality of the coefficient layer, but it does not establish that the stable-series descendant is the historically or scientifically preferred model route.

## Qualification consequence

This finding must remain separate from TCD-019 for three reasons.

1. The cancellation is in a generic analytical transport coefficient layer, not in the nonlinear P sorption constitutive equation.
2. Correcting coefficient arithmetic changes the equation surface against which TCD-019 convergence is measured.
3. The effect is not uniformly aligned with smaller P balance residuals, so it cannot be admitted opportunistically as part of a mass-balance repair.

Current classification:

`NEW_DISCREPANCY_CANDIDATE_PENDING_REGISTRY_AUTHORITY_ASSIGNMENT`

Local NQ02 key:

`NQ02-LCL-IFLSOL4-DETCOEF-CANCELLATION`

Before any TCD-019 B3 admission workunit, the numerical coefficient semantics used for comparison must be pinned. A later independent qualification workunit should determine whether the revision-53 expressions are intended historical arithmetic, whether an algebraically stable evaluation is admissible, and what other `Iflsol` branches have comparable conditioning risk.

`corrected_legacy_admitted=false`

`B3_admitted=false`

`production_migration_admitted=false`
