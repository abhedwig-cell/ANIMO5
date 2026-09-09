# ANIMO-BUILDQ03 — GHG explicit task and solver context qualification

Status: `QUALIFIED_GHG_HIDDEN_TASK_CONTEXT_OWNERSHIP_AND_CONTROLLED_EQUIVALENCE_FLAIR_BOTTOM_BOUNDARY_RUNTIME_HAZARD_SEPARATE_HISTORICAL_INTEL_OPEN`

## Scope and authority

BUILDQ03 continues canonical `TCD-011` storage-duration qualification for active GHG routines. It does not reopen GHG science discrepancies `TCD-032` through `TCD-037` and does not allocate a new TCD.

Authority used:

- BUILDQ03 base: `work/animo-buildq02-tcd011-storage-runtime-qualification@e7c675c6654026d5c12836f36f2fd347e9d547c2`;
- B3 routing authority originally consumed: `work/animo-b3i01-canonical-register-append@d2fe4eb3793a1ffc6c09197d7db01c3e3fe33f88`;
- latest B3I01 head checked during closeout: `8e3ce76a3b842814d3f1e3bbebdcbf84e77768f3`;
- GHG source audit: `work/animo-ghg01-ghg-qualification@dac7b7b5c591b781b82ec968896edb5957664c88`;
- frozen source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- diagnostic compiler GNU Fortran 14.2.0.

Canonical disposition remains:

`GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE -> TCD-011`

All results below are B1 diagnostic qualification. Historical Intel storage behaviour remains unknown.

## 1. GHGponding: exact scoped restore snapshot

`GHGponding` Task 1 stores the original ponding representation in unsaved locals `He0`, `Mofr0`, `Mofro0`, `Mofrsa0` and `Mofrt0`, then mutates the caller-visible layer-0 hydrological representation. Later Task 2 and Task 3 calls restore from those hidden locals.

A controlled case used nontrivial initial values and executed Task 1 followed by stack clobbering and Task 2, then repeated Task 1 followed by clobbering and Task 3.

Observed GNU behaviour:

- original source with static locals at O0 and O2 restores exactly;
- original source with automatic locals and signalling-NaN initialization restores NaNs;
- an explicit-snapshot diagnostic variant under automatic locals at O0 and O2 is byte-identical to original static execution.

Reference output SHA-256:

`b7284678e9658b48ac6f77d8aeb71639350c4c43db810741525acd94baa1afef`

Qualified owner:

`SCOPED_GHG_PONDING_PHASE_SNAPSHOT`

This is not accepted persistent physical state. It is a pre-transform transaction snapshot and cannot be reconstructed after the original caller-visible values have been overwritten.

## 2. CH4 oxidation: explicit nonlinear solver context

`CH4oxid` uses hidden state across Task 1, repeated Task 2 and Task 3 calls:

- `Nlox`;
- `AmO2`;
- `AvCoCH4Old`;
- `OxDmndOmNit`;
- `R0CH4oxAct`.

Original automatic-storage behaviour is not stable. The controlled O0 probe terminated with `SIGSEGV`; the O2 probe returned a false convergence path and skipped the intended nonlinear update. Original static O0/O2 execution produced the intended continuation.

An explicit-context diagnostic variant under automatic storage at O0 and O2 reproduces the complete static Task-1-to-Task-3 output byte-identically.

Reference output SHA-256:

`c01bba7b40652cbd38e1c3199a0e244db0f70cce6f08a0771c8741a18974e54c`

Qualified owner:

`CH4_NONLINEAR_SOLVER_CONTEXT`

This is solver state, not accepted persistent physical state. Context minimization is not claimed by BUILDQ03.

## 3. N2O production/reduction: explicit coupled solver and correction context

`N2Oproreduc` retains `AvCoN2Oold`, `AvCoNO3`, `FrDenAct_Pot`, `RatFacN2O`, `RekiNO3` and `FlInit`. Nested `NO3N2OReduc` retains `FlExcd` and `QPrN2OdenMax`.

Original automatic-storage execution diverges from original static execution: the controlled case can report false convergence during Task 2 and propagate NaN into Task-3 nitrate and oxygen-deficit state.

An explicit-context diagnostic variant threads both top-level and nested correction context through the call sequence and reproduces original static O0/O2 output byte-identically under automatic storage.

Reference output SHA-256:

`ffb0c1fb1f7471ac9d50d214717ce1bcc520fdf2fbb5e91e223d3a5ec52f88b4`

Qualified owner:

`N2O_NONLINEAR_SOLVER_AND_CORRECTION_CONTEXT`

This is coupled solver and correction history, not accepted persistent physical state.

## 4. GHGtransport: branch and representation snapshot context

`GHGtransport` retains three unsaved locals between Task 1 and Task 2:

- `Ln1`;
- `FlTopUns`;
- `Co1Old`.

`Ln1` is directly derivable from `Flpn`, while `FlTopUns` records the Task-1 branch and `Co1Old` is a pre-iteration concentration representation snapshot used later during restoration.

A controlled diagnostic separates these three values from compiler-local lifetime. Under automatic storage, captured Task-2 average and end gas state becomes invalid in the affected probe. Threading the three values through explicit context reproduces the retained/static protocol byte-identically.

Reference output SHA-256:

`5ead8015d31cfe0ae58a8a9d3fecb49f5059c31c674c9af2824c0d131f709afc`

Diagnostic explicit-context source SHA-256:

`63575307aa170187b68b3e20d116c535b02a5d4984c2f88195ad531a5e078f12`

Qualified owner:

`GAS_TRANSPORT_BRANCH_AND_REPRESENTATION_SNAPSHOT_CONTEXT`

Persistent `ModelState` candidate: `false`.

The combined fixed-form diagnostic required syntax-preserving GNU source-format normalization. This is a diagnostic build boundary, not a source correction.

## 5. GHGtranssub: fixed timestep coefficient context

`GHGtranssub` computes fixed Task-1 coefficient/help state and reuses it while reaction coefficients change during Task 2. Qualified members include:

- `P1`, `P2`;
- `Y1`, `Y2`, `Y3`;
- `Hv`, `Hv2`, `Hvnil`;
- `AlfBuAv1` for the exercised branch.

Original automatic-storage execution yields invalid Task-2 average and end concentrations in the controlled probe. An explicit coefficient-context diagnostic reproduces original static O0/O2 output byte-identically under automatic storage.

Reference output SHA-256:

`54bb8578d13d1f65ee156c2bb6aa7ec105656d8528178f38a867849d2dbb3e8b`

Diagnostic explicit-context source SHA-256:

`6adb9df1eee8729a476b18b620074d40aea44648bb404a8d1109411daeb92ae8`

Qualified owner:

`FIXED_TIMESTEP_TRANSPORT_COEFFICIENT_CONTEXT`

Persistent `ModelState` candidate: `false`.

BUILDQ03 does not claim that every coefficient may safely be recomputed during Task 2. The qualified surface is explicit retained timestep context.

## 6. GHGasses: explicit phase context

`GHGasses` Task 1 prepares hidden hydrology and air-flow projections that a later separate Task-2 invocation consumes for final N2O calculations.

The cross-call hidden context was narrowed to:

- `Floux`;
- `Mofrx`;
- `Mofrsax`;
- `Flaiib`;
- `Flaiio`;
- `Flaiou`;
- `FlaiAtmos`.

`Mofrox` and `Mofrtx` are formal arguments and are not hidden state. `Flair` is a Task-1 helper and is not itself required across the Task-1-to-Task-2 return boundary.

A controlled 16-case phase-projection matrix compares retained/static execution, automatic-local execution and a diagnostic explicit phase-context variant. With the independent bottom-boundary initialization seam controlled separately, explicit phase context reproduces the retained/static reference output exactly. Original automatic-storage execution loses the required Task-2 projection state.

Reference output SHA-256:

`c4f47a3e09b6087a37d7351dcea62aa103a4e2421e1a018693eba8d9edbfcc55`

Original automatic output SHA-256:

`411f2ee264dbdb4c3f5bd80eed58e17f131f610512bb57d7545113335febdc46`

Diagnostic explicit-context source SHA-256:

`2439d63bfe2dc9753dff7d302f7434117265609512ffc4832c59e08646eab9b2`

Qualified owner:

`GHG_TIMESTEP_PHASE_CONTEXT`

Persistent `ModelState` candidate: `false`.

BUILDQ03 qualifies explicit threading of the retained projection. It does not qualify Task-2 recomputation from nominally similar inputs because intervening input invariance has not been proven strongly enough.

## 7. Separate GHGasses bottom-boundary initialization hazard

The GHGasses phase-context probe exposed a separate source/runtime finding:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

When `La < Nl`, `Flair(Nl+1)` can be read by the bottom-layer `Flaiio`/`Flaiou` transformation without a source assignment to that slot. Those flow terms feed `GHGtransport` and `GHGtranssub`, including air-flow-dependent `Y2` and `Y3` coefficients.

Controlled GNU behaviour is optimization-sensitive. In the explicit-context projection probe, automatic O0 produced NaN in the bottom-layer air-flow terms while O2 happened to match the retained/static output. This is evidence of a conditional uninitialized-local boundary slot, not of an intended zero boundary condition.

For the phase-context equivalence matrix, `Flair(Nl+1)=0.0` was used only as a diagnostic control to isolate this independent seam. That diagnostic value is not admitted as scientific semantics or as a production correction.

Current disposition requested from B3 governance:

`RUNTIME_INITIALIZATION_HAZARD_PENDING_INTAKE_NO_NEW_TCD_REQUESTED_BY_BUILDQ03`

Historical Intel effect: `UNKNOWN`.

## Ownership result across the active GHG hidden-local surface

All six active GHG hidden-local families audited by BUILDQ03 now have a qualified explicit semantic owner and controlled equivalence surface:

| Routine/family | Qualified owner | Persistent ModelState |
| --- | --- | --- |
| `GHGponding` | scoped ponding phase snapshot | no |
| `CH4oxid` | CH4 nonlinear solver context | no |
| `N2Oproreduc` + `NO3N2OReduc` | N2O solver and correction context | no |
| `GHGtransport` | gas-transport branch and representation snapshot | no |
| `GHGtranssub` | fixed timestep transport coefficient context | no |
| `GHGasses` | GHG timestep phase context | no |

This directly rejects a migration design that turns hidden locals wholesale into checkpointed physical state. It also rejects blanket `SAVE`, `/Qsave` or compiler-static lifetime as the ANIMO5 state architecture.

## Qualification boundary

BUILDQ03 qualifies how the active GHG cross-call local state must be owned in an explicit implementation. It does not establish historical Intel numerical equivalence and does not close canonical `TCD-011` because other storage-duration families and the historical build contract remain open.

The newly isolated `Flair(Nl+1)` finding is not silently repaired by the explicit-context design. It must be routed independently as an initialization/runtime hazard before any production migration of the affected GHG air-flow seam.

## Current gate

`QUALIFIED_GHG_HIDDEN_TASK_CONTEXT_OWNERSHIP_AND_CONTROLLED_EQUIVALENCE_FLAIR_BOTTOM_BOUNDARY_RUNTIME_HAZARD_SEPARATE_HISTORICAL_INTEL_OPEN`

`qualified_active_hidden_families=6`

`open_active_hidden_families=0`

`historical_intel_equivalence_qualified=false`

`tcd011_closed=false`

`new_canonical_tcd_requested=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
