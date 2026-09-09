# ANIMO-NQ02 — TCD-019 fallback `Recfso` branch causality

Status: `HISTORY_DEPENDENT_FALLBACK_RATE_BRANCH_CAUSALLY_MATERIAL_POLICY_NOT_QUALIFIED`.

This document records B1 diagnostic evidence only. It does not admit a fallback formulation, adsorption/desorption branch rule, root-selection rule or numerical tolerance.

## Purpose

The Newton/fallback relation audit established that the revision-53 fallback inherits `Recfso` from the unsuccessful Newton history instead of deriving the rate branch from each fallback trial state. Natural Zuiderzeeland fallbacks were observed where inherited and accepted-state-local branches disagree.

The controlled question here is narrower:

> Does changing only the fallback `Recfso` branch from inherited history to the current fallback trial state materially change the accepted solution?

This is a one-factor causal probe. A smaller mass-balance residual is not treated as proof that the alternative branch policy is scientifically correct.

## Frozen evidence and diagnostic identity

- frozen source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- B0 hash check passed before the diagnostic run;
- diagnostic driver SHA-256: `00f36924dc07e23bbd609e74b9a23d56550e1d7047eb2006450aef9e07960a30`.

The scientific route was held fixed at:

- fast Langmuir storage represented by the cancellation-safe exact finite secant;
- Newton `Small = 1e-7`;
- otherwise unchanged fallback equation and bracket;
- bisection `|Df|` acceptance tested at `1e-6` and `1e-8` as existing diagnostic points.

The only scientific factor changed is that fallback recomputes slow-sorption equilibrium and selects adsorption/desorption `Recfso` from the current fallback trial state instead of retaining the failed-Newton selection.

Hashed scientific `Transorp` descendants before observer instrumentation:

| fallback `|Df|` | `Transorp` SHA-256 |
| ---: | --- |
| `1e-6` | `301795b83aa5978bc452f5dcffeff48c9ff8cf13e20d7b3c84171223b608fa84` |
| `1e-8` | `fb74d74154d34a16e67ca225b90cb131d14aab26d7e3c6b0f86c2f0a6edeabd3` |

All observer and executable identities are retained in `integration/animo-numerics/TCD019_FALLBACK_RECFSO_CAUSAL.json`.

## Puitmijn control

`Puitmijn_Cranendonck_60` had no inherited-versus-state-local `Recfso` mismatch in the earlier fallback observer study. It therefore serves as a causal control.

At both fallback thresholds, recomputing `Recfso` from the fallback trial state leaves the aggregate conservation result unchanged within the captured diagnostic arithmetic.

| fallback `|Df|` | cumulative `R_cons`, kg/ha | sum `|R_cons|`, kg/ha | bisection accepts |
| ---: | ---: | ---: | ---: |
| `1e-6` | `+1.8121039901993128e-3` | `5.0570109451064365e-3` | `12` |
| `1e-8` | `-1.8371581432759552e-4` | `3.205814865975566e-4` | `19` |

These are the same aggregates as the corresponding inherited-`Recfso` runs. That is consistent with the observer finding that no branch disagreement was active in this case.

## Zuiderzeeland

At the looser `Df=1e-6` diagnostic point, the state-local branch probe also reproduces the inherited-route aggregate:

- cumulative `R_cons = +3.2703492633138534e-3 kg/ha`;
- sum `|R_cons| = 1.2044790404298528e-2 kg/ha`;
- 15 bisection accepts.

At `Df=1e-8`, where the earlier observer found first-step inherited/state-local branch mismatches, changing only the branch ownership produces a materially different accepted trajectory.

| quantity | inherited `Recfso` | state-local `Recfso` |
| --- | ---: | ---: |
| cumulative `R_cons`, kg/ha | `-2.5252972774996354e-2` | `+1.8363583594392793e-4` |
| sum `|R_cons|`, kg/ha | `2.5910382512428002e-2` | `4.85938447464702e-4` |
| first-timestep `R_cons`, kg/ha | `-2.526056285746824e-2` | `+1.466068297977211e-4` |
| first-timestep sum `|R_cons|`, kg/ha | `2.5812879493605063e-2` | `4.1757728656454746e-4` |
| post-first cumulative `R_cons`, kg/ha | `+7.590082471883756e-6` | `+3.7029006146206835e-5` |
| post-first sum `|R_cons|`, kg/ha | `9.750301882293674e-5` | `6.836116090015455e-5` |
| bisection accepts | `13` | `12` |

The maximum accepted scalar `|Df|` in the state-local run remains within the `1e-8` diagnostic threshold, about `6.0e-9`. The large first-step change is therefore not explained by failing to solve the fallback scalar equation. It arises because the scalar equation itself changes when the kinetic branch is made a function of the trial state.

## Causal interpretation

The comparison supports four statements.

1. The inherited `Recfso` path is behaviorally inert where inherited and state-local branch choices coincide, as demonstrated by Puitmijn.
2. It is materially causal where the failed-Newton history disagrees with the fallback state, as demonstrated by Zuiderzeeland at the tighter diagnostic point.
3. The effect is nonlinear and coupled to root/branch selection. It cannot be represented as a small additive ledger correction.
4. The substantially smaller conservation residual in the state-local Zuiderzeeland diagnostic does **not** qualify that policy. It is causal evidence only. Scientific admission still requires one explicit governing residual, branch semantics, bracketing/root selection and initialization policy.

The current classification is therefore:

`HISTORY_DEPENDENT_FALLBACK_RATE_BRANCH_CAUSALLY_MATERIAL_POLICY_NOT_QUALIFIED`.

This strengthens the requirement that TCD-019 cannot be admitted by selecting a tighter `Small` or `Df` alone. Newton and fallback state, branch and residual semantics must be qualified together.

`TOLERANCE_NOT_YET_QUALIFIED`.

`corrected_legacy_admitted=false`

`B3_admitted=false`

`production_migration_admitted=false`
