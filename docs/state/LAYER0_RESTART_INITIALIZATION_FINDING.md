# ANIMO-STATEQ01 local finding: layer-0 restart initialization zeroing

Status: `SOURCE_CONFIRMED_NATURALLY_REACHABLE_LOCAL_FINDING_PENDING_B3_INTAKE`

Frozen source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Provisional reconciliation key:

`RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`

Canonical TCD allocation: `NONE`

## 1. Finding

Revision 53 reads layer-0 dissolved state from `INITIAL.INP`, writes layer-0 dissolved result state to `INITIAL.OUT`, but then unconditionally erases several read layer-0 coordinates during initial calculations before the first timestep.

This is a restart/initialization continuity finding. It is distinct from TCD-016, which concerns runtime wet-to-low-storage NH4 continuation and the absence of a scientifically admitted non-aqueous owner.

## 2. Reader surface

`input1.for:3197-3218` reads:

```fortran
Conhtop,(Conh(Ln),Ln=0,Nl)
Conitop,(Coni(Ln),Ln=0,Nl)
```

`input1.for:3263-3287` similarly reads layer-0 labile DOM and DON. The P initialization block reads layer-0 P state as well.

Thus index 0 is part of the explicit restart/input representation.

## 3. Initial calculation zeroing

Immediately after `Input1`, the main program calls `Inicalc` before the simulation loop.

`Inicalc.for:125-129` executes unconditionally:

```fortran
Conh(0)=0.0
Coni(0)=0.0
Codiorma(0)=0.0
Codiorni(0)=0.0
Codiorpo(0)=0.0
```

No preceding preservation assignment copies the values read from `INITIAL.INP` into another accepted owner.

On the first ordinary `Init`, `Init.for:227-245` zeroes the corresponding result arrays rather than restoring those input values.

The dataflow therefore has no continuation path for nonzero restart values of these layer-0 families.

## 4. Writer surface

`Output_Init.for:82-105` writes `Rsconh(0)`, `Rsconi(0)`, `Rscodiorma(0)` and `Rscodiorni(0)` as part of the standard restart-style output. `Output_Init.for:122-134` writes layer-0 P/DOP state when P is active.

The existence of a writer and reader therefore does not imply round-trip continuity.

## 5. Natural supplied-case reachability

The supplied `GrassPeat` case uses `Input/INITIAL.INP` directly through its `animo.ini` binding.

Its unmodified input contains nonzero layer-0 values:

```text
Conh(0)      = 6.885736E-03 kg N m-3 water
Coni(0)      = 5.743774E-04 kg N m-3 water
Codiorma(0)  = 9.904185E-02 kg OM m-3 water
Codiorni(0)  = 5.673512E-03 kg N m-3 water
Copo(0)      = 3.703004E-03 kg P m-3 water
```

The first four listed values are among the coordinates unconditionally zeroed by `Inicalc`. `Copo(0)` is not covered by the same unconditional zeroing statement and must remain governed separately.

This establishes natural testbank reachability of the zeroing path without editing testcase bytes.

The supplied GHG case also contains nonzero layer-0 NH4, but its known source/testcase lineage mismatch means it is not used to strengthen this finding.

## 6. Classification boundary

Current classification:

`SOURCE_CONFIRMED_NATURALLY_REACHABLE_LAYER0_DISSOLVED_RESTART_INITIALIZATION_ZEROING`

What is proven:

- nonzero layer-0 NH4/NO3/labile DOM/DON are valid reader inputs in a supplied case;
- `Inicalc` then sets those coordinates to zero before the first timestep;
- no state handoff preserving them is visible in the source path audited;
- restart-style output serializes the corresponding result-state coordinates.

What is not yet claimed:

- a canonical TCD number;
- historical-reference behavioural magnitude;
- an accepted correction;
- that all species share one scientific defect mechanism;
- that this finding subsumes TCD-016.

## 7. Governance routing

Route this candidate to ANIMO B3 intake as:

`RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`

B3 governance must decide whether it is:

- a new canonical discrepancy;
- part of an existing restart-state discrepancy family;
- species-split into multiple discrepancies;
- or otherwise reconciled.

STATEQ01 must not allocate the canonical identity itself.

## 8. State-admission consequence

General `CORE_CNP` is blocked independently by:

1. TCD-016-C1, the unresolved runtime low-storage NH4 continuation science;
2. this local restart initialization zeroing finding for explicitly represented layer-0 dissolved state.

`CORE_CNP_SUBSURFACE_ONLY` can avoid the second finding only if its admitted envelope requires zero layer-0 restart state and zero surface storage at every accepted/candidate boundary. The guard must fail closed rather than silently zeroing a nonzero input.

Production migration remains `NOT_ADMITTED`.
