# PREP05 — TCD-024 composition and non-interference probe

Status: `DIAGNOSTIC_COMPOSITION_AND_BRANCH_NONINTERFERENCE_CONFIRMED_REFERENCE_ADMISSION_BLOCKED`.

This note extends the causal TCD-024 evidence with two independent checks:

1. interaction with TCD-019 nonlinear phosphorus conservation policy;
2. non-interference on the supplied `OPTCXSL=3` Freundlich route.

The frozen source and supplied testcases remain unchanged.

## 1. Composition matrix

A three-site synthetic `OPTCXSL=2` case with unequal slow-Langmuir affinity parameters was executed under four diagnostic source-copy policies:

1. frozen revision-53 index and numerical policy;
2. TCD-019 only: stable fast-Langmuir secant plus tighter `C_unl` convergence;
3. TCD-024 only: `Parcxsl(3,I) -> Parcxsl(3,J)` in `Conc_unl`;
4. TCD-019 + TCD-024 combined.

All four executions completed.

### Final cumulative Bapp deviation

| policy | GP kg/ha P | TP kg/ha P | RP kg/ha P |
| --- | ---: | ---: | ---: |
| frozen synthetic baseline | `-158` | `-329` | `-54.4` |
| TCD-019 only | `-157` | `-328` | `-54.1` |
| TCD-024 only | `-0.432` | `-0.726` | `-0.254` |
| TCD-019 + TCD-024 | `+0.0148` | `+0.349` | `-2.11e-5` |

TCD-019 alone barely changes the catastrophic slow-Langmuir nonclosure. TCD-024 removes the dominant error. Applying TCD-019 after the site-index correction removes most of the remaining recurrent numerical drift.

This demonstrates that the findings are distinct and approximately orthogonal:

- TCD-024 owns parameter-site binding in one slow-Langmuir iterative branch;
- TCD-019 owns constitutive finite-change consistency and nonlinear stopping policy.

The remaining combined GP/TP cumulative offsets are not accepted as numerical tolerance. Their period structure is sparse rather than the prior recurrent annual drift and must be reconciled with existing initialization/other P ledger seams before any corrected-reference admission.

## 2. Period residual behavior after composition

For the combined diagnostic run:

- GP largest period deviation: `+0.0148 kg/ha P` in 1996; final 2015 period deviation approximately `-5.05e-8`;
- TP largest period deviation: `+0.0803 kg/ha P` in 2012; final 2015 period deviation approximately `+9.38e-9`;
- RP largest period deviation: `-2.11e-5 kg/ha P` in 1991; final 2015 period deviation approximately `+4.08e-11`.

Thus the composition removes the strong year-after-year negative drift. The remaining GP/TP cumulative offsets are driven by isolated periods and belong to a separate causal analysis if they become relevant to corrected-reference qualification.

## 3. Non-interference on supplied Freundlich route

The TCD-024-only executable was run against the unmodified supplied LWKM testcase, which uses:

```text
OPTCXSL = 3
```

The output tree was compared with the existing frozen-source GNU diagnostic execution.

Ignoring only local harness stdout/stderr files and normalizing only the already-declared volatile timestamp/CPU metadata:

```text
model outputs compared: 55
normalized differences: 0
missing model outputs: 0
extra model outputs: 0
```

The only files present in the earlier execution tree but not regenerated as model outputs were local harness logs `diag_stdout.txt` and `diag_stderr.txt`.

Therefore the `I -> J` correction is diagnostically inert on the supplied Freundlich route, as expected from the source branch condition.

## 4. Interpretation

The evidence supports the following separation:

```text
TCD-024 = wrong parameter index / latent bounds risk
TCD-019 = numerical constitutive-conservation policy
```

Neither should be hidden inside a single broad phosphorus modernization patch.

A future corrected-legacy qualification should admit them serially and then re-run the composition matrix against a qualified frozen reference.

## 5. Gate

`DIAGNOSTIC_TCD024_TCD019_INDEPENDENCE_AND_FREUNDLICH_NONINTERFERENCE_CONFIRMED`

Historical-reference qualification remains blocked and production migration remains `NOT_ADMITTED`.
