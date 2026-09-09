# ANIMO-BUILDQ03 — GHG explicit task and solver context qualification

Status: `PARTIAL_RUNTIME_QUALIFICATION_PERSISTED_TRANSPORT_CONTEXT_STILL_OPEN`

## Scope and authority

BUILDQ03 continues the canonical `TCD-011` storage-duration qualification for active GHG routines. It does not reopen GHG science discrepancies `TCD-032` through `TCD-037` and does not allocate a new TCD.

Authority used:

- BUILDQ03 base: `work/animo-buildq02-tcd011-storage-runtime-qualification@e7c675c6654026d5c12836f36f2fd347e9d547c2`;
- B3 routing: `work/animo-b3i01-canonical-register-append@d2fe4eb3793a1ffc6c09197d7db01c3e3fe33f88`;
- GHG source audit: `work/animo-ghg01-ghg-qualification@dac7b7b5c591b781b82ec968896edb5957664c88`;
- frozen source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- diagnostic compiler GNU Fortran 14.2.0.

The B3 disposition remains:

`GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE -> TCD-011`

This document records B1 diagnostic qualification only. Historical Intel storage behaviour remains unknown.

## 1. GHGponding: exact scoped restore snapshot

`GHGponding` Task 1 stores the original ponding representation in unsaved locals:

- `He0`;
- `Mofr0`;
- `Mofro0`;
- `Mofrsa0`;
- `Mofrt0`.

Task 1 then mutates the caller-visible layer-0 hydrological representation. Tasks 2 and 3 later restore from the hidden locals.

Exact frozen routine SHA-256:

`5de27ef4688f4a4d21a534c931d2d437aafbcba3df22f9e2114f7902e4c979ca`

A controlled case used nontrivial initial values `He=0.25`, `Mofr=0.4`, `Mofro=0.3`, `Mofrsa=0.5`, `Mofrt=0.35` and executed Task 1 followed by stack clobbering and Task 2, then repeated Task 1 followed by clobbering and Task 3.

Observed GNU behaviour:

- original source, static locals, O0 and O2: exact restoration;
- original source, automatic locals plus signalling-NaN initialization, O0 and O2: all five restored values become NaN;
- diagnostic explicit-snapshot variant, automatic locals, O0 and O2: exact byte-identical output to original static execution.

The original-static and explicit-context outputs all have SHA-256:

`b7284678e9658b48ac6f77d8aeb71639350c4c43db810741525acd94baa1afef`

The diagnostic explicit-context source SHA-256 is:

`9f733396dd96e17e1bb7caa748d65012af8a0abd1b34525b3a354f4dbb9c28bd`

### Semantic decision

This state is not accepted persistent physical state. It is an exact pre-transform snapshot owned by the GHG ponding transaction. It cannot safely be reconstructed after the caller-visible ponding representation has been overwritten because the original values are precisely the information being temporarily replaced.

Qualified owner:

`SCOPED_GHG_PONDING_PHASE_SNAPSHOT`

Persistent `ModelState` candidate:

`false`

## 2. CH4 oxidation: explicit nonlinear solver context

`CH4oxid` uses hidden local state across Task 1, repeated Task 2 and Task 3 calls. The qualified context family is:

- `Nlox`;
- `AmO2`;
- `AvCoCH4Old`;
- `OxDmndOmNit`;
- `R0CH4oxAct`.

Exact-source diagnostic unit SHA-256:

`43a77989e7d0e8bf3e1fa8370a009bb2334252c2965746ad4b7c6225e8889362`

A controlled two-layer case executed Task 1, clobbered automatic local storage, changed `AvCoCH4` to force a nonlinear update, then executed Task 2 and Task 3.

Original automatic-storage behaviour was not stable:

- O0 with signalling-NaN initialization terminated with `SIGSEGV` inside `CH4oxid`;
- O2 completed but Task 2 returned `FlConv=.TRUE.` without the intended update, demonstrating that lost hidden state can change solver control flow.

Original static O0/O2 execution produced the intended nonlinear continuation. Task 2 returned `FlConv=.FALSE.` and changed the two tested `RekiCH4` values from approximately `0.1157714861` and `0.0953816751` to `0.2185586733` and `0.3227639467`.

A diagnostic variant made the five hidden context families explicit. Under automatic storage at O0 and O2, its full Task 1 to Task 3 output is byte-identical to original static O0/O2 execution. All four output files have SHA-256:

`c01bba7b40652cbd38e1c3199a0e244db0f70cce6f08a0771c8741a18974e54c`

Diagnostic explicit-context source SHA-256:

`f1def7438038d332876abdbab889db05e0e1114114d4a52942e51e9b727fee73`

Representative final values in this controlled case are:

- Task-2 `RekiCH4(1)=0.21855867332941689`;
- Task-2 `RekiCH4(2)=0.32276394665203856`;
- Task-3 oxidation `QOxCH4(1)=3.9340561199295039e-4`;
- Task-3 oxidation `QOxCH4(2)=3.8731673598244634e-4`.

### Semantic decision

This family is nonlinear solver context, not accepted persistent state. `AvCoCH4Old` is genuine iteration history. Other members are fixed setup or active-domain context, but BUILDQ03 does not yet minimize the context by assuming they can be recomputed. The all-at-once explicit-context representation is the qualified equivalence surface for this probe.

Qualified owner:

`CH4_NONLINEAR_SOLVER_CONTEXT`

Persistent `ModelState` candidate:

`false`

## 3. N2O production/reduction: explicit coupled solver and correction context

`N2Oproreduc` retains top-level context across Task 1, Task 2 and Task 3:

- `AvCoN2Oold`;
- `AvCoNO3`;
- `FrDenAct_Pot`;
- `RatFacN2O`;
- `RekiNO3`;
- `FlInit`.

The nested `NO3N2OReduc` routine additionally retains:

- `FlExcd`;
- `QPrN2OdenMax`.

Exact-source diagnostic unit SHA-256:

`aa2b1b3ef84f78c0275310aaf76fbb1292f789c925a8f3c5fe6c8eb5c85d28aa`

A controlled one-layer case executed Task 1, clobbered automatic local storage, changed `AvCoN2O`, then executed Task 2 and Task 3.

Original automatic O0/O2 execution with initialization diagnostics diverged from original static execution:

- Task 2 reported `FlConv=.TRUE.` without the static-build update;
- Task 3 propagated NaN into `AvCoNO3`, `Rdfaox` and `RekiNO3`-related state in the controlled case.

Original static O0/O2 output SHA-256:

`ffb0c1fb1f7471ac9d50d214717ce1bcc520fdf2fbb5e91e223d3a5ec52f88b4`

A diagnostic explicit-context variant threaded both top-level and nested correction context through the call sequence. Under automatic O0/O2, its complete output is byte-identical to original static O0/O2 execution, with the same SHA-256 above.

Diagnostic explicit-context source SHA-256:

`ea1aafa987487f6a5aef323459ec5e864d6325f17bfb9a5ed5dc71e2783b7cab`

Representative controlled-case values:

- Task-2 `FlConv=.FALSE.`;
- Task-2 `QRdN2O=6.2659250871002596e-4`;
- Task-2 `RekiN2O=0.87026737320836933`;
- Task-3 `AvCoNO3=0.03`;
- Task-3 `Rdfaox=0.54556307768057388`;
- Task-3 `RekiNO3=-0.05`.

### Semantic decision

This is coupled nonlinear solver and correction history. `AvCoN2Oold`, `FlExcd` and `QPrN2OdenMax` are direct inter-iteration history. Other members are setup/coupling context and can be mutated during the nested correction path, so BUILDQ03 does not claim they are freely recomputable at each task invocation.

Qualified owner:

`N2O_NONLINEAR_SOLVER_AND_CORRECTION_CONTEXT`

Persistent `ModelState` candidate:

`false`

## 4. GHGasses phase context: reconstruction candidate, not yet runtime-qualified

Task 1 of `GHGasses` prepares hidden hydrology and air-flow projections such as `Floux`, `Mofrx`, `Mofrsax`, `Flaiib`, `Flaiio`, `Flaiou`, `Flair` and `FlaiAtmos`. A later separate Task-2 invocation consumes those values for final N2O calculations.

Source inspection shows that both top-level GHG calls receive the same hydrology argument families, while chemistry and nitrate processing occur between the calls. This makes deterministic phase-2 reprojection from explicit hydrology/macropore inputs plausible.

However, BUILDQ03 has not yet proven that all required inputs are invariant across the intervening call sequence or that recomputation is byte-equivalent to the retained Task-1 projection.

Current classification:

`RECONSTRUCTION_CANDIDATE_SOURCE_SUPPORTED_RUNTIME_UNQUALIFIED`

Do not replace this context by recomputation yet.

## 5. Shared GHG transport context: source-qualified, runtime equivalence open

`GHGtransport` retains `Ln1`, `FlTopUns` and `Co1Old` between Task 1 and Task 2. `Ln1=1-Flpn` is directly derivable. `FlTopUns` is derived from fixed hydrological conditions at Task 1. `Co1Old` is a pre-iteration concentration snapshot used to restore the original representation and must be treated as snapshot state unless equivalence of reconstruction is proven.

`GHGtranssub` prepares fixed Task-1 coefficient/help arrays including `P1`, `P2`, `Y1`, `Y2`, `Y3`, `Hv`, `Hv2`, `Hvnil` and top-unsaturated `AlfBu` coefficient families, then reuses them while `Reki` and `Reko` vary during Task 2.

Current owner candidates:

- `GHGtransport`: `GAS_TRANSPORT_BRANCH_AND_REPRESENTATION_SNAPSHOT_CONTEXT`;
- `GHGtranssub`: `FIXED_TIMESTEP_TRANSPORT_COEFFICIENT_CONTEXT`.

Runtime explicit-context equivalence is still open for these two families. No migration claim is made for them in this checkpoint.

## Qualification consequence

The current evidence is enough to reject three unsafe migration shortcuts:

1. retaining blanket static locals as the ANIMO5 state model;
2. moving all hidden GHG locals into persistent checkpoint state;
3. recomputing every hidden value at the consuming task without proving that the required pre-mutation or iteration-history information still exists.

For `GHGponding`, CH4 oxidation and N2O production/reduction, explicit scoped context reproduces the tested original static-local protocol under automatic GNU storage. That supports explicit-context architecture for those families while keeping TCD-011 and historical Intel equivalence open.

## Current gate

`PARTIAL_GHG_TCD011_EXPLICIT_CONTEXT_EQUIVALENCE_CONFIRMED_FOR_PONDING_CH4_N2O_TRANSPORT_CONTEXT_OPEN_HISTORICAL_INTEL_OPEN`

`new_canonical_tcd_requested=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
