# ANIMO-BUILDQ01 — Fortran Storage Duration Contract

Status: `QUALIFIED_STORAGE_DURATION_CONTRACT_FOR_MIGRATION_DESIGN_ONLY`

## Purpose

Revision 53 demonstrates that the legacy runtime sometimes uses procedure-local storage as an implicit communication channel between calls. ANIMO5 may preserve the **semantics** of such communication where it is qualified, but must not preserve the accidental storage mechanism.

## Contract

### 1. Accepted physical state is explicit

Any quantity required to reproduce an accepted timestep boundary must have an explicit owner, units, initialization rule and restart rule. It may not depend on compiler local-variable lifetime, stack reuse, zero initialization, COMMON layout accident, or a diagnostic build flag.

### 2. Transaction/phase context is explicit but normally not persistent

State that exists only between phases of one timestep or one event belongs to a scoped transaction context. Examples include the original layer-0 values temporarily saved by `GHGponding`, air-flow projections reused by `GHGasses`, and wrapper phase flags in `MapoTransport`.

Such context is checkpointed only if the architecture admits checkpoints inside that phase. The current accepted-boundary restart model does not justify moving these locals into persistent `ModelState` merely because legacy static storage kept them alive.

### 3. Numerical iteration context is explicit and ephemeral

Iteration counters, previous iterates, fixed-step analytical coefficients, convergence flags and correction history belong to solver context. Examples are `GHGtransport`, `GHGtranssub`, CH4 oxidation, `N2Oproreduc`, `NO3N2OReduc` and `MPTRANSP` locals.

If exact continuation after an interrupted nonlinear iteration is ever required, that is a separate checkpoint policy decision. It is not inferred from legacy static storage.

### 4. Diagnostic/session state is outside physical state

Output filenames, output-unit mappings, formatting strings, balance-writing session state and elapsed-time state are diagnostics. `Outsel` and `elapsedTime` use explicit `SAVE`; `Outbal_write` relies on hidden retention. ANIMO5 must keep such information out of physical conservation/restart state.

### 5. Constants are constants

A DATA-initialized local that is never semantically mutated should become an explicit constant with an explicit kind. DATA's implicit static lifetime is not a reason to allocate runtime model state.

### 6. Initialization is semantic, not compiler-provided

No read may rely on compiler zero fill, prior stack contents, debug initialization, or operating-system page state. Array index 0 receives an explicit initialization contract whenever index 0 is in the declared and reachable scientific domain.

The SQ01 `Transca` layer-0 parameter/rate gap and GHG01 layer-0 restart reconstruction gap are examples where this rule matters for different reasons.

### 7. SAVE is necessary only when the design actually requires procedure-static ownership

A production ANIMO5 process routine should normally not own mutable procedure-static state. If procedure-static state is retained for a compatibility adapter, it must be declared explicitly, isolated, documented, non-reentrant by contract, and covered by tests. That is an adapter exception, not the target architecture.

### 8. Compiler flags can qualify a legacy harness, not define science

`-fno-automatic`, default-real promotion, floating traps, or initialization flags may be used to expose or reproduce legacy behavior in diagnostics. They do not define intended ANIMO science and cannot substitute for explicit state, domain or numerical policy.

### 9. Historical Intel and GNU evidence remain separate

Known Intel compiler lineage and documented defaults are evidence, not proof of the historical project flags. GNU behavior under a compatibility recipe is also evidence, not a surrogate historical executable. A semantic claim must state which runtime/compiler evidence supports it.

### 10. Call sequence is part of the contract when results depend on it

For every multi-task routine, migration must specify legal phase order and which context is produced/consumed by each phase. An out-of-order call must fail closed or be impossible by type/API construction. Undefined local contents are not an error-handling mechanism.

### 11. Reentrancy and parallelism are blocked until hidden contexts are externalized

Active hidden local state means the affected routines cannot be assumed reentrant, thread-safe, column-parallel safe, or safe for interleaved model instances. This is a runtime architecture constraint even where current serial output happens to match.

### 12. Observer/diagnostic code may not become a hidden physical owner

Mass ledgers, warning counters and output caches can observe physical state and transfers, but may not become the only retained owner of physical continuation data.

### 13. Mixed explicit and accidental lifetime in one routine must be decomposed per variable

`Mapohydro` is the clearest counterexample to a blanket storage policy. It explicitly saves `FlMpInTo` and `FlMpOuTo` across Task 1 to Task 3, while the scalar INTEGER `LnBoMpMx` is also consumed across Task 1 to Task 4 but has no explicit `SAVE`. GNU probes show that automatic-storage variants can either terminate or skip the required Task-4 state reset, whereas static storage preserves the observed task protocol.

This does not justify adding `SAVE` to every local. It shows that the semantic contract must be reconstructed per variable. Where a retained value is deterministically derivable from already explicit context, recomputation or an explicit scoped context is preferable to checkpointing compiler-lifetime artifacts.

The distinction is also relevant to historical Intel reconstruction. PREP01's default `/Qauto-scalar` hypothesis can plausibly explain persistence of the CHARACTER locals used by `Outbal_write`, but does not by itself retain a non-SAVEd scalar INTEGER such as `LnBoMpMx`. Intel-default storage therefore cannot be treated as a complete explanation of revision-53 cross-call behavior.

### 14. Bounds checks must precede array access structurally

A logical `.AND.` must never be used as the only protection against an out-of-domain array subscript. `MAPOHYDRO.FOR` contains wet-domain search predicates that access second-dimension index zero before testing that the index is at least one. A bounds-checking GNU build traps. Future ANIMO5 code must sequence the bound test and the array access in separate control-flow steps. This is a runtime-language contract, not a scientific equation change.

## Migration classification test

For each legacy retained local ask, in order:

1. Is it needed at an accepted boundary? If yes, evaluate as persistent scientific or numerical continuation state.
2. Is it needed only between phases of the same timestep/event? If yes, transaction context.
3. Is it needed only for iterative solution history? If yes, solver context.
4. Is it only for output/timing/warnings? If yes, diagnostic session state.
5. Is it immutable? If yes, constant/configuration.
6. If none apply, treat it as an unqualified compiler accident until evidence establishes intended semantics.

No field enters canonical `ModelState` before this test and feature/restart qualification are complete.

## Admission boundary

This contract supports architecture and qualification work. It does not authorize rewriting the legacy source or choosing corrected production behavior.
