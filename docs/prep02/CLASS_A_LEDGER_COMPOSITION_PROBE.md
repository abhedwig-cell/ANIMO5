# Class-A corrected-legacy ledger composition probe

Status: `DIAGNOSTIC_COMPOSITION_STATE_TRAJECTORY_EQUIVALENCE_DEMONSTRATED_FOR_LWKM_NOT_REFERENCE_ADMISSION`.

## Purpose

TCD-017 and TCD-018 were independently localized as balance-accounting defects. This probe tests the stronger claim needed for a future Class-A corrected-legacy workunit: composing both accounting corrections should change only their intended balance ledgers and should not alter the physical/process state trajectory.

This is diagnostic evidence only. The frozen source remains unchanged and no corrected-legacy candidate is reference-qualified.

## Probe composition

Starting point: the deterministic GNU diagnostic contract used by PREP01.

Temporary source-copy changes:

1. TCD-017 organic-P redistribution bookkeeping:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

for the top-reservoir ploughing balance scope.

2. TCD-018 water interception storage:

accumulate `(Sict-Sic)*1000` for every top-profile balance period and subtract the accumulated interception-storage change from `Bawa(Ddev,Ly)` at balance finalization, preserving period reset semantics.

No transport equation, process rate, hydrology state, forcing, input state or testcase file was changed.

Case: `LWKM_gras_1040.2021.2045`.

## Resulting balance envelope in LWKM

| balance | maximum absolute period residual after Class-A probe |
| --- | ---: |
| water | `2.07e-4 mm` |
| fresh organic matter | `6.98e-10 kg/ha OM` |
| humus | `5.82e-10 kg/ha OM` |
| dissolved organic matter | `1.10e-4 kg/ha OM` |
| NH4-N | `3.16e-6 kg/ha N` |
| NO3-N | `5.76e-1 kg/ha N` |
| organic N | `5.99e-6 kg/ha N` |
| PO4-P | `1.71e-2 kg/ha P` |
| organic P | `6.54e-7 kg/ha P` |

The large NO3 residual remains, as expected, because TCD-015 was deliberately not included. The remaining PO4 residual is also outside Class A and is not interpreted here.

The important result is that the characteristic water `~0.06 mm` residual and the organic-P ploughing residuals are removed without reducing or hiding unrelated residual classes.

## State and ordinary-output equivalence

The combined Class-A run was compared with the frozen-source GNU diagnostic LWKM run.

Twenty ordinary non-balance output files common to both executions were compared after normalizing only the run/file creation timestamp strings already treated as volatile by PREP01. Examples include concentration and process-output surfaces such as `ammonium.out`, `nitrate.out`, `miner-N.out`, `pal-P.out`, `pw-P.out`, `Animoinputs.Out` and `animointermediate.Out`.

Result:

```text
ordinary outputs compared: 20
normalized differences:    0
```

In addition, 21 unaffected balance-output files for OM/N/inorganic-P families were compared after the same timestamp normalization.

Result:

```text
unaffected balance outputs compared: 21
normalized differences:             0
```

Thus, within the investigated LWKM diagnostic scope, the composed TCD-017/TCD-018 corrections change only the balance surfaces they are intended to correct.

## Interpretation

This provides stronger evidence for the future `CL-01` classification:

`state_trajectory_unchanged = demonstrated_for_LWKM_diagnostic_scope`

It does not yet prove that the same property holds for every testcase, every balance-profile configuration or the historical Intel executable.

The future corrected-legacy admission must therefore repeat this comparison against a qualified frozen reference and expand it across cases with:

- ploughing/tillage active and inactive;
- interception storage changing and constant;
- multiple balance profiles and reset schedules;
- both detailed and other admitted hydrology routes.

## Gate

`DIAGNOSTIC_CLASS_A_COMPOSITION_SUPPORTED_NOT_REFERENCE_QUALIFIED`

No production correction is admitted by this probe.
