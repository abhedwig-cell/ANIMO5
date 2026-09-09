# ANIMO-BUILDQ01 — Hidden Runtime State Audit

Status: `QUALIFIED_POST_G5_FORTRAN_RUNTIME_SEMANTIC_HAZARD_AUDIT_PRODUCTION_BLOCKS_EXPLICIT`

## Scope and evidence basis

This workunit audits revision 53 runtime semantics without changing production physics or admitting corrected legacy behavior. It starts from post-G5 head `5c278152eacc33660f1c5870c7d419b8041b20a9` and cross-checks the following live evidence streams:

- PREP01/PREP05 evidence head `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`;
- GHG01 head `dac7b7b5c591b781b82ec968896edb5957664c88`;
- MP02 head `6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- SQ01 head `26d0c74aa440bd73c23709d313e24ea8af2a0bcd`;
- NQ02 current qualification head `40a41089020f78ee1d5181b8afc7bdb511af3193`;
- PREP03 interface audit as attached in G5.

Frozen local evidence was used only after B0 hash verification:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- diagnostic compiler: GNU Fortran 14.2.0.

The primary static scan excluded alternate units `input1_1.for` and `Outselorg.for`, matching PREP03 selection logic. A local scan saw 58 selected source compilation files, approximately 790 `CALL` statements to 92 distinct names, 19 computed-GOTO dispatch statements, 44 `DATA` statement starts, and only five explicit `SAVE ::` declaration lines. PREP03 independently counts 137 selected routines/functions and demonstrates that implicit, large mixed-semantic interfaces are systemic.

## Main result

The earlier statement that legacy ANIMO requires static local storage is too coarse. Revision 53 contains at least four semantically different lifetime classes:

1. **accepted physical/continuation state**, which must be explicit and restart-qualified;
2. **timestep transaction or phase context**, which may need to survive several calls but must not automatically enter a checkpoint;
3. **numerical iteration context**, which is algorithm history inside a timestep;
4. **diagnostic/session state**, such as output metadata and timers.

The strongest new result is that GHG and macropore code contain active, non-`SAVE` locals that are intentionally written in one call and read after return in another. Treating all of these as persistent `ModelState` would be wrong. Most are transaction or solver context, not physical storage.

## Confirmed active hidden-state families

| Family | Hidden continuation | Qualification | Correct semantic owner candidate |
|---|---|---|---|
| `Outbal_write` | task-1 format/separator strings reused by task 3 | PREP01 build-contract dependency | diagnostic output session |
| `GHGasses` | air-flow and temporary hydrology projection reused by task 2 | source-confirmed | GHG timestep context |
| `GHGponding` | original layer-0 representation stored while GHG temporarily rewrites ponding | GNU exact-source probe confirmed | scoped phase snapshot |
| `GHGtransport` | top-regime flag/index and fixed diffusion geometry reused during iterations | source-confirmed | gas transport solver context |
| `GHGtranssub` | fixed-step analytical coefficients reused during iterations | source-confirmed | gas transport solver context |
| CH4 oxidation | oxygen availability, old CH4 concentration and active depth reused across tasks | source-confirmed | CH4 nonlinear iteration context |
| `N2Oproreduc` | NO3/N2O coupled iteration arrays reused across tasks | source-confirmed | N2O nonlinear iteration context |
| `NO3N2OReduc` | `FlExcd` and `QPrN2OdenMax` correction history reused across calls | source-confirmed | nested N2O solver context |
| `MapoTransport` | phase flags and substance-specific macropore source arrays reused across dispatch | source-confirmed; active MP02 route | macropore process transaction context |
| `MPTRANSP` | iteration counters, flags, old concentrations, original source terms and balance context across Tasks 1/2/3 | source-confirmed; active MP02 route | macropore transport solver/transaction context |

`GHG_Miner` contains the same pattern but its calls in `resp_miner.for` are commented in frozen revision 53. It is therefore a dormant source hazard, not current active-route runtime evidence.

## Controlled storage-duration probe

The exact frozen `GHGponding` routine was extracted unchanged into a diagnostic harness. The harness calls task 1 followed by task 2 for a ponding layer with original values `He=0.25`, `Mofr=0.4`, `Mofro=0.3`, `Mofrsa=0.5`, `Mofrt=0.35`.

GNU 14.2 results:

- `-fautomatic`: task 2 restored garbage (`He≈4.58e-41`, `Mofr≈34.5`, other values zero in this run);
- `-O2 -fautomatic`: task 2 restored zeros;
- `-fautomatic -finit-real=snan`: task 2 restored NaNs;
- `-fno-automatic -finit-real=snan`: task 2 restored the original values exactly.

This probe proves a storage-duration dependency. It does **not** prove historical Intel behavior, and `-fno-automatic` is not a scientific fix. The same pattern is visible statically in the larger GHG task families.

## Index-0 and initialization findings

SQ01 already identified a separate source-static layer-0 gap. `Transca` assigns local `Reko(0)`/`Reki(0)` from `Recfpddior*(0)` and `Recfca(0)` and passes `Rhbd(0)` and `Socfdom(0)` into transport. `Rates` and `Inicalc` populate the audited corresponding arrays only for `1..Nl`. BUILDQ01 therefore retains this as `INDEX0_INITIALIZATION_GAP`, with runtime effect unqualified. Compiler zero-initialization is not a valid semantic contract.

GHG01 identifies a different layer-0 restart gap: total gas state `Cs(0)` can be serialized/read, while `Inicalc` reconstructs dissolved `Co` from `Cs` only for `1..Nl`. This is genuine restart-relevant physical phase state and must not be confused with transient GHG task locals.

## Explicit SAVE and DATA are not automatically defects

`Outsel` explicitly saves output metadata arrays and strings. `elapsedTime` explicitly saves its wallclock start. These are diagnostic/session state and are semantically distinct from model physics.

`DATA` initialization itself gives static lifetime by Fortran semantics. The selected scan found 44 DATA statement starts, predominantly constants or sentinels (`Zero`, `Small`, `One`, `ConvCrit`, etc.). No new active mutable scientific state was admitted merely because a local is DATA-initialized. Constants should become explicit constants, not fields in persistent state.

## Interfaces and aliasing

PREP01/PREP03 show that implicit interfaces are pervasive and that `-fallow-argument-mismatch` is part of the GNU diagnostic build recipe. A syntactic duplicate-actual scan found repeated actual objects in several calls. Inspected examples include `AvCo` passed to both `AvCo` and `CoTemp` in `MPTRANSP`, and `Con` passed to both `Ct` and `Ct0` in `Sorpfast`; those particular pairs are read as inputs and are not evidence of a harmful alias defect. The scan therefore does **not** admit an aliasing discrepancy. It also does not prove absence of overlapping subsection or definable-alias hazards. Explicit interfaces and owner contracts remain required before broad refactor.

## Evaluation order and exception-sensitive predicates

The confirmed MP02 `MPTRANSP` balance warning uses:

`Abs(BaDev) > 1e-5 .AND. Abs(BaDev/BaMx) > 0.005`

Fortran does not guarantee short-circuit evaluation. With `BaDev=BaMx=0`, the exact-expression GNU probe sets IEEE invalid even though the first conjunct is false. Under an invalid trap the program terminates. This is reconciled in `FLOATING_EXCEPTION_HAZARD_MATRIX.md`.

Static scanning found similar source-level risk in relative balance checks in `TRANSPORT`, `Transgen` and `GHGtransport`, and in nonlinear convergence/domain divisions in `Transorp`, `Transsub` and `NO3N2OReduc`. These are not promoted to defects without reachability/materiality evidence.

## Scientific-state decision rule

A hidden local is a candidate for persistent scientific state **only** if it represents information required to reproduce an accepted model boundary and cannot be reconstructed deterministically from canonical state, configuration and accepted forcing. By that rule:

- GHG task caches, ponding snapshots, CH4/N2O nonlinear iteration arrays and macropore iteration locals are **not** persistent scientific state candidates;
- GHG layer-0 gas phase state at restart **is** restart-relevant physical state;
- SQ01's possible dry-solute continuation state remains a scientific model-extension question under TCD-016, not a compiler-storage question;
- output strings, file mappings and timers are diagnostic state only.

## B3 impact

BUILDQ01 does not allocate new canonical TCD numbers. It provides routing evidence:

- GHG hidden task-state families block explicit GHG migration and must be reconciled with GHG01 restart/state work;
- macropore hidden task-state families block explicit MP migration and coexist with MP02's qualified active route and known conservation findings;
- the SQ01 layer-0 parameter/rate initialization gap remains runtime-effect unqualified and should enter B3 intake only if materiality is established;
- NQ02 nonlinear P policy remains TCD-019 scope unless independent runtime-semantic defect evidence is obtained;
- no compiler flag is admitted as a scientific correction.

The machine-readable row-level audit is `integration/animo-build/HIDDEN_STATE_REGISTER.csv`.

## Gate

`QUALIFIED_POST_G5_FORTRAN_RUNTIME_SEMANTIC_HAZARD_AUDIT_PRODUCTION_BLOCKS_EXPLICIT`

This closes the BUILDQ01 audit scope only. It does not admit production migration, corrected legacy behavior, or a compiler-specific runtime as canonical science.
