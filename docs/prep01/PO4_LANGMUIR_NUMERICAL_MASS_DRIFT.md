# PO4 Langmuir equilibrium-sorption numerical mass drift

Status: `CONFIRMED_LEGACY_NUMERICAL_MASS_NONCONSERVATION_AND_CONVERGENCE_POLICY_DEPENDENCY`.

This note records PREP01 diagnostic evidence against the supplied revision-53 source and the deterministic LWKM testcase. The frozen source and testcase are unchanged.

## Observed cumulative drift

For `LWKM_gras_1040.2021.2045`, source instrumentation of `Transgen.for` records 27,000 layer/timestep PO4 mass checks. Summing the exact local residual `BAPD-BATR` over the complete run gives:

`-0.27254515116349 kg/ha P`.

This matches the cumulative `Bapp` drift to the precision exposed by the legacy output. The drift is therefore generated inside the `Transgen` / `Transorp` numerical mass seam and is not an `Outbal_calc` bookkeeping omission.

## Source structure

`Transgen` defines for soil layers:

```text
BAPD = Rekopo * St * He
```

and compares this process mass with transport plus changes in:

- dissolved PO4;
- precipitated PO4;
- instantaneous/equilibrium sorption pools;
- rate-dependent sorption pools.

For the LWKM case the equilibrium sorption option is Langmuir (`OPTCXFA=2`, one fast/equilibrium site).

`Sorpfast` has two materially different Langmuir paths.

For `abs(Ct-Ct0) < 1e-6`, it uses the endpoint tangent as the average adsorption coefficient:

```text
Avadco = Q*K / (Rhbd * (1 + K*Ct)^2)
```

while still setting final sorbed mass from the nonlinear Langmuir relation.

For larger concentration changes, it instead uses the actual secant between final and supplied initial sorbed state:

```text
Avadco = (Rsampocxfa - Ampocxfa) / (Ct-Ct0)
```

when that secant is non-negative.

The latter form is directly consistent with the storage change represented in `Transgen`; the small-delta tangent shortcut is only an approximation to that storage change.

## Localization to the small-delta shortcut

A source-consistent trace identifies 25,923 of the 27,000 LWKM layer/timestep checks as using the Langmuir small-delta condition.

The exact `BAPD-BATR` sum over only those 25,923 events is:

`-0.27254514417026 kg/ha P`.

The sum over all remaining events is only:

`-6.99323e-9 kg/ha P`.

Thus essentially the complete baseline dynamic PO4 mass drift occurs on events covered by the small-delta Langmuir shortcut.

For the same events, the difference between the actual fast-sorption storage change and the tangent-based storage approximation sums to approximately:

`+0.25489380345319 kg/ha P`.

Its sign is opposite to the corresponding mass residual, as expected from the storage side of the `BAPD-BATR` equation.

## Controlled numerical probes

All probes below were performed on temporary execution-only source copies. No frozen source or input was changed.

### Probe A: tighten only `Conc_unl` convergence

Change:

```text
Small = 1e-4 -> 1e-8
```

Resulting cumulative `Transgen` residual:

`-0.25489423322790 kg/ha P`.

This almost isolates the tangent-shortcut contribution. It demonstrates that the ordinary nonlinear convergence policy contributes additional drift, but tightening convergence alone does not solve the dominant mass inconsistency.

### Probe B: avoid the tangent shortcut except at near-machine-small delta

Change only:

```text
abs(Ct-Ct0) < 1e-6 -> abs(Ct-Ct0) < 1e-12
```

so that the existing general secant path is used for almost all small but finite changes.

Resulting cumulative `Transgen` residual:

`-0.01797396283765 kg/ha P`.

This removes most of the baseline drift without changing the sorption isotherm itself.

### Probe C: combine A and B

With `Small=1e-8` and the shortcut threshold reduced to `1e-12`, the complete 27,000-event cumulative residual becomes:

`+9.63374343e-6 kg/ha P`.

The largest local event is approximately:

`1.01408e-5 kg/ha P`.

The legacy formatted `Bapp` period residuals simultaneously collapse to roughly micro-scale values.

### Negative controls

Tightening the fallback bisection mass equation from `1e-6` to `1e-12` did not materially alter the baseline drift.

Correcting the unrelated `Parcxsl(3,I)` index to `Parcxsl(3,J)` also did not alter this case because LWKM uses Freundlich (`OPTCXSL=3`) for the slow sorption sites. That suspicious source construct is therefore not causal for this finding.

## Interpretation

Two numerical mechanisms are separated:

1. `Sorpfast` small-delta Langmuir shortcut: a deterministic mass-inconsistent approximation because a tangent coefficient is substituted for the finite storage change represented by the nonlinear isotherm and supplied starting sorbed state.
2. `Conc_unl` convergence policy: a numerical tolerance dependency that adds a smaller but still systematic closure error under the legacy `Small=1e-4` criterion.

Classification of mechanism 1:

`CONFIRMED_LEGACY_NUMERICAL_MASS_NONCONSERVATION`.

Classification of mechanism 2:

`NUMERICAL_POLICY_MASS_CLOSURE_DEPENDENCY`.

PREP01 does not yet prescribe the production correction. Simply changing thresholds is not a sufficiently general scientific design.

## Corrected-legacy / ANIMO5 consequence

A corrected implementation should enforce a conservative relationship between:

- start dissolved concentration;
- start equilibrium-sorbed mass;
- end dissolved concentration;
- end equilibrium-sorbed mass;
- the effective storage coefficient used by the nonlinear transport solve.

For a Langmuir isotherm, a numerically stable finite-change formulation is available analytically, but it must also define what happens when the supplied starting sorbed state is not exactly on the equilibrium isotherm. That connects this finding to the separate initial-state consistency seam TCD-014.

ANIMO5 should therefore treat nonlinear-solver tolerances as explicit numerical policy and test local and cumulative mass closure independently of convergence success.

The raw `~0.273 kg/ha P` LWKM drift must not be promoted to a mass-balance acceptance tolerance.
