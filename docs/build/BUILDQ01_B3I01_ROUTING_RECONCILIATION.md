# ANIMO-BUILDQ01 — B3I01 canonical routing reconciliation

Status: `RECONCILED_WITH_B3I01_CANONICAL_RUNTIME_ROUTING_NO_NEW_TCD`

This post-closeout note reconciles BUILDQ01 with the later ANIMO-B3I01 canonical intake. It does not change the BUILDQ01 runtime evidence, does not modify frozen source or testbank bytes, and does not admit a correction.

## Authority

Current BUILDQ01 evidence head before this reconciliation:

`e09d3a83467b736158c9a81523b05c3464eebbb3`

Authoritative B3I01 branch checked:

`work/animo-b3i01-canonical-register-append@d2fe4eb3793a1ffc6c09197d7db01c3e3fe33f88`

B3I01 supplement 01 consumed BUILDQ01 at:

`bf5c932753518c883d868c372c6c26bcdcacec68`

A live ancestry comparison shows the current BUILDQ01 evidence head is exactly two commits ahead of that consumed head and zero commits behind. Those two later commits only strengthened the BUILDQ01 register/status around the already identified MAPOHYDRO findings. They do not create a different phenomenon requiring re-intake.

## Canonical disposition of MAPOHYDRO findings

### `BUILDQ01-LCL-MAPOHYDRO-LNBOMPMX-CROSS-TASK-LIFETIME`

BUILDQ01 established that the unsaved scalar INTEGER `LnBoMpMx` is written during MAPOHYDRO Task 1 and read after procedure return during Task 4. Controlled GNU probes demonstrated both control-flow and state materiality under automatic-storage variants, while static-local storage retained the task protocol.

B3I01 routes this finding to existing canonical `TCD-011`, `local storage duration`.

Disposition:

`MAP_TO_EXISTING_TCD -> TCD-011`

Reason: this is the same build/storage-duration contract family. BUILDQ01 strengthens TCD-011 by showing that the family is not confined to diagnostic CHARACTER locals and can be state-material in active macropore hydrology. `LnBoMpMx` itself remains derivable timestep/task context, not persistent scientific state.

No new top-level TCD is allocated.

Qualification owner proposed by B3I01:

`ANIMO-BUILDQ02`

### `BUILDQ01-LCL-MAPOHYDRO-INDEX0-BOUNDS-ORDER`

BUILDQ01 established that the MAPOHYDRO wet-domain search can evaluate `FrHeWeMpWl` with second-dimension index zero before the lower-bound conjunct is evaluated. GNU bounds checking terminates on that read.

B3I01 disposition:

`BUILD_RUNTIME_HAZARD_NOT_TCD`

Reason: the evidence establishes an out-of-declared-domain language/runtime evaluation-order seam, but does not yet establish a distinct scientific-equation discrepancy or a qualified historical state/flux difference. It therefore remains separate from `TCD-025` and does not receive a canonical TCD number.

Qualification owner proposed by B3I01:

`ANIMO-BUILDQ02`

## Closed suspicion retained closed

BUILDQ01's earlier generic zero-scale balance-division suspicion for `TRANSPORT`, `Transgen` and `GHGtransport` was closed by full source control-flow reinspection. B3I01 correctly allocates no TCD to that closed suspicion.

## Consequence for BUILDQ01 status

The BUILDQ01 closeout gate remains:

`QUALIFIED_POST_G5_FORTRAN_RUNTIME_SEMANTIC_HAZARD_AUDIT_PRODUCTION_BLOCKS_EXPLICIT`

The earlier wording that the two MAPOHYDRO findings were still pending B3 intake is superseded by this reconciliation. Their canonical routing is now fixed as:

- `LnBoMpMx` cross-task lifetime: existing `TCD-011`;
- index-0 bounds/evaluation order: runtime hazard without TCD at current evidence strength.

This routing does not increase evidence strength, does not establish historical Intel behaviour, and does not authorize blanket `SAVE`, `/Qsave`, `-fno-automatic`, bounds disabling, source correction or production migration.

`new_canonical_tcd_allocated=false`

`corrected_legacy_admission=false`

`production_migration_admitted=false`
