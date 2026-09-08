# ANIMO-PREP06 — Exudate initial-storage omission in fresh-OM balance

Status: `CONFIRMED_LEGACY_INITIAL_STORAGE_LEDGER_OMISSION_ACCOUNTING_ONLY`.

The frozen revision-53 source and supplied testcases remain unchanged. All mutations described below were confined to temporary diagnostic copies.

## Source asymmetry

`Ex(Ln)` is a persistent organic-matter state:

- `input1.for` reads it from `INITIAL.INP`;
- `Resp_miner` evolves it to `Rsex(Ln)`;
- `Init.for` commits `Ex(Ln)=Rsex(Ln)` for the next step;
- `Output_Init.for` persists `Rsex` in restart output.

The fresh-organic-matter balance is asymmetric across the period boundary.

At period end, `Outbal_calc.for` includes:

```fortran
Bfom(Finp_x,Ly) = Bfom(Finp_x,Ly) + Rsex(Ln) * Z
```

At initialization, `Outbal_Init.for` includes fresh fractions `Os`, then humus states, but omits `Ex` from `Bfom(Inip_x,Ly)`.

The same beginning exudate state is correctly represented in the elemental organic ledgers:

```fortran
Bano(Inip_x,Ly) = ... + Ex(Ln)*Nifrex*P
Bapo(Inip_x,Ly) = ... + Ex(Ln)*Pofrex*P
```

Therefore the omission is specific to the fresh-organic-matter mass ledger, not to the underlying exudate state.

## Supplied-testbank coverage

Every supplied `>orgexu:` block initializes all layers to zero. The ordinary supplied testbank therefore cannot expose this defect.

## Synthetic causal probe

A diagnostic copy of the already executable `RuurloGrass` case was changed only by setting:

```text
Ex(1) = 1.0e-3 kg/m2
```

Equivalent beginning exudate mass:

```text
10.0 kg/ha organic matter
```

The frozen-source diagnostic executable completes the case. The first fresh-OM balance record reports:

```text
Bfom period deviation = -10.0 kg/ha
cumulative deviation  = -10.0 kg/ha
```

The residual is therefore exactly the omitted beginning exudate mass.

Organic-N closure for the same synthetic run remains at approximately `1e-11 kg/ha N`, consistent with the fact that `Ex*Nifrex` is already present in the N initial ledger.

## Ledger-only correction probe

A second temporary build changed only `Outbal_Init.for` by adding:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

No state, process rate, hydrology, forcing or testcase quantity was otherwise changed.

Result:

```text
baseline maximum fresh-OM period residual: 10.0 kg/ha
ledger-only maximum residual:              6.55e-11 kg/ha
```

The cumulative fresh-OM residual drops from `10.0 kg/ha` to about `9.09e-11 kg/ha`.

## Non-interference

Seventy-two generated outputs were compared between the baseline synthetic execution and the ledger-only correction after normalizing only the already admitted volatile timestamps/CPU metadata.

Exactly six files differ:

- `ani_omGP.Bal`;
- `ani_omRP.Bal`;
- `ani_omTP.Bal`;
- `baomGP.Out`;
- `baomRP.Out`;
- `baomTP.Out`.

All ordinary state/process outputs and all N/water outputs are normalized-identical.

## Classification

`CONFIRMED_LEGACY_INITIAL_STORAGE_LEDGER_OMISSION`

Proposed corrected-legacy class:

`A_ACCOUNTING_ONLY_INITIAL_STORAGE_COVERAGE`

Properties:

```text
physics_changed = false
state_trajectory_changed = false
initial_ledger_coverage_corrected = true
reference_qualification_required = true
production_migration_admitted = false
```

## ANIMO5 requirement

Beginning and end storage for every conserved state must be generated from one explicit state-ownership model. A restartable state such as exudate mass must not be present on the end side of a ledger while absent from the beginning side.

Qualification must include nonzero initial-state tests for every independently restartable conserved store; zero-filled production testbanks are insufficient to prove ledger completeness.
