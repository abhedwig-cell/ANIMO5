# ANIMO-BUILDQ03 — GHGasses phase-context qualification

Status: `QUALIFIED_SEMANTIC_OWNER_AND_DETERMINISTIC_PROJECTION_UNDER_INPUT_INVARIANCE_FULL_ROUTE_EQUIVALENCE_OPEN`

## Scope

This qualification addresses the last active GHG hidden cross-invocation family left open by BUILDQ03: the hydrology and air-flow projection prepared by `GHGasses` Task 1 and consumed by `GHGasses` Task 2.

Canonical routing remains:

`GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE -> TCD-011`

No new TCD is requested. This is B1 runtime-semantic evidence only. It does not establish historical Intel behaviour, corrected legacy behaviour, or production migration.

Frozen evidence identities:

- revision-53 source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- diagnostic compiler GNU Fortran 14.2.0.

## Source protocol

Revision-53 `Animo.for` calls `GHGasses(1,...)`, then performs the definitive nutrient/reaction/transport sequence, and later calls `GHGasses(2,...)` in the same timestep.

Inside `GHGasses`:

1. Task 1 invokes `GHGponding(1)` to construct the temporary ponding representation used for GHG calculations;
2. it projects hydrology into temporary gas-transport arrays, including macropore adjustment through `GHGMapohydro` when active;
3. it derives air-flow fluxes;
4. it calls methane and preliminary nitrous-oxide calculations;
5. it restores the ordinary ponding representation through `GHGponding(2)` and returns;
6. Task 2 later invokes `GHGponding(1)` again and passes the previously prepared projection into final `GHG_NitrousOxide(2,...)` before `GHGponding(3)` restores the ordinary representation.

The source therefore requires phase-1 information to survive a procedure return, but it does not explicitly own that information.

## Cross-call member minimization

The earlier GHG01/BUILDQ01 inventory included:

- `Floux`;
- `Mofrx`;
- `Mofrsax`;
- `Flaiib`;
- `Flaiio`;
- `Flaiou`;
- `Flair`;
- `FlaiAtmos`.

Full Task-2 use inspection narrows the true cross-call family to seven members:

- `Floux`;
- `Mofrx`;
- `Mofrsax`;
- `Flaiib`;
- `Flaiio`;
- `Flaiou`;
- `FlaiAtmos`.

`Flair` is Task-1 scratch. It is used to construct the positive in/out air-flow arrays and atmospheric influx but is not itself read by Task 2. It therefore does not need cross-phase lifetime.

`Mofrtx` is also consumed by Task 2, but it is already a formal output argument of `GHGasses` and therefore caller-visible rather than hidden local state. `Mofrox` is likewise a formal argument and is excluded from the hidden-local family.

## Semantic owner

The seven hidden values are a deterministic within-timestep projection of explicit hydrology, ponding and macropore inputs. They are not independently conserved physical stores and do not represent an accepted-boundary degree of freedom.

Qualified owner:

`GHG_TIMESTEP_PHASE_CONTEXT`

Persistent `ModelState` candidate:

`false`

Accepted-boundary restart relevance:

`false`

The context exists only between GHG phase 1 and phase 2 inside one timestep. A checkpoint at an accepted model boundary does not need to serialize it. A future implementation that supports checkpointing inside an unaccepted timestep would require a separate transaction-state policy and is outside this qualification.

## Input-invariance audit

The two top-level `GHGasses` calls receive the same hydrology/macropore argument families. Source inspection of the intervening direct top-level sequence in `Animo.for` and the directly inspected transport/reaction callees found no direct assignment to the hydrology coordinates from which this phase projection is constructed, including the relevant `Flib`, `Flio`, `Flou`, `He`, `Mofr`, `Mofro`, `Mofrsa`, `Mofrt`, macropore extent/storage inputs, and timestep length.

This is useful source evidence for phase-2 reconstruction, but it is deliberately not promoted to a complete transitive alias proof. Legacy implicit interfaces and possible deeper alias effects remain a reason to keep full-route equivalence open.

## 64-case deterministic projection probe

A controlled projection-only diagnostic is persisted as:

`tools/buildq03/GHGASSES_PHASE_PROJECTION_PROBE.f90`

Source SHA-256:

`5d002a3bc969f36bf3e6fa0a48c66cb6e88f3f00fa9bf3c4c64ae9c72ed44bef`

The probe reproduces the Task-1 ponding view, hydrology/macropore projection and air-flow equations needed to construct the seven cross-phase values. It then clobbers automatic stack storage and reconstructs the projection from the same explicit inputs.

The 64 cases vary, among other things:

- ponding active/inactive;
- macropores active/inactive;
- macropore layer extents and storage;
- water contents and layer geometry;
- vertical fluxes;
- timestep length;
- shallow saturation conditions that stop the air-flow domain.

For every case the independently reconstructed values are exactly equal for the captured projection surface. GNU O0 and O2 outputs are byte-identical, 64 lines each, with SHA-256:

`5a532e79df994fb29019d74ad7e5cbdf7dc1a73ea6e7c5743c0b810a591cfbe3`

Reproduction commands:

```text
gfortran -O0 -fautomatic -finit-real=snan tools/buildq03/GHGASSES_PHASE_PROJECTION_PROBE.f90 -o ghgasses_phase_O0.exe
gfortran -O2 -fautomatic -finit-real=snan tools/buildq03/GHGASSES_PHASE_PROJECTION_PROBE.f90 -o ghgasses_phase_O2.exe
./ghgasses_phase_O0.exe > O0.out
./ghgasses_phase_O2.exe > O2.out
sha256sum O0.out O2.out
```

## What this proves, and what it does not

Supported:

- the hidden GHGasses family has a scoped timestep-phase owner rather than a persistent physical-state owner;
- `Flair` can be removed from the cross-call context because it is Task-1-only scratch;
- the phase projection is deterministic from explicit inputs in the tested B1 envelope;
- recomputation after stack clobbering is stable across GNU O0/O2 for the projection equations;
- blanket static local storage is unnecessary as the semantic representation of this family.

Not yet supported:

- byte-equivalence of a complete original-static versus reconstructed-context `GHGasses(1)->intervening ANIMO sequence->GHGasses(2)` execution with active final N2O calculations;
- absence of all transitive alias-driven changes to projection inputs in the complete legacy call graph;
- historical Intel storage equivalence;
- a production choice between explicit phase snapshot and phase-2 recomputation.

The conservative migration baseline is therefore to represent the seven values as explicit scoped `GHG_TIMESTEP_PHASE_CONTEXT`. Deterministic phase-2 recomputation is a qualified design candidate only after a full-route equivalence probe demonstrates that the reconstruction inputs are unchanged at the consuming boundary.

## BUILDQ03 consequence

All active GHG hidden-local families now have a semantic owner classification. Controlled explicit-context runtime equivalence is already established for `GHGponding`, CH4 oxidation, N2O production/reduction, `GHGtransport` and `GHGtranssub`. `GHGasses` now has qualified semantic ownership and deterministic projection evidence, but its full-route runtime equivalence remains open.

TCD-011 therefore remains open.

Current local gate:

`GHG_TCD011_SEMANTIC_OWNERSHIP_QUALIFIED_FOR_ALL_ACTIVE_GHG_FAMILIES_RUNTIME_EQUIVALENCE_5_OF_6_GHGASSES_FULL_ROUTE_OPEN_HISTORICAL_INTEL_OPEN`

`new_canonical_tcd_requested=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
