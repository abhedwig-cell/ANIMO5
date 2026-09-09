# ANIMO-GHG01 - GHG task-state persistence and build-contract audit

Status: `SOURCE_CONFIRMED_BUILD_CONTRACT_DEPENDENT_HIDDEN_SCIENTIFIC_STATE_ACROSS_ACTIVE_GHG_TASK_CALLS`

This post-closeout audit identifies task-style GHG routines that write local variables during one invocation and require those values during a later invocation without passing them through arguments or declaring them `SAVE`. The finding is source-bound. It does not establish the numerical values produced by the historical Intel executable and does not authorize a blanket `SAVE` or `/Qsave` correction.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant frozen source-file SHA-256:

- `Animo.for`: `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`
- `ghgasses.for`: `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`
- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`
- `ghg_n2o.for`: `493bf88d4b321df64817a7c0eaa2725ad614a45df0a0f16cefa96ac348254175`
- `ghgtransport.for`: `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`
- `ghgtranssub.for`: `48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c`

Umbrella local reconciliation key:

`GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE`

Classification:

`SOURCE_CONFIRMED_BUILD_CONTRACT_DEPENDENT_HIDDEN_SCIENTIFIC_STATE_ACROSS_ACTIVE_GHG_TASK_CALLS`

## 1. Why this is distinct from the earlier build-contract finding

PREP01 `TCD-011` established that `Outbal_write` reuses local CHARACTER format state across `Itask` calls without explicit `SAVE`. The historical Intel build-contract reconstruction correctly keeps the actual storage policy unresolved and notes that Intel default storage can plausibly preserve CHARACTER locals without requiring `/Qsave`.

The GHG finding is materially broader. The same task-style pattern occurs inside source-reachable scientific calculations and temporary physical-state transformations. It affects CH4 oxidation, N2O production/reduction iteration, shared gas transport, air-flow coupling and restoration of the ponding-layer hydrological state.

Therefore this audit does not silently absorb the GHG finding into `TCD-011`. B3 governance must decide whether `TCD-011` should be broadened or whether the GHG scientific-state dependency warrants a distinct canonical discrepancy.

## 2. Top-level execution proves separate invocations

Revision-53 `Animo.for` calls `GHGasses(1,...)` after aeration and before definitive nitrate transport. Later, after nitrate transport and correction, it separately calls `GHGasses(2,...)` for final N2O calculations.

Inside those calls, several routines use `Goto (...) Itask` and return after each task. Their task-1 and task-2/task-3 sections therefore execute in separate procedure invocations, not as one continuous activation record.

No explicit `SAVE` statement was found in the audited GHG task routines for the hidden state listed below. Variables initialized by `DATA` are not included in this finding when their persistence is explicitly supplied by the language construct.

## 3. `GHGponding`: hidden scalar restore state

`ghgasses.for::GHGponding` temporarily rewrites the ponding-layer physical state for GHG diffusion calculations.

Task 1 stores the original values only in local scalar variables:

- `He0`
- `Mofr0`
- `Mofro0`
- `Mofrt0`
- `Mofrsa0`

It then changes the caller-visible `He(0)`, `Mofr(0)`, `Mofro(0)`, `Mofrt(0)` and `Mofrsa(0)`.

Task 2 and task 3 are later separate calls. They restore the caller-visible hydrological state from those same local scalars. The original values are not arguments and have no explicit `SAVE`.

This is a direct hidden-state dependency on scalar REAL persistence. If the values do not persist, the GHG routine cannot source-semantically guarantee restoration of the hydrological state it temporarily modified.

Subfinding:

`GHG01-LCL-GHGPONDING-HIDDEN-RESTORE-STATE`

Classification:

`SOURCE_CONFIRMED_UNSAVED_CROSS_CALL_HYDROLOGICAL_RESTORE_STATE`

## 4. `GHGasses`: hidden state between the two main GHG phases

Task 1 of `GHGasses` constructs temporary hydrological and air-flow state, including local arrays:

- `Floux`
- `Mofrx`
- `Mofrsax`
- `Flaiib`
- `Flaiio`
- `Flaiou`
- `Flair`

and local scalar `FlaiAtmos`.

These values are used for the initial CH4 and N2O calculations. The routine returns. After definitive nitrate transport, `Animo.for` invokes `GHGasses(2,...)` separately. Task 2 does not reconstruct the temporary hydrological/air-flow state; it directly passes the prior local `Floux`, `Mofrx`, `Mofrsax`, `Flaiib`, `Flaiio`, `Flaiou` and `FlaiAtmos` into final `GHG_NitrousOxide`.

`Mofrox` and `Mofrtx` are caller-visible arguments and are not part of this hidden-state claim. The listed local arrays and scalar are.

Subfinding:

`GHG01-LCL-GHGASSES-HIDDEN-PHASE-STATE`

Classification:

`SOURCE_CONFIRMED_UNSAVED_CROSS_CALL_GHG_PHASE_COUPLING_STATE`

Impact: final N2O production/transport is build-storage dependent unless this local state persists as the source assumes.

## 5. `CH4oxid`: hidden nonlinear oxidation iteration state

`ghg_ch4.for::CH4oxid` is called successively with `Itask=1`, repeated `Itask=2`, and finally `Itask=3`.

Task 1 calculates local state including:

- scalar `Nlox`, the deepest compartment relevant for oxidation;
- `AmO2(0:Manl)`;
- `AvCoCH4Old(0:Manl)`;
- `OxDmndOmNit(0:Manl)`;
- `R0CH4oxAct(0:Manl)`.

Task 2 returns to these values for convergence and recalculation of `RekiCH4`. Task 3 again uses `Nlox`, `AmO2` and `OxDmndOmNit` to calculate final CH4 oxidation and adjust the oxygen-deficit factors.

These quantities are not passed as arguments and have no explicit `SAVE`.

Subfinding:

`GHG01-LCL-CH4-OXIDATION-HIDDEN-TASK-STATE`

Classification:

`SOURCE_CONFIRMED_UNSAVED_CROSS_CALL_HIDDEN_STATE_IN_ACTIVE_CH4_OXIDATION_ITERATION`

This is scientific process state, not merely formatting or reporting state.

## 6. `N2Oproreduc` and `NO3N2OReduc`: hidden N2O iteration/correction state

`ghg_n2o.for::N2Oproreduc` is called with task 1, then repeatedly with task 2, and finally with task 3. Task 1 calculates local arrays that later tasks consume, including:

- `AvCoN2Oold`
- `AvCoNO3`
- `FrDenAct_Pot`
- `RatFacN2O`
- `RekiNO3`
- `FlInit`

Task 2 uses these arrays to iterate N2O production/reduction. Task 3 uses `AvCoNO3`, `FrDenAct_Pot` and `RekiNO3` to reset the nitrate/oxygen-deficit state or finalize N2O reduction. They are not explicit arguments of `N2Oproreduc` and are not explicitly saved.

The nested routine `NO3N2OReduc` has its own cross-call hidden arrays:

- `FlExcd(Manl)`
- `QPrN2OdenMax(Manl)`

They are initialized when `FlInit` is true and consulted in later calls when `FlInit` is false to decide and bound correction behavior.

Subfindings:

`GHG01-LCL-N2O-PROREDUC-HIDDEN-TASK-STATE`

`GHG01-LCL-NO3N2OREDUC-HIDDEN-CORRECTION-STATE`

Classification:

`SOURCE_CONFIRMED_UNSAVED_CROSS_CALL_HIDDEN_STATE_IN_ACTIVE_N2O_ITERATION_AND_CORRECTION`

## 7. `GHGtransport`: hidden scalar transport branch state

Shared `GHGtransport` is used by both CH4 and N2O. Task 1 computes local scalar state including:

- `Ln1`, the top active compartment;
- `FlTopUns`, whether the top soil layer is unsaturated and the CTE is air-based there;
- `Co1Old`, the original top-layer concentration when `FlTopUns` is true.

Task 2 is invoked separately during CH4 and N2O nonlinear iterations. It immediately uses `FlTopUns` and `Ln1`, passes them to `GHGtranssub`, and later uses `Co1Old` to restore the concentration representation.

`DfcfAv` and `HeAv` appear under a misleading local-variable comment but are in the formal argument list, so they are caller-visible state and are explicitly excluded from this hidden-state claim.

Subfinding:

`GHG01-LCL-GHGTRANSPORT-HIDDEN-TASK-STATE`

Classification:

`SOURCE_CONFIRMED_UNSAVED_CROSS_CALL_SCALAR_STATE_IN_SHARED_GHG_TRANSPORT`

This subfinding is especially relevant to the candidate Intel default storage hypothesis because `Ln1` is INTEGER, `FlTopUns` is LOGICAL and `Co1Old` is REAL scalar state.

## 8. `GHGtranssub`: hidden CTE coefficient state

`GHGtranssub` receives the task index from `GHGtransport`. Task 1 calculates local coefficient/help arrays that depend on hydrology, Bunsen partitioning, diffusion and flow. Task 2 reuses them while `Reki` and `Reko` change during nonlinear GHG iteration.

Examples of local task-1 state reused by task 2 are:

- `P1`, `P2`
- `Y1`, `Y2`, `Y3`
- `Hv`, `Hv2`, `Hvnil`
- `AlfBu01`, `AlfBuAv1`, `AlfBuAv2` for the unsaturated-top branch.

These are not dummy arguments and have no explicit `SAVE`.

Subfinding:

`GHG01-LCL-GHGTRANSSUB-HIDDEN-CTE-STATE`

Classification:

`SOURCE_CONFIRMED_UNSAVED_CROSS_CALL_HIDDEN_CTE_COEFFICIENT_STATE`

## 9. Build-contract reconciliation

PREP01 reconstructed the leading historical Intel hypothesis as Intel Visual Fortran Composer XE 12.1.0.233 with eight-byte default REAL and PowerStation-compatible I/O, while local storage remained incompletely proven.

The same PREP01 record notes Intel default `/Qauto-scalar` semantics: non-SAVEd scalar INTEGER, REAL, COMPLEX and LOGICAL variables are stack allocated, whereas its prior `Outbal_write` explanation concerned CHARACTER state.

The GHG inventory therefore changes the importance of the unresolved storage contract:

- several hidden GHG arrays may plausibly have static storage under Intel defaults, but that remains build-contract behavior rather than explicit model state;
- `GHGponding` restore values are scalar REALs;
- `GHGasses` includes scalar REAL `FlaiAtmos`;
- `GHGtransport` depends on scalar INTEGER `Ln1`, LOGICAL `FlTopUns` and REAL `Co1Old`.

Thus the earlier CHARACTER-specific Intel-default explanation is not sufficient to establish the active GHG task-state contract.

No inference is made that the historical executable necessarily failed. Stack reuse, optimization, project switches such as `/Qsave`, or neighboring source/build artifacts could make historical execution appear stable. Those possibilities are precisely why the historical numerical effect remains reference-blocked.

## 10. Controlled storage-sensitivity diagnostic

A minimal diagnostic copied the frozen `GHGponding` task logic exactly and called task 1 followed by task 2 with a nontrivial ponding state. This is a synthetic B1 storage-sensitivity probe, not B0 source evidence and not B2 historical reference.

Compiler:

`GNU Fortran 14.2.0`

Initial state:

`He=0.02, Mofr=0.5, Mofro=0.4, Mofrsa=0.7, Mofrt=0.6`

With automatic local storage and explicit NaN initialization:

`-O0 -fautomatic -finit-real=snan`

Task 1 produced the expected temporary GHG ponding state. Task 2 then restored all five caller-visible quantities to `NaN`, because the second invocation did not possess the task-1 local restore values.

With static local storage:

`-O0 -fno-automatic -finit-real=snan`

Task 2 restored the exact initial values.

Probe source SHA-256:

`26bcac0b2ddb621af9c82e83b43d944e58b2e8c04068a7026ad22d95bccd3f32`

Classification:

`B1_SYNTHETIC_STORAGE_SENSITIVITY_CAUSAL_CONFIRMATION_NOT_REFERENCE`

This diagnostic establishes that local-storage policy is causally capable of changing physical state restoration. It does not identify the historical Intel result.

## 11. ANIMO5 architectural consequence

Task progression must not be represented through implicit procedure-local persistence in a migrated GHG subsystem.

A qualified ANIMO5 design must make persistent scientific state explicit. At minimum:

- ponding temporary-state save/restore must be transaction-owned;
- GHG phase-1 to phase-2 hydrology and air-flow coupling must be explicit state or recomputed from accepted inputs;
- CH4 oxidation iteration state must be explicit trial-solver state;
- N2O production/reduction iteration and correction state must be explicit trial-solver state;
- shared transport branch state and CTE coefficients must be explicit trial state or deterministic recomputation;
- rollback/restart semantics must distinguish persistent physical state from within-step solver scratch state.

This aligns with ARCH01/ARCH02/TS01 principles but does not itself modify those workunits.

## 12. Qualification consequence

The GHG subsystem is more build-contract dependent than the prior output-formatting evidence alone showed. Source reachability is not sufficient for behavioral qualification because active GHG scientific calculations require hidden cross-invocation local state that the source does not explicitly own.

Required closure before GHG B3 admission:

1. include this hidden-state inventory in historical Intel build-contract qualification;
2. obtain a revision-53-compatible activated GHG case;
3. compare Intel-default, any historically evidenced storage policy, and explicit-state diagnostic variants without promoting diagnostics to B2;
4. verify repeated deterministic CH4/N2O results and exact ponding-state restoration;
5. reconstruct CH4/N2O conservation from explicit state and transfers;
6. only then decide whether the canonical discrepancy is a broadened build-contract TCD or one or more GHG-specific TCDs.

Historical runtime magnitude: `REFERENCE_BLOCKED`.

B3 admission: `NOT_ADMITTED`.

Production migration: `NOT_ADMITTED`.
