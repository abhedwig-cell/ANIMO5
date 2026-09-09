# ANIMO-BUILDQ02 — TCD-011 MAPOHYDRO storage-duration qualification

Status: `QUALIFIED_MAPOHYDRO_EXPLICIT_TASK_CONTEXT_EQUIVALENCE_HISTORICAL_INTEL_OPEN`

## Question

BUILDQ01 proved that revision-53 `MAPOHYDRO` reads local scalar INTEGER `LnBoMpMx` in Task 4 after it was calculated in an earlier Task-1 invocation. The value has no explicit `SAVE`, is not a formal argument, and is not recomputed in Task 4. GNU automatic-storage variants can therefore change Task-4 behaviour.

B3I01 maps this phenomenon to existing canonical `TCD-011`, local storage duration. BUILDQ02 asks the narrower migration question: is the retained local actually a hidden physical state, or can its required semantics be represented deterministically from explicit task inputs?

## Source identity and call protocol

Frozen revision-53 source ZIP SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

`Hydro_detailed.for` calls `Mapohydro` four times during one hydrology timestep with `TaskMp=1,2,3,4`.

In `MAPOHYDRO.FOR`:

- Task 1 calculates `LnBoMp(1:2)` by inspecting wet macropore extent;
- Task 1 then assigns `LnBoMpMx = Max(LnBoMp(1),LnBoMp(2))`;
- Task 4 uses `LnBoMpMx` as the upper bound of the loop that removes temporary `FlMpOuSoTo` additions from `Flid`;
- Task 4 does not otherwise require information that is unique to the retained local because `LnBoMp(1:2)` remain explicit formal arguments.

Therefore the Task-4 value has the exact reconstruction identity:

`LnBoMpMx = Max(LnBoMp(1),LnBoMp(2))`

This is not a fitted replacement and does not introduce a new model degree of freedom.

## Controlled storage variants

The exact frozen subroutine was compiled with GNU Fortran 14.2.0 under the existing eight-byte-default-REAL diagnostic semantics. A four-case harness exercised wet, partially dry and fully dry macropore configurations. For active cases, the driver inserted the exact `FlMpOuSoTo` amounts into `Flid` before Task 4 and checked whether Task 4 removed them again.

The unmodified source under `-O0 -fno-automatic` removed the temporary terms as expected in all active cases.

The unmodified source under automatic storage did not have stable semantics:

- at `-O0 -fautomatic`, one active case retained `Flid=[1.30,1.12]` instead of `[1.00,1.00]`;
- at `-O2 -fautomatic`, the three active cases retained respectively `[1.30,1.12]`, `[1.14,1.00]` and `[1.04,1.06]`.

A temporary diagnostic copy that recomputed `LnBoMpMx` at Task 4 produced `[1.00,1.00]` in every active case under both automatic-storage optimization variants.

This isolates the Task-4 difference to hidden local lifetime. It is not evidence that any particular historical Intel build behaved like one GNU variant.

## 64-case full-task equivalence matrix

A separate 64-case matrix exercised Tasks 1, 2, 3 and 4 and deliberately stayed inside the original source's declared array domain. It varied:

- wet macropore extent;
- direct macropore precipitation and runon terms;
- positive and negative matrix/macropore interface fluxes;
- drainage terms;
- stored macropore water;
- timestep-level balance terms.

The captured output surface included topology, task-range state, public hydrology working state and warning text:

- `LnBoMp`;
- `LnTpMpSr`;
- `Nd`;
- `Badev`;
- `Flid`;
- `Flou`;
- `MpWfps`;
- `FlMpOuDrTo`;
- `Pr`;
- `FlMpHlp`;
- `SrWaMp`;
- `CoStat`.

The complete unfiltered 256-line output had SHA-256:

`16dc28adce374a956e77dc17420d814b64bf112ae3ff5524afe2422cb29433e3`

That hash was identical for all of the following:

- original source, `-O0 -fno-automatic`;
- original source, `-O2 -fno-automatic`;
- diagnostic explicit-context/bounds-ordered variant, `-O0 -fautomatic`;
- same diagnostic variant, `-O2 -fautomatic`;
- original source with bounds checking on the in-domain matrix;
- diagnostic variant with bounds checking;
- diagnostic variant with `-finit-real=snan` plus bounds checking at both O0 and O2.

No timestamp or text normalization was used.

## Semantic classification

`LnBoMpMx` is not accepted persistent physical state.

It is a deterministic projection of explicit Task-1 topology that remains available through the formal `LnBoMp` arguments. Its correct migration owner is therefore scoped macropore hydrology task context, or direct local recomputation where needed.

Qualified classification:

`DERIVABLE_TIMESTEP_TASK_CONTEXT_EXPLICIT_RECONSTRUCTION_EQUIVALENCE_SUPPORTED`

This result narrows TCD-011. It shows that at least this active state-material storage-duration dependency can be removed without adding checkpoint state and without preserving compiler-static lifetime as architecture.

It does not prove the same for every BUILDQ01 hidden-local family.

## Intel boundary

PREP01's Intel-default `/Qauto-scalar` explanation was plausible for `Outbal_write` CHARACTER scalars. `LnBoMpMx` is a scalar INTEGER and therefore demonstrates that this explanation cannot cover all active revision-53 cross-call state.

BUILDQ02 still has no direct historical Intel project file, command line or executable comparison. It therefore does not infer whether the legacy production executable retained `LnBoMpMx` because of `/Qsave`, another project setting, optimization/stack accident or a neighbouring source/build lineage.

Historical classification remains:

`HISTORICAL_INTEL_STORAGE_BEHAVIOR_UNKNOWN`

## TCD-011 consequence

TCD-011 remains OPEN. BUILDQ02 strengthens it in two ways:

1. storage duration is now demonstrated to be state-material in active macropore hydrology, not merely output-session material;
2. a compiler-independent semantic replacement for this specific hidden local is qualified as a migration candidate because it is exact, derivable and byte-equivalent over the declared in-domain matrix.

No blanket static-storage setting is admitted. No production correction is made.

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
