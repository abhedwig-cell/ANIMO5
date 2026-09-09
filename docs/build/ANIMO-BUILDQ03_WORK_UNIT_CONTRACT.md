# ANIMO-BUILDQ03 — GHG Explicit Task/Solver Context Qualification

Status: `STARTED_PERSISTED_BEFORE_EXTENDED_DIAGNOSTICS`

## Purpose

BUILDQ03 continues the TCD-011 runtime-semantic qualification after BUILDQ02. It focuses only on active GHG hidden cross-invocation task and solver context identified by GHG01 and BUILDQ01.

Canonical routing authority:

- `GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE` -> existing `TCD-011`;
- no new scientific TCD is requested by this workunit unless a separate physical or numerical discrepancy is independently established.

## Base and authority

Base branch/head:

`work/animo-buildq02-tcd011-storage-runtime-qualification@e7c675c6654026d5c12836f36f2fd347e9d547c2`

Canonical B3 routing authority:

`work/animo-b3i01-canonical-register-append@d2fe4eb3793a1ffc6c09197d7db01c3e3fe33f88`

GHG source-evidence authority:

`work/animo-ghg01-ghg-qualification@dac7b7b5c591b781b82ec968896edb5957664c88`

Frozen evidence identities:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Scope

Qualify the semantic owner and reconstructability of these active hidden-state families:

1. `GHGponding` restore snapshot;
2. `GHGasses` phase-1 to phase-2 hydrology/air-flow projection;
3. `GHGtransport` transport-branch context;
4. `GHGtranssub` fixed-step coefficient context;
5. CH4 oxidation task/iteration context;
6. `N2Oproreduc` task/iteration context;
7. nested `NO3N2OReduc` correction context.

`GHG_Miner` remains dormant in frozen revision 53 and is outside active-route qualification except as a future-activation hazard.

## Questions

For each family BUILDQ03 will determine:

- whether the retained value is accepted physical state, within-step transaction state, nonlinear solver history, or deterministically reconstructable derived context;
- whether a diagnostic explicit-context representation can reproduce the retained-value protocol under GNU without blanket static locals;
- which values must be snapshotted exactly because later reconstruction from mutated caller state would not be equivalent;
- which values can be recomputed from explicit arguments at the consuming task without introducing a new degree of freedom;
- whether the task protocol can be made fail-closed with explicit phase ownership;
- whether reentrancy or model-instance interleaving remains blocked after local externalization.

## Hard boundaries

- no frozen source or testbank mutation;
- diagnostic temporary source variants are evidence only;
- no blanket `SAVE`, `/Qsave` or `-fno-automatic` as semantic solution;
- no assumption that GNU behaviour equals historical Intel behaviour;
- no automatic promotion of solver or transaction context into persistent `ModelState`;
- no change to GHG governing equations, reaction rates, convergence policy, restart phase model or ledger semantics;
- no production migration or corrected-legacy admission.

## Planned evidence

At minimum:

- exact-source declaration/use audit for each family;
- controlled static versus automatic-storage probes where compilation can be isolated safely;
- explicit-context diagnostic variants for the narrowest families first;
- context owner/reconstruction matrix;
- phase-order and first-read contract;
- non-interference checks on unchanged in-domain calculations;
- B3 handoff preserving TCD-011 as open unless historical storage semantics and all active families are closed.

## Initial checkpoint

Local frozen source and testbank hashes were rechecked before extended diagnostics and match the identities above. GNU Fortran 14.2.0 is available.

`production_migration_admitted=false`

`corrected_legacy_admitted=false`

`new_canonical_tcd_requested=false`
