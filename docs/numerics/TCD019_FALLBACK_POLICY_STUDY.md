# ANIMO-NQ02 — TCD-019 fallback-policy sensitivity

Status: `FALLBACK_POLICY_CAUSALLY_MATERIAL_JOINT_QUALIFICATION_REQUIRED`.

This study is B1 diagnostic evidence only. It does not select a bisection tolerance, does not establish B2 and does not admit a numerical policy.

## Question

The primary LWKM study showed a stable Newton region before the legacy bisection route begins to control rare steps. The natural multi-case extension then showed that fallback is not merely an extreme-refinement edge case: it is already active in some supplied cases and becomes more frequent under nonlinear refinement.

The remaining question is whether the fallback residual threshold can be treated as an ordinary accuracy knob. The answer from the controlled runs below is no.

## Source-bound fallback semantics

After unsuccessful Newton iteration, `C_unl` switches to a scalar bisection-like equation. The route:

- uses `abs(Df) < 1e-6` as the legacy scalar acceptance condition;
- constrains `Rsc` and `Avc` by `Rsc = 2*Avc - Con`;
- constructs its own `Cmin/Cmax` bracket;
- inherits `Recfso`, the slow-sorption adsorption/desorption rate selection, from the preceding Newton route rather than recomputing it for every bisection trial;
- returns a physically accepted state through a control path that is therefore not simply a tighter continuation of the two-variable Newton solve.

NQ02 does not classify each of these properties as a separate defect. Their materiality must be established before any production fallback policy can be selected.

## Controlled natural-case experiment

Two supplied cases with natural fallback activation were used:

- `Puitmijn_Cranendonck_60`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

The constitutive route and Newton policy were held fixed at the same B1 diagnostic point used in the natural multi-case study: cancellation-safe fast-Langmuir secant plus `Small=1e-7`. Only the bisection scalar residual threshold was changed from the legacy `1e-6` to `1e-7` and `1e-8`.

These powers-of-ten refinements are diagnostic probes around the source value. They are not candidate tolerances.

## Puitmijn

| bisection `|Df|` acceptance | cumulative `R_cons`, kg/ha | sum `|R_cons|`, kg/ha | bisection accepts | max accepted `|Df|` |
| ---: | ---: | ---: | ---: | ---: |
| `1e-6` legacy | `+1.8121039902e-3` | `5.0570109451e-3` | `12` | `9.6276772e-7` |
| `1e-7` | `-8.7294872749e-5` | `9.6639949177e-4` | `19` | `8.8008364e-8` |
| `1e-8` | `-1.8371581433e-4` | `3.2058148660e-4` | `19` | `9.6149935e-9` |

The first timestep is nearly invariant across these runs, about `-1.98e-4 kg/ha`. Excluding that first timestep, the absolute residual drops from about `4.82e-3` to `7.30e-4` and then `8.37e-5 kg/ha` as the bisection residual is refined.

That is useful convergence evidence for this trajectory segment. It is not enough to choose a threshold because Zuiderzeeland behaves differently at initialization.

## Zuiderzeeland

| bisection `|Df|` acceptance | cumulative `R_cons`, kg/ha | sum `|R_cons|`, kg/ha | bisection accepts | max accepted `|Df|` |
| ---: | ---: | ---: | ---: | ---: |
| `1e-6` legacy | `+3.2703492633e-3` | `1.2044790404e-2` | `15` | `6.6801247e-7` |
| `1e-7` | `-2.6444651639e-2` | `2.7214091680e-2` | `16` | `6.7390821e-8` |
| `1e-8` | `-2.5252972775e-2` | `2.5910382512e-2` | `13` | `9.6318303e-9` |

At first sight this looks like tightening the fallback makes conservation worse. The timestep decomposition shows what actually happens.

For the legacy `1e-6` fallback threshold:

- first-timestep residual sum: `-1.4689e-3 kg/ha`;
- later absolute residual sum: `1.0024e-2 kg/ha`.

For `1e-7`:

- first-timestep residual sum: `-2.5258e-2 kg/ha`;
- later absolute residual sum: `1.4042e-3 kg/ha`.

For `1e-8`:

- first-timestep residual sum: `-2.5261e-2 kg/ha`;
- later absolute residual sum: `9.7503e-5 kg/ha`.

Thus the post-initial trajectory shows the same refinement direction as Puitmijn, but tighter bisection acceptance selects a materially different first-step solution in layers 5 and 6. The largest first-step layer residual is about `-2.386e-2 kg/ha` at `1e-8`, whereas the legacy fallback gives only about `-5.49e-4 kg/ha` in the corresponding layer.

The accepted scalar `Df` itself becomes an order of magnitude smaller at each refinement. A smaller scalar fallback residual therefore does not guarantee a scientifically preferable accepted state.

## Interpretation

This study rejects three shortcuts.

First, the bisection threshold cannot be chosen by minimizing cumulative P balance error in one case. Puitmijn and Zuiderzeeland would push that choice in different directions if the first-step seam were not separated.

Second, the fallback route is not merely an alternative way to obtain the same root to higher accuracy. Tightening its scalar residual changes branch/root selection in a natural first-step state. The fallback equation, bracketing, inherited slow-sorption rate choice and initialization state must therefore be reviewed as one control-path contract.

Third, the first-step Zuiderzeeland response must not be silently assigned to TCD-019. It is an interaction with initialization/state consistency. The exact attribution belongs to the separate initialization qualification, including TCD-014 where applicable.

## Qualification consequence

For TCD-019 the route-level candidate remains:

`EXACT_CONSERVATIVE_CONSTITUTIVE_STORAGE_REPRESENTATION_PLUS_QUALIFIED_NONLINEAR_AND_FALLBACK_POLICY`.

The fallback part is now more precisely classified as:

`FALLBACK_POLICY_CAUSALLY_MATERIAL_BUT_NOT_YET_QUALIFIED`.

A future production-policy study must define one governing residual/acceptance contract across Newton and fallback, or justify why the two paths solve different equations. It must also establish root/bracket uniqueness or safeguarded branch selection and explicitly handle initialization-state inconsistency.

No numerical threshold is admitted here.

`TOLERANCE_NOT_YET_QUALIFIED`.
