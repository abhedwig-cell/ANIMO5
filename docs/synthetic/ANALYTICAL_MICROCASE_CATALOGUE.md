# ANIMO-SYNQ01 analytical and conservation microcase catalogue

Status: `QUALIFIED_SYNTHETIC_MICROCASE_CATALOGUE`

The machine-readable authoritative records are in `integration/animo-synthetic/SYNTHETIC_ORACLE_REGISTER.json`. This document explains the cases and their evidence boundaries.

## Core discrepancy oracles

| Oracle | Target | Type | Independent expected relation | SYNQ result | Main limit |
| --- | --- | --- | --- | --- | --- |
| `SYNQ-O001` | TCD-015 | O1/O6 conservation | duplicated moisture-storage contribution is exactly `Avc*Hv*St*Ld`; conservative reconstruction residual is zero | PASS | does not choose clipping physics |
| `SYNQ-O002` | TCD-017 | O1/O6 conservation | internal P source plus destinations sum to zero | PASS | not full ploughing non-interference proof |
| `SYNQ-O003` | TCD-018 | O1/O6 conservation | beginning interception storage + input - outputs = ending storage | PASS | not a SWAP hydrology qualification |
| `SYNQ-O004` | TCD-023 | O1 analytical | each C/N/P daughter pair partitions its own species parent exactly | PASS | broader stable-DOM theory not qualified here |
| `SYNQ-O005` | TCD-023 | O5 metamorphic | species permutation of inputs gives the same permutation of outputs | PASS | no historical activation claim |
| `SYNQ-O006` | TCD-024 | O2 analytical | each slow-Langmuir site uses its own `K_j`, rate and state in the closed relaxation solution | PASS | formulation authority partly source-bound |
| `SYNQ-O007` | TCD-024 | O1 index-domain | site selector must lie in `1..Nsite`; trial counter `1..20` is invalid for `Nsite<=3` | PASS | does not prove historical trial count reached 4 |
| `SYNQ-O008` | TCD-025 | O6 conservation | internal matrix/macropore exchange cancels; direct drain is external | PASS | does not qualify the macropore transfer law |
| `SYNQ-O009` | TCD-019 | O4/O3 high precision | one-site Langmuir mass-storage equation has a unique independently solved positive root | PASS | no fallback/tolerance admission |

## TCD-015 controlled clipping discriminator

Synthetic input:

```text
Avc = 0.2 kg m-3
Hv  = 0.1 d-1
St  = 2 d
Ld  = 0.1 m
```

The exact extra mass created by using the storage derivative twice is:

```text
Avc * Hv * St * Ld
= 0.2 * 0.1 * 2 * 0.1
= 0.004 kg m-2.
```

This is not fitted to the known B1 event. The values were chosen independently. The expected result is the algebraic difference between a full storage-change reconstruction and a reconstruction that inserts the same storage derivative again inside the disappearance coefficient.

The natural PREP01 B1 event is useful corroboration because its residual equals the same term, but that observed magnitude is not the oracle.

What this proves: the duplicated term necessarily violates the local mass identity whenever all four factors are nonzero.

What it does not prove: whether clipping to a near-zero concentration is itself the scientifically preferred state policy.

## TCD-017 exact internal organic-P redistribution

Synthetic stores and transfer:

```text
initial physical P total = 1.70 kg P m-2
top source loss          = 0.31 kg P m-2
layer 1 destination gain = 0.12 kg P m-2
layer 2 destination gain = 0.19 kg P m-2
```

The internal ledger is:

```text
-0.31 + 0.12 + 0.19 = 0 exactly.
```

The final physical P total remains `1.70 kg P m-2`. This is a pure control-volume result. A reporting path that includes only the positive destination entries fails the oracle even though physical redistribution can remain conservative.

## TCD-018 interception control volume

The selected control volume is the interception store alone:

```text
begin storage = 0.06 mm
precipitation = 0.10 mm
evaporation   = 0.04 mm
throughfall   = 0.08 mm
end storage   = 0.04 mm
```

Then:

```text
0.06 + 0.10 - 0.04 - 0.08 - 0.04 = 0 mm.
```

Throughfall is an output for the canopy control volume. If canopy plus soil are composed into a larger control volume, throughfall becomes an internal transfer and must cancel against the receiving store or flux.

This explicit boundary rule prevents a ledger from silently mixing control volumes.

## TCD-023 asymmetric species partition

The synthetic parent-transfer map is:

```text
X17 = m * k * C_X * H
X19 = (1-a) * X17
X20 = a * X17
```

with:

```text
m = 0.35
k = 0.08
H = 0.2
a = 0.3
C_C = 2.0
C_N = 0.2
C_P = 0.05
```

Expected tuples `(parent, daughter_19, daughter_20)` are:

```text
C: (0.011200, 0.0078400, 0.0033600)
N: (0.001120, 0.0007840, 0.0003360)
P: (0.0002800, 0.00019600, 0.00008400)
```

The large C/N/P asymmetry is deliberate. If the P daughters are constructed from the N parent, they sum to `0.001120`, not to the P parent `0.0002800`. The defect is therefore strongly discriminated.

A separate metamorphic relation permutes the three species and their concentrations. A correct species-local implementation must permute the output tuples in exactly the same way.

## TCD-024 unequal slow-Langmuir sites

For a site `j` at fixed solution concentration during the isolated microcase:

```text
qeq_j = (Qmax_j/rho) * (K_j*C)/(1+K_j*C)
y_j   = exp(-r_j*(1+K_j*C)*dt)
qnew_j = qold_j*y_j + qeq_j*(1-y_j)
```

Synthetic values:

```text
C   = 0.04
dt  = 1.5
rho = 1
site 1: Qmax=0.30, K=2,   qold=0.010, r_ads=0.20,  r_des=0.02
site 2: Qmax=0.90, K=40,  qold=0.020, r_ads=0.07,  r_des=0.01
site 3: Qmax=0.12, K=600, qold=0.005, r_ads=0.015, r_des=0.003
```

Independent 80-digit evaluation gives:

```text
site 1: 0.01338249703757970376432360100
site 2: 0.1475396964503997007310583129
site 3: 0.05240993271465228432371740819
```

A deliberately seeded wrong-selector comparator that substitutes site 1 `K` into every exponential gives:

```text
site 1: 0.01338249703757970376432360100
site 2: 0.07723179301663063224564232867
site 3: 0.007645585949326259218924871008
```

The mutation is therefore strongly detectable. The comparator is explicitly not an oracle. It exists only to show that the independent expected relation discriminates the target defect.

The separate index-domain oracle is exact: the frozen source trial loop has `I=1,20`, the slow-site loop has `J=1,Ncxsl`, and the site parameter dimension is at most three. A site parameter lookup by `I` can therefore leave the site domain at trial 4. This proves latent bounds risk, not historical reachability of trial 4.

## TCD-025 matrix/macropore ledger

Synthetic beginning stores:

```text
matrix    = 1.00
macropore = 0.40
```

Transfers:

```text
matrix -> macropore internal transfer = 0.15
direct macropore drainage             = 0.05 external
```

Expected ending stores:

```text
matrix    = 0.85
macropore = 0.50
```

Internal ledger:

```text
-0.15 + 0.15 = 0.
```

Whole control volume:

```text
1.40 - 0.05 - 1.35 = 0.
```

This matches the ownership pattern that MP02 needs the main ledger to represent. It does not state how the physical exchange rate should be calculated.

## TCD-019 high-precision nonlinear storage root

SYNQ01 uses a deliberately narrow one-site Langmuir storage problem:

```text
M = theta*C + Qmax*K*C/(1+K*C)
M     = 0.19
theta = 0.35
Qmax  = 0.24
K     = 125
```

The equation is monotone for `C>=0`. An independent 80-digit bisection gives:

```text
C = 0.024732930809625083503747803765411500305928116656832687079812828494088910154040112
```

The final bracket width is `8.73226197e-73` after 240 bisection iterations. Re-evaluating the equation at 100-digit precision gives an absolute residual of about `5.188148027200227070292506930e-73`.

Independently multiplying the equation by `(1+K*C)` gives a quadratic. Its exact positive root agrees within the final bisection bracket. This cross-check is useful because it does not reuse the bisection convergence logic.

This oracle tests solution correctness for this constitutive microproblem. It intentionally says nothing about ANIMO `Small`, fallback policy, Newton iteration count or a production tolerance.

## Temporal microcases

### `SYNQ-T001` management `(t0,t1]`

For `t0=0`, `t1=1` and events at `0`, `0.5`, `1`, the exact selected set is:

```text
0.5, 1
```

The event at `t0` is excluded and the event at `t1` is included.

### `SYNQ-T002` harvest `[t0,t1)`

For the same values, the exact selected set is:

```text
0, 0.5
```

The event at `t0` is included and the event at `t1` is excluded.

These relations come from the qualified reconstructed TIME01 candidate contract. Their independence classification is therefore `STRUCTURALLY_CORRELATED`, even though the test implementation is separate.

### Retry with changed `t1`

Changing `t1` from `1` to `1.5` changes management membership from `[0.5,1]` to `[0.5,1,1.5]` exactly. No epsilon is used. This provides a clean fixture for the TIME01 rule that changed `t1` requires a new interval identity.

### `SYNQ-T003` split run

A fully explicit scalar state with deterministic updates is run continuously and split after an accepted boundary. Both paths end at exactly `1.20`.

This only proves the serializer identity for complete explicit state. Actual ANIMO restart equivalence remains blocked where continuation state is incomplete or hidden.

## Limiting-case library

| ID | Limiting relation | Result |
| --- | --- | --- |
| `SYNQ-L001` | zero reaction rate leaves a closed store unchanged | PASS |
| `SYNQ-L002` | zero transport leaves transport-only storage unchanged | PASS |
| `SYNQ-L003` | zero Langmuir capacity gives zero sorbed amount | PASS |
| `SYNQ-L004` | zero crop demand gives zero demand-limited uptake | PASS |
| `SYNQ-L005` | zero external forcing contributes zero ledger delta | PASS |
| `SYNQ-L006` | single-layer profile total equals its sole layer | PASS |
| `SYNQ-L007` | one active species has no inactive-species partition dependency | PASS |
| `SYNQ-L008` | one active site reduces to that site's analytical relation | PASS |
| `SYNQ-L009` | identical sites are invariant under permutation | PASS |
| `SYNQ-L010` | identical layers preserve total storage under permutation | PASS |
| `SYNQ-L011` | zero macropore exchange leaves both stores unchanged absent external drain | PASS |
| `SYNQ-L012` | inactive synthetic feature contributes no state or ledger delta | PASS |

These cases are negative controls and structural sentinels. Passing them alone never establishes process qualification.
