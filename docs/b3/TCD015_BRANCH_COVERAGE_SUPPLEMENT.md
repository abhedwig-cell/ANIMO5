# ANIMO-B3B01 TCD-015 branch-coverage supplement

Status: `QUALIFIED_REACHABLE_CLIPPING_RECONSTRUCTION_BRANCH_COVERAGE_WITH_STRUCTURAL_UNREACHABILITY_FOR_IFLSOL_2_AND_5`

This supplement strengthens the Class-B branch-coverage evidence for `TCD-015`. It does not change the atomic claim, does not alter clipping policy or tolerances, does not create B2, and does not admit corrected legacy behaviour.

## Exact branch under review

The target remains the second negative-concentration reconstruction in frozen revision-53 `Transsub.for`, after `Rsc` has been set to `Vsmall` and `Avc` has been recomputed. The only candidate algebra is the nitrate-scoped replacement of `Avc*Hv1` by `Avc*(Hv1-Hv)` in the reconstructed `Reko` term.

Therefore, whenever the target reconstruction is reached:

```text
Delta(Reko) = Reko_candidate - Reko_legacy = -Avc*Hv
```

No analytical-solution selection, clipping trigger, `Vsmall`, `Ttry`, state reconstruction, hydrology, or non-nitrate transport policy is changed.

## Natural B1 reachability observation

A diagnostic build was made from the exact frozen B0 source with only one stdout observer inserted immediately before the target `Reko` reconstruction. Frozen `Transsub.for` SHA-256 remains the source identity `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`; the observer copy has SHA-256 `fdd0b6cf3e2814121484399a78d220d3bb58c5b66971fa2e54a471183355496a` and diagnostic executable SHA-256 `b8f0b2421200cde55c848a60e5fc942761363af113d8ed555d423bacd9e02013`.

Across the same eight PREP01-compatible natural B1 cases, the target reconstruction was reached 508 times, all for `NITRATE`:

| Case | Target hits | `Iflsol=1` | `Iflsol=3` |
|---|---:|---:|---:|
| CranGrass | 0 | 0 | 0 |
| CranMais | 0 | 0 | 0 |
| GrassPeat | 301 | 279 | 22 |
| LWKM_gras_1040.2021.2045 | 199 | 199 | 0 |
| RuurloGrass | 0 | 0 | 0 |
| STONE_akk_0006.2001.2015 | 8 | 8 | 0 |
| Puitmijn_Cranendonck_60 | 0 | 0 | 0 |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 0 | 0 | 0 |

Thus natural B1 directly covers `Iflsol=1` and `Iflsol=3`. `Iflsol=1` has nonzero `Hv` and therefore carries the proposed correction effect. `Iflsol=3` has `Hv=0`, so the candidate algebra is exactly identical to legacy on that branch and acts as a structural zero-delta control.

## Isolated frozen-source coverage of the reachable modes

An isolated harness calls the exact frozen `Transsub.for` and, separately, the already qualified execution-only nitrate-scoped candidate. The harness SHA-256 is `6826809198954ab7adea3aabf729b34b85c08bccfcd5553d62607a6c854d1b41`. Baseline and candidate harness executable SHA-256 values are respectively `da7d11adb8f870cfca0b4a987eddb9ad67884274844aebe5e77e912ff8fab2c2` and `b9f4e01a4a416aa6973e15c798ef17028b5f15087ef283ab91c580f2764c3501`.

The common synthetic inputs are `NITRATE`, `Optneg=0`, `Ln=1`, `Co=0.01`, `St=1`, `Ld=0.05`, `Socf=0`, `Rhbd=1000`, zero boundary-solute inputs, zero `Reki`, and initial `Reko=-0.002`.

Three target calls qualify the reachable analytical modes:

| Mode | `Mto` | `Mt` | `Fu` | `Hv` | `Hv1` | Legacy `Reko` | Candidate `Reko` | `-Avc*Hv` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Iflsol=1` | 0.2 | 0.1 | 0.001 | -0.1 | -0.08 | -0.0024574754342038042 | -0.0018856311413240493 | +0.0005718442928797548 from printed `Avc` |
| `Iflsol=3` | 0.2 | 0.2 | 0.001 | 0 | 0.02 | -0.0019062035958855592 | -0.0019062035958855592 | 0 |
| `Iflsol=4` | 0.2 | 0.1 | 0.005 | -0.1 | 0 | -0.0019999999999000002 | -0.0015436139438016437 | +0.0004563860560983565 |

For every call, both baseline and candidate reach the target reconstruction with `Rsc=Vsmall`. `Rsc` and `Avc` are identical between baseline and candidate. The source-level candidate-minus-legacy expression is algebraically `-Avc*Hv`. For `Iflsol=4` the subtraction reconstructed from the printed outputs matches the printed `-Avc*Hv` value exactly. For `Iflsol=1`, subtracting the separately rounded printed `Reko` values gives `0.0005718442928797549`, while `-Avc*Hv` from the printed `Avc` gives `0.0005718442928797548`, a one-rounding-unit evaluation-order difference of `1.0842021724855044e-19`. This is recorded explicitly and is not converted into a tolerance criterion. `Iflsol=3` remains exactly unchanged because `Hv=0`.

This explicitly covers `Iflsol=4`, which is not reached by the target reconstruction in the supplied natural B1 suite.

## Structural unreachability of `Iflsol=2` and `Iflsol=5`

Let

```text
B = Mto + Rhbd*Socf
```

Before analytical-solution selection, frozen `Transsub.for` applies the zero-order pre-adjustment such that

```text
B*Co + Hv2*St >= 0
```

or, if the adjustment fires, replaces `Hv2` so that this numerator becomes `Vsmall`.

For `Iflsol=2`, `Hv1=Hv` and the frozen analytical coefficients reduce to

```text
Rsc = (B*Co + Hv2*St) / (B + Hv*St)
```

For a valid positive final storage denominator, `Rsc` cannot be negative because the numerator is non-negative by the frozen pre-adjustment. The second negative-concentration reconstruction is therefore structurally unreachable for `Iflsol=2` in the valid storage domain.

For `Iflsol=5`, `Hv=0` and `Hv1=0`, and the frozen solution reduces to

```text
Rsc = (B*Co + Hv2*St) / B
```

With positive `B`, the same pre-adjustment makes negative `Rsc` impossible. The target reconstruction is therefore structurally unreachable for `Iflsol=5` as well.

The target branch is consequently covered over all reachable analytical modes:

- `Iflsol=1`: natural B1 plus isolated frozen-source nonzero-effect probe;
- `Iflsol=3`: natural B1 plus isolated exact zero-delta control;
- `Iflsol=4`: isolated frozen-source nonzero-effect probe;
- `Iflsol=2` and `Iflsol=5`: structurally unreachable for the target negative-reconstruction branch under the valid positive-storage domain.

## Admission boundary

This supplement removes a branch-coverage ambiguity from the readiness dossier. It does not resolve the admission route or independent-review gates. PREP02R remains without a qualified historical reference and the GOV02 historical-uncertainty route remains ineligible while acquisition is still active. Independent second-line review is still not complete.

The ANIMO-B3B01 decision therefore remains:

`QUALIFIED_TCD015_CLASS_B_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`
