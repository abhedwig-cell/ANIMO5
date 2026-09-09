# ANIMO-BUILDQ03 — GHGasses deterministic reprojection supplement

Status: `SUPPLEMENTARY_DETERMINISTIC_REPROJECTION_EVIDENCE_EXPLICIT_PHASE_CONTEXT_REMAINS_QUALIFIED_BASELINE`

This document is a supplement to the stronger controlled cross-call qualification in:

`docs/build/GHGASSES_PHASE_CONTEXT_AND_BOTTOM_BOUNDARY_PROBE.md`

That qualification already establishes explicit seven-member `GHG_TIMESTEP_PHASE_CONTEXT` equivalence when the separate `Flair(Nl+1)` first-use hazard is controlled. This supplement asks a narrower follow-up question: can the same hydrology/air-flow projection be recomputed deterministically from invariant explicit inputs?

## Cross-call family

The hidden Task-1 to Task-2 family is:

- `Floux`;
- `Mofrx`;
- `Mofrsax`;
- `Flaiib`;
- `Flaiio`;
- `Flaiou`;
- `FlaiAtmos`.

`Flair` is Task-1 scratch, not cross-call state. `Mofrox` and `Mofrtx` are caller-visible formal arguments.

Qualified owner remains:

`GHG_TIMESTEP_PHASE_CONTEXT`

Persistent `ModelState` candidate remains `false`.

## 64-case reprojection probe

The additional diagnostic is persisted as:

`tools/buildq03/GHGASSES_PHASE_PROJECTION_PROBE.f90`

Source SHA-256:

`5d002a3bc969f36bf3e6fa0a48c66cb6e88f3f00fa9bf3c4c64ae9c72ed44bef`

The probe constructs the Task-1 ponding view, hydrology/macropore projection and air-flow outputs, clobbers automatic stack storage, and then independently reconstructs the projection from the same explicit inputs.

It covers 64 cases varying ponding, macropore activation and extent, storage, hydrology, fluxes, timestep length and shallow saturation topology.

GNU Fortran 14.2.0 results:

- `-O0 -fautomatic -finit-real=snan`: 64 cases pass;
- `-O2 -fautomatic -finit-real=snan`: 64 cases pass;
- both complete outputs are byte-identical;
- common SHA-256: `5a532e79df994fb29019d74ad7e5cbdf7dc1a73ea6e7c5743c0b810a591cfbe3`.

This strengthens the claim that the phase projection is deterministic under unchanged explicit inputs. It does not establish that every required input is invariant across the complete intervening legacy call graph between `GHGasses(1)` and `GHGasses(2)`.

## Design consequence

The conservative qualified migration representation remains explicit scoped phase context. Task-2 recomputation is a plausible later simplification, but it should only replace explicit threading after full-route input-invariance and equivalence evidence.

The separate `Flair(Nl+1)` conditional uninitialized boundary-slot finding is not solved or admitted by this reprojection probe. It remains a distinct runtime hazard requiring B3 disposition.

Canonical `TCD-011` remains open. Historical Intel storage behaviour remains unknown.

`new_canonical_tcd_requested=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
