# ANIMO-BUILDQ02 — TCD-011 Storage-Duration Runtime Contract Qualification

Status: `STARTED_PERSISTED_BEFORE_EXTENDED_DIAGNOSTICS`

## Purpose

BUILDQ02 follows the canonical B3I01 routing of BUILDQ01 runtime findings. It does not reopen BUILDQ01 and does not allocate a new TCD.

Canonical target:

`TCD-011 — local storage duration`

B3I01 also assigns the MAPOHYDRO index-0 bounds/evaluation-order seam to BUILDQ02 as a runtime hazard without a scientific TCD at current evidence strength.

## Authority

Base branch/head:

`work/animo-buildq01-runtime-semantics@5e5c4c2bc678a11e87f358ac6163ba13409ee565`

Canonical B3 routing authority checked:

`work/animo-b3i01-canonical-register-append@d2fe4eb3793a1ffc6c09197d7db01c3e3fe33f88`

Relevant routing:

- `BUILDQ01-LCL-MAPOHYDRO-LNBOMPMX-CROSS-TASK-LIFETIME` -> existing `TCD-011`;
- `BUILDQ01-LCL-MAPOHYDRO-INDEX0-BOUNDS-ORDER` -> `BUILD_RUNTIME_HAZARD_NOT_TCD`.

Frozen evidence identities:

- revision-53 source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Questions

BUILDQ02 will determine narrowly:

1. whether the MAPOHYDRO Task-4 dependency on `LnBoMpMx` can be represented as explicitly reconstructable task context without relying on procedure-static lifetime;
2. whether that reconstruction is algebraically and diagnostically equivalent to the retained-value protocol where the original source stays inside its declared array domain;
3. whether automatic-storage variants demonstrably diverge because of lifetime rather than physical-state ownership;
4. whether structurally sequencing MAPOHYDRO lower-bound checks removes the confirmed out-of-domain read under bounds checking without altering in-domain results;
5. which remaining TCD-011 storage-duration families still require separate qualification before any runtime modernization.

## Hard boundaries

- no frozen source or testbank mutation;
- diagnostic temporary source variants are evidence probes only, never production corrections;
- no blanket `SAVE`, `/Qsave` or `-fno-automatic` is admitted as the semantic solution;
- no assumption that GNU behaviour equals historical Intel behaviour;
- no persistent `ModelState` allocation for a value that is deterministically reconstructable from explicit task inputs;
- no new TCD for the MAPOHYDRO bounds-order seam unless independent evidence establishes a distinct scientific state/flux discrepancy;
- no production migration or corrected-legacy admission.

## Planned evidence

At minimum:

- exact-source static versus automatic-storage probes;
- diagnostic explicit-context reconstruction under automatic storage at O0 and O2;
- multi-case in-domain equivalence matrix;
- dry/edge-domain bounds-check matrix;
- exact source-diff description for every diagnostic variant;
- B3 routing reconciliation and fail-closed status.

## Initial checkpoint

Before branch creation, the local frozen source and testbank hashes were rechecked and matched the identities above. GNU Fortran 14.2.0 is available.

A first four-case diagnostic already shows that an explicit Task-4 reconstruction

`LnBoMpMx = Max(LnBoMp(1),LnBoMp(2))`

restores the expected Task-4 `Flid` undo under both GNU `-O0 -fautomatic` and `-O2 -fautomatic`, while the unmodified automatic-storage source can leave the temporary additions in place. The same diagnostic variant with structurally ordered lower-bound checks completes dry-domain cases under `-fcheck=bounds`.

These are preliminary B1 diagnostic results. They are not yet a closeout claim and do not establish historical Intel behaviour.

`production_migration_admitted=false`

`corrected_legacy_admitted=false`

`new_canonical_tcd_allocated=false`
