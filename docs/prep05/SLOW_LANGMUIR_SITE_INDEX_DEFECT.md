# ANIMO-PREP05 — Slow-Langmuir site-index defect

Status: `SOURCE_BOUND_CAUSAL_DEFECT_CONFIRMED_REFERENCE_ADMISSION_BLOCKED`.

This workunit records a distinct defect in the revision-53 phosphorus slow-sorption path. It is separate from TCD-019, which concerns fast-sorption finite-change linearization and nonlinear convergence policy.

The frozen source archive and supplied testcases remain unchanged. All source changes described below were made only in temporary diagnostic execution copies.

## 1. Source finding

In `Transorp.for`, subroutine `Conc_unl`, the outer trial loop is:

```fortran
Do 1030 I=1,20
```

After an acceptable transport trial, the routine loops over slow-sorption sites:

```fortran
Do 1050 J=1,Ncxsl
```

Inside that site loop, the equilibrium amount, adsorption/desorption rate and updated site amount are all indexed by `J`, but the Langmuir kinetic exponent uses:

```fortran
If(Optcxsl .Eq. 2)Then
   Yy = One + Parcxsl(3,I) * Avc
   Yy = exp( - Recf(J) * Yy * T )
End If
```

`I` is not a sorption-site index here. It is the trial counter. The site index is `J`.

The source-wide surrounding Langmuir implementation consistently uses the site-specific affinity as `Parcxsl(3,site)`. The corresponding expression in this loop is therefore structurally inconsistent with its own data model.

`Parcxsl` has `Macx=3` site columns while `I` may range from 1 through 20. The expression therefore also creates a latent out-of-bounds path if the accepted trial reaches `I > 3`.

## 2. Supplied-testbank coverage gap

All six supplied cases with active phosphorus use:

```text
OPTCXSL = 3
```

for Freundlich slow sorption. None exercises `OPTCXSL=2` slow Langmuir.

The defect is therefore not discoverable from ordinary supplied-testbank coverage alone.

## 3. Synthetic path probe

A controlled synthetic path probe was derived from the already executable LWKM diagnostic case. Only the slow-sorption option and its site parameters were changed in the temporary testcase copy:

```text
OPTCXSL = 2
NCXSL   = 3
```

with deliberately different Langmuir affinity parameters for the three sites:

```text
site 1: Parcxsl(3,1) =  500
site 2: Parcxsl(3,2) = 1000
site 3: Parcxsl(3,3) = 2000
```

The synthetic baseline completed successfully under a GNU diagnostic build with bounds checking on `Transorp`.

A second build changed exactly one source expression in the temporary source copy:

```text
Parcxsl(3,I) -> Parcxsl(3,J)
```

No other source, forcing, hydrology, initial state or testcase field was changed.

The corrected synthetic run also completed successfully.

## 4. Causal output result

Both executions produced the same 55-output file set. After normalization of only the already-declared volatile run timestamps and CPU time:

```text
files compared: 55
normalized equal: 44
changed: 11
missing: 0
extra: 0
```

The changed set is concentrated in phosphorus-related state/balance/reporting surfaces plus outputs carrying those P quantities:

- `PClassYearSwitch.out`;
- `ani_pGP.Bal`;
- `ani_pRP.Bal`;
- `ani_pTP.Bal`;
- `bappGP.Out`;
- `bappRP.Out`;
- `bappTP.Out`;
- `discharge.out`;
- `initial.out`;
- `pal-P.out`;
- `pw-P.out`.

`message.out` and `animointermediate.Out` remain normalized-identical, as do the inspected ordinary N/OM output and balance families.

The phosphorus balance impact is large.

### Groundwater-profile balance

```text
legacy-index final cumulative Bapp deviation:  -158 kg/ha P
site-index correction:                          -0.432 kg/ha P
largest annual deviation: -6.92 -> -0.0244 kg/ha P
```

### Total-profile balance

```text
legacy-index final cumulative Bapp deviation:  -329 kg/ha P
site-index correction:                          -0.726 kg/ha P
largest annual deviation: -15.1 -> -0.0457 kg/ha P
```

### Root-profile balance

```text
legacy-index final cumulative Bapp deviation:  -54.4 kg/ha P
site-index correction:                         -0.254 kg/ha P
largest annual deviation: about -2.53 -> -0.0152 kg/ha P
```

The single index correction therefore removes more than 99.5% of the synthetic cumulative P nonclosure in all three balance scopes.

The remaining sub-kg/ha drift is not interpreted as validation of the corrected route. TCD-019 has already established an independent numerical-conservation seam in the nonlinear P sorption solver and remains active in this synthetic test.

## 5. Classification

`CONFIRMED_LEGACY_WRONG_INDEX_DEFECT_AND_LATENT_BOUNDS_RISK`

This classification is stronger than a static source suspicion because:

1. the index is inconsistent with the surrounding site-indexed algorithm;
2. the supplied array dimension and loop bounds prove a latent bounds risk;
3. an `OPTCXSL=2` synthetic execution reaches the affected branch;
4. changing only `I` to `J` produces large, directionally coherent P-state and balance changes;
5. the correction sharply improves P mass closure without changing unrelated N/OM output families in the observed diagnostic scope.

It is not yet a qualified corrected-legacy fix because no historical native reference exists for the slow-Langmuir path and no supplied testcase covers it.

## 6. Corrected-legacy class

Proposed class:

`B_LOCAL_ALGEBRAIC_INDEX_CORRECTION_WITH_STATE_TRAJECTORY_CHANGE`

Expected properties:

```text
physics_model_changed = false
parameter_binding_corrected = true
state_trajectory_changes = true
mass_conservation_improves = true
reference_qualification_required = true
```

The correction is not accounting-only.

## 7. Qualification requirements

Before corrected-legacy admission:

1. obtain or reconstruct a qualified frozen reference environment;
2. create a dedicated `OPTCXSL=2` qualification case with at least two unequal slow-Langmuir affinity parameters;
3. capture unrounded slow-sorption site states and P ledger terms;
4. prove site `J` receives its own `Parcxsl(3,J)` parameter throughout every analytical and iterative branch;
5. run with bounds checking or equivalent index diagnostics;
6. compose the correction separately with TCD-019 because both affect phosphorus trajectories;
7. verify linear (`OPTCXSL=1`) and Freundlich (`OPTCXSL=3`) routes remain unchanged;
8. only then admit the correction to a corrected-legacy lineage.

## 8. Architectural consequence for ANIMO5

Constitutive parameter arrays must not be accessed through unrelated solver-iteration counters. ANIMO5 should use typed/site-local structures or explicit site objects so that a trial index and a sorption-site index cannot be silently interchanged.

Dedicated path coverage is required for every supported constitutive option even when the historical production testbank exercises only one option.

Production migration remains `NOT_ADMITTED`.
