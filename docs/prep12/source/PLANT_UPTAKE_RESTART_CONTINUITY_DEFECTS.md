# ANIMO-PREP10 — Plant uptake restart-continuity defects

Status: `DIAGNOSTIC_CAUSAL_AND_NATURALLY_REACHABLE_REFERENCE_ADMISSION_BLOCKED`.

This document separates two distinct restart-state defects in the revision-53 plant uptake lifecycle. The frozen source archive and supplied testbank remain unchanged. Observer and correction changes were applied only to temporary diagnostic execution copies.

Frozen source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Baseline GNU diagnostic executable SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Observer executable SHA-256:

`05b13666dd4ba4c99a13954e8d286a62461c8557b021c412f84c1a236a00ae78`

## 1. State lifecycle

For plant modes 1 and 3, `Init.for` carries both actual and potential cumulative uptake between accepted timesteps:

```fortran
Amplni_act = Rsamplni_act
Amplni_pot = Rsamplni_pot
...
Amplpo_act = Rsamplpo_act
Amplpo_pot = Rsamplpo_pot
```

Potential uptake is scientifically active state. `Uptpar_Plant.for` uses quantities including:

```text
Amplni_pot - Amplni_act
Amplpo_pot - Amplpo_act
```

in subsequent nutrient-demand logic. `Upintg_Plant` and `Upintg_Extern` update the corresponding result states.

The restart contract must therefore preserve the cumulative actual and potential quantities if a trajectory is to continue from a restart boundary.

## 2. TCD-033 — actual uptake restart initialization direction

### Source defect

`input1.for` reads `Rsamplni_act` and optional `Rsamplpo_act` from `>orgpla:`.

For a non-grass or externally controlled crop, `Inicalc.for` then executes:

```fortran
If(Rsamplni_act.Lt.1.0d-4) Amplni_act = 0.0
Rsamplni_act = Amplni_act
Amplni_pot = 0.0
```

with the analogous phosphorus statements.

When the restart value is above the small-value threshold, no statement assigns:

```text
Amplni_act <- Rsamplni_act
Amplpo_act <- Rsamplpo_act
```

before the opposite assignment overwrites the restart-side value. The intended restart value therefore has no dataflow path into the accepted actual-uptake state.

### Natural supplied-case reachability

The unmodified supplied LWKM initial file already contains nonzero `>orgpla:` cumulative actual uptake:

```text
Rsamplni_act = 0.0666813 kg/m2 N
Rsamplpo_act = 0.0088759 kg/m2 P
```

An observer-only diagnostic executable records state immediately after `Inicalc`.

Frozen-source behaviour:

```text
Amplni_act   = 0.0
Rsamplni_act = 0.0
Amplpo_act   = 0.0
Rsamplpo_act = 0.0
```

The supplied nonzero restart values are therefore discarded before the simulation loop.

### Minimal causal correction probe

A temporary source copy added only the missing direction before the existing small-value filter:

```fortran
Amplni_act = Rsamplni_act
...
Amplpo_act = Rsamplpo_act
```

The existing threshold logic and opposite result-state copy were otherwise left unchanged.

Corrected observer result immediately after `Inicalc`:

```text
Amplni_act   = 0.0666813 kg/m2 N
Rsamplni_act = 0.0666813 kg/m2 N
Amplpo_act   = 0.0088759 kg/m2 P
Rsamplpo_act = 0.0088759 kg/m2 P
```

Temporary corrected observer executable SHA-256:

`ad6b32062c458f6e9eda061e7a02e1143eaaad23c920687c3f06a7b5e5f7ec64`

The full diagnostic trajectory is not used to define a scientific correction tolerance. The important causal fact is the restart-state handoff at initialization.

### Classification

`CONFIRMED_LEGACY_PLANT_ACTUAL_UPTAKE_RESTART_INITIALIZATION_DIRECTION_DEFECT`

This is not accounting-only. Preserving a different accepted plant uptake state can affect later nutrient-demand and crop response calculations.

## 3. TCD-034 — potential uptake absent from restart representation

### Source omission

Revision 53 carries:

```text
Amplni_pot <-> Rsamplni_pot
Amplpo_pot <-> Rsamplpo_pot
```

between normal timesteps for plant modes that use potential uptake.

However `input1.for` `>orgpla:` reads only root/shoot state and cumulative **actual** N/P uptake. `Output_Init.for` writes only:

```text
Rsamplro
Rsamplsh
Rsamplni_act
Rsamplpo_act   [when P active]
```

There are no restart fields for `Rsamplni_pot` or `Rsamplpo_pot`.

`Inicalc.for` explicitly initializes `Amplni_pot` and `Amplpo_pot` to zero.

### Natural supplied-case reachability

The unmodified LWKM diagnostic execution uses `CropUptakeModel=1`, which selects plant mode 3. Immediately before the final `Output_Init` call the observer records:

```text
Rsamplni_act = 0.06659176667769946 kg/m2 N
Rsamplni_pot = 0.06634733          kg/m2 N
Rsamplpo_act = 0.007806854062503923 kg/m2 P
Rsamplpo_pot = 0.007806854         kg/m2 P
```

The emitted `initial.out` `>orgpla:` block contains the actual values:

```text
0.000000E+00  0.000000E+00  0.665918E-01
0.780685E-02
```

but contains no potential-uptake values anywhere in the `>orgpla:` restart representation.

Thus a scientifically used, naturally nonzero persistent state reaches the restart writer and has no serialized representation.

### Classification

`CONFIRMED_LEGACY_PLANT_POTENTIAL_UPTAKE_RESTART_STATE_OMISSION`

A split-run behavioural magnitude is still unmeasured and must not be guessed. Historical-reference qualification remains blocked by PREP02.

## 4. Interaction between TCD-033 and TCD-034

The two defects compound but must remain separate:

- TCD-033 loses a restart field that **is present** in the file because initialization copies in the wrong direction;
- TCD-034 omits a scientifically active state from the restart file entirely.

Correcting only one does not establish restart continuity.

## 5. ANIMO5 requirement

Every persistent scientific state must have a tested round-trip lifecycle:

```text
serialized state -> accepted state -> trial/result state -> commit -> serialized state
```

Tests must use nonzero state values and must exercise both continuous and split-run trajectories. State fields that influence subsequent demand or process rates cannot be reconstructed as zero unless that reset is an explicit, scientifically qualified transaction boundary.

Production migration remains `NOT_ADMITTED`.
